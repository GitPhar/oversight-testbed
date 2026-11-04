---
bet: ng-p3-1
program: nature-graded (program 3)
prereg_commit: bbd6348
results_commit: 280e180
auditor_session: audit2 worktree, subagent audit of ng-p3-1 (clean copy of 280e180 in scratchpad ng-p3-1/repo; checked byte-identical to `git archive 280e180`)
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5 (bbd6348, 593f8fd and 280e180 all carry "Co-Authored-By: Claude Opus 5.5")
same_model_family: true
date: 2026-11-04 15:50 America/Denver
claims_checked: 32
holes_found: 9
overclaims_cut: 15
reproduced: true
verdict_claimed: null            # the pre-registered label is "fail" (§5.2: control in band, scheduled < 0.40); the template has no "fail", so it is entered as null = predicted event absent
verdict_after_audit: null        # "fail" stands, including on a corrected re-run; the model that produced it is not the pre-registered model, and three explanations attached to it do not stand
verdict_stands: true
canary: unknown
false_alarms: 0
failed: true
failure_reason: Idle relaxation over a 9.6 µs circuit is negligible against T1/T2 of about 45–200 µs, so ALAP scheduling moves P(yes) by about 0.000 (−0.0004 at 4M shots); this omission is not the gap. Kind world.
failure_kind: world
premortem_score: named
risk_seen: null
---

# Audit of ng-p3-1: Does a correctly scheduled noise model close the Stage 1 gap?

## In plain English

The verdict stands. Laying the circuit out in time does not bring the simulator anywhere near the chip. The simulator says about 27% "yes" with or without the fix, and the pass mark was 40%. The run regenerates byte for byte from the frozen code and the beacon seed.

But the simulator did not do everything the write-up says it did. It never loaded the chip's T1 and T2 from that afternoon: a silent bug left in place the 2025 snapshot values that ship with the library. The "twist on every two-qubit gate" variation (E2) never applied its twist. And the "tripled errors" variation (E3) did not shorten T1 and T2 as its label says. When I fixed the T1/T2 bug, the verdict did not change (control 0.268, scheduled 0.268). E3 came out at 0.288, not 0.277.

The control that was meant to show the rebuild is faithful cannot show it, because a simulator with no noise at all (0.279) also passes it. The "7% of the gap closed" is almost all the gap between our rebuild and program 1's 1,000-shot estimate, not idle decay. Idle decay on its own closes about 0%. The claim that more noise of the modelled kind "pulls answers toward randomness, not toward the chip's pattern" is wrong as stated. Randomness gives exactly the chip's headline 0.50. Scaling the modelled noise ×10 gives 0.44, and every step brings the per-qubit pattern closer to the chip's.

The scheduled model is pre-registered to become the program's "corrected simulator". It must not be used for P3-2 and later predictions until the T1/T2 and ZZ bugs are fixed.

## The case that this result is false

*(Written before the checklist.)* The headline is "fail: the gap is not our set-up". The case against it runs as follows. The result is a single 9-qubit circuit for a single item, simulated with a model that only the author has checked against its own spec. The pass/fail number rests on `p3sim.overwrite_calibration` doing what the pre-registration says: writing the job-time T1, T2, readout, sx/x and CZ numbers into FakeFez. Nothing in the record tests that it did. The control, "the rebuild lands within ±0.03 of the archived 0.251", is weak. The archived value has a 1,000-shot SE of 0.014, and the band is wide enough that almost any model of this circuit might land in it, perhaps even no noise at all.

The primary effect is a difference of +0.0008 between two runs that share one seed. That is nothing, whatever its sign. The "7% gap closed" may be mostly reconstruction offset (0.267 vs 0.251) given a causal label ("idle decay closes 7%"). The exploratory variations offered as "pointing the same way" may be just as fragile. A 0.1 rad ZZ added by `add_all_qubit_quantum_error` to a noise model that already has a local error on every CZ may never fire. And "errors ×3" is one point on a curve whose shape the write-up then generalises ("pulls answers toward randomness").

If the model is mis-built, then "the gap is not our set-up" is the one sentence the run cannot support. A mis-built simulator is exactly "our set-up". The strongest version of the case: the verdict number might survive while every explanatory sentence around it is an artefact. And the program then adopts that mis-built model as its "corrected simulator" for later bets.

The checklist below confirms most of this case for the explanations and the adopted model, but not for the verdict.

## Claims checked

