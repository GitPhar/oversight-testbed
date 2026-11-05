---
bet: em-gm1
program: entangled-mind
round: 3
prereg_commit: 28a20b2 (author time 2026-11-04 03:52:51; code first committed in amendment 954b4da at 03:58:25, 3.5 min after the first call, as round 1 found)
results_commit: bc0f125 (author time 2026-11-04 04:15:08)
auditor_session: round-3 auditor fork (stripped clone at the scratchpad path clone-p1a, checked out at bc0f125; scripts p1a/rederive_gm1.py)
auditor_model: claude-fable-5-1
author_model: claude-opus-5-5
same_model_family: true          # same vendor (Anthropic), a different and stronger model than rounds 1 and 2 (both claude-opus-5-5)
date: 2026-11-05 05:40 America/Denver
claims_checked: 14
holes_found: 3
overclaims_cut: 4
reproduced: true                 # every cell, I and both CIs re-derived from gm1-calls.json and the pool archives with independent code
verdict_claimed: null            # "no self-advantage"
verdict_after_audit: null
verdict_stands: true
verdict_round1: stands with caveats (20 cuts)
verdict_round2: not re-audited in round 2 (mm-gm1 replication was)
canary: unknown
false_alarms: 0
design_review_missed: []         # no design review existed (pre-dates operators/design-review.md); a review should have flagged the 26-item subset as unable to decide rule 1
failed: true
failure_reason: "The bet's event (a self-advantage with its CI above 0 on the 26-item disagreement subset) did not occur: the interaction is negative on all 298 and its subset interval [-0.48, +0.22] includes 0. Kind world."
failure_kind: world
premortem_score: null            # no pre-mortem (pre-dates operators/premortem.md)
risk_seen: null
---

# Audit of em-gm1 (round 3): privileged self-knowledge, the 2×2 self-versus-other confidence test

## In plain English

The verdict stands as **null** ("no self-advantage"), and the ledger's outcome 0 at odds 0.15 is right. I re-derived all four AUROC cells and the judge × author interaction from the archived calls with my own code: I = −0.055 on all 298 questions, 95% interval about [−0.109, −0.005] over three seeds (the file's [−0.103, −0.007] used 2,000 resamples); on the 26-item disagreement subset −0.135 [−0.48, +0.22]. The pre-registered rule needed I > 0 on all questions *and* a subset interval above 0 for a self-advantage; the first clause failed on its own, so the statistic that decided the bet was the all-298 sign, not the subset. Three things the round-1 audit did not quantify: (1) the all-298 interval excludes 0 only narrowly, since dropping any one of 28 questions puts its upper end at or above 0; (2) the negative sign is mostly the 26 disagreement questions, since on the other 272 the interaction is −0.036 [−0.103, +0.027]; (3) even where both models gave the same answer, Sonnet judges Haiku's errors better than Haiku does (0.90 against 0.84), so the cross-judge edge is not only knowing the answer. The paper's "Self-report is not privileged" heading states a non-detection as a finding and is cut to "no privileged self-report detected"; the subset where privilege would show cannot exclude a self-advantage of up to +0.22.

## The case that this result is false

