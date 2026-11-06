# Bet description for odds elicitation (rule 14, template v2)

**Title.** Sequential Peres–Mermin on IBM's ibm_fez chip under the exact Contextuality-by-Default (CbD 2.0) linear program.

**Assumption at stake.** A contextuality check of the kind used earlier in the testbed on a language model (where it found nothing beyond chance) detects contextuality where quantum physics says it must be: two qubits measured sequentially through an ancilla on a superconducting chip, after the CbD correction for the chip's own measurement disturbance between contexts.

**Design.**
- Three physical qubits on ibm_fez: (3, 4, 5), with ancilla 4. They were chosen by a fixed rule from IBM's reported calibration: ancilla readout error 0.24%, CZ errors 0.17% and 0.33%, T1 and T2 between 148 and 216 µs.
- The nine Peres–Mermin observables (Z1, Z2, Z1Z2 / X2, X1, X1X2 / Z1X2, X1Z2, Y1Y2). Each is measured by the same block in every context: rotate the data qubits, CNOT them onto the ancilla, rotate back, measure the ancilla mid-circuit, reset it.
- 6 contexts (3 rows, 3 columns) × 2 measurement orders (forward, reverse) × 2 input states (|00⟩ and the Bell state (|00⟩+|11⟩)/√2) = 24 circuits × 4,000 shots, in one job. All three outcomes in every context are recorded individually.
- Analysis: each (input state, order) pair is one 6-context system of 18 binary variables, four systems in all. For each, the exact CbD 2.0 LP (multimaximal couplings; Dzhafarov & Kujala 2016) computes CNT2 (Kujala & Dzhafarov 2019), the L1 distance from the observed bunches to the noncontextuality polytope. Its uncertainty comes from a nonparametric bootstrap, 1,000 resamples of each circuit's 4,000 shots; the 99% lower bound is the 10th smallest value.
- The LP code was validated before data:
  - it agrees with the Kujala–Dzhafarov–Larsson criterion on 450 random cyclic systems;
  - it gives 0 on 90 noncontextual models with deliberate context-dependent errors, and 0 on a "cheat" system with fixed context-dependent answers whose raw Peres–Mermin sum is 6;
  - it gives CNT2 0.25 on ideal quantum data;
  - on Kirchmair et al. 2009's published ion-trap numbers, it gives contextual under every completion (min CNT2 0.141).

**Models.** None: no language model is in the loop. The chip is the referee and the object measured.

**Cost.** $0 API; about 29 QPU seconds nominal, up to 45 s cap (IBM's free monthly plan); laptop analysis under an hour.

**Pass rule (as it will be frozen).** Pass if, for **both** input states and in **both** measurement orders (all four systems), CNT2's bootstrap 99% lower bound is above 0 (above 1e-6). Otherwise fail. Untestable (not scored) if the job does not run, any circuit returns under 90% of its shots, or the circuits are not runnable on the live chip.

**What published work predicts for this pass rule.**
- Peres–Mermin exceeds the classical bound of 4 on every platform tried: ions 5.46 (Kirchmair 2009); Google Willow with mid-circuit measurement 5.618 (Kumar et al. 2025, no CbD); IBM Heron r2 (ibm_kingston, same chip family) 5.31 with product-only readout and no error bars (Kelleher & Holweck 2025); old 5-qubit IBM devices about 4.99.
- The one CbD treatment of hardware PM data (Massé 2021, ions, an adapted formula) finds it stays contextual after correction.
- No exact CbD LP on superconducting sequential data exists. Prior work predicts a pass.

**Simulator prediction (committed before any data).**
- An ideal simulator gives Peres–Mermin sum 6.0 and CNT2 0.25 in all four systems.
- IBM's reported-error noise model (qiskit-aer from_backend) gives sums 5.72–5.79 and CNT2 0.220–0.227.
- That noise model omits mid-circuit-measurement crosstalk and reset errors, which are the main known risk.
- A synthetic stress test adds extra per-measurement flip errors growing with position in the sequence (ε, 2ε, 3ε) to the noisy prediction. CNT2 stays above 0 in all four systems at ε = 0.03 (sum 3.9), reaches 0 in two of the four systems at ε = 0.04, and is 0 in all four at ε = 0.06.

**Rows on prior.md's tables.**

| table | row |
|---|---|
| program | nature-graded |
| referee | nature |
| cost tier | free ($0) |
| source | literature |
| layer | layer 2 |

**prior.md as committed at 73eb5cf.**
