# Reads: other foundations tests (real vs complex, psi-ontology, Born rule, objectivity/Darwinism, superdeterminism, no-signalling, GHZ calibration, MIPT)

Reader: other-foundations cluster. Date: 2026-11-04. Cost rule used throughout: about 0.28 ms per shot plus 1–2 s per job (from `_scout-brief.md`). Shot budgets below are total shots summed over all circuits in a job.

Checks on the candidate list I was given:
- **Nigg et al. 2016 NJP is a trapped-ion experiment, not superconducting.** The abstract says "we report on an experimental implementation using trapped ions." No superconducting PBR test existed until Yang, Yuan & Barnes (arXiv 2510.11213, Oct 2025), and that one ran on IBM Heron2 *ibm_marrakesh* (record below).
- Li et al. 2022 PRL (photonic) exists: Z.-D. Li et al., PRL 128, 040402, arXiv **2111.15128**. The arXiv ID 2103.12000 is a different paper (Eckstein & Horodecki).
- Chen et al. 2022 PRL exists: PRL 128, 040403, arXiv 2103.08123.
- Zhu et al. 2025 (quantum Darwinism) exists: arXiv 2504.00781, Science Advances per the PMC listing. I could not open PMC because of a bot wall. It ran on a 121-qubit Zhejiang processor, not on IBM hardware.
- I did not open Chen et al. 2019 Sci. Bull. (photonic quantum Darwinism) or Unden et al. 2019 PRL (NV quantum Darwinism). I know they exist only because Zhu et al. cite them as [32] and [33].
- The real-vs-complex test has **already been run on IBM hardware twice** (Lancaster & Palladino; Batle et al.), and the no-signalling question has **already been checked on a Heron r2 device** (ibm_kingston, in Bednorz et al. 2025). Both are recorded below.

---

## A. Real vs complex quantum theory

### Renou et al. (real QT falsifiable): Renou, Trillo, Weilenmann, Le, Tavakoli, Gisin, Acín, Navascués, 2021, Nature 600, 625. https://arxiv.org/abs/2101.10873
- read_depth: full (arXiv PDF main text; supplementary material not read)
- what_tested: theory and proposal. Real and complex QT give different predictions in an entanglement-swapping network with two independent sources (A–B1 and B2–C). Bob performs a Bell-state measurement; Alice and Charlie measure locally.
- on_whom: no hardware.
- how_scored: functional T, the sum of CHSH3 variants for each of Bob's four outcomes, weighted by the probability of that outcome. Complex QT reaches 6√2 ≈ 8.49. The real-QT bound, found numerically with an NPA-type hierarchy, is T ≲ 7.66, and "It remains open, whether this upper bound is tight."
- result: beating 7.66 needs each distributed state to have visibility above sqrt(7.66/(6√2)) ≈ 0.95.
- limits: the real-QT claim depends on the *independence of the two sources*, meaning tensor-product preparations. The bound is numerical and may not be tight. Because T is linear, the bound still holds with shared randomness, so the i.i.d. assumption can be dropped.
- borrow: the 0.95-visibility threshold per source as a go/no-go check from calibration data; the linearity argument for non-i.i.d. hypothesis testing.
- next_steps_it_suggests: experimental realisation; proving whether 7.66 is tight.

### Chen et al. (superconducting real-QT test): M.-C. Chen, C. Wang, F.-M. Liu, …, A. Cabello, C.-Y. Lu, J.-W. Pan, 2022, PRL 128, 040403. https://arxiv.org/abs/2103.08123
- read_depth: full (main text; supplementary not read)
- what_tested: the Renou game with a deterministic Bell-state measurement on superconducting qubits.
- on_whom: a custom 4-qubit linear transmon chip (USTC) with iSWAP-based gates. 12 setting combinations (xz), 16 outcome strings each. Shots are not stated in the main text.
- how_scored: Γ = Σ w·P(abc|xz). Classical bound 6, real-QT bound 7.66, complex maximum 6√2 ≈ 8.49.
- result: Γ = 8.09(1), which is 43σ above 7.66. Mean conditional Alice–Charlie Bell fidelity 0.952(1), against a threshold of about 0.927. T1 is 34.8 µs on average, T2* 8.0 µs, 1q gates 99.88%, iSWAP process fidelity 96.7%.
- limits: Alice's and Charlie's qubits sit on one chip, so source independence is assumed from the tensor-product axiom. No locality and no independent sources. The abstract garbles the numbers ("fidelity of 0.952(1), which beats the real-number bound of 7.66"); the score is 8.09(1).
- borrow: per-step tomography checkpoints (EPR pair, then four-qubit state, then conditional Bell states) as a diagnostic chain; the 0.927 conditional-fidelity threshold.
- next_steps_it_suggests: none beyond the claim itself.

