# Reads: Leggett–Garg / NSIT on hardware, clumsiness loophole, and certified randomness for setting seeds

Reader agent, cluster (a) LGI/NSIT + clumsiness, (b) certified randomness on an Open Plan device. Compiled 2026-11-04.
All numbers come from the text I opened. Where I worked out a number myself, it says "(my calc)".

## Corrections to the brief (findings in their own right)

- **Knee et al. 2016** does *not* use ideal negative measurements. It uses a "blind" measurement pulse whose result is never read, and bounds clumsiness with control experiments on classical preparations. Ideal negative measurements are the earlier paper, Knee et al. 2012, Nat. Commun. 3, 606 (ref. 19 of the 2016 paper; I did not open it).
- **Huffman & Mizel 2017**: the arXiv title is "Leggett-Garg test of superconducting qubit addressing the clumsiness loophole" (arXiv:1609.05957). The published version is PRA 95, 032131 (2017). The quantity tested is not K3 but a Wilde–Mizel "adroit" variant (see record).
- **"Ku et al. 2020, Hidden nonmacrorealism"** conflates two papers:
  - Ku et al., npj Quantum Inf. 2020, "Experimental test of non-macrorealistic cat states in the cloud" (arXiv:1905.13454), which ran on IBM.
  - "Hidden nonmacrorealism: reviving the LGI with stochastic operations" (arXiv:2105.08273, 2021), which is photonic, not IBM. I found no hidden-nonmacrorealism experiment on IBM.
- **Santini & Vitale**: confirmed as PRA 105, 032610 (2022), arXiv:2109.02507. It ran on ibmq_manila.
- **Kofler & Brukner 2013**: confirmed as PRA 87, 052115 (2013), arXiv:1207.3666. I took the venue from Knee 2016's reference list; the arXiv page does not show it.
- **Nath et al. arXiv:2502.02973**: exists, by P. P. Nath, A. Sinha and U. Sinha. It was published as Front. Quantum Sci. Technol. (2025), DOI 10.3389/frqst.2025.1661544.
  - The analysis comes from a companion paper: Nath, Saha, Home and Sinha, arXiv:2402.03712 (photonic). Read together with it.
- **Liu et al. 2025**: confirmed as Nature, DOI 10.1038/s41586-025-08737-1, arXiv:2503.20498, with 32 authors.

---

## Foundations

### LG 1985 — A. J. Leggett & A. Garg, 1985, PRL 54, 857, https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.54.857
- read_depth: abstract (paywalled). The assumptions were cross-checked against the restatement in Emary et al. 2014.
- what_tested: Theory paper. Quantum mechanics conflicts with the joint assumptions of (A1) macroscopic realism (MR) and (A2) noninvasive measurability (NIM). The later review adds (A3) induction: no backward causation.
- on_whom: none (proposal for a SQUID flux qubit).
- how_scored: the K3 inequality on two-time correlators (form given under Emary below).
- result: n/a.
- limits: NIM cannot be verified directly. This is the origin of the clumsiness loophole.
- borrow: state A1–A3 explicitly in our pre-registration, and say which one each control targets.
- next_steps_it_suggests: realistic macroscopic-coherence experiments.

### LGI review — C. Emary, N. Lambert, F. Nori, 2014, Rep. Prog. Phys. 77, 016001, https://arxiv.org/abs/1304.5133
- read_depth: partial (first ~100k characters of the ar5iv HTML: assumptions, K_n bounds, clumsiness, superconducting experiments). The Lüders-bound and NSIT sections were not reached.
- what_tested: review.
- on_whom: n/a.
- how_scored:
  - K3 = C21 + C32 − C31 ≤ 1. The qubit maximum is 3/2 at Ωτ = π/3.
  - K4 has classical bounds −2 ≤ K4 ≤ 2. The qubit maximum is 2√2.
  - General K_n: −n ≤ K_n ≤ n−2 for odd n.
- result: the reviewed superconducting experiments:
  - Palacios-Laloy et al. (transmon, continuous weak measurement): a single violating point, f_LG = 1.37 ± 0.13.
  - Groen et al.: no magnitude given on the page I read.
- limits:
  - Says almost all tests to that date are open to the clumsiness loophole.
  - Weakness does not imply non-invasiveness.
  - Stationarity-based inequalities avoid NIM but add time-translation and Markov assumptions.
