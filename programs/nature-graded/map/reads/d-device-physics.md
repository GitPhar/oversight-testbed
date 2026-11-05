# Reads: device physics — why `AerSimulator.from_backend` misses Heron r2 hardware

Reader cluster: noise-model fidelity vs IBM Heron r2 (`ibm_fez`). Date of reads: 2026-11-04.
Our own data (NOT from any paper): 9 qubits, depth 208, 117 CZ: P(yes) 0.50 hardware / 0.25 from_backend sim / 0.29 ideal (1,000 shots, z ≈ 12). Several per-qubit marginals crossed 0.5 (one: P(1) 0.75 ideal → 0.30 hardware). Two-qubit tomography after 137–230 CZ: negativity 0.063 vs 0.149, 0.067 vs 0.118, 0.147 vs 0.171 (hardware vs noisy sim).

## Two things to fix in our own reasoning first (from reading the Aer source and docs)

1. **Idle qubits get no noise in Aer unless the circuit is scheduled.** In `qiskit_aer/noise/noise_model.py` (main branch, read 2026-11-04), `from_backend` attaches thermal relaxation to idle time only through a `RelaxationNoisePass` with `op_types=Delay`. That pass acts only on explicit `Delay` instructions. A circuit transpiled without a `scheduling_method` contains no delays, so qubits waiting during a depth-208 circuit have no T1/T2 decay in the simulation. On hardware they decay. This alone could explain much of the gap. Checking it costs zero QPU seconds: re-simulate the same ISA circuit after scheduling it ALAP with the backend's durations.
2. **"Incoherent noise cannot push a marginal across 0.5" holds only for unital noise applied at the end of the circuit.** Amplitude damping (T1) is non-unital and pulls P(1) toward 0, not toward 0.5. Readout error on Heron is also usually asymmetric (1→0 more likely). A drop from 0.75 to 0.30 is therefore the *direction* T1, idle decay and 1→0 readout errors push. Stochastic Pauli errors in the middle of the circuit are also spread by later gates into branches whose marginals need not centre on 0.5. So crossings alone do not prove coherent error. **Free check on data we already have:** did every crossed marginal move *down* (toward 0)? If all moved down, excess relaxation, idle decay or readout asymmetry is the leading suspect. Any qubit that crossed *upward* points to coherent error, leakage (|2⟩ read as 1) or crosstalk.

---

### Aer NoiseModel.from_backend (docs + source) — Qiskit Aer devs, 0.18.2 docs / main-branch source, https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.noise.NoiseModel.html ; https://github.com/Qiskit/qiskit-aer/blob/main/qiskit_aer/noise/noise_model.py ; .../noise/device/models.py
- read_depth: full (docs page; source functions `from_backend`, `basic_device_readout_errors`, `_device_depolarizing_error`)
- what_tested: n/a (software documentation)
- on_whom: n/a
- how_scored: n/a
- result: Each 1q/2q gate gets a depolarising error followed by a thermal-relaxation error. For 2q gates, relaxation is single-qubit on each participant, so the model has **no correlated 2q coherent term, no ZZ, no crosstalk to spectators**. The depolarising parameter is set so that depolarising composed with relaxation reproduces the reported gate error (`p = dim·(F_relax − F)/(dim·F_relax − 1)`). The reported error is therefore converted *entirely* into Pauli-symmetric noise. Readout is a per-qubit 2×2 matrix: asymmetric if the Target exposes `prob_meas1_prep0`/`prob_meas0_prep1`, otherwise symmetric `prop.error`. `temperature` defaults to 0, so there is no residual excited-state population. T2 is truncated to ≤ 2T1. Idle relaxation applies only to explicit `Delay` instructions (see above). The docs call it "An approximate noise model for the device backend." The docs list no omissions; by construction it omits coherent over- and under-rotation, residual ZZ, drive crosstalk, leakage, non-Markovian and time-varying noise, measurement-induced spectator errors and state-preparation (reset) error.
- limits: Static snapshot of one calibration. Per-gate errors come from IBM's reported values, which are themselves RB-type averages.
- borrow: Re-simulate with (a) an ALAP-scheduled circuit, (b) `temperature>0`, and (c) an added `coherent_unitary_error` ZZ phase on each CZ pair. Then see which of these reproduces the marginal pattern. All free.
- next_steps_it_suggests: none stated.

