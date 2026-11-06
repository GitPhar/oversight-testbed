# P3-17 result: untestable by its own re-run rule (D48); the re-run's numbers say the blur-type term is still needed on all three pairs, reported and not scored

Pre-registration: `experiments/p3-17-bounded-readout.md` (commit `db13dc7`, 06:28; seed `323018a`, CURBy-RNG 1592273, seed32 1052259867). Design review `ledger/design-reviews/ng-p3-17.md`: fix-first (4, `dd1205c`), fixes D43 (`514e634`), pre-run worlds re-run (`a1b2687`), confirmed (`a4e7135`). Runs: the first `--run` crashed in a bookkeeping line before writing anything (D46, `ee30b52`); the second was stopped from outside after two of three pairs, last written 09:41, no traceback (partial file and log committed as they stand, `2452d3e`, D48); the third, from the same seed, ran 16:12:56–17:49:29 America/Denver (`0fd969c`). Audited: `ledger/audits/ng-p3-17.md` (dfc26bf; stands, untestable; pl-049 planted and caught; cuts 2-5 applied verbatim, D49; cut 1 was the plant). Archive only: **$0, 0 QPU s**, no model, no network. The chip is a referee here, never a computational resource: its archived 3 November counts decide a pre-registered bet about the chip.

## In plain English

**The verdict is untestable, and the bet is not scored.** This is because of how the run was finished, not because of what the data said. The second run stopped after two of the three qubit pairs. Before running it again, D48 (committed before the re-run) set a condition: the re-run had to reproduce the first two pairs' numbers exactly; if it did not, it would count as a different run, and the third pair (h268) would be untestable. Pair h221 came back identical to the last digit. Pair h088 did not: its fitted log-likelihoods moved by up to 0.00014. Both null generators are fitted to the observed counts and the null fits start from the observed optima, so all 2,000 of its null draws changed (by up to 7.2 in LR) and its null's 99th percentile moved from 14.57 to 14.37. Its label, p-value and number of draws were unchanged. The code, the seed and every analysis input were byte-identical. The audit found the cause: the code rebuilds each pair's reference state with the Aer density-matrix simulator on every run. That state differs between calls by up to 3e-16 on h088 and h268, and not at all on h221, and the fits carry the difference into the fourth decimal of logL. So D48's exact check could not be relied on to pass on h088, and h268's numbers were not fixed by the seed, as D48 assumed (`ledger/audits/ng-p3-17.md`). Loosening "exactly" after seeing the result would be changing a committed bar after the data (rule 6), so the bet is untestable by D48, with the sentence `verdict()` gives for that case:

The refit could not be completed on h268, so this test cannot say whether per-qubit readout error of the modelled kind (each qubit separately, fixed over the job) within three times the calibration value can stand in for the blur-type term.

*What the re-run found (reported, not scored).* The question was whether the "blur-type" error term P3-5c needed on 3 November's archived chip data could instead be extra misreading: each qubit allowed to misread anywhere from not at all up to three times as often as that job's own calibration measured. In the re-run, the answer on all three pairs was no. Misreading of that kind and size could not stand in for the blur term (p = 0.001 at 1,000 draws on every pair, against two null generators each). These are the sentences `verdict()` printed for the re-run, verbatim:

On pair h221, the blur-type term is still needed even when per-qubit readout error of the modelled kind (each qubit separately, fixed over the job) may be up to three times its calibration value in that job: readout knobs of this kind, that large, cannot stand in for it.

On pair h088, the blur-type term is still needed even when per-qubit readout error of the modelled kind (each qubit separately, fixed over the job) may be up to three times its calibration value in that job: readout knobs of this kind, that large, cannot stand in for it. Its full model misfits these counts (deviance 59.6 on 7 df); scaled for that misfit, the blur-type term's gain is within its null, so on this pair the label rests on a null the counts reject.

On pair h268, the blur-type term is still needed even when per-qubit readout error of the modelled kind (each qubit separately, fixed over the job) may be up to three times its calibration value in that job: readout knobs of this kind, that large, cannot stand in for it.

Overall: on all three archived pairs (one job, 3 November), P3-5c's blur-type term is still needed when per-qubit readout error of the modelled kind (each qubit separately, fixed over the job) may be up to three times the job's own calibration value. These are terms in a fitted model, not identified physical mechanisms; larger readout drift, and readout errors of other kinds (correlated between qubits, or drifting during the job), are not excluded.

*What this does and does not say.* Had D48's check held, this would have been a **pass, unreplicated** (one job, one archive). The h088 difference is far too small to change any label: in the re-run, every LR is at least 2.3 times its null's 99th percentile (h268 the closest) and above the largest null draw, and the stalled run gives h088 the same label, p and B. But the rule was written to make "it can't have been re-rolled" checkable, and the check failed. h221 and h088 had been seen (both "still needed") before the re-run, so only h268 could have decided pass or fail. h268's LR (34.5 against 14.5) is the weakest of the three, as P3-5c's was. On h088 the full model misfits the counts, and once scaled for that misfit, the blur term's gain (13.0) falls within its null (14.4). So h088's label rests on a null the counts reject, as round 3's audit of P3-5c found. The no-blur model, given the chance, pushes nearly every readout knob to its upper bound (3× calibration). The full model with blur puts most of them at the lower bound (no readout error at all). Under the auditor's wide bounds (readout error up to 5%), the point LR falls below the primary null's 99th percentile on h221 (9.5) and h268 (7.7), as round 2's audit found. That is a point fit against the primary null, not a test, and those knob limits are 1.2 to 12.5 times this bet's upper knob bounds. Three primary tests were run, one per pair. All three p = 0.001 are below the Bonferroni line of 0.0033.

