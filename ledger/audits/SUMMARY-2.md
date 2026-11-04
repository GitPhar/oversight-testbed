# Independent audit, round 2: summary

Branch `audit2`, 2026-11-04, from 14:32 America/Denver. The standard is `oversight-testbed/operators/auditor.md` (as amended at 14:39–14:44 with plants, pre-mortems and E23–E24) and the house style of `audits/SUMMARY.md`.

Scope: every result committed today that had no audit, or whose text changed after the first audit (`b009a15`, 10:27). That covers the D51 cut pass and the D52/D53 corrections. Also in scope: each program 2 (`other-minds`) and program 3 (`nature-graded`) result committed between 14:32 and 16:32, and the probe rerun on `probes`. Those folders were polled every 20 minutes or less.

No API calls were made. Everything was recomputed from archived JSON, and no local model was run. Nothing outside `audits/` was changed.

The auditor model and the author model are both Claude Opus 5.5 (commit trailers), so **every audit here is same-family**.

## In plain English

**The numbers hold again.** Every headline statistic in the thirteen audit files was recomputed from the archive. Every table that has a generator regenerates, byte for byte where checked. No arithmetic error changes a verdict.

**Three labels do not survive as written:**

1. **Experiment 5's re-issue, TIE → CLASSICAL (D52).** It applied the frozen rule to a subset the pre-registration did not choose (anchor a only).
   - The pre-registration pools the two scale directions on purpose: "after anchor recoding", with anchor reversal named as the control for scale artefacts (§8 item 4 of `2c2ef6c`).
   - The two directions depart from QQ with opposite signs (−0.345 and +0.241), the pattern a direction-dependent response artefact would also produce.
   - The only pre-registered single-direction QQ data (run 2) do not meet the contradiction condition.
   - So the pre-registered verdict is still TIE, and CLASSICAL is a post-hoc reading; between them it is unsettled. The first audit pushed for this re-issue without quoting §8, so part of this is the first audit's own error.

2. **Opus's "a usable single belief" (D49), and the paper's "On Opus there is a credence to read" (D50).** The F′ label is robust to folds, items and claim set. But a one-bit predictor ("is the 0–100 rating above 50?") reaches Q = 0.88 [0.81, 0.93] on Opus, also above the 0.75 bar.
   - Opus answers yes/no unanimously over 10 repeats on 91% of statements.
   - So the test shows the six formats share a format-free **verdict**. It does not show a graded **credence** beyond it, which adds about 0.06 of Q.
   - The label stands as "pass, unreplicated"; the word "credence" does not.

3. **Program 2's only pass, om-p2-4 ("self-prediction not detectably better than predicting Sam"), is a non-detection written as a pass.**
   - The frozen rule is "CI of ΔMAE not wholly below 0", with no equivalence margin and no power check. The program's own map requires one for every self/other null.
   - The bootstrap SD of ΔMAE is 0.030, so the minimum detectable effect is about 0.084: 87% of Sam's whole error. The observed self advantage (self error 56% of Sam's) could not have been detected.
   - The pre-registered percentile interval [−0.074, +0.043] is biased toward 0 by the absolute value in MAE. Basic and BCa intervals are [−0.129, −0.012] and [−0.105, −0.004], and both favour self.
   - The rule's letter is met. Its claim, "knows itself about as well as Sam", is not shown, so the audit reads **undetermined**.

**The rest stands, with cuts:**
- **The probe study is verified on its rating side (DP2).** Fresh seeds replicate DP1's label, and the replay hole is closed. But the probe side is a near-replay by construction (r ≥ 0.994 with DP1), and "not with the rating" is again decided by one item, h191.
- **Program 2's first result (om-p2-1) stands as "fail".** "How likely" and "how confident are you" are not interchangeable on Haiku (Q 0.77 [0.65, 0.88] against a 0.90 bar). The gap sits in a minority of claims, so "reorders the statements" overstates it.
- **Program 2's second result (om-p2-2) stands as "fail", but its explanation does not.** The pooled Q (0.50) is almost entirely the condition label: a predictor that knows only whether Noor saw the change gets 0.477. The fail is driven by true-belief stories, not false-belief ones. The exploratory "cause-only perception" excuse is contradicted by its own items, and the "+9-point curse of knowledge" has a median of +5 and rests largely on two stories.
- **Program 2's third bet (om-p2-3) is untestable, as its pre-mortem predicted.** A refusal on a severity-3 story stopped it after 26 calls ($0.001). The stop rule held, and the beacon seed recomputes.
- **Calibration under format stands as "mixed".** Sonnet's format effect survives every binning and matching check. Its *sign* depends on how a "no" plus a number is read. Sonnet's conversation-vs-fresh effect disappears on matched questions.
- **Multi-model stands as "mixed".** One item, h058, decides 3 of the 5 per-model DM4/DM2 labels. The six-format table in `multi-model.md` is stale against its own cited source.

