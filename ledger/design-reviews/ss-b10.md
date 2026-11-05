---
bet: ss-b10
program: settled-science
prereg_commit: ef2fa6b
seed_commit: 70efc56
code_commit: 7cb74dd
reviewer_session: design-review ss-b10 (fresh subagent launched by the engine session; no chat, transcript or author message read)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true          # reviewer, author and the flattery and bettor prompts' models are all Claude
date: 2026-11-05 06:51 America/Denver
checks: {D1: flaw, D2: holds, D3: holds, D4: holds, D5: holds, D6: holds, D7: flaw, D8: flaw, D9: holds, D10: holds, D11: holds, R12: flaw}
flaws: 4
pilot_usd: 0.00
verdict: fix-first
confirmed_at: 2026-11-05 07:03 America/Denver (fixes D54 at 386d462, D56 at 418d79b)
---

# Design review of ss-b10

## In plain English

As built, this test can answer its question. At n = 200 it can both pass and fail: if both models' flattery prompt is truly right about 70% of the time, it passes 29–54% of the time; at 60% it essentially never passes. The code does what the pre-registration says. The option order follows the beacon seed, the two prompts are the frozen texts, ties score 0.5, the bootstrap and the 0.634 threshold are as written, and the caps and the refusal stop hold in a stubbed run. Four things must change before the first call, none of which changes what is tested:
- the "untestable" rule lets a non-pass that is already settled go unscored;
- two verdict sentences claim a mechanism ("valence shortcut … solves much of BrainBench", "does not account for") the design cannot show;
- the bettor comparison is worded as if only the question changed, when the two prompts differ in three ways;
- the reason for leaving Opus out is cost, which CONTEXT rule 12 says is not a reason.

The five text-only baselines all score at chance on the frozen items (0.48–0.505), so none of them can explain a pass.

## Checks

Commands ran from `/Users/seanpharris/oversight-testbed` (repo root) or `programs/settled-science`. Paid calls: none. Scratch scripts are in `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/6509f5b7-80b2-4dab-9f54-37652f9d2839/scratchpad/` (`d11.py`, `stub.py`, `race.py`). Each stubs `structured()` and sends caches, outputs and `refusal.md` to scratch.

Frozen state read: `git show ef2fa6b:programs/settled-science/experiments/ss-b10.md`. The current file differs only by the seed line (`git diff ef2fa6b -- …/ss-b10.md`). The code (`bettor/brainbench.py`, `scoring/score_bb.py`, `common.py`) was last changed at 7cb74dd, before the pre-registration. `shasum -a 256 items/brainbench/*.jsonl` matches `SHA256SUMS` (`0a9acfeb…`, `d57fd577…`).

**D1. A stranger can apply the rule: flaw (F1).** `verdict()` returns exactly one label on each synthetic world (`python3 scoring/score_bb.py --synthetic <w>`): coin → fail; strong → pass, unreplicated; edge → mixed; weak → fail; split → mixed; allfifty → fail; inverted → fail. A hand-built untestable table (Sonnet stopped after 100 flattery ratings) → untestable. Accuracy with ties is implemented as written (`hit()`: 1 if p_orig > 0.5, 0.5 if p_orig = 0.5, else 0). A 50 maps to exactly 0.5 in both option orders (1 − 0.5 is exact). The bootstrap is `default_rng(20261104)`, 10,000 resamples, bounds at index 250 and 9749, i.e. int(0.025n) and int(0.975n) − 1. "Clears" is `lo > 0.634 + 1e-12` (P13). At n = 200, accuracies move in steps of 0.0025, so 0.634 itself cannot occur.

The flaw is in §5.4/§5.6 and `verdict()`. "Untestable if either model is untestable" overrides a result that is already settled. Test: Haiku testable at 0.55 [0.465, 0.605], so it does not clear, and Sonnet stopped at 100 ratings. Output: "untestable", and the bet is not scored. No Sonnet result could have made that a pass, so the outcome is known to be 0. The run order makes this plausible: Haiku finishes (steps 1–2) before Sonnet starts. A refusal or error in step 3 would then turn a settled miss into an unscored bet. Separately, when 150–199 ratings are scored, the sentences still say "On BrainBench's 200 … pairs" (Haiku n = 160 → pass sentence unchanged). That part is fixed under F2.

