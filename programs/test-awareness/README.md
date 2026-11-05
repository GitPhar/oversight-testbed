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

## Reproducibility

One command, from the repository root, with Python 3 and numpy installed (no keys, no network):

    python3 programs/test-awareness/reproduce.py

The root `python3 reproduce.py` runs it too and prints one line for this program. It takes a copy of the program as committed, runs each bet's own `--analyse` step (`experiments/ta_b1.py`, `ta_b2.py`, `ta_b3.py`) on its archived call cache (`results/<bet>-calls.json`), and checks that `results/<bet>-analysis.json` comes out byte for byte the same.

Today there is nothing to rebuild: no bet has run, and the only archived calls are the cost probe's (`results/probe-calls.json`), which feed no table. When a bet's analysis or a results write-up (`results/*.md`) lands, the script picks the analysis up by name; a write-up's tables are added to `reproduce.py` in the same commit, or the script fails on the unregistered file. Nothing is missing from the archive.
