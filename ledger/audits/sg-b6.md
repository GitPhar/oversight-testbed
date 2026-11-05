---
bet: sg-b6
program: self-grading
prereg_commit: 738472c
results_commit: 19582bf   # the clone's last commit (Novelty line); the result itself is a3a0341, data 3164fff
auditor_session: fresh auditor subagent, working only in the audit clone /Users/seanpharris/oversight-testbed-audit-sg-b6 (HEAD 19582bf)
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 12:21 America/Denver
claims_checked: 26
holes_found: 5
overclaims_cut: 5
reproduced: false              # reproduce.py: NOT REPRODUCED, table 4 (spend total $0.652 committed, $0.642 regenerated); every statistic and the analysis JSON regenerate byte for byte
verdict_claimed: mixed
verdict_after_audit: mixed
verdict_stands: true
canary: unknown
false_alarms: 0
design_review_missed: []
novelty_checked: partly new
novelty_holds: true
novelty_search: "historical controls versus concurrent controls overestimate treatment effect same-batch re-measurement LLM evaluation" (one WebSearch, standard, 2026-11-05; clinical-trial words for a cross-run comparison against a concurrent one). Found the non-contemporaneous control literature (historical controls inflate effects on average, by about a third, but in both directions); nothing on LLM judges or a quoted-copy gap.
failed: true
failure_reason: Haiku's same-run T came out at +5.26, under the 6.3 bar, with a domain-cluster interval [+2.0, +8.4] about three times wider than its distance from the bar; the fall from sg-b4's +6.82 (−1.56 [−3.60, +0.38]) is split about evenly between the own-turn and quoted cells and is itself not distinguishable from zero. Kind: world.
failure_kind: world
premortem_score: kind_only
risk_seen: null
---

# Audit of sg-b6: same-run re-grade of sg-b4's Haiku turn-role reading

## In plain English

The verdict stands: **mixed**. With every grade taken in one run, Haiku 5.5 was stricter about the planted exaggeration in the quoted copy than in its own reply by +5.26 points [+2.02, +8.43]. That is below the 6.3 bar, but the interval does not rule the bar out, so the pre-registered rule reads "undetermined". I rebuilt every statistic from the archived calls, byte for byte. I dropped each study and each domain in turn, read each repeat alone, and moved the bootstrap seed. None of that changes the reading.

Five things have to be fixed:
- One table cell is wrong. The spend total reads $0.652; the archive and the per-model cells add up to $0.642. `reproduce.py` fails on that cell. The Novelty commit changed it, and its commit message does not say so.
- Two sentences say Opus's result "holds, and is larger" and holds "more strongly" than in sg-b4. Opus's change from sg-b4 is +1.07 [−0.38, +2.56], which is not distinguishable from zero, and Opus is reported, not scored.
- One sentence misreads the repeat-noise SD.
- The Novelty line cites, as in print, a paper that arXiv withdrew two days earlier. That paper's number (test-retest above 0.95) also does not support the sentence it is cited for.
- The scored engine odds (0.55) came from a re-elicitation that was handed this bet's design-review noise figures and a number from sg-b4's audit. Rule 14 excludes both.

What would break it next: a third same-run Haiku run on the same 60 studies (about $0.04). At least as useful: the record should say that Haiku's T is +7.5 on sg-b4's 30 studies and about +3.0 on the other 30, so study-to-study spread, not repeat noise, is what keeps this interval wide.

## The case that this result is false

Written before the checklist.

The headline is "mixed", so "false" means one of two things: the data actually support pass or fail, or "mixed" is a reading that the write-up then turns into claims it cannot carry.

**First, "mixed" is the wrong verdict.** The statistic is a mean of 60 per-study differences, and those differences are very spread out: SD 10.9, ranging from −24 to +30. Domain-level means run from −9.2 to +16.3. A domain-cluster bootstrap over 20 domains with that spread could easily be unstable. A different seed, or dropping one domain such as domain 0 (+16.3) or domain 7 (−9.2), might push the mean over 6.3 (giving pass, since the guard F is above zero) or pull the upper end of the CI under 6.3 (giving fail). The two Haiku repeats are averaged, and averaging is a pooling step. If one repeat alone reads differently, the average hides that.

