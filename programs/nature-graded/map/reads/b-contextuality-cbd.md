# Reads: sequential contextuality tests and Contextuality-by-Default (CbD)

Reader agent, cluster "sequential contextuality + CbD". Date 2026-11-04. All numbers come from the text opened (PDFs pulled from arXiv and converted with pdftotext, or arXiv HTML). Numbers I derived myself are marked **[our calc]**.

**Checks on the sources named in the brief:**
- Kirchmair 2009 Nature, Jerger 2016 Nat Commun, Leupold 2018 PRL, Gühne 2010 PRA and Kujala–Dzhafarov–Larsson 2015 PRL all exist as described. KDL 2015 is arXiv:1412.4724. arXiv:1503.02181 is a different paper: Kujala & Dzhafarov, Found. Phys. 2016, the proof of the cyclic conjecture.
- "Malinowski et al. 2018" is *Probing the limits of correlations in an indivisible quantum system*, PRA 98, 050102 (2018), arXiv:1712.06494.
- arXiv:2009.10751 is by Dikme, Reichel, Laghaout and Björk (KTH). It was published as Laghaout et al., Eur. J. Phys. 43, 055401 (2022). It ran on 2019-era 5-qubit IBM devices, not a current chip.
- arXiv:2101.03812 is by Holweck alone and has no journal reference listed.
- arXiv:2505.21243 is by Kelleher & Holweck (2025) and ran on Heron r2.

---

### Kirchmair 2009 — Kirchmair, Zähringer, Gerritsma, Kleinmann, Gühne, Cabello, Blatt, Roos, 2009, Nature 460, 494, https://arxiv.org/abs/0904.1655
- read_depth: full (main text + Methods)
- what_tested: State-independent Peres–Mermin (PM) inequality ⟨X_KS⟩ = ⟨R1⟩+⟨R2⟩+⟨R3⟩+⟨C1⟩+⟨C2⟩−⟨C3⟩ ≤ 4 (noncontextual bound), QM = 6 for every state. Each of the 3 observables in a row or column is measured sequentially as a QND measurement. A disturbance-corrected CHSH-like subset inequality ⟨X_DHV⟩ ≤ 2 is also tested.
- on_whom: Two ⁴⁰Ca⁺ ions. Each observable A_ij is measured by applying a unitary U that maps A_ij onto σz of one ion, then fluorescence detection with the other ion shelved, then U†. There is no ancilla, and each observable's ±1 outcome is recorded individually. Singlet: 6,600 state copies (1,100 per row/column). Ten input states at 6,600 copies each. All 36 order permutations used 39,600 copies.
- how_scored: Means of row/column products with 1σ errors. All 36 temporal orders were also measured, which gives a direct order-dependence check.
- result:
  - Singlet: ⟨X_KS⟩ = 5.46(4). Across ten states (pure, mixed, separable, entangled): 5.23(5) to 5.46(4).
  - The 36 orderings give 5.22 to 5.49, average 5.38.
  - Disturbance-corrected test on another state: ⟨X_KS⟩ = 5.22(10) and ⟨X_DHV⟩ = 2.23(5) > 2.
  - Entangling gates were applied up to six times per run. State-detection errors were 0.24% and 0.39%.
  - The figures show individual-observable means in each context, e.g. ⟨σz⊗σz⟩ ≈ −0.92 and −0.95 in its two contexts. These are the raw material for CbD (see Massé below).
- limits: The authors say the disturbance analysis "can be extended to the full Mermin-Peres square", but that experimental techniques would have to improve to violate the full inequality. Only the 4-observable subset was disturbance-corrected.
- borrow: The 9-observable square (A11=Z1, A12=Z2, A13=Z1Z2; A21=X2, A22=X1, A23=X1X2; A31=Z1X2, A32=X1Z2, A33=Y1Y2). The design of recording each outcome individually. All 36 permutations as an order-robustness check. The X_DHV inequality, with correction terms −2p_err[A B A] taken from A B A sequences.
- next_steps_it_suggests: Extend the disturbance-corrected analysis to the full square once errors are low enough.

