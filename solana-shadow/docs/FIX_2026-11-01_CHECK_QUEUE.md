# Fix 1 Nov 2026: new tokens were checked about 4 hours late

## What the week 1 report showed
- 7 signals in 5 days, 6 of them in the first 40 minutes after the first start (27 Oct).
- Median delay from "token first seen" to "first check": 258 minutes (p90 297).
- Tokens checked while 2 to 15 minutes old (the window the new_pair_flow strategy needs): 607 on 27 Oct, then 5, 1, 0, 1 a day.
- The control group (passed, no trigger) had a median age of 230 minutes, so it was not a fair comparison for 2 to 15 minute signals.

## Cause
The scanner checks `max_evals_per_cycle` (15) tokens every 30 seconds, OLDEST FIRST. New tokens arrive faster than that, so a queue of about 10,900 pools built up and fresh tokens waited at the back.

## What changed (code only; `thresholds.toml` untouched)
| File | Change |
|---|---|
| `shadowbot/db.py` | `due_pools` now orders newest first (by first seen). New `expire_stale` and `due_count`. `add_pool_if_new` can delay the first check. |
| `shadowbot/runner.py` | Pools first seen more than `watch_max_age_minutes` (360) ago are retired without a check. New pools are first checked after `stage1_free_cut.min_age_minutes` (2 min), because checking a brand-new pool only returns TOO_YOUNG and wastes a slot. Cycle stats now include `backlog` and `expired`. |
| `shadowbot/__main__.py` | Log line now ends with `backlog N retired N`. |
| `tests/test_shadowbot.py` | 2 new tests (newest first under the cap; stale pools retired unchecked). The full-cycle test now expects the 2 minute wait. 110 tests pass. |

No limit was raised: still 15 checks per cycle, same data calls.

## How to read the results from here
- Week 1 (26 Oct to 1 Nov) is a WARM-UP week. It is not test evidence for signals or for the control comparison.
- The test clock for signals and controls starts 1 Nov 2026 (about 23:10 UTC, scanner restarted twice).
- Watch the `backlog` figure in `data\run.log`. If it stays in the thousands, new tokens are again waiting too long, and the next lever is `max_evals_per_cycle` (a thresholds.toml change that needs Saed's OK).
- Old data stays in `shadow.db`. Nothing was deleted.

## Still true
- The 7 signals so far are too few to say anything. Four of the first six lost 34% to 97% within the hour; that is not evidence either way.
- The means in the weekly report (311,825% and 2,279%) come from one broken price reading (+1,874,755%). Read the medians.
