---
bet: ng-p3-9
program: nature-graded
prereg_commit: 96cccf4
reviewer_session: fresh subagent of the p3-9 worktree session
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 17:29 America/Denver
checks: {D1: holds, D2: holds, D3: holds, D4: holds, D5: holds, D6: holds, D7: holds, D8: flaw, D9: holds, D10: flaw, D11: holds, D12: flaw}
prior_work_search: "magic square contextuality IBM quantum mid-circuit measurement ancilla sequential QND experiment signaling marginals" (web search, $0; not required, since the line cites a predicted outcome; it found no CbD, marginal or signalling analysis of sequential superconducting PM data)
papers_opened: 5
flaws: 4
pilot_usd: 0.00
verdict: fix-first
confirmed_at: null
---

# Design review of ng-p3-9

## In plain English

As built, this test would answer its question. The circuits measure what the square says, in both orders. The reverse-order bits are put back in the right place. The linear program agrees with an independent one written from the definitions. A noncontextual system cannot pass, even one sitting right on the boundary with sampling noise. The bet can pass, and it can fail under noise that is plausible, if larger than IBM reports. The budget sits far inside both the hard stop and the reserve line: 89 s used plus the 45 s cap is 134 s, against a 420 s hard stop and a 300 s reserve line.

Four things must change before the job runs, and none of them changes what is tested:
- **A crashed client.** If the client crashes after IBM has taken the job, the job id is lost. The code then calls the bet untestable, while the pre-registration says the counts are fetched. That leaves the choice to someone acting by hand, possibly after the counts are visible.
- **"Program 1's check."** The pass sentence credits program 1's check, but this is a new program. It does reduce to program 1's two-question Γ (I checked: 305 of 305), but nothing committed shows that.
- **The 45 s budget.** "≤ 45 QPU s enforced in code" overstates it: only the estimate is gated.
- **One prior-work number.** The Heron r2 figure of 5.31 is the best of several squares, which the prior-work row and the planned comparison should say.

## Checks

Commands were run from the worktree at `eacc118` with `PY=/Users/seanpharris/entangled-mind/.venv/bin/python`. The reviewer's scripts are in the session scratchpad, `review/r1_mapping_lp.py`, `r2_boundary_dephase.py` and `r3_rank2.py`. The machine was at load ≈ 64 from other sessions during the review, so the runs were slow, not wrong.

**D1. The rule can be applied by a stranger: holds.**
- `verdict()` returns exactly one of pass or fail on all 81 label combinations, and pass happens iff all four systems are contextual (`--check` part 4). The untestable branch is separate.
- I applied §5 by hand to the committed worlds file (`data/p3-9-worlds.json`):
  - `noisy_sim`: 4 × contextual, so pass.
  - `flip0.04`: 00-fwd and bell-rev are below, so fail plus the "below" noise sentence.
  - `cheat`: 4 × absorbed, so fail plus the "absorbed" sentence.
  - In each case the code's verdict matched mine.
- Boundaries (P13): every comparison against zero uses the same tolerance of 1e-6. That holds in `classify`, `verdict`, `worlds`, `n_boot_zero` and `loo_rests_on`, and χ's bar is `> 4 + TOL` everywhere. A lower bound of exactly 1e-6 lands on "not contextual", as §4 says ("≤ 1e-6 counts as zero").
- The lower bound is `np.sort(vals)[LB_RANK-1]`, the 10th smallest of 1,000, as §4 says.
- The one gap a stranger meets is the client-error case, which is under D10 (F1).

