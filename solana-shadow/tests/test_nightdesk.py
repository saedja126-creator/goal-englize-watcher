import os
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from shadowbot import nightdesk as nd
from shadowbot.http import ApiError

NOW = 1_800_000_000
CFG = nd.load_settings()


def iso(ts):
    return datetime.fromtimestamp(ts, timezone.utc).isoformat().replace("+00:00", "Z")


def pool(mint="MINTAAAA", dex="pumpswap", age_min=120, fdv="1000000", liq="100000", vol_h1="60000", vol_m5="10000",
         pc_m5="10", pc_h1="20", price="1.0", name="GOOD / SOL"):
    return {"attributes": {
        "address": "pair" + mint, "name": name, "pool_created_at": iso(NOW - age_min * 60), "base_token_price_usd": price,
        "fdv_usd": fdv, "market_cap_usd": None, "reserve_in_usd": liq,
        "volume_usd": {"m5": vol_m5, "h1": vol_h1}, "price_change_percentage": {"m5": pc_m5, "h1": pc_h1},
        "transactions": {"m5": {"buys": 30, "sells": 10, "buyers": 20, "sellers": 8}, "h1": {"buys": 200, "sells": 100, "buyers": 120, "sellers": 80}}},
        "relationships": {"base_token": {"data": {"id": "solana_" + mint}}, "dex": {"data": {"id": dex}}}}


def rug_full(**over):
    full = {"mintAuthority": None, "freezeAuthority": None, "token": {"supply": 10 ** 9}, "creatorBalance": 0,
            "topHolders": [{"address": f"a{i}", "owner": f"o{i}", "pct": 2.0} for i in range(10)], "knownAccounts": {},
            "risks": [], "insiderNetworks": []}
    full.update(over)
    return full


class FakeHttp:
    """Routes by source name. gecko -> pools, rugcheck -> reports, dexscreener -> price table."""

    def __init__(self, pools=None, rugs=None, prices=None, gecko_fail=False):
        self.pools = pools or []
        self.rugs = rugs or {}
        self.prices = prices or {}
        self.gecko_fail = gecko_fail
        self.calls = []

    def get(self, source, url, **kw):
        self.calls.append((source, url))
        if source == "gecko":
            if self.gecko_fail:
                raise ApiError("HTTP 429", 429)
            return {"data": self.pools}
        if source == "rugcheck":
            mint = url.split("/tokens/")[1].split("/")[0]
            if mint not in self.rugs:
                raise ApiError("HTTP 404", 404)
            kind = "summary" if url.endswith("/summary") else "full"
            return self.rugs[mint][kind]
        if source == "dexscreener":
            addrs = url.rsplit("/", 1)[-1].split(",")
            return [{"chainId": "solana", "baseToken": {"address": m}, "priceUsd": str(self.prices[m]), "liquidity": {"usd": 100000},
                     "pairAddress": "p" + m} for m in addrs if m in self.prices]
        raise AssertionError(source)


def good_rug():
    return {"summary": {"lpLockedPct": 90}, "full": rug_full()}


def new_db():
    return nd.DeskDB(":memory:", start_equity=150.0)


class SettingsTests(unittest.TestCase):
    def test_values_match_the_prompt(self):
        d, s, f = CFG["desk"], CFG["scout"], CFG["filter"]
        self.assertTrue(d["paper_only"])
        self.assertEqual((d["start_equity_usd"], d["position_pct_of_equity"], d["max_open_positions"]), (150.0, 8.0, 1))
        self.assertEqual((d["hard_stop_pct"], d["trail_activate_pct"], d["trail_pct"]), (6.0, 12.0, 6.0))
        self.assertEqual((s["min_age_minutes"], s["max_age_minutes"], s["min_mcap_usd"], s["max_mcap_usd"]), (30, 72 * 60, 300000, 20000000))
        self.assertEqual((f["min_liquidity_usd"], f["min_volume_h1_usd"], f["max_top10_pct"], f["max_dev_pct"], f["max_bundled_pct"], f["max_pump_h1_pct"]),
                         (40000, 50000, 25, 3, 10, 80))
        self.assertEqual(CFG["analyst"]["pass_score"], 70)