**How the cut pass did.** D51 applied the first audit's cuts faithfully: in the files re-audited here, 0 of 34 listed cuts were missed or applied wrongly. But it acted only on *listed* cuts. Holes the first audit found without writing a replacement sentence stayed open (h058's label flip, the Holm-corrected probe gate, Sonnet's format-dependent max_tokens stops, the DM "Date" fields). In two places the cut pass's own new wording overclaims again (calibration `:43`).

**Program 3's later results.**
- **ng-p3-5 ("fail, incoherent better")** stands as a count. But the families were not matched: the coherent family cannot change purity, so on h221 no coherent model could have won. A joint fit finds coherent terms on every pair, so "not steering" is contradicted.
- **ng-p3-2 and ng-p3-3** are both untestable, by pre-registered gates that held: today's chip matched the simulator in P(yes) (gap 0.023 [0.004, 0.042]). The headline "0.502 → 0.246" compares a circuit with a barrier, run as one 1,000-shot block on Nov 3, with one without it, interleaved in 100-shot instances today, so "one unusual afternoon" is not shown. The T1/T2 bug does not reach these predictions.

**Program 3's first result (ng-p3-1) stands as "fail", but it ran a different model from the one described.**
- The code meant to load the job-time T1/T2 never did: `Target.qubit_properties` returns a fresh list in qiskit 2.6.1, so the assignment is discarded. The run used FakeFez's 2025 values (q117 T1 177.1 µs against the snapshot's 87.6).
- E2's ZZ error was never applied: counts are identical at 0, 0.1 and 1.0 rad.
- E3's "÷3" did nothing. Corrected, it gives 0.288, not 0.277.
- With T1/T2 set properly the verdict is unchanged (control 0.2679, scheduled 0.2678).
- The control band cannot tell a noiseless simulator (0.279) from the noisy rebuild.
- "Idle decay closes 7%" is about 95% the rebuild-versus-archive gap. Scheduling alone closes 0.3%, and over 10 seeds scheduled − control is −0.0002 (SD 0.001).
- The pre-registered consequence, adopting this model as the "corrected simulator" for later program-3 predictions, should be **held until the T1/T2 bug is fixed**.

## Headline rates

