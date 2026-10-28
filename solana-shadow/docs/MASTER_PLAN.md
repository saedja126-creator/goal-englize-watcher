# MASTER PLAN: Shadow Desk (Solana memecoin scanner)

Version of 28 Oct 2026. One file with everything: what to do now, the dated calendar, what every payment is for, what to expect,
what pings you, the rules, and the full content of the presentation. Nothing here is a forecast or a promise of returns.

---

## 0. For a new chat or workflow: read this first

**The user:** UK-based, thinks in pounds, not technical, works in sports media and social strategy. Wants plain English, honesty over
hype, tables, and a **weekly** report only (never daily pings). Gets frustrated by vague plans: every payment must say what it is for,
when it starts, and how it is paid.

**What exists (all of it is already built; do not rebuild):**

| Thing | Where |
|---|---|
| Code, tests, docs | GitHub repo `saedja126-creator/goal-englize-watcher`, branch `claude/solana-shadow`, folder `solana-shadow/` |
| The presentation (20 slides) | https://claude.ai/artifact/3U9QE1hLhyzLipnj3b4t44 (private; opens and can be edited from the same claude.ai account; a chat on that account can read and update it by this URL) |
| Offline copy of the presentation | `solana-shadow/docs/Shadow_Desk_presentation.html` (open in a browser; arrow keys; Ctrl+P, Save as PDF) |
| Other documents | `docs/PROJECT_SUMMARY.md` (what is built), `docs/CONVERSATION_SUMMARY.md` (how we got here), `docs/PLAN.md` (shorter plan) |

**Moving the presentation:** an artifact cannot be copied to another account. Within the same account the link above is enough: any
chat can read it and update it. Appendix A of this file also holds every slide's content as text, so it can be recreated anywhere.

**Rules for any assistant using this file:**
1. Never promise or imply returns. The most likely outcome of a first version is flat to negative after costs.
2. Never ask for, accept or print a private key, recovery phrase, API key, Telegram token or card number in chat. Keys live only in `.env`.
3. Label every fact as verified or not. Prices and tool features below come from third-party review sites and are **unconfirmed**.
4. Shadow mode only until the gates are met. No orders, no wallet, until then.
5. Plain English, pounds first, weekly cadence, tables for structure.

---

## 1. The idea in five lines
1. A video claimed $44.82 became $11,643 overnight with a six-agent memecoin bot. Its own footer says the detail is illustrative, and it shows no proof, so it is treated as a design idea only.
2. We built a **shadow-mode scanner** for new Solana tokens: it filters with hard rules, logs every decision with the reason, and tracks what each token did afterwards.
3. It never trades and holds no wallet. Its job is to find out, at **£0 of capital risk**, whether the rules have any edge after costs.
4. Only if the data supports it do we move through paper trading, then a small live slice (£200, capped at £500), with hard limits in code.
5. Paid data is bought only to test one question, starting with the cheapest option, and only after three months of free data.

---

## 2. DO THIS NOW (dated checklist)

| When | Action | Who | Done when |
|---|---|---|---|
| **Wed 28 Oct 2026** | Run `python -m shadowbot status`. If it does not say RUNNING, run `python -m shadowbot start` | You, or Claude Code on your PC | Status says RUNNING and "last scan cycle" is under 2 minutes ago |
| **Wed 28 Oct** | Update the code: `git pull` on branch `claude/solana-shadow`, run the tests, restart the scanner. This adds the weekly Telegram notice | Claude Code on your PC | 56 tests pass; `status` says RUNNING |
| **By Fri 30 Oct** | *Optional:* set up Telegram alerts (steps in section 6) | You with Claude Code | A test message arrives on your phone |
| **Sun 1 Nov, evening UTC** | First weekly report arrives (week 1, Mon 26 Oct to Sun 1 Nov). Expect "too early to conclude" | The scanner | `reports/weekly-2026-11-01.html` exists (and a Telegram notice if set up) |
| **Mon 2 Nov** | Send the headline lines of the report to the assistant for a plain-English explanation | You | Explained |
| **By Mon 9 Nov** | Send: the three book titles (or cover photos); confirm the free wallet list for the Spy strategy (GMGN rankings); confirm the £500 live cap with £200 first; give the live GBP/USD rate for `usd_per_gbp` in `thresholds.toml` | You | All four answered |
| **9 Nov to 6 Dec** | Build the Spy strategy in shadow mode | Assistant | Spy rows appear in the weekly report |