- borrow:
  - The list of remedies: ideal negative measurement, a "venality" bound for badly prepared ancillas (f ≥ −2ζ), and adroit-measurement controls.
  - K4 as a cheap extension: four correlators, bound 2√2.
- next_steps_it_suggests: tests closing the clumsiness loophole; applications in transport and biology.

### NSIT — J. Kofler & Č. Brukner, 2013, PRA 87, 052115, https://arxiv.org/abs/1207.3666
- read_depth: full (ar5iv HTML).
- what_tested: theory. NSIT is defined as P(B at t_B) = Σ_A P(A at t_A, B at t_B), i.e. an earlier measurement does not change later one-point statistics. It is introduced as a second necessary condition for macrorealism.
- on_whom: n/a.
- how_scored: one-point probabilities with and without the earlier measurement.
- result:
  - Neither NSIT nor the LGI implies the other.
  - Mach–Zehnder example where NSIT is violated and the 3-time LGI is satisfied: R1 = R2 = 1/2, φ = π, q = 1.
  - Reverse example where the LGI is violated and NSIT holds: R1 = 1/4, R2 = 3/4, φ = π, q = 1/2.
  - NSIT needs only two times and no correlators.
- limits:
  - Non-invasiveness still needs ideal negative-result measurements.
  - A mixed initial state can hide an NSIT violation.
- borrow:
  - NSIT is the cheapest test: two circuits per time pair.
  - It is the natural signalling-in-time diagnostic to put beside K3.
  - Our design can choose the initial state so that NSIT holds or fails by design (see summary).
- next_steps_it_suggests: closing the non-invasiveness, fair-sampling and freedom-of-choice loopholes.

### CbD for LG systems — J. V. Kujala, E. N. Dzhafarov, J.-Å. Larsson, 2015, PRL 115, 150401, https://link.aps.org/accepted/10.1103/PhysRevLett.115.150401
- read_depth: full (accepted manuscript, 5 pp).
- what_tested: theory. Gives a necessary and sufficient criterion for "maximal noncontextuality" in cyclic systems, allowing inconsistent connectedness (signalling in time).
- on_whom: n/a. The worked example is the KCBS photonic data.
- how_scored:
  - For rank n: s1(⟨R_i R_{i⊕1}⟩) − Σ_i |⟨R_i^i⟩ − ⟨R_i^{i⊕1}⟩| ≤ n − 2.
  - s1 is the maximum, over sign patterns with an odd number of −1's, of the signed sum of the correlators.
  - The LG system is rank n = 3, so the bound is 1.
- result:
  - The paper notes that in an LG system, signalling in time can make ⟨R2⟩ and ⟨R3⟩ depend on context.
  - ⟨R1⟩ differences can come only from design biases.
- limits: no LG data analysed.
- borrow:
  - This is the exact correction to use. The marginals needed are a by-product of the three correlator circuits, so the CbD treatment adds no QPU cost.
  - Use the Bonferroni / confidence-interval construction from their KCBS example.
- next_steps_it_suggests: study contextuality without first eliminating biases and signalling.

---

## LGI / NSIT on superconducting hardware

### Knee 2016 — G. C. Knee, K. Kakuyanagi, …, A. J. Leggett, W. J. Munro, 2016, Nat. Commun. 7, 13253, https://arxiv.org/abs/1601.03728
- read_depth: full (arXiv v3 PDF, including supplementary notes).
- what_tested:
  - Not K3. Tests the "non-disturbance condition", NDC: d = ⟨Q3⟩_G − ⟨Q3⟩_2̄ = 0.
  - This is an NSIT-type equality: compare ⟨Q3⟩ with and without an operation O at t2.
  - Supplementary Note 1 derives the NDC from the LGIs and lists the three disturbance terms d_c^I, d_c^II, d_c^III that a full LGI test should control.
- on_whom:
  - NTT three-junction flux qubit, I_p = 170 nA, T2 ≈ 10 ns, read out by a JBA.
  - O is an un-inspected 12 ns measurement pulse at 6.5 GHz.
  - 7×10⁶ trials per data point.