### Li et al. (photonic real-QT test): Z.-D. Li, Y.-L. Mao, M. Weilenmann, A. Tavakoli, …, J. Fan, 2022, PRL 128, 040402. https://arxiv.org/abs/2111.15128
- read_depth: abstract (only the abstract was opened)
- what_tested: real-QT bound in a three-party network with "two independent EPR sources".
- on_whom: photons. No further numbers in the abstract.
- result: violation of the real-QT bound by more than 4.5σ (abstract).
- Does not transfer: its value is truly independent photon sources, which a single chip cannot supply.

### Lancaster & Palladino (real-QT test on IBM cloud): 2022–2024, accepted at Am. J. Phys. https://arxiv.org/abs/2205.01262
- read_depth: full (arXiv HTML v3; supplementary not read)
- what_tested: the Renou/Chen Γ game on IBM cloud devices.
- on_whom: Sampler runs on ibmq_lima, ibmq_manila, ibm_lagos and ibm_nairobi used 12 circuits (one per αγ setting) with 20,000 or 32,000 shots per setting and 9–44 trials. Estimator runs on ibm_osaka, ibm_kyoto, ibm_brisbane and ibm_kyiv used one trial each. The circuits use 4 qubits.
- how_scored: Γ against 7.6605 (real) and 8.485 (complex).
- result (readout-mitigated): lagos 8.065 ± 0.060; nairobi 8.399 ± 0.060; kyoto 8.097 ± 0.057; brisbane 8.054 ± 0.077; kyiv 8.028 ± 0.043; lima 7.689 ± 0.039; manila 7.810 ± 0.144; osaka 7.500 ± 0.128. **Unmitigated results "generally fall below" 7.66.** The exception is ibm_kyiv (Estimator, uncorrected) at 7.840 ± 0.029. Estimator resilience level 2 gave "erroneously high correlations."
- limits: the authors say cloud Bell tests "does not allow one to address such loopholes." Real constructions that break the tensor-product structure are not excluded. The bound may not be tight.
- borrow: **the warning that heavier mitigation inflates correlations**, so any pre-registration should score on raw counts. Device-to-device spread is about ±0.3 in Γ.
- next_steps_it_suggests: student projects; extending the method to multipartite nonlocality.

### Batle et al. (efficient real/complex discrimination on IBM): J. Batle, T. Białecki, T. Rybotycki, J. Tworzydło, A. Bednorz, 2024–2025, arXiv 2405.03013. Published in Quantum per the journal listing in search; the arXiv v2 I read names no journal. https://arxiv.org/abs/2405.03013
- read_depth: full (arXiv HTML v2)
- what_tested: a new real-vs-complex functional ℱ with fewer settings. A and C each have 3 settings; B has 6 settings with 4 outcomes.
- on_whom: ibm_brisbane (Eagle), qubits 47 (A), 48 (P), 49 (Q) and 55 (C). 18 correlations, 6 jobs, 20,000 shots.
- how_scored: classical bound 12; real bound 6√6 ≈ 14.6969; complex maximum 18.
- result: ℱ = 15.4436 ± 0.0066, **without error mitigation**, which is "more than 100 standard deviations" above the real bound. The authors found no significant signalling in these data.
- limits: no locality; efficiency loophole open; source separability assumed. IBM distances and times cannot rule out signalling. Optimality of the test and of the bound is open.
- borrow: the 18-correlation design (cheaper than 12 settings × 16 outcomes); unmitigated scoring; checking no-signalling marginals inside the same data set.
- next_steps_it_suggests: run at larger distances to close locality; settle whether the bound is optimal.

**Verdict for real vs complex on Heron r2: settled, replication only.** A Heron run adds nothing foundational. The independent-source assumption cannot be met on one chip, and replacing Bob's Bell measurement with a mid-circuit one plus feed-forward does not change the logic. As a calibration it costs 18 circuits × 2,000 shots = 36,000 shots ≈ 10 s + 2 s ≈ 12 s.

---

## B. psi-ontology (PBR and maximally psi-epistemic bounds)

