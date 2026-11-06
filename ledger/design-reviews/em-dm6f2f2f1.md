---
bet: em-dm6f2f2f1
program: entangled-mind
prereg_commit: 39b9f16
reviewer_session: fresh design-review subagent (worktree p1-wave4, launched by the program 1 wave-4 session; has not seen the authoring chat)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 16:51 America/Denver
checks: {D1: holds, D2: holds, D3: holds, D4: holds, D5: holds, D6: holds, D7: flaw, D8: flaw, D9: flaw, D10: flaw, D11: flaw, D12: holds}
prior_work_search: "WebSearch: same respondents probability format versus frequency format \"out of 100\" risk judgments test-retest reliability agreement classification cutoff (judgment and decision making / forensic risk words, not the seed question's); follow-up: Slovic Monahan MacGregor 2000 violence risk assessment probability versus frequency formats"
papers_opened: 3
flaws: 6
pilot_usd: 0.00
verdict: fix-first
confirmed_at: 2026-11-05 17:53
---

# Design review of em-dm6f2f2f1

## In plain English

As built, the test can pass and can fail, its cap holds, and its statistic is em-dm6f2's, applied correctly. But it does not test what its sentences say. The "unsure set" is mostly not questions where Sonnet and Haiku were unsure. It is mostly questions where they gave a low number to a "No" guess, which is the reading em-dm6f2f2's audit tied to the referent. Those are also the questions where Sonnet's own list changed with format: 47% of them, against 9% of the other non-claim questions. So a pass would show the gap on Opus on the questions where Sonnet's gap lived, not on questions where models are unsure. The words must say that. Three numbers in the pre-registration are also wrong or fragile:
- The cost simulation drew from the wrong cost pool. About 36 of the 40 questions will run, not 40 in 99.9% of runs.
- The "Opus-confident" dry-run world is a knife edge.
- The leave-one-out check ignores this bet's own floors.

The refusal stop also misses refusals inside a batch collected after a crash. All six can be fixed before any call without changing what is tested.

## Checks

Commands were run from `programs/entangled-mind` with `/Users/seanpharris/entangled-mind/.venv/bin/python`. Scratch scripts are in this session's scratchpad (`rev-f1-x7/`: `fake_client.py`, `t_run.py`, `t_crash.py`, `worlds_f1.py`). No `.env` was loaded and no API call was made. The committed `results/dm6f2f2f1-dry-run.json` was not rewritten: I called `dry_run()` and `cost_sim()` from a scratch script.

**D1. A stranger can apply the rule: holds.** The §5 reading is three ordered clauses: untestable (under 25 usable, or under 6 flagged), then pass, else fail. Every tolerance is named. I applied it to synthetic tables, each run through `read_rule`:
- 12 of 25 questions flagged in P only: pass.
- The same 10 flagged in every cell: fail.
- Single-cell flags spread over the four cells: fail (J_F 0, J_N 0).
- 5 flagged: untestable.
- 24 usable: untestable.

Each table returned exactly one verdict. `--selftest` passes. Its output: unsure set 80 (28/25/27), draw repeatable, worst case $0.0036 per request, floors hold, and `f2.MIN_Q` restored to 40.

**D2. Every manipulation takes effect: holds.**
- The templates are em-dm6f2f2's two reworded templates. The P and F prompts differ in the format clause, and the parse is per format.
- Settings asserted by the selftest: max_tokens 300 and `output_config` effort low. These match §2 and D87.
- The unsure-set selection takes effect: all 30 drawn non-claim questions are in the set, and `--print-questions` gives 10 per category.
- Each floor moves the verdict, as in the D1 runs.
- The seed recomputes: `ledger/seed.py <randomness> em-dm6f2f2f1 --purpose bootstrap|items` gives 1922030650083322747 and 5271620121328318991, as in D93 and `SEED_RECORDED`.
- I did not re-fetch pulse 1592874 to confirm it predates the commit (no npm client run). That part of the seed check is recorded, not re-verified.

**D3. Every control can fail: holds.** The control is the same-format replicate overlap J_N. I built a null that keeps real replicate noise: each question's four Sonnet cells shuffled at random, so formats are exchangeable. The rule rejected it in 98.5% of 200 draws (pass 0.015, Sonnet cells) and in 100% of 200 draws (Haiku cells). The committed "no format effect" world is degenerate (P cells copied from the crossed F cells, so D is exactly 0). It cannot pass by construction, so it is not by itself evidence that the control works. The shuffled null is.