- how_scored:
  - Disturbance d_σ = [P(Q3=+1|σ,O) − P(Q3=−1|σ,O)] − [P(Q3=+1|σ) − P(Q3=−1|σ)].
  - Measured for classical preparations g, e (S1 at θ = 0, π) and the superposition ρ (θ = π/2).
  - The macrorealist bound is min(d_g, d_e) ≤ d_ρ ≤ max(d_g, d_e).
- result:
  - d_g = −0.026612 ± 4.38×10⁻⁴
  - d_e = 0.015884 ± 6.09×10⁻⁴
  - d_ρ = −0.089788 ± 6.12×10⁻⁴
  - d_ρ − d_g = −0.063177, about 84 s.d., with variances propagated as Var(d_ρ) + Var(d_g).
  - Visibility V ≈ 0.28, far below what an LGI violation would need.
- limits:
  - O must be calibrated against classical preparations. The bound assumes S1 prepares a convex mixture or the "worst" state.
  - Macroscopicity is modest (10 ns, 170 nA).
- borrow:
  - **The clumsiness control to pre-register.** Run O (our mid-circuit measurement) on |0⟩ and |1⟩, then on |+⟩, and compare d_ρ with [d_g, d_e].
  - Six circuits cover it, and the test works even at low visibility.
- next_steps_it_suggests: strict tests at higher macroscopicity, which needs small classical disturbance.

### Huffman & Mizel 2017 — E. Huffman & A. Mizel, 2017, PRA 95, 032131, https://arxiv.org/abs/1609.05957
- read_depth: full (ar5iv).
- what_tested:
  - Wilde–Mizel "adroit" LG test: LG = ⟨O1O3⟩_a + ⟨O1O2⟩_f + ⟨O2O3⟩_f + 1 ≥ 0.
  - Violation requires LG < 0 *and* |LG| ≥ ε_total, where ε_total = ε_b + ε_c + ε_d + ε_e comes from four verification protocols.
  - Each protocol checks whether one intermediate measurement, by itself, shifts ⟨O1O3⟩.
- on_whom:
  - IBM 5Q, with qubit Q2 as the system and the other four qubits as measurement ancillas.
  - Intermediate measurements are made by CNOT onto an ancilla (one measurement per qubit was allowed then).
  - θ = −3π/4.
  - Six protocols, the whole program repeated 10 times, 8192 shots per measurement.
- how_scored: measured LG against ε_total, with errors taken from the spread across the 10 repeats.
- result:
  - LG = −0.21 ± 0.03 (QM prediction ≈ −0.16).
  - ε_total = 0.08 ± 0.04.
  - Controls: ⟨O1O3⟩ over the b–e protocols = −0.69, −0.71, −0.68, −0.67 (each ±0.01–0.02), against ⟨O1O3⟩_a = −0.70 ± 0.01.
  - No σ count is stated. My calc: margin 0.13 ≈ 2.6σ in quadrature.
- limits:
  - The authors assume the four measurements do not "collude nonlinearly".
  - Gate fidelity too low for generic implementations; specific gates and qubits had to be chosen.
  - O1 was an initialization, not a measurement.
- borrow:
  - The ε-adroitness bookkeeping. It is a stronger clumsiness control than Knee's when ancilla-coupled measurements are used.
  - The failure mode: the margin shrinks quickly because the ε terms add linearly.
- next_steps_it_suggests: test the equality form (Kofler–Brukner / Clemente–Kofler) instead of the inequality.

### Ku 2020 — H.-Y. Ku et al., 2020, npj Quantum Inf. (doi 10.1038/s41534-020-00321-x), https://arxiv.org/abs/1905.13454
- read_depth: full (ar5iv).
- what_tested:
  - LG "quantum witness" W = |p_t2(j) − p_t2^M(j)|, an NSIT-type quantity, on 2-qubit cat states and 4- and 6-qubit GHZ states.
  - Clumsy-macrorealist bound W ≤ max_i I(i), with invasiveness I(i) = |1 − ε^M(i|i)| measured on basis states.
- on_whom:
  - IBM Q5 Tenerife and IBM Q14 Melbourne.
  - Intermediate measurement by CNOT to ancillas, or by "prepare-and-measure" re-preparation.
  - 8192 shots per run; invasiveness repeated across 25 experiments on different days.
