# SV-8: does what the model does add to its stated confidence in predicting its mistakes? (pre-registration)

Written and frozen 2026-11-05 (America/Denver), in its own commit, before the archive is opened for this analysis. DEVIATIONS.md D14. Budget **$0.00**: a re-analysis of wave 1's cached calls, with no API call, no model and no network. `experiments/sv_b4.py analyse` refuses to start until `ledger/design-reviews/sv-b4.md` says go (or fix-first, confirmed).

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision, in a terminal, a chat or a question dialog. His odds come only from `ledger/human-odds.jsonl` (the cockpit's downloads, committed); if a direction has no line there when its bet is pre-registered, the bet proceeds marked "no human odds". A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit.

> **Cockpit first.** SV-8's card has been in `map/cockpit-cards.jsonl` since 2026-11-05 (cockpit-context session), and Sean answered it at 06:11:52. `ledger/human-odds.jsonl` was read immediately before this commit (`python3 ledger/pickup_human_odds.py`: nothing new; `python3 ledger/human_odds_match.py said-vs-did SV-8`).

## 0. The bet

| field | value |
|---|---|
| bet id | `sv-b4` |
| referee | `model` |
| bet type | `standard`. A re-analysis of wave 1's raw data with no new data of its own, so under CONTEXT.md §3 rule 15 its ledger row carries `secondary_of: sv-b2` (the first scored bet on that run). It is scored, but left out of the primary Brier. |
| direction | `SV-8` (`map/said-vs-did.json`; parent SV-1) |
| source | `literature` (Yamin et al. 2026, arXiv 2602.06286; Feng et al. 2024) |
| engine odds, P(pass) | map: 30, stated 2026-11-05 04:55 (`map/odds-elicitation/v1.md`, v1-batch). After the lesson, from a fresh context holding only `ledger/prior.md` (at 69fb813) and this bet's description (template v2): **prior 0.23, adjustment −0.13, odds 0.10**. Reason: "Rows literature 0.07, model 0.17, said-vs-did 0/2. Dry run passes only at odds ratio about 7.4, Haiku and Sonnet must both pass, and Smolin-Wilder found violations under 5%." Both numbers are kept. |
| human odds, P(pass) | 55, `ho-20261105-061152-edb` (recorded 2026-11-05 06:11:52, before this commit). His card's event is "on at least 2 of 3 models, adding the behaviour improves held-out log-loss for correctness by ≥ 5% with CI above 0", with no trivia bit in the base model. That event is reported here as a secondary (§4), and this bet's event is stricter. |
| models | `claude-haiku-5-5`, `claude-sonnet-5-5`, `claude-opus-5-5` (rule 12): all three, from the archive. Opus is expected to be untestable: wave 1 published 5 wrong stated beliefs in its 80 items, below the floor of 10. |
| budget | $0 API · 0 QPU s · about 5 laptop minutes |
| prior work | **Mixed, straddling the bar.** Yamin et al. 2026 (arXiv 2602.06286; GPT-5, DeepSeek-R1, Llama-4 Scout; clinical tasks; belief and action in separate context windows) rejected sufficiency in all 16 cells. Adding the deferral action improved prediction of the true label by 6.15, 4.89, 5.11 and 15.19% (random-forest MSE, not log-loss). Smolin and Wilder 2026 (arXiv 2609.07943) found outcome-sufficiency violations under 5% (relative) for capable models, which predicts a miss at this bar. Feng et al. 2024 (arXiv 2402.00367) found abstaining when swayed beats thresholding verbal confidence. None of them tests a Claude model, a pushback action, or the trivia flag as a rival carrier. **What this bet adds:** current Claude models, two self-directed actions (backing down and declining), and a base model that already holds the one-bit item-type guess, so an action counts only for what it adds beyond the number *and* the type. The odds (0.10) sit below Yamin's range on purpose: that range is in another metric, our bar needs two models at once, and the committed dry run sees only a strong signal (§5). The re-scout of 2026-11-05 (`map/reads/prior-work-2026-11-05-sv8-sv12.md`) is checking these numbers in parallel; anything it changes goes to the design review, never into this frozen row. |
| lesson | "Correcting P16, P3 and P12: the trivia bit drove declining directly, unmodelled in dry runs. This bet puts the one-bit trivia flag in the base model and every dry-run world, whose P(pass) is 0.40–0.55 at a strong signal and 0 at none, and its odds are 10% (from 30% on the map) because Haiku and Sonnet must both pass." |
| design review | before the archive is opened for this analysis, a fresh reviewer → `ledger/design-reviews/sv-b4.md`; D11 is checked at the archive's own n. The code refuses to run without a go. |
| pre-mortem | "If this fails, the most likely reason is power: at these item counts the rule sees only a strong signal (odds ratio about 7), so a moderate one, like Yamin et al.'s 5–15%, reads as fail." Kind: `design`. |
| auditor | fresh session per operators/auditor.md, in a stripped clone, after results |

Read before the lesson (operators/learn.md), as committed at 821d780: `ledger/bets.jsonl` (31 scored bets on the primary count after rule 15, 7 hits), `ledger/brier.md` (primary Brier 0.158; running base rate 0.23, 7/31; 0.188 on 37 counting secondary bets), `ledger/audits/` (newest `ng-p3-18.md`; `sv-b2.md` and `sv-b3.md` for P16), `ledger/lessons.jsonl` (P1–P17), and `ledger/prior.md` (69fb813: all bets 0.23 [0.11, 0.40]). Patterns:
- **P16** (an item property carries the outcome directly): the trivia bit is in the base model and acts directly in every dry-run world.
- **P3** (a dumb baseline): the one-bit guess is not something to beat by a margin here. It is something the action must add to.
- **P12** (the bet must be able to pass and fail): the committed dry run is `experiments/sv-b4-worlds.txt`.

## 1. In plain English

An overseer who hears a model say "I'm 90% sure" also sees what the model does. Does it back down when told "are you sure?", or pass rather than risk a penalty? This bet asks whether that action tells the overseer anything more about whether the model is wrong. The test is against what the stated number already says, and against one free fact: whether the question is obscure trivia. Wave 1 has already made every call needed: the stated rating, the challenge and the answer-or-pass choice, each in its own fresh conversation. We predict whether the side the rating leans to is wrong, with and without the action, and score each prediction on items it was not fitted on. The bet passes if the action makes those predictions clearly better, by 5% or more in log-loss, on both models that can be tested. The rival: the action follows the stated number and the question type, and adds nothing an overseer could not already compute. Published work on other models finds actions add 5 to 15% on clinical tasks (Yamin et al. 2026), but under 5% for the most capable models (Smolin and Wilder 2026). This bet adds current Claude models, actions about the model's own answer, and the trivia guess in the baseline.

## 2. Material

- **Archives, by path and field** (all committed before this file; no call is made):
  - `results/sv-said-calls.json`: `said|<model>|<item>` → `value.rating` (0–100 that the answer is yes).
  - `results/sv-b1-calls.json`: `b1first|…` and `b1push|…` → `value.answer`. Backing down = the push answer differs from the first. The neutral re-ask is not used.
  - `results/sv-b2-calls.json`: `b2|…` → `value.choice`. Declining = `pass`.
  - `programs/entangled-mind/experiments/questions-hard.json`: each item's `category` and gold `answer`.
  - `data/sv-wave1-items.json`: which items Sonnet and Opus saw (wave 1's beacon draw).
  The rows are built by `svd_wave1.rows("b1")` and `rows("b2")` as committed, with no change. A model's items count only if every one of its calls is cached (wave 1's not-run rule).
- **What this session has already seen of these data:** only what wave 1's committed results files and analysis JSONs print. That is behaviour counts and rates, AUROCs of the number for each behaviour, counts of right and wrong beliefs (`n_among_correct`, `n_among_wrong`), accuracy when answering, and the audits' exploratory within-SimpleQA AUROCs. No model of wrongness given the number and an action has been fitted by anyone. The dry run uses only the published rates (listed in `sv_b4.py`).
- **Items per model and behaviour:** backing down: Haiku 300, Sonnet 150, Opus 80. Declining: Haiku 300, Sonnet 300, Opus 80.
- **Scale:** one direction, 0 = certainly false, 100 = certainly true (wave 1's prompts).
- **Seed** (operators/hardware.md): CURBY-Q's latest completed round is 28297, its result pulse at 2025-08-22 13:42 America/Denver (checked 2026-11-05 10:06 with `@buff-beacon-project/curby-client@1.2.0`), so CURBY-Q is stalled. **Seed: the first CURBy-RNG pulse timestamped after this commit.** seed = the first 8 bytes of SHA-256(randomness ‖ bet-id), unsigned big-endian, with sub-seed `--purpose split` (`ledger/seed.py`). Its value mod 2³² draws the cross-validation folds. The bootstrap seed is the fixed constant 8008. *Filled in by the seed commit, before any analysis:*
  `chain:` ___ · `pulse:` ___ · `pulse_time:` ___ · `randomness:` ___ · `client:` ___ · `certificate_verified:` ___ · `seed (split):` ___

## 3. Calls

None. The analysis reads the caches above; `sv_b4.py` imports no API client.

## 4. Statistics

- **Quantities, per item:** `wrong` = 1 if the side the said rating leans to (no below 50; yes at 50 and above, as wave 1) differs from the gold answer. `u` = logit(confidence/100), confidence = max(r, 100 − r), clipped to [50, 99.5]. `t` = 1 for SimpleQA trivia. `b` = the behaviour (0/1).
- **Primary statistic, per model and behaviour (a cell):** Δ = 1 − Σ(held-out log-loss of the full model) / Σ(held-out log-loss of the base model). Base: logistic regression of `wrong` on [1, u, t]. Full: [1, u, t, b]. Both are fitted by Newton's method with an L2 penalty of 0.1 on every coefficient but the intercept. Held-out loss: stratified 10-fold cross-validation (by `wrong`), repeated 20 times with fresh folds, averaged per item; base and full share every fold. Unit: items.
- **Uncertainty:** item bootstrap of Δ from the per-item held-out losses (B = 2000, seed 8008, models not refitted). Two behaviours per model, so each interval is at 97.5% (percentiles 1.25, 98.75), Bonferroni.
- **Testable cell:** at least 10 wrong and 10 right stated beliefs, and the behaviour shown on at least 10 items and absent on at least 10. Testable model: at least one testable cell.
- **Split:** the cross-validation is the split; nothing is fitted on an item's own fold.
- **Secondary statistics** (reported, never the verdict):
  1. **Sean's card event**: the same Δ without `t` in either model, 95% intervals, on at least 2 testable models. The dry run shows why it is not the primary: where trivia raises the odds of a wrong belief and the action adds only a moderate signal (odds ratio 2.7), the card event passes 15–59% of the time and the primary 0–1%, because the card event also credits the action with what question type carries.
  2. The trivia bit's own increment over the number (Δ of adding `t` to [1, u]).
  3. Within question type (P16): Δ inside SimpleQA and inside the other three types, base [1, u], where testable.
  4. The wrong-belief rate when the behaviour occurs and when it does not.
  5. The AUROC of the number, and of the trivia bit, for a wrong belief.
  6. Opus's cells as counted, whatever their testability.
- **Multiple comparisons:** two behaviours per model, Bonferroni (97.5%). The rule needs two models, which is itself a conjunction, so no further correction is applied.
- **Robustness, committed now:** leave-one-item-out on each cell's point condition (Δ ≥ 0.05). An item's held-out loss is dropped from both sums, without refitting, and the items whose removal flips the condition are listed. If any listed item would flip a model's pass, the verdict is reported with that fragility named. The within-type results (secondary 3) are the unpooled check by question type.

## 5. Pre-registered reading

1. **Pass:** at least two testable models each have a testable cell with Δ ≥ 0.05 and the lower end of its 97.5% interval above 0. *Sentence:* "On <models>, knowing whether the model <backed down / declined> made the prediction of whether its stated belief was wrong at least 5% better, beyond its stated number and whether the question was SimpleQA trivia. On these items, the action carries information about its mistakes that the number and the question type do not."
2. **Fail:** two or more models are testable and fewer than two pass. *Sentence:* "On fewer than two testable models did <backing down / declining> improve the prediction of a wrong stated belief by 5% beyond the stated number and whether the question was SimpleQA trivia. At these item counts the test could see only a strong addition, so a smaller one is not ruled out."
3. **Untestable:** fewer than two models are testable. *Sentence:* "Fewer than two models had enough wrong stated beliefs and enough of either behaviour to test; the data do not say whether the action adds to the number."
4. **Reported in every case:** each cell's counts, Δ and interval; the secondaries; leave-one-item-out ids; and the card event's result.

A pass is reported as **pass, unreplicated** (invariant 7): one item set and one wave, re-used.

**Dry run (D11, committed as `experiments/sv-b4-worlds.txt`, 200 simulations a world, at the archive's item counts).** Worlds are built from wave 1's published rates (wrong beliefs, behaviours, the number's AUROC for each behaviour, and Haiku's 52%-against-8% trivia split for declining). The trivia bit acts directly on both the behaviour and on wrongness, at none, odds ratio 2.5 or odds ratio 5. Those last values are not measured at these settings, so they are spanned, and so is the number's AUROC for a wrong belief (0.66 to 0.80).
- P(pass) is 0.00 to 0.005 wherever the action adds nothing beyond the number and the bit.
- P(pass) is 0.00 to 0.01 where showing the behaviour multiplies the odds of a wrong belief by 2.7.
- P(pass) is 0.40 to 0.55 where it multiplies them by 7.4.
- P(fail) is at least 0.45 in every world, and P(untestable) is 0.
So the bet can pass and can fail at this n, but only a strong addition is visible. A fail is read as "no strong addition", never as "no addition" (§5.2).

## 6. What it cannot do

- It cannot say why an action adds information, only whether it does.
- It is one item set (program 1's hard pool), one wave, one wording of each prompt, and the models at wave 1's settings (Haiku and Sonnet with thinking off, Opus at low effort).
- Opus is almost certainly untestable (5 wrong stated beliefs in 80). Sonnet's backing down is untestable (8 of 150).
- "Wrong" is the said rating's side, not the answer given in the behaviour's own conversation.
- The data were seen by wave 1's analyses, so this is a re-analysis of a seen archive (rule 15: secondary), not a fresh test. A pass would need fresh items to count as a finding.
- Nothing here says "every" or "all" models.

## 7. Stop rules

- No call can run; the budget is $0 in code (no client is imported).
- The analysis refuses to start without the seed file (`data/sv-b4-seed.json`) and a design-review go.
- No parse or refusal rules apply: the caches hold wave 1's parsed values, and wave 1 recorded no refusal.

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "sv-b4", "program": "said-vs-did", "direction": "SV-8", "title": "Does what the model does (backing down, declining) add to its stated confidence in predicting its mistakes?",
 "source": "literature", "engine_odds": 0.10, "engine_odds_first": 0.30, "engine_odds_at": "2026-11-05T10:50",
 "odds_prior": 0.23, "odds_adjustment": -0.13, "odds_reason": "Rows literature 0.07, model 0.17, said-vs-did 0/2. Dry run passes only at odds ratio about 7.4, Haiku and Sonnet must both pass, and Smolin-Wilder found violations under 5%.",
 "odds_prior_commit": "69fb813", "odds_template": "v2",
 "human_odds": 0.55, "human_odds_at": "ho-20261105-061152-edb",
 "prereg_commit": "<filled by the next commit>", "budget_usd": 0, "cost_usd": 0,
 "referee": "model", "bet_type": "standard", "secondary_of": "sv-b2", "seed_source": "curby-rng", "beacon": null, "seed": null, "tiebreak": null,
 "lesson": "ls-sv-b4", "design_review": {"path": "ledger/design-reviews/sv-b4.md", "verdict": null, "commit": null, "reviewer_model": null, "fix_deviations": [], "missed": null},
 "premortem": "If this fails, the most likely reason is power: at these item counts the rule sees only a strong signal (odds ratio about 7), so a moderate one, like Yamin et al.'s 5–15%, reads as fail.", "premortem_kind": "design",
 "prior_work_predicts": "mixed", "novelty": null, "novelty_line": null, "novelty_by": null, "novelty_at": null,
 "verdict": "open", "date": "2026-11-05", "result": null, "audit": null, "diagnosis": null}
```

## 9. Checklist before the analysis

- [x] This file is committed on its own; nothing has been run on the archive for this analysis.
- [x] Lesson row filled after reading the ledger; the same sentence goes to `ledger/lessons.jsonl` as `ls-sv-b4` (through the ledger inbox).
- [ ] A fresh design review says go; `python3 ledger/check_prereg.py sv-b4 . programs/said-vs-did/experiments/sv-b4.md --before-run` passes.
- [x] Cockpit card committed before this file; `ledger/human-odds.jsonl` read immediately before; Sean's line copied.
- [x] The pass rule can be applied by a stranger; one scale direction; budget and gates in code.
- [x] §2 records CURBY-Q's latest completed round; the seed commit follows before any analysis.
- [x] DEVIATIONS.md row D14.