**Second, the write-up says more than the data.** Three examples:
- "sg-b4's Haiku half does not hold up as a clean pass": today's T is lower than sg-b4's +6.82, but the paired drop is −1.56 with a 95% interval that includes zero. The data do not show that anything changed between sg-b4 and today. They show only that today's mean landed on the other side of a line.
- The Opus sentences ("holds, and is larger", "more strongly than in sg-b4") compare two point estimates from single runs with one repeat each, on an unscored model.
- "Took away 46% of it, just under the half the bar asks for" states a ratio of two noisy means with no interval, and quietly swaps the bar's denominator (sg-b3's G, 12.58) for today's G (11.53).

**Third, the scored odds.** The engine's 0.55 equals Sean's 0.55 to the hundredth. It was re-elicited after a design review whose figures and recommendations were handed to the eliciting context. If the engine's odds were moved toward a number it had seen, the bet's Brier score is contaminated.

**Fourth, the clone may carry a plant.** Every number in the results file needs checking against the regenerated tables.

## Claims checked

| # | claim (quoted or paraphrased) | check run | outcome |
|---|---|---|---|
| 1 | Verdict mixed; T +5.26 [+2.02, +8.43] | `sg_b6_samerun.py analyse`, byte-identical JSON; my re-analysis | holds |
| 2 | F +4.15 [+0.86, +7.46], "the guard held" | analysis JSON | holds |
| 3 | own penalty 67.7, quoted 73.0 | JSON `o`, `q` | holds |
| 4 | T study CI [+2.55, +7.87]; reading on study bootstrap undetermined | JSON | holds |
| 5 | same-run G +11.53 [+8.73, +14.42]; sg-b3 G 12.6 | JSON; recomputed sg-b3 G from archive (12.58) | holds |
| 6 | "The quoted copy took away 46% of it, just under the half the bar asks for" | ratio cluster bootstrap | point value holds; interval [0.20, 0.65] not reported (recommendation) |
| 7 | Opus T +5.03 [+3.80, +6.14], reads turn role at 3.0 | JSON; F CI [3.17, 4.81] | holds |
| 8 | "Opus's sg-b4 result holds, and is larger (sg-b4: +4.0)" | paired difference, cluster CI | **hole**: +1.07 [−0.38, +2.56] |
| 9 | "Opus's half does hold, more strongly than in sg-b4" | same | **hole** (C14, C16) |
| 10 | Sonnet T +0.70 [−0.91, +2.21]; "almost no blunting in sg-b3" | JSON; sg-b3 Sonnet G 1.37 | holds |
| 11 | sg-b4 cross-run T on the same studies +6.82 / +3.97 / +1.33 | JSON `cross_run` | holds |
| 12 | own penalty +0.82 [−0.62, +2.42]; quoted −0.74 [−1.9, +0.2]; "neither distinguishable from zero" | JSON | holds |
| 13 | "The −4.3-point drift ... did not reappear across all 60" | own penalty on sg-b4's 10 drift studies: today 64.45, sg-b3 64.2, sg-b4 drift 59.9 | holds (it did not reappear on those 10 either) |
| 14 | T on r1 +4.85, r2 +5.67 | JSON; my per-repeat cluster CIs [1.35, 8.27], [2.20, 9.20] | holds; each repeat alone also reads undetermined |
| 15 | "55% of its grades were identical ... and the rest moved by 4.5 points (SD)" | recomputed | **hole**: 4.54 is the SD over all 480 pairs, identical ones included; among the 45% that moved, SD is 6.77 (mean absolute change 5.1) |
| 16 | "mostly on the flawed texts" | variance split | holds: 95% of squared change is on flawed cells |
| 17 | median +5.00, 10% trimmed +5.34, one tie | JSON | holds |
| 18 | "Dropping any one study or any one domain does not change the reading" | JSON robustness; my LOSO range [4.84, 5.75], LODO range [4.68, 6.02] | holds |
| 19 | 960 calls, complete, no refusal, $0.642 | cache: 960 records, all integer grades 0–100, 960 distinct request IDs, no `results/refusal.md`; spend 0.641988 | holds |
| 20 | Table 4 total **$0.652** | `reproduce.py` | **hole**: regenerates $0.642 |
| 21 | Program spent $5.93 of $7.65 | `sg_common.program_spent()` = 5.9285 | holds |
| 22 | Design review fix-first, D23, go at 12:02 (4a55e29) before first call | git log; review file; check_prereg R1/R2 ok | holds |
| 23 | Seed: CURBy-RNG pulse 1592585 | beacon fetch; seed.py | holds |
| 24 | Odds: engine 55, "re-elicited before data under D23" | D23, inbox rows 4, 5, 7; CONTEXT rule 14 | **hole**: before data, but the elicitation was handed material rule 14 excludes |
| 25 | Novelty line, citations | five arXiv abstract/HTML pages and one search | **hole**: Norman et al. withdrawn and miscited; the rest hold |
| 26 | §6 limits restated ("Not 'models', not 'every'"; the bundle) | read against prereg §6 | holds |

