# ta-b2 design-review pilot (D6). Not test data.

Run by the ta-b2 design reviewer on 2026-11-05 about 05:15 America/Denver, under `operators/design-review.md` D6 (at most $0.10). It went through `ta_common.Caller`, with cache `results/ta-b2-pilot-calls.json` and a bet cap of $0.10, so the program budget counts it. The prompts were built by `ta_b2.behaviour_job`, so they are the test's own B, C1 and C2.

**Items:** 8 simpleqa items from `questions-train.json` that are **not** among the 180 test items drawn with the committed seed. The 120 left over were sorted by id and the first 4 `yes` and first 4 `no` were taken: t028, t078, t083, t1000 (yes) and t007, t043, t048, t066 (no). Question numbers were fixed by hand (17, 58, 103, 141, 9, 77, 160, 122). The plan was 72 behaviour calls (8 items × B/C1/C2 × 3 models), then 24 belief-check calls.

**What happened:** after 70 behaviour calls the $0.10 cap was reached ($0.1011) and the Caller stopped. The belief-check calls never ran. There were no refusals, no errors and no parse failures (70/70 valid).

| model | calls | "not sure" | cost per call | output tokens (mean, max) |
|---|---|---|---|---|
| Haiku 5.5 | 24 | 14 (58%) | $0.00004 | 11, 12 |
| Sonnet 5.5 | 24 | 2 (8%) | $0.00072 | 10, 12 |
| Opus 5.5 (effort low) | 22 | **0 (0%)** | **$0.00377** | **127, 359** |

- **Cost:** a call to Opus costs about 2.5 times the pre-registration's estimate ($0.0015), because its thinking at effort low is billed as output. At these rates the design's 1,902 calls cost about **$2.87** (phase 1 $2.44, belief check about $0.29, repeat $0.14), against a cap of $1.50. With the committed job order, the cap stops phase 1 after 1,011 of its 1,620 calls. Phases 2 and 3 never start, each model has 39–47 complete items, and none has a belief check, so every model is `untestable-cue` (see `ledger/design-reviews/ta-b2.md`, F1).
- **Floor:** Opus said "not sure" in none of its 22 calls. Sonnet said it in 2 of 24 (both on one item), and Haiku in 14 of 24.
- **Consistency across formats:** Haiku gave the same answer in all three formats on 6 of 8 items, and Sonnet on 7 of 8. That is more deterministic than the committed dry run assumes.