### Gühne 2010 — Gühne, Kleinmann, Cabello, Larsson, Kirchmair, Zähringer, Gerritsma, Roos, 2010, PRA 81, 022121, https://arxiv.org/abs/0912.4846
- read_depth: partial (Secs. I–IV read; Sec. V hidden-variable models skimmed)
- what_tested: Theory of the compatibility loophole for sequential measurements, plus an error analysis of the Kirchmair data. It defines p_flip (unobservable) and bounds it by the observable p_err[B1 A2 B3] = P(B1 ≠ B3 | sequence B A B), assuming measuring B and A disturbs B at least as much as measuring A alone. This gives |⟨X_CHSH⟩| ≤ 2(1 + Σ p_err terms) and a PM generalisation that needs sequences of length four (C1 A2 B3 C4).
- on_whom: The same two-ion setup. Repeated-measurement tables use 1,100 repetitions.
- how_scored: Repeat correlations ⟨A_i A_j | A1…A5⟩ and comparisons of the form A B A versus A A A.
- result:
  - Five repeats of σz⊗1 on a maximally mixed state give correlations 0.95–0.98. Five repeats of σx⊗σx give 0.80–0.94.
  - ⟨A1A3|A1A2A3⟩ = 0.88(1) versus ⟨A1A3|A1B2A3⟩ = 0.83(2) for A=σx⊗σx, B=σz⊗σz, maximally mixed state. For a singlet: 0.92(1) versus 0.90(1).
  - The authors say that for the full PM disturbance-corrected inequality "these p_err terms have to be smaller than 2/48 ≈ 0.0417" on average. Measured p_err was about 0.06 for 3-step sequences and about 0.1 for 4-step sequences, roughly twice too large.
  - The text quotes ⟨χ_KS⟩ = 5.36(4) for its partially entangled state.
- limits: The bounds need assumptions about how hidden variables are disturbed (three different "approaches"). Classical models with memory remain possible. On the full PM version: "an experimental test is very demanding".
- borrow: The **0.0417 average p_err threshold** is the feasibility number for a disturbance-corrected full PM test. On Willow, Google measured a repeat-disagreement of 1 − 0.9636 = 0.036 (see Kumar et al.), just under it. A B A and A A A sequences are the calibration circuits.
- next_steps_it_suggests: Lower error rates so the length-4-sequence PM inequality can be tested.

### Jerger 2016 — Jerger, Reshitnyk, Oppliger, Potočnik, Mondal, Wallraff, Goodenough, Wehner, Juliusson, Langford, Fedorov, 2016, Nat. Commun. 7, 12930, https://arxiv.org/abs/1602.00440
- read_depth: full
- what_tested: State-dependent KCBS inequality Σ⟨A_iA_{i+1}⟩ ≥ −3 (noncontextual), QM −3.944. Tested on a superconducting transmon **qutrit**, with sequential pairs measured in **both orders**. Uses the Gühne-style extended inequality with ε_ij = |⟨A_j|A_jA_i⟩ − ⟨A_j|A_iA_j⟩|, plus a hypothesis test.
- on_whom:
  - One transmon in a 3D cavity, read out through a JPA. The readout is a binary projector onto |0⟩ that leaves the {|1⟩,|2⟩} subspace coherent.
  - Five contexts × 2 orders. The sequence was repeated a number of times printed as "221" in the extracted text, presumably 2^21. 4,603,450 trials were recorded.
  - Heralding readout rejects about 10% of trials. Trials are triggered every 100 µs, with 475 ns cavity ring-down between measurements.
- how_scored: Sum of correlators, compared with −3 − Σε_ij, and a P-value from a game-style hypothesis test.
- result:
  - Forward order: sum −3.489(1) against threshold −3.352(2) (Σε = 0.352(2)). Reverse order: −3.513(1), Σε = 0.367(2).
  - Violations exceed 53σ and 56σ.
  - **Disturbance size:** the first-measured ⟨A_i⟩ is about 0.074–0.082, while the same observable measured second is about 0.145–0.155. Each ε_ij is 0.067–0.079. The authors attribute this to qutrit decoherence during the sequence.
  - The hypothesis test recorded 3,912,769 wins in 4,603,450 trials, P ≤ 2.96×10⁻⁵⁷⁵, against ε-incompatible models with ε ≲ 0.0413.
- limits: The test is state-dependent. A state-independent test is called a "straightforward extension" but was not done. The authors assume i.i.d. trials and no memory, and say memory-based classical simulation loopholes "will most likely remain" for single-system tests. It needs qutrit control.
- borrow: The **both-orders design**. Using the **same pulse block for each observable regardless of context**, which is exactly what makes CbD connections meaningful. The per-observable first/second marginal table, which is a CbD connection table in all but name. The ~0.07 disturbance per pair is a realistic superconducting scale.
- next_steps_it_suggests: A state-independent superconducting test, and a general recipe for noncontextuality tests with minimal assumptions.