- how_scored: W compared with the maximum measured invasiveness.
- result:
  - n = 2 cat at θ = π/2: W = 0.453 ± 0.008. Single-qubit maximum invasiveness 0.023 ± 0.004; two-qubit maximum 0.077 ± 0.008.
  - n = 4 GHZ: W = 0.245 ± 0.008, against invasiveness 0.146 ± 0.006, so it passes.
  - n = 6 GHZ: W = 0.181 ± 0.007, against invasiveness 0.686 ± 0.007, so it fails (consistent with clumsy macrorealism).
  - θ = 0 baseline W ≈ 0.058, which the authors attribute to CNOT errors.
- limits:
  - Ancilla CNOTs add errors. The authors propose direct mid-circuit measurement as the fix.
  - A non-Markovian (~5 µs) loophole is only partly addressed.
  - Clumsy and "macroscopic" invasiveness cannot be separated.
- borrow:
  - Invasiveness measured on *every* computational basis state, not just one.
  - The finding that invasiveness grows with qubit number faster than the witness does.
  - Mid-circuit measurement is the authors' own stated next step.
- next_steps_it_suggests: mid-circuit / multiple measurements per qubit, error mitigation, larger n.

### Santini & Vitale 2022 — A. Santini & V. Vitale, 2022, PRA 105, 032610, https://arxiv.org/abs/2109.02507
- read_depth: full (ar5iv).
- what_tested: K3, K3′ and K3perm for one qubit, one transmon under its own dynamics, and a 5-qubit TFIC Trotter evolution; plus LG–Bell inequalities on two qubits. No K4 and no Lüders-bound test.
- on_whom:
  - ibmq_manila (5 qubits).
  - Separate circuits per correlator; no mid-circuit measurement.
  - 2^13 shots per circuit, 75 time points.
- how_scored: the K values against bound 1, after inverse-response-matrix readout mitigation.
- result:
  - No numerical violation values or σ are given; statistical error is about 10⁻².
  - Mitigation was "essential".
  - Transmon violations appear for t < 30 µs.
- limits:
  - No NIM, NSIT or clumsiness test; the authors say loophole-free LGI remains open.
  - Mitigation cost is exponential in qubit number.
- borrow: the failure mode — without readout mitigation and a clumsiness control, an IBM LGI "violation" says little.
- next_steps_it_suggests: relax NIM or locality; ancilla coupling to all qubits.

### Rybotycki 2025 — T. Rybotycki, …, W. Belzig, A. Bednorz, 2025/2026, EPJ Quantum Technol. 13, 8, https://arxiv.org/abs/2507.07904
- read_depth: full (HTML v3).
- what_tested: two quantities, both on weak-measurement correlators.
  - Weak-measurement LG: ⟨𝒜⟩ + ⟨ℬ⟩ − ⟨𝒜ℬ⟩ ≤ 1, ideal value √2. The paper's captions inconsistently say 2√2.
  - Time-order invariance: ⟨𝒜ℬ𝒞⟩ − ⟨ℬ𝒜𝒞⟩, ideal value 1.
- on_whom:
  - Devices: Eagle (ibm_brisbane, sherbrooke, kyiv), Heron (ibm_torino, ibm_kingston; revision not stated), and IonQ Forte.
  - 10 sets of 3 qubits per IBM device.
  - Each weak measurement couples system to an ancilla meter, with strength λ = sin θ, θ = ±0.1, via CZ / ECR or a fractional RZZ on Heron.
  - 10,000 shots × 25 repetitions × 8 circuits = 200 circuits, i.e. 2×10⁶ shots per job.
- how_scored: the difference between θ = +0.1 and −0.1 runs, divided by 2λ; Bernoulli errors of about 0.013 per correlation.
- result:
  - Eagle: LG violation about 10σ on average.
  - Heron fractional RZZ: LG violated for one group on torino and at least five on kingston; time-order violated for all groups.
  - IonQ: LG = 1.583 ± 0.025, which is above √2 and attributed to about 5% RZZ miscalibration.
- limits:
  - The LG test needs an assumed measurement strength; whether fractional gates really scale strength "remains ambiguous".
  - The meter and gate model must be trusted.
  - Weak measurements need very large statistics.
  - No NSIT test.
- borrow:
  - The ±θ differencing trick for drift.
  - Fractional RZZ is available on Heron.
  - Weak-measurement LG is a sensitive gate benchmark: deviations exceeded the declared error rates.
