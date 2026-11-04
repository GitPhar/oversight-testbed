---
bet: om-p2-4
program: other-minds (program 2)
prereg_commit: 0ee0ee9 (author 2026-11-04 15:04:37 -07:00); seed commit d8bdbc7 (15:05:31)
results_commit: b271227 (author 2026-11-04 15:41:33 -07:00)
auditor_session: bb46787f-112b-4a3c-a1e9-dd87d67b2c75 (local tab, entangled-mind-audit2 worktree)
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5   # commit trailer of 0ee0ee9, d8bdbc7, b271227: "Co-Authored-By: Claude Opus 5.5"
same_model_family: true
date: 2026-11-04 15:57 America/Denver
claims_checked: 26
holes_found: 9
overclaims_cut: 14
reproduced: true
verdict_claimed: pass            # stated as "pass, unreplicated"
verdict_after_audit: null        # "null written as a finding": the frozen rule's letter is met, the test cannot decide
verdict_stands: false
canary: unknown
false_alarms: 0
failed: true
failure_reason: "design: the pass's main conjunct is a non-detection with no power check, its percentile interval is biased toward 0 for the more accurate arm (bias-corrected intervals exclude 0), and the gate and r>=0.70 bar are met by a predictor that predicts no uptake at all"
failure_kind: design
premortem_score: other
risk_seen: null
---

# Audit of om-p2-4: interpersonal replication against program 1's fingerprint

## In plain English

The run itself is clean. It was frozen before any call, the seed recomputes, every call is archived, the budget held ($0.90 of $1.25) and nothing was refused. The analysis regenerates byte for byte, and my own independent code gets the same numbers. The "pass", though, is a failure to detect a difference, not evidence of no difference. The pre-registered rule asks only that the interval for "self error minus Sam error" not lie wholly below 0. The self arm's error is 0.054 against Sam's 0.097, and the interval reaches +0.043 only because the bootstrap used is biased toward 0 here: 70% of resamples sit above the point estimate. A basic bootstrap interval gives [−0.129, −0.012] and a bias-corrected (BCa) one [−0.105, −0.004]. Both exclude 0 on the self-advantage side. No power check was pre-registered, although program 2's own map requires one for every self/other null. Given the observed error pattern, the self arm's error would have had to fall roughly by half again before the frozen rule could see it. The other two conditions (the gate and r(a, b) ≥ 0.70) are also met by a dumb predictor that says the planted answer has no pull at all. Verdict after audit: **null**, the test does not decide. The plain-English sentences saying the model "knows itself about as well as it knows Sam", that this "supports the seed hypothesis", and that self and Sam are "one operation" are cut. Exploratory data point the other way: on own-answer uptake, the self arm is more accurate (block ΔMAE −0.193 [−0.237, −0.016]), and the "you"/"Sam" label alone shifts the predicted uptake by −0.21 [−0.28, −0.14].

## The case that this result is false

*Written before the checklist.* The headline says self-prediction is "not detectably better than predicting Sam" and calls that a pass. A pass is supposed to be a finding, but this rule turns *any* failure to detect into one. The rule has no equivalence margin, and the pre-registration has no power analysis. Eleven effects are bootstrapped over 16 and 40 items, so the interval will be wide whatever the truth. Worse, the point estimate is not near 0. The self arm's error is about half of Sam's (0.054 against 0.097), and the published interval [−0.074, +0.043] is lopsided around −0.043. That lopsidedness is the mark of a biased bootstrap. MAE is a mean of absolute values, and resampling inflates small absolute errors far more than large ones. So the more accurate arm's MAE is pushed up in resamples, and the difference is dragged toward 0, the direction that makes "pass" more likely. The second condition, r(a, b) ≥ 0.70, is computed over eleven numbers that share a lot of built-in structure, such as "shown answer → high repeat agreement" and the always-50 predictor's own pattern. Two arms that both read the transcript would correlate above 0.70 even if their *errors* were unrelated. If so, it does not measure "the two accounts look alike". The headline's second half, "causal reports anti-correlated −0.94, −0.97", is a pre-registered *secondary* computed over six condition means, yet it sits in the commit headline. Finally, the "self" and "Sam" arms differ in the very effect the hypothesis is about: the Sam arm predicts much stronger commitment to "Sam's" own earlier answer. That is a label effect. It is the opposite of "one operation run on the same transcript". If all of this holds, the honest reading is "the test could not tell, and it leans toward a self advantage on own-answer commitment", not "pass".

