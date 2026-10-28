# FINAL SUMMARY: Shadow Desk (hand this file to a new Claude Code session)

Version of 28 Oct 2026. Read this first, then `MASTER_PLAN.md` (the full plan) if you need detail. Nothing here is a forecast or a promise of returns.

## 1. The user and the rules
UK-based, thinks in pounds, not technical, works in sports media and social strategy. Wants plain English, honesty over hype, tables, **weekly** reports only, and every payment explained (what, when, how). Gets frustrated by vagueness and by being asked permission for changes already agreed.

1. Never promise returns. The most likely outcome of a first version is flat to negative after costs.
2. **Shadow mode only** until the gates are met: no orders, no wallet, no keys.
3. Never ask for or print a private key, seed phrase, API key, Telegram token or card number. Keys live only in `.env`.
4. Label facts as verified or not. All prices and tool features are third-party and unconfirmed.
5. Do not change `thresholds.toml` without telling the user what and why.

## 2. Where we are (28 Oct 2026)
| Item | State |
|---|---|
| Scanner, filters, logger, outcome tracker, weekly report, risk engine, background mode, watchdog, weekly Telegram notice | **Built.** 56 tests pass |
| Real API shapes (GeckoTerminal, DexScreener, RPC) | Checked on the user's PC on 27 Oct; parsers pass real samples |
| Scanner running since 27 Oct? | **Unconfirmed.** Nobody has seen `status`, collected data or a weekly report |
| Windows background mode and watchdog task over several days | Unverified |
| Telegram | Optional; setup status unknown |
| Paper executor, Spy (wallet-copy) strategy, paid-data A/B arm, dev-wallet/LP-lock checks, calendar reminders, loss-limit alerts | **Not built** |
| Presentation | 23 slides. Live: https://claude.ai/artifact/3U9QE1hLhyzLipnj3b4t44. Offline: `docs/Shadow_Desk_presentation.html`. Source: `docs/presentation-source/` |

## 3. The plan (gates decide, not dates)
| Date | What | Money |
|---|---|---|
| Tue 27 Oct 2026 | Shadow test starts; weekly report Sunday evening UTC (first Sun 1 Nov) | £0 |
| 9 Nov – 6 Dec | Build the Spy strategy in shadow mode | £0 |
| Tue 26 Jan 2027 | Decision day: stop, revise or continue (needs 200+ signals and a positive edge over the control group across several weeks) | £0 |
| Wed 27 Jan | Paper trading starts, free data only | £0 |
| Mon 15 Feb | Rung 1: Birdeye Pro, one month, A/B test | about £7 ($9) |
| Mon 15 Mar | Rung 2: Nansen Pro, monthly, only if rung 1 helped but was too limited | about £51 ($69) |
| About Mon 29 Mar | Live £200, only if the paper gate is met | £200 |
| About Tue 27 Apr | First step-up check (£350): 4 live weeks, 30+ trades, stop untouched | up to £350 |
| May – Oct | Scale to the £500 cap; £1,000 much later | up to £500 |
| 27 Oct 2027 | 12-month review | n/a |

Data worst case about £58 (under a £100 cap); live money capped at £500. Live money goes to a **separate burner Solana wallet** funded from a UK exchange (exchange, wallet app, SOL vs USDC decided at month 5; my lean USDC). Never the main wallet. Each swap may be a taxable disposal (UK; not tax advice).

## 4. What we are adapting (new on 28 Oct)
| Topic | Before | Now | Status |
|---|---|---|---|
| Daily loss accepted | £10 (5%) | up to £30 a day | **User must choose preset A, B or C** |
| One position | £14 (7%) | £20 (B) or £30 (C) | same choice |
| Project stop | −30% (£60) | unchanged | decided |
| Paid data | £100 up front | ladder: about £7, then about £51 only if it helps | decided |
| Alerts | watchdog only | weekly Telegram notice added | built |
| Strategy | shadow test first | unchanged after an evidence check | decided |

**Why:** the user said "I don't want smaller wins. I don't mind if I lost up to £30 in one day." That is a tolerance, not an edge: bigger positions scale wins and losses equally, and only the win rate decides which wins. Web search found nothing that clearly beats testing for free first (retail day trading mostly loses; memecoin wallets mostly lose; staking and USDC lending about 4–7% a year; figures third-party).