### PBR theorem: Pusey, Barrett, Rudolph, 2012, Nature Physics 8, 475. https://arxiv.org/abs/1111.3328
- read_depth: full (arXiv v3)
- what_tested: theorem. If systems prepared independently have independent ontic states (preparation independence), then psi-epistemic models contradict QT.
- on_whom: no hardware.
- how_scored: the noise-tolerant version. If every observed outcome probability is within ε of QT, then D(µ0,µ1) ≥ 1 − 2ε^{1/n} for 2^{1/n} − 1 ≤ tan(θ/2).
- result: n/a.
- limits: needs preparation independence. Needs high-fidelity gates "in a non post-selected fashion", because post-selection lets the device dodge the zero-probability outcomes.
- borrow: **no post-selection** is a hard rule for any PBR run. The bound is model-independent given ε, so no noise model is needed.
- next_steps_it_suggests: implement the circuit for small n.

### Nigg et al. (first PBR test; trapped ions): D. Nigg, T. Monz, P. Schindler, E. A. Martinez, M. Chwalla, M. Hennrich, R. Blatt, M. F. Pusey, T. Rudolph, J. Barrett, 2016, NJP 18, 013007. https://arxiv.org/abs/1211.0942
- read_depth: full (arXiv PDF)
- what_tested: the 2-qubit PBR test with |φ0,1⟩ = cos(π/8)|1⟩ ± sin(π/8)|0⟩. The joint measurement is a conditional phase gate (α = π, β = 0) followed by Hadamards.
- on_whom: **two 40Ca+ ions (trapped ions), not superconducting.** 4 input states, "up to 10000" repetitions each.
- how_scored: forbidden-outcome probabilities ε_k. A crosstalk-aware bound (Eq. 12) gives D(µ0,µ1) + D(µ0,µ0') + D(µ1,µ1') ≥ 1 − 2√ε. Matching quantum trace distances would need ε ≥ 1.83%.
- result: ε_k = {1.88%, 1.04%, 0.6%, 1.04%}, mean ε = (1.14 ± 0.15)%, a violation of more than 4.5σ, p < 10^-5 for a psi-epistemic model.
- limits: the ions are adjacent. Single-ion addressing crosstalk (κ ≈ 1%) creates a "potential state preparation loophole", which they handle by modelling the modified preparations. Preparation independence rests on QT's own product-state assignment.
- borrow: **fold measured preparation crosstalk into the bound**, rather than assuming ideal states. The 1.83% threshold is the yardstick for the 2-qubit π/8 states.
- next_steps_it_suggests: preparations "independent by any reasonable scientific judgement", such as spacelike separated and separately built.

### Ringbauer et al. (measurements on the reality of the wavefunction): M. Ringbauer, B. Duffus, C. Branciard, E. G. Cavalcanti, A. G. White, A. Fedrizzi, 2015, Nature Physics 11, 249. https://arxiv.org/abs/1412.6213
- read_depth: full (arXiv v2, including Methods)
- what_tested: bounds on maximally (and partially) psi-epistemic models through the ratio of classical to quantum overlap, with **no preparation-independence assumption**. Requires d ≥ 3.
- on_whom: heralded single photons dual-encoded in polarisation and path, d = 3 and d = 4, real-amplitude states. About 2 × 10^4 coincidences per measurement, 10 s per setting.
- how_scored: S = Σ P(forbidden outcomes)/ωq ≥ 1 for maximally psi-epistemic models. Here ωq = 1 − sqrt(1 − |⟨ψ|φ⟩|²), computed from the intended states using QT.
- result: for n = 10 ququart (d = 4) states, S = 0.690 ± 0.001, a violation of "more than 250 standard deviations."
- limits: relies on **fair sampling**. Without it, detection efficiency above about 98% is needed, with 0.976 the lowest threshold (d = 4, n = 5). The authors note this "might be achievable in ... superconductors" but qudit control was not yet shown. The inequality is not theory-independent, because ωq comes from QT. Accurate state preparation is crucial.
- borrow: a d = 4 test is two transmons used as one ququart with real amplitudes. **A transmon readout gives an outcome on every shot, so the fair-sampling assumption disappears** and readout error becomes plain noise counted in S.
- next_steps_it_suggests: optimise states and measurements to lower the efficiency threshold.