**D2. Every manipulation takes effect: holds.**
- *Observables and blocks.* I prepared a random two-qubit state (`random_statevector(4, seed=11)`) in front of the 12 logical |00⟩-slot circuits and simulated 40,000 shots each (Aer statevector). In both orders, after `pm_system`'s re-indexing, every variable's mean in every context and every within-line pair correlation was compared with Tr(ρ O) and Tr(ρ A B), computed from Pauli matrices independently of `logical()`. That is about 90 quantities. Result:
  - max deviation 0.0084, at a sampling SE of about 0.005;
  - χ 6.0 in both orders, CNT2 0.33, Δ0 at the sampling level (0.013 and 0.010) (`r1_mapping_lp.py ab`). On a state with no symmetry, a wrong rotation (X→H; Y→S†,H and back H,S), a wrong CNOT set or a wrong reverse-order bit map would show here.
  - By hand: in `pm_system(reverse=True)`, measured bit 0 is the line's last observable, and `t = b[2] | b[1]<<1 | b[0]<<2` puts it back at index 2. Correct.
  - The square's signs check by hand: C3 = Z⊗Z · X⊗X · Y⊗Y = −I; the other five lines give +I.
  - The Bell preparation through the ancilla (H; CX(d1,a); CX(a,d2); CX(d1,a)) gives (|00⟩+|11⟩)/√2 with the ancilla back in |0⟩.
- *Committed ISA circuits.* `data/p3-9-circuits.qpy`'s SHA-256 equals `prepared.json`'s `qpy_sha256`.
  - The 24 circuits are named in canonical label order and are ISA on FakeFez's target on (3, 4, 5).
  - They have 156 qubits and one 3-bit register `meas`, which is what `run_hardware` reads as `pub.data.meas`.
  - Simulated ideally (Aer density matrix, 20,000 shots), they give χ 6.0 in all four systems, CNT2 0.246–0.248 and Δ0 0.011–0.015 (sampling).
  - So level-0 transpilation onto (3, 4, 5) changed nothing that matters.
  - `job_order`'s permutation inverts to canonical order the way `analyse` inverts it (`counts[order[pos]] = job[pos]`).
- *Noise knobs.*
  - The flip ε moves the true CNT2 monotonically. Taking 00-fwd / 00-rev / bell-fwd / bell-rev in turn:
    - 0.03: 0.049 / 0.087 / 0.087 / 0.044;
    - 0.035: 0.022 / 0.066 / 0.066 / 0.018;
    - 0.04: 0 / 0.045 / 0.045 / 0;
    - 0.05: 0 / 0.006 / 0.006 / 0.

    (`worlds.json` and my rerun.)
  - My exact Kraus world (outcome flip r per block, Z-dephasing p of both data qubits after each readout) moves CNT2 smoothly in p and r; table under D11.
  - The order and state knobs change the systems: ideal CNT2 is 0.250 forward and 0.248 reverse at 200,000 shots, and the noisy Δ0 differs by order (0.013 against 0.024 for |00⟩).
- *Parameters actually used.*
  - SHOTS 4000, B 1000, LB_RANK 10, TOL 1e-6, EST 0.28 ms + 2 s, cap 45, reserve 300, hard stop 420, MIN_SHOT_FRAC 0.90.
  - The bootstrap seed is `seed_boot` from `data/p3-9-seed.json`, and the order seed is `seed_order`.
  - All of these match the pre-registration's text.

**D3. Every control can fail: holds.**
- *Wrong set-up 1: a noncontextual system with χ = 6 (the cheat).* It must be rejected and it is: CNT2 0 in all four systems, labelled absorbed, P(pass) 0 (`--check` part 2, `worlds.json`).
- *Wrong set-up 2: noncontextual models with signalling.* `--check` runs 30 models with context- and position-dependent flips of up to 10%; the maximum CNT2 is 0.
- *Wrong set-up 3, the one `--check` does not run: a noncontextual system exactly on the boundary, with 4,000-shot sampling noise.* This is the case where a percentile bootstrap could be anti-conservative.
  - I bisected the flip family to ε* = 0.03929, the first ε where |00⟩-fwd's true CNT2 reaches 0, and took ε = 0.03939 (true CNT2 0, true χ 3.430).
  - Of 300 sampled datasets, 1% had point CNT2 > 0 (maximum 0.0035).
  - I bootstrapped the five with the largest point CNT2 (B = 200, 99% lower bound = 2nd smallest). Every lower bound was 0, so there were **0 false positives** (`r2_boundary_dephase.py d 300 5`). Every other dataset had a smaller point value.
