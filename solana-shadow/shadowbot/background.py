"""Run the scanner in the background: no window, a log file, a pid file, and plain start / status / stop.

The Windows branch of `start` and `stop` could not be tested where this was written (Linux only); the logic is
the standard subprocess flags for a window-less process and `taskkill`. Check it once on the PC with `status`.
"""
from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

from . import config


def data_dir() -> Path:
    return Path(os.environ.get("SHADOWBOT_DATA_DIR") or config.ROOT / "data")


def pid_file() -> Path:
    return data_dir() / "run.pid"


def log_file() -> Path:
    return data_dir() / "run.log"


def log_line(msg: str) -> None:
    """Append to run.log (rotated at 2 MB). Never raises: logging must not stop the scanner."""
    try:
        data_dir().mkdir(parents=True, exist_ok=True)
        lf = log_file()
        if lf.exists() and lf.stat().st_size > 2_000_000:
            os.replace(lf, lf.with_name("run.log.1"))
        with open(lf, "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
    except OSError:
        pass


def tail(n: int = 5) -> list[str]:
    try:
        return log_file().read_text(encoding="utf-8", errors="replace").splitlines()[-n:]
    except OSError:
        return []


def read_pid() -> int | None:
    try:
        return int(pid_file().read_text().strip())
    except (OSError, ValueError):
        return None


def is_alive(pid: int) -> bool:
    if not pid or pid <= 0:
        return False
    if os.name == "nt":
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True).stdout
        return str(pid) in out
    try:  # reap it if it is our own finished child, so it does not look alive as a zombie
        done, _ = os.waitpid(pid, os.WNOHANG)
        if done == pid:
            return False
    except ChildProcessError:
        pass
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def claim_pid() -> bool:
    """Called by `run`. False if another scanner is already running (so two never run at once)."""
    cur = read_pid()
    if cur and cur != os.getpid() and is_alive(cur):
        return False
    data_dir().mkdir(parents=True, exist_ok=True)
    pid_file().write_text(str(os.getpid()))
    return True


def release_pid() -> None:
    if read_pid() == os.getpid():
        try:
            pid_file().unlink()
        except OSError:
            pass


def start(db_path: str | None = None) -> tuple[bool, str]:
    pid = read_pid()
    if pid and is_alive(pid):
        return False, f"Already running in the background (pid {pid})."
    data_dir().mkdir(parents=True, exist_ok=True)
    args = [sys.executable, "-m", "shadowbot"] + (["--db", str(db_path)] if db_path else []) + ["run"]
    kw: dict = {}
    if os.name == "nt":
        kw["creationflags"] = subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        kw["start_new_session"] = True
    with open(data_dir() / "run.err", "ab") as err:
        proc = subprocess.Popen(args, cwd=str(config.ROOT), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                stderr=err, close_fds=True, **kw)
    for _ in range(60):  # wait up to 15s for the scanner to claim the pid file
        time.sleep(0.25)
        if proc.poll() is not None:
            return False, "The scanner stopped straight away. Look at data/run.err and run `python -m shadowbot doctor`."
        if read_pid() == proc.pid:
            return True, f"Started in the background (pid {proc.pid}). You can close this window."
    return False, "The scanner did not report in. Run `python -m shadowbot status`."


def stop() -> tuple[bool, str]:
    pid = read_pid()
    if not pid or not is_alive(pid):
        try:
            pid_file().unlink()
        except OSError:
            pass
        return False, "No background scanner is running."
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True)
    else:
        os.kill(pid, signal.SIGTERM)
    for _ in range(40):
        if not is_alive(pid):
            break
        time.sleep(0.25)
    try:
        pid_file().unlink()
    except OSError:
        pass
    return (not is_alive(pid)), (f"Stopped (pid {pid})." if not is_alive(pid) else f"Could not stop pid {pid}.")


def status(db) -> dict:
    pid = read_pid()
    running = bool(pid and is_alive(pid))
    now = int(time.time())
    last = db.conn.execute("SELECT MAX(ts) m FROM cycles").fetchone()["m"]
    since = now - 86400
    checked = db.conn.execute("SELECT COUNT(DISTINCT mint) c FROM decisions WHERE ts>=?", (since,)).fetchone()["c"]
    signals = db.conn.execute("SELECT COUNT(*) c FROM decisions WHERE decision='SIGNAL' AND ts>=?", (since,)).fetchone()["c"]
    return {"running": running, "pid": pid if running else None,
            "last_cycle_age": (now - last) if last else None, "checked_24h": checked, "signals_24h": signals,
            "log_tail": tail(5)}
