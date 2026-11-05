# ss-b1 results: the published-record referee, first round

Pre-registration `ebd2c80` (D10); seed `1f5c1bf`; design review `ledger/design-reviews/ss-b1.md` (fix-first, then go after D12–D20). Run 2026-11-04, after commit `9d4bcf4` (D20) and before this results commit. **Audited** (`ledger/audits/ss-b1.md`, engine `cdce1ba`; clean audit pl-003): all three passes stand as pass-unreplicated; its seven required cuts are applied here (DEVIATIONS D21).

## In plain English

We asked the engine's own model to say which way 184 published findings went, without telling it the answers or letting it look anything up. It was also not told which paper each finding came from. The findings come from arXiv papers in model psychology, interpretability, scalable oversight and quantum-device physics. The papers' abstracts settled each one. The 116 that count were first posted on arXiv after the bettor's stated knowledge cutoff of June 2026 (31 July to 3 November 2026; 105 of them in September or later), so it should not have read them, though an earlier talk, workshop copy or blog post cannot be ruled out (§7).

**It did clearly better than a coin.** On those 116 new findings it put more than half its probability on the reported direction 76% of the time. Its Brier score was 0.163 (95% interval 0.139 to 0.190); always saying 50% scores 0.25. That passes the pre-registered rule.

**It was not just guessing that papers report that their own method works.** We tagged, before any bet, which option was each paper's own "it works" side. A predictor that only leaned 75% toward that side scored 0.232. Item-writers, who saw the answers, were told to prefer findings that went against the headline (item-spec), which makes this baseline weaker than it would be on a random sample of papers. The bettor beat it by 0.068 (interval 0.036 to 0.099). Where the paper's result went *against* its own headline (10 items), the bettor still got 6 of 10.

**It was better still on older papers it may have read** (68 items, Brier 0.105, 90% right). That fits memory. It also fits those items simply being easier, and this design cannot tell the two apart.

**Fields were uneven.** It did best on scalable oversight (90% right) and interpretability (84%), and worst on model psychology (62% right, Brier 0.235, interval 0.181 to 0.293, which includes 0.25). So on findings about how language models behave as minds, which is the field closest to itself, it was not shown to beat a coin. These field splits are descriptive. No test was pre-registered on them, and each has only 28–30 items.

**On the whole its confidence looked low rather than high (exploratory, not a pre-registered test).** On the new findings it was right 76% of the time at an average confidence of about 69%; the gap's 95% interval by item is −0.002 to 0.142, so it is not established, and its 60–70% calls were overconfident (right 57% of the time). When it said 70–80%, it was right 91% of the time (39 of 43).

**All three passed against the engine's odds of 50%, 30% and 35%.** Three correlated outcomes from one run cannot show the odds were miscalibrated. The lesson line had moved the main bet from 60% to 50% toward the ledger's base rate (pattern P1); on this outcome that move cost Brier 0.25 against 0.16.

**What this does and does not show.** It shows that, for this model on these items, the published record is a referee that can tell its judgment apart from a coin and from a publication-bias shortcut, cheaply: $2.02 of API in total, of which $1.55 was the bettor. It does not show that the model "understands" these fields. The record is a referee of what got published, not of what is true. Item-writer and bettor are the same model family, which could have shaped which findings were chosen. And this is one model, one prompt, one item set.

**The bettor ran with adaptive thinking at effort low (the least thinking claude-opus-5-5 allows), with its reasoning hidden; every result here is about the bettor at that setting, not about the same model with thinking off or at higher effort.** (D18, D20: the model cannot run with thinking off. Its calls used a median of 147 output tokens in all, of which the visible answer was about 110, so its hidden reasoning was short, roughly 35 tokens per call.)

### The three bets, in the pre-registered sentences (§5, D15)

| bet | engine odds | verdict | sentence |
|---|---|---|---|
| ss-b1 | 50 (first 60) | **pass, unreplicated** | On 116 findings published after its training cutoff, the bettor's probabilities beat always saying 50% (Brier 0.163 [0.139, 0.190]). |
| ss-b2 | 30 | **pass, unreplicated** | The bettor beat a predictor that only knows papers tend to report that their own method works. |
| ss-b3 | 35 | **pass, unreplicated** | The bettor scored better on papers it may have read than on papers it cannot have read, consistent with memory (or with the older items being easier; this design cannot separate the two). |