**What to expect in the first weeks:** week 1 is plumbing only (is it running, error rates, how many tokens it sees). No conclusion
about the strategy is possible before about 200 signals.

---

## 3. THE CALENDAR (dates are plans; the gates decide, not the calendar)

| Date | What starts or ends | Money |
|---|---|---|
| **Tue 27 Oct 2026** | Shadow test starts (first day of real data). Weekly report every Sunday evening UTC; first on Sun 1 Nov | £0 |
| **9 Nov to 6 Dec** | Spy strategy built and measured in shadow mode, using free wallet lists | £0 |
| **Sun 24 Jan 2027** | 13th weekly report: end of the three-month shadow test | £0 |
| **Tue 26 Jan 2027** | **Decision day:** stop, revise or continue. Name the one question the paid data must answer | £0 |
| **Wed 27 Jan 2027** | **Paper trading starts**, free data only (a two-and-a-half-week baseline first) | £0 |
| **Mon 15 Feb 2027** | **Rung 1: Birdeye Pro starts**, one month, run as an A/B test against the free wallet list | about £7 ($9) |
| **Fri 12 Mar 2027** | Decide: cancel Birdeye, or move to rung 2 (Birdeye renews 15 Mar) | none |
| **Mon 15 Mar 2027** | **Rung 2: Nansen Pro, monthly**, only if rung 1 helped but was too limited | about £51 ($69) |
| **About Mon 29 Mar 2027** | **Live £200 starts**, only if the paper gate is met | £200 |
| **About Tue 27 Apr 2027** | First step-up check (£350): needs 4 live weeks, 30+ trades, stop untouched | up to £350 |
| **May to Oct 2027** | Scale in steps to the £500 cap. £1,000 only much later, only if validated | up to £500 |
| **27 Oct 2027** | 12-month review | n/a |

Every step after the shadow test is **gated**: if a gate fails, everything after it moves or stops. If signals are too rare (under
200 by 24 Jan), the shadow test is extended or the triggers are loosened.

**Assumption to confirm:** that the scanner has really been collecting since 27 Oct. If it started later, every date shifts by the difference.

---

## 4. MONEY MAP: what every payment is for

| # | Payment | Amount | What it buys | When | How you pay | Rule |
|---|---|---|---|---|---|---|
| 1 | Shadow test running costs | £0 for data; electricity roughly £2–3 a month (my estimate) | Nothing to buy: free data sources, your PC | From 27 Oct | n/a | Free tiers are unconfirmed; check Helius limits |
| 2 | **Rung 1: Birdeye Pro** | about **$9 a month** (about £7) | Wallet profit-and-loss and top-trader lists, to test whether paid wallet data beats the free list for the Spy strategy | From **15 Feb 2027**, one month | Birdeye's own website, your card, monthly plan | Keep only if it adds wallets the free list lacks. Cancel or move up by 12 Mar |
| 3 | **Rung 2: Nansen Pro** | about **$69 a month** (about £51) | Deeper wallet labels | From **15 Mar 2027**, one month, **only if rung 1 helped but was too limited** | Nansen's own website, **monthly** (the $49 price needs an annual commitment: do not take it) | Cancel by 14 Apr unless it clearly beats rung 1 |
| 4 | Live trading money | £200 first, then £350, then £500 | Trading capital, **not a cost**: it sits in a separate wallet | From about 29 Mar 2027, if the paper gate is met | Buy SOL or USDC on a UK exchange you trust, withdraw to a **new burner Solana wallet** | Only add money after the step-up rule passes and you say so |
| 5 | Tax and records | n/a | Each swap may be a taxable disposal (UK) | Always | The bot's log is the record; confirm with GOV.UK or an accountant | Not tax advice |