### Leupold 2018 — Leupold, Malinowski, Zhang, Negnevitsky, Alonso, Home (+Cabello), 2018, PRL 120, 180401, https://arxiv.org/abs/1706.07370
- read_depth: full (main + supplement Secs. on detection, repeatability, signalling, memory)
- what_tested: State-independent contextuality on a single-ion qutrit (Yu–Oh 13 rays). Uses a random sustained sequence of QND projections chosen in real time by a quantum random number generator.
- on_whom: One ⁴⁰Ca⁺ qutrit, 53 million concatenated sequential measurements of 13 observables (the abstract says 53 million). Detection error < 2×10⁻⁴.
- how_scored:
  - Yu–Oh witness χ_YO ≤ 8 (QM 25/3 ≈ 8.333) and optimal witness χ_opt3 ≤ 25 (QM 83/3 ≈ 27.667).
  - Signalling statistics S^(ba), S^(fo): differences of conditional marginals for the same observable when the neighbouring compatible observable differs (Eq. 10).
- result:
  - χ_YO = 8.279(4) and χ_opt3 = 27.357(11), violations of 69σ and 214σ (statistical only).
  - Repeatability is above 99.6%.
  - Backward-in-time signalling z-scores fit μ = −0.02(4), σ = 0.93(4), consistent with none. Forward-in-time: μ = −0.04(4), σ = 1.64(4), so there is excess spread, which the authors attribute to imperfect coherent rotations.
- limits: The authors are "not aware of any standard method to account for these imperfections" when evaluating SIC (Yu–Oh) witnesses. They note such methods exist only for cyclic systems and cite KDL 2015. **This is a published statement that the CbD-type correction for non-cyclic state-independent witnesses was missing.**
- borrow: Separate backward and forward signalling tests. Backward signalling (a later choice changing an earlier marginal) should be zero by causality. Forward signalling is the physical disturbance that CbD must absorb. Report z-score histograms.
- next_steps_it_suggests: Multi-particle versions, and a penalising method for imperfections in SIC witnesses.

### Malinowski 2018 — Malinowski, Zhang, Leupold, Alonso, Home, Cabello, 2018, PRA 98, 050102, https://arxiv.org/abs/1712.06494
- read_depth: partial (main text, Appendices E and G)
- what_tested: KCBS on a trapped-ion qutrit, scanning the pentagon opening angle θ to *deliberately vary signalling*. Evaluated with the **KDL 2015 (CbD) extended inequality** S5^(ext) = S5 + Σε_i ≥ −3, where ε_i = |⟨A_i^(1)⟩ − ⟨A_i^(2)⟩| (first-measured versus second-measured marginal). Normal and reverse orders are treated as separate systems. KCBS is extended to N = 5…121 observables.
- on_whom: One ⁴⁰Ca⁺ ion. 10,000 repetitions per correlator per setting, 5 correlators per order.
- how_scored: Standard error of the mean from sample standard deviations.
- result:
  - Near compatibility (θ ≈ 48°), normal order: S5 = −3.915(14), S5^(ext) = −3.864(34). Reverse order: S5 = −3.937(14), S5^(ext) = −3.890(34). QM ideal is −3.944, with an ideal S5^(ext) of −3.888.
  - KCBS is violated by 65σ (normal) and 67σ (reverse). The extended (CbD) inequality is violated by up to 25σ.
  - Per-observable marginal differences between first and second position are up to about 0.02 (e.g. −0.111 vs −0.092).
  - Contextuality was seen up to N = 101 observables but lost at 121.
- limits: The authors say closing the compatibility loophole for all noncontextual models would need multiple entangled qutrits. Cyclic (KCBS) only. Needs qutrits.
- borrow: **This is the clearest precedent: CbD's inconsistent-connectedness correction (KDL 2015) applied to a sequential hardware contextuality experiment**, with both orders and a deliberate signalling scan. The "scan signalling on purpose" control maps onto deliberately mis-calibrating our ancilla mapping, for example a small over-rotation, to see CbD track it.
- next_steps_it_suggests: Close the compatibility loophole with entangled qutrits, and use operational (Spekkens-type) definitions.

