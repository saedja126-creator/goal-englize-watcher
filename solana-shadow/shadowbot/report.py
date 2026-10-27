"""Test A/B/C report straight from the log. Numbers only; warnings say when n is too small to conclude."""
from __future__ import annotations

import json
import statistics as st
import time

STAGES_ONCHAIN_PLUS = ("S2_ONCHAIN", "S3_OPTIONAL", "S4_STRATEGY")


def _since(hours: float | None) -> int:
    return int(time.time() - hours * 3600) if hours else 0


def _pct(x: float | None, nd: int = 1) -> str:
    return "n/a" if x is None else f"{x * 100:.{nd}f}%"


def _row(cells, widths):
    return "| " + " | ".join(str(c).ljust(w) for c, w in zip(cells, widths)) + " |"


def _table(headers: list[str], rows: list[list]) -> str:
    if not rows:
        return "_no data yet_"
    widths = [max(len(str(x)) for x in col) for col in zip(headers, *rows)]
    out = [_row(headers, widths), "|" + "|".join("-" * (w + 2) for w in widths) + "|"]
    out += [_row(r, widths) for r in rows]
    return "\n".join(out)


def test_a(db, cfg, since: int) -> tuple[str, list[str]]:
    warnings: list[str] = []
    calls = db.conn.execute(
        "SELECT source, COUNT(*) n, SUM(1-ok) errs, AVG(latency_ms) lat FROM api_calls WHERE ts>=? GROUP BY source",
        (since,)).fetchall()
    rows = []
    for c in calls:
        rate = (c["errs"] or 0) / c["n"]
        rows.append([c["source"], c["n"], c["errs"] or 0, _pct(rate), f"{c['lat']:.0f} ms" if c["lat"] else "n/a"])
        if rate > 0.05:
            warnings.append(f"API error rate for {c['source']} is {_pct(rate)} (target < 5%)")
    out = ["### Test A: plumbing", _table(["source", "calls", "errors", "error rate", "avg latency"], rows)]

    verdicts = db.conn.execute(
        "SELECT mint, MAX(CASE WHEN decision IN ('PASS','SIGNAL') THEN 1 ELSE 0 END) passed, "
        "MAX(CASE WHEN decision='FILTERED' THEN 1 ELSE 0 END) filtered FROM decisions WHERE ts>=? GROUP BY mint",
        (since,)).fetchall()
    passed = sum(1 for v in verdicts if v["passed"])
    rejected = sum(1 for v in verdicts if not v["passed"] and v["filtered"])
    total = passed + rejected
    rr = rejected / total if total else None
    out.append(f"\nTokens with a verdict: {total} (passed {passed}, rejected {rejected}); rejection rate {_pct(rr)}")
    if rr is not None and total >= 30:
        if rr < cfg["report"]["min_reject_rate"]:
            warnings.append(f"rejection rate {_pct(rr)} is below {_pct(cfg['report']['min_reject_rate'], 0)}: "
                            "the filter may be too loose or broken")
        if rr > cfg["report"]["max_reject_rate"]:
            warnings.append(f"rejection rate {_pct(rr)} is above {_pct(cfg['report']['max_reject_rate'], 0)}: "
                            "thresholds too strict or data missing")

    # completeness among passed tokens and decision latency
    rows_pass = db.conn.execute(
        "SELECT features FROM decisions WHERE decision IN ('PASS','SIGNAL') AND ts>=?", (since,)).fetchall()
    complete, ages = 0, []
    for r in rows_pass:
        f = json.loads(r["features"] or "{}")
        on = f.get("onchain") or {}
        if f.get("liq_usd") is not None and on.get("top10_pct_ex_largest") is not None:
            complete += 1
        if f.get("age_min") is not None:
            ages.append(f["age_min"])
    if rows_pass:
        comp = complete / len(rows_pass)
        out.append(f"Feature completeness on passed tokens: {_pct(comp)} (target > 95%)")
        if comp < 0.95:
            warnings.append(f"feature completeness {_pct(comp)} is below 95%")
    if ages:
        out.append(f"Token age at decision: median {st.median(ages):.1f} min (strategy window starts at 2 min)")

    cyc = db.conn.execute("SELECT AVG(overlap) o, AVG(discovered) d, AVG(new_pools) n, COUNT(*) c FROM cycles WHERE ts>=?",
                          (since,)).fetchone()
    if cyc and cyc["c"]:
        out.append(f"Discovery: {cyc['c']} cycles, avg {cyc['d'] or 0:.1f} pools/call, avg {cyc['n'] or 0:.1f} new/call, "
                   f"overlap with already-seen {_pct(cyc['o'])}")
        if cyc["o"] is not None and cyc["o"] < 0.05:
            warnings.append("discovery overlap is near 0%: the new-pools feed may be moving faster than we poll, "
                            "so coverage of new tokens is probably incomplete")
    return "\n".join(out), warnings


def _outcome_rows(db, since: int, decision_where: str, params: tuple, offset: int):
    return db.conn.execute(
        f"""SELECT d.id, d.decision, d.check_fired, d.price_usd p0, d.liq_usd l0, o.status, o.price_usd p1, o.liq_usd l1,
                   (SELECT o2.price_usd FROM outcomes o2 WHERE o2.decision_id=d.id AND o2.offset_s=30 AND o2.status='done') pe
            FROM decisions d JOIN outcomes o ON o.decision_id=d.id AND o.offset_s=?
            WHERE d.ts>=? AND {decision_where}""", (offset, since, *params)).fetchall()


