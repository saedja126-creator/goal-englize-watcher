import argparse
import sys
import time

from . import config
from .db import DB
from .doctor import run_doctor
from .http import Http, scrub
from .report import build_report
from .runner import run_cycle
from .solana_rpc import Rpc


def _open(db_path):
    return DB(db_path or config.DEFAULT_DB)


def cmd_run(args) -> int:
    config.load_env()
    cfg = config.load_thresholds()
    url = config.rpc_url()
    if not url:
        print("No RPC configured. Put HELIUS_API_KEY in .env (see .env.example), then run `doctor`.")
        return 2
    db = _open(args.db)
    http = Http(db)
    rpc = Rpc(http, url)
    print("Shadow mode: scanning and logging only. No orders, no wallet. Ctrl+C to stop.")
    last_report = 0.0
    try:
        while True:
            started = time.time()
            try:
                s = run_cycle(db, http, rpc, cfg)
                print(f"{time.strftime('%H:%M:%S')} discovered {s['discovered']} new {s['new']} "
                      f"evaluated {s['evaluated']} decisions {s['decisions']} outcomes {s['outcomes']}")
            except Exception as exc:  # keep the desk alive; the error is logged, not hidden
                print(f"[cycle error] {scrub(repr(exc))}")
            if time.time() - last_report > 3600:
                config.REPORTS_DIR.mkdir(exist_ok=True)
                (config.REPORTS_DIR / "latest.md").write_text(build_report(db, cfg), encoding="utf-8")
                last_report = time.time()
            if args.once:
                break
            time.sleep(max(1.0, cfg["scan"]["cycle_seconds"] - (time.time() - started)))
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        db.close()
    return 0


def cmd_report(args) -> int:
    cfg = config.load_thresholds()
    db = _open(args.db)
    text = build_report(db, cfg, hours=args.hours)
    print(text)
    config.REPORTS_DIR.mkdir(exist_ok=True)
    (config.REPORTS_DIR / "latest.md").write_text(text, encoding="utf-8")
    db.close()
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="shadowbot", description="Shadow-mode Solana scanner. Never trades.")
    p.add_argument("--db", help="path to the SQLite file (default data/shadow.db)")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor", help="check setup and every API; saves samples/")
    r = sub.add_parser("run", help="start the scan loop")
    r.add_argument("--once", action="store_true", help="run a single cycle and exit")
    rep = sub.add_parser("report", help="print Test A/B/C report from the log")
    rep.add_argument("--hours", type=float, help="only the last N hours")
    args = p.parse_args(argv)
    if args.cmd == "doctor":
        return run_doctor()
    if args.cmd == "run":
        return cmd_run(args)
    return cmd_report(args)


if __name__ == "__main__":
    sys.exit(main())
