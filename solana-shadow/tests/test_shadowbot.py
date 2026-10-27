"""Logic tests on SYNTHETIC fixtures. The fixture shapes follow my memory of the providers' JSON and are not
verified against live responses; `python -m shadowbot doctor` does that on a machine with network access.
"""
import json
import sys
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shadowbot import config, funnel, report, tracker  # noqa: E402
from shadowbot.db import DB  # noqa: E402
from shadowbot.http import ApiError, Http, scrub  # noqa: E402
from shadowbot.runner import apply_verdict, run_cycle  # noqa: E402
from shadowbot.solana_rpc import holder_concentration  # noqa: E402
from shadowbot.sources import pair_to_features, parse_gecko_new_pools  # noqa: E402
from shadowbot.strategy import evaluate_strategies  # noqa: E402

CFG = config.load_thresholds()
NOW = 1_800_000_000


def feats(**kw):
    base = {"symbol": "TST", "age_min": 5.0, "liq_usd": 20000.0, "price_usd": 0.001, "txns_m5": 40,
            "buy_ratio_m5": 0.75, "vol_m5": 9000.0, "vol_h1": 20000.0, "spike_mult": 5.4}
    base.update(kw)
    return base


class FakeRpc:
    def __init__(self, mint_authority=None, freeze_authority=None, amounts=None, supply=1000, extensions=None, fail=False):
        self.calls = 0
        self.info = {"mint_authority": mint_authority, "freeze_authority": freeze_authority, "supply_raw": supply,
                     "decimals": 6, "extensions": extensions or [], "owner_program": "Token"}
        # largest account (assumed LP vault) 50%, then ten small holders
        self.amounts = amounts if amounts is not None else [500] + [20] * 10
        self.fail = fail

    def mint_info(self, mint):
        self.calls += 1
        if self.fail:
            raise ApiError("boom")
        return self.info

    def largest_accounts(self, mint):
        self.calls += 1
        return self.amounts


def ctx(rpc, left=10_000):
    return funnel.Context(rpc=rpc, http=None, rpc_left=lambda: left)


class FakeHttp:
    def __init__(self, routes):
        self.routes = routes

    def get(self, source, url, **kw):
        for key, value in self.routes.items():
            if key in url:
                if isinstance(value, Exception):
                    raise value
                return value() if callable(value) else value
        raise AssertionError(f"unexpected url {url}")


def dex_pair(mint, **over):
    p = {"chainId": "solana", "pairAddress": "pool-" + mint, "dexId": "raydium", "priceUsd": "0.001",
         "baseToken": {"address": mint, "symbol": "TST"}, "liquidity": {"usd": 20000},
         "txns": {"m5": {"buys": 30, "sells": 10}}, "volume": {"m5": 9000, "h1": 20000},
         "pairCreatedAt": (NOW - 5 * 60) * 1000, "fdv": 100000}
    p.update(over)
    return p


