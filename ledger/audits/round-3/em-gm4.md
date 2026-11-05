---
bet: em-gm4
program: entangled-mind
prereg_commit: e913227
results_commit: bc9e70d
round: 3
verdict_round1: mixed (stands; 5 cuts)
verdict_round2: not re-audited
auditor_session: round-3 auditor fork (parent session 4f777718), stripped clone at scratchpad/clone-p1b checked out at bc9e70d
auditor_model: claude-fable-5-1
author_model: claude-opus-5-5
same_model_family: true          # same vendor, different model
date: 2026-11-05 05:30 America/Denver
claims_checked: 12
holes_found: 1
overclaims_cut: 1
reproduced: true                 # every hit rate, chance rate, excess, CI and contrast recomputed to 3 decimals from gm4-calls.json and the frozen gm4-menus.json
verdict_claimed: mixed
verdict_after_audit: mixed
verdict_stands: true
canary: unknown
false_alarms: 0
design_review_missed: []         # the overlap of EIG and confirmatory targets on 62–78% of menus is a D9 (baseline) flaw a design review should have caught
failed: true
failure_reason: "the bet's event (EIG above chance and above the confirmatory rule) failed because the EIG and confirmatory targets coincide on most menus; where they differ, EIG picks are exactly at chance. Kind design."
failure_kind: design
premortem_score: null            # pre-registered before operators/premortem.md
risk_seen: null
---

# Audit of em-gm4 (round 3): evidence seeking, informative or confirmatory?

## In plain English

The verdict "mixed" stands and the ledger's miss (outcome 0 at 0.20) is right: the bet's event needed EIG above the confirmatory rule, and the two contrasts are −0.24 [−0.52, +0.04] and −0.14 [−0.40, +0.14]. Every number regenerates exactly from the archive with my own code, including the screen-position mapping on all 1,200 calls. The one thing the results file still lets a reader believe is that the model's picks "beat chance under every rule", the informative rule included. They do not in any informative sense: the EIG rule's target coincides with the confirmatory claim on 74 of 120 menus (D5) and 94 (BA5), and on the menus where they differ the EIG rule is at chance (−0.002 and 0.000) while the confirmatory rule stays above chance under D5 (+0.20 [+0.04, +0.36]; 26 menus favour it against 15). Round 1 found this and did not write it into the file; it is now there, labelled exploratory. The deeper point is that the test was weak by design: on 62–78% of menus it could not tell the two rules apart, and the decisive comparison rests on 14–23 items.

## The case that this result is false

The strongest case against "mixed" is that it should read "confirmatory". On the discriminating menus the point estimates favour the confirmatory claim under both models, the sign count under D5 is 26 menus to 15, and the confirmatory rule alone keeps its above-chance excess where the EIG rule loses all of it. The pre-registered rule asked for a CI above 0 on the paired difference, which fails, so "mixed" is the frozen reading; but a reader who takes "mixed" as "the model does both" would be wrong: the data point one way and lack the power to say so. The case for the opposite direction, that the model does track EIG, has nothing: its only support is a +14/+21 point excess that evaporates on the disjoint menus.

What survived: the frozen rule returns "mixed or at chance", and neither direction clears its interval. The results file's "if anything it leans confirmatory" is the right hedge. The cut is to stop the "every rule" sentence from implying informativeness-seeking was shown.

## Claims checked