| # | claim (quoted or paraphrased) | check run | outcome |
|---|---|---|---|
| 1 | Verdict fail: control 0.267 in [0.221, 0.281], scheduled 0.268 < 0.40 | frozen script re-run offline (`work/run1`), `cmp` to archive | holds: JSON byte-identical (sha256 ab4c4735…a88e) |
| 2 | Same verdict with the model actually built as pre-registered | `work/scripts/corrected_run.py` | holds: control 0.26787, scheduled 0.26778 |
| 3 | "rebuilt the exact circuit the chip ran" | sha256 of circuit archive; gate counts | holds (a773bd6e…4029 matches; barrier omission disclosed) |
| 4 | "loaded the chip's error rates from that afternoon" | `work/scripts/check_t1t2_zz.py` | **hole**: T1/T2 never overwritten (FakeFez 2025-02-26 values used) |
| 5 | "simulated it again 100,000 times" | JSON shot totals | holds |
| 6 | "The fix makes almost no difference" | 10-seed rerun, 4M-shot run | holds: diff −0.00017 ± 0.00104 (SD over 10 seeds) |
| 7 | "corrected simulator says 26.8%" | reproduction | holds (0.26791) |
| 8 | "rebuild says 26.7%, reproduces program 1's 25.1% within tolerance" | reproduction | holds (0.26712) |
| 9 | "so the rebuild is faithful" | noiseless and one-channel models through the control (`variance_and_alternatives.py`) | **hole**: noiseless 0.279 and readout-only 0.276 also pass; the bugged model passed |
| 10 | "circuit lasts under 10 millionths of a second" | JSON `circuit_duration_s` | holds (9.612 µs) |
| 11 | "qubits keep their state for 90 to 200 millionths of a second" | snapshot; target values | **hole** (minor): snapshot T2 goes down to 44.6 µs; the sim used FakeFez T1 95.6–177.1, T2 49.2–144.8 |
| 12 | "There isn't enough waiting for decay to matter" | corrected run; toy positive control | holds (delays do decay: toy q87 0.305 vs expected 0.298) |
| 13 | "So the gap is not our set-up." / title "the simulator was not just set up wrong" | prereg §6; claims 4, 15, 16 | **hole**: tests one omission; the set-up has two other bugs |
| 14 | "Either the chip's errors were larger … or of a kind the simulator does not model" | prereg §6 | part of hole 13 (false dichotomy: other set-up differences untested) |
| 15 | E2: "small systematic twist … changes nothing (26.7%)" | zz = 0, 0.1, 1.0 rad, same seed (`corrected_run.py`) | **hole**: counts identical for all three; ZZ never applied |
| 16 | E3: "every error ×3, T1 and T2 ÷3 … only reaches 27.7%" | `check_t1t2_zz.py`, `corrected_run.py` | **hole**: T1/T2 ÷3 not applied; with it, 0.288 |
| 17 | ×3 is "about what published work says such models need on this chip family" | scout's Vezvaee 2025 summary (map/reads/d-device-physics.md) | cannot check primary source (no network); the scout summary gives χ 3.6–4.0 without DD, 2.3–2.5 with DD, and says ibm_fez underperformed and was not shown |
| 18 | "turning up noise of the modelled kind pulls answers toward randomness, not toward the chip's pattern" | real-scale sweep ×1–×40; uniform distribution | **hole**: ×10 gives 0.443, ×20 0.541; the L1 distance to the hardware marginals falls 1.52 → 0.56; uniform gives P(yes) 0.500 |
| 19 | q125 moved most (0.75 → 0.30) and has the worst T2 (44.6 vs 86–191 µs) | `tables.py` | holds |
| 20 | "noticed after the data, so it is a lead, not a finding" | — | holds (correctly ranked) |
| 21 | "This scheduled model is now the program's corrected simulator, and every later program-3 prediction uses it" | prereg §4, D1 | adoption is pre-registered (holds as a rule); the code adopted does not implement its spec (claim 4, 15): cut to conditional |
| 22 | Primary table (0.294, 0.251, 0.267 ± 0.0014, 0.268 ± 0.0014, 0.502 ± 0.016, 87 delays) | `tables.py` | holds |
| 23 | Per-qubit table, all 54 cells | `tables.py` | holds |
| 24 | "Every simulator variant stays within about 0.1 of ideal on every qubit" | `tables.py` | holds (max 0.108, E3 q123) |
| 25 | "The hardware drops by 0.12 to 0.45 on eight of nine" | `tables.py` | **hole**: drops on 8 of 9 range 0.078–0.446; only 7 of 9 lie in 0.12–0.45 (q143 drops 0.08) |
| 26 | Gap closed (0.268 − 0.251)/(0.502 − 0.251) = 7% | `tables.py` | holds as arithmetic (0.0674), pre-registered reported quantity (§5.4); but see 27 |
| 27 | Commit message: "idle decay closes 7% of the Stage 1 gap" | `tables.py`, 4M-shot run | **hole**: 95.3% of the 7% is the control-vs-archive offset; scheduling alone is (s − c)/(hw − c) = 0.3% at the frozen seed, −0.2% at 4M shots |
| 28 | "scheduled-minus-control difference is +0.001" | 10 seeds | **hole** (B10): reported without uncertainty; sign flips across seeds (SD 0.00104) |
| 29 | E1 not run, stated in prereg | prereg §3 | holds |
| 30 | Seed: CURBy-RNG pulse 1591379 at 15:35, seed32 1158620522 | `ledger/seed.py` | holds (recomputes); beacon authenticity cannot check |
| 31 | $0, 0 QPU s, no network | run with socket blocked | holds |
| 32 | Pre-mortem quote and "That was the pre-mortem's guess" | prereg §0 | holds |

