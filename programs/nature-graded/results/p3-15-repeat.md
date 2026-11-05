# P3-15 result: restoring the barrier did not bring back 3 November's result, and three hours later the chip agreed

Pre-registration: `experiments/p3-15-repeat.md` (commit `7f9cedf`, 17:12; seed `8118e86`, CURBy-RNG 1591477). Design-review fixes D11–D17; review `ledger/design-reviews/ng-p3-15.md`: fix-first, confirmed 17:43. Budget ruling D18 (Sean: "approve 10 s, the full design"; engine steer st-16). Engine odds 7%; human odds: none (Sean skipped). **Verdict: fail** (run 1 decides it; run 2 agrees; audited: `ledger/audits/ng-p3-15.md`, cuts applied in D27, and round 3, `ledger/audits/round-3/ng-p3-15.md`).

| | job (ibm_fez) | predictions | executed (America/Denver) | QPU s billed | cumulative of 420 |
|---|---|---|---|---|---|
| run 1 | `dbltng9kbkrc73cod80g` | `11895cd` | 2026-11-04 18:28:35–18:28:43 | 4.0 (estimate 3.4) | 58 |
| run 2 | `dbm0d9d8ft8s738tta70` | `45c20b4` (raw `fb569de`) | 2026-11-04 21:31:35–21:31:41, 3 h 03 min after run 1 | 4.0 (estimate 3.4) | 62 |

Run 2's code was committed and clean at `45c20b4` when it was submitted (guard in the orchestrator). Run 1's was not: a token-loading refactor that changed nothing the chip ran was uncommitted (engine process note).

## In plain English

*These are the sentences pre-registered in §5, applied as the rule says.*

Restoring the barrier did not bring back 3 November's result, and in this job, averaged over the two shot groupings, the barrier made no difference larger than 0.05 (assuming IBM's servers treated 3 November's identical submission the same way). The surprise was not the barrier.

PUB grouping may make a smaller difference (+0.030, 90% CI +0.006 to +0.054), which this job cannot pin down. In run 2 it was −0.002 (90% CI −0.026 to +0.022).

Three hours later the chip gave the same answers within 0.05.

