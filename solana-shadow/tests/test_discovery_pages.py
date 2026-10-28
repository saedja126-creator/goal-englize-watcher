"""Extra discovery pages, the per-cycle page log, and the Jupiter coverage check. All on fake data, no network."""
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shadowbot import compare, config, discovery_log  # noqa: E402
from shadowbot.db import DB  # noqa: E402
from shadowbot.http import ApiError  # noqa: E402
from shadowbot.runner import run_cycle  # noqa: E402
from shadowbot.sources import GECKO_SOFT_LIMIT_PER_MIN, MAX_DISCOVERY_PAGES, discover_adaptive  # noqa: E402

CFG = config.load_thresholds()
NOW = 1_800_000_000


def gecko_item(mint):
    return {"attributes": {"address": "pool-" + mint, "name": f"{mint} / SOL"},
            "relationships": {"base_token": {"data": {"id": "solana_" + mint}}}}


class PagedGecko:
    """Answers GeckoTerminal new_pools by page number; a page can be an Exception."""

    def __init__(self, pages):
        self.pages = pages
        self.requested = []

    def get(self, source, url, **kw):
        if "dexscreener" in url:  # new pools become due at once; no pair data keeps this test about discovery
            return []
        if "geckoterminal" not in url:
            raise AssertionError(f"unexpected url {url}")
        page = kw["params"]["page"]
        self.requested.append(page)
        data = self.pages.get(page, [])
        if isinstance(data, Exception):
            raise data
        return {"data": [gecko_item(m) for m in data]}


class TestAdaptivePages(unittest.TestCase):
    def test_one_page_when_it_overlaps(self):
        http = PagedGecko({1: ["a", "b", "c"]})
        found, info = discover_adaptive(http, lambda m: m == "b")
        self.assertEqual(http.requested, [1])
        self.assertEqual((info["pages"], info["needed_extra"], info["hit_limit"], info["stopped"]), (1, False, False, None))
        self.assertEqual([d["mint"] for d in found], ["a", "b", "c"])

    def test_reads_next_page_until_there_is_overlap(self):
        http = PagedGecko({1: ["a", "b"], 2: ["c", "d"], 3: ["e", "old"]})
        found, info = discover_adaptive(http, lambda m: m == "old")
        self.assertEqual(http.requested, [1, 2, 3])
        self.assertEqual((info["pages"], info["needed_extra"], info["hit_limit"]), (3, True, False))
        self.assertEqual(len(found), 6)

    def test_stops_at_three_pages_and_says_it_hit_the_limit(self):
        http = PagedGecko({1: ["a"], 2: ["b"], 3: ["c"], 4: ["d"]})
        found, info = discover_adaptive(http, lambda m: False)
        self.assertEqual(MAX_DISCOVERY_PAGES, 3)
        self.assertEqual(http.requested, [1, 2, 3])
        self.assertEqual((info["pages"], info["needed_extra"], info["hit_limit"]), (3, True, True))
        self.assertEqual(len(found), 3)

    def test_empty_page_ends_the_search(self):
        http = PagedGecko({1: ["a"], 2: []})
        _, info = discover_adaptive(http, lambda m: False)
        self.assertEqual(http.requested, [1, 2])
        self.assertFalse(info["hit_limit"])

    def test_duplicates_across_pages_are_dropped(self):
        http = PagedGecko({1: ["a", "b"], 2: ["b", "c"], 3: ["c", "old"]})
        found, _ = discover_adaptive(http, lambda m: m == "old")
        self.assertEqual([d["mint"] for d in found], ["a", "b", "c", "old"])

    def test_failure_on_a_later_page_keeps_what_we_have(self):
        http = PagedGecko({1: ["a", "b"], 2: ApiError("HTTP 429", 429)})
        found, info = discover_adaptive(http, lambda m: False)
        self.assertEqual([d["mint"] for d in found], ["a", "b"])
        self.assertEqual((info["pages"], info["stopped"], info["needed_extra"]), (1, "error", True))

    def test_failure_on_page_one_still_raises(self):
        with self.assertRaises(ApiError):
            discover_adaptive(PagedGecko({1: ApiError("down", 500)}), lambda m: False)

    def test_rate_guard_blocks_extra_pages_but_not_the_first(self):
        http = PagedGecko({1: ["a"], 2: ["b"]})
        found, info = discover_adaptive(http, lambda m: False, may_fetch_more=lambda: False)
        self.assertEqual(http.requested, [1])
        self.assertEqual(info["stopped"], "rate_guard")
        self.assertEqual(len(found), 1)

    def test_configured_base_pages_are_always_read(self):
        http = PagedGecko({1: ["a"], 2: ["old"], 3: ["c"]})  # page 1 has no overlap but is not the last base page
        _, info = discover_adaptive(http, lambda m: m == "old", base_pages=2)
        self.assertEqual((http.requested, info["pages"], info["needed_extra"]), ([1, 2], 2, False))
        http = PagedGecko({1: ["old"], 2: ["b"], 3: ["old2"]})  # overlap is judged on the last base page
        _, info = discover_adaptive(http, lambda m: m in ("old", "old2"), base_pages=2)
        self.assertEqual((http.requested, info["needed_extra"]), ([1, 2, 3], True))