- *The LP itself (independent rebuild).* I wrote the CbD feasibility LP from the definitions, without `cbd_lp`'s threshold-string reduction: all 2¹⁸ joint values; every bunch cell (6 × 8) matched exactly; each connection maximally coupled, Pr[unequal] = |p₁ − p₂|. I ran it on all 24 world systems (six worlds — `noisy_sim`, `flip0.03`, `flip0.035`, `flip0.04`, `flip0.05`, `cheat` — times four systems), and it gave the same verdict as `cbd_lp.cnt2 > 1e-6` on **24 of 24** (`r1_mapping_lp.py c`):
  - contextual: every `noisy_sim` and `flip0.03` system;
  - noncontextual: `flip0.04`'s 00-fwd and bell-rev and all four `cheat` systems;
  - `flip0.05`: 00-rev and bell-fwd still contextual, at CNT2 0.006 with χ 2.9.

  The pre-registration's sharpest claim, contextual with χ < 4 in `flip0.03`, therefore does not rest on `cbd_lp` alone. My exact dephasing world shows the same thing (bell-fwd at p = 0.15: χ 3.47, CNT2 0.089). It comes from noncontextuality constraints other than the Peres–Mermin sum, which mean little for a near-deterministic Bell state; §5.3's extra sentence covers it.
- *The Kirchmair control* is the "sees it where it is" check on published data: minimum CNT2 0.141 over every completion (`--check` part 2).
- `$PY programs/nature-graded/experiments/p3_9_pm.py --check` printed "check OK" (about 47 minutes of wall time under load). Its output:
  - (1) LP = KDL on 180 of 180;
  - (2) Kirchmair minimum CNT2 0.1414, χ 5.463, Δ0 0.166; the cheat at χ 6.000 with CNT2 0 in all four systems; 30 noncontextual flip models with maximum CNT2 0; `build_fast` = `build`;
  - (3) ideal χ 6.0 in all four systems; full 2¹⁸ LP = reduced LP on Bell-fwd; ISA on FakeFez (3, 4, 5);
  - (4) one verdict on all 81 combinations.

**D4. Rivals are matched: holds (not applicable).** There are no competing model families. The rule tests one exact criterion against the data, and noncontextual explanations enter through the LP itself, with any amount of signalling absorbed (D3).

**D5. A dumb baseline is beaten: holds.**
- The dumb rule "χ > 4" is passed by the cheat (χ 6.000) and refused by this rule (CNT2 0). §4 names it.
- The noiseless-simulator baseline is not a predictor of the chip here. The carry-over baseline (0.95) and the base rate (0.32) are named for scoring.
- This is not a null rule, so no equivalence margin is needed.

**D6. Foreseeable execution risks: holds.**
- The pre-mortem is of kind `design`, not `execution`.
- Execution risks:
  - *Dynamic circuits on SamplerV2.* Measure and reset are in the live target; `check_isa` runs against `be.target` at submission and refuses, as untestable, if they are not.
  - *Open Plan batch mode.* All nine earlier jobs ran through the same `Batch` path.
  - *The 90% shot floor.* It is in `untestable()`.
- A pilot would itself cost QPU seconds, and none is needed. No API call is involved.

**D7. Comparisons match: holds.** The scored event is a conjunction over four systems, not a comparison. One secondary comparison, "χ against Kelleher & Holweck's 5.31 on another Heron r2", differs from this run in every respect but the chip family:
- device (ibm_kingston against ibm_fez);
- readout (not sequential mid-circuit measurement);
- input state;
- shots (10,000);
- and the 5.31 is the best of several embedded squares (see F4).

It is "reported, never promoted", so it is not a flaw here. The write-up must describe it as a comparison of the whole bundle, never as the cost of sequential measurement.

