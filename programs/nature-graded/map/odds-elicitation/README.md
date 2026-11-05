# How the engine's odds for program 3 were elicited

Written 2026-11-04 14:15 America/Denver, before any program-3 data existed.

## Procedure (odds template v1, `oversight-testbed/operators/scout.md`)

1. **The rows.** The scout wrote one row per direction (`rows-v1.md`). Each row gives the assumption at stake, prior work, our data, the cheapest test, its cost and a draft pass rule. The scout wrote all 14 rows before any odds existed.
2. **The headline odds** (`v1.md`).
   - **Who:** a fresh context that read only `rows-v1.md`. It had no reads files, no ranking, no weights and no human odds.
   - **How:** for each direction, in id order, one pass: a rationale of at most 100 words, then one integer from 1 to 99. That integer is P(pass), the probability that the draft pass rule as written will be met.
   - **Scale:** 0 = certainly will not pass, 100 = certainly will.
   - **When:** 2026-11-04 14:06 MST.
3. **The elicitation check.** A random half of the directions was drawn with Python `random.Random(20261104).sample(ids, 7)`: P3-1, P3-4, P3-6, P3-8, P3-11, P3-12 and P3-13. Two more fresh contexts re-elicited those seven:
   - **Paraphrase check** (`check-paraphrase.md`): the same rows, each pass rule reworded with the same meaning (`rows-paraphrase.md`).
   - **Negation check** (`check-negation.md`): the original rows, but asking for P(not pass) (`rows-negation.md`).
4. **The ranking** was set afterwards, by the scout, in `../program-3-map.md`. **The odds were not revised after ranking.**

All three elicitors were `claude-opus-5-5`, the same model as the scout.

**One departure from the template.** Template v1 gives each direction its own fresh context holding only that row. Here a single fresh context saw all 14 rows in one file and was told to judge each row on its own. That makes 3 elicitation contexts instead of 28. Cross-row anchoring is therefore possible. Logged as template variant `v1-batch`.

## The numbers

Headline P(pass) (v1):

| id | P3-1 | P3-2 | P3-3 | P3-4 | P3-5 | P3-6 | P3-7 | P3-8 | P3-9 | P3-10 | P3-11 | P3-12 | P3-13 | P3-14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v1 | 7 | 25 | 12 | 25 | 42 | 50 | 48 | 35 | 40 | 72 | 72 | 68 | 35 | 12 |

Elicitation check, random half:

| id | v1 P(pass) | paraphrase P(pass) | negation P(not pass) | implied by negation (100 − x) | spread (max − min of the three) | \|P(pass) + P(not pass) − 100\| |
|---|---|---|---|---|---|---|
| P3-1 | 7 | 12 | 85 | 15 | 8 | 8 |
| P3-4 | 25 | 30 | 65 | 35 | 10 | 10 |
| P3-6 | 50 | 50 | 35 | 65 | 15 | 15 |
| P3-8 | 35 | 30 | 70 | 30 | 5 | 5 |
| P3-11 | 72 | 72 | 25 | 75 | 3 | 3 |
| P3-12 | 68 | 50 | 40 | 60 | 18 | 8 |
| P3-13 | 35 | 50 | 35 | 65 | 30 | 30 |

- **Mean negation incoherence:** 11.3 points. **Mean |v1 − paraphrase|:** 6.9 points.
- **Worst case is P3-13.** It is the same event rated 35, 50 and an implied 65.
- **Which way the negation pulls:**
  - In 5 of 7 directions, the negated question implied a *higher* pass probability than the direct one: P3-1 +8, P3-4 +10, P3-6 +15, P3-11 +3, P3-13 +30.
  - In 2 it implied a lower one: P3-8 −5, P3-12 −8.
  - Asked whether a test would fail, the elicitor usually gave a failure probability below 100 minus its pass probability. The direct question was the more pessimistic of the two. Seven items cannot establish a bias.
- **Expected passes:** on the 13 nature-graded bets the v1 numbers sum to 5.08. P3-8 is excluded because mathematics, not the chip, decides it.

**What this means for scoring.** The headline numbers stay the v1 numbers. The spread is published beside them, because the engine's own odds move with wording by up to 30 points on these items. That matters for the comparison this program exists to make. When the engine's calibration is compared between the AI-graded and nature-graded ledgers, any difference smaller than this elicitation noise should be read as no difference.