## Checklist

**A1. Pre-registration predates the run.** *Holds,* with one part that cannot be checked. Author dates: bbd6348 15:34:03, 593f8fd 15:35:28, 280e180 15:36:41 (author = committer in the original repo). The script refuses to run without `data/p3-1-seed.json`, which first appears in 593f8fd. The run takes 22 s wall time on this laptop (`time … nonet.py run1/experiments/p3_1_scheduled.py`), which fits the 73 s window. Cannot check: whether any simulation of the archived circuit ran before bbd6348. The prereg says only a structure check and a toy check did, and neither is archived. I did not read the working tree's file timestamps (outside the permitted git reads).

**A2. Rules match word for word.** The pass rule, statistic, control band, shots, seed and budget hold: `PASS_AT = 0.40`, `CONTROL_TARGET, CONTROL_TOL = 0.251, 0.03`, `SHOTS = 100_000`, `SHOTS_EXPLORATORY = 20_000` at bbd6348, and the code at 280e180 equals the code at bbd6348 for every file the run used. `diff -r` of `git archive` trees shows only `data/p3-1-seed.json`, `experiments/seed_commit.py` and the filled beacon line added. **Hole** on the model: §2 says "T1, T2 … are overwritten with the job-time snapshot", and the run did not do this (B9, hole 1). No DEVIATIONS row records it; DEVIATIONS has D0 and D1 only.

**A3. Bar not lowered.** *Holds.* The 0.40 and 0.251 ± 0.03 thresholds are in code at bbd6348. 0.251 and 0.502 come from `entangled-mind/results/stage1-run-1.json` (`arms.noisy_sim.readout.p_yes` = 0.25100000000000017, `arms.hardware.readout.p_yes` = 0.5020000000000003; sha256 d4b86572…278f), last changed 2026-11-03 21:03 (2a03f81). They were published in `stage1-run-1.md` before the prereg.

**A4. Primary is the pre-registered primary.** *Holds.* Scheduled P(yes) at 100,000 shots.

**B5. Ties.** *Holds.* The readout counts magnetisation-0 shots as ½. The tie mass is 0.0 in all four runs (`work/scripts/ties_and_toy.py`).

**B6. Pooling.** *Holds / not applicable.* One circuit, one item, nothing pooled.

**B7. Few items.** *Not applicable as a re-analysis,* since n = 1 item (q01). Stated as a scope limit under C13.

**B8. Circular estimators.** *Holds.* Nothing is fitted.

