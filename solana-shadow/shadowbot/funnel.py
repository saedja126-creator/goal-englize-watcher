"""The funnel: cheapest check first, hard facts in code, every rejection carries the check that fired.

Stages
  S1_FREE      data already in hand (age, liquidity, activity)
  S2_ONCHAIN   Solana RPC facts (mint/freeze authority, extensions, holder concentration)
  S3_OPTIONAL  RugCheck enrichment, Jupiter sell route (off by default)
  S4_STRATEGY  entry triggers -> SIGNAL, otherwise PASS (kept as the control group)

Bench by reason, not by token: a permanent reason never retries; transient reasons retry when the
reason can have changed (TOO_YOUNG becomes tellable at min age, not an hour later).
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from .http import ApiError
from .optional_checks import jupiter_sell_quote, rugcheck_summary
from .solana_rpc import holder_concentration
from .strategy import evaluate_strategies

REASON_CLASS = {
    "TOO_YOUNG": "RETRY_SHORT", "NO_PAIR_DATA": "RETRY_SHORT", "LOW_LIQUIDITY": "RETRY_SHORT",
    "LOW_ACTIVITY": "RETRY_SHORT", "RPC_ERROR": "RETRY_SHORT", "RPC_BUDGET": "RETRY_SHORT",
    "NO_SELL_ROUTE": "RETRY_SHORT",
    "MINT_AUTHORITY_OPEN": "RETRY_LONG", "FREEZE_AUTHORITY_OPEN": "RETRY_LONG",
    "TOP10_CONCENTRATION": "RETRY_LONG", "TOP_HOLDER_CONCENTRATION": "RETRY_LONG",
    "TOO_OLD": "PERMANENT", "PERMANENT_DELEGATE": "PERMANENT", "RUGCHECK_RUGGED": "PERMANENT",
}


@dataclass
class Verdict:
    decision: str                       # PASS | SIGNAL | FILTERED | SKIP
    stage: str
    check_fired: str | None = None
    reason_text: str = ""
    reason_class: str | None = None
    bench_minutes: float | None = None
    done: bool = False                  # stop evaluating this pool
    track: bool = False                 # schedule outcome checkpoints
    signals: list[str] = field(default_factory=list)
    onchain: dict = field(default_factory=dict)


@dataclass
class Context:
    rpc: object
    http: object
    rpc_left: callable                  # () -> remaining RPC calls today
    jupiter_key: str | None = None
    rugcheck_key: str | None = None


def _reject(decision: str, stage: str, code: str, text: str, cfg: dict, *, track: bool = False,
            minutes: float | None = None, onchain: dict | None = None) -> Verdict:
    cls = REASON_CLASS[code]
    bench = cfg["bench_minutes"]
    if cls == "PERMANENT":
        wait = None
    else:
        wait = minutes if minutes is not None else bench.get(code, bench[cls])
    return Verdict(decision=decision, stage=stage, check_fired=code, reason_text=text, reason_class=cls,
                   bench_minutes=wait, done=(cls == "PERMANENT"), track=track, onchain=onchain or {})


def stage1(f: dict, cfg: dict) -> Verdict | None:
    s = cfg["stage1_free_cut"]
    age = f.get("age_min")
    if age is None:
        return _reject("SKIP", "S1_FREE", "NO_PAIR_DATA", "pair creation time unknown", cfg)
    if age < s["min_age_minutes"]:
        return _reject("SKIP", "S1_FREE", "TOO_YOUNG", f"age {age:.1f}m < {s['min_age_minutes']}m", cfg,
                       minutes=max(0.5, s["min_age_minutes"] - age))
    if age > s["max_age_minutes"]:
        return _reject("FILTERED", "S1_FREE", "TOO_OLD", f"age {age:.0f}m > {s['max_age_minutes']}m", cfg)
    liq = f.get("liq_usd")
    if liq is None or liq < s["min_liquidity_usd"]:
        return _reject("FILTERED", "S1_FREE", "LOW_LIQUIDITY", f"liquidity {liq} < {s['min_liquidity_usd']}", cfg)
    txns = f.get("txns_m5")
    if txns is None or txns < s["min_txns_m5"]:
        return _reject("FILTERED", "S1_FREE", "LOW_ACTIVITY", f"txns_m5 {txns} < {s['min_txns_m5']}", cfg)
    return None


def stage2(mint: str, ctx: Context, cfg: dict) -> tuple[Verdict | None, dict]:
    s = cfg["stage2_onchain"]
    if ctx.rpc_left() < 2:
        return _reject("SKIP", "S2_ONCHAIN", "RPC_BUDGET", "daily RPC budget used up", cfg), {}
    try:
        info = ctx.rpc.mint_info(mint)
        amounts = ctx.rpc.largest_accounts(mint)
    except ApiError as exc:
        return _reject("SKIP", "S2_ONCHAIN", "RPC_ERROR", f"rpc failed: {exc}", cfg), {}
    onchain = {
        "mint_authority_open": info["mint_authority"] is not None,
        "freeze_authority_open": info["freeze_authority"] is not None,
        "extensions": info["extensions"],
        "decimals": info["decimals"],
        "owner_program": info["owner_program"],
        **holder_concentration(amounts, info["supply_raw"]),
    }
    if s["require_mint_authority_revoked"] and onchain["mint_authority_open"]:
        return _reject("FILTERED", "S2_ONCHAIN", "MINT_AUTHORITY_OPEN", "mint authority not revoked", cfg,
                       track=True, onchain=onchain), onchain
    if s["require_freeze_authority_revoked"] and onchain["freeze_authority_open"]:
        return _reject("FILTERED", "S2_ONCHAIN", "FREEZE_AUTHORITY_OPEN", "freeze authority not revoked", cfg,
                       track=True, onchain=onchain), onchain
    if s["reject_permanent_delegate"] and "permanentDelegate" in (info["extensions"] or []):
        return _reject("FILTERED", "S2_ONCHAIN", "PERMANENT_DELEGATE", "token-2022 permanentDelegate set", cfg,
                       track=True, onchain=onchain), onchain
    top10, top1 = onchain["top10_pct_ex_largest"], onchain["top_holder_pct_ex_largest"]
    if top10 is None or top1 is None:
        # Missing is not neutral: holders unknown means we cannot vouch for the token.
        return _reject("SKIP", "S2_ONCHAIN", "RPC_ERROR", "holder data unavailable", cfg, onchain=onchain), onchain
    if top10 > s["max_top10_pct_ex_largest"]:
        return _reject("FILTERED", "S2_ONCHAIN", "TOP10_CONCENTRATION",
                       f"top10 ex-largest {top10:.1f}% > {s['max_top10_pct_ex_largest']}%", cfg,
                       track=True, onchain=onchain), onchain
    if top1 > s["max_top_holder_pct_ex_largest"]:
        return _reject("FILTERED", "S2_ONCHAIN", "TOP_HOLDER_CONCENTRATION",
                       f"top holder ex-largest {top1:.1f}% > {s['max_top_holder_pct_ex_largest']}%", cfg,
                       track=True, onchain=onchain), onchain
    return None, onchain


def stage3(mint: str, f: dict, onchain: dict, ctx: Context, cfg: dict) -> tuple[Verdict | None, dict]:
    s = cfg["stage3_optional"]
    extras: dict = {}
    if s.get("rugcheck_enabled"):
        try:
            summary = rugcheck_summary(ctx.http, mint, ctx.rugcheck_key)
            extras["rugcheck"] = summary
            if summary.get("rugged") is True:
                return _reject("FILTERED", "S3_OPTIONAL", "RUGCHECK_RUGGED", "rugcheck reports rugged", cfg,
                               track=True, onchain={**onchain, **extras}), extras
        except ApiError as exc:
            extras["rugcheck_error"] = str(exc)
    if s.get("jupiter_sell_route_enabled") and f.get("price_usd") and onchain.get("decimals") is not None:
        try:
            extras["jupiter"] = jupiter_sell_quote(ctx.http, mint, int(onchain["decimals"]), f["price_usd"],
                                                   s["jupiter_probe_usd"], ctx.jupiter_key)
        except ApiError as exc:
            if exc.status in (400, 404) and "route" in (exc.body or "").lower():
                return _reject("FILTERED", "S3_OPTIONAL", "NO_SELL_ROUTE", "no sell route for probe size", cfg,
                               track=True, onchain={**onchain, **extras}), extras
            extras["jupiter_error"] = str(exc)
    return None, extras


def evaluate(mint: str, f: dict, ctx: Context, cfg: dict) -> Verdict:
    v = stage1(f, cfg)
    if v:
        return v
    v, onchain = stage2(mint, ctx, cfg)
    if v:
        return v
    v3, extras = stage3(mint, f, onchain, ctx, cfg)
    onchain = {**onchain, **extras}
    if v3:
        return v3
    signals = evaluate_strategies(f, cfg)
    return Verdict(
        decision="SIGNAL" if signals else "PASS", stage="S4_STRATEGY",
        check_fired=None, reason_text=("triggers: " + ", ".join(signals)) if signals else "passed all filters, no trigger",
        reason_class=None, bench_minutes=cfg["bench_minutes"]["reeval_after_pass"], track=True,
        signals=signals, onchain=onchain,
    )


def env_keys() -> dict:
    return {"jupiter_key": os.environ.get("JUPITER_API_KEY") or None,
            "rugcheck_key": os.environ.get("RUGCHECK_API_KEY") or None}