class ParseAndScoutTests(unittest.TestCase):
    def test_parse_and_pass(self):
        c = nd.parse_trending({"data": [pool()]}, NOW)[0]
        self.assertEqual(c["mint"], "MINTAAAA")
        self.assertEqual(c["symbol"], "GOOD")
        self.assertAlmostEqual(c["age_min"], 120, places=1)
        self.assertEqual(c["mcap"], 1_000_000.0)
        self.assertIsNone(nd.scout(c, CFG))

    def test_scout_rules(self):
        def rule(**kw):
            return nd.scout(nd.parse_trending({"data": [pool(**kw)]}, NOW)[0], CFG)
        self.assertEqual(rule(dex="orca"), "SCOUT_DEX")
        self.assertEqual(rule(age_min=29), "SCOUT_AGE")
        self.assertEqual(rule(age_min=72 * 60 + 5), "SCOUT_AGE")
        self.assertEqual(rule(fdv="299999"), "SCOUT_MCAP")
        self.assertEqual(rule(fdv="20000001"), "SCOUT_MCAP")
        self.assertEqual(rule(fdv="14200000014200"), "SCOUT_DATA_MISSING")
        self.assertIsNone(rule(age_min=30, fdv="300000"))


class FilterTests(unittest.TestCase):
    def c(self, **kw):
        return nd.parse_trending({"data": [pool(**kw)]}, NOW)[0]

    def test_free_rules(self):
        self.assertEqual(nd.free_filters(self.c(liq="39999"), CFG)[0], "LIQUIDITY_LOW")
        self.assertEqual(nd.free_filters(self.c(vol_h1="49999"), CFG)[0], "VOLUME_1H_LOW")
        self.assertEqual(nd.free_filters(self.c(pc_h1="80"), CFG)[0], "ALREADY_PUMPED_1H")
        self.assertIsNone(nd.free_filters(self.c(pc_h1="79.9"), CFG))
        self.assertIsNone(nd.free_filters(self.c(liq="40000", vol_h1="50000"), CFG))

    def test_rug_rules_each_kill(self):
        ok = good_rug()
        self.assertIsNone(nd.rug_filters(ok, CFG))
        mint_open = {"summary": ok["summary"], "full": rug_full(mintAuthority="X")}
        self.assertEqual(nd.rug_filters(mint_open, CFG)[0], "MINT_OR_FREEZE_AUTHORITY_NOT_REVOKED")
        freeze_open = {"summary": ok["summary"], "full": rug_full(freezeAuthority="X")}
        self.assertEqual(nd.rug_filters(freeze_open, CFG)[0], "MINT_OR_FREEZE_AUTHORITY_NOT_REVOKED")
        self.assertEqual(nd.rug_filters({"summary": {"lpLockedPct": 10}, "full": rug_full()}, CFG)[0], "LP_NOT_BURNED_OR_LOCKED")
        holders = [{"address": f"a{i}", "owner": f"o{i}", "pct": 3.0} for i in range(10)]
        self.assertEqual(nd.rug_filters({"summary": ok["summary"], "full": rug_full(topHolders=holders)}, CFG)[0], "TOP10_HOLDERS_HIGH")
        self.assertEqual(nd.rug_filters({"summary": ok["summary"], "full": rug_full(creatorBalance=4 * 10 ** 7)}, CFG)[0], "DEV_WALLET_HIGH")
        risk = [{"name": "Creator history of rugged tokens", "level": "danger"}]
        self.assertEqual(nd.rug_filters({"summary": ok["summary"], "full": rug_full(risks=risk)}, CFG)[0], "DEPLOYER_RUG_HISTORY")
        nets = [{"currentHolding": 11 * 10 ** 7}]
        self.assertEqual(nd.rug_filters({"summary": ok["summary"], "full": rug_full(insiderNetworks=nets)}, CFG)[0], "BUNDLED_LAUNCH_HIGH")

    def test_known_pool_accounts_are_not_counted_as_holders(self):
        holders = [{"address": "pool", "owner": "poolowner", "pct": 40.0}] + [{"address": f"a{i}", "owner": f"o{i}", "pct": 2.0} for i in range(10)]
        full = rug_full(topHolders=holders, knownAccounts={"pool": {"name": "Raydium", "type": "AMM"}})
        self.assertAlmostEqual(nd.top10_pct(full), 20.0)
        self.assertIsNone(nd.rug_filters({"summary": {"lpLockedPct": 90}, "full": full}, CFG))

    def test_missing_data_is_a_skip_not_a_pass(self):
        self.assertEqual(nd.rug_filters({"summary": None, "full": None, "error": "HTTP 404"}, CFG)[0], "DATA_MISSING:RUGCHECK")
        self.assertEqual(nd.rug_filters({"summary": {}, "full": rug_full()}, CFG)[0], "DATA_MISSING:LP_LOCK")
        no_risks = rug_full(); no_risks.pop("risks")
        self.assertEqual(nd.rug_filters({"summary": {"lpLockedPct": 90}, "full": no_risks}, CFG)[0], "DATA_MISSING:DEPLOYER_HISTORY")
        no_creator = rug_full(); no_creator.pop("creatorBalance")
        self.assertEqual(nd.rug_filters({"summary": {"lpLockedPct": 90}, "full": no_creator}, CFG)[0], "DATA_MISSING:DEV_WALLET")


