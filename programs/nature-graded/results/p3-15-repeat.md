# P3-15 result, run 1: restoring the barrier did not bring back 3 November's result

Pre-registration: `experiments/p3-15-repeat.md` (commit `7f9cedf`, 17:12; seed `8118e86`, CURBy-RNG 1591477). Design-review fixes D11–D17; review `ledger/design-reviews/ng-p3-15.md`: fix-first, confirmed 17:43. Budget ruling D18 (Sean: "approve 10 s, the full design"; engine steer st-16). Predictions committed before submission (`11895cd`). Run 1 is job `dbltng9kbkrc73cod80g` on ibm_fez: executed 2026-11-04 18:28:35–18:28:43 America/Denver, **4.0 QPU s billed** (estimate 3.4), cumulative 58 s of 420. **Verdict: fail** (run 1 decides it; unaudited). Engine odds 7%; human odds: none (Sean skipped). **Run 2** is scheduled no earlier than 21:30:43, three hours after run 1 finished plus a 2-minute margin; this file will be updated when it reports.

## In plain English

*These are the sentences pre-registered in §5, applied as the rule says.*

Restoring the barrier did not bring back 3 November's result, and in this job the barrier made no difference larger than 0.05 (assuming IBM's servers treated 3 November's identical submission the same way). The surprise was not the barrier.

PUB grouping may make a smaller difference (+0.030, 90% CI +0.006 to +0.054), which this job cannot pin down.

*Which rules applied, so a stranger can check:*
- BB was 0.311, below 0.40, and BB − NB was −0.008, below +0.10, so the bet **fails**.
- The pooled barrier effect's 90% CI, −0.017 to +0.031, lies inside ±0.05, so the "no difference larger than 0.05" sentence applies.
- The pooled grouping effect's CI is not inside ±0.05, and the effect is not ≥ 0.10 at z ≥ 3, so the "smaller difference" sentence applies. The "held fixed or could not vary" add-on does **not** apply.
- The execution spans show the barrier block ran in the same span as the no-barrier block (PUBs 0 and 1 together). So, by the D14 rule, the blocks do **not** count as contiguous, and the contrast is named "PUB grouping".
- The control passed: the no-barrier interleaved arm (4 November's circuit, qubits and 100-shot pieces) gave 0.274, within 0.05 of 4 November's 0.246.

## Tables

**Arms** (raw counts; P(yes) by `readout.quantum_readout`; binomial SE):

| arm | what | shots | P(yes) | SE |
|---|---|---|---|---|
| BB | barrier, one 1,000-shot PUB | 1,000 | **0.311** | 0.015 |
| NB | no barrier, one 1,000-shot PUB | 1,000 | **0.319** | 0.015 |
| BI | barrier, 10 × 100 interleaved | 1,000 | 0.296 | 0.014 |
| NI | no barrier, 10 × 100 interleaved (control) | 1,000 | 0.274 | 0.014 |
| prediction | live calibration 18:09, ALAP (barrier = no barrier) | 100,000 | 0.2685 | 0.0014 |
| prediction | ASAP: barrier / no barrier | 100,000 | 0.2755 / 0.2665 | |
| 3 November | barrier, own job of 1,000 shots (archived) | 1,000 | 0.502 | 0.016 |
| 4 November | no barrier, 20 × 100 in a 200-PUB job (archived) | 2,000 | 0.246 | 0.008 |

**Comparisons:**

| contrast | Δ | SE | z | 90% CI | class |
|---|---|---|---|---|---|
| BB − NB (primary) | −0.008 | 0.021 | −0.39 | −0.042 to +0.026 | within ±0.05 |
| barrier pooled, (BB + BI) − (NB + NI) | +0.007 | 0.015 | +0.48 | −0.017 to +0.031 | within ±0.05 |
| PUB grouping pooled, (BB + NB) − (BI + NI) | +0.030 | 0.015 | +2.07 | +0.006 to +0.054 | between |
| predicted barrier effect | 0.000 (if ALAP), +0.009 (if ASAP) | | | | |

- Leave-one-piece-out (O3): the barrier class is stable across all 20 drops. The grouping class is **not** stable: at least one drop changes it.
- Execution spans: span 1 (18:28:37.27–18:28:40.42) held PUBs 0–1 (BB, NB); span 2 (18:28:40.42–18:28:42.32) held PUBs 2–31 (the interleaved section). So "block" and "interleaved" also differ in when they ran within the job.
- Distance from uniform (O2): entropy 7.38–7.81 bits of 9, total-variation distance 0.44–0.50. 3 November's output had entropy 7.92 bits (design review).

**Per-qubit P(1)** (secondary; clbit order, physical qubit in brackets):

| arm | 0 (117) | 1 (125) | 2 (124) | 3 (123) | 4 (144) | 5 (136) | 6 (143) | 7 (141) | 8 (142) |
|---|---|---|---|---|---|---|---|---|---|
| prediction (ALAP) | 0.59 | 0.65 | 0.71 | 0.83 | 0.63 | 0.63 | 0.67 | 0.47 | 0.62 |
| BB | 0.55 | 0.51 | 0.74 | **0.60** | 0.61 | 0.65 | 0.65 | 0.47 | 0.68 |
| NB | 0.58 | 0.52 | 0.74 | **0.59** | 0.59 | 0.65 | 0.65 | 0.47 | 0.70 |
| BI | 0.60 | 0.47 | 0.71 | 0.74 | 0.61 | 0.67 | 0.67 | 0.47 | 0.67 |
| NI | 0.60 | 0.49 | 0.74 | 0.75 | 0.62 | 0.70 | 0.66 | 0.50 | 0.71 |

**Readout** (R0, R1; error rates): P(1 | 0) at most 0.026 (qubit 125), P(0 | 1) at most 0.028 (qubit 141). Qubit 141's large readout error on 4 November (P(1 | 0) 0.21) is not present today.

**Noticed after the data; leads, not findings:**
- Qubit 123 reads 0.59–0.60 in the two 1,000-shot PUBs, against 0.74–0.75 in the interleaved pieces and 0.83 predicted. That one qubit carries most of the +0.030 PUB-grouping difference. Because the blocks also ran first in the job, it cannot be separated from position in time.
- Qubit 125 is still 0.13–0.18 below prediction in every arm, as on 4 November.
- Every arm sits above the prediction: 0.274–0.319 against 0.2685.

**Pre-mortem** ("IBM's servers already schedule measurements as late as possible, so the barrier changes nothing and both 1,000-shot blocks read about 0.25, as 4 November did"; kind `world`). For the auditor: the barrier changed nothing (−0.008). The blocks read 0.31–0.32, not about 0.25. Whether IBM schedules ALAP is not observed.

Data: `data/p3-15-run1-raw.json` (counts, per-shot bitstrings, execution spans), `results/p3-15-repeat.json`. Code: `experiments/p3_15_repeat.py --analyse`.