class TestPureLogic(unittest.TestCase):
    def test_holder_concentration_excludes_only_the_largest(self):
        r = holder_concentration([500] + [20] * 10, 1000)
        self.assertAlmostEqual(r["top1_pct_incl"], 50.0)
        self.assertAlmostEqual(r["top10_pct_ex_largest"], 20.0)
        self.assertAlmostEqual(r["top_holder_pct_ex_largest"], 2.0)

    def test_holder_concentration_missing_data_is_none_not_zero(self):
        self.assertIsNone(holder_concentration([], 1000)["top10_pct_ex_largest"])
        self.assertIsNone(holder_concentration([5], 0)["top10_pct_ex_largest"])

    def test_stage1_reasons(self):
        self.assertEqual(funnel.stage1(feats(age_min=0.5), CFG).check_fired, "TOO_YOUNG")
        self.assertEqual(funnel.stage1(feats(age_min=0.5), CFG).decision, "SKIP")
        v = funnel.stage1(feats(age_min=1000), CFG)
        self.assertEqual((v.check_fired, v.done, v.bench_minutes), ("TOO_OLD", True, None))
        self.assertEqual(funnel.stage1(feats(liq_usd=100), CFG).check_fired, "LOW_LIQUIDITY")
        self.assertEqual(funnel.stage1(feats(liq_usd=None), CFG).check_fired, "LOW_LIQUIDITY")
        self.assertEqual(funnel.stage1(feats(txns_m5=1), CFG).check_fired, "LOW_ACTIVITY")
        self.assertIsNone(funnel.stage1(feats(), CFG))

    def test_too_young_waits_exactly_until_tellable(self):
        v = funnel.stage1(feats(age_min=0.5), CFG)
        self.assertAlmostEqual(v.bench_minutes, 1.5)

    def test_stage2_authority_and_concentration(self):
        v, _ = funnel.stage2("m", ctx(FakeRpc(mint_authority="x")), CFG)
        self.assertEqual((v.decision, v.check_fired, v.reason_class, v.bench_minutes, v.track),
                         ("FILTERED", "MINT_AUTHORITY_OPEN", "RETRY_LONG", 120, True))
        v, _ = funnel.stage2("m", ctx(FakeRpc(freeze_authority="x")), CFG)
        self.assertEqual(v.check_fired, "FREEZE_AUTHORITY_OPEN")
        v, _ = funnel.stage2("m", ctx(FakeRpc(amounts=[300] + [60] * 10)), CFG)  # top10 ex-largest = 60%
        self.assertEqual(v.check_fired, "TOP10_CONCENTRATION")
        v, _ = funnel.stage2("m", ctx(FakeRpc(amounts=[300, 250] + [5] * 9)), CFG)  # one 25% holder
        self.assertEqual(v.check_fired, "TOP_HOLDER_CONCENTRATION")
        v, on = funnel.stage2("m", ctx(FakeRpc()), CFG)
        self.assertIsNone(v)
        self.assertFalse(on["mint_authority_open"])

    def test_permanent_reason_never_retries(self):
        v, _ = funnel.stage2("m", ctx(FakeRpc(extensions=["permanentDelegate"])), CFG)
        self.assertEqual((v.check_fired, v.done, v.bench_minutes), ("PERMANENT_DELEGATE", True, None))

    def test_rpc_failure_and_budget_are_skips_not_rejections(self):
        v, _ = funnel.stage2("m", ctx(FakeRpc(fail=True)), CFG)
        self.assertEqual((v.decision, v.check_fired), ("SKIP", "RPC_ERROR"))
        rpc = FakeRpc()
        v, _ = funnel.stage2("m", ctx(rpc, left=1), CFG)
        self.assertEqual((v.decision, v.check_fired), ("SKIP", "RPC_BUDGET"))
        self.assertEqual(rpc.calls, 0)

    def test_evaluate_pass_signal_and_cheap_checks_run_first(self):
        rpc = FakeRpc()
        v = funnel.evaluate("m", feats(age_min=5, buy_ratio_m5=0.75, spike_mult=1.0), ctx(rpc), CFG)
        self.assertEqual((v.decision, v.signals), ("SIGNAL", ["new_pair_flow"]))
        v = funnel.evaluate("m", feats(buy_ratio_m5=0.40), ctx(rpc), CFG)
        self.assertEqual((v.decision, v.signals), ("PASS", []))
        calls = rpc.calls
        funnel.evaluate("m", feats(liq_usd=10), ctx(rpc), CFG)  # dies at stage 1
        self.assertEqual(rpc.calls, calls)

    def test_strategy_missing_value_fails_condition(self):
        self.assertEqual(evaluate_strategies(feats(buy_ratio_m5=None), CFG), [])
        self.assertEqual(evaluate_strategies(feats(age_min=60, spike_mult=4.0, buy_ratio_m5=0.65), CFG), ["volume_spike"])

    def test_parsers_on_synthetic_shapes(self):
        payload = {"data": [{"attributes": {"address": "poolA", "name": "FOO / SOL", "pool_created_at": "2026-01-01T00:00:00Z"},
                             "relationships": {"base_token": {"data": {"id": "solana_MintA", "type": "token"}}}},
                            {"attributes": {"address": "poolB", "name": "SOL / USDC"},
                             "relationships": {"base_token": {"data": {"id": "solana_" + config.WSOL_MINT}}}}]}
        parsed = parse_gecko_new_pools(payload)
        self.assertEqual([p["mint"] for p in parsed], ["MintA"])
        f = pair_to_features(dex_pair("MintA"), NOW * 1000)
        self.assertAlmostEqual(f["age_min"], 5.0)
        self.assertAlmostEqual(f["buy_ratio_m5"], 0.75)
        self.assertAlmostEqual(f["spike_mult"], 9000 / (20000 / 12))
        self.assertIsNone(pair_to_features({"baseToken": {"address": "x"}}, NOW * 1000)["liq_usd"])

    def test_scrub_removes_keys(self):
        self.assertNotIn("SECRET", scrub("GET https://x/?api-key=SECRET&a=1 failed"))
        self.assertNotIn("SECRET", str(ApiError("failed https://h/?api-key=SECRET")))


