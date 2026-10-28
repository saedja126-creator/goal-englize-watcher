"""Watchdog: keep the scanner alive, and tell a person when it cannot be revived.

Run by a Windows scheduled task at login and every 15 minutes as `python -m shadowbot watch`. If the scanner is not
running, or has not finished a scan cycle for 10 minutes, it is (re)started. Only if that fails is an alert sent: a PC
pop-up and, when TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are set in .env, a Telegram message. One alert per incident,
repeated every 6 hours while it stays down, plus one "back up" message when it recovers. It never trades.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import requests

from . import background

STALE_AFTER = 600           # seconds without a finished scan cycle before the scanner counts as stuck
REALERT_AFTER = 6 * 3600    # while it stays down, remind at most this often
WAIT_TRIES, WAIT_GAP = 6, 15  # after a restart, wait up to ~90s for the first scan cycle


def state_file() -> Path:
    return background.data_dir() / "alert_state.json"


def _load_state(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _save_state(path: Path, state: dict) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(state), encoding="utf-8")
    except OSError:
        pass


def healthy(st: dict) -> bool:
    age = st.get("last_cycle_age")
    return bool(st.get("running")) and age is not None and age <= STALE_AFTER


def send_telegram(text: str) -> bool:
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        return False
    try:
        r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                          json={"chat_id": chat, "text": text}, timeout=15)
        return r.ok
    except Exception as exc:  # never log the exception text: it can contain the URL with the token
        background.log_line(f"watchdog: telegram send failed ({type(exc).__name__})")
        return False


def show_popup(title: str, text: str) -> bool:
    """A topmost message box on the PC, in its own process so a person not clicking it never blocks the watchdog."""
    if os.name != "nt":
        return False
    code = "import ctypes,sys;ctypes.windll.user32.MessageBoxW(0,sys.argv[1],sys.argv[2],0x40030)"
    base = subprocess.DETACHED_PROCESS
    for flags in (base | subprocess.CREATE_BREAKAWAY_FROM_JOB, base):  # breakaway may be refused; then plain
        try:
            subprocess.Popen([sys.executable, "-c", code, text, title], creationflags=flags, close_fds=True,
                             stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except OSError:
            continue
    return False


def notify(title: str, text: str, popup: bool = True) -> None:
    tg = send_telegram(f"{title}\n{text}")
    pu = show_popup(title, text) if popup else False
    background.log_line(f"watchdog: alert '{title}' (telegram={'sent' if tg else 'off/failed'}, popup={'shown' if pu else 'no'})")


def run_watchdog(get_status, restart=background.start, stop=background.stop, notify_fn=notify,
                 sleep=time.sleep, now=time.time, state_path: Path | None = None) -> int:
    """0 if the scanner is healthy at the end, 1 if it is still down."""
    path = state_path or state_file()
    state = _load_state(path)
    st = get_status()
    if not healthy(st):
        background.log_line("watchdog: scanner not healthy, trying to start it")
        if st.get("running"):
            stop()  # alive but stuck: stop it first so the restart is clean
        restart()
        for _ in range(WAIT_TRIES):
            st = get_status()
            if healthy(st):
                break
            sleep(WAIT_GAP)
        st = get_status()
    if healthy(st):
        if state.get("alerted_at"):
            notify_fn("Shadow scanner is back", "The scanner is running again.", popup=False)
            state = {}
            _save_state(path, state)
        return 0
    last = state.get("alerted_at")
    if last is None or now() - last >= REALERT_AFTER:
        notify_fn("Shadow scanner is DOWN",
                  "The scanner stopped and could not be restarted automatically. Open PowerShell and run: "
                  "python -m shadowbot status", popup=True)
        state["alerted_at"] = now()
        _save_state(path, state)
    return 1
