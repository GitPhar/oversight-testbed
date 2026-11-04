# Direction rows given to the odds elicitor (template v1)

This is exactly what the fresh-context elicitor saw: each direction's row and its draft pass rule, and nothing else. It saw no ranking, no weights, no human odds and no reads files. Written 2026-11-04 by the program-3 scout, before any program-3 data existed.

Shared facts for every row:
- Device: `ibm_fez`, IBM Heron r2, 156 qubits, IBM Open Plan.
- Calibration at program 1's job time: median CZ error about 2×10⁻³, T1 about 130–145 µs, readout error about 0.6–0.8%; one Stage 1 qubit had T2 of 44.6 µs.
- SamplerV2 applies no twirling and no dynamical decoupling (DD) unless asked.
- Mid-circuit measurement (MCM) takes about 1.56 µs (offline FakeFez snapshot). Each shot costs about 0.28 ms.

---

## P3-1. Does a correctly scheduled noise model close the Stage 1 gap? (archives, $0)
- **Assumption at stake:** The Stage 1 gap shows the device departing from its own calibration, not our simulator being built wrong.
- **Prior work:**
  - In the Qiskit Aer source, `NoiseModel.from_backend` adds idle T1/T2 decay only on explicit `Delay` instructions. Program 1 transpiled without a scheduling step, so qubits waiting during the circuit had no decay in simulation.
  - Bautra et al. 2026 (Eagle, 5 qubits, depth 10–30): `from_backend` twins reached ≥95% similarity to hardware in only 7 of 96 comparisons.
  - Vezvaee et al. 2025 (Heron, deep circuits): a calibration-derived model had to be scaled up 2.3–2.5× with DD, or 3.6–4.0× without, to match hardware.
- **Our data:**
  - Stage 1 circuit: 9 qubits, depth 208, 117 CZ, 1,000 shots.
  - P(yes) (a weighted vote over the 9 bits): ideal 0.294, `from_backend` noisy sim 0.251, hardware 0.502 (z ≈ 12).
  - Hardware per-qubit P(1) is below the ideal value on 8 of 9 qubits; the largest drop is 0.75 → 0.30. The noisy sim stays within 0.05 of ideal on every qubit.
  - The scout saw these marginals while reading, before any pre-registration.
- **Cheapest test:**
  - Rebuild the archived as-run circuit and schedule it ALAP with FakeFez gate durations.
  - Build the noise model from FakeFez, then overwrite T1, T2, readout and gate errors for the 9 qubits with the job-time calibration snapshot.
  - Run 100,000 simulated shots and compute P(yes) with program 1's readout.
  - Control: the unscheduled version must reproduce about 0.25.
- **Cost:** $0, 0 QPU s, minutes on a laptop.
- **Draft pass rule:** The scheduled noise model gives P(yes) ≥ 0.40, closing at least 60% of the gap.

## P3-2. Coherent or stochastic? Twirling and DD on the Stage 1 circuit
- **Assumption at stake:** IBM's reported per-gate error rates describe the error of an untwirled, structured circuit. Those rates are randomized-benchmarking averages, i.e. measured under twirling.
- **Prior work:**
  - Wallman & Emerson 2016: randomized compiling turns coherent error into stochastic error.
  - Cenedese et al. 2022 (ibm_lagos): the simulator's Bloch ellipsoid is z-aligned, while hardware's is rotated off-axis. Random echoes restored agreement.
  - Proctor et al. 2022: structured (periodic) circuits did worse than disordered ones on every processor tested, and predictions from published error rates were over-optimistic.
  - Vezvaee et al. 2025: on Heron, the main errors are non-Markovian dephasing and coherent ZZ crosstalk.
  - Hickman et al. 2025 (ibm_marrakesh, Heron r2): DD raised the idle decay time from 6.95 µs to 10.5–13.8 µs. Crosstalk was not dominant.
  - No published twirl-on/off comparison of a deep, user-level Heron r2 circuit against `from_backend`.
- **Our data:** As in P3-1. Program 1 ran with neither twirling nor DD.
- **Cheapest test:**
  - One job, interleaved: the identical Stage 1 circuit on its original 9 physical qubits.
  - Four arms of 2,000 shots each: (a) as run; (b) gate and measurement twirling; (c) DD with XY4; (d) twirling plus DD.
  - Plus readout calibration circuits (all-0, all-1), 2 × 2,000 shots.