### qiskit-ibm-runtime SamplerV2 options and repetition-rate guide — IBM, current docs, https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/options-twirling-options ; .../options-dynamical-decoupling-options ; .../options-sampler-execution-options-v2 ; https://quantum.cloud.ibm.com/docs/en/guides/repetition-rate-execution
- read_depth: full (four pages)
- what_tested: n/a
- on_whom: n/a
- how_scored: n/a
- result: **SamplerV2 applies no twirling and no DD by default.** `TwirlingOptions.enable_gates`: "For the Sampler: False". `enable_measure`: Sampler False. `num_randomizations` and `shots_per_randomization` default "auto", `strategy` "active-accum". `DynamicalDecouplingOptions.enable` default False; when enabled, `sequence_type` defaults to "XX" and scheduling to "alap". (Estimator is different: gate twirling turns on at resilience level 2, measurement twirling at levels 1 and 2.) **rep_delay**: "Default is given by `backend.default_rep_delay`". It can be set only from `backend.rep_delay_range`, and only on backends with `dynamic_reprate_enabled=True`. The guide says lowering it shortens QPU time "at the expense of increasing the state preparation error rate", and that values "are not the same for every QPU and can also change over time". `init_qubits` defaults True.
- limits: The docs give **no Heron or ibm_fez rep-delay numbers**. I found no public source stating ibm_fez's `rep_delay_range`. The ~250 µs in our cost rule is our own inference, not a documented default.
- borrow: Read `backend.configuration().dynamic_reprate_enabled`, `.rep_delay_range` and `.default_rep_delay` for ibm_fez (free, no QPU). If the lower bound is well below 250 µs, cost per shot could drop by up to roughly 2×. That trades for more state-prep error, which matters most for *this* question because it adds residual |1⟩ population the sim does not model. Do not lower it for the discrimination tests.
- next_steps_it_suggests: "Always verify the supported `rep_delay` range for the specific QPU".

### Layer fidelity / EPLG — McKay, Hincks, Pritchett, Carroll, Govia, Merkel, 2023, arXiv:2311.05933, https://arxiv.org/abs/2311.05933
- read_depth: full (v1)
- what_tested: Layer fidelity (LF) of a connected chain of 2q gates. Built from simultaneous direct RB on disjoint sub-layers; EPLG = 1 − LF^(1/n₂q).
- on_whom: ibm_sherbrooke (127q Eagle, CX) and **ibm_montecarlo (133q Heron, tunable coupler, CZ)**. Chains up to 100 qubits. 300 shots/circuit, 6 randomisations, depths 1–400 (Heron to 750). Appendix: LF needed 178 circuits vs 14,000 for Pauli-learning γ on 16 qubits. Mirror RB comparison on ibm_peekskill used 10 randomisations × 2000 shots.
- how_scored: Exponential RB decay fits per sub-layer; product of process fidelities.
- result: Heron LF 0.61 (N=80), 0.26 (N=100); EPLG 6.2×10⁻³, 1.2×10⁻². Eagle LF 0.26/0.19, EPLG 1.7×10⁻²/1.7×10⁻². The paper says layered-mode crosstalk is "greatly alleviated" on Heron because couplers turn off. The Heron device is **ibm_montecarlo, not ibm_torino**.
- limits: Assumes Markovian noise. SPAM-insensitive. A lower bound for some crosstalk terms. Uses the best of a heuristic set of chains. Predictive power for other circuit types is left open.
- borrow: The per-gate error IBM reports is an RB-twirled average, so it **hides coherent error by design**. Feeding it into a depolarising model cannot reproduce coherent build-up in a structured, untwirled circuit. 300 shots × 6 randomisations is enough for decay fits.
- next_steps_it_suggests: Predictive power for other circuits; limits of twirling; mid-circuit measurements.

