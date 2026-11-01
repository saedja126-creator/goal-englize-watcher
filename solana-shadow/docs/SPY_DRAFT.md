# Spy strategy: DRAFT for approval (written 29 Oct 2026)

SHADOW MODE ONLY. Nothing here places an order, creates a wallet or needs a key. Wallet addresses are public information.
Nothing in this file is built or switched on. It becomes active only after Saed approves it and after the first weekly report (Sun 1 Nov).
Once approved, these rules are FROZEN and dated. Changing them later means the test restarts.

## 1. The one question

When wallets with a good recent record buy a new token, does a token we notice AFTER their buy do better than a similar token nobody followed, after costs?

## 2. What I found while checking free data (29 Oct)

| Item | Finding | Confidence |
|---|---|---|
| GMGN rankings as a free feed | No free official API found. Sources say access is restricted or paid (about $39 a month for API on one comparison site). The website leaderboard can be read by a person. | Medium (secondary sources) |
| Cielo free tier | One review says 50 wallets, Saed's earlier notes say 10. Not confirmed on Cielo's own page. | Low |
| Helius free plan | Current docs: 1M credits a month, 10 RPC requests a second. Credit cost of watching a wallet not checked yet. | Medium |
| Our own scanner vs Jupiter (3 hour check) | We missed 52% of Jupiter's tokens, but only 7 of 3,838 missed ones ever showed $10,000+ liquidity. Discovery is not the weak link for tradable tokens. | High (one 3 hour sample, 9 of 539 polls rolled over) |

## 3. Where the wallet list comes from (Saed to choose)

| Option | How | Cost | Weakness |
|---|---|---|---|
| A. By hand from GMGN | Saed opens the GMGN smart-money page in his browser and copies 20 to 30 public addresses into a text file I give him. | 0 | Sorted by past winners, so partly lucky. Takes him about 15 minutes. |
| B. Build our own list | I rank wallets from on-chain data (Helius) using rules fixed first: many closed trades, not one lucky win. | 0, uses part of the free Helius quota | More work. Still sorted by past results. |

I will NOT invent or guess wallet addresses.

## 4. Proposed rules (all proposals until approved)

| Rule | Proposal |
|---|---|
| List size | 20 to 30 wallets, frozen on one date, never changed during the test |
| Before freezing, each wallet needs | At least 30 closed trades in the last 30 days (so one lucky trade cannot qualify) |
| What we watch | Buys of tokens that are also new to our scanner |
| Primary signal (SPY_SIGNAL) | 2 or more different listed wallets buy the same token within 15 minutes |
| Secondary, description only, NOT used to judge | A single listed wallet buys. Logged so we can learn, never counted as a win or a loss for the test |
| Same hard filters as our main strategy | Liquidity at least $10,000 and the on-chain checks. Failing tokens are logged as FILTERED with the reason |
| Entry price | The price when WE notice it, not the wallet's price (that is the price we could really get) |
| Outcomes | +30 s, +5 min, +15 min, +1 hour, same as the other tests |
| Control group | Tokens passing the same filters that no listed wallet bought (the existing PASS group) |
| Costs | Same slippage and fee assumptions as the risk engine |
| Lateness | Record the gap between the wallet's buy and our notice. This is a headline number |
| Sample needed | 100 or more primary signals before any conclusion |
| Counts as a pass | Median result better than control at +15 min AND positive after costs AND the same direction across several weeks |
| Counts as a fail | Anything else. Stated now so we cannot move the goalposts later |

## 5. Known weaknesses (honest)

| Weakness | Why it matters |
|---|---|
| Lists built from past winners | Some of those wallets were lucky. The test counts only trades after the freeze. |
| Late arrival | Bots buy within seconds. Our polling is slower, so we may only see leftovers. |
| Crowding | If many people copy the same wallets, the price is already pushed up. |
| Wallets can change behaviour or go quiet | We do not replace them mid-test, so the list may decay. We will report that. |
| More strategies, more chances of a false win | The main scanner and Spy are judged separately, and the Spy pass bar above is fixed in advance. |
| Free quota | Watching 20 to 30 wallets by checking every 30 seconds may use up Helius free credits. A slower check (for example every 2 to 5 minutes) would be late. To be measured before switching on. |

## 6. What I need from Saed

1. Choose option A or B in section 3.
2. Approve or change the table in section 4.
3. Say go after he has read the first weekly report.

## 7. What I will NOT do

Touch thresholds.toml, the risk settings or the main database for this work. Spy will use its own settings file and its own log file.
