"""One-off coverage check: how many new tokens does a second free source list that our scanner never saw?

Second source: Jupiter's free "recent tokens" list (lite-api.jup.ag/tokens/v2/recent, 30 newest tokens per call, no key).
It is a second opinion, not ground truth: it only lists tokens Jupiter has indexed.

Read-only against the scanner's database (opened with mode=ro) and Http(None) so nothing is written to shadow.db.
Its own notes go to data/compare_jupiter.jsonl; the finished report to reports/compare-<time>.md.
"""
from __future__ import annotations

import json
import sqlite3
import statistics as st
import time
from datetime import datetime, timezone
from pathlib import Path

from . import background, config
from .http import ApiError
from .sources import fetch_pairs

JUP_RECENT = "https://lite-api.jup.ag/tokens/v2/recent"
GRACE_SECONDS = 15 * 60       # a token must have been listed this long ago before a miss is counted
LATE_SECONDS = 10 * 60        # "caught late" = our first sighting came more than this after Jupiter listed it


def data_file() -> Path:
    return background.data_dir() / "compare_jupiter.jsonl"


def _iso_ts(text) -> int | None:
    try:
        return int(datetime.fromisoformat(str(text).replace("Z", "+00:00")).timestamp())
    except ValueError:
        return None


def parse_jupiter_recent(payload) -> list[dict]:
    out = []
    for t in payload if isinstance(payload, list) else []:
        mint = t.get("id")
        if not mint:
            continue
        created = _iso_ts((t.get("firstPool") or {}).get("createdAt") or t.get("createdAt"))
        out.append({"mint": mint, "symbol": t.get("symbol"), "launchpad": t.get("launchpad"), "created_ts": created})
    return out


def poll_once(http, known: dict, now: int, file: Path | None = None) -> dict:
    """One Jupiter call. Adds unseen mints to `known` (and the notes file). Returns {'items','new','saturated'}.
    saturated = every item was new, so Jupiter itself may have rolled past tokens between our polls."""
    items = parse_jupiter_recent(http.get("jupiter", JUP_RECENT))
    fresh = [t for t in items if t["mint"] not in known]
    f = file or data_file()
    f.parent.mkdir(parents=True, exist_ok=True)
    with open(f, "a", encoding="utf-8") as fh:
        for t in fresh:
            t["seen_ts"] = now
            known[t["mint"]] = t
            fh.write(json.dumps(t) + "\n")
    return {"items": len(items), "new": len(fresh), "saturated": bool(items) and len(fresh) == len(items)}


def load_known(file: Path | None = None) -> dict:
    known: dict = {}
    try:
        for raw in (file or data_file()).read_text(encoding="utf-8").splitlines():
            try:
                t = json.loads(raw)
                known[t["mint"]] = t
            except (ValueError, KeyError):
                continue
    except OSError:
        pass
    return known


def _open_readonly(db_path) -> sqlite3.Connection:
    conn = sqlite3.connect(Path(db_path).resolve().as_uri() + "?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def analyse(known: dict, conn: sqlite3.Connection, now: int, http=None, min_liq_usd: float = 10000.0,
            grace: int = GRACE_SECONDS) -> dict:
    """Compare Jupiter's tokens (first seen at least `grace` seconds ago) with our `pools` table."""
    eligible = [t for t in known.values() if t["seen_ts"] <= now - grace]
    ours = {r["mint"]: r["first_seen_ts"] for r in conn.execute("SELECT mint, first_seen_ts FROM pools")}
    caught = [t for t in eligible if t["mint"] in ours]
    missed = [t for t in eligible if t["mint"] not in ours]
    lags = [ours[t["mint"]] - t["created_ts"] for t in caught if t.get("created_ts")]
    late = sum(1 for x in lags if x > LATE_SECONDS)
    by_pad: dict[str, list[int]] = {}
    for t in eligible:
        pad = t.get("launchpad") or "other"
        row = by_pad.setdefault(pad, [0, 0])
        row[0] += 1
        row[1] += 0 if t["mint"] in ours else 1
    tradable = checked = None
    if http is not None and missed:
        try:
            pairs = fetch_pairs(http, [t["mint"] for t in missed])
            checked = len(missed)
            tradable = sum(1 for p in pairs.values()
                           if float((p.get("liquidity") or {}).get("usd") or 0) >= min_liq_usd)
        except ApiError:
            pass
    return {"listed": len(eligible), "caught": len(caught), "missed": len(missed),
            "missed_pct": (len(missed) / len(eligible)) if eligible else None,
            "median_lag": st.median(lags) if lags else None,
            "p90_lag": (sorted(lags)[int(0.9 * (len(lags) - 1))] if lags else None),
            "late": late, "by_launchpad": by_pad, "missed_tradable": tradable, "missed_checked": checked,
            "min_liq_usd": min_liq_usd, "missed_examples": [t["mint"] for t in missed[:5]]}