**Novelty:** partly new. In SPAM tomography a "blame gauge" trades loss of state purity for detector noise with no change in the counts (Lin et al. 2021, arXiv:1910.07511; Jayakumar et al. 2024, arXiv:2308.15648), and standard state tomography fixes it only by assuming the measurement is known (Jackson & van Enk 2015, arXiv:1508.05633); on a transmon, Aasen et al. (2024, arXiv:2312.04211) report that mitigated tomography does less well when T1/T2 are effectively shortened, and suggest that state-dependent errors are the cause. No paper found tests whether per-qubit readout error bounded at 3× in-job calibration can stand in for an incoherent term. This bet's re-run, which is untestable by D48 and not scored, says no on the three pairs of one 3 November ibm_fez job; with the wide bounds (knob up to +0.05) its point LR falls within the null on two (h221, h268), as the gauge implies. Search: WebSearch plus arXiv abstract/API and HTML full-text pages, 2026-11-05, terms "gate set tomography gauge freedom SPAM", "blame gauge state preparation measurement", "simultaneous tomography quantum states SPAM noise", "readout error mitigated state tomography T1 T2", "assignment matrix conflates state preparation readout error IBM", "noise model selection likelihood ratio IBM tomography", "ibm_fez Heron two-qubit tomography readout dephasing". Written by a fresh session (claude-opus-5-5) that did not run the bet; it classifies the re-run's unscored reading.

## Tables

**Primary test, the re-run** (LR_b = 2 × (logL full16R − logL cohR); parametric bootstrap from two generators, the fitted cohR and cohR with all four knobs at the upper bound, each B = 100 extended to 1,000 at p ≤ 0.05; p = the larger; "still needed" iff p < 0.01):

| pair (qubits) | calibration misread rates r (e0 R, e1 R, e0 L, e1 L) | LR_b | null 99th pct (fitted / corner) | null max (fitted / corner) | p (B) | label | P3-5c LR (no readout knobs) |
|---|---|---|---|---|---|---|---|
| h221 (10, 9) | 0.0025, 0.0121, 0.0034, 0.0055 | 59.7 | 13.5 / 13.7 | 23.6 / 20.4 | 0.001 (1000) | still needed | 128.8 |
| h088 (44, 37) | 0.0093, 0.0124, 0.0030, 0.0096 | 111.0 | 13.8 / 14.4 | 24.9 / 24.0 | 0.001 (1000) | still needed | 242.3 |
| h268 (4, 16) | 0.0020, 0.0108, 0.0036, 0.0206 | 34.5 | 11.4 / 14.5 | 19.7 / 22.8 | 0.001 (1000) | still needed | 72.0 |

**D48's check: the stalled run against the re-run** (same code, seed and inputs):

| pair | logL cohR (stalled / re-run) | logL full16R (stalled / re-run) | LR_b | corner null 99th pct | p (B) | same? |
|---|---|---|---|---|---|---|
| h221 | −39203.232449 / −39203.232449 | −39173.390488 / −39173.390488 | 59.68 / 59.68 | 13.72 / 13.72 | 0.001 (1000) both | identical (every field) |
| h088 | −46356.981269 / −46356.981303 | −46301.483907 / −46301.484046 | 110.99 / 110.99 | 14.57 / 14.37 | 0.001 (1000) both | no |
| h268 | not reached / −43283.224870 | not reached / −43265.994844 | — / 34.46 | — / 14.48 | — / 0.001 (1000) | — |

**Secondaries** (reported, never tests):

| pair | rotation given blur and readout, point LR | full16R deviance (7 df; q99 18.5) | LR_b scaled by overdispersion | top setting (share) | point LR_b, knob ±3r / 3 SE / wide [−0.02, 0.05] |
|---|---|---|---|---|---|
| h221 | 24.7 | 11.3 | 36.9 | YZ (0.25) | 40.5 / 109.0 / 9.5 |
| h088 | 169.0 | **59.6 (misfit)** | 13.0 | XX (0.45) | 76.8 / 216.2 / 38.9 |
| h268 | 171.3 | 14.6 | 16.5 | YX (0.31) | 21.8 / 62.0 / 7.7 |

Knobs at a bound (e0 R, e1 R, e0 L, e1 L; ✓ = at a bound): h221 cohR ✓✓✓✓ (all upper), full16R ✓·✓✓; h088 cohR ✓✓✓✓ (all upper), full16R ·✓✓✓ (lower); h268 cohR ✓✓✓·, full16R ✓·✓✓ (lower).

**Scoring and baselines.** Untestable by D48, so not scored, like ng-p3-2 and ng-p3-3. Engine odds 0.55 (map 0.70, v1 0.72, after lesson 0.60, revised before data by D43); Sean's 0.30 (`ho-20261105-061152-9fe`). Both stay on the row. The dumb baselines pre-registered in §4 were carry-over 0.95 and the running base rate 0.35. Had the bet been scored, it would have been secondary to ng-p3-5 under rule 15: same 3 November tomography counts, no new data of its own.

**Pre-mortem** ("on h221 or h268 the knobs hit their upper bounds and absorb enough blur to push LR below its null's 99th percentile"; kind `world`). For the auditor: the bet did not fail by its rule; it is untestable for an execution reason (D48). In the re-run, the no-blur model's knobs did sit at their upper bounds on h221 (all four) and h268 (three of four), but the LRs stayed above both nulls.

Data: `results/p3-17-bounded-readout.json` (the re-run: fits, every null draw, labels, `verdict()` and sentences), `results/p3-17-bounded-readout.run2-partial.json` (the stalled run, h221 and h088 only), `results/p3-17-run2-partial.log`, `results/p3-17-run3.log`. Code: `experiments/p3_17_bounded.py --run`. Checked by `programs/nature-graded/reproduce.py`.
