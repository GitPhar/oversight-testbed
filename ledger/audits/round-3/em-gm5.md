---
bet: em-gm5
program: entangled-mind
prereg_commit: 9ef909d
results_commit: 8685008 (DP1, probes branch, merged); DP2 3fa5832 is on the unmerged probes branch and is not in this repository
round: 3
verdict_round1: mixed (stands with caveats; 15 cuts)
verdict_round2: mixed -> untestable (DP1, replay) -> mixed (DP2, verified on the rating side only)
auditor_session: round-3 auditor fork (parent session 4f777718), stripped clone at scratchpad/clone-p1b checked out at 8685008
auditor_model: claude-fable-5-1
author_model: claude-opus-5-5
same_model_family: true          # same vendor, different model
date: 2026-11-05 05:30 America/Denver
claims_checked: 14
holes_found: 4
overclaims_cut: 4
reproduced: true                 # own code: Q 3.72, r +0.31, p_V = p_P = 0.0001; CIs [1.51, 7.23] and [−0.43, +0.98] against the archive's [1.43, 7.03] and [−0.49, +0.99] (a different resampling of duplicated gate items); 500 of 500 gate keys replayed, confirmed
verdict_claimed: mixed
verdict_after_audit: mixed
verdict_stands: true
canary: unknown
false_alarms: 0
design_review_missed: ["D9/D11: the pass event (probe holds within its noise) was nearly unreachable by construction: the probe's within-order SD is 1% of its true–false gap, so any context sensitivity gives p_P < 0.05; the pre-registration names this risk and did not change the rule", "D10: the gate rule has no multiplicity correction; under Holm it is 2 of 10, below the threshold"]
failed: true
failure_reason: "the probe moved with order (p_P = 0.0001) and Q's interval sat above 0.5 under every scaling, so the 'clean dissociation' the odds were on could not be read; the design made the probe-holds-still outcome nearly impossible. Kind design."
failure_kind: design
premortem_score: null
risk_seen: null
---

# Audit of em-gm5 (round 3): belief versus readout on Llama-3-8B

## In plain English

The ledger's verdict "mixed" and its miss (outcome 0 at 0.30) stand. I recomputed Q, r, both permutation tests and the bootstrap from the archived run with my own code, and the numbers match. The miss is secure on both halves of the event: the probe did not hold still (p_P = 0.0001, and in told-range units it moves 3.7 times as far as the rating), and Q's interval is above 0.5 under the pre-registered scaling and does not reach below 0.5 under either alternative scaling (0.66 and 0.86). Four things are wrong with the record as it stands in this repository. First, the results file on main still carries the "UNVERIFIED, fresh run queued" banner, while the ledger scores the bet on DP2, a rerun whose data, code and results live only on a branch that was never merged here; the repository the ledger points at cannot reproduce the verdict it records. Second, one sentence contradicts the file's own numbers (order moves the probe "more than testimony" at :116, "about half as far" at :85). Third, the gate passes only without a multiplicity correction (2 of 10 under Holm; the pre-registration asked for none, so the frozen rule holds, but the file should say so). Fourth, "the internal truth signal … is not a fixed belief" reads a probe direction as a belief. All four are now cut. The scoring question is settled the other way from what a Holm purist would want: applying a correction the pre-registration did not ask for, after data, to turn a miss into "untestable, unscored" would be changing the bar after data in the engine's favour.

## The case that this result is false

Assigned the other side: the label has two halves and neither is established. "Probe moves" is a near-certainty for any probe with a within-order SD of 1% of its range; the pre-registration admitted as much ("p_P < 0.05 is likely even if the belief barely moves"). What moved is 6% of a true–false gap, from a probe that moves only 12% of that gap when told the answer outright, and in those units the probe moves *less* than the rating (Q 0.66–0.86), so "by more" is an artefact of dividing by a tiny told-cue response. "Not with the rating" is a CI on 12 cells from 3 items, decided by h191 (per-item r +0.73, +1.00, −0.45); hold the items fixed and the interval is [+0.01, +0.56]; drop h191 and r is +0.75 [+0.49, +1.00], which the frozen rule would call BELIEF MOVES. The gate itself passes at exactly its threshold and only uncorrected. And the verbal half of the test in this repository is a replay of the selection data. On this reading the result is "a probe moved a little, for reasons unknown, on three items chosen for their rating effect", and the right ledger entry is undetermined and unscored, by the om-p2-4 precedent.

