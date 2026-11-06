---
bet: ng-p3-9
program: nature-graded
prereg_commit: 96cccf4
results_commit: 6fbb48b          # clone head; the result itself is d59573d, the Novelty line 6fbb48b
auditor_session: fresh auditor subagent, session b30ff553-38c2-441e-aced-1318a18e362d, audit clone /Users/seanpharris/oversight-testbed-audit-ng-p3-9
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true          # same model as the author, the design reviewer and the Novelty session
date: 2026-11-05 18:39 America/Denver
claims_checked: 24
holes_found: 4
overclaims_cut: 5
reproduced: true
verdict_claimed: fail            # "fail" is the bet's pre-registered outcome-0 verdict (§5.2); the template's enum has no "fail"
verdict_after_audit: fail
verdict_stands: true
canary: unknown
false_alarms: 0
design_review_missed: []
novelty_checked: partly new
novelty_holds: true
novelty_search: WebSearch, 2026-11-05: "sequential mid-circuit measurements superconducting qubits contextuality signaling disturbance "Peres-Mermin" OR "magic square" disturbance-corrected noncontextuality inequality experiment"; opened arXiv:2604.24735 (Dutra, Baldijão & Terra Cunha 2026, theory) and arXiv:2105.00940 (La Cour 2021, theory). Neither applies CbD to hardware PM data.
failed: true
failure_reason: In the Bell-state, reverse-order system, the chip's later sequential measurements carried large order-dependent biases (Δ0 0.70; R3 reverse X1Z2 +0.42 and Z1X2 −0.39 where 0 is expected), so the CbD LP fitted a noncontextual model. Kind design.
failure_kind: design
premortem_score: named
risk_seen: null
---

# Audit of ng-p3-9: does program 1's contextuality check see contextuality on the chip, where physics says it must be? (sequential Peres–Mermin under the exact CbD 2.0 LP)

## In plain English

The verdict stands. It is **fail**: the exact CbD linear program rejected noncontextuality in three of the four state-and-order systems but not in the fourth (the Bell state measured in reverse order). I re-derived every primary number from the archived counts:
- the point CNT2 of all four systems;
- the full 1,000-draw bootstrap from the beacon seed, which matches to the last digit;
- a second bootstrap from my own seed, with the same four labels;
- the other encoding;
- the leave-one-out table;
- an independent noncontextuality LP over all 2¹⁸ joint values, written without the code's reduction.

They all agree. `reproduce.py` reproduces every table under both numpy versions.

Four statements in the write-up are wrong and must be fixed:
- **The line products.** It says every line's product was 0.65–0.74 on the chip. That holds for only three of the six lines; the others are 0.76–0.92.
- **The calibration date.** It says IBM's calibration date was the same at submission and at run time. It was not: 17:35:25 at submission, 17:57:35 at run time. The values were the same.
- **The citation correction (D51) is wrong.** The Eur. J. Phys. article lists Laghaout first; only the arXiv preprint lists Dikme first.
- **The Kelleher & Holweck comparison.** Their 5.31 comes from a square of three-qubit operators, not the two-qubit square measured here.

None of these moves the verdict. What would break it: re-running the Bell-reverse system, or only line R3 in reverse, in a second job, where a coherent error on data qubit 5 after the Y1Y2 block should show up again if it is a property of the device.

## The case that this result is false

*Written before the checklist.*

The headline is a fail that rests on one system out of four and, inside it, on one line: replacing R3's reverse-order counts with the simulator's prediction makes Bell-reverse contextual (CNT2 0.106). So "the check failed to see contextuality" is really "one circuit of 24, one 4,000-shot sample, carried a large bias". Three ways the claim could be false:

