# Shadow Desk: project summary

As of 28 Oct 2026. Repo: `saedja126-creator/goal-englize-watcher`, branch `claude/solana-shadow`, folder `solana-shadow/`.

## What it is
A **shadow-mode scanner** for brand-new Solana tokens. It filters them with hard facts in code, logs every decision with the
check that fired, and records what each token did afterwards. It exists to answer one question at **zero capital risk**:
do the rules from the video (new-pair buy-heavy flow, volume spikes, rug filters) have any edge after costs?

It **never trades, has no wallet, and never asks for a private key.**

## Status

| Component | Built | Tested | Caveat |
|---|---|---|---|
| Scanner, funnel, logger, outcome tracker | Yes | Logic tests plus trimmed **real** samples | Real GeckoTerminal, DexScreener and RPC shapes were captured on the user's PC on 27 Oct 2026 and the parsers pass on them. Coverage of new tokens and free-tier credit use are still unreviewed |
| `doctor` command (checks every API, saves samples) | Yes | Run for real on the PC (27 Oct) | Fixed 28 Oct: the holder check now tests a brand-new token, because the RPC refuses wrapped SOL (millions of holders) |
| Watchdog (`python -m shadowbot watch`) | Yes (built by Claude Code on the PC) | Unit tests | Restarts a dead or stuck scanner; alerts by PC pop-up and optional Telegram only if the restart fails; meant for a Windows scheduled task at login and every 15 minutes |
| Weekly report (Markdown + HTML) | Yes | Synthetic data | Not seen on real data yet |
| Risk engine (slice ladder, halts, step-up rule) | Yes | Unit tests | Not connected to any executor yet |
| Background mode (`start`, `status`, `stop`) | Yes | Linux tests pass | **Windows branch untested** |
| Presentation (18 slides) | Yes | Standalone copy rendered and checked | https://claude.ai/artifact/3U9QE1hLhyzLipnj3b4t44 ; offline copy: `docs/Shadow_Desk_presentation.html` |
| Paper-trading executor | **No** | | Next phase |
| Wallet-copy ("Spy") strategy | **No** | | Needs a free wallet-list source |
| Paid-data A/B arm | **No** | | Comes with paper phase |
| Dev-wallet % and LP-lock checks | **No** | | Logged as missing, never treated as safe |

## How it works (every 30 seconds)
1. **Discover** new pools (GeckoTerminal) and add unseen tokens to a watch list.
2. **Evaluate** tokens whose bench has expired, cheapest check first:
   - `S1` free cut: age, liquidity, activity.
   - `S2` on-chain facts (Helius RPC): mint authority, freeze authority, token-2022 permanent delegate, holder concentration.
   - `S3` optional enrichment (RugCheck, Jupiter sell route): off by default.
   - `S4` entry triggers: `new_pair_flow` and `volume_spike` produce a SIGNAL; everything else that passes is a PASS (the control group).
3. **Log** one row per decision (`PASS`, `SIGNAL`, `FILTERED`, `SKIP`) with reason class and bench time.
4. **Track** price and liquidity at +30s, +5m, +15m, +1h after each tracked decision.

Bench rules: permanent reasons never retry; "too young" retries exactly when tellable; on-chain rejections retry after 2 hours;
passed tokens are rechecked every 30 minutes.

## Commands (run inside `solana-shadow/`, with the virtual environment active)

| Command | Purpose |
|---|---|
| `python -m shadowbot doctor` | Check setup and every API; saves raw samples to `samples/` |
| `python -m shadowbot start` | Start the scanner in the background (no window) |
| `python -m shadowbot status` | Running? last scan? tokens checked in 24h? latest log lines |
| `python -m shadowbot stop` | Stop the background scanner |
| `python -m shadowbot watch` | Check the scanner; restart it if dead or stuck; alert only if the restart fails |
| `python -m shadowbot run [--once]` | Run in the foreground |
| `python -m shadowbot weekly [--end YYYY-MM-DD]` | Weekly report to `reports/weekly-DATE.html` (also written Sunday evenings, UTC) |
| `python -m shadowbot report [--hours N]` | Technical report (Tests A, B, C) |
| `python -m shadowbot slices` | The slice ladder in pounds |
| `python -m shadowbot risk-status` | Paper and live risk state, halts, step-up eligibility |
| `python -m shadowbot stepup [--confirm]` | Show or apply a step-up (needs the rule to pass AND `--confirm`) |

Files written on the PC: `data/shadow.db` (all state), `data/run.log`, `data/run.err`, `reports/`, `samples/`. The Helius key
lives only in `.env` (git-ignored).

## Settings (all in `thresholds.toml`, all proposals to tune from data)
- Stage 1: age 2–360 min, liquidity at least $5,000, at least 5 transactions in 5 min.
- Stage 2: reject if mint or freeze authority is open; top-10 holders (excluding the largest account) over 50%; biggest other holder over 20%.
- Strategies: `new_pair_flow` (age 2–15 min, buy ratio 70%+, liquidity $10k+) and `volume_spike` (3× the hourly pace, age 15–360 min).
- Report: 4% assumed round-trip friction; weekly gates target 200 signals over 12 weeks.
- Risk ladder (pounds): slices £200, £350, £500, £1,000; 7% max position; 1% risk per trade; 5% daily loss limit; 30% project stop;
  position under 1% of pool liquidity; one position at a time; `usd_per_gbp = 1.30` (update to the live rate).

## Risk engine rules
- Every order must pass `RiskEngine.allow_order` (smallest of the position, risk and liquidity caps; refuses a second position).
- Daily-loss and project-stop halts **persist until a person resets them**. A restart or a new day does not clear them.
- Step-up needs: 4+ live weeks, 30+ trades, stop never touched, live average trade positive and within 3 points of paper, AND an
  explicit `--confirm`. The bot never raises its own slice.

## Safety rules
- Shadow mode only until the gates are met. No wallet, no keys.
- Never paste the Helius key into any chat. It goes in `.env` only, as do the optional Telegram token and chat id for the watchdog.
- Later, a separate burner wallet holding only the live amount, never a main wallet.

## Known unverified items
- Whether the new-pools feed moves faster than 30-second polling (the report shows an overlap number). The response shape itself matched on 27 Oct.
- DexScreener rate limits (field names matched the real sample).
- Helius free-plan credit limits and real daily usage (sources conflict: 1M vs 500K credits). The RPC URL format works.
- Whether the "largest account is the pool vault" assumption holds broadly: one real pump-style sample showed the bonding curve as the largest account (about 93%), which supports it.
- All API prices (Helius, Jupiter, RugCheck, Birdeye, Nansen) came from search snippets, not official pages.
- GBP/USD rate: no reliable live figure found (about 1.25–1.34 in stale sources).

## Tests
Run `python -m unittest discover -s tests -v` (stdlib only). 55 tests. Most use synthetic data and prove the logic; `tests/test_real_samples.py` uses trimmed real responses captured on 27 Oct 2026.
