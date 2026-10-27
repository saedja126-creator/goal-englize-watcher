"""Outcome tracker: price and liquidity checkpoints after every tracked decision.

Checkpoints are forward snapshots, not a simulated exit strategy. The +30s checkpoint approximates the
price you would actually get after an entry delay (real lag is 30-60s because the loop runs every
cycle_seconds). Rule-based exits (stops, trailing) arrive with the paper-trading phase.
"""
from __future__ import annotations

from .http import ApiError
from .sources import _num, fetch_pairs


def run_due(db, http, cfg: dict, now: int) -> int:
    pending = db.pending_outcomes(now)
    if not pending:
        return 0
    give_up = cfg["tracking"]["give_up_after_seconds"]
    mints = sorted({r["mint"] for r in pending})
    try:
        pairs = fetch_pairs(http, mints)
    except ApiError:
        for r in pending:
            if now - r["due_ts"] > give_up:
                db.finish_outcome(r["id"], status="error", now=now, price_usd=None, liq_usd=None)
        return 0
    done = 0
    for r in pending:
        pair = pairs.get(r["mint"])
        if pair is None:
            db.finish_outcome(r["id"], status="missing", now=now, price_usd=None, liq_usd=None)
        else:
            db.finish_outcome(r["id"], status="done", now=now, price_usd=_num(pair.get("priceUsd")),
                              liq_usd=_num((pair.get("liquidity") or {}).get("usd")))
        done += 1
    return done
