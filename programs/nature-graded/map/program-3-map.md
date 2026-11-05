# Program 3 map: nature as referee

Written 2026-11-04 (America/Denver) by the scout session, before any program-3 data existed. No circuit was submitted to hardware and no model API was called. The engine's odds below were elicited in fresh contexts at 14:06 MST and are not revised here (`odds-elicitation/`). Sean's odds are collected separately in `human-odds.md`, which does not show these numbers.

## In plain English

**What this program is for.** The engine bets on its own experiments before it runs them. In program 1, what settled each bet was a language model's behaviour. In this program, an IBM quantum chip settles each bet. Comparing the engine's calibration across the two shows whether its judgment holds up when the referee shares none of its habits. The chip is used only as ground truth. Every circuit here is small enough to simulate exactly, and nothing is a claim of quantum advantage.

**What the reading found** (81 Read records, `reads/`):
- **Wigner's friend.** The strong form of the Wigner's-friend no-go, a "genuine" local-friendliness inequality that is more than a Bell test, has never been run on any quantum computer. The two chip experiments so far, on ibm_torino and on a Heron r2, both used inequalities that reduce to Bell tests. The newer one also drew its settings from qubits on the same chip, which its own authors flag as uncertified. A two-friend test with settings fixed from a public randomness beacon costs about 37 QPU seconds, not the 220 s the gold map estimated.
- **Contextuality.** Nobody has applied the exact Contextuality-by-Default (CbD) analysis to a sequential contextuality experiment on a superconducting chip. On a Heron r2, Peres–Mermin has been run only with product-only readout, which CbD cannot analyse. Google's Willow ran the sequential version with mid-circuit measurement, but did no CbD. CbD is the analysis program 1 pointed at the language model and found nothing with. Here we can check that it finds contextuality where physics guarantees it, for about 57 s.
- **Leggett–Garg.** No IBM Leggett–Garg test has used mid-circuit measurement, a CbD correction, or a clumsiness control written down in advance. That test costs about 29 s.
- **Our own surprise.** Two corrections to our own reasoning about the program 1 hardware gap (0.50 on the chip against 0.25 from its simulator):
  - The simulator we used puts no decay on idle qubits unless the circuit is laid out in time first, and ours was not.
  - A qubit's probability crossing 0.5 does not prove "coherent error", because decay and readout error both push toward 0.
  - The closest published analogue: on Heron, calibration-based models must be scaled up 2.3–4.0 times to match deep circuits.
  - Three cheap checks, two of them free, can say which explanation holds.
- **Settled, so replication only:** real-versus-complex quantum theory (already run on IBM hardware), the PBR theorem (already run on a Heron r2), and quantum Darwinism (no assumption at stake).
- **Ruled out by our access:** anything needing qutrits, pulse access or spacelike separation.
- **Random seeds.** For settings, use the public Bell-certified randomness beacon CURBy with NIST's commit-then-reveal procedure, at 0 QPU s. Leggett–Garg randomness from the chip *consumes* more random input than it produces.

**What to do first.** Two free archive tests, then one 21-second device job. They tell us what the device is really doing, and therefore which error-suppression settings (twirling, DD) to fix in advance for the foundations tests. Next come the CbD instrument check (about 59 s with the cheap memory test), then local friendliness and Leggett–Garg (about 66 s). That totals about 146 s on the chip, leaving about 228 s under the hard stop for replications and conditional tests.

**One disclosure.** While reading the Stage 1 archive, the scout computed per-qubit marginals that were not in the results file. On 8 of 9 qubits, the hardware P(1) is below ideal; the largest drop is 0.75 → 0.30. The noisy simulator is within 0.05 of ideal on every qubit. Those marginals were seen before any pre-registration. So no bet here is about their direction, and the fact was put in the P3-1 to P3-3 rows the elicitor saw.

## How to read this map

- **Odds.** Each P is the engine's probability that the named event (the draft pass rule) happens in the first test. The pre-registration must lock the same event, or log the change as a deviation before data. The odds were elicited once, in id order, in a fresh context that saw only the rows in `odds-elicitation/rows-v1.md` (template `v1-batch`; see that folder's README for the one departure from the template).
- **Human odds** (rule set 2026-11-04 by Sean): the human is a non-specialist whose judgment is about direction, not mechanism. `human-odds.md` asks one plain-English question per direction ("Is <direction> worth about <cost>? Will it come back a hit?"), scored against whether the direction's first pre-registered test passes. The technical sub-bets (pass-rule thresholds, chip-vs-simulator agreement, the secondary events in the notes below, the elicitation checks) keep engine odds only and are marked `engine-only`. P3-1, 2, 3 and 5 were pre-registered with human odds not recorded, by Sean's choice.
- **Elicitation check.** On a seeded random half (seed 20261104: P3-1, 4, 6, 8, 11, 12, 13), the odds were re-elicited with the rule paraphrased and with the question negated. The spread is shown in the table. It averaged 11.3 points of negation incoherence and reached 30 points on P3-13.
- **Expected passes.** On the 13 nature-graded bets the odds sum to 5.08 passes. P3-8 is excluded: mathematics decides it, not the chip, so it is scored on its own line.
- **Costs.** QPU seconds come from `0.28 ms × shots + ≈ 2 s per job`, measured on program 1's two ibm_fez jobs (156,000 shots billed 44 s; 1,000 shots billed 2 s).
  - Circuits with mid-circuit measurement (MCM) get a ×1.5 contingency. No source gives Heron r2's billed overhead for dynamic circuits. The offline FakeFez snapshot gives about 1.56 µs per measurement, small against the roughly 250 µs repetition delay, so ×1.5 is deliberately conservative.
  - The repetition delay itself is our inference, not a documented default. It can be read from `backend.configuration()` (an IBM API call, 0 QPU s; not made in this session).
- **Source tags** for the engine's question Q5 (literature-sourced versus self-generated bets):
  - **L**: from a read's next steps (cluster letter given);
  - **E**: engine-generated;
  - **P1**: from a program-1 result or the gold map.
- **Record ids:**
  - A = `reads/a-local-friendliness.md`
  - B = `reads/b-contextuality-cbd.md`
  - C = `reads/c-leggett-garg-randomness.md`
  - D = `reads/d-device-physics.md`
  - E = `reads/e-other-foundations.md`
