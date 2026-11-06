# P3-9 result: the contextuality check saw contextuality in three of the four chip systems, but not in the fourth, where the chip's own measurement errors let a non-quantum explanation fit (fail)

Pre-registration: `experiments/p3-9-peres-mermin.md` (commit `96cccf4`, 2026-11-05 16:20; seed `8c56681`, CURBy-RNG 1592865). Design review `ledger/design-reviews/ng-p3-9.md`: fix-first (4 flaws, `aee8d85`), fixes D49 (`102f7e8`) and D50 (`d9fbab1`), confirmed 17:53 (`b20ea79`). Budget ruling br-025 (45 QPU s under st-16, `a939980`). Simulator prediction committed before submission (`b1a06a5`). Job `dbmib3t8mdtc73d80on0` on ibm_fez, qubits (3, 4, 5), created 17:55:43, ran 18:08:19–18:08:52 America/Denver; **28.0 QPU s** billed (estimate 28.9, cap 45); raw counts committed at once (`5c55784`). Analysis `experiments/p3_9_pm.py --analyse`, $0. Engine odds 0.80 (first 0.40); Sean's odds 0.90. **Verdict: fail. Not yet audited.**

**Limits first.** This is one chip, one qubit triple, one job, one evening. The chip is a referee and the object measured here, never a computational resource. Its counts decide a pre-registered bet about this device, and nothing uses them as an estimate of anything else. The result says nothing against quantum theory and nothing about language models. It cannot say which physical mechanism made the chip's sequential measurements worse than predicted: the design measures the disturbance, it does not identify its cause.

## In plain English

We pointed the "does the answer depend on what else was asked?" check, an exact version of the one program 1 used on a language model, at a textbook quantum experiment (the Peres–Mermin square) run on IBM's chip. Physics says the effect must be there. The check had to find it in all four set-ups: two starting states, each measured in two orders. It found it in three. In the fourth (the entangled starting state, measured in reverse order), the chip's measurements disturbed one another so much that a non-quantum explanation with that much disturbance fitted the counts. So the bet fails by its rule. The failure is the chip's measurement quality, not the check and not physics.

*These are the sentences pre-registered in §5, applied as the rule says.*

Fail by the rule: the check saw contextuality for the |00⟩ input in both orders, but not for the Bell-state input in both orders. Wherever it missed, the raw sum still beat the classical bound, so what failed is the chip's measurement quality under CbD's correction, not quantum theory.

For the |00⟩ input measured in the square's order, the exact CbD linear program rejects noncontextuality (CNT2's 99% lower bound 0.0460 > 0).

For the |00⟩ input measured in reverse order, the exact CbD linear program rejects noncontextuality (CNT2's 99% lower bound 0.0375 > 0).

For the Bell-state input measured in the square's order, the exact CbD linear program rejects noncontextuality (CNT2's 99% lower bound 0.0834 > 0).

For the Bell-state input measured in reverse order, the raw Peres-Mermin sum still beat the classical bound of 4 (99% lower bound 4.334), but the chip's measurements disturbed each other enough that CbD could not tell the result from a noncontextual system with that disturbance (CNT2's 99% lower bound 0.0000): noise spoiled the check here, not quantum theory.

For the Bell-state input, one order passed and the other did not, so the order of the measurements mattered on this chip (by CbD 2.0 Theorem 3 the system with order folded into context is still contextual for that input).

*What this does and does not say.*
- **The fail rests on one line.** Leave-one-out was pre-registered as a report, not a gate (§4). In the Bell-reverse system, replacing line R3's counts with the simulator's prediction for R3 gives CNT2 0.106; replacing any of the other five lines leaves it at 0. In the three contextual systems, no single replacement moves CNT2 to zero.
- **R3 in reverse order measures Y1Y2 first, then X1Z2, then Z1X2.** On the chip, the second and third outcomes had means +0.422 and −0.394 for the Bell input (−0.27 for Z1X2 with |00⟩). Quantum theory and the noisy simulator both give 0 there (simulator: +0.005, −0.005). That is a large disturbance carried from earlier measurements into later ones in that line, which is what CbD corrects for. Its size is why the correction absorbed the sum. The design cannot tell where it comes from: ancilla readout, reset, crosstalk onto the data qubits, or a calibration error in the Y rotations.
- **This was the pre-mortem's mechanism in shape, not shown in cause.** The pre-mortem said that mid-circuit readouts and resets on ancilla 4 would disturb the data qubits, more with each later measurement, until CNT2 reached 0 in at least one system. CNT2 reached 0 in one system, and the biases sit in the later positions, but nothing here isolates the ancilla.
- **The chip did much worse than the simulator predicted, everywhere.** χ was 4.35–4.69 against a predicted 5.72–5.79. Each line's product had magnitude 0.65–0.74 against the simulator's 0.95–0.96. The simulator holds IBM's reported gate, readout and T1/T2 errors, and omits mid-circuit-measurement crosstalk, reset error and idle decay (§2). The gap says those omissions, or the calibration, matter for this circuit. It is not a quantum advantage and not a fault in quantum theory.
- **Sean's card event holds; the scored event does not.** His card asked whether the check rejects noncontextuality "for both input states". The scored event tightened that to "in both orders" (D48). Under his card's wording it holds, as a reported secondary (§4): |00⟩ in both orders, the Bell state in forward order, and by CbD 2.0 Theorem 3 the order-folded system is contextual for both states. The bet is scored on the pre-registered event, so the outcome is 0.
- **What it says about program 1.** The linear program can say "contextual" on real counts where physics fixes the answer: it did so three times out of four here, with lower bounds 0.04–0.08. It also shows that heavy measurement disturbance can hide a real effect from it. It does not show that program 1's Γ had the power to detect contextuality at program 1's sample sizes (§6).