**B9. Baselines and controls.** **Hole (three parts).**
- *(a) The model is not the pre-registered model.* `overwrite_calibration` sets `t.qubit_properties[i] = QubitProperties(...)`. In qiskit 2.6.1, `Target.qubit_properties` returns a new list on every access (`… is …` → False), so the assignment is discarded. Every qubit keeps FakeFez's 2025-02-26 T1/T2. For example, q117 has T1 177.1 µs in the run against 87.6 µs in the snapshot, and q125 has T2 49.2 against 44.6. Scale = 3 also leaves T1/T2 untouched (`work/scripts/check_t1t2_zz.py`). Readout, sx/x and all 11 directed CZ pairs used *were* overwritten (`work/scripts/check_model.py`). With T1/T2 actually written in (`work/scripts/corrected_run.py`, same seed and shots), control is 0.26787 and scheduled 0.26778, so the verdict is unchanged.
- *(b) The control cannot detect a broken model.* At the frozen seed and 100,000 shots (`work/scripts/variance_and_alternatives.py`), the results are: noiseless 0.27871, readout-only 0.27639, relaxation-only 0.26975, depolarising-only 0.26862, full 0.26791. All of these lie inside [0.221, 0.281]. A simulator with no noise passes the "faithful reconstruction" test, and so did the bugged one.
- *(c) Does the manipulation bite?* Yes, mechanically. The Aer `RelaxationNoisePass` puts 87 `quantum_channel`s on the 87 delays. Per-qubit idle time runs from 1.5 µs (q143) to 7.7 µs (q117). A toy X–9.6 µs–measure circuit through `p3sim.simulator` decays as expected: q87 (T1 27.1 µs) gives 0.305 against an expected 0.298, and q125 gives 0.075 − 0.021 = 0.054 against 0.056. The prereg's toy "18% decay" names no qubit and is not archived, so it cannot be checked.

**B10. Uncertainty.** **Hole.** Over 10 seeds (the frozen seed plus 1–9), scheduled − control is −0.00017 with SD 0.00104, and its sign flips. The +0.001 is noise. At 4M shots, control is 0.26831 and scheduled 0.26794, so scheduling *lowers* P(yes) by 0.0004. The "7%" carries the archived baseline's 1,000-shot SE of 0.0137, about ±5.5 points of "gap closed", and none is reported. The verdict itself is not near its edge: the gap to 0.40 is about 90 SE.

**B11. Multiple comparisons.** *Holds.* One scored test.

**B12. Leakage.** *Holds.* Nothing is fitted. The hardware marginals were seen by the scout, and this is disclosed.

**C13. Scope drift.** **Hole.** "So the gap is not our set-up" and the title "the simulator was not just set up wrong" generalise from one omission (idle decay) to the whole set-up. The prereg's own §6 says: "It tests one omission … A fail … shows that this omission is not the explanation." The set-up demonstrably has other defects (B9a, C15 E2), and differences the prereg disclosed (FakeFez durations versus IBM's compiler schedule, symmetric readout, x error set to sx error) stay untested. One circuit, one item, one backend snapshot.

**C14. Rank drift.** **Hole.** The single exploratory point E3 (×3), which was mis-built, becomes a general law in "Simply turning up noise of the modelled kind pulls answers toward randomness, not toward the chip's pattern". The "corrected simulator" adoption is *pre-registered* (§4: "whatever the verdict"; D1), so it is not rank drift. But the model being adopted does not implement its own spec, so the adoption has to be conditional on the fix.

**C15. Mechanism drift.** **Hole (two parts).** First, the commit message says "idle decay closes 7% of the Stage 1 gap". 95.3% of that 7% is the control-vs-archive offset (0.26712 − 0.251 = 0.0161, 1.18 archived SE). The idle-decay share is (0.26791 − 0.26712)/(0.502 − 0.26712) = 0.34% at the frozen seed and −0.2% at 4M shots (`work/scripts/tables.py`, `variance_and_alternatives.py`). Second, E2's "changes nothing" is attributed to a ZZ twist that was never applied. `add_all_qubit_quantum_error(…, ["cz"])` adds an all-qubit error, but every CZ pair already has a local error from `from_backend` (352 local cz errors), and Aer applies the local error in preference. Counts at zz = 0, 0.1 and 1.0 rad are identical, dict for dict (`corrected_run.py`: `E2_counts_identical_zz0_vs_0.1: true`, `…_vs_1.0: true`). E2 is simply the scheduled model at 20,000 shots.

