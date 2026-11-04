# Reads: Wigner's friend and local friendliness (LF) no-go theorems and experiments

Reader: LF cluster. Date: 2026-11-04. The question being costed: a two-friend, *genuine* LF test (an inequality that is not a Bell facet) with 3×3 settings chosen externally, with friend-register size n = 1, 2, 4, 8 qubits, on a Heron r2 chip.

**Checking the sources I was given.** All four papers named with IDs exist and the authors match. Bong et al. 1907.05607 is Nat. Phys. 16, 1199–1205 (2020). Proietti et al. 1902.05080 is Sci. Adv. 5, eaaw9832 (2019). Zeng, Labib & Russo 2409.15302 is **Quantum 9, 1851 (2025)**, so the "Quantum 2025?" guess is right. Laux & Cavalcanti 2609.12527 was submitted 11 Sep 2026 and has no journal yet. Wiseman, Cavalcanti & Rieffel is Quantum 7, 1112 (2023), arXiv 2209.08491. Two corrections to the brief: the Wiseman, Cavalcanti & Rieffel title is *A "thoughtful" Local Friendliness no-go theorem: a prospective experiment with new assumptions to suit*, and Laux & Cavalcanti do **not** call it "rule-based agent friends". They call them "agent-like observers" (reflex, guessing, always-3/4 and betting agents).

**How the PDFs were read.** WebFetch could not parse arXiv PDFs. For four papers (Bong, Proietti, Wiseman–Cavalcanti–Rieffel, Utreras-Alarcón) I read the PDF that WebFetch saved, either as page images or after `pdftotext`. Every number below comes from those texts or from the arXiv HTML. Numbers marked **[our calc]** are my own numerical checks with numpy, using only the inequality and state family given in the text. They are not literature values.

---

### Bong et al. (strong LF no-go) — K.-W. Bong, A. Utreras-Alarcón, F. Ghafari, Y.-C. Liang, N. Tischler, E. G. Cavalcanti, G. J. Pryde, H. M. Wiseman, 2020, Nature Physics 16:1199, https://arxiv.org/abs/1907.05607
- read_depth: full (arXiv v4, main text, Methods and Supplementary Information, pp. 1–15)
- what_tested: The extended Wigner's friend scenario (EWFS) with two superobservers (Alice, Bob) and two friends (Charlie, Debbie). Each superobserver has N = 3 binary settings: x = 1 is "ask the friend" (a = c); x = 2 or 3 is "reverse the friend's measurement, then measure the system". LF is the conjunction of Absoluteness of Observed Events, No-Superdeterminism and Locality. For N = 2 the LF set equals the local-hidden-variable (LHV) set. For N = 3, O = 2 the LF polytope has **932 facets in 9 classes**, and it is strictly larger than the LHV polytope (Table I).
- on_whom: Photonics. Polarisation-entangled photon pairs from type-I SPDC in BiBO. Each "friend" is the photon's path inside a beam-displacer interferometer: the friend's projective measurement is the path, and setting 1 is chosen by inserting a motorised mirror. The state is ρ_μ = μ|Φ⁻⟩⟨Φ⁻| + (1−μ)/2 (|HV⟩⟨HV| + |VH⟩⟨VH|), with |Φ⁻⟩ = (|HV⟩−|VH⟩)/√2. Six μ values were run (0.744 to 0.992 ± 0.002, state fidelity 0.979–0.989). All **9 setting pairs** were measured at each μ. Counts: about 550 coincidences/s, **typically 91,000 coincidences per measurement set**, and about 22,000 per tomography. Settings were run as fixed blocks, not randomised shot by shot.
- how_scored: The left-hand side of each LF inequality, with uncertainties of ±1 s.d. from Monte Carlo resampling (100 Poisson samples).
  - **Genuine LF facet 1 (Eq. 13; 256 of the 932 facets):** −⟨A1⟩ −⟨A2⟩ −⟨B1⟩ −⟨B2⟩ −⟨A1B1⟩ −2⟨A1B2⟩ −2⟨A2B1⟩ +2⟨A2B2⟩ −⟨A2B3⟩ −⟨A3B2⟩ −⟨A3B3⟩ − 6 ≤ 0.
  - **Genuine LF facet 2 (Eq. 14; 256 facets):** −⟨A1⟩−⟨A2⟩−⟨A3⟩−⟨B1⟩ −⟨A1B1⟩−⟨A2B1⟩−⟨A3B1⟩−2⟨A1B2⟩ +⟨A2B2⟩+⟨A3B2⟩−⟨A2B3⟩+⟨A3B3⟩ − 5 ≤ 0.
  - Semi-Brukner (Eq. 18): −⟨A1B2⟩+⟨A1B3⟩−⟨A3B2⟩−⟨A3B3⟩−2 ≤ 0.
  - Brukner (Eq. 17): ⟨A1B1⟩−⟨A1B3⟩−⟨A2B1⟩−⟨A2B3⟩−2 ≤ 0.
  - I3322-type facets (Eqs. 15, 16).
  - "Bell non-LF" (Eq. 22), ⟨A2B2⟩−⟨A2B3⟩−⟨A3B2⟩−⟨A3B3⟩−2 ≤ 0. This is a Bell facet but not an LF facet.
  - Index 1 is the friend ("peek") setting.