### Modelling and simulating noisy NISQ behaviour — Georgopoulos, Emary, Zuliani, 2021, PRA 104, 062432, https://arxiv.org/abs/2101.02109
- read_depth: full (v4 HTML, last ~2% not read)
- what_tested: A unified noise model (depolarising + Pauli-X SPAM + T1/T2) built from calibration, compared with Qiskit's composite model and with hardware. A genetic algorithm then tuned the error rates.
- on_whom: IBMQ Melbourne (15q). Quantum-walk circuits, N = 4…64 states. 100,000 shots per configuration.
- how_scored: Hellinger distance (HD) to hardware.
- result: HD for their model vs Qiskit's composite model: N=4: 0.033 vs 0.040; N=16: 0.224 vs 0.262; N=64: 0.457 vs 0.509. Distance grows with size for every model. GA tuning cut HD at N=4 from 0.033 to 0.005 (50 generations), and at N=64 from 0.457 to 0.336 (100 generations). Tuned 2q CNOT errors came out *lower* than calibrated (e.g., 0.015850 → 0.010435) and some readout errors higher.
- limits: Markovian only. No crosstalk, no coherent ("Clifford-type") errors. T1/T2 not tuned. Older fixed-coupler device. The authors note a possible GA artefact.
- borrow: Even after free tuning of depolarising rates, the large-circuit gap stays (HD 0.336 at 64 states). Rescaling depolarising strength alone cannot close a structured-circuit gap. This is the failure mode to test against.
- next_steps_it_suggests: Non-Markovian noise; including more error sources.

### Utility experiment (sparse Pauli-Lindblad + ZNE) — Kim, Eddins, Anand, … Kandala, 2023, Nature 618, 500, https://pmc.ncbi.nlm.nih.gov/articles/PMC10266970/
- read_depth: partial (main text; SI not opened)
- what_tested: Error-mitigated expectation values of 2D TFIM Trotter circuits.
- on_whom: ibm_kyiv (127q Eagle, CX, median T1 288 µs, T2 127 µs). Up to 60 CNOT layers (2,880 CNOTs). Each CNOT layer Pauli-twirled. 2,000 circuit instances per gain × 64 shots (Fig. 2a: 384,000 executions).
- how_scored: Comparison with exact or tensor-network values.
- result: IBM's own working model of its noise is *twirled* Pauli noise with weight-1 and weight-2 jump operators on connected pairs (so it captures crosstalk). They do not use the bare calibration depolarising model. Noise-model stability over time must be handled, partly because of TLS defects (details in the SI, not read).
- limits: Eagle, not Heron. ZNE bias remains. The main text does not mention DD.
- borrow: IBM itself twirls before trusting a Pauli model. Our untwirled circuit is outside the regime where any Pauli model, Aer's included, is expected to hold.
- next_steps_it_suggests: PEC once overhead allows.

### PEC with sparse Pauli-Lindblad models — van den Berg, Minev, Kandala, Temme, 2023, Nature Physics (DOI 10.1038/s41567-023-02042-2), https://arxiv.org/abs/2201.09866
- read_depth: partial (first ~65% of HTML)
- what_tested: Learning a twirled, sparse, crosstalk-aware Pauli noise model per layer and inverting it.
- on_whom: 27q ibm_hanoi (Falcon); 20-qubit layer of 10 concurrent CX. Learning: 100 random instances × 256 shots per data point, 9 measurement bases.
- how_scored: Learned vs measured Pauli fidelities; mitigated vs ideal observables.
- result: Learned fidelities "closely match" measurement (no number in the read text). Number of model coefficients for a linear n-qubit chain is 3n + 9(n−1). The model is re-learned at fixed intervals to track drift.
- limits: Sparsity (local-range) assumption. γ² sampling overhead.
- borrow: Twirling is a precondition for any Pauli model. 100 instances × 256 shots is the order needed per learned layer, which is too expensive for us at 374 s.
- next_steps_it_suggests: Reduce execution time and classical cost.

### T1 fluctuations from TLS — Klimov et al., 2018, PRL 121, 090502, https://arxiv.org/abs/1809.01043
- read_depth: full (PDF incl. supplement)
- what_tested: T1 resolved in frequency and time, using flux-tunable Xmon qubits as TLS probes.
- on_whom: Google Xmon flip-chip sample. Main dataset is 31,278 T1 measurements over 400 MHz × 1,200 min (1 MHz, 15-min steps); 2,000 repetitions × 40 delays per T1 curve. 13 defects tracked across several qubits.
- how_scored: T1 maps; distributions of TLS centre frequencies.
- result: "T1 can vary by up to an order of magnitude", with abrupt changes on 15-minute timescales and across 5 MHz. TLS spectral diffusion D = 2.5 ± 0.1 MHz·h^-½, with both telegraphic and diffusive regimes.
- limits: Tunable-frequency Google qubits. Heron qubits are fixed-frequency, but CZ pulses on tunable couplers can still pass near TLS.
- borrow: A calibration snapshot can be hours old and T1 can move by 10× in 15 minutes. One low-T2 qubit (33–45 µs) in our layout is a prime TLS suspect.
- next_steps_it_suggests: Use defect diffusivity to choose frequencies; materials work.

