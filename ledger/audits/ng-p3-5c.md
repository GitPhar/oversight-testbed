---
bet: ng-p3-5c
program: nature-graded
prereg_commit: 930efe8
results_commit: 5c01437            # the audit clone's HEAD; author time 2026-11-04 22:51:33 -07:00
auditor_session: audit ng-p3-5c (fresh subagent session, audit clone /Users/seanpharris/oversight-testbed-audit-ng-p3-5c)
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5      # ls-ng-p3-5c "model", session nature-graded-0a; the design reviewer is the same model too
same_model_family: true
date: 2026-11-04 23:20 America/Denver
claims_checked: 28
holes_found: 4
overclaims_cut: 4                  # Required cuts 1-4
reproduced: true                   # p3_5c_fits.run() on a scratch copy, with the archived bootstrap nulls reused (120 of 12,000 null draws recomputed by seed index). Every table value regenerates at its displayed precision except the secondary CV column (h088 +22.4 / +228.2 against +22.9 / +228.7; h268 +145.7 / +67.3 against +145.6 / +67.1), from floating-point drift of about 1e-4 logL starting at h088. h221 is bit-exact.
verdict_claimed: pass              # the bet has no pass/fail rule (unscored). Its pre-registered reading "both present" on every pair (the outcome §1 anticipated) is entered as pass, so the pre-mortem, whose failure is "steering hidden", can be scored. Reported as "both present on 3 of 3 pairs"
verdict_after_audit: pass-unreplicated   # one job, one afternoon (3 November), three pairs, an archive already analysed twice; not scored
verdict_stands: true               # every label regenerates and survives every re-analysis run here (60-start refits, all 9 leave-one-setting-out refits, all 36 leave-two-out refits on h221, overdispersion scaling). The holes are one scope word, two mechanism nouns and one missing fragility number
canary: unknown
false_alarms: 0
design_review_missed: ["D9: F6's fix is a one-setting rule (more than half of an LR). Two settings carrying most of it pass that rule unseen: on h221, XZ and XY carry 69% of the rotation LR (26.5 of 38.5), and dropping both leaves 13.8 against the null's 99th percentile of 13.0", "D4: the review checked rivals inside the state model (decay, an XX rotation) but not against the fixed assignment matrix. Symmetric readout error beyond A acts on tomography counts exactly like local depolarising, so the blur family cannot be told apart from readout drift in principle. On h221 and h268 a rotation model with 4 readout knobs makes the blur term unnecessary (LR_i 8.9 and 7.6, below the null q99s of 9.0 and 8.8). Here it needs 2.7-5% extra readout error per qubit, against IBM's reported 0.2-0.9%, so it is an unlikely rival on this archive"]
failed: false
failure_reason: "None: the bet's reading came out 'both present' on all three pairs and survives re-analysis. Had it failed, my most likely reason: h221's rotation label, the weakest (LR 38.5 against a null maximum of 22.8, 69% of it from XZ and XY), falling under the line after a small change to the blur side of the model (with 4 readout knobs it drops to 20.3). Kind design."
failure_kind: null
premortem_score: not_failed
risk_seen: false                   # the named risk was local optima widening the null. The three largest h221 rotation null draws refit with 40 starts move by at most 0.02; the observed nested fits are at their 60-start optima (gains <= 0.003; full16 on h088 +0.056); the rotation nulls' q99s (13.0-17.5) sit below chi2_7's 18.5
---

# Audit of ng-p3-5c: corrected P3-5, nested rotation-given-blur and blur-given-rotation tests

## In plain English

The result stands. On each of the three archived qubit pairs, the 16-knob model needs both its rotation-type term and its blur-type term, and every one of the six tests clears its bootstrap null by a wide margin. The run regenerates from the archive and the code. The labels survive refitting from 60 extra starts, dropping any one tomography setting, dropping any two settings on the weakest pair (h221), and scaling for the misfit on h088. Four sentences go further than the data. The title says "every pair" where the data are three pairs from one job on one afternoon. Two sentences say "kind" or "steering" where the design can only say "term". And the weakest label (rotation on h221) rests 69% on two settings, which the file does not say in numbers. What would break it next: a $0 refit that treats the job's readout calibration as uncertain rather than exact. On h221 and h268, extra readout error (implausibly large here) can stand in for the blur term.

## The case that this result is false

*Written before the checklist.*