- **Every hardware bet shares these rules**, to be written into each pre-registration:
  - **Seeds.** Setting choices, circuit order and layout tie-breaks come from Z = SHA-256(pre-registration commit hash ‖ the first CURBy pulse after that commit). Failure handling (beacon down, qubit unavailable) is written in advance (C, NIST beacon record).
  - **Scoring.** Score on raw counts plus pre-registered readout handling only. Heavier mitigation is known to inflate correlations (E, Lancaster & Palladino).
  - **Twirling and DD** are fixed per bet in advance. Once wave 1 reports, its result decides the default for later bets, and that rule is itself written down before wave 1 runs.
  - **No-signalling audit.** Every multi-qubit foundations test includes one on its own qubits, at zero extra shots (A and E, Bednorz; C, Rybotycki).
  - **Noisy-sim prediction.** Every bet's pre-registration records it, using the P3-1-corrected simulator, so that "the chip departs from its own description" is measured on every run.
  - **Compilation.** Barriers and `optimization_level=0` wherever the compiler could cancel a copy and uncopy (A, Zeng; Laux).

## Ranking

The order weighs four things, in this order:
1. **Gating:** does the result change how later bets must be designed?
2. **Openness:** has nobody done it?
3. **Link to program 1:** does it test an instrument or a result from program 1?
4. **Cost.**

The odds were not used to rank, so a long shot is not demoted for being one.

| rank | id | direction | assumption at stake | cheapest test | QPU s | P(pass) | check spread |
|---|---|---|---|---|---|---|---|
| 1 | P3-1 | Does a correctly scheduled noise model close the Stage 1 gap? | The gap is the device, not our simulator | Re-simulate the archived circuit ALAP-scheduled with job-time calibration | 0 | 0.07 | 0.08 |
| 2 | P3-5 | Coherent or incoherent, from archived tomography | Reported (twirled) error rates describe untwirled circuits | 7-parameter coherent vs incoherent fits to 3 archived 2-qubit tomographies | 0 | 0.42 | — |
| 3 | P3-2 | Twirling and DD on the Stage 1 circuit | Same | 4 interleaved arms × 2,000 shots, plus readout calibration | 6 | 0.25 | — |
| 4 | P3-3 | Is the gap nine particular qubits, or one afternoon? | The gap is a stable property of the device | 2 pre-chosen alternative layouts + 2 repeats ≥ 3 h apart | 6 | 0.12 | — |
| 5 | P3-10 | Sequential 4-cycle with the exact KDL criterion | Program 1's CbD pipeline sees contextuality where it exists | 8 MCM circuits × 4,000 shots | 15 | 0.72 | — |
| 6 | P3-9 | Sequential Peres–Mermin under exact CbD | Same, plus: PM contextuality survives exact CbD on superconducting hardware | 24 MCM circuits × 4,000 shots | 42 | 0.40 | — |
| 7 | P3-7 | Two-friend genuine local friendliness, external settings | Local friendliness (absoluteness of observed events + no superdeterminism + locality) | Bong facet 1, 3×3 settings, friend n = 0, 1, 2, 4, with controls | 37 (70 full) | 0.48 | — |
| 8 | P3-11 | Leggett–Garg with MCM, clumsiness control and CbD | Macrorealism with noninvasive measurability; "IBM violations are clumsiness" | 16 circuits × 4,000 shots × 6 parallel copies | 29 | 0.72 | 0.03 |
| 9 | P3-12 | Alternating non-commuting measurements: any memory? | No superdeterministic memory at µs spacing | 2 MCM circuits on ~50 qubits × 4,000 shots | 6 | 0.68 | 0.18 |
| 10 | P3-8 | Is there a one-friend genuine LF inequality? | "One friend → no genuine LF beyond Bell" | Facet enumeration + see-saw (desk); hardware only if found | 0 (then 17–26) | 0.35 (mathematics) | 0.05 |
| 11 | P3-4 | Does DD restore the missing entanglement? | The missing negativity is idle dephasing | Re-tomography of item h088, DD off vs XY4 | 9 | 0.25 | 0.10 |
| 12 | P3-6 | Does ibm_fez leak settings between qubits? | On-chip no-signalling holds on this Heron r2 | Rybotycki idle test on ~40 pairs | 13 (30 full) | 0.50 | 0.15 |
| 13 | P3-14 | Maximally ψ-epistemic models in d = 4, no fair sampling | Maximally ψ-epistemic models | 30 circuits × 2,000 shots + 9 tomography | 21 | 0.12 | — |
| 14 | P3-13 | LG-certified randomness from P3-11's data | Semi-DI randomness from one transmon's LG violation | Nath Theorem 2 bound on P3-11's data | 0 extra | 0.35 | 0.30 |
| 15 (added 2026-11-04 17:00) | P3-15 | What made 3 November different: the afternoon, or the circuit's barrier and shot grouping? | Program 1's gap was the chip that afternoon, not the circuit build or job grouping | {barrier, no barrier} × {one 1,000-shot block, 10 × 100 interleaved} + R0/R1; repeated ≥ 3 h later | ≈ 3.4 per run (2 runs) | 0.07 | — |
| 16 (added 2026-11-04 22:55) | P3-16 | Does 3 November's result come back when the circuit runs alone in its own job? | Program 1's gap was the chip that afternoon, not the circuit running alone in its own job | (A) barrier circuit alone, (B) no-barrier circuit alone, (C) both in one job; 1,000 shots each, back to back in a seeded order | ≈ 7.1 | 0.05 | — |

Total if everything ran at the lean costs: about 184 QPU s. Recommended plan (below): about 146 s in waves 1–3, up to 60 s more conditionally, and a reserve of at least 120 s kept for replication.

---

## Directions

### P3-1. Does a correctly scheduled noise model close the Stage 1 gap? — rank 1 · P = 0.07 · source L (D) + P1
- **Assumption at stake:** That the Stage 1 gap shows the device departing from its own calibration, not our simulator being built wrong.
- **Who has looked:**
  - Aer's source (D, from_backend record): `NoiseModel.from_backend` attaches idle relaxation only to explicit `Delay` instructions. Program 1's `transpile` (`entangled-mind/src/entangled_mind/backends.py`) had no scheduling step, so waiting qubits never decayed in simulation.
  - Bautra et al. 2026 (D): from_backend twins matched Eagle hardware to ≥ 95% similarity in 7 of 96 comparisons.
  - Vezvaee et al. 2025 (D): Heron calibration models must be scaled up 2.3–4.0×.
  - Open: nobody has separated "missing idle noise" from "under-reported gate noise" for a deep user-level Heron r2 circuit.
