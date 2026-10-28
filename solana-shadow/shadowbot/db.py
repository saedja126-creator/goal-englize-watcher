import json
import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS pools(
  mint TEXT PRIMARY KEY,
  pair_address TEXT,
  symbol TEXT,
  first_seen_ts INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT 'WATCH',          -- WATCH | DONE
  next_eval_ts INTEGER NOT NULL,
  last_decision TEXT,
  last_check TEXT
);
CREATE TABLE IF NOT EXISTS decisions(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts INTEGER NOT NULL,
  mint TEXT NOT NULL,
  symbol TEXT,
  stage TEXT NOT NULL,
  decision TEXT NOT NULL,                        -- PASS | SIGNAL | FILTERED | SKIP
  check_fired TEXT,
  reason_class TEXT,                             -- PERMANENT | RETRY_SHORT | RETRY_LONG
  reason_text TEXT,
  bench_until INTEGER,
  price_usd REAL,
  liq_usd REAL,
  features TEXT,
  model_version TEXT
);
CREATE INDEX IF NOT EXISTS ix_decisions_mint ON decisions(mint, ts);
CREATE INDEX IF NOT EXISTS ix_decisions_decision ON decisions(decision, check_fired);
CREATE TABLE IF NOT EXISTS outcomes(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  decision_id INTEGER NOT NULL,
  offset_s INTEGER NOT NULL,
  due_ts INTEGER NOT NULL,
  done_ts INTEGER,
  price_usd REAL,
  liq_usd REAL,
  status TEXT NOT NULL DEFAULT 'pending',        -- pending | done | missing | error
  UNIQUE(decision_id, offset_s)
);
CREATE INDEX IF NOT EXISTS ix_outcomes_status ON outcomes(status, due_ts);
CREATE TABLE IF NOT EXISTS api_calls(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts INTEGER NOT NULL,
  source TEXT NOT NULL,
  endpoint TEXT,
  ok INTEGER NOT NULL,
  status INTEGER,
  latency_ms INTEGER,
  error TEXT
);
CREATE INDEX IF NOT EXISTS ix_api_calls_ts ON api_calls(ts, source);
CREATE TABLE IF NOT EXISTS cycles(
  ts INTEGER NOT NULL,
  discovered INTEGER,
  new_pools INTEGER,
  evaluated INTEGER,
  overlap REAL
);
"""


class DB:
    def __init__(self, path: Path | str):
        if str(path) != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    # ---- pools -------------------------------------------------------
    def add_pool_if_new(self, mint: str, pair_address: str | None, symbol: str | None, now: int) -> bool:
        cur = self.conn.execute(
            "INSERT OR IGNORE INTO pools(mint, pair_address, symbol, first_seen_ts, next_eval_ts) VALUES(?,?,?,?,?)",
            (mint, pair_address, symbol, now, now),
        )
        self.conn.commit()
        return cur.rowcount == 1

    def is_known_mint(self, mint: str) -> bool:
        return self.conn.execute("SELECT 1 FROM pools WHERE mint=? LIMIT 1", (mint,)).fetchone() is not None

    def source_calls_since(self, source: str, since_ts: int) -> int:
        row = self.conn.execute("SELECT COUNT(*) AS n FROM api_calls WHERE source=? AND ts>=?", (source, since_ts)).fetchone()
        return int(row["n"])

    def due_pools(self, now: int, limit: int) -> list[sqlite3.Row]:
        return self.conn.execute(
            "SELECT * FROM pools WHERE status='WATCH' AND next_eval_ts<=? ORDER BY next_eval_ts LIMIT ?",
            (now, limit),
        ).fetchall()

    def update_pool(self, mint: str, *, next_eval_ts: int, status: str, last_decision: str | None, last_check: str | None,
                    symbol: str | None = None) -> None:
        self.conn.execute(
            "UPDATE pools SET next_eval_ts=?, status=?, last_decision=?, last_check=?, symbol=COALESCE(?, symbol) WHERE mint=?",
            (next_eval_ts, status, last_decision, last_check, symbol, mint),
        )
        self.conn.commit()

    # ---- decisions / outcomes ---------------------------------------
    def add_decision(self, *, ts: int, mint: str, symbol: str | None, stage: str, decision: str,
                     check_fired: str | None, reason_class: str | None, reason_text: str,
                     bench_until: int | None, price_usd: float | None, liq_usd: float | None,
                     features: dict, model_version: str | None = None) -> int:
        cur = self.conn.execute(
            """INSERT INTO decisions(ts, mint, symbol, stage, decision, check_fired, reason_class, reason_text,
                                     bench_until, price_usd, liq_usd, features, model_version)
               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (ts, mint, symbol, stage, decision, check_fired, reason_class, reason_text, bench_until,
             price_usd, liq_usd, json.dumps(features, default=str), model_version),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def schedule_outcomes(self, decision_id: int, ts: int, offsets: list[int]) -> None:
        self.conn.executemany(
            "INSERT OR IGNORE INTO outcomes(decision_id, offset_s, due_ts) VALUES(?,?,?)",
            [(decision_id, off, ts + off) for off in offsets],
        )
        self.conn.commit()

    def pending_outcomes(self, now: int, limit: int = 300) -> list[sqlite3.Row]:
        return self.conn.execute(
            """SELECT o.*, d.mint FROM outcomes o JOIN decisions d ON d.id=o.decision_id
               WHERE o.status='pending' AND o.due_ts<=? ORDER BY o.due_ts LIMIT ?""",
            (now, limit),
        ).fetchall()

    def finish_outcome(self, outcome_id: int, *, status: str, now: int, price_usd: float | None, liq_usd: float | None) -> None:
        self.conn.execute(
            "UPDATE outcomes SET status=?, done_ts=?, price_usd=?, liq_usd=? WHERE id=?",
            (status, now, price_usd, liq_usd, outcome_id),
        )
        self.conn.commit()

    def recent_signal(self, mint: str, strategy: str, since_ts: int) -> bool:
        row = self.conn.execute(
            "SELECT 1 FROM decisions WHERE mint=? AND decision='SIGNAL' AND check_fired=? AND ts>=? LIMIT 1",
            (mint, strategy, since_ts),
        ).fetchone()
        return row is not None

    # ---- api accounting ----------------------------------------------
    def log_api_call(self, *, ts: int, source: str, endpoint: str, ok: bool, status: int | None,
                     latency_ms: int | None, error: str | None) -> None:
        self.conn.execute(
            "INSERT INTO api_calls(ts, source, endpoint, ok, status, latency_ms, error) VALUES(?,?,?,?,?,?,?)",
            (ts, source, endpoint, int(ok), status, latency_ms, error),
        )
        self.conn.commit()

    def rpc_calls_since(self, since_ts: int) -> int:
        row = self.conn.execute(
            "SELECT COUNT(*) AS n FROM api_calls WHERE source='rpc' AND ts>=?", (since_ts,)
        ).fetchone()
        return int(row["n"])

    def log_cycle(self, ts: int, discovered: int, new_pools: int, evaluated: int, overlap: float | None) -> None:
        self.conn.execute(
            "INSERT INTO cycles(ts, discovered, new_pools, evaluated, overlap) VALUES(?,?,?,?,?)",
            (ts, discovered, new_pools, evaluated, overlap),
        )
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()
