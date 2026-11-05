---
bet: em-dm6f2f1
program: entangled-mind
prereg_commit: 0d7e98a
reviewer_session: fresh design-review subagent, main checkout read-only (seed commit bb6a99b read; scratch scripts under /private/tmp/claude-501/-Users-seanpharris-oversight-testbed/e93ce59f-1dc3-4451-8206-bee8c0537bfa/scratchpad/review-dm6f2f1/)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 07:41 America/Denver
checks: {D1: holds, D2: holds, D3: holds, D4: flaw, D5: holds, D6: holds, D7: holds, D8: flaw, D9: flaw, D10: flaw, D11: holds}
flaws: 3
pilot_usd: 0.00
verdict: fix-first
confirmed_at: null
---

# Design review of em-dm6f2f1

## In plain English

As built, the test can both pass and fail, and a pass would mean something: in worlds where 'no' guesses simply carry lower numbers in every format, it passes at most 3% of the time. But the real archive is smaller than the design assumes. 63 science questions are usable, not about 94. Of these, 18 are flagged only in the probability format and **7** in all four cells, not "two groups of about twenty". On these numbers the rule comes down to one count. If nearly all 18 probability-only questions are 'no' guesses, the bet passes when at most 3 of the 7 both-format questions are 'no' guesses, and fails at 4 or more. The proposed-answer reading itself predicts some 'no' guesses in that group of 7, because em-dm6 measured the same reading in the frequency format for 14–19% of Sonnet's 'no' guesses. So guard (b) can fail even when the reading is true. In referent-reading worlds built on the real numbers, the bet passes 3–77% of the time, depending mostly on how a handful of uncertain questions are guessed. Three things need fixing before the run, and none of them moves the bar:
1. The leave-one-out check must also cover the 7 both-format questions, which is where the verdict hangs.
2. The "part (a) holds, guard (b) does not" fail needs its own sentence. Without it, the fail sentence would say the probability-only flags were "not shown to be mainly 'no' guesses" even if 17 of 18 were.
3. The record must state the real group sizes and the parent audit's exact parse counts.

## What I measured on real data (and what I did not)

All from `results/cal-sonnet-conversations.json` and `results/pool-run-3.json`, whose sha256 values match the code's pinned values (76e2e55c…, 8011ae79…). The script's only write path was not run. I never ran `--seed`. I never read the *value* of any guess (yes or no): no share of 'no' in any group, and no table of guess against group. What I did read:

