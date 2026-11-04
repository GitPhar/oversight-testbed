# P3-2 and P3-3 result: the gap was gone today, so neither bet could be tested

Pre-registrations: `experiments/p3-2-twirl-dd.md` (commit `534b3eb`, seed `80db49d`, CURBy-RNG 1591393) and `experiments/p3-3-layouts.md` (`4d1fea0`, seed `ce9e186`, CURBy-RNG 1591395). The predictions and all 200 circuits were committed before submission (`cd2963a`). One job on `ibm_fez`, `dblrect8ft8s738tl2v0`, submitted 15:52:35 and run 15:52:36–15:52:51 America/Denver, 2026-11-04, via `run_hardware`. **Billed 8.0 QPU s** (estimate 7.6 s, so the 1.5× re-costing rule is not triggered). Cumulative project use: **54 s** of the 420 s hard stop. **Verdicts: P3-2 untestable, P3-3 untestable** (unaudited). Engine odds 0.25 and 0.12. Human odds not recorded.

## In plain English

On 3 November, program 1's circuit made the chip say "yes" 50% of the time, where the chip's own description predicted about 25%. Three of this program's first bets were built to find out why. Today, one day later, we ran the identical circuit on the identical nine qubits, 2,000 times. **The chip said "yes" 24.6% of the time. The corrected simulator, using today's calibration, predicted 26.9%.** The big disagreement did not come back.

That makes both chip bets untestable by the rules written before the run. P3-2 asked whether scrambling the errors (twirling) closes at least half the gap. P3-3 asked whether other qubits show less than half the gap. Each rule needs a gap to work on, and the pre-registration said in advance that below 0.125 (P3-2) or 0.10 (P3-3) the question cannot be answered. Today's gap is 0.023. This is not a pass or a fail, and it is not scored.

**What it suggests, not scored.** Program 1's 50% looks like something that happened to this chip on 3 November, not a fixed property of these nine qubits or of the simulator. Its cause is unknown. The difference between the two days (0.502 against 0.246) is about 14 standard errors. Only a repeat, the drift check this session was told not to run, can say how often such afternoons happen. That makes it the most useful next chip test. It also changes how P3-1 and P3-5 read: they described one unusual afternoon's data.

**The rest of the job, all secondary:**
- **Twirling** moved the answer by +0.047 (z = 3.8). It went *past* the simulator, to 0.293 against 0.269, so it changed the error without simply removing it. Gate twirling alone moved it +0.038. **Decoupling** moved it +0.010, which is not distinguishable from zero. Both together moved it +0.031.
- **The pre-registered defaults for waves 2–3: twirling off, decoupling off.** Twirling's shift of 0.047 is just under the 0.05 bar the rule set. Decoupling did not help.
- **The two other sets of nine qubits** also agree with the simulator: 0.277 against 0.265, and 0.297 against 0.264.
- **One qubit's readout is much worse than IBM reports.** On physical qubit 141, the job's own readout check read a prepared 0 as 1 21% of the time, and a prepared 1 as 0 11% of the time. IBM's calibration, read at the moment the job ran, says about 1%.
- **The deep "mirror" check** runs the circuit forward and then backward, so a perfect device returns where it started. The chip got all nine qubits right in 2.2% of runs. A simulation run afterwards with the same noise model (not pre-registered) expects 13.6%. So on a circuit twice as deep, the chip still falls well short of its description, even on a day when the forward circuit agrees.

## Tables

**Arms** (20 instances × 100 shots each, interleaved in a seeded order; P(yes) by `readout.quantum_readout` on raw pooled counts, with masked bits flipped back; SE from instance spread):

