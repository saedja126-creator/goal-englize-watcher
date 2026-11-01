# Spy wallet analysis (29 Oct 2026)

SHADOW MODE. Read-only, public addresses only. No keys, no orders. Full addresses are in `docs/SPY_WALLETS_PASTE_HERE.txt` (wallets here are shown by first 8 characters).

## Method and limits (read first)

- Source: 21 wallets that passed the activity screen (3 from batch 2, 18 from batch 3). Web search found no public labels. GMGN profile pages need a login, so they were not used.
- For each wallet: up to the 600 most recent successful transactions in the last 30 days (13 to 30 days of history depending on how busy the wallet is), read with Helius `getSignaturesForAddress` and `getTransaction` (1 credit each, 9,627 calls in total).
- Results are in SOL. They are APPROXIMATE: stablecoin-quoted trades and transactions with several tokens at once are ignored; fees, tips and token-account rent add noise; "closed" means the wallet sold at least 80% of what it bought in the window; positions still open are not valued.
- These are the wallets' own results with their own speed. A copier who is 2 to 5 minutes late would do worse. Treat every profit number as an upper bound for us.

## Per wallet

| Wallet | Days of data | Buys/day | Closed tokens | Net SOL on closed | Return on money used | Win rate | Typical hold | Biggest win as share of all gains | Typical buy (SOL) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| 7tkPWE2c | 13.8 | 16.5 | 177 | +153.8 | x1.75 | 40% | 1.3 min | 73% | 1.2 | Fast scalper. One trade did most of the work. Same tokens as CFkd. |
| CFkdHRyb | 14.6 | 16.2 | 186 | +17.0 | x1.08 | 46% | 1.3 min | 12% | 1.2 | Fast. Bought 181 of the same tokens as 7tkP: same operator or copying it. Count as ONE with 7tkP. |
| 5x8tfrJS (Tahi) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | NOT MEASURABLE here: 529 of 600 transactions are stablecoin-quoted. Unknown. |
| 84vL38o5 | 23.7 | 0.9 | 10 | +35.9 | x2.47 | 30% | 3.6 min | 82% | 2.5 | Tiny sample, one big win. Not evidence. |
| CzeYKKJJ | 21.0 | 7.1 | 61 | +0.2 | x1.00 | 44% | 1.5 min | 24% | 1.2 | Break-even, fast. Same operator as 77Uy (61 shared tokens). |
| 77Uy6sLL | 27.0 | 7.9 | 87 | +1.9 | x1.01 | 45% | 1.5 min | 17% | 1.3 | Break-even, fast. Count as ONE with CzeY. |
| BAdJW3mm | 29.5 | 1.7 | 17 | +1.7 | x1.16 | 65% | 7.8 hours | 44% | 0.3 | Slow, small, positive. Small sample (17). |
| tmdStKtu | 28.0 | 0.4 | 5 | +2.3 | x1.89 | 100% | 4.1 min | 20% | 0.5 | Only 5 closed trades. Not evidence. |
| 4bSUHKxB | 28.9 | 3.2 | 57 | +103.1 | x1.32 | 42% | 81 min | 84% | 3.5 | Slow, large. But one trade is 84% of gains: could be luck. |
| J8N8cW3A | 21.3 | 6.0 | 66 | +60.5 | x1.11 | 42% | 4.7 min | 53% | 5.0 | Fast-ish. Profit half from one trade. |
| Hsu75uJh | 24.7 | 2.7 | 51 | +10.1 | x1.02 | 29% | 18 sec | 41% | 6.6 | Bot-speed (18 sec). Break-even. Not copyable. |
| 8n9tnbCA | 24.2 | 5.5 | 101 | +107.2 | x1.32 | 62% | 3.7 min | 35% | 3.0 | Best numbers (101 trades, 62% wins), but holds only about 4 min: a 2 to 5 min delay eats the trade. |
| C32NsZNd | 26.1 | 5.7 | 36 | +66.7 | x1.08 | 39% | 3.6 hours | 43% | 9.1 | Slow, big size. Quiet for 3.6 days at check time. |
| 5dXRP54f | 13.0 | 5.3 | 14 | +44.3 | x2.09 | 71% | 6.0 hours | 54% | 0.2 | Slow, tiny size, only 14 closed. Many non-swap transactions. |
| EvWaM15D | 29.5 | 7.8 | 107 | +15.1 | x1.06 | 40% | 2.5 min | 26% | 2.0 | Fast, near break-even. |
| C7bFqgUr | 20.8 | 10.5 | 137 | -3.2 | x0.99 | 36% | 3.9 min | 20% | 1.5 | Loser/break-even. Drop. |
| AfGjJQkv | 29.9 | 1.2 | 18 | +12.4 | x1.15 | 67% | 31 min | 27% | 3.0 | Slow, positive, small sample (18). |
| DDsFBzcB | 29.6 | 3.5 | 43 | +7.7 | x1.08 | 42% | 34 hours | 25% | 1.4 | Very slow holder. Only 43 of 93 tokens closed, so the result is biased. |
| rnmpJGT2 | 20.6 | 11.1 | 183 | +10.7 | x1.07 | 33% | 1.9 min | 13% | 0.6 | Fast, near break-even. |
| HFLX1Gnx | 20.3 | 8.0 | 42 | +2.8 | x1.04 | 52% | 60 min | 20% | 1.0 | Slow, break-even. |
| ArfVe1K5 | 23.0 | 1.0 | 16 | +6.6 | x1.09 | 44% | 5.0 min | 41% | 5.0 | Small sample. Typical trade loses (median 0.82). |

