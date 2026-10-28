"""Risk engine: the slice ladder, hard limits and the step-up rule. Pure rules plus a small SQLite state.

Nothing here talks to a market. Every order, paper or live, must pass `RiskEngine.allow_order` first, and the
engine halts itself on a loss limit and stays halted until a person resets it. It never raises its own slice:
stepping up needs the eligibility rule to pass AND an explicit confirmation.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone

SCHEMA = """
CREATE TABLE IF NOT EXISTS risk_state(key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS risk_events(
  id INTEGER PRIMARY KEY AUTOINCREMENT, ts INTEGER NOT NULL, mode TEXT NOT NULL, event TEXT NOT NULL, detail TEXT);
CREATE TABLE IF NOT EXISTS trades(
  id INTEGER PRIMARY KEY AUTOINCREMENT, ts INTEGER NOT NULL, mode TEXT NOT NULL, mint TEXT,
  slice_index INTEGER NOT NULL, size_gbp REAL NOT NULL, pnl_gbp REAL NOT NULL, pnl_pct REAL NOT NULL);
"""


def daily_limit_gbp(base_equity: float, r: dict) -> float:
    """Daily loss limit in pounds: the percentage rule, never above the pound cap."""
    return min(base_equity * r["daily_loss_limit_pct"] / 100, r.get("daily_loss_limit_gbp_max", float("inf")))


def limits_table(cfg: dict) -> list[dict]:
    """The slice table: the same numbers as the presentation, from the settings file."""
    r = cfg["risk"]
    lo, hi = r["illustrative_good_month_pct"]
    rlo, rhi = r["illustrative_first_months_range_pct"]
    rows = []
    for s in r["slice_steps"]:
        rows.append({
            "slice": s,
            "per_trade": s * r["position_pct"] / 100,
            "project_stop": s * r["project_stop_pct"] / 100,
            "daily_limit": daily_limit_gbp(s, r),
            "good_low": s * lo / 100, "good_high": s * hi / 100,
            "range_low": s * rlo / 100, "range_high": s * rhi / 100,
        })
    return rows


def position_size_gbp(equity: float, stop_pct: float, pool_liq_usd: float | None, r: dict) -> tuple[float, str]:
    """Smallest of three caps. Returns (size in pounds, name of the cap that bound)."""
    caps = {
        "position_pct": equity * r["position_pct"] / 100,
        "risk_per_trade": (equity * r["risk_per_trade_pct"] / 100) / (stop_pct / 100),
        "liquidity_cap": ((pool_liq_usd or 0.0) / r["usd_per_gbp"]) * r["max_pool_liquidity_pct"] / 100,
    }
    binding = min(caps, key=caps.get)
    return caps[binding], binding


@dataclass
class Decision:
    allowed: bool
    size_gbp: float = 0.0
    binding: str | None = None
    reasons: list[str] = field(default_factory=list)


def _utc_day(ts: int) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")


class RiskEngine:
    def __init__(self, db, cfg: dict, mode: str = "live", initial_equity: float | None = None, now: int | None = None):
        if mode not in ("paper", "live"):
            raise ValueError("mode must be 'paper' or 'live'")
        self.db, self.cfg, self.r, self.mode = db, cfg, cfg["risk"], mode
        db.conn.executescript(SCHEMA)
        self.key = f"state:{mode}"
        row = db.conn.execute("SELECT value FROM risk_state WHERE key=?", (self.key,)).fetchone()
        if row:
            self.s = json.loads(row["value"])
        else:
            now = now or int(time.time())
            start = float(initial_equity if initial_equity is not None else self.r["slice_steps"][0])
            self.s = {"slice_index": 0, "slice_start_equity": start, "slice_start_ts": now, "equity": start,
                      "day": _utc_day(now), "day_start_equity": start, "open_positions": 0, "halted": None}
            self._save()

    # ---- persistence -------------------------------------------------
    def _save(self) -> None:
        self.db.conn.execute("INSERT INTO risk_state(key, value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                             (self.key, json.dumps(self.s)))
        self.db.conn.commit()

    def _event(self, event: str, detail: str, now: int) -> None:
        self.db.conn.execute("INSERT INTO risk_events(ts, mode, event, detail) VALUES(?,?,?,?)", (now, self.mode, event, detail))
        self.db.conn.commit()

    def _roll_day(self, now: int) -> None:
        today = _utc_day(now)
        if today != self.s["day"]:
            self.s["day"], self.s["day_start_equity"] = today, self.s["equity"]
            self._save()

    # ---- the gate ------------------------------------------------------
    def allow_order(self, *, stop_pct: float | None = None, pool_liq_usd: float | None = None,
                    now: int | None = None) -> Decision:
        now = now or int(time.time())
        self._roll_day(now)
        if self.s["halted"]:
            return Decision(False, reasons=[f"HALTED:{self.s['halted']}"])
        if self.s["open_positions"] >= self.r["max_open_positions"]:
            return Decision(False, reasons=["POSITION_OPEN"])
        size, binding = position_size_gbp(self.s["equity"], stop_pct or self.r["default_stop_pct"], pool_liq_usd, self.r)
        if size < self.r["min_trade_gbp"]:
            return Decision(False, size, binding, [f"SIZE_TOO_SMALL:{binding}"])
        return Decision(True, round(size, 2), binding)

    def on_open(self) -> None:
        self.s["open_positions"] += 1
        self._save()

    def on_close(self, pnl_gbp: float, pnl_pct: float, *, size_gbp: float = 0.0, mint: str | None = None,
                 now: int | None = None) -> str | None:
        """Record a closed trade after costs. Returns a halt reason if this close triggered one."""
        now = now or int(time.time())
        self._roll_day(now)
        self.db.conn.execute(
            "INSERT INTO trades(ts, mode, mint, slice_index, size_gbp, pnl_gbp, pnl_pct) VALUES(?,?,?,?,?,?,?)",
            (now, self.mode, mint, self.s["slice_index"], size_gbp, pnl_gbp, pnl_pct))
        self.db.conn.commit()
        self.s["equity"] += pnl_gbp
        self.s["open_positions"] = max(0, self.s["open_positions"] - 1)
        reason = self._check_halts(now)
        self._save()
        return reason

    def _check_halts(self, now: int) -> str | None:
        if self.s["halted"]:
            return None
        eq = self.s["equity"]
        if eq <= self.s["slice_start_equity"] * (1 - self.r["project_stop_pct"] / 100):
            self.s["halted"] = "PROJECT_STOP"
        elif eq <= self.s["day_start_equity"] - daily_limit_gbp(self.s["day_start_equity"], self.r):
            self.s["halted"] = "DAILY_LOSS"
        if self.s["halted"]:
            self._event(self.s["halted"], f"equity {eq:.2f}", now)
        return self.s["halted"]

    def reset_halt(self, note: str, now: int | None = None) -> None:
        """Manual only. Logs who/why; the daily baseline restarts from the current equity."""
        now = now or int(time.time())
        self._event("HALT_RESET", f"{self.s['halted']} -> reset: {note}", now)
        self.s["halted"] = None
        self.s["day"], self.s["day_start_equity"] = _utc_day(now), self.s["equity"]
        self._save()

    # ---- step-up ---------------------------------------------------------
    def stepup_report(self, now: int | None = None) -> dict:
        now = now or int(time.time())
        steps, idx = self.r["slice_steps"], self.s["slice_index"]
        reasons: list[str] = []
        if idx >= len(steps) - 1:
            return {"eligible": False, "reasons": ["already at the top step"], "next_slice": None}
        live = self.db.conn.execute(
            "SELECT ts, pnl_pct FROM trades WHERE mode='live' AND slice_index=? ORDER BY ts", (idx,)).fetchall()
        paper = self.db.conn.execute("SELECT pnl_pct FROM trades WHERE mode='paper'").fetchall()
        weeks = ((now - live[0]["ts"]) / (7 * 86400)) if live else 0.0
        if weeks < self.r["stepup_min_live_weeks"]:
            reasons.append(f"only {weeks:.1f} live weeks at this slice (need {self.r['stepup_min_live_weeks']})")
        if len(live) < self.r["stepup_min_trades"]:
            reasons.append(f"only {len(live)} live trades (need {self.r['stepup_min_trades']})")
        touched = self.db.conn.execute(
            "SELECT 1 FROM risk_events WHERE mode='live' AND event='PROJECT_STOP' AND ts>=? LIMIT 1",
            (self.s["slice_start_ts"],)).fetchone()
        if touched or (self.mode == "live" and self.s["halted"]):
            reasons.append("the stop was touched or the desk is halted")
        if live and paper:
            lv = sum(x["pnl_pct"] for x in live) / len(live)
            pp = sum(x["pnl_pct"] for x in paper) / len(paper)
            if lv <= 0:
                reasons.append(f"live average trade is {lv:.2f}%, not positive")
            if lv < pp - self.r["stepup_match_tolerance_pct"]:
                reasons.append(f"live average {lv:.2f}% trails paper {pp:.2f}% by more than "
                               f"{self.r['stepup_match_tolerance_pct']} points")
        elif not paper:
            reasons.append("no paper trades to compare against")
        return {"eligible": not reasons, "reasons": reasons, "next_slice": steps[idx + 1]}

    def stepup(self, *, confirm: bool, equity_after_topup: float | None = None, now: int | None = None) -> dict:
        """Move up one step. Needs the rule to pass AND confirm=True (a person's decision)."""
        now = now or int(time.time())
        report = self.stepup_report(now)
        if not report["eligible"] or not confirm:
            return {**report, "applied": False}
        new = float(report["next_slice"])
        self.s.update({"slice_index": self.s["slice_index"] + 1, "slice_start_equity": new, "slice_start_ts": now,
                       "equity": float(equity_after_topup if equity_after_topup is not None else new),
                       "day": _utc_day(now)})
        self.s["day_start_equity"] = self.s["equity"]
        self._event("STEP_UP", f"new slice {new:.0f}", now)
        self._save()
        return {**report, "applied": True}
