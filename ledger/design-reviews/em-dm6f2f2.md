---
bet: em-dm6f2f2
program: entangled-mind
prereg_commit: 33d18d7
reviewer_session: fresh design-review subagent (worktree oversight-testbed-p1-wave3; has not seen the authoring session)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 11:27 America/Denver
checks: {D1: holds, D2: flaw, D3: holds, D4: holds, D5: holds, D6: holds, D7: flaw, D8: flaw, D9: holds, D10: flaw, D11: holds, D12: flaw}
prior_work_search: "format dependence subjective probability calibration half-range full-range confidence chosen answer versus probability statement true" (WebSearch, 2026-11-05), then "Juslin Wennerholm Olsson 1999 Format dependence in subjective probability calibration"
papers_opened: 2
flaws: 5
pilot_usd: 0.0246
verdict: fix-first
confirmed_at: null
---

# Design review of em-dm6f2f2

## In plain English

The test can answer its narrow question as built: on Sonnet, with both templates reworded the same way, does the overseer's under-70% list still change with format? The statistic, the bars and the bootstrap are em-dm6f2's, imported unchanged. They work, and the code runs end to end with a fake Batches client. Two things stop the result from meaning what its sentences say.

First, nothing checks that the rewording changed what Sonnet's number refers to. In the dry run's own "rewording changes nothing" world the bet passes 100% of the time, and the pass sentence would then say the gap "is not only the old wording's double meaning". The pilot also found one Sonnet "No" answer under the new frequency wording that still gave the proposed answer's chance (3 out of 100).

Second, the pilot shows the new clause changes more than the referent. It turns Sonnet's open answers ("Guess: 40 W", "Guess: 1889") into Yes/No guesses: 5 of 5 in the pilot. In em-dm6's archive only 31% of simpleqa and 64% of science probability-format answers were Yes/No.

Three smaller fixes:
- the pass sentence drops em-dm6f2's "more or other questions" caveat;
- the Kim and Kang 2026 citation describes a different experiment from the one the paper ran;
- the cache is not keyed by content.

All five can be fixed before any call without changing what is tested.

## Checks

**D1. A stranger can apply the rule: holds.** §5 maps to one function (`dm6f2_flag_overlap.verdict`): untestable if n < 40; pass if J_F < 0.70, J_F's upper bound < 0.70, D ≥ 0.10 and D's lower bound > 0; fail otherwise. I ran `run()` with a fake Batches client and then `analyse()` on three synthetic worlds, with all outputs redirected to the scratchpad:
- F shifted +0.25 gave pass, D +0.528;
- exchangeable formats gave fail, D −0.006;
- Opus on 24 questions gave untestable.

`dm6f2_flag_overlap.py --selftest` covers 30 questions (untestable) and the 1e-9 boundaries: SELFTEST OK. Each case returned exactly one verdict.

If Sonnet's wave is not run, the code returns the label "not run" with the untestable sentence. §5 does not name that case, but it cannot happen without a cap failure, which §3 reports as "not run". Cosmetic: `opus_questions`'s docstring says "10 per category" but the code draws 6. And Opus is printed with the label "untestable", although §0 says it is reported "without a label".

**D2. Every manipulation takes effect: flaw.**
- *The knob is applied.* `--print-prompts` shows each template differs from `cal_format.TIAN_P` / `TIAN_F` by exactly the one clause. A fake-client run confirms that NEW_P / NEW_F are in the requests actually sent. The parameters sent match §2: Sonnet `max_tokens` 300 with `thinking: between_tools`; Haiku thinking disabled; Opus `max_tokens` 1000 with `output_config.effort: low`.
- *Nothing checks that it acts on the model.* The manipulation is "the number now refers to the model's own guess". The only measure of it is a science-only secondary ("no below half") that cannot change any sentence. The dry run's "unchanged" world passes at 1.00, and in that world the pass sentence's second clause ("not only the old wording's double meaning") is unsupported, because the double meaning is still there.
- *Pilot evidence that the risk is real.* Under the new frequency template, Sonnet answered "Guess: No / Frequency: 3" on the pH question (0.0010 M HCl; gold No). That is the proposed-answer chance, the reading the clause was meant to remove (msg_011CgkFSZh6mMWxaznXmz1RG). The other 3 of 4 new-template No answers were 97–99.
- *An archive baseline exists.* For a binary question, a best guess carrying a number below 0.5 is incoherent under the own-guess reading. In em-dm6's archive that share was 101/199 = 0.51 of Sonnet's Yes/No-guess answers in the probability format and 33/158 = 0.21 in the frequency format.
- Fix 1 below.

