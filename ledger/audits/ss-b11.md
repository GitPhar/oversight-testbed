---
bet: ss-b11
program: settled-science
prereg_commit: 3fd6037
results_commit: b6a45b2
auditor_session: fresh auditor subagent in the audit clone /Users/seanpharris/oversight-testbed-audit-ss-b11; launched by the engine session (its scratch path is the same session's as the ss-b11 design review's); no chat or transcript read
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true          # author, design reviewer and auditor are all claude-opus-5-5
date: 2026-11-05 07:09 America/Denver
claims_checked: 16
holes_found: 5
overclaims_cut: 4
reproduced: true
verdict_claimed: pass-unreplicated
verdict_after_audit: pass-unreplicated
verdict_stands: true
canary: unknown
false_alarms: 0
design_review_missed: []
failed: false
failure_reason: none; the bet passed as pre-registered (the pre-registered rule's in-sample Brier 0.223 never came near the bettor's 0.163)
failure_kind: null
premortem_score: not_failed
risk_seen: false
---

# Audit of ss-b11: does the round-1 bettor beat a rule that knows each field's habits?

## In plain English

The result stands as **pass, unreplicated**. The scorer rebuilt every table byte for byte. The pass does not depend on the shrinkage weight: weights from 0 to a million all pass, in-sample and leave-one-out. It also survives a paper-level bootstrap, every single-field drop and every single-item drop. But the test shows less than the plain-English section says. The four fields barely differ on these items. The rule fits no better with the real field labels than with shuffled ones, so what the model beat is in effect a pair of pooled rates, not "field habits". On the 38 good-news-tagged items alone, the model's margin is not shown. Four sentences have to change. One brings back the "good news" wording that D55 removed. One calls the leave-one-out rule "without the unfair advantage" when it is a handicap. One says "clearly". One leaves out that the honest four-cluster interval includes zero. The result would break against a finer answer-free rule fitted on these items: a field-by-up-word rule fitted in-sample already gives a null. That rule only overfits (shuffling its words fits about as well), so it does not reverse this verdict. But it shows the in-sample bar mostly rewards the number of fitted cells.

## The case that this result is false

*(Written before the checklist.)* The headline is that the model's edge is "more than knowing which fields usually report good news, or which way results in a field tend to go". That claim needs a rule that actually knows field habits. Here the rule has four fields of about 29 items, split into two classes. The good-news part covers only 38 items (4 of them in model psychology), and the "higher / more" part covers 74. If the fields do not differ, the rule cannot carry field knowledge at all. Beating it then shows nothing about field habits: it shows the model beats pooled rates, which ss-b2 and the ss-b1 audit already showed (0.232, 0.233). Worse, the outcome was nearly known before scoring. The engine already had the bettor's 0.163, ss-b2's margin of 0.068 and the ss-b1 audit's leave-one-out cousins of this rule (0.233 to 0.263). The design review put P(pass) at 0.80–0.94. So a "pass" was bought largely from published numbers.

The in-sample bar, sold as "unfair to the bettor", is also arbitrary. Its strength is set by how many cells the rule fits, not by any field knowledge. Fit enough cells in-sample and any rule reaches the bettor, so the pass could flip on the choice of cells. The margin's shape points the same way. Model psychology goes the rule's way, and two of the four fields carry most of the edge. Leave out two fields and the bound crosses zero in half the pairs. Clustering by field, with an honest t multiplier on four clusters, gives an interval that includes zero. On this view the honest reading is "the bettor beats pooled base rates on 116 items, again". The write-up's "more than field habits" is decoration on a re-run of ss-b2.

## Claims checked

