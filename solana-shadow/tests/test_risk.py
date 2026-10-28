"""Risk engine tests: the slice table, sizing caps, halts, and the step-up rule."""
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shadowbot import config  # noqa: E402
from shadowbot.__main__ import main  # noqa: E402
from shadowbot.db import DB  # noqa: E402
from shadowbot.risk import RiskEngine, limits_table, position_size_gbp  # noqa: E402

CFG = config.load_thresholds()
R = CFG["risk"]
T0 = int(datetime(2026, 11, 2, 9, tzinfo=timezone.utc).timestamp())
DAY, WEEK = 86400, 7 * 86400


class TestSliceTable(unittest.TestCase):
    def test_table_matches_the_presentation(self):
        rows = {int(x["slice"]): x for x in limits_table(CFG)}
        self.assertEqual([(rows[s]["per_trade"], rows[s]["project_stop"]) for s in (200, 350, 500, 1000)],
                         [(14, 60), (24.5, 105), (35, 150), (70, 300)])
        self.assertEqual((rows[200]["good_low"], rows[200]["good_high"]), (20, 40))
        self.assertEqual((rows[1000]["range_low"], rows[1000]["range_high"]), (-1000, 400))

    def test_cli_prints_the_ladder(self):
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(main(["slices"]), 0)
        out = buf.getvalue()
        self.assertIn("£25", out)
        self.assertIn("-£1000 to +£400", out)


class TestSizing(unittest.TestCase):
    def test_position_cap_binds_at_default_stop(self):
        size, binding = position_size_gbp(200, 14, 50_000, R)
        self.assertAlmostEqual(size, 14.0)
        self.assertEqual(binding, "position_pct")

    def test_risk_cap_binds_with_a_wide_stop(self):
        size, binding = position_size_gbp(200, 50, 50_000, R)
        self.assertAlmostEqual(size, 4.0)  # 1% of 200 = £2 at risk, a 50% stop => £4
        self.assertEqual(binding, "risk_per_trade")

    def test_liquidity_cap_binds_in_thin_pools(self):
        size, binding = position_size_gbp(1000, 14, 650, R)  # $650 pool = £500, 1% = £5
        self.assertAlmostEqual(size, 5.0)
        self.assertEqual(binding, "liquidity_cap")
        self.assertEqual(position_size_gbp(200, 14, None, R)[0], 0.0)  # unknown liquidity => no size