### KDL 2015 — Kujala, Dzhafarov, Larsson, 2015, PRL 115, 150401, https://arxiv.org/abs/1412.4724
- read_depth: full (main text; supplementary proofs not read)
- what_tested: Theory. The necessary and sufficient condition for a maximally noncontextual description of a **cyclic** system of rank n with binary variables, allowing inconsistent connectedness: s_odd(⟨R_i^i R_{i⊕1}^i⟩, 1 − |⟨R_i^i⟩ − ⟨R_i^{i⊖1}⟩|) ≤ 2n − 2. The simpler sufficient-for-contextuality form is s_odd(correlations) − Σ|⟨R_i^i⟩ − ⟨R_i^{i⊖1}⟩| ≤ n − 2. Covers LG (n=3), CHSH (n=4) and KCBS (n=5).
- on_whom: Reanalysis of the photonic KCBS data of Lapkiewicz et al. (not sequential QND; path-blocking photonics).
- how_scored: A conservative 1 − 10⁻¹⁰ confidence interval using Bonferroni intervals of ±14 standard errors per term.
- result:
  - The Lapkiewicz data are inconsistently connected, e.g. ⟨R1^1⟩ = .136(6) versus ⟨R1^5⟩ = .172(4), significant at 0.1%.
  - The left-hand side of the criterion has CI [3.127, 4.062] against n − 2 = 3, so the system is contextual.
- limits: Cyclic systems only. PM (non-cyclic, three variables per context) needs CbD 2.0 / LP machinery.
- borrow: The exact formula for a cyclic validation test. The point is to "analyze the data directly as found in the measurement record" rather than trying to remove disturbance first.
- next_steps_it_suggests: Treat inconsistently connected systems directly instead of eliminating signalling experimentally.

### CbD 2.0 — Dzhafarov & Kujala, 2016/2017, LNCS (arXiv preprint), https://arxiv.org/abs/1604.04799
- read_depth: abstract (the full text was not opened)
- what_tested: Theory. Defines contextuality for arbitrary finite systems of binary variables using **multimaximal couplings** of each connection, i.e. maximal for every pair of the same property across contexts. For cyclic systems it agrees with the earlier version.
- on_whom: none (theory)
- how_scored: n/a
- result: n/a
- limits: Abstract only.
- borrow: This is the definition to use when order is folded into context, so that each PM observable appears in 4 contexts (2 lines × 2 orders) and connections have more than 2 members.
- next_steps_it_suggests: n/a (abstract)

### Measures of contextuality — Kujala & Dzhafarov, 2019, Phil. Trans. R. Soc. A 377, 20190149, https://arxiv.org/abs/1903.07170
- read_depth: partial (Secs. 1–5, 7 skimmed for definitions and LP formulation)
- what_tested: Theory. Three CbD measures for arbitrary binary systems, plus a CbD generalisation of the contextual fraction (CNTF), all computed by **linear programming**:
  - CNT1: L1 distance of the connection couplings from multimaximal.
  - CNT2: L1 distance of the bunch probabilities from the noncontextual polytope surface. It has a noncontextuality counterpart, NCNT2.
  - CNT3: minimum total variation of a quasi-probability, minus 1.
- on_whom: none (theory)
- how_scored: n/a
- result: Sec. 3.8 says the **1-marginals and 2-marginals define the multimaximal couplings uniquely** and suffice for all CbD measures. Higher-order marginals of the connections can be dropped.
- limits: Relations between CNT1–3 and CNTF are "yet to be investigated" (their words).
- borrow: The **data requirement for a CbD analysis of PM**:
  - For every context, and for every order if order is part of the context: the full joint ("bunch") distribution of the three individual ±1 outcomes, 8 cells.
  - From those, the 1-marginals of each observable in each context.
  - Then an LP feasibility test (is there a joint over all random variables with these bunches and multimaximal connections?) plus CNT2/NCNT2 as an effect size.
  - **Product-only readout, as in Dikme and Holweck, cannot be analysed this way.**
- next_steps_it_suggests: Relating CbD measures to CNTF.

### Massé 2021 review — Gaël Massé, 2021, arXiv only, https://arxiv.org/abs/2105.13821
- read_depth: partial (Sec. XI.C–D only)
- what_tested: A review. Sec. XI.D writes PM in CbD form (18 random variables, 9 connections) and applies it to **Kirchmair 2009's supplementary data**.
- on_whom: Reanalysis of Kirchmair ion data.
- how_scored:
  - Δ0 = ½Σ|⟨A^k_ij⟩ − ⟨A^l_ij⟩| over the 9 connections.
  - Δmin = ½ max(2Δ0, s_odd(a1…a6) − 4), with a_k the context products.
  - CNTX = Δmin − Δ0.
- result:
  - Δ0 = 0.166, s_odd = 5.463, Δmin = 0.732, CNTX = 0.566 > 0, so Kirchmair's data stay contextual after the signalling correction.
  - Context products a1…a6 = 0.924, 0.931, 0.900, 0.900, 0.895, −0.913.
  - The largest connection discrepancy is ⟨X1Z2⟩ = −0.007 in row 3 versus −0.1 in column 2.