**Totals:** data worst case about **£58** ($9 + $69), under a **£100 hard cap**. If rung 1 shows nothing, you stop at about **£7**.
Live money capped at **£500**. Whole plan worst case about £560 plus electricity.

**Not decided yet:** the exchange and the wallet app (decided at month 5, with click-by-click steps, after checking what works in the
UK); SOL versus USDC as the base asset (my lean: USDC keeps the £ value steadier, to confirm).

**Never:** your main wallet; a private key, recovery phrase or card details in any chat. £1 is roughly $1.30–1.40 (live rate unconfirmed).

**Tool differences (third-party sources; none tested accuracy):**

| Tool | Price (unconfirmed) | Good for | Weak spot |
|---|---|---|---|
| GMGN | Free (1% per trade only if you trade through them) | Finding smart-money wallets | Basic copy trading |
| Cielo | Free for 10 Solana wallets; Pro about $59 | Alerts on specific wallets | Not deep analysis |
| Birdeye Pro | about $9 a month | Wallet P&L, top-trader lists | Algorithmic labels, partial P&L; data API priced separately |
| Nansen Pro | $69 monthly, or $49 billed annually | Strongest wallet labels, deep analysis | About 30 s for live watching; about 7× Birdeye's price |
| Helius | about $49 | Infrastructure (RPC, webhooks), not a wallet list | Not a wallet-quality product |

---

## 5. EXPECTATIONS

| Phase | What to expect |
|---|---|
| Weeks 1–13 (shadow) | £0 of risk. The output is data. Week 1 is plumbing. Nothing meaningful before about 200 signals. A week only counts as "positive" or "not positive" with 20+ signals and controls |
| Paper trading | Realistic fills and costs, still £0 of trading risk. Paid data runs as an A/B test |
| First live months | Noisy. Plausible range **−100% to +40%** of the live slice (my judgement, not a calculation) |
| 12 months | **10–20% a month after all costs is a good outcome.** Above 30% sustained is suspicious, not a goal |

**In pounds (good cases before losses, not forecasts):**

| Live slice | Per trade (7%) | Stop at −30% | Good month (10–20%) | First live months range |
|---|---|---|---|---|
| £200 (first step) | £14 | £60 | £20–40 | −£200 to +£80 |
| £350 | £25 | £105 | £35–70 | −£350 to +£140 |
| £500 (the cap) | £35 | £150 | £50–100 | −£500 to +£200 |
| £1,000 (much later) | £70 | £300 | £100–200 | −£1,000 to +£400 |

**Why not more:** returns scale with capital. At £500, even a good month is £50–100. A $69 tool needs a 34.5% month on $200 just to
pay for itself, so paid data is a capped **research cost**, not an investment. The most likely single outcome of a first version is
flat to negative after costs.

---

## 6. NOTIFICATIONS: what pings you

| Event | Where | When | Status |
|---|---|---|---|
| Scanner down and **cannot be restarted** | PC pop-up + Telegram (if set up) | Immediately; repeated every 6 hours while down | **Built** (watchdog) |
| Scanner back up | Telegram | Once, on recovery | **Built** |
| **Weekly report ready**, with a 3-line summary and gate progress | Telegram (if set up) + the file on your PC | Sunday evening UTC (after 20:00) | **Built 28 Oct**; needs `git pull` and a scanner restart |
| Weekly report file | `reports/weekly-DATE.html` and `.md` | Sunday evening UTC | **Built** |
| Key dates: decision day, buy dates, cancel dates | Calendar reminders | On the dates in section 3 | **Not set up** (the assistant can create Google Calendar events if you say yes) |
| Daily loss limit or project stop hit | Telegram + PC pop-up | Immediately | **Not built yet**; needed before live money |
| Step-up eligible | `python -m shadowbot risk-status` | On demand | Built as a command; not pushed to Telegram |
| Daily updates | None | n/a | By your choice |