**D2. Every manipulation takes effect: holds.** Knobs checked with `bb.plan()` on the real seed file:
- **Option order.** The original is Option 1 on 98 of 200 items. The `original_is_option` label matches the prompt text on all 800 primary jobs. A different seed changes 101 of the 200 orders.
- **Order check.** 100 items. Every one has its label flipped and its text reversed (0 mismatches).
- **Prompt.** The flattery jobs have no Question or Methods line; the bettor jobs have one of each.
- **Matching across conditions.** Haiku and Sonnet get identical user text, and flattery and bettor get the same order per item.
- **Cache keys.** 1,000 unique keys for 1,000 jobs.
- **Seed.** `python3 ledger/seed.py <randomness> ss-b10 --purpose order|order-check` gives 11639161481964073238 and 17576409040787437905, matching `bettor/bb-seed.json` and the ledger. Pulse 06:34:00 is after the pre-registration commit (06:33:09).
- **Prompt text.** The FLATTERY text differs from ss-b6's `valence.py` SYSTEM in exactly the three places §2 lists.

The dry run (`…/.venv/bin/python programs/settled-science/bettor/brainbench.py --dry-run`) printed 200/200/200/200/100/100 calls, an estimate of $2.09, a bet cap of $2.50, a program cap of $7.50 and $4.761 spent.

**D3. Every control can fail: holds.** Wrong set-ups run through `score()` with the real option labels:
- a pure Option-1-bias rater (always 70) → 0.49 on both models, fail, and the order check shows an Option-1 pull of +20.0;
- an always-50 rater → fail;
- an inverted rater → fail;
- a coin → fail.

If the order knob were broken (original always first), the Option-1-bias rater would score 1.0. That is why D2's 98/200 check matters, and it holds.

**D4. Rivals are matched: holds.** No fitted rival families compete. The named rival, memory of BrainBench or of the papers, cannot be separated by this design, and §6 says so. Neither prompt wins by construction. The bettor is told one version was altered. The flattery rater is told to treat both as hypothetical.

**D5. A dumb baseline is beaten: holds.** The dumbest raters (constant 50, fixed Option-1 lean) fail (D3). I ran the five pre-registered text-only rules on the frozen items (`score_bb.dumb_block`; deterministic, no model, rules frozen at 7cb74dd):

| rule | accuracy | 95% CI | ties |
|---|---|---|---|
| longer abstract | 0.4975 | [0.4375, 0.5575] | 51 |
| shorter abstract | 0.5025 | [0.4425, 0.5625] | 51 |
| more up- than down-words | 0.505 | [0.46, 0.5475] | 120 |
| fewer negation words | 0.4825 | [0.46, 0.505] | 177 |
| more "significant" | 0.5025 | [0.5, 0.5075] | 199 |

None clears 0.634, so the S4 qualifier will not fire. The lesson's P3 correction holds. Note that these rules are weak: a pass beats them easily, and they say nothing about non-valence model judgements (plausibility, recognition). F2 deals with that. This is not a "no difference" rule, so no equivalence margin is needed.

**D6. Foreseeable execution risks: holds; no pilot.** The pre-mortem is of kind `world`. The items are *Journal of Neuroscience* abstracts. Some mention drug-seeking or disease models, but none is the kind of content likely to be refused, and the program's two refusals were the claim extractor on SimpleQA. The call path has been exercised:
- Sonnet 5.5 through `common.structured` with `between_tools` and no tools: 456 cached calls in this program (`items/leakage-cache.json`, `items/r2/leakage-cache.json`), with no thinking block;
- Haiku 5.5 with `output_config` JSON schema: program 1 (`mm_common.py` and others).

`max_tokens` 1000 against a rationale of at most 100 words is ample. Truncation stops the run (`_check_stop`). With no execution risk named, I made no pilot. Note for any later pilot: the 100 GPT-4 items share their *originals* with 100 test items (SOURCE.md). Calls are stateless, so this is harmless, but "excluded from the test" holds only for the pairs.