def test_b(db, cfg, since: int) -> str:
    t = cfg["tracking"]
    groups = [("PASS/SIGNAL", "d.decision IN ('PASS','SIGNAL')", ())]
    for r in db.conn.execute(
            "SELECT DISTINCT check_fired FROM decisions WHERE decision='FILTERED' AND stage IN ('S2_ONCHAIN','S3_OPTIONAL') AND ts>=?",
            (since,)).fetchall():
        groups.append((f"FILTERED: {r['check_fired']}", "d.decision='FILTERED' AND d.check_fired=?", (r["check_fired"],)))
    rows = []
    for label, where, params in groups:
        data = _outcome_rows(db, since, where, params, 3600)
        done = [x for x in data if x["status"] in ("done", "missing")]
        if not done:
            continue
        rugged = missing = 0
        rets = []
        for x in done:
            if x["status"] == "missing":
                missing += 1
                continue
            p0, l0, p1, l1 = x["p0"], x["l0"], x["p1"], x["l1"]
            if (l0 and l1 is not None and l1 < (1 - t["rug_liquidity_drop"]) * l0) or \
               (p0 and p1 is not None and p1 < (1 - t["rug_price_drop"]) * p0):
                rugged += 1
            if p0 and p1:
                rets.append(p1 / p0 - 1)
        n = len(done)
        rows.append([label, n, _pct(rugged / n), _pct(missing / n), _pct(st.median(rets)) if rets else "n/a"])
    return "### Test B: filter validity (1h after the decision)\n" + _table(
        ["group", "n", "rugged", "missing", "median 1h move"], rows) + (
        "\n\nRead it as: filtered tokens should rug far more often than passed ones. "
        "'missing' = DexScreener no longer returns the pair (often a rug, sometimes an API gap).")


def test_c(db, cfg, since: int) -> tuple[str, list[str]]:
    friction = cfg["report"]["friction_pct"] / 100.0
    warnings: list[str] = []
    groups = [(f"SIGNAL {r['check_fired']}", "d.decision='SIGNAL' AND d.check_fired=?", (r["check_fired"],))
              for r in db.conn.execute("SELECT DISTINCT check_fired FROM decisions WHERE decision='SIGNAL' AND ts>=?",
                                       (since,)).fetchall()]
    groups.append(("CONTROL (passed, no trigger)", "d.decision='PASS'", ()))
    rows = []
    n_signals = db.conn.execute("SELECT COUNT(*) c FROM decisions WHERE decision='SIGNAL' AND ts>=?", (since,)).fetchone()["c"]
    for label, where, params in groups:
        for off in (300, 900, 3600):
            data = _outcome_rows(db, since, where, params, off)
            rets = []
            for x in data:
                if x["status"] != "done" or not x["p1"]:
                    continue
                entry = x["pe"] or x["p0"]  # +30s snapshot approximates entry delay
                if entry:
                    rets.append(x["p1"] / entry - 1)
            if not rets:
                continue
            pos = sum(1 for r in rets if r > 0) / len(rets)
            rows.append([label, f"+{off // 60}m", len(rets), _pct(st.mean(rets)), _pct(st.median(rets)), _pct(pos),
                         _pct(st.mean(rets) - friction)])
    out = ["### Test C: signal edge (forward price moves, NOT a simulated exit strategy)",
           _table(["group", "horizon", "n", "mean gross", "median gross", "% up", f"mean after {friction * 100:.0f}% friction"], rows),
           "\nEntry price = the +30s snapshot after the decision (approximate delay). A signal beats the control "
           "only if its after-friction mean is positive AND clearly above the control row."]
    need = cfg["report"]["min_signals_for_conclusion"]
    if n_signals < need:
        warnings.append(f"only {n_signals} signals logged; {need}+ needed before drawing conclusions "
                        "(100 trades still leaves about +/-10 percentage points on a win rate)")
    return "\n".join(out), warnings


def funnel_table(db, since: int) -> str:
    rows = db.conn.execute(
        "SELECT stage, decision, COALESCE(check_fired,'-') c, COUNT(*) n, COUNT(DISTINCT mint) m FROM decisions "
        "WHERE ts>=? GROUP BY stage, decision, c ORDER BY n DESC", (since,)).fetchall()
    return "### Funnel: every decision and the check that fired\n" + _table(
        ["stage", "decision", "check", "rows", "tokens"], [[r["stage"], r["decision"], r["c"], r["n"], r["m"]] for r in rows])


def build_report(db, cfg, hours: float | None = None) -> str:
    since = _since(hours)
    a, wa = test_a(db, cfg, since)
    c, wc = test_c(db, cfg, since)
    warnings = wa + wc
    head = f"# Shadow report ({time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())})\n"
    head += "SHADOW MODE: nothing here placed an order. Figures are measurements, not P&L.\n"
    warn = "\n### Warnings\n" + "\n".join(f"- {w}" for w in warnings) if warnings else "\n### Warnings\n- none"
    return "\n\n".join([head, funnel_table(db, since), a, test_b(db, cfg, since), c]) + "\n" + warn + "\n"