- result:
  - **Quantum maximum of genuine facet 1 = 1.345** (LF bound 0), reached with a partially entangled two-qubit state (Schmidt coefficients about 0.776 and 0.631) and rank-1 projective measurements. A semidefinite-programming hierarchy confirms it is optimal to 10⁻⁷. It tolerates up to **18.3% white noise**.
  - Genuine facet 2: maximum 0.880, which needs a two-qutrit state; noise tolerance about 18.0%.
  - Settings used in the experiment (measurements in the XY plane of the Bloch sphere): φ1 = 168°, φ2 = 0°, φ3 = 118°, β = 175°, with Bob's angle β − φ_y.
  - The genuine LF inequality was violated only at the two highest μ values (0.921 and 0.992). At μ = 0.80 and 0.81 a Bell inequality was violated while none of the 932 LF inequalities was. Every data point except μ = 0.81 was at least 2 s.d. from zero.
  - **[our calc]** With the paper's angles, the genuine-facet-1 value (maximised over relabelings) is +0.591 at μ = 1, +0.538 at 0.992, +0.070 at 0.921, −0.292 at 0.866 and −0.661 at 0.810. This matches the trend in Fig. 4.
  - **[our calc]** A see-saw optimisation reproduces 1.3449 and the Schmidt coefficients (0.7757, 0.6311). One optimal configuration has all measurements in the x–z plane: the state is 0.7757|00⟩ − 0.6311|11⟩, and θ_A = θ_B = (58.16°, 153.51°, 68.56°) for settings 1, 2, 3. Each observable is cos θ Z + sin θ X, and θ is identical for Alice and Bob. Ideal values at that point: ⟨A_x⟩ = ⟨B_x⟩ = (+0.108, −0.182, +0.075); correlators ⟨A1B1⟩ = −0.428, ⟨A1B2⟩ = ⟨A2B1⟩ = −0.843, ⟨A2B2⟩ = +0.606, ⟨A2B3⟩ = ⟨A3B2⟩ = −0.734, ⟨A3B3⟩ = −0.715.
- limits: The authors call it a proof-of-principle: the friend is a photon path. They say a rigorous demonstration would need a more plausible observer, "implementing shot-by-shot randomized measurement settings", and closing the separation, efficiency and freedom-of-choice loopholes. The inequality shown in each category was picked as the one violated first, which is a post hoc choice among relabelings.
- borrow:
  - Use genuine facet 1 (Eq. 13). It needs only qubits and projective measurements, gives the largest violation, and has the highest noise tolerance.
  - Use the white-noise threshold (visibility ≥ 0.817) as the hardware go/no-go figure.
  - Measure all nine setting pairs.
  - In the Methods, the x = 2, 3 POVMs are U_Z E U_Z⁻¹, which is exactly "uncompute the copy, then measure the system".
  - Add a sanity check: if Bell non-LF is violated while genuine LF is not, LF still holds.
- next_steps_it_suggests: Use more complex friends, up to an AI running on a quantum computer. A single friend already suffices for semi-Brukner tests. Close the loopholes, including shot-by-shot random settings.

