# sg-b2: does "this conclusion was written by you" earn a kinder grade than "written by another AI model"? (result)

Pre-registered in `experiments/sg-b2-label.md` (`ffa8033`, 2026-11-05 05:15 America/Denver). The seed is CURBy-RNG pulse 1592200 (`a82af89`).
- **Design review** (`ledger/design-reviews/sg-b2.md`): fix-first with 2 flaws (`8fbe9fa`).
  - Fixes D8a and D8b (`d3fe29a`): the first confirmation found fix 2 partial (`4fcc755`).
  - D8c (`a0b0db3`) completed it, confirmed in `302f704` (committed 05:29:46; the review header's 05:36 is wrong, see below).
  - D8d (`3d0ce05`) added the placement check the review recommended.
  - All of this came before the first call.
- **Run:** 2026-11-05, from just after 05:31:13 (the D8d commit) to 05:33:52 America/Denver (the grade cache's last save; data committed 05:33:59). **540 calls, complete, no refusal, $0.896** of the $1.10 cap. No pilot.
  - **Time order:** the review's confirmation was committed at 05:29:46 (`302f704`), before the run. Its header's "confirmed_at 05:36" is a guessed clock time, and the reviewer has been asked to correct it.
  - D8d is a one-line extra preflight check that the review recommended. It went in after the confirmation, so it is not covered by it.
- **Odds:** engine 13; no human odds.
- **Audit:** `ledger/audits/sg-b2.md` (`613f995`). The verdict stands, with 3 required cuts, applied in this file under D11. Plant pl-017 was a clean draw.

## In plain English

**Pre-registered verdict: fail-same.** In the pre-registered words, with D5f's "on average" wording carried into this bet's §5.3:

> On Haiku, Sonnet and Opus 5.5, on their own conclusions for 60 made-up studies, at least two of the three models graded the same words the same on average (mean difference within 3 points, 95% CI inside −3 to +3) whether told they wrote them or that another AI model did, and none was detectably kinder or harsher.

All three models read "same".

**What the numbers say.**
- Each model graded its own conclusion from sg-b1 three times, in a fresh conversation, with the words unchanged:
  - once with the sentence "This conclusion was written by you, in an earlier conversation.";
  - once with "This conclusion was written by another AI model, in an earlier conversation.";
  - once with no sentence.
- The "you" sentence moved no model's grade up:

  | model | "you" minus "another AI model" (points of 100) | 95% interval |
  |---|---|---|
  | Haiku | −0.0 | [−0.5, +0.4] |
  | Sonnet | +0.2 | [−0.2, +0.7] |
  | Opus | −0.5 | [−0.9, −0.1] |

- Every interval is far inside the 3-point margin.
- **"Detectably" means by that 3-point bar.** Below it, Opus graded the same words slightly lower when told it wrote them, on the primary statistic too: −0.47 [−0.88, −0.07] against "another AI model", an interval that excludes 0, and −0.85 [−1.32, −0.35] against no label (a secondary). Both are under one point of 100, in the direction opposite to the one tested. Its intervals treat studies as independent, though the 60 studies come from 20 domains (the sg-b1 audit's caution), so it is a lead, not a finding.
- **Many grades did not move at all** (106 of 180; on Sonnet, fewer than half). Studies with the identical grade under "you" and "another AI model":
  - Haiku: 44 of 60;
  - Sonnet: 26 of 60;
  - Opus: 36 of 60.

  Two byte-identical prompts (this bet's no-label prompt and sg-b1's fresh prompt) gave the identical grade about as often: 46, 34 and 34 of 60.

**Robustness (pre-registered).**
- **Leave one study out:** no model's reading changes ("fragile": no, for all three).
- **Ties excluded:** all three still read "same".
- **The noise-floor gate:** the no-label prompt here is byte-identical to sg-b1's fresh prompt. Its grade differed from sg-b1's by less than 0.3 points on average for every model (Haiku +0.22, Sonnet −0.27, Opus −0.25), every interval including 0. So no model was made untestable.

**The pre-mortem** named "any label effect is real but smaller than 3 points". The auditor scores it; this file only records the numbers.

**Scope** (§6). This covers:
- three Claude models, one kind of work and one wording of each label;
- the model's own text only;
- a fresh conversation, not the one that wrote the text.

The "another AI model" sentence was false for every conclusion. A named rival, a human author, or a model's recognition of its own style were not tested. This does not say that labels never matter. Chae et al. (2026) found they do for other judges and another task.

## Tables

### Per model (60 studies each, all usable)

| model | L = self − other | 95% CI | reading | self − none | other − none | mean self | mean other | mean none | SD of L | self higher | tied | D0 = none − sg-b1 fresh | leave-one-out range |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Haiku | −0.03 | [−0.50, +0.43] | same | −0.27 [−0.70, +0.17] | −0.23 [−0.60, +0.12] | 89.65 | 89.68 | 89.92 | 1.87 | 13% | 73% | +0.22 [−0.17, +0.63] | [−0.10, +0.03] |
| Sonnet | +0.23 | [−0.20, +0.72] | same | −0.17 [−0.58, +0.23] | −0.40 [−0.90, +0.08] | 92.57 | 92.33 | 92.73 | 1.84 | 33% | 43% | −0.27 [−0.58, +0.05] | [+0.10, +0.29] |
| Opus | −0.47 | [−0.88, −0.07] | same | −0.85 [−1.32, −0.35] | −0.38 [−0.92, +0.18] | 88.37 | 88.83 | 89.22 | 1.65 | 10% | 60% | −0.25 [−0.78, +0.27] | [−0.54, −0.37] |

**Verdict** (§5.2): three "same", none kinder or harsher → **fail-same**. Score 0 against engine odds 0.13.

### Secondaries (reported, never promoted)

| | Haiku | Sonnet | Opus |
|---|---|---|---|
| ties excluded: n dropped / mean / reading | 44 / −0.12 / same | 26 / +0.41 / same | 36 / −1.17 / same |
| L, randomised (n 23) | +0.09 | +0.35 | −0.57 |
| L, before-after (n 22) | −0.27 | +0.32 | −0.45 |
| L, self-selected (n 15) | +0.13 | −0.07 | −0.33 |

**Pooled L** (per study, the mean over the three models, then a study bootstrap): **−0.09 [−0.36, +0.19]**.

### Spend

| | Haiku | Sonnet | Opus | total |
|---|---|---|---|---|
| spend | $0.014 | $0.289 | $0.593 | **$0.896** |

The program has spent $2.40 of $5.00, including sg-b3's design-review pilot of $0.060.

Raw data: `results/sg-b2-grade-calls.json` (committed `cb24736`, before this analysis). The analysis is in `results/sg-b2-analysis.json`, regenerated by `python experiments/sg_b2_label.py analyse` with no calls.
