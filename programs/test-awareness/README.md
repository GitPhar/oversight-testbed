# Program 6: test-awareness

**Seed question, in Sean's words:** does a model behave differently when it thinks it is being tested?

**Why it matters for safety:** an evaluation only means something if the model behaves the same when it is not told it is one. If telling a model "this is a test" (or letting it guess) changes what it does, then test scores describe test behaviour, not the behaviour an overseer will meet in use.

**Models:** `claude-haiku-5-5`, `claude-sonnet-5-5`, `claude-opus-5-5`. **Budget:** $5.00 for the whole program, every bet and pilot included, enforced in code (`experiments/ta_common.py`). Stop on any refusal, program-wide; nothing is reworded or retried.

## Layout

- `map/reads/`: the scout's reads, one file per cluster of fields, every source recorded (`READER-BRIEF.md` is the brief each reader got).
- `map/program-6-map.md`: the ranked directions, with the engine's odds stated before any data.
- `experiments/`: pre-registrations (`<bet>.md`) and the code that runs them. `ta_common.py` holds the budget, refusal and design-review gates.
- `results/`: plain-English results first, then tables; raw calls cached as `*-calls.json` (content-keyed, so a crash never pays twice).
- `DEVIATIONS.md`: every pre-registration and every departure from one, dated.

All times America/Denver.
