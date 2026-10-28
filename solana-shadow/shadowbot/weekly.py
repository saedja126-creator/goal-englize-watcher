"""Weekly report: what happened each day, this week against last week, and progress to the gates.

Written for a non-technical reader: day-by-day timeline, a short scorecard, plain-English reading, and a gate
tracker. All days are UTC. Every sentence is produced from fixed rules over the log (no model involved).
"""
from __future__ import annotations

import html
import math
import statistics as st
from datetime import date, datetime, timedelta, timezone

from .report import _outcome_rows, _pct, _table

DAY = 86400


def _ts(d: date) -> int:
    return int(datetime(d.year, d.month, d.day, tzinfo=timezone.utc).timestamp())


def _verdicts(db, since: int, until: int) -> dict:
    rows = db.conn.execute(
        "SELECT mint, MAX(CASE WHEN decision IN ('PASS','SIGNAL') THEN 1 ELSE 0 END) p, "
        "MAX(CASE WHEN decision='FILTERED' THEN 1 ELSE 0 END) f FROM decisions WHERE ts>=? AND ts<? GROUP BY mint",
        (since, until)).fetchall()
    return {"evaluated": len(rows), "passed": sum(1 for r in rows if r["p"]),
            "rejected": sum(1 for r in rows if not r["p"] and r["f"])}


def _returns(db, since: int, until: int, where: str, params: tuple, offset: int) -> list[float]:
    rows = _outcome_rows(db, since, f"{where} AND d.ts<?", (*params, until), offset)
    out = []
    for x in rows:
        if x["status"] != "done" or not x["p1"]:
            continue
        entry = x["pe"] or x["p0"]
        if entry:
            out.append(x["p1"] / entry - 1)
    return out


def _rug(db, cfg: dict, since: int, until: int, where: str) -> tuple[int, int, int]:
    t = cfg["tracking"]
    n = rugged = missing = 0
    for x in _outcome_rows(db, since, f"{where} AND d.ts<?", (until,), 3600):
        if x["status"] not in ("done", "missing"):
            continue
        n += 1
        if x["status"] == "missing":
            missing += 1
        elif (x["l0"] and x["l1"] is not None and x["l1"] < (1 - t["rug_liquidity_drop"]) * x["l0"]) or \
             (x["p0"] and x["p1"] is not None and x["p1"] < (1 - t["rug_price_drop"]) * x["p0"]):
            rugged += 1
    return n, rugged, missing


def edge(db, cfg: dict, since: int, until: int) -> dict:
    friction = cfg["report"]["friction_pct"] / 100.0
    sig = _returns(db, since, until, "d.decision='SIGNAL'", (), 900)
    ctl = _returns(db, since, until, "d.decision='PASS'", (), 900)
    s_after = st.mean(sig) - friction if sig else None
    c_after = st.mean(ctl) - friction if ctl else None
    need = cfg["weekly"]["min_n_per_week"]
    if len(sig) < need or len(ctl) < need:
        label = "Too few"
    elif s_after > 0 and s_after > c_after:
        label = "Positive"
    else:
        label = "Not positive"
    return {"label": label, "n_signal": len(sig), "n_control": len(ctl), "signal_after": s_after, "control_after": c_after}


def period(db, cfg: dict, since: int, until: int, now: int) -> dict:
    v = _verdicts(db, since, until)
    sig_rows = db.conn.execute("SELECT COUNT(*) c FROM decisions WHERE decision='SIGNAL' AND ts>=? AND ts<?",
                               (since, until)).fetchone()["c"]
    api = db.conn.execute("SELECT COUNT(*) n, COALESCE(SUM(1-ok),0) e FROM api_calls WHERE ts>=? AND ts<?",
                          (since, until)).fetchone()
    cycles = db.conn.execute("SELECT COUNT(*) c FROM cycles WHERE ts>=? AND ts<?", (since, until)).fetchone()["c"]
    first = db.conn.execute("SELECT MIN(ts) m FROM cycles").fetchone()["m"]
    uptime = None
    if first is not None:
        start, end = max(since, first), min(until, now)
        expected = (end - start) / cfg["scan"]["cycle_seconds"]
        uptime = min(1.0, cycles / expected) if expected >= 1 else None
    top = db.conn.execute(
        "SELECT check_fired c, COUNT(*) n FROM decisions WHERE decision='FILTERED' AND ts>=? AND ts<? "
        "GROUP BY check_fired ORDER BY n DESC LIMIT 1", (since, until)).fetchone()
    nf, rf, mf = _rug(db, cfg, since, until, "d.decision='FILTERED' AND d.stage IN ('S2_ONCHAIN','S3_OPTIONAL')")
    npass, rpass, mpass = _rug(db, cfg, since, until, "d.decision IN ('PASS','SIGNAL')")
    total = v["passed"] + v["rejected"]
    return {
        **v, "signals": sig_rows, "api_calls": api["n"], "api_errors": api["e"],
        "api_error_rate": (api["e"] / api["n"]) if api["n"] else None,
        "uptime": uptime, "top_reason": (top["c"], top["n"]) if top else None,
        "reject_rate": (v["rejected"] / total) if total else None,
        "rug_filtered": (rf / nf) if nf else None, "n_filtered": nf,
        "rug_passed": (rpass / npass) if npass else None, "n_passed": npass,
        "edge": edge(db, cfg, since, until),
    }