- **Parse status.** I counted whether `turns[0].guess` is null or not, by cell and category. Science, P r0: 38 of 60 chemistry and 29 of 60 physics are non-null. Claim questions: 0 in every cell. (The em-dm6f2 audit's "`guess` is null in the archive" is not right for science. About half are parsed.)
- **Science questions.** All 120 read "… Is the (correct) answer X?". The gold labels are 60 yes and 60 no. 115 have fresh cells, 94 have a number in all four cells (em-dm6f2's matched set), and **63** of those have a parsed P r0 guess (the usable set: chemistry 34, physics 29). The 31 matched-but-unparsed questions all have a `Guess:` line with an open-form answer (for example "43 ft").
- **Flags per cell, usable set** (P r0 / P r1 / F r0 / F r1): 32 / 34 / 16 / 17. In the matched set: 46 / 48 / 20 / 25.
- **Group sizes.** P-only: 18 usable (chemistry 10, physics 8), out of 24 matched. Both: **7** usable (4, 3), out of 10 matched. Neither group: 38, out of 60 matched. So the strict parse drops 25%, 30% and 37% of the three groups.
- **Confidence values only, by group.** These are what my plausible worlds are built from (P15).
  - In 17 of the 18 P-only questions, the mean of the two P numbers is below 0.2 (most are 0.02–0.05), and both F numbers are 0.8–0.97. The P number is close to 1 − F. The 18th has P 0.25/0.30 against F 0.85/0.90.
  - The 7 both-format rows (P0, P1, F0, F1) are: (0.03, 0.02, 0.55, 0.55), (0.60, 0.55, 0.55, 0.55), (0.02, 0.02, 0.03, 0.03), (0.50, 0.45, 0.45, 0.40), (0.50, 0.30, 0.62, 0.50), (0.20, 0.20, 0.35, 0.40), (0.03, 0.03, 0.03, 0.03). That is two questions near 0.03 in all four cells, one with P near 0.03 and F mid-range, and four with every number mid-range.
  - One usable value is exactly 0.70.

*Disclosure.* The confidence pattern above is not a guess value, but it makes part (a) close to foregone. A 'yes' guess stated at 0.03 in P and 0.95 in F would be incoherent. The author will read this review before the run. The frozen rule and the data cannot change, so this matters only for the fixes, and none of the fixes below touches a bar.

## Checks

**D1. Holds.** As a stranger, I applied §5 to planted tables. I used the frozen `analyse()` on the real 63 × 4 confidence matrix with planted guess counts (`threshold.py`): k_p 'no' among the 18 P-only questions, k_b among the 7 both-format questions, and the rest at 40% or 60%, with three placements and three bootstrap seeds each. Every table returned exactly one verdict. `--selftest` covers the untestable branch (n_P-only 9) and the 0.20 and 0 boundaries with tolerance. The untestable branch cannot occur on the real archive (n_P-only = 18 ≥ 10). Result:

| k_p of 18 | pass when k_b of 7 is | fail when k_b is |
|---|---|---|
| 18 | 0–3 | 4–7 |
| 17 | 0–3 | 4–7 |
| 16 | 0–2 (3 split: pass, fail, pass) | 4–7 |
| 14 (rest 0.6) | never | always |

**D2. Holds.** There is no manipulation, only an archive split. The knob that must move the output is the guess label. Planting more 'no' guesses in the both group moves the verdict from pass to fail at k_b = 4 (table above). The parameters the code uses match §2 and §4: flag < 0.70 − 1e-9; P-only = both P flagged and neither F flagged; both = all four flagged; usable = number in all four cells plus a parsed P r0 guess; 10,000 resamples; `seed % 2**63`; leave-one-out with shifted bounds over P-only questions. The code is unchanged from 0d7e98a to HEAD.

**D3. Holds.** Guard (b) has to reject the boring world it was added for, and it does (`guard_value.py`, real confidences, synthetic guesses):

| world | P(part (a) alone passes) | P(full rule passes) |
|---|---|---|
| 'no' more likely the lower the mean of all four numbers (4 strengths) | 0.07–0.38 | 0.00–0.01 |
| 'no' tracks the lower of the two format means (2 strengths) | 0.89–1.00 | 0.00–0.03 |
| no link (P(no) 0.55 everywhere) | — | 0.00 |

Without guard (b), the bet would pass in boring worlds. With it, it does not. The lesson's correction does real work.

**D4. Flaw: the control is not matched to the hypothesis.** The referent reading predicts that the both-format group also holds 'no' guesses.
- em-dm6 (`results/calibration-under-format.md`, exploratory) measured the proposed-answer reading in fresh frequency cells for 14–19% of Sonnet's 'no' guesses. A 'no' guess read that way in both formats is low in all four cells, so it lands in "both".
- Three of the 7 both-format rows look like that (0.02–0.03 in all four cells, or in both P cells).
- The four mid-range rows are genuine uncertainty, and the hypothesis says nothing about their guesses.

In referent-reading worlds built on these rows (`worlds.py`), P(pass) is set mostly by the 'no' rate u among the four uncertain questions:
- 0.49–0.77 at u = 0.2;
- 0.26–0.57 at u = 0.35;
- 0.12–0.38 at u = 0.5;
- 0.06–0.18 at u = 0.65;
- 0.03–0.09 at u = 0.8.

The ranges come from varying the 'no' rate of the low-everywhere rows (0.5 or 0.9) and of the high-confidence rows. So guard (b) rejects the boring world (D3), but it can also reject the hypothesis it protects, for reasons the hypothesis predicts. Making it fair would change the test, so I do not ask for that. I ask that a fail on guard (b) alone be read for what it is (fix 2), and I recommend the reported secondary in the fixes.

**D5. Holds.** This is a "beat it by a margin" rule, not a null rule. The constant predictor (no link to the guess) passes 0% of the time, and the one-bit "'no' means lower numbers everywhere" predictor passes at most 1–3% (D3).

**D6. Holds.** No calls, no refusals possible. Parse rate measured: 63 of the 94 matched science questions have a strict-parsed P r0 guess. Every one of the other 31 is an open-form answer. Whether the strict parse biases the shares (the brief's question):
- By count, the drops are similar across groups (25%, 30%, 37%), so the parse does not empty one group.
- The bias that matters is within groups. An open-form answer different from X is a rejection that the strict parse drops. If P-only open-form answers are mostly rejections and the both group's are not (or the reverse), the shares move. I cannot check this without reading the guesses.
- With 3 of 10 both-format questions dropped, one or two such questions could cross the k_b = 3/4 line. That is why the dropped counts must be reported (fix 3), and why a broad-parse secondary is recommended.

**D7. Holds.** All three groups come from the same archive, the same four fresh cells, the same guess source (P r0) and the same parse. The groups differ in confidence level by construction, which is the design. One unstated asymmetry, not a flaw: guesses are read from P r0 only. A question whose guess changes between formats (yes in F, no in P) is classified by its P guess. This fits the claim, which is about the P number.

**D8. Flaw: wording.** There are three verdict sentences, but "fail" covers two different worlds:
- (i) the P-only flags are not mostly 'no' (D1 short);
- (ii) they are mostly 'no', more than all science questions, but not shown to be more than the 7 both-format questions.

Branch (ii) is the likeliest fail. In it, the frozen fail sentence ("were not shown … to be mainly ones where Sonnet's guess rejected the proposed answer") would be false in plain English if, say, 17 of 18 were 'no'. All three sentences also omit the scope: they cover only the answers with a yes/no guess, 18 of the 24 matched P-only questions. Fix 2.

**D9. Flaw: leave-one-out misses the group that decides it.** The frozen LOO removes only P-only questions. On the real sizes, the verdict changes at one both-format question (k_b 3 → 4). In referent worlds, removing one both-format question flips the verdict in 17–39% of simulated runs (`worlds.py`, shifted-bound rule as frozen). In the planted tables, the P-only LOO reported no flip at k_b = 3 when k_p is 17 or 18, which is exactly where the result is most fragile. Fix 1. One cluster check (P14): the questions are not template-generated within category, and two categories are too few clusters, as §4 says. Category counts are reported. I agree.

**D10. Flaw (record).** The machinery holds:
- Budget: $0. The script imports only argparse, hashlib, json, pathlib and numpy.
- No calls, so stop-on-refusal does not apply.
- One scale direction: confidence 0 = certainly wrong. F is divided by 100 in `cal_format.parse`.
- Hashes pinned. The code stops on a mismatch before analysis.
- Beacon. I fetched CURBy-RNG pulse 1592328 here (`@buff-beacon-project/curby-client@1.2.0`, from the em-dm6f2 audit's scratch install). It is timestamped 2026-11-05T14:24:00.163Z, and its randomness matches §2 byte for byte. Pulse 1592327 is at 14:23:00.178Z (07:23:00 MST), before the commit at 07:23:29, so 1592328 is the first pulse after it. `python3 ledger/seed.py <randomness> em-dm6f2f1 --purpose bootstrap` gives 8073910693128109651, as recorded, and it is below 2^63.
- `ledger/check_prereg.py`: L1, L2, L3 and H1 ok. R1 fails only because this file did not exist yet.
- `results/dm6f2f1-no-guess.*` does not exist, so the run has not happened.

The record has two problems:
- **Wrong group sizes.** The lesson, §0's lesson row and the odds rationale say guard (b) "compares two groups of about twenty". It compares 18 with 7. The odds were set on a premise the archive does not hold.
- **Independence.** §0 reports the em-dm6f2 auditor's crude parse as "most probability-format science flags as 'no'". The audit's counts are 40 of 58 (chemistry) and 22 of 44 (physics), so physics is exactly half. The same audit line gives a frequency-format count, chemistry "36 of 47 'no' answers unflagged". That bears on guard (b): it says the F-flagged set holds 'no' guesses in number. §0 does not cite it.

*Does the auditor's parse weaken the bet?*
- For part (a), yes. With 62 of 102 P-format science flags already seen as 'no', and the confidence pattern above, part (a) was largely known before the run. A pass on part (a) alone would carry little information.
- For guard (b), only slightly. The crude parse pools both replicates and all 60 questions per category and never splits by group, so it does not reveal the 7-question count that decides the bet. The F-format line hints that the both group is not 'no'-free, which fits a 45% rather than a high number.
- So the bet still carries information, almost all of it in guard (b), provided §0 states exactly what was known. Fix 3.

**D11. Holds, narrowly.** The plausible worlds use the real 63 × 4 confidences and synthetic guesses.
- **Boring worlds:** P(fail) 0.97–1.00.
- **No-link world:** P(fail) 1.00.
- **Referent-reading worlds:** P(pass) 0.03–0.77 and P(fail) 0.23–0.97 over the grid. Both are at least 10% in 14 of 20 settings. Only the worlds where 65–80% of the uncertain both-format questions are 'no' guesses push P(pass) below 10%.

So the bet can both pass and fail at the available n (P12 is not triggered). The fail side is weakly informative about the referent reading (D4), and that is handled by fix 2's sentence, not by moving a bar.

## Required fixes

Each needs a dated DEVIATIONS row (D74 or the next free number), written before the guesses are read and naming this review. No bar moves: 0.20, the two lower bounds > 0, MIN_PONLY 10 and the 0.70 flag all stay.

1. **(D9) Leave-one-question-out over every usable question.**
   - What changes: run the existing shifted-bound LOO over all 63 questions, not only P-only. The both-format and other questions change share(both) and share(all).
   - What is reported: flips listed by group (P-only, both, other). The §5 rule "verdict stands, reported as '<verdict>, carried by <id>'" applies to any flip.
   - Code: in `analyse()`, drop the `if not ponly[i]: continue` guard, and pass `int((ponly & (w > 0)).sum())` as the P-only count. Extend `--selftest` with a planted table at k_b = 3 of 7 that must report a both-group flip.

2. **(D4, D8) Two fail sentences and the scope.** Keep the verdict labels (pass / fail / untestable) and the rule. Split the fail sentence by branch, chosen mechanically:
   - **fail, part (a) holds:** D1 ≥ 0.20 and D1's lower bound > 0, but D2's lower bound ≤ 0. Use: "On Sonnet's science questions with a yes/no guess, the answers that only the probability format put under 70% were mostly ones where Sonnet's guess rejected the proposed answer, more often than among all such science answers, but not shown to be more often than among the answers both formats put under 70% (n = <n_both>). The design cannot tell whether that is because 'no' answers carry lower numbers in every format or because the proposed-answer reading also occurs in the frequency format."
   - **fail, otherwise:** the frozen sentence, with "science questions" → "science questions with a yes/no guess".
   - **pass and untestable:** add the same scope, "with a yes/no guess". The pass sentence's "but does not prove it" stays.

3. **(D10) Record.**
   - In a DEVIATIONS row and §0 errata (frozen text kept, correction beside it), state the usable sizes: 63 usable; P-only 18; both 7; matched 24 / 10 / 60 before the strict parse. Note that the guard comes down to "at most about 3 of the 7 both-format questions are 'no'" if P-only is nearly all 'no'.
   - Correct "about twenty" in `ls-em-dm6f2f1` with a note (the line stays, with a correction field).
   - Quote the parent audit's crude counts exactly: P 40/58 and 22/44; F chemistry 36 of 47 'no' unflagged.
   - Odds may be revised before data, with both numbers kept.
   - Make the script write the matched and usable counts per group to the results JSON and md, so the strict parse's drops are on the page.

**Recommended, not required** (reported secondary, cannot change the verdict). Pre-register, before the guesses are read:
- a broad parse that classes an open-form P r0 guess as 'yes' if it matches X and 'no' otherwise, under a written rule (for example, a numeric match within 2% after unit normalisation, else a string match). Report the three shares and D2 on the 94 matched questions.
- D2 recomputed with the both group limited to questions whose two F numbers are both ≥ 0.2, the rows where the frequency-format proposed-answer reading is not on its face. Report it with its n.

Each answers a question in D4 and D6 that the primary cannot.

VERDICT: fix-first (3)

## Addendum: fix confirmation, 2026-11-05 07:45 America/Denver (not confirmed)

I checked commit f4d82d3 (D76; lesson_correction on ls-em-dm6f2f1). The script is unchanged from f4d82d3 to HEAD, and `results/dm6f2f1-no-guess.*` does not exist. `--selftest` prints SELFTEST OK. I did not run `--seed` and did not read any guess value. Every check below plants synthetic guesses, either on the real 63 × 4 confidence matrix or on the author's own selftest table. Scripts `confirm.py`, `exact_loo.py`, `author_synth.py` and `mutant.py` are in the scratch folder named in the header.

**F2 holds.**
- The branch is chosen mechanically: `fail` with D1 ≥ 0.20 − 1e-9 and D1's lower bound > 1e-9 gives "fail, part (a) holds".
- On planted tables with the real confidences (k_p 17 or 18 of 18, k_b 4 or 5 of 7), that branch and its sentence appear, with n_both filled in.
- Every sentence carries "with a yes/no guess". The pass sentence keeps "but does not prove it". The verdict labels and bars are unchanged.

**F3 holds.**
- D76 states the usable and matched sizes (63: 18 / 7 / 38; 94: 24 / 10 / 60).
- The lesson line keeps its frozen text, and a `lesson_correction` field says that "about twenty" is wrong.
- The parent audit's counts are quoted exactly (40/58, 22/44; F chemistry 36 of 47 'no' unflagged).
- The script writes the counts per group before and after the parse to the JSON and the md.
- Odds stay at 0.45, with a stated reason.
- The F ≥ 0.2 secondary is in and labelled as unable to change the verdict. The broad-parse secondary was recommended, not required, so leaving it out is not a flaw.

**F1 does not hold in substance.** It meets the letter of what I asked: the shifted-bound LOO now runs over every question, and a mutant with the old `if not ponly[i]: continue` makes the new selftest print SELFTEST FAILED. But the shifted-bound rule, which I endorsed in the review, gives the wrong answer in the 7-question both group at exactly the counts that decide the bet. I checked it against an exact leave-one-out, which re-runs the frozen `analyse()` without the question, same seed:

| table | verdict | shifted-bound LOO (as coded) | exact LOO |
|---|---|---|---|
| real confidences, 18 of 18 P-only 'no', 3 of 7 both 'no' | pass (D2 lower bound +0.167) | no flip | dropping a both-format 'yes' → **fail** (a real flip, missed) |
| same, 4 of 7 both 'no' | fail (D2 lower bound 0.000) | 4 both-group flips | dropping a both-format 'no' or 'yes' → fail (**no flip**) |
| same, 5 of 7 both 'no' | fail | 5 both-group flips | no flip |
| the author's selftest table, k = 3 | pass (D2 lower bound +0.200) | no flip | dropping a both-format 'yes' → **fail** |
| the author's selftest table, k = 4 (the asserted case) | fail (D2 lower bound 0.000) | 4 both-group flips | **no flip** |

The cause:
- When P-only is all 'no', its bootstrap share has no variance.
- With 7 questions, the both share's 97.5th percentile sits at 1.0, a point mass. So D2's lower bound is pinned at 0 for k_b ≥ 4.
- Shifting a pinned bound by the change in the point estimate moves it above 0 whenever a 'no' is removed. That is a false flip. At k_b = 3 the shift understates how far the bound falls when a 'yes' is removed. That is a missed flip.

So the selftest's k = 4 assertion checks an artefact. On a fail at 4–5 of 7, the results heading would print "fail (carried by …)" with four or five question ids that do not carry it. On a pass at 3 of 7, it would print no flip when one question does carry it. My review's figure of 17–39% for single both-group flips (`worlds.py`) used the same shifted-bound rule and is therefore unreliable. I withdraw it. The finding it supported, that the verdict hangs on one both-format question, stands on the exact check: at 3 of 7, one 'yes' decides it.

**What F1 needs, with no bar moving:**
- In `analyse()`, compute each leave-one-out verdict exactly: re-run the bootstrap on the n − 1 remaining questions with the same seed and nboot, and apply `verdict()` to its own bounds. This is about 63 × 10,000 resamples, a minute or two.
- If run time matters, use the exact LOO at least for every both-group and P-only question, and say which rule each group used.
- Change the selftest edge to the real edge in the author's table. At k = 3 it must list a both-group flip, from dropping a 'yes'. At k = 4 it must list no both-group flip.
- Update the D76 row (or add one) to say that the frozen "bounds shifted by the point change" rule is replaced by the exact LOO for this reported robustness check, citing this addendum. It is reported only and cannot change the verdict, so no bar moves.

This addendum also corrects my review's D9 text: the shifted-bound rule is the source of the problem, not just its coverage.

confirmed_at stays null until F1 is fixed and re-checked.

CONFIRMED: no