**D4. Rivals are matched: holds (not applicable).** One model and two formats, with no competing model families.

**D5. A dumb baseline is beaten: holds.** A constant confident answerer (every number at least 0.75) is untestable. Identical lists in all cells fail. Pure replicate noise fails. A pass needs D ≥ 0.10 with its lower bound above 0, so a "no-difference" reading is never what passes. This is not a no-difference rule, so no equivalence margin is needed.

**D6. Execution risks piloted: holds.** The pre-mortem is of kind `world`. The parent ran these templates on all 300 pool questions on Sonnet and Haiku, and on 20 on Opus, with no refusal. No pilot is needed. The execution risk that does exist is cut-offs at max_tokens, and it is measured in the archive (see F2).

**D7. Comparisons match: flaw (F1).**
- Within the bet: P and F are compared on the same questions, model and settings. The four cells of a question go in the same batch (chunks are whole questions), so only the named factor differs.
- The claim in §0 ("Adds: the replication invariant 7 owes em-dm6f2f2's Sonnet pass") and §1 ("the format gap holds on a third model") compares Opus with Sonnet's pass. That comparison differs in model and in the questions.
- The questions were chosen from the parent's own data on the other two models, and the choice concentrates the parent's effect. Sonnet's list differs by format (flagged in one format only) on 31 of the 66 complete unsure-set questions (47%). On the other non-claim questions it does so on 13 of 142 (9%). For Haiku the figures are 23/76 against 35/153.
- §6 says the questions differ, but calls them questions where "the smaller models were unsure". It does not say the selection picks out the questions where Sonnet's gap lived. A pass is an item-level replication on the parent's most format-sensitive items, not a replication on a fresh sample. The claim must be written as about that bundle.
- The selection uses only Sonnet's and Haiku's answers, and Opus's replicate noise is independent of theirs. So I found no regression artefact on Opus itself. This is a scope issue, not a bias in Opus's statistic.

**D8. The verdict sentences are written, with nouns the design can carry: flaw (F1).** All three `SENTENCES` say "on questions where Sonnet and Haiku were themselves unsure". The selection rule is "at least one number below 0.70 in any of four cells, for both models". In the archive those numbers are mostly not uncertainty:
- Of Sonnet's qualifying cells on the 80 questions, 52% are below 0.2 and 66% below 0.5. 94% of the sub-0.5 ones carry a "No" guess.
- Of Haiku's qualifying cells, 79% are below 0.2 and 95% below 0.5, all with a "No" guess.
- Only 24 of the 80 questions have both models stating a number in [0.2, 0.7). In the actual draw, 10 of the 30 non-claim questions do.

Under the own-guess template, a "No" guess with 0.03 is the reading em-dm6f2f2's audit attributes to the referent ("of the 32 questions flagged only in the probability format, 28 carry a 'No' guess there and 25 a probability below 0.5"). So "unsure" is the wrong noun. The parent's 20 Opus questions include 8 from this set, and on those Opus gave no number below 0.55 in any cell, so Opus did not show that reading there.

**D9. One item cannot decide it: flaw (F4).** §5 pre-registers that a one-question flip is reported first. The code's leave-one-out is em-dm6f2's, run inside `read_rule` with `f2.MIN_Q` patched to 25. It is inconsistent with this bet's rule in two ways, both confirmed on synthetic data:
- At exactly 25 usable questions, every leave-one-out sample has 24 < 25 and reads untestable. All 25 questions were reported as flips (`loo_flips` 25 of 25 on a clean level-shift pass).
- The 6-flag floor is not applied. With exactly 6 flagged questions, removing any flagged one makes the bet untestable under §5, yet `loo_flips` was empty.

The leave-one-out also reuses the full-sample interval bounds, so it tests only the point-estimate conditions (inherited, and acceptable if stated). In dry-run passes, one-question flips are rare at 40 asked (0–5 of about 70–185 passes). At the realistic cap-limited count they reach 11 of 59 and 13 of 61, so the check matters.

**D10. Machinery: flaw (F2, F5).** I exercised `run()` with a fake `client.messages.batches` (create, retrieve, results) that bills through usage tokens matched to em-dm6f2f2's measured Opus costs.