1. **A software artefact.** The bias in that circuit may be a bug rather than the chip. The PUB order is a seeded permutation that must be inverted. Reverse-order bits must be re-indexed to the line's order. One misplaced circuit, or a swapped classical bit, could manufacture exactly the kind of context-dependent mean (+0.42 on an observable whose quantum mean is 0) that CbD reads as disturbance and absorbs.
2. **A boundary artefact.** CNT2 = 0 depends on a tolerance (1e-6) and on HiGHS returning an exact 0. If the Bell-reverse system sat just inside the noncontextual polytope, the 1,000 draws at zero could be a solver artefact, and an encoding or seed change could flip it.
3. **An unreliable instrument.** CbD's correction is the thing being tested. If the LP is wrong, a pass or a fail means nothing. Maybe the threshold-string reduction, or the multimaximal coupling as coded, admits noncontextual models it should not.

The "absorbed, not below" framing ("the raw sum still beat 4") also depends on the χ bootstrap, which is computed at shot level inside one job. Calibration drift between jobs is not in the interval, so "the chip's measurement quality" is a statement about one 33-second window.

Finally, the plain-English story attributes the miss to "the chip's measurement quality, not the check". The design cannot separate a coherent gate-calibration error from measurement disturbance, so this may claim more mechanism than the data allow.

## Claims checked

| # | claim (quoted or paraphrased) | check run | outcome |
|---|---|---|---|
| 1 | Verdict fail; 3 of 4 systems contextual, Bell-reverse absorbed | full bootstrap rerun (beacon seed, numpy 2.5.4); own seed 20261105 | holds (identical; own seed same labels) |
| 2 | CNT2 points 0.0663 / 0.0572 / 0.1031 / 0.0000 | `cbd_lp.cnt2` reference build on the archived counts | holds (exact) |
| 3 | CNT2 99% lower bounds 0.0460 / 0.0375 / 0.0834 / 0.0000; medians; draws at 0 (0, 0, 0, 1000) | bootstrap rerun | holds (exact) |
| 4 | Bell-reverse is noncontextual under CbD | independent full 2¹⁸ LP (8-cell bunches, maximal pair couplings) | holds (residual 0; the other three are infeasible, residuals 0.53 / 0.46 / 0.83) |
| 5 | The pass decision does not depend on the encoding | CNT2 with 1 = eigenvalue +1 | holds (identical values) |
| 6 | χ 4.688 / 4.623 / 4.345 / 4.399 with SE; χ 99% lower 4.634 / 4.569 / 4.286 / 4.334 | reproduce.py; bootstrap | holds |
| 7 | Δ0, Massé CNTX columns | reproduce.py | holds |
| 8 | Counts put back in canonical order | qpy names = labels; raw order = `job_order(seed_order)`; ISA circuits ideal-simulated give χ 6.000 | holds |
| 9 | "The fail rests on one line": R3 → 0.106; others stay 0; no single replacement zeroes the other systems | LOO recomputed | holds |
| 10 | R3 reverse means +0.422, −0.394 (Bell); −0.27 (\|00⟩); simulator +0.005, −0.005 | recomputed | holds |
| 11 | R3/C3 means table | reproduce.py and own recomputation | holds |
| 12 | "Each line's product had magnitude 0.65–0.74 against the simulator's 0.95–0.96." | all 24 products | **hole**: chip 0.648–0.923, simulator 0.946–0.970 |
| 13 | χ 4.35–4.69 against predicted 5.72–5.79 | table / prepared.json | holds |
| 14 | Calibration identical at submission and run, "`last_update_date` 17:35:25 both times" | `data/p3-9-raw.json` | **hole**: values identical, but last_update_date is 17:57:35 at run |
| 15 | T1/T2, readout and CZ values at submission/run; different from the 10:09 preparation read | raw and prepared | holds |
| 16 | Job id, created 17:55:43, ran 18:08:19–18:08:52, 28.0 QPU s, cap 45 | raw `usage` and `timestamps` | holds |
| 17 | Cumulative 117 s = 46 program 1 + 71 program 3 (8, 8, 7, 20, 28) | `ibm-usage.json` summed | holds |
| 18 | Sean's card event holds (both states, at least one order); by CbD 2.0 Theorem 3 the folded system is contextual | lower bounds; arXiv:1604.04799v4 PDF, Theorem 3 | holds |
| 19 | Lower bounds "0.04–0.08" in the three contextual systems | table | holds |
| 20 | D51: the EJP article's first author is Dikme | Crossref, DOI 10.1088/1361-6404/ac79e0 | **hole**: journal lists Laghaout first; Dikme is first only on the arXiv preprint |
| 21 | Kelleher & Holweck 5.31 "best of several embedded squares" | arXiv HTML 2505.21243, Table 1 | **hole** (omission): the squares are labelled with 3-qubit operators in W(5,2), not the 2-qubit PM square |
| 22 | Novelty line citations (KDL 2015, Massé 2021, Kirchmair 2009, Gühne 2010, Kumar 2025, Hothem 2024) | papers opened | holds, with small imprecisions (F27) |
| 23 | Pre-registered sentences printed verbatim | reproduce.py (6 sentences found) | holds |
| 24 | "The failure is the chip's measurement quality, not the check and not physics" | C15 reading against the design | holds, narrowly (see C15) |