- **Cost:** ≈ 6 QPU s.
- **Draft pass rule:** Arm (b) moves P(yes) toward the `from_backend` prediction by at least 0.125 relative to arm (a), at ≥ 3σ.

## P3-3. Is the gap these nine qubits, or this afternoon?
- **Assumption at stake:** The gap is a stable property of the device as calibrated, not of one defective qubit (T2 44.6 µs in the original layout) or of one moment in time.
- **Prior work:**
  - Klimov et al. 2018: T1 varies by up to 10× on 15-minute scales because of TLS defects.
  - Carroll et al. 2022 (IBM): TLS positions wander 1–10 MHz over 272 h.
  - Kim et al. 2024/25 (IBM): T1 fluctuated by more than 300% over 60 h. Heron r2 has a TLS-mitigation feature.
- **Our data:** As in P3-1.
- **Cheapest test:**
  - In P3-2's job, run the same logical circuit on 2 other 9-qubit layouts chosen by a fixed rule written in advance (exclude the low-T2 qubit; maximise median T2), at 2,000 shots each, each with its own noisy-sim prediction.
  - Plus 2 repeats of the original layout as run, at least 3 h apart, 1,000 shots each.
- **Cost:** ≈ 6 QPU s.
- **Draft pass rule:** On both alternative layouts, the hardware-minus-simulation P(yes) gap is less than half the original layout's gap measured in the same job.

## P3-4. Does DD restore the missing entanglement?
- **Assumption at stake:** The missing half of the witness negativity is idle dephasing that DD removes.
- **Prior work:**
  - Vezvaee et al. 2025: DD changed the model-scaling factor on Heron from 3.6–4.0 to 2.3–2.5 for phase-sensitive states.
  - Ezzell et al. 2023: DD beats free evolution in every sequence tested on IBM devices.
  - Hickman et al. 2025: as in P3-2.
- **Our data:** Two-qubit tomography after deep circuits on ibm_fez, negativity on hardware vs noisy sim:
  - item h088: 0.063 [0.051, 0.075] vs 0.149 (162 CZ, physical qubits 44 and 37);
  - item h268: 0.067 vs 0.118;
  - item h221: 0.147 vs 0.171 (its pair is decoupled from the rest).
- **Cheapest test:**
  - Re-run h088's 9 tomography settings plus 4 readout-calibration circuits on the same physical qubits, with DD off and DD XY4, 1,000 shots each (26,000 shots).
- **Cost:** ≈ 9 QPU s.
- **Draft pass rule:** Negativity with DD on exceeds negativity with DD off by at least 0.043 (half the original gap), and the bootstrap 95% interval of the difference is above 0.

## P3-5. Coherent or incoherent, read from the archived tomography ($0)
- **Assumption at stake:** As in P3-2, tested on data already in hand.
- **Prior work:** Cenedese et al. 2022: coherent error shows as a rotated state relative to the simulator's.
- **Our data:** As in P3-4. The archived tomography counts are 9 settings × 4,000 shots for each of 3 items. They have not been analysed beyond the negativity table.
- **Cheapest test:**
  - For each item, fit the hardware two-qubit state with two families that have the same number of parameters (7). Each family is applied to the noisy-sim state:
    - (i) a coherent family: local unitaries plus a ZZ-phase rotation;
    - (ii) an incoherent family: local Pauli channels plus global depolarising.
  - Compare log-likelihoods on the raw counts.
- **Cost:** $0, 0 QPU s.
- **Draft pass rule:** The coherent family fits better than the incoherent family on at least 2 of 3 items, with a log-likelihood margin of at least 10.

## P3-6. Does ibm_fez leak settings between qubits? (no-signalling screen)
- **Assumption at stake:** On one Heron r2 chip, a qubit's outcome statistics do not depend on the setting chosen on another qubit. Every foundations test here relies on this as its stand-in for locality.
- **Prior work:**
  - Rybotycki et al. 2025 (IBM Eagle): marginal shifts δP up to about 0.05; one fourth-neighbour pair at p = 5.3×10⁻¹⁷; cause unidentified.
  - Bednorz et al. 2025: significant signalling in several qubit groups on Eagle devices and on ibm_torino (Heron r1), but none beyond statistical error on ibm_kingston (Heron r2).
  - ibm_fez has never been screened. In IBM's 100-qubit GHZ work it was the weakest of three Heron r2 devices (fidelity 0.46 vs 0.55 and 0.70).