**Telegram setup (optional, about 10 minutes, ask Claude Code on your PC to do it):**
1. In Telegram, message **@BotFather**, send `/newbot`, follow the prompts. It gives you a **token**.
2. Send any message to your new bot.
3. Claude Code looks up your **chat id** (without printing the token).
4. Both go into `.env` as `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`. **Never paste them into a chat.**
5. Test: restart the scanner; it sends the weekly notice on the next Sunday evening, or ask Claude Code to send a test message.

Watchdog: `python -m shadowbot watch`, meant to run from a Windows scheduled task at login and every 15 minutes. It restarts a dead
or stuck scanner and alerts only if the restart fails.

---

## 7. THE WEEKLY ROUTINE AND THE GATES

**Every Sunday evening (about 15–30 minutes of your time):**
1. Open the report (or read the Telegram notice, then the file).
2. Read the plain-English summary, then the day-by-day table, then the gate tracker.
3. Send anything odd to the assistant; otherwise nothing is needed.

**Gate to leave the shadow test:** 200+ signals; a positive edge over the control group after the assumed 4% friction, seen across several
weeks (not one lucky week); filters that separate collapsed tokens from passed ones.

**Gate to go live:** paper results positive after realistic costs; the paid data (if kept) shows a lift in the A/B test.

**Step-up rule (£200 to £350 to £500):** 4+ live weeks at the current slice; 30+ trades; the stop never touched; live average trade
positive and within 3 points of paper; **and** you run `python -m shadowbot stepup --confirm`. The bot never raises its own slice.

**Stop conditions:** a gate fails and the data says no edge (stop; nothing more is spent); project stop hit (−30% of the live slice);
daily loss limit hit (desk halts until you reset it); data costs exceed the measured benefit.

---

## 8. THE STRATEGIES (what the bot actually does)

Every 30 seconds: discover new pools (GeckoTerminal) → evaluate by stages, cheapest check first → log every decision → track price and
liquidity at +30 s, +5 min, +15 min, +1 h.

| Stage | Checks | Examples |
|---|---|---|
| S1 free cut | age, liquidity, activity | age 2–360 min, liquidity at least $5,000, 5+ transactions in 5 min |
| S2 on-chain facts | mint and freeze authority, token-2022 permanent delegate, holder concentration | reject if an authority is open; top-10 holders (excluding the largest account) over 50%; biggest other holder over 20% |
| S3 optional | RugCheck, Jupiter sell route | off by default |
| S4 triggers | entry rules | `new_pair_flow`: age 2–15 min, buy ratio 70%+, liquidity $10k+; `volume_spike`: 3× the hourly pace, age 15–360 min |

- A token that passes with no trigger is logged as **PASS** and is the **control group**. A trigger is logged as **SIGNAL**.
- Bench by reason: permanent reasons never retry; "too young" retries when tellable; on-chain rejections retry after 2 hours; passed tokens are rechecked every 30 minutes.
- **Spy (wallet copying)**, built 9 Nov to 6 Dec: scores wallets in code (win rate, holding time, how early) from a free wallet list; follows only consistent moves; late arrival, crowding, bots and selection bias are the known weaknesses. **Confluence** (wallet buy + flow + clean filters) comes after both exist.
- All thresholds live in `thresholds.toml` and are proposals to tune from data.

---

## 9. RISK RULES AND LIMITS (enforced in code; no model can override)

| Rule | Value |
|---|---|
| Biggest position | about 7% of the slice, and under 1% of the pool's liquidity |
| Risk per trade | 0.5–1% of the slice at the stop |
| Daily loss limit | about 5%: the desk halts until you reset it |
| Project stop | −30% of the live slice: live trading halts |
| Positions at once | one |
| Halts | persist across restarts and new days until a person resets them |
| Keys | none in the bot during shadow; later a separate burner wallet holding only the slice |

**Why position size matters most:** a stop-loss cannot save a token that collapses in one step. Loss of the whole account after three
rugs in a row: 40% per trade = −78%; 25% = −58%; 7% = −20%.

**Why win rate matters:** with a 14% stop, 30% average win, 7% position, 5 trades a day and 4% friction, a 45% win rate gives about +21% a
month and a 35% win rate about −24%. A 10-point swing flips the month. 100 trades only pins a win rate to about ±10 points.