**C16. Plain English matches the table.** **Hole.**
- "loaded the chip's error rates from that afternoon": false for T1/T2 (B9a).
- "the qubits keep their state for 90 to 200 millionths of a second": the snapshot has T1 87.6–203.5 µs but T2 44.6–191.1 µs, and the results file's own next paragraph cites 44.6. The sim used neither set.
- "Tripling every error rate … only reaches 27.7%": T1/T2 were not divided by 3. Correctly built, the value is 0.2878.
- "The hardware drops by 0.12 to 0.45 on eight of nine": ideal minus hardware is 0.118, 0.446, 0.281, 0.183, 0.226, 0.159, 0.078, −0.011, 0.181. That is 8 of 9 drops spanning 0.078–0.446, and 7 of 9 in 0.12–0.45.
- "toward randomness, not toward the chip's pattern": the uniform distribution's P(yes) is exactly 0.500, against the chip's 0.502. In the T1/T2-correct sweep, P(yes) at ×1/3/5/10/20/40 is 0.266/0.290/0.337/0.443/0.541/0.565, and the L1 distance from the hardware marginals is 1.52/1.09/0.83/0.67/0.56/0.66. More modelled noise moves both toward the chip until about ×20. It does not reproduce q125's overshoot (0.50 at ×20 against the chip's 0.30). That narrower statement is what the data support.
- All 54 per-qubit cells and all primary-table cells match the JSON. E3's 0.27650 (5530/20000) rounding to 0.277 is acceptable.

**C17. Citations.** *Cannot check* the primary source (Vezvaee et al. 2025, arXiv:2510.18847; network forbidden). The program's own scout summary, the only record, says χ = 3.6–4.0 without DD and 2.3–2.5 with DD, from a uniform median model on surface-code circuits. It also says ibm_fez "was run but not shown because [it] underperformed". "About" ×3 understates the no-DD range, and the record does not say whether the Stage 1 job used DD.

**C18. Negative stated plainly.** *Holds.* "Verdict: fail", "The fix makes almost no difference".

**D19. Budget.** *Holds.* $0, 0 QPU s. The frozen run completes with socket `connect`, `create_connection` and `getaddrinfo` patched to raise (`work/scripts/nonet.py`). The code does not *enforce* no-network (prereg §7 "the script cannot reach the network"); it simply makes no calls.

**D20. Stop-on-refusal.** *Not applicable* (no API).

**D21. Scale direction.** *Not applicable.*

**D22. Replication.** *Holds.* No hit is claimed.

**E23. Seed.** Seed recomputation, chain choice, timing and use *hold*; the beacon itself *cannot be checked*.
- Chain choice holds. CURBY-Q's latest completed round is 28297 at 2025-08-22 13:42, more than 24 h old, so the chain is stalled and CURBy-RNG is used, as §2 states.
- The seed recomputes: `python3 -I ledger/seed.py 6c61b0fe…096c ng-p3-1 --purpose sim` gives seed 1832684880191759722 and seed32 1158620522, equal to `data/p3-1-seed.json` and the prereg line.
- The code uses `seed32_sim` from that file as `seed_simulator` for every run and nothing else is random (deterministic ALAP, FakeFez).
- Nothing was drawn between the commits: 593f8fd adds only the seed file, `seed_commit.py` and the beacon line.
- Pulse after the commit holds *on the archived record*: pulse 2026-11-04T22:35:00.190Z against prereg author time 22:34:03Z.
- **Cannot check** that the pulse, its index 1591379, its randomness, or the "previous pulse" 1591378 at 22:34:00.164Z (before the commit) are genuine and first on the chain. That needs a beacon fetch, which the user forbade. `certificate_verified: false` is recorded honestly.

**E24. Tiebreak.** *Not applicable* (bet type `standard`; no QPU).

## The pre-mortem, scored

My failure reason, written before reading the pre-mortem: *"Idle relaxation over a 9.6 µs circuit is negligible against T1/T2 of about 45–200 µs, so ALAP scheduling moves P(yes) by about 0.000; this omission is not the gap."* Kind: `world`. Disclosure: the results file itself quotes a fragment of the pre-mortem ("idle relaxation over a roughly 10–20 µs circuit … is far too small"; kind `world`). I read that while reading the results file, before the checklist. I formed my reason from the 10-seed, 4M-shot and corrected runs, not from that fragment.

Pre-mortem (bbd6348 §0): "If this fails, the most likely reason is that idle relaxation over a roughly 10–20 µs circuit, against T1 ≈ 90–200 µs, is far too small to move P(yes) from 0.25 to 0.40." Kind `world`.

Score: **named**. The bet failed by exactly this mechanism: a 9.6 µs circuit, an idle-decay effect of −0.0004 at 4M shots, and the same result with correct T1/T2. The execution bugs found here did not cause the failure.

## Required cuts