## Checklist

**A. Pre-registration**

- **A1 holds.** Author times:
  - Prereg 96cccf4 at 16:20:14.
  - Seed 8c56681 at 16:21:42.
  - Design review aee8d85 at 17:29; fixes 102f7e8 and d9fbab1; confirmed b20ea79 at 17:53:45.
  - Budget ruling a939980 at 17:55:13.
  - Job created at 17:55:43 (raw `timestamps.created` 00:55:43Z); ran 18:08:19–18:08:52.
  - Raw counts 5c55784 at 18:09:10. Analysis run at head 5c55784 (`analysed_at_head`). Result d59573d at 18:14:58.

  The free IBM property reads, circuits and simulator prediction (b1a06a5, 10:13) predate the prereg. They are reads of calibration, not outcome data.
- **A2 holds.** The rule, statistic, units, seed purposes, B = 1,000, rank-10 lower bound, TOL 1e-6 and the labels are unchanged from 96cccf4 to the run.
  - The prereg file changed after 96cccf4 only at 8c56681 (seed fill-in), 102f7e8 (D49) and d9fbab1 (D50). Both D rows are dated before the data, and each change concerns budget wording, the untestable path, the Γ wording or prior-work wording.
  - `p3_9_pm.py` was not touched after d9fbab1. `classify`, `lower`, `bootstrap` and `verdict`'s fail branch are unchanged (diff read).
  - The budget is unchanged: 45 s approved (br-025), 28.0 s billed.
- **A3 holds.** No bar moved. D49, D50 and D51 change no number, rule or bar. D51 comes after the data but is a citation note.
- **A4 holds.** CNT2's lower bound is the primary and decides the verdict. χ, Δ0, CNTX and LOO are reported as secondaries.

**B. Is the number real?**

- **B5 holds.** No ties. The boundary is CNT2 ≤ 1e-6. Bell-reverse is 0 in 1,000 of 1,000 draws (and in 1,000 of 1,000 with my seed). An independent LP finds that point exactly feasible (residual 0.0). The three contextual systems sit 0.036–0.083 above the boundary at their 10th-smallest draw.
- **B6 holds.** Unpooled by state and order, as registered. The registered encoding robustness check gives identical CNT2 under 1 = +1.
- **B7 holds as disclosed.** The fail rests on line R3 in Bell-reverse, and the results file says so in numbers (LOO table recomputed exactly). Inside R3 reverse, the bias appears only after the Y1Y2 block:
  - The same observables measured first or elsewhere are near 0: X1Z2 0.010 in R3 forward and 0.011 in C2 reverse; Z1X2 0.017 in C1 reverse (Bell).
  - So the bias is carried into later measurements and is not a fault of the X1Z2 or Z1X2 blocks themselves.
  - It points at one coherent effect, consistent with a rotation of data qubit 5 after the Y1Y2 block (the signs +0.42 and −0.39 fit a Y-axis rotation on qubit 2 of about 25°). The design cannot confirm that, and the write-up does not claim it.
