# Plan: from shadow test to a decision about live money

Written 28 Oct 2026. Honest framing: this is a **measured experiment**. A flat or negative result is the most likely outcome of a
first version, and finding that out cheaply is a success. Nothing in this plan promises a return.

## Goal
Find out, with data and in stages, whether the video's rules (and later the wallet-copy idea) have a positive edge after costs,
and only then risk live money, capped at £500 (about $650–700), starting at £200.

## Money at risk, by stage

| Stage | When | Money at risk |
|---|---|---|
| Shadow test | Months 0–3 | £0 |
| Decision point | Month 3 | £0 |
| Paper trading, with paid data A/B (about £100 total, two months) | Months 3–5 | about £100 spent, no trading risk |
| Live, first slice | Months 5–6 | £200 (cap £500) |
| Scale in steps | Months 6–12 | up to £500; £350 and £500 steps |
| £1,000 slice | Much later | Only if the £500 stretch validated |

Worst case of the whole plan: about £600 (£100 data plus the £500 cap).

## Money map: where every pound goes

| When | Amount | What it pays for | How you pay | Status |
|---|---|---|---|---|
| Months 0–3 | £0 | Nothing. Free data sources; your PC runs the scanner (electricity roughly £2–3 a month, my estimate) | n/a | Decided |
| Months 3–5 | **Hard cap £100; expected about £58 at most** | **A paid-data ladder, start cheap.** Rung 0 (free, always first): GMGN wallet rankings, Cielo free tier (10 wallets), our own wallet scoring. Rung 1, month 1 of the trial: **Birdeye Pro, about $9 a month** (wallet profit-and-loss, top-trader lists; labels are algorithmic). Rung 2, month 2, only if rung 1 helped but was too limited: **Nansen Pro, about $69 a month paid monthly** ($49 needs an annual commitment, so do not). One question throughout: does a paid wallet list find better wallets for the Spy test than the free one? | On each provider's own website with your card, monthly plan only, reminder to cancel. Worst case about £58 ($78); if rung 1 shows nothing, stop at about £7 | Prices unconfirmed (third-party review sites, none tested accuracy). Nothing is bought until month 3 and only if the user says yes |
| Months 5–6 | £200 | Trading money, in a **separate burner Solana wallet** used for nothing else | Buy SOL or USDC on a UK exchange you trust, then withdraw to that wallet | Exchange and wallet app **not chosen or verified**; decided at month 5 with click-by-click steps |
| Months 6–12 | Up to £500 in total | The same wallet, topped up in steps (£350, then £500) | Top up the same wallet, only after the step-up rule passes and you say so | Gated |
| Later | Up to £1,000 | Only if the £500 stretch validated | Same wallet | Gated |
| Always | n/a | Records for tax: each swap may be a taxable disposal | The bot's log is the record; confirm with GOV.UK or an accountant | Not tax advice |

Nothing is bought, scheduled or charged until month 3, and only if the user says yes. If the answer is no, the plan still works with
£0 of data spend: only the paid-list test is skipped.

Never use your main wallet. Never share a private key, recovery phrase or card details in any chat. £100 is about $138 at
$1.30–1.40 per £1 (the live rate is unconfirmed). SOL versus USDC as the base asset is decided at month 5 (my lean: USDC keeps
the £ value steadier, to be confirmed).

## Phases, with gates

### Phase 0: today (week 0)
- Done on 27–28 Oct by Claude Code on the PC: real `doctor` run, parsers checked on real samples, doctor fixed, watchdog added.
- Remaining: confirm the scanner runs in the background (`python -m shadowbot status`) and the watchdog task is installed.
- Send the Test A section of `python -m shadowbot report` so it can be explained.
- **Done when:** `status` says RUNNING, error rate under 5%, feature completeness over 95%, discovery overlap understood.

### Phase 1: shadow test (weeks 1–12)
- The scanner runs continuously. The user reads **one weekly report** (Sunday evening UTC), about 30 minutes: summary, day-by-day,
  scorecard, gates.
- Weeks 3–6: build the **Spy** strategy in the same log (free wallet-list source, scored in code). Both strategies are measured against
  the control group (passed tokens with no trigger).
- **Gate to leave shadow:** 200+ signals AND a positive edge over the control after the assumed 4% friction, seen across several
  weeks (not one lucky week), AND filters that separate collapsed tokens from passed ones.
- If signals are too rare, extend the test or loosen triggers. If the edge is not there, stop or revise: nothing has been spent.

### Phase 2: month 3 decision
- Stop, revise, or continue. If continuing, name the **one question** the paid data must answer and pick the provider.

### Phase 3: paper trading (months 3–5)
- Build the paper executor. It must call `RiskEngine.allow_order` before every order and record every close.
- About the 15th of the first paper month, start the paid data (monthly, never upfront): an **A/B** with a free-data arm and a
  free-plus-paid arm on the same tokens. Decide the second paid month at the end of the first by a rule set in advance.
- **Gate to go live:** positive after realistic costs and fills over enough trades, and the paid data (if kept) shows a lift.

### Phase 4: live, small (months 5–6)
- Separate burner wallet holding only the slice (£200), never a main wallet. The key is never in the bot's chat or logs.
- Hard limits (already built): 7% per position, 1% risk per trade, 5% daily loss limit, 30% project stop (£60 on £200), one position
  at a time. Halts stay on until the user resets them.
- **Step-up:** only after 4 live weeks at the slice, 30+ trades, stop untouched, live average trade positive and within 3 points of
  paper, AND the user runs `python -m shadowbot stepup --confirm`.

### Phase 5: scale (months 6–12)
- £350, then £500. £1,000 only after a validated stretch at £500.

## Weekly routine (the only regular task for the user)
1. Open the Sunday report (`reports/weekly-DATE.html`).
2. Read the plain-English summary, then the day-by-day table, then the gates.
3. Paste anything odd into the chat; otherwise nothing is needed.

## Stop conditions
- Any phase gate fails and the data says the rules have no edge: stop, spend nothing more.
- Project stop hit (−30% of the live slice): everything halts until the user decides.
- Daily loss limit hit: the desk halts until reset.
- Costs of data exceed the measured benefit.

## What each side does

| Claude (in the new chat or Claude Code) | The user |
|---|---|
| Keeps the code, parsers and reports correct; fixes parsers once real samples arrive | Keeps the PC awake and the scanner running; reads the weekly report |
| Builds Spy, the paper executor and the A/B arm | Provides the wallet-list source choice, the book titles, the live GBP/USD rate |
| Explains each report in plain English; flags weak evidence | Approves any money step and any step-up |
| Never invents numbers; labels everything verified or not | Never shares the Helius key in chat |

## Open items before Phase 1 is trustworthy
1. The first Test A report on real collected data (error rate, completeness, discovery coverage).
2. Windows check: background mode, the watchdog scheduled task, and a reboot test.
3. Live GBP/USD rate into `thresholds.toml` (`usd_per_gbp`).
4. The three books (titles or cover photos).
5. A free source for the Spy wallet list.