class AnalystTests(unittest.TestCase):
    def test_score_range_and_components(self):
        c = nd.parse_trending({"data": [pool()]}, NOW)[0]
        score, comps = nd.analyst_score(c)
        self.assertEqual(len(comps), 4)
        self.assertAlmostEqual(score, 100.0)
        weak = nd.parse_trending({"data": [pool(pc_m5="-5", vol_m5="0", liq="10000", fdv="1000000")]}, NOW)[0]
        s2, _ = nd.analyst_score(weak)
        self.assertLess(s2, 70)
        self.assertGreaterEqual(s2, 0)

    def test_no_inputs_gives_none(self):
        self.assertEqual(nd.analyst_score({})[0], None)


class RiskTests(unittest.TestCase):
    def trade(self, **kw):
        t = {"entry_raw": 1.0, "peak": 1.0, "stop_price": 0.94, "trail_active": 0}
        t.update(kw)
        return t

    def test_hard_stop(self):
        f, r = nd.risk_check(self.trade(), 0.94, CFG)
        self.assertEqual(r, "HARD_STOP")
        _, r2 = nd.risk_check(self.trade(), 0.95, CFG)
        self.assertIsNone(r2)

    def test_gap_below_stop_still_closes(self):
        _, r = nd.risk_check(self.trade(), 0.5, CFG)
        self.assertEqual(r, "HARD_STOP")

    def test_trailing_activates_at_12_and_trails_6(self):
        f, r = nd.risk_check(self.trade(), 1.12, CFG)
        self.assertIsNone(r)
        self.assertEqual(f["trail_active"], 1)
        self.assertAlmostEqual(f["stop_price"], 1.12 * 0.94)
        f2, r2 = nd.risk_check(self.trade(**f), 1.50, CFG)
        self.assertAlmostEqual(f2["stop_price"], 1.50 * 0.94)
        f3, r3 = nd.risk_check(self.trade(**f2), 1.45, CFG)
        self.assertEqual(r3, None)
        self.assertAlmostEqual(f3["stop_price"], 1.50 * 0.94)       # never moved further away
        _, r4 = nd.risk_check(self.trade(**f3), 1.50 * 0.94, CFG)
        self.assertEqual(r4, "TRAIL_STOP")

    def test_stop_never_lowered_when_price_falls_but_holds(self):
        f, _ = nd.risk_check(self.trade(stop_price=0.94), 0.97, CFG)
        self.assertEqual(f["stop_price"], 0.94)


