"""`doctor`: checks setup and each real API, and saves raw sample responses to samples/ so the parsers
can be verified against real data (send me those files; they contain no keys).
"""
from __future__ import annotations

import json
import os
import sys
import time

from . import config
from .http import ApiError, Http, scrub
from .optional_checks import jupiter_sell_quote, rugcheck_summary
from .solana_rpc import Rpc
from .sources import DEX_TOKENS, GECKO_NEW_POOLS, fetch_pairs, pair_to_features, parse_gecko_new_pools

OK, FAIL, SKIP = "PASS", "FAIL", "SKIP"


def _save(name: str, data) -> None:
    config.SAMPLES_DIR.mkdir(exist_ok=True)
    (config.SAMPLES_DIR / f"{name}.json").write_text(json.dumps(data, indent=2)[:200_000], encoding="utf-8")


def _line(status: str, name: str, note: str = "") -> bool:
    print(f"[{status}] {name}" + (f": {note}" if note else ""))
    return status != FAIL


def run_doctor() -> int:
    config.load_env()
    http = Http(db=None, max_retries=1)
    ok = True
    print(f"Python {sys.version.split()[0]}")
    ok &= _line(OK if sys.version_info >= (3, 11) else FAIL, "Python 3.11+")
    ok &= _line(OK if (config.ROOT / ".env").exists() else FAIL, ".env file present",
                "" if (config.ROOT / ".env").exists() else "copy .env.example to .env and add your Helius key")
    url = config.rpc_url()
    ok &= _line(OK if url else FAIL, "RPC configured (HELIUS_API_KEY or SOLANA_RPC_URL)")
    print()

    # DexScreener
    try:
        payload = http.get("dexscreener", DEX_TOKENS.format(addresses=config.WSOL_MINT), label="tokens/v1")
        _save("dexscreener_tokens", payload)
        pairs = fetch_pairs(http, [config.WSOL_MINT])
        if config.WSOL_MINT in pairs:
            feats = pair_to_features(pairs[config.WSOL_MINT], int(time.time() * 1000))
            missing = [k for k in ("liq_usd", "price_usd", "txns_m5", "vol_h1", "age_min") if feats.get(k) is None]
            ok &= _line(OK if not missing else FAIL, "DexScreener pairs", f"missing fields: {missing}" if missing else "all key fields parsed")
        else:
            ok &= _line(FAIL, "DexScreener pairs", "no pair parsed; see samples/dexscreener_tokens.json")
    except ApiError as exc:
        ok &= _line(FAIL, "DexScreener pairs", str(exc))

    # GeckoTerminal
    try:
        payload = http.get("gecko", GECKO_NEW_POOLS, params={"page": 1})
        _save("gecko_new_pools", payload)
        parsed = parse_gecko_new_pools(payload)
        ok &= _line(OK if parsed else FAIL, "GeckoTerminal new pools", f"{len(parsed)} pools parsed" if parsed else "0 parsed; see samples/gecko_new_pools.json")
        if parsed:
            print(f"        newest: {parsed[0]['symbol']} {parsed[0]['mint']} created {parsed[0]['created_at']}")
    except ApiError as exc:
        ok &= _line(FAIL, "GeckoTerminal new pools", str(exc))

    # Solana RPC
    if url:
        rpc = Rpc(http, url)
        try:
            slot = rpc.call("getSlot", [])
            ok &= _line(OK, "Solana RPC getSlot", f"slot {slot}")
            info = rpc.mint_info(config.WSOL_MINT)
            _save("rpc_mint_info_wsol", info)
            ok &= _line(OK, "Solana RPC getAccountInfo(jsonParsed)", f"decimals {info['decimals']}, extensions {info['extensions']}")
            amounts = rpc.largest_accounts(config.WSOL_MINT)
            _save("rpc_largest_accounts_wsol", amounts)
            ok &= _line(OK if amounts else FAIL, "Solana RPC getTokenLargestAccounts", f"{len(amounts)} accounts")
        except ApiError as exc:
            ok &= _line(FAIL, "Solana RPC", scrub(str(exc)))
    else:
        _line(SKIP, "Solana RPC", "no RPC configured")

    # Optional
    if os.environ.get("RUGCHECK_API_KEY"):
        try:
            s = rugcheck_summary(http, config.WSOL_MINT, os.environ["RUGCHECK_API_KEY"])
            _save("rugcheck_summary_wsol", s)
            _line(OK, "RugCheck summary", f"fields: {sorted(k for k, v in s.items() if v is not None)}")
        except ApiError as exc:
            _line(FAIL, "RugCheck summary (optional)", str(exc))
    else:
        _line(SKIP, "RugCheck (optional)", "no RUGCHECK_API_KEY")
    if os.environ.get("JUPITER_API_KEY"):
        try:
            q = jupiter_sell_quote(http, config.WSOL_MINT, 9, 150.0, 50.0, os.environ["JUPITER_API_KEY"])
            _save("jupiter_quote_probe", q)
            _line(OK, "Jupiter quote (optional)", f"fields: {sorted(q)}")
        except ApiError as exc:
            _line(FAIL, "Jupiter quote (optional)", str(exc))
    else:
        _line(SKIP, "Jupiter (optional)", "no JUPITER_API_KEY")

    print("\nSamples saved to samples/ (no keys inside). " + ("All required checks passed." if ok else "Some required checks FAILED."))
    return 0 if ok else 1