**D7. Comparisons match: flaw (F3).**

The primary comparison (flattery accuracy vs the experts' published 63.4%) is with a fixed published constant. §2 names it as such, and the comparison with 81.4% is flagged as a different measurement. Acceptable.

The secondary S1/S2 comparison is the bettor prompt against the flattery prompt on the same model, items and option order. The two calls differ in:
1. the system text: the frame (forecasting a published study vs "better news"), the instruction "treat both as hypothetical: do not try to judge which one was actually published" (flattery only), and the scale anchors;
2. the Question line (bettor only);
3. the Methods line (bettor only). It tells the model that one version was "altered by an expert so that it still reads coherently".

They match in model, items, order, schema, `max_tokens`, thinking setting and field line. More than the named factor differs, and the §5.5 sentence reads as a single-factor attribution: "Asked directly … d points more than its flattery rule; the flattery rule matched s% of its above-chance accuracy". So does §1: "how much of their own skill the flattery rule matches". It must be worded about the bundle. The ss-b6 audit cut the same kind of sentence (its required cut 3).

**D8. The verdict sentences are written: flaw (F2).** §5 has sentences for pass, mixed, fail and untestable, and `score_bb.sentences()` reproduces them verbatim. But:
- **Pass.** "A one-line valence shortcut solves much of BrainBench on these two models" fails three ways. It names a mechanism (valence) that §6 says the design cannot separate from memory or plausibility. "Much of" is not supported: a pass needs only about 0.70 observed. And the prompt is a paragraph, not one line. The ss-b6 audit cut "most of round 2's result is explained by … flatters the paper" for the same reason.
- **Fail.** "so this valence shortcut does not account for BrainBench's 'LLMs beat experts' result on these models" draws a causal conclusion from a "not shown" result. It also refers to a result that was not measured on these models: Luo et al. tested other LLMs, scored by perplexity.
- **Mixed.** "but not on <other>" asserts a negative where the design shows only "not shown".
- **n.** The sentences say "200" even when 150–199 ratings are scored.

**D9. One item cannot decide it: holds.** Leave-one-item-out and leave-one-section-out (five sections, n 24–75) are pre-registered (§4) and implemented (`model_block`: `loo_flips`, `section_flips`). Each flip produces a written "fragile" sentence. §4 states that the verdict does not change.

**D10. Machinery: holds, with notes.**
- **Bet cap and program cap.** Stubbed runs (`stub.py`; fake cost per call, no API call; output below):
  - $0.0017/call: all 1,000 calls run, $1.70.
  - $0.004/call: the cap binds at $7.2605 (= $4.7605 + $2.50). Steps 1–3 complete; step 4 stops after 13 calls; steps 5–6 do not run; 613 rows are written by the `finally`.
  - $0.02/call: the run stops in step 1 at 126 calls, $2.52 (overshoot = in-flight calls, inside the 0.05 margin).

  The order-of-steps cut works as §3 says. Steps 1 and 3 are protected unless costs run about 4× the estimate, because step 2 costs only about $0.03. The pilot cache counts against `BET_CAP` (`cap_for`).
- **Stop-on-refusal.** A fake refusal on call 37 stops the run, writes `results/refusal.md` with the request ID, writes 40 rows, and starts nothing new. `race.py`, over 5 runs with random latency, recorded 0 calls started after the refusal returned; at most 5 calls already in flight complete. Rule 3 holds.
- **Errors.** Any error or `max_tokens` stops the run (§7).
- **Other checks.** One scale direction in both prompts (99 = Option 1); content-hash cache (`key_of(tag, model, system, user)`); beacon rule (D2). Lesson: `python3 ledger/check_prereg.py ss-b10 . programs/settled-science/experiments/ss-b10.md` → L1, L2, L3 and H1 ok (R1 failed only because this file did not exist yet).
- **Note for the ledger session (not a design flaw).** `ls-ss-b10.read.read_at` says 9a75cc2, where `brier.md` reads 24 bets and 0.223. The numbers recorded (26, 0.217, 8/26) match `brier.md` at ef2fa6b. The newest audit at ef2fa6b was `ledger/audits/ta-b1r2.md` (added 06:31:14), not `sv-b3.md`.

**D11. The bet can both pass and fail: holds.** `d11.py` draws per-item accuracies at n = 200, takes the percentile bootstrap lower bound (2,000 resamples), and runs 1,000 simulations per cell. P(lower bound > 0.634) per model:

| true accuracy | 0.60 | 0.65 | 0.68 | 0.70 | 0.72 | 0.75 | 0.80 |
|---|---|---|---|---|---|---|---|
| no ties | 0.001 | 0.083 | 0.308 | 0.537 | 0.759 | 0.966 | 1.000 |
| 10% ties | 0.002 | 0.079 | 0.330 | 0.569 | 0.807 | 0.975 | 1.000 |

P(pass), for the conjunction across both models:

| world (Haiku, Sonnet) | P(pass) |
|---|---|
| 0.70, 0.70 | 0.29 if the models are independent, up to 0.54 if fully correlated (same items) |
| 0.60, 0.60 | about 0.000, so P(fail) is about 1 |
| 0.65, 0.75 (the pre-mortem's world) | 0.08 |
| 0.70, 0.80 | 0.54 |
| 0.80, 0.80 | 1.00 |

Both P(pass) in the world where it holds and P(fail) in the world where it doesn't are well above 10%. The rule effectively needs an observed accuracy of about 0.70 or more on each model (lower bound ≈ accuracy − 0.064). The engine's 0.30 sits inside this range.

**R12. Three models by default (CONTEXT rule 12): flaw (F4).** The §0 reason for leaving Opus out has three parts:
1. "the novelty page's named replication on these two models": the novelty page chose them for cost ("about $0.20 on Haiku, $1.50 on Sonnet"), not because the question is about these models;
2. Opus "would cost about $2.90 … more than the whole ruling": cost;
3. "Opus's flattery rater already has its own result on round 2 (ss-b6)": that was on different items (our one-word sentence pairs) with a different prompt wording, so it says nothing about BrainBench.

None is one of rule 12's reasons, and rule 12 says that "cost alone is not a reason: … use fewer repeats or items on it and say so". Leaving Opus out also means ss-b6 (Opus, our items) and ss-b10 (Haiku and Sonnet, BrainBench) differ in both model and items. A failure could then not be put down to either.

## Required fixes

Each goes in one dated DEVIATIONS row (D-next, naming this review), written before any call. None lowers the bar or changes the pass rule.

**F1 (D1) → untestable cannot hide a settled non-pass.** In §5.4, after the untestable sentence, add: *"If one model is untestable and the other was tested and does not clear, the bet cannot pass: the verdict is **fail (one model untestable)**, scored 0, with the sentence: 'On BrainBench's expert-written abstract pairs, a model asked only which version is better news for the paper's own idea was not shown to beat the neuroscientists' published 63.4% on <tested> (a% [lo, hi]); <other> could not be tested (n of 200 flattery ratings scored), so the bet cannot pass and is scored as a miss.'"* In §5.6, add that this verdict scores 0. In `score_bb.verdict()`, before the untestable return: if any tested block has `clears_experts == False` and at least one block is untestable, return `"fail-partial"`, and add the matching branch in `sentences()`. Show it on the hand-built table from D1 (Haiku 0.55, Sonnet stopped at 100 ratings) → fail-partial.

**F2 (D8) → verdict sentences use only nouns the design carries.** In §5 and `score_bb.sentences()`:
- **Pass.** Replace "A one-line valence shortcut solves much of BrainBench on these two models; this does not show that the LLMs in the original study used it." with "This design cannot tell whether the models answered by valence, by plausibility or from memory of the papers, and it does not show that the LLMs in the original study used such a rule."
- **Mixed.** Replace "but not on <other> (b% [lo, hi]), so the shortcut beats the experts on one of the two models only." with "but was not shown to on <other> (b% [lo, hi]), so this prompt beats the experts' published rate on one of the two models only."
- **Fail.** Replace ", so this valence shortcut does not account for BrainBench's 'LLMs beat experts' result on these models." with ". This says nothing about how the LLMs in the original study, other models scored by perplexity, reached 81.4%."
- **n below 200.** In every main sentence, when either model has fewer than 200 scored flattery ratings, replace "BrainBench's 200 expert-written abstract pairs" with "BrainBench's expert-written abstract pairs (Haiku n = <n>, Sonnet n = <n> of 200 scored)".
- §1's "A model could therefore look good at 'predicting results' just by picking the version that flatters the paper" may stay. It is a hypothesis, not a verdict.

**F3 (D7) → the bettor comparison is worded about the two prompts as bundles.** In §5.5's first bullet and `sentences()`, replace "Asked directly which abstract the study published, <model> was right x% [lo, hi] of the time, d points more|less than its flattery rule (difference [lo, hi]); the flattery rule matched s% [lo, hi] of its above-chance accuracy." with "With the program's forecasting prompt instead (a different system text, plus a question line and a methods line saying one version was altered by an expert), <model> picked the published abstract x% [lo, hi] of the time, d points more|less than with the flattery prompt (difference [lo, hi]); the flattery prompt's above-chance accuracy was s% [lo, hi] of the forecasting prompt's." Keep the no-share branch with "forecasting prompt" for "it". Add a §6 bullet listing D7's three differences and the matched items. In §1, replace "to see how much of their own skill the flattery rule matches" with "to compare the two prompts on the same items".

**F4 (R12) → Opus runs, on fewer items, as a reported secondary.** Add step 7, run last after step 6 so that it cannot cut steps 1–6:
- **What.** `claude-opus-5-5`, FLATTERY prompt, primary option order, on the 100 `order-check` items (the beacon-drawn set already fixed; at least 50 of them if the budget ruling is smaller: the first 50 of `random.Random(seeds["order-check"]).sample(ids, 100)` in sample order).
- **Settings.** `common.structured` (adaptive thinking at effort low, D18; record it), `max_tokens` 4000 as in ss-b6, because hidden thinking counts against it.
- **Reporting.** Secondary S9: accuracy with CI, and whether its lower bound clears 0.634, labelled as run with thinking on. Never in the pass rule, and the odds event is unchanged. Add a §5.5 sentence: "On the 100 beacon-drawn items, Opus (thinking on, at its lowest setting) with the flattery prompt picked the published abstract x% [lo, hi] of the time." It is reported whatever the verdict.
- **Cost and caps.** About $0.75 at the pre-registration's own $2.90 per 400 Opus calls. Raise `BET_CAP` from $2.50 to $3.75 and the program cap from $7.50 to $8.75 by a new budget ruling in `ledger/spend.jsonl` (the engine's call under rule 4), or to fit 50 items, $3.10 and $8.10.
- **Models row.** Rewrite §0 "models" as one sentence: Haiku and Sonnet on all 200 items carry the pass rule, and Opus runs on 100 items only, as a secondary, because it cannot turn thinking off and costs far more per call.
- **Order of work.** Re-run `--dry-run` and show the 7-step plan and estimate before the confirmation.

Recommended, not required: a stronger answer-free baseline than the five above, which are all at chance, for example "the version whose changed words recur more often in the unchanged sentences". It is not needed for this bet's claim once F2 removes the mechanism wording.

## Addendum 1: check of the D54 fixes (2026-11-05 06:59 America/Denver)

I checked 386d462 (code and the D54 row), 05e13e6 (the row's time) and 5ee223a (ledger) against F1–F4. No paid call, no pilot ($0.00). **Not confirmed yet: one phrase from F2 is still in the code. Everything else holds.**

- **F1: holds.** I ran `score_bb.score()` on hand-built tables with the real option labels.

  | Haiku | Sonnet | verdict |
  |---|---|---|
  | 0.55 | stopped at 100 ratings | `fail-partial`, reported "fail (one model untestable)" |
  | stopped at 100 ratings | 0.55 | `fail-partial` |
  | 0.80 | stopped at 100 ratings | untestable |

  The D54 row scores fail-partial as 0. The sentence names the per-model n and the untested model.
- **F2: one phrase not applied.** The pass, fail and n-below-200 wording are as required. The n=160 case prints "(Haiku: 160 of 200 scored; Sonnet: 200 of 200 scored)". "But was not shown to on <other>" is in. But the mixed sentence still ends "**so the shortcut beats the experts on one of the two models only**" (`scoring/score_bb.py` line 249, and the D54 row's text). F2 required "so this prompt beats the experts' published rate on one of the two models only". "The shortcut" claims what the design cannot show: that the prompt succeeds by a route other than knowledge. That is the noun F2 removed from the pass sentence.
- **F3: holds.** The forecasting-prompt sentence names the bundle: "a different instruction, a question line, and a note that one version was altered by an expert". The share is worded as the flattery prompt's above-chance accuracy over the forecasting prompt's, and the §6 line is in D54.
- **F4: holds, and the $2.50 cap is acceptable.**
  - **The step.** The dry run shows step 7: `claude-opus-5-5`, 50 calls, kind `opus-secondary`, all of them in the beacon-drawn order-check half (bb-005 to bb-100). All five sections appear (16, 11, 9, 9, 5). The user text is identical to the Haiku primary text (same option order). There are 1,050 unique cache keys, and `max_tokens` is 4000 for Opus only. `model_block` filters by model, so Opus rows cannot enter the pass rule.
  - **The cap.** A stubbed run at $0.0017/call completes all 7 steps for $1.785. At $0.00235/call the cap binds at $7.2605, after steps 1–6 complete, and step 7 stops at 48 of 50. S9 is then reported on n = 48.

  A binding cap therefore cuts only the secondary, and rule 12 accepts fewer Opus items. Steps 1–6 measure about $1.70, so step 7's about $0.40 fits under the cap's $2.45 stop. Even at the conservative $2.09, Opus would still get about 35 items. Recommended, not required: if step 7 is cut, have the S9 sentence say "n of the 50 items (cut by the cap)".

  The program cap now reads $8.25 (br-005 for ss-b12, 8140cf6). The bet's own cap still binds first: min($8.25, others + $2.50 − pilot).
- **Ledger note: fixed.** `ls-ss-b10.read` now says read_at ef2fa6b, newest audit ta-b1r2.md. `check_prereg.py` gives L1–L3 ok and R1 ok. R2 is "fix-first, confirmed null", as expected until confirmation.
- **Regression:** all seven synthetic worlds give the same verdicts as before.

**Remaining fix (F2a), before any call:** in `scoring/score_bb.py` `sentences()`, mixed branch, replace "so the shortcut beats the experts on one of the two models only." with "so this prompt beats the experts' published rate on one of the two models only." Do the same in the D54 sentence text, through a dated DEVIATIONS row or an amendment to D54 written before any call. Once that commit exists, I confirm with no further change needed.

## Addendum 2: confirmation (2026-11-05 07:03 America/Denver)

**Confirmed: the run may start.** F2a is applied at 418d79b (DEVIATIONS D56, which amends D54's text). No paid call, no pilot ($0.00), and still no run data (`bettor/bb-cache.json`, `bb-pilot-cache.json` and `bb-ratings.jsonl` do not exist).

- **F2a holds.** On a hand-built mixed table (Haiku 0.80, Sonnet 0.60), the sentence now ends "…so this prompt beats the experts' published rate on one of the two models only." `grep shortcut scoring/score_bb.py` finds nothing.
- **The recommended S9 wording is in.**
  - On the earlier stubbed outputs, 50 Opus rows print "on 50 of the 50 items" and 48 rows print "on 48 of the 50 items (cut by the cap)".
  - One small point: the clause appears whenever fewer than 50 Opus items ran. An error stop in step 7 would therefore also print "cut by the cap". The results file should give the actual stop reason. That is a wording note, not a flaw.
- **No regressions.** The seven synthetic worlds give the same verdicts as before (coin fail, strong pass, edge mixed, weak fail, split mixed, allfifty fail, inverted fail). The dry run is unchanged: 7 steps, estimate $2.60, bet cap $2.50, program cap $8.25, $4.761 spent.

F1, F2, F3 and F4 are all confirmed. The verdict stays fix-first, confirmed at the time above.