---

## 10. STATUS: built, unverified, not built

| Built | Not yet verified | Not built yet |
|---|---|---|
| Scanner, filters, logger; outcome tracker; weekly report; risk engine and slice ladder; background mode and watchdog; weekly Telegram notice (28 Oct); 56 tests including real API samples captured 27 Oct | Whether it keeps up with new tokens (coverage); Windows background mode over several days; API prices and limits (third-party snippets); the live GBP/USD rate; accuracy of any wallet-data provider | Paper-trading executor; Spy strategy; paid-data A/B arm; dev-wallet % and LP-lock checks; Calendar reminders; loss-limit alerts |

On 27 Oct, Claude Code on the user's PC ran the real `doctor` check, captured real GeckoTerminal, DexScreener and RPC responses, fixed
the holder check, and added the watchdog. **Nobody has yet reviewed the collected data, `status` output or a weekly report.**

---

## 11. DECISIONS AND INPUTS NEEDED

| Needed | By | Why |
|---|---|---|
| Confirm the scanner started on 27 Oct and is running now | 28 Oct | Every date depends on it |
| Telegram yes or no | 30 Oct | Decides whether weekly and alert pings reach your phone |
| Three book titles or cover photos | 9 Nov | Chapters on scam tokens, position sizing and on-chain wallet analysis help most |
| Free wallet list for Spy (GMGN rankings) | 9 Nov | The Spy build starts that day |
| £500 cap, £200 first | 9 Nov | Sets the risk limits |
| Live GBP/USD rate | 9 Nov | Used for the liquidity cap |
| Which single question the paid data answers | 26 Jan 2027 | Default: does a paid wallet list beat the free one for Spy? |
| Calendar reminders yes or no | any time | Dates in section 3 |
| Exchange, wallet app, SOL versus USDC | about 1 Mar 2027 | Before live money |

---

## 12. COMMANDS AND FILES (run inside `solana-shadow/`, virtual environment active)

| Command | Purpose |
|---|---|
| `python -m shadowbot status` | Running? last scan? tokens checked in 24 h? latest log lines |
| `python -m shadowbot start` / `stop` | Start or stop the scanner in the background (no window) |
| `python -m shadowbot watch` | Watchdog: restart if dead or stuck; alert only if that fails |
| `python -m shadowbot weekly [--end YYYY-MM-DD]` | Weekly report (also written Sunday evenings UTC) |
| `python -m shadowbot report [--hours N]` | Technical report (Tests A, B, C) |
| `python -m shadowbot slices` | The slice ladder in pounds |
| `python -m shadowbot risk-status` | Paper and live risk state, halts, step-up eligibility |
| `python -m shadowbot stepup [--confirm]` | Show or apply a step-up |
| `python -m shadowbot doctor` | Check setup and every API; saves samples |
| `python -m unittest discover -s tests -v` | Run the tests |

Files on the PC: `data/shadow.db` (all state), `data/run.log`, `data/run.err`, `reports/`, `samples/`, `.env` (keys, git-ignored).
Keep the PC awake while it runs (PowerShell: `powercfg /change standby-timeout-ac 0`). Background mode survives closing the window,
not a restart; the watchdog task covers restarts.

---

## 13. EVIDENCE AND CAVEATS
- The video's results are labelled illustrative and unproven.
- No independent, verified evidence was found of retail memecoin bots being profitable. Regulators warn about "AI trading bot" claims (CFTC advisory; reported FCA warnings). Industry reports (secondary, some from interested parties) show most memecoin wallets lose.
- Jev / TypeSafe: launch and funding are reported by several outlets; speed and price are company figures with no independent benchmarks; the article's "$10–25 a month" cost claim does not hold at its own state size (about $145 a month by my arithmetic). Monad's 300 ms block time is confirmed.
- UK tax: each swap can be a taxable disposal; the £3,000 annual exempt amount is from secondary sources; HMRC's "badges of trade" test could treat a 24/7 bot as trading (Income Tax). Not tax advice.
- Selling signals or managing other people's money is a different, regulated activity (FCA). This project uses your own money and public data only.
- All prices and tool features in section 4 come from third-party review sites (some vendor-written). None tested data accuracy. Check each provider's own site.