## Checklist

**A1. Pre-registered before data: holds.**
- Author times: prereg 738472c at 11:40:35; seed 08043ce at 11:42:54; design-review go 4a55e29 at 12:05:14; data 3164fff at 12:09:00; result a3a0341 at 12:10:35.
- The cache records carry no timestamps, so the stated run window (12:05:20 to 12:08:53) can be checked only against the commits, which agree with it.
- The archives opened for the dry run (sg-b3, sg-b4) are earlier bets' data, used as the pre-registration says.

**A2. Rule, statistic, split, seed and budget match the pre-registration: holds.**
- `git diff 738472c HEAD` on the prereg file shows the seed line only.
- In the code, the statistic, `read()`, bars, gate, guard, CAP, REPS and the study sets are unchanged since 738472c. The only additions are the D23 fresh cells (G_today, a secondary) and the D24 `pilot` argument.
- Call count 960 rather than §3's 720: the extra 240 are the D23 fresh cells, logged in D23 (dated 2026-11-05, committed 12:00:34, before the first call). The reviewer showed on synthetic caches that they cannot reach the reading.

**A3. Bar not lowered: holds.** The bar stays 6.3 (Haiku) and 3.0 (Opus). D23 changed only the dry-run noise model.

**A4. Primary is the pre-registered primary: holds.** The verdict is read on Haiku's T with the domain-cluster CI. Opus and Sonnet are kept as reported readings.

**B5. Ties and floating point: holds.**
- The mean (5.26) is 1.04 from the bar, and the CI upper end (8.43) is 2.13 above it. The `ge`/`lt` tolerance is irrelevant at those distances.
- Over 50 bootstrap seeds the CI upper end ranges 8.35 to 8.52 and the lower end 1.88 to 2.12. The reading never changes.
- One tie (T = 0); excluding it, the mean is 5.35.

**B6. Pooling: holds.**
- The two Haiku repeats are averaged, as pre-registered. Read separately they give r1 +4.85 [1.35, 8.27] and r2 +5.67 [2.20, 9.20], both undetermined.
- The fresh cells are not pooled into anything that is read.
- T is the clean shift (+1.11) plus F (+4.15). So about a fifth of T comes from the quoted copy being kinder to clean text. The guard requires F > 0, and F's CI lower end is 0.86.

**B7. Few items driving it: holds, with a note.**
- Leave-one-study-out T ranges 4.84 to 5.75; leave-one-domain-out ranges 4.68 to 6.02. Nothing crosses 6.3.
- Domains are heterogeneous: domain means run −9.2 to +16.3, with 5 of 20 negative.
- Not reported, and worth knowing: on sg-b4's 30 studies (the Opus and Sonnet set) Haiku's T is +7.48 [3.95, 11.60]; on the other 30 it is about +3.0. That subset would have cleared the bar on the mean. Study-to-study spread, not repeat noise, sets the width of this interval.

**B8. Circular estimators: holds.** The bar comes from sg-b3's G, measured before this bet. Nothing is fitted.

**B9. Baselines and controls: holds.**
- The layout baseline (T = 0) is rejected: the CI lower end is 2.0.
- The kinder-to-clean rival is excluded by the guard (F CI above 0).
- The gate holds: q 73.0, CI [69.4, 76.5].

