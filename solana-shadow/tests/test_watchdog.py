import os
import tempfile
import unittest
from pathlib import Path

from shadowbot import watchdog

GOOD = {"running": True, "last_cycle_age": 20}
DOWN = {"running": False, "last_cycle_age": 5000}
STUCK = {"running": True, "last_cycle_age": 5000}


class Fake:
    def __init__(self, statuses):
        self.statuses, self.restarts, self.stops, self.alerts = list(statuses), 0, 0, []

    def status(self):
        return self.statuses.pop(0) if len(self.statuses) > 1 else self.statuses[0]

    def restart(self):
        self.restarts += 1

    def stop(self):
        self.stops += 1

    def notify(self, title, text, popup=True):
        self.alerts.append(title)


class TestWatchdog(unittest.TestCase):
    def setUp(self):
        tmp = Path(tempfile.mkdtemp())
        self.path = tmp / "alert_state.json"
        old = os.environ.get("SHADOWBOT_DATA_DIR")  # keep test log lines out of the real data/run.log
        os.environ["SHADOWBOT_DATA_DIR"] = str(tmp)
        self.addCleanup(lambda: os.environ.__setitem__("SHADOWBOT_DATA_DIR", old) if old is not None
                        else os.environ.pop("SHADOWBOT_DATA_DIR", None))

    def run_wd(self, fake, now=1000.0):
        return watchdog.run_watchdog(fake.status, restart=fake.restart, stop=fake.stop, notify_fn=fake.notify,
                                     sleep=lambda s: None, now=lambda: now, state_path=self.path)

    def test_healthy_does_nothing(self):
        f = Fake([GOOD])
        self.assertEqual(self.run_wd(f), 0)
        self.assertEqual((f.restarts, f.alerts), (0, []))

    def test_down_then_restart_works_gives_no_alert(self):
        f = Fake([DOWN, DOWN, GOOD])
        self.assertEqual(self.run_wd(f), 0)
        self.assertEqual((f.restarts, f.alerts), (1, []))

    def test_stuck_scanner_is_stopped_before_restart(self):
        f = Fake([STUCK, STUCK, GOOD])
        self.run_wd(f)
        self.assertEqual((f.stops, f.restarts), (1, 1))

    def test_failed_restart_alerts_once_then_repeats_after_six_hours(self):
        f = Fake([DOWN])
        self.assertEqual(self.run_wd(f, now=1000.0), 1)
        self.assertEqual(f.alerts, ["Shadow scanner is DOWN"])
        self.run_wd(f, now=1000.0 + 3600)
        self.assertEqual(len(f.alerts), 1)
        self.run_wd(f, now=1000.0 + 7 * 3600)
        self.assertEqual(len(f.alerts), 2)

    def test_recovery_sends_one_back_up_message_and_clears_state(self):
        f = Fake([DOWN])
        self.run_wd(f)
        g = Fake([GOOD])
        self.assertEqual(self.run_wd(g, now=2000.0), 0)
        self.assertEqual(g.alerts, ["Shadow scanner is back"])
        self.run_wd(g, now=3000.0)
        self.assertEqual(len(g.alerts), 1)

    def test_no_cycles_yet_counts_as_unhealthy(self):
        self.assertFalse(watchdog.healthy({"running": True, "last_cycle_age": None}))


if __name__ == "__main__":
    unittest.main()