- **What our data say:**
  - `entangled-mind/results/stage1-run-1.md`: P(yes) ideal 0.294, noisy sim 0.251, hardware 0.502, over 1,000 shots.
  - The as-run circuit (all 503 gates with parameters, and its layout) is archived in `entangled-mind/window/data/hardware/dbl423dgg49c73dk0db0-0.json`.
  - The job-time calibration for the 9 qubits is in `entangled-mind/results/ibm-calibration.json`.
- **Cheapest test:**
  - Rebuild the ISA circuit from the archive and schedule it ALAP with FakeFez durations (qiskit-ibm-runtime 0.51.0, offline: CZ 84 ns, measure 1.56 µs).
  - Build the noise model from FakeFez, then overwrite T1, T2, readout and gate errors on the 9 physical qubits with the job-time snapshot.
  - Simulate 100,000 shots and compute P(yes) with `readout.quantum_readout`.
  - Control: the same model, unscheduled, must reproduce 0.25 ± 0.03, or the reconstruction is wrong and the test is untestable.
  - Secondary (exploratory, not scored): add `temperature > 0`, and a ZZ `coherent_unitary_error` on each CZ pair.
- **Cost:** $0, 0 QPU s.
- **Pass rule:** The scheduled model gives P(yes) ≥ 0.40.
- **Why first:** Every later bet's noisy-sim prediction uses whichever simulator survives this test.

### P3-5. Coherent or incoherent, from the archived tomography — rank 2 · P = 0.42 · source E
- **Assumption at stake:** That IBM's reported per-gate error rates, measured under randomized-benchmarking twirling, describe the error of untwirled circuits.
- **Who has looked:**
  - Cenedese et al. 2022 (D) saw a rotated (coherent) state on ibm_lagos that random echoes removed.
  - McKay et al. 2023 (D): IBM's reported error is a twirled average that hides coherent error by design.
  - Nobody has fitted archived Heron r2 tomography this way.
- **What our data say:**
  - `entangled-mind/results/witness-run-1.json`: 3 items × 9 settings × 4,000 shots, plus assignment matrices.
  - Hardware negativity: 0.147, 0.063, 0.067, against noisy-sim 0.171, 0.149, 0.118.
  - Never analysed beyond the negativity table.
- **Cheapest test:**
  - Per item, fit the hardware counts by maximum likelihood with two 7-parameter families, each applied to the noisy-sim state:
    - (i) local unitaries (6) plus a ZZ phase (1);
    - (ii) local Pauli channels (6) plus global depolarising (1).
  - Local unitaries alone cannot change negativity, so only family (i)'s ZZ term can mimic the negativity loss. That is why it is included.
- **Cost:** $0.
- **Pass rule:** Family (i) beats family (ii) by ΔlogL ≥ 10 on at least 2 of 3 items.

### P3-2. Coherent or stochastic? Twirling and DD on the Stage 1 circuit — rank 3 · P = 0.25 · source L (D)
- **Assumption at stake:** As P3-5, on the device.
- **Who has looked:**
  - Wallman & Emerson 2016; Cenedese 2022; Proctor et al. 2022 (structured circuits do worse than predicted on every processor tested); Vezvaee 2025; Hickman et al. 2025 (all D).
  - SamplerV2 enables no twirling and no DD by default (D, runtime docs), so program 1 ran with neither.
  - Open: no published twirl-on/off comparison against from_backend for a deep Heron r2 circuit.
- **Cheapest test:**
  - One SamplerV2 job, arms interleaved so that drift cancels (D, Hashim).
  - The identical archived ISA circuit on its original physical qubits (initial layout 136, 143, 123, 142, 144, 141, 124, 125, 117).
  - Arms, at 2,000 shots each:
    - (a) as run;
    - (b) `twirling.enable_gates` and `enable_measure`;
    - (c) `dynamical_decoupling` XY4;
    - (d) both.
  - Plus all-0 and all-1 readout calibration (2 × 2,000).
  - Plus an exploratory mirror arm: U · random Pauli · U†, 2,000 shots.
  - 16,000 shots in total.
- **Cost:** ≈ 6 QPU s.
- **Pass rule:** Arm (b) moves P(yes) toward the corrected-simulator prediction by ≥ 0.125 relative to arm (a), at ≥ 3σ.
- **Gating:** This result, together with P3-4's, sets the pre-registered twirl/DD default for every later bet.

### P3-3. Is the gap nine particular qubits, or one afternoon? — rank 4 · P = 0.12 · source L (D)
- **Assumption at stake:** That the gap is a stable property of the device as calibrated.
- **Who has looked:**
  - Klimov et al. 2018: T1 moves by up to 10× within 15 minutes.
  - Carroll et al. 2022, IBM: one T1 reading is a weak estimate.
  - Kim et al. 2024/25, IBM: T1 fluctuated by more than 300% over 60 h; Heron r2 has a TLS-mitigation feature.
  - All from D. No public Heron r2 study of drift in user-level outputs.
- **What our data say:** Physical qubit 125 had T2 = 44.6 µs at job time; the others were 86–191 µs (`ibm-calibration.md`). Eight of nine marginals dropped, which argues against a single-qubit cause (see the disclosure above).
- **Cheapest test:**
  - In P3-2's job: the same logical circuit on 2 alternative 9-qubit layouts, 2,000 shots each, each with its own corrected-sim prediction.
  - The layouts are chosen by a rule written in advance: exclude qubit 125; among chains of the original's connectivity, maximise median T2 at submission time; break ties with the seed.
  - Plus 2 single-arm repeats of arm (a), ≥ 3 h apart, 1,000 shots each.
- **Cost:** ≈ 6 QPU s.
- **Pass rule:** On both alternative layouts, |hardware − sim| P(yes) is less than half the same-job original-layout gap.
- **Secondary, not scored:** whether the repeats differ by more than 0.05.