- **Our data:** None.
- **Cheapest test:**
  - Rybotycki's idle test: about 40 disjoint neighbouring pairs in parallel, phase-only settings, no entangling gate.
  - Lean version: 4 circuits × 10,000 shots, which detects δP of about 0.03 or more.
- **Cost:** ≈ 13 QPU s (≈ 30 s for the 4.5×10⁻³-sensitivity version).
- **Draft pass rule (pass = clean):** No pair shows |δP| > 4.5σ after a Bonferroni correction over all pair-setting tests.

## P3-7. Two-friend genuine local friendliness with external settings
- **Assumption at stake:** Local friendliness: absoluteness of observed events, no superdeterminism, and locality, holding jointly. "Genuine" means testing an inequality that is not a Bell inequality, with the friend a 1–4-qubit register. Quantum theory predicts a violation.
- **Prior work:**
  - Bong et al. 2020 (photons): the genuine LF facet was violated only at the two highest state purities, 0.921 and 0.992.
  - Zeng, Labib & Russo 2025: the semi-Brukner inequality (a Bell facet) with a friend of up to 5 qubits on ibm_torino.
  - Laux & Cavalcanti 2026 (ibm_marrakesh, Heron r2): a single friend, a CHSH-type inequality, settings drawn from qubits on the same chip and flagged as uncertified. Hardware S_LF was 0.31–0.47 against an ideal 0.83, implying an effective CHSH visibility of about 0.87 at 3 CZ.
  - No genuine LF inequality has been tested on any quantum processor.
- **Our data:** None.
- **Cheapest test:**
  - Inequality: Bong facet 1 (Eq. 13). Quantum maximum 1.345, LF bound 0. It survives white noise only if visibility ≥ 0.817. Under white noise, S = 7.345v − 6.
  - Circuit:
    - State 0.7757|00⟩ − 0.6311|11⟩, with angles 58.16°, 153.51° and 68.56° in the x–z plane.
    - The friend is a CNOT-ladder copy into n qubits, read by majority vote; "reverse" applies the inverse ladder.
    - n = 0, 1, 2, 4; 9 setting pairs each, 2,500 shots each; measurement twirling.
    - Settings and block order fixed by a public Bell-certified randomness beacon pulse drawn after pre-registration.
  - Controls:
    - a decohered friend at n = 1 (a mid-circuit measurement replaces the uncompute; quantum theory predicts S ≤ 0);
    - a no-signalling audit;
    - a friend-record fidelity audit.
- **Cost:** ≈ 37 QPU s (≈ 70 s for n up to 8 at 4,000 shots).
- **Draft pass rule:** S > 0 by at least 5σ at n = 1 or larger. In the same run, the decohered-friend control must be consistent with S ≤ 0, and the no-signalling audit must show no deviation above 3σ.

## P3-8. Is there a one-friend genuine LF inequality? (desk work, then hardware)
- **Assumption at stake:** "For one friend there are no genuine LF inequalities beyond Bell inequalities." Laux & Cavalcanti 2026 state this for a 2-setting scenario.
- **Prior work:**
  - Haddara & Cavalcanti 2024 list the cases where the LF polytope equals the Bell polytope. A one-friend scenario where the friend's party has 3 settings is not among them, which implies genuine LF facets exist there.
  - No text read gives an explicit facet or a quantum violation for it.
- **Our data:** None.
- **Cheapest test:**
  - Enumerate the facets of the partially deterministic LF polytope: Alice has a friend and 3 settings, her setting 1 deterministic; Bob has 2 or 3 settings and no friend.
  - Run a see-saw for each facet's quantum maximum.
  - Hardware only if a facet tolerates at least 15% white noise: n + 2 qubits, ≈ 17–26 QPU s.
- **Cost:** $0 (laptop hours) for the desk stage.
- **Draft pass rule (desk stage, refereed by mathematics):** A non-Bell LF facet exists in the one-friend 3×2 or 3×3 scenario that quantum theory violates with a white-noise tolerance of at least 15%.