| # | claim (quoted or paraphrased from the results file) | check run | outcome |
|---|---|---|---|
| 1 | bettor Brier 0.163 [0.139, 0.190] | `score_f3.py` rerun; `reproduce.py` | holds (byte for byte) |
| 2 | field-aware rule Brier 0.223 [0.199, 0.248] | same | holds |
| 3 | d = −0.059 [−0.093, −0.024], pass | same; own recomputation −0.0592 [−0.0934, −0.0240] | holds |
| 4 | leave-one-out rates: −0.085 [−0.123, −0.048] | same | number holds; its description in plain English is a hole (cut 2) |
| 5 | field jackknife −0.059 [−0.110, −0.008] | own jackknife: SE 0.0262; ±1.96 gives the same | number holds; with t(3) it is [−0.142, +0.024] (cut 4) |
| 6 | composition 38 / 74 / 4 | recount by class | holds |
| 7 | by-field table (rates, Briers, differences) | recomputed; weighted sum of the field differences = −0.0591 | holds |
| 8 | leave-one-field-out: all four pass | rerun | holds |
| 9 | "Leave-one-item-out flips: 0" | rerun | holds |
| 10 | "No single finding and no single field changes that" | rows 8 and 9 | holds |
| 11 | "In model psychology the shortcut did slightly better (0.223 against 0.235)" | field table | holds |
| 12 | "the model's edge … is more than knowing which fields usually report good news, or which way results in a field tend to go" | tagged-class split; field-label shuffle | hole (cut 1): tagged-only margin −0.053 [−0.117, +0.008]; the real fields fit worse than shuffled ones in 69% of 2,000 shuffles |
| 13 | "The model still clearly beat it" | t(3) field interval; dropping the most favourable items | hole (cut 3) |
| 14 | prior work: 0.263, 0.241, 0.233, bettor −0.070 [−0.104, −0.035] (ss-b1 audit, item 9) | opened `ledger/audits/ss-b1.md` lines 120–125 | holds |
| 15 | "design review put the chance of a pass at about 80–94%"; odds 0.70 → 0.85 (D55); Sean 0.65 | design review D11; D55; `ledger/bets.jsonl` (0.85, first 0.50, lesson 0.70, review 0.85; human 0.65) | holds |
| 16 | 4 items at 0.5, with "raised/lowered" not on the list | listed: ss-002 and ss-049 (raised/lowered), ss-006 and ss-043 (earlier/later) | holds |

## Checklist

**A. Pre-registration**

1. **Holds.** All times below are author times from `git log --format=%aI`.
   - The scorer `score_f3.py` was committed at 26fc1c8 (06:40:55), before the pre-registration 3fd6037 (06:41:05).
   - The design review 1422610 (06:54:52) came next. The fixes 386d462 (06:56:02), 05e13e6 (06:56:08) and 5ee223a (06:56:36) followed, and the confirmation e19586f at 06:57:54.
   - The results file states the archive checks ran at 06:58:31. The results commit b6a45b2 has author time 07:00:27; its committer time, 07:02:40, is the clone's.
   - `f3-scores.json` first appears in b6a45b2.
   - The archive was last changed at 230cbe4 (2026-11-04T18:59:54), and `shasum -a 256 -c items/SHA256SUMS` passes.
   - Caveat, disclosed in the results file: the archive had already been scored for ss-b1 to ss-b3 and by the ss-b1 audit. The author knew the bettor's 0.163 when pre-registering, since the pre-mortem quotes it. "Before the archive is opened for this analysis" is true only in that narrow sense.
2. **Holds.** `git diff 3fd6037 HEAD -- scoring/score_f3.py` changes only `sentence()`, the checksum stop and the untestable guard. The rule, `SHRINK = 4`, the bootstrap (10,000 resamples, `default_rng(20261104)`, the bound indices), `EPS` and the pass test are unchanged. The sentence changes are D55, dated 06:56, before scoring.
3. **Holds.** The bar is unchanged. Odds rose from 0.70 to 0.85 before data, with every number kept.
4. **Holds.** The headline is the pre-registered d.

**B. Is the number real?**

