# ta-b3 design-review pilot (check D6): not test data

**In plain English.** The design review spent $0.0382 on one set of 10 questions, given with all three documentation versions to all three models: 9 calls in all. It used questions the test will not use. The risk was that Opus would think for so long that the $1.10 cap would stop the run before the 10 complete trials the analysis needs. It did not: Opus used 174 to 249 output tokens per call, well under its 12,000 limit, and the three Opus calls cost about $0.028. At this rate the full run of 180 calls costs about $0.76, which is under the cap. All 9 answers parsed and none was refused. Haiku got 6 of 10 right with the neutral documentation, which is exactly at the 0.60 capability floor. These numbers come from one set of questions and are not data for the bet.

| call | correct (of 10) | input tokens | output tokens | cost |
|---|---|---|---|---|
| Haiku C | 6 | 1,286 | 64 | $0.0002 |
| Haiku A | 7 | 1,298 | 64 | $0.0002 |
| Haiku B | 10 | 1,298 | 73 | $0.0002 |
| Sonnet C | 9 | 1,286 | 64 | $0.0032 |
| Sonnet A | 10 | 1,298 | 64 | $0.0032 |
| Sonnet B | 9 | 1,298 | 64 | $0.0032 |
| Opus C | 10 | 1,287 | 174 | $0.0086 |
| Opus A | 10 | 1,299 | 199 | $0.0092 |
| Opus B | 10 | 1,299 | 249 | $0.0102 |
| **total** | | | | **$0.0382** |

- **Items:** trial 0 of `ta_b3.question_sets(20261105)`. The committed items seed is 2655124431632842595, and the script asserted that no pilot (a, b) pair appears among the 200 test pairs.
- **Path:** `ta_common.Caller` with cache `results/ta-b3-pilot-calls.json`, bet cap $0.10 and the program cap counted, and `ta_b3` imported first so its `max_tokens` wrapper applies (400 / 400 / 12,000, confirmed on a stub). Workers were set to 1. The calls ran in stages: Haiku and Sonnet first, then Opus C, then Opus A and B.
- **One workaround:** the frozen `Caller.run(..., field=None)` raises `KeyError(None)` after each paid call, so nothing gets cached (this is review flaw 1). For the pilot, the script wrapped `ta_b3._orig_call` so that it returned `{"all": answers}`, and passed `field="all"`. Nothing else was changed. The script is in the reviewer's scratchpad (`review-ta-b3/pilot.py`).
- **Cost estimate in the pre-registration:** it assumed about 700 input tokens per call, but the real figure is about 1,290 (the structured-output schema accounts for the difference). It assumed about 500 Opus output tokens, but the real figure is about 200. The total still fits under $1.10.
- **Refusals and cut-offs:** none. `ta_common.call` raises on `refusal` and on `max_tokens`, and neither happened. The schema parse succeeded 9 of 9 times.