The checklist below finds this case largely right.

## Claims checked

| # | claim (results file, ≤15 words or paraphrase) | check run | outcome |
|---|---|---|---|
| 1 | Pre-registered at 0ee0ee9, seed d8bdbc7, "both came before any call" | author dates; ridtime on 13,796 request IDs | holds: first call 15:16:15, last 15:39:36 |
| 2 | 13,796 calls, $0.90 of $1.25, no refusal | count/sum of `p2-4-calls.json`; no refusal file in tree | holds ($0.8987) |
| 3 | Eleven-effect table (measured, a, b, c, always-50) | `work/indep.py` (independent code) | holds, all 55 cells |
| 4 | Measured fingerprint = program 1's published values | P1 `bm0-source-distance-lag.json`; P1 file dates | holds (u own .708/.443/.206, other .192/−.107/−.125; all archives committed before 09:37 and clean) |
| 5 | Gate r 0.978 [0.891, 0.993], 0.963 [0.906, 0.985] | `indep.py` | number holds; meaning is a hole (B9) |
| 6 | MAE a 0.054 [0.045, 0.121], b 0.097 [0.066, 0.150] | `indep.py` | numbers hold; bootstrap biased (boot means 0.078, 0.104) |
| 7 | ΔMAE −0.043 [−0.074, +0.043] | `indep.py`, same seed and RNG order; seeds 1–3 | number holds exactly; seed-insensitive; interval biased (B10) |
| 8 | "not detectably more accurate" → pass | basic and BCa intervals; detection boundary (`attack.py` §1) | hole: basic [−0.129, −0.012], BCa [−0.105, −0.004]; no power check |
| 9 | r(a, b) 0.948 [0.815, 0.982] on departures | `indep.py` | number holds; meaning is a hole (B9): error r = 0.142 |
| 10 | Leave-one-effect-out r(a, b) 0.904–0.941 | `indep.py` | hole: that is the raw-effect r, which D3 rules invalid; departure r is 0.907–0.965 |
| 11 | Leave-one-effect-out ΔMAE −0.062 to −0.023 | `indep.py` | holds |
| 12 | "knows itself about as well as it knows Sam" | table | hole: 0.054 vs 0.097 |
| 13 | "Almost all of the self arm's edge is one effect" (own commitment) | `blocks.py` | holds, understated: own-uptake block contributes −0.053 of the −0.043 total |
| 14 | Self 0.71/0.42/0.22; Sam 0.84/0.67/0.47 own uptake | `indep.py` | holds |
| 15 | "Sam ... repeat the shown number exactly 60%, self 41%" | `attack.py` §4 | hole: exact rates 49.4% / 31.5%; 60/41 are within ±1; measured rate (44.3%) omitted |
| 16 | Cell r 0.87 vs 0.93 (U), 0.89 vs 0.88 (O/RA) | `attack.py` §4 | holds |
| 17 | Causal reports rise with distance and for other's number | `attack.py` §3 | holds |
| 18 | Causal r −0.94 / −0.97 vs measured uptake; 0.98 between arms | `attack.py` §3 | numbers hold; n = 6 condition means; item-bootstrap CI (a) [−0.976, −0.746], (b) [−0.984, −0.835]; Spearman −1.0 |
| 19 | "That is Nisbett and Wilson's 1977 pattern" | `map/reads/d-first-third-person.md` | partly: N&W's observers read a one-line description; arm (b) reads the full transcript (C15/C17) |
| 20 | One-line observer ≈0.45 everywhere; error 0.21, CIs exclude 0 | JSON, `indep.py` | holds |
| 21 | "comes out on this model the way it came out in people" | table, read of N&W | hole: N&W subjects were no more accurate; here self error is 56% of Sam's |
| 22 | "This fits program 1's F5" | rank check | hole: non-detection presented as support |
| 23 | "first wave result that supports the seed hypothesis ... one operation" | `blocks.py`, `attack.py` §2 | hole: label shifts own-uptake prediction −0.21 [−0.28, −0.14]; error r 0.14 |
| 24 | Secondary table (contrasts, raw r 0.926, cell r 0.887, MAE c, n50) | JSON vs md | holds |
| 25 | Conversations rebuilt exactly | `turns_for` structure vs 8,000 archived conversations; planted-value files | holds: 0 mismatches; gm2/gm2b planted records identical |
| 26 | "pass, unreplicated" label | invariant 7 | the label is right for a pass; after audit the verdict is null |

