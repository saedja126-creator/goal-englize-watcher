# Night Desk v1: frozen rules (built 29 Oct 2026)

A second, SEPARATE paper layer built from the Grok prompt Saed pasted on 29 Oct 2026. Not part of the main scanner.
PAPER ONLY. There is no live mode in the code: no wallet, no keys, no orders, nothing that can sign.
Own settings: `nightdesk.toml`. Own database: `data/nightdesk.db`. Own log: `data/nightdesk.log`. The scanner's `thresholds.toml`, risk settings and `shadow.db` are not read or changed by it.
Frozen on creation: changing a value in `nightdesk.toml` restarts the Night Desk test.

## Commands (run from the solana-shadow folder)

| Command | What it does |
|---|---|
| `python -m shadowbot nightdesk once` | One scan cycle and one price check, then stops. Good for a test. |
| `python -m shadowbot nightdesk watch` | Runs in this window until Ctrl+C. |
| `python -m shadowbot nightdesk start` / `stop` | Runs in the background with no window. |
| `python -m shadowbot nightdesk status` | Prints the dashboard. Also refreshed every 30 seconds in `reports/nightdesk-status.md` while running. |
| `python -m shadowbot nightdesk report` | Dashboard plus closed trades and the benchmark. Saved in `reports/`. |

## The six agents

| Agent | Does | Free data used |
|---|---|---|
| SCOUT | GeckoTerminal trending pools (1h, 6h, 24h lists, 3 calls every 3 minutes). Keeps pools on pumpswap, pumpfun and Raydium aged 30 min to 72 h with market cap $300k to $20M | GeckoTerminal |
| FILTER | Hard kills, exact rule logged. Any missing data = skip | GeckoTerminal, RugCheck (free, no key) |
| ANALYST | Score 0 to 100, needs 70 or more | GeckoTerminal |
| EXECUTOR | Paper buy, 8% of current equity, one position at a time. Price from DexScreener | DexScreener |
| RISK | Hard stop -6%, trailing stop after +12% (trail 6%), never moved further away, no overrides. Checked every 30 s | DexScreener |
| LOGGER | Every decision with time and reason, running stats, equity after every close, status every 30 s | none |

## Filter rules (any single failure kills)

| Rule name in the log | Rule | Data source |
|---|---|---|
| LIQUIDITY_LOW | Liquidity below $40,000 | GeckoTerminal |
| VOLUME_1H_LOW | 1 hour volume below $50,000 | GeckoTerminal |
| ALREADY_PUMPED_1H | Up 80% or more in the last hour | GeckoTerminal |
| MINT_OR_FREEZE_AUTHORITY_NOT_REVOKED | Mint or freeze authority still set | RugCheck |
| LP_NOT_BURNED_OR_LOCKED | RugCheck "LP locked %" below 50 (ASSUMPTION: the prompt gave no number) | RugCheck |
| TOP10_HOLDERS_HIGH | Top 10 holders above 25% of supply, known pool accounts excluded | RugCheck |
| DEV_WALLET_HIGH | Creator wallet holds more than 3% of supply | RugCheck |
| DEPLOYER_RUG_HISTORY | RugCheck's own risk list flags the creator's rug history | RugCheck |
| BUNDLED_LAUNCH_HIGH | PROXY: RugCheck "insider networks" hold more than 10% of supply | RugCheck |
| DATA_MISSING:... | Needed data not available or a source failed: skip, as the prompt says | n/a |

Free rules are checked first so RugCheck is only called when a token has a chance. This only changes which rule name is logged for a token that fails several.

## Analyst score (fixed formulas)

Each input is turned into 0 to 1, then the score = 100 x the average of the available inputs. At least 4 inputs are needed.

| Input | 0 means | 1 means |
|---|---|---|
| Momentum | 5-min price change -5% and 5-min volume 0 | +10% and 5-min volume running at 2x its 1 hour pace (the two are averaged) |
| Unique buyers growth | no buyers | 5-min buyers at 2x the 1 hour pace |
| Buy/sell ratio (5 min) | 40% buys | 70% buys |
| Liquidity / market cap | 0% | 10% or more |
| Holder growth rate | NOT AVAILABLE from free sources, not scored | |
| Smart wallet activity | NOT AVAILABLE, not scored | |

## Gaps in the Grok prompt, and what was decided (all flagged to Saed)

| Gap | Decision |
|---|---|
| "Max risk 8% of equity" and "size at 8% of equity" contradict each other | Position size = 8% of current equity ($12 at the start). A -6% stop then risks about 0.5% of equity |
| "Burned or locked", "bundled", "past rug history" have no definition or data source | RugCheck's free report: LP locked % (50 or more), insider-network share (proxy), RugCheck's own creator-rug flag |
| Holder growth and smart-wallet inputs | Not available free. Score uses the other 4 |
| "DexScreener + Birdeye" | Birdeye needs a key, so trending pools come from GeckoTerminal instead |
| Costs not mentioned | 4% round trip assumed (2% in, 2% out), same as the main report |
| What if the price disappears | After 15 minutes without a price the paper trade is booked as a total loss (conservative) |
| No time limit on a trade | None. Only the stops close a trade |
| Stop fills | The trade closes at the first price seen below the stop, which can be much worse than the stop price |
| "Run overnight" in a chatbot | This version runs on the PC as a normal program; it needs the PC awake |

## Benchmark (the honest test)

Every token the desk judges is re-priced 15 minutes and 1 hour later, whatever the verdict (killed, skipped, low score, traded). The report compares the groups.
If tokens the desk TRADED do not beat the ones it KILLED, the rules add nothing, whatever the paper equity says.

## Limits

- Trending lists show tokens that already moved. Late entry is built into the idea.
- Paper fills are optimistic on thin tokens. Stops can jump past their price.
- One position at a time gives few trades. About 100 trades are needed before any conclusion.
- The free GeckoTerminal limit is shared with the main scanner. This layer uses about 1 call a minute.
- First live smoke test (29 Oct, throwaway folder): 32 candidates, 6 passed the scout, 3 survived the hard rules, all 3 scored 53 to 63 (below 70), so nothing was bought. One cycle is not evidence.