class TestPersistence(unittest.TestCase):
    def setUp(self):
        self.db = DB(":memory:")

    def pool(self, mint="m1"):
        self.db.add_pool_if_new(mint, "pool-" + mint, "TST", NOW)
        return self.db.conn.execute("SELECT * FROM pools WHERE mint=?", (mint,)).fetchone()

    def count(self, where="1=1"):
        return self.db.conn.execute(f"SELECT COUNT(*) c FROM decisions WHERE {where}").fetchone()["c"]

    def test_same_rejection_is_logged_once_and_benched(self):
        f = feats()
        v, _ = funnel.stage2("m1", ctx(FakeRpc(mint_authority="x")), CFG)
        apply_verdict(self.db, self.pool(), f, v, NOW, CFG)
        again = self.db.conn.execute("SELECT * FROM pools WHERE mint='m1'").fetchone()
        apply_verdict(self.db, again, f, v, NOW + 7300, CFG)
        self.assertEqual(self.count("decision='FILTERED'"), 1)
        row = self.db.conn.execute("SELECT * FROM pools WHERE mint='m1'").fetchone()
        self.assertEqual(row["next_eval_ts"], NOW + 7300 + 120 * 60)
        self.assertEqual(row["status"], "WATCH")
        self.assertEqual(self.db.conn.execute("SELECT COUNT(*) c FROM outcomes").fetchone()["c"], len(CFG["tracking"]["offsets_seconds"]))

    def test_permanent_rejection_closes_the_pool(self):
        v, _ = funnel.stage2("m1", ctx(FakeRpc(extensions=["permanentDelegate"])), CFG)
        apply_verdict(self.db, self.pool(), feats(), v, NOW, CFG)
        self.assertEqual(self.db.conn.execute("SELECT status FROM pools WHERE mint='m1'").fetchone()["status"], "DONE")

    def test_pass_is_a_single_control_row_and_signal_cooldown_holds(self):
        rpc = FakeRpc()
        pool = self.pool()
        v = funnel.evaluate("m1", feats(buy_ratio_m5=0.40), ctx(rpc), CFG)
        apply_verdict(self.db, pool, feats(buy_ratio_m5=0.40), v, NOW, CFG)
        pool = self.db.conn.execute("SELECT * FROM pools WHERE mint='m1'").fetchone()
        apply_verdict(self.db, pool, feats(buy_ratio_m5=0.40), v, NOW + 2000, CFG)
        self.assertEqual(self.count("decision='PASS'"), 1)
        sig = funnel.evaluate("m1", feats(), ctx(rpc), CFG)
        pool = self.db.conn.execute("SELECT * FROM pools WHERE mint='m1'").fetchone()
        apply_verdict(self.db, pool, feats(), sig, NOW + 2100, CFG)
        pool = self.db.conn.execute("SELECT * FROM pools WHERE mint='m1'").fetchone()
        apply_verdict(self.db, pool, feats(), sig, NOW + 2200, CFG)  # inside cooldown: no duplicate signal
        self.assertEqual(self.count("decision='SIGNAL'"), 1)

    def test_full_cycle_then_outcomes_then_report(self):
        mint = "MintA"
        http = FakeHttp({
            "geckoterminal": {"data": [{"attributes": {"address": "poolA", "name": "FOO / SOL"},
                                        "relationships": {"base_token": {"data": {"id": "solana_" + mint}}}}]},
            "dexscreener": [dex_pair(mint)],
        })
        stats = run_cycle(self.db, http, FakeRpc(), CFG, now=NOW, log=lambda *_: None)
        self.assertEqual((stats["new"], stats["evaluated"], stats["decisions"]), (1, 1, 1))
        d = self.db.conn.execute("SELECT * FROM decisions").fetchone()
        self.assertEqual((d["decision"], d["check_fired"]), ("SIGNAL", "new_pair_flow"))
        f = json.loads(d["features"])
        self.assertIn("onchain", f)
        self.assertEqual(self.db.conn.execute("SELECT COUNT(*) c FROM outcomes").fetchone()["c"], 4)
        # outcomes come due: price up 20% at +5m, gone at +60m
        later = NOW + 3601
        http.routes["dexscreener"] = [dex_pair(mint, priceUsd="0.0012")]
        tracker.run_due(self.db, http, CFG, NOW + 301)
        http.routes["dexscreener"] = []
        tracker.run_due(self.db, http, CFG, later)
        statuses = {r["offset_s"]: r["status"] for r in self.db.conn.execute("SELECT * FROM outcomes")}
        self.assertEqual(statuses[3600], "missing")
        self.assertEqual(statuses[300], "done")
        text = report.build_report(self.db, CFG)
        self.assertIn("Test C", text)
        self.assertIn("only 1 signals logged", text)

    def test_discovery_failure_does_not_stop_evaluation(self):
        self.db.add_pool_if_new("MintB", "poolB", "BAR", NOW)
        http = FakeHttp({"geckoterminal": ApiError("down", 500), "dexscreener": [dex_pair("MintB")]})
        stats = run_cycle(self.db, http, FakeRpc(), CFG, now=NOW, log=lambda *_: None)
        self.assertEqual(stats["evaluated"], 1)

    def test_api_calls_are_logged_without_secrets(self):
        import requests
        from unittest import mock

        class Resp:
            status_code = 200
            text = "{}"

            def json(self):
                return {"result": 1}

        http = Http(self.db, sleep=lambda *_: None)
        with mock.patch.object(http.session, "request", return_value=Resp()):
            http.post("rpc", "https://mainnet.example/?api-key=SECRET", json={}, label="getSlot")
        row = self.db.conn.execute("SELECT * FROM api_calls").fetchone()
        self.assertEqual((row["source"], row["endpoint"], row["ok"]), ("rpc", "getSlot", 1))
        with mock.patch.object(http.session, "request", side_effect=requests.ConnectionError("fail api-key=SECRET")):
            with self.assertRaises(ApiError):
                http.post("rpc", "https://mainnet.example/?api-key=SECRET", json={}, label="getSlot")
        errs = " ".join(r["error"] or "" for r in self.db.conn.execute("SELECT error FROM api_calls"))
        self.assertNotIn("SECRET", errs)


if __name__ == "__main__":
    unittest.main()