5. **Holds.** There are no ties to break. Brier is continuous, the bettor gave 50 on 1 item, and the rule sits at exactly 0.5 on 4 items, by design. The bootstrap bound indices match §4.
6. **Holds, with a finding.** The primary pools two rule components. Unpooled:

   | class | n | bettor | rule | d [95% CI] |
   |---|---|---|---|---|
   | tagged (headline rate) | 38 | 0.134 | 0.187 | −0.053 [−0.117, +0.008] |
   | untagged with an up option | 74 | 0.183 | 0.239 | −0.057 [−0.099, −0.012] |
   | at 0.5 | 4 | 0.085 | 0.250 | −0.165 |

   The up-option class passes on its own, so the pool is not an artefact. The good-news class alone does not pass, though. This matters for the "good news" wording (cut 1).
7. **Holds; concentration stated in numbers.**
   - Leave-one-item-out: 0 flips. Leave-one-field-out: all pass. The paper-level cluster bootstrap (108 papers, 8 of them with two items) gives [−0.094, −0.024].
   - Leaving out two fields at once, my own check, not pre-registered and at n of about 58: three of the six pairs lose the pass. Without interpretability and scalable oversight, d is −0.020 [−0.072, +0.034]. Without interpretability and quantum devices, −0.039 [−0.093, +0.015]. Without quantum devices and scalable oversight, −0.047 [−0.101, +0.008].
   - Dropping the 10 items most favourable to the bettor, with the rule not refitted, takes the upper bound to +0.004. Dropping 5 leaves it at −0.009. The edge is broad-based but modest.
8. **Holds.** The rule is fitted on the labels on purpose, which favours the rule. The bettor fits nothing.
9. **Holds, with a finding about what the rule is.** All my re-analyses are $0, scratch only.
   - **Other shrinkage weights.** Every weight passes. In-sample, d runs from −0.059 to −0.066 for weights 0, 0.5, 1, 2, 4, 8, 16, 64 and 10⁶. Leave-one-out, it runs from −0.074 to −0.092. Weight 0, the rule's most overfitted form, gives −0.0588 [−0.0944, −0.0230].
   - **The fields carry no signal.** I shuffled the field labels across items 2,000 times, refitting the rule each time. The shuffled rule's Brier averaged 0.2188 (SD 0.0061), against the real fields' 0.2225: 69% of shuffles fit as well or better. The pooled-only rule (weight 10⁶) scores 0.2298 in-sample. So the field split buys 0.007 of in-sample fit, less than random splits buy, and out of sample it loses: leave-one-out 0.249 against pooled leave-one-out 0.238, and against ss-b2's flat 0.232. The "field-aware rule" is pooled rates plus overfitting. This matches the design review's estimate that the field spread τ is small.
   - **Finer answer-free rules** (fitted in-sample / leave-one-out):
     - field × tag × whether the headline side is the up option: 0.216 / 0.247, d −0.053 [−0.086, −0.019], pass;
     - the up-rate first, the headline only where there is no up option: 0.241 / 0.259, pass;
     - field × the up word itself (24 cells, 11 of them singletons): **0.194 in-sample, d −0.031 [−0.067, +0.006], null**; leave-one-out 0.243, pass.

     The null is overfitting. With the words shuffled across items, that rule fits 0.198 on average, and 23% of 500 shuffles fit as well as the real words. So it is not a stronger shortcut, but the in-sample bar does reward fitted cells. A pre-registered rule with about 30 cells would have failed for that reason alone. The pre-registered 8-cell rule is not near that point.
   - **Permutation nulls.**
     - Paired sign-flip on d (20,000 flips): one-sided p = 0.0006.
     - A bettor keeping its own confidence but pointing at random: null d is +0.073 on average; P(null ≤ observed) < 1/5,000.
     - Answers coin-flipped and both sides rescored, with the rule refitted on the false labels (1,000 relabellings): d has mean +0.062 and 95% range [+0.019, +0.106]. It never reaches the observed −0.059, so random labels never give a pass.
