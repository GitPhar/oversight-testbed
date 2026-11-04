---
bet: ng-p3-5
program: nature-graded (program 3)
prereg_commit: ff2c7e7
results_commit: 9e9ae5d
auditor_session: audit2 worktree, subagent audit of ng-p3-5 (clean copy of 9e9ae5d in scratchpad ng-p3-5/repo; all 32 files checked byte-identical to `git show 9e9ae5d:<path>`)
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5 (ff2c7e7, 1593b09 and 9e9ae5d all carry "Co-Authored-By: Claude Opus 5.5")
same_model_family: true
date: 2026-11-04 16:15 America/Denver
claims_checked: 27
holes_found: 8
overclaims_cut: 11
reproduced: true
verdict_claimed: null            # the pre-registered label is "fail, incoherent better" (§5.2); the template has no "fail", so it is entered as null = predicted event absent (same convention as ng-p3-1)
verdict_after_audit: null        # "fail" stands on every re-analysis; the "incoherent better" label stands as the §5.2 count, but the plain-English reading of it ("blur, not steering") does not
verdict_stands: true
canary: unknown
false_alarms: 0
failed: true
failure_reason: The reference state is purer than the chip's state on all three items and a unitary family cannot change purity, so a 7-v-7 contest is decided by the reference's spectrum (on h221 even an arbitrary 15-parameter unitary loses by 40). Kind design.
failure_kind: design
premortem_score: named
risk_seen: null
---

# Audit of ng-p3-5: Coherent or incoherent, from the archived tomography

## In plain English

The verdict stands: under the pre-registered rule the bet fails. Steering wins clearly on 1 of 3 items, and the rule needed 2. Blurring wins by 10 or more on 2 of 3, which is the pre-registered "incoherent better" label. The tables regenerate from the archive to 0.001 in ΔlogL. The fail survives 251 random starts, four choices of reference state, cross-validation over settings and a bootstrap (it holds in 99% of resamples). What does not stand is the plain-English reading, "the chip's errors look mostly like random blur, not steering":
- The two families are not matched. A unitary cannot make a state more mixed, and the reference is purer than the chip's state on every item. So on h221, no unitary at all, even one with 15 parameters, can beat the 7-parameter blur fit.
- When both kinds are allowed together, steering terms improve the fit by 22, 89 and 116 log-likelihood units on the three items. Steering errors are present on every pair.
- The "corrected simulator" behind the reference never received the job's T1/T2 values.
- h088's margin rests mostly on one of nine settings.

What would break the label: drop setting XX or YX and refit, and the in-sample verdict becomes a pass. Held-out prediction does not follow, though.

## The case that this result is false

(Written before the checklist.) The headline says "the chip's errors … look mostly like random blur, not steering". The test cannot say that, for four reasons.

First, the contest is lopsided by construction. Family (i) is unitary, so it keeps the reference's eigenvalues. Family (ii) can only add mixing. Program 1 already showed that the hardware pair states carry less entanglement than the simulator on all three items: 0.147/0.063/0.067 against 0.171/0.149/0.118, and this was in the map row at 14:06. If the reference is too pure, then any amount of mixing beyond it can only be captured by (ii), however much coherent error is also present. "Same seven knobs" is a parameter count, not matched flexibility.

Second, the two families are not nested, so "(ii) fits better than (i)" says nothing about whether coherent error is present. Only a model with both, tested by a nested likelihood ratio, can say that.

Third, the result is a 2–1 split, and the largest margin (+63) is on the coherent side. Summed, the three ΔlogL come to −15.4, which is barely negative. Any reasonable change to the reference could flip the sign of that sum. Reading a 2–1 count over three qubit pairs as a property of "the chip" is a pooling step.

Fourth, the reference is not what it is called. Another audit (ng-p3-1) reported that p3sim's T1/T2 overwrite never takes effect, and on h088 and h268 the measured pair is entangled with unmeasured qubits (program 1: ideal pair purity 0.746 and 0.819). So steering errors on spectator qubits would show up as blurring on the pair. On top of that, ΔlogL of ±35–45 between non-nested fits to 36,000 shots has a sampling spread that nobody reported. A threshold of 10 justified by "e¹⁰" is not a sampling statement.

## Claims checked