### Yang, Yuan & Barnes (PBR on Heron2): S. Yang, H. Yuan, C. H. W. Barnes (Cambridge), Oct 2025, arXiv 2510.11213 (preprint). https://arxiv.org/abs/2510.11213
- read_depth: full (arXiv HTML v1)
- what_tested: PBR for n = 2 and n = 5 on IBM hardware, as a function of qubit separation.
- on_whom: **ibm_marrakesh (Heron2, 156 q)**. 20 adjacent pairs (10 best and 10 worst CZ), giving 80 circuits. Five-qubit groups: 5 configurations. Distant pairs at d = 2…8 and at qubit 0 ↔ 155. **100,000 shots per circuit.** No named error mitigation.
- how_scored: forbidden-outcome frequency against a tolerance ε_tol = (1 − D)^n / 2^n, plus noise-model variants: n = 2 thermodynamical 2.72 ± 0.36%, depolarising 2.14 ± 0.10%; n = 5 thermodynamical 0.63 ± 0.41%, depolarising 0.55 ± 0.09%.
- result: adjacent pairs at θ0 = π/4: best 0.17 ± 0.02%, worst 0.56 ± 0.03%; about 97.5% of the 80 circuits pass. At 1.2θ0, nearly all pairs fail (2.19–4.62%). n = 5 at θ0: 0.32 ± 0.10% / 0.48 ± 0.18%. Distant pairs rise to 1.07% (best) and 6.91% (worst) at d = 8. Full span is 6.30 ± 0.65% and fails.
- limits: **the pass threshold comes from the authors' own noise model, which makes the scoring partly circular.** The text calls passing a "violation" of the bound, which contradicts its own pass definition. The abstract says the results rule out the epistemic view, while the conclusion says the rejection "remains contingent on the noise characteristics." Idle errors are neglected, and the simple noise models under-estimate errors in deep circuits.
- borrow: the **actual Heron-generation numbers**: about 0.2–0.6% forbidden-outcome rates on adjacent pairs, which is about 3–10× below the 1.83% Nigg threshold. Also the warning that SWAP routing destroys the margin.
- next_steps_it_suggests: larger n, other angles, use as a device benchmark, compare with Quantum Volume and XEB.

**Verdict for PBR on Heron r2: settled, replication only.** The 2-qubit π/8 test already passes on a Heron2 device by a large margin. A clean replication that scores with the model-independent PBR/Nigg bound rather than a noise model costs 4 circuits × 4,000 shots = 16,000 shots ≈ 4.5 s + 2 s ≈ 7 s. **The Ringbauer-type d = 4 test without fair sampling looks unrealised on superconducting hardware (one search, not exhaustive).** It is listed below as a narrow open item.

---

## C. Born rule and higher-order interference

### Białecki et al. (Born rule as an accuracy test of IBM): T. Białecki, T. Rybotycki, J. Tworzydło, A. Bednorz, 2022, arXiv 2112.07567 (v3). https://arxiv.org/abs/2112.07567
- read_depth: partial (abstract, Sections I–IV; appendices skimmed)
- what_tested: a single-qubit "Born rule" test. Prepare S_θ^n S|0⟩ and check that p(1) = A_n sinθ + B_n cosθ + C_n, i.e. linear in the first harmonics of θ, using virtual-Z frame changes. Deviations need a larger Hilbert space, θ-dependent ρ, M or S, or a non-diagonal M.
- on_whom: IBM lima, jakarta, bogota, lagos, perth and armonk (1 qubit). 16 angles θ = jπ/8, shuffled within each job. 8192 shots per job (later 20,000, 32,000 or 100,000), 56 circuits per angle per job, about 100 jobs. Armonk took more than 1,500 jobs. Data were collected over 2021–2022.
- how_scored: residuals from the 3-parameter fit, in units of the binomial σ.
- result: deviations "at the level 10−3" relative, beyond 5σ, θ-dependent, similar across devices. Some are not explained by waveform-generator nonlinearity. The magnitude is comparable to RB error, but with a clear dependence on θ.
- limits: the cause is unknown. Candidates are leakage to |2⟩ and imperfect pulses. It needs about 10^7–10^8 shots, far beyond our budget.
- borrow: **shuffle angles within each job** and fit the affine form exactly predicted by QT plus a 2-level system. This is a clean null-hypothesis design.
- next_steps_it_suggests: use it as a diagnostic tool for gate implementations.

Higher-order (Sorkin) interference: **no superconducting or IBM test found.** The hits were photonic (5-path, arXiv 1508.03253) and an NV-spin qutrit (arXiv 1612.08563, not opened). On qubits, three "paths" would have to be built as a single excitation spread over 3 qubits by compiled gates, so a Sorkin test would only check gate compilation. Doing it properly needs qutrit control, which Open Plan does not offer. Killed.

---

## D. Objectivity, no-signalling and quantum Darwinism

