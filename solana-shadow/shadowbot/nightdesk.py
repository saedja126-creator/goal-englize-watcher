"""Night Desk v1: a second, separate PAPER layer built from the rules in a Grok prompt.

Separate on purpose: its own settings (nightdesk.toml), its own database (data/nightdesk.db), its own pid and log.
It never imports or opens the scanner's database, and has no live mode: no wallet, no orders, no keys.
Agents as plain functions: scout -> filter -> analyst -> executor -> risk -> logger.
"""
from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
import time
import tomllib
from datetime import datetime, timezone
from pathlib import Path

from . import background, config
from .http import ApiError, Http, scrub
from .sources import fetch_pairs

GECKO_TRENDING = "https://api.geckoterminal.com/api/v2/networks/solana/trending_pools"
RUGCHECK_SUMMARY = "https://api.rugcheck.xyz/v1/tokens/{mint}/report/summary"
RUGCHECK_FULL = "https://api.rugcheck.xyz/v1/tokens/{mint}/report"

SCHEMA = """
CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT, ts INTEGER NOT NULL, mint TEXT, symbol TEXT,
  agent TEXT NOT NULL, decision TEXT NOT NULL, rule TEXT, detail TEXT);
CREATE INDEX IF NOT EXISTS ix_nd_events_ts ON events(ts);
CREATE TABLE IF NOT EXISTS seen(mint TEXT PRIMARY KEY, last_ts INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS trades(id INTEGER PRIMARY KEY AUTOINCREMENT, mint TEXT NOT NULL, symbol TEXT, entry_ts INTEGER NOT NULL,
  entry_raw REAL NOT NULL, entry_fill REAL NOT NULL, size_usd REAL NOT NULL, qty REAL NOT NULL, stop_price REAL NOT NULL,
  peak REAL NOT NULL, trail_active INTEGER NOT NULL DEFAULT 0, score REAL, status TEXT NOT NULL DEFAULT 'open',
  last_price REAL, last_price_ts INTEGER, exit_ts INTEGER, exit_raw REAL, exit_fill REAL, exit_reason TEXT,
  pnl_usd REAL, pnl_pct REAL);
CREATE TABLE IF NOT EXISTS equity(ts INTEGER NOT NULL, equity REAL NOT NULL, note TEXT);
CREATE TABLE IF NOT EXISTS bench(id INTEGER PRIMARY KEY AUTOINCREMENT, mint TEXT NOT NULL, symbol TEXT, eval_ts INTEGER NOT NULL,
  ref_price REAL, verdict TEXT NOT NULL, p15 REAL, p60 REAL, done15 INTEGER DEFAULT 0, done60 INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS scans(ts INTEGER NOT NULL, candidates INTEGER, scout_pass INTEGER, data_lag INTEGER, scout_kills TEXT);
CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT);
"""


def load_settings(path: Path | None = None) -> dict:
    with open(path or config.ROOT / "nightdesk.toml", "rb") as f:
        return tomllib.load(f)


def db_file() -> Path:
    return background.data_dir() / "nightdesk.db"


def pid_file() -> Path:
    return background.data_dir() / "nightdesk.pid"


def log_file() -> Path:
    return background.data_dir() / "nightdesk.log"


def say(msg: str) -> None:
    try:
        background.data_dir().mkdir(parents=True, exist_ok=True)
        lf = log_file()
        if lf.exists() and lf.stat().st_size > 2_000_000:
            os.replace(lf, lf.with_name("nightdesk.log.1"))
        with open(lf, "a", encoding="utf-8") as fh:
            fh.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
    except OSError:
        pass
    try:
        print(msg, flush=True)
    except (OSError, ValueError):
        pass