**D8. The verdict sentences are written: flaw (F2).**
- Sentences exist for every outcome:
  - pass;
  - each of the three fail headlines;
  - both noise sentences, including the one for when chip noise spoils the check ("every miss is absorbed");
  - every per-system label, the χ ≤ 4 rider and the order-mattered sentence;
  - untestable.
- `--check` prints them for every combination.
- But the pass headline uses a noun the design does not carry: "**Program 1's check** sees contextuality on this chip". Program 1's check is Γ = |q_QQ| − OSS on two-question, two-order systems (`programs/entangled-mind/experiments/exp4_run.py`, `"Gamma": abs(q) - oss`; experiment 5 reused it). This bet runs `cbd_lp.py`, a new exact LP written for P3-9, on a rank-6 system.
  - The two do agree where both apply. I ran `cbd_lp.cnt2` against KDL (n = 2) and against program 1's Γ formula on 305 random rank-2 systems, 177 of them contextual: **305 of 305 agree** (`r3_rank2.py`).
  - Nothing committed shows this. `--check` tests KDL only at ranks 3–5.
  - A pass would also say nothing about whether Γ had the power to fire at program 1's sample sizes. That is the open question behind program 1's null (1 of 80 pairs with Γ > 0), and readers will reach for this bet to answer it.

**D9. One item cannot decide it: holds.**
- Leave-one-out is pre-registered and reported, not a gate: each of a system's six circuits in turn is replaced by its noisy prediction, and the line is named if the point CNT2 crosses zero.
- Replacing with the prediction rather than dropping is the right choice: any five of the six lines can be satisfied by a noncontextual model, so dropping a circuit would always say "noncontextual".
- The replacement is a favourable value, so this leave-one-out can flag a fail that rests on one bad line more easily than a pass that rests on one line. The write-up should say so if `loo_rests_on` is empty.

**D10. Machinery: flaw (F1, F3).**
- *Budget estimate against the ledger* (`programs/entangled-mind/results/ibm-usage.json`, all nine ibm_fez jobs; billed seconds are rounded to whole seconds):
  - witness: 39 circuits × 4,000 = 156,000 shots → 44 s, 0.269 ms per shot all-in;
  - P3-18: 66,000 shots → 20 s, 0.27 ms per shot after the 2 s;
  - wave 1: 20,000 shots → 8 s;
  - small jobs bill 2–4 s.
  - The estimate of 0.28 ms × 96,000 + 2 s = 28.9 s is consistent with the two large jobs.
  - All nine earlier jobs were static circuits. This is the first job with mid-circuit measurements and resets, so the per-shot cost is untested here. Three measures and three resets add about 10 µs to a shot of roughly 270 µs, under 5%. The ×1.5 contingency (43.3 s) covers far more than that.