10. **Holds, with a hole in the write-up.** The intervals are at item level, and the paper-level bootstrap agrees. The field jackknife with ±1.96 on four clusters is [−0.110, −0.008]. With t(3) = 3.182 it is **[−0.142, +0.024], which includes zero**. The results file says only "would be wider" (cut 4).
11. **Holds.** One primary test, no correction, as stated. The secondaries are labelled.
12. **Holds.** No outcome reaches the bettor. The headline tags were written by a writer who saw the answers, which favours the rule (disclosed).

**C. Write-up**

13. **Holds, mostly.** It names one bettor (Opus at effort low), one run and one item set. "The strongest Claude model" follows §1 of the pre-registration.
14. **Holds.** The leave-one-out and jackknife figures are labelled secondary.
15. **Hole (cut 1).** The text explains the margin as the model having "more than knowing which fields usually report good news, or which way results in a field tend to go". The design cannot tell this apart from "the model beats pooled rates": the fields carry no signal here (B9). On the good-news-tagged class alone, the margin is not shown (B6).
16. **Hole (cuts 1, 2, 3).**
    - Cut 1: the plain-English section brings back "report good news", which D55 F1 removed from the generated sentence because 74 of 116 items use an up-option rate, not a good-news rate.
    - Cut 2: "Without the unfair advantage (each finding's own answer left out of the rates)" misdescribes the leave-one-out rule. The pre-registration (§4, D52, P11) says leaving the item out handicaps the rule. The design review's worlds give in-sample < oracle < leave-one-out, so −0.085 overstates the fair gap; the fair gap lies between −0.059 and −0.085.
    - Cut 3: "clearly" is not supported. The four-cluster t interval includes zero, and dropping the 10 most favourable items reaches zero.
17. **Holds.** The ss-b1 audit's item 9 numbers match `ledger/audits/ss-b1.md` lines 120–125. ss-b2's −0.068 [−0.099, −0.036] matches `results/ss-b1-results.md` line 53.
18. **Hole (cut 4).** The jackknife bullet hides a negative: with the t multiplier, the field-level interval includes zero. That should be said as plainly as the pass (rule 5).

**D. Process**

19. **Holds.** $0. There is no call path in `score_f3.py`, and the spend table shows 0 calls.
20. **Holds (n/a).** No calls were made.
21. **Holds.** `p_option_1` is on 1–99, clipped, in one direction.
22. **Holds.** Reported as "pass, unreplicated". The file says this is the same run scored a fourth time.

**E. Engine records**

