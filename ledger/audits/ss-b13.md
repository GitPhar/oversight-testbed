---
bet: ss-b13
program: settled-science
prereg_commit: 012449c
results_commit: d3f8201
auditor_session: fresh auditor subagent in audit clone /Users/seanpharris/oversight-testbed-audit-ss-b13 (no chat or transcript read)
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 11:02 America/Denver
claims_checked: 18
holes_found: 5
overclaims_cut: 4
reproduced: false
verdict_claimed: mixed
verdict_after_audit: mixed
verdict_stands: true
canary: unknown
false_alarms: 0
design_review_missed: []
novelty_checked: partly new
novelty_holds: true
novelty_search: WebSearch (standard) "LLM predict clinical trial results "positive" outcome bias baseline smaller vs larger model forecasting unpublished trials" (the mechanism in clinical-trial forecasting words); found Jin et al. arXiv 2411.17595, opened
failed: true
failure_reason: Haiku's Brier minus the good-news rule's (-0.024) has upper bound +0.011 (item) / +0.012 (cluster), not below -0.01; on the 38 items where the rule bets, Haiku is worse than it (+0.024).
failure_kind: world
premortem_score: named
risk_seen: null
---

# Audit of ss-b13: do Haiku and Sonnet, as bettors, beat always-50% and two shortcut rules on the findings Opus scored?

## In plain English

The verdict holds: the bet is **mixed**. Sonnet met the pre-registered rule and Haiku did not. Haiku missed on C3 (the good-news rule) by a clear amount. My re-analysis of the archive gives the same numbers, and the run followed its pre-registration, D69's fixes and the design review. But the reproduce script fails on this results file. One table cell says Haiku was scored on 106 items, and the archive and `score_f1.py` both give 116. That cell was changed in the Novelty-line commit (d3f8201), after the results commit, which had 116. Three statements also say more than the data allow:
- "Sonnet did as well as Opus" was never tested as an equivalence. The paired difference is +0.004 (interval −0.018 to +0.027).
- Most of Sonnet's 0.064 gain over the good-news rule comes from the 78 items where that rule just says 50%. On the 38 items where the rule actually bets, Sonnet is not shown to beat it (−0.027, interval −0.109 to +0.053), and neither is Opus.
- The Novelty line says Haiku does not beat the good-news rule at all, when the miss is only on the margin. It also understates CUSP's baselines.

"Partly new" survives the cited papers and my own search. What would break the verdict next: an Opus flattery rater run on round 1's 116 items, about $0.30, to see whether Sonnet beats the good-news idea applied to every item.

## The case that this result is false

The headline says Sonnet "did as well as Opus" and beat the good-news rule "well past the margin". So the case that matters is whether the Sonnet half, and with it the "mixed", is an artefact of a weak comparator.

The good-news rule abstains on 78 of 116 items (it gives 0.5 where the writer left no headline tag). On those 78 items, C3 reduces to "Brier below 0.25", which is C1 again. So C3 is mostly a coin comparison, with only a third of it testing the publication-bias rival.

On the 38 items where the rule does bet, Sonnet's gain is −0.027 with an item interval of [−0.109, +0.053]. On those items, Sonnet's choice agrees with the writer's good-news tag 70% of the time, while the tag itself is right 74% of the time. On exactly the items that test the rival, then, Sonnet is not separated from "bet on the paper's own success". Even Opus is not: −0.060 [−0.130, +0.008].

Read that way, neither smaller model is shown to beat the publication-bias shortcut where it applies. The verdict would be "fail" under a rule that compared like with like. "Sonnet did as well as Opus" would then be true but empty: both beat a coin, and neither is shown to beat the rival.

Two more things support this reading. On round 2, where a flattery rater bets on every item, Sonnet only ties it (+0.002). And Sonnet's own label flips when the interpretability field is dropped (C3 upper bound −0.009). So the Sonnet "met" is fragile, and on the part of the test that matters it is untested.

What the case cannot overturn is the pre-registered statistic. C3 was defined over all 116 items with 0.5 on untagged items, and the bar was set before data (§2, §4). The verdict under the rule as written is mixed. The checklist below finds that the case is right about the write-up, not about the verdict.

