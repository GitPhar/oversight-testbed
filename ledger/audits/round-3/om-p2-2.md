---
bet: om-p2-2
program: other-minds
round: 3
prereg_commit: fc00c58
results_commit: df4adee
verdict_round1: null
verdict_round2: null (fail stands; 13 cuts, applied D5; D7 follow-up)
auditor_session: round-3 fork of the audit-3 session, stripped clone at scratchpad/clone-p2 checked out at df4adee
auditor_model: claude-fable-5-1
author_model: claude-opus-5-5
same_model_family: true          # same vendor, a different and stronger model than rounds 1-2
date: 2026-11-05 05:36 America/Denver
claims_checked: 12
holes_found: 1
overclaims_cut: 1
reproduced: true                 # own code (r3_p22.py) reproduces Q, the within-condition Qs, reliabilities and the label-only predictor
verdict_claimed: null            # pre-registered "fail" (Q 0.499 < 0.80)
verdict_after_audit: null
verdict_stands: true
canary: unknown
false_alarms: 0
design_review_missed: []        # pre-registered before the design-review rule
failed: true
failure_reason: "Rendering (i), the belief attribution, varies a great deal across stories within each condition (within-TB variance 1,216 against a between-condition term of 751) while the filtered world-judgment does not track it (within-condition Q 0.07 and 0.09 at reliability 0.99); the pooled Q is almost all the seen/not-seen split. Kind world."
failure_kind: world
premortem_score: kind_only
risk_seen: null
---

# Round-3 audit of om-p2-2: perspective-filter equivalence

## In plain English

The miss stands. My own code gives pooled Q 0.499 [0.414, 0.589], TB 0.070, FB 0.092, reliabilities 0.994 / 0.999, a condition-label-only predictor at 0.477 and a condition-centred Q of 0.076, all matching the file. Could the 0.80 bar have been met? Yes: both renderings repeat at 0.99 reliability, so a genuinely equivalent pair would score near 1 and the bar is well inside reach. The miss is informative. One sentence still overstates: the heading "fail, even on the lenient test". The file's own next sentences (added in round 2) show that the pooled test was not lenient at all, since a rendering that tracked only seeing would have scored 0.48, so "even on the lenient test" says the fail is extra damning when the pooled bar was in fact a demanding one. That phrase is cut.

## The case that this result is false

Equivalence might hold and the test miss it if (a) rendering (ii) in true-belief stories is unfiltered (nothing to remove) and asks a different question ("X" rather than "Noor believes X"), so the two numbers answer different questions by construction; (b) the pooled Q is driven by a seen/not-seen split that both renderings share, so a low Q could be range or ceiling restriction in one condition; (c) the "lenient" framing hid that the bar required full story-level agreement. On the checklist: (a) is true and is disclosed in §6 and after the round-2 cuts; it limits the reading, not the verdict, because the pre-registered event is about these two renderings. (b) fails: within-condition Qs are 0.07 and 0.09 at reliability 0.99, and Spearman within TB is only +0.37, so it is not a floor artefact. (c) is right about the wording and is the one cut.

## Claims checked

| # | claim | check run | outcome |
|---|---|---|---|
| 1 | pooled Q 0.499 [0.414, 0.589] | own code, seed 2201 | holds (0.4986 [0.414, 0.589]) |
| 2 | TB Q 0.070, FB Q 0.092 | own code | hold |
| 3 | reliabilities 0.994 / 0.999 (pooled), 0.99 within | own code | hold |
| 4 | label-only predictor about 0.48 | own code | holds (0.477) |
| 5 | condition-centred share 8% | own code | holds (0.076) |
| 6 | means TB 32.9 / 13.0, FB 87.7 / 81.6 | own code | hold |
| 7 | 195 of 200 rewrites pass the frozen check | own re-implementation | holds |
| 8 | verdict fail | rule re-applied; untestable gates | holds |
| 9 | bar reachable (new) | reliabilities; Q is disattenuated | holds: an equivalent pair scores about 1.0 |
| 10 | "fail, even on the lenient test" | file's own label-only figure | **overstated** (cut 1) |
| 11 | round-2 cuts applied as written | diff df4adee → HEAD | holds (13 of 13, D5; D7) |
| 12 | scope "On this model and these stories" | text | holds |

## Checklist

A1–A4 hold (round 2 verified 13,050 request IDs in one continuous run after the commit; code diff empty). B5 holds. B6: the pooled statistic is almost all between-condition variance, now stated in the file. B7 holds (LOO 0.496–0.510). B8–B9 hold (the dumb baseline, 0.477, is in the file after round 2). B10 holds. B11: the order-arm and 2 × 2 secondaries are now labelled uncorrected. B12 n/a. **C13–C16:** one hole, the "lenient" heading (cut 1); every other plain-English sentence matches the tables after D5 and D7. C17 cannot check (BigToM licence only). C18 holds. D19–D22 hold. E23–E26: before the lesson, seed and design-review rules.

**Retest ceiling against the bar.** No cross-session retest exists for either rendering. Within-session split-half reliability is 0.99 for both, and Q is disattenuated by it, so an equivalent pair reaches about 1.0. Bar 0.80, observed 0.50. Reachable; informative miss.

## The pre-mortem, scored

My reason (header): the attribution varies across stories in a way the filtered judgment does not share. Pre-mortem: curse-of-knowledge leakage on false-belief stories. Kind world either way, mechanism different (the fail is a true-belief phenomenon; perfect FB agreement would still fail at 0.63). Score: kind_only.

## Required cuts

1. In "In plain English", replace "**Pre-registered verdict: fail, even on the lenient test.**" with "**Pre-registered verdict: fail.**" (The next bullet already explains that the pooled test, called lenient before data, turned out not to be: a seeing-only tracker scores 0.48.) Applied in this round.

## What would break it next

Unchanged from round 2 (about $0.05): rerun TB rendering (i) with the verbatim "Noor believes X" sentence deleted, to test whether the attribution's story-level variation is read-back of that sentence.

Scratch: `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/4f777718-cc86-43e1-837e-ef53cbe2abaf/scratchpad/r3/r3_p22.py`.