class TestEngine(unittest.TestCase):
    def setUp(self):
        self.db = DB(":memory:")
        self.live = RiskEngine(self.db, CFG, mode="live", now=T0)
        self.paper = RiskEngine(self.db, CFG, mode="paper", now=T0)

    def tearDown(self):
        self.db.close()

    def test_order_allowed_with_size_and_reason_for_cap(self):
        d = self.live.allow_order(pool_liq_usd=50_000, now=T0)
        self.assertEqual((d.allowed, d.size_gbp, d.binding), (True, 14.0, "position_pct"))

    def test_one_position_at_a_time(self):
        self.live.on_open()
        d = self.live.allow_order(pool_liq_usd=50_000, now=T0)
        self.assertEqual((d.allowed, d.reasons), (False, ["POSITION_OPEN"]))

    def test_too_small_trades_are_vetoed(self):
        d = self.live.allow_order(pool_liq_usd=300, now=T0)  # £230 pool => £2.3 cap
        self.assertFalse(d.allowed)
        self.assertEqual(d.reasons, ["SIZE_TOO_SMALL:liquidity_cap"])

    def test_daily_loss_halts_and_stays_halted_until_reset(self):
        self.live.on_open()
        self.assertEqual(self.live.on_close(-10, -70, now=T0 + 3600), "DAILY_LOSS")  # 5% of £200
        d = self.live.allow_order(pool_liq_usd=50_000, now=T0 + 3700)
        self.assertEqual(d.reasons, ["HALTED:DAILY_LOSS"])
        # a new engine object (a restart) still sees the halt, and a new day does not clear it
        again = RiskEngine(self.db, CFG, mode="live")
        self.assertEqual(again.allow_order(pool_liq_usd=50_000, now=T0 + 2 * DAY).reasons, ["HALTED:DAILY_LOSS"])
        again.reset_halt("reviewed the day", now=T0 + 2 * DAY)
        self.assertTrue(again.allow_order(pool_liq_usd=50_000, now=T0 + 2 * DAY).allowed)
        events = [r["event"] for r in self.db.conn.execute("SELECT event FROM risk_events ORDER BY id")]
        self.assertEqual(events, ["DAILY_LOSS", "HALT_RESET"])

    def test_project_stop_after_a_slow_bleed(self):
        reason = None
        for i in range(12):  # £5 a day stays under the 5% daily limit, but 12 days ends at £140 = the project stop
            self.live.on_open()
            reason = self.live.on_close(-5, -35, now=T0 + i * DAY)
            if i < 11:
                self.assertIsNone(reason)
        self.assertEqual(reason, "PROJECT_STOP")
        self.assertAlmostEqual(self.live.s["equity"], 140.0)

    def test_a_faster_bleed_trips_the_daily_limit_first(self):
        self.live.on_open()
        self.assertEqual(self.live.on_close(-10, -70, now=T0), "DAILY_LOSS")

    def test_paper_and_live_are_separate_books(self):
        self.paper.on_open()
        self.paper.on_close(-9, -60, now=T0)
        self.assertAlmostEqual(self.paper.s["equity"], 191.0)
        self.assertAlmostEqual(self.live.s["equity"], 200.0)

    def _fill(self, engine, n, pct, start, weeks):
        for i in range(n):
            engine.on_open()
            engine.on_close(pct * 0.14, pct, now=start + int(i * weeks * WEEK / n))

    def test_stepup_rule_and_human_confirmation(self):
        self._fill(self.paper, 40, 2.5, T0, 6)
        self.assertFalse(self.live.stepup_report(now=T0)["eligible"])  # no live trades yet
        self._fill(self.live, 12, 2.0, T0, 2)
        young = self.live.stepup_report(now=T0 + 2 * WEEK)
        self.assertFalse(young["eligible"])
        self.assertTrue(any("live weeks" in r for r in young["reasons"]))
        self.assertTrue(any("live trades" in r for r in young["reasons"]))
        self._fill(self.live, 30, 2.0, T0 + 2 * WEEK, 3)
        now = T0 + 6 * WEEK
        rep = self.live.stepup_report(now=now)
        self.assertTrue(rep["eligible"], rep["reasons"])
        self.assertEqual(rep["next_slice"], 350)
        # eligibility alone changes nothing: a person must confirm
        self.assertFalse(self.live.stepup(confirm=False, now=now)["applied"])
        self.assertEqual(self.live.s["slice_index"], 0)
        out = self.live.stepup(confirm=True, equity_after_topup=350, now=now)
        self.assertTrue(out["applied"])
        self.assertEqual((self.live.s["slice_index"], self.live.s["slice_start_equity"], self.live.s["equity"]), (1, 350.0, 350.0))
        self.assertIn("STEP_UP", [r["event"] for r in self.db.conn.execute("SELECT event FROM risk_events")])

    def test_stepup_blocked_when_live_trails_paper_or_is_negative(self):
        self._fill(self.paper, 40, 6.0, T0, 6)
        self._fill(self.live, 40, 1.0, T0, 5)  # positive but 5 points behind paper (tolerance 3)
        rep = self.live.stepup_report(now=T0 + 6 * WEEK)
        self.assertFalse(rep["eligible"])
        self.assertTrue(any("trails paper" in r for r in rep["reasons"]))

    def test_cannot_step_past_the_top(self):
        self.live.s["slice_index"] = len(R["slice_steps"]) - 1
        self.assertEqual(self.live.stepup_report()["reasons"], ["already at the top step"])


class TestCli(unittest.TestCase):
    def test_risk_status_and_stepup_commands_run_on_a_fresh_db(self):
        import contextlib
        import io
        with tempfile.TemporaryDirectory() as tmp:
            db = str(Path(tmp) / "r.db")
            DB(db).close()
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                self.assertEqual(main(["--db", db, "risk-status"]), 0)
                self.assertEqual(main(["--db", db, "stepup"]), 0)
            out = buf.getvalue()
            self.assertIn("not eligible", out)
            self.assertIn("Not eligible yet", out)


if __name__ == "__main__":
    unittest.main()
