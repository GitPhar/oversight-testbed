# P3-18 result: in a fresh chip job on 5 November, both error terms came back on 2 of the 3 entangled pairs (pass, unreplicated)

Pre-registration: `experiments/p3-18-fresh-job.md` (commit `036a70d`, 06:31; seed `4535457`, CURBy-RNG 1592276). Design review `ledger/design-reviews/ng-p3-18.md`: fix-first (5, `0ebf95b`), fixes D44 (`bb37564`) and D45 (`4f0bc54`), confirmed 07:49 (`6a72fea`). Budget ruling br-006 (24 QPU s, under st-16, `01e8ebe`). Prepared snapshot and circuits committed before submission (`6fe09e1`). Job `dbm9gcm74qds73drshgg` on ibm_fez, run 07:52:35–07:53:01 America/Denver, **20.0 QPU s** billed (estimate 20.48; cap 24); raw counts committed at once (`465262a`). Analysis `experiments/p3_18_fresh.py --analyse`, $0. Audited: `ledger/audits/ng-p3-18.md` (4f07a2f; stands; pl-032 clean; three cuts applied in D47).

The chip is a referee here, never a computational resource: its counts decide a pre-registered bet about the chip, and nothing here uses them as an estimate of anything else.

## In plain English

*These are the sentences pre-registered in §5 (as amended by D44–D45), applied as the rule says.*

On pair h221, the fresh job's counts need a blur-type term but not a rotation-type term.

On pair h088, the fresh job's counts need both a rotation-type and a blur-type term beyond the simulator's state, as on 3 November. These are terms in a 16-knob model, not identified mechanisms. The rotation-type term rests mostly on settings YZ and ZX. Even both terms together leave a misfit the model cannot explain (deviance 34.2 on 11 df), so part of what each term absorbs may be neither kind. Scaled by the misfit (x3.1), the LRs are 80.7 (rotation) and 27.0 (blur) against the nulls' 99th percentiles of 17.7 and 8.4 (rotation above; blur above).

On pair h268, the fresh job's counts need both a rotation-type and a blur-type term beyond the simulator's state, as on 3 November. These are terms in a 16-knob model, not identified mechanisms.

Overall: both terms came back on 2 of 3 pairs in a fresh job on 5 November, so P3-5c's 'both terms' reading held on a second job, not only on 3 November's afternoon. Two jobs on one chip are still not a description of the chip in general. The pass rests on h088 and h268; either one's label flipping would make it a fail.

