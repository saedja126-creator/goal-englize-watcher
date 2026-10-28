"""Parsers checked against trimmed REAL responses captured by `python -m shadowbot doctor` on 27 Oct 2026."""
import unittest

from shadowbot.solana_rpc import holder_concentration
from shadowbot.sources import pair_to_features, parse_gecko_new_pools

GECKO_REAL = {"data": [{
    "id": "solana_CLUXe7pKLMydHwpPUZqZzUDXdNKd1aLXrtW7JS4nBa2A",
    "type": "pool",
    "attributes": {"address": "CLUXe7pKLMydHwpPUZqZzUDXdNKd1aLXrtW7JS4nBa2A", "name": "SHOGGOTH / SOL",
                   "pool_created_at": "2026-10-27T22:45:03Z"},
    "relationships": {
        "base_token": {"data": {"id": "solana_3fajJhhDirSDMg9ddqVA69K96rjQKA6iqffD1y5Lpump", "type": "token"}},
        "quote_token": {"data": {"id": "solana_So11111111111111111111111111111111111111112", "type": "token"}},
    },
}]}

DEX_REAL = {
    "chainId": "solana", "dexId": "orca", "pairAddress": "Czfq3xZZDmsdGdUyrNLtRhGc47cXcZtLG4crryfu44zE",
    "baseToken": {"address": "So11111111111111111111111111111111111111112", "symbol": "SOL"},
    "priceUsd": "101.21",
    "txns": {"m5": {"buys": 44, "sells": 9}},
    "volume": {"h1": 2180615.69, "m5": 21761.39},
    "priceChange": {"m5": 0.01, "h1": -0.22},
    "liquidity": {"usd": 28976947.32},
    "pairCreatedAt": 1688106058000,
}

# Real getTokenLargestAccounts amounts for a pump-style token (first entry is the bonding curve), supply 1e15 raw.
LARGEST_REAL = [930000000000000, 12000000000000, 10000000000000, 9000000000000, 8000000000000]


class TestRealSamples(unittest.TestCase):
    def test_gecko_new_pool_real_shape(self):
        out = parse_gecko_new_pools(GECKO_REAL)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["mint"], "3fajJhhDirSDMg9ddqVA69K96rjQKA6iqffD1y5Lpump")
        self.assertEqual(out[0]["symbol"], "SHOGGOTH")
        self.assertEqual(out[0]["created_at"], "2026-10-27T22:45:03Z")

    def test_dexscreener_pair_real_shape(self):
        f = pair_to_features(DEX_REAL, 1688106058000 + 60000 * 10)
        self.assertAlmostEqual(f["age_min"], 10.0)
        self.assertEqual(f["txns_m5"], 53)
        self.assertAlmostEqual(f["liq_usd"], 28976947.32)
        self.assertAlmostEqual(f["price_usd"], 101.21)
        self.assertIsNotNone(f["spike_mult"])

    def test_dexscreener_pair_without_liquidity_is_none_not_zero(self):
        pump = {**DEX_REAL, "liquidity": None, "dexId": "pumpfun"}
        self.assertIsNone(pair_to_features(pump, 1688106058000)["liq_usd"])

    def test_largest_account_is_treated_as_curve_vault(self):
        c = holder_concentration(LARGEST_REAL, 10 ** 15)
        self.assertAlmostEqual(c["top1_pct_incl"], 93.0)
        self.assertAlmostEqual(c["top_holder_pct_ex_largest"], 1.2)


if __name__ == "__main__":
    unittest.main()