### Rybotycki et al. (no-signalling violation on IBM): T. Rybotycki, T. Białecki, J. Batle, A. Bednorz, 2024–2025, Adv. Quantum Technol. (per search), arXiv 2409.11348. https://arxiv.org/abs/2409.11348
- read_depth: full (arXiv HTML v2)
- what_tested: whether one qubit's marginal depends on the other's setting, in three tests: (a) a Bell pair via a source qubit, (b) idle neighbours, (c) idle fourth neighbours.
- on_whom: ibm_sherbrooke, brisbane, kyoto and kyiv (all Eagle). 20,000 shots × 60 jobs (kyiv: 7,500 × 58–60). 25 repetitions per setting pair, so 100 circuits per job. About 3 × 10^7 trials in total. Settings α ∈ {0, π/2} and β ∈ {±π/4} differ by phase only.
- how_scored: δP = P_{a0}(+*) − P_{a1}(+*) and the mirror quantity; σ ≈ 1.3 × 10^-4 (6.4 × 10^-5 for test c).
- result: large violations, up to δP ≈ 510 × 10^-4 on sherbrooke 117-118-119, with idle test (b) as large as (a). Test (c), pair 49-66: about ±3.3 × 10^-4 (about 5σ), p = 5.3 × 10^-17 after look-elsewhere correction. CHSH 2.2–2.6. The effect is strongest at small detuning but persists at 230 MHz.
- limits: ZZ crosstalk argued out (phase-only settings) but not fully excluded. An AWG/LO/IQ phase–amplitude correlation or a cable fault is possible. Subluminal signalling cannot be excluded at IBM scales.
- borrow: **the idle test (b)** (no entangling gate, settings by phase only) is the cleanest null test for setting leakage. Run many pairs in parallel; correct for look-elsewhere.
- next_steps_it_suggests: technical root cause; rerun loophole-free Bell tests with much more data.

### Bednorz et al. (closing the objectivity loophole): A. Bednorz, J. Batle, T. Białecki, J. K. Korbicz, 2025, arXiv 2506.08940 (SciPost submission). https://arxiv.org/abs/2506.08940
- read_depth: full (arXiv HTML v2)
- what_tested: a CHSH test in which each outcome is first made "objective". The outcome is copied by CNOT to 3 "friends" per side, and a trial counts ±1 only on unanimity (000 → +1, 111 → −1, otherwise 0). The framing comes from quantum Darwinism and spectrum broadcast structures.
- on_whom: ibm_brisbane and sherbrooke (Eagle), **ibm_torino (Heron r1), ibm_kingston (Heron r2)**, and IonQ Forte. 7 qubits per group on IBM, 6 groups per device. 60 jobs × 20,000 shots, 25 repetitions per setting, N = 3 × 10^7.
- how_scored: B against 2; errors about 2.6–2.9 × 10^-4.
- result: **kingston (Heron r2): B = 2.535, 2.045, 2.478, 2.379, 2.443, 2.444, all above 2, with no-signalling "within statistical error."** Torino has one group with signalling and B as low as 1.493. Sherbrooke shows "the most serious signaling." IonQ: 2.569 ± 0.0024, with some signalling.
- limits: no locality; freedom of choice assumed; qubits are majority-voted rather than traced out. The source of the signalling on Eagle is unidentified. A referee report (search snippet, not read) questions the claim of closing a loophole while signalling remains.
- borrow: **Heron r2 is the clean device class for no-signalling at the 10^-4 level.** The unanimity-scored Bell test is a direct measure of how much quantumness survives outcome redundancy.
- next_steps_it_suggests: "limits on distance and on the number of friends"; identify the source of the signalling.

### Zhu et al. (quantum Darwinism with superconducting circuits): Z. Zhu, …, R. Mondaini, A. Touil, et al., 2025, Science Advances (per PMC), arXiv 2504.00781. https://arxiv.org/abs/2504.00781
- read_depth: partial (first 100k characters of arXiv HTML v2: main text and most of the supplement)
- what_tested: a demonstration of QD predictions: branching states, a mutual-information plateau, vanishing discord, and robustness to scrambling. It also proposes a local-observable witness.
- on_whom: Zhejiang 121-qubit, 220-coupler processor. Sub-lattices of 3×3 (1 system qubit, 4 environment, 4 auxiliary) and 3×4 (2 system, 10 environment). Median CZ error 0.246%, readout error about 0.66%. Full tomography on 5 qubits (3^n settings), averaged over 5 runs. Shots are not given in the text I read.
- result: at m = 4, θ = π/2, I(S:F) ≈ 1.83; discord near 0 until the whole environment is captured.
- limits: tomography does not scale; a finite environment leaves residual coherence.
- Does not transfer as a falsification test: the "environment" is a set of programmed qubits, so the plateau is a QT prediction for the compiled unitary and the only way to "fail" is gate noise. Chen et al. 2019 (photons) and Unden et al. 2019 (NV) are cited there but not opened.

