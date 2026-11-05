# Rows for the paraphrase elicitation check (template v1 check, random half, seed 20261104)

Shared facts: device `ibm_fez` (IBM Heron r2, 156 qubits, IBM Open Plan); median CZ error ≈ 2×10⁻³, T1 ≈ 130–145 µs, readout error ≈ 0.6–0.8% at program 1's job time; SamplerV2 applies no twirling or dynamical decoupling unless asked; mid-circuit measurement ≈ 1.56 µs; ≈ 0.28 ms per shot.

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
- **Pass rule (paraphrased):** Re-simulating the archived Stage 1 circuit with ALAP scheduling (so idle qubits decay) and the job-time calibration yields a simulated P(yes) of 0.40 or more, i.e. at least 60% of the distance from 0.25 to 0.50 is recovered.

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
- **Pass rule (paraphrased):** Turning on XY4 dynamical decoupling raises item h088's reconstructed negativity by 0.043 or more compared with the DD-off run in the same job, and the 95% bootstrap interval for that increase excludes zero.

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
- **Pass rule (paraphrased):** After Bonferroni correction across every pair and setting comparison, none of the ~40 qubit pairs shows a setting-dependent marginal shift |δP| larger than 4.5 standard errors (the device screens clean).

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
- **Pass rule (paraphrased):** The desk enumeration turns up at least one facet of the one-friend, three-setting LF polytope that is not a Bell inequality and that quantum theory violates while tolerating 15% or more white noise.

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
- **Pass rule (paraphrased):** With the maximally mixed preparation, the pooled K3 after subtracting the summed CbD marginal differences is more than 5σ above 1, and the amount by which K3 exceeds 1 is at least 3σ larger than the biggest disturbance measured on the |0⟩/|1⟩ control preparations.

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
- **Pass rule (paraphrased):** In the alternating Z/X circuit, every pooled same-observable correlation at lags 2, 4 and 6 stays under 0.01 in absolute value, while the all-Z control shows ≥ 95% agreement between consecutive repeats.

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
- **Pass rule (paraphrased):** Using Nath et al.'s Theorem 2 with a 99%-confidence finite-size correction, P3-11's mixed-preparation correlator data certify at least 0.05 bits of min-entropy per round.