## Checklist

**A1. Pre-registration predates the first call and the first archive read for analysis.** *Holds.* Author times: 0ee0ee9 15:04:37, d8bdbc7 15:05:31, b271227 15:41:33 (`git -C /Users/seanpharris/other-minds log --format='%h %aI'`). Request IDs decoded with `audits/tools/ridtime.py -k`: first call 15:16:15 (U), last 15:39:36 (CR), all 13,796 IDs unique and well formed. The program 1 ground truth was computed before freezing (the pre-registration says so). This is not analysis of the bet's data, because no predictions existed yet. P2-3's 26 calls run 15:40:39–15:40:41, after P2-4's last call, so D3's run order was kept.

**A2. Pass rule, statistic, split, seed, budget match the pre-registration.** *Holds for what is written. Hole for what is missing.* The code at b271227 is byte-identical to 0ee0ee9 (`diff`). The §5 rule (gate; CI of ΔMAE not wholly below 0; r(a, b) ≥ 0.70 point), 2,000 resamples over bm items (16) and gm items (40) independently, `seed32 (boot)` 2905035151 and the $1.25 cap all match. The map's event at a20824d ("CI of the error difference includes 0 or favours (b)") is the same event. **Hole:** `map/program-2-map.md` (a20824d), next-steps table: "Power simulation before claiming a self/other null (C5, C14) | standing rule: every null claim needs a pre-registered power check." The pre-registration has none, and no deviation row waives it. See B10 for what a power check would have shown.

**A3. Bar not lowered after data.** *Holds.* No change after 0ee0ee9, apart from the seed fill-in in d8bdbc7.

**A4. Reported primary is the pre-registered primary.** *Holds* in the results file. The commit subject puts a pre-registered secondary (the causal report) beside the primary (C14).

**B5. Ties and floating point.** *Holds.* Integer ratings; RA uses ≤ 5 on integers; no ranking or tie-breaking enters the primary. Floor: predictions at 0 or 100 are ≤ 0.5% in U and G. **Causal report (a): 33.9% of answers are exactly 0** (Sam arm 4.8%). The self arm's causal report is largely at floor (`blocks.py`).

**B6. Pooling.** *Hole (disclosure).* The primary MAE pools three blocks whose self-minus-Sam gaps have opposite signs (`blocks.py`, pre-registered seed, 2,000 item resamples):

| block | ΔMAE (a − b) | 95% pct CI |
|---|---|---|
| own uptake (3 effects) | −0.193 | [−0.237, −0.016] |
| other uptake (3) | +0.034 | [−0.078, +0.224] |
| order + repeat agreement (5) | +0.001 | [−0.030, +0.020] |
| all 11 (primary) | −0.043 | [−0.074, +0.043] |

Unpooled, the self arm is detectably more accurate on own-answer uptake, the F3 effect the hypothesis is about. This is exploratory and not a replacement primary. The pooled "not detectably more accurate" sentence must say so.

**B7. Few items driving it.** *Holds.* Leave-one-bm-item-out ΔMAE ranges over [−0.050, −0.017], all 16 negative. Leave-one-gm-item-out ranges over [−0.045, −0.042]. Leave-one-item-out r(a, b) on departures: [0.936, 0.960]. Leave-one-effect-out ΔMAE: [−0.062, −0.023], all negative. No item or effect carries the sign. Every deletion leaves the point estimate on the self-advantage side.

**B8. Circular estimators.** *Holds.* Nothing is fitted. Measured and predicted effects come from the same function, on the same resampled items.

**B9. Baselines and controls.** *Hole.* The gate and part 2 are supposed to show that the arms "know the fingerprint" and "look alike". Both are met by predictors that know nothing about uptake (`attack.py` §2). Such a predictor gives every cell u = 0 (no pull) and, for the conversations, copies the visible earlier answer:
- gate r(x − n50, measured − n50) = 0.805, CI [0.481, 0.954]: **passes the gate**;
- r(x − n50, a − n50) = **0.716**: **meets the r ≥ 0.70 bar against the self arm**;
- MAE 0.220, i.e. it gets every uptake wrong.