## P3-9. Sequential Peres–Mermin under exact Contextuality-by-Default
- **Assumption at stake:**
  - (Method) Program 1's Contextuality-by-Default (CbD) pipeline certifies contextuality where physics says it exists, after the measured disturbance between sequential measurements is accounted for.
  - (Physics) Peres–Mermin contextuality survives an exact CbD correction on superconducting hardware.
- **Prior work:**
  - Kirchmair et al. 2009 (ions): 5.46 against a noncontextual bound of 4.
  - Massé 2021 (unrefereed review): an adapted, not exact, CbD formula on Kirchmair's data leaves a margin of 0.566.
  - Kumar et al. 2025 (Google Willow): sequential mid-circuit measurement, χ = 5.618 ± 0.005, repeat agreement 0.9636, no CbD.
  - Kelleher & Holweck 2025 (Heron r2): Peres–Mermin 5.31 with product-only readout and no error bars.
  - Leupold et al. 2018: no correction method existed for state-independent witnesses.
  - Typical per-observable marginal shifts between contexts: about 0.02–0.11 across ion and superconducting experiments.
- **Our data:** Program 1's CbD/QQ analysis found no contextuality in language-model ratings.
- **Cheapest test:**
  - 2 data qubits and 1 ancilla. Each observable is mapped onto the ancilla, which is measured mid-circuit and reset; all three outcomes per context are stored individually.
  - 6 contexts × 2 orders × 2 input states (|00⟩, Bell) = 24 circuits × 4,000 shots.
  - Analysis: the exact CbD linear program with order treated as part of the context, and CNT2 with a bootstrap.
- **Cost:** ≈ 42 QPU s (≈ 22 s for one input state).
- **Draft pass rule:** For both input states, the exact CbD linear program rejects noncontextuality, with CNT2's bootstrap 99% lower bound above 0.

## P3-10. Sequential 4-cycle with the exact KDL criterion (pipeline check)
- **Assumption at stake:** As P3-9 (method), on a cyclic system, where the Kujala–Dzhafarov–Larsson (KDL 2015) criterion is necessary and sufficient.
- **Prior work:**
  - Kirchmair/Gühne: 2.23(5) on the disturbance-corrected 4-observable subset (ions).
  - Wang et al. 2022: two ions, not sequential, C = 2.526 ± 0.016, CbD correction term 0.023.
  - Malinowski et al. 2018: KDL on a sequential ion KCBS test in both orders, violated by up to 25σ.
- **Our data:** None.
- **Cheapest test:**
  - Observables Z2, Z1Z2, X1, X1X2 in the 4 contexts {Z2, Z1Z2}, {X1, X1X2}, {Z2, X1}, {Z1Z2, X1X2}, each in both orders: 8 circuits × 4,000 shots on the optimal state.
  - Statistic: the signed correlator sum minus the summed marginal differences. The noncontextual bound is 2; the quantum ideal is 2√2.
- **Cost:** ≈ 15 QPU s.
- **Draft pass rule:** The KDL statistic is above 2 with its 99.9% lower bound above 2, in both orders.

## P3-11. Leggett–Garg with mid-circuit measurement, a clumsiness control and CbD
- **Assumption at stake:** Macrorealism with noninvasive measurability for one transmon. The rival reading is that IBM "violations" are clumsiness: the measurement itself disturbs.
- **Prior work:**
  - Huffman & Mizel 2017 (IBM 5Q, ancilla CNOTs): LG = −0.21 ± 0.03 against a total invasiveness of 0.08 ± 0.04, a margin of about 2.6σ.
  - Knee et al. 2016 (flux qubit): a non-disturbance test passed by 84 s.d., but no LGI.
  - Ku et al. 2020 (IBM): invasiveness grows with qubit number.
  - Santini & Vitale 2022 (ibmq_manila): K3 violations, but no clumsiness test, and readout mitigation was essential.
  - Nath et al. 2025 (IBM Brussels): K3 slightly below the 1.5 target.
  - No IBM LGI has used mid-circuit measurement, CbD or a pre-registered clumsiness control.
- **Our data:** None.
- **Cheapest test:**
  - One qubit, Ry(π/3) between three times (ideal K3 = 1.5). Mid-circuit measurements at t1 and t2, final measurement at t3.
  - Two preparations: maximally mixed (|0⟩ and |1⟩ pooled) and the eigenstate |0⟩.
  - 16 circuits: correlators and the grand ensemble (8), NSIT (2), and Knee controls on |0⟩, |1⟩ and |+⟩ with and without the t2 measurement (6). 4,000 shots each, in 6 parallel copies on non-adjacent qubits.
