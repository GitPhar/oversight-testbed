---
bet: om-p2-3b
program: other-minds
round: 3
prereg_commit: 26ee5d2
results_commit: 05bfd04
verdict_round1: null
verdict_round2: null (fail (small) stands; 1 real cut applied D10; pl-002 miscount caught)
auditor_session: round-3 fork of the audit-3 session, stripped clone at scratchpad/clone-p2 checked out at 05bfd04
auditor_model: claude-fable-5-1
author_model: claude-opus-5-5
same_model_family: true          # same vendor, a different and stronger model than round 2
date: 2026-11-05 05:37 America/Denver
claims_checked: 12
holes_found: 0
overclaims_cut: 0
reproduced: true                 # own code (r3_p23b.py) reproduces Δ, its split, the pulls and R_MS
verdict_claimed: null            # pre-registered "fail (small)"
verdict_after_audit: null
verdict_stands: true
canary: unknown
false_alarms: 0
design_review_missed: []
failed: true
failure_reason: "The other reader's planted 'Yes' pulled behaviour more than the same answer in the model's own turn (other pull +0.114, own pull +0.060 over redacted), so Δ = −0.053 [−0.081, −0.028] with the same sign in both letter strata and both severities. Kind world."
failure_kind: world
premortem_score: kind_only
risk_seen: null
---

# Round-3 audit of om-p2-3b: SimpleToM decomposed on lower-severity stories

## In plain English

The miss stands and is a strong one. From the archived 7,553 calls my own code gives y(c5) = 0.148, y(c6) = 0.201, Δ = −0.053 with a 469-scenario cluster bootstrap of [−0.081, −0.028] (a different seed from the author's), Δ_match −0.027, Δ_mismatch −0.080, own pull +0.060, other pull +0.114, R_MS 0.81, judgment Δ +0.108. The bar (+0.10, interval above 0) was reachable: y(c6) = 0.20 leaves 0.80 of room, the pre-registration's own power table gives 80% at 0.125, and the paired table (15 stories aware only under c5, 46 only under c6, 71 under both) shows the effect ran the other way, not merely short. No letter artefact: the c5 answer equals the planted letter in 50.4% of stories against a 50.6% base rate. The current results file (after D10) says only what the archive carries. No cut.

## The case that this result is false

A real own-over-other effect could hide behind c6's salience (recency, prose, the word "Yes") and the single repeat. But the verdict sentence names the bundle, the sign is the same in every stratum, reaching the bar would take 90 stories to move, and the judgment question's positive Δ was pre-registered as a secondary and stayed one. The case does not survive.

## Claims checked

| # | claim | check run | outcome |
|---|---|---|---|
| 1 | c5 14.8%, c6 20.1% | own count | holds |
| 2 | Δ −0.053 [−0.079, −0.029] | own cluster bootstrap, seed 7 | holds ([−0.081, −0.028]) |
| 3 | Δ_match −0.027 (294), Δ_mismatch −0.080 (287) | own code | hold |
| 4 | own pull +0.060, other pull +0.114 | own code | hold |
| 5 | R_MS 0.81 | own code | holds (0.809) |
| 6 | judgment Δ +0.108 | own code | holds |
| 7 | 581 stories, 153 / 428 by severity | own split with the frozen regex | holds |
| 8 | verdict fail (small) | rule re-applied | holds |
| 9 | letter copying absent (new) | c5 answer = planted letter 50.4%; base 50.6% | holds |
| 10 | bar reachable (new) | room 0.80; prereg power 0.80 at 0.125 | holds |
| 11 | D10 cut applied as written | diff | holds |
| 12 | scope sentence (581 stories, severity 1–2, one model, one repeat) | text | holds |

## Checklist

A1–A4 hold (round 2: commit order, gates in code, code diff only D9). B5 holds (binary, no ties). B6 holds (same sign in every split). B7 holds (LOO −0.055 to −0.050, 0 flips). B8 n/a. B9: c6 is the control; letter baseline reported. B10 holds (469 clusters; my seed agrees). B11 holds. B12 holds (pilot ids disjoint). C13–C18 hold after D10. D19–D22 hold. E23 holds (round 2 re-fetched the pulse). E25–E26 hold.

**Retest ceiling against the bar.** One repeat per cell, so no retest noise is measured; the pre-registration's synthetic power (0.80 at Δ 0.125, 0 at Δ 0) is the ceiling statement. Observed Δ is 6 standard errors below the bar.

## The pre-mortem, scored

Pre-mortem: both planted conditions stay near the redacted rate. They did not (own +0.060, other +0.114 above it). Kind world, different mechanism: kind_only.

## Required cuts

None.

## What would break it next

Unchanged from round 2: a second sample of the c5 and c6 behaviour calls (about $0.05) to show the reversal is stable; and a judgment-primary bet, which on this archive would pass the full rule as an exploratory reading.

Scratch: `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/4f777718-cc86-43e1-837e-ef53cbe2abaf/scratchpad/r3/r3_p23b.py`.