A constant u = 0.45 (arm c's pattern) plus the same copy rule gets gate 0.711 [0.454, 0.913] and r with (b) = 0.701. Pure random predictors do not pass (median r 0.05; 8% ≥ 0.70), so D3's fix works against noise but not against structure. The reason is that subtracting n50 subtracts the *same* vector (its u values +0.541/−0.212/−0.469, and RA ≈ 0) from every predictor, which builds a shared component into every departure. The two arms' *errors* (departures from measured) correlate at **r = 0.142** over the 11 effects. So r(a, b) = 0.95 says both arms are near the truth plus shared structure. It does not show that they err alike.

**B10. Uncertainty.** *Hole.* Level: items, as pre-registered (bm 16, gm 40, resampled independently). Correct. Independent code with the same seed and RNG order reproduces [−0.0739, +0.0425] exactly, and seeds 1, 2, 3 give [−0.0746, +0.0423], [−0.0743, +0.0424], [−0.0743, +0.0427]. The interval is seed-insensitive and is not a seed artefact. But the bootstrap is biased. Output of `work/indep.py`:
- the point ΔMAE is −0.0430, but the bootstrap mean is −0.0258 and the median −0.0296. Only 30.4% of resamples fall below the point (z0 = −0.51), and 82.2% of resamples have ΔMAE < 0;
- MAE(a) point 0.054 vs bootstrap mean 0.078 (+0.023); MAE(b) 0.097 vs 0.104 (+0.006). The absolute value inflates the smaller error more, so the percentile interval for the difference is dragged toward 0 and favours "pass";
- basic (reverse-percentile) interval **[−0.129, −0.012]**; BCa (joint jackknife over the 56 items, a = −0.070) **[−0.105, −0.004]**. Both exclude 0 on the self-advantage side, so under either the frozen rule's part 1 would *fail*.

The frozen code uses the percentile interval, so the letter of the rule is met. But whether "pass" or "fail" comes out depends on the choice of bootstrap interval, which is the same class as the founding week's tie-breaking artefact.

**Power / minimum detectable effect** (`attack.py` §1). Bootstrap SD of ΔMAE = 0.030, so 80% power at two-sided 5% needs a true ΔMAE of about 2.8 × 0.030 ≈ **0.084**. That is 87% of Sam's whole MAE (0.097): the self arm would need an error near 0.013. The second check scales the observed self arm's cell errors by λ. The frozen percentile rule detects a self advantage only at λ ≤ 0.5, with self MAE ≈ 0.029 (λ = 0.75, MAE 0.044: CI [−0.089, +0.016], not detected). The observed self arm, with an error 56% of Sam's, was not detectable by construction. A different error structure (a mix of truth and Sam's predictions) is detectable at λ = 0.75 because its errors co-vary with Sam's. Power therefore depends on an error structure that was not modelled before the run.

**B11. Multiple comparisons.** *Holds.* One primary rule (three conjuncts); secondaries are declared descriptive. The secondary "CIs exclude 0" for arm (c) is uncorrected and labelled secondary.

**B12. Leakage.** *Holds.* No fitting step.

**C13. Scope drift.** *Holds mostly.* "One model; program 1's item sets." is stated. "That is Nisbett and Wilson's 1977 pattern, in a language model" should say "in this model".

**C14. Rank drift.** *Hole.* "It is the first wave result that supports the seed hypothesis" and "This fits program 1's F5" present a non-detection as support. The commit subject carries the secondary causal-report correlations beside the primary. The results file labels them secondary, so only the commit message drifts. That cannot be cut, but the ledger line should not repeat it.