---

## E. Superdeterminism and measurement dependence

### Hossenfelder & Palmer (rethinking superdeterminism): S. Hossenfelder, T. N. Palmer, 2020, Front. Phys. 8:139. https://arxiv.org/abs/1912.06462
- read_depth: partial (abstract, Sec. 6 "Experimental Test"; the rest skimmed)
- what_tested: proposal only. Superdeterministic theories with environment-borne hidden variables predict *time correlations* between outcomes on near-identically prepared systems in place of Born statistics.
- on_whom: no hardware.
- how_scored: not specified. The proposal says to look for short-term regularities that "according to quantum mechanics alone, should not exist."
- result: n/a. The prescription is "devices as small and cool as possible in time-increments as small as possible"; failing that, repeated measurements of non-commuting observables on the same state.
- limits: the authors say the required similarity of states cannot be fixed without a model.
- borrow: the lever is time spacing. **Mid-circuit measurements within one shot (µs spacing) are the right regime; shot-to-shot spacing (about 250 µs) is not.**
- next_steps_it_suggests: model-specific predictions.

### Hossenfelder (testing superdeterministic conspiracy): S. Hossenfelder, 2014, arXiv 1401.0286 (conference proceedings). https://arxiv.org/abs/1401.0286
- read_depth: full (4 pages)
- what_tested: proposal. Alternate measurements of two non-commuting observables on the same system. QT predicts uncorrelated outcomes, so the pass probability decays exponentially. An environment-induced superdeterministic theory predicts Corr_κ = exp(−κ/τ) with τ > 0.
- on_whom: no hardware. Her estimate for a µm-scale detector is τ̃ ≈ 10^-6 s.
- how_scored: the autocorrelation of same-observable outcomes against the measurement index κ. Standard QT is the limit τ → 0.
- limits: "cannot test generic superdeterminism, but only certain types" (attributed to the von Neumann and Schrödinger discussion). It assumes the hidden variables are environmental and decorrelate as a Poisson process.
- borrow: **this maps directly onto a Heron dynamic circuit**: alternate Z and X readouts on one qubit via H between mid-circuit measurements, in parallel on many qubits.
- next_steps_it_suggests: build it with small, cold, fast detectors.

No hardware test of either proposal was found in two searches.

---

## F. Calibration: GHZ size and measurement-induced transitions

### Big cats (120-qubit GHZ, IBM): IBM Quantum authors, Oct 2025, arXiv 2510.09520. https://arxiv.org/abs/2510.09520
- read_depth: partial (arXiv HTML v1, main text)
- what_tested: GHZ fidelity at scale, using adaptive compilation, parity-check post-selection and temporary uncomputation.
- on_whom: 120-qubit GHZ on ibm_aachen (CNOT depth 18, 8 parity ancillas). 100-qubit GHZ on ibm_kobe, ibm_kingston and **ibm_fez**. Shots are not stated in the text I read.
- result: 120 q: F = 0.56(3) at post-selection rate 0.28. 100 q (DFE): kobe 0.70(4) at 0.36; kingston 0.55(3) at 0.28; **fez 0.46(4) at 0.14**, or 0.68(3) at 0.04 with non-Markovian post-selection. Kingston parity oscillations 0.513(8).
- limits: post-selected; no nonlocality claim; Z errors only partly caught.
- borrow: **ibm_fez is the weakest of the three Heron r2 devices for large-entanglement work.** Budget accordingly. Post-selection is incompatible with PBR- or Bell-type claims.
- Does not transfer as a foundations test: GHZ fidelity is a calibration figure, not a falsifiable assumption.

### Koh et al. (MIPT on IBM): J. M. Koh, S.-N. Sun, M. Motta, A. J. Minnich, 2023, Nat. Phys. 19, 1314. https://arxiv.org/abs/2203.04338
- read_depth: partial (arXiv PDF main text and Methods)
- what_tested: volume-law to area-law crossover under mid-circuit measurement.
- on_whom: L ≤ 5 with QST on lagos, perth, jakarta and casablanca. L ≤ 14 for S2 on hanoi, cairo, kolkata, auckland and washington. At least 100–300 random circuits per (p, η) point, at least 1000 × 2^m shots per MUB, and trajectories with ≤ 128 shots discarded.
- Does not transfer: the cost of post-selecting trajectories scales exponentially in the number of mid-circuit measurements, and the transition is a QT prediction rather than an assumption. No sub-100-s falsifiable version exists.

