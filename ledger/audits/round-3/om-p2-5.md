---
bet: om-p2-5
program: other-minds
round: 3
prereg_commit: a29d6ab
results_commit: 65f1e2b
verdict_round1: null
verdict_round2: null (fail (not inherited) stands; 3 cuts applied D13; pl-008 clean)
auditor_session: round-3 fork of the audit-3 session, stripped clone at scratchpad/clone-p2 checked out at 65f1e2b
auditor_model: claude-fable-5-1
author_model: claude-opus-5-5
same_model_family: true          # same vendor, a different and stronger model than round 2
date: 2026-11-05 05:39 America/Denver
claims_checked: 14
holes_found: 1
overclaims_cut: 1                # one added sentence; the frozen verdict sentence is untouched
reproduced: true                 # own code (r3_p25.py) reproduces every U, every CI and the rule trace
verdict_claimed: null            # the ledger entered the pre-registered "fail (not inherited)" as null
verdict_after_audit: mixed       # the map's event and the pre-registered margin and copy guard are all met by a wide margin; only the design-review conjunct 5b fails. "null" (effect not found) misreads this; "mixed" is the ledger word for it. Outcome stays 0: the odds (0.25) were set for the full rule at D12, before data.
verdict_stands: false            # label only; the scored outcome is unchanged
canary: unknown
false_alarms: 0
design_review_missed: ["D8/D5: the review added conjunct 5b (Sam's uptake must not exceed the model's own re-rating) to exclude a 'Sam anchors on the planted number' responder, but the SWAP margin already excludes number-anchoring (U_sam(SWAP) 0.02). 5b therefore fails a bet when the own-labelled number pulls Sam MORE than it pulls the model's own re-rating, which on the map's own terms is stronger egocentric leakage, not its absence. The review did not pre-register what reading a 5b fail would carry beyond 'not inherited', and its 'cannot be … carried over' sentence was later found to say more than the data carry (round 2, cut 2)."]
failed: true
failure_reason: "Sam's attributed rating followed the model's own planted answer (0.50 per point) more than the model's own re-rating followed it (0.36), so the 5b conjunct fired; every other step of the rule, including the map's event and the 0.47 margin over the source-blind swap, was met. Kind design (the conjunct), with a world component (the Sam-over-self gap is real on upward plants)."
failure_kind: design
premortem_score: kind_only
risk_seen: null
---

# Round-3 audit of om-p2-5: egocentric leakage, own planted answer against the same number as Alex's

## In plain English

The numbers all hold. My own code, independent of the project's, gives U_self(OWN) 0.357 [0.259, 0.448], U_sam(OWN) 0.496 [0.389, 0.593], U_sam(SWAP) 0.022, ΔU 0.473 [0.366, 0.574], copy guard 0.411 [0.344, 0.481], Sam-minus-own +0.139 [+0.096, +0.186], and the rule trace returns fail (not inherited). The up/down split from round 2 also reproduces (+0.217 [+0.161, +0.276] upward, +0.042 [−0.022, +0.101] downward). The scored outcome, 0, is right: the odds of 0.25 were set at D12 for the rule including 5b, before any call.

What does not hold is the ledger's word for it. In this ledger "null" means the effect was looked for and not found. Here the effect the map named, the model's own planted answer pulling the rating it attributes to an uninformed Sam, was found at five times the bar and 0.47 above the source-blind baseline, with the copy guard cleared. The bet failed one conjunct, added at the design review, which says the pull on Sam must not detectably exceed the pull on the model's own re-rating. It exceeded it, by 0.14. That is a fail by the frozen rule and it stays scored as one, but it is a fail in the direction of more effect, not less. The ledger label should be "mixed", and the results file should say in one sentence what the miss is and is not. The round-2 audit already found that the "cannot be carried over" clause says more than the data carry, and that the gap sits on upward plants; those cuts are applied. This round adds the one sentence and changes the label, not the score.

Was the bar reachable? Yes: a model whose Sam uptake tracked its own re-rating (as on downward plants, where the rule reads pass) would have passed every step. So this is not a cheap miss by an impossible bar. It is a miss by a conjunct that fires on too much effect.

## The case that this result is false

The headline is a fail. The case against it is that the bet's own question was answered yes. Step 3 (the map's event) passes at 0.50 against 0.10. Step 4 (beat the swap by 0.05) passes by 0.47. Step 5 (copy guard) passes by 0.41. The only fail is 5b, which compares answers to two differently worded questions ("Please give your rating again" against "what rating would Sam give"), and the round-2 audit showed Alex's number pulls the self re-rating back (U_self(SWAP) 0.07) in a way it does not pull Sam. Adding that back, Sam still leads by +0.067 [+0.025, +0.115], so the gap is real, but its meaning is "Sam is pulled more than the self re-rating", which is a stronger projection of the model's stated answer onto Sam, not a weaker one. On that reading the verdict "null" is wrong even though the outcome 0 is right.

