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

The root `python3 reproduce.py` runs it too and prints one line for this program. It takes about 3 seconds. It takes a copy of the program as committed, plus program 1's hard pool (`programs/entangled-mind/experiments/questions-hard.json`), which holds the items. Nothing is called, and nothing outside the standard library and numpy is used. Nothing is read from outside that copy: the script checks every module and every path the program's code holds.

What it checks:
- **The analyses.** It runs the wave-1 script's own `analyse` step (`experiments/svd_wave1.py analyse b1|b2|b3`) on the archived call caches (`results/sv-said-calls.json`, `results/sv-<bet>-calls.json`). Each `results/sv-<bet>-analysis.json` comes out byte for byte the same.
- **The generated part of each write-up.** `results/sv-b1-pushback.md`, `sv-b2-decline.md` and `sv-b3-ask.md` each hold a section printed by `experiments/svd_report.py`: the verdict, the pre-registered sentences and every table in the file. The script runs `svd_report.py` on the regenerated analysis and checks that its output appears in the write-up exactly. No cell is copied. The file's table count must match, so no table sits outside the check.
- **The hand-written part.** The plain-English lead and the "Run" section copy numbers from the analysis and the caches: counts, AUROCs, margins and intervals, secondary percentages, and costs. Each is rebuilt and checked. So is the lead's verdict and its first sentence, which must be the first pre-registered sentence.

Two values are accepted in a second faithful printing, and the script names both:
- Opus's agreement with the never-check rule in sv-b3 is 71 of 80, exactly 88.75%. The write-up prints 88.7%; Python prints 88.8%. Either is accepted.
- sv-b3's cost is printed as $0.600, the sum of its rounded parts ($0.424 + $0.176). The exact cost is $0.6006, which rounds to $0.601. Both printings are accepted, and the script says which one the write-up used.

Not checked: commit hashes, and the thresholds the prose restates (75%, 87.5%, 0.10), which are fixed in the code, not results. Wave 1 wrote no run log, error log or refusal record. The "Run" check relies on their absence. Nothing the tables need is missing from the archive. A new results file fails the script until it is taught there.