- limits: This is a single-author, unrefereed review. The Δmin formula is carried over "following the steps used for similar cases" from cyclic-system work. I did not see a proof that it is the exact CbD criterion for the non-cyclic PM system. **An exact LP over the 18 variables would be needed to confirm it.**
- borrow: A worked template and a target number. On ion data, PM contextuality survives CbD with a margin of about 0.57.
- next_steps_it_suggests: The review frames CbD as a way to separate within-context noise (compatibility) from between-context noise (signalling).

### Dikme 2020 / Laghaout 2022 — Dikme, Reichel, Laghaout, Björk, 2020 arXiv / 2022 Eur. J. Phys. 43, 055401, https://arxiv.org/abs/2009.10751
- read_depth: full (arXiv v1)
- what_tested: The PM square (the variant with X, Y and ZZ on the last row) on IBM Quantum Experience.
- on_whom:
  - ibmqx4 "Tenerife" (5 qubits, 3 used: 2 system qubits + 1 ancilla). ibmqx2 and ibmqx16 were also tried.
  - 6 circuits, one per row/column, × 8,192 shots.
  - The device had 2-qubit gate errors of 2.12–7.95% and readout errors of 3.4–34.8%.
- how_scored: The **product of the three outcomes is coherently accumulated on one ancilla** and read once. There are no individual outcomes and no mid-circuit measurement. A result vector is compared with the noncontextual convex hull (bound v·q ≤ 4).
- result:
  - v·q1 = 4.987 against a bound of 4. The distance to the hull is 0.4029 against a 1σ radius of 0.0145, i.e. 27.8σ.
  - Typo: row 3 reads 0.833 in Table V but 0.883 in the vector v_b. The sum of 4.987 only works with 0.833 **[our calc]**.
  - Single observables were biased about 8% toward +1. 10–30% of runs gave non-quantum results, with day-to-day drift.
  - The order XX, YY, ZZ (more gates) gave worse results than the reverse order.
- limits: The authors themselves flag that product-only readout and circuit concatenation open loopholes: ideally one would "read out the value of each measurement operator". Commutativity and contextual biases cannot be checked this way.
- borrow: A failure mode to avoid. Ancilla product-accumulation makes CbD impossible. Order changes gate counts, so order effects on hardware are real.
- next_steps_it_suggests: Read out individual observables and switch orders to certify compatibility.

### Holweck 2021 — F. Holweck, 2021, arXiv only, https://arxiv.org/abs/2101.03812
- read_depth: full
- what_tested: Cabello-type state-independent inequalities on symplectic polar spaces: χ_G = Σ⟨C_i⟩ − Σ⟨C'_i⟩ ≤ 2P − M (noncontextual), with QM value M.
- on_whom:
  - ibmq_casablanca (best results). Also ibmq_valencia, ibmq_santiago and ibmq_yorktown. ibmq_rome showed no violation.
  - Doily W(3,2): 15 contexts × 8,192 shots on 2 qubits + 1 auxiliary. W(5,2): 315 contexts on 3 qubits + 1 auxiliary.
- how_scored: As in Dikme, **only the context product is read out on one auxiliary qubit**. Barriers are added and transpiler optimisation is off, to force the sequential order.
- result:
  - Doily: χ = 12.27 against a bound of 9 (QM 15), σ = 0.012, more than 270σ. Context means are 0.74–0.91 in magnitude.
  - W(5,2): 236.57 against a bound of 135 (QM 315), σ = 0.064, more than 1,500σ.
  - Hyperbolic quadric Q⁺₀(5,2): 82.17 against a bound of 51 (QM 105), 890σ.
- limits: There is no disturbance, compatibility or signalling analysis, no individual outcomes, and no order swaps.
- borrow: Doily (15 contexts) as a larger 2-qubit alternative to PM (6 contexts). The same ancilla-mapping circuit, with barriers.
- next_steps_it_suggests: Other finite geometries, such as the split Cayley hexagon.

### Kelleher & Holweck 2025 — Kelleher, Holweck, 2025, arXiv only, https://arxiv.org/abs/2505.21243
- read_depth: full
- what_tested: The "Rio Negro" inequality (bound L − 2d, QM L) on PM squares, doilies, quadrics and W(5,2). Also pseudo-telepathy Mermin games on the same devices (no spacelike separation).
- on_whom:
  - Rio Negro: **ibm_kingston (Heron r2)**. Games: ibm_marrakesh and ibm_aachen (Heron r2).
  - 10,000 shots per test. Circuit count not stated. The measurement method is deferred to Saniga et al., Quantum 9 (2025), and not described here.