- **Budget in code: holds.** With every reply at max_tokens (worst case), 21 questions ran in 3 batches, spending $0.2928, and the rest were reported as not run. With measured costs, the maximum over 20 runs was $0.2904. The cap was never crossed.
- **Cost claim in §0 and §3: wrong (F2).** The claim is "all 40 questions run in 99.9% of runs, maximum $0.286". `cost_sim()` draws non-claim costs from all of Opus's non-claim calls in the parent, a mix of unsure-set and other questions. But every non-claim question here is from the unsure set. Measured per-request Opus cost on unsure-set questions is $0.00239, against $0.00150 on the other non-claim questions and $0.00062 on claims. With unsure-set costs, the fake-client run completed 34–38 of 40 questions (median 36) in 20 of 20 runs, and never 40. With the mixed pool, as in `cost_sim`, it completed 40 in 20 of 20, which reproduces the committed number. Expected spend at measured unsure-set costs is about $0.31, above the cap. The questions dropped are the last in the seeded run order, so they are random, not chosen.
- **Cut-off rate (F2).** The dry run uses 0.054, which is Opus's rate on the random draw's non-claim calls. All 3 cut-offs in the parent's Opus archive fell on unsure-set questions: 3 of 32 cells (0.094), against 0 of 24 on the others. With only Opus's own missingness (claims complete), the realistic picture is:

  | assumptions | mean usable | P(usable < 25) |
  |---|---|---|
  | cap-limited count (34–38 asked), cut 0.094 | 26.9 | 0.18 |
  | cap-limited count, cut-off rate given its uncertainty (Beta(4, 30)) | 25.4 | 0.41 |
  | 40 asked, cut 0.054 (the pre-registration's assumption) | 34.0 | 0.000 |

- **Stop on refusal: holds on the main path.** A refusal in a live batch writes the refusal file and exits with no further batch, and a restart is refused while the file exists.
- **Stop on refusal: flaw on the crash path (F5).** I crashed the run while it polled batch 2, with a refusal planted in that batch. On restart, the lost-batch loop (lines 131–142) counted the batch's cost but never looked at `stop_reason`. The run went on and resubmitted the refused request in batch 3. A real refusal there would be retried, which §7 forbids.
- **Crash recovery otherwise: holds.** The lost batch's cost was counted ($0.0466 in `_lost_prior`), its requests were resubmitted, and total spend ($0.2868) equalled what the fake billed, under the cap.
- **Residual gap in "the cap cannot be crossed" (F5).** A crash between `batches.create` and the `save()` on line 180 leaves a billed batch with no ID on disk. Its cost would never be counted.
- **Caching: holds.** A cached entry with a changed request hash stopped the run with nothing resubmitted. A second run after a complete one submitted no batch. A request that keeps erroring stops after two resubmissions.
- **Other machinery: holds.** There is one scale direction (number = P(own guess correct), flag below 0.70). The beacon rule followed operators/hardware.md: CURBY-Q stalled, so the first CURBy-RNG pulse after the commit. The lesson line is present and matches §0 (`ledger/check_prereg.py ... --before-run`: L1–L3 and H1 ok; R1 waits for this file).

**D11. The bet can both pass and fail: flaw (F3). The floor itself is met.** The committed table reproduces exactly (my rerun of `dry_run()`: 0.75/0.55/0.12/0.00/0.00 pass). Every world is built from archived numbers, as P15 asks, but three of its inputs do not hold:
- (a) The cut-off rate and question count are not this draw's (F2).
- (b) The "Opus-confident" world is degenerate. It maps x to 1 − k(1 − x) with k = 0.31 chosen on a 0.01 grid. Under that map a number is flagged only if Sonnet's number was at most 0.03. At k = 0.30 no number can be flagged (untestable 1.00). At k = 0.31 the flags are exactly Sonnet's 0.01–0.03 numbers, all referent-type "No" answers. Its pass rate is also Monte Carlo-noisy at 100 draws: my reruns at k = 0.31 gave 0.36, 0.46 and 0.42 (200–400 draws each) against the committed 0.55.
- (c) The 0.75 "Opus like Sonnet" world inherits Sonnet's referent-type flips (for example h081: Sonnet P 0.07/0.07, F 0.90/0.90). On the 6 unsure-set questions where Opus answered all four cells in the parent, it flagged one question (h039) in all four cells and nothing else. That is the pre-mortem's world.

Recomputed with the realistic inputs (36 asked, cut chosen so total missingness is about 0.094, 200–400 draws each):

| world | pass | fail | untestable |
|---|---|---|---|
| Sonnet-like | 0.70 | 0.27 | 0.03 |
| Opus-confident (k = 0.31) | 0.41 | 0.46 | 0.14 |
| Haiku-like | **0.045** | 0.86 | 0.10 |
| Sonnet-like with the referent fixed (a "No" guess below 0.5 read as 1 − x) | 0.40 | 0.58 | 0.03 |
| no format effect, Sonnet-like | 0.00 | 1.00 | 0.00 |
| no format effect, Opus-confident | 0.00 | 0.19 | 0.82 |
| shuffled-cells null | about 0.01 | about 0.99 | about 0.01 |

So P(pass) stays at or above about 0.40 in every effect world except Haiku-like, and P(fail) is 0.19–1.00 in every null. The bet can pass and fail, and the most informative new world (referent fixed) still passes 0.40. This is not a redesign. But the committed table, and the 0.45 odds weighted from it (0.75/0.55/0.12), overstate the inputs and omit that Opus's only measured unsure-set data look like the null.

**D12. Prior work: holds.**
- (a) The line states a predicted outcome: pass direction, size unknown, with citations.
- (b) Papers opened:
  - Zhao et al. 2025, arXiv:2505.21701, "Do We Know What LLMs Don't Know?" (HTML v2). Models: Mistral-7B, LLaMA-3.x 1B–70B, OLMo-2-7B. Prompt: "the probability between 0.0 and 1.0 that your guess is correct". Table 1, option shuffling on MMLU, AskCal IoU_rej: .61 Mistral-7B, .20 LLaMA-3.1-8B. Cited correctly.
  - Kim and Kang 2026, arXiv:2605.27752, "Same Answer, Different Confidence: Protocol Sensitivity in LLM Confidence Calibration". Five open 7–9B models plus models up to 72B, no Claude. Its Ethical Considerations says "a threshold or calibration set under one prompt may not hold under another". Cited correctly.
- (c) The predicted direction is in print only on open models and option shuffling. §0 says what this adds (Opus, the probability against frequency pair), and the odds context names the literature row. Holds.
- (d) My own search was in judgment and decision making and forensic risk words, and found Slovic, Monahan and MacGregor 2000 (*Law and Human Behavior* 24(3), 271–296). I read the abstract through database records; the full text did not open (ncjrs 403). In 409 forensic clinicians, frequency scales gave lower mean likelihoods than probability scales, yet the same likelihood read as higher risk when it came from a frequency. That is a mean-level format effect in people, the same kind as the Gigerenzer confidence-frequency effect the line names. It predicts a level shift, which would move a threshold list (the pass direction), and it does not measure set overlap against test-retest. Evidence for the line, not a gap in it.

## Required fixes

Each goes under one dated DEVIATIONS row (D94), written before any call and naming this review. None lowers the bar.

1. **F1 (D7, D8): describe the question set as what it is.**
   - In §1, §2, §6, the `SENTENCES` and the bet row's title and `odds_event`, replace "questions where Sonnet and Haiku were (themselves) unsure" with words the selection carries. For example: "questions on which Sonnet and Haiku each gave a number below 70% in at least one asking (most of them low numbers on 'No' guesses)".
   - In §2, add the composition: 66% and 95% of the qualifying numbers below 0.5, almost all on "No" guesses; 24 of 80 questions with both models in [0.2, 0.7); 10 of the 30 drawn.
   - In §6 and §0's "Adds", say plainly that the selection concentrates the parent's effect: Sonnet's list differed by format on 31 of 66 of these questions against 13 of 142 elsewhere. A pass therefore shows the gap on Opus on the questions where Sonnet's gap appeared, not a replication on a fresh sample.
   - Rewrite §1's "the format gap holds on a third model" accordingly.
   - Pre-register as a reported secondary the Opus share of "No" guesses below 0.5 per format, restricted to these questions. The existing `below_half_yesno` covers this if it is reported first.
2. **F2 (D10, D11): correct the cost and cut-off inputs.**
   - Draw `cost_sim()`'s non-claim costs from Opus's unsure-set calls in the parent ($0.00239 mean, n = 32). Restate §0's budget line and §3 with the result: about 34–38 of 40 questions run, median 36.
   - Rerun the dry run with that question count and the unsure-set cut-off rate (3 of 32). Either correct for the double count of Sonnet's own missing cells (6.2% on these questions) or state it.
   - Keep the $0.30 cap (br-022). Any higher cap is a new ruling under Sean's steer, not this review's call. If the author tightens the worst-case input bound to fit more questions, it must remain a true upper bound for LaTeX-heavy prompts.
3. **F3 (D11): rebuild the "Opus-confident" world so it is not a knife edge, and add the world the archive suggests.**
   - Replace the one-parameter shrink with a map that does not flag only Sonnet's 0.03s. Options: map Sonnet's numbers by quantile onto Opus's measured unsure-set distribution (29 numbers), or report k from 0.30 to 0.40.
   - Add the referent-fixed Sonnet world.
   - State that on the 6 complete parent Opus questions in this set, Opus flagged one question, the same in all four cells.
   - Use at least 400 draws per world.
   - Recommit the table. If the table moves, the engine odds may be re-elicited before data with both numbers kept; the 0.45 was weighted from 0.75/0.55/0.12.
4. **F4 (D9): make the leave-one-out apply this bet's rule.**
   - In `read_rule`, compute the leave-one-out with this bet's verdict: both floors, applied to the reduced sample.
   - Pre-register in §5 how a flip that comes only from a floor (pass or fail to untestable) is reported: say so first, separately from a pass-to-fail flip.
   - Add a selftest case for exactly 25 usable questions and for exactly 6 flagged questions.
5. **F5 (D10): close the refusal stop on the crash path, and the create-to-save window.**
   - In the start-up loop that collects a lost batch, check each succeeded result's `stop_reason`. On "refusal", write `results/refusal-dm6f2f2f1.md` and exit before any submission.
   - Write a "submitting" marker to the batch log before `batches.create`. On start-up, if a marker has no batch ID, reconcile with `client.messages.batches.list()` and count the batch, or stop and report.
   - Otherwise soften §3's "the cap cannot be crossed" to name this window.
   - Add both cases to the selftest with a fake client.
6. **F6 (human odds): pre-register how Sean's line is scored.**
   - Sean's 0.65 (`ho-20261105-162756-bus`) was given on the card's event: a random draw and a 40-usable floor. Its `event` field is in `ledger/human-odds.jsonl`.
   - Rule 11 and H1 require the bet to carry it, and it was picked up after this design was frozen (`f4158c2` 16:29:15, pickup `f65b377` 16:30:43), so there is no contamination.
   - But `ledger/brier.md` prints one "event the odds were for" per row: this bet's event. And the engine's number on Sean's event is `engine_odds_first` 0.18, not 0.45.
   - Before data, state in §0 and the bet row (a `human_odds_note` update through the inbox) which of these applies:
     - (a) Sean's line is scored on this bet's outcome, and the human-against-engine comparison pairs it with 0.18 on the same card event, marked as an event mismatch; or
     - (b) it is left out of the human score.
   - Make this decision under rule 11 and state it in the commit, where Sean can veto it.

## Addendum: confirmation of the D98 fixes (commit 43cc063)

2026-11-05 17:26 America/Denver. Same reviewer session. I read D98 in `DEVIATIONS.md`, the new `experiments/dm6f2f2f1_opus.py`, `experiments/batch_runner.py`, `results/dm6f2f2f1-dry-run.json`, the re-elicitation in `experiments/dm6f2f2f1-odds.md` and the last update line in `ledger/inbox/p1-wave4.jsonl`. No paid call was made and no `.env` was loaded.
- `--selftest` passes. It now includes the 25-usable and 6-flagged leave-one-out cases and the three fake-client cases.
- `python3 ledger/check_prereg.py em-dm6f2f2f1 . programs/entangled-mind/experiments/dm6f2f2f1-opus.md --before-run`: L1–L3, R1 and H1 ok. R2 waits for this confirmation.
- D98 is used instead of the D94 I named, because D94 was already taken. That is fine.

**F1, the question set described as selected: confirmed.**
- D98 supersedes §1, §2, §6 and §0's "Adds" with the review's wording and counts.
- `SENTENCES` in the code now say "questions where Sonnet and Haiku had each given a number below 70% in at least one asking (mostly low numbers on 'No' guesses…)". The pass sentence adds "not on a fresh sample".
- The bet row's `title` and `odds_event` follow, in the inbox update line.
- `no_guess_below_half` is listed first among the secondaries. The archive stores guesses in lower case (`collections.Counter` over Sonnet's guesses: 'no' 767, 'yes' 275, None 158), so its test `guess == "no"` matches.

**F2, cost and cut-off inputs: confirmed.**
- `cost_sim()` now draws non-claim costs from Opus's unsure-set calls ($0.00239, n 32). My rerun gives the committed figures: P(all 40 run) 0.000, median 36 run (5–95%: 34–37), spend mean $0.2842, maximum $0.2922.
- My own fake client, run against the new `run()`, gives the same: unsure-set costs ran 38 questions for $0.2863; every reply at max_tokens ran 21 questions for $0.2928.
- The dry run now cuts at 3/32 (`cut_rate_unsure` 0.09375). It resamples only questions where the source model has all four cells, so Sonnet's missing cells are no longer counted twice. It runs the number of questions the cost simulation says will run.

**F3, the dry-run worlds: confirmed in design, with one new flaw (F7 below).**
- The knife-edge shrink is replaced by a quantile map of Sonnet's numbers onto Opus's 29 measured numbers.
- The referent-fixed world is added. In it only P cells are flipped: a "No" guess below 0.5 becomes 1 − x. The docstring says so, and I accept it as the author's stated choice.
- Each world now has 400 draws.
- Opus's parent pattern is stated: 6 complete questions, flagged only h039.
- I reran `dry_run()` and `cost_sim()` from a scratch script (output `rev-f1-x7/dry-rerun-d98.json`; the committed file was not touched). Committed figures first, my rerun second:

  | world | P(pass) | P(fail) | P(untestable) |
  |---|---|---|---|
  | Sonnet-like | 0.605 / 0.640 | 0.233 / 0.198 | 0.163 / 0.163 |
  | referent fixed | 0.590 / 0.552 | 0.253 / 0.290 | 0.158 / 0.158 |
  | Opus quantile | 0.4125 / 0.403 | 0.360 / 0.362 | 0.228 / 0.235 |
  | Haiku-like | 0.0925 / 0.090 | 0.738 / 0.740 | 0.170 / 0.170 |
  | no effect, Sonnet-like | 0.000 / 0.000 | 0.855 / 0.855 | 0.145 / 0.145 |
  | no effect, Opus quantile | 0.000 / 0.000 | 0.160 / 0.180 | 0.840 / 0.820 |

- D11 holds on both sets. Three effect worlds pass at least 0.40, every null passes 0.00, and every null fails at least 0.16.
- The numbers do not regenerate exactly. See F7.

**F4, leave-one-out with this bet's rule: confirmed.**
- `read_rule` sets `f2.MIN_Q = 0` and applies both floors through `verdict_here` to the reduced sample (n − 1 usable, flagged count less the removed question).
- Floor-only flips go to `loo_floor_flips`, pass-to-fail flips to `loo_flips`. The selftest asserts 25 floor flips and no statistic flips at exactly 25 usable, and exactly the 6 flagged questions as floor flips at exactly 6 flagged.
- `cluster_verdict` is recomputed with the floors.

**F5, the crash path: confirmed.**
- `batch_runner.recover()` stores a crashed batch's results with the refusal stop applied. I reran my own case: a refusal planted in batch 2, a crash while polling batch 2, then a restart. It stopped with "STOPPED on a refusal found in a crashed batch: opus|P|r0|h069", wrote the refusal record and created no further batch (2 batches in all). Before the fix it resubmitted the request in batch 3.
- A submission marker and the key map are written before `batches.create`. A marker with no batch ID is reconciled through `batches.list()` (creation time and request count), and anything other than exactly one match stops the run. The selftest's create-crash case adopts `fake_1` without resubmitting it.
- `real_list_adapter` maps the SDK's `request_counts` and `created_at` correctly.
- One behaviour to know: a `create` call that fails without making a batch also leaves a marker. That stops the next start-up for a person to clear. This fails safe and is not a flaw.

**F6, Sean's line: confirmed.**
- D98 and the inbox update pre-register before data: `human_event_mismatch: true`; scored on this bet's outcome; paired for the human-against-engine comparison with `engine_odds_first` 0.18; the decision stated under rule 11.
- The order of events is as I found it: design frozen at `f4158c2` (16:29:15), pickup at `f65b377` (16:30:43).
- A follow-up for the ledger session, not this bet's design: `ledger/brier.py` does not read `human_event_mismatch`. It prints this bet's `odds_event` as "the event the odds were for" beside Sean's 0.65. The mark should be printed in that table before this bet is scored.

**Odds re-elicited, 0.45 to 0.28 (fresh v2 context, prior 0.25, adjustment +0.03): recorded with all three numbers kept.** This is consistent with the rebuilt table.

### New flaw found in the confirmation

**F7 (D10): the committed dry run cannot be regenerated, because its draws depend on Python's hash seed.**
- In `dry_run()`, line 386 builds `ids = [q for q in U if …]` with `U = set(unsure_set(R))`.
- A set of strings iterates in an order that changes with `PYTHONHASHSEED`. On three runs, the first five simpleqa ids were `h055 h145 h297 h201 h026` (seed 1), `h297 h110 h063 h112 h094` (seed 2) and `h055 h145 h297 h201 h026` (seed 1 again).
- So `rng.choice(ids, …)` draws different questions in every new process, and `results/dm6f2f2f1-dry-run.json` does not regenerate from the committed code. My rerun moved P(pass) by up to 0.038 (Sonnet-like 0.605 against 0.640).
- The conclusions do not change. But a committed result that cannot be regenerated is a flaw in this repository's terms.
- Line 372 iterates over `U` too, but then sorts, so it is unaffected.
- **Fix:**
  - Iterate `sorted(U)` (or `unsure_set(R)`, which is already sorted) on line 386.
  - Rerun `--dry-run` and recommit `results/dm6f2f2f1-dry-run.json`.
  - Under a dated DEVIATIONS row before any call, restate the table if it moves. The odds stay 0.28 unless the table moves materially; if they are re-elicited, all numbers are kept.
  - Optionally assert in the selftest that two `dry_run(n_sims=5)` runs under different hash seeds give equal output.

**Verdict after confirmation: fix-first (1 remaining: F7).** F1–F6 are confirmed. Once F7 is fixed and recommitted, a short second addendum can confirm it and set `confirmed_at`. The front matter above is left as written; `confirmed_at` stays null until then.

## Second addendum: confirmation of F7 (D99, commit c7805e4)

2026-11-05 17:53 America/Denver. Same reviewer session. No paid call was made and no `.env` was loaded.

**F7, a dry run that does not depend on the hash seed: confirmed.**
- The diff in `c7805e4` changes one line, which is the fix asked for: `ids = [q for q in sorted(U) if …]`.
- I checked the other uses of `U` in `dry_run()` and `cost_sim()`. They are membership tests or sorted (`son_nums` is passed through `np.sort`; `ocells` and `pq` iterate over a dict, whose order is fixed). No other set-order dependence remains.
- I reran `dry_run()` from a scratch script under `PYTHONHASHSEED=3`, a seed neither the author nor I had used before (output in `rev-f1-x7/f7-check.txt`). Every world matches the committed `results/dm6f2f2f1-dry-run.json` exactly. The rerun printed `IDENTICAL`, and every world compared equal.
- The table matches D99. P(pass) / P(fail) / P(untestable) by world:

  | world | P(pass) | P(fail) | P(untestable) |
  |---|---|---|---|
  | Sonnet-like | 0.575 | 0.2625 | 0.1625 |
  | referent fixed | 0.6225 | 0.22 | 0.1575 |
  | Opus quantile map | 0.40 | 0.365 | 0.235 |
  | Haiku-like | 0.08 | 0.75 | 0.17 |
  | no format effect (Sonnet-like) | 0.00 | 0.855 | 0.145 |
  | no format effect (Opus quantile) | 0.00 | 0.1975 | 0.8025 |

- D11 holds. Three effect worlds pass at least 0.40, every null passes 0.00, and every null fails at least 0.1975.
- Haiku-like, at 0.08, is the one effect world below 0.10. D11 asks only for a world where the hypothesis holds to pass at least about 10%, and three do, so it is not a flaw. The results file should still say that a Haiku-like Opus would rarely pass.
- `--selftest` passes.
- The odds stay at 0.28, which is consistent with moves of at most 0.035.

A follow-up for the ledger session, not this design, carried over from the first addendum: `ledger/brier.py` should print `human_event_mismatch` before this bet is scored.

**Final verdict: go.** F1–F7 are confirmed, and `confirmed_at` is set above.