Under the reference prepared before submission (IBM's calibration read at preparation; nulls at B = 100 only), the labels are h221: blur only; h088: both; h268: both. Reported, not scored.

*What this does and does not say.* The bet passes by its rule (both terms on at least 2 of 3 pairs). Six primary tests were run (3 pairs × 2 terms). All five present labels have p = 0.001, below the Bonferroni line of 0.0017, so the labels and the verdict are the same with that correction. It is not a clean repeat of 3 November: there, all three pairs needed both terms; here, h221's rotation-type term, P3-5c's weakest label (LR 38.5 then), was not detected (LR 11.6, p = 0.069). The pre-run worlds put the chance of missing it at 2,000 shots, if 3 November's terms were the truth, at about 2 in 6 draws (`data/p3-18-worlds.json`), so this miss is not out of line with half the shots; it is also consistent with a smaller rotation on that pair today. The fresh job differs from 3 November's in a bundle (another day and time, IBM's newer calibration, half the tomography shots and a quarter of the calibration shots, possibly server-side handling), so nothing here says which of those matters. IBM's `last_update_date` moved between preparation (07:13:02) and the run (07:47:01), but every property the reference uses (T1, T2, readout, sx and CZ error for the job's 14 qubits and 12 CZ pairs) was identical in the prepared, submission-time and run-time reads. The two reference states are therefore the same (agreeing to 1e-15), and the secondary table repeats the analysis with fresh bootstrap draws. It is not a check against a different calibration.

**Novelty:** known. Coherent and stochastic error together on superconducting processors are in print: Hashim et al. 2021 (PRX 11, 041039; arXiv 2010.00215, read in full) measured coherent error as 2.0 to 2.9 × 10⁻² of 3.3 to 4.4 × 10⁻² CNOT infidelity on four AQT@LBNL transmons, with the tune-up drifting between experiments, Carignan-Dugas et al. 2024 (Quantum 8, 1367; arXiv 2303.09945) a Z/ZZ-only coherent part beside a larger decoherent part on three IBM chips, and Seif et al. 2024 (ISCA; arXiv 2403.06852) correlated coherent ZZ on IBM ECR devices. ng-p3-18's fresh-job reading (both terms beyond the IBM-calibrated simulator's state on 2 of 3 ibm_fez pairs, blur alone on the third) is the same statement in the same direction on a Heron r2 device, and a replication of our own ng-p3-5c, not a finding about chips; no paper found fits nested rotation and blur terms to Heron tomography across two jobs, which is a method, not a result. Search: WebSearch "Heron processor residual ZZ crosstalk coherent error Pauli twirling ibm_fez OR ibm_torino OR ibm_kingston", "readout error miscalibration mistaken for decoherence two-qubit state tomography superconducting", "Pauli twirling Bell state tomography IBM coherent error twirled versus untwirled" (2026-11-05), arXiv HTML for each lead; claude-opus-5-5, fresh reader subagent of the 2026-11-05c remap. *(Rule 13; written by a fresh claude-opus-5-5 reader subagent of the 2026-11-05c remap session, which ran none of these bets; its searches and reads are in programs/nature-graded/map/reads/remap-2026-11-05c-ng-p3-18.md.)*

## Tables

**Primary tests** (P3-5c's 16-knob model, unchanged; LR = 2 × log-likelihood gain; parametric bootstrap at 2,000 shots per setting, B = 100, extended to 1,000 if p ≤ 0.05; "present" iff p < 0.01):

| pair (qubits) | rotation given blur: LR | null 99th pct | p (B) | blur given rotation: LR | null 99th pct | p (B) | labels | 3 November (P3-5c): LR rot / blur |
|---|---|---|---|---|---|---|---|---|
| h221 (10, 9) | 11.6 | 18.5 | 0.069 (100) | 54.5 | 9.2 | 0.001 (1000) | blur only | 38.5 / 128.8 |
| h088 (44, 37) | 250.8 | 17.7 | 0.001 (1000) | 84.0 | 8.4 | 0.001 (1000) | both present | 183.6 / 242.3 |
| h268 (4, 16) | 271.5 | 17.8 | 0.001 (1000) | 38.5 | 9.4 | 0.001 (1000) | both present | 237.6 / 72.0 |

The largest null LRs drawn were, for rotation and blur: h221 21.6 and 14.0, h088 28.1 and 14.2, h268 22.8 and 13.7. Every present LR exceeds its null's maximum (by 2.8 to 11.9 times), and h221's rotation LR (11.6) does not.

**Fit diagnostics** (secondary):

| pair | full16 deviance (11 df; q99 24.7) | overdispersion | scaled LR rot / blur | top setting share, rotation | top setting share, blur | negativity: ref / coh / inc9 / full16 |
|---|---|---|---|---|---|---|
| h221 | 18.5 | 1.68 | 6.9 / 32.4 | 0.22 (ZY) | 0.26 (YX) | 0.178 / 0.165 / 0.135 / 0.141 |
| h088 | **34.2 (misfit)** | 3.11 | 80.7 / 27.0 | 0.44 (YZ) | 0.28 (ZX) | 0.105 / 0.128 / 0.015 / 0.084 |
| h268 | 22.2 | 2.02 | 134.3 / 19.1 | 0.25 (ZZ) | 0.37 (XX) | 0.106 / 0.107 / 0.015 / 0.073 |

**Secondary: the reference prepared before submission** (nulls at B = 100 only, floor 0.0099):

| pair | LR rot | p | LR blur | p | labels |
|---|---|---|---|---|---|
| h221 | 11.6 | 0.089 | 54.5 | 0.0099 | blur only |
| h088 | 250.8 | 0.0099 | 84.0 | 0.0099 | both |
| h268 | 271.4 | 0.0099 | 38.5 | 0.0099 | both |

**Scoring and baselines.** Outcome 1 (pass). Engine odds 0.60 (map 0.60, v1 0.72); Sean's 0.55 (`ho-20261105-061152-7q5`). Dumb baselines pre-registered in §4: carry-over 0.95, running base rate 0.35. The map's engine-only sub-bet "all three pairs both" (0.40) did not come true.

**Pre-mortem** ("halved shots push h221's weak rotation term and one other pair's term below their nulls' 99th percentiles"; kind `design`). For the auditor: the bet did not fail; h221's rotation term did fall below its null, the other two pairs did not.

Data: `data/p3-18-raw.json` (counts, usage, calibration at submission and at run time), `data/p3-18-prepared.json` (prepared snapshot and reference states), `results/p3-18-fresh-job.json` (fits, all bootstrap nulls, labels, sentences). Code: `experiments/p3_18_fresh.py --analyse`.