- **Cost:** ≈ 29 QPU s.
- **Draft pass rule:** For the mixed preparation, both of these hold:
  - the CbD-corrected K3 (K3 minus the summed marginal differences) exceeds 1 by at least 5σ, pooled across copies;
  - K3 − 1 exceeds the largest measured disturbance on the classical preparations by at least 3σ.

## P3-12. Do alternating non-commuting measurements show memory? (a Hossenfelder-type test)
- **Assumption at stake:** Outcomes of repeated non-commuting measurements on one system are uncorrelated, as quantum theory says. There is no superdeterministic memory at microsecond spacing.
- **Prior work:**
  - Hossenfelder 2014 proposed that environment-borne hidden variables give Corr(κ) = exp(−κ/τ), with τ of order 10⁻⁶ s for µm-scale detectors.
  - Hossenfelder & Palmer 2020 §6 call for small, cold devices with short time increments.
  - No hardware test was found.
- **Our data:** None.
- **Cheapest test:**
  - About 50 non-adjacent qubits in parallel. On each: H, then 8 mid-circuit measurements alternating Z and X, all outcomes stored.
  - Control: 8 Z measurements in a row, the repeatability ceiling.
  - 2 circuits × 4,000 shots.
- **Cost:** ≈ 6 QPU s.
- **Draft pass rule (pass = quantum theory holds):** In the alternating circuit, the pooled correlation between same-observable outcomes is below 0.01 in magnitude at lags 2, 4 and 6. In the control circuit, consecutive repeats agree at least 95% of the time.

## P3-13. LG-certified randomness from P3-11's data
- **Assumption at stake:** One transmon's Leggett–Garg violation can certify randomness semi-device-independently (Nath et al.). This assumes dimension 2, projective measurements at t1 and t2, and a time-pair choice independent of the system.
- **Prior work:**
  - Nath et al. 2025 (IBM Brussels): no bit count, no σ, no extractor, time pairs not seeded.
  - Nath et al. 2024 (photons): K3 = 1.32 ± 0.04, 919,118 bits; no certified randomness below about 3,000 runs; about 68% of the asymptotic rate at 10⁵ runs. Theorem 2 rate: 0.054 bits per round at K3 = 1.31, 0.115 at 1.40.
  - Known caveats:
    - the time-pair choice uses about 1.58 input bits per round;
    - the provider sees the settings in advance;
    - transmon leakage strains the dimension-2 assumption.
- **Our data:** None.
- **Cheapest test:**
  - 0 extra QPU s. Use the mixed-preparation correlator circuits of P3-11 (about 72,000 rounds), with their order seeded from the beacon.
  - Compute the Theorem 2 min-entropy bound with a finite-size correction at 99% confidence.
- **Cost:** 0 extra QPU s (≈ 19 s if run standalone).
- **Draft pass rule:** The finite-size certified min-entropy is at least 0.05 bits per round.

## P3-14. Maximally ψ-epistemic models, with no fair-sampling assumption (d = 4)
- **Assumption at stake:** Maximally ψ-epistemic models, in which quantum state overlaps are fully explained by overlapping distributions of an underlying real state.
- **Prior work:**
  - Ringbauer et al. 2015 (photons, d = 4): S = 0.690 ± 0.001 against a ψ-epistemic bound of 1. It assumed fair sampling; without it, about 98% detection efficiency is needed.
  - Yang, Yuan & Barnes 2025 ran PBR on a Heron r2 (ibm_marrakesh): forbidden-outcome rates of 0.17–0.56% on adjacent pairs. PBR needs preparation independence, and their pass threshold came from their own noise model.
  - No superconducting test with d ≥ 3 was found.
- **Our data:** None.
- **Cheapest test:**
  - Two transmons as one 4-level system with real amplitudes, 5 states, 10 pairwise measurements: 30 circuits × 2,000 shots.
  - The quantum overlap ωq is computed two ways: from the intended states, and from states reconstructed by tomography (9 × 1,000 shots).
  - Raw counts, no post-selection.
- **Cost:** ≈ 21 QPU s.
- **Draft pass rule:** S + 5σ < 1 under both choices of ωq.
