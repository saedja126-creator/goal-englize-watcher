"""Background run tests (POSIX branch; the Windows branch needs a Windows machine)."""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shadowbot import background  # noqa: E402
from shadowbot.__main__ import main  # noqa: E402
from shadowbot.db import DB  # noqa: E402


class TestPidAndLog(unittest.TestCase):
    def test_log_tail_and_stale_pid(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {"SHADOWBOT_DATA_DIR": tmp}):
            for i in range(8):
                background.log_line(f"line {i}")
            self.assertEqual([x.split(" ", 2)[2] for x in background.tail(3)], ["line 5", "line 6", "line 7"])
            background.pid_file().write_text("999999")  # a pid that does not exist
            self.assertFalse(background.is_alive(999999))
            ok, msg = background.stop()
            self.assertFalse(ok)
            self.assertIn("No background scanner", msg)
            self.assertFalse(background.pid_file().exists())  # stale file is cleaned up

    def test_a_second_scanner_cannot_claim_the_pid(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {"SHADOWBOT_DATA_DIR": tmp}):
            background.pid_file().write_text(str(os.getppid()))  # another live process
            self.assertFalse(background.claim_pid())
            background.pid_file().write_text("999999")
            self.assertTrue(background.claim_pid())
            self.assertEqual(background.read_pid(), os.getpid())
            background.release_pid()
            self.assertIsNone(background.read_pid())


@unittest.skipIf(os.name == "nt", "POSIX branch only")
class TestStartStop(unittest.TestCase):
    def test_start_status_second_start_refused_stop(self):
        env = {"SOLANA_RPC_URL": "http://127.0.0.1:9", "HTTPS_PROXY": "", "https_proxy": ""}
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {"SHADOWBOT_DATA_DIR": tmp, **env}):
            db = str(Path(tmp) / "b.db")
            ok, msg = background.start(db)
            self.assertTrue(ok, msg)
            pid = background.read_pid()
            try:
                self.assertTrue(background.is_alive(pid))
                self.assertFalse(background.start(db)[0])      # a second start is refused
                self.assertEqual(main(["--db", db, "run"]), 3)  # so is a second foreground run
                handle = DB(db)
                st = background.status(handle)
                handle.close()
                self.assertTrue(st["running"])
                self.assertEqual(st["pid"], pid)
            finally:
                ok, msg = background.stop()
            self.assertTrue(ok, msg)
            self.assertFalse(background.is_alive(pid))
            self.assertFalse(background.pid_file().exists())


if __name__ == "__main__":
    unittest.main()
