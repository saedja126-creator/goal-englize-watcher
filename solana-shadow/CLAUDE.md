# Solana shadow desk: instructions for a local Claude Code session

> **Current state and plan: read `docs/FINAL_SUMMARY.md` first.** The setup steps below were written before the real-sample check; the summary is newer (56 tests, watchdog, weekly Telegram notice, risk preset B applied: 10% position, up to 2% risk, 15% daily limit capped at £30).

You are running on the user's own PC, with normal internet access. A previous cloud session wrote this project but
could NOT reach the market-data APIs, so the parsers are untested against real responses. Your job is to finish setup,
verify against real data, and start the shadow run.

## Hard rules
- SHADOW MODE ONLY. Never place an order, never create or ask for a wallet, private key or seed phrase.
- Secrets live only in `.env` (git-ignored). Never print, log, echo or commit a key. Ask the user to paste their
  Helius key into `.env` themselves; do not have them paste it into chat.
- Don't change thresholds in `thresholds.toml` without telling the user what and why.
- Don't promise returns. The user is UK-based and thinks in GBP. Realistic framing: the shadow test measures whether the
  rules have any edge; most likely outcome of a first version is flat to negative after costs.
- Ask before installing anything system-wide (e.g. Python). Use a virtual environment for packages.

## Steps
1. Check `python --version` is 3.11+ (tomllib is required). If missing, tell the user how to install it.
2. In `solana-shadow/`: `python -m venv .venv`, activate, `pip install -r requirements.txt`.
3. Run `python -m unittest discover -s tests -v` (all tests should pass: 57 at last count).
4. Copy `.env.example` to `.env`; ask the user to paste their free Helius key after `HELIUS_API_KEY=` and tell you when done.
5. Run `python -m shadowbot doctor`. Read `samples/*.json` (real responses, no keys inside).
6. Compare real shapes with the parsers in `shadowbot/sources.py` (GeckoTerminal new_pools, DexScreener
   `tokens/v1/solana/{mints}`), `shadowbot/solana_rpc.py` (getAccountInfo jsonParsed, getTokenLargestAccounts) and
   `shadowbot/optional_checks.py` (RugCheck, Jupiter). Fix any mismatch, then add a test that uses a trimmed real sample.
7. Run `python -m shadowbot run --once`, check `data/shadow.db` has sensible rows, then start it with `python -m shadowbot start`
   (background, no window; `status` and `stop` manage it; log in `data/run.log`). If a visible scanner window is already running
   from an older version, stop it with Ctrl+C first, then `start`: state lives in SQLite, so nothing is lost. Tell the user to
   keep the PC awake. The Windows branch of start/stop is untested: check it once with `status` and a test stop/start.
8. After a few hours, run `python -m shadowbot report` and explain Test A first (plumbing), in plain English.
9. Weekly: the run loop writes `reports/weekly-DATE.html` on Sunday evenings (UTC); `python -m shadowbot weekly` makes one on demand.
   Each week open it with the user and walk through it in plain English: day by day, then the scorecard, then the gates.
   The user wants a weekly view only (no daily pings). The shadow phase is planned for about 12 weeks (`[weekly]` in
   `thresholds.toml`); paper trading starts only when the gates are met (200+ signals and a positive edge over the control
   group across several weeks), not on a date. Paid data is considered only after the shadow phase, for a specific question
   the free data raised.

## Known unverified items (check these first)
- GeckoTerminal new_pools: base token id format (`solana_<mint>`), `pool_created_at`, and how many pools per page vs how
  fast new pools arrive (the report's discovery overlap number shows coverage gaps).
- DexScreener `tokens/v1/solana/{addresses}`: returns a list of pairs; field names `pairCreatedAt`, `txns.m5`, `volume.m5/h1`,
  `liquidity.usd`; rate limits.
- Helius RPC URL format `https://mainnet.helius-rpc.com/?api-key=KEY`, and free-plan limits (credits per month).
- Whether the "largest account = pool vault" assumption in `holder_concentration` holds for pump-style launches.
- RugCheck summary fields and Jupiter quote params are optional and off by default.

## Not built yet
Dev-wallet %, LP lock/burn status (logged as missing, never treated as safe), the paper-trading executor with a live price
loop and stop/trailing exits, one-position-at-a-time rule, Telegram digest. Build these only after shadow data justifies it.

## Project map
`shadowbot/funnel.py` stages and reason classes; `runner.py` one cycle; `report.py` Tests A/B/C; `thresholds.toml` all
thresholds; `README.md` user-facing steps.

## Risk engine (built, not yet connected to any executor)
`shadowbot/risk.py` holds the slice ladder, hard limits and step-up rule (settings in `[risk]`). When the paper executor is
built it MUST call `RiskEngine.allow_order(...)` before every order and `on_open`/`on_close` around every trade, in `paper`
mode first. Never bypass it, never auto-reset a halt, and never raise the slice without the user typing
`python -m shadowbot stepup --confirm`. Paid data (about 2 months from the 15th of the first paper month) is a controlled
A/B: run a free-data arm and a free-plus-paid arm on the same tokens, and compare after costs.