### Dynamics of qubit relaxation times — Carroll, Rosenblatt, Jurcevic, Lauer, Kandala (IBM), 2021/2022, arXiv:2105.15201 (npj QI 2022 per search listing; arXiv page lists no journal), https://arxiv.org/abs/2105.15201
- read_depth: partial (PDF text, main sections)
- what_tested: Stark-shift T1 spectroscopy near the qubit frequency; correlation with long-run mean T1.
- on_whom: IBM single-junction fixed-frequency transmons, 10 qubits on a 20q device. Daily T1 over ~9 months; Stark scans every 3–4 h over 272 h.
- how_scored: Pearson R between the 9-month mean T1 and estimators.
- result: TLS dip positions wander 1–10 MHz over 272 h. One ~20-min Stark sweep gives 0.76 < R < 0.84 against the 9-month mean. Repeated single-frequency T1 needs ~10 measurements (>100 h) to reach R ~ 0.8, because fluctuations are autocorrelated (~0.2⟨T1⟩).
- limits: Device-screening focus. Not Heron r2.
- borrow: One T1 reading (our 130–145 µs) is a weak estimate of the T1 during our job. A same-session T1/T2 check on the suspect qubit costs little.
- next_steps_it_suggests: Optimise Δω, sample count and spacing for fast ⟨T1⟩ estimation.

### Time-varying quantum channels — Etxezarreta Martinez, Fuentes, Crespo, Garcia-Frias, 2021, npj QI (DOI 10.1038/s41534-021-00448-5); extension arXiv:2207.06838 (PRR 5, 033055, 2023)
- read_depth: abstract (2021 paper: nature.com redirected to login; I saw only the search-listing description). Partial for the 2022/23 extension (HTML, first ~90%).
- what_tested: Static T1/T2 channels vs channels whose T1/T2 fluctuate in time; effect on QEC.
- on_whom (extension): five 5q IBM devices (quito, belem, lima, santiago, bogota).
- how_scored: Inter-qubit Pearson r of T1 time series; QEC thresholds.
- result (extension): Cites a coefficient of variation of about 25% for T1. Fluctuations were judged local to each qubit (|r| < 0.6, with one table inconsistency). Planar-code threshold 0.112 static vs 0.105 time-varying.
- limits: Small, old devices. Wide confidence intervals.
- borrow: A static from_backend model is one draw from a distribution with CV ~25%. That is not enough on its own to double an error over a single job.
- next_steps_it_suggests: Larger processors; correlation studies.

### Stabilising noise via TLS control — Y. Kim, Govia, Dane, van den Berg, … Kandala (IBM), 2024/2025, arXiv:2407.02467v3, https://arxiv.org/abs/2407.02467
- read_depth: partial (first ~75%)
- what_tested: A bias electrode tunes the TLS environment ("optimized" re-tuning vs "averaged" 1 Hz modulation); effect on noise-learning and error mitigation.
- on_whom: IBM 6-qubit fixed-frequency chain with tunable couplers (family not named). P_e after 40 µs delay, 300 shots at 1 kHz, over ~50–60 h.
- how_scored: 2q EPG; ⟨Z⊗6⟩ of a mirror circuit (ideal 1).
- result: Over 60 h, T1 values "fluctuate on average by over 300%". Q1–Q2 EPG (×10⁻³) control 2.78 / optimized 2.58 / averaged 3.04. Unmitigated ⟨Z⊗6⟩: 0.341 ± 0.052 / 0.446 ± 0.036 / 0.371 ± 0.027.
- limits: One benchmark circuit. Hardware knob not available to users.
- borrow: This is the mechanism behind Heron r2's "TLS mitigation feature" (IBM processor-types page: it "controls the TLS environment of the chip"). If ibm_fez runs the "averaged" mode, TLS noise becomes shot-to-shot quasi-static. That breaks the single-exponential assumption, a non-Markovian effect Aer cannot represent.
- next_steps_it_suggests: Close the remaining gap between ideal and mitigated values.

### Randomized compiling — Wallman & Emerson, 2016, PRA 94, 052325, https://arxiv.org/abs/1512.01098
- read_depth: abstract
- what_tested: Theory and numerics: random single-qubit gates that compile to the same circuit tailor noise into stochastic Pauli noise.
- on_whom: none (no hardware)
- result: The abstract claims "dramatic reductions in worst-case and cumulative error rates" with little or no overhead (no numbers in the abstract).
- borrow: The rationale for test T1 below. Under twirling, coherent error adds in probability (∝ n·θ²) instead of in amplitude (∝ (n·θ)²).