**C15. Mechanism drift.** *Hole.* (i) "the account of self and the account of another assistant look like one operation run on the same transcript". The design cannot separate this from its rivals, and the data lean against it. The label alone moves the predicted own-answer uptake by **−0.208 [−0.277, −0.140]** (a − b, `blocks.py`). The Sam arm's own-uptake signed error is +0.207 [+0.115, +0.291], against the self arm's −0.002 [−0.113, +0.094]. The error correlation is 0.14. (ii) The causal-report reading ("gives a theory that is wrong") has a rival the design cannot exclude: the scale is "100 = all the way to that number", and an arm that cannot see the statement's base may read it as an absolute change. Within own-source, the self arm's reports (0.084, 0.129, 0.190) track the absolute measured shift u·|d| (0.071, 0.133, 0.124) better than the fraction. A third of the self arm's reports are at the floor.

**C16. Plain English matches the table.** *Hole.* Sentences the table does not support:
- "the model knows itself about as well as it knows 'Sam'" (MAE 0.054 vs 0.097);
- "Given the same transcript, the model predicts 'Sam' nearly as well as itself";
- "Sam is predicted to repeat the shown number exactly 60% of the time, the self arm 41%" (exact equality: 49.4% and 31.5%; 60.3% and 41.2% are *within ±1*, as the exploratory table itself says);
- "Leave-one-effect-out ... r(a, b) from 0.904 to 0.941". That is the raw-effect r (`p2_4_interpersonal.py` line 338 uses `np.corrcoef(vec["a"][keep], vec["b"][keep])`), which D3 declares invalid. The pre-registered statistic on departures ranges over [0.907, 0.965];
- "The pre-registered gate is passed with room to spare" (a predictor that predicts no uptake passes it too: B9).

All other numbers in the file match `results/p2-4-interpersonal.json` and my recomputation.

**C17. Citations.** *Cannot check fully.* No network, and the paper itself was not opened. The program's own read (`map/reads/d-first-third-person.md`, Nisbett & Wilson 1977, Nisbett & Bellows) says that subject and observer reports correlated .77–.99 and that subjects were no more accurate than observers, where the observers read a one-line description. The results file's mapping ("subjects' and observers' causal reports agree with each other and not with what actually moved the behaviour") is consistent with the stocking/position studies. Its observer, arm (b), reads the full transcript, not a one-line description. The design's one-line arm (c) had no causal report.

**C18. Negatives stated as plainly as positives.** *Partly holds.* The file does say "'No difference' would overstate it; 'not shown' is accurate" and "a larger test could find one". It does not say that the self arm is detectably better on own-answer uptake when that block is taken alone (exploratory), and the cut sentences above contradict its own caveat.

**D19. Budget.** *Holds.* The cap is checked under a lock before every call (`om_common.Caller.run`), with at most 8 calls in flight past the cap. Spend $0.8987 against the §3 estimate of $0.55 and the cap of $1.25.

**D20. Stop on refusal.** *Holds.* 13,796 = the full job list (U a/b 1,920 each, G a/b 3,200 each, U c 1,920, O c 20, RA c 80, CR a/b 768 each). No refusal or error file in the tree. P2-3's refusal (15:40:41) came after P2-4's last call (15:39:36).

**D21. One scale direction.** *Holds.* Every predicted rating is anchored "0 = certainly false, 100 = certainly true". The causal-report and observer scales are one-directional magnitudes.

**D22. Replication label.** *Holds.* "pass, unreplicated" is used, and the scope is one model. After audit the verdict is null.

**E23. Seed.** *Holds where checkable.* CURBY-Q round 28297 (2025-08-22 13:42), more than 24 h before the commit, so the chain is stalled and the first CURBy-RNG pulse after the commit is the right source. The hardware amendment 69d1bcd (14:57:50) predates the prereg. Pulse 1591349 at 15:05:00 is after the 15:04:37 author time, and the recorded previous pulse (1591348) is at 15:04:00. `python3 /Users/seanpharris/oversight-testbed/ledger/seed.py c16a97f4…f81a om-p2-4 --purpose boot` → seed 14963471766438498703, seed32 2905035151, equal to `data/p2-4-seed.json` and the JSON's `seed32_boot`. The code reads only that file (line 284). Nothing was called between the commits: first call 15:16:15. **Cannot check:** that the randomness and the pulse times are CURBy's (a beacon fetch is forbidden in this audit). The seed drives only the bootstrap, and seeds 1–3 give the same interval to ±0.0004, so seed shopping could not have changed the verdict.

**E24. Tiebreak.** Not applicable (`bet_type: standard`).