class TestCycleIntegration(unittest.TestCase):
    def setUp(self):
        self.db = DB(":memory:")

    def tearDown(self):
        self.db.close()

    def run_it(self, http):
        return run_cycle(self.db, http, None, CFG, now=NOW, log=lambda *_: None)

    def test_new_tokens_from_every_page_are_stored(self):
        stats = self.run_it(PagedGecko({1: ["a", "b"], 2: ["c"], 3: ["d"]}))
        self.assertEqual((stats["pages"], stats["new"], stats["hit_limit"], stats["needed_extra"]), (3, 4, True, True))
        self.assertEqual(self.db.conn.execute("SELECT COUNT(*) c FROM pools").fetchone()["c"], 4)

    def test_known_token_on_page_one_means_one_page(self):
        self.db.add_pool_if_new("a", "pool-a", "A", NOW - 100)
        http = PagedGecko({1: ["a", "b"], 2: ["c"]})
        stats = self.run_it(http)
        self.assertEqual((http.requested, stats["pages"], stats["new"]), ([1], 1, 1))

    def test_rate_guard_uses_our_own_call_log(self):
        for i in range(GECKO_SOFT_LIMIT_PER_MIN):
            self.db.log_api_call(ts=NOW - 10 - i, source="gecko", endpoint="new_pools", ok=True, status=200,
                                 latency_ms=50, error=None)
        http = PagedGecko({1: ["a"], 2: ["b"], 3: ["c"]})
        stats = self.run_it(http)
        self.assertEqual((http.requested, stats["stopped"]), ([1], "rate_guard"))

    def test_discovery_failure_is_still_survivable(self):
        stats = self.run_it(PagedGecko({1: ApiError("down", 500)}))
        self.assertEqual((stats["discovered"], stats["pages"]), (0, 0))


