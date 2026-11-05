---
bet: em-dm6f2f2f2
program: entangled-mind
prereg_commit: 4759da2
reviewer_session: fresh design-review subagent (worktree oversight-testbed-p1-wave4; has not seen the authoring session; scripts and fake-client runs in its scratchpad, no file in the repo touched but this one)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 16:50 America/Denver
checks: {D1: holds, D2: flaw, D3: holds, D4: holds, D5: holds, D6: flaw, D7: flaw, D8: flaw, D9: holds, D10: flaw, D11: flaw, D12: holds}
prior_work_search: WebSearch (standard), 2026-11-05, in memory-research words: "metamemory confidence calibration recall versus recognition test format forced-choice versus open-ended answers overconfidence"
papers_opened: 5
flaws: 8
pilot_usd: 0.00
verdict: fix-first
confirmed_at: null
---

# Design review of em-dm6f2f2f2

## In plain English

As built, the test could come back "untestable" more often than its dry run says. It could also score a pass whose own sentence contradicts itself. Four things drive that:

- **The existing cells are mixed, not pure.** On these science questions, em-dm6's "old wording, open guess" cell is not open: Sonnet answered Yes or No in 55–64% of its askings, and 32 of the 120 questions were Yes/No in all four. So the two new forced cells are the first pure-form cells, not the missing half of a 2×2. The claim and sentences need rewording to match.
- **Forcing an open answer will likely cut off more answers.** In both archives, questions Sonnet answers openly lose their number far more often (27% of askings with the old wording, 88% with the own-guess wording, against 4–5% for Yes/No questions). The dry run instead borrows the mixed cells' usable rate (0.75–0.78). At the usable rates those open-answer questions show, P(untestable) is 0.12–0.62, not 0.00–0.01. A pilot of at most $0.10 on excluded science questions has to measure this before the run.
- **The guess-form check is miscounted, and it never touches the verdict.** It counts cut-off replies as "not Yes/No". If the open-guess instruction does not take, the bet still scores a pass, and the pass sentence then says both "neither carries the gap" and "this cell does not separate the answer form".
- **Crash recovery breaks the refusal rule.** After a crash, run() pays for the crashed batch again and never looks for a refusal in it. In the fake-client run a crash plus a refusal finished with no refusal record.

All of this can be fixed without changing what is tested. Verdict **fix-first**: eight fixes, the pilot first.

## Checks

Commands, all from `programs/entangled-mind` with `/Users/seanpharris/entangled-mind/.venv/bin/python`, no `.env` loaded, no API call:

- `--selftest`: passes.
- `--print-prompts`: four templates, below.
- The dry run and `cost_sim()`, run through an import with output to the scratchpad so the committed `results/dm6f2f2f2-dry-run.json` is not overwritten. They reproduce the committed numbers exactly: 0.89/0.77/0.98/0.00/0.00, cost mean $0.4830, max $0.5298.
- A fake `client.messages.batches` (create/retrieve/results, billing measured-style usage at $2/$10 per MTok × 0.5; the Sonnet 5.5 price and the batch discount are confirmed in the claude-api reference).
- Synthetic caches pushed through `analyse()` with `results_dir` pointed at a scratch copy.
- Archive re-analyses of `cal-sonnet-conversations.json` and `dm6f2f2-calls.json` restricted to the 120 science questions.

**D1. A stranger can apply the rule: holds.** Synthetic results tables through `analyse()` (cells of 60 questions, a format effect of +0.25 or none):

| synthetic table | verdict returned |
|---|---|
| both cells gap | pass |
| NO no gap | fail ("old wording, forced Yes/No guess: pass; own-guess wording, open guess: fail") |
| OY no gap | fail |
| NO 35 usable, both gap | pass (floor at 35 inclusive) |
| NO 34 usable, OY a clear fail | **untestable** (see Fix 5) |

Each returns exactly one verdict. The `rule()` and `f2.MIN_Q` override behave as §5 says, and `f2.MIN_Q` is restored afterwards.

