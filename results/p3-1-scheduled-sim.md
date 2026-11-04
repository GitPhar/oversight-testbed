# P3-1 result: the simulator was not just set up wrong

Pre-registration: `experiments/p3-1-scheduled-sim.md` (commit `bbd6348`, 15:34; seed commit `593f8fd`, CURBy-RNG pulse 1591379 at 15:35). Run 2026-11-04 on the laptop: $0, 0 QPU s. **Verdict: fail** (unaudited). Engine odds were 0.07. Human odds were not recorded.

## In plain English

In program 1, the chip answered "yes" 50% of the time on one circuit, where its own simulator said 25%. We asked whether that was our mistake. The simulator we used lets a waiting qubit decay only if the circuit is first laid out in time, and ours wasn't. So we rebuilt the exact circuit the chip ran, laid it out in time the way the chip runs it, loaded the chip's error rates from that afternoon, and simulated it again 100,000 times.

**The fix makes almost no difference.** The corrected simulator says 26.8% "yes". Without the fix, our rebuild says 26.7%, which reproduces program 1's 25.1% within the pre-registered tolerance, so the rebuild is faithful. The pass mark was 40%. The whole circuit lasts under 10 millionths of a second, and the qubits keep their state for 90 to 200 millionths of a second. There isn't enough waiting for decay to matter. That was the pre-mortem's guess.

So the gap is not our set-up. Either the chip's errors were larger than its calibration said that afternoon, or they were of a kind the simulator does not model. Two rough variations point the same way, though neither was scored. Adding a small systematic "twist" to every two-qubit gate changes nothing (26.7%). Tripling every error rate, about what published work says such models need on this chip family, only reaches 27.7%. Simply turning up noise of the modelled kind pulls answers toward randomness, not toward the chip's pattern.

One detail stands out: the qubit that moved most (physical qubit 125, from 75% "1" in the ideal circuit to 30% on the chip) is the one whose T2, its phase memory, was worst that afternoon (44.6 µs, against 86–191 µs for the others). That was noticed after the data, so it is a lead, not a finding.

**What this changes.** This scheduled model is now the program's "corrected simulator", and every later program-3 prediction uses it. P3-2 and P3-3 will ask whether the extra error is systematic (twirling should then remove it) or tied to these nine qubits (other qubits should then agree with the simulator).

## Tables

**Primary** (100,000 shots each; seed32 1158620522; P(yes) by `readout.quantum_readout`, q01 web):

| run | P(yes) | SE |
|---|---|---|
| ideal (archived, 1,000 shots) | 0.294 | — |
| program 1 noisy sim (archived, 1,000 shots) | 0.251 | — |
| **control:** rebuild, unscheduled | **0.267** | 0.0014 |
| **primary:** rebuild, ALAP-scheduled (87 delays) | **0.268** | 0.0014 |
| hardware (archived, 1,000 shots) | 0.502 | 0.016 |

- Control within 0.251 ± 0.03: **yes** (0.267), so the test is testable.
- Scheduled ≥ 0.40: **no** (0.268), so **fail**.
- Gap closed: (0.268 − 0.251) / (0.502 − 0.251) = **7%**. The scheduled-minus-control difference is +0.001.
- Scheduled circuit duration: 9.6 µs (FakeFez durations).

**Exploratory, not scored** (20,000 shots each):

| variant | P(yes) |
|---|---|
| E2: scheduled + ZZ phase 0.1 rad after every CZ | 0.267 |
| E3: scheduled, every error ×3, T1 and T2 ÷3 | 0.277 |
| E1: temperature > 0 | not run (FakeFez has no qubit frequencies; stated in the pre-registration) |

**Per-qubit P(1)**, by classical bit (physical qubit), secondary. The hardware row was already seen by the scout (map disclosure).

| clbit (physical) | 0 (117) | 1 (125) | 2 (124) | 3 (123) | 4 (144) | 5 (136) | 6 (143) | 7 (141) | 8 (142) |
|---|---|---|---|---|---|---|---|---|---|
| ideal (archived) | 0.62 | 0.75 | 0.78 | 0.90 | 0.64 | 0.64 | 0.69 | 0.48 | 0.64 |
| program 1 noisy sim | 0.65 | 0.72 | 0.73 | 0.88 | 0.64 | 0.67 | 0.68 | 0.46 | 0.64 |
| control (unscheduled) | 0.62 | 0.71 | 0.75 | 0.87 | 0.65 | 0.65 | 0.69 | 0.47 | 0.64 |
| scheduled | 0.61 | 0.69 | 0.73 | 0.85 | 0.63 | 0.64 | 0.68 | 0.47 | 0.64 |
| E3 (errors ×3) | 0.59 | 0.65 | 0.69 | 0.79 | 0.60 | 0.61 | 0.65 | 0.48 | 0.61 |
| **hardware** | 0.50 | **0.30** | 0.50 | 0.72 | 0.42 | 0.48 | 0.61 | 0.49 | 0.46 |

Every simulator variant stays within about 0.1 of ideal on every qubit. The hardware drops by 0.12 to 0.45 on eight of nine.

**Pre-mortem** ("idle relaxation over a roughly 10–20 µs circuit … is far too small"; kind `world`). For the auditor to score: the circuit was 9.6 µs, and the scheduled-minus-unscheduled shift was +0.001.

Data: `results/p3-1-scheduled-sim.json` (all counts). Code: `experiments/p3_1_scheduled.py`, `experiments/p3sim.py`.
