# P3-2 and P3-3 result: the gap was gone today, so neither bet could be tested

> Audited 2026-11-04 (round 2, entangled-mind audit2 8091d01, audits/ng-p3-2-3.md): verdict stands (P3-2 untestable, P3-3 untestable); 13 of 15 required cuts applied in D5 (cuts 14 and 15 are in README.md and map/program-3-map.md and were not applied here; see D5).

Pre-registrations: `experiments/p3-2-twirl-dd.md` (commit `534b3eb`, seed `80db49d`, CURBy-RNG 1591393) and `experiments/p3-3-layouts.md` (`4d1fea0`, seed `ce9e186`, CURBy-RNG 1591395). The predictions and all 200 circuits were committed before submission (`cd2963a`). One job on `ibm_fez`, `dblrect8ft8s738tl2v0`, submitted 15:52:32 (local clock); execution started 15:52:37 (IBM), America/Denver, 2026-11-04, via `run_hardware`. **Billed 8.0 QPU s** (estimate 7.6 s, so the 1.5× re-costing rule is not triggered). Cumulative project use: **54 s** of the 420 s hard stop. **Verdicts: P3-2 untestable, P3-3 untestable** (audited in round 2; see above). Engine odds 0.25 and 0.12. Human odds not recorded.

## In plain English

On 3 November, program 1's circuit made the chip say "yes" 50% of the time, where the chip's own description predicted about 25%. Three of this program's first bets were built to find out why. Today, one day later, we ran program 1's gate list on the same nine qubits, 2,000 times (without the one pre-measurement barrier the 3 November circuit had, and as 20 interleaved blocks of 100 shots rather than one block of 1,000). **The chip said "yes" 24.6% of the time. The corrected simulator, using today's calibration, predicted 26.9%.** The big disagreement in P(yes) did not come back. Qubit by qubit it is smaller but not gone: qubit 125 still reads 0.14 below the simulator (about 12 standard errors).

That makes both chip bets untestable by the rules written before the run. P3-2 asked whether scrambling the errors (twirling) closes at least half the gap. P3-3 asked whether other qubits show less than half the gap. Each rule needs a gap to work on, and the pre-registration said in advance that below 0.125 (P3-2) or 0.10 (P3-3) the question cannot be answered. Today's gap is 0.023. This is not a pass or a fail, and it is not scored.

**What it suggests, not scored.** Program 1's 50% did not recur a day later on the same nine qubits. Two runs cannot say which day was typical, and the two runs also differed in one barrier and in how the shots were grouped. Its cause is unknown. The difference between the two days (0.502 against 0.246) is about 14 standard errors. Only a repeat, the drift check this session was told not to run, can say how often such afternoons happen. That makes it the most useful next chip test. P3-1 and P3-5 explain the 3 November data; whether that afternoon was unusual is untested.

**The rest of the job, all secondary:**
- **Twirling** moved the answer by +0.047 (z = 3.8). It ended above the simulator (0.293; the model predicts 0.270 for the twirled circuits), by about 2.3 standard errors, which is not enough to say how it changed the error. Gate twirling alone moved it +0.038. **Decoupling** moved it +0.010, which is not distinguishable from zero. Both together moved it +0.031.
- **The pre-registered defaults for waves 2–3: twirling off, decoupling off.** Twirling's shift of 0.047 (95% CI 0.019–0.075) is just under the 0.05 bar the rule set, so this default is close to a tie. Decoupling did not help.
- **The two other sets of nine qubits** are also close to the simulator in P(yes): 0.277 against 0.265 (about 1 SE) and 0.297 against 0.264 (about 3 SE). Each has one qubit 0.12–0.14 below the simulator.
- **One qubit's readout is much worse than IBM reports.** On physical qubit 141, the job's own readout check read a prepared 0 as 1 21% of the time, and a prepared 1 as 0 11% of the time. IBM's calibration, read at the moment the job ran, says about 1%. It was also unstable: about 0.3 in the first third of the 15-second job and about 0.17 at the end.
- **The deep "mirror" check** runs the circuit forward and then backward, so a perfect device returns where it started. The chip got all nine qubits right in 2.2% of runs. A simulation run afterwards with the same noise model, idle periods included (not pre-registered; code not committed), expects 13.6%; without idle decay, 19.8%. The chip's 2.2% is far below either. On a circuit twice as deep, that is a lead for a pre-registered test, not a finding.

## Tables

**Arms** (20 instances × 100 shots each, interleaved in a seeded order; P(yes) by `readout.quantum_readout` on raw pooled counts, with masked bits flipped back; SE from instance spread):

| arm | what | P(yes) | SE |
|---|---|---|---|
| S | corrected-sim prediction, original layout (live calibration 15:51, 100,000 shots) | 0.269 | 0.001 |
| **A** | **as run (program 1's gate list and qubits; no pre-measurement barrier)** | **0.246** | 0.008 |
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
- Neither named the actual reason: the departure was absent on the day. Both bets are untestable, which counts as failed for pre-mortem scoring (operators/premortem.md).

**Not run this session:** P3-3's two repeats ≥ 3 h apart (D0). After today, they are the direct test of what changed between 3 and 4 November.

Data: `data/p3-2-3-raw.json` (all counts), `results/p3-2-3-job.json` (analysis). Code: `experiments/p3_2_3_job.py --analyse`.
