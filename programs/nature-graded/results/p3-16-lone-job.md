# P3-16 result: running the 3 November circuit alone in its own job did not bring back 3 November's result

Pre-registration: `experiments/p3-16-lone-job.md` (commit `209c1e2`, 2026-11-04 22:58; seed `d09f541`, CURBy-RNG 1591823). Design review `ledger/design-reviews/ng-p3-16.md`: fix-first (`960b1f1`), fixes D31–D35 (`4820d25`), then three confirmations that did not confirm (`71ac76a`, `1f68e33`, `6cf65a5`) with fixes D36–D38 (`cf84f77`, `05e3234`, `42f824a`), and a fourth that said go (`8566cd7`, confirmed 2026-11-05 05:13). Budget ruling br-003 in `ledger/spend.jsonl` (`960e2b1`): 10 QPU s under st-16. Predictions `39ffbff`; raw counts `fe77aac`. Engine odds 5%; human odds: none. **Verdict: fail. Audited** (`ledger/audits/ng-p3-16.md`, `60eae19`): stands; 26 claims checked, 0 holes, 0 required cuts, 1 optional wording edit applied (D39); plant pl-013 was a clean draw.

| job (ibm_fez) | what | executed (America/Denver) | QPU s billed | cumulative of 420 |
|---|---|---|---|---|
| C `dbm77dpkbkrc73covuu0` | CB (barrier) + CN (no barrier), two PUBs in one job | 2026-11-05 05:16:57–05:17:18 | 3.0 (estimate 2.56) | 65 |
| B `dbm77kd8ft8s738ub8j0` | no-barrier circuit alone | 05:17:23–05:18:08 | 2.0 (estimate 2.28) | 67 |
| A `dbm780u74qds73droub0` | barrier circuit alone (3 November's packaging) | 05:18:13–05:18:35 | 2.0 (estimate 2.28) | 69 |
| total | | 1.6 minutes, first start to last finish | **7.0** of 10 approved (estimate 7.12) | **69** |

The chip was a referee here: its counts decide a pre-registered bet, and it computed nothing the engine uses.

## In plain English

*These are the sentences pre-registered in §5 (as amended D31–D38 before any data), applied as the rule says.*

Running the 3 November circuit (with its barrier) alone in its own job did not bring back 3 November's result, and for the barrier circuit, running alone or sharing a job made no difference larger than 0.05. On this run (05:17–05:18 on the morning of 5 November), running the barrier circuit alone in its own job did not raise its rate by more than 0.05 (assuming IBM's servers handled a one-circuit job the same way on 3 November).

Of the things the 4 November runs and this one varied (the barrier, the shot grouping, running alone), none brought back 3 November's result. The chip on that afternoon remains the main candidate among them, not a demonstrated cause.

Run alone, the barrier made no difference larger than 0.05.

*Audit ng-p3-16 (`60eae19`) recommended one wording edit, applied (D39): the pre-registered "This evening" became "On this run (05:17–05:18 on the morning of 5 November)", because the jobs ran in the morning. Nothing else in the sentence changed.*

*Which rules applied, so a stranger can check:*
- A (the barrier circuit alone) read 0.306, below 0.40. A − CB was −0.013 (z −0.63), below +0.10. So the bet **fails** (§5.1, §5.2). All three jobs completed with 1,000 shots per PUB, so it is not untestable (§5.3).
- A − CB's 90% CI, −0.047 to +0.021, lies inside (−0.05, +0.05), so the "within ±0.05" fail sentence applies.
- B (0.297), CB (0.319) and CN (0.315) are all below 0.40, so the "none brought back" sentence applies, and neither "B came back" nor "the shared job came back" does.
- A − B was +0.009 (90% CI −0.025 to +0.043), inside ±0.05, so "the barrier made no difference larger than 0.05" applies.
- Control: CB 0.319 is within 0.05 of P3-15's pooled 0.2965, so the "chip had moved" sentence does **not** apply.
- The three jobs ran within 1.6 minutes of each other, so the "not back to back" sentence does **not** apply.
- Job C's one execution span held both of its PUBs, so the "separate spans" sentence does **not** apply.
- The in-evening replicate, B − CN, was −0.018 (90% CI −0.052 to +0.016). It qualifies only a pass, so it adds no sentence here.

## Tables

**Arms** (raw counts; P(yes) by `readout.quantum_readout`, no readout mitigation; binomial SE about 0.015 per 1,000-shot PUB):

