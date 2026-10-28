# Conversation summary: from the video to today

Written 28 Oct 2026. The user is UK-based, thinks in pounds, is not technical, and works in sports media and social strategy
(the "Goal Englize" football content brand). They want plain English, honesty over hype, tables, and weekly (not daily) reports.

## 1. Where it started
The user shared a video: "Six Grok Bot agents were given $44.82". It is an animated dashboard of a six-agent memecoin pipeline
(Scanner, Rug Check, Sizer, Executor, Logger, Equity) that turns $44.82 into $11,643.21 in one night over 64 trades (43 wins,
21 losses). Positions were 22–43% of equity; stops 10–14%; take-profit at 2R–3R; trailing and time stops. The footer says
**"trade-level detail illustrative"**, and there is no on-chain proof. I treated it as a design idea, not evidence of returns.
The user asked how it works and then how to rebuild it.

## 2. Early decisions
- **Log first, shadow first:** measure whether the rules have an edge before any money moves.
- **Pure Python and SQLite, on the user's own PC.** n8n is optional later (reporting only). Claude writes the code in a cloud
  session; the PC runs it.
- **Solana** was my assumption (the video never names the chain); the small $44 account also makes Solana's low fees the only
  sensible fit.
- **Phases:** contract and log, shadow, paper, live tiny, scale. A statistics note: 100 trades only gives about ±10 points on a win rate.

## 3. The expectation reset (important)
The user wanted returns like the video. I refused to promise any number. What I said and still stand by:
- A good outcome is 10–20% a month after costs. Above 30% sustained is suspicious. Plausible first live months: −100% to +40% (my judgement).
- Illustrative arithmetic: a 45% win rate gives about +21% a month; 35% gives about −24% (assumes a 14% stop, 30% average win,
  7% position, 5 trades a day, 4% friction).
- Rugs hit position size, not stop-losses: three rugs at 40% per trade cost 78% of the account; at 7%, about 20%.
- Returns scale with capital: a $69 tool needs a 34.5% month on $200 just to pay for itself.
- The user got frustrated ("is that a joke?"), and we settled on: this is a measured experiment, not an income promise.
  I withdrew an unsupported suggestion that content creation would pay more reliably.

## 4. The article (TypeSafe "Jev" desk)
The user pasted an article about a multi-bot desk (Gambler, House, Spy) using a decision model called Jev. I checked it:
TypeSafe's launch and funding are reported by several outlets; Jev's speed and price are **company figures with no independent
benchmarks**; Monad's 300 ms block time is confirmed; the "$10–25 a month" cost claim does not hold at the article's own state
size (about $145 a month by my arithmetic).
**Adopted from the article:** facts in code before judgments; bench rejections by reason; "no trade is a result" (alert if the
filter rejects almost nothing); one position at a time; a hard-coded risk engine; shadow, paper, live ladder; calibration checks.
**Not adopted yet:** Jev itself (not needed for Phase 1, vendor claims unverified), the order-book bots (different venues).
The user liked the **Spy (wallet-copying)** idea as a second strategy.

## 5. Spy, other techniques, data costs
- Spy benefits: borrows an existing edge, narrows the search, independent signal, explainable. Weaknesses: late arrival, crowding,
  survivorship bias in wallet rankings, bots and insiders.
- Other techniques: the video's flow rules (built), Spy (next), confluence of both, migration events (hypothesis), order-book bots
  and prediction markets (other venues, later).
- Costs found (all unverified against official pages): Helius free plan (credits conflict: 1M vs 500K; 2 req/s for wallet-history
  APIs; 5 webhooks), Jupiter free key (1 req/s), DexScreener free, GMGN free, Birdeye about $9 Pro, Nansen $69–$100+ (sources conflict).
- Decision: **free sources only for shadow and paper**; paid data only to answer one specific question.
- Evidence on retail results: no independent verified evidence of retail memecoin bots being profitable. Regulators warn about "AI
  trading bot" claims (CFTC advisory; reported FCA warnings). Industry reports show most memecoin wallets lose (e.g. 6.16% of Fomo
  copy-trading wallets profitable over 3 months; one Pump.fun study 14.1% of wallets ahead). These are secondary and unverified.

## 6. The user's business logic, and where we landed
The user's rule: a tool costing $69 should be at most 10% of what it earns. I agreed with the rule but showed that at £500 of
capital it cannot be met, so the paid data is a **capped research cost, not an investment**. The user wants data built up first,
then paid data to widen the view. Final structure:
- **Months 0–3:** shadow test, weekly reports. No live money.
- **Month 3:** decision point (stop, revise, continue).
- **From about the 15th of the first paper month:** paid data, about **£100 for two months**, run as an **A/B comparison**
  (free-data arm vs free-plus-paid arm on the same tokens), paying month by month, not upfront.
