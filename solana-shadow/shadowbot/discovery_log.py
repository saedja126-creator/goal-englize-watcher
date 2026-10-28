"""Per-cycle record of how many discovery pages were read.

Kept in its own small file (data/discovery_pages.jsonl, one JSON line per cycle) so the main database is not changed.
Never raises: a logging problem must not stop the scanner.
"""
from __future__ import annotations

import json
from pathlib import Path

from . import background


def path() -> Path:
    return background.data_dir() / "discovery_pages.jsonl"


def append(ts: int, stats: dict, file: Path | None = None) -> None:
    try:
        f = file or path()
        f.parent.mkdir(parents=True, exist_ok=True)
        line = {"ts": ts, "pages": stats.get("pages", 0), "needed_extra": bool(stats.get("needed_extra")),
                "hit_limit": bool(stats.get("hit_limit")), "stopped": stats.get("stopped")}
        with open(f, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(line) + "\n")
    except OSError:
        pass


def summary(since: int, until: int, file: Path | None = None) -> dict:
    """Counts for cycles with since <= ts < until. All zero when there is no file yet."""
    out = {"cycles": 0, "needed_extra": 0, "hit_limit": 0, "stopped": 0, "pages": 0}
    try:
        text = (file or path()).read_text(encoding="utf-8")
    except OSError:
        return out
    for raw in text.splitlines():
        try:
            row = json.loads(raw)
            ts = int(row["ts"])
        except (ValueError, KeyError, TypeError):
            continue
        if not since <= ts < until:
            continue
        out["cycles"] += 1
        out["pages"] += int(row.get("pages") or 0)
        out["needed_extra"] += 1 if row.get("needed_extra") else 0
        out["hit_limit"] += 1 if row.get("hit_limit") else 0
        out["stopped"] += 1 if row.get("stopped") else 0
    return out