## Claims checked

| # | claim (quoted or paraphrased) | check run | outcome |
|---|---|---|---|
| 1 | verdict mixed: Sonnet meets the rule, Haiku does not | reproduce.py; own re-score with `score_f1` functions | holds |
| 2 | table: Haiku n 106 | reproduce.py; count in f1-bets.jsonl (116 r1 primaries, all scored) | **hole**: 116 |
| 3 | Haiku C3 −0.024 [−0.059, 0.011]; cluster [−0.060, 0.012] | regenerated; own bootstrap, 5 other seeds (ub 0.0111–0.0116) | holds |
| 4 | Sonnet C3 −0.064 [−0.099, −0.028] | regenerated; other seeds ub −0.028 to −0.029 | holds |
| 5 | "Sonnet did as well as Opus", "Sonnet matches Opus" | paired Sonnet−Opus Brier +0.004 [−0.018, +0.027] | **hole**: no equivalence test |
| 6 | Sonnet "beat the good-news rule by 0.064 … well past the margin" | split by headline tag | **hole** (wording): tagged-only −0.027 [−0.109, +0.053] |
| 7 | accuracies 70.7 / 77.6 / 76.3% | regenerated | holds (Sonnet has 2 ties at 50, Opus 1; accuracy only) |
| 8 | Haiku "clearly better than always saying 50%" | C1 ub 0.236 / 0.236 | holds |
| 9 | Sonnet's label changes without interpretability; no single item changes either label | LOFO (Sonnet C3 ub −0.009 / −0.011); LOO item; own leave-one-paper-out (no flips) | holds |
| 10 | round 2: Sonnet +0.002 [−0.021, +0.026], Haiku +0.037, Opus −0.036 vs flattery rater | regenerated (f1-tables.md match) | holds |
| 11 | up-word rule 0.316, good-news 0.232 | regenerated | holds |
| 12 | card's event met | C1 item ub both < 0.25 | holds |
| 13 | first call 10:39:24, last 10:41:59, after go c751f77 10:38:33 | t_utc in f1-bets.jsonl; author dates | holds |
| 14 | 416 calls, 0 refusals, $0.626 + $0.037 pilot = $0.663 of $0.85 | f1-cache.json (416 keys = 416 planned keys), f1-pilot-cache.json (24) | holds |
| 15 | same prompt and option order as Opus | own plan-vs-archive check: 116/116, 92/92 order and prompt bytes; 416/416 bets match plan | holds |
| 16 | thinking off (Haiku disabled, Sonnet between_tools) | usage.thinking on all 416 | holds |
| 17 | ss-b10: flattery prompt 92% of Sonnet's forecasting skill | results/ss-b10-results.md line 11, table row 0.92 [0.79, 1.07] | holds |
| 18 | Novelty line's citations and verdict word | opened 2403.03230, 2604.10718, 2506.00794, 2605.22681, Hewitt et al. PDF; one own search | verdict holds; two wording holes (cut 4) |

## Checklist

**A1. Pre-registered before data: holds.** The author dates are:
- pre-registration 012449c, 10:13:08;
- design review 247d484, 10:33:40;
- pilot calls 10:34:22–10:34:35, on 12 pre-cutoff items per model, excluded from the test (`f1-pilot-cache.json`);
- D69, a5142f5, 10:34:56;
- the go, c751f77, 10:38:33;
- first test call 10:39:24 and last 10:41:59 (`t_utc`);
- scores committed in 8d9ef0e at 10:42:45;
- results 4f90f23 at 10:43:27.

Opus's archive was public before the pre-registration. It set the context for the bar ("Opus margined only 0.036"), but it is not data for the two models tested.

**A2. Rule, statistic, split, seed and budget match: holds.**
- `passes()` reads C1 < 0.25, and C2 and C3 < −0.01, on the item and cluster bootstraps with EPS. Its logic is unchanged between 012449c and HEAD: the only edits to `score_f1.py` are D69's sentence edits.
- The seed is 20261104, fixed.
- The budget went from $0.70 to $0.85 by br-010 and D69 (10:34). Both are dated before the first test call, and the results header states them.