### DD performance survey — Ezzell, Pokharel, Tewala, Quiroz, Lidar, 2023, arXiv:2207.03670v3, https://arxiv.org/abs/2207.03670
- read_depth: partial (PDF abstract, setup, conclusions)
- what_tested: 60 DD sequences from 10 families for single-qubit state preservation.
- on_whom: ibmq_armonk, ibmq_bogota (qubit 2), ibmq_jakarta (qubit 1; T2 = 21 ± 3 µs). 8,192 shots per circuit, bootstrap with 1,000 resamples. ~20 calibrations.
- how_scored: Fidelity decay vs idle time.
- result: All DD sequences beat no DD. UR and QDD were best; CPMG and XY4 nearly match them once the pulse interval is optimised. Always-on ZZ produces coherent oscillations in undecoupled decay, and DD cancels it to first order.
- limits: Single qubit only; old fixed-coupler devices; required pulse access.
- borrow: A low-T2 qubit (ours: 33–45 µs) idling across a long circuit is where DD should matter. The DD on/off comparison is a direct test of idle dephasing and ZZ.
- next_steps_it_suggests: Multi-qubit DD survey.

### Crosstalk-robust DD on Eagle vs Heron — Hickman, Wu, Quiroz, 2025, arXiv:2506.18010, https://arxiv.org/abs/2506.18010
- read_depth: full
- what_tested: Simultaneous DD vs crosstalk-robust (staggered, 2-colour) DD on idle path graphs.
- on_whom: ibm_sherbrooke, ibm_kyiv (Eagle r3) and **ibm_marrakesh (Heron r2)**, run 2025-01-09. n = 5–20 qubits. 20 initial states per embedding; Marrakesh had 10 embeddings of n=10. **1,000 shots per circuit**.
- how_scored: Characteristic decay time τγ of fidelity.
- result: Marrakesh n=10: IDLE τγ 6.95 µs; SIM-XY4 10.5 µs; CR-XY4 9.79 µs; best SIM-UR10-8 13.8 µs. Crosstalk-robust variants "offer little advantage over their non-robust counterparts" on Heron (a 3–11% penalty), whereas they gave 3–10× on Eagle. So on Heron r2, **ZZ crosstalk at idle is not dominant**, but plain DD still raises τγ by ~1.5–2× over idle.
- limits: Static first-order ZZ model; π-pulse sequences only. No ZZ strengths in kHz reported.
- borrow: On Heron, expect DD on/off to change idle-dominated error. Do not expect a large staggered-vs-simultaneous difference. 1,000 shots per circuit was enough for their decay fits.
- next_steps_it_suggests: Non-π pulses; non-bipartite topologies.

### Surface-code scaling on Heron — Vezvaee, Benito, Morford-Oberst, Bermudez, Lidar, 2025, arXiv:2510.18847, https://arxiv.org/abs/2510.18847
- read_depth: full (three chunks; one summary may have mislabelled Marrakesh as non-Heron)
- what_tested: Distance-3 and (3,5)/(5,3) codes via SWAP embedding on heavy-hex; comparison with calibration-derived circuit-level noise models.
- on_whom: ibm_aachen (main), ibm_marrakesh, ibm_pittsburgh. ibm_fez and ibm_kyiv were run but not shown because they underperformed. 37–65 qubits, depth >140, ~2,200 entangling gates. **3,000 shots per experiment**.
- how_scored: Logical infidelity vs cycles; a noise-scaling factor χ applied to a median-calibration model to match experiment.
- result: **The calibration-derived model had to be scaled up by χ = 2.3–2.5 (with DD) and 3.6–4.0 (without DD) for |±⟩ logical states to match Heron data.** |0⟩/|1⟩ changed little with DD. Deterministic-benchmarking sequences on ibm_marrakesh q21–q22 showed "pronounced oscillations" (coherent error from the CZ on one qubit). The authors name "non-Markovian dephasing and coherent ZZ-crosstalk" as the main hardware errors.
- limits: Uniform median model. No leakage rate measured (reset does not remove leakage).
- borrow: **The closest published analogue of our gap**: on Heron r2, a calibration model under-predicts error by ~2–4× in deep circuits, and DD is worth a factor ~1.5 in χ for phase-sensitive states. Our negativity being ~½ of sim is consistent with that. Deterministic benchmarking (short repeated-gate sequences on |+0⟩ vs |0+⟩) is a cheap coherent-error probe.
- next_steps_it_suggests: ~30% noise reduction needed for sub-threshold (5,5) scaling.

