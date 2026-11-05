---
bet: em-gm2
program: entangled-mind
round: 3
prereg_commit: 9e23b6f (author time 2026-11-04 03:58:35; analysis code and planted values committed with it; first call 04:15:33 by decoded request IDs, round 1)
results_commit: 4c5c34f (author time 2026-11-04 04:41:00)
auditor_session: round-3 auditor fork (stripped clone at the scratchpad path clone-p1a, checked out at 4c5c34f; scripts p1a/rederive_gm2.py, p1a/followup_gm2.py)
auditor_model: claude-fable-5-1
author_model: claude-opus-5-5
same_model_family: true          # same vendor (Anthropic), a different and stronger model than rounds 1 and 2
date: 2026-11-05 05:40 America/Denver
claims_checked: 15
holes_found: 3
overclaims_cut: 5
reproduced: true                 # OE per condition, R, its CI, b_MF, the pulls and the MF agreement re-derived from gm2-conversations.json with independent code
verdict_claimed: pass            # "question-driven"
verdict_after_audit: pass
verdict_stands: true
verdict_round1: stands with caveats (10 cuts; "consistency is memory" cut)
verdict_round2: not re-audited in round 2 (mm-gm2 and gm2b were; the 40-item replication em-gm2b gives R = 1.23 [0.75, 2.02])
canary: unknown
false_alarms: 0
design_review_missed: []         # no design review existed; one should have noted that the 0.5 bar on a ratio of clipped variance components sits only 1.5× above the estimator's null floor (0.34), and that the placeholder cannot be separated from the question
failed: false
failure_reason: "None: the bet passed. Had it failed, the most likely reason: the shown order effect would have been too small to divide by (one item, h112, carries 57% of it), leaving R undefined or its interval straddling 0.5. Kind design."
failure_kind: null
premortem_score: null            # no pre-mortem (pre-dates operators/premortem.md)
risk_seen: null
---

# Audit of em-gm2 (round 3): measurement as self-conditioning (shown, redacted, planted transcripts)

## In plain English

The verdict stands as **pass** ("question-driven"), and the ledger's outcome 1 at odds 0.25 is right. With my own code the ratio of the redacted to the shown order effect is R = 1.91 with a 95% item-bootstrap interval of [0.93, 4.70] (10,000 resamples; four seeds give lower bounds 0.928 to 0.934; a bias-corrected interval gives [0.93, 4.67]). The pre-registered bar is a lower bound at or above 0.5. The label is not fragile: no single dropped item takes the lower bound below 0.86, and dropping both h191 and h261, which carry 74% of the redacted between-order variance, leaves R = 1.01 [0.79, 1.81]. Under a permutation null with no redacted order effect, the point estimate R clears 0.5 in 19% of shuffles but never reaches the observed lower bound (its maximum is 1.04). What does not hold: the claim that redaction gives a *larger* order effect than showing. The difference between the two, 8.0 points, has an interval of [−0.8, +17.7]. Thirty of the 400 redacted chain finals are end-of-scale jumps more than 50 points from the item's shown mean; excluding them R is still 1.79, so the pass does not rest on them, but the design cannot separate the question from the placeholder that replaces the answer, and the "questions themselves change the judgment" sentence now says so. The memory reading holds by its rule (agreement drop 0.58 [0.31, 0.83]), with the added fact that the hidden-answer re-rating also sits 8 points lower on average, so part of the drop is a shift rather than scatter.

## The case that this result is false

The claim is that the order of the sub-questions changes the final rating even when the model cannot see its earlier answers, so the question itself, not the recorded answer, does the work. The strongest case against it: the redacted condition is not "the question without the answer". It is the question followed by a strange turn, "[rating recorded]", in the model's own voice, repeated four times. A model that has never seen such a turn may behave erratically, and erratic behaviour that happens to depend on which question comes first will register as a between-order variance. The data show exactly that shape: in h191 the shown final rating is 3 in every order, and under redaction it is 81 in one order and 3 in the other three; in h112 one redacted order collapses to 6 against 37 shown. Two items supply three quarters of the redacted variance, and a ratio with ten items in the denominator, one of which (h112) supplies more than half the shown variance, is a statistic that a single item can swing. The bar itself is generous: the variance-component estimator is clipped at zero, so pure noise produces a positive "order effect" of about a third of the shown one, and 0.5 is not far above that floor. The bootstrap is a percentile interval on a ratio from ten items, and the basic (reverse-percentile) interval runs from −0.87 to 2.90, which would not pass. And the 81% → 23% "memory" figure is partly a level shift: with the answer hidden the model re-rates lower, not just differently.

