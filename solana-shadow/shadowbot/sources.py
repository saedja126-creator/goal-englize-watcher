"""Market-data sources.

Discovery: GeckoTerminal new_pools. Pair data and price tracking: DexScreener tokens endpoint.
Response shapes below follow each provider's documented JSON as I remember it, and are UNVERIFIED
against live responses (my build sandbox could not reach these hosts). Parsers are tolerant: a missing
field becomes None, never a crash and never a silent zero. Run `python -m shadowbot doctor` to check
the real shapes and save samples.
"""
from __future__ import annotations

from .config import WSOL_MINT

GECKO_NEW_POOLS = "https://api.geckoterminal.com/api/v2/networks/solana/new_pools"
DEX_TOKENS = "https://api.dexscreener.com/tokens/v1/solana/{addresses}"
USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
QUOTE_MINTS = {WSOL_MINT, USDC_MINT}
DEX_CHUNK = 30
MAX_DISCOVERY_PAGES = 3          # extra pages are read only when a page shows no token we have seen
GECKO_SOFT_LIMIT_PER_MIN = 8     # GeckoTerminal's published free limit is 30/min (one third-party source says ~10);
                                 # extra pages are skipped when our own last minute already used this many calls


def _strip_prefix(token_id: str | None) -> str | None:
    if not token_id:
        return None
    return token_id.split("_", 1)[1] if token_id.startswith("solana_") else token_id


def parse_gecko_new_pools(payload: dict) -> list[dict]:
    out = []
    for item in (payload or {}).get("data") or []:
        attrs = item.get("attributes") or {}
        rel = ((item.get("relationships") or {}).get("base_token") or {}).get("data") or {}
        mint = _strip_prefix(rel.get("id"))
        if not mint or mint in QUOTE_MINTS:
            continue
        name = attrs.get("name") or ""
        out.append({
            "mint": mint,
            "pair_address": attrs.get("address"),
            "symbol": (name.split(" / ")[0].strip() or None),
            "created_at": attrs.get("pool_created_at"),
        })
    return out


def discover_new_mints(http, pages: int = 1) -> list[dict]:
    found: list[dict] = []
    for page in range(1, pages + 1):
        payload = http.get("gecko", GECKO_NEW_POOLS, params={"page": page})
        found.extend(parse_gecko_new_pools(payload))
    return found


def discover_adaptive(http, is_known, base_pages: int = 1, max_pages: int = MAX_DISCOVERY_PAGES,
                      may_fetch_more=lambda: True) -> tuple[list[dict], dict]:
    """New pools, reading further pages only while a page shows no token we have seen before.

    A page with zero overlap means the 20-pool window may have rolled past tokens we never fetched, so the next
    page is read, up to `max_pages`. Returns (found, info). info: pages (fetched OK), needed_extra (the first page
    had no overlap), hit_limit (no overlap even on the last allowed page), stopped (why extra pages ended early:
    'rate_guard', 'error', or None). Page 1 failing raises ApiError as before; a later page failing keeps what we have.
    """
    from .http import ApiError
    max_pages = max(max_pages, base_pages)
    found: list[dict] = []
    seen: set[str] = set()
    info = {"pages": 0, "needed_extra": False, "hit_limit": False, "stopped": None}
    for page in range(1, max_pages + 1):
        if page > 1 and not may_fetch_more():
            info["stopped"] = "rate_guard"
            break
        try:
            payload = http.get("gecko", GECKO_NEW_POOLS, params={"page": page})
        except ApiError:
            if page == 1:
                raise
            info["stopped"] = "error"
            break
        info["pages"] = page
        items = parse_gecko_new_pools(payload)
        for d in items:
            if d["mint"] not in seen:
                seen.add(d["mint"])
                found.append(d)
        if page < base_pages:
            continue
        if not items or any(is_known(d["mint"]) for d in items):
            break
        if page == base_pages:
            info["needed_extra"] = True
        if page == max_pages:
            info["hit_limit"] = True
    return found, info


def _num(x) -> float | None:
    try:
        return float(x) if x is not None else None
    except (TypeError, ValueError):
        return None


def _liq(pair: dict) -> float:
    return _num((pair.get("liquidity") or {}).get("usd")) or 0.0


def fetch_pairs(http, mints: list[str]) -> dict[str, dict]:
    """Best pair (highest USD liquidity, token as base) per mint. Raises ApiError on request failure."""
    best: dict[str, dict] = {}
    for i in range(0, len(mints), DEX_CHUNK):
        chunk = mints[i:i + DEX_CHUNK]
        payload = http.get("dexscreener", DEX_TOKENS.format(addresses=",".join(chunk)), label="tokens/v1")
        pairs = payload if isinstance(payload, list) else ((payload or {}).get("pairs") or [])
        wanted = set(chunk)
        for p in pairs:
            if p.get("chainId") not in (None, "solana"):
                continue
            base = (p.get("baseToken") or {}).get("address")
            if base not in wanted:
                continue
            if base not in best or _liq(p) > _liq(best[base]):
                best[base] = p
    return best


def pair_to_features(pair: dict, now_ms: int) -> dict:
    txns_m5 = (pair.get("txns") or {}).get("m5") or {}
    buys, sells = txns_m5.get("buys"), txns_m5.get("sells")
    total = (buys + sells) if isinstance(buys, (int, float)) and isinstance(sells, (int, float)) else None
    vol = pair.get("volume") or {}
    vol_m5, vol_h1 = _num(vol.get("m5")), _num(vol.get("h1"))
    created = _num(pair.get("pairCreatedAt"))
    change = pair.get("priceChange") or {}
    return {
        "symbol": (pair.get("baseToken") or {}).get("symbol"),
        "pair_address": pair.get("pairAddress"),
        "dex_id": pair.get("dexId"),
        "age_min": (now_ms - created) / 60000.0 if created else None,
        "liq_usd": _num((pair.get("liquidity") or {}).get("usd")),
        "price_usd": _num(pair.get("priceUsd")),
        "fdv": _num(pair.get("fdv")),
        "market_cap": _num(pair.get("marketCap")),
        "txns_m5": total,
        "buys_m5": buys,
        "sells_m5": sells,
        "buy_ratio_m5": (buys / total) if total else None,
        "vol_m5": vol_m5,
        "vol_h1": vol_h1,
        "spike_mult": (vol_m5 / (vol_h1 / 12.0)) if (vol_m5 is not None and vol_h1) else None,
        "price_change_m5": _num(change.get("m5")),
        "price_change_h1": _num(change.get("h1")),
    }