"Both present on 3 of 3" is the default outcome of this design, not a discovery. With 36,000 shots per pair, any model short of saturation leaves misfit, and any seven or nine extra knobs that can soak up part of it will be "needed". The bootstrap nulls are drawn from the fitted nested model itself, so they are well specified by construction. They contain none of the real data's misspecification: of ρ_ref (a simulator's state, wrong once already through the T1/T2 bug), of the assignment matrix (treated as exact), or of errors outside both families. So each test asks "does this block of knobs reduce misfit?", and the answer is yes for almost any block. h088 shows it openly: even the full model misfits (deviance 63.3 on 11 df), so there both terms are certainly absorbing something that is neither. The recovery study already showed an out-of-family XX rotation drawing a blur label on h088. The run's own spectator check shows rotations on other qubits being read as "rotation" on h268 in 20 of 20 draws. And symmetric readout error beyond the assignment matrix is mathematically the same as local depolarising on tomography counts, so the "blur" term may be readout. Two more things weaken it. The nested fits may sit in local optima: P3-5's audit found 21-start fits up to 4.1 logL short, and an under-fitted nested model inflates the LR. The weakest label (h221 rotation, LR 38.5 against a null maximum of 22.8) has little room for that. Finally, the author knew the answer before designing the test: the archive had been analysed twice and the auditor had already seen both terms on every pair. The decay-family change (D19) was made with that knowledge, so it is not a blind test. On this reading the result is the design's prior, restated.

The checklist below tests each of these points. Most do not hold up. The local-optimum point fails outright: 60-start refits change nothing. The overdispersion point fails too: all six survive scaling by deviance/df. The fragility point partly holds: two settings carry most of h221's rotation LR. The readout point holds in principle but needs readout drift several times IBM's reported error. The "default outcome" point is answered by the recovery study, where in-family single-kind and "neither" truths were labelled correctly on all three pairs, and by the margins: the observed LRs are 3–25 times their null 99th percentiles.

## Claims checked

| # | claim (quoted or paraphrased) | check run | outcome |
|---|---|---|---|
| 1 | Title: "every pair needs both a rotation-type and a blur-type term" | read against data scope (3 pairs, one job, 3 Nov) and CONTEXT §3 rule 6 | **hole** (scope; cut 1) |
| 2 | Prereg 930efe8 17:31, seed 03356ad, CURBy-RNG 1591496 | `git log --format=%aI`; `seed.py` recompute | holds |
| 3 | Fixes D19–D25 and recovery D26 at 511ea05; review confirmed (709d8c1) | `git show --stat`; DEVIATIONS diff | holds (typed 21:45 vs commit 21:38:51; see E26) |
| 4 | $0, 0 QPU s, archive counts only | code read; scratch run with sockets blocked | holds |
| 5 | P3-5 verdict "fail, odds 0.42" stands | bets.jsonl ng-p3-5 row | holds |
| 6 | Per-pair "both present" sentences are §5's | compared with §5 as amended (D22) | holds, verbatim |
| 7 | h088 misfit sentence; deviance 63.3 on 11 df | JSON gof; repro | holds (63.328) |
| 8 | h088 spectator "invisible" sentence | JSON spectator 0/1/19; repro identical | holds |
| 9 | Overall 3 of 3; not-blind sentence | §5; ledger/audits/ng-p3-5.md C15 (+22, +89, +116 and +65, +124, +49) | holds |
| 10 | All six p = 0.001 at B = 1,000; every LR above its null maximum; Bonferroni 0.0017 met | JSON nulls; LR/max 1.69–15.4 | holds |
| 11 | Misfit rule: only h088 > 24.7; h221 14.0, h268 16.8 | JSON; repro | holds |
| 12 | No setting carries more than half; largest 0.43, YZ rotation h088 | JSON shares; repro 0.4268 | holds, but see 26 |
| 13 | CV positive for both kinds on every pair | JSON; repro (h088 +22.4 / +228.2) | holds (values drift ≤ 0.6, signs unchanged) |
| 14 | Spectator h088 19/20 invisible, h268 20/20 rotation | JSON; repro identical | holds |
| 15 | Primary table: LRs, q99s, p's | JSON; repro (LR diffs ≤ 2e-4) | holds |
| 16 | Fit diagnostics table (deviance, shares, CV, negativity) | JSON; repro | holds (CV drift as in 13) |
| 17 | Secondary 14-knob: same labels; LRs 42.9/183.6/234.0 and 128.8/242.2/68.4 | JSON; repro | holds |
| 18 | P3-5 three-way table, every cell | JSON to 4 dp; repro ≤ 8e-4 | holds |
| 19 | Legacy line reproduces P3-5 to 0.1 | −43.530/−34.876/+63.007 vs results/p3-5-coherent-fits.md −43.5/−34.9/+63.0 | holds |
| 20 | T1/T2 fix moves h088 +5.6, h268 +19.8; reparametrisation changes nothing to 0.001; decay moves only h221 (−2.2) | differences from JSON: +5.553, +19.774; ≤ 0.00023; −2.203 | holds |
| 21 | "each kind is needed given the other on every pair" | design (D22 says "terms") | **hole** (mechanism; cut 2) |
| 22 | Spectator table trace distances 0.009, 0.037; 344 CZ pairs | JSON | holds |
| 23 | Lead: h268 rotation term could partly come from spectators | JSON; hedged, labelled post hoc | holds |
| 24 | Lead: h088 largest misfit, largest blur LR, largest negativity loss (0.109 → 0.062) | JSON: losses 0.034 / 0.047 / 0.025 | holds |
| 25 | Overflow warning printed inside the legacy comparison | scratch repro log | cannot check: my run printed no warning; immaterial (the line reproduces) |
| 26 | (implicit) no label rests on a few settings | auditor leave-one- and leave-two-setting-out | **hole** (missing number; cut 4) |
| 27 | Pre-mortem paragraph: "no steering was hidden" | design nouns (D22) | **hole** (mechanism; cut 3) |
| 28 | Pre-mortem paragraph: rotation LRs beat all nulls "by a factor of 3 to 14" over q99; 16-knob behaves like 14-knob | JSON ratios 2.97 / 10.48 / 13.73; 14-knob 2.75 / 10.48 / 13.45 | holds |