**D2. Every manipulation takes effect: flaw (Fix 2).**
- **The templates hold.** Each new template differs from its parent cell only in the guess field. Selftest asserts this. `--print-prompts` shows OY = TIAN_P/F with "Guess: <Yes or No: whether the proposed answer is correct; just Yes or No!>", and NO = em-dm6f2f2's templates with "Guess: <your own answer to the question, as short as possible; not Yes or No …>". Settings print as max_tokens 300 and thinking between_tools.
- **The guess-form check is broken.** `yesno_share` counts every reply with non-empty `raw`, including max_tokens cut-offs, whose `guess` is None. A cut-off therefore counts as "not Yes/No".
  - Synthetic OY cell where every completed reply is "Yes" and 25% of replies are cut: share 0.75 in both formats, `took: OY False`.
  - In NO the same bias helps the ≤ 0.20 bar pass.
  - The parent's Sonnet science calls were cut 19% (P) and 11% (F) of the time. So OY can fail its 0.80 bar with full compliance, and NO can pass its bar partly on cut-offs.
- This is the same denominator problem the em-dm6f2f2 audit charged to its design review as a D2 miss.

**D3. Every control can fail: holds.**
- The same-format overlap J_N is the control. The "no format effect" worlds are rejected (fail 0.99–1.00).
- Those worlds are degenerate: crossing the F columns, `X[:, [3, 2, 2, 3]]`, makes J_F = J_N exactly, so D = 0 with no noise. I therefore also ran a wrong set-up with a real but sub-margin effect: the em-dm6f2f2 science cell with 50%, 65% and 80% of questions given no format effect. It passes 0.21, 0.03 and 0.01, i.e. it is rejected mostly.
- The cost of that: a true gap near 0.15 is detected only about one time in five at this n. The design sees gaps of the size already found (+0.31 to +0.42 on science), not small ones.

**D4. Rivals matched: holds (no competing families).** The heaping rival (Dai and Wang 2026) is addressed only by the reported threshold-sensitivity secondaries (0.5/0.6/0.8). §6 says what it cannot do.