**B10. Uncertainty: holds.**
- The CIs are at domain level (20 clusters), as pre-registered.
- The paired change from sg-b4 (−1.56 [−3.60, +0.38]) and the T/G ratio interval ([0.20, 0.65]) are not reported. Recommended, not required.

**B11. Multiple comparisons: holds.** One scored reading plus a gate and a guard; the file says no correction was made.

**B12. Leakage: holds.** Nothing is fitted. `verify()` checks every record's conclusion and messages hash against the frozen code.

**C13. Scope drift: holds.** The file says "Three models from one family, one item set. Not 'models', not 'every'".

**C14. Rank drift: hole.**
- Opus is pre-registered as "reported, not scored ... never promoted to the verdict".
- The plain English says "On a same-run comparison Opus's sg-b4 result holds, and is larger" and "Opus's half does hold, more strongly than in sg-b4". Both state a comparison with sg-b4 as a finding.
- The paired difference is +1.07 [−0.38, +2.56], on one repeat per cell, with no measure of Opus's repeat noise (§6 says so itself).
- "Reads turn role at its bar on a same-run comparison" is supported. "Larger" and "more strongly" are not.

**C15. Mechanism drift: holds.**
- "Why Haiku's number fell" splits the drop between the two cells and says that neither shift is distinguishable from zero.
- The Novelty line says run-to-run noise "is neither shown nor ruled out as the cause". That is correct.

**C16. Plain English matches the table: hole.**
- (a) The Opus sentences (C14).
- (b) The repeat sentence: "the rest moved by 4.5 points (SD)". The table's 4.54 is the SD of the second-minus-first difference over all 480 pairs, including the 55% that are zero. Among the pairs that moved, the SD is 6.77.
- (c) The table's spend total ($0.652) disagrees with the header's $0.642 and with the sum of its own row ($0.054 + $0.399 + $0.190 = $0.643, $0.642 unrounded).
- Every other sentence checked matches the table.

**C17. Citations: hole (in the Novelty line; see F27).**

**C18. Negative results stated plainly: holds.** The file opens with "Pre-registered verdict: mixed" in the pre-registered words, and says plainly that sg-b4's Haiku half does not hold as a clean pass.

**D19. Budget: holds for the run.** CAP 0.80 and PROGRAM_CAP 7.65 are in code, checked before each call; spend is $0.642. The table misstates the total (C16c).

**D20. Stop-on-refusal: holds.** There is no refusal file. All 960 records have request IDs and integer grades. No key was retried: one record per key.

**D21. One scale direction: holds** (`sg_common.SCALE`, unchanged).

**D22. Replication: holds for the verdict.** No pass is claimed. Opus's turn-role reading is one model, one run, one repeat, sg-b4's design; it should not be described more strongly than "reported" (C14).

**E23. Seed: holds.**
- I fetched CURBy-RNG pulses with `@buff-beacon-project/curby-client@1.2.0`, a free read:
  - 1592584 at 18:40:00Z (11:40:00 MST), before the prereg author time of 11:40:35;
  - 1592585 at 18:41:00Z, with randomness equal to `data/sg-b6-seed.json`.
- `ledger/seed.py` reproduces order 15078222124198125769 and boot 12959117145896730554.
- The code reads only that file (`S.seeds(BET)`). No study is drawn.

**E24. Tiebreak:** not applicable.

**E25. Lesson: holds. Odds revision: hole.**
- *Lesson.* The lesson row is in §0 at 738472c. `check_prereg.py` returns L1–L3 ok. The read block (74 bet rows, 35 scored, Brier 0.164, newest audit ss-b10c at 11:19) matches the ledger at 738472c. P8's do_this ("the claim is about the bundle") is in §6. P10's (leave-one-out with a stated flip rule) is in §4.
- *Odds revision.* The odds change 0.16 → 0.55 is recorded before data (inbox, 12:00; D23 at 12:00:34; first call 12:05:20).
- But rule 14 says every odds elicitation is handed `ledger/prior.md` and the bet's own description and "nothing about the bet's history: ... no audit or review notes about it".
- D23 says the re-elicitation was handed "the corrected prior-work clause, the measured noise and sg-b4's same-run T on its 10 drift studies (+12.1)":
  - the measured noise and the corrected clause are this bet's design-review findings;
  - the +12.1 is a figure from sg-b4's audit (B9).