class TestDiscoveryLog(unittest.TestCase):
    def test_append_and_summary_by_time_window(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "pages.jsonl"
            discovery_log.append(100, {"pages": 1}, f)
            discovery_log.append(130, {"pages": 2, "needed_extra": True}, f)
            discovery_log.append(160, {"pages": 3, "needed_extra": True, "hit_limit": True}, f)
            discovery_log.append(190, {"pages": 2, "needed_extra": True, "stopped": "error"}, f)
            with open(f, "a", encoding="utf-8") as fh:
                fh.write("not json\n")
            whole = discovery_log.summary(0, 1000, f)
            self.assertEqual((whole["cycles"], whole["needed_extra"], whole["hit_limit"], whole["stopped"], whole["pages"]),
                             (4, 3, 1, 1, 8))
            part = discovery_log.summary(125, 165, f)
            self.assertEqual((part["cycles"], part["needed_extra"], part["hit_limit"]), (2, 2, 1))

    def test_missing_file_is_all_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(discovery_log.summary(0, 10, Path(tmp) / "none.jsonl")["cycles"], 0)


JUP = [{"id": "m1", "symbol": "ONE", "launchpad": "pump.fun", "firstPool": {"createdAt": "2026-10-28T20:00:00Z"}},
       {"id": "m2", "symbol": "TWO", "launchpad": "pump.fun", "firstPool": {"createdAt": "2026-10-28T20:01:00Z"}},
       {"id": "m3", "symbol": "TRE", "launchpad": None, "createdAt": "2026-10-28T20:02:00Z"},
       {"symbol": "NOID"}]


class FakeJup:
    def __init__(self, payloads):
        self.payloads = list(payloads)

    def get(self, source, url, **kw):
        if "jup.ag" in url:
            return self.payloads.pop(0)
        return [{"chainId": "solana", "baseToken": {"address": "m3"}, "liquidity": {"usd": 25000}}]


class TestCompare(unittest.TestCase):
    def test_parse_skips_items_without_an_id_and_reads_times(self):
        items = compare.parse_jupiter_recent(JUP)
        self.assertEqual([t["mint"] for t in items], ["m1", "m2", "m3"])
        self.assertEqual(items[1]["created_ts"] - items[0]["created_ts"], 60)
        self.assertIsNotNone(items[2]["created_ts"])
        self.assertEqual(compare.parse_jupiter_recent({"error": "x"}), [])

    def test_poll_records_only_new_mints_and_flags_a_full_turnover(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "c.jsonl"
            known = {}
            first = compare.poll_once(FakeJup([JUP]), known, 1000, f)
            self.assertEqual((first["items"], first["new"], first["saturated"]), (3, 3, True))
            again = compare.poll_once(FakeJup([JUP]), known, 1020, f)
            self.assertEqual((again["new"], again["saturated"]), (0, False))
            self.assertEqual(len(f.read_text().splitlines()), 3)
            self.assertEqual(set(compare.load_known(f)), {"m1", "m2", "m3"})

    def test_analyse_counts_misses_late_catches_and_launchpads(self):
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        conn.execute("CREATE TABLE pools(mint TEXT, first_seen_ts INTEGER)")
        known = {t["mint"]: {**t, "seen_ts": 1000} for t in compare.parse_jupiter_recent(JUP)}
        known["m4"] = {"mint": "m4", "launchpad": "pump.fun", "created_ts": None, "seen_ts": 99_999}  # too recent to judge
        conn.execute("INSERT INTO pools VALUES('m1', ?)", (known["m1"]["created_ts"] + 120,))   # 2 minutes after Jupiter
        conn.execute("INSERT INTO pools VALUES('m2', ?)", (known["m2"]["created_ts"] + 1800,))  # 30 minutes after
        res = compare.analyse(known, conn, now=100_000, http=FakeJup([]), min_liq_usd=10000)
        self.assertEqual((res["listed"], res["caught"], res["missed"], res["late"]), (3, 2, 1, 1))
        self.assertAlmostEqual(res["missed_pct"], 1 / 3)
        self.assertEqual(res["median_lag"], 960)
        self.assertEqual(res["by_launchpad"], {"pump.fun": [2, 0], "other": [1, 1]})
        self.assertEqual(res["missed_examples"], ["m3"])
        self.assertEqual((res["missed_checked"], res["missed_tradable"]), (1, 1))

    def test_report_text_and_empty_case(self):
        empty = compare.format_report({"listed": 0}, 0, 100, 5, 0, 7)
        self.assertIn("Not enough data yet", empty)
        res = {"listed": 10, "caught": 6, "missed": 4, "missed_pct": 0.4, "median_lag": 120, "p90_lag": 600, "late": 1,
               "by_launchpad": {"pump.fun": [8, 3], "other": [2, 1]}, "missed_tradable": 1, "missed_checked": 4,
               "min_liq_usd": 10000.0, "missed_examples": []}
        text = compare.format_report(res, 0, 3600, 540, 2, 12)
        for needle in ("**4 (40.0%)**", "2.0 min", "pump.fun", "1 of 4", "SHADOW MODE"):
            self.assertIn(needle, text)

    def test_readonly_connection_cannot_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.db"
            DB(path).close()
            conn = compare._open_readonly(path)
            with self.assertRaises(sqlite3.OperationalError):
                conn.execute("INSERT INTO pools(mint, first_seen_ts, next_eval_ts) VALUES('z', 1, 1)")
            conn.close()


if __name__ == "__main__":
    unittest.main()