| # | claim (quoted or paraphrased from results/p3-5-coherent-fits.md) | check run | outcome |
|---|---|---|---|
| 1 | ΔlogL −43.5, −34.9, +63.0 | `work/rerun.py` (the frozen script, output redirected, network blocked) | holds: −43.53, −34.88, +63.01 (archived −34.877 vs rerun −34.876 on h088) |
| 2 | logL ρ_ref / coherent / incoherent / saturated, 12 cells | rerun | holds, every cell |
| 3 | "1 of 3" ≥ 10, so fail | rerun | holds |
| 4 | "2 of 3" ≤ −10, so pre-registered label "incoherent better" | prereg §5.2 at ff2c7e7 | holds as the count rule |
| 5 | "best family is 28, 121 and 61 below" saturated | arithmetic on table | holds (28.4, 120.7, 60.7) |
| 6 | "All six fits converged." | `work/a1_multistart.py`, 251 starts (200 wide, 50 narrow, 1 at ρ_ref) | hole (minor): the best-of-21 coherent fit is 0.9 below the optimum found (h221) and 4.1 below it (h268); ΔlogL becomes −42.7, −34.9, +67.1; verdict unchanged |
| 7 | "Each explanation got the same seven adjustable knobs" (implying a fair contest) | a1: SU(4) (15-parameter arbitrary unitary) and full-state MLE | hole: every coherent fit keeps purity(ρ_ref) exactly (0.9842, 0.6139, 0.7190), while the full-state MLE has 0.9078, 0.5127, 0.6538; SU(4) loses to the 7-parameter incoherent fit on h221 by 40.3 and on h088 by 2.2 |
| 8 | "each started from what our corrected simulator says" | `work/check_overwrite.py` | hole: `target.qubit_properties[i] = …` is lost; T1 stays at FakeFez values (q9 247 µs vs snapshot 147; q37 222 vs 115). Gate-error overwrite does take effect |
| 9 | verdict robust to the reference | `work/fixed_ref.py` + a1 (T1/T2 really overwritten; and bare FakeFez) | holds: fixed-T1 ΔlogL −41.8, −29.3, +86.0; bare −24.5, −19.8, +127.6; both fail, "incoherent better" |
| 10 | "On two of the three pairs, blurring fits clearly better" | `work/a2_boot_loso.py` bootstrap (B = 200) | holds with a caveat: h221 95% [−65.1, −18.6]; h088 [−75.6, +4.3], ≤ −10 in 86.5% of resamples |
| 11 | "The margins are large … 44 and 35" | bootstrap SD | hole (no uncertainty reported): SD 12.9, 20.9, 20.6; h088 is 1.2 SD from the bar |
| 12 | h088's margin | `work/a3_decomp.py` per-setting decomposition | hole: XX contributes −45.5 of −34.9 (YX −18.6, YZ +30.8) |
| 13 | verdict under leave-one-setting-out (in-sample) | a2/a3 | hole: dropping XX gives h088 +35.9 → **pass**; dropping YX gives +10.9 → **pass**; 7 of 9 drops keep "fail, incoherent better" |
| 14 | held-out (cross-validated over settings) ΔlogL | a2 | holds: −79.8, −224.0, +31.9 → still 1 of 3 coherent, 2 of 3 incoherent |
| 15 | "look mostly like random blur, not steering" (title) | a1 nested hybrids (coherent∘incoherent, both orders, 14 parameters) | hole: adding coherent terms to the incoherent fit gains +22.1, +88.7, +116.1 logL (7 extra parameters; χ²₇ p = 0.001 needs 12.2); adding incoherent terms to coherent gains +64.8, +123.6, +49.0. Both are present on every item (these are lower bounds, from 51 starts) |
| 16 | "the chip's extra error looked mostly like random noise, which is what IBM's reported error rates are built to describe" | design, §6 of prereg | hole: scope ("the chip", 3 pairs, one afternoon) and mechanism (twirled rates not tested here) |
| 17 | "That leans against the idea that hidden systematic errors explain program 1's surprises" | design | hole: program 1's "surprises" (Stage 1 P(yes) 0.50 vs 0.25) are a different circuit; and coherent terms are significant on all three items here (#15) |
| 18 | "Where blurring wins, it also reproduces the lost entanglement … roughly the chip's" | JSON negativities | hole: h088 incoherent fit 0.035 against chip 0.063 (from ρ_ref 0.112 it removes 0.077 against a gap of 0.049, overshooting by 57% of that gap); h221 0.139 vs 0.147 does hold |
| 19 | "fitted steering errors leave the entanglement almost untouched (0.111, against the chip's 0.067)" | JSON | holds |
| 20 | negativity table, 15 cells | rerun + JSON | holds |
| 21 | φ = −0.009, −0.086, +0.049; p = 0.011, 0.011, 0.000 | `work/a4_params.py` | holds |
| 22 | "local Pauli errors of 1–13% on one qubit of each pair: q9 p_X 0.053; q44 p_Z 0.073, q37 p_X 0.096; q16 p_X 0.103" | a4 (clbit 0 = first physical qubit, from the as-run measure gates) | holds per value; the summary is loose: the largest primary value is 10.3% (13.1% only in the secondary), and h088 has two qubits, so "one qubit of each pair" is wrong |
| 23 | ideal-reference ΔlogL −73.8, −438.7, −191.6; "sign flips" for h268 | rerun | holds |
| 24 | ρ_ref negativity 0.112, 0.103 vs program 1 0.149, 0.118, labelled not pre-registered | rerun | holds, labelled correctly |
| 25 | seed32 2090756689 from pulse 1591384 | `python3 ledger/seed.py <randomness> ng-p3-5 --purpose starts` | holds (seed 15010879962529819217) |
| 26 | $0, 0 QPU s | rerun with socket connect/getaddrinfo patched to raise | holds: the run completed with no network |
| 27 | pre-mortem paragraph "For the auditor: … through local Pauli terms, not the global depolarising term (p ≈ 0.01)" | a4 | holds as a fact; out of place, because the auditor scores the pre-mortem (operators/premortem.md) |