*Citation correction (D51):* the pre-registration's §0 cites the 2019-era IBM figure (about 4.99) as "Laghaout et al. 2022"; its first author is Dikme (Dikme, Reichel, Laghaout & Björk 2022, Eur. J. Phys. 43:055401, arXiv:2009.10751), as the Novelty session found. The frozen text is left as committed.

*Novelty line, written by a fresh session that did not run the bet (a subagent of the p3-9 worktree session, claude-opus-5-5), after its own search; inserted verbatim:*

**Novelty:** partly new. Both Contextuality-by-Default (CbD) analyses of quantum hardware data that I found say contextuality survives the measured inconsistent connectedness. One is Lapkiewicz et al.'s photonic KCBS data: the conservative interval is [3.127, 4.062] against a bound of 3 (Kujala, Dzhafarov & Larsson 2015, PRL 115:150401, arXiv:1412.4724). The other is Kirchmair et al.'s sequential ion Peres–Mermin data, with CNTX = 0.566 from an adapted formula, not the exact LP (Massé 2021, arXiv:2105.13821, unrefereed). Earlier work also said a disturbance-corrected test of the full sequential square was out of reach: Kirchmair et al. 2009 (Nature 460:494, arXiv:0904.1655) violated their disturbance inequality only on part of the square (2.23(5) > 2), and Gühne et al. 2010 (PRA 81:022121, arXiv:0912.4846) showed the error terms must average below 0.0417. No paper was found that applies the exact CbD 2.0 LP (CNT2) to sequential Peres–Mermin data from superconducting hardware. The ancilla/mid-circuit square on Google's processor reports only raw χ = 5.618 ± 0.005, with no marginal or signalling analysis (Kumar et al. 2025, arXiv:2512.02284), and the IBM squares give raw values only (5.3076 on ibm_kingston, no error bars, Kelleher & Holweck 2025, arXiv:2505.21243; 4.987 from products only, already worse in one measurement order, Dikme et al. 2022, Eur. J. Phys. 43:055401, arXiv:2009.10751). Ours agrees with the CbD record in three systems. It points the other way in the fourth (Bell input, reverse order), where CbD's correction for the measured disturbance absorbed a raw χ of 4.40, which fits the known excess of IBM mid-circuit-measurement error over calibration (7.98–26.1% observed against 0.72–1.0% predicted on ibmq_algiers; Hothem et al. 2024, arXiv:2410.16706). Search: WebSearch and the arXiv API (sorted newest first, checked through 2026-11), on "contextuality-by-default" (all 46 arXiv hits listed), "inconsistent connectedness", CbD + KCBS/Peres–Mermin experimental data, Peres–Mermin/Mermin–Peres/magic square + superconducting/IBM/mid-circuit, contextuality + "compatibility loophole", sequential-measurement disturbance (Szangolies, Gühne), "mid-circuit measurement crosstalk IBM", "no-signaling violation IBM quantum computer", "signaling in time" + quantum computer; 2026-11-05. claude-opus-5-5.

## Tables

**The four systems** (4,000 shots per circuit; bootstrap B = 1,000, seed from the beacon's `boot` sub-seed; 99% lower bound = the 10th smallest draw; "contextual" iff CNT2's lower bound > 1e-6):