**D3. Every control can fail: holds.** The control is J_N (two askings, same format).
- A world of four exchangeable noisy replicates (Sonnet-like confidence values, noise SD 0.12, n = 272) passed 0 of 100 times.
- em-dm6f2's selftest worlds "identical formats" and "noise only" fail.
- The dry run's "no format effect" world is degenerate: P cells are copies of the F cells, so D = 0 exactly. That is why it fails 100%. The exchangeable-noise world above is the fair version, and it also fails.

**D4. Rivals are matched: holds.** The rivals are the referent reading (predicts fail) and a format effect on confidence (predicts pass). Neither wins by construction:
- a pure level shift passes;
- an exchangeable null fails.

The dry run's "referent fixed" world (0.99 pass) is partly an artifact:
- the flip is applied per cell, so replicates disagree when one P replicate's guess parses as "no" and the other's does not (18 of 94 science questions). This lowers J_N from 0.756 to 0.674;
- applied to simpleqa as well, the flip raises simpleqa's D from +0.083 to +0.178.

With the flip limited to science, where the mechanism is claimed, the point D is +0.145 and P(pass) is 0.89 (100 resamples, nboot 1000). That is still a pass-leaning world, but the odds reason's "99%" should name it (recommendation, not a required fix).

**D5. A dumb baseline is beaten: holds, with a sentence consequence.**
- A constant 0.95 in every cell fails.
- A one-bit level shift (P always 0.5, F always 0.9) passes. That is within the claim ("a different set"), but it is why em-dm6f2's sentence carried "cannot say whether one format flags more questions or other questions". See D8.
- This is not a null rule, so no equivalence margin is needed.

**D6. Execution risks piloted: holds.** Pilot $0.0246, 28 direct calls, run from the scratchpad. The questions were self-written and asserted absent from `pool-run-3.json`. The script kept a running cost total with a worst-case gate at $0.10, stopped on any refusal, and never retried. No pilot row went into results/. Results:
- Opus at effort low, new template: 8/8 parsed, 0 at max_tokens, 15–47 output tokens. That is $0.0012–0.0019 at full price, about $0.0006–0.0009 at the batch rate, below the $0.0023 estimate.
- Sonnet, new template: 12/12 parsed, 0 at max_tokens, 15–18 output tokens.
- Sonnet, old template: 8/8 had a number, but 5 of 8 guesses were open-form and so unparsed as Yes/No. See D7.
- No refusals.

So the cap holds comfortably in practice. One more fake-client finding: if every Opus reply hit its 1000-token cap, the total would be $1.68, because the cap is checked only against the pre-wave estimate. Splitting the Opus wave into chunks, each checked at worst case, would close that (recommendation). The pilot cost suggests Opus could reach em-dm6f2's 40-question floor (10 per category, as the docstring says) within the cap (recommendation).

**D7. Comparisons match: flaw.** The primary comparison is P against F, both under the new template. These differ only in format, so they are matched. The claim's interpretation is against em-dm6f2 ("not only the old wording's double meaning"; "consistent with the old wording's double meaning carrying em-dm6f2's gap"). That comparison differs in:
- the clause (named);
- the date, fresh calls against the archive (named in §6);
- **the guess form (not named).** The clause "if your guess is No" turns open answers into Yes/No guesses. Pilot, Sonnet, same eight questions: old template 3/8 Yes/No, new template 8/8. Archive: probability-format Yes/No share 69/99 chemistry, 57/98 physics, 73/237 simpleqa, 0/120 claim ("Guess: True").

So a fail could come from the task becoming a Yes/No verification task, as much as from the referent. Simpleqa is 118 of the 272 usable questions, and in the archive most of its flags were open-form low numbers. The secondary "no below half" then compares different subsets: the old template's 'no' answers are those Sonnet chose to phrase as No. Fix 2.