**Other checks.**
- Wording confound (self vs Sam): *holds.* `predict_prompt` and `causal_prompt` differ only in the subject ("you, an AI assistant" / "an AI assistant called Sam"; "yours"/"Sam's"; "you would give"/"Sam would give"), and the transcript is identical.
- Fidelity of the rebuilt conversations: *holds.* 0 turn-structure mismatches over 8,000 archived gm2/gm2b conversations, identical planted records in gm2 and gm2b files, and the U wording equals bm0/bm1/run 3's. One difference: the archived "other" turns used a `{decision, probability}` schema that the predictor never sees.
- Program 1 archives: all were last committed between 2026-11-03 15:14 and 2026-11-04 09:36, and are clean in the working tree, so the fingerprint was fixed before the run.

**Auditor's own deviation.** The pre-mortem's gist was visible to me before the checklist was done, because it sits in 0ee0ee9's commit message ("Pre-mortem (artefact): planted own answer pulls self-prediction, not Sam's") and in §0 of the pre-registration, which A2 requires reading. The failure reason in the front matter was still written from the checklist evidence, and it names a different kind (design).

## The pre-mortem, scored

**Auditor's failure reason (from the checklist):** design. The primary conjunct is a non-detection without the map's required power check. Its percentile interval is biased toward 0 for the more accurate arm, so bias-corrected intervals exclude 0. The other two conjuncts are met by a know-nothing predictor. The test could not decide.

**Pre-mortem (§0 at 0ee0ee9):** "If this fails, the most likely reason is that the planted 'own' answer pulls the self-prediction but not the Sam prediction, so arm (a) wins on own-answer uptake through a source label, not self-knowledge." Kind: `artefact`.

**Score: `other`.** The bet failed on design (power and interval bias), not on the named label artefact. Part of the named territory did show up. Arm (a) does win on own-answer uptake (block ΔMAE −0.193), and a source label does move own-uptake predictions (−0.21). But the direction is reversed: the label pulled the *Sam* prediction more. That did not sink the primary, which is not where the verdict turned.

## Required cuts

