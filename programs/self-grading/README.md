# Self-Grading (placeholder name)

Program 5 of the scalable-oversight testbed (the engine: this repository's root). The working name comes from the folder slug; a real title waits for the program's own write-up (CONTEXT.md §0: sessions do not propose names).

## The seed question

**Does a model grade its own work more kindly than someone else's identical work?** (Sean, steer st-17.)

Why it matters for oversight: this testbed exists because an AI grading its own research drifts toward what looks good to itself. The founding week saw it twice, and both times a re-check caught it. If a model gives its own work a better grade than it gives the same words from someone else, then any loop where a model checks its own output (self-review, self-critique, an AI scientist grading its own papers, an auditor of the same family as the author) is tilted, and the tilt can be measured and priced.

What earlier programs already say, on Haiku: a number framed as the model's own earlier answer pulled its next rating by +0.37, against about 0 for the same number framed as another person's (program 1, bm1). But program 2 found the reverse pull once (om-p2-3b: another reader's answer pulled more) and found that the turn an answer sits in matters more than its label (om-p2-6). So "own" is not a settled lever here, which is why the question is worth a program.

## Status

Opened 2026-11-04 23:38 America/Denver; the session crashed at 23:44 and was resumed on 2026-11-05 (starting point `753e334`). Budget **$5.00 of API for the whole program**, enforced in code (`experiments/sg_common.py`). Models: `claude-haiku-5-5`, `claude-sonnet-5-5`, `claude-opus-5-5`.

- `map/reads/`: the scout's Read records, one file per cluster.
- `map/program-5-map.md` (and `map/self-grading.json` at the engine root, for the site): ranked directions with the engine's odds stated before any data.
- `map/human-odds.md`: the form for Sean's odds (no engine odds shown); his odds come only from `ledger/human-odds.jsonl`.
- `experiments/`: pre-registrations and code. `results/`: results files, plain English first.
- `DEVIATIONS.md`: every departure from a pre-registration, dated.

## Rules inherited from the engine

Odds before data, both sides, in writing. Cheapest falsifier first. Every test pre-registered in its own commit before its first call, with a lesson from the ledger and a fresh design review that says go. One scale direction in every graded prompt (0 = the worst end, 100 = the best end). Budgets enforced in code. Stop on refusal: nothing reworded or retried. No result without an independent audit, with a sealed plant draw. Nothing disappears: dead directions stay on the map with a diagnosis. Plain English first.
