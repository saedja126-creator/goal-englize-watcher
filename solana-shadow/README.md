# Solana shadow desk (Phase 0 + 1)

Scans new Solana pairs, filters them with hard facts in code, logs **every** decision with the check that fired,
and records what each token did afterwards. **It never trades and never touches a wallet.** The goal is to find out,
with data and at no capital risk, whether the video's rules have any edge.

## Fastest route: let Claude Code on your PC do it

Open Claude Code in an empty folder and paste:

> Clone https://github.com/saedja126-creator/goal-englize-watcher, check out branch `claude/solana-shadow`, read
> `solana-shadow/CLAUDE.md`, and follow it step by step.

You only need a free Helius key. Paste it into the `.env` file yourself when asked, not into the chat.

## Setup by hand (about 30 minutes)

1. Install **Python 3.11 or newer** (python.org). On Windows tick "Add Python to PATH".
2. Create a free **Helius** account (helius.dev) and copy your API key.
3. In a terminal, inside this folder:

   ```
   python -m venv .venv
   # Windows:  .venv\Scripts\activate        Mac/Linux:  source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and paste your Helius key after `HELIUS_API_KEY=`. Never share or commit `.env`.
5. Run the checks:

   ```
   python -m shadowbot doctor
   ```
   It tests every API and saves raw sample responses to `samples/` (no keys inside). **If anything says FAIL, send me the
   output and the files in `samples/`.** The parsers were written without live access to these APIs, so this is the
   step that confirms them.
6. Start the shadow run in the background (no window, survives closing PowerShell): `python -m shadowbot start`.
   Check on it any time with `python -m shadowbot status` (is it running, when it last scanned, the latest log lines)
   and stop it with `python -m shadowbot stop`. The log is `data/run.log`; crashes go to `data/run.err`.
   (`python -m shadowbot run` still works if you want to watch it in a window. Only one scanner can run at a time.)
   Turn off computer sleep while it runs. On Windows, in PowerShell: `powercfg /change standby-timeout-ac 0`.
   The background mode survives closing the window, not a restart or log-off: run `start` again after a reboot.
7. **Weekly report (the one to read):** every Sunday evening (UTC) the running scanner writes `reports/weekly-DATE.html`.
   Open it in your browser. You can also make one any time with `python -m shadowbot weekly` (add `--end 2026-11-08`
   for a specific week). It has a plain-English summary, a day-by-day table, a this-week vs last-week scorecard and a
   progress-to-the-gates tracker.
8. For the technical view at any time: `python -m shadowbot report` (or `--hours 24`). It writes `reports/latest.md`.

Run the tests anytime: `python -m unittest discover -s tests -v`.

## Optional Telegram notices

If `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are in `.env`: the watchdog messages you when the scanner is down and cannot be restarted (and when it is back), and the running scanner sends a short notice with a 3-line summary when the Sunday weekly report is written. Never paste the token into a chat.

## What it does each cycle (every 30s)

1. **Discover** new pools (GeckoTerminal) and add unseen tokens to a watch list.
2. **Evaluate** tokens whose bench has expired, cheapest check first:
   `S1` age/liquidity/activity (free) -> `S2` mint & freeze authority, token-2022 permanent delegate, holder
   concentration (Solana RPC) -> `S3` optional RugCheck/Jupiter (off by default) -> `S4` entry triggers.
3. **Log** one row per decision (`PASS`, `SIGNAL`, `FILTERED`, `SKIP`) with reason class and bench time.
4. **Track** price and liquidity at +30s, +5m, +15m, +1h after each tracked decision.

Bench rules: a permanent reason (e.g. permanent delegate) never retries; "too young" retries exactly when it becomes
tellable; on-chain rejections retry after 2 hours; a passed token is rechecked every 30 minutes.

## Reading the report

| Section | Question it answers | Good looks like |
|---|---|---|
| Test A | Is the plumbing sound? | API errors < 5%, features > 95% complete, rejection rate not near 0% or 100% |
| Test B | Do the filters work? | FILTERED tokens rug far more often than PASS/SIGNAL tokens |
| Test C | Does an entry trigger have an edge? | A SIGNAL group beats the CONTROL group after friction, with 100+ signals |

Test C reports forward price moves, **not** a simulated exit strategy. Rules with stops and trailing exits come in the
paper-trading phase. Until 100+ signals exist the report says so; even then 100 trades only rules out a disaster.

## Limits to know

- All thresholds are in `thresholds.toml`: they are starting proposals, not proven numbers.
- Dev-wallet % and LP-lock status are **not** checked yet: they need the token creator and LP-holder data. They are
  logged as missing, not treated as safe. RugCheck can fill part of this once `doctor` confirms its fields.
- "Top holders" excludes only the single largest account (assumed to be the pool vault). Raw numbers are logged too.
- Shadow mode logs every signal; the one-position-at-a-time rule applies from the paper phase.
- Free-tier limits: the RPC budget is capped by `daily_rpc_budget`. Check your Helius plan limits on their site.
- Discovery uses a feed that returns only the newest pools per call, so coverage of brand-new tokens may be incomplete.
  The report shows the overlap number so you can see whether that is happening.

## The slice ladder (how money is controlled later)

Live money, when it comes, goes through `shadowbot/risk.py`. The numbers live in `thresholds.toml` under `[risk]`:
slice steps in pounds (200, 350, 500, 1000), 7% maximum position, 1% risk per trade, 5% daily loss limit, 30% project stop,
position capped at 1% of the pool's liquidity, one position at a time.

- `python -m shadowbot slices` prints the ladder in pounds (the same table as the presentation).
- `python -m shadowbot risk-status` shows paper and live state, any halt, and whether a step-up is allowed.
- `python -m shadowbot stepup` shows why you can't step up yet; `--confirm` applies it, only if the rule passes
  (4+ live weeks, 30+ trades, stop never touched, live average trade positive and within 3 points of paper).
- A daily-loss or project-stop halt **stays on until you reset it**. A restart or a new day does not clear it.
- Set `usd_per_gbp` in `[risk]` to the live rate; it is only used for the pool-liquidity cap.

Nothing places orders yet. The paper trading executor (next phase) must call `RiskEngine.allow_order` before every order.