| system | label | χ (± SE) | χ 99% lower | CNT2 | CNT2 99% lower | CNT2 boot median | draws at 0 | Δ0 | Massé CNTX | predicted χ / CNT2 / Δ0 (noisy sim) |
|---|---|---|---|---|---|---|---|---|---|---|
| \|00⟩, forward | contextual | 4.688 (± 0.024) | 4.634 | 0.0663 | 0.0460 | 0.0640 | 0 | 0.125 | 0.219 | 5.787 / 0.227 / 0.013 |
| \|00⟩, reverse | contextual | 4.623 (± 0.024) | 4.569 | 0.0572 | 0.0375 | 0.0516 | 0 | 0.351 | 0.000 | 5.785 / 0.227 / 0.024 |
| Bell, forward | contextual | 4.345 (± 0.027) | 4.286 | 0.1031 | 0.0834 | 0.0974 | 0 | 0.225 | 0.000 | 5.718 / 0.226 / 0.006 |
| Bell, reverse | absorbed | 4.399 (± 0.027) | 4.334 | 0.0000 | 0.0000 | 0.0000 | 1000 | 0.696 | 0.000 | 5.721 / 0.220 / 0.029 |

**Leave-one-out** (point CNT2 with one line's counts replaced by the noisy simulator's prediction; reported, not a gate):

| system | R1 | R2 | R3 | C1 | C2 | C3 |
|---|---|---|---|---|---|---|
| \|00⟩, forward | 0.0663 | 0.1086 | 0.0996 | 0.0971 | 0.0813 | 0.0987 |
| \|00⟩, reverse | 0.0572 | 0.0778 | 0.1188 | 0.0674 | 0.0597 | 0.0982 |
| Bell, forward | 0.1212 | 0.1102 | 0.1339 | 0.1240 | 0.1207 | 0.1031 |
| Bell, reverse | 0.0000 | 0.0000 | 0.1064 | 0.0000 | 0.0000 | 0.0000 |

**Lines R3 and C3, outcome means in measurement order** (±1 units; chip against the noisy simulator):

| state | line | order | observables in order | chip means | chip product | simulator means | simulator product |
|---|---|---|---|---|---|---|---|
| \|00⟩ | R3 | forward | Z1X2, X1Z2, Y1Y2 | +0.012, −0.006, −0.015 | +0.665 | −0.006, +0.001, −0.000 | +0.959 |
| \|00⟩ | R3 | reverse | Y1Y2, X1Z2, Z1X2 | +0.010, +0.057, −0.266 | +0.662 | −0.001, +0.002, −0.001 | +0.956 |
| \|00⟩ | C3 | forward | Z1Z2, X1X2, Y1Y2 | +0.930, +0.014, −0.033 | −0.735 | +0.987, +0.001, +0.000 | −0.957 |
| \|00⟩ | C3 | reverse | Y1Y2, X1X2, Z1Z2 | +0.014, −0.024, +0.636 | −0.661 | −0.001, +0.001, +0.968 | −0.957 |
| Bell | R3 | forward | Z1X2, X1Z2, Y1Y2 | −0.008, +0.010, −0.588 | +0.650 | +0.000, +0.001, −0.956 | +0.946 |
| Bell | R3 | reverse | Y1Y2, X1Z2, Z1X2 | −0.881, +0.422, −0.394 | +0.664 | −0.973, +0.005, −0.005 | +0.946 |
| Bell | C3 | forward | Z1Z2, X1X2, Y1Y2 | +0.900, +0.752, −0.656 | −0.698 | +0.977, +0.968, −0.956 | −0.946 |
| Bell | C3 | reverse | Y1Y2, X1X2, Z1Z2 | −0.871, +0.686, +0.648 | −0.675 | −0.973, +0.967, +0.958 | −0.947 |

**Secondary comparisons** (reported, never promoted):
- Kelleher & Holweck's 5.31 on another Heron r2 (ibm_kingston) was the best of several embedded squares, measured with another readout and with no error bars. Every system here is lower (4.35–4.69). The comparison is loose: an upward-selected figure from another device (D49).
- The calibration of qubits 3, 4 and 5 was identical in the reads at submission and at run time (IBM's `last_update_date` 17:35:25 both times).
  - T1/T2: 210/222, 170/121, 270/121 µs.
  - Readout error: 2.73%, 0.38%, 1.70%.
  - CZ error: 0.33% (3–4), 0.22% (4–5).
  - These are not the values read at preparation (10:09, `data/p3-9-prepared.json`). The simulator's prediction used those earlier values, as frozen.

**QPU:** 28.0 s billed against 28.9 estimated and 45 approved (br-025). Cumulative **117 s** of the 420 s hard stop: 46 s from program 1, 71 s from program 3 (wave 1 8 s, P3-15 8 s, P3-16 7 s, P3-18 20 s, P3-9 28 s).
