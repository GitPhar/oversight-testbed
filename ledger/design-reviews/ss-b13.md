---
bet: ss-b13
program: settled-science
prereg_commit: 012449c
reviewer_session: fresh design-review subagent (ss-wave4 worktree; no chat or transcript read)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 10:30 America/Denver
checks: {D1: holds, D2: flaw, D3: holds, D4: holds, D5: holds, D6: flaw, D7: holds, D8: flaw, D9: holds, D10: flaw, D11: holds, D12: flaw}
prior_work_search: WebSearch (standard) "language model size predicting treatment effects of unpublished social science experiments accuracy smaller models" (the mechanism in social-science forecasting words, not the seed question's)
papers_opened: 3
flaws: 5
pilot_usd: 0.00
verdict: fix-first
confirmed_at: 2026-11-05 10:37 America/Denver (fixes a5142f5, DEVIATIONS D69, budget ruling br-010)
---

# Design review of ss-b13

## In plain English

As built, the test can answer its question. The rule is clear, a coin and the two shortcut rules all fail it, and it can come out either way under worlds built from measured numbers. Sonnet at Opus's level passes almost surely. Haiku at Opus's level, with the position bias measured on it in ss-b10, passes about 64% of the time. Haiku at the skill ss-b10 measured relative to Sonnet passes about 0–1% of the time. Five things need fixing before any call:
- Haiku 5.5 and Sonnet 5.5 have a refusal category (`frontier_llm`) that Opus 5.5 lacks. 88 of the 116 items are about LLM research, ss-b10's neuroscience run never tested this category, and a single refusal stops the whole run.
- The cost plan repeats ss-b10's underestimate, so Sonnet's round-2 step will probably be cut off by the cap.
- The pass sentence hard-codes "116" and says more about the rival than the design shows.
- The pre-registration says the dry run checks the option order, and it does not. I ran that check myself: it matches.
- The prior-work row says no paper reports Sonnet, but SciPredict reports Claude Sonnet 4.5, and the odds name neither paper.

None of these changes what is tested.

## Checks

**D1. A stranger can apply the rule: holds.** §5 reads per model: C1 upper bound < 0.25, and C2 and C3 upper bounds < −0.01, on both the item and the paper-cluster bootstrap. Pass needs both models, mixed exactly one, fail neither, and untestable means fewer than 100 of 116 on either model. I ran `scoring/score_f1.py` on synthetic tables for every verdict (scratchpad `d1.py`), and each gave exactly one verdict:
- coin → fail;
- oracle → pass;
- Opus's archive relabelled as both models → pass;
- Haiku coin with Sonnet Opus → mixed (and the reverse → mixed);
- Haiku with 99 round-1 bets → untestable;
- Haiku with 100 → pass;
- Sonnet missing → untestable.

Boundaries use EPS: the coin's C1 upper bound of exactly 0.250 fails, and each rule against itself (C2 or C3 = 0) fails.

**D2. The manipulations take effect: flaw (machinery claim).** The knob is the model. I checked the following on the code (scratchpad `order_check.py`, no calls):
- `f1.plan()` sends `j["model"]` into `common.structured`, and the cache key includes the model.
- The prompts are byte-identical to Opus's: under Opus's model name, 116 of 116 round-1 and 92 of 92 round-2 user texts hit Opus's cached keys in `bettor-cache.json` and `r2-bettor-cache.json`.
- The option order matches Opus's archive: 116 of 116 and 92 of 92, the same round-2 ids.
- Thinking settings: `bb-cache.json` shows Haiku ran `disabled` 500 times and Sonnet `between_tools` 474 times with no thinking block, and the code raises if one returns. This agrees with the platform docs: Sonnet 5.5 rejects `disabled`, and `between_tools` turns off up-front thinking.
- The up-word rule gives a 99, b 15, none 2, as §2 says.

**The flaw:** §2 says "`bettor/f1.py --dry-run` checks it against the archive: 116 of 116 and 92 of 92 match." The dry run does not do this. It prints only the per-step counts (b-first on 63 and 41). The match holds, but the pre-registration describes a check that is not in the code.

**D3. The controls can fail: holds.**
- Always-50% rejects a coin (C1 upper bound 0.250/0.250 → fail).
- The up-word and good-news rules reject themselves (`uprule`: C2 upper bound +0.000; `flatrule`: C3 upper bound +0.000 → fail).
- The Opus reference row reproduces ss-b1's published numbers: Brier 0.163 [0.139, 0.190], good-news rule 0.232.
- The cluster bootstrap is honest but nearly the same as the item bootstrap here (108 papers for 116 items, at most two per paper), so P14 is met without changing much.

**D4. Rivals are matched: holds, with a note.** The good-news rule is fixed at 0.75 on the writer's tag and has no free parameter to favour either side. Its accuracy on the 38 tagged items is 73.7%, so 0.75 is about calibrated. But it abstains on 78 of 116 items, so it cannot reproduce the best case of a model that applies "the paper's method works" to every item. That rival is live: ss-b10 measured Sonnet's flattery prompt at 92% of its forecasting skill on BrainBench. §6 says this, and the verdict sentences claim only to beat the rule, not to rule out the rival. §1's "the good-news rule is that rival, made into a predictor" overstates it. The wording fix is under D8.

**D5. A dumb baseline is beaten, and the design can see the effect: holds.** Dumb answer-free rules on the 116 (scratchpad `d5.py`), Brier at p = 0.6 / 0.75:

| rule | Brier at 0.6 | Brier at 0.75 |
|---|---|---|
| shorter option | 0.243 | 0.254 |
| longer option | 0.269 | 0.318 |
| down-word | 0.258 | 0.307 |
| headline, else down-word | 0.237 | 0.255 |
| always the writer's option_a (true on 72 of 116) | 0.236 | 0.252 |

Negation cues never differ between options. The bettor cannot see option_a: order is randomised and matches Opus's draw. Passing needs a Brier of about 0.19 or less, because C3's upper bound sits about 0.032 above its mean. No dumb rule comes near that. This is not a no-difference rule, so no equivalence margin is needed.

**D6. Foreseeable execution risks are piloted: flaw.** The pre-mortem is of kind `world`, and the brief says ss-b10 measured the execution risk. It did not cover this one:
- Haiku 5.5 and Sonnet 5.5 run safety classifiers with a `frontier_llm` category ("could assist the development of competing AI models"; the claude-api model-migration reference, Sonnet 5.5 §Safeguards and Haiku 5.5 §Safeguards). Opus 5.5's categories are cyber, bio and reasoning_extraction, so Opus's archive could never have shown this.
- 88 of the 116 round-1 post-cutoff items are interpretability (29), scalable-oversight (30) or model-psychology (29), all methods of frontier-LLM research. Round 2 draws from the same four fields.
- ss-b10's 974 Haiku and Sonnet calls were neuroscience abstracts, and `grep` finds no `frontier_llm` anywhere in the repository.
- Under §7, one refusal stops everything. A refusal in step 1 makes the bet untestable, and steps 3 and 4 never run.

This is a foreseeable refusal category, and nothing has piloted it. I was barred from paid calls, so I could not pilot it.

**D7. The comparisons match: holds.** The rule compares each model with fixed rules on the same items, so nothing differs there but the predictor. The reported comparison with Opus differs in model, thinking (named in §5.5 and §6), the refusal classifiers (see D6) and the call date. Prompt bytes, option order, schema, `max_tokens` 4000 and the absence of tools are matched (D2).

The cutoff in "posted after the models' training cutoff" holds for all three models. The platform models overview (platform.claude.com/docs/en/about-claude/models/overview, read 2026-11-05) gives the training data cutoff as June 2026 for Opus 5.5, Sonnet 5.5 and Haiku 5.5. `protocol/fixed-rules.md` fixes it for Opus only; citing the overview in the results would close that gap.

Note (not a flaw): the single order costs Haiku points for position, not knowledge. ss-b10 measured Haiku's Option-1 pull at +11.8 points and Sonnet's at +7.3; Opus's own pull on round 1's order check is −0.5. A Haiku order check as a reported row would cost about $0.02.

**D8. The verdict sentences are written: flaw.** `score_f1.sentences` produces all four verdicts and the reported clauses verbatim (D1 run). Two faults:
- (a) The pass and mixed sentences hard-code "116 findings". In the edge case run (Haiku 100 scored) the pass sentence still says "On round 1's 116 findings". Between 100 and 115 scored is a legal pass, and items would be lost in id order, not at random.
- (b) The pass sentence's "Knowing which way these findings went is not only the strongest model's" uses a noun the design cannot carry, by its own §6. It also does not say that the good-news rule abstains on 78 of 116 items (D4).

**D9. One item cannot decide it: holds.** Leave-one-item-out and leave-one-field-out are pre-registered and run on each model's label (`model_result`). A flip is reported as "rests on …" and does not change the verdict (§4, §5.5). In the Opus-relabelled world, no single item flips the label.

**D10. Machinery: flaw (cost plan).** These hold:
- Both caps are in code: `cap()` = spent elsewhere + $0.70, under the program cap; `Caller` stops at cap − $0.05.
- Stop-on-refusal writes `results/refusal.md` and exits, and `write_out` runs in `finally`.
- One scale direction is used throughout.
- Caching is by content hash, with `f1-cache.json` registered in `CACHES`.
- `seed_source: fixed` is correct (no draw).
- The lesson `ls-ss-b13` matches §0 word for word, and the ledger row's `odds_event` matches §5.

**The flaw:** §3's $0.51 uses `estimate()`, which assumes 160 output tokens and characters / 3.6 for input. That method gives about 395 input tokens per call, while Opus measured 646 on these exact prompts. ss-b10 measured, on these two models with this schema, Sonnet at 202 output tokens and $0.0049 per call, and Haiku at 218. At measured tokens:
- Sonnet costs about $0.0030–0.0033 per call here, so $0.62–0.69 for 208 calls;
- Haiku costs about $0.04;
- the total is about $0.66–0.73, against an effective stop at $0.65.

Step 3 (Sonnet round 1, the rule) finishes at about $0.42 cumulative, so the rule is safe. Step 4 (Sonnet round 2, reported) will probably stop at about 60–75 of 92, cut in id order. This is the D10 miss ss-b10's audit recorded (D61), and ss-b10b fixed it in D65 ("costed from measured tokens"), but ss-b13 did not.

**D11. The bet can both pass and fail: holds.** I built the worlds from measured numbers (P15; scratchpad `d11.py`, 300 call-noise draws per world, B = 2,000 per bootstrap, same percentile indices). The parts:
- Opus's archived logits, multiplied by a skill scale s;
- call noise SD 0.24 logit, measured from Opus's primary and order-check pairs (55 post-cutoff items);
- each model's Option-1 pull as measured in ss-b10.

| world | P(one model meets the rule) | mean Brier |
|---|---|---|
| Opus re-drawn (s 1, pull 0) | 1.00 | 0.167 |
| Sonnet = Opus skill, pull +7.3 | 1.00 | 0.173 |
| Haiku = Opus skill, pull +11.8 | 0.64 | 0.182 |
| s 0.8, pull +7.3 | 0.90 | 0.182 |
| Haiku at ss-b10's measured skill relative to Sonnet (s 0.5–0.7, noise SD 0.5, pull +11.8) | 0.00–0.01 | 0.209–0.224 |
| `noisy-opus` (SD 0.8) | 0.21 | 0.191 |

On ss-b10's forecasting prompt, Haiku's Brier skill was 0.51 of Sonnet's (0.073 against 0.142).
- **Hold world** (both at Opus's skill, measured pulls): P(pass) ≈ 0.64.
- **Non-hold world** (Haiku at ss-b10's relative skill): P(pass) ≈ 0.01, P(fail or mixed) ≈ 0.99.

Both clear the 10% floor. The engine's 0.18 fits a prior that puts most weight on the non-hold world for Haiku. The rule has a cliff near Brier 0.19 for each model.

**D12. The prior work line: flaw.**
- (a) **Holds.** The row states predicted outcomes with citations: BrainBench predicts pass for smaller models, and SciPredict predicts fail for verbal probabilities.
- (b) **Partly holds.**
  - BrainBench (arXiv 2403.03230; abstract and HTML v4 opened) says what it is cited for: 15 LLMs, "every LLM outperformed human experts", 81.4% against 63.4%, 7B models "performed comparably to larger models", chat or instruction-tuned models worse than base (t(5) = 5.4, p = .002), and scoring by lower perplexity.
  - SciPredict (arXiv 2604.10718; abstract and HTML opened) does report model accuracy of 14–26% against about 20% for experts, with confidence "weak, inconsistent, and often non-monotonic" against accuracy. But it evaluates **Claude Sonnet 4.5** beside Opus 4.1 and 4.5, and Sonnet 4.5 is close to Opus 4.5. Overall (no background knowledge) it is 22.55 against 23.05; on multiple choice, 29.01 against 33.54 (Tables 3 and 4). No Haiku is tested.
  - So §0's "No paper reports Haiku or Sonnet" is wrong for Sonnet (another version), and the row leaves out the one per-model fact in print that bears on the Sonnet conjunct: it predicts Sonnet tracks Opus.
  - SciPredict's tasks are 3–4-option, free-form and numerical, not binary directions, so "predicts fail" there is an inference.
- (c) **Flaw.** BrainBench's "pass for smaller models" is in print on other models, and §0 says what the bet adds (rule-12 replication on Haiku and Sonnet, the shortcut rules, the cluster bootstrap). But the odds rationale and the lesson name neither paper, and the 0.18 is far from BrainBench's pass. The reason given (the stricter bar) is not tied to the paper.
- (d) **My search** (terms in the header) found Hewitt, Ashokkumar, Ghezae and Willer (Stanford). GPT-4 simulating respondents predicted 70 pre-registered US survey experiments at r = 0.85, and r = 0.90 on studies unpublished before the training cutoff, with accuracy reported high also for open-weight models (the project page and search summaries; the PDF did not render). It predicts that capable models below the frontier still forecast unpublished results. It gives no size comparison I could read, and it uses another measurement (effect correlations, not direction Brier). It adds no prediction that changes this bet.

Commands run (all $0): `bettor/f1.py --dry-run`; `scoring/score_f1.py --synthetic coin oracle uprule flatrule opus noisy-opus`; and the reviewer scripts `order_check.py`, `measure.py`, `d1.py`, `d5.py` and `d11.py` (in this session's scratchpad, not committed).

## Required fixes

Each fix is to be written under one dated DEVIATIONS row before any call, naming this review. The next free number is D67. The reviewer confirms each in an addendum.

1. **D6, the refusal pilot.**
   - **Fix:** before step 1, pilot at most $0.10 on items excluded from the test: 12 round-1 pre-cutoff items from interpretability, scalable-oversight and model-psychology (52 such items exist), on both Haiku and Sonnet, with the unchanged prompt, through `common.structured`, into a separate pilot cache registered in `CACHES` (about $0.05). Record the refusal count and category, parse failures and output tokens.
   - **If any refusal:** stop and re-review before data. Do not reword, and do not write a filter after seeing which items refused.
   - **DEVIATIONS text:** "D67 (1). Design review ss-b13 (D6): Haiku 5.5 and Sonnet 5.5 run a `frontier_llm` refusal classifier that Opus 5.5 does not, and 88 of the 116 items are LLM-research findings; ss-b10's neuroscience calls did not test it. Before any test call, a pilot of ≤$0.10 ran on 12 pre-cutoff items from the three LLM fields (excluded from the test) on each model, cache `bettor/f1-pilot-cache.json`: <n> refusals, <n> parse failures, mean output tokens Haiku <x>, Sonnet <y>. Pilot results are not test data."

2. **D10, the cost plan.**
   - **Fix:** re-cost from measured tokens (Opus's 646 input tokens per call on these prompts; ss-b10's 202 Sonnet and 218 Haiku output tokens; or the pilot's), about $0.70 in total. Then either (a) a budget-ruling amendment to br-007 lifting the bet cap to $0.85 (the program cap has room: $13.40), or (b) keep $0.70 and pre-state that step 4 is expected to stop at about 60–75 of 92, and that its rows are reported with their n and marked "cut by the cap, in id order". The rule's steps 1 and 3 are unaffected either way.
   - **DEVIATIONS text:** "D67 (2). Design review ss-b13 (D10): §3's $0.51 used 160 output tokens and characters/3.6 for input (about 395 tokens against Opus's measured 646); at measured tokens the run costs about $0.70 against an effective stop at $0.65 (cap − $0.05), the D10 miss ss-b10's audit recorded (D61). <Either: br-007 amended to $0.85, ledger/spend.jsonl, BET_CAP 0.85.> <Or: the cap is kept; step 4 (Sonnet, round 2, reported only) may stop at about 60–75 of 92, reported with its n and labelled as cut by the cap in id order.> Steps 1 and 3, which carry the rule, finish at about $0.42."

3. **D8, the verdict sentences.**
   - **Fix:** in `score_f1.sentences`, replace the hard-coded "116 findings" in the pass and mixed sentences with the scored counts ("<n_H> (Haiku) and <n_S> (Sonnet) of round 1's 116 …").
   - **Also:** replace "Knowing which way these findings went is not only the strongest model's;" with "Picking which way these findings went, better than these two shortcut rules, is not only the strongest model's; the good-news rule bets on only the 38 of 116 items the writers tagged, so this does not rule out a model applying the good-news idea to every item, which matched 92% of Sonnet's forecasting skill on BrainBench (ss-b10);". Keep the rest. This tightens the claim and leaves the bar unchanged.
   - **DEVIATIONS text:** "D67 (3). Design review ss-b13 (D8, D4): §5's sentences now state the number of items scored per model instead of '116', and the pass sentence's 'Knowing which way these findings went' becomes 'Picking which way these findings went, better than these two shortcut rules', with a clause that the good-news rule bets on only 38 of the 116 items and so does not rule out a model-applied good-news heuristic (ss-b10: 92% of Sonnet's forecasting skill on BrainBench). The rule and the bar are unchanged; `score_f1.py` edited before any call."

4. **D2, the order check.**
   - **Fix:** add the archive check to `f1.py --dry-run`: compare each job's `option_1_is` with `bettor/bets.jsonl` and `r2-bets.jsonl`, compare the user-text keys with Opus's caches, and print "order matches archive: 116/116, 92/92; prompts identical to Opus's: 116/116, 92/92". Or, if the code is left alone, correct §2's claim in DEVIATIONS.
   - **DEVIATIONS text:** "D67 (4). Design review ss-b13 (D2): §2 said `f1.py --dry-run` checks the option order against Opus's archive; it did not. The check is now in the dry run <or: was run by the reviewer>: the order matches 116/116 and 92/92, and every user text is byte-identical to Opus's cached prompt (116/116, 92/92)."

5. **D12, the prior work.**
   - **Fix:** correct §0's prior-work statement and tie the odds to the papers.
   - **DEVIATIONS text:** "D67 (5). Design review ss-b13 (D12): §0's 'No paper reports Haiku or Sonnet' is corrected. SciPredict (arXiv 2604.10718) evaluates Claude Sonnet 4.5 beside Opus 4.1 and 4.5 and finds Sonnet 4.5 close to Opus 4.5 (overall 22.55 against 23.05; multiple choice 29.01 against 33.54, no background knowledge), which predicts that Sonnet tracks Opus; no paper tests Haiku or these versions with verbal probabilities on masked post-cutoff findings. The odds are stated with BrainBench's pass for smaller models and SciPredict's Sonnet≈Opus in view: the Sonnet conjunct is likely, and the 0.18 rests on the Haiku conjunct under the stricter bar (C3 needs a Brier of about 0.19 or less; at ss-b10's measured Haiku-to-Sonnet skill ratio Haiku's Brier would be about 0.21–0.22). <Odds unchanged at 0.18 | revised to x, both kept.>"

## Addendum: fixes confirmed (2026-11-05 10:37 America/Denver)

This addendum checks commit a5142f5 (DEVIATIONS D69, written before any test call; the numbers D67 and D68 went to the withdrawals of ss-b14 and ss-b10b) and budget ruling br-010 in `ledger/spend.jsonl`. I made no paid calls. I re-ran `bettor/f1.py --dry-run` and `scoring/score_f1.py --synthetic coin opus`, plus the review's `d1.py` tables. `bettor/f1-cache.json` does not exist, so no test call has run.

1. **F1 (D6), refusal pilot: confirmed.** `bettor/f1-pilot-cache.json` holds 24 calls:
   - 12 per model, with Haiku `disabled` and Sonnet `between_tools`;
   - all on round-1 **pre-cutoff** items (4 each from interpretability, scalable-oversight and model-psychology), so none is in the test;
   - pilot keys use the prefix `bettor-v1-pilot`, so they cannot collide with the test cache;
   - cost $0.037 (≤ $0.10); `p_option_1` ranges from 5 to 90, so every reply parsed;
   - no refusal and no error: `Caller` exits on either before writing the summary.

   The cache is in `common.CACHES`, so its cost counts toward the program cap. Residual risk, which the pilot cannot remove: 0 of 24 bounds the per-call refusal rate only to about ≤ 12% (rule of three). A refusal in the test would still stop the run under §7 and could make the bet untestable. That is the program's rule, and D69 does not loosen it.

2. **F2 (D10), cost plan: confirmed.** `BET_CAP` is 0.85 (br-010 amends br-007; the program cap of $13.40 is unchanged). The pilot measured 657 input tokens per call and 164 output for Haiku, 163 for Sonnet: $0.00295 per Sonnet call and $0.00015 per Haiku call. That puts the 416 calls at about $0.64. The effective stop is $0.80 (cap − $0.05), so the run has room even at ss-b10's 202 Sonnet output tokens (about $0.70). The pilot sits in its own cache and counts outside `cap()`'s own-cache term, so the bet's total stays at or below $0.84.

   Cosmetic, not required: the dry run still prints the old estimator's "$0.51". D69 and br-010 carry the measured figure.

3. **F3 (D8, D4), verdict sentences: confirmed.** All three verdict sentences now start "On <n_H> (Haiku) and <n_S> (Sonnet) of round 1's 116 …". The edge table (Haiku 100 scored) prints "On 100 (Haiku) and 116 (Sonnet) …". The pass sentence carries "Picking which way these findings went, better than these two shortcut rules" and the clause about 38 of 116 items and ss-b10's 92%. Verdicts are unchanged on every synthetic table (coin fail; Opus pass; both mixed cases mixed; 99 untestable; 100 pass; Sonnet missing untestable), so the rule and the bar did not move.

4. **F4 (D2), archive check: confirmed.** The dry run now prints "r1: order matches archive 116/116; prompts identical to Opus's 116/116" and "r2: … 92/92; … 92/92". `archive_check` reads only Haiku's jobs, but `plan()` builds Sonnet's jobs from the same items, swaps and `user_text`, so they are identical by construction.

5. **F5 (D12), prior work: confirmed.** D69 (5) corrects §0's statement with SciPredict's Sonnet 4.5 and Opus 4.5 figures, as opened in this review. It states the odds with both papers in view and keeps 0.18 with a reason (the Haiku conjunct under the C3 bar; the review's worlds put P(pass) between 0.01 and 0.64). The frozen §0 is left as written, with the correction in DEVIATIONS, as fix-first requires.

All five hold, and none lowers the bar. **Verdict: go.**
