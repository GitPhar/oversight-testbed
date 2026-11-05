---
bet: ss-b12
program: settled-science
prereg_commit: 0e81ddc
results_commit: 1efe6c5
auditor_session: fresh auditor subagent (Claude Code), audit clone "/Users/seanpharris/oversight-testbed-audit-ss-b12 1efe6c5"
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true          # author, design reviewer, bettor and auditor are all claude-opus-5-5
date: 2026-11-05 07:24 America/Denver
claims_checked: 16
holes_found: 5
overclaims_cut: 4
reproduced: true
verdict_claimed: null
verdict_after_audit: null
verdict_stands: true
canary: unknown
false_alarms: 0
design_review_missed: [D2]       # minor: arXiv submission date used as "first posted"; one older item (f4-021) was first public in late July 2026
failed: true
failure_reason: "design: at about 93% right on both sides, 40 older items could only see an advantage of about 0.04-0.05 in Brier, so the observed -0.008 [-0.044, 0.031] cannot tell no advantage from a round-1-sized one"
failure_kind: design
premortem_score: named
risk_seen: null
---

# Audit of ss-b12: is the bettor's advantage on older papers recall?

## In plain English

The null verdict stands. The tables regenerate exactly from the archive, the run followed the pre-registration as amended before data (D57, D58), and nothing was fetched or called before the design review's go. No re-analysis changes the label: other recognition rules, my own reading of the 43 older rationales, leave-one-item-out, leave-one-bucket-out, and dropping the one older item that was public only after the cutoff all leave the upper bound above zero. Four sentences of the write-up say more than the record does, and they must be rewritten:
- the bold plain-English sentence turns "not shown" into "there is no advantage";
- the leakage checker did not drop "more" of the older items (59% against 60%);
- only one of the flagged rationales names the paper's own authors;
- the "silent memory" bullet implies a missed recall that the rule in fact caught.

The test is weak. It can see only an advantage of about 0.04–0.05 in Brier, and the round-1-sized advantage it was built to look for lies inside its interval. A larger draw from the 2024–2025 windows is the cheapest test that could overturn it.

## The case that this result is false

The headline is that the bettor shows no advantage on older papers beyond recall. Its interval, −0.044 to +0.031, runs from an advantage larger than any round-1 estimate to a small disadvantage. The design review's own worlds put the round-1-calibrated advantage at about 0.015–0.025 in Brier, and this test passes such a world only 10–30% of the time. So a null here is what one would expect whether or not the advantage exists. The data also hint that it does. The oldest window, the one most likely to be in training data, scores 0.022 on 11 unrecognised items: all 11 right, and −0.050 [−0.077, −0.023] against the newer side, permutation p = 0.014. The 2026H1 third is 19 of the 40 items. Those papers were posted in the four weeks before the stated June 2026 cutoff and may be effectively unseen, so they can dilute any memory effect toward zero. One of them (f4-021, arXiv 2607.22653) was not public until late July. The selection also works against an advantage. A Claude leakage checker that may know the older papers dropped 59% of them, and if it drops the ones it recognises, the survivors are the ones the bettor knows least. Finally, the word rule only catches recall the model mentions, and the null rests on three wrong older items: drop those three and the test passes. On this reading, the result is "a small, diluted, selected-against test saw nothing", not "no advantage beyond recall".

The checklist below finds that this case is right about the wording and wrong about the verdict. The pre-registered rule says null, and every re-analysis agrees. The window heterogeneity is not significant (permutation p = 0.20). The 2024 row is mostly 11 of 11 right, which has probability 0.45 at the common 93% rate. The results file already labels it descriptive. But "there is no advantage on older papers beyond recall" cannot stand.

## Claims checked