- **B8 holds.** The threshold strings come from the same 1-marginals the LP fixes, which is the definition. Nothing fitted is tested with itself. The LOO replacement uses the committed pre-data simulator prediction.
- **B9 holds.** The χ-only baseline (passed by the χ = 6 noncontextual cheat) and the cheat world are registered. A dumber method (χ > 4) would have said "contextual" in all four systems, so the CbD correction is what made the difference here.
- **B10 holds.** The bootstrap resamples each circuit's shots, at the level the rule names. The interval does not include job-to-job or calibration drift; the write-up's "one job, one evening" limit covers that.
- **B11 holds.** The rule is a conjunction of four tests, uncorrected, which the prereg states and justifies. Nothing else is promoted.
- **B12 holds.** No fitting step sees the outcome. The prediction was committed at b1a06a5.

**C. Does the write-up say only what the data say?**

- **C13 holds.** "One chip, one qubit triple, one job, one evening". No "every" or "superconducting hardware".
- **C14 holds.** Sean's card event and the Kelleher comparison are labelled secondary.
- **C15 holds, narrowly.**
  - "The failure is the chip's measurement quality, not the check and not physics" is supported in two parts:
    - The check behaves as specified: my independent LP agrees, and so do `--check`'s cheat and KDL tests.
    - The inconsistent connectedness comes from the measurement sequence, since the biases appear only in later positions.
  - The limits paragraph and the "in shape, not shown in cause" bullet correctly refuse to name a physical cause. "Measurement quality" must be read as the whole sequential measurement block, gates included, not readout alone. No cut is required.
- **C16 holes (two).** Comparing the plain-English and bullet text with the table and the archive:
  - **(i) The line products.** "Each line's product had magnitude 0.65–0.74 against the simulator's 0.95–0.96" is false.
    - Chip products range over 0.648–0.923: 0.65–0.73 on R2, R3 and C3, and 0.76–0.92 on R1, C1 and C2.
    - Simulator products range over 0.946–0.970.
    - The sentence contradicts the table's own χ: six products of at most 0.74 give χ ≤ 4.44, yet |00⟩-forward has χ 4.688.
  - **(ii) The calibration date.** "IBM's `last_update_date` 17:35:25 both times" is false. `calibration_at_run.last_update_date` is "2026-11-05 17:57:35-07:00"; every listed property value is identical.
- **C17 holes (two), with smaller imprecisions noted.**
  - **Hole: Dikme as first author.** The D51 correction is itself an error. Crossref for Eur. J. Phys. 43:055401 (DOI 10.1088/1361-6404/ac79e0) gives "Laghaout, Dikme, Reichel, Björk", title "A demonstration of contextuality using quantum computers". Dikme is first only on arXiv:2009.10751, titled "Measuring the Mermin-Peres magic square using an online quantum computer". The prereg's "Laghaout et al. 2022, Eur. J. Phys." was right. The results file's correction paragraph and its Novelty line ("Dikme et al. 2022, Eur. J. Phys. 43:055401") are wrong.
  - **Hole: the Kelleher & Holweck square.** Their 5.3076 on ibm_kingston is for the best of the "3360 square configurations, each labelled with 3-qubit operators" in W(5,2) (arXiv HTML, Table 1, 10,000 shots, no error bars). It is not the two-qubit Peres–Mermin square measured here. "Best of several embedded squares" omits this, and the comparison is looser than stated.
  - **Holds: CbD 2.0 Theorem 3.** arXiv:1604.04799v4, PDF line "Theorem 3. In a noncontextual c-c system of binary random variables every subsystem … is noncontextual".
  - **Holds: CNT2 definition.** Kujala & Dzhafarov 2019 define CNT2 at eq. 38, with the LP form at eqs. 39–40.
  - **Not verified: 4.987 in the Dikme/Laghaout paper.** Its tables are images, and I did not find the number in text.