## What the numbers say

1. **Almost no wallet is clearly good.** 14 of 20 measured wallets returned between x0.99 and x1.16 on money used, which is break-even once costs and lateness are counted. Typical single trade loses (median return per token is below 1.0 for most). Profit comes from a few big winners.
2. **Several results rest on one lucky trade.** For 7tkP, 84vL, 4bSU, J8N8 and 5dXR, the single biggest win is 50% to 84% of all gains.
3. **Duplicates:** 7tkP and CFkd are the same operator or copies of each other (181 shared tokens). 77Uy and CzeY too (61 shared tokens). So the 21 wallets are really 19 independent operators, and 18 measurable ones.
4. **Most wallets are too fast for us.** 12 hold for under about 5 minutes. A copier that notices 2 to 5 minutes late gets little of that move.
5. **Wallets that hold 30 minutes or more** (copyable timing): BAdJ (7.8 h), 4bSU (81 min), C32N (3.6 h), 5dXR (6 h), DDsF (34 h), AfGj (31 min), HFLX (60 min). 7 wallets. They also have the smallest samples and the most open positions, so their results are the least certain.

## How many signals would the proposed rule produce?

Proposed primary signal: 2 or more different operators buy the same token within 15 minutes.
Real count from the last 13 to 16 days: **11 independent events** (about 5 a week), before our liquidity and safety filters, which will remove some. Over the 11 weeks from 9 Nov to 26 Jan that is roughly 50 signals at most, below the 100 needed.
Because 7tkP/CFkd and 77Uy/CzeY buy together, a naive count shows 247 events. 242 of those are just these two pairs and are NOT independent.

## Options for the Spy primary signal (decision for Saed)

| Option | Signal | Rough volume (before filters) | Pros | Cons |
|---|---|---|---|---|
| 1. Keep as drafted | 2+ independent operators buy within 15 min, all 19 operators | about 5 a week, about 50 by decision day | Strongest evidence per signal | Too few signals to reach a verdict |
| 2. Slow group, single buy (RECOMMENDED) | A buy by any of the 7 slow wallets (BAdJ, 4bSU, C32N, 5dXR, DDsF, AfGj, HFLX) | about 29 buys a day combined | Enough signals within weeks. Our delay matters less because they hold 30 min or more | Weaker per signal. Small, noisy wallets. Needs a "per wallet" breakdown to avoid one wallet dominating. |
| 3. Both | Option 2 primary, Option 1 reported as secondary | as above | Keeps the strong version visible | Two things to judge, more false-win risk. Pre-declare which is primary. |

## Unverified or not done

- Tahi (5x8tfrJS) was not measurable. It trades stablecoin pairs.
- Profits ignore open positions and are before our delay, fees and slippage.
- Volume numbers rest on 13 to 16 days of data.
- Nothing is built or switched on. The screening rule and the final list still need Saed's approval.