| # | claim (quoted or paraphrased from the results file) | check run | outcome |
|---|---|---|---|
| 1 | Verdict null; 40 vs 89 items, Brier 0.063 vs 0.071, d −0.008 [−0.044, 0.031] | `score_f4.py` rerun, `reproduce.py` | holds (byte-identical outputs) |
| 2 | "A permutation test agrees (p = 0.35)" | rerun; own perm | holds (0.349) |
| 3 | "So, on these template items, there is no advantage on older papers beyond recall." | rule §5 vs table | **hole**: the interval does not exclude an advantage (cut 1) |
| 4 | "an advantage below about 0.05 in Brier could not reliably have been seen" | normal MDE; resampled power at n = 40/89 | holds (0.054 normal; 80% power near 0.035–0.04 in a scaled world) |
| 5 | "both sides are already about 93% right" | table | holds |
| 6 | "only 3 of the 43 older rationales were flagged" | `recognised2` on f4-bets | holds (f4-001, f4-015, f4-033) |
| 7 | "(2024 and 2025 papers, two naming the paper's authors)" | rationales against `pool.json` author lists | **hole**: f4-033 names "Balagansky et al."; the authors are Balcells, Lerner, Oesterle, Ucar, Heimersheim (cut 2) |
| 8 | "a Claude leakage checker dropped more of them (61 of 104) than of round 2's newer candidates (146 of 243)" | leakage-status files | **hole**: 58.7% against 60.1%, so fewer, not more; the tables section says "The rates are close" (cut 3) |
| 9 | "The engine gave this 20%; Sean gave it 100%." | prereg §0 | holds |
| 10 | Pre-registered sentence (33 July–August; 3 of 43 and 3 of 92 flagged) | `f4-scores.json` | holds |
| 11 | Tables (sets, differences, item mix, rule gaps, windows, buckets, LOO flips 0) | `reproduce.py` "match … (6 table(s))" | holds |
| 12 | Leakage drop 61/104 and 146/243 | `items/f4/leakage-status.json`, `items/r2/leakage-status.json` | holds |
| 13 | 2024 row descriptive, three windows looked at | own window tests | holds (Bonferroni-3 interval [−0.083, −0.018]; heterogeneity p = 0.20; caveat adequate) |
| 14 | "One older rationale names 'the OpenAI confessions paper' without a citation" (Silent memory bullet) | f4-015 flags | **hole**: true literally, but f4-015 is flagged by both rules ("As I recall"); the bullet implies a miss (cut 4) |
| 15 | Spend $0.51 (104 leak, 43 bettor), program $7.75 of $8.25, 0 refusals | cache sums | holds ($0.3008 + $0.2055; program caches $7.7459; run status complete/complete) |
| 16 | Timeline: go 07:08:36, fetch started 07:09:17, calls 07:10–07:12 | author times, `pool.json` stamp, request ids | holds as far as checkable (see A1) |

## Checklist

**A. Was it pre-registered as claimed?**

1. *Pre-registration before data:* **holds.** Author times:
   - code `8140cf6` 06:44:41;
   - prereg `0e81ddc` 06:45:36;
   - seed `9e6ee65` 06:46:50;
   - design review `bd0e782` 07:02:55;
   - fixes D57 `52fd0a4` 07:05:58;
   - go `7aecdf4` 07:08:36;
   - D58 `988d227` 07:09:09;
   - results `1efe6c5` 07:13:31.

   No f4 data file, cache or run-status file appears in any commit before `1efe6c5` (`git log -- items/f4 bettor/f4-*`). `pool.json` records `fetched: 2026-11-05 07:10 MST`, the time written at the end of the fetch. The caches carry no timestamps. Their request ids (leak `req_011Cgjv69a…`–`…v9Eew`, bettor `…v9am…`–`…vAnY`) all sort after the last ss-b10 BrainBench call (`…v3JC6T`), and ss-b10's calls could start only after its go at 07:03:17. The reviewer's addendum at 07:08 records that `items/f4/` and both f4 caches did not exist. The code was unchanged after `988d227`; only data and results were added. Clone note: the clone ends at `813b2c5`, one ledger-only commit (em-gm2q) after the results commit. Its directory name contains a space and the hash.
2. *Rule, statistic, split, seed, budget match:* **holds.** The pass rule (upper bound < 0, tolerance 1e-12), the statistic (item Brier, independent per-side percentile bootstrap, 10,000 resamples, `default_rng(20261104)`, bounds int(0.025n), int(0.975n)−1), the 30-item untestable floor, the seeds and the $0.75 cap are in the code as pre-registered. The binding recognition rule changed from RECOG to `recognised2`, the sentences changed, and the permutation p and item-mix secondaries were added. All are in D57 (07:05) and D58 (07:09), before the fetch. The frozen rule is still reported.
3. *Bar not lowered:* **holds.** The bar is unchanged. D57's rule change was made before any f4 rationale existed and moves toward a stricter test of the pass.
4. *Primary is the pre-registered primary:* **holds.**