| arm | what | P(yes) | SE |
|---|---|---|---|
| S | corrected-sim prediction, original layout (live calibration 15:51, 100,000 shots) | 0.269 | 0.001 |
| **A** | **as run (identical to program 1's circuit and qubits)** | **0.246** | 0.008 |
| B | gate + measurement twirl | 0.293 | 0.009 |
| B2 | gate twirl only | 0.284 | 0.010 |
| C | DD XY4 | 0.256 | 0.009 |
| D | twirl + DD | 0.277 | 0.010 |
| L1 | original circuit on qubits 20, 21, 22, 23, 2, 16, 3, 5, 4 (sim 0.265) | 0.277 | 0.012 |
| L2 | original circuit on qubits 97, 87, 88, 89, 98, 90, 91, 93, 92 (sim 0.264) | 0.297 | 0.011 |
| program 1, Nov 3 | the same circuit and qubits, 1,000 shots (archived) | 0.502 | 0.016 |

**P3-2** (pre-registered rule, §5): |P_A − S| = **0.023 < 0.125**, so **untestable**. For the record: m_B = +0.047 toward S at z = 3.8 (it overshoots S by 0.024); m_B2 = +0.038 (z 3.0); m_C = +0.010 (z 0.8); m_D = +0.031 (z 2.4).

**P3-3** (pre-registered rule, §5): g_orig = **0.023 < 0.10**, so **untestable**. For the record: g_L1 = 0.012, g_L2 = 0.033.

**Defaults for waves 2–3** (rule fixed in P3-2 §5): twirl **off** (|P_B − P_A| = 0.047 < 0.05, although z = 3.8); DD **off** (m_C = 0.010 < 0.05).

**Per-qubit P(1)** by classical bit (physical qubit on the original layout). For R0 and R1 the row is the readout error. For M it is the per-qubit error rate after flipping to the ideal outcome.

| row | 0 (117) | 1 (125) | 2 (124) | 3 (123) | 4 (144) | 5 (136) | 6 (143) | 7 (141) | 8 (142) |
|---|---|---|---|---|---|---|---|---|---|
| S (sim, today) | 0.59 | 0.65 | 0.70 | 0.83 | 0.63 | 0.63 | 0.67 | 0.47 | 0.62 |
| A (chip, today) | 0.60 | 0.51 | 0.74 | 0.78 | 0.63 | 0.64 | 0.69 | 0.54 | 0.68 |
| chip, Nov 3 (archived) | 0.50 | 0.30 | 0.50 | 0.72 | 0.42 | 0.48 | 0.61 | 0.49 | 0.46 |
| B (twirled) | 0.57 | 0.62 | 0.66 | 0.78 | 0.63 | 0.58 | 0.68 | 0.49 | 0.62 |
| R0: P(1 \| prepared 0) | 0.02 | 0.02 | 0.00 | 0.00 | 0.01 | 0.02 | 0.00 | **0.21** | 0.01 |
| R1: P(0 \| prepared 1) | 0.01 | 0.03 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | **0.11** | 0.00 |
| M: chip error | 0.29 | 0.25 | 0.25 | 0.36 | 0.46 | 0.45 | 0.62 | 0.47 | 0.27 |
| M: sim error (post hoc) | 0.21 | 0.19 | 0.22 | 0.28 | 0.26 | 0.37 | 0.36 | 0.27 | 0.19 |

Qubit 125 is still the largest single-qubit departure today (0.51 against 0.65), but it is far smaller than on Nov 3 (0.30). Its T2 was 56 µs at execution, still the worst of the nine.

**Mirror** (exploratory): P(all 9 correct) = **0.022** on the chip. A post-hoc corrected-sim run on the same 20 circuits (`data/p3-2-3-mirror-posthoc-sim.json`; not pre-registered) gives 0.136.

**Calibration** at prediction time is in `data/p3-2-3-predictions.json`; at execution start, read with `backend.properties(datetime=…)`, it is in `data/p3-2-3-exec-calibration.json`. Qubit 141's reported readout error at execution: 0.011 (P(1|0) 0.011, P(0|1) 0.011).

**Pre-mortems**, for the auditor:
- P3-2 said "the departure is stochastic, not coherent, so twirling leaves P(yes) near the untwirled arm" (`world`).
- P3-3 said "the departure is device-wide … so other layouts depart as much as the original" (`world`).
- Neither named the actual reason: the departure was absent on the day. Both bets are untestable, not failed.

**Not run this session:** P3-3's two repeats ≥ 3 h apart (D0). After today, they are the direct test of what changed between 3 and 4 November.

Data: `data/p3-2-3-raw.json` (all counts), `results/p3-2-3-job.json` (analysis). Code: `experiments/p3_2_3_job.py --analyse`.