- how_scored: Raw χ against the bound. **No error bars are reported.**
- result:
  - **PM square: χ = 5.3076 against a bound of 4 (QM 6), on Heron r2.** The noisy simulator gave 5.1340.
  - Doily: 13.0092 against 9. W(5,2): 264.2206 against 189.
  - Mermin games: the table columns are misaligned in both the HTML and the PDF. My reading, consistent with the Fig. 3 range, is hardware = 0.96527 against 17/18 (point-line square) and 0.93498 against 8/9 (line-line square).
- limits: There is no measurement-scheme description, no uncertainties, and no compatibility, disturbance or CbD analysis.
- borrow: **An existing Heron r2 PM number (about 5.31) to calibrate expectations.** Our test should match it in χ and add the CbD layer.
- next_steps_it_suggests: Larger geometries give more data for comparing experiments. There is no explicit future-work section.

### Kumar et al. 2025 (Google Quantum AI) — Kumar, Rosenberg, …, Neven (283 authors), 2025, arXiv only, https://arxiv.org/abs/2512.02284
- read_depth: partial (KSB / magic-square section, main text and Supplement 4.A–B)
- what_tested: **A sequential PM (KSB) test on superconducting hardware with mid-circuit measurement and reset.** It also runs the magic-square game, GHZ games and a 2D hidden linear function problem.
- on_whom:
  - A Willow processor (the paper uses 72- and 105-qubit Willows and does not say which one ran KSB). 3 qubits: 2 data qubits and 1 ancilla.
  - Each two-qubit Pauli is mapped onto the ancilla's phase. The ancilla is measured and **reset after every measurement**. Reset-induced phase is compensated with a calibrated virtual-Z.
  - One circuit streams 180 random contexts (540 QND measurements), with **random order within each context**, repeated 1,000 times. That is about 20,000 occurrences per Pauli.
- how_scored: χ_KSB from context products, bound 4, QM 6. Disturbance is checked from repeated occurrences of the same Pauli in consecutive compatible contexts (P_agree).
- result:
  - **χ_KSB = 5.618 ± 0.005.** Figure error bars are drawn at 10σ.
  - **P_agree = 0.9636 ± 0.0004** for compatible repeats, versus 0.500 ± 0.001 when an incompatible Pauli intervenes. A disagreement of about 0.036 is just under Gühne's 0.0417 threshold **[our calc]**.
- limits: χ uses products only. Individual outcomes are recorded but used only for P_agree. There is **no CbD, marginal-consistency or signalling analysis**, and the Gühne extended inequality is not evaluated. The gap from 6 is attributed to "various experimental errors".
- borrow: **The closest template for our design**: one ancilla, MCM plus reset per observable, random order within contexts, and a long streamed sequence that yields every order and every repeat statistic from one circuit. Its data would support a CbD analysis, but none was done.
- next_steps_it_suggests: Reduce the gap to the noiseless value. Use many-body contextuality as a device benchmark.

### Wang 2022 — Wang, Zhang, Luan, Um, Wang, Qiao, Xie, Zhang, Cabello, Kim, 2022, Sci. Adv. 8, eabk1660, https://arxiv.org/abs/2112.13612
- read_depth: full
- what_tested: A CHSH-form KS inequality (4-cycle) with the two observables of each context on **different ions** (¹⁷¹Yb⁺ and ¹³⁸Ba⁺, using different lasers and detectors), to close the compatibility loophole. Sharpness (repeatability) and detection loopholes are also addressed.
- on_whom: Two ions, 4 contexts. The text says 40,000 repetitions, while Table I says 10,000 per setting. Repeatability was tested 1,000 times per observable.
- how_scored: C ≤ 2 + ε for three classes of models:
  - ε = 0.06: partial-repeatability models.
  - **ε = 0.023 ± 0.027 for "maximally noncontextual models", which is the KDL/CbD term Σ|⟨O_i^{i⊕1}⟩ − ⟨O_i^{i⊖1}⟩|.**
  - ε = 0.128: Gühne-type sequential models fed with repeatability data.
- result:
  - C = 2.526 ± 0.016 (ideal 2√2 ≈ 2.828), which violates all three corrected bounds.
  - Repeatability is 98.4% ± 0.4%.
  - Per-observable marginals across the two contexts differ by up to about 0.11, e.g. ⟨O_0⟩ = −0.0008 versus 0.1096.
- limits: Not a sequential same-system test, and state-dependent. The authors allow that "there could be more loopholes".
- borrow: **Reporting all three ε corrections side by side**: CbD (marginals), Gühne (sequence errors) and repeatability. CbD's ε was the smallest here.
- next_steps_it_suggests: Certifying quantum systems, and looking for further loopholes by analogy with Bell tests.