---

## Cluster summary

### Open questions that fit our budget

1. **Do repeated non-commuting measurements on one qubit show the time correlations an environment-induced superdeterministic theory predicts (Hossenfelder 2014, Hossenfelder & Palmer 2020 §6)?**
   - Who came closest: nobody on hardware, from two searches. The closest data are sequential-measurement contextuality and Leggett–Garg runs, which use different hypotheses; **coordinate with the LG/randomness and sequential-contextuality readers.**
   - Why open: the proposal names µs time spacing and small, cold detectors. Heron mid-circuit readout is exactly that regime, and no one has published the autocorrelation analysis.
   - Test: 50 non-adjacent qubits in parallel. Per qubit: H, then 8 mid-circuit measurements with an H between each pair (Z, X, Z, X…), all outcomes stored. Control circuit: the same with no H between measurements (Z, Z, Z…, a QND-repeatability check giving the classical-correlation ceiling). 2 circuits × 4,000 shots = 8,000 shots. Mid-circuit measurement duration not verified from a text I read.
   - Cost: about 2.2 s + 2 s ≈ **5 s**, one job. That gives 200,000 eight-measurement records per circuit.
   - Pre-registered criterion:
     - QT passes if, for every lag κ ∈ {2, 4, 6} between same-observable measurements, the pooled correlation satisfies |Corr_κ| < 0.01. The pooled statistical σ is about 1/sqrt(200,000 × (8 − κ)) ≈ 1 × 10^-3. The 0.01 allowance covers H-gate and readout error (about 10^-3 to 10^-2).
     - The run-length distribution of repeated "pass" outcomes must match 2^-k.
     - Falsifies QT plus Markovian noise if Corr_2 > 0.05 with a 5σ excess over the H-gate error budget. A τ that is not tiny compared with the measurement spacing predicts exp(−2·Δt/τ), i.e. order 0.1.
     - Null result: report it as an upper bound on τ in units of the mid-circuit spacing.

2. **Does a maximally psi-epistemic bound (Ringbauer-type, d = 4) fall on two transmons with no fair-sampling assumption?**
   - Who came closest: Ringbauer et al. 2015 with photons, S = 0.690 ± 0.001, but with fair sampling assumed. Without it, efficiency above about 98% is needed. Yang et al. 2025 ran only PBR, which needs preparation independence, on Heron2.
   - Why open: no superconducting d ≥ 3 psi-epistemic test was found. Transmon readout returns an outcome on every shot, so the detection loophole Ringbauer names disappears. The question is whether Heron's two-qubit preparation and measurement errors keep S below 1.
   - Test: encode a ququart in 2 qubits with real amplitudes (RY plus one CZ for preparation and the reverse for measurement). Use n = 5 states ψ0…ψ4 and measurements M_{j1j2} for the 10 pairs, each applied to the 3 relevant states: 30 circuits × 2,000 shots = 60,000 shots. Compute ωq from the intended states, plus a sensitivity analysis using states reconstructed by 2-qubit tomography (+9 circuits × 1,000 shots).
   - Cost: about 19 s + 2 s ≈ **21 s**.
   - Pre-registered criterion: the maximally psi-epistemic hypothesis is rejected if S + 5σ < 1 under both ωq choices. "Inconclusive on Heron r2" if S ≥ 1 under either choice. This is genuinely uncertain, because forbidden-outcome rates of 0.2–0.6% per CZ pair (Yang et al.) must stay small against ωq values that are themselves small. **The answer is new (loophole-wise) but not a challenge to QT. Be honest that the inequality uses QT to compute ωq.**

