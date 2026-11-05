---
bet: ss-b16
program: settled-science
prereg_commit: 2c46eb0
reviewer_session: ss-b16 design review (fresh subagent launched by the ss-wave5 engine session; has not seen the chat or the authoring work)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 16:45 America/Denver
checks: {D1: holds, D2: holds, D3: holds, D4: holds, D5: flaw, D6: holds, D7: flaw, D8: flaw, D9: flaw, D10: holds, D11: holds, D12: holds}
prior_work_search: "web search 'language model judge which of two research findings is genuine versus altered by expert, hypothesis-supporting result heuristic, positive results bias forecasting replication' (2026-11-05): no paper testing a valence or hypothesis-supporting rule for picking real over altered results; nearest hit Bao et al. 2025 (arXiv 2505.18942, abstract opened: LLMs infer peer-review norms from paper pairs, not positive-result preference, no BrainBench)"
papers_opened: 2
flaws: 4
pilot_usd: 0.00
verdict: fix-first
confirmed_at: null
---

# Design review of ss-b16

## In plain English

The run code does what the pre-registration says. It reuses ss-b10c's 162 Opus calls under identical keys, follows the same beacon item order, enforces the $5.95 cap and stops on a refusal. A stranger can apply the scorer, and it reaches every verdict. The bet can both pass and fail, and the 41 items already published (40 right) do not settle it in advance. They make C1 (beat 81.4%) close to certain, so the bet is really a bet on C2, as the pre-mortem says.