## Checklist

**A1 (pre-registration predates analysis).** Holds, with the archival caveat. Author times: ff2c7e7 at 15:39:08, seed 1593b09 at 15:40:32, result 9e9ae5d at 15:43:08, so the result came 2 min 36 s after the seed. My run of the frozen script took 1 min 49 s, which is consistent. The frozen script refuses to read the archive without the seed file. The analysis code was frozen in the prereg commit, unlike program 1's text-only archival freezes. The archives are unchanged since program 1 committed them: `witness-run-1.json` sha256 6e681d61…, last changed in 655a8f8 (2026-11-03); `ibm-calibration.json` b47b92a5…, last changed in e2215bb (2026-11-03); the working tree equals HEAD. The prereg names the files but gives no hashes. Neighbouring analyses before the freeze: program 1 reconstructed these same counts into density matrices and negativities (mitigated and unmitigated, with CIs; `results/witness-run-1.json`) on 2026-11-03, and published the pair purities of the ideal states. The map row (14:06) carried the hardware-versus-sim negativity gap and the remark that "local unitaries alone cannot change negativity". So the structural tilt toward the incoherent family (B9) was knowable when the contrast and bar were set. That knowledge would have lowered P(pass), not helped it (engine odds 0.42), and the bar comes from the map, written before any program-3 computation on the counts. The "incoherent better" sub-label was added at 15:39, after the map but before the data. The test is labelled a frozen, pre-registered test, not an exploratory one. The prereg's "structure-only check built ρ_ref for item h221 … not printed or inspected" cannot be checked. Local file-read times cannot be checked (no cache files; the export's mtimes are those of the copy).

**A2 (rule, statistic, seed, budget match word for word).** Hole, on the material, not the rule. The pass rule, count, label rule and seed match §4–§5 exactly. But §2 defines ρ_ref as "FakeFez + the witness job's calibration snapshot". The frozen code (`p3sim.overwrite_calibration`) does not apply the snapshot's T1/T2: `t.qubit_properties[i] = QubitProperties(...)` writes into a copy, and `be.target.qubit_properties[9].t1` stays at 247 µs where the snapshot says 147 µs (`work/check_overwrite.py`). sx/x/CZ errors do change. There is no DEVIATIONS row. Impact on the verdict is none: with T1/T2 really overwritten (`work/fixed_ref.py`), ΔlogL is −41.8, −29.3, +86.0, still fail and still "incoherent better". The results file's descriptions of the reference as the "corrected simulator" are inaccurate.

**A3 (bar not lowered).** Holds. ≥ 10 on ≥ 2 of 3 is the same in map row P3-5 (14:06), prereg and results.

**A4 (primary is primary).** Holds. ΔlogL per item and the count are reported first. The ideal-reference fit is labelled secondary.

**B5 (ties, floating point).** Holds. No item sits within 10 of a threshold, and rerun drift is 0.001.

**B6 (pooling).** Hole in the write-up, not the rule. The rule counts items, but the plain English turns a 2–1 split across three different qubit pairs into a statement about "the chip's errors". The summed ΔlogL, which the prereg does not score, is −15.4 as run and −10.5 at the audit's better optimum. It is **+14.9** with the reference the prereg describes (fixed T1/T2) and +83.4 with bare FakeFez. The sign of any pooled reading depends on the reference.

**B7 (few items).** Hole. On h088 one setting, XX, contributes −45.5 to a total of −34.9 (`work/a3_decomp.py`). Refitting with one setting dropped (`work/a2_boot_loso.py`): dropping XX gives h221 −33.5, h088 **+35.9**, h268 +47.2, which is a **pass**. Dropping YX gives −32.6, **+10.9**, +73.4, also a **pass**. The other 7 drops keep "fail, incoherent better". Caveat: with one Pauli correlator missing, the coherent family can exploit the unconstrained direction. The held-out log-likelihood of the dropped setting (cross-validation) favours incoherent strongly on h088 (XX −107.3, YX −93.8), so the out-of-sample reading supports the label. Read together, the verdict holds out of sample, but the in-sample margin on h088 is carried by one or two of nine settings.

**B8 (circular estimator).** Holds. ρ_ref comes from simulation and the assignment matrix from calibration circuits; neither is fitted to the tomography counts. Both families are fitted in-sample with equal k, and cross-validation over settings gives the same signs (−79.8, −224.0, +31.9).

**B9 (fair comparison).** Hole (design). "Seven knobs each" is not matched flexibility. Family (i) is unitary, so every coherent fit keeps exactly the spectrum of ρ_ref: purity 0.9842, 0.6139, 0.7190. The best unconstrained physical state has purity 0.9078, 0.5127, 0.6538, so the chip's state is more mixed than the reference on all three items. Even an arbitrary two-qubit unitary (SU(4), 15 parameters) reaches only −39236.4 on h221 against the incoherent fit's −39196.1, a loss of 40.3, and loses on h088 by 2.2. On h221, therefore, *no* coherent model built from this reference can win. The comparison measures whether ρ_ref is too pure, not which error type dominates. The fair baselines are a nested model with both families (run here, see C15) and the full-state MLE (−39172.1, −46283.4, −43265.8). Neither appears in the results. Prereg §6 anticipated part of this ("a family can partly win by repairing ρ_ref's errors of its own kind"), but the results file does not carry the caveat. Convergence: 21 starts miss the coherent optimum by 0.9 on h221 and 4.1 on h268. Only 48 of 251 starts reach within 1 of the best on h268. The incoherent fits are stable (≥ 248 of 251). Verdict unaffected.

**B10 (uncertainty).** Hole. The prereg declares "uncertainty: none beyond the threshold" and justifies 10 as a likelihood ratio of e¹⁰. That is a model-selection margin, not the sampling spread of a non-nested ΔlogL. Bootstrap over counts (B = 200, per-setting multinomial resampling, refit warm-started plus 8 random starts): h221 mean −42.4, 95% [−65.1, −18.6], SD 12.9; h088 −34.1 [−75.6, +4.3], SD 20.9; h268 +68.9 [+29.4, +110.6], SD 20.6. The fail holds in 99.0% of resamples and the "incoherent better" label in 86.5%. Claim #11 sits near the edge of its interval, and no interval is reported. (Bootstrap seeds in my script include Python's `hash(iid)`, which is randomised per process, so a rerun will give slightly different bootstrap numbers.)

**B11 (multiple comparisons).** Holds. One scored rule over 3 items. The secondaries are labelled.

**B12 (leakage).** Holds. No count reaches ρ_ref or A.

**C13 (scope).** Hole. The title and plain English say "the chip's errors" and invoke "what IBM's reported error rates are built to describe". The data are three qubit pairs, one job, one afternoon, untwirled (prereg §6 says so itself).

**C14 (rank).** Holds, mostly. The negativity paragraph is secondary, but it is presented under "Two details matter" as a finding. Covered under C16.

**C15 (mechanism).** Hole. "Not steering" and "mostly like random noise" are not what the design can separate. With both families combined (14 parameters, either order of composition), the coherent terms add +22.1 (h221), +88.7 (h088) and +116.1 (h268) to the incoherent fit, against a χ²₇ 0.001 critical ΔlogL of 12.2. Coherent error is present on every pair; the 7-v-7 contest only says which restricted family fails less badly. Separately, the h088 and h268 pairs are entangled with unmeasured qubits (ideal pair purity 0.746 and 0.819, program 1). Coherent errors on those spectators show up as mixing on the pair, so even a clean incoherent win on those items would not identify incoherent physical error. h221, whose pair is decoupled, is not affected by this point.

**C16 (plain English vs table).** Hole.
- "It brings the predicted entanglement down … to roughly the chip's": h088's incoherent fit gives 0.035 against the chip's 0.063.
- "All six fits converged": see B9.
- "1–13% on one qubit of each pair": the largest primary value is 10.3%, and h088 has two qubits.
- "Corrected simulator": see A2.

**C17 (citations).** Holds (n/a). The results file cites no external source.

**C18 (negative stated plainly).** Holds. "The bet … fails" is stated in the second paragraph and in the header.

**D19 (budget).** Holds. $0 and 0 QPU s. The frozen script ran to completion with socket connect/getaddrinfo patched to raise.

**D20 (stop-on-refusal).** Holds (n/a). No API calls.

**D21 (one scale direction).** Holds (n/a). No graded scale.

**D22 (hit replicated).** Holds (n/a). Not a hit.

**E23 (seed).** Holds where checkable. §2 at ff2c7e7 records CURBY-Q round 28297 at 2025-08-22 13:42, which is more than 24 h old, so stalled, so CURBy-RNG is correctly chosen. The record has pulse 1591384 at 22:40:00.181Z (15:40:00 Denver), after the commit at 15:39:08, and previous pulse 1591383 at 15:39:00.190, before it, so this is the first pulse after the commit. `seed.py` recomputes seed 15010879962529819217 and seed32 2090756689 exactly. The code seeds `default_rng(seed32_starts)` once and uses no other seed (the synthetic dry run's seed 0 touches no archive). 1593b09 touched only `data/p3-5-seed.json` and the one prereg line. **Cannot check:** that the pulse index, randomness and timestamps match the public beacon, because network fetches are forbidden in this audit. The seed only places optimiser starts, and B9 shows that the starts matter by at most 4.1 logL here.

**E24 (tiebreak).** n/a. Standard bet.

## The pre-mortem, scored

My reason, written before scoring: *The reference state is purer than the chip's state on all three items, and a unitary family cannot change purity, so the 7-v-7 contest is decided by the reference's spectrum (on h221 even an arbitrary 15-parameter unitary loses by 40). Steering terms are still significant on every item.* Kind: `design`.

Disclosure: the pre-mortem sits in the prereg's §0 table and was seen when I first read the prereg, before the checklist. My failure reason comes from the a1 results (purity and SU(4) bound), not from that sentence. This is a breach of the reading order in operators/auditor.md and should be weighed when scoring this score.

Pre-mortem (ff2c7e7 §0): "If this fails, the most likely reason is that the lost negativity comes mostly from depolarising-type decay, which the incoherent family's global depolarising term captures and local rotations plus one ZZ phase cannot." Kind: `world`.

Score: **named**. The mechanism matches mine: mixing beyond the reference, which no rotation plus ZZ can produce. Two details are wrong. The carrier was local Pauli terms, not the global term (p = 0.011, 0.011, 0.000). The kind is mis-tagged: `world` says steering is absent, while the nested fits show it present on every item, so the failure is a property of the design.

## Required cuts

1. Title: "the chip's errors in program 1's entanglement data look mostly like random blur, not steering" → "On two of three archived qubit pairs, a blurring model fits better than a steering model with the same number of knobs; both kinds of error are present on every pair".
2. "Each explanation got the same seven adjustable knobs, and each started from what our corrected simulator says the state should be." → "Each explanation got seven adjustable knobs, and each started from the P3-1 simulator's state (which, it turns out, kept FakeFez's T1/T2 rather than the job's). The knobs are not equally capable: steering cannot make a state more mixed, and the chip's states are more mixed than the simulator's on all three pairs, so blurring starts with an advantage."
3. "The margins are large: on a scale where 10 counts as clear, they are 44 and 35." → "The margins are 44 and 35 on a scale where 10 counts as clear; bootstrap 95% intervals are [−65, −19] and [−76, +4], and the second rests mostly on one of nine settings (XX)."
4. "Read plainly: on this afternoon's data, the chip's extra error looked mostly like random noise, which is what IBM's reported error rates are built to describe." → "Read plainly: on these three pairs, the chip's states were more mixed than the simulator predicts, and only the blurring model can produce that. When both kinds are allowed together, steering terms still improve the fit clearly on every pair (by 22, 89 and 116)."
5. "That leans against the idea that hidden systematic errors explain program 1's surprises, but it doesn't settle it." → delete.
6. "Where blurring wins, it also reproduces the lost entanglement: it brings the predicted entanglement down from the simulator's value to roughly the chip's." → "Where blurring wins, it lowers the predicted entanglement: to 0.139 against the chip's 0.147 on h221, and to 0.035 against the chip's 0.063 on h088 (an overshoot)."
7. "All six fits converged." → "All six best fits report optimiser success. With 251 starts, the coherent fits improve by 0.9 (h221) and 4.1 (h268), giving ΔlogL −42.7, −34.9, +67.1; the verdict is unchanged."
8. Table caption "(reference: the P3-1-corrected simulator's reduced state; …)" → add "(T1/T2 not overwritten from the snapshot: FakeFez values; with them overwritten, ΔlogL −41.8, −29.3, +86.0)".
9. "The incoherent fits put their weight on local Pauli errors of 1–13% on one qubit of each pair" → "The incoherent fits put their weight on local Pauli errors of 5–10% (largest per qubit)".
10. Header "**Verdict: fail, "incoherent better"** (unaudited)" → add "a 2–1 split; the third pair favours steering by 63, and no uncertainty was pre-registered".
11. Pre-mortem paragraph "For the auditor: the incoherent family won 2 of 3, but through *local* Pauli terms, not the global depolarising term (p ≈ 0.01)." → delete. The auditor scores the pre-mortem; the parameter fact is already in the fitted-parameters line.

## What would break it next

The ($0, laptop, about 10 min) re-analysis to pre-register: replace the 7-v-7 contest with nested likelihood-ratio tests from the combined 14-parameter model ("is coherent error present given incoherent", and the reverse). Use the reference with T1/T2 actually overwritten, a parametric bootstrap for the null of each nested test, and cross-validation over settings as a co-primary. This audit's exploratory pass suggests coherent terms are present on all three pairs (+22, +89, +116), which would reverse the plain-English reading. A second $0 check: simulate the h088/h268 circuits with a small coherent error on the *spectator* qubits only, and ask whether the incoherent family then wins on the pair. If it does, the design cannot tell spectator steering from blur. The device-level answer is P3-2 (twirling and DD on hardware), already on the map.

Producing scripts (all in `/private/tmp/claude-501/-Users-seanpharris-entangled-mind-audit2/bb46787f-112b-4a3c-a1e9-dd87d67b2c75/scratchpad/ng-p3-5/work/`, run with `/Users/seanpharris/entangled-mind/.venv/bin/python -I`, network blocked by `nonet.py`):
- `rerun.py`: the frozen script, unchanged.
- `cache_refs.py`, `fixed_ref.py`: reference states.
- `check_overwrite.py`: T1/T2 overwrite check.
- `a1_multistart.py`: starts, SU(4), full state, hybrids, purity, reference variants.
- `a2_boot_loso.py`: bootstrap, leave-one-setting-out, cross-validation.
- `a3_decomp.py`: per-setting decomposition and LOSO verdicts.
- `a4_params.py`: fitted parameters and qubit mapping.