### P3-10. Sequential 4-cycle with the exact KDL criterion — rank 5 · P = 0.72 · source L (B)
- **Assumption at stake:** Method: program 1's CbD pipeline certifies contextuality where it exists. Here this is tested on a cyclic system, where the Kujala–Dzhafarov–Larsson (KDL 2015) criterion is necessary and sufficient.
- **Who has looked:**
  - Kirchmair/Gühne: X_DHV 2.23(5) on ions.
  - Wang et al. 2022: two ions, not sequential, CbD term 0.023.
  - Malinowski et al. 2018: KDL on sequential ion KCBS, up to 25σ.
  - All from B. There is no sequential superconducting version under KDL.
- **What our data say:** Program 1's contextuality check was rank-2 CbD, Γ = |q_QQ| − OSS (`entangled-mind/experiments/exp4_run.py`; experiment 5, `results/exp5-run-1.md`). It found 1 of 80 LLM claim–question pairs with Γ > 0 (h248, +0.20), about what chance gives (gold map, direction 8).
- **Cheapest test:**
  - 2 data qubits plus 1 ancilla adjacent to both.
  - Observables Z2, Z1Z2, X1, X1X2; contexts {Z2, Z1Z2}, {X1, X1X2}, {Z2, X1}, {Z1Z2, X1X2}.
  - Each observable is measured by basis change, CNOT(s) to the ancilla, un-rotation, then ancilla MCM and reset, with every outcome stored. The same block is used for an observable in every context, so the CbD connections are meaningful (B, Jerger).
  - Both orders; the optimal state for ⟨Z1 + X2 + X1Z2 + Y1Y2⟩.
  - 8 circuits × 4,000 shots.
  - The analysis generalises program 1's rank-2 Γ to the rank-n KDL criterion. Unit test: the rank-2 case must reproduce program 1's archived Γ values exactly.
- **Cost:** ≈ 15 QPU s, or 13 s shared with P3-9.
- **Pass rule:** The KDL statistic, s_odd(correlators) − Σ|marginal differences|, exceeds 2 with its 99.9% lower bound above 2, in both orders.

### P3-9. Sequential Peres–Mermin under exact CbD — rank 6 · P = 0.40 · source L (B) + P1 (gold map direction 8)
- **Assumption at stake:**
  - Method: as P3-10.
  - Physics: Peres–Mermin (PM) contextuality survives an *exact* CbD correction on superconducting hardware.
- **Who has looked:**
  - Kirchmair 2009: 5.46 on ions.
  - Massé 2021: an adapted, not exact, CbD formula on Kirchmair's data gives a margin of 0.566 (unrefereed).
  - Kumar et al. 2025 (Willow): sequential MCM, χ = 5.618 ± 0.005, no CbD.
  - Kelleher & Holweck 2025 (Heron r2): 5.31, product-only readout, no error bars.
  - Leupold et al. 2018: no correction existed for state-independent witnesses.
  - All from B. Open: no exact linear-programming CbD analysis of PM on any hardware, and no superconducting sequential CbD.
- **Cheapest test:**
  - The P3-10 block applied to the 9 PM observables (Z1, Z2, Z1Z2 / X2, X1, X1X2 / Z1X2, X1Z2, Y1Y2).
  - 6 contexts × 2 orders × 2 input states (|00⟩ and a Bell state) = 24 circuits × 4,000 shots, all three outcomes per context stored.
  - Analysis:
    - χ per order;
    - the 9-connection marginal table;
    - the exact CbD linear program with multimaximal couplings, order folded into context (12 contexts, connections of size 4; CbD 2.0);
    - CNT2 with a bootstrap;
    - Massé's Δ0/Δmin for comparison.