C2 is where the design is weak. "The forecasting prompt does no more than 5 points better" is decided by the point estimate. That rule accepts a true gap of exactly 5 points about 45% of the time and a true 7-point gap 12–18% of the time, so the gap it can reliably detect (about 7.5 points) is wider than its own 5-point margin (P2). The pass sentence then claims the two prompts do "about as well", says "on Opus too" (on the same 200 items, Sonnet's forecasting prompt beat its flattery prompt by 6.3 points, more than the margin), and drops the note that the two prompts differ in three ways (P8).

Four fixes are needed before any call: decide C2 on its one-sided 95% upper bound, name the bundle, correct the "too" sentence, and add a leave-one-out check on C2. None changes what is tested.

## Checks

Commands run (no paid calls):
- `cd programs/settled-science && python3 scoring/dry_b16_b17.py --rules`, which reproduced §4's table exactly: opus-41 1.000; sonnet-like P(C1) 0.933, P(C2) 0.377, P(pass) 0.376; haiku-like 0.010; valence-only v = 0.80/0.85/0.88/0.90/0.95 gives 0.150/0.731/0.960/0.993/1.000; every `score_b16` verdict reached.
- `/Users/seanpharris/entangled-mind/.venv/bin/python bettor/brainbench_opus.py --dry-run`: "800 calls, 162 from ss-b10c's cache, 638 new, about $5.81; … items with a reused call 41; first new items ['bb-044', 'bb-127']".
- Reviewer scripts, all in `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed-ss-wave5/aadb0e9f-7e6b-4ba3-a7d3-8203f13d7b12/scratchpad/review-b16/`:
  - `look.py`: archive cross-tabs.
  - `code_checks.py`: keys, order, cap, `write_out` and the scorer end to end, using the real `common.Caller` with a fake `fn` and paths redirected to scratch.
  - `worlds.py` and `ub95_full.py`: D11 worlds.
  - `power.py`: C2 power, P18 and P13 boundaries, and Haiku's and Sonnet's own C2.

**D1. Holds.** The §5 rule has one statistic per condition, a fixed bar, a conjunction and an untestable floor, and each input gives exactly one verdict:
- Synthetic rows reach pass, both mixed labels, fail and untestable (`--rules`).
- On the boundaries:
  - d = 10/200 = 0.050 gives C2 true (EPS).
  - d = 0.055 gives C2 false.
  - 180 items is testable; 179 is untestable.
  - 200 flattery items with only 179 all-four items is untestable, as §5 item 5 says.
- End to end: the real archive plus 638 synthetic new ratings, run through `write_out` and `score_b16.score`, gives verdict pass with n 200/200. The archive split is 41 (0.976) against 159 (0.899), and the sources are 162 "ss-b10c archive" and 638 "ss-b16". The generated sentences are the §5 sentences.

**D2. Holds.** The factors are prompt (flattery against forecasting) and option order:
- The plan has 800 unique keys, and each item gets four calls: flattery orig-first, flattery orig-second, bettor orig-first, bettor orig-second.
- `original_is_option` flips with the order.
- All 162 archive keys are in the plan, and 0 of them differ in id, task, option or model from the job with the same key. Recomputing `key_of(TAGS, model, system, user)` reproduces the key, so the prompts, user texts and settings are byte-identical to ss-b10c's.
- Settings: Opus is in `ADAPTIVE_LOW` (effort low), `max_tokens` 4000 and no tools field (`common.structured`). The archive's Opus output tokens are at most 233 of 4000.

**D3. Holds for C1; C2's weakness is under D5.**
- C1 rejects a position-only rater (an averaged Option-1-always rater scores 0.500; ss-b10c's text-only rules score 0.48–0.51) and a Haiku-like rater (P(pass) 0.010).
- C2 must reject a "memory" world, where forecasting knows more than valence. A world with Opus's flattery equal to Sonnet's per item, and forecasting fixing half of Sonnet's forecasting misses, is rejected 100% of the time.
- The dry run's Sonnet-like world (true gap about +0.069 on the 159) is rejected only 62% of the time. See D5.

**D4. Holds (not applicable).** No fitted rival families compete. The rival explanations (valence, plausibility, memory) are named as not separable (§6), and no sentence claims to separate them.

**D5. Flaw (F1).**
- *Dumb baseline: holds.* The dumbest predictors cannot pass C1:
  - Constant 50 gives 0.5.
  - The position rule gives 0.5.
  - The text-length, up-word and negation rules give 0.48–0.51 (ss-b10c tables).
  - A constant rater passes C2 (d = 0), but the conjunction blocks it.
  - P3's concern carries over in a weaker form. Sonnet already clears C1 on these 200 items with this prompt (0.882 [0.840, 0.922]), so C1 is close to known for Opus (P(C1) ≥ 0.86 in every plausible world below). The information is in C2.
- *C2 is a "no more than 5 points better" rule decided by a point estimate, with no power check* (P2's do_this: "an equivalence margin and a power check (MDE below the margin)"). Paired-item simulation at n = 199, at the discordance Opus-like and Sonnet-like raters show (π 0.08 and 0.12):

  | true gap (bettor − flattery) | point rule P(C2 holds) | one-sided 95% upper-bound rule |
  |---|---|---|
  | 0.00 | 0.98–0.99 | 0.64–0.78 |
  | 0.03 | 0.75–0.81 | 0.18–0.28 |
  | 0.05 (the margin) | 0.44–0.46 | 0.05 |
  | 0.07 | 0.12–0.18 | 0.01 |
  | 0.09 | 0.04 | 0.00 |

  The point rule's MDE (80% rejection) is a true gap of about 0.075, above its own 0.05 margin. It passes a true 7-point gap up to 18% of the time. The pass sentence then reads as parity ("does about as well as asking which version is real"). §6's "C2 is a point estimate" caveat discloses the weakness, but a disclosure does not give the rule power. The upper-bound rule has the right size at the margin and keeps power in the worlds where the claim is true (see D11).

**D6. Holds.** The pre-mortem is of kind `world`, not execution. Same prompts, items and settings as ss-b10c, whose 162 Opus calls and roughly 1,600 Haiku and Sonnet calls on all 200 items had 0 refusals and no truncation. No pilot is needed. The cost risk is checked under D10.

**D7. Flaw (F2).**
- *C2's comparison.* Same model, items, orders, settings and date window. The two prompts differ in three ways: the system instruction (flattery's "Treat both as hypothetical: do not try to judge which one was actually published" against the bettor's "forecasting the result of a scientific study that has already been published … Exactly one of the two is what the study reported"), a question line, and the Methods note that one version is "altered by an expert". ss-b10c's sentence named this bundle ("a different instruction, a question line, and a note that one version was altered by an expert"), and its audit checked it (P8). ss-b16's §5 and `score_b16.sentences` (`fc`) drop it. They say only "asked directly which version was published (the program's forecasting prompt)", and the pass sentence attributes the result to "asking which version is real".
- *C1's comparison* with 0.814 (other models, perplexity) is unmatched but disclosed in §6 and in the closing sentence. It is a reference bar.
- *The 41 archived items* were run about six hours earlier with 2 workers rather than 4. Neither difference changes the content of a call.

**D8. Flaw (F3).** All five verdict sentences are written and generated verbatim by `score_b16.sentences`. Two phrases go beyond what the design carries:
- "So on Opus **too**…" implies the smaller models showed the same thing. On the same 200 items, ss-b10c's own data give bettor − flattery of +0.0625 [+0.028, +0.100] for Sonnet, beyond the 5-point margin with its interval above 0, and +0.0475 [−0.018, +0.113] for Haiku (`power.py`, from `bbb-ratings.jsonl`). ss-b10c's +4.0 was on Sonnet's 126 scored items only.
- "does about as well as asking which version is real" is a parity claim that the point-estimate rule cannot carry (F1), on a bundle the sentence does not name (F2).
- §4 calls the valence-only world "the null world", but in that world the claim is true. That is not a verdict sentence, so it is a note under D11, not a flaw here.

**D9. Flaw (F4).** Leave-one-item-out and leave-one-section-out are pre-registered and computed for C1 only (`loo_flips` and `section_flips` call `c1`). C2 is the condition the pre-mortem and the odds reason call fragile. It has neither check, though one item that flips from concordant to "flattery wrong, bettor right" moves d by 0.005. At d within 0.005 of 0.05, one item decides the label.

**D10. Holds.**
- *Budget in code.* `cap()` = `min(BUDGET_USD, spent_total − own(bbo-cache) + 5.95)` = 17.517. The real `Caller` with a fake 1.25×-cost `fn` stopped at $5.904 of own spend (519 calls), giving 170 items and an untestable verdict, as §3 says. Resampling per-item costs from ss-b10c's 40 complete Opus items (per call mean $0.00904, SD $0.00108) puts P(the cap stops before the 159th new item) at 0.007 and P(untestable) at about 0. The run stays testable unless per-call cost runs about 18% above ss-b10c's.
- *Program cap.* $11.57 + $5.95 + $2.25 = $19.77 of $21.40.
- *Stop on a refusal or error* is in `common.Caller`, which writes `results/refusal.md` and sets the status file.
- *Scale.* One direction (99 = Option 1) in both prompts.
- *Cache.* Content-hash keyed; the archive is read only (the code never writes `bbb-opus-cache.json`).
- *Seed.* Carried, not drawn. The first 41 of `random.Random(opus-order).shuffle` are exactly the 41 archived items, and the 638 new calls follow the beacon order (bb-044's two missing forecasting calls first, then bb-127, …).
- *Lesson.* `ls-ss-b16` in `ledger/inbox/ss-wave5.jsonl` matches §0's sentence word for word and cites P12 and P3.
- *P18.* At B = 10,000, C1's lower bound has a seed-to-seed SD of about 0.001 near the bar. At accuracy 0.865 it sits at 0.815, 0.001 above 0.814, on all 40 seeds tried. That case is possible but unlikely in every plausible world. Not a flaw. The new C2 bound in F1 must report the same check.
- *P13.* EPS is applied at every threshold, including the untestable floor, and the boundaries tested under D1 land on the stated sides.

**D11. Holds** (at the frozen rule, and at F1's rule). Required emphasis:
- *Valence-only world* (both prompts give the same pick, right with probability v on each new item):
  - C2 holds by construction in this world. d is exactly 0 on the 159, and Opus's 40 archived all-four items are all concordant (39 right on both prompts, 1 wrong on both).
  - So P(fail) comes only from C1: P(pass) is 0.15, 0.47, 0.73, 0.96, 0.997 and 1.00 at v = 0.80, 0.83, 0.85, 0.88, 0.90 and 0.95.
  - Plausible v for Opus is at least Sonnet's accuracy on these same 159 items (0.868), and the 41 put it near 0.95. At plausible v, P(fail) is under 5%.
  - That is not a defect. In this world the claim ("the better-news question alone does as well as asking") is true, so a pass is the right answer. The world is mislabelled "null" in §4: it is a world where the hypothesis holds.
- *Worlds where the claim is false* are memory worlds (forecasting more than 5 points better) and weak-valence worlds. The design's Sonnet-like world is one: forecasting is +0.069 on the 159, P(fail) 0.62.
- *Measured worlds (P15).* I built worlds from the measured data, using Opus's outcomes on the 40 archived items within each of Sonnet's per-item cells:
  - On Sonnet-right/right items Opus was 37 of 37 right/right. On Sonnet's two "flattery wrong, forecasting right" items it was right on both prompts both times. On Sonnet's one wrong/wrong item it was wrong/wrong.
  - Each cell gets a Dirichlet over Opus's outcomes, with prior weight w on "Opus = Sonnet".
  - The 159 new items fall into Sonnet's cells as 132 right/right, 15 flattery-wrong/forecasting-right, 10 wrong/wrong and 2 flattery-right/forecasting-wrong.

  | world | P(pass), frozen point rule | P(pass), F1's upper-bound rule |
  |---|---|---|
  | Sonnet-conditional, w = 0.5 | 0.915 | 0.738 |
  | Sonnet-conditional, w = 2 | 0.811 | 0.443 |
  | Sonnet-conditional, w = 5 | 0.590 | 0.173 |
  | Sonnet-conditional, w = 20 | 0.227 | 0.008 |
  | Sonnet-like (dry run) | 0.337 | 0.037 |
  | Opus-41 | 1.000 | 1.000 |

- *Where the outcome turns.* The verdict turns on whether Opus fixes at least about a third of Sonnet's 15 "flattery wrong, forecasting right" new items. At the frozen rule, a pass needs a gap of at most 0.063 on the 159. The 41 cannot settle that (they hold two such items), so both P(pass) and P(fail) are at least 10% across the plausible range, w from 0.5 to 5.
- *P12, the 41 published items.* They do not make the outcome known in advance, but they do these things:
  - They fix 40 of the needed hits, lowering the flattery accuracy the 159 need for C1 from about 0.862 to about 0.835.
  - They contribute 40 concordant zeros to C2.
  - They are a random beacon-order sample, so including them does not bias the estimate.
  - They make C1 close to certain.

  §4's archive-split row (the 159 alone, with their own interval) is the right disclosure, and the scorer produces it.

**D12. Holds.**
- (a) The Prior work line (map ss-f9 and §0) states "predicts: unknown", backed by a described search ("no paper reports a prompted Claude model, or a valence question, on BrainBench"). That is the no-prior-statement case, so (d) applies.
- (b) Luo et al. 2024, arXiv 2403.03230 v4 HTML, opened. Every phrase the line cites is in the paper verbatim:
  - "Every LLM outperformed human experts on BrainBench with LLMs averaging 81.4% accuracy and human experts averaging 63.4%"
  - "LLMs were scored as choosing the abstract with the lower perplexity"
  - "Chat or instruction-optimized models performed worse than their base model counterparts"
  - "Prompting in natural language may yield less reliable judgments and degrade model competency"
  - "Phi-3 achieved an 82.5% accuracy"

  The paper evaluates no Claude model and no GPT-4 on the 200 human-written items (GPT-4 only wrote the 100 extra items), and it tests no valence, order or positive-result shortcut.
- (c) The only predicted outcome "in print" is this repository's own: ss-b10c's 41-item Opus row. §0 says what this bet adds (the 159 new items, the stricter bar, the matched C2), and the odds were stated with the dry run that fixes those 41 in view.
- (d) My search, in metascience and LLM-judge words rather than BrainBench's, is in the header. Its nearest hit, Bao et al. 2025 (arXiv 2505.18942, abstract opened), is about LLMs inferring peer-review norms from paper pairs, not about preferring positive results or telling real from altered findings. ss-b10c's Novelty search (results file) covered Luo et al.'s follow-ups, Wen et al. 2025, Lee 2026 and Zheng et al. 2023, and found none either.

## Required fixes

Each fix needs one dated DEVIATIONS.md row, written before any call and naming this review; one row covering F1–F4 is fine. Odds may be revised, with both numbers kept. Every fix tightens the design or its wording. None lowers the bar.

**F1 (D5, P2): decide C2 on a one-sided 95% upper bound, not on the point estimate.**
- **Rule.** In `scoring/score_b16.py`, C2 becomes: *the one-sided 95% upper bound of the paired item-bootstrap mean of (bettor item score − flattery item score), on the items with all four Opus calls, is at most 0.05 + EPS.* Use 10,000 resamples with `default_rng(20261104)`, same as `SB.boot`, and take the bound as the sorted resample means at index `int(0.95 * 10000) - 1`.
- **Reported, not the bar.** The point estimate and the two-sided [2.5%, 97.5%] interval.
- **Text.** Rewrite §4's C2 line, the `odds_event` (map node, §8, inbox bet row) and the §5 sentences to match. For example, in the pass sentence: "…the forecasting prompt did at most 5 points better (one-sided 95% upper bound +u points; point estimate d [lo, hi])…". Replace "does about as well as" with "does no more than 5 points worse than".
- **P18 check for the new bound.** Report the bound at 10 seeds. If its side of 0.05 differs across them, rerun at B = 100,000 and use that.
- **Dry run.**
  - Rerun `scoring/dry_b16_b17.py` under the new C2.
  - Add the Sonnet-conditional worlds above, built from the measured per-cell transitions on Opus's 40 archived items with w = 0.5, 2 and 5 (P15).
  - Relabel the valence-only world as "a world where the hypothesis holds", not "the null".
  - Show P(pass) and P(fail) each at least 10% under named plausible worlds. My runs give 0.17–0.74 pass across w = 0.5–5.
  - Commit the dry run.
- **Odds.** Re-elicit the engine odds on the new event from a fresh context handed the rerun dry run, keeping 0.50 as `engine_odds_first`.

**F2 (D7, P8): name the bundle.** In §5 and in `score_b16.sentences`' `fc` string, write: "asked directly which version was published, with the program's forecasting prompt (a different instruction, a question line, and a note that one version was altered by an expert), it was right …". In the pass sentence, replace "asking which version is real" with "the program's forecasting prompt". This brings back ss-b10c's audited wording.

**F3 (D8, P9): remove "too" and report the smaller models' C2.**
- Delete "too" from the pass sentence ("So on Opus, the 'better news' question alone …").
- In §4's secondaries, §5 item 6 and the scorer (`others_same_items`), add reported rows giving Haiku's and Sonnet's own bettor − flattery on the same items from `bettor/bbb-ratings.jsonl` (no calls), with the same bootstrap. Their current values are Sonnet +6.3 [+2.8, +10.0] and Haiku +4.8 [−1.8, +11.3] on all 200.
- The sentence: "On the same n items, ss-b10c's forecasting prompt did x points better than its flattery prompt on Sonnet [lo, hi] and y on Haiku [lo, hi] (reported rows)."

**F4 (D9, P10): run the leave-one-out checks on C2 too.**
- In `score_b16.py`, compute `c2_loo_flips` (items whose removal changes C2) and `c2_section_flips` (sections whose removal changes C2) under F1's rule, plus whether either flips the overall verdict.
- Add the matching §4 robustness line and a §5 item 6 clause, worded as for C1: "Leaving out any one of k items (…) would change whether the forecasting prompt stays within 5 points." Reported; the verdict is unchanged.
- Show both on synthetic rows in `dry_b16_b17.py --rules`.

When F1–F4 are committed, the reviewer checks them in an addendum to this file and sets `confirmed_at`. No call runs before then.