## Checklist

**A1. Pre-registered before data: holds.** 930efe8 author time 2026-11-04T17:31:33-07:00 holds the pre-registration, the code and D10. Its §9 says the archived counts were not yet touched. The seed commit 03356ad follows at 17:32:18. The design review (8f20006, 18:16:57) read archived *circuits* only, not counts. So did the synthetic B100 run (a6ca8a1, 17:56) and the recovery study (511ea05, 21:32), which use synthetic counts on the real reference states. The confirmation is 709d8c1 (21:38:51). The run is stated as 21:47–22:50 and the results commit is 22:51:33. The record has no file timestamps for the run's start (the JSON carries none), so "21:47" is the author's statement. The run is gated in code on the confirmed review and on `check_prereg.py --before-run`, which I re-ran on the clone: L1–L3 and R1–R2 ok, exit 0. Disclosed in the pre-registration: the archive had been analysed by P3-5 and its auditor before this design. That is why the bet is unscored. It is not a pre-registration hole.

**A2. Rule, statistic, seed, budget match: holds.** The primary is "present" iff bootstrap p < 0.01, per pair and per kind (§4 at 930efe8). The model (14 → 16 knobs, D19) and B (100 → adaptive 1,000, D20) changed in DEVIATIONS rows committed at 511ea05 (21:32), before any `--run`, at the design review's request. The seed32 used, 1446222194, is in the output JSON and matches the seed file. Budget: $0 · 0 QPU s · ≤ 3 laptop h, and the stated run time was about 63 min.

**A3. Bar not lowered: holds.** D19 makes the rotation test harder: decay now sits in the null family it must beat. D20 raises B. D21 restates a reason and keeps CV secondary. D22–D25 add sentences and reports. None was written after data. D10's earlier demotion of CV (the P3-5 audit had suggested it as a co-primary) was made before data, from a synthetic run. The review found the stated reason wrong (D21 corrects it). It is moot here, because CV agrees with every label.

**A4. Primary is the pre-registered primary: holds.** The 16-knob primary is reported first and the 14-knob set as secondary, as D19 specifies. The labels are identical in both.

**B5. Ties and floating point: holds.** p counts null LRs ≥ the observed LR. The LRs are continuous, and every observed LR exceeds its null's maximum by a factor of 1.69 to 15.4, so no tie is possible. Floating-point drift between the original run and my reproduction is at most 2e-4 in any LR.

**B6. Pooling: holds.** Nothing is pooled across pairs. Each label is per pair, and the overall reading is a count. The run's only pooled figures are the recovery-study power ranges in the pre-registration, which are reported as ranges across pairs.

