# P3-1 re-run with the bugs fixed: still fail; the gate twist, now actually applied, is the one variation that moves

Pre-registered as DEVIATIONS.md **D8** (commit `7acdc3c`, 16:48, before running), after audit round 2 (entangled-mind audit2 `8091d01`, `audits/ng-p3-1.md`). Same seed (seed32 1158620522; no new beacon draw), same shots, same §5 rule as `experiments/p3-1-scheduled-sim.md`. Run 2026-11-04 on the laptop: $0, 0 QPU s. **Verdict: fail** (re-run; audited in round 3, `ledger/audits/round-3/ng-p3-1.md`: fail stands, and the loaded T1/T2 equal the 3 November snapshot on all nine qubits). The first run and its write-up (`results/p3-1-scheduled-sim.md`, `.json`) are unchanged and still reproduce exactly with `--legacy`.

## In plain English

The first P3-1 run had two bugs. It never loaded the chip's T1 and T2 from 3 November, so it kept the 2025 values that ship with the software. And its "small twist on every two-qubit gate" variation (E2) never applied the twist. Both are now fixed and checked in code, and the pre-registered test was run again with the same seed.

**The verdict doesn't change.** The corrected simulator still says 26.8% "yes" (scheduled) and 26.8% (unscheduled control), against the chip's 50% and the 40% pass mark. These match the auditor's independent re-run to four decimals. Letting idle qubits decay, with that afternoon's real decay times, still makes no difference.

**One exploratory variation does move.** Adding a small systematic twist (0.1 rad of ZZ phase) after every two-qubit gate, which the first run thought it had tested, now runs and gives **33.7%**. Tripling every error rate of the modelled, random kind gives only 28.8%. So a modest *steering* error moves this circuit's answer toward the chip's much more than three times the random error does. That fits the post-hoc qubit-125 lead in the P3-2/P3-3 write-up, where gate twirling nearly removed that qubit's departure. It was not scored, it is one value of one parameter, and it is a reason to pre-register a twist sweep, not a finding.

**The extra control the audit suggested doesn't help much here.** The audit noted that a noiseless simulator also passes the pre-registered control. We added, as a reported check only, a qubit-by-qubit comparison with program 1's archived simulation. It barely separates the two: worst qubit 2.6 standard errors off for the noiseless model, 1.8 for ours. The archived simulation has only 1,000 shots, too few to tell them apart.

## Tables

| run | first run (bugs on) | **re-run (D8, fixed)** | auditor's fixed re-run |
|---|---|---|---|
| control, unscheduled, 100,000 shots | 0.2671 | **0.2679** | 0.26787 |
| primary, ALAP-scheduled, 100,000 shots | 0.2679 | **0.2678** | 0.26778 |
| E2: scheduled + ZZ 0.1 rad per CZ, 20,000 | 0.2673 (twist not applied) | **0.3367** | — |
| E3: scheduled, errors ×3, T1 and T2 ÷3, 20,000 | 0.2765 (T1/T2 not divided) | **0.2878** | 0.288 |

- Control within 0.251 ± 0.03: **yes**. Scheduled ≥ 0.40: **no**. Verdict: **fail**.
- T1/T2 now loaded, for example qubit 125: T1 143.4 µs, T2 44.6 µs (snapshot values; recorded in `t1t2_check`).
- Scheduled-minus-control: −0.0001 at this seed. The auditor's ten seeds give −0.0002 ± 0.0010, so idle decay closes about 0% of the gap.

**Per-qubit P(1)** (re-run, secondary):

| clbit (physical) | 0 (117) | 1 (125) | 2 (124) | 3 (123) | 4 (144) | 5 (136) | 6 (143) | 7 (141) | 8 (142) |
|---|---|---|---|---|---|---|---|---|---|
| scheduled (re-run) | 0.61 | 0.69 | 0.73 | 0.85 | 0.64 | 0.64 | 0.68 | 0.47 | 0.63 |
| E2 (ZZ 0.1 rad, re-run) | 0.56 | 0.58 | 0.64 | 0.81 | 0.56 | 0.62 | 0.66 | 0.51 | 0.60 |
| hardware, Nov 3 (archived) | 0.50 | 0.30 | 0.50 | 0.72 | 0.42 | 0.48 | 0.61 | 0.49 | 0.46 |

E2 moves every qubit except 141 toward the 3 November chip values, qubit 125 by the most (0.69 → 0.58). It is still far from 0.30.

**Marginal control** (reported, not a gate; D8): max over the 9 qubits of |marginal − archived noisy-sim marginal| / that marginal's 1,000-shot SE. Noiseless model: **2.61** (P(yes) 0.279). Our unscheduled control: **1.78**. The check does not discriminate at this archive size.

**Corrected-simulator adoption** was **held** until an auditor checked this fix (D8). It has now been checked twice on the record: the ng-p3-15 design review ran the fixed code (its `dry4.py`: the snapshot's T1/T2 reach the noise model, and a 0.1 rad ZZ moves P(yes) from 0.268 to 0.337), and audit round 3 confirmed that this re-run's `t1t2_check` equals the snapshot on all nine qubits and that its P(yes) values regenerate from the archived counts. Lifting the hold needs a DEVIATIONS row from the owning session.

Data: `results/p3-1-rerun.json`. Code: `experiments/p3_1_scheduled.py --rerun`, `experiments/p3sim.py` (fixed `overwrite_calibration` and `simulator`).