- Its reason then cites "+12.1" and "low repeat noise". The second contradicts the 5.5-point per-call noise it was handed.
- The design review and inbox row 7 disclose this as "a strict reading" and argue it is "facts about the parent bet's run". The rule's text names review notes about the bet. The noise figure is exactly that.
- The scored number therefore comes from an elicitation outside rule 14.
- It does not flatter the engine (Brier on a 0 outcome is 0.30 at 0.55 against 0.026 at 0.16). It does contaminate the odds-calibration record either way.
- *Required.* The ledger row carries a note that `engine_odds` 0.55 was not elicited under rule 14, and `ledger/brier.md` reports this bet's score at both numbers. Which number counts is a ledger and steer decision, not the audit's.
- I found no evidence that the eliciting context saw Sean's 0.55. The equality is recorded but unexplained.

**E26. Design review: holds.**
- 20c8185 (11:56:09) is after the prereg, verdict fix-first with 2 flaws.
- The fixes are in D23 (12:00:34), dated before data.
- Confirmed go in 4a55e29 (12:05:14), before the first call.
- `check_prereg.py` returns R1 and R2 ok.
- I found no flaw that D1–D12 should have caught. The rule-14 issue came from the review's own recommendation, and the review disclosed it.

**F27. Novelty line: holds as a verdict, with a citation hole.**
- *Presence.* The line exists, is written by "a fresh claude-opus-5-5 Novelty session (subagent)", and names its search.
- *Ledger row.* The `novelty*` fields are not in this clone. The clone ends at 19582bf, and the inbox in it has no novelty op for sg-b6. Cannot check.
- *Papers opened:*
  - **Khullar, Hopkins, Wang and Roger 2026** (arXiv 2603.04582 v1, abs and HTML): holds. Monitors fail to report risky or incorrect actions more often when evaluation follows a previous assistant turn. "self-attribution bias is strongest in on-policy settings".
  - **Tsui 2025** (arXiv 2507.02778 v3): holds. Models "correct external errors but fail on identical internal ones".
  - **Haldar and Hockenmaier 2025** (arXiv 2510.27106, HTML): holds. Intra-rater Krippendorff's alpha on MT-Bench over 3 runs: 0.265 (Llama 3.1), 0.507 (DeepSeek-R1 distill), 0.563 (Qwen 3), all open-weight.
  - **Norman, Rivera and Hughes 2026** (arXiv 2606.19544): **hole**, for two reasons.
    - The abstract page shows v2 (3 Nov 2026) withdrawn: "arXiv admin note: This submission has been withdrawn because it does not meet arXiv's research content quality standards". The Novelty line, written 5 Nov, cites v1 among "papers in print" without saying so.
    - Its number, "high test–retest reliability (>0.95) coexists with severe position bias (>0.10)", says judges *agree* with themselves across repeats. It is cited under "LLM judges disagree with themselves across identical runs", which it does not support.
  - **Roytburg et al. 2026** (arXiv 2601.22548 v2): holds. The v2 abstract reads "only 51% of initial findings retain statistical significance". The baseline is a judge's votes for its own wrong answers against its votes for others' wrong answers. No repeated runs.
  - **Quellmalz 1980** (CSE Report 136, "Problems in Stabilizing the Judgment Process"): the CRESST listing summary separates drift from scale instability across scoring sessions. Holds at abstract level, as the line says.
- *Verdict word.* "Partly new" follows. The kind of result (own-turn leniency, judge run-to-run instability) is in print. The specific same-run against cross-run re-measure of a quoted-copy gap is not.
- *My search* (header) found the clinical-trial literature on non-contemporaneous (historical) controls: concurrent comparisons are unbiased on average, while historical ones inflate effects by about a third, in either direction case by case. That is the general methodological point behind this bet. It is not a statement of this result, and here the cross-run-to-same-run change is not distinguishable from zero. It does not move the word.
- *Required.* Correct the Norman clause (Required cuts 5). Citing the clinical-trial literature beside Quellmalz is recommended, not required.

## The pre-mortem, scored