**B7. Few items (here: settings) driving it: hole, small (cut 4).** I refit leave-one-setting-out for all 9 settings on all three pairs, warm-started from the archived optima plus 4 random starts (`scripts/reanalyse.py`). Minimum remaining LR, against the 9-setting null q99, as D24 does:
- h221: rotation 19.5 (XZ dropped; q99 13.0), blur 90.3 (q99 9.0);
- h088: rotation 105.7, blur 104.1 (XX dropped);
- h268: rotation 172.7, blur 48.9.

Every label survives every single drop. h221's rotation label is the weak one. XZ (15.5) and XY (11.0) carry 26.5 of its 38.5, which is 69%. I ran all 36 leave-two-out refits on h221 (`scripts/l2o.py`). Dropping XY and XZ together leaves 13.8, just above the 13.0 line. Five of the 36 pairs fall below χ²₇'s 99th point (18.5), and none falls below the null q99. The results file reports only "no setting carries more than half", which is true but hides the fact that two settings carry most of the weakest label. The checklist asks for this "in numbers".

**B8. Circular estimators: holds.** The nulls are parametric bootstraps from the fitted nested model, the standard construction. The spectator draws are classified with the real data's null q99s, which are fixed before the spectator fits. The recovery study's power figures use synthetic nulls. Nothing tested is also used to select its own test.

**B9. Baselines and controls: holds, with a note.** The rival to each term is the nested model with the other term, a matched comparison. The dumbest output, "both present everywhere", is not the design's default: on the three real reference states the recovery study labels blur-only, rotation-only and neither truths correctly (D26, confirmed by the review). Two extra $0 controls I ran:
- *Overdispersion.* Scaling each LR by max(1, deviance/11) (h221 1.27, h088 5.76, h268 1.52) gives χ² p-values of 8e-5 or smaller for all six tests (the largest is h221 rotation, 30.3 on 7 df), all below Bonferroni's 0.0017. h088's misfit does not explain its labels away.
- *Readout model.* I gave every model 4 extra readout knobs (per-qubit e0, e1 ∈ [−0.02, 0.05], applied after A). Rotation survives on all three pairs (20.3, 168.1, 146.0). Blur survives on h088 (38.9) but not on h221 (8.9) or h268 (7.6), which fall below their null q99s of 9.0 and 8.8. The mechanism is exact in principle: symmetric readout error shrinks every measured Pauli expectation the way local depolarising does. But the readout knobs this needs reach 2.7–5% per qubit (several at the bound), on top of an in-job A measured from 4,000 shots per state. IBM's snapshot puts these qubits' readout error at 0.24–0.88%. So the rival needs readout drift 3–20 times the reported size. It is unlikely on this archive, but the design cannot exclude it. It goes to "What would break it next" and `design_review_missed`, not to a cut, because the sentences already say "terms in a 16-knob model …, not identified physical mechanisms".

**B10. Uncertainty: holds.** The tests are per pair, against pair-level nulls. Every p is given with its floor 1/(B+1). No interval is claimed for the LRs. The closest call (h221 rotation, LR 38.5 against a null maximum of 22.8) is not near the edge at B = 1,000.

**B11. Multiple comparisons: holds.** Six primary tests, reported against α = 0.01 and against Bonferroni 0.0017, and all six meet both. The secondary 14-knob tests, CV, spectator and P3-5 lines are reported as secondary.

**B12. Leakage: holds.** No archive count reached a design choice after 930efe8. The review and the recovery study used circuits and synthetic counts only. The prior analyses (P3-5 and its audit) are disclosed in the not-blind sentence.

**C13. Scope drift: hole (cut 1).** The title says "every pair needs both …". The data are three pairs from one job (`dbl6e1d8mdtc73d5gesg`) on one afternoon, and the pre-registration's §6 says so ("three pairs on one afternoon"). The results file never restates that scope. CONTEXT §3 rule 6 rules out "every" or "all" for one set.

**C14. Rank drift: holds.** The spectator, misfit-size and overflow observations are filed under "Noticed after the data; leads, not findings". CV is called secondary.

**C15. Mechanism drift: holes (cuts 2, 3).** D22 replaced "the chip's errors need a steering and a blurring part" with "the counts need a rotation-type term and a blur-type term", because the design cannot tell physical kinds of error apart. The recovery study (decay, an XX rotation), the spectator check and my readout check all show why. Two sentences slip back:
- "each kind is needed given the other on every pair" (P3-5 comparison bullets);
- "For the auditor: no steering was hidden." (pre-mortem paragraph).

