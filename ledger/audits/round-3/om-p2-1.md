---
bet: om-p2-1
program: other-minds
round: 3
prereg_commit: 8fb40f3
results_commit: 5931024
verdict_round1: null
verdict_round2: null (fail stands; 4 cuts, applied D5)
auditor_session: round-3 fork of the audit-3 session, stripped clone at scratchpad/clone-p2 checked out at 5931024
auditor_model: claude-fable-5-1
author_model: claude-opus-5-5
same_model_family: true          # same vendor (Anthropic), a different and stronger model than the author and than rounds 1-2 (claude-opus-5-5)
date: 2026-11-05 05:35 America/Denver
claims_checked: 14
holes_found: 0
overclaims_cut: 0
reproduced: true                 # own code (r3_p21.py) reproduces every pre-registered number to 3 d.p.
verdict_claimed: null            # the pre-registered label is "fail" (Q 0.772 < 0.90)
verdict_after_audit: null
verdict_stands: true
canary: unknown
false_alarms: 0
design_review_missed: []        # pre-registered before the design-review rule
failed: true
failure_reason: "Haiku moves a minority of claims a long way when 'how likely is it' becomes 'how confident are you' (18 of 160 by more than 30 points, 16 of 160 across the 50 line) while same-wording retest moves 3; Q 0.77 against a bar the retest ceiling (0.955) left reachable. Kind world."
failure_kind: world
premortem_score: kind_only
risk_seen: null
---

# Round-3 audit of om-p2-1: Whose belief is a rating? The framing check

## In plain English

The miss stands, and it is an informative miss. I recomputed the primary from the archived 6,400 calls with my own code (no project imports): Q(a, b) = 0.772 [0.651, 0.878], shift +0.12 [−2.88, +2.84], retest Q(a, p1) = 0.955 [0.882, 1.006]. The bar was 0.90. The question a stronger auditor has to ask of a miss is whether the bar could have been met at all. It could: the same wording asked in another session reaches 0.955, and a label-swap null between the two same-wording sessions gives Q 0.98–1.02 (2.5th to 97.5th percentile). So "interchangeable up to noise" would have scored above 0.90 comfortably, and 0.77 is far outside that band (the retest-minus-a-b difference is +0.18 [+0.08, +0.29]). Nothing in the current results file (after round 2's four cuts) says more than the data carry. No cut is required.

## The case that this result is false

The claim is that two wordings are not interchangeable. The case against: the Q statistic disattenuates only within-session repeat noise (split-half 0.98), so any between-session drift lands in the numerator, and a bar of 0.90 might sit above what even identical wording can reach. If so, the miss would be a cheap miss that flatters the engine's Brier with a bet that could never pay. Second, the two wordings differ in verb and subject at once, so even a genuine miss says nothing about "the self". Third, the gap could be a handful of self-referential claims.

The checklist settles the first line against the case: the cross-session same-wording Q is 0.955 and the label-swap null never falls below 0.98, so the bar was reachable and the miss is real. The second and third lines are right and are already in the results file after round 2 (cuts 2 and 3; the exploratory 28-claim split, with its regex now committed).

## Claims checked

| # | claim | check run | outcome |
|---|---|---|---|
| 1 | Q(a,b) 0.772 [0.651, 0.880] | own code, same seed; 2,000 question resamples | holds (0.772 [0.651, 0.878]) |
| 2 | shift +0.12 [−2.71, +2.81] | own code | holds (+0.12 [−2.88, +2.84]; seed-level wobble) |
| 3 | a–p1 retest 0.955 [0.884, 1.006] | own code | holds |
| 4 | b–d 0.667 [0.526, 0.790]; a–c 0.561; a–d 0.662; c–d 0.746 | own code | hold |
| 5 | reliabilities 0.985 / 0.982 / 0.989 / 0.993 / 0.991 | own code | hold |
| 6 | verdict fail (Q < 0.90, shift met) | rule re-applied | holds |
| 7 | "18 of 160 by more than 30 points, against 3 in the retest" | own count | holds (18; 28 over 20 points) |
| 8 | "whole interval is below it" | CI upper 0.878 | holds |
| 9 | bar reachable (new check) | retest Q; a/p1 label-swap null | holds: null band [0.981, 1.017], median 1.002 |
| 10 | retest − (a,b) excludes 0 (new) | own bootstrap | +0.18 [+0.08, +0.29] |
| 11 | 16 claims cross the 50 line between a and b (new, descriptive) | own count | 16 of 160 |
| 12 | no missing or out-of-range values | own scan | holds |
| 13 | round-2 cuts applied as written | diff 5931024 → HEAD | holds (4 of 4, D5) |
| 14 | scope: "on Haiku", one item set | text | holds |

## Checklist

A1–A4: hold (round 2 verified timing from request IDs; code diff between prereg and results is empty; no bar change). B5 holds (Pearson on means; rank version ρ² 0.80 also fails). B6 holds (round 2: unpooled by claim slot 0.70–0.82, all under 0.90). B7: a minority of claims carries the gap, disclosed in the file (7 removals → 0.90). B8 holds. **B9, the bar check (new):** the same-wording cross-session Q is 0.955 and the swap null between the two same-wording sessions is [0.98, 1.02], so the 0.90 bar is below the ceiling an interchangeable pair would reach. The miss is not an artefact of an unreachable bar. B10 holds (question-level clusters). B11 holds (one primary; the "another AI" secondary now carries its correction note). B12 n/a. C13–C18 hold after round 2's cuts. D19–D22 hold. E23–E26: pre-registered before the lesson, seed and design-review rules.

**Retest ceiling against the bar.** Ceiling 0.955 (cross-session, same wording); bar 0.90; observed 0.772. The bar sat 0.055 under the ceiling and 0.18 above the observation. An informative miss.

## The pre-mortem, scored

My own reason first (above, header). Pre-mortem: hedging toward 50 would keep Q high and break the shift. Q broke and the shift held; hedging did happen (3.1 points closer to 50) but symmetrically. Score: kind_only, as rounds 2 and the blind audit found.

## Required cuts

None. The results file as it stands after D5 says only what the archive carries.

## What would break it next

Unchanged from round 2: a verb × subject 2 × 2 on a non-self-referential item set (about $0.28 on Haiku). Nothing on this archive can overturn the miss.

Scratch: `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/4f777718-cc86-43e1-837e-ef53cbe2abaf/scratchpad/r3/r3_p21.py` (python3 -I, numpy only).
