---
bet: ng-p3-5c
program: nature-graded
prereg_commit: 930efe8
reviewer_session: design-review ng-p3-5c (fresh subagent session, launched by the oversight-testbed session)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-04 18:20 America/Denver
checks: {D1: flaw, D2: holds, D3: holds, D4: flaw, D5: flaw, D6: holds, D7: flaw, D8: flaw, D9: flaw, D10: holds}
flaws: 7
pilot_usd: 0.00
verdict: fix-first
confirmed_at: null
---

# Design review of ng-p3-5c

## In plain English

As built, the test fixes both of the original P3-5's construction faults. The job's T1/T2 really reach the simulator now. Both kinds of error sit in one model, so neither can win just because the other was left out. On synthetic data built from the three real simulator states, it labels every in-family truth correctly: blur only, steering only, both, and neither. But it has a blind spot that matters for this chip. The "blur" family contains only random flips and uniform mixing. It has no energy decay (the T1 kind, where an excited qubit relaxes to 0), and that is the most expected incoherent error on a superconducting chip. When the synthetic truth is 3% extra decay per qubit and nothing else, the steering test fires falsely in 12–38% of draws. One full run labels a pure-decay pair "steering only". Adding two decay knobs to the blur family brings the false steering rate to 0 in 24 draws. Six smaller fixes follow:
- a bootstrap too small for the Bonferroni line it promises;
- a dry run on a reference state on which the ZZ knob does nothing;
- verdict sentences that say "the chip's errors" where the design can only say "this model's terms";
- an undefined spectator rule;
- no rule for a label that rests on one setting;
- a "comparison with P3-5" that differs from P3-5 in two ways.

None changes the question, so the verdict is **fix first**.

## What an unscored re-analysis of a twice-analysed archive can claim

This archive's counts have been fitted by P3-5 and twice by its auditor. The auditor's in-sample nested fits (+22, +89, +116 logL for steering given blur) are quoted in the pre-registration itself, and the pre-registration predicts "both present" (§1). So this is not a blind test, and it cannot add evidence in the sense a bet does. What freezing it in advance does buy is real: the model, the starts, the null, the threshold and the sentences were all fixed before this code saw the counts. Neither the author nor the result can tune them. The fair claim is "a pre-specified procedure, run on data whose rough answer was already known, gives labels X". It is not "a test confirmed X". The §5 sentences must say this (F4). Not scoring it and stating no odds is correct.

The two pre-data changes in D10 (bounded blur probabilities; CV demoted) were made on synthetic data only, as far as the record shows. `synthetic()` builds its own state and assignment matrix and opens no archive. `p3_5c_fits.py` first appears in 930efe8 with the pre-registration. No `results/p3-5c*` file exists. The record contains no nested CV on the real counts, so the author could not have chosen to demote CV after seeing it fail on the real data. The auditor's 7-v-7 CV on the real data (−79.8, −224.0, +31.9) is about a different model. *Cannot check:* what was run outside the record before 930efe8.

Demoting CV hides nothing that the CV would have caught; on the real reference states it agrees with the LR test (see D4). But D10's stated reason does not hold up (F3).

## Checks

All runs are offline, with `/Users/seanpharris/entangled-mind/.venv/bin/python` (qiskit 2.6.1, qiskit-aer 0.18.2, qiskit-ibm-runtime 0.51.0, numpy 2.5.4, scipy 1.18.1).
- Every script imports a guard first (`guard.py`). The guard replaces `dotenv` with a stub, so `p3sim`'s import-time `.env` load reads nothing, and it makes socket connect and getaddrinfo raise.
- No IBM call, no hardware, no paid call. `--run` was not run.
- The archived **circuits** (`window/data/hardware/dbl6e1d8mdtc73d5gesg-*.json`, field `gates` only, via `p3sim.load_isa`) were read to build the three real reference states ρ_ref, as `reference_states_fixed` does. No hardware **counts** and no assignment matrix were read. Synthetic counts use the author's synthetic assignment matrix.
- Scripts and outputs are in `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/19f84df9-a6ff-48ba-89d6-d3f43e5d1747/scratchpad/rv/`: `d2_t1t2.py`, `d2_knobs.py`, `d2_spect.py`, `exp1.py` (the pre-registered `analyse_item`, B = 100, on known truths), `exp2.py` / `an2.py` (calibration and power) and `exp3.py` (amplitude damping, and the fix).
- The pre-registration at 930efe8 matches the current file except the seed line filled in by 03356ad. `p3_5c_fits.py` and `p3sim.py` are unchanged since 930efe8 (`git log`).
- The author's `data/p3-5c-synthetic-B100.json` (a6ca8a1, 17:56) is committed and was checked (D4).