1. §In plain English, "**Pre-registered verdict: pass.** On this test, the model knows itself about as well as it knows "Sam", and its two accounts look alike." → "**Pre-registered rule: met by its letter; audited verdict: null.** The test could not tell whether the model predicts itself better than "Sam". Its self-prediction error is about half of Sam's (0.054 vs 0.097). The pre-registered interval includes 0 only under a percentile bootstrap that is biased toward 0 here; basic and bias-corrected intervals exclude 0 (audit om-p2-4)."
2. "**Both arms know the fingerprint.** Each reproduces the eleven effects closely. … The pre-registered gate is passed with room to spare." → "**Both arms beat chance.** Their departures from an always-50 predictor correlate with the measured ones at 0.98 (self) and 0.96 (Sam). A predictor that assumes no uptake at all and copies the visible answer also passes this gate (0.81 [0.48, 0.95]), so the gate shows little beyond reading the transcript."
3. "The difference, −0.043, has a 95% interval of [−0.074, +0.043], which includes 0. By the pre-registered rule that is "no detectable self advantage"." → add: "The interval is lopsided because the bootstrap inflates the smaller error more: 82% of resamples favour the self arm, and the basic and BCa intervals are [−0.129, −0.012] and [−0.105, −0.004]. No power check was pre-registered; only a true difference of about 0.08 (nearly all of Sam's error) was detectable with 80% power."
4. "**The two accounts move together:** r = 0.95 [0.82, 0.98] across the eleven effects (the bar was 0.70)." → "r(a, b) on departures from always-50 is 0.95 [0.82, 0.98] (bar 0.70). A no-uptake predictor reaches 0.72 with the self arm on the same statistic, and the two arms' errors correlate at only 0.14, so this shows shared structure, not shared mistakes."
5. "**Where Sam's account goes wrong.** Almost all of the self arm's edge is one effect: commitment to one's own earlier answer." → "… All of the self arm's edge, and more, comes from the three own-answer uptakes (block ΔMAE −0.193 [−0.237, −0.016], exploratory); on other-person uptake the self arm is worse (+0.034), and on order and repeat effects they tie (+0.001)."
6. "Exploratory: Sam is predicted to repeat the shown number exactly 60% of the time, the self arm 41%." → "Exploratory: Sam is predicted to repeat the shown number within ±1 point 60% of the time, the self arm 41%; the model actually did so 44% of the time (exactly: 49% and 32%)."
7. "So the model can *simulate* its own behaviour well when it is shown the situation. When asked *why*, it gives a theory that is wrong in the same way for itself and for Sam. That is Nisbett and Wilson's 1977 pattern, in a language model: …" → "Over six condition means (secondary; item-bootstrap CIs (a) [−0.98, −0.75], (b) [−0.98, −0.83]) the causal reports run opposite to the measured uptake. The design cannot separate a wrong causal theory from a reading of the scale as absolute change, and a third of the self arm's reports are 0. This resembles Nisbett and Wilson's pattern in this model, though here the observer reads the whole transcript, not a one-line description."
8. "The interpersonal test, Bem's and Nisbett and Wilson's, comes out on this model the way it came out in people. Given the same transcript, the model predicts "Sam" nearly as well as itself, and its causal self-reports are no better than its reports about Sam. Both are wrong." → "The interpersonal test does not decide on this model. The self arm's error is about half of Sam's, and the label changes the predicted own-answer uptake by −0.21 [−0.28, −0.14]. The causal reports are equally wrong in both arms."
9. "This fits program 1's F5 (no privileged self-knowledge), now measured against the model's own behavioural fingerprint rather than against its errors." → delete, or "It neither confirms nor contradicts program 1's F5."
10. "It is the first wave result that supports the seed hypothesis: the account of self and the account of another assistant look like one operation run on the same transcript." → delete.
11. "Eleven effects are few, which is why the error-difference interval is wide." → "The interval's width comes from resampling 16 and 40 items. No power check was pre-registered, although the map's standing rule requires one for a self/other null."
12. "The engine gave 60; this was a hit, **pass, unreplicated**." → "The engine gave 60. The frozen rule's letter was met; the audited verdict is **null** (om-p2-4)."
13. "**Primary verdict (§5): pass.**" → "**Primary verdict (§5): pass by the frozen code; null after audit (percentile-interval bias, no power check; see audit).**"
14. "Leave-one-effect-out: ΔMAE ranges from −0.062 to −0.023, and r(a, b) from 0.904 to 0.941. No single effect decides it." → "… and r(a, b) on departures from always-50 from 0.907 to 0.965 (the 0.904–0.941 first reported was the raw-effect r, which D3 rules invalid). Every deletion leaves ΔMAE negative."

## What would break it next

The cheapest test that could overturn the null in either direction costs about **$0.15**: 1,920 Haiku calls. Re-run arms (a) and (b) on the 192 own-source U cells only, with 10 repeats instead of 5. Pre-register the **own-uptake block ΔMAE** as the primary, with a BCa interval, an equivalence margin (for example |ΔMAE| < 0.05), and a power simulation built from this run's error structure. If the self advantage on own-answer commitment (−0.193 here, exploratory) replicates outside the margin, the bet fails. If it falls inside the margin, the null becomes a real equivalence. Invariant 7 still requires a second model: Sonnet predicting its own archived `mm-gm2-sonnet` conversations (O and RA only, about 3,200 calls, est. $2–3, above this program's per-bet caps; needs approval).

---
Scripts (no network; Python `-I`; program 1 archives read-only):
- `/private/tmp/claude-501/-Users-seanpharris-entangled-mind-audit2/bb46787f-112b-4a3c-a1e9-dd87d67b2c75/scratchpad/om-p2-4/work/run_authors.py` runs the authors' `analyse()` on a copy with sockets and the client patched to raise. The output is byte-identical to the committed `results/p2-4-interpersonal.json`.
- `…/work/indep.py` recomputes the effects, MAE, ΔMAE, r, gate, bootstrap, basic/BCa intervals, leave-one-item-out, leave-one-effect-out and other seeds with independent code. Output: `…/work/indep_out.txt`.
- `…/work/attack.py` covers the detection boundary, the know-nothing predictors, random predictors, causal-report CIs and the exploratory numbers. Output: `…/work/attack_out.txt`.
- `…/work/blocks.py` gives the unpooled block ΔMAE, the label gap, signed errors and floor/ceiling shares. Output: `…/work/blocks_out.txt`.