**Scope (D20):** the bettor ran with adaptive thinking at effort low (the least thinking claude-opus-5-5 allows), with its reasoning hidden; every verdict above is about the bettor at that setting, not about the same model with thinking off or at higher effort.

Leave-one-item-out (D16, 10,000 resamples per bound): no single item flips any of the three labels, so none is fragile. By field, ss-b1 and ss-b2 pass with any one field removed, but ss-b3 does not: without the model-psychology items its upper bound is +0.019, so the memory gap rests on that one field (pre 0.076 against post 0.235). This check was not pre-registered (audit).

Engine calibration on these three: Brier (0.50−1)² + (0.30−1)² + (0.35−1)², divided by 3, gives **0.388**. Always saying 50% would have scored 0.25. With the odds written before the lesson (0.60 for ss-b1), it would have been 0.358.

## The leakage caveat (pre-cutoff items)

**The 68 pre-cutoff items are not evidence of judgment.** Their papers were public before the bettor's training cutoff, so a good score there can be memory. Masking removes titles, authors and the names of methods, but not findings a model has read. These items are reported only to compare with the post-cutoff set (ss-b3). They never enter the headline. Four of them have a first arXiv version after the cutoff: ss-152 (moved by the writer, D8, ICML 2026 workshop) and ss-026, ss-027, ss-094 (moved by D12). They were moved to pre-cutoff before any bet because a workshop or TMLR version may have been public earlier.

## Tables

Generated by `scoring/score.py` from `items/items.jsonl` and `bettor/bets.jsonl` (`scoring/tables.md`, `scoring/scores.json`).

### By cutoff side

| side | n | Brier | 95% CI | share right | publication-bias baseline | bettor − baseline [95% CI] |
|---|---|---|---|---|---|---|
| **post-cutoff (primary)** | 116 | **0.163** | [0.139, 0.190] | 0.76 | 0.232 | −0.068 [−0.099, −0.036] |
| pre-cutoff (**may be memory**) | 68 | 0.105 | [0.076, 0.136] | 0.90 | 0.259 | −0.155 [−0.194, −0.115] |

Pre minus post: −0.059 [−0.098, −0.019].

### By field (post-cutoff; descriptive)

| field | n | Brier | 95% CI | share right | bettor − baseline [95% CI] |
|---|---|---|---|---|---|
| interpretability | 29 | 0.132 | [0.092, 0.180] | 0.84 | −0.109 [−0.182, −0.038] |
| model psychology | 29 | 0.235 | [0.181, 0.293] | 0.62 | −0.006 [−0.067, 0.052] |
| quantum devices | 28 | 0.176 | [0.120, 0.237] | 0.68 | −0.059 [−0.125, 0.012] |
| scalable oversight | 30 | 0.113 | [0.082, 0.148] | 0.90 | −0.098 [−0.139, −0.053] |

### By field (pre-cutoff; **may be memory**)

| field | n | Brier | 95% CI | share right |
|---|---|---|---|---|
| interpretability | 18 | 0.120 | [0.069, 0.184] | 0.89 |
| model psychology | 17 | 0.076 | [0.028, 0.151] | 0.94 |
| quantum devices | 16 | 0.122 | [0.072, 0.182] | 0.88 |
| scalable oversight | 17 | 0.100 | [0.049, 0.167] | 0.88 |

### By year (descriptive)

| year (first arXiv version) | side | n | Brier | 95% CI | share right |
|---|---|---|---|---|---|
| 2024 | pre (**may be memory**) | 21 | 0.073 | [0.031, 0.128] | 0.90 |
| 2025 | pre (**may be memory**) | 22 | 0.079 | [0.050, 0.117] | 0.95 |
| 2026, Jan–Jun | pre (**may be memory**) | 21 | 0.155 | [0.093, 0.230] | 0.86 |
| 2026, after Jun, moved to pre (D8, D12) | pre | 4 | 0.146 | [0.067, 0.266] | 0.75 |
| **2026, Jul–Nov** | **post** | **116** | **0.163** | [0.139, 0.190] | 0.76 |

