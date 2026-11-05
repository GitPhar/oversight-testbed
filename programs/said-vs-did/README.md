# Said vs did (placeholder name)

Program 7 of the scalable-oversight testbed (the engine: this repository's root). The working name comes from the folder slug; a real title waits for the program's own write-up (CONTEXT.md §0).

**Seed question (Sean):** when a model says it is unsure, does it act unsure? Program 1 found the stated number is built by the question; this program asks whether it predicts anything the model then does: hedging, asking for more, changing its answer under pushback, declining to act. The safety reason: an overseer can only use a model's stated confidence if it predicts the model's behaviour.

**Models:** `claude-haiku-5-5`, `claude-sonnet-5-5`, `claude-opus-5-5`. **Budget:** $5.00 for the whole program, enforced in code (`experiments/svd_common.py`). Stop on any refusal, program-wide.

- `map/reads/`: the scout's reads (87, six readers on disjoint lists plus one scout read).
- `map/program-7-map.md` (and `.json`): thirteen open directions and one killed, with the engine's odds stated before any data.
- `experiments/`: the wave-1 pre-registrations (`sv-b1.md`, `sv-b2.md`, `sv-b3.md`), their shared code and committed dry runs.
- `DEVIATIONS.md`: every pre-registration and every departure from one, dated.

All times America/Denver.

## Reproducibility

One command, from the repository root, with Python 3 and numpy installed (no keys, no network):

    python3 programs/said-vs-did/reproduce.py

The root `python3 reproduce.py` runs it too and prints one line for this program. It takes a copy of the program as committed, runs the wave-1 script's own `analyse` step (`experiments/svd_wave1.py analyse b1|b2|b3`) on the archived call caches (`results/sv-said-calls.json`, `results/sv-<bet>-calls.json`), and checks that `results/sv-<bet>-analysis.json` comes out byte for byte the same.

Today there is nothing to rebuild: no call has been made. When an analysis or a results write-up (`results/*.md`) lands, the script picks the analysis up by name; a write-up's tables are added to `reproduce.py` in the same commit, or the script fails on the unregistered file.