What survives: the pass is robust to every single-item drop, to both heavy items dropped together, to the end-of-scale jumps excluded, to four bootstrap seeds and to bias correction; the permutation null never reaches the observed lower bound; the 40-item replication (em-gm2b) gives the same label. The placeholder confound is real, disclosed in the pre-registration's §6, and now stated with its numbers. The basic interval is the wrong tool for a right-skewed ratio and the pre-registration specified an item bootstrap, which the authors implemented as the percentile form; I note it and do not reverse on it.

## Claims checked

| # | claim (results file as it stands, or paper) | check run | outcome |
|---|---|---|---|
| 1 | OE shown 8.7, redacted 16.7, high 6.2, low 3.2 | my variance components | holds (8.73, 16.71, 6.16, 3.23) |
| 2 | R = 1.91 [0.92, 4.90] | my bootstrap, 10,000 resamples, seeds 1, 2, 3, 2003: [0.93, 4.70], [0.93, 4.65], [0.93, 4.72], [0.93, 4.67]; BCa [0.93, 4.67] | holds; the 4.90 upper end is the 2,000-resample draw |
| 3 | pre-registered reading "question-driven" (lower bound ≥ 0.5) | row 2 | holds |
| 4 | ledger outcome 1 at 0.25; event "R CI above 0.5" | row 2 | holds |
| 5 | "by even more than when the answers are shown" | OE_redacted − OE_shown 8.0 [−0.8, +17.7] | **hole 1**: not established (cut 1) |
| 6 | "much of the redacted order effect comes from 2 of them (h191, h261)" | 74% of the redacted summed VC; h112 is 57% of the shown | holds; numbers added (cut 3) |
| 7 | leave-one-item-out: implicit "not fragile" | lowest lower bound 0.86 (drop h191, R 1.32); drop h191 + h261: 1.01 [0.79, 1.81] | holds; now stated (cut 3) |
| 8 | gate p 0.0002 | my permutation 0.0002; without h112, 0.0004 | holds |
| 9 | "The questions themselves change the judgment" | 30 of 400 redacted O-chain finals are >50 points from the item's shown mean (h112 12, h191 9, h261 7); R without them 1.79; prereg §6 | **hole 2**: question and placeholder not separable (cuts 2, 4) |
| 10 | b_MF 1.27 [0.70, 2.14]; median item 1.00; h238 inflates | per item 0.09–4.56, mean 1.27, median 1.00 | holds |
| 11 | later sub-question ratings move about 3 points; final verdict about 10 | S-only pull 2.94 [1.55, 4.33]; final-M shift 10.45 | holds |
| 12 | MF agreement 81% / 23% / 30% / 40%; drop > 10 points = memory | 0.81, 0.23, 0.30, 0.40; drop 0.58 [0.31, 0.83] by item bootstrap; redacted M₂ − M₁ averages −8.3 | holds by the rule; shift added (cut 5) |
| 13 | gate / within-order SD: placeholder "may unsettle the model" | within-order SD shown 10.4, redacted 11.5 | holds as a caveat |
| 14 | 2,000 conversations, $0.55, no refusal | 2,000 keys, $0.547 | holds |
| 15 | paper lines 19, 215–224, 306–307, 321, 409 citing this bet | 1.91 is reported as the 10-item value with h191 named; 40-item values used | hold |

## Checklist

**A.** 1. *Holds* (round 1 decoded the call times: first call 04:15:33, 17 min after the freeze; code frozen with the text). 2. *Holds:* statistic, seeds, R = 10, orders, planted values and the four-way rule are as frozen. 3. *Holds.* 4. *Holds:* R is the primary; planted effects and agreement are "reported".