def collect(db, cfg: dict, end: date, now: int) -> dict:
    start = end - timedelta(days=6)
    week_since, week_until = _ts(start), _ts(end) + DAY
    days = []
    for i in range(7):
        d = start + timedelta(days=i)
        days.append({"date": d, **period(db, cfg, _ts(d), _ts(d) + DAY, now)})
    this_week = period(db, cfg, week_since, week_until, now)
    prev_week = period(db, cfg, week_since - 7 * DAY, week_since, now)
    all_time = period(db, cfg, 0, week_until, now)

    first = db.conn.execute("SELECT MIN(ts) m FROM decisions").fetchone()["m"]
    history = []
    if first is not None:
        w_until = week_until
        while w_until > first and len(history) < 30:
            history.append({"until": w_until, "edge": edge(db, cfg, w_until - 7 * DAY, w_until)})
            w_until -= 7 * DAY
        history.reverse()
    weeks_elapsed = max(1, math.ceil((week_until - first) / (7 * DAY))) if first is not None else 0
    return {"end": end, "start": start, "days": days, "week": this_week, "prev": prev_week, "all": all_time,
            "history": history, "weeks_elapsed": weeks_elapsed}


def day_note(d: dict) -> str:
    if d["evaluated"] == 0 and d["uptime"] is None:
        return "No data"
    bits = [f"{d['signals']} signal{'s' if d['signals'] != 1 else ''}"]
    if d["top_reason"]:
        bits.append(f"top rejection {d['top_reason'][0]} ({d['top_reason'][1]})")
    if d["uptime"] is not None and d["uptime"] < 0.5:
        bits.append("scanner mostly off")
    if d["api_error_rate"] is not None and d["api_error_rate"] > 0.10:
        bits.append("data-source trouble")
    return "; ".join(bits)


def reading(data: dict, cfg: dict) -> list[str]:
    w, a = data["week"], data["all"]
    out: list[str] = []
    need = cfg["report"]["min_signals_for_conclusion"]
    if a["signals"] < need:
        out.append(f"Too early to conclude: only {a['signals']} signals so far, and {need}+ are needed before the "
                   "results mean anything.")
    if w["uptime"] is not None and w["uptime"] < 0.8:
        out.append(f"The scanner ran only {_pct(w['uptime'], 0)} of the week. Check the PC's sleep settings; gaps mean "
                   "missed tokens.")
    if w["api_error_rate"] is not None and w["api_error_rate"] > 0.05:
        out.append(f"Data sources failed on {_pct(w['api_error_rate'])} of calls (target under 5%).")
    if w["reject_rate"] is not None and w["evaluated"] >= 30:
        if w["reject_rate"] < cfg["report"]["min_reject_rate"]:
            out.append(f"Only {_pct(w['reject_rate'], 0)} of checked tokens were rejected, which is low. The filters may be too loose.")
        elif w["reject_rate"] > cfg["report"]["max_reject_rate"]:
            out.append(f"{_pct(w['reject_rate'], 0)} of checked tokens were rejected, which is very high. Thresholds may be too strict or data is missing.")
    n_min = cfg["weekly"]["min_n_per_week"]
    if a["n_filtered"] >= n_min and a["n_passed"] >= n_min and a["rug_filtered"] is not None and a["rug_passed"] is not None:
        if a["rug_filtered"] > a["rug_passed"]:
            out.append(f"The filters look useful so far: {_pct(a['rug_filtered'])} of rejected tokens collapsed within an hour, "
                       f"against {_pct(a['rug_passed'])} of passed tokens.")
        else:
            out.append(f"The filters are not separating collapses from passes yet ({_pct(a['rug_filtered'])} rejected vs "
                       f"{_pct(a['rug_passed'])} passed). Review the thresholds before trusting them.")
    e = a["edge"]
    if e["label"] == "Too few":
        out.append(f"Entry signals: not enough data to compare against the control group yet "
                   f"({e['n_signal']} signals and {e['n_control']} controls with a 15-minute result).")
    elif e["label"] == "Positive":
        out.append(f"Entry signals are ahead of the control group after costs ({_pct(e['signal_after'])} vs "
                   f"{_pct(e['control_after'])} at 15 minutes). Keep watching: one good stretch proves nothing.")
    else:
        out.append(f"Entry signals are not beating the control group after costs ({_pct(e['signal_after'])} vs "
                   f"{_pct(e['control_after'])} at 15 minutes).")
    if len(out) == 0:
        out.append("Nothing unusual this week.")
    return out