| # | claim | check run | outcome |
|---|---|---|---|
| 1 | EIG D5 39% / 25% / +0.141 [+0.042, +0.245] | `r3/gm4_recompute.py` | holds (+0.141 [+0.042, +0.245]) |
| 2 | EIG BA5 55% / 34% / +0.210 [+0.113, +0.310] | same | holds |
| 3 | dM D5 +0.196, dM BA5 +0.166, confirmatory +0.207 [+0.109, +0.313], most-uncertain −0.128 [−0.205, −0.043] | same | holds |
| 4 | discriminating: D5 46 menus −0.237 [−0.523, +0.044]; BA5 26 menus −0.135 [−0.403, +0.142] | same; 23 and 14 items | holds |
| 5 | per-model "neither", verdict "mixed or at chance" | §6 rule applied | holds |
| 6 | modal share 87%; positions 27/26/26/21; D5–BA5 agree 41/120 | same | holds (0.868; 26.8/26.3/26.0/20.8; 41) |
| 7 | screen-position mapping (i + r) mod 4 | asserted on all 1,200 calls | holds |
| 8 | "Its picks beat chance under every rule that scores a claim by how much it bears on the answer" | overlap split | **misleading**: EIG excess on disjoint menus −0.002 [−0.135, +0.137] (D5), 0.000 [−0.150, +0.183] (BA5); on overlap menus +0.230, +0.269 (cut 1) |
| 9 | "if anything it leans confirmatory" | sign count 26 vs 15 (D5), 9 vs 8 (BA5); confirmatory excess on D5-disjoint +0.197 [+0.038, +0.357] | holds as a hedge |
| 10 | "Neither is a clear confirmation bias" | contrast CIs include 0 | holds |
| 11 | ledger outcome 0 at 0.20 for "EIG above chance and above the confirmatory rule" | rule | holds |
| 12 | spend $0.11, no refusal | cache sum | holds |

## Checklist

**A.** 1 holds (pre-registration 04:05, calls 05:02–05:04 decoded in round 1, result 05:05; menus and scores frozen in the pre-registration commit). 2 holds. 3 holds. 4 holds.
**B.** 5 holds: ties in target sets are handled as pre-registered (chance = |set|/4); mean set sizes 1.0–1.8. 6 holds, with the finding at claim 8: pooling overlap and disjoint menus is the design, and unpooled the EIG excess is all overlap. 7: the discriminating sets are 23 and 14 items; the file says 46 and 26 menus, and the item counts are now added. 8 holds: no circularity (scores frozen; chooser never sees them). 9 **hole**: the baseline the bet had to beat (confirmatory) shares its target with EIG on most menus, so the design could discriminate on 38% (D5) or 22% (BA5) of menus; a design review would have asked for menus built to separate them. Listed as the failure kind. 10 holds. 11 holds (one pre-registered conjunction; secondaries labelled). 12 holds.
**C.** 13 holds (one model). 14: the exploratory overlap split is now labelled exploratory. 15: "partly what an inquiring mind would do" is interpretation, left as an aside. 16 hole (claim 8, cut 1). 17: Jhaveri et al. cited for a direction, not a number; not opened. 18 holds.
**D.** 19–22 hold ($0.11 of $0.50; one scale; "mixed" never called a hit).
**E.** 23–26 n/a (pre-beacon, pre-learn, pre-design-review).

## The pre-mortem, scored

None written. My own line: the confirmatory and informative targets coincide on most menus, so the contrast had little power; kind design. `premortem_score: null`.

## Required cuts

1. `results/gm4-evidence-seeking.md:11`: after the "every rule" bullet list, add: "(Exploratory, after the verdict: the informative rule's excess comes entirely from the 74 (D5) and 94 (BA5) menus where its target is also the confirmatory claim; on the 46 and 26 menus where they differ it is at chance, −0.002 [−0.135, +0.137] and 0.000 [−0.150, +0.183], while the confirmatory rule stays above chance on the D5 menus, +0.197 [+0.038, +0.357]. So the excess does not show that the model seeks informative checks.)" and give the item counts (23 and 14) beside the menu counts. **Applied.**

## What would break it next

Menus built so that the EIG target and the confirmatory target never coincide (drop menus where they do, or choose 4-subsets that separate them), 40 items × 3 menus × 10 repeats, about $0.12. If the confirmatory rule's advantage holds with a CI above 0, the verdict becomes "confirmatory", the Jhaveri et al. pattern inside the model's own deliberation. Script: `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/4f777718-cc86-43e1-837e-ef53cbe2abaf/scratchpad/r3/gm4_recompute.py`.
