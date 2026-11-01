# Spy strategy v1: FROZEN rules (29 Oct 2026)

Decided by Saed on 29 Oct 2026: "I will go with your recommendation" (Option 2 in `SPY_WALLET_ANALYSIS.md`).
SHADOW MODE ONLY. No orders, no wallet of ours, no keys. Only public addresses are read.
Frozen: changing anything below means the Spy test restarts from zero. Not built and not switched on yet. Planned switch-on: after the first weekly report (Sun 1 Nov 2026), start date to be announced to Saed.

## 1. The one question

When one of 7 slow wallets buys a new token, does a token we notice AFTER that buy do better than a similar token nobody followed, after costs?

## 2. Wallets (frozen list)

File: `docs/SPY_WALLETS_FROZEN_2026-10-29.txt` (SHA-256 of its text when created: `ae0a23a8d99c59da5d80be1d6c5f714e0dec3554795370e47eeaff2a78339748`).

| Group | Wallets | Used for |
|---|---|---|
| Primary (7 slow wallets) | `BAdJW3mm`, `4bSUHKxB`, `C32NsZNd`, `5dXRP54f`, `DDsFBzcB`, `AfGjJQkv`, `HFLX1Gnx` | The pass/fail verdict |
| Secondary (14 other measured wallets) | see file | Only the report of "2+ independent operators bought the same token within 15 minutes" (information, never the verdict) |

- Excluded for good: the 2 "Top Dev" wallets (token creators), all wallets that failed the activity screen (bots, failed-transaction spam).
- `7tkP` and `CFkd` count as ONE operator. `77Uy` and `CzeY` count as ONE operator (they bought the same tokens).
- Evidence counts only from signals AFTER the switch-on date. The 13 to 30 days already measured are NOT evidence.

## 3. Signals

| Item | Rule |
|---|---|
| Primary signal (SPY_SIGNAL) | A buy of a token by any primary wallet. Our noticing time is the entry time |
| Entry price | The price when WE notice it, not the wallet's price |
| Filters | The same hard filters as the main strategy (liquidity at least $10,000 and the on-chain checks). Tokens that fail are logged FILTERED with the reason |
| Outcomes | +30 s, +5 min, +15 min, +1 hour after our noticing time, same as the other tests |
| Control group | Tokens passing the same filters that no listed wallet bought (existing PASS group) |
| Costs | Same slippage and fee assumptions as the risk engine |
| Lateness | The gap between the wallet's buy and our noticing is recorded for every signal. Headline number |
| Repeat buys | Several buys of the same token by the same wallet count as ONE signal. The same token bought by two primary wallets counts as ONE signal with both wallets named |
| Secondary report | 2 or more independent operators (any list) buy the same token within 15 minutes. Reported, not judged |

## 4. How the verdict is judged (fixed now)

| Item | Rule |
|---|---|
| Sample needed | 100 or more primary signals after filters |
| Per wallet limit | No single wallet may supply more than 40% of counted signals. If one does, the verdict is also shown with that wallet removed. (This 40% limit is my addition to the approved option, flagged to Saed) |
| Counts as a pass | Median result better than the control group at +15 min AND positive after costs AND the same direction in several separate weeks AND still positive with the biggest single winner removed |
| Counts as a fail | Anything else |
| Too few signals by 26 Jan 2027 | The result is reported as INCONCLUSIVE, not as a pass or a fail |
| Reports | Weekly report gets Spy rows: signals, filtered, lateness median, per-wallet counts, result vs control |

## 5. Data and cost plan (estimates, not measured)

| Item | Estimate |
|---|---|
| Helius cost | 1 credit per lookup. Checking 7 wallets every 2 minutes is about 5,000 lookups a day, about 150,000 a month, plus one lookup per new transaction found. Under the 1,000,000 free monthly credits together with the main scanner. To be measured after switch-on |
| Expected signals | About 29 primary-wallet buys a day before filters, measured on 13 to 30 days of history. Filters will remove many |
| Where it runs | A separate Spy settings file and log. `thresholds.toml`, the risk settings and `shadow.db` are NOT changed for this unless Saed agrees |

## 6. Known weaknesses

- The slow wallets have the smallest samples (14 to 43 closed trades). Their past profit is partly luck.
- Lists built from past winners; only forward results count.
- Late arrival: we notice minutes late and the price may have moved.
- Wallets can change or go quiet. They are NOT replaced mid-test. A quiet wallet is reported.
- More than one strategy raises the chance of a false win. Spy is judged separately from the main scanner.
- 5 of the 7 wallets have much of their result in a few trades, and several positions are still open, so their results are the least certain.

## 7. Not decided yet

- Exact switch-on date (after Sun 1 Nov report).
- Polling interval (proposal: every 2 minutes).
- Whether to build the Spy code before or after the 9 Nov date in the master plan.