### Proietti et al. (local observer independence) — M. Proietti, A. Pickston, F. Graffitti, P. Barrow, D. Kundys, C. Branciard, M. Ringbauer, A. Fedrizzi, 2019, Science Advances 5:eaaw9832, https://arxiv.org/abs/1902.05080
- read_depth: full (main text and Supplementary Materials, pp. 1–10)
- what_tested: Brukner's "Bell–Wigner" scenario with 2 friends and 2 settings per superobserver. The score is CHSH: S = ⟨A1B1⟩+⟨A1B0⟩+⟨A0B1⟩−⟨A0B0⟩ ≤ 2, where A0 and B0 read the friend's record and A1 and B1 are Bell-state measurements on the photon plus the record. Because of the 2-setting scenario this is a Bell inequality, not a genuine LF inequality (Bong et al. Table I classes it as "Brukner").
- on_whom: Six photons at 1550 nm from three SPDC sources. Each friend's measurement is a type-I fusion gate that copies h/v onto an ancilla photon (the memory), heralded by a detector. Four setting pairs, each projected onto 16 eigenstate combinations, gives 64 settings. In total **1,794 six-fold coincidences in 360 hours**. Source fidelity is 99.62% (+0.01/−0.04).
- how_scored: CHSH, with Poissonian error propagation and a 100,000-sample Monte Carlo check.
- result: **S_exp = 2.416 ± 0.075, more than 5 s.d. above 2.** With the alternative friend observables: 2.407 (+0.073/−0.073), more than 5 s.d. With the less invasive polariser protocol: 2.346 (+0.110/−0.110), more than 3 s.d.
- limits: Fair sampling is assumed (detection loophole). There is no space-like separation; no-signalling is checked only empirically. A new loophole is specific to this kind of test: one must trust that A0/B0 really read the friends' memories. Closing it needs detectors that "only look" at the memory. They estimate the minimal detection efficiency as η > 0.875.
- borrow: The friend-memory-fidelity loophole, which on chip means checking that the x = 1 readout touches only the friend register. A consistency variant of the friend observable that also measures the system and assigns 0 on disagreement. Shots per σ: about 450 six-fold events per correlator gave σ(S) ≈ 0.075.
- next_steps_it_suggests: Event-ready configuration with heralding events space-like separated from the setting choices. Measure all eigenstates in every run. More complex observers, mainly to test collapse models.

### Zeng, Labib & Russo (LF with quantum computers) — W. J. Zeng, F. Labib, V. Russo, 2025, Quantum 9:1851, https://arxiv.org/abs/2409.15302
- read_depth: full (arXiv HTML v3, all sections and appendices, read through targeted extraction)
- what_tested: The **semi-Brukner inequality** with one effective friend. Debbie is cut to one qubit "since the semi-Brukner inequality has no B1 term". Charlie is scaled up as an n-qubit GHZ friend, and the "branch factor" is B = C_I − C_D, which is n − 1 for GHZ friends. They used it for its "relative simplicity"; the authors do not test genuine LF inequalities.
- on_whom: IBM ibm_osaka, ibm_sherbrooke and **ibm_torino** (10,000 shots over 10 trials per data point). On Torino, the physical nodes were 43, 44 and 45 for Debbie, Bob and Alice, with Charlie on the chain 46–52, 37, 33, 32, 31. Quantinuum H1-1 used 200 shots and 4 trials per experiment (7 trials for 17 qubits). Transpiled at `optimization_level=0` plus single-qubit merging only.
- how_scored: X = −⟨A1B2⟩+⟨A1B3⟩−⟨A3B2⟩−⟨A3B3⟩, with LF requiring X ≤ 2. The quantum maximum is 2√2 (the table reports X − 2 = 0.82843); with the original experiment's angles it is 0.380364.
  - Friend circuit: Charlie's measurement is a CNOT ladder from the system into the friend register (the GHZ copy). PEEK (x = 1) measures the friend register. REVERSE (x = 2, 3) applies the inverse ladder, then measures the system in a rotated basis. The friend outcome is a majority vote, F0 = Σ_{H(x)<n/2}|x⟩⟨x| and F1 = Σ_{H(x)>n/2}|x⟩⟨x|. Ties at even n are not defined in the text.
  - Error bars are 3 s.d.