**D8. Verdict sentences written: flaw.** Sentences exist for pass, fail and untestable, verbatim in code. But:
- (a) the pass sentence dropped em-dm6f2's caveat "This design cannot say whether one format flags more questions or other questions", which D5 shows is still needed;
- (b) em-dm6f2's D63 noise-asymmetry addendum is computed (`r["noise_asymmetric"]`) but never reaches the verdict sentence or the tables. J_PP and J_FF are not printed either;
- (c) `results/dm6f2f2-own-guess.json` would carry em-dm6f2's per-model sentence "On this archive, …" under `models.sonnet.sentence` (seen in the fake run), which is false for fresh calls;
- (d) the fail sentence attributes the outcome only to the double meaning (see D7).

Fix 3, and Fix 2 for (d).

**D9. One item cannot decide it: holds.** Leave-one-question-out is computed (`loo_flips`), and §5 says the results file reports a flip first. As inherited from em-dm6f2, it reuses the full-sample intervals rather than re-bootstrapping. With n near 272 and a parent margin of +0.12 over the bar, this is acceptable. §5 does not say whether the verdict stands when one item flips it; the reading is that it stands with the flip reported, as em-dm6f2f1 wrote. Recommendation: say so.

**D10. Machinery: flaw (caching).**
- *Budget:* checked in code before each wave (spent + estimate × 1.10 + $0.02 ≤ $1.00). A fake-client run billing the estimates completes all three models (the §3 claim of $0.943). Batch IDs are saved before polling, and orphaned batches are collected and costed. A wave whose estimate does not fit is not run.
- *Stop on refusal:* in code. It writes `results/refusal-dm6f2f2.md`, exits, and a rerun refuses to start.
- *Persistently errored requests:* exactly 3 submissions, then stop.
- *Scale:* one direction (1 = sure the guess is right).
- *Seed:* the pulse after the commit. 1592560 at 18:16:00Z is after 33d18d7's author time of 18:15:51Z, and `ledger/seed.py` reproduces bootstrap 12892736311446276367 and items 14564298516711186911.
- *Lesson:* ls-em-dm6f2f2 is present and identical to the §0 row.
- *Imports:* the script puts this worktree's `src` first on sys.path; checked, `entangled_mind.__file__` resolves to the worktree. Importing `cal_format` and `mm_common` writes nothing: `load_dotenv` of a missing `programs/entangled-mind/.env` and a lazily created client. `git status` stayed clean.
- **Flaw:** the cache is keyed `model|fmt|rN|qid`, not by content hash. An entry made under any other template or parameters would be silently reused. Fix 4.

**D11. The bet can pass and fail: holds.** The design's worlds give P(pass) of 1.00 (unchanged), 0.99 (referent fixed) and 0.00 (no format effect); I reproduced all three in 11 s, without writing the dry-run file. My two worlds give 0.89 (science-only referent fix) and 0.00 (exchangeable null). Both outcomes are reachable under worlds the design names.

**D12. Prior work: flaw at (b).**
- (a) The line states a predicted outcome: "Predicts: unknown", with a stated search and what the bet adds. That is acceptable.
- (b) **Kim and Kang 2026** (arXiv:2605.27752, abstract and HTML opened). The main study holds each verbalized answer and its score fixed and varies the *context in which the token probability is read* (bare question, "Answer:", "Guess:"). The 19/20 (ECE) and 17/20 (AUROC) intervals are shifts in the *verbalized-minus-token gap*. "Mostly through the instruction rather than the answer's position" refers to that scoring context. The verbalized instruction is not varied in the main study; its one verbalized-wording variation is a 0–100 integer scale (App. B.1). The models are Llama-3-8B, Mistral-7B, Qwen2.5-7B, Qwen3.5-9B and Ministral-3-8B, plus four up to 72B. §0 and the map cite it as "changing the confidence instruction shifts calibration (…19 and 17 of 20 settings)… predicts the rewording moves which answers fall under a threshold", which is not what those numbers measure. The abstract does say stated confidence depends on how a supplied answer is worded, which is the defensible link.
- **Tian et al. 2023** (arXiv:2305.14975, abstract opened). Correctly cited as the source template; models were ChatGPT, GPT-4 and Claude.
- (c) No prior statement of this pass rule was found, so not applicable.
- (d) My own search, in judgment-and-decision-making words (terms in the header), found the human calibration literature on **format dependence**, and specifically the half-range versus full-range distinction: "probability that my chosen answer is correct" against "probability that the statement is true". This is Ferrell's calibration model; Juslin, Wennerholm and Olsson 1999 (JEP:LMC); and Winman, Hansson and Juslin 2004 (JEP:LMC, "Subjective probability intervals: how to reduce overconfidence by interval evaluation"). That is this bet's referent mechanism, studied in people. The literature reports that the same judgments look over- or underconfident depending on format. I saw these only in search snippets and did not open them, so I record them as leads, not as a prediction for this pass rule. None tests threshold-list overlap on LLMs. Fix 5.

