# How the engine's odds for program 5 were elicited

Written 2026-11-05 04:55 America/Denver, before any program-5 data and before the ranking.

## Procedure (odds template v1, `operators/scout.md`; variant `v1-batch`, as program 3)

1. **The rows** (`rows-v1.md`, committed `bc3604c` at 04:52) were written by the scout before any odds: one row per direction, with the assumption at stake, the cheapest test, its cost and a draft pass rule.
2. **Headline odds** (`v1.md`): one fresh subagent (claude-opus-5-5) that was told to read only `rows-v1.md` (no reads, maps, ledger or results, no web, no code). For each row, in id order, a rationale of at most 100 words, then one integer P(pass) from 1 to 99. Scale: 0 = certainly will not pass, 100 = certainly will pass. Written 04:53.
3. **Elicitation check** on a random half, drawn with Python `random.Random(20261105).sample(ids, 5)`: sg-d2, sg-d3, sg-d4, sg-d5 and sg-d10. Two more fresh subagents, also claude-opus-5-5:
   - **paraphrase** (`check-paraphrase.md`): the same rows, with each pass rule reworded to the same meaning (`rows-paraphrase.md`);
   - **negation** (`check-negation.md`): the original rows, asking for P(not pass) (`rows-negation.md`).
4. **The ranking** is set afterwards, in `../program-5-map.md`. The odds are not revised after ranking.

**Departure from the template, as in program 3:** one context saw all the rows in one file, rather than one context per row (`v1-batch`), so cross-row anchoring is possible. The three elicitors are the same model as the scout. None of them could read a clock, so their times come from the files' write times (04:53:36 to 04:53:41).

## The numbers

Headline P(pass) (v1):

| id | sg-d1 | sg-d2 | sg-d3 | sg-d4 | sg-d5 | sg-d6 | sg-d7 | sg-d8 | sg-d9 | sg-d10 |
|---|---|---|---|---|---|---|---|---|---|---|
| v1 | 24 | 13 | 18 | 8 | 20 | 15 | 8 | 8 | 7 | 17 |

Elicitation check, random half:

| id | v1 P(pass) | paraphrase P(pass) | negation P(not pass) | implied by negation (100 − x) | spread (max − min of the three) | \|P(pass) + P(not pass) − 100\| |
|---|---|---|---|---|---|---|
| sg-d2 | 13 | 12 | 80 | 20 | 8 | 7 |
| sg-d3 | 18 | 20 | 75 | 25 | 7 | 7 |
| sg-d4 | 8 | 12 | 85 | 15 | 7 | 7 |
| sg-d5 | 20 | 25 | 70 | 30 | 10 | 10 |
| sg-d10 | 17 | 22 | 80 | 20 | 5 | 3 |

- **Mean negation incoherence: 6.8 points. Mean |v1 − paraphrase|: 3.4 points.** Program 3's were 11.3 and 6.9.
- **The direction of the negation pull is the same in all five:** asked whether the rule would fail, the elicitor implied a higher pass probability than when asked directly (by +3 to +10 points). On five items this is a hint, not a finding. It matches program 3's 5 of 7.
- **Expected passes on the ten:** 1.38. sg-d9 opens only if sg-d1 passes.

The headline numbers stay the v1 numbers. The spread is published beside them: the engine's odds move with wording by up to 10 points here.