- **C18 holds.** "Verdict: fail" is in the header, the title and the first sentences of the plain English.

**D. Process**

- **D19 holds.** The estimate and the 45 s cap are gated in `submit()` and `run_hardware(expected_s=45)`. 28.0 s was billed (raw `usage`, `job_metrics_usage.qpu_charge_time_seconds` 28), and service usage went 89 → 117.
- **D20 holds.** One job, no client error, no retry, and the marker is present.
- **D21: not applicable.** No graded scale.
- **D22: not applicable.** It is not a hit, so no hit is claimed.

**E. Engine records**

- **E23 holds, except that the randomness string itself was not re-derived.**
  - CURBy-RNG pulse 1592865 is at 2026-11-05T23:21:00.177Z and 1592864 at 23:20:00.205Z. I fetched both from random.colorado.edu's CURBy-RNG chain. The commit is at 23:20:14Z, so 1592865 is the first pulse after it.
  - CURBY-Q's latest round is still 28297 (randomness stage 2025-08-22T19:42:38Z), so it is stalled and the fallback chain is correctly used.
  - `ledger/seed.py` recomputes seed_order 17761473774835708074 and seed_boot 13690150415164649744 from the recorded randomness.
  - The job order equals `job_order(seed_order)`, and the bootstrap reproduced exactly from seed_boot.
  - Nothing was committed between 96cccf4 and 8c56681.
  - I did not re-derive the recorded randomness hex from the pulse payload (the client computes it; `certificate_verified: false` is stated).
- **E24: not applicable.** This is a standard bet, not a tiebreak. Still, the simulator prediction was committed before the chip ran (b1a06a5), and the qpy SHA-256 matches `prepared.json`.
- **E25 holds.**
  - The §0 lesson sentence is identical to `ls-ng-p3-9` in `ledger/inbox/p3-9.jsonl` (eacc118, two minutes after the prereg; the ledger takes it through the inbox).
  - The read block matches `ledger/brier.md` at 73eb5cf: 37 scored, Brier 0.188, 12 hits. The newest audit is ng-p3-18.md (4f07a2f, 3a7f38f).
  - P6's do_this (a wrong set-up the control must reject) is in the design: the cheat world, and 30 flip-noise noncontextual models with CNT2 0.
  - P12's do_this is in the design: committed worlds with P(pass) 0.95–1.00 and P(fail) 1.00, matching `data/p3-9-worlds.json`.
  - The odds change from 0.40 to 0.80 was recorded at 8bf9942, before the prereg.
- **E26 holds.**
  - `ledger/design-reviews/ng-p3-9.md` is fix-first (aee8d85, 17:29), after the prereg and before the first call.
  - Its four fixes are in D49 (17:42) and D50 (17:52), and the confirmation (b20ea79, 17:53:45) comes 2 minutes before the job.
  - I found no flaw D1–D12 should have caught. The D11 worlds modelled disturbance as symmetric flips, which cannot shift a zero mean. The failure came from mean shifts (inconsistent connectedness), but the bet could still both pass and fail, so D11's test was met. A world with order-dependent bias would have priced the fail better: a note for future designs, not a miss.
  - The four citation and calibration slips are write-up errors after the data.

**F. Prior work**