**B.** 5. *Ties and floating point: holds.* The variance component is clipped at 0; no shown item has VC = 0 (smallest h191 at 0.16), so R is defined in every resample (0 NaN resamples of 10,000). 6. *Pooling: holds as designed.* OE pools ten items under a square root of a mean, which weights high-variance items heavily; the per-item view (9 of 10 items have a redacted OE at least half the shown) agrees with the pooled label. 7. *Few items: hole, now stated.* Two items carry 74% of the redacted variance and one carries 57% of the shown; the label survives every single drop (lowest bound 0.86) and the double drop (1.01 [0.79, 1.81]), but the size of R is item-driven, as the 40-item replication (1.23) confirms. 8. *Circular: holds.* Nothing is fitted; planted values come from archived runs. 9. *Baselines: holds, with a design note.* A permutation null that destroys any redacted order effect but keeps the redacted within-order noise gives R with mean 0.34, 95th percentile 0.64 and maximum 1.04 over 3,000 shuffles: the bar of 0.5 sits only 1.5× above the clipped estimator's noise floor, and a point estimate clears it 19% of the time under the null. The observed *lower bound* (0.93) is above the null's maximum point estimate, so the pass is not a floor artefact; a future design should set the bar against this null rather than at a round number. 10. *Uncertainty: holds, with a note.* Item-level percentile bootstrap on 10 items, as frozen; BCa agrees; the basic interval ([−0.87, 2.90]) does not, which is the usual behaviour of a right-skewed ratio with a small denominator and not evidence against the label. 11. *Holds:* one primary. 12. *Holds:* no outcome reaches any fitting step; the model never sees the condition label.

**C.** 13. *Holds:* one model, 10 items, stated. 14. *Holds:* planted and agreement results are secondary. 15. *Hole 2:* "The questions themselves change the judgment" names a cause the design cannot separate from the placeholder turn (the pre-registration's own §6); the pass rule's wording "a measurement effect in the strict sense" inherits the same limit. 16. *Hole 1 (cut 1):* "by even more than when the answers are shown" is a point-estimate ranking whose difference interval includes 0. Also cut 5: the agreement drop is partly a level shift. 17. *Holds:* Kumaran et al. is cited for the hidden-first-answer design, which it supports. 18. *Holds.*

**D.** 19. *Holds:* $0.547 of $1. 20. *Holds.* 21. *Holds:* anchor (a) only. 22. *Holds:* the 40-item and Sonnet replications are reported separately; the first-10 pass is scored as the bet.

**E.** 23–26. *n/a:* pre-dates the beacon, lesson and design-review rules; no pre-mortem.

## The pre-mortem, scored

No pre-mortem exists. My own line, written before re-reading the pre-registration's §6: had it failed, the most likely reason would have been a shown order effect too small to divide by, with one item carrying most of it; kind design. The pre-registration's §6 names the wide interval and the placeholder, not the denominator.

## Required cuts

All in `programs/entangled-mind/results/gm2-self-conditioning.md`; all **applied**.

1. "by even more than when the answers are shown: an order effect of 16.7 points against 8.7." → "by at least as much as when the answers are shown: an order effect of 16.7 points against 8.7 (the difference, 8.0 points [−0.8, +17.7], is not established; audit round 3)."
2. "The questions themselves change the judgment." → "The questions themselves, or the questions together with the placeholder that stands in for the answer, change the judgment."
3. Caveat 1: add the shares (74% and 57%) and the leave-one-out numbers (lowest lower bound 0.86; without h191 and h261, R 1.01 [0.79, 1.81]).
4. Caveat 3: add "30 of the 400 redacted O-chain final ratings sit more than 50 points from the item's shown mean (h112 12, h191 9, h261 7); with those conversations excluded R is 1.79, so the pass does not rest on them alone, but the design cannot separate the question from the placeholder."
5. "Repeat agreement" bullet: add the drop's interval (0.58 [0.31, 0.83]) and that the hidden-answer re-rating averages 8 points lower.

No paper sentence citing this bet was found unsupported: `paper/no-credence-to-read.md` reports 1.91 as the first-10 value, names h191, and uses the 40-item numbers.

## What would break it next

A neutral-placeholder arm, as the round-2 audit of the Sonnet replication also recommended: the same 10 items with the answer replaced by "[answer withheld]" and, separately, by an empty assistant turn, R = 10 per cell, about $0.30 on Haiku. If the order effect under a different placeholder is near the null floor (R about 0.34) while "[rating recorded]" keeps it near 1.9, the effect is the placeholder's, not the question's. If both placeholders give R above 0.5 with lower bounds above the permutation null, the question-driven reading is strengthened beyond what this run can show.

Scripts: `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/4f777718-cc86-43e1-837e-ef53cbe2abaf/scratchpad/p1a/rederive_gm2.py` and `.../p1a/followup_gm2.py` (run with `python3 -I` in that folder, on files extracted from the clone at 4c5c34f).