- next_steps_it_suggests: calibrate fractional-gate strength; pulse-level weak ECR, which the Open Plan does not offer.

### Rybotycki 2026 — same group, arXiv:2603.22020 (2026), https://arxiv.org/html/2603.22020v1
- read_depth: full (HTML v1).
- what_tested: conditioned two-detector inequality ⟨a+b|c⟩²/(4⟨ab|c⟩) ≤ 1, ideal value 4/3. Needs no ±1 bound and no strength calibration.
- on_whom:
  - ibm_kingston (the text) or ibm_pittsburgh (a figure caption) — the paper is inconsistent.
  - 10 sets of 3 qubits, fractional RZZ(±0.1).
  - 80 jobs × 10,000 shots, 200 circuits per job.
  - IonQ: 1 job of 100,000 shots.
- how_scored: Bernoulli errors.
- result:
  - IBM: "beyond 12 standard deviations" in the text, 10σ in the abstract.
  - IonQ: 1.272 ± 0.035 and 1.289 ± 0.035.
- limits:
  - Assumes identical, independent, informative detectors.
  - Statistics scale as 1/λ², and the effect vanishes at λ = 1.
- borrow: removes the strength-calibration assumption of the 2025 paper. At their shot counts it is still far above our budget.
- next_steps_it_suggests: none explicit.

### Rybotycki no-signalling 2025 — T. Rybotycki, T. Białecki, J. Batle, A. Bednorz, 2025, Adv. Quantum Technol., https://arxiv.org/abs/2409.11348
- read_depth: full (HTML v2).
- what_tested: spatial no-signalling — Alice's marginal independent of Bob's setting — on qubit pairs.
- on_whom:
  - IBM Eagle (sherbrooke, brisbane, kyoto, kyiv).
  - Nearest- and fourth-neighbour pairs.
  - 100 circuits per job, 20,000 shots per circuit (7,500 on kyiv); about 3×10⁷ trials total.
- how_scored: marginal differences δP against σ ≈ 1.3×10⁻⁴.
- result:
  - δP of several ×10⁻⁴, up to about 0.05 for one pair.
  - Sherbrooke pair 49–66: p = 5.3×10⁻¹⁷.
  - The authors say simple ZZ crosstalk does not explain the violation.
- limits: mechanism unidentified; the communication loophole is open on a chip.
- borrow: **a failure mode for us.** Setting-dependent marginal shifts of 10⁻⁴–10⁻² exist on IBM hardware. Any ancilla- or spectator-based LG test needs a CbD-style connection term to absorb them, and this is a reason to use well-separated qubits for parallel copies.
- next_steps_it_suggests: higher-statistics reruns; a technical source analysis.

---

## Certified randomness

### Nath, Sinha & Sinha 2025 — P. P. Nath, A. Sinha, U. Sinha, 2025, Front. Quantum Sci. Technol. (arXiv:2502.02973), https://arxiv.org/html/2502.02973v1
- read_depth: full (arXiv v1 HTML; the Frontiers version was also opened, but its tables lost their numbers in extraction).
- what_tested:
  - LG-certified semi-device-independent randomness on one IBM qubit.
  - Inequality K3: ⟨Q1Q2⟩ + ⟨Q2Q3⟩ − ⟨Q1Q3⟩ ≤ 1, quantum cap 1.5.
  - Plus NSIT checks.
- on_whom:
  - Main device: IBM Brussels, qubit 12 chosen with mapomatic. Supplement: Perth, Lagos, Kyoto.
  - 5 circuits: three correlator circuits plus two single-time circuits for NSIT.
  - 50,000 shots per circuit, 10 repetitions; mitigation runs at 20,000 shots.
  - Initial state (|0⟩ − i|1⟩)/√2.
  - Projective Z measurements. The text does not say whether the earlier measurement is mid-circuit; they report "a few microseconds" per circuit.
- how_scored: min-entropy bound H∞ ≥ −log2[(1 + α + √(1−2α))/2], with α = K3 − 1 (from arXiv:2402.03712, Theorem 2).
- result:
  - Measured K3 is "slightly lower" than target.
  - RMSE 0.00073 raw and 0.000183 with mthree.
  - NSIT holds to order 10⁻². No residuals are tabulated and no σ is given.
  - No total certified bit count, no extractor, no QPU time.
  - My calc from their formula: 0.0496 bits/round at K3 = 1.30; 0.115 at 1.40; 0.179 at 1.45; 0.415 at 1.50.
