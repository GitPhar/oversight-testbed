# Said vs did (placeholder name)

Program 7 of the scalable-oversight testbed (the engine: this repository's root). The working name comes from the folder slug; a real title waits for the program's own write-up (CONTEXT.md §0).

**Seed question (Sean):** when a model says it is unsure, does it act unsure? Program 1 found the stated number is built by the question; this program asks whether it predicts anything the model then does: hedging, asking for more, changing its answer under pushback, declining to act. The safety reason: an overseer can only use a model's stated confidence if it predicts the model's behaviour.

**Models:** `claude-haiku-5-5`, `claude-sonnet-5-5`, `claude-opus-5-5`. **Budget:** $5.00 for the whole program, enforced in code (`experiments/svd_common.py`). Stop on any refusal, program-wide.

- `map/reads/`: the scout's reads (87, six readers on disjoint lists plus one scout read).
- `map/program-7-map.md` (and `.json`): thirteen open directions and one killed, with the engine's odds stated before any data.
- `experiments/`: the wave-1 pre-registrations (`sv-b1.md`, `sv-b2.md`, `sv-b3.md`), their shared code and committed dry runs; wave 2's `sv-b5.md` (SV-1r, Sonnet backing down) and `sv-b6.md` (SV-2w, declining within trivia), each with its own script (`sv_b5.py`, `sv_b6.py`) and dry runs.
- `DEVIATIONS.md`: every pre-registration and every departure from one, dated.

All times America/Denver.

## Reproducibility

One command, from the repository root, with Python 3 and numpy installed (no keys, no network):

    python3 programs/said-vs-did/reproduce.py

The root `python3 reproduce.py` runs it too and prints one line for this program. It takes about 3 seconds. It takes a copy of the program as committed, plus program 1's hard pool (`programs/entangled-mind/experiments/questions-hard.json`), which holds the items. Nothing is called, and nothing outside the standard library and numpy is used. Nothing is read from outside that copy: the script checks every module and every path the program's code holds.

What it checks:
- **The analyses.** It runs the wave-1 script's own `analyse` step (`experiments/svd_wave1.py analyse b1|b2|b3`) on the archived call caches (`results/sv-said-calls.json`, `results/sv-<bet>-calls.json`). Each `results/sv-<bet>-analysis.json` comes out byte for byte the same.
- **The generated part of each write-up.** `results/sv-b1-pushback.md`, `sv-b2-decline.md` and `sv-b3-ask.md` each hold a section printed by `experiments/svd_report.py`: the verdict, the pre-registered sentences and every table in the file. The script runs `svd_report.py` on the regenerated analysis. Every line it prints must appear in the write-up, in order. No cell is copied. The file's table count must match, so no table sits outside the check.
- **Insertions in that section.** A paragraph between generated lines is allowed only if it says it is the auditor's or exploratory. Extra blank lines are allowed too. The script names each one. Anything else between generated lines fails. Today there is one: a blank line left in sv-b1's section when the audit's below-floor paragraph was moved to just below it. That paragraph's numbers are still checked.
- **The hand-written part.** The plain-English lead and the "Run" section copy numbers from the analysis and the caches: counts, AUROCs, margins and intervals, confidence bins, secondary percentages, and costs. Each is rebuilt and checked. So is the lead's verdict and its first sentence, which must be the first pre-registered sentence.
- **The audit's own figures.** Where the program's code can compute them, they are recomputed and checked:
  - sv-b1: Sonnet's and Opus's below-floor AUROC, best simple guess and margin, with the bet's own bootstrap and seed;
  - sv-b1: question length doing worse than chance inside every question type;
  - sv-b2: most declines falling within SimpleQA, and no decline on the 60 author-written claims;
  - sv-b3: leaving out one question type at a time (Sonnet clears the 0.10 condition only without physics; Haiku stays below 0).

Two values are accepted in a second faithful printing, and the script names both:
- Opus's agreement with the never-check rule in sv-b3 is 71 of 80, exactly 88.75%. The write-up prints 88.7%; Python prints 88.8%. Either is accepted.
- sv-b3's cost is printed as $0.600, the sum of its printed parts ($0.424 + $0.176). The exact cost is $0.6006, which rounds to $0.601. Both printings are accepted, and the script says which one the write-up used.

Not checked:
- sv-b2's "stated confidence is about the same on trivia and non-trivia questions". It is the auditor's exploratory re-analysis and states no number.
- Commit hashes.
- The thresholds the prose restates (75%, 87.5%). They are fixed in the code, not results.

**Wave 2 (sv-b5, sv-b6).** Each bet's own script has an `analyse` step that makes no calls (`experiments/sv_b5.py`, `sv_b6.py`). The script runs it on the archived caches (`results/sv-b5-calls.json`; `results/sv-b6-said-calls.json` and `sv-b6-decline-calls.json`, with `data/sv-b6-items.json`), and `results/sv-b5-analysis.json` and `sv-b6-analysis.json` must come out byte for byte the same. Each write-up (`results/sv-b5-pushback.md`, `sv-b6-decline-trivia.md`) must contain the script's own `report` output verbatim. Every decimal of two or more places in its plain-English and limits sections must appear in that generated block. The Novelty line is excepted, since it quotes papers. Not checked: the header's odds, and the Run section's program-wide spend (a budget figure that later bets change). sv-b6's item draw needs the SimpleQA CSV, which is not archived; the draw is checked by its pre-registered SHA-256 and the committed items file, not rebuilt here.

Wave 1 wrote no run log, error log or refusal record. The "Run" check relies on their absence. Nothing the tables need is missing from the archive. A new results file fails the script until it is taught there.