The rest of the file keeps to "term".

**C16. Plain English matches the table: holds.** Every number in the plain-English section and the rule bullets is in the JSON (claims 6–14). "Neither alone fits as well" is supported: each nested model is worse than full16 by LR 38.5–242.3.

**C17. Citations: holds.** The P3-5 published values (−43.5, −34.9, +63.0) are in `results/p3-5-coherent-fits.md`. "The auditor … saw both kinds of term on every pair" matches `ledger/audits/ng-p3-5.md` (C15: +22.1, +88.7, +116.1 coherent and +64.8, +123.6, +49.0 incoherent). The design-review fixes and their DEVIATIONS rows are as cited.

**C18. Negative results stated plainly: holds.** The h088 misfit is put in the per-pair sentence. The h268 spectator result, which cuts against the rotation term there, appears in the rules, the table and the leads. The result is reported "beside, never in place of" P3-5's scored fail.

**D19. Budget: holds.** $0 and no network. The code reads local files only, and my scratch run ran with sockets blocked. The ≤ 3 laptop h budget is not enforced in code. The stated run time is 63 min, which I cannot verify beyond the author's statement.

**D20. Stop-on-refusal: n/a.** No model calls.

**D21. Scale direction: n/a.** No graded scale.

**D22. Replication (invariant 7): holds as reported.** The bet is unscored and not called a hit. It is one job and one archive, so after audit it is entered as `pass-unreplicated`.

**E23. Seed: holds where checkable.** CURBY-Q was stalled: §2 records round 28297 at 2025-08-22. CURBy-RNG pulse 1591496 is at 00:32:00.187Z, after the commit at 00:31:33Z. The previous pulse, 1591495 at 00:31:00.197Z, is before it. `ledger/seed.py <randomness> ng-p3-5c --purpose boot` recomputes seed 10131417812182473074 and seed32 1446222194, identically with the engine's copy and the clone's copy. `run()` seeds `SeedSequence` and `default_rng` from that seed32 only. Program 4's ss-b1 row records the same pulse with the same randomness, independently. *Cannot check:* the pulse against the public beacon (no fetch made; `certificate_verified: false`).

**E24. Tiebreak: n/a.**

**E25. Lesson: holds.** The pre-registration (17:31) is after 17:00. The §0 lesson row is in 930efe8, and `ls-ng-p3-5c` has the same sentence (check_prereg L2 ok). Its read block (9 resolved, Brier 0.236, base rate 0.27, newest audit ng-p3-5.md) matches the ledger at 930efe8. I recomputed 9 scored bets with 2 hits and Brier 0.2357. The read_note discloses that the ledger was read once at about 17:05 and not re-read before the commit. The cited patterns' `do_this` are in the design. P4: manipulations dry-run (T1/T2 asserted in code, checked in review D2). P5: rivals checked on synthetic data (nesting plus the D26 recovery on the real reference states). No odds, so no odds revision.

**E26. Design review: holds.** `ledger/design-reviews/ng-p3-5c.md`, verdict fix-first (8f20006, 18:16:57), after the pre-registration and before the run. Every fix is in a DEVIATIONS row (D19–D26, 511ea05, 21:32) dated before data, and the confirmation addendum is 709d8c1 (21:38:51). One record discrepancy: the addendum's typed `confirmed_at: 21:45` is six minutes after its own commit, and the results file and bet row copy 21:45. Either time is before the stated 21:47 run start. Missed by D1–D10 (header `design_review_missed`):
- D9: the two-setting fragility on h221 passes the one-setting rule that F6 wrote.
- D4: the blur family is confounded with readout error beyond A. It is unlikely here but not excluded by the design.

**Reproduction (how it was run).** The audit copy is at `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/19f84df9-a6ff-48ba-89d6-d3f43e5d1747/scratchpad/audit-ng-p3-5c/copy`. The environment is a fresh venv with the review's pins (qiskit 2.6.1, qiskit-aer 0.18.2, qiskit-ibm-runtime 0.51.0, numpy 2.5.4, scipy 1.18.1). The old checkout's venv and `.env` were not used. `scripts/repro.py` runs `p3_5c_fits.run()` unchanged, with two substitutions:
- `check_prereg` is faked, because the copy has no git; I ran it on the clone separately.
- `bootstrap()` recomputes 10 null draws per test by exact seed index (indices 0–4 and 100–104; 120 draws in all) and returns p and q99 from the archived 1,000-draw nulls against the recomputed observed LR.