# ---------------------------------------------------------------- database ----
class DeskDB:
    def __init__(self, path: Path | str | None = None, start_equity: float = 150.0):
        p = Path(path) if path else db_file()
        if str(path) != ":memory:":
            p.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(":memory:" if str(path) == ":memory:" else str(p))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        if self.get_meta("start_equity") is None:
            self.set_meta("start_equity", str(start_equity))
            self.set_meta("started_ts", str(int(time.time())))
        self.conn.commit()

    def get_meta(self, key: str) -> str | None:
        r = self.conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return r["value"] if r else None

    def set_meta(self, key: str, value: str) -> None:
        self.conn.execute("INSERT INTO meta(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, value))
        self.conn.commit()

    def event(self, ts: int, agent: str, decision: str, mint: str | None = None, symbol: str | None = None,
              rule: str | None = None, detail: str | None = None) -> None:
        self.conn.execute("INSERT INTO events(ts,mint,symbol,agent,decision,rule,detail) VALUES(?,?,?,?,?,?,?)",
                          (ts, mint, symbol, agent, decision, rule, (detail or "")[:400]))
        self.conn.commit()

    def equity(self) -> float:
        start = float(self.get_meta("start_equity") or 0)
        pnl = self.conn.execute("SELECT COALESCE(SUM(pnl_usd),0) s FROM trades WHERE status='closed'").fetchone()["s"]
        return start + pnl

    def open_trade(self) -> sqlite3.Row | None:
        return self.conn.execute("SELECT * FROM trades WHERE status='open' ORDER BY id LIMIT 1").fetchone()

    def recently_seen(self, mint: str, now: int, minutes: float) -> bool:
        r = self.conn.execute("SELECT last_ts FROM seen WHERE mint=?", (mint,)).fetchone()
        return bool(r and now - r["last_ts"] < minutes * 60)

    def mark_seen(self, mint: str, now: int) -> None:
        self.conn.execute("INSERT INTO seen(mint,last_ts) VALUES(?,?) ON CONFLICT(mint) DO UPDATE SET last_ts=excluded.last_ts", (mint, now))
        self.conn.commit()

    def add_bench(self, now: int, mint: str, symbol: str | None, ref_price: float | None, verdict: str) -> int:
        cur = self.conn.execute("INSERT INTO bench(mint,symbol,eval_ts,ref_price,verdict) VALUES(?,?,?,?,?)", (mint, symbol, now, ref_price, verdict))
        self.conn.commit()
        return cur.lastrowid

    def set_bench_verdict(self, bench_id: int, verdict: str) -> None:
        self.conn.execute("UPDATE bench SET verdict=? WHERE id=?", (verdict, bench_id))
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()


# ------------------------------------------------------------------ helpers ----
def _f(x) -> float | None:
    try:
        return float(x) if x is not None else None
    except (TypeError, ValueError):
        return None


def parse_trending(payload: dict, now_ts: float) -> list[dict]:
    """GeckoTerminal trending pools -> candidate dicts. Missing values stay None (never guessed)."""
    out = []
    for p in (payload or {}).get("data") or []:
        a = p.get("attributes") or {}
        rel = p.get("relationships") or {}
        base = ((rel.get("base_token") or {}).get("data") or {}).get("id") or ""
        mint = base[7:] if base.startswith("solana_") else base
        if not mint:
            continue
        age = None
        created = a.get("pool_created_at")
        if created:
            try:
                age = (now_ts - datetime.fromisoformat(str(created).replace("Z", "+00:00")).timestamp()) / 60.0
            except ValueError:
                age = None
        tx = a.get("transactions") or {}
        vol = a.get("volume_usd") or {}
        pc = a.get("price_change_percentage") or {}
        out.append({
            "mint": mint, "pair": a.get("address"), "name": a.get("name"),
            "symbol": (a.get("name") or "").split(" / ")[0] or None,
            "dex": ((rel.get("dex") or {}).get("data") or {}).get("id"),
            "age_min": age, "price": _f(a.get("base_token_price_usd")),
            "mcap": _f(a.get("market_cap_usd")) or _f(a.get("fdv_usd")),
            "liq": _f(a.get("reserve_in_usd")), "vol_m5": _f(vol.get("m5")), "vol_h1": _f(vol.get("h1")),
            "pc_m5": _f(pc.get("m5")), "pc_h1": _f(pc.get("h1")),
            "buys_m5": (tx.get("m5") or {}).get("buys"), "sells_m5": (tx.get("m5") or {}).get("sells"),
            "buyers_m5": (tx.get("m5") or {}).get("buyers"), "buyers_h1": (tx.get("h1") or {}).get("buyers"),
        })
    return out


# -------------------------------------------------------------------- SCOUT ----
def scout(c: dict, cfg: dict) -> str | None:
    """Rule that rejects the candidate, or None if it passes. Rejects are counted, not logged one by one."""
    s = cfg["scout"]
    if c.get("dex") not in s["allowed_dex"]:
        return "SCOUT_DEX"
    if c.get("age_min") is None or c.get("mcap") is None or c.get("price") is None:
        return "SCOUT_DATA_MISSING"
    if not s["min_age_minutes"] <= c["age_min"] <= s["max_age_minutes"]:
        return "SCOUT_AGE"
    if c["mcap"] > s["sane_max_mcap_usd"]:
        return "SCOUT_DATA_MISSING"
    if not s["min_mcap_usd"] <= c["mcap"] <= s["max_mcap_usd"]:
        return "SCOUT_MCAP"
    return None


# ------------------------------------------------------------------- FILTER ----
def free_filters(c: dict, cfg: dict) -> tuple[str, str] | None:
    """Rules answerable from the trending data alone (checked first so RugCheck is only called when worth it)."""
    f = cfg["filter"]
    if c.get("liq") is None:
        return "DATA_MISSING:LIQUIDITY", "no liquidity figure"
    if c["liq"] < f["min_liquidity_usd"]:
        return "LIQUIDITY_LOW", f"liq ${c['liq']:,.0f} < ${f['min_liquidity_usd']:,.0f}"
    if c.get("vol_h1") is None:
        return "DATA_MISSING:VOLUME_1H", "no 1h volume figure"
    if c["vol_h1"] < f["min_volume_h1_usd"]:
        return "VOLUME_1H_LOW", f"1h volume ${c['vol_h1']:,.0f} < ${f['min_volume_h1_usd']:,.0f}"
    if c.get("pc_h1") is None:
        return "DATA_MISSING:PRICE_CHANGE_1H", "no 1h price change"
    if c["pc_h1"] >= f["max_pump_h1_pct"]:
        return "ALREADY_PUMPED_1H", f"+{c['pc_h1']:.0f}% in 1h"
    return None


def top10_pct(full: dict) -> float | None:
    holders = full.get("topHolders")
    if not holders:
        return None
    known = set((full.get("knownAccounts") or {}).keys())
    picked = [h for h in holders if h.get("address") not in known and h.get("owner") not in known]
    return sum(float(h.get("pct") or 0) for h in picked[:10])


def dev_pct(full: dict) -> float | None:
    supply = _f((full.get("token") or {}).get("supply"))
    bal = _f(full.get("creatorBalance"))
    if not supply or bal is None:
        return None
    return 100.0 * bal / supply


def insider_pct(full: dict) -> float | None:
    if "insiderNetworks" not in full:
        return None
    supply = _f((full.get("token") or {}).get("supply"))
    nets = full.get("insiderNetworks") or []
    if not nets:
        return 0.0
    if not supply:
        return None
    held = sum(float(n.get("currentHolding") or n.get("tokenAmount") or 0) for n in nets)
    return 100.0 * held / supply


def creator_rug_flag(full: dict) -> bool | None:
    risks = full.get("risks")
    if risks is None:
        return None
    return any("creator" in str(r.get("name", "")).lower() and "rug" in str(r.get("name", "")).lower() for r in risks)


def rug_filters(rc: dict, cfg: dict) -> tuple[str, str] | None:
    """Rules needing RugCheck. Any rule whose data is missing returns DATA_MISSING:<rule> (the prompt says skip)."""
    f = cfg["filter"]
    full, summary = rc.get("full"), rc.get("summary")
    if not full:
        return "DATA_MISSING:RUGCHECK", rc.get("error") or "no RugCheck report"
    if "mintAuthority" not in full or "freezeAuthority" not in full:
        return "DATA_MISSING:MINT_FREEZE_AUTHORITY", "fields absent"
    if full.get("mintAuthority") or full.get("freezeAuthority"):
        return "MINT_OR_FREEZE_AUTHORITY_NOT_REVOKED", f"mint={bool(full.get('mintAuthority'))} freeze={bool(full.get('freezeAuthority'))}"
    lp = _f((summary or {}).get("lpLockedPct"))
    if lp is None:
        return "DATA_MISSING:LP_LOCK", "no lpLockedPct"
    if lp < f["min_lp_locked_pct"]:
        return "LP_NOT_BURNED_OR_LOCKED", f"LP locked {lp:.0f}% < {f['min_lp_locked_pct']}%"
    t10 = top10_pct(full)
    if t10 is None:
        return "DATA_MISSING:TOP10_HOLDERS", "no holder list"
    if t10 > f["max_top10_pct"]:
        return "TOP10_HOLDERS_HIGH", f"top10 {t10:.1f}% > {f['max_top10_pct']}%"
    dv = dev_pct(full)
    if dv is None:
        return "DATA_MISSING:DEV_WALLET", "no creator balance"
    if dv > f["max_dev_pct"]:
        return "DEV_WALLET_HIGH", f"dev {dv:.1f}% > {f['max_dev_pct']}%"
    cr = creator_rug_flag(full)
    if cr is None:
        return "DATA_MISSING:DEPLOYER_HISTORY", "no risk list"
    if cr:
        return "DEPLOYER_RUG_HISTORY", "RugCheck flags the creator's rug history"
    ins = insider_pct(full)
    if ins is None:
        return "DATA_MISSING:BUNDLED_LAUNCH", "no insider data"
    if ins > f["max_bundled_pct"]:
        return "BUNDLED_LAUNCH_HIGH", f"insider networks hold {ins:.1f}% > {f['max_bundled_pct']}% (proxy)"
    return None


def fetch_rugcheck(http, mint: str, sleep=time.sleep) -> dict:
    out: dict = {"summary": None, "full": None, "error": None}
    try:
        out["summary"] = http.get("rugcheck", RUGCHECK_SUMMARY.format(mint=mint), label="rugcheck/summary")
        sleep(1.0)
        out["full"] = http.get("rugcheck", RUGCHECK_FULL.format(mint=mint), label="rugcheck/report")
    except ApiError as exc:
        out["error"] = f"{exc}"[:120]
    return out


# ------------------------------------------------------------------ ANALYST ----
def _clamp(x: float) -> float:
    return max(0.0, min(1.0, x))


def analyst_score(c: dict) -> tuple[float | None, dict]:
    """0 to 100. Formulas fixed in docs/NIGHT_DESK_V1_RULES.md. Equal weight over the inputs that are available."""
    comps: dict[str, float] = {}
    mom = []
    if c.get("pc_m5") is not None:
        mom.append(_clamp((c["pc_m5"] + 5.0) / 15.0))                         # -5% -> 0, +10% -> 1
    if c.get("vol_m5") is not None and c.get("vol_h1"):
        mom.append(_clamp((c["vol_m5"] * 12.0 / c["vol_h1"]) / 2.0))          # 5-min volume running at 2x the hourly pace -> 1
    if mom:
        comps["momentum"] = sum(mom) / len(mom)
    if c.get("buyers_m5") is not None and c.get("buyers_h1"):
        comps["buyers_growth"] = _clamp((c["buyers_m5"] / (c["buyers_h1"] / 12.0)) / 2.0)   # buyers at 2x the hourly pace -> 1
    b, s = c.get("buys_m5"), c.get("sells_m5")
    if isinstance(b, (int, float)) and isinstance(s, (int, float)) and b + s > 0:
        comps["buy_sell_ratio"] = _clamp((b / (b + s) - 0.4) / 0.3)           # 40% buys -> 0, 70% buys -> 1
    if c.get("liq") and c.get("mcap"):
        comps["liq_mcap"] = _clamp((c["liq"] / c["mcap"]) / 0.10)             # liquidity at 10% of market cap -> 1
    if not comps:
        return None, comps
    return 100.0 * sum(comps.values()) / len(comps), comps


# ----------------------------------------------------------- EXECUTOR / RISK ----
def open_position(db: DeskDB, cfg: dict, c: dict, entry_raw: float, score: float, now: int) -> int:
    d = cfg["desk"]
    slip = d["friction_pct"] / 2.0 / 100.0
    equity = db.equity()
    size = equity * d["position_pct_of_equity"] / 100.0
    fill = entry_raw * (1.0 + slip)
    stop = entry_raw * (1.0 - d["hard_stop_pct"] / 100.0)
    cur = db.conn.execute(
        "INSERT INTO trades(mint,symbol,entry_ts,entry_raw,entry_fill,size_usd,qty,stop_price,peak,score,last_price,last_price_ts) "
        "VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
        (c["mint"], c.get("symbol"), now, entry_raw, fill, size, size / fill, stop, entry_raw, score, entry_raw, now))
    db.conn.commit()
    return cur.lastrowid


def risk_check(trade: dict, price: float, cfg: dict) -> tuple[dict, str | None]:
    """Pure rule engine. Returns (updated fields, exit reason or None). The stop is never moved further away."""
    d = cfg["desk"]
    entry = trade["entry_raw"]
    peak = max(trade["peak"], price)
    stop = trade["stop_price"]
    trail = bool(trade["trail_active"])
    if not trail and peak >= entry * (1.0 + d["trail_activate_pct"] / 100.0):
        trail = True
    if trail:
        stop = max(stop, peak * (1.0 - d["trail_pct"] / 100.0))
    reason = None
    if price <= stop:
        reason = "TRAIL_STOP" if trail and stop > entry * (1.0 - d["hard_stop_pct"] / 100.0) else "HARD_STOP"
    return {"peak": peak, "stop_price": stop, "trail_active": int(trail)}, reason


def close_trade(db: DeskDB, cfg: dict, trade_id: int, exit_raw: float, reason: str, now: int) -> None:
    d = cfg["desk"]
    t = db.conn.execute("SELECT * FROM trades WHERE id=?", (trade_id,)).fetchone()
    slip = d["friction_pct"] / 2.0 / 100.0
    fill = exit_raw * (1.0 - slip) if exit_raw > 0 else 0.0
    pnl = t["qty"] * fill - t["size_usd"]
    db.conn.execute("UPDATE trades SET status='closed', exit_ts=?, exit_raw=?, exit_fill=?, exit_reason=?, pnl_usd=?, pnl_pct=? WHERE id=?",
                    (now, exit_raw, fill, reason, pnl, 100.0 * pnl / t["size_usd"], trade_id))
    db.conn.commit()
    db.conn.execute("INSERT INTO equity(ts,equity,note) VALUES(?,?,?)", (now, db.equity(), f"close {t['symbol']} {reason}"))
    db.conn.commit()
    db.event(now, "RISK", "CLOSE", t["mint"], t["symbol"], reason, f"pnl ${pnl:+.2f} ({100.0 * pnl / t['size_usd']:+.1f}%)")


def _pair_price(pair: dict | None) -> float | None:
    return _f((pair or {}).get("priceUsd"))


def track_position(http, db: DeskDB, cfg: dict, now: int) -> str:
    """RISK agent: one price check for the open position (DexScreener), apply the stops, close if hit."""
    t = db.open_trade()
    if not t:
        return "idle"
    try:
        pair = fetch_pairs(http, [t["mint"]]).get(t["mint"])
    except ApiError:
        pair = None
    price = _pair_price(pair)
    if price is None:
        if now - (t["last_price_ts"] or t["entry_ts"]) >= cfg["desk"]["data_lost_minutes"] * 60:
            close_trade(db, cfg, t["id"], 0.0, "DATA_LOST", now)
            return "closed DATA_LOST"
        return "no price (waiting)"
    fields, reason = risk_check(dict(t), price, cfg)
    db.conn.execute("UPDATE trades SET peak=?, stop_price=?, trail_active=?, last_price=?, last_price_ts=? WHERE id=?",
                    (fields["peak"], fields["stop_price"], fields["trail_active"], price, now, t["id"]))
    db.conn.commit()
    if reason:
        close_trade(db, cfg, t["id"], price, reason, now)
        return f"closed {reason}"
    return "holding"


# ------------------------------------------------------------------- CYCLE ----
def discover(http, cfg: dict, now: float) -> tuple[list[dict], int]:
    """SCOUT: trending pools from the free source. Returns (candidates by mint, number of failed calls)."""
    seen: dict[str, dict] = {}
    lag = 0
    for dur in cfg["scout"]["trending_durations"]:
        try:
            payload = http.get("gecko", GECKO_TRENDING, params={"include": "base_token", "duration": dur}, label="trending_pools")
        except ApiError:
            lag += 1
            continue
        for c in parse_trending(payload, now):
            seen.setdefault(c["mint"], c)
    return list(seen.values()), lag


def run_cycle(http, db: DeskDB, cfg: dict, now: int | None = None, sleep=time.sleep) -> dict:
    now = int(now if now is not None else time.time())
    cands, lag = discover(http, cfg, now)
    stats = {"candidates": len(cands), "scout_pass": 0, "data_lag": lag, "killed": 0, "skipped": 0, "scored_low": 0,
             "traded": 0, "rugcheck_calls": 0, "scout_kills": {}}
    if lag and not cands:
        db.event(now, "SCOUT", "SKIP", rule="DATA_LAG", detail=f"{lag} trending call(s) failed, nothing to judge this cycle")
    budget = cfg["loop"]["rugcheck_per_cycle"]
    for c in cands:
        rule = scout(c, cfg)
        if rule:
            stats["scout_kills"][rule] = stats["scout_kills"].get(rule, 0) + 1
            continue
        if db.recently_seen(c["mint"], now, cfg["loop"]["reeval_minutes"]):
            stats["scout_kills"]["COOLDOWN"] = stats["scout_kills"].get("COOLDOWN", 0) + 1
            continue
        stats["scout_pass"] += 1
        sym = c.get("symbol")
        db.event(now, "SCOUT", "PASS", c["mint"], sym, detail=f"{c['dex']} age {c['age_min']:.0f}m mcap ${c['mcap']:,.0f} liq ${c['liq'] or 0:,.0f}")
        bid = db.add_bench(now, c["mint"], sym, c.get("price"), "PENDING")
        kill = free_filters(c, cfg)
        rc = None
        if not kill:
            if budget <= 0:
                stats["skipped"] += 1
                db.event(now, "FILTER", "SKIP", c["mint"], sym, "DATA_MISSING:RUGCHECK_BUDGET", "RugCheck budget used up this cycle, will retry later")
                db.set_bench_verdict(bid, "SKIP:RUGCHECK_BUDGET")
                continue
            budget -= 1
            stats["rugcheck_calls"] += 2
            rc = fetch_rugcheck(http, c["mint"], sleep=sleep)
            kill = rug_filters(rc, cfg)
        db.mark_seen(c["mint"], now)
        if kill:
            rule_name, detail = kill
            if rule_name.startswith("DATA_MISSING"):
                stats["skipped"] += 1
                db.event(now, "FILTER", "SKIP", c["mint"], sym, rule_name, detail)
                db.set_bench_verdict(bid, "SKIP:" + rule_name.split(":", 1)[1])
            else:
                stats["killed"] += 1
                db.event(now, "FILTER", "KILL", c["mint"], sym, rule_name, detail)
                db.set_bench_verdict(bid, "KILLED:" + rule_name)
            continue
        db.event(now, "FILTER", "SURVIVE", c["mint"], sym, detail="passed every hard rule")
        score, comps = analyst_score(c)
        if score is None or len(comps) < cfg["analyst"]["min_components"]:
            stats["skipped"] += 1
            db.event(now, "ANALYST", "SKIP", c["mint"], sym, "DATA_MISSING:ANALYST_INPUT", f"only {len(comps)} scoring inputs")
            db.set_bench_verdict(bid, "SKIP:ANALYST_INPUT")
            continue
        detail = "score %.0f (%s)" % (score, ", ".join(f"{k} {v:.2f}" for k, v in comps.items()))
        if score < cfg["analyst"]["pass_score"]:
            stats["scored_low"] += 1
            db.event(now, "ANALYST", "KILL", c["mint"], sym, "SCORE_BELOW_70", detail)
            db.set_bench_verdict(bid, "LOW_SCORE")
            continue
        db.event(now, "ANALYST", "PASS", c["mint"], sym, detail=detail)
        if db.open_trade():
            db.event(now, "EXECUTOR", "SKIP", c["mint"], sym, "POSITION_OPEN", "one position at a time")
            db.set_bench_verdict(bid, "SCORED_PASS_BUSY")
            continue
        try:
            pair = fetch_pairs(http, [c["mint"]]).get(c["mint"])
        except ApiError:
            pair = None
        entry = _pair_price(pair)
        if entry is None:
            stats["skipped"] += 1
            db.event(now, "EXECUTOR", "SKIP", c["mint"], sym, "DATA_MISSING:ENTRY_PRICE", "no DexScreener price")
            db.set_bench_verdict(bid, "SKIP:ENTRY_PRICE")
            continue
        tid = open_position(db, cfg, c, entry, score, now)
        t = db.conn.execute("SELECT * FROM trades WHERE id=?", (tid,)).fetchone()
        db.event(now, "EXECUTOR", "ENTER", c["mint"], sym, detail=f"PAPER buy ${t['size_usd']:.2f} at {entry:.8g} (fill {t['entry_fill']:.8g}), stop {t['stop_price']:.8g}, {detail}")
        db.set_bench_verdict(bid, "TRADED")
        stats["traded"] += 1
    db.conn.execute("INSERT INTO scans(ts,candidates,scout_pass,data_lag,scout_kills) VALUES(?,?,?,?,?)",
                    (now, stats["candidates"], stats["scout_pass"], lag, json.dumps(stats["scout_kills"])))
    db.conn.commit()
    return stats


def settle_bench(http, db: DeskDB, cfg: dict, now: int) -> int:
    """Benchmark: price of every judged token 15 minutes and 1 hour later, so we can tell if the desk adds anything."""
    o15, o60 = cfg["loop"]["bench_offsets_seconds"]
    rows = db.conn.execute(
        "SELECT * FROM bench WHERE (done15=0 AND eval_ts+?<=?) OR (done60=0 AND eval_ts+?<=?) LIMIT 60", (o15, now, o60, now)).fetchall()
    if not rows:
        return 0
    mints = sorted({r["mint"] for r in rows})
    prices: dict[str, float | None] = {}
    try:
        for m, p in fetch_pairs(http, mints).items():
            prices[m] = _pair_price(p)
    except ApiError:
        return 0
    n = 0
    for r in rows:
        px = prices.get(r["mint"])
        if not r["done15"] and r["eval_ts"] + o15 <= now:
            db.conn.execute("UPDATE bench SET p15=?, done15=1 WHERE id=?", (px, r["id"])); n += 1
        if not r["done60"] and r["eval_ts"] + o60 <= now:
            db.conn.execute("UPDATE bench SET p60=?, done60=1 WHERE id=?", (px, r["id"])); n += 1
    db.conn.commit()
    return n


# ------------------------------------------------------------ DASHBOARD ----
def _rows(db: DeskDB, sql: str, *a):
    return db.conn.execute(sql, a).fetchall()


def kill_stats(db: DeskDB, since: int = 0) -> list[tuple[str, int]]:
    rs = _rows(db, "SELECT rule, COUNT(*) n FROM events WHERE decision IN ('KILL','SKIP') AND ts>=? GROUP BY rule ORDER BY n DESC", since)
    return [(r["rule"] or "?", r["n"]) for r in rs]


def build_status(db: DeskDB, cfg: dict, now: int | None = None) -> str:
    now = int(now if now is not None else time.time())
    d = cfg["desk"]
    eq = db.equity()
    start = float(db.get_meta("start_equity") or d["start_equity_usd"])
    closed = _rows(db, "SELECT * FROM trades WHERE status='closed'")
    wins = sum(1 for t in closed if t["pnl_usd"] > 0)
    last_scan = db.conn.execute("SELECT * FROM scans ORDER BY ts DESC LIMIT 1").fetchone()
    tot = db.conn.execute("SELECT COALESCE(SUM(candidates),0) c, COALESCE(SUM(scout_pass),0) p FROM scans").fetchone()
    L = [f"# {d['name']}: PAPER ONLY (no wallet, no orders)", f"_Updated {datetime.fromtimestamp(now, timezone.utc):%Y-%m-%d %H:%M:%S} UTC_", ""]
    L += [f"**Equity ${eq:,.2f}** ({100.0 * (eq - start) / start:+.2f}% from ${start:,.0f} start). Closed trades {len(closed)}: {wins} wins, {len(closed) - wins} losses.", ""]
    ago = (now - last_scan["ts"]) if last_scan else None
    L += ["| Agent | Status |", "|---|---|",
          f"| SCOUT | {'last scan %ds ago: %d candidates, %d passed' % (ago, last_scan['candidates'], last_scan['scout_pass']) if last_scan else 'no scan yet'} (total scanned {tot['c']}, passed {tot['p']}) |"]
    for agent, label in (("FILTER", "last decision"), ("ANALYST", "last decision"), ("EXECUTOR", "last decision")):
        e = db.conn.execute("SELECT * FROM events WHERE agent=? ORDER BY id DESC LIMIT 1", (agent,)).fetchone()
        L.append(f"| {agent} | {('%s %s %s' % (e['decision'], e['symbol'] or '', e['rule'] or '')).strip() if e else 'nothing yet'} |")
    t = db.open_trade()
    L.append(f"| RISK | {'holding %s, stop %.8g, trail %s' % (t['symbol'], t['stop_price'], 'ON' if t['trail_active'] else 'off') if t else 'no open position'} |")
    L.append(f"| LOGGER | {db.conn.execute('SELECT COUNT(*) c FROM events').fetchone()['c']} decisions logged |")
    L += ["", "## Open position"]
    if t:
        L.append(f"{t['symbol']}: paper ${t['size_usd']:.2f} bought {int(now - t['entry_ts'])}s ago at {t['entry_raw']:.8g}, last {t['last_price']:.8g} ({100.0 * (t['last_price'] / t['entry_raw'] - 1):+.1f}%), score {t['score']:.0f}.")
    else:
        L.append("None.")
    L += ["", "## Latest kills and skips (newest first)", "| Time | Token | Agent | Rule | Detail |", "|---|---|---|---|---|"]
    for e in _rows(db, "SELECT * FROM events WHERE decision IN ('KILL','SKIP') ORDER BY id DESC LIMIT 10"):
        L.append(f"| {datetime.fromtimestamp(e['ts'], timezone.utc):%H:%M:%S} | {e['symbol'] or '-'} | {e['agent']} | {e['rule']} | {e['detail']} |")
    L += ["", "## Kill and skip statistics by rule", "| Rule | Count |", "|---|---|"]
    L += [f"| {r} | {n} |" for r, n in kill_stats(db)] or ["| none yet | 0 |"]
    return "\n".join(L) + "\n"


def _avg(xs):
    xs = [x for x in xs if x is not None]
    return (sum(xs) / len(xs)) if xs else None


def build_report(db: DeskDB, cfg: dict, now: int | None = None) -> str:
    now = int(now if now is not None else time.time())
    L = [build_status(db, cfg, now), "## Closed trades", "| Token | Entry | Exit reason | Result | Score |", "|---|---|---|---|---|"]
    for t in _rows(db, "SELECT * FROM trades WHERE status='closed' ORDER BY id"):
        L.append(f"| {t['symbol']} | {datetime.fromtimestamp(t['entry_ts'], timezone.utc):%m-%d %H:%M} | {t['exit_reason']} | {t['pnl_pct']:+.1f}% (${t['pnl_usd']:+.2f}) | {t['score']:.0f} |")
    if not _rows(db, "SELECT 1 FROM trades WHERE status='closed' LIMIT 1"):
        L.append("| none yet | | | | |")
    L += ["", "## Benchmark: what judged tokens did next (raw price change, before costs)",
          "Compares the desk's choices with every other token it looked at. If TRADED and SCORED are not better than KILLED, the rules add nothing.", "",
          "| Group | Tokens | Avg change after 15 min | Avg change after 1 h |", "|---|---|---|---|"]
    groups: dict[str, list] = {}
    for b in _rows(db, "SELECT * FROM bench WHERE verdict != 'PENDING'"):
        key = b["verdict"].split(":")[0]
        groups.setdefault(key, []).append(b)
    for key in sorted(groups):
        rs = groups[key]
        ch = lambda col: _avg([100.0 * (r[col] / r["ref_price"] - 1) for r in rs if r[col] and r["ref_price"]])
        a, b2 = ch("p15"), ch("p60")
        L.append(f"| {key} | {len(rs)} | {'n/a' if a is None else '%+.1f%%' % a} | {'n/a' if b2 is None else '%+.1f%%' % b2} |")
    L += ["", "## What this does NOT prove",
          "- Paper results assume fills at the observed price plus the assumed friction. Real fills on thin tokens are usually worse, and stops can jump past their price.",
          "- A handful of trades says nothing. About 100 trades and a benchmark that beats the killed group would be needed.",
          "- Several rules use proxies (see docs/NIGHT_DESK_V1_RULES.md). Holder growth and smart-wallet activity are not in the score."]
    return "\n".join(L) + "\n"


def write_status(db: DeskDB, cfg: dict) -> Path:
    config.REPORTS_DIR.mkdir(exist_ok=True)
    p = config.REPORTS_DIR / "nightdesk-status.md"
    p.write_text(build_status(db, cfg), encoding="utf-8")
    return p


# ---------------------------------------------------------------- RUNNING ----
def watch(once: bool = False, db: DeskDB | None = None, http=None, cfg: dict | None = None) -> int:
    cfg = cfg or load_settings()
    own_db = db is None
    db = db or DeskDB(start_equity=cfg["desk"]["start_equity_usd"])
    http = http or Http(None)
    if not once:
        cur = _read_pid()
        if cur and cur != os.getpid() and background.is_alive(cur):
            say(f"Night Desk already running (pid {cur}).")
            return 3
        background.data_dir().mkdir(parents=True, exist_ok=True)
        pid_file().write_text(str(os.getpid()))
    say(f"{cfg['desk']['name']}: PAPER ONLY. No wallet, no orders. Ctrl+C to stop.")
    last_disc = 0.0
    try:
        while True:
            now = int(time.time())
            if now - last_disc >= cfg["loop"]["discovery_seconds"] or once:
                try:
                    s = run_cycle(http, db, cfg, now)
                    say("cycle: %d candidates, %d passed scout, %d killed, %d skipped, %d traded" % (s["candidates"], s["scout_pass"], s["killed"], s["skipped"], s["traded"]))
                except Exception as exc:  # one bad cycle must not stop the desk overnight
                    db.event(now, "SCOUT", "SKIP", rule="CYCLE_ERROR", detail=scrub(str(exc)))
                    say("cycle error: " + scrub(str(exc))[:150])
                last_disc = now
            try:
                state = track_position(http, db, cfg, now)
                settle_bench(http, db, cfg, now)
            except Exception as exc:
                state = "tracking error"
                say("tracking error: " + scrub(str(exc))[:150])
            write_status(db, cfg)
            if once:
                say("risk: " + state)
                return 0
            time.sleep(cfg["loop"]["iteration_seconds"])
    except KeyboardInterrupt:
        say("Night Desk stopped.")
        return 0
    finally:
        if not once and _read_pid() == os.getpid():
            try:
                pid_file().unlink()
            except OSError:
                pass
        if own_db:
            db.close()


def _read_pid() -> int | None:
    try:
        return int(pid_file().read_text().strip())
    except (OSError, ValueError):
        return None


def start() -> tuple[bool, str]:
    pid = _read_pid()
    if pid and background.is_alive(pid):
        return False, f"Night Desk already running in the background (pid {pid})."
    background.data_dir().mkdir(parents=True, exist_ok=True)
    kw: dict = {}
    if os.name == "nt":
        kw["creationflags"] = subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        kw["start_new_session"] = True
    with open(background.data_dir() / "nightdesk.err", "ab") as err:
        proc = subprocess.Popen([sys.executable, "-m", "shadowbot", "nightdesk", "watch"], cwd=str(config.ROOT),
                                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=err, close_fds=True, **kw)
    for _ in range(60):
        time.sleep(0.25)
        if proc.poll() is not None:
            return False, "Night Desk stopped straight away. Look at data/nightdesk.err."
        if _read_pid() == proc.pid:
            return True, f"Night Desk started in the background (pid {proc.pid}). Paper only."
    return False, "Night Desk did not report in. Run `python -m shadowbot nightdesk status`."


def stop() -> tuple[bool, str]:
    pid = _read_pid()
    if not pid or not background.is_alive(pid):
        try:
            pid_file().unlink()
        except OSError:
            pass
        return False, "No Night Desk is running."
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True,
                       creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        import signal
        os.kill(pid, signal.SIGTERM)
    for _ in range(40):
        if not background.is_alive(pid):
            break
        time.sleep(0.25)
    try:
        pid_file().unlink()
    except OSError:
        pass
    return (not background.is_alive(pid)), (f"Stopped (pid {pid})." if not background.is_alive(pid) else f"Could not stop pid {pid}.")