**A3. Bar not lowered: holds.** D69 changed the cap, the sentences, the dry-run check and the prior-work row, not the bar.

**A4. Primary statistic is the pre-registered one: holds.** C1–C3 per model on round 1. Round 2 and the Opus rows are labelled as reported.

**B5. Ties: holds.** Brier has no ties. Accuracy gives 0.5 credit to p = 50 (Sonnet 2, Opus 1). Randomised, Sonnet's accuracy is 0.767 or 0.784. This is secondary only. No p fell outside 3–97, so clipping never bound.

**B6. Pooling: holds, with a note.** Split by option order:
- Haiku: C3 −0.016 (Option 1 = a, n 53) and −0.031 (b, n 63).
- Sonnet: −0.061 and −0.067.

Neither model's sign depends on the order. Haiku's mean p_option_1 is 46.2 and Sonnet's 50.1, so there is no strong pull.

The pooling that matters is inside C3: tagged and untagged items. C3 pools 38 items where the rule bets with 78 where it is a coin:

| model | C3 on 38 tagged items | C3 on 78 untagged items |
|---|---|---|
| Haiku | +0.024 [−0.060, +0.107] | −0.048 |
| Sonnet | −0.027 [−0.109, +0.053] | −0.082 |
| Opus | −0.060 [−0.130, +0.008] | −0.072 |

This is pre-registered (§2 and §6 say the rule is weakened), so it is not a hole in the verdict. It is a hole in how the plain English reports Sonnet's win (C15, cut 2).

**B7. Few items: holds.** Leave-one-item-out flips neither label. My own leave-one-paper-out (108 papers) flips neither. Leave-one-field-out flips Sonnet on interpretability (C3 upper bound −0.009 item / −0.011 cluster), and the results report that. Haiku's C3 upper bound stays above −0.01 whichever field is dropped (+0.009 to +0.028).