The checklist agrees with this case on the label and disagrees on the score: the rule including 5b was frozen before data, the engine's odds were for that rule, and never lowering a bar after data cuts both ways.

## Claims checked

| # | claim | check run | outcome |
|---|---|---|---|
| 1 | U_self(OWN) 0.357 [0.259, 0.448] | own code, seed 4252181476 | holds |
| 2 | U_sam(OWN) 0.496 [0.389, 0.593] | own code | holds |
| 3 | U_sam(SWAP) 0.022 [0.007, 0.039]; ΔU 0.473 [0.366, 0.574] | own code | hold |
| 4 | G 0.411 [0.344, 0.481] | own code | holds |
| 5 | Sam minus own +0.139 [+0.096, +0.186] | own code | holds |
| 6 | rule → fail (not inherited) | own rule | holds |
| 7 | upward +0.22 [+0.16, +0.27], downward +0.04 [−0.02, +0.10] | own code, seed 1 | hold |
| 8 | per-vignette gap > 0 in 15 of 16 | own code | holds |
| 9 | REF ratings equal across questions (new) | own means 45.5 / 45.3 / 45.3 | holds: no question-wording offset at d = 0 |
| 10 | U_self(SWAP) 0.072; Sam − (self + selfswap) +0.067 | own code | hold |
| 11 | map's event passes; margin and guard in the pre-registration, 5b from the reviews | prereg §5 at a29d6ab; D12, D12a | holds (round-2 cut 1 applied) |
| 12 | outcome 0 at odds 0.25 set before data | bets.jsonl; D12 commit time | holds |
| 13 | "null" as the ledger label | ledger convention (D5: null = effect not found) | **hole**: the effect was found; the fail is a conjunct in the direction of more effect |
| 14 | round-2 cuts applied as written | diff 65f1e2b → HEAD | holds (3 of 3, D13) |

## Checklist

A1–A4 hold (round 2: commit order, D12/D12a before the 20:55:38 run start in the run log; the rule got stricter, never looser). B5 holds. B6: pooled over directions by design; the split is now in the file. B7 holds (16 of 16 LOO; leave-two-out floor +0.079 in round 2). B8 holds. **B9, baselines:** the source-blind SWAP baseline is the strongest fair one and is beaten by 0.47; the 5b comparison is not a baseline but a theory constraint, and that is the hole. B10 holds. B11 holds. B12 n/a. **C13–C16:** the frozen verdict sentence is quoted and glossed; the one missing sentence is the plain statement of what the miss is (cut 1). C17–C18 hold. D19–D22 hold. E23 holds (round 2 fetched the pulse). E25 holds with the disclosed read-block mismatch. **E26:** see `design_review_missed`.

**Retest ceiling against the bar.** The model is near-deterministic (median within-cell SD 0), so call noise is not the limit. Every bar except 5b was cleared by a wide margin; 5b is reachable (downward plants pass it). The miss is not a ceiling artefact.

## The pre-mortem, scored

Pre-mortem: Alex's number pulls Sam as much as the model's own. It did not (0.02 against 0.50). The fail came at 5b. Kind: the pre-mortem says world; the actual failure is the conjunct's construction (design) with a real Sam-over-self gap behind it. Score: kind_only (round 2's score, kept; the failure reason is partly design).

## Required cuts

1. **Results file, "Beside the verdict" paragraph, add after the existing text:** "Round-3 audit: every step of the rule except 5b was met, and 5b fails when Sam's rating follows the model's own planted answer *more* than the model's own re-rating does. So this miss does not say the own answer failed to reach Sam; it says it reached Sam more than the design's notion of inheritance allows. The ledger label is "mixed" (the map's event met, the frozen rule not); the scored outcome stays 0 because the odds were set for the frozen rule before data." Applied in this round.

Ledger (parent session): set `verdict_after_audit` to `mixed` with a `scoring_note`; outcome 0 and the Brier are unchanged.

## What would break it next

Unchanged from round 2: a third-person self question in OWN and REF (about $0.10) to test whether 5b measures wording; and a pre-registered direction split or balanced anchors. Either would decide whether "mixed" becomes "pass" on a re-bet.

Scratch: `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/4f777718-cc86-43e1-837e-ef53cbe2abaf/scratchpad/r3/r3_p25.py`.