*Which rules applied, so a stranger can check:*
- Run 1: BB was 0.311, below 0.40, and BB − NB was −0.008, below +0.10, so the bet **fails**.
- Run 1: the pooled barrier effect's 90% CI, −0.017 to +0.031, lies inside ±0.05, so the "no difference larger than 0.05" sentence applies.
- Run 1: the pooled grouping effect's CI is not inside ±0.05, and the effect is not ≥ 0.10 at z ≥ 3, so the "smaller difference" sentence applies. The "held fixed or could not vary" add-on does **not** apply.
- Run 1: the execution spans show the barrier block ran in the same span as the no-barrier block (PUBs 0 and 1 together). So, by the D14 rule, the blocks do **not** count as contiguous, and the contrast is named "PUB grouping". The same holds in run 2 (PUBs 30 and 31 together).
- Run 1: the control passed. The no-barrier interleaved arm (4 November's circuit, qubits and 100-shot pieces) gave 0.274, within 0.05 of 4 November's 0.246. Run 2's gave 0.285, also within 0.05.
- Run 2, same rule: BB 0.282 (below 0.40), BB − NB −0.029 (below +0.10), so its label is also **fail**. The labels agree, so "unstable across runs" does **not** apply.
- Drift (run 2 − run 1): pooled barrier arms −0.007 (90% CI −0.030 to +0.017), pooled no-barrier arms +0.002 (−0.022 to +0.025). Both lie inside ±0.05, so the "same answers within 0.05" sentence applies.
- *(Audit cut 2, D27.)* The barrier sentence rests on the pooled contrast, so it is scoped to the average over the two groupings. Unpooled, the barrier raised P(yes) in the interleaved pieces in both runs (+0.022, +0.027), and neither CI lies inside ±0.05. It lowered it in the blocks (−0.008, −0.029). The interaction is not significant (post hoc, uncorrected). This limits the null sentence; it is not evidence for a barrier effect.
- The verdict sentences come from run 1 alone (§3). Run 2's own contrasts are in the tables. Its grouping effect was −0.002, within ±0.05, so run 1's +0.030 did not repeat.

## Tables

**Arms** (raw counts; P(yes) by `readout.quantum_readout`; binomial SE about 0.014–0.015 per 1,000-shot arm):

| arm | what | shots per run | run 1 | run 2 | drift (90% CI) |
|---|---|---|---|---|---|
| BB | barrier, one 1,000-shot PUB | 1,000 | **0.311** | **0.282** | −0.029 (−0.063 to +0.005) |
| NB | no barrier, one 1,000-shot PUB | 1,000 | **0.319** | **0.311** | −0.008 (−0.042 to +0.026) |
| BI | barrier, 10 × 100 interleaved | 1,000 | 0.296 | 0.312 | +0.016 (−0.018 to +0.050) |
| NI | no barrier, 10 × 100 interleaved (control) | 1,000 | 0.274 | 0.285 | +0.011 (−0.022 to +0.044) |
| B pooled | BB + BI | 2,000 | 0.304 | 0.297 | −0.007 (−0.030 to +0.017) |
| N pooled | NB + NI | 2,000 | 0.297 | 0.298 | +0.002 (−0.022 to +0.025) |
| prediction | live calibration, ALAP (barrier = no barrier) | 100,000 | 0.2685 (read 18:28) | 0.2685 (read 21:31) | |
| prediction | ASAP: barrier / no barrier | 100,000 | 0.2755 / 0.2665 | 0.2755 / 0.2665 | |
| 3 November | barrier, own job of 1,000 shots (archived) | 1,000 | 0.502 | | |
| 4 November | no barrier, 20 × 100 in a 200-PUB job (archived) | 2,000 | 0.246 | | |

**Comparisons** (within each job):

| contrast | run 1 Δ (90% CI) | class | run 2 Δ (90% CI) | class |
|---|---|---|---|---|
| BB − NB (primary) | −0.008 (−0.042 to +0.026) | within ±0.05 | −0.029 (−0.063 to +0.005) | between |
| barrier pooled, (BB + BI) − (NB + NI) | +0.007 (−0.017 to +0.031) | within ±0.05 | −0.001 (−0.025 to +0.023) | within ±0.05 |
| PUB grouping pooled, (BB + NB) − (BI + NI) | +0.030 (+0.006 to +0.054) | between | −0.002 (−0.026 to +0.022) | within ±0.05 |
| barrier, interleaved only, BI − NI (*auditor's re-analysis, post hoc; D27*) | +0.022 (−0.011 to +0.055) | not inside ±0.05 | +0.027 (−0.007 to +0.061) | not inside ±0.05 |
| predicted barrier effect | 0.000 (if ALAP), +0.009 (if ASAP) | | same | |

- Leave-one-piece-out (O3): run 1's barrier class is stable across all 20 drops, but its grouping class is **not** (one drop changes it). Run 2's two classes are both stable across all 20 drops.
- Execution spans. Run 1: span 1 (18:28:37.27–18:28:40.42) held PUBs 0–1 (BB, NB), and span 2 (18:28:40.42–18:28:42.32) held PUBs 2–31 (interleaved). Run 2: the seeded order put BB and NB last (PUBs 30–31), but span 1 (21:31:36.70–21:31:38.28) held them, and span 2 (21:31:38.29–21:31:40.16) held PUBs 0–29. So in **both** runs the two 1,000-shot PUBs executed first and together.
- Distance from uniform (O2): entropy 7.38–7.81 bits of 9 in run 1 and 7.24–7.47 in run 2. Total-variation distance 0.44–0.50 and 0.48–0.51. 3 November's output had entropy 7.92 bits (design review).

**Per-qubit P(1)** (secondary; clbit order, physical qubit in brackets):

| arm | 0 (117) | 1 (125) | 2 (124) | 3 (123) | 4 (144) | 5 (136) | 6 (143) | 7 (141) | 8 (142) |
|---|---|---|---|---|---|---|---|---|---|
| prediction (ALAP) | 0.59 | 0.65 | 0.71 | 0.83 | 0.63 | 0.63 | 0.67 | 0.47 | 0.62 |
| run 1 BB | 0.55 | 0.51 | 0.74 | **0.60** | 0.61 | 0.65 | 0.65 | 0.47 | 0.68 |
| run 1 NB | 0.58 | 0.52 | 0.74 | **0.59** | 0.59 | 0.65 | 0.65 | 0.47 | 0.70 |
| run 1 BI | 0.60 | 0.47 | 0.71 | 0.74 | 0.61 | 0.67 | 0.67 | 0.47 | 0.67 |
| run 1 NI | 0.60 | 0.49 | 0.74 | 0.75 | 0.62 | 0.70 | 0.66 | 0.50 | 0.71 |
| run 2 BB | 0.63 | 0.70 | 0.68 | 0.82 | 0.60 | 0.61 | 0.66 | 0.46 | 0.63 |
| run 2 NB | 0.60 | 0.66 | 0.67 | 0.80 | 0.61 | 0.61 | 0.66 | 0.49 | 0.62 |
| run 2 BI | 0.62 | 0.68 | 0.67 | 0.81 | 0.57 | 0.58 | 0.64 | 0.50 | 0.62 |
| run 2 NI | 0.62 | 0.70 | 0.69 | 0.79 | 0.63 | 0.61 | 0.65 | 0.47 | 0.64 |

**Readout** (R0, R1; error rates): P(1 | 0) at most 0.026 (qubit 125) in both runs. P(0 | 1) at most 0.028 (qubit 141) in run 1 and 0.018 (qubit 125) in run 2. Qubit 141's large readout error on 4 November (P(1 | 0) 0.21) is not present today.

**Noticed after the data; leads, not findings:**
- Run 1: qubit 123 read 0.59–0.60 in the two 1,000-shot PUBs, against 0.74–0.75 in the interleaved pieces and 0.83 predicted. That one qubit carried most of run 1's +0.030 PUB-grouping difference. **Run 2 did not repeat it:** qubit 123 read 0.80–0.82 in the blocks and 0.79–0.81 interleaved, although the blocks again executed first. So position in time within the job does not explain run 1's dip by itself.
- Qubit 125 read 0.47–0.52 in run 1 (as on 4 November, 0.13–0.18 below prediction), but 0.66–0.70 in run 2, at the prediction. Qubit 124 moved the other way (0.71–0.74, then 0.67–0.69). Individual qubits moved by about 0.2 in three hours, but P(yes) moved by at most 0.03 per arm.
- Every arm in both runs sits above the prediction: 0.274–0.319 against 0.2685. Pooled over the four arms, 0.300 (4,000 shots) in run 1 and 0.2975 in run 2, which are 4.5 and 4.1 binomial SEs above the prediction; P3-16's four arms (0.297–0.319) sit above its 0.2717 the same way. Both P3-15 predictions use the same inputs, so within P3-15 this is one comparison made twice, not two (audit note B9; see below), and across P3-15 and P3-16 it is the same chip against the same 4 November calibration read. It is post hoc and uncorrected, and it stays a lead; nothing pre-registered covers it (audit round 3).

**Was run 2's calibration live?** (audit note B9) Yes, but IBM had not re-measured these qubits. Each `--predict` was a fresh process: `backends.backend()` builds the target from IBM's server, and qiskit-ibm-runtime caches properties only in memory, per process. The document timestamp (`last_update_date`) advances every hour (18:09, 21:09; 21:34 at a read-only re-check at 21:46). But the per-qubit T1 values are dated 2026-11-04 12:04 (qubit 143: 03:21), and the 21:46 re-read returned the same T1, T2 and readout error as both runs to the last digit. So both predictions used IBM's 12:04 measurements. They cannot see the ~0.2 per-qubit moves between the runs (qubit 125: 0.47–0.52, then 0.66–0.70).

**Pre-mortem** ("IBM's servers already schedule measurements as late as possible, so the barrier changes nothing and both 1,000-shot blocks read about 0.25, as 4 November did"; kind `world`). For the auditor: the barrier changed nothing (−0.008 in run 1, −0.029 in run 2, both below the bar). The blocks read 0.28–0.32, not about 0.25. Whether IBM schedules ALAP is not observed.

Data: `data/p3-15-run1-raw.json`, `data/p3-15-run2-raw.json` (counts, per-shot bitstrings, execution spans), `results/p3-15-repeat.json`. Code: `experiments/p3_15_repeat.py --analyse`.
