import argparse
import os
import signal
import sys
import time

from . import background, config
from .db import DB
from .doctor import run_doctor
from .http import Http, scrub
from .report import build_report
from .risk import RiskEngine, limits_table
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


def say(msg: str) -> None:
    """Print (when there is a console) and append to data/run.log."""
    try:
        print(msg, flush=True)
    except (OSError, ValueError):
        pass
    background.log_line(msg)


def cmd_run(args) -> int:
    config.load_env()
    cfg = config.load_thresholds()
    url = config.rpc_url()
    if not url:
        say("No RPC configured. Put HELIUS_API_KEY in .env (see .env.example), then run `doctor`.")
        return 2
    if not args.once and not background.claim_pid():
        say(f"A scanner is already running (pid {background.read_pid()}). Use `python -m shadowbot status` or `stop`.")
        return 3
    db = _open(args.db)
    http = Http(db)
    rpc = Rpc(http, url)
    if hasattr(signal, "SIGTERM") and os.name != "nt":
        signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    say("Shadow mode: scanning and logging only. No orders, no wallet. Ctrl+C to stop.")
    last_report = 0.0
    try:
        while True:
            started = time.time()
            try:
                s = run_cycle(db, http, rpc, cfg, log=say)
                say(f"discovered {s['discovered']} new {s['new']} evaluated {s['evaluated']} "
                    f"decisions {s['decisions']} outcomes {s['outcomes']}")
            except Exception as exc:  # keep the desk alive; the error is logged, not hidden
                say(f"[cycle error] {scrub(repr(exc))}")
            if time.time() - last_report > 3600:
                config.REPORTS_DIR.mkdir(exist_ok=True)
                (config.REPORTS_DIR / "latest.md").write_text(build_report(db, cfg), encoding="utf-8")
                last_report = time.time()
                now_utc = time.gmtime()
                if now_utc.tm_wday == 6 and now_utc.tm_hour >= 20:  # Sunday evening, UTC
                    day = time.strftime("%Y-%m-%d", now_utc)
                    if not (config.REPORTS_DIR / f"weekly-{day}.html").exists():
                        say(f"Weekly report written: {_write_weekly(db, cfg)}")
            if args.once:
                break
            time.sleep(max(1.0, cfg["scan"]["cycle_seconds"] - (time.time() - started)))
    except KeyboardInterrupt:
        say("Stopped.")
    finally:
        db.close()
        if not args.once:
            background.release_pid()
    return 0


def cmd_start(args) -> int:
    ok, msg = background.start(args.db)
    print(msg)
    return 0 if ok else 1


def cmd_stop(args) -> int:
    ok, msg = background.stop()
    print(msg)
    return 0 if ok else 1


def cmd_status(args) -> int:
    db = _open(args.db)
    st = background.status(db)
    db.close()
    age = st["last_cycle_age"]
    if st["running"]:
        print(f"Scanner: RUNNING in the background (pid {st['pid']})")
    elif age is not None and age < 120:
        print("Scanner: running in a window (not started with `start`)")
    else:
        print("Scanner: NOT running")
    print("Last scan cycle: " + ("none yet" if age is None else f"{age} seconds ago"))
    print(f"Last 24 hours: {st['checked_24h']} tokens checked, {st['signals_24h']} entry signals")
    if st["log_tail"]:
        print("\nLatest log lines:")
        for line in st["log_tail"]:
            print("  " + line)
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


def cmd_slices(args) -> int:
    cfg = config.load_thresholds()
    r = cfg["risk"]
    print(f"Slice ladder in pounds (settings from thresholds.toml). Not forecasts: good month {r['illustrative_good_month_pct']}% "
          f"and first-months range {r['illustrative_first_months_range_pct']}% are illustrative.\n")
    print(f"{'Live slice':>10} | {'Per trade':>9} | {'Daily limit':>11} | {'Project stop':>12} | {'Good month':>12} | First live months")
    up = lambda v: int(v + 0.5)  # round half up, so £24.5 reads £25 like the presentation  # noqa: E731
    for x in limits_table(cfg):
        print(f"{'£%d' % up(x['slice']):>10} | {'£%d' % up(x['per_trade']):>9} | {'£%d' % up(x['daily_limit']):>11} | "
              f"{'£%d' % up(x['project_stop']):>12} | {'£%d-%d' % (up(x['good_low']), up(x['good_high'])):>12} | "
              f"-£{up(-x['range_low'])} to +£{up(x['range_high'])}")
    return 0


def cmd_risk(args) -> int:
    cfg = config.load_thresholds()
    db = _open(args.db)
    for mode in ("paper", "live"):
        e = RiskEngine(db, cfg, mode=mode)
        s = e.s
        print(f"[{mode}] slice £{cfg['risk']['slice_steps'][s['slice_index']]} | equity £{s['equity']:.2f} | "
              f"open positions {s['open_positions']} | halted: {s['halted'] or 'no'}")
    rep = RiskEngine(db, cfg, mode="live").stepup_report()
    print("\nStep-up:", "ELIGIBLE" if rep["eligible"] else "not eligible")
    for why in rep["reasons"]:
        print(" -", why)
    db.close()
    return 0


def cmd_stepup(args) -> int:
    cfg = config.load_thresholds()
    db = _open(args.db)
    engine = RiskEngine(db, cfg, mode="live")
    out = engine.stepup(confirm=args.confirm, equity_after_topup=args.equity)
    if out["applied"]:
        print(f"Stepped up to a £{out['next_slice']:.0f} slice. Make sure the account really holds that amount.")
    elif out["eligible"]:
        print(f"Eligible for the next step (£{out['next_slice']:.0f}). Nothing changed: add --confirm to apply it.")
    else:
        print("Not eligible yet:")
        for why in out["reasons"]:
            print(" -", why)
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
    sub.add_parser("slices", help="print the slice ladder: per-trade size, stops and limits in pounds")
    sub.add_parser("risk-status", help="show risk state (paper and live) and step-up eligibility")
    su = sub.add_parser("stepup", help="move the live slice up one step (needs eligibility AND --confirm)")
    su.add_argument("--confirm", action="store_true", help="actually apply the step-up")
    su.add_argument("--equity", type=float, help="account value after you top up (default: the new slice size)")
    sub.add_parser("start", help="start the scanner in the background (no window)")
    sub.add_parser("stop", help="stop the background scanner")
    sub.add_parser("status", help="is it running, when did it last scan, and the latest log lines")
    args = p.parse_args(argv)
    if args.cmd == "start":
        return cmd_start(args)
    if args.cmd == "stop":
        return cmd_stop(args)
    if args.cmd == "status":
        return cmd_status(args)
    if args.cmd == "slices":
        return cmd_slices(args)
    if args.cmd == "risk-status":
        return cmd_risk(args)
    if args.cmd == "stepup":
        return cmd_stepup(args)
    if args.cmd == "doctor":
        return run_doctor()
    if args.cmd == "run":
        return cmd_run(args)
    if args.cmd == "weekly":
        return cmd_weekly(args)
    return cmd_report(args)


if __name__ == "__main__":
    sys.exit(main())