- result:
  - **ibm_torino: violation up to branch factor 4 (a 5-qubit friend). It is the only IBM device beyond B = 0.** The text is inconsistent here: Sec. 4.3.1 says 9 and Fig. 11 says 7.
  - H1-1: violation up to **B = 16** (17-qubit friend).
  - Depolarising-noise simulations: violations reach B = 9 at 2% per gate and B = 4 at 3%. Correlators scale as (1−p1)ⁿ(1−p2)ᵐ, and a violation needs this factor ≥ about 0.707.
  - Exact hardware values and per-setting shots are given only in plots.
  - Their stated friend-state fidelity threshold of 93.66% does not match their own Eq. 20 (8 − 6q ≤ 2.828 gives q ≥ 0.862). This is an internal inconsistency.
- limits: Not loophole-free: no light-speed separation. The noisy-data bound is worst-case. The text does not say how settings were assigned; each (x, y) appears to be its own circuit. Branch factor is a proxy, not a certified "observerhood".
- borrow:
  - The ladder-copy/uncompute construction and majority-vote readout.
  - `optimization_level=0`, so the compiler cannot cancel the copy–uncopy pair.
  - The (1−p)^(#gates) scaling model.
  - Failure mode: violation falls with friend size, and the crossover size is the measured quantity.
- next_steps_it_suggests: Loophole-free tests on networked quantum computers. Error detection on the friend through stabiliser checks. Self-testing or cross-entropy validation of branch factor. "EWFS, with more than two friends and more choices of measurement settings … might be advantageous."

### Laux & Cavalcanti (agent-like friends on ibm_marrakesh) — J. Laux, E. G. Cavalcanti, 2026, arXiv preprint, https://arxiv.org/abs/2609.12527
- read_depth: full (arXiv HTML v1, read through targeted extraction)
- what_tested: A **single-friend** EWFS with S_LF = −⟨A1B1⟩+⟨A1B2⟩−⟨A2B1⟩−⟨A2B2⟩−2 ≤ 0, with 2×2 settings and x = 1 the peek. This is a CHSH-type (Bell) inequality. The authors state that for one friend "there are no genuine LF inequalities beyond Bell inequalities". In their 2-setting scenario this agrees with Haddara & Cavalcanti, below. The state is |Φ⁺⟩; α = 3π/2, β1 = 3π/4, β2 = π/4.
- on_whom: **ibm_marrakesh** ("Heron-r2 native gate set").
  - Agents: Reflex (6 qubits, 3 CZ, depth 28), Guessing (7 qubits, 4 CZ, depth 37), Always-3/4 and Betting (8 qubits, 4–5 CZ, depth 38–44).
  - Hardware runs: 10⁴ shots per run, 10 runs per circuit. Layout example: (10, 11, 12, 13) for the circuit qubits, with the choice qubits on q0 and q155.
  - `optimization_level=0`, no SWAPs, no readout mitigation reported.
  - x = 2 reverses the **whole** agent evolution, not only the copy CNOT.
- how_scored: Mean ± standard error over 10 runs. There is also a relaxed-LF bound S_LF ≤ 4ε, with ε = max_y P(c≠a | x=1, y), estimated by swapping the agent's interaction for fixed memory preparations (10³ shots per initialisation per run). The authors call this "a practical estimate", not a bound.
- result: Hardware S_LF (ideal value 0.828):

  | Agent | S_LF | ε (ε_max) |
  |---|---|---|
  | Reflex | 0.465 ± 0.009 | 0.0175 (0.110) |
  | Guessing | 0.435 ± 0.013 | 0.0234 (0.099) |
  | Always-3/4 | 0.378 ± 0.019 | 0.0194 (0.080) |
  | Betting | 0.306 ± 0.012 | 0.0171 (0.067) |

  Noise-model simulations gave about 0.66–0.68, so the hardware is worse than the model. **[our calc]** The Reflex value means an effective CHSH visibility of (2+0.465)/2.828 ≈ 0.872 for a 6-qubit, 3-CZ circuit.
- limits:
  - **Settings come from H-then-measure choice qubits on the same chip**, with feed-forward through classically conditioned operations. All four (x, y) pairs come from one compiled circuit. The authors say the settings are internal "and therefore this independence is not certified".
  - Locality is neither satisfied nor assumed; the required separation is "of order 1.8 km for the longest circuit".
  - Not loophole-free. ε is not certified. Crosstalk and drift are beyond the noise model.
- borrow:
  - The Heron r2 noise baseline (0.872 CHSH visibility at 3 CZ).
  - The relaxed-ε friend-fidelity audit (replace the copy by fixed memory preparations and read P(c≠a)).
  - Reverse the entire friend evolution, not only the first gate.
  - Their own stated fix: external settings supplied as classical inputs.
- next_steps_it_suggests: Two spatially separated devices sharing an entangled pair. Externally generated settings. Larger, structured reversible agents with higher branch complexity.

### Wiseman, Cavalcanti & Rieffel (thoughtful LF) — H. M. Wiseman, E. G. Cavalcanti, E. G. Rieffel, 2023, Quantum 7:1112, https://arxiv.org/abs/2209.08491
- read_depth: partial (Secs. 2.1, 4.2–4.3 and 7 milestones, from the published PDF)
- what_tested: Theory. An LF theorem in which having thoughts is enough to count as an observer. It assumes human-level AI ("Quall-E") on a fast, large universal quantum computer. The proposed experiment uses a one-friend scenario where the LF inequalities equal CHSH, "though not in scenarios including more than two settings for Alice".
- on_whom: No hardware. The rough estimate is sL = 3 × 10¹⁹ logical qubits, and Bob must be about a light-second away.
- how_scored: —
- result: The authors restate that Bong et al. achieved an LF violation "even with roughly 20% depolarizing noise". Perfect reversibility is not needed.
- limits: Prospective only. Space-like separation is an explicit technological requirement: light-second-scale quantum communication.
- borrow: Their suggested near-term milestones: replace the single physical-qubit friend with an error-detected logical qubit, or with minimal agent-like behaviour. Either fits within a few qubits.
- next_steps_it_suggests: Intermediate milestones with more sophisticated friends, and the new metaphysical assumptions such tests need to mean anything.

### Cavalcanti & Wiseman (LF and quantum causality) — E. G. Cavalcanti, H. M. Wiseman, 2021, Entropy 23:925, https://arxiv.org/abs/2106.04065
- read_depth: partial (abstract and Sec. I, from the PDF; the MDPI HTML returned 403)
- Does not transfer to the test design: purely conceptual. It shows that quantum causal models, which rescue relativity from Bell violations, cannot rescue it from LF violations. It treats LF violation with "genuine" observers as an open question. It matters only for interpreting a pass.

### Utreras-Alarcón, Cavalcanti & Wiseman (sequential friend measurements) — A. Utreras-Alarcón, E. G. Cavalcanti, H. M. Wiseman, 2024, Proc. R. Soc. A (DOI 10.1098/rspa.2024.0040, as listed by search; I did not open the journal page), https://arxiv.org/abs/2305.09102
- read_depth: partial (abstract, Secs. I–IV, from the PDF)
- what_tested: Theory. The superobserver may repeatedly reverse the friend and order a new measurement within one run, or ask the friend and stop.
- result: In such sequential scenarios "the local friendliness inequalities will always be the same as Bell inequalities" (Theorem 4 direction: any Bell violation there implies an LF violation).
- borrow: A negative design rule. Repeated reverse-and-remeasure loops on one friend buy nothing beyond Bell, so a genuine test needs the non-sequential, two-friend 3×3 structure. It also explains why dynamic-circuit "re-measure the friend" designs are not genuine.
- next_steps_it_suggests: —

### Haddara & Cavalcanti (possibilistic LF no-go) — M. Haddara, E. G. Cavalcanti, 2023, New J. Phys. 25:093028, https://arxiv.org/abs/2205.12223
- read_depth: abstract (the PDF was not opened)
- Does not transfer yet: a probability-free, Hardy-type LF no-go under "Possibilistic Local Agency". The abstract gives no scenario size or experiment, so I cannot cost a Hardy-type LF test from it.

### Haddara & Cavalcanti (multipartite LF polytopes) — M. Haddara, E. G. Cavalcanti, 2024 (arXiv); PRA 111:012206 (2025) per the APS listing found in search, https://arxiv.org/abs/2407.20346
- read_depth: full (arXiv HTML v1, two passes, with the theorem statements extracted verbatim)
- what_tested: Theory. When does the LF polytope equal the Bell polytope?
  - Theorem 14: LF = Bell if |I_F| = |I_A| − 1 and every friend's party has 2 settings.
  - Corollary 15: LF = Bell if every party has a friend and at least |I_A|−1 parties have 2 settings.
  - Theorem 18: "the only ones where ℒℱ(S)=ℬ(S)".
  - For one friend with two settings, LF = Bell "regardless of the number of settings of the other party".
- result: No explicit genuine inequalities, quantum values or noise thresholds are given.
- limits: The bipartite two-friend 3×3 case is deferred to Bong et al.
- borrow: **My reading** of Theorems 14 and 18 is that a *one-friend* bipartite scenario where the friend's party has **3** settings is not covered by the equality cases, so LF is strictly larger than Bell and genuine inequalities exist. That would need only one friend register. The text gives no explicit inequality or quantum violation for that case. Also, Laux & Cavalcanti's sentence ("one friend → no genuine LF") is scoped to their 2-setting scenario. This needs a desk check (facet enumeration plus see-saw) before any QPU spend.
- next_steps_it_suggests: Characterise the LF polytopes beyond the equality cases.

### Haddara, Wiseman & Cavalcanti (partially deterministic polytopes) — M. Haddara, H. M. Wiseman, E. G. Cavalcanti, 2025, arXiv preprint, https://arxiv.org/abs/2510.25127
- read_depth: abstract
- Does not transfer directly: a general theory of polytopes where only some inputs are deterministic, the mathematical object behind LF. It applies these to LF and to sequential EWFS. The abstract has no inequalities or numbers; it is the likely place to find one-friend, 3-setting facets for the open question above.

### Bednorz et al. (objectivity loophole in Bell tests on public QCs) — A. Bednorz, J. Batle, T. Białecki, J. K. Korbicz (as extracted), 2025, arXiv preprint, https://arxiv.org/abs/2506.08940
- read_depth: full (arXiv HTML v3, read through extraction)
- what_tested: CHSH where each party's system is copied into 3 "friend" qubits **before** readout. An outcome counts as ±1 only if all copies agree, otherwise 0, with no postselection. It also tests no-signalling. It is not an LF test.
- on_whom: Seven-qubit groups (A2 A1 A0 M B0 B1 B2), 6 groups per device, on ibm_brisbane, ibm_sherbrooke, ibm_torino and **ibm_kingston (Heron)**. Sixty jobs of 20,000 shots, 25 shuffled repetitions per setting pair, giving N = 3×10⁷ trials per setting. IonQ Forte: 10,000 shots, 35 repetitions.
- how_scored: CHSH value ℬ with 1σ errors, plus signalling statistics.
- result: ibm_kingston: all 6 groups above 2 (2.045–2.535). ibm_torino: only 2 of 6 groups above 2 (as low as 1.493). IonQ: 2.569 ± 0.0024. **Statistically significant signalling (beyond 5σ or 10σ) appeared in several groups on brisbane, sherbrooke and torino**, with no identified cause. Kingston showed none beyond statistical error.
- limits: On a single chip, the authors note that light-crossing time is far shorter than gate times, so communication is "only minimized": parties are separated by a middle qubit, settings are phase-only, and no-signalling is tested. Freedom of choice rests on randomness "at some stage"; superdeterminism is addressed only by appeal to common sense. The text does not say whether settings came from on- or off-device randomness.
- borrow: **This is the only on-chip paper that argues locality explicitly, and its argument is an empirical no-signalling audit.** We should pre-register the same audit (marginal of A_x independent of y, and vice versa). Unanimity scoring ("0 if friend copies disagree") is an alternative to majority vote that costs nothing in post-processing. Shuffled repetitions of setting blocks.
- next_steps_it_suggests: Combine objectivity-copy scoring with LF tests, and find the cause of on-chip signalling.

### Altman (Wigner's friend circuit benchmarks) — C. Altman, 2026, arXiv preprint, https://arxiv.org/abs/2601.16004
- read_depth: full (arXiv HTML v1, read through extraction)
- Does not transfer: a 5-qubit "inter-branch communication witness" on **ibm_fez** (20,000 shots per circuit; V = 0.8771 ± 0.0034). It tests no LF inequality, and the author says unitary interpretations predict the same statistics. Its one use is as a rough ibm_fez coherence sanity number.

### Adlam (reference-system loophole) — E. Adlam, 2026 (submitted 1 Nov 2026), arXiv preprint, https://arxiv.org/abs/2611.02283
- read_depth: abstract
- Does not change the circuit design. It argues that LF theorems have a "reference system" loophole through which quantum mechanics can be compatible with LF, applying to "any type of Wigner's Friend experiment". It is a caveat on what a pass would mean.

---

## Cluster summary

### Open questions that fit our budget

**1. Two-friend genuine LF (Bong Eq. 13) with 3×3 externally fixed settings, scaling the friend register n = 0, 1, 2, 4, 8.**
- **Who came closest:**
  - Bong 2020 ran genuine LF, but with photon-path friends, at 91,000 coincidences per setting.
  - Zeng 2025 scaled the friend to n = 5 on ibm_torino and n = 17 on H1-1, but only for the semi-Brukner inequality, which is a Bell facet.
  - Laux 2026 ran on Heron r2, but with one friend, a CHSH-type inequality and on-chip settings.
- **Why it is still open:** No genuine (non-Bell-facet) LF inequality has been tested on any quantum processor, at any friend size, and none with externally fixed settings on a chip.
- **Circuit** (all angles from the refined optimum above, [our calc] reproducing Bong's 1.345):
  - Qubits: a linear chain F_A^n … F_A^1 – S_A – S_B – F_B^1 … F_B^n, which is 2n + 2 qubits (2, 4, 6, 10, 18).
  - State: R_y(−78.26°) on S_A, then CNOT S_A→S_B, giving 0.7757|00⟩ − 0.6311|11⟩.
  - Friend measurement (in basis θ1 = 58.16°): R_y(−θ1) on S, then a CNOT ladder S → F^1 → … → F^n.
  - x = 1 (peek): measure F^1…F^n and score by majority vote. Pre-register the tie rule for even n (for example, tie → value of F^1), or also report unanimity scoring.
  - x = 2 or 3: run the inverse ladder, apply R_y(+θ1), then R_y(−θ_x) with θ2 = 153.51° or θ3 = 68.56°, and measure S. Bob does the same.
  - Put barriers around the copy and uncopy and transpile at `optimization_level=0`. Check that 2n two-qubit gates survive on the x ≠ 1 paths.
  - **Readout twirling is mandatory.** Facet 13 has single-party marginal terms, so asymmetric (T1-biased) readout shifts S directly and could fake or hide a violation. Apply a random X before each measurement and flip the bit back in post-processing, with the masks pre-registered.
- **Settings:** All 9 (x, y) circuits, as 9 PUBs per n. "External choice" means a pre-registered random interleaving: split each setting into about 10 shuffled blocks, with the order taken from a public beacon value fixed after pre-registration. Truly per-shot external settings would need 1-shot parameter bindings, whose per-binding overhead on IBM is unknown; that is a risk to price before trying it.
- **Controls:**
  - (a) n = 0, the plain Bell-scenario value of the same facet. It separates base visibility from friend cost.
  - (b) **Decohered friend:** replace the uncompute with a mid-circuit measurement of F^1 (dynamic circuit) at n = 1 and n = 4. Quantum mechanics predicts S ≤ 0 here. A violation means a bug or that the "friend" never really measured.
  - (c) No-signalling audit on all marginals, as in Bednorz.
  - (d) Laux-style ε audit, with P(c ≠ S_A) on x = 1 by also measuring S_A.
- **Pass:** S > 0 by at least 5σ at a given n, on the single pre-registered facet and labelling, with no look-elsewhere across the 256 relabelings. In the same run, control (b) must be consistent with S ≤ 0 and the no-signalling audit must show no deviation above 3σ. The reported quantity is the largest n that passes (n*) and the S(n) curve.
- **Fail:**
  - S ≤ 0 already at n = 1, which means visibility is below about 0.817 on this chip.
  - Any control failing, which makes the run uninterpretable rather than a refutation.
  - A pass on its own would show only that "LF fails *or* a 1–8-qubit CNOT register is not an observer" (Bong's framing), with locality assumed on-chip. No on-chip paper argues locality beyond a no-signalling check.
- **Expected outcome [our calc]:**
  - Under white noise, S = 7.345v − 6, so S = 0.399 at v = 0.87 and 0.618 at v = 0.90.
  - Model: base visibility v0, with a (1−p) factor per ladder CNOT (n CNOTs on peek paths, 2n on reverse paths).
  - With v0 = 0.92 and p = 0.5%: S(n) = 0.65, 0.54, 0.32, −0.10 for n = 1, 2, 4, 8.
  - With v0 = 0.87 and p = 1%: 0.18, −0.02, −0.42, −1.13.
  - So the crossover n* is likely between 1 and 4, and **n = 8 probably fails**. Locating n* is the result.
- **Shots [our calc]:** σ(S) ≈ 0.10/√(N/1000) per setting. For 5σ you need about 640 shots per setting at v = 0.90, 1,600 at v = 0.87 and 4,100 at v = 0.85.
- **QPU cost:**
  - Main: 5 sizes × 9 settings × 4,000 shots = 180,000 shots → about 50 s.
  - Controls: 18 circuits × 2,000 shots = 36,000 → about 10 s. Mid-circuit measurement may lengthen shots; this is untested on our account.
  - Job overhead about 2–4 s.
  - **Total about 63 s.** A lean version (n = 1, 2, 4 at 2,500 shots plus control (b) at n = 1) is about 90,000 shots → **about 27 s**.

**2. Single-friend genuine LF: Alice with a friend and 3 settings, Bob with 2–3 settings and no friend.**
- **Who came closest:** Haddara & Cavalcanti, whose equality theorems by my reading exclude this case, so genuine inequalities should exist. Laux used one friend but only 2 settings.
- **Why it is still open:** No explicit facet or quantum violation appears in any text I read.
- **First step:** Desk work at zero QPU cost: enumerate the partially deterministic polytope (Alice's input 1 deterministic, plus a no-signalling box) and run a see-saw.
- **If a facet with visibility threshold ≤ 0.85 exists:** The circuit needs only n + 2 qubits, so it is half the friend cost of Q1. 6–9 settings × 4 sizes × 2,500 shots ≈ 60,000–90,000 shots → **about 17–26 s**.

**3. Majority vote vs unanimity scoring of the friend register, and friend-record fidelity ε(n).**
- **Who came closest:** Zeng used majority vote; Bednorz used unanimity on 3 copies with no LF test; Laux estimated ε for 1-qubit memories only.
- **Why it is still open:** Nobody has reported how the friend-record disagreement rate grows with n, or whether unanimity scoring keeps a genuine-LF violation.
- **Test:** Post-processing of Q1's x = 1 data, plus control (d). **Extra QPU cost about 0 s** beyond Q1, or about 3 s for a separate 4 × 2 × 1,000-shot ε calibration.

### Questions that do not fit
- **Loophole-free locality or freedom of choice:** needs space-like separation (Laux: about 1.8 km for their longest circuit; Wiseman–Cavalcanti–Rieffel: about a light-second for human-speed friends). This is impossible on one chip.
- **Thoughtful LF with an AI friend:** about 3×10¹⁹ logical qubits.
- **Genuine facet 2 (Eq. 14):** its optimum needs a two-qutrit state, and there is no qutrit control on the Open Plan. Its qubit value was not given.
- **Sequential reverse-and-remeasure friends:** already settled; they reduce to Bell (Utreras-Alarcón 2024).
- **Hardy-type possibilistic LF test:** there is no explicit scenario in what I could read. Needs theory first.
- **Per-shot external settings with 1-shot bindings:** feasible in principle, but the per-binding overhead is unknown. Measure it with a tiny job (for example 200 bindings × 1 shot, about 2–3 s) before relying on it.
- **Replicating Zeng's 17-qubit friend on Heron:** already done better on H1-1 and not genuine LF. Low value per second.

### Fields searched that returned nothing relevant
- Genuine (non-Bell-facet) LF tests on any quantum computer, whether superconducting, trapped-ion or neutral-atom: none found.
- Trapped-ion or Quantinuum LF experiments other than Zeng's H1-1 runs: none.
- Hardware noise-robustness studies of the 3×3 genuine LF facets: none.
- Explicit arguments for locality or freedom of choice on a single chip, beyond Bednorz's timing remark and no-signalling audit and Laux's "not satisfied": none.
- Two-friend LF circuits with externally pre-registered settings: none.