---

## Appendix A: the presentation, slide by slide (the artifact in text)

1. **Cover.** Shadow Desk: risk, benefits and trajectory for a Solana memecoin scanner. Shadow mode first: nothing here trades or holds a wallet. Every figure is a scenario, not a forecast.
2. **The bottom line.** Test for free first. Put money in only when the data says so. £0 of capital at risk during the 3-month shadow test and paper trading; £500 live cap (roughly $650–700), first £200 only after the gates are met, then in steps; 0 returns promised. Plus about £100 for two paid-data months, a research cost.
3. **What the shadow desk does.** Scan (new tokens every 30 s) → Check (hard facts in code) → Log (every decision with the check that fired) → Track (+30 s, +5 m, +15 m, +1 h) → Report (weekly: do the filters work? does a trigger beat the control?). No wallet, no orders, no keys; runs in the background.
4. **Market risks and their controls.** Rug or sudden collapse (High): position near 7%. Oversized positions (High): risk 0.5–1% per trade, daily limit 5%, project stop −30%. Thin liquidity and slippage (Medium): under 1% of pool liquidity, 2% slippage cap. Late signal when copying wallets (Medium): measured at +30 s against a control group.
5. **Operational and money risks.** Bad or missing data (Medium); too few trades to conclude (High): no conclusion before 200+ signals; paid data that does not pay (Medium): month by month, two-month A/B test, capped research cost; key or wallet loss (Low now); UK tax and records (Low).
6. **Rugs hit position size, not stop-losses.** After three rugs: 40% per trade −78%; 25% −58%; 7% −20%.
7. **A 10-point win-rate swing flips the month.** 45% win rate +21%; 35% win rate −24% (assumptions in section 9).
8. **A $69 tool needs a big month to pay for itself.** Return needed to cover $69: $200 capital 34.5%; $1,000 6.9%; $5,000 1.4%. 10× rule: $690 profit needs about $3,450 at 20% a month or $6,900 at 10%; out of reach at £500, so paid data is a capped research cost (about £100).
9. **Staged spending about halves the worst case.** Upfront plan $1,690 (about £1,250) versus staged about £600.
10. **The 12-month path, with a gate at every step.** Shadow test (months 0–3, £0); decision point (month 3); paper + data trial (months 3–5, about £100 on data); live first slice (months 5–6, £200, cap £500, stop −30%); scale in steps (months 6–12, £500 cap, up to £1,000 later).
11. **The calendar: what starts when.** Section 3 above.
12. **Start cheap: the paid-data ladder.** Rung 0 free (£0); rung 1 Birdeye Pro about $9 a month; rung 2 Nansen Pro about $69 a month. Worst case about £58 ($78), not £100; stop at about £7 if rung 1 shows nothing. Nothing bought until month 3, only if you say yes.
13. **Where the £200–500 trading money goes.** New Solana wallet used for nothing else → buy SOL or USDC on a UK exchange and withdraw to it → the bot trades only from it, inside the limits → add money only in steps after the step-up rule and your OK → keep the log for tax. Decided at month 5: exchange and wallet app; SOL or USDC. Never: your main wallet; your private key in any chat.
14. **What will ping you.** Section 6 above.
15. **What you get, even if there is no edge.** Benefits: a £0 answer on whether the video's rules work; an audit trail; a reusable log (wallet-copy plugs in); a measured basis for any paid tool. Limits: no edge guaranteed; copied wallets arrive late; free-tier limits may hide tokens; dev-wallet and LP-lock checks not built.
16. **What to expect, and when.** Section 5 above.
17. **The money path by slice size, in pounds.** The slice table in section 5, plus the step-up rule.
18. **Hard rules the code enforces.** Section 9 above.
19. **Where things stand today.** Section 10 above.
20. **Do this now.** Section 2 above.