The score falls off as papers get closer to the cutoff (2024–25 about 0.08, early 2026 0.15, post-cutoff 0.16). That is the shape memory would give. Recent papers being harder would give the same shape.

### By publication-bias tag (post-cutoff)

| reported side was… | n | Brier | share right | baseline Brier |
|---|---|---|---|---|
| no headline side (descriptive comparison) | 78 | 0.178 | 0.73 | 0.250 |
| the paper's own "it works" side | 28 | 0.110 | 0.91 | 0.062 |
| against the paper's own headline | 10 | 0.200 | 0.60 | 0.562 |

On the 28 items where the paper's method did work, the baseline (which always leans that way) beats the bettor. The bettor wins overall because of the 78 descriptive items and the 10 where the result went against the paper.

### Calibration (post-cutoff)

| confidence in the favoured side | n | mean confidence | share right |
|---|---|---|---|
| 0.5–0.6 | 14 | 0.56 | 0.61 |
| 0.6–0.7 | 42 | 0.63 | 0.57 |
| 0.7–0.8 | 43 | 0.73 | 0.91 |
| 0.8–0.9 | 14 | 0.82 | 1.00 |
| 0.9–1.0 | 3 | 0.92 | 1.00 |

Its 60–70% calls did no better than a coin (57%), while its 70%+ calls were right 93% of the time (56 of 60). Most of its skill sits in the items it was more confident about.

### Order check (secondary)

92 items (a beacon-drawn half) were asked a second time with the options reversed. The bettor chose the same side both times on 95% of them. Its two probabilities summed to 100 within 4.9 points on average. The pull toward whichever option is shown first was −0.4 points [−1.2, 0.4]: none detected.

### Checks against leakage and shortcuts

| check | pre-registered? | result |
|---|---|---|
| Post-cutoff items that needed a leakage rewrite vs those that did not | yes (§4) | rewritten 0.159 [0.097, 0.234], n = 17; clean 0.164 [0.138, 0.193], n = 99 |
| Leave-one-item-out on every label | yes (D16) | no flips |
| A rule that always picks the "higher / more / increased" option | no (exploratory) | right on 57 of 116 post-cutoff items (0.49) and 40 of 68 pre (0.59) |
| Was Option 1 the reported one more often than chance? | no (exploratory) | 55 of 116 (beacon-drawn order) |
| Out-of-range probabilities; rationales over 100 words | no | 0; 0 |

## Process and spend

| step | calls | cost | refusals |
|---|---|---|---|
| leakage check (claude-sonnet-5-5) | 213 | $0.47 | 0 |
| bettor pilot (one excluded item, D18) | 1 | $0.006 | 0 |
| bettor, primary (claude-opus-5-5) | 184 | $1.03 | 0 |
| bettor, order check | 92 | $0.52 | 0 |
| **total** | 490 | **$2.02** of the $5.00 cap | 0 |

Deviations D1–D20 are in `DEVIATIONS.md`. The ones that bear on reading these results:
- **D10:** the pre-registration landed inside another session's commit, unchanged.
- **D12:** three items were moved to pre-cutoff by an explicit venue rule.
- **D18 and D20:** thinking cannot be disabled on the bettor model.
- **D9:** some hand-written times were wrong; the git times are the record.

## What would break it next

1. Done: `ledger/audits/ss-b1.md`.
2. **A different item-writer.** Have a non-Claude model, or a person, write 60 post-cutoff items to the same spec, so the item-writer and the bettor are not the same family. This tests whether same-family selection made the items easier. About $1 of bettor calls.
3. **Run the bettor without its model's field.** The model-psychology items scored worst. A second round of 60 model-psychology items would show whether that is real or a 29-item fluke. About $0.40.
4. **Sean's 20 calls** (`human/form.md`), once committed to `ledger/human-odds.jsonl` from the cockpit (engine rule 11). They give a first human-vs-engine comparison on the same record.