### D1. The rule can be applied by a stranger: **flaw** (F5)

The per-item rule is mechanical: two bootstrap p-values, each "present" iff p < 0.01. That gives four classes, plus "untestable" for a non-finite likelihood or no ρ_ref. I applied it to the 18 synthetic results tables from `exp1.py` and to the author's four. Each gave exactly one class, and `analyse_item`'s labels agree with §5. The overall reading (a count per class, and never "blur, not steering" unless every pair says so) is unambiguous.

The spectator add-on is not. §5 says: "If the spectator check shows spectator steering absorbed as blur, add …". The code returns only `spectator_steering_detected_as_coherent = LR_c > q99(null_c)`, and "absorbed as blur" is defined nowhere. A stranger given `False` has three readings: absorbed as blur, absorbed by nothing, or too small to see. Only one licenses the sentence. The comparison is also made on one synthetic draw. → F5.

### D2. Every manipulation takes effect: **holds**

- **T1/T2** (`d2_t1t2.py`). `overwrite_calibration(..., legacy_t1t2_bug=False)` writes the snapshot values. Its own assertion passes, and so does the extra T2 assertion in `reference_states_fixed`. They reach the simulator: Aer's delay-relaxation pass carries T1(q9) = 147.1 µs, T1(q37) = 115.0 µs and T2(q9) = 33.3 µs (snapshot values). The legacy path carries FakeFez's 247.0, 221.9 and 53.9. The sx error channel on q9 differs too (3 against 12 circuit terms). The reference states move: trace distance fixed v legacy is 0.0009 (h221), 0.0080 (h088) and 0.0129 (h268). Purity fixed v legacy: 0.9838 v 0.9842, 0.6102 v 0.6139, 0.7053 v 0.7190. Small, but nonzero and in the expected direction (shorter T1/T2, more mixed).
- **Coherent and incoherent knobs** (`d2_knobs.py`). On the author's synthetic reference, each of the 14 knobs moves logL at +0.02 and +0.1, **except φ_ZZ, which moves it by exactly 0.00**. The author's ψ = 0.78|00⟩ − 0.63|11⟩ and its Pauli-blurred mixture commute with ZZ, so a final ZZ phase is a global phase there. The local Z rotations on the two qubits are also interchangeable there (a_i, c_i, a_j, c_j all give −1.06 at +0.02). On the **real** reference states the ZZ knob is live: ‖[ρ_ref, ZZ]‖ = 1.40, 0.80 and 1.10, and steering truths with φ = 0.15 are recovered (D4). So the manipulation works where it will be used, but the dry run cited in §2 did not exercise it. → F3.
- **Nesting.** `fam_full(θ_coh, 0) == fam_coherent(θ_coh)` and `fam_full(0, θ_inc) == fam_inc(θ_inc)` hold to machine precision. The coherent family leaves purity unchanged (0.8677 → 0.8677) and the incoherent family lowers it (→ 0.5964), as intended. The warm starts `[fc.x, 0]` and `[0, fi.x]` guarantee logL_full ≥ max(logL_coh, logL_inc). No negative LR occurred in any of more than 5,000 fits.
- **Spectator ZZ** (`d2_spect.py`, circuits only). The 0.1 rad ZZ composes onto 344 noise-model CZ pairs. 122 (h088) and 167 (h268) spectator CZ gates in the XX circuit actually receive it. It moves the pair's state by trace distance 0.0087 (h088) and 0.0372 (h268); at 0.5 rad, by 0.0122 and 0.0905. It takes effect. On h088 the effect is small enough that "not detected" is a live outcome, which is why F5 needs an "invisible" branch.
- **Parameters the run will use.** B = 100, α = 0.01, 1 zero start + 10 random starts + warm starts per fit, and 2 random starts + warm starts per bootstrap refit. The bounds are [0, 0.25] ×6 and [0, 0.5], and the seed32 is 1446222194. All match §2 and §4.