- **Debt before pre-registration:** CbD 2.0 (Dzhafarov & Kujala 2016) was read at abstract depth only. It must be read in full, and the linear program checked on Kirchmair's published marginals, before the pre-registration is written.
- **Cost:** ≈ 42 QPU s (≈ 22 s for one input state).
- **Pass rule:** For both input states, the exact CbD linear program rejects noncontextuality, with CNT2's bootstrap 99% lower bound above 0.
- **Follow-up, if it passes** (not on this month's plan): Gühne's full disturbance-corrected PM inequality. It needs average p_err < 0.0417; Google's data imply about 0.036. Cost ≈ 57 s.

### P3-7. Two-friend genuine local friendliness with external settings — rank 7 · P = 0.48 · source L (A) + P1 (gold map direction 7)
- **Assumption at stake:** Local friendliness: absoluteness of observed events, no superdeterminism and locality, holding jointly. Quantum theory predicts a violation, so a pass confirms quantum theory and counts against LF. A pass shows "LF fails, *or* a 1–4-qubit CNOT register is not an observer", with locality assumed on-chip (Bong's own framing).
- **Who has looked:**
  - Bong et al. 2020: photons, genuine facet violated only at state purities ≥ 0.921.
  - Zeng, Labib & Russo 2025: the semi-Brukner Bell facet with a friend of up to 5 qubits on ibm_torino.
  - Laux & Cavalcanti 2026: ibm_marrakesh, one friend, a CHSH-type inequality, settings from qubits on the same chip flagged as uncertified; S_LF 0.31–0.47 against an ideal 0.83.
  - All from A. Open: **no genuine (non-Bell-facet) LF inequality has been run on any quantum processor**, and none with externally fixed settings on a chip.
- **Cheapest test:**
  - Inequality: Bong facet 1 (Eq. 13). Quantum maximum 1.345, LF bound 0, survives white noise only if visibility ≥ 0.817; S = 7.345v − 6 under white noise.
  - Qubits: the chain F_A^n…F_A^1 – S_A – S_B – F_B^1…F_B^n.
  - State: R_y(−78.26°) on S_A, then CNOT, giving 0.7757|00⟩ − 0.6311|11⟩.
  - Measurement angles θ = 58.16°, 153.51°, 68.56° in the x–z plane, the same for both sides (A, our-calc see-saw reproducing 1.3449).
  - Friend: R_y(−θ1), then a CNOT ladder into n qubits.
    - x = 1: read the friend by majority vote, with the tie rule written in advance. Unanimity scoring is reported too (A, Bednorz).
    - x = 2, 3: inverse ladder, R_y(+θ1), R_y(−θ_x), then measure the system.
  - n = 0, 1, 2, 4; 9 setting pairs each, 2,500 shots each.
  - Barriers and `optimization_level=0`; measurement twirling is mandatory, because facet 1 has single-party marginal terms that asymmetric readout shifts directly.
  - External settings: the circuit order, the split into about 10 shuffled blocks per setting, and the qubit chain are fixed by Z (seed rule above). This improves on on-chip setting qubits. It does not give per-shot free choice: each circuit carries its setting.
  - Controls:
    - (b) decohered friend: an MCM replaces the uncompute at n = 1, and quantum theory predicts S ≤ 0;
    - (c) a no-signalling audit on all marginals;
    - (d) a friend-record fidelity audit, P(c ≠ S_A) on x = 1.
- **Cost:** ≈ 37 QPU s lean. ≈ 70 s full: n up to 8 at 4,000 shots, with control (b) at n = 1 and 4.
- **Pass rule:** S > 0 by ≥ 5σ at some n ≥ 1, on the single pre-registered facet and labelling. In the same run, control (b) must be consistent with S ≤ 0 and control (c) must show no deviation above 3σ.
- **Reported, not scored:** n*, the largest passing n, and the curve S(n).

### P3-11. Leggett–Garg with MCM, a clumsiness control and CbD — rank 8 · P = 0.72 · source L (C)
- **Assumption at stake:** Macrorealism with noninvasive measurability for one transmon. The rival reading is that IBM "violations" are clumsiness.
- **Who has looked:**
  - Huffman & Mizel 2017: IBM 5Q, ancilla CNOTs, a margin of about 2.6σ over measured invasiveness.
  - Knee et al. 2016: a non-disturbance test on a flux qubit, no LGI.
  - Ku et al. 2020: IBM; invasiveness grows with n.
  - Santini & Vitale 2022: K3 on ibmq_manila with no clumsiness test.
  - Nath et al. 2025.
  - All from C. Open: no IBM LGI with MCM, CbD or a clumsiness control fixed in advance; Ku et al. name MCM as the next step.
- **Cheapest test:**
  - One qubit, R_y(π/3) between three times (ideal K3 = 1.5); MCMs at t1 and t2, final measurement at t3.
  - Two preparations: maximally mixed (|0⟩ and |1⟩ pooled) and eigenstate |0⟩.
  - Circuits:
    - C12, C23, C13 and the grand ensemble, × 2 preparations (8);
    - NSIT (2);
    - Knee controls on |0⟩, |1⟩ and |+⟩, with and without the t2 MCM (6).
  - 16 circuits × 4,000 shots, in 6 parallel copies on non-adjacent qubits.
  - CbD: the rank-3 KDL criterion. Its marginals come free from the correlator circuits.
- **Sharp secondary prediction** (C, my-calc), to be pre-registered and scored as its own event: from the eigenstate |0⟩, ideal quantum theory gives a CbD value of 0.75 ≤ 1, i.e. *no* contextuality, because the t2 measurement signals into ⟨Q3⟩.
- **Cost:** ≈ 29 QPU s.
- **Pass rule:** For the mixed preparation, both hold:
  - the CbD-corrected K3 exceeds 1 by ≥ 5σ, pooled;
  - K3 − 1 exceeds the largest measured disturbance on the classical preparations by ≥ 3σ.
- **Optional, in the same job:** the ancilla-CNOT versus MCM invasiveness comparison (C, Q2), +11 s.

### P3-12. Do alternating non-commuting measurements show memory? — rank 9 · P = 0.68 · source L (E)
- **Assumption at stake:** No superdeterministic memory at µs spacing. Outcomes of repeated non-commuting measurements are uncorrelated, as quantum theory says.
- **Who has looked:**
  - Hossenfelder 2014 proposed Corr(κ) = exp(−κ/τ), with τ of order 10⁻⁶ s for µm detectors.
  - Hossenfelder & Palmer 2020 §6.
  - No hardware test found in two searches (E).
- **Honest framing:** The prior that such memory exists is tiny. The bet is mostly whether Heron r2's MCM is clean enough to say "no memory at this spacing". A pass is reported as an upper bound on τ in units of the MCM spacing, not as a refutation of superdeterminism in general (Hossenfelder herself says only "certain types" are testable).
- **Cheapest test:**
  - About 50 non-adjacent qubits, chosen by the seed.
  - On each: H, then 8 MCMs alternating Z and X, all outcomes stored.
  - Control: 8 Z MCMs in a row (the repeatability ceiling).
  - 2 circuits × 4,000 shots.
- **Cost:** ≈ 6 QPU s (best packed into the P3-9/10 job).
- **Pass rule:** In the alternating circuit, pooled |Corr_κ| < 0.01 at κ = 2, 4 and 6. In the control circuit, consecutive repeats agree ≥ 95% of the time.

### P3-8. Is there a one-friend genuine LF inequality? — rank 10 · P = 0.35 · source L (A) · referee: mathematics
- **Assumption at stake:** "For one friend there are no genuine LF inequalities beyond Bell" (Laux & Cavalcanti, said for 2 settings).
- **Who has looked:**
  - Haddara & Cavalcanti 2024 (A) list the equality cases. By the reader's reading, one friend with 3 settings is not among them, so genuine facets should exist.
  - No explicit facet or quantum violation is published.
  - Haddara, Wiseman & Cavalcanti 2025 (abstract only) is the likely place to look.
- **Cheapest test:**
  - Enumerate the facets of the partially deterministic polytope for Alice (a friend, 3 settings, setting 1 deterministic) × Bob (2 or 3 settings, no friend), with cdd/PORTA.
  - See-saw each facet class for its quantum maximum and white-noise tolerance.
  - If one tolerates ≥ 15%: a hardware test on n + 2 qubits, ≈ 17–26 QPU s. That is half P3-7's friend cost.
- **Cost:** $0, laptop hours.
- **Pass rule (mathematics-graded):** A non-Bell LF facet exists in the one-friend 3×2 or 3×3 scenario that quantum theory violates with a white-noise tolerance of at least 15%.
- **Why rank 10 despite being free:** Its referee is mathematics, so it does not feed the nature-graded ledger. Its main value is a cheaper P3-7 for next month. It is scored on a separate line, as a third kind of referee.

### P3-4. Does DD restore the missing entanglement? — rank 11 · P = 0.25 · source L (D)
- **Assumption at stake:** That the missing half of the witness negativity is idle dephasing.
- **Who has looked:**
  - Vezvaee 2025: DD reduced Heron model-scaling from 3.6–4.0× to 2.3–2.5×.
  - Ezzell et al. 2023.
  - Hickman et al. 2025: on Heron r2, crosstalk-robust DD gave little benefit over plain DD.
  - All from D. Open for entanglement witnesses.
- **Cheapest test:**
  - Re-run item h088 (physical qubits 44 and 37; 162 CZ, unpruned, so the circuit is identical): 9 tomography settings plus 4 readout calibrations.
  - DD off versus XY4, 1,000 shots each, interleaved in one job.
  - The archived DD-off value (0.063) is a stability check.
- **Cost:** ≈ 9 QPU s (shares wave 1's batch).
- **Pass rule:** Negativity with DD on minus negativity with DD off ≥ 0.043, with the bootstrap 95% interval of the difference above 0.

### P3-6. Does ibm_fez leak settings between qubits? — rank 12 · P = 0.50 · source L (E, C, A)
- **Assumption at stake:** That on-chip no-signalling holds on this Heron r2. Every foundations test here leans on it as its stand-in for locality.
- **Who has looked:**
  - Rybotycki et al. 2025: Eagle, δP up to about 0.05, p = 5.3×10⁻¹⁷ on a fourth-neighbour pair, cause unknown.
  - Bednorz et al. 2025: signalling on Eagle and on ibm_torino (Heron r1); none on ibm_kingston (Heron r2).
  - IBM's 100-qubit GHZ work: ibm_fez was the weakest of three Heron r2 devices.
  - All from E. Never screened on ibm_fez.
- **Why ranked low:** P3-7, P3-9, P3-10 and P3-11 each audit no-signalling on their own qubits at zero extra cost. This screen asks the device-wide question.
- **Cheapest test:**
  - Rybotycki's idle test: about 40 disjoint neighbouring pairs, phase-only settings, no entangling gate.
  - Lean: 4 circuits × 10,000 shots, which detects δP ≳ 0.03.
  - Full: 16 × 6,250, σ ≈ 4.5×10⁻³.
- **Cost:** ≈ 13 QPU s lean (≈ 30 s full).
- **Pass rule (pass = clean):** No pair has |δP| > 4.5σ after a Bonferroni correction over all pair-setting tests.

### P3-14. Maximally ψ-epistemic models in d = 4, with no fair sampling — rank 13 · P = 0.12 · source L (E)
- **Assumption at stake:** Maximally ψ-epistemic models.
- **Who has looked:**
  - Ringbauer et al. 2015: photons, S = 0.690 ± 0.001, but fair sampling assumed; without it, about 98% detection efficiency is needed.
  - Yang, Yuan & Barnes 2025: PBR on Heron r2, which needs preparation independence; its threshold came from the authors' own noise model.
  - All from E. No superconducting test with d ≥ 3 found (one search).
- **Caveat:** ωq is computed with quantum theory, so this is a loophole-closing replication, not a theory-independent test.
- **Cheapest test:**
  - Two transmons as one real-amplitude ququart, 5 states, 10 pairwise measurements: 30 circuits × 2,000 shots.
  - ωq computed from the intended states and from tomography-reconstructed states (+9 × 1,000 shots).
  - Raw counts, no post-selection.
- **Cost:** ≈ 21 QPU s.
- **Pass rule:** S + 5σ < 1 under both choices of ωq.

### P3-13. LG-certified randomness from P3-11's data — rank 14 · P = 0.35 · source L (C) + P1 (gold map direction 11's "one feasible piece")
- **Assumption at stake:** That one transmon's LG violation certifies randomness semi-device-independently. This assumes dimension 2, projective measurements at t1 and t2, and a time-pair choice independent of the system.
- **Who has looked:**
  - Nath et al. 2025 (IBM Brussels): no bit count, σ or extractor; time pairs not seeded.
  - Nath et al. 2024 (photons): 919,118 bits; none below about 3,000 runs.
  - Both from C.
- **Honest framing:**
  - The time-pair choice uses about 1.58 input bits per round to make at most about 0.11 certified bits.
  - The provider sees the settings in advance.
  - Leakage strains the dimension-2 assumption, and the Open Plan cannot bound it.
  - So this is a foundations check, **not our seed source**. Seeds come from CURBy at 0 QPU s.
- **Cheapest test:** Nath's Theorem 2 bound with a finite-size correction, applied to P3-11's mixed-preparation correlator data (about 72,000 rounds) after the circuit order is seeded from the beacon.
- **Cost:** 0 extra QPU s.
- **Pass rule:** Certified min-entropy ≥ 0.05 bits per round at 99% finite-size confidence.

### P3-15. What made 3 November different: the afternoon, or the circuit's barrier and shot grouping? — added 2026-11-04 17:00 · P = 0.07 · source P1 (audit round 2, ng-p3-2-3 "What would break it next")
- **Assumption at stake:** that program 1's 3 November gap (P(yes) 0.502 against a predicted ≈ 0.26) was the chip that afternoon, not the circuit's pre-measurement barrier or its single 1,000-shot block.
- **Why now:** wave 1 ran the same gate list without the barrier and as interleaved 100-shot pieces, and found no P(yes) gap (0.246 against 0.269). So the two days differ in three things at once (P8).
- **What we know offline:** in Qiskit's ALAP schedule the barrier changes no measurement time; in ASAP, removing it lets qubits be measured from 3.3 µs instead of 8.05 µs. How IBM's servers schedule is not documented in our reads. In the noise model, idle time does not move this circuit (P3-1).
- **Cheapest test:** one job on the original nine qubits: barrier/no barrier × one 1,000-shot block / 10 × 100 interleaved, plus R0/R1 (5 × 100 each). An identical job ≥ 3 h later. ≈ 3.4 QPU s each.
- **Pass rule (draft):** in the first job, the barrier block gives P(yes) ≥ 0.40 and beats the no-barrier block by ≥ 0.10 at z ≥ 3.
- **Odds:** elicited in a fresh context from `odds-elicitation/rows-v1-p3-15.md` alone (template v1, single row; `odds-elicitation/v1-p3-15.md`, 17:00:05). No elicitation check. Human odds: Sean skipped (no odds).

### P3-16. Does 3 November's result come back when the circuit runs alone in its own job? — added 2026-11-04 22:55 · P = 0.05 · source P1 (audit ng-p3-15, "What would break it next")
- **Assumption at stake:** that program 1's 3 November gap (P(yes) 0.502 against a predicted ≈ 0.26) was the chip that afternoon, not the job it ran in: one circuit, alone in its job.
- **Why now:** P3-15 found no effect of the barrier or of block-versus-pieces (0.28–0.32 in every arm, two runs), but in both its jobs the server ran the two 1,000-shot blocks together in one execution span. No 4 November job ran the circuit alone, which is the one 3 November feature not yet reproduced.
- **What we know offline:** IBM's per-qubit calibration had not been re-measured between P3-15's two runs (values dated 12:04), so live predictions cannot see the ~0.2 per-qubit moves between runs.
- **Cheapest test:** three jobs back to back in a seeded order on the original nine qubits, 1,000 shots per circuit: (A) the barrier circuit alone; (B) the no-barrier circuit alone; (C) both circuits in one job. ≈ 7.1 QPU s (0.28 ms per shot + ~2 s per job).
- **Pass rule (draft):** job A gives P(yes) ≥ 0.40 and beats the barrier circuit in job C by ≥ 0.10 at z ≥ 3.
- **Odds:** elicited in a fresh context from `odds-elicitation/rows-v1-p3-16.md` alone (template v1, single row; `odds-elicitation/v1-p3-16.md`, 22:54). No elicitation check. Human odds: from `ledger/human-odds.jsonl` only (CONTEXT §3 rule 11); none recorded when mapped.

---

## Closed, merged and killed (nothing disappears)

| candidate | verdict | diagnosis |
|---|---|---|
| Gold map direction 11: hardware as an oracle for the engine | **stays closed** | This program uses the chip only as a referee. Liu et al. 2025 certified randomness needs a ~2.2 s response latency, exascale verification and about 6×10⁴ QPU s (C). |
| Real vs complex quantum theory | killed: settled | Run on IBM hardware twice (Batle et al. > 100σ unmitigated; Lancaster & Palladino on 8 devices) and on a USTC chip at 43σ (E). Independent sources are impossible on one chip. Replication-only cost ≈ 12 s. |
| PBR theorem | killed: settled | Already passed on a Heron r2 (ibm_marrakesh; E). Preparation independence cannot be closed on one chip. Replication with model-independent scoring ≈ 7 s. |
| Bell test with k redundant friends (Bednorz) | merged into P3-7 | Unanimity scoring of the friend register is reported in P3-7 at zero extra cost. |
| Gühne full disturbance-corrected PM inequality | deferred | Follow-up to P3-9 if it passes (≈ 57 s). |
| Sorkin / higher-order interference | killed | Needs qutrits or genuine multi-path systems. A qubit encoding tests only compiled gates (E). |
| KCBS, Yu–Oh, Lüders-bound LG | killed | Need qutrit control, which the Open Plan lacks (B, C). |
| Weak-measurement LG (Rybotycki) | killed: cost | About 2×10⁶ shots ≈ 560 s per job, over the whole remaining budget (C). |
| Single-qubit Born-rule deviations at 10⁻³ | killed: cost | Needs 10⁷–10⁸ shots (E). |
| Quantum Darwinism | killed | A demonstration of quantum theory on an engineered environment; no assumption at stake (E). |
| Quantum switch, indefinite causal order | killed | On a chip, the gates run in a definite order, so a simulation tests nothing about causal structure (E). |
| Frauchiger–Renner | killed | On a chip it checks only a Hardy-type probability; the paradox is about reasoning rules (E). |
| Measurement-induced phase transitions | killed | The post-selection cost grows exponentially with the number of mid-circuit measurements, and the transition is a quantum-theory prediction (E). |
| Loophole-free locality or freedom of choice | killed | Needs spacelike separation: about 1.8 km for Laux's circuit (A). |
| Leupold-style sustained sequences | killed: cost | About 10⁷ measurements, against our whole budget of about 1.3 M shots (B). |
| Layer fidelity / EPLG, sparse Pauli–Lindblad learning | killed | IBM already publishes layer fidelity, and the measurement hides coherent error. Learning costs tens of seconds per layer (D). |
| Direct residual-ZZ or leakage measurement | killed | Needs pulse or qutrit access (D). |

## What changed from the gold map

- **Cost of direction 7 (local friendliness).** About 37 s lean or 70 s full, not about 220 s. The gold map assumed about 2 s per circuit. Our own billing gives 0.28 ms per shot plus about 2 s per job.
- **Cost of direction 8 (sequential Peres–Mermin).** About 42 s plus 15 s for the 4-cycle, within the 72–150 s estimated.
- **Both now fit in one month.** That reverses the gold map's rule "7 and 8 cannot both run" (46 + 220 + 150 > 420), and the reason is stated: the cost model was wrong.
- **Inequality for direction 7.** It is now named: Bong facet 1, a genuine LF facet. Zeng and Laux both ran Bell facets.
- **Direction 11** stays closed. Its "one feasible piece" (LG randomness) becomes P3-13, at zero extra cost, with its caveats stated.

## Month plan under the hard stop

**Budget.**
- IBM Open Plan: 600 QPU s a month.
- Project hard stop: 420 s cumulative, enforced in code by `run_hardware`.
- Used so far: 46 s, so **374 s remain**.
- The monthly allowance resets in December; the hard stop does not. Raising it is Sean's call alone.

**Rules for the month.**
1. **Reserve.** No wave starts if cumulative billed seconds plus 1.5× the wave's estimate would pass **300 s**. That keeps at least 120 s for replicating any audited surprise (invariant 7: a hit is not a hit until it replicates) and for audit-requested reruns.
2. **Re-costing.** After every job, compare billed against estimated seconds. If billed exceeds estimated by more than 1.5×, re-cost the rest of the plan before submitting anything else.
3. **Approval.** Each wave is a separate pre-registered, separately approved submission (CONTEXT.md rule 7). Nothing in this map approves hardware.
4. **Queue.** Queue waits have run to almost 3 hours, so plan one wave per day at most.

| wave | dates (target) | what | QPU s (estimate) | cumulative after |
|---|---|---|---|---|
| 0 | Nov 4–8 | Sean's odds form, before any pre-registration. Pre-register and run P3-1 and P3-5 (archives, $0). P3-8 desk work. Read CbD 2.0 in full; check the CbD linear program on Kirchmair's published marginals. Write the beacon seed protocol. Build every circuit and its corrected-sim prediction offline. With approval, read ibm_fez's `rep_delay_range`, dynamic-circuit support and current usage (IBM API, 0 QPU s). | 0 | 46 |
| 1 | Nov 9–10 | Pre-register P3-2, P3-3 and P3-4, with the rule that turns their result into the twirl/DD default for waves 2–3. One batch: P3-2 + P3-3 layouts + P3-4. The two P3-3 repeats as small jobs ≥ 3 h apart. | ≈ 21 | ≈ 67 |
| 2 | Nov 11–13 | Pre-register P3-10, P3-9 and P3-12. One job: 4-cycle + PM + alternating MCM. | ≈ 59 | ≈ 126 |
| 3 | Nov 14–18 | Pre-register P3-7 (lean) and P3-11 (+ P3-13's analysis, plus P3-11's eigenstate prediction as a separate scored event). Two jobs. | ≈ 66 | ≈ 192 |
| 4 | Nov 19–22, conditional | Only what the reserve rule allows, in this order: P3-6 lean (13); P3-8's hardware stage if the desk work found a facet (17–26); P3-14 (21); P3-7 full extension to n = 8 if lean passed at n = 4 (+33). | ≤ 60 (93 with the P3-7 extension) | ≤ 252 |
| reserve | to Dec | Replication of any audited pass that would surprise; audit-requested reruns. | ≥ 120 | ≤ 420 |

- **If wave 1 shows that twirling or DD materially changes outputs:** those settings become the pre-registered default for waves 2–3, and the noisy-sim predictions are rebuilt to match before those pre-registrations.
- **If wave 1 shows ibm_fez drifting badly** (P3-3 repeats differing by more than 0.10): waves 2–3 use same-job controls everywhere. P3-7 also runs its n = 0 Bell-scenario control in the same job, which it does in any case.

**Deadline.** The residency deadline is 2026-11-22. Waves 0–3 give, by Nov 18:
- 11 nature-graded scored bets: P3-1, 2, 3, 4, 5, 7, 9, 10, 11, 12 and 13;
- 1 correlated secondary event: P3-11's eigenstate prediction;
- 1 mathematics-graded bet: P3-8. That is enough to put a second column on the calibration chart. It is not enough to compare calibrations with confidence (see the notes below).

## After wave 1 (2026-11-04)

Odds above are not revised. Outcomes, audited in round 2 (entangled-mind audit2 `8091d01`); all verdicts stand:

| id | verdict | one line |
|---|---|---|
| P3-1 | fail | Scheduled sim 0.268 (control 0.267); 7% of the Nov 3 gap closed by the pre-registered formula, nearly all of it reconstruction offset; idle decay ≈ 0%. Run kept FakeFez's T1/T2 (bug); verdict unchanged when fixed |
| P3-5 | fail, incoherent better | ΔlogL −43.5, −34.9, +63.0; both kinds of error present on every pair, so not "blur, not steering" |
| P3-2 | untestable | No P(yes) gap on Nov 4: chip 0.246, sim 0.269 (Nov 3 chip: 0.502, but that run had a pre-measurement barrier and one 1,000-shot block; Nov 4 had neither). Qubit 125 still 0.14 below sim |
| P3-3 | untestable | Same; alternative layouts 0.277 / 0.297 against sim 0.265 / 0.264 in P(yes), each with one qubit 0.12–0.14 below sim |

- **Re-weighting.** The live question is now what made Nov 3 different: the chip that afternoon, or the circuit's barrier and the way the shots were grouped. Nov 4's run cannot separate them. The direct test is one small job (≈ 2.5 QPU s): the circuit with and without the barrier, each as one 1,000-shot block and as interleaved blocks, ≥ 3 h from other runs, then repeated on another day. Coherent-error directions (P3-2's premise; P3-4 in part) cool slightly: P3-5's fits found steering and blurring both present, and on Nov 4 there was no P(yes) gap for twirling to close.
- **Defaults for waves 2–3** (P3-2's pre-registered rule): twirling off (its shift, 0.047, 95% CI 0.019–0.075, is just under the 0.05 bar, so close to a tie), DD off.
- **Corrected simulator: held.** The "P3-1-corrected simulator" named in the shared rules above is not used for any prediction until `p3sim.overwrite_calibration` (T1/T2 discarded) and E2's ZZ (overridden) are fixed, the fix is pre-registered as a deviation, and P3-1 is re-run.
- **New leads, not bets:** qubit 141's measured readout error (P(1|0) 0.21) is about 20× its reported value; the mirror circuit succeeds 2.2% on the chip against 13.6% in a post-hoc run of the corrected sim (not pre-registered).
- **QPU:** 8.0 s billed against 7.6 estimated; cumulative 54 s.

## Notes for the engine

- **The comparison this program exists for is underpowered, and it is said so up front.**
  - This month gives about 10–13 nature-graded bets. Program 1 has 5 scored AI-graded bets.
  - A Brier difference between two ledgers of that size is noise unless it is large.
  - The elicitation check showed the engine's own odds moving by up to 30 points with wording, and by 11 points on average under negation. Any calibration difference smaller than that is not a difference.
  - Report it as a pilot of the measure, as proposal.md already does for the engine.
- **The referees differ in more than one way.** Nature-graded bets here are mostly bets about *device noise against a known physics prediction*. AI-graded bets were about a model's behaviour with no settled theory. A calibration gap between them could come from that difference in item type, not from the referee's independence. Two partial controls:
  - (a) Both ledgers use the same v1 elicitation template.
  - (b) Each nature-graded pre-registration also records the corrected noisy-sim prediction, so the chip's departure from its own description is a separate, scored quantity.
- **More scored events per QPU second, honestly.** Several jobs carry secondary predictions that can be pre-registered as separate scored events at no extra cost:
  - P3-11's eigenstate CbD value;
  - P3-3's drift;
  - P3-7's n*, as an interval forecast.
  
  They are correlated with their parent bets, and the ledger must mark them as such and not count them as independent.
- **Path dependence (Q4).** This program is seeded by program 1: its Stage 1 gap, its witness data, its CbD instrument and gold map directions 7, 8 and 11. It is not an independent seed.
- **What the engine got wrong before data, caught by reading.**
  - The gold map's QPU cost model was off by about 4–6× for direction 7.
  - The scout's working belief that "crossing 0.5 proves coherent error" was wrong (D, Aer and T1 note).
  - The brief described several sources wrongly: Knee 2016's method, Nigg 2016's platform, the device in McKay 2023, the authors of 2407.08828.
  
  These count toward Q2's "overclaims caught" tally, as caught by reading rather than by an auditor.