3. **How many "friends" (redundant outcome copies) can a Bell violation survive on Heron r2 under unanimity scoring (Bednorz et al. 2025, "limits ... on the number of friends")?**
   - Who came closest: Bednorz et al. with k = 3 friends per side on ibm_kingston, B up to 2.535 with no signalling.
   - Why open: the authors list k-scaling and distance as next steps. QT predicts 2√2 for every k, so the curve B(k) on fez measures how much quantumness survives outcome objectivity. This is closer to a calibration than a falsification. Our fez device is weaker than kingston.
   - Test: in one circuit, run parallel groups with k = 1, 3, 7 and 15 friends per side (CNOT fan-out trees). Each group is a source qubit M → A0, B0 with a middle-qubit separation, and phase-only settings α ∈ {0, π/2}, β ∈ {±π/4}. Use 4 setting circuits; randomise which group gets which setting by using 8 circuits with permuted assignments. 8 circuits × 5,000 shots = 40,000 shots. σ_B ≈ 2/sqrt(10,000) = 0.02 per group.
   - Cost: about 11 s + 2 s ≈ **13 s**.
   - Pre-registered criterion: k* is the largest k with B_k > 2 + 5σ, with no-signalling marginals |δP| < 5σ in the same data. A signalling violation voids that group. Report B(k) against the depolarising prediction from published fez CZ/readout errors as a secondary, exploratory comparison.

4. **(Cheap screening, overlaps with the noise-gaps reader.) Does ibm_fez show the gross setting-dependent marginals seen on Eagle devices, or is it clean like kingston?**
   - Evidence: Rybotycki et al. saw δP up to about 5 × 10^-2 on Eagle; Bednorz et al. found none on kingston at about 3 × 10^-4 precision.
   - Test: idle test (b) on about 40 disjoint neighbour pairs in parallel, phase-only settings, 16 circuits with balanced pseudo-random setting assignment per pair, 6,250 shots each = 100,000 shots. That gives 25,000 shots per pair-setting combination, σ(δP) ≈ 4.5 × 10^-3.
   - Cost: about 28 s + 2 s ≈ **30 s**. A 4-circuit × 10,000-shot version (about 13 s) detects only δP of at least about 0.03.
   - Criterion: signalling is flagged if |δP| > 4.5σ after Bonferroni over 160 tests. This is mostly a replication of the kingston null; it is worth running only if the noise-gaps reader does not already plan it.

Replication-only items, should a calibration slot be wanted:
- **PBR, model-independent scoring.** 4 circuits × 4,000 shots, about 7 s. Passes if max ε_k < 1.83% − 5σ with no post-selection; expect about 0.2–0.6%.
- **Real vs complex, Batle 18-correlation form, unmitigated.** About 12 s. Passes if ℱ > 14.697 + 5σ.

### Questions that do not fit
- Real vs complex as a *foundations* test: settled three times on hardware (Chen 43σ; Batle more than 100σ on IBM; Lancaster–Palladino on 8 IBM devices). Truly independent sources are impossible on one chip.
- PBR proper: already passed on Heron2 (Yang et al. 2025). The preparation-independence loophole cannot be closed on a chip, because the qubits share a fridge and a control stack.
- Sorkin / higher-order interference: needs qutrits or genuine multi-path systems. A qubit encoding only tests compiled gates.
- Peres real/complex/quaternionic interferometric tests: photonic multi-path. Not searched in depth; same objection as Sorkin.
- Białecki-type single-qubit Born-rule deviations at 10^-3: need about 10^7–10^8 shots, roughly 3,000–30,000 s.
- Quantum Darwinism (Zhu 2025 style): a demonstration of QT on an engineered environment, so there is no assumption at stake. Full tomography is also expensive.
- Frauchiger–Renner: no hardware runs found. On a chip it only checks the QT Hardy-type probability; the paradox is about reasoning rules. The Wigner's-friend / local-friendliness reader covers this.
- Quantum switch / indefinite causal order: no superconducting implementation found (searched). Simulating it on a chip uses gates in a definite order, so it tests nothing about causal structure.
- MIPT (Koh 2023): post-selection cost exponential in mid-circuit measurements, and the transition is a QT prediction.
- Large-N Mermin/GHZ: a calibration, not open foundations. Big cats already gives fez GHZ-100 F = 0.46(4) post-selected. Mermin violation at large N needs only modest coherence but is not loophole-free and settles nothing new.
- Anything spacelike: impossible on one chip.

### Fields searched that returned nothing relevant
- Higher-order (Sorkin) interference on superconducting or IBM qubits: none found.
- Superdeterminism hardware tests on any quantum processor: none found.
- Quantum switch / indefinite causal order on superconducting hardware: none found (only photonic, plus a theory paper, arXiv 2109.14951, not opened).
- Frauchiger–Renner on IBM hardware: none found (only proposals, e.g. arXiv 2606.15467, not opened).
- Maximally psi-epistemic tests on superconducting or ion hardware without fair sampling: none found.
- Mermin violations above about 7 qubits on IBM: none found in one search.