**B. Is the number real?**

5. *Ties:* **holds.** Brier is continuous. The permutation uses ≤ obs + EPS. No item has p = 0.5.
6. *Pooling:* **holds, with a note.** The three older windows are pooled by design. Unpooled, they read 2024 −0.050, 2025 +0.026 and 2026H1 −0.002. A permutation test of between-window spread gives p = 0.20, so pooling hides no detectable heterogeneity. Both sides have the same up-word share, 0.77.
7. *Few items:* **holds.** There are no leave-one-item-out flips, and the upper bound ranges from 0.020 to 0.037 over all 129 drops. No leave-one-bucket-out flip either. In numbers, the null rests on the three wrong older items (f4-024, f4-029, f4-038): drop the worst two and the upper bound is +0.006; drop three and it is −0.008, a pass. That is the ceiling at work, not one item carrying the result.
8. *Circular estimators:* **holds.** The recognition rule is answer-free. It reads the rationale, plus the item's own question and options for the year clause.
9. *Baselines:* **holds.** The up-word and swap-pair rule gaps are reported: +0.013 [−0.065, 0.093] and −0.031 [−0.111, 0.052]. Neither shows an item-mix gap.
10. *Uncertainty:* **holds.** Intervals are at the item level, and a permutation p is reported beside the bootstrap. The field jackknife over 4 clusters ([−0.030, 0.013]) is narrower than the item bootstrap. With k = 4 it is not informative, and it is correctly kept secondary.
11. *Multiple comparisons:* **holds.** There is one primary. Windows (3) and buckets (4) are descriptive, and the file says so.
12. *Leakage:* **hole (minor; no cut required; not verdict-changing).** No test label reaches a fitting step. But the pre/post boundary uses the arXiv `published` (v1 submission) date. f4-021 (arXiv **2607**.22653, "submitted" 2026-06-26) received a late-July identifier, so it was first public after the stated cutoff. It is the only older item whose id month differs from its v1 month. Dropping it gives d = −0.008 [−0.045, 0.033], still null. "40 papers first posted between January 2024 and June 2026" is therefore true of 39 by first public appearance.

   **Recognition rule, read by hand (all 43 older rationales).** I read every older rationale against its paper's title and author list.
   - **True recall, flagged:**
     - f4-001 names "Google's color code paper (Lacroix et al., 2024)". Correct first author. The quoted "abstract says…" is copied from the option text.
     - f4-015 names "the OpenAI confessions paper" and adds "As I recall". The paper is correct.
   - **Flagged, but a misidentification:** f4-033 names "Balagansky et al.", who is not an author of 2410.08869. Its Brier of 0.062 shows no recall benefit.
   - **Borderline, unflagged, judged not recall:**
     - f4-020 says "the study of literary MT judged by readers' highlights". "Readers' highlights" is in the option text.
     - f4-017 names a different paper as a guess and says "Without knowing the paper".
     - f4-007 cites related "circuit QAD work", not this paper.

   No clear miss. Rule variants:

   | rule | n older / newer | d [95% CI] | perm p | label |
   |---|---|---|---|---|
   | binding (`recognised2`, primary) | 40 / 89 | −0.008 [−0.044, +0.031] | 0.349 | null |
   | no filter | 43 / 92 | −0.009 [−0.044, +0.028] | 0.328 | null |
   | frozen RECOG | 42 / 92 | −0.008 [−0.042, +0.029] | 0.355 | null |
   | auditor's reading (drop f4-001, f4-015; newer all 92, since post-cutoff papers cannot be recalled) | 41 / 92 | −0.007 [−0.042, +0.032] | 0.380 | null |
   | strict (also drop f4-007, f4-017, f4-020) | 37 / 89 | −0.011 [−0.050, +0.030] | 0.307 | null |
   | binding, r2-084 ("well-known results", a generic false flag) kept | 40 / 90 | −0.007 [−0.044, +0.031] | 0.371 | null |
   | drop f4-021 (public after cutoff) | 39 / 89 | −0.008 [−0.045, +0.033] | 0.359 | null |
   | 2024 + 2025 windows only | 21 / 89 | −0.014 [−0.058, +0.041] | 0.334 | null |

   **Window split.** The bootstrap intervals were recomputed, and the permutation p is one-sided:

   | window | n | d [95% CI] | perm p |
   |---|---|---|---|
   | 2024 | 11 | −0.050 [−0.077, −0.023] | 0.014 |
   | 2025 | 10 | +0.026 [−0.054, +0.125] | 0.76 |
   | 2026H1 | 19 | −0.002 [−0.044, +0.047] | 0.51 |

   The 2024 Bonferroni-3 interval is [−0.083, −0.018], but 0 of 11 wrong has probability 0.45 at 93%, and the percentile bootstrap cannot draw a wrong item from a side that has none. It is descriptive, as the file says.

   **Power at the realised n (40 against 89; item Brier sd 0.099 and 0.107).**
   - Normal approximation, 80% power at one-sided 2.5%: MDE 0.054.
   - A resampled world, with older Brier equal to newer × s, 600 simulations each with 2,000 bootstrap resamples:

     | true advantage | 0 | 0.014 | 0.029 | 0.043 | 0.050 |
     |---|---|---|---|---|---|
     | P(pass) | 0.06 | 0.19 | 0.52 | 0.94 | 0.99 |

   So "about 0.05" is fair to slightly conservative. The bootstrap passes 6% in the no-effect world, as the design review found.

   Scripts: `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/6509f5b7-80b2-4dab-9f54-37652f9d2839/scratchpad/ss-b12/reanalyse.py` and `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/6509f5b7-80b2-4dab-9f54-37652f9d2839/scratchpad/ss-b12/power.py`, run on the archive at $0.