def _mins(sec) -> str:
    return "n/a" if sec is None else f"{sec / 60:.1f} min"


def format_report(res: dict, started: int, ended: int, polls: int, saturated: int, total_listed: int) -> str:
    fmt = lambda t: datetime.fromtimestamp(t, tz=timezone.utc).strftime("%d %b %H:%M")  # noqa: E731
    out = [f"# Coverage check vs Jupiter's new-token list ({fmt(started)} to {fmt(ended)} UTC)", "",
           "SHADOW MODE: nothing here placed an order. Jupiter is a second opinion, not ground truth.", ""]
    if not res["listed"]:
        out.append("Not enough data yet: no token was listed long enough ago to judge (needs 15 minutes).")
        return "\n".join(out) + "\n"
    pct = lambda x: "n/a" if x is None else f"{100 * x:.1f}%"  # noqa: E731
    out += ["| Measure | Result |", "|---|---|",
            f"| Tokens Jupiter listed (and 15+ min old) | {res['listed']} (of {total_listed} seen in total) |",
            f"| We had also found | {res['caught']} |",
            f"| **We missed** | **{res['missed']} ({pct(res['missed_pct'])})** |",
            f"| Typical delay when we did catch one (median / 90th percentile) | {_mins(res['median_lag'])} / {_mins(res['p90_lag'])} after Jupiter listed it |",
            f"| Caught more than 10 min late | {res['late']} |"]
    if res["missed_checked"] is not None:
        out.append(f"| Missed tokens that later showed at least ${res['min_liq_usd']:,.0f} liquidity on DexScreener | "
                   f"{res['missed_tradable']} of {res['missed_checked']} |")
    out += ["", "| Launchpad | Listed | Missed |", "|---|---|---|"]
    for pad, (n, m) in sorted(res["by_launchpad"].items(), key=lambda kv: -kv[1][0]):
        out.append(f"| {pad} | {n} | {m} |")
    out += ["", f"Polls made: {polls}. Polls where all 30 listed tokens were new: {saturated} "
            "(if this is more than a few, Jupiter's own list rolled over between polls and some tokens were not even seen here).",
            "Read it as: a high miss rate with very few missed tokens ever reaching real liquidity matters little; "
            "a high miss rate with many reaching liquidity means the discovery source is the weak link."]
    return "\n".join(out) + "\n"


def run_compare(db_path, http, hours: float, poll_seconds: int = 20, min_liq_usd: float = 10000.0,
                sleep=time.sleep, clock=time.time, say=print) -> str:
    """Poll Jupiter for `hours`, then write and return the report. Ctrl+C ends the polling early and still reports."""
    known = load_known()
    started = int(clock())
    end_at = started + hours * 3600
    polls = saturated = 0
    try:
        while clock() < end_at:
            try:
                r = poll_once(http, known, int(clock()))
                polls += 1
                saturated += 1 if (r["saturated"] and polls > 1) else 0
            except ApiError as exc:
                say(f"[jupiter] poll failed: {exc}")
            sleep(poll_seconds)
    except KeyboardInterrupt:
        say("Polling stopped early; reporting what was collected.")
    return report_now(db_path, http, started, polls, saturated, min_liq_usd, clock=clock)


def report_now(db_path, http, started: int, polls: int, saturated: int, min_liq_usd: float, clock=time.time) -> str:
    now = int(clock())
    known = load_known()
    conn = _open_readonly(db_path)
    try:
        res = analyse(known, conn, now, http=http, min_liq_usd=min_liq_usd)
    finally:
        conn.close()
    text = format_report(res, started, now, polls, saturated, len(known))
    config.REPORTS_DIR.mkdir(exist_ok=True)
    path = config.REPORTS_DIR / f"compare-{datetime.fromtimestamp(now, tz=timezone.utc).strftime('%Y%m%d-%H%M')}.md"
    path.write_text(text, encoding="utf-8")
    return text + f"\nSaved: {path}\n"