### Correcting coherent errors on IBM hardware — Cenedese, Benenti, Bondani, 2022/2023, arXiv:2211.16114 (Entropy 25(2) 324, 2023, by search listing; MDPI page returned 403), https://arxiv.org/abs/2211.16114
- read_depth: full (ar5iv)
- what_tested: Single-qubit process tomography after even CNOT sequences (CNOT² = I) vs Haar-random U·U† pairs; hardware vs Qiskit calibration simulator.
- on_whom: ibm_lagos qubits 0 and 1. 8,192 shots × 25 repetitions per tomography.
- how_scored: Bloch-ellipsoid orientation; state fidelities.
- result: The simulator's ellipsoid is z-aligned. On hardware it is **rotated off-axis**, which the authors attribute to coherent error. With random-unitary echoes, hardware matched the simulator. Inserting random single-qubit rotations around CNOT pairs made fidelity roughly state-independent. Mostly qualitative (no fidelity numbers in the text).
- limits: One pair, one day, old device.
- borrow: This is the twirl-on/off and U·U† pattern we need. A coherent-dominated gap closes when randomised; a stochastic-dominated gap does not.

### Measuring capabilities with mirror circuits — Proctor, Rudinger, Young, Nielsen, Blume-Kohout, 2022, Nature Physics 18, 75, https://arxiv.org/abs/2008.11294
- read_depth: partial (first ~50% of HTML: methods and results)
- what_tested: Randomised vs periodic (structured) mirror circuits; observed vs predicted success.
- on_whom: 12 IBM and Rigetti processors; 40 circuits per (width, depth, embedding), ~1,000 shots. Periodic test: 8 processors, 40 circuits per type, 1,024 shots.
- how_scored: Polarisation P = (S − 1/2^w)/(1 − 1/2^w); threshold 1/e.
- result: Periodic circuits had worse worst-case performance than disordered ones on *every* processor. Aspen-4 failed periodic circuits at depth 32 but passed disordered ones to depth 128. Predictions from published error rates were "biased toward over-optimism". Faster-than-predicted decay with depth signals coherent error; faster with width signals crosstalk.
- limits: Old devices; arbitrary 1/e threshold.
- borrow: Our depth-208 structured circuit is the case where calibration predictions are over-optimistic. Run a mirror of our own circuit (with a random Pauli layer at the midpoint) and compare its return probability with from_backend's prediction.

### Practical benchmarking guide — Hashim, Nguyen, Goss, … Proctor, Young, Siddiqi, Blume-Kohout, 2025, PRX Quantum 6, 030202, arXiv:2408.12064, https://arxiv.org/abs/2408.12064
- read_depth: partial (HTML fetched in three chunks; the fetcher did not surface the RB, unitarity or mirror sections)
- result: Coherent errors scale the diamond norm ∝ θ vs ∝ θ² for stochastic ones. Static ZZ and classical crosstalk are context-dependent (non-Markovian) errors outside n-qubit CPTP gate models. Randomised compiling makes errors "add up non-constructively". To catch drift, collect data rastered or in 2–3 interleaved batches. RPE example: CZ ZZ-phase error ~0.06 rad from <60 circuits.
- borrow: Interleave the arms of every test (twirl on/off, DD on/off, layouts) *within one job* so drift does not bias the comparison.
- **ID note:** arXiv:2407.08828 is *not* Hashim et al. It is Proctor, Young, Baczewski, Blume-Kohout, "Benchmarking quantum computers".

### Mid-circuit measurement RB suite — Govia, Jurcevic, Wood, Kanazawa, Merkel, McKay, 2023, New J. Phys. 25, 123016, https://arxiv.org/abs/2207.04836
- read_depth: partial (HTML; results sections)
- what_tested: mcm-rb, delay-rb and mcm-rep, separating measurement-induced spectator error from equal-duration idle.
- on_whom: ibm_peekskill (27q Falcon r8), 23 qubits in two configurations. 40 sequences × 15 lengths × 1,024 shots; 1,800 circuits per configuration.
- result: Q24 control / Q18 ancilla: measurement-induced control error ε = 1.7×10⁻³ ± 1.0×10⁻³, Z-phase (Stark-like). Ancilla non-QND errors were mostly weak.
- limits: Falcon, not Heron. Crosstalk not quantified.
- borrow: Only relevant if our circuits use mid-circuit measurement. Our gap circuits do not (final measurement only), so this mechanism is ruled out for the P(yes) gap. Keep for any dynamic-circuit test.