**C. Does the write-up say only what the data say?**

13. *Scope drift:* **holds.** "On these template items" and "One bettor (claude-opus-5-5 at effort low)".
14. *Rank drift:* **holds.** The 2024 row is labelled descriptive.
15. *Mechanism drift:* **hole** (with 16). "There is no advantage on older papers beyond recall" asserts an absence and a cause the test cannot show. → cut 1.
16. *Plain English matches the table:* **hole**, three sentences:
    - "there is no advantage…" → cut 1;
    - "two naming the paper's authors" (only f4-001 does) → cut 2;
    - "dropped more of them (61 of 104) than … (146 of 243)" (59% against 60%; the tables section itself says "The rates are close") → cut 3.

    Also, in "What it cannot do", the confessions-paper sentence implies a miss the rule caught → cut 4.
17. *Citations:* **holds.** No external source is cited. Internal references (ss-b3, ss-b5, D57, D58, br-005) say what they are cited for.
18. *Negative stated plainly:* **holds**, apart from cut 1. The null, its power limit and the round-1 caveat are all stated.

**D. Process**

19. *Budget:* **holds.** `BET_CAP = 0.75`, and `cap()` counts both f4 caches inside `min(BUDGET_USD, …)`. Spend was $0.5063 for this bet. The program total from `common.CACHES` is $7.7459 of $8.25. The br-005 ruling is in `ledger/spend.jsonl` (06:44), before the prereg.
20. *Stop-on-refusal:* **holds.** `f4-run-status.json` reads leak complete and bet complete. No `results/refusal.md` change in range. 43 primary rows for 43 items, and a maximum of 241 output tokens.
21. *One scale direction:* **holds.** 1–99 on option 1, mapped to p_true.
22. *Unreplicated:* not applicable (null).

**E. Engine records**

23. *Seed:* **holds / cannot check in part.**
    - Pulse 1592290 at 13:46:00.150Z follows the commit at 13:45:36Z. The recorded previous pulse, 1592289 at 13:45:00.178Z, precedes it. I did not refetch the beacon.
    - `ledger/seed.py` reproduces items 2418064898708106585 and order 8371102074377508067.
    - The 104-item sample and all 43 option orders recompute exactly from those seeds.
    - Leakage status matches the cache, and items equal the clean sample.
    - No f4 item overlaps round 2's candidates.
