# How the engine's odds for program 7 were elicited

Written 2026-11-05 05:00 America/Denver, before any program-7 data existed.

## Procedure (odds template v1, `operators/scout.md`, in its `v1-batch` variant as program 3 used it)

1. **The rows.** The scout wrote one row per direction (`rows-v1.md`, committed at 073ac30 before any odds existed): assumption at stake, prior work, our data, cheapest test, cost and a draft pass rule.
2. **The headline odds** (`v1.md`): one fresh context that read only `rows-v1.md` (no reads files, no ranking, no human odds, no other bets' outcomes). For each direction, in id order: a rationale of at most 100 words, then one integer from 1 to 99, P(pass) of the draft pass rule as written. Scale: 0 = certainly will not pass, 100 = certainly will. Elicited 2026-11-05 04:55.
3. **The elicitation check.** A random half drawn with `random.Random(20261105).sample(ids, 7)`: SV-2, SV-3, SV-7, SV-10, SV-11, SV-13, SV-14. Two more fresh contexts:
   - paraphrase (`check-paraphrase.md`): the same rows, each pass rule reworded with the same meaning (`rows-paraphrase.md`);
   - negation (`check-negation.md`): the original rows, asked for P(not pass) (`rows-negation.md`).
4. **The ranking** was set afterwards by the scout in `../program-7-map.md`. The odds were not revised after ranking.

All three elicitors were `claude-opus-5-5`, the same model as the scout. Departure from template v1, as in program 3: one fresh context saw all rows at once (3 contexts, not 28), so cross-row anchoring is possible (`v1-batch`).

## The numbers

Headline P(pass) (v1):

| id | SV-1 | SV-2 | SV-3 | SV-4 | SV-5 | SV-6 | SV-7 | SV-8 | SV-9 | SV-10 | SV-11 | SV-12 | SV-13 | SV-14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v1 | 45 | 55 | 45 | 55 | 50 | 20 | 8 | 30 | 40 | 30 | 35 | 25 | 50 | 55 |

Elicitation check, random half:

| id | v1 P(pass) | paraphrase P(pass) | negation P(not pass) | implied by negation (100 − x) | spread (max − min of the three) | \|P(pass) + P(not pass) − 100\| |
|---|---|---|---|---|---|---|
| SV-2 | 55 | 38 | 40 | 60 | 22 | 5 |
| SV-3 | 45 | 33 | 50 | 50 | 17 | 5 |
| SV-7 | 8 | 7 | 88 | 12 | 5 | 4 |
| SV-10 | 30 | 20 | 62 | 38 | 18 | 8 |
| SV-11 | 35 | 28 | 62 | 38 | 10 | 3 |
| SV-13 | 50 | 33 | 50 | 50 | 17 | 0 |
| SV-14 | 55 | 58 | 35 | 65 | 10 | 10 |

- **Mean negation incoherence:** 5.0 points. **Mean |v1 − paraphrase|:** 9.6 points.
- **The paraphrase ran lower** on 6 of 7 (by 1 to 17 points); it spelled out the testability floor in each sentence, which may have made the floor salient. Seven items cannot establish a bias.
- **Largest spread: SV-2** (55, 38, implied 60). The headline stays the v1 number; the spread is published beside it.

**For scoring.** The headline numbers stay the v1 numbers. Before a bet is pre-registered, its lesson line (`operators/learn.md`) may revise the odds toward the running base rate, with both numbers kept.