## Required fixes

Each needs a dated DEVIATIONS.md row (next free number after D85), written before any call and naming this review.

1. **(D2) Pre-register a manipulation check that gates the interpretive sentence.**
   - §5 and `analyse()` add: for Sonnet, in each format, over all categories, the share of answers with a parsed Yes/No guess whose number is below 0.5. Report it beside em-dm6's archive values (P 101/199 = 0.51, F 33/158 = 0.21).
   - The rewording "took effect" iff the share is ≤ 0.10 in both formats.
   - The verdict and score are unchanged.
   - If it did not take effect, the second sentence of the pass or fail text is replaced verbatim by: "The rewording did not remove numbers below 0.5 on Yes/No guesses (probability format <x>, frequency format <y>), so this result does not separate the old wording's double meaning from other explanations."
   - Store the values in `out["manipulation"]`.
2. **(D7, D8d) Name the guess-form change and rewrite the fail sentence as about the bundle.**
   - §6 adds: "The new clause also turns open answers into Yes/No guesses (pilot 8/8 against 3/8; archive simpleqa 73/237)."
   - The fail sentence's second sentence becomes: "This is consistent with the old wording's double meaning, or the new wording's switch to Yes/No guesses, carrying em-dm6f2's gap; the design does not show which."
   - Add a reported secondary: the share of Yes/No-parsed guesses per cell and category, new template against archive.
3. **(D8a–c) Restore em-dm6f2's caveats and drop its stale sentence.**
   - Append to the pass sentence, verbatim: "This design cannot say whether one format flags more questions or other questions."
   - When `r["noise_asymmetric"]` is true, append em-dm6f2's addendum (the `f2.analyse` text) to the top-level sentence.
   - Print J_PP, J_FF and the asymmetry flag in the tables.
   - Set `out["models"][m]["sentence"] = None` for every model, so em-dm6f2's "On this archive" sentence is not written.
4. **(D10) Content-hash the cache.**
   - Store `"sha": sha256(json.dumps(params(m, text), sort_keys=True))` in each cache entry.
   - In `run()`, reuse an entry only if its key exists and its `sha` matches. Otherwise stop with an error; do not resubmit silently.
5. **(D12b) Correct the Kim and Kang 2026 description** in §0's prior work row and the map's `prior_work_line`, to: "Kim and Kang 2026 hold verbalized answers and scores fixed and vary the context in which token probability is read; the verbalized-minus-token gap shifts (19/20 ECE, 17/20 AUROC, 95% intervals), mostly through that context's instruction text; their verbalized-wording variation is a 0–100 scale (App. B.1); stated confidence also depends on how a supplied answer is worded. Human calibration work on format dependence (half-range 'my answer is correct' against full-range 'the statement is true'; Ferrell; Juslin, Wennerholm and Olsson 1999; Winman, Hansson and Juslin 2004) names the referent mechanism in people; none tests threshold-list overlap. Predicts: unknown." Keep both odds if they move.

Recommendations (not required): name the science-only referent world (0.89) in the odds reason; check the Opus wave in chunks at worst-case cost, or raise Opus to 10 per category, since the pilot cost was about $0.0008 per request at the batch rate; say in §5 that a one-question flip leaves the verdict standing, with the flip reported; fix the `opus_questions` docstring.
