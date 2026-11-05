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

The root `python3 reproduce.py` runs it too and prints one line for this program. It takes a copy of the program as committed, with keys removed, the network blocked and every package except numpy stubbed out. Then it checks two things.

- **The analyses.** It runs the `--analyse` step of `experiments/ta_b2.py` and `ta_b3.py` on the archived calls (`results/<bet>-calls.json`) and compares the `results/<bet>-analysis.json` it writes with the committed one. ta-b2's matches byte for byte. ta-b2 reads program 1's questions, so `programs/entangled-mind/experiments/questions-train.json` and `questions-hard.json` are in the copy too. `ta_common.py` names program 1 by an old absolute path; the script points it into the copy, and checks that nothing is read from outside it.
- **The tables.** Every table in the five write-ups (`ta-b1-pilot.md`, `ta-b2-pilot.md`, `ta-b3-pilot.md`, `ta-b2-results.md`, `ta-b3-results.md`) is rebuilt and compared line for line. The results tables come from the regenerated analysis. The pilot tables come from the pilot call caches (`results/<bet>-pilot-calls.json`). Every number is recomputed. Row labels and column headers are copied, and the output counts both. The prose is not compared. The run log `ta-b2-run.log` is not a table and is skipped.

Three things to know:

- ta-b3 uses scipy's t quantile, which the clean copy does not have. The script computes it itself with the standard library. Its value is correctly rounded; scipy's differs in the last one or two binary digits. So the four fields built from it (`t_upper_bonferroni_AB` and `t90_AB`, Sonnet and Opus) are compared to 1e-12 relative, not byte for byte. They agree to 5e-16. Every other field matches exactly.
- The ta-b3 pilot ran on the question generator as pre-registered (979ec5d), before fix T5 changed it. Today's generator gives different questions from the same seed. The script uses the pre-registered generator and checks each of the 9 rebuilt prompts against the hash stored in the pilot cache.
- In `ta-b1-pilot.md`, Opus's "median" output tokens (93) is the upper of the two middle values of 16 calls. The usual median, their average, is 63.5. The script checks 93 as the upper median and says so in its output.

Nothing is missing from the archive: there are no gaps. ta-b1 was withdrawn and ta-b1r has no calls yet. When a new analysis or write-up lands, the script fails on it until its tables are added to `reproduce.py`.