**D5. A dumb baseline is beaten: holds.**
- Constant numbers give J_F = J_N = 1, D = 0: fail.
- Noise-only gives a low J_N: fail (em-dm6f2's selftest worlds, imported unchanged).
- A pure level shift between formats passes. The pass sentence's "cannot say whether one format flags more questions or other questions" covers that.
- This is not a "no difference" rule, so no equivalence margin is needed.

**D6. Foreseeable execution risks piloted: flaw (Fix 1).** The pre-mortem is of kind `world`, but forced instructions are untested on these items. Three risks:
- **Cut-offs.** The archives show answer form drives cut-offs on science:

  | archive (science, 120 q) | questions mostly Yes/No: askings without a number | questions mostly open or cut: askings without a number |
  |---|---|---|
  | em-dm6 (old wording) | 4.4% (74 q) | 27.2% (46 q) |
  | em-dm6f2f2 (own-guess wording) | 4.8% (105 q) | 88.3% (15 q) |

  With the old wording, questions answered openly in all four askings were usable 16 of 26 (0.62). With the own-guess wording, questions answered openly in three or four askings were usable 0 of 15. Forcing an open answer ("your own answer to the question … not Yes or No") on calculation questions invites the worked calculations ("Compute: d = v²/(2μg) …" in the archive) that hit max_tokens 300.
- **The instruction may not take.** NO's number field still says "if your guess is No, the probability that No is the right answer…", which invites the guess the guess field forbids. And the question itself is a yes/no question ("Is the correct answer X?").
- **Cost.** Longer open answers raise cost. At 1.5× the measured cost in the NO cell, P(all 60 run) falls to 0.10 (mean 57.9 questions); at 1.3× in both cells, to 0.00 (mean 55.9).

None of these is measured by the dry run.

**D7. Comparisons match: flaw (Fix 4).**
- **Within a cell, holds.** P against F differs only in the format clause, the same as in em-dm6.
- **Across the "2×2", does not hold.** The pre-registration calls the existing cells "old wording, open guess" and "own-guess wording, Yes/No". On the 120 science questions, em-dm6's cell was 64% (P) and 55% (F) Yes/No, and em-dm6f2f2's 73% (P) and 88% (F). Both are unforced mixtures, and on science they differ less in answer form than the framing says. So the guess-form axis has four levels:
  - unforced (old wording);
  - unforced (own-guess wording);
  - forced Yes/No;
  - forced open.

  The two new cells are a diagonal pair of forced cells (they differ from each other in both factors), not the missing corners of a factorial.
- **Is NO a fair "open" cell?** Yes, as a cell. With an open answer the number's referent is the model's own answer, so the double meaning cannot arise. Its No clause is moot, and §6 already says so. But it also changes what the number is about, from a binary judgment of a proposed answer to the chance that an open answer is exactly right. That is part of "answer form", and the claim should say so.
- **What each cell can tell.** Read the bet as "does the gap appear in each pure form?", not as "which factor carries it".
  - NO is the diagnostic cell: under "the double meaning carries it" or "Yes/No answers carry it", the gap should vanish there.
  - OY is diagnostic only against "the gap lives in open answers". Under the double-meaning hypothesis it is predicted to pass. The archive's all-Yes/No questions (old wording, 32 q) give D +0.61, J_F 0.15.
- Other differences (later date, fresh calls, a forced instruction against an unforced choice) are listed in §6. They affect cross-cell interpretation only, since no cross-cell test is run.

**D8. Verdict sentences written: flaw (Fixes 3, 4, 5, 7).**
- **The pass sentence's second sentence.** "Neither the own-guess wording nor the Yes/No answer form alone carries the gap" names a carrier that was never a candidate (the own-guess wording was the fix, not a suspect). It omits the one that was: the old wording's double meaning.
- **The fail sentence.** "The cell that did not show it points to what carried the gap in earlier runs" over-reads a fail. In the dry run's gap worlds the bet fails 0.11–0.23 of the time by chance at this n. And a fail can come from J_F's upper bound rather than from D.
- **The guess-form clause.** It is appended after a pass sentence that it contradicts. The synthetic NO cell with every guess Yes/No returns: "…with the own-guess wording and an open guess. Neither the own-guess wording nor the Yes/No answer form alone carries the gap … The guess-form instruction did not take in own-guess wording, open guess (Yes/No share outside the pre-registered 0.80 bar)…". For NO the bar is 0.20, not 0.80.
- **The noise-asymmetry clause is dropped.** `read_cell` sets `sentence = None`, which removes em-dm6f2's pass addendum. em-dm6f2 and em-dm6f2f2 both kept it.

**D9. One item cannot decide it: holds.** `loo_flips` is computed per cell and printed, and §5 says the results file states any flip first.

**D10. Machinery: flaw (Fix 6).** What holds:
- **Budget in code.** Every fake-client run stayed under $0.56: normal $0.399; every reply at max_tokens $0.541 with 35 questions run and 25 reported "not run"; heavy open cell $0.542.
- **The worst-case bound.** 2 characters per token plus 300 output tokens was never exceeded by any of the parent's 1,200 Sonnet requests; the closest came to 0.955 of the bound.
- **Chunks of whole questions** across both cells.
- **Stop on refusal** in the normal path. The batch ended, the refusal record was written, no further batch was sent, and a restart was refused.
- **Content-hash cache reuse.** A rerun made no batches.
- **Stop after two failed resubmissions.**
- **The beacon seed.** `ledger/seed.py` gives bootstrap 17580700879670056277 and items 13273746342911101247 from pulse 1592880. That is the first pulse after 4759da2 (16:35:05; pulse 23:36:00Z). It matches `SEED_RECORDED` and the inbox row.
- **The lesson line** is present and verbatim (`ls-em-dm6f2f2f2`).
- **Scale direction.** 1 = sure the model's own guess is right. In OY, a "No" can carry the old double meaning by design: that is the tested factor.

What fails, crash recovery:
- An unfinished batch found on start-up is collected only as `_lost_prior` cost. Its answers are discarded and the same requests are resubmitted.
- Fake crash while polling batch 0 (280 requests): restart re-paid $0.224 and ran 47 of 60 questions (13 not run).
- Same crash with a refusal inside batch 0: the restart **finished with no refusal file**, re-asked the refused request, and ran 46 questions. That breaks §7's "stop on any refusal; nothing … retried".
- The parent's code has the same path; it did not fire there.

**D11. The bet can pass and fail: flaw (Fix 1).**
- **What the committed worlds show.** P(pass) 0.77–0.98 in gap worlds and P(fail) 0.99–1.00 without, so the statistic can go either way at n ≈ 45.
- **What they cannot show.** They resample the mixed existing cells, usable rate included (0.78/0.75). So they say nothing about the new cells' usable rate, flag rate or cost, which is P15's point. The pre-registration's "P(untestable) 0.00–0.01" is a property of the old cells.
- **Proxy worlds closer to the new cells.** OY from em-dm6's all-Yes/No science questions (32 q). NO from its questions with at most one Yes/No asking (28 q), usable rate varied:

  | NO usable rate per question | P(pass) | P(fail) | P(untestable) |
  |---|---|---|---|
  | 0.75 | 0.96 | 0.04 | 0.00 |
  | 0.65 | 0.81 | 0.07 | 0.12 |
  | 0.60 | 0.63 | 0.07 | 0.30 |
  | 0.55 | 0.34 | 0.04 | 0.62 |
  | 0.45 | 0.02 | 0.00 | 0.98 |

  The observed rate for open-answering questions is 0.62 with the old wording and about 0 with the own-guess wording.
- **Two consequences.** P(untestable) is plausibly far above 0.01. And in these pure-form proxies P(fail) given testable is small (0.04–0.07), because the archive's pure-form subsets carry large gaps (D +0.51 to +0.61).
- Whether the bet is a test therefore depends on numbers only a pilot can give.

**D12. Prior work: holds.**
- **(a)** The Prior work line states "Predicts: unknown" with reasons: format dependence in people is a mean-level calibration result, and no paper separates referent wording from answer form for a threshold list. It is not a bare topic list.
- **(b)** Papers opened and what each is cited for:
  - Hansson, Juslin and Winman 2003 (CogSci Proceedings 25; eScholarship PDF read). Figure 1, reproduced from Juslin and Persson 2002: "With the half-range (two alternatives, forced choice-50-100% scale) format there is close to zero over/underconfidence, with the full-range … marginal overconfidence…". Holds for "calibration depends on the response format" (people).
  - Zhao et al. 2025, arXiv:2505.21701 (abstract): "shuffling answer options can decrease agreement to around 40%"; decision consistency across methods "as low as 7%". Holds for "prompt changes move" knowledge/abstention decisions (the model names are in the body; the parent's re-scout read Mistral-7B and Llama-3.1-8B there).
  - Kim and Kang 2026, arXiv:2605.27752 (abstract): "stated confidence depends on how a supplied answer is written", "five open LLMs". Holds for open models.
  - Dai and Wang 2026, arXiv:2603.09309 (abstract): over 78% of verbal confidences fall on three round values. Holds as the heaping rival.
  - Gigerenzer, Hoffrage and Kleinbölting 1991 is marked "not opened". Correctly so labelled.
- **(c)** Nothing found predicts this pass rule's outcome.
- **(d)** My own search, in memory-research words: "metamemory confidence calibration recall versus recognition test format forced-choice versus open-ended answers overconfidence". It found Buratti and Allwood 2012 (Judgment and Decision Making 7(5), 590–601; PDF read). Their introduction reports that people answering directed-recall questions ("no answer alternatives provided") improved their calibration by excluding unrealistic judgments, while "participants who answered recognition questions (i.e., with answer alternatives provided) were not able to increase their confidence realism". They cite Robinson and Johnson 1996 for a stronger confidence–accuracy link under recall than recognition.
  - This is human evidence that the answer form (choosing or judging against producing an answer) changes how confidence relates to correctness. It predicts that OY and NO will differ in level and flag rate, which matters for usable flags, not whether the probability-against-frequency gap holds within each.
  - It adds nothing in print that predicts this bet's outcome. It may go in §0 as a human precedent for the answer-form factor.

## Required fixes

Each fix goes under a dated DEVIATIONS row (D96 or the next free number) written before any data and naming this review. The author confirms each in an addendum here. Fixes 1–5 change no pass bar. Fix 3 adds an untestable branch that applies to pass and fail alike; Fix 5 scores a case as fail that is now unscored.

1. **Pilot, then re-run the dry run at the pilot's rates (D6, D11).**
   - **The pilot.** At most $0.10 by the code's worst-case bound, on science questions not among the 60 drawn: for example 6 (3 chemistry, 3 physics) drawn with the items seed from the other 60, both new cells, all eight requests (48 requests, worst case about $0.093). Report per cell and format:
     - the share of replies at max_tokens;
     - the share without a parsed number;
     - the Yes/No share among completed replies;
     - refusals;
     - mean cost per request.

     Pilot results are not test data and do not enter `dm6f2f2f2-calls.json`.
   - **Before the pilot, write the rule for what follows.** Replace `usable_rate` and the request costs in `dry_run()`/`cost_sim()` with the pilot's NO and OY rates. If P(untestable) then exceeds about 0.10, or either cell's form fails its bar, the design changes before the run. Options: max_tokens raised in both new cells, with the question count re-sized to the cap; rewording the NO number field so it no longer invites "No"; or redesign.
   - **Record where the pilot money sits.** Is the pilot inside br-022's $0.56 (the code's cap then falls by the pilot spend) or under its own ruling? This is unclear now; spend.jsonl must say.
2. **Fix the guess-form denominator (D2).** In `yesno_share` for this bet, count only replies that completed (`stop != "max_tokens"`) and carry a parsed Guess line. Report the cut-off share beside it. Add a selftest case: a forced Yes/No cell with 25% cut-offs must read "took".
3. **Make the guess-form check a gate, not only a sentence (D2, D8; point 5 of the brief).** A cell whose form check fails (on Fix 2's denominator) reads "untestable: the guess-form instruction did not take", and the bet is then untestable, whichever way its statistic came out.
   - The scored event is "the two missing cells". A cell where the instruction did not take is a replicate of an existing mixed cell, not that cell. The parent's sentence-only check was counted as a design-review miss.
   - If the author prefers to keep it scored, the clause must replace the pass sentence's second sentence (as D87 did), not be appended. It must also give the right bar per cell ("at least 0.80" for OY, "at most 0.20" for NO).
4. **Reword the claim to match the existing cells (D7).** In the docstring, §1, §6, the map entry's framing and the pass sentence, say that on these questions the existing cells are unforced mixtures (em-dm6 science 55–64% Yes/No by asking; em-dm6f2f2 73–88%). Say the new cells are forced pure forms. Suggested pass sentence after the first: "On these questions the gap shows both when Sonnet must answer Yes or No under the old wording and when it must give its own answer, not Yes or No, under the own-guess wording, so it does not need Yes/No answers or the old wording's double meaning, and it does not need open answers. The answer forms were set by instruction, and this design cannot say whether one format flags more questions or other questions." Drop "Neither the own-guess wording nor the Yes/No answer form alone carries the gap".
5. **Reword the fail sentence and close the conjunction gap (D8, D1).**
   - The fail sentence names each failing cell and which bar it missed (J_F bound, D, or D's lower bound). It says that at this size a cell like the earlier runs fails by chance about one time in ten to one in four (cite the re-run dry run), so a single-cell fail does not by itself show which factor carried the gap. Remove "points to what carried the gap".
   - Pre-register that a testable cell whose form took and which fails makes the bet **fail** even when the other cell is untestable. The conjunction is already false. Under the current rule that case is unscored, and with Fix 1's untestable risk it is not rare.
6. **Fix crash recovery (D10).** Save the `custom_id → key` map, the request sha and the texts in the batch log before polling. On start-up, store a collected batch's results in the cache like a normal batch, applying the refusal stop to them, instead of counting them as lost cost and resubmitting. Never resubmit a request whose collected result was a refusal. Add a fake-client selftest: a crash while polling, then a restart, with a refusal in the crashed batch, must write the refusal record and stop.
7. **Restore the noise-asymmetry clause (D8).** On a pass, append em-dm6f2's addendum for any cell whose `noise_asymmetric` is True, naming the cell. `read_cell` currently drops it.
8. **Correct the human-odds note (point 6).** The bet row and §0 say "same cells, statistic and bars". Sean's line `ho-20261105-162756-iy8` was given on a different event in three ways:
   - "Sonnet's 120 science questions", not 60;
   - "new own-guess template with open answers allowed". The existing own-guess template already allows open answers; this design forces them;
   - no floor stated (the parent's was 40), where this design uses 35.

   List all three in `human_odds_note` and §0, and in the result's scoring note. The line's `spend_asked` reads "about /bin/zsh.56" (a shell expansion of "$0.56"); check what the card showed him and record it. His number stays attached; he is not asked.
