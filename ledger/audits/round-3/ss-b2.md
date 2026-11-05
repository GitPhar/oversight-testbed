---
bet: ss-b2
program: settled-science
round: 3
prereg_commit: ebd2c80 (author time 2026-11-04 17:31:23; same pre-registration and run as ss-b1)
results_commit: 230cbe4; audited text as it stands at d3fe29a
auditor_session: round-3 audit session (main checkout; stripped clone p4/clone in the session scratchpad)
auditor_model: claude-fable-5-1
author_model: claude-opus-5-5
same_model_family: true          # same vendor, different and stronger model
date: 2026-11-05 05:32 America/Denver
verdict_round1: none
verdict_round2: pass-unreplicated (in ledger/audits/ss-b1.md)
claims_checked: 9
holes_found: 2
overclaims_cut: 1
reproduced: true                 # own code: bettor − baseline −0.0683 [−0.0996, −0.0368]; baseline Brier 0.2317
verdict_claimed: pass
verdict_after_audit: pass-unreplicated
verdict_stands: true
canary: unknown
false_alarms: 0
design_review_missed: []
failed: false
failure_reason: null
failure_kind: null
premortem_score: not_failed
risk_seen: false
---

# Audit of ss-b2 (round 3): the bettor against the publication-bias baseline

## In plain English

The pass stands, and it is more robust than round 2 said, for a reason round 2 did not test. The worry was that the item-writers were told, with the answers in hand, to prefer findings that go against the paper's headline, which handicaps the publication-bias baseline. I reweighted the tagged items to every mix from 74% to 100% headline-right. The bettor beats the 0.75 baseline on the tagged items alone at every mix up to about 88%, and it beats any constant lean (h = 0.75 to 0.90) on the 38 tagged items as a set (0.134 against 0.194 or worse). On the 78 untagged items the baseline can only say 0.5 and the bettor scores 0.178. So the pass does not depend on the writers' selection. What ss-b2 does not do is add evidence beyond ss-b1: it is the same 116 bettor outputs against a weaker bar on 78 of them and a stronger bar on 38. The ledger counts it as a second hit. That is a ledger question, not a hole in the bet.

## The case that this result is false

The baseline was built to lose. Its 0.75 lean is on a side the writers tagged knowing the answer, and the writers were told to pick against it. A fair publication-bias predictor on a random sample of papers, where perhaps 85–90% of headline findings come out in the paper's favour, would score near 0.06 on those items and beat the bettor's 0.110. So "beat the publication-bias shortcut" is true of this sample and might be false of the literature.

What the checklist finds: the argument is half right. On tagged items where the headline was right, the baseline does beat the bettor (0.062 against 0.110). But the break-even share of headline-right tagged items is about 88%, the untagged items are two-thirds of the set and the baseline has nothing to say on them, and the pre-registered rule was over all post-cutoff items. The pass is robust to the selection worry; the scope note belongs in the file and is already there since D21 (cut 6 of round 2).

## Claims checked

| # | claim | check | outcome |
|---|---|---|---|
| 1 | bettor − baseline −0.068 [−0.099, −0.036] | own code | holds (−0.0683 [−0.0996, −0.0368]) |
| 2 | baseline Brier 0.232 | own code | holds (0.2317) |
| 3 | pass rule: upper bound below 0 | §5.4 at ebd2c80 | holds |
| 4 | "where the result went against its headline (10 items) the bettor got 6 of 10" | own count | holds |
| 5 | on the 28 "it works" items the baseline beats the bettor | own code (0.062 vs 0.110) | holds |
| 6 | the writers' preference weakens the baseline (D21 sentence) | reweighting, break-even 88% | holds; and the pass survives it (new) |
| 7 | "The bettor beat a predictor that only knows papers tend to report…" | pre-registered sentence | holds |
| 8 | ss-b2 scored at odds 0.30 as a hit | ledger | letter holds; not independent of ss-b1 (hole 2) |
| 9 | LOO no flip | round 2; my greedy drop of the 10 best items keeps the bound under 0 | holds |

## Checklist

A1–A4 hold (as ss-b1). B5 holds. B6 holds (tagged and untagged unpooled, above). B7 holds. B8: holds, with the circularity named: the headline tags were written by a writer who knew the answers; it favours the baseline, not the bettor. B9: hole closed by the reweighting (new): the strongest fair baseline on the tagged items alone, h chosen in hindsight from 0.75 to 0.90, is 0.194, against the bettor's 0.134. B10–B12 hold. C13–C18 hold after D21; one cut (below). D19–D22 hold. E23–E26 as ss-b1.

## The pre-mortem, scored

As ss-b1 (shared pre-mortem): not_failed, risk_seen false.

## Required cuts

1. Same as ss-b1 cut 1 (one sentence under the verdict table saying the three bets are one run scored three times). Applied once in `results/ss-b1-results.md`.

## What would break it next

A random sample of 60 post-cutoff papers in one field, items written to the same spec without the "prefer against-headline" instruction, scored against the same 0.75 baseline. About $0.40. If the bettor loses there, the baseline was beaten by the sample, not by judgment.

Scratch: `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/4f777718-cc86-43e1-837e-ef53cbe2abaf/scratchpad/p4/rederive.py` (section "ss-b2", reweighting rows).