- limits:
  - The authors say it is not loophole-free.
  - Sub-runs were sequential with no random seed for the time-pair choice; seeded runs were done only on a simulator.
  - No extraction.
  - State-preparation security rests on trusting IBM's preparation.
  - The assumption wording differs between versions: arXiv says projective measurements at t1 and t2; the Frontiers text says first and third.
- borrow:
  - The 5-circuit layout.
  - The formula, which sets the target: K3 ≥ 1.40 gives ≥ 0.11 bits/round.
- next_steps_it_suggests: random seeds for the setting choice, an extractor, a loophole-free implementation.

### Nath, Saha, Home & Sinha 2024 — P. P. Nath, D. Saha, D. Home, U. Sinha, 2024, arXiv:2402.03712 (photonic; the companion analysis), https://arxiv.org/html/2402.03712v2
- read_depth: partial (first ~100k characters of the HTML: protocol, theorems, experiment, randomness results).
- what_tested: theory and photonic experiment for an LG-based semi-device-independent QRNG.
- on_whom: heralded SPDC photon in a two-path interferometer, with motorized blockers as the projective measurements at t1 and t2.
- how_scored:
  - Theorem 1 (joint probabilities) gives up to about 1.41 bits/round.
  - Theorem 2 (conditional probabilities, secure against state-preparation attacks) gives −log2[(1+α+√(1−2α))/2], up to about 0.415 bits/round.
- result:
  - K3 = 1.32 ± 0.04.
  - NSIT residuals 0.002 ± 0.017, 0.002 ± 0.016, 0.004 ± 0.016.
  - 919,118 bits in total, at 3,865 bits/s.
  - At K3 = 1.31 the paper reports 0.05406 bits/run, which matches Theorem 2 (my calc 0.0541).
  - With memory effects at n = 10⁵ runs: 3,673 bits (0.0367 bits/run), with no certified randomness below about 3,000 runs. A biased seed gives 2,777 bits.
- limits:
  - **Assumptions:** dimension 2; projective measurements at t1 and t2; the t3 measurement can be a general POVM; the initial state is uncorrelated; time-pair choice is independent of the system; NSIT holds.
  - No extractor.
  - The time-pair choice itself consumes input randomness (uniform over 3 pairs).
- borrow:
  - The finite-size scaling: about 68% of the asymptotic rate at 10⁵ runs, and none below about 3×10³ runs.
  - The explicit assumption list. On a transmon, "dimension 2" is exactly what leakage breaks.
- next_steps_it_suggests: extraction and amplification.

### Li 2021 SI-QRNG on IBM — Y. Li, Y. Fei, W. Wang, X. Meng, H. Wang, Q. Duan, Z. Ma, 2021, Sci. Rep. 11, 23873, https://pmc.ncbi.nlm.nih.gov/articles/PMC8669044/
- read_depth: full.
- what_tested: source-independent QRNG. The source is untrusted and the measurement is trusted. X-basis rounds bound the phase error of the Z-basis raw bits.
- on_whom:
  - ibmq_5_yorktown and ibmq_lima, qubit 0.
  - 8192 shots per circuit; n_z = 819,200 Z-basis bits; n_x = 25,100 X-basis bits as stated (inconsistent with the 251 runs × 8192 shots they describe).
- how_scored: finite-size phase-error bound, then Toeplitz hashing.
- result:
  - Yorktown: e_z ≤ 0.0122442, 741,006 bits (rate 0.9045).
  - Lima: e_z ≤ 0.0397301, 621,729 bits (rate 0.7589).
- limits:
  - The basis choice was fixed, not random, "for demonstration".
  - Trusts the measurement device and a readout-error model.
  - Uses Shannon rather than min-entropy.
- borrow: the high-rate option if we accept a trusted measurement. It is very cheap: about 10⁶ shots for 7×10⁵ bits. The certification is only as good as trusting IBM's readout.
- next_steps_it_suggests: none beyond more devices.