- **F27 holds: the verdict word survives. Holes in two citations of the Novelty line are counted under C17.**
  - The line exists. It was written by a fresh session (claude-opus-5-5) and names its search, and the verdict is "partly new".
  - Papers opened:
    - **KDL 2015** (PRL 115:150401): conservative interval [3.127, 4.062] against n − 2 = 3 for Lapkiewicz's KCBS data; "The system is contextual." Holds.
    - **Massé 2021** (arXiv:2105.13821): only v1, no journal-ref; CNTX 0.566 (eq. 116 in ar5iv, the line does not give an equation number). Holds. The paper does not itself call the formula "adapted"; it applies a cyclic-system result to the non-cyclic square, so "adapted" is a fair reading.
    - **Kirchmair 2009**: 5.46(4) holds. 2.23(5) > 2 is the disturbance-corrected (CHSH-like, 4 of the 9 observables) inequality, from a separate run on another state with σy and σz swapped. "Only on part of the square" holds.
    - **Gühne et al. 2010** (PRA 81:022121): "smaller than 2/48 ≈ 0.0417". Holds.
    - **Kumar et al. 2025** (arXiv:2512.02284): Willow, ancilla with reset, χ = 5.618 ± 0.005, no CbD or signalling analysis. Holds. The paper does not say "raw".
    - **Kelleher & Holweck 2025**: 5.3076, no error bars. Holds, but it is a 3-qubit square (C17 hole).
    - **Dikme/Laghaout**: wrong first author for the journal version (C17 hole). The order dependence ("worse results when the third row … was implemented as …") is in the journal version.
    - **Hothem et al. 2024** (arXiv:2410.16706): observed ε_MCM 7.98 ± 0.18 % (5Q, with DD) to 26.14 ± 0.46 % (15Q, without DD) on ibmq_algiers, "much larger than predicted by IBM's calibration data", "26× larger than predicted" at n = 15. The predicted "0.72–1.0%" appears only in a figure, so I could not check it. The range mixes conditions.
  - My own search (header) found two theory papers:
    - Dutra, Baldijão & Terra Cunha 2026 (arXiv:2604.24735): open-system dynamics suppress the sequential-measurement correlations needed to witness PM contextuality ("classicalization").
    - La Cour 2021 (arXiv:2105.00940): reads apparent PM contextuality as measurement disturbance.
  - Neither applies CbD to hardware data or states our result. The verdict word "partly new" holds. Dutra et al. is relevant theory for the fourth system's direction, and the Novelty line could cite it, but that is not a hole.

## The pre-mortem, scored

**Disclosure.** I read the pre-mortem before writing my own failure reason. It sits in the pre-registration's §0 table, which A2 requires reading at 96cccf4. My failure reason, written from the checklist evidence, is in the header.

**My failure reason.** In the Bell-state, reverse-order system, the chip's later sequential measurements carried large order-dependent biases. Δ0 was 0.70, and in R3 reverse X1Z2 and Z1X2, measured after Y1Y2, had means +0.42 and −0.39 against 0. So the CbD LP fitted a noncontextual model there. Kind: `design` (the effect is there by physics; the design could not see it through the device's disturbance).

**The pre-mortem** (§0, 96cccf4): "If this fails, the most likely reason is that ancilla 4's mid-circuit readouts and resets disturb the data qubits enough, growing with each later measurement, that CNT2 reaches 0 in at least one of the four systems." Kind: `design`.

**Score: `named`.** The checkable mechanism happened as stated:
- disturbance of the data qubits by the sequential measurement blocks;
- concentrated in later positions (the biases appear only after an earlier block; first-position means are near ideal);
- CNT2 reaching 0 in exactly one system.

The one part the record cannot confirm is the attribution to the ancilla's readout and reset rather than to the blocks' gates (for example the Y-rotation calibration) or crosstalk. The results file says so ("in shape, not shown in cause"). A stricter reading would give `kind_only`. I score `named` because the mechanism at the level the design can resolve is the one named.

## Required cuts

1. Results file, "What this does and does not say", fourth bullet. Cut: "Each line's product had magnitude 0.65–0.74 against the simulator's 0.95–0.96."
   Replace with: "Each line's product had magnitude 0.65–0.92 against the simulator's 0.95–0.97: 0.65–0.73 on lines R2, R3 and C3, and 0.76–0.92 on R1, C1 and C2."