def gate_lines(data: dict, cfg: dict) -> list[tuple[str, str]]:
    w = cfg["weekly"]
    good = sum(1 for h in data["history"] if h["edge"]["label"] == "Positive")
    counted = sum(1 for h in data["history"] if h["edge"]["label"] != "Too few")
    return [
        ("Signals logged", f"{data['all']['signals']} of {w['target_signals']} wanted"),
        ("Weeks of testing", f"{data['weeks_elapsed']} of {w['test_weeks']} planned"),
        ("Weeks with a positive edge", f"{good} of {counted} weeks that had enough data"),
    ]


def scorecard_rows(data: dict) -> list[list[str]]:
    w, p, a = data["week"], data["prev"], data["all"]

    def r(label, key, fmt):
        return [label, fmt(w[key]), fmt(p[key]), fmt(a[key])]

    num = lambda x: "n/a" if x is None else str(x)  # noqa: E731
    pct = lambda x: _pct(x)  # noqa: E731
    rows = [
        r("Tokens checked", "evaluated", num),
        r("Tokens rejected", "rejected", num),
        r("Tokens passed", "passed", num),
        r("Entry signals", "signals", num),
        r("Rejection rate", "reject_rate", pct),
        r("Rejected tokens that collapsed within 1h", "rug_filtered", pct),
        r("Passed tokens that collapsed within 1h", "rug_passed", pct),
        r("Data-source error rate", "api_error_rate", pct),
        r("Scanner uptime", "uptime", pct),
    ]
    rows.append(["Signals vs control after costs (15 min)",
                 _edge_cell(w["edge"]), _edge_cell(p["edge"]), _edge_cell(a["edge"])])
    return rows


def _edge_cell(e: dict) -> str:
    if e["label"] == "Too few":
        return f"Too few ({e['n_signal']}/{e['n_control']})"
    return f"{e['label']} ({_pct(e['signal_after'])} vs {_pct(e['control_after'])})"


def _title(data: dict) -> str:
    return f"Weekly report: {data['start'].strftime('%a %d %b')} to {data['end'].strftime('%a %d %b %Y')} (UTC)"


def to_markdown(data: dict, cfg: dict) -> str:
    out = [f"# {_title(data)}", "", "SHADOW MODE: nothing here placed an order. Figures are measurements, not profit.", "",
           "## Reading this week in plain English", ""]
    out += [f"- {s}" for s in reading(data, cfg)]
    out += ["", "## Day by day", "", _table(
        ["Day", "Checked", "Rejected", "Passed", "Signals", "Uptime", "What happened"],
        [[d["date"].strftime("%a %d %b"), d["evaluated"], d["rejected"], d["passed"], d["signals"],
          _pct(d["uptime"], 0), day_note(d)] for d in data["days"]])]
    out += ["", "## Scorecard", "", _table(["Measure", "This week", "Last week", "All time"], scorecard_rows(data))]
    out += ["", "## Progress to the gates", "", _table(["Gate", "Progress"], [list(x) for x in gate_lines(data, cfg)])]
    if data["history"]:
        out += ["", "## Week-by-week edge (signals vs control after costs)", "", _table(
            ["Week ending", "Result", "Signals", "Controls"],
            [[datetime.fromtimestamp(h["until"] - 1, tz=timezone.utc).strftime("%d %b"), h["edge"]["label"],
              h["edge"]["n_signal"], h["edge"]["n_control"]] for h in data["history"]])]
    out += ["", "How to read it: a week is only counted as positive or not positive when it has "
            f"{cfg['weekly']['min_n_per_week']}+ signals and controls. The shadow test moves to paper trading only when the "
            "gates are met, not on a date.", ""]
    return "\n".join(out)