class CycleTests(unittest.TestCase):
    def run_cycle(self, http, db=None, now=NOW):
        db = db or new_db()
        return db, nd.run_cycle(http, db, CFG, now=now, sleep=lambda s: None)

    def test_a_good_token_is_bought_in_paper_at_8_percent(self):
        http = FakeHttp([pool()], {"MINTAAAA": good_rug()}, {"MINTAAAA": 1.0})
        db, s = self.run_cycle(http)
        self.assertEqual(s["traded"], 1)
        t = db.open_trade()
        self.assertAlmostEqual(t["size_usd"], 12.0)
        self.assertAlmostEqual(t["entry_fill"], 1.02)               # 2% entry friction
        self.assertAlmostEqual(t["stop_price"], 0.94)
        decisions = [(e["agent"], e["decision"]) for e in db.conn.execute("SELECT * FROM events ORDER BY id")]
        for step in [("SCOUT", "PASS"), ("FILTER", "SURVIVE"), ("ANALYST", "PASS"), ("EXECUTOR", "ENTER")]:
            self.assertIn(step, decisions)
        self.assertEqual(db.conn.execute("SELECT verdict FROM bench").fetchone()["verdict"], "TRADED")

    def test_kill_is_logged_with_the_exact_rule_and_no_rugcheck_call_is_wasted(self):
        http = FakeHttp([pool(liq="30000")], {}, {})
        db, s = self.run_cycle(http)
        self.assertEqual(s["killed"], 1)
        e = db.conn.execute("SELECT * FROM events WHERE decision='KILL'").fetchone()
        self.assertEqual(e["rule"], "LIQUIDITY_LOW")
        self.assertFalse([c for c in http.calls if c[0] == "rugcheck"])

    def test_rugcheck_failure_skips_the_pair(self):
        http = FakeHttp([pool()], {}, {"MINTAAAA": 1.0})
        db, s = self.run_cycle(http)
        self.assertEqual((s["traded"], s["skipped"]), (0, 1))
        self.assertEqual(db.conn.execute("SELECT rule FROM events WHERE decision='SKIP'").fetchone()["rule"], "DATA_MISSING:RUGCHECK")

    def test_low_score_is_killed_and_logged_with_the_score(self):
        http = FakeHttp([pool(pc_m5="-5", vol_m5="0", liq="40000", fdv="2000000")], {"MINTAAAA": good_rug()}, {"MINTAAAA": 1.0})
        db, s = self.run_cycle(http)
        self.assertEqual(s["scored_low"], 1)
        e = db.conn.execute("SELECT * FROM events WHERE rule='SCORE_BELOW_70'").fetchone()
        self.assertIn("score", e["detail"])

    def test_one_position_at_a_time(self):
        http = FakeHttp([pool("MINTAAAA"), pool("MINTBBBB")], {"MINTAAAA": good_rug(), "MINTBBBB": good_rug()}, {"MINTAAAA": 1.0, "MINTBBBB": 2.0})
        db, s = self.run_cycle(http)
        self.assertEqual(s["traded"], 1)
        self.assertEqual(db.conn.execute("SELECT COUNT(*) c FROM trades").fetchone()["c"], 1)
        self.assertEqual(db.conn.execute("SELECT rule FROM events WHERE agent='EXECUTOR' AND decision='SKIP'").fetchone()["rule"], "POSITION_OPEN")

    def test_cooldown_prevents_rejudging(self):
        http = FakeHttp([pool(liq="30000")], {}, {})
        db, _ = self.run_cycle(http)
        _, s2 = self.run_cycle(http, db, now=NOW + 600)
        self.assertEqual(s2["scout_pass"], 0)
        self.assertEqual(s2["scout_kills"].get("COOLDOWN"), 1)

    def test_lagging_source_is_logged_and_nothing_is_traded(self):
        db, s = self.run_cycle(FakeHttp(gecko_fail=True))
        self.assertEqual(s["traded"], 0)
        self.assertEqual(db.conn.execute("SELECT rule FROM events").fetchone()["rule"], "DATA_LAG")

    def test_scout_rejects_are_counted_not_traded(self):
        http = FakeHttp([pool(dex="orca"), pool("MINTBBBB", age_min=5)], {}, {})
        db, s = self.run_cycle(http)
        self.assertEqual(s["scout_pass"], 0)
        self.assertEqual(s["scout_kills"], {"SCOUT_DEX": 1, "SCOUT_AGE": 1})