The claim is that being the author gives no advantage in judging one's own errors. The strongest case against it: the test could not have found one. Privileged self-knowledge, if it exists, should show where the two authors disagree, and that subset has 26 questions, 19 of them Haiku errors. Its interval runs from −0.48 to +0.22, so a self-advantage of 0.2 AUROC, which would be large, is inside it. On all 298 questions the interval does exclude 0, but 272 of those are questions where both models are right or both wrong, where the stronger judge's general skill and the two models' shared blind spots dominate and where authorship has little to add. The negative point estimate, which the write-up treats as "no advantage, even slightly the reverse", is driven by the outside judge knowing the right answer on the disagreement questions: Sonnet rates Haiku's wrong answers low because Sonnet got them right. So the design pits authorship against a confound (judge knowledge of the answer) that works in the opposite direction, and the interaction cannot separate them. The paraphrase and recognition controls that would have shown whether self-recognition is even possible were cut by the budget (60 of 80, Sonnet's recognition not run). Finally, every cell is a fresh call that sees only the answer text, so "privileged access" was never available to any cell; the test can only show that shared weights add nothing, on one pair of models of unequal strength.

What survives the checklist: the all-298 non-detection is real but narrow; the subset non-detection is uninformative about effects below about 0.2; the "knows the answer" confound explains most but not all of the negative sign. None of this reverses a null: the bet's event was a detection, and it did not happen.

## Claims checked

| # | claim (results file as it stands, or paper) | check run | outcome |
|---|---|---|---|
| 1 | HH 0.845, SH 0.932, SS 0.903, HS 0.872 on 298 | my AUROC (ties half) on gm1-calls.json | holds exactly |
| 2 | I = −0.055 [−0.103, −0.007] | my item bootstrap, 5,000 resamples, seeds 1–3: [−0.110, −0.005], [−0.109, −0.005], [−0.108, −0.007] | holds; upper end −0.005 to −0.007 |
| 3 | disagreement subset 26 (Haiku wrong 19, Sonnet 7); I −0.14 [−0.50, +0.23] | recount; my bootstrap [−0.48, +0.22] | holds |
| 4 | "slightly negative" and the interval excludes 0 | leave-one-question-out: 28 of 298 drops give an upper end ≥ 0 (max +0.004) | **hole 1**: fragile, now stated (cut 1) |
| 5 | "The negative sign comes from questions where the other model knew the answer" | I on the 272 agreement questions −0.036 [−0.103, +0.027] | holds in part: the CI-excluding sign is the 26; the point estimate stays negative without them (cut 1: "mostly") |
| 6 | Sonnet beats Haiku on Haiku's errors because it knows the answer | one-bit "Sonnet's answer differs from Haiku's" scores 0.713 for Haiku's errors against the SH cell's 0.932; on the 272 same-answer questions SH 0.900 against HH 0.844 | **hole 2**: the cross edge is not only answer knowledge (cut 2 adds the number) |
| 7 | pre-registered reading "no self-advantage" | rule 1 fails on clause 1 (I < 0 on all); rule 2 fails (subset CI not below 0); rule 3 | holds; decided by the all-298 sign |
| 8 | ledger outcome 0 at 0.15; event "I > 0 with CI excluding 0 on the disagreement subset" | subset CI includes 0 | holds |
| 9 | framing effect −0.011 / +0.007; you-gave disagreement −0.316 [−0.608, −0.033] | reproduced by the author's analysis path; one of 21 uncorrected intervals | holds as a labelled secondary |
| 10 | recognition 0.51 [0.36, 0.67] on 30 + 30; Sonnet not run | cache keys recog\|*\|S absent | holds |
| 11 | 1,710 calls, $2.82, no refusal | summed cache | holds ($2.815) |
| 12 | paper line 24 "**Self-report is not privileged.**"; §4.4 heading | subset CI [−0.48, +0.22] | **hole 3**: non-detection written as a finding (cuts 3, 4) |
| 13 | paper §4.4 bullets (authorship does not help; wording; recognition) | as rows 1–10 | hold as written after round 1 |
| 14 | README "authorship gives no advantage" | as row 12 | cut to "no detectable advantage" |

## Checklist

**A.** 1. *Holds with the round-1 caveat:* the text predates the first call (03:52:51 against 03:54:55 decoded); the runner was committed 3.5 min after calls began. No new finding. 2. *Holds:* statistic, seeds, cells and the three-way rule are as frozen; amendments 1–2 are dated and change run order and crash handling only. 3. *Holds:* no bar moved. 4. *Holds:* the primary is the interaction on all 298 and on the subset, both reported.

**B.** 5. *Holds:* AUROC uses ties-half; 34 distinct Haiku-judge scores, so ties are common, but the point and interval agree with a tie-free rank statistic to three decimals. 6. *Pooling, hole 1:* the all-298 interval pools 272 agreement questions with 26 disagreement questions; unpooled, the 272 give −0.036 [−0.103, +0.027] and the 26 give −0.135 [−0.48, +0.22]. The CI-excluding-0 claim depends on the pooled set. 7. *Few items, hole 1:* 28 single-question drops put the all-298 upper end at or above 0 (max +0.004); the subset's LOO range is −0.21 to −0.03. The verdict (null) does not depend on this; the "slightly negative, excludes 0" sentence does. 8. *Holds:* nothing is fitted. 9. *Baselines, hole 2:* a one-bit predictor "the judge's own answer differs from the author's" reaches 0.713 (Sonnet on Haiku) and 0.581 (Haiku on Sonnet), well below the cross cells; restricted to the 272 questions where judge and author gave the same answer, SH is still 0.900 against HH 0.844 and HS 0.891 against SS 0.911. So the cross-judge advantage is largely text-reading by a stronger judge, not only answer knowledge; on those 272 the interaction's interval includes 0. 10. *Holds:* intervals are at question level with all four cells resampled together. 11. *Holds, stated:* 21 intervals in the table, uncorrected, labelled; only the primary carries the verdict. 12. *Holds:* no label reaches any fitting step; the archived "you gave" cells are from an earlier run on the same questions.

**C.** 13. *Hole 3:* "Self-report is not privileged" (paper line 24, §4.4 heading) states more than a non-detection with a subset interval to +0.22 allows; the pre-registration's own reading-3 wording is "as far as this test can see". 14. *Holds:* secondaries are labelled. 15. *Holds after round 1:* "text-reading" was cut; the current "mostly on questions where Sonnet knew the answer" is supported with "mostly". 16. *Cuts 1–2:* see rows 4–6. 17. *Holds:* Xiao et al. and Ashuach et al. are cited for the capability-dominates and disagreement-subset points, as in round 1. 18. *Holds.*

**D.** 19. *Holds:* $2.815 recorded against a $3 cap, with the lost-call bound disclosed. 20. *Holds:* no refusal file; one token-cap call recorded as no rating. 21. *Holds:* one confidence scale. 22. *n/a* for a null; the mm-gm1 replication is reported separately.

**E.** 23–26. *n/a:* pre-dates the beacon, lesson and design-review rules; no pre-mortem.

## The pre-mortem, scored

No pre-mortem exists (pre-registered before operators/premortem.md). My own line, written before reading the pre-registration's §6: the bet failed because the event was a detection on a 26-question subset whose interval spans half an AUROC, and because the all-298 interaction is dominated by the stronger judge's reading skill; kind world (the effect, if any, is below what this pair can show). The pre-registration's §6 names both limits.

## Required cuts

1. `results/gm1-self-knowledge.md`, "The combined self-advantage" bullet: after "−0.055 [−0.103, −0.007]" add "The interval excludes 0 only narrowly: dropping any one of 28 single questions puts its upper end at or above 0 (at most +0.004; audit round 3)." and change "comes from questions where the other model knew the answer" to "comes mostly from the 26 questions where the other model knew the answer: on the other 272 the interaction is −0.036 [−0.103, +0.027]". **Applied.**
2. Same file, "What it means": after "especially one that knows the right answer" add "; even on the 272 questions where both models gave the same answer, Sonnet judges Haiku's errors better (0.90 against 0.84; audit round 3)". **Applied.**
3. `paper/no-credence-to-read.md` line 24: "**Self-report is not privileged.**" → "**No privileged self-report detected.**" **Applied.**
4. Same file, §4.4 heading: "Self-reported confidence is not privileged" → "No privileged self-knowledge detected in self-reported confidence". **Applied.** `README.md`: "authorship gives no advantage" → "no detectable advantage". **Applied.**

## What would break it next

A same-strength pair. The design cannot separate authorship from judge strength when the judges differ by a model tier. Haiku × Haiku-clone is impossible, but Sonnet × Opus (em-dm3, run) gave −0.045 [−0.107, +0.017], the same sign with an interval including 0. The cheapest new test is 60 more disagreement questions for the Haiku × Sonnet pair, drawn from a pool where Haiku is right and Sonnet wrong as often as the reverse, so the "judge knows the answer" confound is balanced across the two self cells (about $1.50 at the recorded rates). If I on that balanced subset is positive with an interval above 0, the null here was a design artefact.

Scripts: `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/4f777718-cc86-43e1-837e-ef53cbe2abaf/scratchpad/p1a/rederive_gm1.py` (run with `python3 -I` in that folder, on files extracted from the clone at bc0f125).