2. Results file, "Secondary comparisons", calibration bullet. Cut: "(IBM's `last_update_date` 17:35:25 both times)"
   Replace with: "(every value below was the same in both reads; IBM's `last_update_date` was 17:35:25 at submission and 17:57:35 at run time)"
3. Results file, the citation-correction paragraph. Cut, in full: "*Citation correction (D51):* the pre-registration's §0 cites the 2019-era IBM figure (about 4.99) as "Laghaout et al. 2022"; its first author is Dikme (Dikme, Reichel, Laghaout & Björk 2022, Eur. J. Phys. 43:055401, arXiv:2009.10751), as the Novelty session found. The frozen text is left as committed."
   Replace with: "*Citation note (D51, corrected by the audit):* the pre-registration's §0 cites the IBM figure (about 4.99) as "Laghaout et al. 2022", which is right for the journal article: Laghaout, Dikme, Reichel & Björk, "A demonstration of contextuality using quantum computers", Eur. J. Phys. 43:055401 (2022). Its arXiv preprint (arXiv:2009.10751, "Measuring the Mermin-Peres magic square using an online quantum computer") lists Dikme first. The frozen text is left as committed."
4. Results file, Novelty line (F27: the required cut is the corrected line). Two edits:
   - Cut "4.987 from products only, already worse in one measurement order, Dikme et al. 2022, Eur. J. Phys. 43:055401, arXiv:2009.10751)".
     Replace with "4.987 from products only, already worse in one measurement order, Laghaout et al. 2022, Eur. J. Phys. 43:055401; preprint Dikme et al., arXiv:2009.10751)".
   - Cut "(5.3076 on ibm_kingston, no error bars, Kelleher & Holweck 2025, arXiv:2505.21243;".
     Replace with "(5.3076 on ibm_kingston for the best of the squares of three-qubit operators embedded in W(5,2), not the two-qubit square, no error bars, Kelleher & Holweck 2025, arXiv:2505.21243;".
5. Results file, "Secondary comparisons", first bullet. Cut: "Kelleher & Holweck's 5.31 on another Heron r2 (ibm_kingston) was the best of several embedded squares, measured with another readout and with no error bars."
   Replace with: "Kelleher & Holweck's 5.31 on another Heron r2 (ibm_kingston) was the best of several squares of three-qubit Pauli operators embedded in W(5,2), not the two-qubit square measured here, with another readout and with no error bars."

D51's row in DEVIATIONS.md carries the same author error ("The paper's authors are Dikme, Reichel, Laghaout & Björk"). The owning session should correct it in a new dated row and leave the old row unedited.

Not a cut, but recorded: `reproduce.py` copies CNT2 and its bootstrap from the archive rather than recomputing them ("the LP needs scipy"). So the primary statistic is not regenerated by the reproducibility script. I regenerated it here (exact match), so `reproduced: true`. A scipy-gated CNT2 check in `reproduce.py` would close this.

## What would break it next

- **The cheapest overturning test.** Re-run, in a fresh job on the same triple (3, 4, 5), the Bell-state reverse-order R3 circuit and its forward twin. The Bell-reverse system needs six circuits × 4,000 shots, about 7 QPU s; the two-line diagnostic needs about 3 s.
  - If R3 reverse's X1Z2 and Z1X2 biases (+0.42, −0.39) do not recur, the fail was one job's coherent error and the Bell-reverse label is not a stable property of the device.
  - If they recur, adding one circuit that measures Y1Y2 and then reads qubit 5 in the X and Z bases tells a coherent rotation on qubit 5 after the Y block from ancilla readout or reset disturbance. That would turn the pre-mortem's "in shape" into "in cause".
- **Free, offline.** Fit a single-qubit rotation on data qubit 5 after the Y1Y2 block to the 24 archived distributions and see whether it explains Δ0 0.70.

Either would be its own pre-registered bet. This audit makes no hardware call.