**My failure reason**, written before scoring: Haiku's same-run T came out at +5.26, under the 6.3 bar, with a domain-cluster interval [+2.0, +8.4] about three times wider than its distance from the bar. The fall from sg-b4's +6.82 is split about evenly between a larger own-turn penalty (+0.82) and a smaller quoted penalty (−0.74), and neither is distinguishable from zero. Kind: **world** (the true effect sits near or just under the bar), with study heterogeneity setting the width.

**Disclosure:** the pre-mortem sits in the §0 table of the pre-registration, which I had to read for A2, so I saw it before the checklist. I wrote the line above from the checklist evidence.

**Pre-mortem:** "If this fails, the most likely reason is that same-run own-turn penalties come out larger than sg-b3's archived ones, shrinking Haiku's T to between 0 and 6.3: sg-b4's half-point margin was cross-run luck." Kind: `world`.

**Score: kind_only.** T did land between 0 and 6.3, and the own-turn penalty did move in the named direction. But it carries only about half the drop (+0.82 of 1.56), with a CI of [−0.62, +2.42], and the quoted cell carries the other half. Nothing shows that sg-b4's margin was cross-run luck: the paired change is −1.56 [−3.60, +0.38]. So the failure is of the stated kind, but the named mechanism is not the shown cause.

## Required cuts

1. **Table 4, spend total.** "| test run | $0.054 | $0.399 | $0.190 | **$0.652** |" becomes "| test run | $0.054 | $0.399 | $0.190 | **$0.642** |". This is what `reproduce.py` regenerates. The commit that put $0.652 there (19582bf, the Novelty commit) does not mention the change (rule 8).
2. "On a same-run comparison Opus's sg-b4 result holds, and is larger (sg-b4: +4.0 on the same studies)." becomes "On a same-run comparison Opus still reads turn role at its 3.0 bar (sg-b4: +4.0 on the same studies; the change, +1.1 [−0.4, +2.6], is not distinguishable from zero, and Opus ran one repeat)."
3. "Opus's half does hold, more strongly than in sg-b4." becomes "Opus's reported reading, turn role, is the same as in sg-b4 (one run, one repeat, not scored)."
4. "55% of its grades were identical across the two repeats, and the rest moved by 4.5 points (SD), mostly on the flawed texts." becomes "55% of its grades were identical across the two repeats; the SD of the change over all grades was 4.5 points (6.8 among those that moved), almost all of it on the flawed texts."
5. Novelty line: "Norman, Rivera and Hughes 2026, arXiv 2606.19544 v1: test-retest above 0.95 alongside position bias above 0.10" is removed from the "disagree with themselves" clause. If it is kept anywhere, it reads: "(Norman, Rivera and Hughes 2026, arXiv 2606.19544, withdrawn by arXiv on 3 Nov 2026, reported the opposite on two production judges: test-retest above 0.95)". The verdict word stays partly new.
6. Header odds line (an addition, not an overclaim): after "re-elicited before data under D23", add "; that elicitation was given this bet's design-review noise figures and sg-b4's audit figure (+12.1), which rule 14 excludes, so the bet is also scored at the first number, 0.16".

Recommended, not required:
- After "The quoted copy took away 46% of it", add the interval "(95% domain CI 20% to 65%)", and say that the bar is half of sg-b3's G, not of today's.
- Add the paired change from sg-b4 (−1.56 [−3.60, +0.38]) to "Why Haiku's number fell".
- Add Haiku's T on sg-b4's 30 studies (+7.5) against the other 30 (about +3.0).

## What would break it next

Mixed is overturned only by narrowing the interval, and its width comes from study-to-study spread (SD of T 10.9; domain means −9 to +16), not from repeat noise.

- **Cheapest overturning test.** Run the identical four-cell Haiku design again on the same 60 studies, twice each: 480 calls, about $0.04. Pre-register reading the mean of the two same-run T's against 6.3 on the domain-cluster bootstrap. This tests whether +5.26 or sg-b4's same-run +12.1 on its 10 drift studies (today's +9.1 on the same 10) is the run-to-run outlier.
- **Better test.** Write conclusions for 60 new studies in 20 new domains (Haiku write plus four-cell grade, about $0.06) and read T on all 120. That roughly halves the cluster interval and can push it wholly above or below 6.3.
- **Opus.** The "larger than sg-b4" question needs two repeats on its 30 studies (120 calls, about $0.40).