### Non-transferring or abstract-only (one line each)
- Vallée & Markham 2025, *Formalizing contextuality in sequential scenarios*, arXiv:2509.14125 (abstract only). A theory framework with a no-disturbance condition and state-update hidden-variable models for sequential scenarios. CbD is not mentioned in the abstract. It may give an alternative analysis lens but no hardware numbers.
- Liu et al. 2026, *Linear-optical test of quantum contextuality with sequential measurements*, arXiv:2605.18112 (abstract only). Photonic sequential KCBS, which does not transfer to our hardware and gives no numbers in the abstract.

---

## Cluster summary

**Key answers to the brief**
- **How sequential two-qubit observables are measured with an ancilla:**
  - Rotate the data qubits so the Pauli becomes Z…Z. X needs H, and Y needs S†H, or the conjugate depending on convention.
  - CNOT from each involved data qubit to the ancilla: 2 CNOTs for XX, ZZ or YY, 1 for single-qubit Paulis.
  - Un-rotate, then measure the ancilla mid-circuit and reset it (Google). Alternatively, use the phase-kickback form: ancilla in |+⟩, controlled Paulis, then H.
  - PM needs 3 such blocks per context and 9 observables in total.
  - Dikme and Holweck instead accumulate the product on one ancilla read once. That is cheaper but makes CbD and order checks impossible.
- **Bounds:** PM ≤ 4 (noncontextual), QM 6. Doily ≤ 9, QM 15. CHSH-form 4-cycle ≤ 2, QM 2√2.
- **Hardware values reached:**
  - Ions: 5.46(4) (Kirchmair).
  - Old IBM devices: about 4.99 (Dikme), using its own vector metric on the same 4/6 scale.
  - Heron r2: 5.3076 with no error bar (Kelleher).
  - Willow, sequential with MCM: 5.618 ± 0.005.
- **Disturbance sizes:**
  - Per-observable marginal shifts: about 0.02 (Malinowski, ions), about 0.07 (Jerger, transmon, first vs second position), up to about 0.09 (Kirchmair via Massé), up to about 0.11 (Wang).
  - Repeat disagreement: about 0.036 (Google). p_err of about 0.06–0.1 for 3–4-step sequences (Gühne, 2009 ions).
- **Has CbD been applied to a sequential hardware experiment?** Yes, but only twice that I found:
  - Malinowski 2018: KDL 2015 on a cyclic KCBS qutrit, trapped ion, both orders.
  - Massé 2021: an adapted CbD formula applied to Kirchmair's PM ion data, in an unrefereed review.
  - Jerger used Gühne's ε (a numerically similar marginal-difference term, but not CbD). Wang used KDL, but not sequentially.
  - **Not found: any exact (LP-based) CbD analysis of a non-cyclic state-independent test (PM or doily) on hardware, or any CbD analysis of superconducting sequential contextuality data.** Leupold 2018 explicitly says no such correction existed for SIC witnesses.
- **What CbD requires for PM:**
  - Individual ±1 outcomes for all three observables in every context run. From these come the 8-cell bunch distribution per context and the 1-marginals; per Kujala & Dzhafarov 2019, 1- and 2-marginals suffice for the connections.
  - **Both orders:** either treat forward and reverse as two separate 6-context systems (Jerger/Malinowski practice), or fold order into context: 12 contexts, each observable in 4 contexts, connections of size 4, multimaximal couplings as in CbD 2.0.
  - Then an LP feasibility test plus CNT2/NCNT2, and the Massé-style Δ0/Δmin numbers for comparison.

**Open questions that fit our budget** (cost rule: 0.28 ms per shot + about 2 s per job; I add **×1.5 contingency for dynamic circuits**, because none of my sources give Heron mid-circuit measurement durations; this is an assumption to check)

1. **Does an exact CbD analysis (LP, CNT2) detect PM contextuality in sequential mid-circuit-measurement data from a Heron r2, after inconsistent connectedness is accounted for?**
   - Closest work: Kumar et al. 2025 has the right data type but no CbD. Massé 2021 did CbD on old ion data with an adapted formula. Kelleher 2025 ran PM on Heron r2 with product-only readout and no CbD.
   - Why still open: no hardware PM dataset has been analysed with the exact non-cyclic CbD LP. No IBM PM test has recorded individual outcomes in both orders.
   - Test:
     - 3 qubits: 2 data qubits plus 1 ancilla adjacent to both on the heavy-hex lattice. MCM plus reset after each of the 3 observables.
     - 6 contexts × 2 orders (forward and reversed) × 2 input states (|00⟩ and a Bell state) = 24 circuits × 4,000 shots = 96,000 shots.
     - Outputs: χ_KS per order, the 9-connection marginal table, an LP feasibility check, CNT2 and Δ0/Δmin.
   - **Cost: about 27 s + 2 s ≈ 29 s nominal, about 43 s with contingency.**
   - Expected: χ ≈ 5.3–5.6 and Δ0 ≈ 0.1–0.3, so a CbD margin of several tenths, resolved at tens of σ with 4,000 shots per context. The statistical error is about 0.04 on the CbD statistic **[our calc]**.
   - Cheaper fallback: 1 state, 12 circuits, ≈ 15 s nominal.

