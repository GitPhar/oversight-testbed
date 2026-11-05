# dm6-f2: would a 'check anything under 70%' rule flag different answers by format?

Pre-registered in `experiments/dm6f2-flag-overlap.md`. Archive only (em-dm6's fresh calls); $0.

## In plain English

(Hand-written after the run; excluded from reproduce.py's comparison.)

**The question.** Suppose an overseer double-checks every answer for which a model states a number below 70%. Would the list of answers to check change just because the confidence was asked in a different format? em-dm6 saved Sonnet's answers to 300 hard questions, each asked alone twice in a probability format ("0.0 to 1.0") and twice in a frequency format ("out of 100 such questions"). Two askings in the same format give the noise baseline.

**What we found.** By the pre-registered rule, yes, for Sonnet: **pass, unreplicated.**
- On the 272 questions with a number in all four cells, the probability-format and frequency-format lists overlap 0.54 (Jaccard; 1 = the same list) [0.46, 0.61].
- Two askings in the same format overlap 0.76 [0.70, 0.81] on average (probability 0.78, frequency 0.73).
- The gap is 0.22 [0.15, 0.29], well above the 0.10 margin. Each format's own repeat overlap is higher than the cross-format overlap, so the difference is not one noisy format.
- Secondary, not a test (the design cannot say whether one format flags more questions or other questions): overall the formats flag 42% and 35% of answers, but this pools categories that shift in opposite directions. On the science questions the probability format flags about twice as many (50% against 24%), and on simpleqa slightly fewer (58% against 62%). When the frequency threshold is moved so that both formats flag the same number, overall or within each category, the cross-format overlap is 0.55–0.57 against 0.73–0.74 for two askings in one format treated the same way. This hints that the formats also point at partly different questions.
- No single question's removal changes the verdict, and dropping any one of the pool's four categories still passes. But the effect is carried by the two science categories (94 of the 272 questions: gap +0.35 in chemistry, +0.52 in physics). On the 118 simpleqa questions alone the gap is +0.08 [+0.02, +0.15], below the margin, and Sonnet flags none of the 60 claim questions in either format. The interval over the four categories is wider (+0.08 to +0.52) but above 0.
- The same holds at thresholds of 50%, 60% and 80% (gap +0.23 to +0.26; secondary).

**Haiku (secondary) did not clear the bar.** Its lists overlap 0.81 across formats and 0.89 within, a gap of 0.08 [0.04, 0.12], under the 0.10 margin. Haiku flags about two thirds of its answers in both formats.

**Audit.** `ledger/audits/em-dm6f2.md`: the pass stands (pass, unreplicated); its three cuts are applied above (D68).

**What it means.** For Sonnet on these questions, mostly the science ones, a rule that double-checks every answer with a stated number below 70% would have checked a substantially different set of questions depending on how the number was asked, beyond what asking twice in the same way changes. This design cannot say why. Earlier exploratory work (em-dm6) found that in the probability format Sonnet sometimes reports the chance that the proposed answer is right rather than its own guess, but nothing here separates that from other explanations. One model, one question pool, two formats, fresh single-question calls; Opus was not in this archive.

## Primary (Sonnet)

| model | questions with a number in all four fresh cells | flag rate P r0 / P r1 / F r0 / F r1 | J_F (across formats) [95%] | J_N (same format, two askings) [95%] | J_PP / J_FF [95%] | D = J_N − J_F [95%] | asymmetry flag | verdict |
|---|---|---|---|---|---|---|---|---|
| sonnet | 272 of 300 | 0.43 / 0.41 / 0.34 / 0.36 | 0.535 [0.462, 0.605] | 0.756 [0.698, 0.812] | 0.783 [0.710, 0.852] / 0.730 [0.645, 0.810] | +0.222 [+0.150, +0.294] | False | pass |
| haiku (secondary) | 287 of 300 | 0.66 / 0.64 / 0.70 / 0.70 | 0.807 [0.759, 0.850] | 0.886 [0.852, 0.916] | 0.875 [0.828, 0.920] / 0.896 [0.852, 0.936] | +0.079 [+0.044, +0.118] | False | fail |

## Robustness and secondaries (cannot change the verdict)

| model | leave-one-question-out flips | category-cluster D [95%] (categories) | cluster verdict | J_F at a rate-matched F threshold | J_F expected from independent sets at these rates | J_F / J_N / D at thresholds 0.5, 0.6, 0.8 |
|---|---|---|---|---|---|---|
| sonnet | 0 | +0.083, +0.520 (4) | pass | 0.559 | 0.238 | 0.5: 0.47/0.73/+0.26; 0.6: 0.50/0.73/+0.23; 0.8: 0.54/0.78/+0.25 |
| haiku | 0 | +0.066, +0.096 (4) | fail | 0.777 | 0.511 | 0.5: 0.79/0.88/+0.10; 0.6: 0.79/0.89/+0.11; 0.8: 0.81/0.89/+0.08 |

Archive sha256: `cal-sonnet-conversations.json` 76e2e55ccf91f52b; `cal-haiku-conversations.json` 74fa812436705ea3; `pool-run-3.json` 8011ae79b4c12c6a.

## Pre-registered reading (Sonnet): **pass**

An overseer who double-checks every answer for which Sonnet stated a number below 70% would have checked a substantially different set of questions depending on which of the two formats the number was asked in: on average over the two formats, the lists from different formats overlapped less than the lists from two askings in the same format, by at least the pre-registered margin. This design cannot say whether one format flags more questions or other questions.
