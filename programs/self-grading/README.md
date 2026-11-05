# Self-Grading (placeholder name)

Program 5 of the scalable-oversight testbed (the engine: this repository's root). The working name comes from the folder slug; a real title waits for the program's own write-up (CONTEXT.md §0: sessions do not propose names).

## The seed question

**Does a model grade its own work more kindly than someone else's identical work?** (Sean, steer st-17.)

Why it matters for oversight: this testbed exists because an AI grading its own research drifts toward what looks good to itself. The founding week saw it twice, and both times a re-check caught it. If a model gives its own work a better grade than it gives the same words from someone else, then any loop where a model checks its own output (self-review, self-critique, an AI scientist grading its own papers, an auditor of the same family as the author) is tilted, and the tilt can be measured and priced.

What earlier programs already say, on Haiku: a number framed as the model's own earlier answer pulled its next rating by +0.37, against about 0 for the same number framed as another person's (program 1, bm1). But program 2 found the reverse pull once (om-p2-3b: another reader's answer pulled more) and found that the turn an answer sits in matters more than its label (om-p2-6). So "own" is not a settled lever here, which is why the question is worth a program.

## Status

Opened 2026-11-04 23:38 America/Denver. The session crashed at 23:44 and was resumed on 2026-11-05 (starting point `753e334`).
- **Budget:** $5.00 of API for the whole program, enforced in code (`experiments/sg_common.py`); **$4.69 spent** (after sg-b4 and sg-b5).
- **Models:** `claude-haiku-5-5`, `claude-sonnet-5-5`, `claude-opus-5-5`.
- **The scout and the map:** 61 reads in four clusters (`map/reads/`), and ten directions with the engine's odds written before any data (`map/program-5-map.md`).
- **Wave 1, 2026-11-05:** three bets, each pre-registered in its own commit with a lesson, a dumb baseline and frozen verdict sentences. Each had a fresh design review (all three fix-first, then confirmed), a sealed plant draw and a fresh audit. No refusals. No human odds: Sean's first cockpit lines reached the ledger after these pre-registrations.

| bet | question | verdict (audited) | engine odds | result file |
|---|---|---|---|---|
| sg-b1 | Is a model kinder to its own conclusion when it grades it in the conversation that wrote it? | **fail-same**: own minus fresh −1.1 (Haiku), −0.4 (Sonnet), −0.9 (Opus) points of 100, all within ±3; audit stands, 3 cuts | 24 | `results/sg-b1-placement.md` |
| sg-b2 | Does "written by you" earn a kinder grade than "written by another AI model", words unchanged? | **fail-same**: −0.0, +0.2, −0.5, all within ±3; audit stands, 3 cuts | 13 | `results/sg-b2-label.md` |
| sg-b3 | Grading in the conversation that wrote it, does a model dock a planted overclaim less? | **pass, unreplicated**: Haiku docked it 12.6 points less, Opus 6.0 less, Sonnet 1.4 (not over the bar); audit stands, 5 cuts (one was the plant, caught) | 18 | `results/sg-b3-flaw.md` |
| sg-b4 | Is sg-b3's blunting carried by the text sitting in the model's own reply, or by the layout and lead-in? (quoted copy of the conversation, lead-in kept) | **pass, unreplicated**: the quoted copy took away 6.8 of Haiku's 12.6 points and 4.0 of Opus's 5.5 (bars 6.3, 3.0; Haiku thin, fragile to one domain); audit stands, 3 cuts; novelty partly new | 18 (Sean 65) | `results/sg-b4-quoted.md` |
| sg-b5 | Does a model still go easier on the exaggeration when it replaces the last sentence, so the answer is no longer than asked? | **fail**: Opus's gap fell to 3.4 (under the 5-point bar); Haiku unchanged at 12.5; the swap also removed the caveat; audit stands, 4 cuts (one the plant, caught) | 22 (Sean 55) | `results/sg-b5-length.md` |

**In one line:** on this work, these models were not kinder to their own good work, whether told they wrote it or grading it where they wrote it. But two of the three went easier on a planted exaggeration sitting in their own turn of the conversation. That is the self-grading failure this testbed was built to catch, and it was already in print before we bet: Self-Attribution Bias (Khullar et al., March 2026, arXiv 2603.04582) and Self-Correction Bench (Tsui, July 2025, arXiv 2507.02778) report the same effect on earlier Claude models, so sg-b3 is a replication on the 5.5 models and one design, graded rather than counted, with Sonnet showing no gap (**Novelty: known**; rule 13; `paper/informed-engine.md`).

## Rules inherited from the engine

Odds before data, both sides, in writing. Cheapest falsifier first. Every test pre-registered in its own commit before its first call, with a lesson from the ledger and a fresh design review that says go. One scale direction in every graded prompt (0 = the worst end, 100 = the best end). Budgets enforced in code. Stop on refusal: nothing reworded or retried. No result without an independent audit, with a sealed plant draw. Nothing disappears: dead directions stay on the map with a diagnosis. Plain English first.

## Reproducibility

One command, from the repository root, with Python 3 and numpy installed (no keys, no network):

    python3 programs/self-grading/reproduce.py

The root `python3 reproduce.py` runs it too and prints one line for this program. It takes a copy of the program as committed. Nothing is called, and nothing outside the standard library and numpy is used.

What it checks:
- **The analyses.** It runs each bet's own `analyse` step on the archived call caches (`results/<bet>-write-calls*.json`, `results/<bet>-grade-calls*.json`). The three main analyses and sg-b1's pilot come out byte for byte the same as the committed `results/<bet>-analysis*.json`.
- **sg-b3's pilot** (`results/sg-b3-analysis-pilot.json`) was committed with its design review, before fixes D9a–D9g added fields to the analysis. Every value the pilot file has is checked exactly. The 18 fields added later (6 per model, such as `clean_D_ci` and `flawed_D_ci`) are counted and named, not compared. A value in both that differed would still fail.
- **The write-ups.** For `results/sg-b1-placement.md`, `sg-b2-label.md` and `sg-b3-flaw.md`, every table is rebuilt from the regenerated analysis and the caches, with the write-up's rounding, signs and bold. Each is compared line for line. Every number is recomputed, including the n in row labels. Column headers and row labels without a number are copied, and counted. The number of tables in each file is checked too.
- **Numbers in the prose.** Calls, spend, tie counts, gate values, pooled estimates and the verdict, where the plain-English part copies them, are checked the same way.

Two numbers in sg-b3-flaw.md are exact decimal ties printed to one place: 63.05 in a table and 8.85 in the prose. The write-up rounds them up; Python rounds them down. Either printing is accepted, and the script counts them. Elsewhere the write-up rounds such ties down (89.85 as 89.8), so both are faithful.

Not checked, because no archived code computes them: sg-b3's logit-scale gaps (0.97, 1.19), the audit's 20-domain bootstrap quoted in sg-b3, and sg-b1's own − fresh2 interval (−1.0 [−1.6, −0.4]).

Nothing the tables need is missing from the archive. A new results file fails the script until it is taught there.