In `results/p3-1-scheduled-sim.md` (and a correcting note in the next commit for the commit message, which cannot be amended):

1. Title "P3-1 result: the simulator was not just set up wrong" → "P3-1 result: idle decay does not explain the Stage 1 gap".
2. "loaded the chip's error rates from that afternoon" → "loaded the chip's gate and readout error rates from that afternoon (a bug left T1 and T2 at the library's 2025 values; with the afternoon's T1 and T2 the result is the same, 26.8%, auditor's re-run)".
3. "which reproduces program 1's 25.1% within the pre-registered tolerance, so the rebuild is faithful" → "which lies within the pre-registered tolerance of program 1's 25.1%. That control is weak: a simulator with no noise at all gives 27.9% and would also pass it."
4. "the qubits keep their state for 90 to 200 millionths of a second" → "the qubits' T1 was 88–204 and T2 45–191 millionths of a second that afternoon".
5. "So the gap is not our set-up." → "So the gap is not this omission in our set-up."
6. "Either the chip's errors were larger than its calibration said that afternoon, or they were of a kind the simulator does not model." → "Other explanations remain: the chip's errors were larger than its calibration said, or of a kind the simulator does not model, or our simulation differs from the run in ways this test did not touch (IBM's actual schedule, readout asymmetry)."
7. "Adding a small systematic "twist" to every two-qubit gate changes nothing (26.7%)." → delete. Replace with: "The planned twist on every two-qubit gate (E2) was not applied because of a bug, so E2 is untested."
8. "Tripling every error rate, about what published work says such models need on this chip family, only reaches 27.7%." → "Tripling every gate and readout error (T1 and T2 were meant to be divided by 3 but a bug left them unchanged) gave 27.7%; with T1 and T2 also divided by 3 it gives 28.8% (auditor's re-run). Published work on Heron chips needed ×2.3–4.0."
9. "Simply turning up noise of the modelled kind pulls answers toward randomness, not toward the chip's pattern." → "More noise of the modelled kind does move P(yes) toward the chip's 50%, but only at about ten times the calibrated rates (44% at ×10, auditor's sweep), and it never reproduces qubit 125's drop to 30%."
10. "This scheduled model is now the program's "corrected simulator", and every later program-3 prediction uses it." → "As pre-registered, this scheduled model becomes the program's "corrected simulator", once its T1/T2 and ZZ bugs are fixed and the fix is checked; no later prediction may use `p3sim` before then."
11. Exploratory table, E2 row: "0.267" → "not applied (bug: all-qubit ZZ error overridden by local CZ errors); 0.267 is the scheduled model at 20,000 shots".
12. Exploratory table, E3 row label "scheduled, every error ×3, T1 and T2 ÷3" → "scheduled, every gate and readout error ×3 (T1, T2 unchanged by a bug)".
13. "The hardware drops by 0.12 to 0.45 on eight of nine." → "The hardware drops on eight of nine, by 0.08 to 0.45."
14. "Gap closed: … = **7%**. The scheduled-minus-control difference is +0.001." → keep the pre-registered 7% and add: "Almost all of it (95%) is the difference between our rebuild and program 1's 1,000-shot estimate (SE 0.014). Scheduling alone closes about 0% (−0.0002 ± 0.0010 over ten seeds)."
15. Commit message 280e180, "idle decay closes 7% of the Stage 1 gap" and "Exploratory E2 (ZZ 0.1 rad) 0.267": correct in the next commit's message to "the gap-closed figure is 7% by the pre-registered formula, nearly all reconstruction offset; idle decay ≈ 0%; E2 was not applied".

## What would break it next

The fail verdict is robust. With the model correctly built it holds at 0.268, and P(yes) does not cross 0.40 until the modelled errors are scaled about ×10 (0.337 at ×5, 0.443 at ×10). What is not yet established is the corrected simulator itself.

Cheapest next test, $0, about one laptop minute:
- Fix `overwrite_calibration` to assign the whole `target.qubit_properties` list, with an assertion that the target's T1/T2 equal the snapshot.
- Fix E2 by composing the ZZ unitary into each pair's local CZ error.
- Re-run P3-1 under a DEVIATIONS row.
- Add a control that a noiseless model fails, such as requiring the per-qubit marginals to match the archived noisy sim within shot noise, not just P(yes) within ±0.03.

This must land before P3-2 scores "toward the corrected sim". The chip-side question (do twirling or DD move P(yes)) stays with P3-2/P3-3.