2. **Pipeline validation on a cyclic system where KDL 2015 is the exact criterion: a sequential 4-cycle on two qubits.**
   - Observables Z2, Z1Z2, X1, X1X2 (Kirchmair's X_DHV subset). Contexts {Z2,Z1Z2}, {X1,X1X2}, {Z2,X1}, {Z1Z2,X1X2}.
   - The quantum sum reduces to ⟨Z1 + X2 + X1Z2 + Y1Y2⟩, maximum 2√2 **[our calc]**.
   - Closest work: Kirchmair/Gühne, 2.23(5) with Gühne correction. Wang 2022, CbD ε = 0.023, but on two ions rather than sequentially.
   - Why still open: there is no sequential superconducting version with the KDL criterion. It is also the cleanest check that program 1's CbD pipeline outputs "contextual" when physics says so, because the criterion is necessary and sufficient here.
   - Test: 3 qubits, 4 contexts × 2 orders = 8 circuits, on the optimal eigenstate (prepared with a few gates) × 4,000 shots = 32,000 shots.
   - **Cost: about 9 s + 2 s ≈ 11 s nominal, about 16 s with contingency.** A deliberate mis-rotation scan (Malinowski-style signalling control) at 3 settings would add about 25 s.

3. **Gühne disturbance terms on Heron: is the average p_err below 2/48 ≈ 0.0417, so that the full disturbance-corrected PM inequality is testable?**
   - Closest work: Gühne 2010 measured about 0.06–0.1 (too large). Google's P_agree of 0.9636 implies about 0.036.
   - Why still open: nobody has evaluated the full length-4-sequence PM inequality on any hardware.
   - Test:
     - A–B–A sequences for the 18 compatible pairs in both roles: 36 circuits. Plus 9 A–A–A repeatability circuits. Total 45 circuits × 2,000 shots = 90,000 shots.
     - Sequences of length four (C A B C) for the 6 contexts × 3 choices of repeated observable add 18 circuits × 2,000 shots = 36,000 shots.
   - **Cost: about 25 s + 10 s + 2–4 s ≈ 37–39 s nominal, about 57 s with contingency.**
   - Alternative: a Google-style streamed random sequence in one circuit gives every statistic at once, but its cost depends on total circuit duration and MCM time, which I could not source.

Tests 1+2+3 together: about 80 s nominal, about 115 s with contingency, out of 374 s.

**Questions that do not fit**
- KCBS or Yu–Oh qutrit tests (Jerger, Malinowski, Leupold): need qutrit control or pulse access, which the Open Plan lacks.
- Compatibility-loophole-free tests via separate systems or species (Wang) or spacelike separation: on one chip, crosstalk between neighbouring qubits is not excluded, so this needs different hardware.
- Leupold-style sustained sequences of about 10⁷ measurements: the whole budget is at most about 1.3 M shots **[our calc: 374 s / 0.28 ms]**.
- A CbD analysis of W(5,2) (315 contexts) × 2 orders × 4,000 shots ≈ 2.5 M shots ≈ 700 s, which is over budget. The doily (15 contexts × 2 orders × 4,000 shots ≈ 34 s) does fit, as a stretch extension of question 1.
- Memory-based classical simulation loopholes (Kleinmann et al. 2011, cited by Dikme and Jerger): no single-system sequential test can close them. Jerger says they will most likely remain.

**Fields searched that returned nothing relevant**
- "mid-circuit measurement contextuality IBM", "contextuality dynamic circuits IBM", "sequential Peres–Mermin superconducting mid-circuit": the only hits were Kumar et al. 2025 (Willow, not IBM) and the older IBM product-readout papers.
- "Contextuality-by-Default IBM quantum computer data" and "CbD Peres–Mermin experimental data": the only hit was Massé 2021's reanalysis of Kirchmair. There are CbD reanalyses of behavioural and double-slit data, which are off-topic.
- No 2022–2026 IBM paper found that records individual PM outcomes in both orders.