### Calibration-based digital twins vs IBM hardware — Bautra, Dimitrijevs, Yakaryılmaz, 2026, arXiv:2603.14607, https://arxiv.org/abs/2603.14607
- read_depth: full
- what_tested: `AerSimulator.from_backend`, CSV-calibration and Fake-backend twins vs hardware.
- on_whom: ibm_brisbane and ibm_sherbrooke (Eagle). Three random 5q circuits (depths 10/20/30) × 4 optimisation levels. 100,000 shots. 24 hardware jobs, 96 simulator runs.
- how_scored: Weighted Jaccard similarity.
- result: Only 7 of 96 comparisons (7.3%) reached ≥95% similarity; 47 (49%) were below 85%. CSV twins matched best in 13 of 24 tests, backend-derived models in 7.
- limits: Eagle only; 5 qubits; no coherent-error or crosstalk analysis.
- borrow: Independent evidence that from_backend fits poorly even at 5 qubits and depth 10–30. Our 9q, depth-208 gap is not surprising.

### Detecting crosstalk errors — Sarovar, Proctor, Rudinger, Young, Nielsen, Blume-Kohout, 2020, Quantum 4, 321, https://arxiv.org/abs/1908.09855
- read_depth: abstract
- Does not transfer directly: it is a definition plus a detection protocol shown only in simulation (2 and 6 qubits), with no hardware numbers. The idea we use: vary which neighbouring qubits are active and look for conditional dependence (our "different layout / spectator idle vs driven" test).

### Not verified
- "Hines et al. 2023 PRL, Demonstrating scalable randomized benchmarking of universal gate sets": not opened. I could not confirm venue or authors from what I read, so it is unverified.
- No public source gives ibm_fez's `rep_delay_range`/`default_rep_delay`, or a measured residual ZZ (kHz) for Heron r2.

---

## Cluster summary

### Candidate explanations, with a cheap discriminating test each
Cost rule: ≈0.28 ms per shot + ≈1.5 s per job. Put all arms of a test in **one job, interleaved**, so drift cancels. Our P(yes) at 2,000 shots has SE ≈ 0.011, so a 0.05 shift between arms is ≈3σ and the full 0.25 sim–hardware gap is ≈16σ. The literature used 1,000–3,000 shots per circuit for this kind of test (Hickman 1,000; Proctor 1,024; Vezvaee 3,000).

| # | Explanation | Test | Rules IN | Rules OUT | QPU s |
|---|---|---|---|---|---|
| T0 | Missing idle noise in sim (unscheduled circuit); T1-biased decay; asymmetric readout | **Free**: re-run Aer on the ALAP-scheduled ISA circuit; add `temperature`; check the direction of each crossed marginal in existing data | Scheduled sim moves P(yes) from 0.25 toward 0.50 and reproduces the downward crossings | Scheduled sim still ≈0.25, or crossings go upward | 0 |
| T1 | Coherent error (CZ phase / over-rotation / residual ZZ) building up in an untwirled structured circuit | Same circuit, same layout: twirl off (2,000 shots) vs `enable_gates=True` (e.g. 16 randomisations × 125 shots) | Twirled hardware moves toward the from_backend sim (~0.25) and crossings disappear | Twirled ≈ untwirled ≈ 0.50 (gap is stochastic: excess incoherent error) | ≈ 1.1 + 1.5 ≈ 3 |
| T2 | Idle dephasing / ZZ during waits (low-T2 qubit) | DD off vs `dynamical_decoupling.enable=True`, `sequence_type="XY4"`, 2,000 shots each (same job as T1, 4 arms total) | DD moves P(yes) substantially toward the sim (Vezvaee: χ 3.6–4.0 → 2.3–2.5 with DD) | No DD effect | +1.1 (shared job) |
| T3 | Error magnitude under-estimated (stochastic χ > 1) vs structure | Mirror U·P·U† of our circuit (random Pauli at midpoint), 2,000 shots; compare return probability with Aer's prediction for the same mirror | Hardware return ≪ sim return: rate under-estimate (fit χ like Vezvaee) | Hardware return ≈ sim: rates fine, so the gap is structural or coherent | ≈ 0.6 + 1.5 |
| T4 | Qubit-specific defect / TLS on the low-T2 qubit | Same logical circuit on 2 other 9-qubit layouts avoiding that qubit, 2,000 shots each | Gap shrinks markedly on other layouts | Same gap on every layout (device-wide or architectural) | ≈ 1.1 + 1.5 |
| T5 | Temporal drift (TLS; Klimov 10× in 15 min; IBM >300% over 60 h) | Re-run the untwirled circuit (1,000 shots) in 3 jobs hours apart; record calibration timestamps | P(yes) differs between runs by >0.05 (≈3σ at 1,000 shots) | Stable within SE across runs | 3 × (0.3 + 1.5) ≈ 5.5 |
| T6 | Readout asymmetry / state-prep (rep_delay) | Prep-0 and prep-1 for all 9 qubits (2 circuits × 2,000 shots) in the T1 job; or `enable_measure=True` | Readout 1→0 rate on the crossing qubit far above the Target value | Matches the Target | +1.1 (shared) |