### Liu 2025 RCS certified randomness — M. Liu, R. Shaydulin, P. Niroula, M. DeCross, S.-H. Hung, et al. (32 authors), 2025, Nature 640, 343, https://arxiv.org/abs/2503.20498
- read_depth: partial (HTML; abstract plus results and security sections).
- Record of why it does not fit:
  - Quantinuum H2-1, 56 qubits.
  - 60,952 circuits; 30,010 valid samples in 64,641 s; abort threshold 2.2 s per sample.
  - XEB 0.32 against a threshold of 0.30.
  - Verification on Frontier, Summit, Perlmutter and Polaris at about 1.1 EFLOPS.
  - 71,313 bits certified against a restricted adversary; Toeplitz extractor.
  - **Does not transfer:** needs seconds-level response latency (our Open Plan queues take hours), exascale classical verification, and about 10⁴–10⁵ QPU seconds.

### CURBy beacon — G. A. Kavuri et al., 2025, Nature (doi 10.1038/s41586-025-09054-3); NIST news, https://www.nist.gov/node/1883571
- read_depth: abstract (NIST news page only; the Nature paper was not opened).
- what_tested: public, Bell-test-certified (device-independent) randomness beacon, with Twine hash-chain traceability.
- on_whom: NIST entangled-photon Bell test; measurements repeat 250,000 times per second.
- result: 7,434 of 7,454 attempts succeeded in the first 40 days (99.7%), each producing 512 random bits. Free, at random.colorado.edu.
- borrow: **the right source of setting seeds for our experiments, at 0 QPU seconds.** Certification is device-independent, which is stronger than anything we can certify on ibm_fez.

### NIST beacon applications — NIST CSRC, "Interoperable Randomness Beacons: applications", https://csrc.nist.gov/Projects/interoperable-randomness-beacons/apps
- read_depth: full (web page).
- what_tested: procedure, not an experiment.
  - Commit up front to a statement S fixing the deterministic use of the pulse at a future time t.
  - Seed Z = Hash(S || randOut[t]).
  - Optionally pre-commit a secret so that even a malicious beacon cannot steer Z.
- borrow: exactly the pre-registration randomisation protocol we need. Hash the pre-registration document together with a future CURBy pulse, and derive all setting choices from Z.
- limits:
  - NIST warns that failure handling (e.g. an unavailable backend or qubit) must be specified in S in advance.
  - I found no study measuring whether quantum seeds improve experimental validity over a good beacon or PRNG; the benefit is auditability, not physics.

---

## Cluster summary

### Open questions that fit our budget

Cost rule used: 0.28 ms per shot plus about 2 s per job. Parallel copies on well-separated qubits in the same circuit add no shot time. Mid-circuit measurement adds microseconds against the ~250 µs repetition delay, so I treat it as negligible.

**Q1. Does a K3 violation from mid-circuit measurement on Heron r2 survive a pre-registered Knee-style clumsiness control and a CbD (Kujala–Dzhafarov–Larsson) correction for signalling in time?**

Prior work:
- Huffman & Mizel 2017 came closest: ancilla CNOTs on IBM 5Q, margin about 2.6σ (my calc).
- Knee 2016 ran the clumsiness control (flux qubit, no LGI).
- Ku 2020 measured invasiveness on IBM, with ancilla CNOTs.
- Every IBM LGI to date used separate circuits or ancilla CNOTs. None used mid-circuit measurement, none applied CbD, and none had a pre-registered control. Ku 2020 names mid-circuit measurement as the next step.

Design:
- 1-qubit LG sequence with Ry(π/3) between measurement times, giving ideal K3 = 1.5.
- Initial state maximally mixed, taken as a pooled |0⟩/|1⟩ preparation. My calc: then all marginals are 0, NSIT holds ideally, and CbD reduces to K3 ≤ 1. Any hardware marginal shift (T1, readout bias) enters the CbD penalty term directly.
- Circuits:
  - C12, C23, C13 and the grand ensemble (MCM at t1, t2 plus final t3), each with 2 preparations: 8 circuits.
  - NSIT single-time circuits: 2.
  - Knee controls (|0⟩, |1⟩, |+⟩, with and without the MCM at t2): 6.
  - Total 16 circuits.
- Run 4,000 shots each, in 6 parallel copies on non-adjacent qubits.

Statistics: σ(K3) ≈ 0.02 per copy, so a 15–20σ violation if hardware K3 ≈ 1.3–1.4 (my calc).