The main random stream is untouched, so the point fits, CV, secondary set, P3-5 lines and 40 spectator draws are rerun exactly.

Results:
- h221 is bit-exact, including all 40 recomputed null draws.
- From h088 on, a drift of about 1e-4 logL appears (it starts in the h088 reference state or fit). It moves the LRs by at most 2e-4, null draws by a median of 2e-5 (max 0.87), and CV by up to 0.57.
- Every label, p, spectator count and displayed table value regenerates, except the h088/h268 CV column (claim 13).

Other scripts:
- `scripts/reanalyse.py`: 60-start refits, leave-one-setting-out, readout knobs.
- `scripts/l2o.py`: leave-two-out on h221.
- `scripts/tail.py`: the largest null draws refit with 40 starts.

## The pre-mortem, scored

*My line first (header `failure_reason`):* none. The bet did not fail: its reading is "both present" on every pair, and it survives re-analysis. Had it failed, my most likely reason is h221's rotation label dropping under the line after a small change to the blur side of the model, kind design. *Disclosure:* the pre-mortem sits in the pre-registration's §0 table and is quoted in the results file, so I saw it (in a grep for the section) before the checklist and before writing this line.

The pre-mortem: "If this fails, the most likely reason is that the 14-knob fits land in different local optima across bootstrap samples, widening the null and hiding steering that the point fit shows, as in the synthetic 'both' case." Kind `design`.

**Score: not_failed, risk_seen: false.** The named mechanism did not appear. The three largest h221 rotation null draws (22.84, 18.26, 17.68) are real optima: refit from 40 starts, they move by at most 0.02. The observed nested fits are at their 60-start optima (gains ≤ 0.003; full16 on h088 +0.056). The rotation nulls' 99th percentiles (13.0–17.5) are below χ²₇'s 18.5, so the nulls are not widened.

## Required cuts

1. **Title.** "P3-5c result: every pair needs both a rotation-type and a blur-type term (not scored)" → "P3-5c result: on all three archived pairs (one job, 3 November), the 16-knob model needs both a rotation-type and a blur-type term (not scored)".
2. **P3-5 comparison, last bullet.** "The nested tests above say why that contest was the wrong question: each kind is needed given the other on every pair." → "The nested tests above say why that contest was the wrong question: in the 16-knob model, each term is needed given the other on all three pairs."
3. **Pre-mortem paragraph.** "For the auditor: no steering was hidden." → "For the auditor: no rotation-type term was hidden."
4. **Rule bullets, one-setting rule.** After "…so no "rests mostly on setting" sentence and no drop-one refit.", add: "The weakest label is rotation on h221: two settings, XZ (15.5) and XY (11.0), carry 69% of its LR of 38.5. In the auditor's post-hoc refits, dropping XZ alone leaves 19.5 and dropping both leaves 13.8, against that null's 99th percentile of 13.0. The label survives every single and paired drop, but narrowly."

*Recommended, not required:* in the leads, add "On h221 and h268, a rotation model with four extra readout knobs makes the blur term unnecessary (LR 8.9 and 7.6). This needs 2.7–5% extra readout error per qubit, several times IBM's reported 0.2–0.9%, so it is unlikely here, but this design cannot exclude it (auditor, post hoc)." Also note the review's typed `confirmed_at` (21:45) against its commit (21:38:51).

## What would break it next

The cheapest test that could overturn part of the reading costs $0 and about 1–2 laptop hours. Treat the assignment matrix as uncertain instead of exact. Put the 4 readout knobs into all three models, with a prior or bounds set by A's own in-job sampling error (4,000 shots per calibration state) and by IBM's reported readout error. Then rerun the parametric bootstrap for the blur test on h221 and h268. Two outcomes are possible:
- If readout drift of a few per cent can be argued plausible, those two blur labels would not stand on the archive alone.
- If the bounds that A's sampling error allows (about ±0.5%) leave LR_i above its new null, the blur labels are secured against readout.

A hardware answer needs an interleaved readout calibration in a new job, which is a separate bet. The device-level twirling and dynamical-decoupling direction (P3-2) is already on the map.
