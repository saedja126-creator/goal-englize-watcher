"""Optional stage-3 checks. Disabled by default: endpoints and fields are UNVERIFIED until `doctor` runs.

RugCheck is used only as enrichment (raw fields logged for calibration); it rejects only on an explicit
`rugged: true`. The Jupiter check proves only that a sell route exists. It is NOT a honeypot proof
(a quote does not simulate transfer restrictions or sell taxes).
"""
from __future__ import annotations

from .config import WSOL_MINT

RUGCHECK_SUMMARY = "https://api.rugcheck.xyz/v1/tokens/{mint}/report/summary"
JUPITER_QUOTE = "https://api.jup.ag/swap/v1/quote"


def rugcheck_summary(http, mint: str, api_key: str | None = None) -> dict:
    headers = {"X-API-KEY": api_key} if api_key else None
    data = http.get("rugcheck", RUGCHECK_SUMMARY.format(mint=mint), headers=headers)
    data = data if isinstance(data, dict) else {}
    return {
        "rugged": data.get("rugged"),
        "score": data.get("score"),
        "score_normalised": data.get("score_normalised"),
        "risks": [r.get("name") for r in (data.get("risks") or []) if isinstance(r, dict)],
    }


def jupiter_sell_quote(http, mint: str, decimals: int, price_usd: float, probe_usd: float,
                       api_key: str | None = None) -> dict:
    amount = int((probe_usd / price_usd) * (10 ** decimals))
    headers = {"x-api-key": api_key} if api_key else None
    data = http.get("jupiter", JUPITER_QUOTE, headers=headers, label="swap/v1/quote",
                    params={"inputMint": mint, "outputMint": WSOL_MINT, "amount": str(amount), "slippageBps": "1000"})
    data = data if isinstance(data, dict) else {}
    return {"out_amount": data.get("outAmount"), "price_impact_pct_raw": data.get("priceImpactPct")}