| arm | what | P(yes) | SE | entropy (bits of 9) |
|---|---|---|---|---|
| A | barrier circuit, alone in its own job | **0.306** | 0.015 | 7.50 |
| B | no-barrier circuit, alone in its own job | **0.297** | 0.014 | 7.65 |
| CB | barrier circuit, sharing job C with CN | **0.319** | 0.015 | 7.57 |
| CN | no-barrier circuit, sharing job C with CB | **0.315** | 0.015 | 7.58 |
| prediction | live calibration, ALAP (barrier = no barrier), 100,000 shots | 0.2717 | | |
| prediction | ASAP: barrier / no barrier | 0.2795 / 0.2693 | | |
| P3-15 (4 November) | barrier, one 1,000-shot PUB in a 32-PUB job, runs 1 and 2 | 0.311, 0.282 (pooled 0.2965) | | |
| 3 November | barrier, own job of 1,000 shots (archived) | 0.502 | | |

**Comparisons** (90% CI is Δ ± 1.645 SE; "within" means the whole CI lies inside ±0.05; "clear" means |Δ| ≥ 0.10 at |z| ≥ 3):

| contrast | Δ | 90% CI | z | class |
|---|---|---|---|---|
| A − CB (primary: alone vs shared, barrier) | −0.013 | −0.047 to +0.021 | −0.63 | within ±0.05 |
| B − CN (in-evening replicate: alone vs shared, no barrier) | −0.018 | −0.052 to +0.016 | −0.87 | not within, not clear |
| A − B (barrier effect, alone) | +0.009 | −0.025 to +0.043 | +0.44 | within ±0.05 |
| CB − CN (barrier effect, shared) | +0.004 | −0.030 to +0.038 | +0.19 | within ±0.05 |
| CB − P3-15 pooled barrier PUB (control) | +0.023 | | | within the ±0.05 band |
| 3 November − A | +0.196 | | | |

- **Execution spans.** C: one span, 05:17:11.9–05:17:17.2, holding both PUBs (as in both P3-15 runs). B: 05:18:04.8–05:18:07.0. A: 05:18:29.2–05:18:33.8. So A ran about 72 seconds after C's span, in the seeded order C, B, A.
- **Leave-one-out** (P10, as pre-registered): one circuit, one morning. The second lone job, B, gives the same answer as A: alone was not higher than shared.

**Per-qubit P(1)** (secondary; clbit order, physical qubit in brackets):

| arm | 0 (117) | 1 (125) | 2 (124) | 3 (123) | 4 (144) | 5 (136) | 6 (143) | 7 (141) | 8 (142) |
|---|---|---|---|---|---|---|---|---|---|
| prediction (ALAP) | 0.59 | 0.65 | 0.70 | 0.83 | 0.63 | 0.62 | 0.67 | 0.47 | 0.61 |
| A | 0.61 | 0.67 | 0.68 | 0.74 | 0.58 | 0.60 | 0.67 | 0.47 | 0.63 |
| B | 0.62 | 0.70 | 0.69 | 0.71 | 0.56 | 0.59 | 0.64 | 0.48 | 0.63 |
| CB | 0.62 | 0.68 | 0.66 | 0.75 | 0.58 | 0.58 | 0.64 | 0.47 | 0.60 |
| CN | 0.63 | 0.64 | 0.64 | 0.76 | 0.59 | 0.59 | 0.66 | 0.47 | 0.60 |

**Calibration** (IBM's properties, re-read before each job with `refresh=True`, D35): identical at all three submissions. The document's `last_update_date` was 2026-11-05 04:47, but the per-qubit T1/T2 values were still dated 2026-11-04 12:04 (qubit 143: 03:21), readout errors 2026-11-04 14:15, and CZ errors 2026-11-04 13:08. Reported readout error on these qubits was 0.003–0.031 (largest qubit 125). So, as in P3-15, the prediction used IBM's measurements from the previous day.

**Noticed after the data; leads, not findings:**
- Every arm again sits above the prediction: 0.297–0.319 against 0.2717 (ALAP). That is the same direction as all eight P3-15 arms (0.274–0.319 against 0.2685). The prediction's inputs were again IBM's 4 November measurements.
- Qubit 123 read 0.71–0.76 in all four arms, against 0.83 predicted. In P3-15 it read 0.59–0.60 (run 1, blocks), 0.74–0.75 (run 1, pieces) and 0.79–0.82 (run 2).

**Pre-mortem** ("3 November's 0.50 was a passing state of the chip, so the lone barrier job reads about 0.30, like every arm on 4 November"; kind `world`). For the auditor: the lone barrier job read 0.306.

Data: `data/p3-16-jobA-raw.json`, `data/p3-16-jobB-raw.json`, `data/p3-16-jobC-raw.json` (counts, per-shot bitstrings, execution spans, calibration at each submission), `data/p3-16-predictions.json`, `results/p3-16-lone-job.json`. Code: `experiments/p3_16_lone.py --analyse`.
