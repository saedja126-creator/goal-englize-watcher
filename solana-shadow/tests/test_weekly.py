"""Weekly report tests on SYNTHETIC log data."""
import sys
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shadowbot import config  # noqa: E402
from shadowbot.__main__ import main  # noqa: E402
from shadowbot.db import DB  # noqa: E402
from shadowbot.weekly import build_weekly, collect, gate_lines, reading  # noqa: E402

CFG = config.load_thresholds()
END = date(2026, 11, 8)  # a Sunday
NOW = int(datetime(2026, 11, 8, 12, tzinfo=timezone.utc).timestamp())
D1 = int(datetime(2026, 11, 7, 12, tzinfo=timezone.utc).timestamp())  # day before END
D2_START = int(datetime(2026, 11, 6, tzinfo=timezone.utc).timestamp())
D1_START = int(datetime(2026, 11, 7, tzinfo=timezone.utc).timestamp())


def add(db, ts, mint, decision, check, stage, outs, p0=1.0, l0=20000.0):
    did = db.add_decision(ts=ts, mint=mint, symbol="T", stage=stage, decision=decision, check_fired=check,
                          reason_class=None, reason_text="", bench_until=None, price_usd=p0, liq_usd=l0, features={})
    db.schedule_outcomes(did, ts, [30, 300, 900, 3600])
    for r in db.conn.execute("SELECT id, offset_s FROM outcomes WHERE decision_id=?", (did,)).fetchall():
        v = outs.get(r["offset_s"])
        if v is None:
            db.finish_outcome(r["id"], status="missing", now=ts + r["offset_s"], price_usd=None, liq_usd=None)
        else:
            db.finish_outcome(r["id"], status="done", now=ts + r["offset_s"], price_usd=v[0], liq_usd=v[1])


def populated() -> DB:
    db = DB(":memory:")
    step = CFG["scan"]["cycle_seconds"]
    db.conn.executemany("INSERT INTO cycles(ts, discovered, new_pools, evaluated, overlap) VALUES(?,?,?,?,?)",
                        [(t, 5, 2, 2, 0.5) for t in range(D2_START, D2_START + 86400 // 2, step)]
                        + [(t, 5, 2, 2, 0.5) for t in range(D1_START, D1_START + 86400, step)])
    db.conn.commit()
    flat = {30: (1.0, 20000), 300: (1.0, 20000), 900: (1.0, 20000), 3600: (1.0, 20000)}
    for i in range(30):
        add(db, D1 + i, f"sig{i}", "SIGNAL", "new_pair_flow", "S4_STRATEGY",
            {30: (1.0, 20000), 300: (1.1, 20000), 900: (1.2, 20000), 3600: (1.2, 20000)})
        add(db, D1 + 100 + i, f"ctl{i}", "PASS", None, "S4_STRATEGY",
            {30: (1.0, 20000), 300: (1.02, 20000), 900: (1.05, 20000), 3600: (1.0, 20000)})
    for i in range(20):
        collapsed = {**flat, 3600: (0.2, 1000)} if i < 16 else flat
        add(db, D1 + 200 + i, f"bad{i}", "FILTERED", "MINT_AUTHORITY_OPEN", "S2_ONCHAIN", collapsed)
    for t in range(D1_START, D1_START + 200):
        db.log_api_call(ts=t, source="rpc", endpoint="getSlot", ok=t % 10 != 0, status=200, latency_ms=50, error=None)
    return db


class TestWeekly(unittest.TestCase):
    def setUp(self):
        self.db = populated()
        self.data = collect(self.db, CFG, END, NOW)

    def tearDown(self):
        self.db.close()

    def day(self, d):
        return next(x for x in self.data["days"] if x["date"] == d)

    def test_day_counts_and_uptime(self):
        d1 = self.day(date(2026, 11, 7))
        self.assertEqual((d1["evaluated"], d1["passed"], d1["rejected"], d1["signals"]), (80, 60, 20, 30))
        self.assertAlmostEqual(d1["uptime"], 1.0, places=2)
        self.assertAlmostEqual(self.day(date(2026, 11, 6))["uptime"], 0.5, places=2)
        self.assertEqual(d1["top_reason"], ("MINT_AUTHORITY_OPEN", 20))
        self.assertAlmostEqual(d1["api_error_rate"], 0.1, places=2)

    def test_empty_days_are_reported_not_hidden(self):
        d = self.day(date(2026, 11, 3))
        self.assertEqual((d["evaluated"], d["signals"]), (0, 0))

    def test_edge_positive_after_costs(self):
        e = self.data["week"]["edge"]
        self.assertEqual(e["label"], "Positive")
        self.assertAlmostEqual(e["signal_after"], 0.16, places=3)
        self.assertAlmostEqual(e["control_after"], 0.01, places=3)

    def test_rug_rates_separate_filtered_from_passed(self):
        w = self.data["week"]
        self.assertAlmostEqual(w["rug_filtered"], 0.8)
        self.assertAlmostEqual(w["rug_passed"], 0.0)

    def test_previous_week_is_empty_and_all_time_matches(self):
        self.assertEqual(self.data["prev"]["signals"], 0)
        self.assertEqual(self.data["all"]["signals"], 30)

    def test_reading_and_gates_are_plain_and_cautious(self):
        text = " ".join(reading(self.data, CFG))
        self.assertIn("Too early to conclude: only 30 signals", text)
        self.assertIn("filters look useful", text)
        gates = dict(gate_lines(self.data, CFG))
        self.assertEqual(gates["Signals logged"], "30 of 200 wanted")
        self.assertEqual(gates["Weeks with a positive edge"], "1 of 1 weeks that had enough data")

    def test_markdown_and_html_render(self):
        md, page, end = build_weekly(self.db, CFG, end=END, now=NOW)
        self.assertEqual(end, END)
        for needle in ("Day by day", "Scorecard", "Progress to the gates", "SHADOW MODE", "Sat 07 Nov"):
            self.assertIn(needle, md)
        self.assertIn("<!doctype html>", page)
        self.assertIn("Sat 07 Nov", page)

    def test_empty_database_still_produces_a_report(self):
        md, page, _ = build_weekly(DB(":memory:"), CFG, end=END, now=NOW)
        self.assertIn("Too early to conclude", md)
        self.assertIn("<table>", page)

    def test_cli_writes_both_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            dbfile = Path(tmp) / "x.db"
            DB(dbfile).close()
            with mock.patch.object(config, "REPORTS_DIR", Path(tmp) / "reports"):
                self.assertEqual(main(["--db", str(dbfile), "weekly", "--end", "2026-11-08"]), 0)
            out = Path(tmp) / "reports"
            self.assertTrue((out / "weekly-2026-11-08.html").exists())
            self.assertTrue((out / "weekly-2026-11-08.md").exists())


if __name__ == "__main__":
    unittest.main()