- *Cumulative usage.* 2 + 44 + 8 + 4 + 4 + 3 + 2 + 2 + 20 = **89 s**, as stated. (The service-reported figure lags one job behind: P3-18's `service_after` reads 69.) The code takes the larger of the ledger and the service figure.
- **89 + 45 (cap) = 134 s < 420 s hard stop.**
- **89 + 1.5 × 28.88 = 132.3 s < 300 s reserve line.**
- **Even at the cap, 89 + 45 = 134 s stays under the reserve line.** Crossing the reserve line would take a bill of 211 s (7.3× the estimate); crossing the hard stop, 331 s (11.5×). Both stay under. The budget is approved as stated, subject to F3's wording.
- *Refusals in code.*
  - `p3_9_pm.submit` refuses, as untestable:
    - if `used + 45 > 420`;
    - if `used + 1.5 × est > 300`;
    - if `est > 45` or `45 > approved`;
    - with no `budget_ruling` row under st-16;
    - without a design-review go.
  - It also refuses on uncommitted files, a failed `check_prereg --before-run`, a hash mismatch, or an existing raw file, marker or ledger entry.
  - `backends.run_hardware` refuses only when `used ≥ 420`. It does **not** refuse a job that would cross 420, and nothing caps the job's billed seconds (no `max_execution_time`). For this bet `submit`'s cap check covers the first gap, and the margin covers the second (F3).
- *One job.*
  - `run_hardware` makes one `sampler.run` call with no retry.
  - `already_ran()` checks the raw file, the marker (written before `run_hardware`) and any usage-ledger purpose starting "Program 3 P3-9 ".
  - Every `NotSubmitted` path writes the raw file first.
  - A kill or Ctrl-C during the job leaves the marker (the `BaseException` handler also writes the raw file).
  - Nothing in `--submit` can start a second job.
- *The failed-job path is not closed (F1).*
- *Other machinery.*
  - The scale direction does not apply.
  - Caching is by content hash (the qpy hash gate).
  - Beacon: CURBY-Q was stalled (round 28297, 2025-08-22), so the chain is CURBy-RNG. Pulse 1592865 is at 23:21:00Z, and the previous pulse 1592864 at 23:20:00Z is before the commit at 23:20:14Z. Sub-seeds `order` and `boot` are recorded and used by `job_order` and `analyse`. I did not recompute `seed.py`; the auditor's E23 does.
  - The lesson line `ls-ng-p3-9` matches §0 verbatim and names P6 and P12, and the design follows both (D3, D11).

**D11. The bet can both pass and fail: holds.**
- The committed worlds give P(pass) 1.00 under `noisy_sim` (the hypothesis world) and 0.95 under `flip0.03`. They give 0.00 under `flip0.04`, `flip0.05` and `cheat`. So each outcome is reachable under a named world.
- Flips are a stylised model, so I added a physical world, built exactly from quantum theory: outcome flip r per readout (readout and reset error), plus Z-dephasing p of both data qubits after each mid-circuit readout (measurement-induced dephasing). True CNT2 (`r2_boundary_dephase.py e`):

  | r | p = 0 | 0.04 | 0.08 | 0.10 | 0.12 | 0.15 |
  |---|---|---|---|---|---|---|
  | 0.005 | 0.235 (all) | 0.143 / 0.196 | 0.061 / 0.157 | 0.024 / 0.138 | **0** / 0.118 | **0** / 0.089 |
  | 0.02 | 0.192 (all) | 0.107 / 0.156 | 0.031 / 0.120 | **0** / 0.102 | **0** / 0.083 | **0** / 0.056 |

  (Each cell gives |00⟩, both orders / Bell-fwd. Bell-rev lies between them and reaches 0 at p ≈ 0.15.)
  - The |00⟩ systems fail first: at 10–12% per-readout dephasing of each data qubit with 0.5–1% outcome flips, or at about 9% with 2% flips.
  - IBM's reported numbers for the triple (ancilla readout 0.24%, CZ 0.17% and 0.33%) are far from that.
  - The one published Heron r2 square (5.31, no mid-circuit measurement) corresponds to r ≈ 0.02 with p = 0, CNT2 0.19, which still passes.
  - Google's Willow repeat-agreement figure (0.9636, about 1.8% per QND measurement) also points to a pass.
- So a fail needs mid-circuit disturbance several times IBM's calibration. That is plausible for an untested dynamic-circuit path on this device, but not likely. The engine's 0.80 prices that reasonably. P(fail) is not below the 10% floor, and the result is not known before it runs.

**D12. The predicted outcome is in print, and the bet says what it adds: flaw (F4, wording only).**
- (a) The line states a predicted outcome ("Prior work predicts a pass for both input states"), with citations.
- (c) The outcome is in print, and §0 says what the bet adds: the exact CbD 2.0 LP, with a bootstrap, on sequential mid-circuit-measurement superconducting data, in both orders and for two states. The engine's 0.80 is stated with that prior in view, and both the lesson and the odds reason name it.
- (d) Not required. I ran one search anyway, in other words: "magic square contextuality IBM quantum mid-circuit measurement ancilla sequential QND experiment signaling marginals". It found Kelleher & Holweck, Laghaout et al., Kumar et al. and nothing with a CbD, marginal or signalling analysis of sequential superconducting PM data. That agrees with the line.
- (b) Papers opened:
  1. **Kumar et al. 2025** (arXiv:2512.02284, full HTML). Supports its citation. χ_KSB = 5.618 ± 0.005, from "successive quantum non-demolition (QND) measurements of two qubits … using an ancilla qubit", with the ancilla reset after each measurement, on Willow processors. There is no signalling or CbD analysis. Repeat agreement in compatible contexts is 0.9636 ± 0.0004.
  2. **Kelleher & Holweck 2025** (arXiv:2505.21243, full HTML). Table 1 gives the square's χ_NISQ = 5.3076 on ibm_kingston (Heron r2), 10,000 shots, no error bars. But the caption says "for subgeometries … **best performing representative shown**", so 5.31 is the best of several embedded squares. The text I read says the readout "follows ref. [18]" and does not call it "product-only". This is F4.
  3. **Massé 2021** (arXiv:2105.13821, PDF). Supports its citation. §XI.D applies "the CbD approach … following the steps used for similar cases in [37]": Δmin 0.732 ≥ Δ0 0.166, CNTX = 0.566 (eq. 115). The formula comes from an earlier cyclic-system method, not the exact CbD 2.0 LP, so "adapted, not exact" is fair.
  4. **Laghaout et al.** (arXiv:2009.10751, PDF). Supports its citation. Sequential QND measurements through an ancilla on ibmqx4; "the best result vector … v · q₁ = 4.987 ≥ 4". This too is a best-of, consistent with the line's "about 4.99".
  5. **Kirchmair et al. 2009** (arXiv:0904.1655, abstract only). A state-independent violation with trapped ions, "despite imperfections and possible measurement disturbances". The 5.46(4) and the per-context means are taken through Massé's transcription, which the desk work reproduces (χ 5.463, Δ0 0.166, CNTX 0.565).

## Required fixes

Each fix goes under one dated DEVIATIONS.md row, written before any submission and naming this review (`ledger/design-reviews/ng-p3-9.md`). The reviewer then confirms it in an addendum here. None of them changes the pass rule, the circuits, the shots, the seed or the odds.

**F1 (D10, also D1): close the failed-job and crashed-client path.**
- *Evidence.*
  - `backends.run_hardware` learns and logs `job.job_id()` only after `job.result()` returns.
  - `submit`'s marker keeps `job_id: None` until `run_hardware` returns.
  - Its `except BaseException` branch writes `data/p3-9-raw.json` with `client_error` and no job id.
  - `untestable()` then returns "the job returned no counts".
  - §7 says instead: "A client error after submission leaves the marker and is resolved by looking the job up by id (a free read); the counts are retrieved, never re-run." No code does this, and no rule says when a client error is untestable and when its counts are the data. The person deciding could see the counts on IBM's dashboard before choosing: a forking path.
  - A job that errors or is cancelled also never reaches `ibm-usage.json`, so its seconds would be missing from the ledger total. The service figure lags one job in this ledger.
- *Fix.*
  - (a) Record the job id at submission. Give `run_hardware` an optional `on_submit(job_id, batch_id)` callback, called right after `sampler.run(...)` and before `job.result()`. P3-9 uses it to write `job_id` into `data/p3-9-submitting.json`. Other callers are unchanged.
  - (b) In `run_hardware`, log a usage entry (seconds from `job.metrics()` when available, else `null` with a note) when `job.result()` raises, before re-raising.
  - (c) Add `p3_9_pm.py --retrieve`, a free read. It requires the marker's job id and no counts in the raw file. If IBM's status is DONE, it fetches the result and writes the raw file in the normal format (`counts_in_job_order`, `order` from the marker, `usage`, `retrieved: true`). Otherwise it records the status. It never submits.
  - (d) Amend §5.4 and §7, and make `untestable()` follow the wording: "a client error is never by itself untestable. If IBM reports the job DONE, its counts are the data and are fetched with `--retrieve`. The bet is untestable only if IBM reports the job ERROR or CANCELLED, returns no counts, returns the wrong number of circuits, or returns a circuit under 90% of its shots."
  - Add a `--check` line that drives `untestable()` with a synthetic `client_error` raw file, with and without retrieved counts.

**F2 (D8): the pass sentence must not credit "program 1's check" without the link.**
- *Evidence.*
  - Program 1's instrument was Γ = |q_QQ| − OSS on rank-2 systems (`exp4_run.py`). This bet runs the new exact LP in `cbd_lp.py` on a rank-6 system.
  - Where both apply, the two agree: 305 of 305 random rank-2 systems, 177 contextual (`r3_rank2.py`). `--check` does not show this.
  - A pass does not test Γ's power at program 1's sample sizes.
- *Fix.*
  - (a) Add a rank-2 block to `--check`. It runs `cbd_lp.cnt2` on random `cyclic_system(2, …)` systems, half of them contextual, and asserts the same sign as `kdl_contextual(2, …)` and as program 1's Γ (|Δ P(disagree)| − (|ΔpX| + |ΔpY|), computed from the same bunches).
  - (b) Reword the pass headline in `verdict()` and §5.1, and the matching phrase in §1 and in the title's reading: "… the exact CbD 2.0 linear program, which reduces to program 1's rank-2 Γ on two-question systems (shown in `--check`), sees contextuality on this chip where physics says it must be. …"
  - (c) Add to §6: "It does not show that program 1's Γ had the power to detect contextuality at program 1's sample sizes. Program 1's null is as informative as its own power made it, and no more."

**F3 (D10): state the budget enforcement as it is.**
- *Evidence.*
  - §0 and §3 say "≤ 45 QPU s … enforced in code". The code gates the *estimate*: `submit` refuses if `est > 45`, if `used + 45 > 420` or if `used + 1.5 × est > 300`.
  - No code caps the job's *billed* seconds.
  - `run_hardware`'s own check is `used ≥ 420`, not `used + job > 420`.
  - At 89 s used, nothing realistic reaches the reserve line (211 s) or the hard stop (331 s), so this is a wording fix, not a risk.
- *Fix.*
  - Reword §0, §3 and §7: "the estimate (28.9 s) and the 45 s cap are gated in code against the 300 s reserve line and the 420 s hard stop. The job's billed seconds are not capped, since a `max_execution_time` cancellation would destroy the one job. A bill above 45 s is reported as an overrun of the budget ruling and changes nothing else."
  - Make the budget ruling row say the same.
  - Optional, for shared code: give `run_hardware` an `expected_s` argument that refuses when `used + expected_s > QPU_STOP_SECONDS`.

**F4 (D12(b)): correct the Kelleher & Holweck citation.**
- *Evidence.* Their Table 1 reports the square's 5.3076 as the "best performing representative" of several embedded squares (10,000 shots, no error bars). The text I read does not describe the readout as "product-only".
- *Fix.*
  - In §0's prior work row, §4's secondary list and the map's Prior work line, write: "5.31, the best of several embedded squares, 10,000 shots, no error bars (readout as in their ref. [18])". Keep "product-only" only if the author can quote the page that says it.
  - Note that Laghaout's 4.987 is also a best-of.
  - In the write-up, describe the "χ against 5.31" secondary as a comparison with an upward-selected figure on a different device and readout (D7).
- The predicted outcome (pass) and the odds do not move.

## Confirmation (fixes at 102f7e8)

I read 102f7e8 and the DEVIATIONS.md row D49 against the code. I did not run `--submit`, `--select`, `--worlds` or `--retrieve`, and made no IBM contact. I tested `untestable()` by importing it directly (`review/r4_untestable.py`). **Three of the four fixes are confirmed. F1 is not, so `confirmed_at` stays null.**

- **F1: not confirmed.**
  - *What works:*
    - `run_hardware` calls `on_submit(job_id, batch_id)` right after `sampler.run`, before `job.result()`, and `submit` writes the id into the marker there.
    - A raising `job.result()` logs a usage entry before re-raising. Its purpose still starts "Program 3 P3-9 ", so `already_ran()` sees it.
    - `--retrieve` is a free read that never submits.
    - `untestable()` refuses on a client error until IBM's status is read, returns untestable on ERROR or CANCELLED, and treats DONE with counts as data.
  - *Two raw-file states a crash can leave are still wrong.* Block (5) drives neither.
    - **(i) A job that has not finished becomes untestable.** If `--retrieve` runs while the job is RUNNING or QUEUED, it records `ibm_status` and no counts. `untestable()` then returns "the job returned no counts" for a job that may still finish DONE. That is the forking path F1 was about: analyse now, or wait and fetch.
    - **(ii) A client error before IBM returns a job id dead-ends.** This happens when the exception is raised inside `run_hardware` before submission: a network error in `service_usage()`, the new `expected_s` hard-stop `RuntimeError`, or `Batch` or `sampler.run` raising. `submit` records it as `client_error` with `job_id: null`. `untestable()` then refuses ("run --retrieve first") and `--retrieve` refuses ("the marker holds no job id"). The marker blocks any resubmission, so the bet can never be analysed or declared untestable, though §5.4 lists "the job was not submitted" as untestable.
  - *Fix:*
    - (a) In `untestable()`, with no counts, refuse (SystemExit "job not finished: run --retrieve again") unless `ibm_status` is ERROR, CANCELLED or NOT_SUBMITTED. DONE without counts also refuses.
    - (b) When the marker has no job id, `--retrieve` makes a free read: `service().jobs(backend_name="ibm_fez", created_after=<marker submitting_at − 2 min>, limit=10)`.
      - No job found: write `ibm_status: "NOT_SUBMITTED"`, which is untestable ("not submitted").
      - Exactly one: adopt its id and proceed as now.
      - More than one: refuse and record the ids.
    - (c) Add the RUNNING, QUEUED, DONE-without-counts and NOT_SUBMITTED cases to `--check` block (5).
    - (d) Put one sentence in §5.4/§7 under D49 (or a new row).
- **F2: confirmed.**
  - `--check` block (1b) asserts that the LP, KDL at n = 2 and program 1's Γ (|q_QQ| − OSS, the same formula as `exp4_run.py`) agree, and that 25–75% of the systems are contextual. The author reports 154 of 154, 92 contextual; my own run of the same construction gave 305 of 305.
  - `verdict()`'s pass headline and §5.1 now say "the exact CbD 2.0 linear program, which reduces to program 1's rank-2 Gamma on two-question systems (shown in --check)".
  - §6 has the power sentence.
- **F3: confirmed.**
  - The header, §0, §3, §7 and §9 now say the estimate and the cap are gated and the bill is not, with an overrun reported against the ruling.
  - `run_hardware(expected_s=45)` refuses when used + 45 > 420.
  - The budget figures are unchanged: 89 + 45 = 134 s, under the 300 s reserve line and the 420 s hard stop.
- **F4: confirmed.**
  - §0 (and the ledger inbox update), §4's secondary list, `program-3-map.md`'s P3-9 entry and Prior work table, `program-3-map.json` and `map/nature-graded.json` now say "the best of several embedded squares, 10,000 shots, no error bars". "Product-only" is gone from each.
  - Laghaout is marked as a best-of too.
  - *New, small:* `programs/nature-graded/map/program-3-map.md` line 11 still says "On a Heron r2, Peres–Mermin has been run only with product-only readout, which CbD cannot analyse". The same unsupported claim should be reworded in the F1 fix commit.

Nothing else new. The pass rule, bars, circuits (the qpy hash is untouched), shots, seed, worlds and odds are unchanged by 102f7e8.
