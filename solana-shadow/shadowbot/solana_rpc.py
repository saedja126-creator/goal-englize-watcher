"""Solana JSON-RPC: mint/freeze authority and holder concentration. Facts, not judgments."""
from __future__ import annotations

from .http import ApiError


def holder_concentration(amounts_raw: list[int], supply_raw: int) -> dict:
    """Concentration from getTokenLargestAccounts amounts.

    The single largest account is usually the pool's token vault (or a bonding curve), so `*_ex_largest`
    excludes exactly that one account. This is an approximation; the raw (inclusive) numbers are logged too
    so thresholds can be recalibrated from data.
    """
    if not supply_raw or supply_raw <= 0 or not amounts_raw:
        return {"top1_pct_incl": None, "top10_pct_incl": None, "top_holder_pct_ex_largest": None,
                "top10_pct_ex_largest": None, "holders_returned": len(amounts_raw or [])}
    amounts = sorted(amounts_raw, reverse=True)
    pct = lambda n: 100.0 * n / supply_raw  # noqa: E731
    return {
        "top1_pct_incl": pct(amounts[0]),
        "top10_pct_incl": pct(sum(amounts[:10])),
        "top_holder_pct_ex_largest": pct(amounts[1]) if len(amounts) > 1 else 0.0,
        "top10_pct_ex_largest": pct(sum(amounts[1:11])),
        "holders_returned": len(amounts),
    }


class Rpc:
    def __init__(self, http, url: str):
        self.http = http
        self.url = url

    def call(self, method: str, params: list):
        data = self.http.post("rpc", self.url, json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params},
                              label=method)
        if isinstance(data, dict) and data.get("error"):
            raise ApiError(f"rpc error in {method}: {data['error']}")
        return (data or {}).get("result")

    def mint_info(self, mint: str) -> dict:
        res = self.call("getAccountInfo", [mint, {"encoding": "jsonParsed"}])
        value = (res or {}).get("value")
        if not value:
            raise ApiError("mint account not found")
        parsed = (value.get("data") or {}).get("parsed") or {}
        if parsed.get("type") != "mint":
            raise ApiError("account is not a token mint")
        info = parsed.get("info") or {}
        extensions = [e.get("extension") for e in (info.get("extensions") or []) if isinstance(e, dict)]
        return {
            "mint_authority": info.get("mintAuthority"),
            "freeze_authority": info.get("freezeAuthority"),
            "supply_raw": int(info.get("supply") or 0),
            "decimals": info.get("decimals"),
            "extensions": extensions,
            "owner_program": value.get("owner"),
        }

    def largest_accounts(self, mint: str) -> list[int]:
        res = self.call("getTokenLargestAccounts", [mint])
        values = (res or {}).get("value") or []
        return sorted((int(v["amount"]) for v in values if v.get("amount") is not None), reverse=True)
