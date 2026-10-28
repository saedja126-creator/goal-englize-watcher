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
from .weekly import build_weekly


def _write_weekly(db, cfg, end=None) -> str:
    md, page, day = build_weekly(db, cfg, end=end)
    config.REPORTS_DIR.mkdir(exist_ok=True)
    stem = config.REPORTS_DIR / f"weekly-{day.isoformat()}"
    stem.with_suffix(".md").write_text(md, encoding="utf-8")
    stem.with_suffix(".html").write_text(page, encoding="utf-8")
    return str(stem.with_suffix(".html"))


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
                now_utc = time.gmtime()
                if now_utc.tm_wday == 6 and now_utc.tm_hour >= 20:  # Sunday evening, UTC
                    day = time.strftime("%Y-%m-%d", now_utc)
                    if not (config.REPORTS_DIR / f"weekly-{day}.html").exists():
                        print(f"Weekly report written: {_write_weekly(db, cfg)}")
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


def cmd_weekly(args) -> int:
    from datetime import date
    cfg = config.load_thresholds()
    db = _open(args.db)
    end = date.fromisoformat(args.end) if args.end else None
    path = _write_weekly(db, cfg, end)
    print(f"Weekly report written. Open this file in your browser:\n{path}")
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
    wk = sub.add_parser("weekly", help="write the weekly report (markdown and HTML) to reports/")
    wk.add_argument("--end", help="last day of the week as YYYY-MM-DD (default: today, UTC)")
    args = p.parse_args(argv)
    if args.cmd == "doctor":
        return run_doctor()
    if args.cmd == "run":
        return cmd_run(args)
    if args.cmd == "weekly":
        return cmd_weekly(args)
    return cmd_report(args)


if __name__ == "__main__":
    sys.exit(main())