### D3. Every control can fail: **holds**

The controls are the bootstrap nulls and the "neither" synthetic truth.
- Wrong set-ups the rule must reject:
  - "steering" when the truth is blur only: rejected on all 3 real states (LR_c 6.5, 7.4, 4.6; p 0.30, 0.31, 0.78) and on the author's state (p 0.53);
  - "blur" when the truth is steering only: rejected on all 3 (p 0.49, 0.10, 0.12) and on the author's (0.63);
  - anything when the truth is "neither": rejected on all 4 (p ≥ 0.069).
- The spectator check can fail: its manipulation moves the state (D2).
- The design has no control on the real data that could show ρ_ref itself is wrong. That is a scope limit, which §6 states, not a control that cannot fail.

### D4. Rivals are matched: **flaw** (F1, F3)

**Recovery inside the families** (`exp1.py`: the pre-registered `analyse_item`, B = 100, CV included; one draw per cell; 4,000 shots × 9 settings; truths from the author's parameter vectors; references = the three real ρ_ref):

| truth | h221: steering / blur | h088: steering / blur | h268: steering / blur | correct? |
|---|---|---|---|---|
| neither | n.d. (6.2, p .30) / n.d. (0.7, .41) | n.d. (11.3, .069) / n.d. (4.9, .069) | n.d. (6.0, .48) / n.d. (2.3, .30) | 3/3 |
| blur only | n.d. (6.5, .30) / **present** (1742) | n.d. (7.4, .31) / **present** (639) | n.d. (4.6, .78) / **present** (919) | 3/3 |
| steering only | **present** (897) / n.d. (1.0, .49) | **present** (260) / n.d. (3.4, .10) | **present** (376) / n.d. (3.1, .12) | 3/3 |
| both | **present** (253) / **present** (1872) | **present** (128) / **present** (601) | **present** (166) / **present** (842) | 3/3 |
| XX rotation 0.15 rad (coherent, outside the family) | **present** (235) / n.d. | **present** (65) / n.d. | **present** (88) / n.d. | 3/3, right kind |
| **amplitude damping γ = 0.03 per qubit (incoherent, outside the family)** | n.d. (13.5, .059) / **present** (19.0, .0099) | **present (20.2, .0099)** / n.d. (3.3, .17) | n.d. (17.3, .020) / n.d. (3.0, .21) | **1/3** |

(n.d. = not detected; numbers are LR, bootstrap p; p = .0099 is the floor 1/101.)

The author's B = 100 file (a6ca8a1) reproduces the in-family result on the author's state. All four truths are labelled correctly there, and the 7-v-7 ΔlogL calls the "both" truth "blur better by 860". That is a clean demonstration of the original P3-5 flaw, which the nesting removes. Within the two families, neither wins by construction. The coherent family can no longer lose just for being unable to blur, and the blur family is not credited for steering. That part holds.

**The flaw (F1).** A non-unital incoherent error is outside both families: amplitude damping, i.e. T1 decay beyond what the simulator already has. A local rotation can partly imitate it, by turning the Bloch vector toward |0⟩. Uniform Pauli blur cannot, because it only shrinks the Bloch vector. So on h088, 3% extra decay per qubit comes out **"steering only"**. Over 8 draws per state (`exp3.py`, LR_c against χ²₇'s 99th point, 18.5, which is close to the bootstrap nulls' 99th percentiles of 11.8–20.3):

| state | γ = 0.01: steering falsely flagged | γ = 0.03: steering falsely flagged | γ = 0.03, with 2 damping knobs added to the blur family | blur only (control), with damping knobs |
|---|---|---|---|---|
| h221 | 0/8 | 1/8 (median LR 12.9) | **0/8** (median 2.2) | 0/8 |
| h088 | 0/8 | 3/8 (median 17.7) | **0/8** (median 3.8) | 0/8 |
| h268 | 0/8 | 2/8 (median 15.6) | **0/8** (median 4.9) | 0/8 |

The blur test also mostly misses this decay on h088 and h268 (median LR_i 3.9 and 6.9). Extra decay is not a far-fetched truth for this archive:
- the chip's states are more mixed than the simulator's on all three pairs (ledger/audits/ng-p3-5.md);
- T1 drifts between the calibration snapshot and the job;
- program 3 exists partly because the simulator's T1 handling was wrong once already.

So the test as built can report "steering" for what is decay. The fix keeps the question and tightens the bar for steering: decay goes into the blur family (F1).

**The dry run cited in §2 is not representative (F3).** It used a reference on which φ_ZZ is inert (D2). And the CV figure behind D10's demotion (−13.8 for steering on "both") was one draw: CV does not depend on B, yet the same truth gave +18.7 in the author's B = 100 run. Both runs share one random stream, so the bootstrap draws for the earlier truths shift the "both" counts (LR_c 46.5 at B = 20, 93.0 at B = 100). On the three real states, the CV gain for steering in "both" is +84.5, +65.9 and +69.1. It is negative on every blur-only truth (−6.6, −10.4, −7.7) and positive on every steering-only truth (+490, +125, +184). CV does not systematically penalise the 14-knob model when steering is present. The demotion is still harmless: CV agreed with the LR on all 18 cells I ran, including the false damping call on h088 (+5.5), so it would not have caught F1 either. But D10 records a reason that does not hold, and the author offers the flip as support for it. A flip of sign between two draws of the same truth shows that CV is noisy. It does not show that CV is biased.

### D5. A dumb baseline is beaten, and the design can see the effect: **flaw** (F2)

- **Dumb baseline.** The dumbest output is the label "both present on every pair", which the pre-registration itself predicts. The test does not produce it by default. It returns single-kind and "neither" labels on the matching synthetic truths (D3, D4).
- **Calibration** (`exp2.py`; true null = 60 datasets drawn at the true parameters, fitted exactly as the observed data are; compared with the bootstrap null the code builds from a fitted state):

| state, test | true null: 95th / 99th / max | code's bootstrap null (one fitted state, B = 100): 95th / 99th / max | true-null LRs above that bootstrap's max |
|---|---|---|---|
| h088, steering given blur (blur-only truth) | 11.3 / 12.0 / 12.2 | 12.3 / 16.7 / 25.0 | 0/60 (conservative) |
| h088, blur given steering (steering-only truth) | 4.0 / 6.9 / 8.3 | 4.4 / 7.0 / 8.3 | 0/60 |
| h221, steering given blur | 12.0 / 15.3 / 16.1 | 11.4 / 13.5 / 14.4 | 2/60 (slightly narrow) |
| h221, blur given steering | 6.1 / 7.2 / 7.4 | 4.1 / 6.3 / 7.0 | 2/60 (slightly narrow) |

On 11 fresh null datasets per kind on h088, the full pre-registered bootstrap (B = 100 each) gave p < 0.01 in 0/11 and p < 0.05 in 1/11, for both kinds; median p 0.76 and 0.54. The false-positive rate is therefore near nominal: at most a few per cent and indistinguishable from 1% at this sample size. There is one visible imprecision. Each dataset's own "beat all 100" threshold ranged from 16.4 to 27.4 for steering, and from 6.3 to 13.9 for blur. That is bootstrap noise in the threshold, not bias (F2). The pre-mortem's risk (local optima widening the null) did not appear. On 40 null datasets, the bootstrap's cheaper refit (2 random starts plus warm starts) gives LRs within −0.46 to +0.23 of the full 10-start fit.

- **Power** (`exp2.py`, 20 draws per level; detection = LR above the true null's 99th percentile):

| effect added on top of the other kind | size (largest knob) | h088 detected | h221 detected |
|---|---|---|---|
| steering × 0.1 | 0.015 rad | 0.10 | 0.05 |
| steering × 0.2 | 0.03 rad | 0.30 | 0.40 |
| steering × 0.35 | 0.05 rad (φ_ZZ 0.053) | 0.85 | 1.00 |
| steering × 0.5 | 0.075 rad | 1.00 | 1.00 |
| blur × 0.05 | Pauli 0.003, depolarising 0.004 | 0.15 | 0.70 |
| blur × 0.1 | Pauli 0.006, depolarising 0.008 | 0.65 | 1.00 |
| blur × 0.2 | Pauli 0.012, depolarising 0.016 | 1.00 | 1.00 |

So, at 36,000 shots per pair, the design sees steering of about 0.05 rad and blur of about 1% almost surely. Below about 0.03 rad and 0.5%, "not detected" is uninformative. The fitted values P3-5 reported (φ up to 0.086 rad; local Pauli terms 5–10%) are well above both. Power is ample for the question; the sentences must say where it ends (F4).

- **The resolution problem (F2).** With B = 100, the smallest attainable p is 1/101 = 0.0099. So "present" means the observed LR beat all 100 null draws: the effective threshold is the null sample's *maximum*. Across my 18 bootstrap nulls, that maximum for steering-given-blur ranged from 12.7 to 26.1, with the 99th percentiles at 11.8–20.3. A borderline case therefore flips on bootstrap noise. The h088 damping case (LR 20.2 against a null maximum of 17.4) is one. And the secondary "also reported against Bonferroni α = 0.01/6 = 0.0017" can never be met: no p below 0.0099 exists at B = 100. Every result will read "not significant after Bonferroni", whatever the data, which is P6's control that cannot pass. → F2.
- No null-type "no difference" claim is scored, so no equivalence margin is required. But "not detected" will be read as "absent" unless the sentence carries the power. → folded into F4.

### D6. Foreseeable execution risks are piloted: **holds**

The pre-mortem is `design` (local optima widening the null), not `execution`, and there are no paid calls. Its risk was checked directly. Refitting null datasets with the bootstrap's cheaper procedure (2 random starts + warm starts) gave LRs within −0.46 to +0.23 of the full 10-start fit (40 synthetic null datasets on h088 and h221). The bootstrap nulls are not visibly widened or narrowed by the optimiser. Runtime: one `analyse_item` took 280–720 s on a heavily shared laptop, so the run fits the 3-hour budget at B = 100. At F2's B = 1,000 it needs the bootstrap parallelised (≈ 25–40 min on 10 cores, by my timings).

### D7. Comparisons match: **flaw** (F7)

The two primary tests use the same counts, ρ_ref, assignment matrix and fits; only the knobs differ. That holds. The secondary "old 7-v-7 ΔlogL, for comparison with P3-5" does not match P3-5 in two respects besides the T1/T2 fix. Its incoherent family is reparametrised: bounded direct probabilities instead of softmax and sigmoid, with ceilings of 0.25 and 0.5 where P3-5's could reach 1. And its fits use a different start scheme. A difference from P3-5's −43.5, −34.9, +63.0 could not be attributed to the reference fix. → F7.

### D8. The verdict sentences are written: **flaw** (F4)

They are written for every class, which is good, but they use nouns the design cannot carry (P9).
- "On pair <id>, **the chip's errors need** both a steering and a blurring part" names a physical mechanism. What the design measures is "the counts need the 7 rotation-type knobs given the 7 blur-type knobs, beyond this simulator's state". D4 shows a decay error can pass as "steering". §6 concedes the point ("'Present' means 'needed by this 14-knob model on these counts', not a physical mechanism"), but §6 is not what gets quoted.
- "Blurring adds nothing detectable" should carry the power at which it was checked: about 1% blur and about 0.05 rad steering are detected almost surely, and below 0.5% and 0.03 rad they mostly are not (D5).
- None of the sentences says that the archive was analysed before and the answer was anticipated.
- With 36,000 shots, a misfit outside both families shows up as one or both terms being "needed". The real data's full model is likely still well short of saturated: P3-5's best family was 28–121 below saturated, and the audit's joint fits recovered only part of that. No sentence covers "both needed, and still misfitting".

→ F4.

### D9. One item cannot decide it: **flaw** (F6)

Across pairs, the design is sound: per-pair labels are reported separately, and the overall reading is a count that may not be pooled into "blur, not steering". Within a pair, P3-5's h088 margin rested on one setting (XX) and flipped when XX was dropped (ng-p3-5 audit, B7). §4 says the CV table "makes this visible". But CV is a held-out quantity on a different scale from the primary in-sample LR. Nothing pre-registers either the per-setting share of LR_c and LR_i, or what happens to a label when one setting carries it. → F6.

### D10. Machinery: **holds** (with two notes)

- **Budget:** $0 and no network. The script makes no network call: FakeFez is offline, and it ran with sockets blocked.
- **Stop-on-refusal and scale direction:** n/a.
- **Caching:** n/a (deterministic local fits).
- **Seed:** recomputes. `ledger/seed.py 27bba9e6… ng-p3-5c --purpose boot` gives 10131417812182473074 and seed32 1446222194, which match `data/p3-5c-seed.json` and §2. Pulse 1591496 is at 00:32:00.187Z; the commit is at 00:31:33Z and the previous pulse (1591495) at 00:31:00.197Z, so it is the first pulse after the commit. `run()` seeds one `default_rng` from it and uses no other seed. *Cannot check:* the pulse against the public beacon (no network fetch made), and `certificate_verified` is false.
- **Lesson line:** `ledger/check_prereg.py ng-p3-5c … --before-run` gives L1, L2 and L3 ok (R1 failed only because this file did not exist yet). The cited patterns' `do_this` are in the design: P5 by the nesting (but see F1), and P4 by the assertion and this review's D2.
- **Gate:** `--run` refuses without the seed file and without `verdict: go` or a fix-first with `confirmed_at` set (`design_review_go()`; it will read this header as no-go until confirmed).
- Note 1: `run()` does not call `check_prereg.py --before-run`, as ng-p3-15's `submit()` now does (D15). It would also check that this review is committed. Recommended.
- Note 2: importing `p3sim` loads the IBM token from `/Users/seanpharris/entangled-mind/.env` into the process environment, although this analysis is offline and §7 says it "reads only local archives". Nothing uses the token here. Making the load lazy (only in `live_backend()`) would make the $0 posture true by construction. Recommended, not required.

## Required fixes

Each needs a dated DEVIATIONS row in `programs/nature-graded/DEVIATIONS.md`, written before `--run` and naming this review. Suggested rows are D16–D22, or one row per fix, as the program prefers. None lowers a bar.

**F1 (D4). Put decay in the blur family.** Add two amplitude-damping knobs γ_i, γ_j ∈ [0, 0.2] to the incoherent family, applied before the Pauli and depolarising terms: inc has 9 knobs, full has 16. LR_c = 2(logL_full16 − logL_inc9) and LR_i = 2(logL_full16 − logL_coh). Bootstrap nulls as before, from the fitted inc9 and coh states. Before `--run`, rerun the synthetic recovery on the **three real ρ_ref** with the six truths in the D4 table (including γ = 0.03 decay) and commit the output; decay must come out "blur", not "steering". Report the 14-knob version as a secondary, for continuity with the pre-registration as frozen. (`exp3.py`'s `inc9` / `full16` is a working sketch: the false steering rate under γ = 0.03 goes from 6/24 to 0/24, and the blur-only control is unchanged.)

**F2 (D5). Bootstrap resolution.** Set B = 1,000 per test, parallelised across items or draws. The smallest p is then 0.001 < 0.0017, so the Bonferroni line can be met, and the "present" threshold becomes a 99.9th-percentile estimate rather than the maximum of 100 draws. If laptop time forbids that: keep B = 100, extend to B = 1,000 for any test with p ≤ 0.05, and pre-register the extension rule. Either way, state the floor 1/(B+1) beside every p.

**F3 (D4/D2). Correct the dry-run record.** In the DEVIATIONS row, restate D10's reason for demoting CV. Drop "CV penalises the 14-knob model when steering is present". Say instead that CV is a noisy single-draw quantity: −13.8 and +18.7 on two draws of the same truth, and +84.5, +65.9, +69.1 on the real reference states. Note that the §2 dry run's reference is a ZZ eigenstate, on which φ_ZZ is inert, and replace it as the D4 evidence with F1's run on the real ρ_ref. Keep CV as a reported secondary, and add a sentence for disagreement: "On pair <id>, the <kind> term improves the in-sample fit (p = …) but not the prediction of a held-out setting (CV gain …); read the label as weaker."

**F4 (D8, P9). Verdict sentences with nouns the design carries.** Replace the §5 sentences with these:
- both: "On pair <id>, the counts need both a rotation-type term (local rotations and a ZZ phase) and a blur-type term (random Pauli flips, uniform mixing and energy decay) beyond the simulator's state; neither alone fits as well."
- rotation only: "On pair <id>, a rotation-type term is needed; once rotations are allowed, a blur-type term adds nothing this test could detect (in synthetic checks it detects blur of about 1% almost surely and misses most blur below 0.5%)."
- blur only: the mirror image.
- neither: "On pair <id>, neither term is detectably needed beyond the simulator's state."
- Append to every per-pair sentence: "These are terms in a 16-knob model fitted to these counts, not identified physical mechanisms."
- Append once, to the overall reading: "This re-analysis was specified before it ran, but the archive had already been analysed by this program and its auditor, who saw both kinds of term on every pair; it is not a blind test."
- Add a goodness-of-fit sentence. Report the full model's deviance against the saturated likelihood (13 df at 14 knobs, 11 at 16). If it exceeds its χ² 99th percentile, add: "Even both terms together leave a misfit the model cannot explain (deviance … on … df), so part of what each term absorbs may be neither kind."
- Fill the power blanks from F1's synthetic run.

**F5 (D1). Define the spectator outcomes.** Using that item's real-data bootstrap nulls (q99 of null_c and of null_i), the spectator check reports exactly one outcome:
- **detected as rotation:** LR_c > q99(null_c);
- **absorbed as blur:** LR_c ≤ q99(null_c) and LR_i > q99(null_i);
- **invisible:** neither.

Only "absorbed as blur" triggers the §5 add-on. "Invisible" adds: "At 0.1 rad, spectator rotations were too small to see on this pair, so this check cannot rule them out." Run 20 synthetic draws, not one, and report the share of each outcome. Report the trace distance between the spectator-ZZ pair state and ρ_ref (this review measured 0.009 on h088 and 0.037 on h268).

**F6 (D9, P10). One setting.** For each "present" label, report each setting's contribution to LR_c and LR_i at the fitted optima. Pre-register: "If one setting contributes more than half of an LR labelled present, the sentence adds 'This rests mostly on setting <S>.'" Also refit with that setting dropped and report whether the LR still exceeds the same item's null q99 (in-sample, reported, not a gate).

**F7 (D7). Make the P3-5 comparison attributable.** Report the 7-v-7 ΔlogL three ways:
- P3-5's own families (`p3_5_fits.fam_incoherent`, softmax and sigmoid, `fit()`'s starts) on the **legacy** ρ_ref, which should reproduce −43.5, −34.9, +63.0;
- the same on the **fixed** ρ_ref (isolating the T1/T2 fix);
- the new bounded family on the fixed ρ_ref (isolating the reparametrisation).

Label each line with what differs.

After the fixes, this reviewer confirms them in an addendum and sets `confirmed_at`. Only then does `--run` unlock.