**B8. Circular estimators: holds.** Nothing is fitted. The up-word list and the headline tags predate the run (de6b5dc and round 1's items).

**B9. Baselines: holds, with the stated limit.** These were run: always-50%, the up-word rule (worse than a coin, 0.316, as §6 foresaw) and the headline-tag rule. The strongest fair rival is a flattery rater that bets on every round-1 item, and it was not run on round 1. On round 2, where it was run, Sonnet ties it. Both the results file and §6 say this. The design review's D5 table of dumb rules (best Brier 0.236) is beaten by both models.

**B10. Uncertainty: holds.** Item and paper-cluster bootstraps (108 clusters), with the bar read on both. Haiku's C3 sits near its edge, and both intervals are reported. My independent bootstraps with five other seeds give upper bounds of 0.0111–0.0116, all above −0.01. As a one-sided sign-flip test of Haiku's C3 against the −0.01 margin, p = 0.22.

**B11. Multiple comparisons: holds.** There is one conjunction (2 models × 3 conditions × 2 bootstraps), uncorrected and strict, as §4 states. The round-2 rows are reported uncorrected and labelled.

**B12. Leakage: holds.** No fitting step. The items are post-cutoff for all three models (the design review's D7 cites the platform's June 2026 cutoff). I could not check that cutoff independently.

**C13. Scope drift: holds.** The results file has "No 'smaller models' or 'LLMs' claim beyond these two", and none appears.

**C14. Rank drift: hole (cut 2, cut 3).** "Sonnet did as well as Opus" leads the plain English, and the Novelty line repeats it as "Sonnet matches Opus". The Opus comparison is a reference row with no pre-registered test, and the thinking settings differ. The paired difference is +0.004 [−0.018, +0.027]: not shown different, and not shown equivalent. The wording should say that, with the paired interval.

**C15. Mechanism drift: hole (cut 2).** "It beat the good-news rule by 0.064 … well past the margin" is true of the statistic. But read beside §1's framing, it says Sonnet beat the publication-bias rival, and the data do not show that where the rule bets (B6 table). The results file mentions the 38-of-116 limit only under "Settings" and "What it cannot do", not next to the claim.

**C16. Plain English against the table: hole (cut 1).** Every plain-English number matches the regenerated tables and sentences:
- 77.6, 76.3, 0.168, 0.163, 0.064 (0.028–0.099);
- 70.7, 0.208 (0.181–0.236), 0.024 (−0.011 to 0.059);
- +0.002 (−0.021 to +0.026), +0.037, −0.036, 0.316, 38 of 116.

The table itself does not regenerate. The results file's round-1 table gives Haiku n = 106, and the archive has 116 (116 round-1 primaries, all parsed, all scored). `score_f1.py` prints 116, and so do the verdict sentence ("On 116 (Haiku) and 116 (Sonnet)") and `scoring/f1-tables.md`. The cell was 116 at the results commit 4f90f23 and became 106 in d3f8201 (`git diff 4f90f23 HEAD`), a commit whose message names only the Novelty line. The other table cells and all five sentences match byte for byte.

**C17. Citations: holds.** The ss-b10 92% figure is in ss-b10-results.md (0.92 [0.79, 1.07]). The Novelty citations are checked under F27.

**C18. Negatives stated plainly: holds.** Haiku's miss, the scored-as-a-miss outcome, Sonnet's field fragility and the round-2 tie with the flattery rater are all stated in the plain English.

**D19. Budget: holds.**
- `BET_CAP` is 0.85 and the program cap is checked in `Caller` before every call.
- Spent: $0.6264 for the test (Haiku $0.030, Sonnet $0.596) plus $0.0371 for the pilot, $0.663 in all.
- The cache has 416 keys, equal to the 416 planned keys, so there was no extra call.

**D20. Stop-on-refusal: holds.** 0 refusals. 416 distinct request ids, one per planned key, so nothing was retried. There is no `results/refusal.md`.

**D21. One scale direction: holds.** The prompt says "1 means Option 1 is almost certainly not the reported result; 99 means Option 1 almost certainly is" (`bettor.py` SYSTEM), and it is the only scale.

**D22. Replication: holds.** Not a pass, and no hit is claimed. Sonnet meeting the rule is reported as one model's result.

**E23. Seed: not applicable.** `seed_source: fixed`: there is no draw, and the option order comes from round 1's and round 2's archived seeds. I verified the order: 116/116 and 92/92 match Opus's archive, and 416/416 bets match the plan (my own check, with the client modules stubbed; `anthropic` is not installed in this clone, so no call was possible).

**E24. Tiebreak: not applicable.**

**E25. Lesson: holds.**
- The §0 lesson row is in 012449c.
- `ls-ss-b13` in `ledger/lessons.jsonl` has the same sentence. It was added at 8e6b1c9 (10:15:01), after the pre-registration commit and before any call.
- The `read` block matches the ledger at 012449c: 37 scored, Brier 0.188, 12/37, newest audit `ng-p3-18.md` (09:06).
- P3's `do_this` (beat the dumbest passing predictor by a margin) is in the design as C2 and C3 with a 0.01 margin.
- P14's (a cluster bootstrap beside the item one, saying which the bar is read on) is in the design as the paper-cluster bootstrap, with the bar read on both.
- The odds change 0.45 → 0.18 is on the map at b42b3d6 (10:12:29), before the pre-registration.

**E26. Design review: holds.** The review (247d484) came after the pre-registration and before any call, with verdict fix-first and five fixes. All five are in D69 (10:34), dated before the first test call, and the review confirmed them at c751f77 before the run. Its D4 had already named the 78-of-116 abstention and the live rival. I found no flaw that D1–D12 should have caught.

**F27. Novelty line: verdict holds; wording holes (cut 3, cut 4); one record hole (cut 5).**

The line exists in the plain-English section. It names its search and model (claude-opus-5-5, a fresh subagent). The ledger row carries `novelty: partly new`, the same `novelty_line` and `novelty_by`.

Papers opened:
- **BrainBench (arXiv 2403.03230, HTML v4).** "Smaller models such as Llama2-7B and Mistral-7B … performed comparably to larger models" and TinyLlama "falling much behind the 7B models" are both verbatim. There is no publication-bias baseline. Holds.
- **SciPredict (arXiv 2604.10718, HTML, Appendix C Table 3, NBK, All Domains).** Sonnet 4.5 22.55 ± 0.75, Opus 4.5 23.05 ± 0.51, Llama 3.1 8B 14.65 ± 1.03. There is no Haiku and no publication-bias baseline. Holds.
- **Hewitt, Ashokkumar, Ghezae and Willer (2024-08-08 PDF, text extracted).** "the accuracy of LLM-derived predictions has improved steadily and markedly across generations of LLMs, between GPT3 Babbage … and GPT-4" is verbatim. Holds.
- **Wen et al. (arXiv 2506.00794, HTML).** Neither "publication bias" nor "positive result" appears. Holds.
- **CUSP (Wu et al., arXiv 2605.22681, HTML).** It has an always-No baseline (57.03% on binary), and also chance (50% binary, 25% MCQ) and a mean-date baseline for timing. **"Has only an always-No baseline" is wrong in its letter.** The point it supports holds: there is no publication-bias or positive-result baseline.

The verdict word follows. The size pattern is in print (one tier down ≈ top; much smaller is worse), and a same-family test against a publication-bias rule or a flattery rater is not. So "partly new" is right.

**My search** (header) used clinical-trial forecasting words. It found Jin et al., "Can artificial intelligence predict clinical trial outcomes?" (arXiv 2411.17595, opened). GPT-4o-mini predicted every trial a success (recall 1.000, specificity 0.000, balanced accuracy 0.500), while GPT-4o did slightly better (0.532). That is a smaller same-family model collapsing onto a "positive outcome" rule. But it reports no positive-result baseline, uses balanced accuracy, and uses trials before each model's cutoff. It is adjacent, not a prior statement of this result. The line is not wrong to miss it, and citing it would strengthen the line.

Wording holes in the line:
- "Sonnet matches Opus" is the C14 problem.
- "the result that Haiku beats a coin but not the good-news rule … is new" drops "by the margin". Haiku's point estimate does beat the rule (−0.024). It is not shown to beat it by 0.01.
- The CUSP clause, above.

Record hole: the ledger row's `novelty_at` is "2026-11-05 11:00 America/Denver", but the commit that wrote it, d3f8201, is dated 10:51:34. This is a hand-typed time ahead of the clock, the class D63 corrected.

**Reproduce.** `python3 programs/settled-science/reproduce.py` matches every program table and `scoring/f1-tables.md` and `scoring/f1-scores.json`, then stops with "NOT REPRODUCED: first mismatch results/ss-b13-results.md". The one regenerated difference is the Haiku n cell (106 against 116). I diffed every table row and quoted sentence in the results file against `f1-tables.md`, and nothing else differs. The verdict and every statistic regenerate. The results file as committed does not.

My other commands, all $0, were own scripts on `f1-bets.jsonl`, `bets.jsonl` and `items.jsonl`:
- independent bootstraps with five other seeds;
- tagged and untagged splits;
- option-order splits;
- paired model differences;
- a sign-flip test;
- leave-one-paper-out;
- the plan-versus-cache-versus-archive check.

## The pre-mortem, scored

**Disclosure first.** The pre-mortem sits in §0's table of the pre-registration, and again in the ledger row, so I read it when I read the pre-registration at its commit, before the checklist. My failure reason below comes from the data, but it was not written blind.

**Own account.** The bet failed because Haiku's C3 upper bound (+0.011 item, +0.012 cluster) is not below −0.01. Haiku's Brier is 0.024 below the good-news rule's, a 2.4-point margin with a 7-point-wide interval, and on the 38 items where the rule bets Haiku is worse than the rule (+0.024). Kind: `world`. The run was clean, the design worked as written, and no artefact produced it.

**Pre-mortem:** "If this fails, the most likely reason is that Haiku's Brier on the 116 items is not 0.01 below the good-news rule's 0.232: its weaker priors leave it close to the publication-bias shortcut." Kind: `world`.

**Score: named.** It names the model (Haiku), the condition (C3 against the good-news rule at the 0.01 margin) and the kind, and that is what failed. Strictly, Haiku's mean Brier is 0.024 below the rule's (0.208 against 0.232), more than 0.01. The miss is the upper bound, not the mean. "Weaker priors" is not tested.

## Required cuts

1. **Table cell (C16, reproduce).** In "## Tables", round-1 table, Haiku row, change `| Haiku | 106 |` to `| Haiku | 116 |`. After this, the ss-b13 results file's tables match the regenerated ones (every other row and sentence already matches).

2. **Sonnet bullet (C14, C15).** Replace
   "**Sonnet did as well as Opus.** It was right 77.6% of the time (Opus 76.3%), Brier 0.168 against Opus's 0.163, and it beat the good-news rule by 0.064 (interval 0.028 to 0.099), well past the margin."
   with
   "**Sonnet was not shown different from Opus.** It was right 77.6% of the time (Opus 76.3%), Brier 0.168 against Opus's 0.163 (paired difference +0.004, interval −0.018 to +0.027; no equivalence test was pre-registered). It beat the good-news rule by 0.064 (interval 0.028 to 0.099), past the margin, but most of that gain is on the 78 items where the rule says 50%. On the 38 items where the rule bets, Sonnet's gain was 0.027 (interval −0.053 to 0.109), not shown (Opus's 0.060, interval −0.008 to 0.130, also not shown)."

3. **Novelty line, size sentence (C14).** Replace "Ours agrees on the size pattern: Sonnet matches Opus (Brier 0.168 against 0.163) and Haiku is weaker (0.208)." with "Ours agrees on the size pattern: Sonnet is not shown different from Opus (Brier 0.168 against 0.163; paired difference +0.004, interval −0.018 to +0.027) and Haiku is weaker (0.208; paired difference from Opus +0.044, interval +0.012 to +0.076)."

4. **Novelty line, CUSP and "new" sentences (F27, C16).** Replace "Wen et al. (2025, arXiv 2506.00794) do not mention publication bias, and CUSP (Wu et al., 2026, arXiv 2605.22681) has only an always-No baseline. So the result that Haiku beats a coin but not the good-news rule, and that neither smaller model beats the flattery rater, is new." with "Wen et al. (2025, arXiv 2506.00794) do not mention publication bias, and CUSP (Wu et al., 2026, arXiv 2605.22681) has always-No, chance and mean-date baselines but no publication-bias one; Jin et al. (2024, arXiv 2411.17595) found GPT-4o-mini predicting every clinical trial a success, a smaller same-family model collapsing onto a positive-outcome rule, but report no such rule as a baseline. So the result that Haiku beats a coin but is not shown to beat the good-news rule by the 0.01 margin, and that neither smaller model beats the flattery rater on round 2's items (a reported row), is new." The verdict word stays `partly new`, and the same text goes to `novelty_line` in `ledger/bets.jsonl`.

5. **Ledger record (F27).** In `ledger/bets.jsonl`, ss-b13 row, change `novelty_at` from "2026-11-05 11:00 America/Denver" to the commit time "2026-11-05 10:51 America/Denver" (d3f8201), with a note, as D63 did. This is not a results-file sentence.

## What would break it next

The verdict is mixed, and only the Sonnet half could move. The cheapest test that could overturn Sonnet's "met" is to run the archived Opus flattery rater (ss-b6's "which version is better news for the paper's method" prompt, unchanged) on round 1's 116 items in the same option order. That is 116 Opus calls, about $0.30 at round 1's measured tokens. Then score Sonnet's C3 against that rater instead of the headline tag, on item and paper-cluster bootstraps at the 0.01 margin.

If Sonnet does not beat the rater by the margin, as it does not on round 2 (+0.002), then neither smaller model is shown to beat a good-news judgment applied to every item. The defensible reading of ss-b13 would become "beats a coin, not shown to beat the publication-bias rival". A Haiku order check (about $0.02, design review D7) would also show how much of Haiku's miss is position rather than knowledge.
