"""One scan cycle: discover -> evaluate due pools -> log -> update outcomes. No orders, ever."""
from __future__ import annotations

import time
from datetime import datetime, timezone

from . import funnel, tracker
from .http import ApiError
from .sources import GECKO_SOFT_LIMIT_PER_MIN, discover_adaptive, fetch_pairs, pair_to_features


def utc_midnight(now: int) -> int:
    d = datetime.fromtimestamp(now, tz=timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    return int(d.timestamp())


def apply_verdict(db, pool, f: dict, v: funnel.Verdict, now: int, cfg: dict) -> int:
    """Write the decision row(s) and reschedule the pool. Returns number of decision rows written."""
    mint = pool["mint"]
    symbol = f.get("symbol") or pool["symbol"]
    bench_until = now + int(v.bench_minutes * 60) if v.bench_minutes is not None else None
    features = dict(f)
    if v.onchain:
        features["onchain"] = v.onchain
    offsets = cfg["tracking"]["offsets_seconds"]
    wrote = 0

    def write(decision: str, check: str | None, extra: dict | None = None) -> None:
        nonlocal wrote
        did = db.add_decision(
            ts=now, mint=mint, symbol=symbol, stage=v.stage, decision=decision, check_fired=check,
            reason_class=v.reason_class, reason_text=v.reason_text, bench_until=bench_until,
            price_usd=f.get("price_usd"), liq_usd=f.get("liq_usd"), features={**features, **(extra or {})},
        )
        if v.track:
            db.schedule_outcomes(did, now, offsets)
        wrote += 1

    last_decision, last_check = pool["last_decision"], pool["last_check"]
    new_last = (v.decision, v.check_fired)
    if v.decision == "SIGNAL":
        cooldown = cfg["bench_minutes"]["signal_cooldown"] * 60
        for name in v.signals:
            if not db.recent_signal(mint, name, now - cooldown):
                write("SIGNAL", name, {"strategy": name})
        new_last = ("SIGNAL", ",".join(v.signals))
    elif v.decision == "PASS":
        # One PASS row per token is the control sample; later re-checks of the same token add nothing.
        if last_decision in ("PASS", "SIGNAL"):
            new_last = (last_decision, last_check)
        else:
            write("PASS", None)
    else:
        if (last_decision, last_check) != new_last:
            write(v.decision, v.check_fired)

    age = f.get("age_min")
    too_old = age is not None and age > cfg["scan"]["watch_max_age_minutes"]
    status = "DONE" if (v.done or too_old) else "WATCH"
    wait = int(v.bench_minutes * 60) if v.bench_minutes is not None else 60
    db.update_pool(mint, next_eval_ts=now + max(wait, 15), status=status,
                   last_decision=new_last[0], last_check=new_last[1], symbol=symbol)
    return wrote


def run_cycle(db, http, rpc, cfg: dict, now: int | None = None, log=print) -> dict:
    now = now or int(time.time())
    stats = {"discovered": 0, "new": 0, "evaluated": 0, "decisions": 0, "outcomes": 0,
             "pages": 0, "needed_extra": False, "hit_limit": False, "stopped": None}

    # 1. discovery (extra pages only while a page has no token we have seen before)
    overlap = None
    try:
        found, info = discover_adaptive(
            http, db.is_known_mint, cfg["scan"]["discovery_pages"],
            may_fetch_more=lambda: db.source_calls_since("gecko", now - 60) < GECKO_SOFT_LIMIT_PER_MIN)
        stats.update(info)
        stats["discovered"] = len(found)
        fresh = sum(1 for d in found if db.add_pool_if_new(d["mint"], d["pair_address"], d["symbol"], now))
        stats["new"] = fresh
        overlap = (len(found) - fresh) / len(found) if found else None
    except ApiError as exc:
        log(f"[discovery] failed: {exc}")

    # 2. evaluate pools whose bench has expired
    due = db.due_pools(now, cfg["scan"]["max_evals_per_cycle"])
    if due:
        mints = [p["mint"] for p in due]
        try:
            pairs = fetch_pairs(http, mints)
        except ApiError as exc:
            log(f"[dexscreener] failed: {exc}")
            pairs = None
        if pairs is not None:
            midnight = utc_midnight(now)
            budget = cfg["scan"]["daily_rpc_budget"]
            ctx = funnel.Context(rpc=rpc, http=http, rpc_left=lambda: budget - db.rpc_calls_since(midnight),
                                 **funnel.env_keys())
            for pool in due:
                pair = pairs.get(pool["mint"])
                if pair is None:
                    give_up = cfg["scan"]["no_data_give_up_minutes"] * 60
                    v = funnel.Verdict(decision="SKIP", stage="S1_FREE", check_fired="NO_PAIR_DATA",
                                       reason_text="no pair data from DexScreener", reason_class="RETRY_SHORT",
                                       bench_minutes=cfg["bench_minutes"]["NO_PAIR_DATA"],
                                       done=(now - pool["first_seen_ts"]) > give_up)
                    f = {}
                else:
                    f = pair_to_features(pair, now * 1000)
                    v = funnel.evaluate(pool["mint"], f, ctx, cfg)
                stats["decisions"] += apply_verdict(db, pool, f, v, now, cfg)
                stats["evaluated"] += 1

    # 3. outcome checkpoints
    stats["outcomes"] = tracker.run_due(db, http, cfg, now)
    db.log_cycle(now, stats["discovered"], stats["new"], stats["evaluated"], overlap)
    return stats