Combined plan: one interleaved job (T1+T2+T6 arms, ~10,000 shots ≈ 2.8 s + 1.5 s) + one job T3+T4 (6,000 shots ≈ 1.7 + 1.5 s) + T5 (~5.5 s) ≈ **13 s of 374 s**. For the negativity gap, one twirled re-tomography of the worst item (9 Pauli settings × 1,000 shots, twirl on/off = 18,000 shots ≈ 5 + 1.5 s) tests whether the ½-negativity is coherent (twirling changes it) or excess dephasing (DD changes it).

### Open questions that fit our budget
1. **Is the from_backend gap on Heron r2 mainly coherent or mainly missing incoherent strength?** Closest: Vezvaee et al. 2025 (χ = 2.3–4.0 on Heron, coherent CZ error seen by deterministic benchmarking) and Cenedese et al. (twirl closes a coherent gap on ibm_lagos). Still open because no one has published twirl-on/off vs from_backend for a deep, structured, user-level Heron circuit. Test: T0 (free) then T1+T2 in one job. 9 qubits, 4 arms, ~8,000 shots ≈ **4 s**.
2. **What does DD buy on a Heron r2 circuit containing a low-T2 qubit, and does it close the negativity gap?** Closest: Hickman et al. (Marrakesh: DD raises τγ 6.95 → 10.5–13.8 µs) and Vezvaee (DD changes χ by ~1.5). Open for entanglement witnesses. Test: tomography of the worst item with DD off/XY4, 9 settings × 1,000 shots × 2 = 18,000 shots ≈ **6.5 s**.
3. **Is the gap layout-specific (TLS) and time-varying on ibm_fez?** Closest: Klimov 2018, Kim Y. 2024/25 (Heron r2 TLS control). Open: no public Heron r2 user-level drift-of-output study. Test: T4 + T5, ≈ **9 s**.

### Questions that do not fit
- Direct residual-ZZ (kHz) or leakage measurement on Heron: needs pulse-level or qutrit readout access (Open Plan has neither). The `meas_type="kerneled"` IQ data might show |2⟩ blobs; I found no paper validating this on Heron.
- Full sparse Pauli-Lindblad learning per layer: ~100 instances × 256 shots × 9 bases per layer (van den Berg), tens of seconds per layer and several layers.
- Layer-fidelity/EPLG remeasurement: IBM already publishes it; a 9-qubit LF costs ≈ 178 circuits × 300 shots ≈ 15 s + overhead, and it hides coherent error anyway.
- TLS-environment control (Kim Y. 2024/25): needs hardware bias electrodes, which users cannot reach.
- Mid-circuit-measurement spectator error (Govia 2023): not a mechanism in our final-measurement-only circuits.

### Fields searched that returned nothing relevant
- A published Heron r2 residual-ZZ value in kHz (none found).
- A published ibm_fez `rep_delay_range` or default (none; it must be read from `backend.configuration()`).
- A leakage-rate measurement on IBM Heron CZ (none found).
- A 2024–2026 TLS/T1 fleet study specifically on Heron r2 (none beyond IBM's processor-types note and 2407.02467).
- A direct from_backend vs Heron hardware comparison for deep circuits (only Eagle, in Bautra 2026).