Pre-registered prediction to make it sharp:
- If K3 were measured from a definite eigenstate preparation (e.g. |0⟩), ideal QM gives a CbD value of 1.5 − |0.25 − (−0.5)| = 0.75 ≤ 1, i.e. *no* CbD contextuality, because the projective measurement at t2 signals into ⟨Q3⟩.
- Running both preparations tests that contrast.

**Cost: 64k shots ≈ 18 s + 2 s ≈ 20 QPU-s.**

**Q2. Is a mid-circuit measurement less invasive on classical states than an ancilla-CNOT measurement on Heron r2 (d_g, d_e, Huffman–Mizel ε-adroitness)?**

- Ku 2020 and Huffman–Mizel measured only the ancilla-CNOT version, on retired devices. Ku attributes the 0.058 baseline to CNOT errors.
- Design: add an ancilla-CZ-based measurement variant of the 6 Knee controls plus the 4 Huffman–Mizel verification circuits, in the same job as Q1.
- Report ε_total for each method.
- **Cost: about 10 circuits × 4,000 = 40k shots ≈ 11 s + 2 s ≈ 13 QPU-s (about 11 s if merged into the Q1 job).**

**Q3. Does the LG semi-device-independent min-entropy bound hold on Heron r2, using mid-circuit measurement at t1 and t2, a seeded time-pair choice, and a leakage check of the dimension-2 assumption?**

- Nath 2025 came closest: IBM Brussels, unseeded, no extractor, NSIT reported only to about 10⁻², no σ, no QPU time.
- Design:
  - Nath's 5 circuits, with the order of time-pair choices drawn from a CURBy-derived seed.
  - Finite-size target from Nath 2024: no randomness below about 3×10³ runs, about 0.037 bits/run at 10⁵.
  - At K3 ≈ 1.4 the asymptotic rate is about 0.11 bits/round (my calc).
  - So 3 × 10,000 correlator shots plus 2 × 5,000 NSIT shots should certify a few hundred bits after finite-size cuts (rough estimate).
- **Cost: 40k shots ≈ 11 s + 2 s ≈ 13 QPU-s.**
- Caveats, which make this a foundations test and not a seed source:
  - (i) The time-pair choice consumes log2 3 ≈ 1.58 input bits per round to produce ≤ 0.11 certified bits, so it is randomness *consumption*, not expansion, unless spot-checking is added.
  - (ii) Choices are fixed per circuit or job, not per shot, so the provider knows them in advance.
  - (iii) Transmon leakage violates dimension 2, and the Open Plan offers no qutrit readout to bound it (not verified here whether IQ-level readout is exposed).
- For actual setting seeds, use CURBy with the NIST commit-then-reveal Z = Hash(S || pulse), at **0 QPU-s**.

Optional extension: K4 (bound 2, quantum 2√2) in the same job, with 4 correlators × 2 preparations × 4,000 shots ≈ 9 s + 2 s.

### Questions that do not fit
- Weak-measurement (fractional RZZ) LG / time-order tests at Rybotycki strength λ = 0.1: 2×10⁶ shots per job ≈ 560 s per job, which exceeds 374 s.
- RCS-certified randomness (Liu 2025): needs about 2 s response latency, exascale verification, and about 6×10⁴ s of QPU time.
- Device-independent (Bell) randomness on chip: needs spacelike separation. On-chip no-signalling is already violated at p ≈ 10⁻¹⁷ (Rybotycki 2409.11348).
- Exceeding the Lüders bound (K3 > 1.5) with multi-level or degenerate measurements: needs qutrit control, which the Open Plan lacks.
- Pulse-level weak ECR or blind-measurement pulses à la Knee: need pulse access.
- Macroscopicity scaling with GHZ size (Ku 2020): fits in shot count, but invasiveness already swamps W at n = 6, so it is likely uninformative without a new control. Deferred.

### Fields searched that returned nothing relevant
- LGI with mid-circuit measurement on IBM dynamic circuits (2019–2026): none found.
- Any CbD-corrected LGI on superconducting hardware: none.
- Temporal-steering or prepare-and-measure dimension-witness randomness on IBM or superconducting devices (2023–2026): none. Only photonic and continuous-variable proposals turned up.
- Hidden-nonmacrorealism experiments on IBM: none (photonic only).
- Empirical studies of whether quantum seeds improve pre-registered randomisation: none. Only NIST beacon guidance.