| measure | value |
|---|---|
| audits written | 13 files covering 14 results (11 new results, with ng-p3-2 and ng-p3-3 in one file; 3 second-round re-audits) |
| claims checked / holes / cuts required | 344 / 98 / 133 |
| results that regenerate from the archive | 13 / 13 (om-p2-3 has no statistic; its archive checks out) |
| verdict changed by the audit | **3 / 13**: om-p2-4 (pass → undetermined: a non-detection with minimum detectable effect 87% of the comparison's error, and bias-corrected intervals favour the self arm); exp5 re-issue (classical → mixed: tie pre-registered, classical post hoc); probe DP1 round 2 (unverified at audit time → untestable, then resolved by DP2) |
| label stands but its wording does not | 2 / 13: ng-p3-5 ("incoherent better" stands as the rule's count; "blur, not steering" is contradicted);  Opus D49 (pass → pass-unreplicated; "credence" cut) |
| verdict stands | 8 / 13 |
| round-1 cuts in re-audited files: applied as written / adapted / obsolete / missed or wrong | 18 / 14 / 2 / **0** (multi-model 25, calibration 6, probe 3) |
| round-1 holes with no listed cut, still open | 9 (3 each in multi-model, calibration, probe) |

## Per-audit table

| audit | result | claimed → after | claims / holes / cuts | most serious finding |
|---|---|---|---|---|
| [`mm-gm3b-opus-completion.md`](mm-gm3b-opus-completion.md) | D49, D49a, D50 | pass → **pass-unreplicated** | 24 / 6 / 13 | a one-bit verdict predictor passes the same F′ bar (Q 0.88 [0.81, 0.93] vs 0.94); "credence to read" unsupported; yes/no is 84%, not 82%; title says 80 claims (68); actual spend $6.04, not $5.78 |
| [`exp5-verdict-reissue.md`](exp5-verdict-reissue.md) | D52 | classical → **mixed** | 11 / 3 / 7 | post-hoc subset reverses the pre-registration's own artefact control; opposite-signed per-direction q; run 2 (pre-registered, one direction) not contradicted; verdict basis is a hard-coded constant |
| [`probe-dissociation-r2.md`](probe-dissociation-r2.md) | DP1 after D51/D53 | mixed → **untestable** (until DP2) | 14 / 4 / 4 | `:116` contradicts `:85` (order moves the probe *half* as far as testimony, not more); Holm gate, alternative Q scalings and items-fixed r still missing |
| [`probe-dissociation-dp2.md`](probe-dissociation-dp2.md) | DP2 (`probes`, 3fa5832) | mixed → mixed | 18 / 2 / 3 | verified on the rating side only; h191 decides "not with" on both draws; "strongest evidence" for a CI reaching +0.06 |
| [`om-p2-1.md`](om-p2-1.md) | program 2 bet 1 (`other-minds`, 5931024) | fail → fail | 24 / 7 / 4 | 7 of 160 claims carry the gap (without them Q 0.90); "Sam is not further than 'how likely'" contradicted by point estimates; "names the self" confounds verb with subject; prereg says frozen 14:45, commit 14:35:02 |
| [`om-p2-2.md`](om-p2-2.md) | program 2 bet 2 (`other-minds`, df4adee) | fail → fail | 34 / 11 / 13 | pooled Q 0.499 is ~all between-condition (label-only predictor 0.477; condition-centred 0.076); fail is TB-driven (TB made perfect → 0.856, FB made perfect → 0.627); "cause-only perception" excuse contradicted (25 of 48 high TB items name the outcome); curse of knowledge +9.2 has median +5.0, two items carry 40% |
| [`om-p2-4.md`](om-p2-4.md) | program 2 bet 4 (`other-minds`, b271227) | pass (unreplicated) → **undetermined** | 26 / 9 / 14 | non-detection rule with no margin; minimum detectable effect 0.084 against Sam's MAE 0.097; percentile CI biased toward 0 (32% of resamples below the point); basic/BCa CIs exclude 0 for self; a predictor ignoring uptake passes the gate and the r ≥ 0.70 bar |
| [`om-p2-3.md`](om-p2-3.md) | program 2 bet 3 (`other-minds`, 5141ca7/f46f8e3) | untestable → untestable | 12 / 2 / 2 | stopped on a refusal at the 22nd step-1 call (severity-3 explosives story), 26 calls, $0.001; 5 in-flight later-wave calls kept but not mentioned; pre-mortem named it (`named`); a foreseen refusal risk (552 of 1,147 stories severity 3) was accepted without a pilot |
| [`calibration-under-format-r2.md`](calibration-under-format-r2.md) | DM6, DM6a after D51 | mixed → mixed | 34 / 11 / 14 | Sonnet conversation-vs-fresh −0.107 → +0.011 on matched questions; "for Haiku, on the context only" and "factor of 1.7 to 2.9" hold under one scoring only; format-dependent exclusions still unreported |
| [`multi-model-r2.md`](multi-model-r2.md) | DM2–DM5 after D51 | mixed → mixed | 54 / 16 / 18 | h058 decides 3 of 5 labels (Sonnet gate p 0.031 → 0.111 without it; Opus → self-anchoring); Opus gate rests on h279 and h238; six-format table stale vs `mm-gm3b-format-invariance.md`; "all calls through the Batches API" false (12 synchronous pilot calls) |
| [`ng-p3-5.md`](ng-p3-5.md) | program 3 bet 5 (`nature-graded`, 9e9ae5d) | fail, incoherent better → same | 27 / 8 / 11 | families not matched: the coherent family is unitary on ρ_ref, so it keeps purity 0.984 while the chip's state is 0.908; even a full SU(4) loses to the incoherent fit by 40.3 on h221; a joint model finds coherent terms on every pair (+22 to +116 logL), contradicting "not steering"; h088's label is two settings deep (XX alone −45.5 of −34.9) |
| [`ng-p3-2-3.md`](ng-p3-2-3.md) | program 3 bets 2 and 3, one job (`nature-graded`, 6badd68) | untestable, untestable → same | 34 / 10 / 15 | the T1/T2 bug does not reach these predictions (live backend; rebuilt S matches to 5 decimals); "0.502 → 0.246" compares different circuits (Nov 3 had a barrier; arm A today has none) and job layouts, so "one afternoon" is unsupported; P(yes) agrees but 5 of 9 qubits are \|z\| > 4 off the simulator; twirl claims rest on about 2σ |
| [`ng-p3-1.md`](ng-p3-1.md) | program 3 bet 1 (`nature-graded`, 280e180) | fail → fail | 32 / 9 / 15 | job-time T1/T2 never loaded (qiskit `qubit_properties` copy), so E3 ÷3 was a no-op; E2 ZZ never applied (identical counts); noiseless sim 0.279 passes the control band; "7%" is mostly rebuild-vs-archive gap; "eight of nine drop 0.12–0.45" is seven |

## What the lead auditor re-verified

These are the subagent findings with the power to change a verdict or a headline, each re-run by the lead auditor:
- calibration: Sonnet format −0.143 [−0.233, −0.066]; matched −0.119 [−0.205, −0.032]; Sonnet conversation-vs-fresh −0.107 [−0.181, −0.030], matched +0.011 [−0.116, +0.096];
- multi-model: the DM4 leave-one-item-out (Sonnet without h058 → gate p 0.111; Opus without h238 → 0.103; Opus without h058 → R 0.14 [0.00, 0.46], self-anchoring);
- om-p2-1: Q = 0.772, and 0.902 without the 7 largest movers; 18 claims move by more than 30 points;
- ng-p3-2/3: `predict()` uses `p3sim.simulator(live_backend())` and never calls `overwrite_calibration`; Nov 3 transpiled ops include `barrier: 1`, and today's arm A has none (`ng-p3-23/work/scripts/circuits_check.py`, re-run);
- ng-p3-5: the coherent family is local unitaries + ZZ on ρ_ref (`p3_5_fits.py:59`), so purity stays 0.9842 against the incoherent fit's 0.8972; SU(4) best −39236.37 against incoherent −39196.05 on h221 (`ng-p3-5/work/a1_multistart.json`);
- om-p2-4: ΔMAE −0.0430; percentile CI [−0.0739, +0.0425] (seed 2905035151); basic [−0.1286, −0.0121]; BCa [−0.1051, −0.0036]; bootstrap SD 0.030; share of resamples below the point 0.304 (`om-p2-4/work/indep.py`, re-run, output identical);
- ng-p3-1: T1/T2 unchanged after `overwrite_calibration` (and after scale=3) on all 9 qubits; E2 counts identical at ZZ 0, 0.1 and 1.0 rad; noiseless p_yes 0.2787, inside [0.221, 0.281]; corrected control 0.2679 and scheduled 0.2678 (`ng-p3-1/work/scripts/`);
- om-p2-2: pooled Q 0.499, condition-label-only Q 0.477; TB-perfect 0.856 and FB-perfect 0.627; cause-split counts 25/15/8 with Q 0.548 (drop cause-only) and 0.624 (drop outcome-named); curse of knowledge +9.20, median 5.0, 5.64 without templates 67 and 39.

One caveat on the last of these. Dropping the claims with the largest differences raises Q in any noisy comparison, so "7 claims carry the gap" describes where the gap sits, not how robust it is. The label-swap null in `om-p2-1.md` (Q 0.987 [0.955, 1.015]; 0 of 2,000 swaps reach 0.772) is the robustness check, and it holds.

## Cross-cutting findings

1. **Rule-faithful labels with the wrong noun, and non-detection rules called passes.** om-p2-4 is round 1's "nulls written as findings" pattern built into a pre-registered rule.
    D49 ("credence"), DP1/DP2 ("not with the rating") and om-p2-1 ("names the self") all apply a frozen rule correctly, then describe the outcome with a word the design cannot carry. This is round 1's "mechanism words" pattern again. It survived the cut pass because the new sentences were written after it.
2. **Missing dumb baselines, weak controls and unmatched rivals.** ng-p3-1's control passes a noiseless simulator, and ng-p3-5's coherent family could not change purity, so the contest was partly decided by construction. Neither F′ (D46, D49) nor the multi-model replications pre-registered a constant or one-bit baseline. On near-deterministic models a one-bit baseline nearly ties. om-p2-2 is the same case: its pooled Q is 0.499, and the condition label alone gives 0.477. Any future "one belief" test should pre-register Q_model − Q_baseline.
3. **Labels that hang on one item.** Round 1 named h058 and h191. Round 2 finds them still deciding labels, now on fresh data too (h191 in DP2; h058 in DM2/DM4). The records name them. The headlines do not.
4. **Post-hoc corrections need the same discipline as results.** D52 re-labelled a verdict on a subset chosen after the data, prompted by an audit. An audit-prompted re-analysis is still a re-analysis. It should be reported beside the pre-registered verdict, never in place of it.
5. **Stale cross-references.** These lag: `multi-model.md`'s six-format row (26 claims), the probe banner and README ("queued", while DP2 ran and reported), and "unverified" on main (DP2 is on unmerged `probes`). Each is correct for its moment and wrong now.
6. **Record times.** These disagree with their own commits: om-p2-1's "frozen 14:45" (the commit is 14:35:02), the DM "Date" fields (6–51 min after their commits, from round 1, still uncorrected), DP2's DEVIATIONS row (no time at all), and a shell-expanded "/bin/zsh.0012" in D49a.

## What the owning sessions should do first

1. Replace CLASSICAL with "tie (pre-registered); classical on a post-hoc single-direction re-analysis; unsettled" in README:161, record:89, the-entangled-mind-paper:19 and v3:67/614 (`exp5-verdict-reissue.md`, Required cuts).
2. Cut "credence to read" for Opus in `paper/no-credence-to-read.md:332`/`:358`, and add the one-bit baseline to every Opus F′ sentence (`mm-gm3b-opus-completion.md`).
3. `results/probe-dissociation.md:116` (contradicts its own `:85`); on merging `probes`, replace "unverified … queued" with DP2's outcome and its two caveats.
4. `results/multi-model.md`: the h058/h238 dependence, the stale six-format row, the Batches API sentence.
5. `results/calibration-under-format.md:43` and `:155` (the cut pass's own wording).
6. `nature-graded`: fix `p3sim.overwrite_calibration` (assign a new `qubit_properties` list, or build the noise model from explicit T1/T2), re-run ng-p3-1's control, scheduled run and E2/E3 under a DEVIATIONS row, and hold the "corrected simulator" adoption until then.
7. `other-minds`: om-p2-4's pass should read "not detected; the test could not detect an advantage smaller than 0.084". Any future self/other null needs a pre-registered equivalence margin and power check, as the program map already requires. Then om-p2-1's four sentences, and a DEVIATIONS row for the 14:45/14:35 freeze-time error. om-p2-2's 13 cuts, first the bold "part of this failure is the design's" and the curse-of-knowledge headline.

## How this round was done, and its limits

- **Who did what.**
  - The lead auditor wrote the D49, D52, DP1-r2 and DP2 audits and this summary.
  - Eight subagents with written briefs wrote multi-model-r2, calibration-r2, om-p2-1, om-p2-2, om-p2-4, ng-p3-1, ng-p3-2-3 and ng-p3-5. The lead auditor wrote om-p2-3. Each was told what to attack, not what to find.
  - The lead auditor re-ran their verdict-relevant checks (above).
- **Polling.** `nature-graded`, `other-minds` (all branches) and `entangled-mind`'s `probes` branch were checked for commits touching `results/` at 14:35, 14:50, 15:00, and every 20 minutes after, through 16:32.
- **Not recomputed or not checkable:**
  - no model (API or local) was re-run;
  - DP2's 12-conversation environment check, h093's unbilled cancellation, Smolin & Wilder's numbers (no network);
  - commit times against an independent clock where no request IDs exist (DP1, DP2).
- **Same-family bias.** The author and every auditor are Claude Opus 5.5. The auditor standard asks for a different model where possible; none was available in this session.
- **Scripts.** Recomputation scripts are in the session scratchpad (`d49/`, `d52/`, `dp2/`, `mm/`, `cal/`, `om-p2-1/work/`), not in the repository.
