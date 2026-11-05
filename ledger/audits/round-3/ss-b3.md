---
bet: ss-b3
program: settled-science
round: 3
prereg_commit: ebd2c80 (same pre-registration and run as ss-b1)
results_commit: 230cbe4; audited text as it stands at d3fe29a
auditor_session: round-3 audit session (main checkout; stripped clone p4/clone in the session scratchpad)
auditor_model: claude-fable-5-1
author_model: claude-opus-5-5
same_model_family: true          # same vendor, different and stronger model
date: 2026-11-05 05:34 America/Denver
verdict_round1: none
verdict_round2: pass-unreplicated, resting on one field (in ledger/audits/ss-b1.md)
claims_checked: 8
holes_found: 2
overclaims_cut: 1
reproduced: true                 # own code: pre 0.1045, post 0.1634, difference −0.0588 [−0.0980, −0.0183]
verdict_claimed: pass
verdict_after_audit: pass-unreplicated
verdict_stands: true
canary: unknown
false_alarms: 0
design_review_missed: ["D9: the pre-cutoff items were hand-picked by a writer who knows which older papers are famous; no rule fixed how pre-cutoff papers were sampled, so 'older papers are easier' and 'older papers are remembered' were confounded by construction before any call"]
failed: false
failure_reason: null
failure_kind: null
premortem_score: not_failed
risk_seen: false
---

# Audit of ss-b3 (round 3): pre-cutoff items score better than post-cutoff

## In plain English

The pass stands by its rule, and it is the weakest of the three round-1 bets. The pre-registered statistic (Brier on pre-cutoff minus post-cutoff items, item bootstrap) is −0.059 with an interval of −0.098 to −0.018, so the upper bound is below zero as the rule requires. Round 2 found it rests on the model-psychology field. I add two things. First, treating the four fields as clusters, a jackknife interval on the difference runs from −0.156 to +0.038, which includes zero; with only four clusters that interval is wide by construction, so it is a warning, not a reversal. Second, the archive supports memory more directly than the write-up says: on the 16 pre-cutoff items whose rationale names or recalls a specific study (my regex), the Brier is 0.024; on the other 52 it is 0.129, close to the post-cutoff 0.163. So the gap is mostly the items the bettor says it remembers. The pre-registered sentence already says the design cannot separate memory from easiness. One cut: the file should carry the cluster interval beside the item interval.

## The case that this result is false

Pre-cutoff papers were chosen by a writer who knows which 2024–2025 papers are famous, and famous papers have findings that are easy to guess from the field's folklore. The post-cutoff papers are whatever was on arXiv in the last three months. "Older scores better" is then "famous scores better", which is easiness, not memory, and the bet's title says "memory signal". The gap also sits in one field, so at the level of fields it is one observation.

What survives: the rule was met at item level, the unit the pre-registration named. The recognition split points toward memory rather than easiness, which is the direction the bet claimed. The cluster warning and the sampling confound go in the file; the label stays.

## Claims checked

| # | claim | check | outcome |
|---|---|---|---|
| 1 | pre 0.105, post 0.163, pre − post −0.059 [−0.098, −0.019] | own code | holds (−0.0588 [−0.0980, −0.0183]) |
| 2 | pass rule: upper bound below 0 | §5.5 at ebd2c80 | holds |
| 3 | "rests on model psychology: without it the upper bound is +0.019" | own code | holds (−0.0255 [−0.0684, +0.0188]) |
| 4 | other three leave-one-field-out drops keep the bound below 0 | own code | holds (−0.026, −0.014, −0.027 upper bounds) |
| 5 | field-cluster interval | own jackknife, k = 4, t(3) | hole: (−0.156, +0.038) includes 0 (cut 1) |
| 6 | "consistent with memory (or … easier; cannot separate)" | pre-registered sentence | holds |
| 7 | the recognised/not-recognised split | own regex, 16 items | memory favoured: 0.024 vs 0.129 (reported, exploratory) |
| 8 | ss-b3 scored at 0.35 as a hit | ledger | letter holds; same run as ss-b1 (see ss-b1) |

## Checklist

A1–A4 hold. B5 holds. B6: hole at the cluster level (claim 5). B7: holds at item level; fails at field level (claim 3). B8 holds. B9: no baseline applies. B10: the interval is at the pre-registered level (items); the cluster level says otherwise (cut 1). B11 holds. B12: not applicable to the statistic; the sampling of pre-cutoff papers is the leak (design_review_missed). C13–C18 hold after D21, with cut 1. D19–D22 hold. E23–E26 as ss-b1.

## The pre-mortem, scored

As ss-b1: not_failed, risk_seen false.

## Required cuts

1. After "By field, ss-b1 and ss-b2 pass with any one field removed, but ss-b3 does not …" add: "Treating the four fields as clusters, a jackknife interval on the pre-minus-post difference runs from −0.156 to +0.038 (four clusters, so wide by construction). On the 16 pre-cutoff items whose rationale recalls a specific study the Brier is 0.024, against 0.129 on the other 52, which favours memory over easiness (exploratory, round-3 audit)."

## What would break it next

Pre-register the recognition split on the next round (free), and sample pre-cutoff papers by the same arXiv query as the post-cutoff ones so fame cannot pick them.

Scratch: `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/4f777718-cc86-43e1-837e-ef53cbe2abaf/scratchpad/p4/rederive.py` (section "ss-b3").