24. *Tiebreak:* not applicable.
25. *Lesson:* **holds.**
    - The §0 lesson is in `0e81ddc`, and `ls-ss-b12` carries the same sentence.
    - The read block (28 bets, Brier 0.202, 8/28) matches `ledger/brier.md` at `0e81ddc`, after D55's ledger-only correction.
    - P8's do_this (name the bundle) entered via D57 F3. P14's (cluster check) is pre-registered as the field jackknife and leave-one-bucket-out, with the bar on the item bootstrap.
    - The 63-word overrun is disclosed.
    - ss-b12 is not yet in P8's or P14's `cited_by`. That is ledger bookkeeping, not a hole in this result.
26. *Design review:* **holds.** It was committed at 07:02:55, after the prereg and before the fetch at about 07:09. The verdict was fix-first. All five fixes are in D57, dated 07:05 before data, confirmed at 07:08:36, and the confirmation's wording note is D58 at 07:09:09, before the fetch. I checked `test_recog_f4.py` ("all 20 labels right"). **Missed:** D2, minor. The date manipulation used arXiv's submission date, and one older item (f4-021, id 2607.22653) was not public until late July 2026. It changes nothing here, but a stricter pre/post boundary would use the identifier's month or the announcement date.

## The pre-mortem, scored

My failure reason, written before scoring: *design: at about 93% right on both sides, 40 older items could see only an advantage of about 0.04–0.05 in Brier, so −0.008 [−0.044, 0.031] cannot tell no advantage from a round-1-sized one.* Kind: `design`. Disclosure: the pre-mortem sits in §0 of the pre-registration, which item A2 requires reading word for word, so I saw it before the checklist. The reason above rests on the power and interval numbers in item 12, not on the pre-mortem's wording.

Pre-mortem (prereg §0, `0e81ddc`): *"If this fails, the most likely reason is a ceiling: template items are already 93% right after the cutoff, so a real pre-cutoff advantage of a few hundredths cannot clear zero with about 50 items."* Kind: `design`.

**Score: named.** The bet failed (null), and the mechanism is the one named. Both sides were 93% right. The interval spans −0.044 to +0.031, and 80% power needs an advantage of about 0.04–0.05. The realised n was 40, below the "about 50" stated.

## Required cuts

1. Plain English, second paragraph. Replace
   > So, on these template items, **there is no advantage on older papers beyond recall.**

   with
   > So, on these template items, **this test found no advantage on older papers beyond recall**; it cannot rule one out.
2. Plain English, third paragraph. Replace
   > (2024 and 2025 papers, two naming the paper's authors)

   with
   > (two 2024 papers and one 2025 paper: one names the paper's first author, one calls it "the OpenAI confessions paper", and one names an author, Balagansky, who is not on the paper)
3. Plain English, third paragraph. Replace
   > and a Claude leakage checker dropped more of them (61 of 104) than of round 2's newer candidates (146 of 243).

   with
   > and a Claude leakage checker that may know the older papers dropped 61 of 104 of them (59%), close to its 146 of 243 (60%) on round 2's newer candidates.
4. "What it cannot do", Silent memory bullet. Replace
   > One older rationale names "the OpenAI confessions paper" without a citation.

   with
   > One older rationale (f4-015) names "the OpenAI confessions paper" without a citation; the rule flagged it only through "As I recall".

## What would break it next

The cheapest test that could overturn the null is a larger, older draw, with $0 spent here.
- Use round 2's four queries in the 2024 and 2025 windows only, at 300 papers per window per query: 24 arXiv requests, free.
- Drop any paper whose arXiv id month is after June 2026.
- Leakage-check every candidate before sampling: about 200 Sonnet calls, about $0.60.
- Run the Opus bettor on the clean ones: about 80–90 calls, about $0.45.
- Total about $1.05. That needs its own budget ruling, because program 4 has $0.50 left.

Pre-register the same rule with the 2024 window as one named secondary. At about 85 older items against 89 newer, 80% power is near 0.03 in Brier, which reaches the round-1-sized advantage this bet could not see. The leakage-selection rival is separate. Re-running the leakage check with a non-Claude checker on the 61 dropped older items costs about $0.20, and it would show whether Sonnet's drops track recognition. That would need its own pre-registration.
