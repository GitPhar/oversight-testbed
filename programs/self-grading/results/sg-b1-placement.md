# sg-b1: does a model grade its own conclusion more kindly in the conversation that wrote it? (result)

Pre-registered in `experiments/sg-b1-placement.md` (`d2589e3`, 2026-11-05 04:59 America/Denver). The seed is CURBy-RNG pulse 1592184 (`b53dc6f`).
- **Design review** (`ledger/design-reviews/sg-b1.md`): fix-first with 5 flaws (`17b6495`). The fixes are D5a–D5f (`5a173cb`), confirmed at 05:14 (`360f874`); D5g corrected a table (`4a722d3`). All of this came before the first test call.
- **Run:** 2026-11-05, from just after 05:15:29 (the D5g commit) to 05:19:58 America/Denver (the write cache was last saved 05:17:21, the grade cache 05:19:58). **720 calls (180 writes, 540 grades), complete, no refusal, $1.373** of the $1.80 cap. With the review's pilot ($0.069), the bet spent $1.44.
- **Odds:** engine 24; no human odds.
- **Audit:** `ledger/audits/sg-b1.md` (`f0a577f`). The verdict stands, with 3 required cuts, applied in this file under D10. Plant pl-014 was a clean draw.

## In plain English

**Pre-registered verdict: fail-same.** In the pre-registered words, with the D5f wording:

> On Haiku, Sonnet and Opus 5.5, on 60 made-up study conclusions, at least two of the three models graded their own conclusion the same on average (mean difference within 3 points of 100, 95% interval inside −3 to +3) in the conversation that wrote it and fresh, and none was detectably kinder or harsher.

All three models read "same", not just two.

**What the numbers say.**
- Each model wrote a short conclusion for each of 60 made-up studies, then graded it twice: once right away in the same conversation, and once in a new conversation showing exactly the same words. Neither version said who wrote it.
- Grading in the same conversation did not make any model kinder. If anything, the grades there were slightly lower:

  | model | own conversation minus new conversation (points of 100) | 95% interval |
  |---|---|---|
  | Haiku | −1.1 | [−1.7, −0.6] |
  | Sonnet | −0.4 | [−1.0, +0.2] |
  | Opus | −0.9 | [−1.6, −0.1] |

- **"Detectably kinder or harsher" means by the pre-registered 3-point bar.** Below that bar, Haiku graded its own conclusion slightly lower in the conversation that wrote it: −1.1, an interval that excludes 0, and −1.0 [−1.6, −0.4] against the second fresh grade too. Opus's −0.9 is about the size of the gap between its own two identical fresh grades (−0.57). Against the second fresh grade it is −0.3 [−1.0, +0.5], so it cannot be told apart from re-grade noise. This is a secondary observation, not the verdict.
- Many studies got the identical grade in both conversations: a majority for Haiku, fewer than half for Sonnet and Opus (79 of 180 in all):
  - **Haiku:** 35 of 60 got the identical grade.
  - **Sonnet:** 17 of 60.
  - **Opus:** 27 of 60.

  The rest moved by a few points either way.

**Robustness (pre-registered).**
- **Leave one study out:** no model's reading changes when any single study is dropped ("fragile": no, for all three).
- **Ties excluded** (studies with the same grade in both conversations dropped): Sonnet and Opus still read "same"; Haiku becomes "undetermined" (−2.7). The verdict is unchanged: two models read "same".
- **The noise-floor gate:** a second, identical fresh grade differed from the first by less than 1 point on average for every model (Haiku −0.13, Sonnet −0.33, Opus −0.57). The Opus difference was −0.57 [−1.18, −0.02], an interval that excludes 0. The gate did not fire only because of the 1-point size floor added before data (D5e). Without that floor, Opus would read untestable, and the verdict would still be fail-same (Haiku and Sonnet "same").

**The pre-mortem** named a ceiling. Grades ran 72–96, with no 100. Sonnet gave 95 or 96 to 35% of its grades; Haiku and Opus did so for 1% and 6%. The auditor scores the pre-mortem; this file only records the numbers.

**Scope** (§6). This covers:
- three Claude models;
- one kind of work: three-sentence conclusions about made-up quantitative studies;
- one wording, and one sample per study.

"Same conversation versus fresh" is a bundle: the turn the conclusion sits in, the message count and the lead-in wording all differ together. This test says nothing about labels ("you wrote this"; that is sg-b2), about catching flaws (sg-b3), or about text the model did not write. It does not say "models do not favour their own work".

## Tables

### Per model (60 studies each, all usable)

| model | D = own − fresh | 95% CI | reading | mean own | mean fresh | mean fresh2 | SD of differences | own higher | tied | D0 = fresh2 − fresh | D0 95% CI | leave-one-out range |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Haiku | −1.12 | [−1.70, −0.57] | same | 88.58 | 89.70 | 89.57 | 2.24 | 8% | 58% | −0.13 | [−0.50, +0.25] | [−1.17, −1.00] |
| Sonnet | −0.42 | [−1.02, +0.20] | same | 92.58 | 93.00 | 92.67 | 2.46 | 25% | 28% | −0.33 | [−0.72, +0.10] | [−0.56, −0.32] |
| Opus | −0.87 | [−1.57, −0.12] | same | 88.60 | 89.47 | 88.90 | 2.89 | 17% | 45% | −0.57 | [−1.18, −0.02] | [−1.02, −0.76] |

**Verdict** (§5.2): three "same", none kinder or harsher → **fail-same**. Score 0 against engine odds 0.24.

### Secondaries (reported, never promoted)

| | Haiku | Sonnet | Opus |
|---|---|---|---|
| ties excluded: n dropped / mean / reading | 35 / −2.68 / undetermined | 17 / −0.58 / same | 27 / −1.58 / same |
| D, randomised studies (n 23) | −1.17 | −0.65 | −0.61 |
| D, before-after (n 22) | −1.55 | −0.55 | −0.59 |
| D, self-selected (n 15) | −0.40 | +0.13 | −1.67 |

**Pooled D** (per study, the mean over the three models, then a study bootstrap): **−0.80 [−1.20, −0.41]**.

### Spend

| model | write | grade |
|---|---|---|
| Haiku | $0.006 | $0.013 |
| Sonnet | $0.149 | $0.279 |
| Opus | $0.336 | $0.590 |
| **total** | **$0.491** | **$0.882** |

All $1.373, plus the review's pilot $0.069. The program has spent $1.44 of $5.00.

Raw data: `results/sg-b1-write-calls.json` and `results/sg-b1-grade-calls.json` (committed `12ae694`, before this analysis). The analysis is in `results/sg-b1-analysis.json`, regenerated by `python experiments/sg_b1_placement.py analyse` with no calls.