23. **Holds (n/a).** Fixed seed 20261104, stated in §2. No beacon.
24. **Holds (n/a).** Not a tiebreak.
25. **Hole (minor).**
    - The §0 lesson is in 3fd6037. `ledger/lessons.jsonl` has the same sentence, added at 08331f8 (06:41:34).
    - Its `read` block was wrong when entered (26 bets, Brier 0.217, read at 9a75cc2, per the design review's D10). It was corrected under D55 (5ee223a, 06:56:36, before data) to 27 bets, 0.209, 8/27 and `ta-b1r2.md`. I checked that against `git show 3fd6037:ledger/brier.md`: it matches.
    - The lesson cites P11, whose `do_this` is to read every verdict against a label-permutation null on the same structure. The design sidesteps P11 for the primary by fitting in-sample. Yet the leave-one-out figure, the case P11 is about, now sits in the verdict sentence (D55 F2), and no label-permutation null is in the design or the results.
    - My relabelling null (B9) closes this at $0: random labels never pass. The `do_this` was still not done.
    - P1's `do_this` (odds above 0.5 need archive evidence) is met by ss-b2's margin.
26. **Holds.** The design review is ledger/design-reviews/ss-b11.md. It was committed at 1422610 (06:54:52), after the pre-registration and before scoring, with verdict fix-first (3 flaws). All three fixes are in D55 (06:56, before data) and were confirmed at e19586f (06:57:54) on synthetic data only. `design_review_missed: []`.
    - The holes above are post-data write-up drift (C15, C16, C18) and a finding that needs the labels (fields carry no signal), which a review that may not score the archive could not compute.
    - The review did flag in advance that τ is small and that a pass "adds little" (D11).
    - The missing P11 permutation null is an E25 matter. D10 checks only that the lesson line is present and matches.

## The pre-mortem, scored

**My own reason, written from the checklist before scoring:** the bet did not fail. If it had, the likeliest mechanism would have been the in-sample bar rewarding the number of fitted cells (`design`). At 24 up-word cells the in-sample rule reaches a null with no real signal (B9). At the pre-registered 8 cells it does not.

**Pre-mortem (§0, 3fd6037):** "If this fails, the most likely reason is that field rates fitted in-sample on about 20 items per field cell overfit enough to bring the rule's Brier near the bettor's 0.163." Kind: `design`. (It sits in the §0 table, which I read for check A2. I wrote my own reason from the checklist evidence above, not from it.)

**Score: `not_failed`; `risk_seen: false`.** The pre-registered rule's in-sample Brier was 0.223. Overfitting gained it about 0.007 over pooled rates and about 0.026 over its own leave-one-out form, and it stayed far from 0.163. The named mechanism is real: it is what makes the 24-cell rule null. But it did not show up at the pre-registered rule's size.

## Required cuts

1. In "In plain English", replace
   > **So the model's edge in round 1 is more than knowing which fields usually report good news, or which way results in a field tend to go.**

   with
   > **So, on these items, the model's edge in round 1 is more than knowing each field's rate of papers' own claims holding and of "higher / more" results.** The four fields barely differ here: the rule fits no better with the real field labels than with shuffled ones (69% of 2,000 shuffles fit as well or better; audit ss-b11), so in effect the model beat pooled rates, not field habits. On the 38 headline-tagged items alone, the gap is 0.053, with an interval of −0.008 to 0.117, so the edge over the good-news rate by itself is not shown.

2. In "In plain English", replace
   > Without the unfair advantage (each finding's own answer left out of the rates), the gap is larger: 0.085 [0.048, 0.123].

   with
   > Leaving each finding's own answer out of the rates does not make the rule fair. It turns the advantage into a handicap (P11), and the gap is then 0.085 [0.048, 0.123]. A rule that knew the true field rates would sit between the two.

3. In "In plain English", replace
   > **The model still clearly beat it.**

   with
   > **The model still beat it.**

4. In "What it cannot do", replace
   > The field jackknife interval uses ±1.96 on four clusters. A t multiplier with 3 degrees of freedom would be wider (design review remark). It is a secondary.

   with
   > The field jackknife interval uses ±1.96 on four clusters. With a t multiplier for 3 degrees of freedom (±3.18) it is [−0.142, +0.024], which includes zero: at the level of fields, four clusters cannot show the edge. It is a secondary.

The status line "**Unaudited.**" becomes a link to this audit, as `operators/auditor.md` requires.

## What would break it next

- **Cheapest ($0).** Pre-register a finer answer-free rule with a fair fit before running it.
  - Example: field × up word × question order, scored by 10-fold cross-validation, or in-sample but against a word-shuffle null on the same cells.
  - It tests whether any answer-free cue on these 116 items reaches the bettor once overfitting is netted out. My exploratory runs say none does: every leave-one-out version, the pooled-only one included, scores 0.238 or worse, against the bettor's 0.163. A pre-registered version would make that a result.
- **Real test (about $1–3; ss-f1's job).** Run the same rule against another bettor (Haiku or Sonnet) on the same items, or against Opus on round 2's items, where field up-rates may differ more.
  - On these items the fields carry no signal, so this bet could not have found a field-habit explanation even if one existed for other papers.
  - Only a set where the fields do differ can test "more than field habits".