_CSS = """body{font-family:'Public Sans',Arial,sans-serif;background:#F6F4EE;color:#1B2536;margin:0;padding:32px 16px}
.wrap{max-width:980px;margin:0 auto}h1{font-family:Georgia,serif;font-size:30px;margin:0 0 6px}
h2{font-family:Georgia,serif;font-size:21px;margin:30px 0 10px}
.banner{background:#F28C38;color:#0F1B2D;padding:8px 14px;border-radius:8px;font-weight:700;display:inline-block;margin:8px 0 4px}
.card{background:#FFFDF8;border:1px solid #DDD8CB;border-radius:12px;padding:14px 18px}
table{border-collapse:collapse;width:100%;background:#FFFDF8;border:1px solid #DDD8CB;font-size:15px}
th{background:#1B2536;color:#F6F4EE;text-align:left;padding:8px 10px}td{padding:8px 10px;border-top:1px solid #E7E2D4;vertical-align:top}
.bar{height:12px;border-radius:4px;background:#2E6FB7}.up{background:#6FB1F0}ul{margin:6px 0 0 18px;padding:0}li{margin:5px 0}
.muted{color:#5B6676;font-size:14px}.pos{color:#2E6FB7;font-weight:700}.neg{color:#A8500A;font-weight:700}"""


def to_html(data: dict, cfg: dict) -> str:
    e = html.escape
    max_sig = max([d["signals"] for d in data["days"]] + [1])
    day_rows = "".join(
        f"<tr><td>{e(d['date'].strftime('%a %d %b'))}</td><td>{d['evaluated']}</td><td>{d['rejected']}</td>"
        f"<td>{d['passed']}</td><td>{d['signals']}<div class='bar' style='width:{int(100 * d['signals'] / max_sig)}px'></div></td>"
        f"<td>{e(_pct(d['uptime'], 0))}<div class='bar up' style='width:{int(100 * (d['uptime'] or 0))}px'></div></td>"
        f"<td>{e(day_note(d))}</td></tr>" for d in data["days"])
    score_rows = "".join("<tr>" + "".join(f"<td>{e(str(c))}</td>" for c in row) + "</tr>" for row in scorecard_rows(data))
    gates = "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td></tr>" for a, b in gate_lines(data, cfg))
    hist = "".join(
        f"<tr><td>{e(datetime.fromtimestamp(h['until'] - 1, tz=timezone.utc).strftime('%d %b'))}</td>"
        f"<td class='{'pos' if h['edge']['label'] == 'Positive' else 'neg' if h['edge']['label'] == 'Not positive' else ''}'>"
        f"{e(h['edge']['label'])}</td><td>{h['edge']['n_signal']}</td><td>{h['edge']['n_control']}</td></tr>"
        for h in data["history"])
    hist_block = (f"<h2>Week-by-week edge</h2><table><tr><th>Week ending</th><th>Signals vs control after costs</th>"
                  f"<th>Signals</th><th>Controls</th></tr>{hist}</table>") if hist else ""
    reading_li = "".join(f"<li>{e(s)}</li>" for s in reading(data, cfg))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(_title(data))}</title><style>{_CSS}</style></head><body><div class="wrap">
<h1>{e(_title(data))}</h1><div class="banner">SHADOW MODE: nothing here placed an order. Measurements, not profit.</div>
<h2>Reading this week in plain English</h2><div class="card"><ul>{reading_li}</ul></div>
<h2>Day by day</h2><table><tr><th>Day</th><th>Checked</th><th>Rejected</th><th>Passed</th><th>Signals</th><th>Uptime</th><th>What happened</th></tr>{day_rows}</table>
<h2>Scorecard</h2><table><tr><th>Measure</th><th>This week</th><th>Last week</th><th>All time</th></tr>{score_rows}</table>
<h2>Progress to the gates</h2><table><tr><th>Gate</th><th>Progress</th></tr>{gates}</table>
{hist_block}
<p class="muted">A week counts as positive or not positive only with {cfg['weekly']['min_n_per_week']}+ signals and controls. Paper trading starts when the gates are met, not on a date. All days are UTC.</p>
</div></body></html>"""


def build_weekly(db, cfg: dict, end: date | None = None, now: int | None = None) -> tuple[str, str, date]:
    import time as _time
    now = now or int(_time.time())
    end = end or datetime.fromtimestamp(now, tz=timezone.utc).date()
    data = collect(db, cfg, end, now)
    return to_markdown(data, cfg), to_html(data, cfg), end