- **Months 3–5:** paper trading.
- **Months 5–6:** live, first slice **£200**, cap **£500** (about $650–700; the exchange rate is uncertain).
- **Later:** £1,000 only if validated. Step-up only after 4 live weeks matching paper with the stop untouched, and only on the
  user's explicit command.
- Worst case of the staged plan is about £600 (£100 data plus the £500 cap) against about £1,250 for the original "pay for a year
  and fund everything on day one" idea.

## 7. What was built (in the repo)
Scanner, filters and logger; outcome tracker; `doctor`; technical report; **weekly report** (Markdown and HTML, written Sunday
evenings UTC); **risk engine** (slice ladder, sizing caps, halts that persist, step-up rule); **background mode**
(`start`, `status`, `stop`). A **18-slide presentation** covers risk, benefits, the trajectory and where things stand; an offline copy is `docs/Shadow_Desk_presentation.html` (arrow keys to move; print to PDF to keep it).
See `PROJECT_SUMMARY.md` for details and `PLAN.md` for what comes next.

## 8. State right now
- Claude Code on the user's PC (commit `3ebfa20`, 28 Oct) ran `doctor` for real on 27 Oct, captured real GeckoTerminal,
  DexScreener and RPC responses, fixed my doctor holder check (the RPC refuses wrapped SOL's millions of holders), added
  `tests/test_real_samples.py`, and added a **watchdog** (`python -m shadowbot watch`: restarts a dead or stuck scanner; alerts by
  PC pop-up and optional Telegram only if the restart fails; meant for a Windows scheduled task at login and every 15 minutes).
  So the parsers are now checked against real response shapes.
- The user has been running the scanner for about a day and asked for it to be hidden in the background. `start`, `status` and
  `stop` exist; whether the PC is running in background mode with the watchdog task is unconfirmed.
- **I have not seen any collected data, `status` output or report.** Coverage, error rates and the first weekly report are unreviewed.
- Nothing trades. No wallet exists.

## 9. Other topics touched
- **n8n and MCP:** explained that MCP is how Claude calls a service, not a data source; the bot should not run through a model.
  No Solana or DexScreener connector was found in the registry.
- **UK:** each swap can be a taxable disposal; the £3,000 annual exempt amount comes from secondary sources; HMRC's "badges of
  trade" test could classify a 24/7 bot as trading (Income Tax). Not tax advice; confirm on GOV.UK.
- **"Are we scamming?"** No: own money, public data, no promises. Selling signals or managing others' money would be a different,
  regulated activity (FCA).
- **EverBee:** an Etsy product-research tool; no MCP connector exists; a separate subject, not pursued.
- **Books:** the user has three books and will send titles or cover photos. Most useful chapters: how scam tokens work on Solana,
  position sizing and risk, and on-chain wallet analysis.

## 9b. A gap the user called out (28 Oct)
The plan said "about £100 for paid data" and "£200 live" but never said what the money buys, where to pay, or where the
trading money physically goes. The presentation and `PLAN.md` now have a money map: the £100 is a hard cap for two months (about £50 a
month) of one wallet-labelling subscription, to test whether a paid wallet list beats the free rankings for the Spy strategy
(provider not chosen until month 3; nothing is bought or scheduled before then), and the live money goes into a separate burner Solana wallet funded from a
UK exchange (exchange and wallet app not chosen or verified until month 5).

## 9c. Change of strategy on paid data (28 Oct)
The user asked why not start with something cheaper and move to the £50 option later, and asked for the best choice by search.
Research (all third-party review sites, vendor-authored in places, **none tested data accuracy**): Nansen has a Free tier and one Pro
plan, $69 a month paid monthly or $49 billed annually, strongest for entity labels, slowest for live watching (about 30 s); Birdeye
Pro about $9 a month (wallet profit-and-loss, algorithmic top-trader lists, partial PnL, no copy trading; its data API is priced
separately); Cielo free for 10 Solana wallets, Pro about $59, best for alerts; GMGN free (1% per trade if trading through it),
the most-cited place to find smart-money wallets. Helius is infrastructure, not a wallet-quality product. Decision: a **ladder**:
free first, then Birdeye Pro for month 1, then Nansen Pro for month 2 only if month 1 helped but was too limited. Worst case about
£58 under the £100 cap; stop at about £7 if rung 1 shows nothing.

## 10. Pending decisions and unanswered questions
1. Run the update on the PC and send back `python -m shadowbot status` and the Test A section of `report`.
2. Send the three book titles (or cover photos).
3. Free source for the Spy wallet list (nothing chosen).
4. Confirm the £500 cap with £200 first, and the live GBP/USD rate for `usd_per_gbp`.
5. At month 3: which single question the paid data must answer, and which provider.