What survived: the first half of that case is right about meaning and wrong about scoring. The bet's event was a *clean dissociation* (probe still, Q < 0.5). The probe moving is a fact under every scaling, and Q's interval never reaches below 0.5, so the event did not occur; that is a miss, not an undetermined, and it is a miss the design nearly guaranteed. om-p2-4 was a rule that could not fail and was called a pass; this is a rule that could hardly pass and is called a miss, which is the honest direction. The second half of the case (h191, items fixed) attacks the "not with the rating" half of the label, which the odds were not for.

## Claims checked

| # | claim (current `results/probe-dissociation.md`) | check run | outcome |
|---|---|---|---|
| 1 | Q 3.72 [1.43, 7.03], r +0.31 [−0.49, +0.99], p_V = p_P = 0.0001 | `r3/gm5_recompute.py` | holds (3.72 [1.51, 7.23]; +0.31 [−0.43, +0.98]; 0.0001, 0.0001) |
| 2 | D_V 76.7, D_P 0.250 | same | holds |
| 3 | gate: 3 of 10 at span ≥ 5 and p < 0.05 | gate summary p's | holds as frozen; **2 of 10 under Holm** (h191 adjusted p 0.107); hole 3 |
| 4 | banner: 500 of 500 step-3 verbal ratings replay the gate | compared keys, sub-ratings and M | holds (500/500) |
| 5 | banner: "a fresh step 3 … is queued" | `git log --all` in this repository; `results/` listing | **stale and unverifiable here**: DP2 (3fa5832) is not in this repository; hole 1 |
| 6 | "the probe's order effect is larger (about 3.7 times the rating's)" in told-range units | own code; alternative scalings | holds in told units; in (probe/true–false gap) over (rating/100 points) it is **0.86**, over (rating/D_V) **0.66**; the file's "6%" sentence partly covers this; hole 2 wording at :116 |
| 7 | :116 "the orderings move it more than testimony does relative to that low range" | :82–85 (order 6%, told 12% of the gap) | **contradicted**; cut 2 (round 2's cut, never applied) |
| 8 | :112 "the internal truth signal … is *not* a fixed belief" | design | mechanism/ontology drift (round 2 hole 3, never cut); cut 4 |
| 9 | sensitivity rows (layer 11 r +0.60 [+0.36, +0.81]; all 10 items r +0.06) | own code | holds (+0.60 [+0.32, +0.82]; +0.06 [−0.31, +0.42]) |
| 10 | "whether the two move together is undetermined" | items fixed [+0.01, +0.56]; without h191 +0.75 [+0.49, +1.00] | holds as written; the file's "two track closely, one does not" is right |
| 11 | told cue moves the probe; T− still reads above B0 on some items | per-item T+/T−/B0 means | T+ below B0 on all three gate items (−0.935 vs −0.850 etc.): the cue moves the probe *relative* to T−, but told-yes does not raise it above the no-chain reading; noted, not cut |
| 12 | $0 API | local run | holds |
| 13 | ledger: outcome 0 at 0.30 for "a clean dissociation" | rule rows 1 vs 4; Q under all scalings | holds (see scoring note) |
| 14 | ledger `audit_status` cites DP2 "verified on the rating side" | ledger/audits/probe-dissociation-dp2.md exists; its data do not | the audit file is here, the record it audited is not; hole 1 |

## Checklist

**A.** 1 cannot check beyond git order (local run, no request IDs; as in rounds 1–2). 2 holds for DP1 (statistic, rule, seed 48, items as frozen). 3 holds: no bar moved; the Holm note below is a caveat, not a re-bar. 4 holds.
**B.** 5 holds. 6 holds: no pooling across scale directions. 7 **hole**: "not with the rating" is one item deep (h191); the odds-bearing half (probe holds still) is not item-dependent. 8 holds: gate and test use the same conversations (the replay), which is a selection/test failure on the verbal side, corrected by DP2 off-repository. 9 **hole**: the pass event was nearly unreachable (header `design_review_missed`). 10 holds: item-and-repeat bootstrap; the items-fixed interval is reported as a sensitivity. 11 **hole**: the gate's ten per-item tests are uncorrected; the pre-registration did not require a correction, so the frozen gate stands, and the file now says what Holm gives. 12 holds (probe trained on Marks & Tegmark sets, never on study items).
**C.** 13 holds (one model, three items, stated). 14 holds. 15 **hole**: :112 (cut 4). 16 **hole**: :116 (cut 2). 17: Marks & Tegmark cited for the method; not re-opened. 18 holds.
**D.** 19 holds ($0). 20 n/a. 21 holds (one scale direction). 22 holds (never called a hit).
**E.** 23–26 n/a (pre-beacon, pre-learn, pre-design-review).

**Records (hole 1).** `ledger/bets.jsonl` em-gm5 and the ledger's audit_status rest on DP2 (`3fa5832`, probes branch). `git log --all` in this repository has no such commit, `programs/entangled-mind/results/` has no `probe-dissociation-run-2.json` or `-run-2.md`, and the results file on main still says the rerun is queued. The engine's reproducibility commitment ("every number traceable to a file") is not met for this bet. Recommendation to the engine session: subtree-pull the probes branch (or copy DP2's pre-registration, run JSON, results file and DEVIATIONS row) into `programs/entangled-mind/`, then replace the banner.

## Scoring note (mixed vs untestable)

The ledger scores em-gm5 as a miss. Three readings were considered: (a) keep "mixed", outcome 0; (b) call the gate failed under Holm, hence "untestable" and unscored; (c) call it "undetermined" by the om-p2-4 precedent. (b) applies a correction the pre-registration did not ask for, after data, and its only effect is to delete a miss, which invariant 6 forbids in either direction. (c) does not fit: om-p2-4's rule could not fail; this rule could not easily *pass*, and the event it priced (probe still, Q < 0.5) demonstrably did not occur under any scaling. (a) is right. The honest addition is that the 0.30 was placed on an event the design made nearly impossible, which is a lesson about the odds, not a reason to unscore them.

## The pre-mortem, scored

None written. My own line: the probe's noise floor is so low that "holds within its noise" could not be read, so the dissociation row was unreachable; kind design. `premortem_score: null`.

## Required cuts (all applied to `programs/entangled-mind/results/probe-dissociation.md`)

1. Banner: "A fresh step 3 on new seeds is queued …" → state that DP2 ran on the `probes` branch (3fa5832), returned the same label with the rating side verified (`ledger/audits/probe-dissociation-dp2.md`), and that its data and results are not in this repository.
2. :116 "and the orderings move it more than testimony does relative to that low range" → "and the orderings move it about half as far as testimony does (6% against 12% of its true–false gap)".
3. :43 gate sentence: add "(uncorrected per-item tests, as pre-registered; under a Holm correction over the ten items only h101 and h190 pass, so the gate would fail at 2 of 10)".
4. :112 "the internal truth signal for the main statement is *not* a fixed belief under an order-dependent readout" → "the layer-13 truth-probe reading of the main statement is not fixed under chain order; whether that reading is a belief is not something this probe can say".
Also at the Q row and the plain-English bullet: add the alternative-scaling figures (0.66 and 0.86), so "by more" is seen to depend on the told-cue denominator.

## What would break it next

Free: adopt DP2 into the repository. Then, $0 and about an hour of laptop time (a local model, so not for an auditor): a probe trained on in-context true/false statements, read at the same point; if it moves with order more than 12% of its gap and in step with the rating (items fixed), the readout is belief-like after all. Script: `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/4f777718-cc86-43e1-837e-ef53cbe2abaf/scratchpad/r3/gm5_recompute.py`.
