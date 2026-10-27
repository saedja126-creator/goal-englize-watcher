"""Entry triggers. Pure functions over the feature dict; thresholds come from thresholds.toml.

A missing value fails the condition (missing is not neutral). In shadow mode a trigger only logs a SIGNAL.
"""
from __future__ import annotations


def _matches(s: dict, f: dict) -> bool:
    age = f.get("age_min")
    if age is None or not (s["min_age_minutes"] <= age <= s["max_age_minutes"]):
        return False

    def at_least(key: str, threshold: float) -> bool:
        v = f.get(key)
        return v is not None and v >= threshold

    return (
        at_least("liq_usd", s["min_liquidity_usd"])
        and at_least("txns_m5", s["min_txns_m5"])
        and at_least("buy_ratio_m5", s["min_buy_ratio_m5"])
        and ("min_spike_mult" not in s or at_least("spike_mult", s["min_spike_mult"]))
    )


def evaluate_strategies(features: dict, cfg: dict) -> list[str]:
    return [name for name, s in (cfg.get("strategy") or {}).items() if _matches(s, features)]