| Preset (£200 slice) | Position | Risk per trade | Daily limit | Rugs to hit daily limit | Rugs to hit −£60 stop | Month at 45% / 35% win rate |
|---|---|---|---|---|---|---|
| A (current code) | 7% = £14 | 1% | 5% = £10 | 1 | 5 | +21% / −24% |
| **B (my lean)** | 10% = £20 | 2% | 15% = £30 | 2 | 3 | +31% / −33% |
| C | 15% = £30 | 2.5% | 15% = £30 | 1 | 2 | +50% / −45% |

Assumptions: 14% stop, 30% average win, 5 trades a day, 4% friction. Illustrative. In the 35% case B and C hit the project stop inside the month. Rug counts follow the code (a limit trips at equity ≤ limit), which corrects an earlier chat message that said 4 and 3.

**To apply the user's choice** (only after they answer; tell them what changed): set in `thresholds.toml` `[risk]`:

| Preset | position_pct | risk_per_trade_pct | daily_loss_limit_pct | project_stop_pct |
|---|---|---|---|---|
| A | 7 | 1.0 | 5 | 30 |
| B | 10 | 2.0 | 15 | 30 |
| C | 15 | 2.5 | 15 | 30 |

Then update `tests/test_risk.py` (it assumes the 5% daily limit, e.g. a −£10 day on £200 trips DAILY_LOSS), run all tests, regenerate `python -m shadowbot slices`, and update MASTER_PLAN section 5 and the slides.

## 5. First actions for Claude Code (in order)
1. `git pull` on branch `claude/solana-shadow`; in `solana-shadow/` run `python -m unittest discover -s tests -v` (expect 56 pass).
2. `python -m shadowbot status`. If not RUNNING: `python -m shadowbot start`. Confirm the scanner has collected since 27 Oct; if it started later, every date shifts.
3. Run `python -m shadowbot report`; explain Test A (plumbing) to the user in plain English. Flag coverage and error rates.
4. Check the Windows watchdog task (`python -m shadowbot watch` at login and every 15 minutes) and that the PC stays awake.
5. Ask whether the user wants Telegram (optional; token and chat id go in `.env`, never in chat).
6. Ask the user to pick preset A, B or C by Mon 9 Nov, then apply section 4.
7. Sun 1 Nov: the first weekly report (`reports/weekly-2026-11-01.html`). Expect "too early to conclude".
8. 9 Nov onward: Spy strategy (needs a free wallet list; GMGN rankings proposed).

## 6. Open inputs from the user
Scanner running since 27 Oct and `status` output; Telegram yes/no; calendar reminders yes/no; preset A/B/C; three book titles; free wallet list source; £500 cap with £200 first; live GBP/USD rate; exchange, wallet app and SOL vs USDC (month 5).

## 7. The presentation: how it moves between sessions
- The artifact is private to the user's claude.ai account. A new Claude Code session on **the same account** can read and update it by URL (Artifact tool: `read`, then publish to the same URL with the downloaded folder as `root`).
- It cannot be pushed into a PC from the cloud. The repo carries everything: `docs/presentation-source/` (deck.json, 23 slide files, builder) and the offline HTML. Rebuild the HTML with `python3 -I docs/presentation-source/build_deck_html.py docs/presentation-source docs/Shadow_Desk_presentation.html`.
- On another account: create an Artifact from the Slides type (`type_url` https://claude.ai/artifact/8jTsAFQMFDb2oA8MsPJ2eL) and publish `project/deck.json` plus `project/slides/*.html`.
- Slide text is also in `MASTER_PLAN.md` Appendix A.

## 8. File map
| File | Purpose |
|---|---|
| `docs/FINAL_SUMMARY.md` | this file |
| `docs/MASTER_PLAN.md` | the full plan (sections 0–13, Appendix A = 23 slides) |
| `docs/PROJECT_SUMMARY.md` | what is built and its caveats |
| `docs/CONVERSATION_SUMMARY.md` | how we got here |
| `docs/PLAN.md` | shorter plan |
| `docs/presentation-source/` | slide source and builder |
| `thresholds.toml` | all thresholds; `[risk]` holds the limits |
| `shadowbot/` | scanner code; `risk.py` risk engine (must gate every order; never auto-reset a halt; never raise the slice without `stepup --confirm`) |
| `CLAUDE.md` | setup steps for a local session |

Commands (inside `solana-shadow/`, venv active): `status`, `start`, `stop`, `watch`, `weekly`, `report`, `slices`, `risk-status`, `stepup [--confirm]`, `doctor`, `python -m unittest discover -s tests -v`.