class PositionTests(unittest.TestCase):
    def open_one(self):
        http = FakeHttp([pool()], {"MINTAAAA": good_rug()}, {"MINTAAAA": 1.0})
        db = new_db()
        nd.run_cycle(http, db, CFG, now=NOW, sleep=lambda s: None)
        return db, http

    def test_stop_hit_books_the_observed_price_not_the_stop_price(self):
        db, http = self.open_one()
        http.prices["MINTAAAA"] = 0.80                              # gap far below the 0.94 stop
        self.assertEqual(nd.track_position(http, db, CFG, NOW + 30), "closed HARD_STOP")
        t = db.conn.execute("SELECT * FROM trades").fetchone()
        self.assertEqual(t["exit_reason"], "HARD_STOP")
        self.assertAlmostEqual(t["exit_raw"], 0.80)
        self.assertAlmostEqual(t["exit_fill"], 0.80 * 0.98)
        self.assertLess(t["pnl_pct"], -20)
        self.assertLess(db.equity(), 150.0)

    def test_winner_is_closed_by_trailing_stop(self):
        db, http = self.open_one()
        for i, px in enumerate([1.05, 1.20, 1.40], 1):
            http.prices["MINTAAAA"] = px
            self.assertEqual(nd.track_position(http, db, CFG, NOW + 30 * i), "holding")
        http.prices["MINTAAAA"] = 1.40 * 0.93
        self.assertEqual(nd.track_position(http, db, CFG, NOW + 200), "closed TRAIL_STOP")
        t = db.conn.execute("SELECT * FROM trades").fetchone()
        self.assertGreater(t["pnl_usd"], 0)
        self.assertGreater(db.equity(), 150.0)
        self.assertEqual(db.conn.execute("SELECT COUNT(*) c FROM equity").fetchone()["c"], 1)

    def test_lost_price_data_is_booked_as_a_total_loss(self):
        db, http = self.open_one()
        http.prices.clear()
        self.assertEqual(nd.track_position(http, db, CFG, NOW + 60), "no price (waiting)")
        self.assertEqual(nd.track_position(http, db, CFG, NOW + 15 * 60 + 1), "closed DATA_LOST")
        t = db.conn.execute("SELECT * FROM trades").fetchone()
        self.assertAlmostEqual(t["pnl_pct"], -100.0)

    def test_equity_compounds_from_closed_trades_only(self):
        db, http = self.open_one()
        self.assertEqual(db.equity(), 150.0)                        # open trade does not change equity
        http.prices["MINTAAAA"] = 0.5
        nd.track_position(http, db, CFG, NOW + 30)
        self.assertLess(db.equity(), 150.0)


class BenchAndDashboardTests(unittest.TestCase):
    def test_benchmark_fills_after_15_min_and_1_hour(self):
        http = FakeHttp([pool(liq="30000")], {}, {"MINTAAAA": 1.5})
        db = new_db()
        nd.run_cycle(http, db, CFG, now=NOW, sleep=lambda s: None)
        self.assertEqual(nd.settle_bench(http, db, CFG, NOW + 10), 0)
        self.assertEqual(nd.settle_bench(http, db, CFG, NOW + 901), 1)
        self.assertEqual(nd.settle_bench(http, db, CFG, NOW + 3601), 1)
        b = db.conn.execute("SELECT * FROM bench").fetchone()
        self.assertEqual((b["p15"], b["p60"]), (1.5, 1.5))
        self.assertIn("KILLED", nd.build_report(db, CFG, NOW + 3700))

    def test_status_dashboard_has_the_requested_sections(self):
        http = FakeHttp([pool(), pool("MINTBBBB", liq="1000")], {"MINTAAAA": good_rug()}, {"MINTAAAA": 1.0})
        db = new_db()
        nd.run_cycle(http, db, CFG, now=NOW, sleep=lambda s: None)
        text = nd.build_status(db, CFG, NOW + 5)
        for part in ["PAPER ONLY", "Equity $150.00", "| SCOUT |", "| FILTER |", "| ANALYST |", "| EXECUTOR |", "| RISK |", "| LOGGER |",
                     "Open position", "Latest kills", "LIQUIDITY_LOW", "Kill and skip statistics"]:
            self.assertIn(part, text)


class SeparationTests(unittest.TestCase):
    def test_uses_its_own_database_file_and_never_the_scanner_database(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = os.environ.get("SHADOWBOT_DATA_DIR")
            os.environ["SHADOWBOT_DATA_DIR"] = tmp
            try:
                db = nd.DeskDB(start_equity=150.0)
                db.close()
                self.assertEqual(sorted(p.name for p in Path(tmp).iterdir() if p.suffix == ".db"), ["nightdesk.db"])
                self.assertFalse((Path(tmp) / "shadow.db").exists())
            finally:
                if old is None:
                    os.environ.pop("SHADOWBOT_DATA_DIR", None)
                else:
                    os.environ["SHADOWBOT_DATA_DIR"] = old

    def test_source_never_touches_the_scanner_database_or_a_wallet(self):
        src = Path(nd.__file__).read_text(encoding="utf-8")
        for banned in ["from .db import", "shadow.db", "import DB", "private_key", "seed", "keypair", "sendTransaction", "signTransaction"]:
            self.assertNotIn(banned, src)


if __name__ == "__main__":
    unittest.main()
