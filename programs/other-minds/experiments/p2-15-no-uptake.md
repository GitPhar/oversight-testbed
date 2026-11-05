# P2-15. Do the model's predictions of its own quirks beat a guess of "no effect"? (pre-registration)

Written and frozen in its own commit; the commit's author time (America/Denver) is the freeze time. Before the om-p2-4 prediction cache (`results/p2-4-calls.json`) is opened for this analysis. DEVIATIONS.md D17. Budget **$0**: archive only, no model is called; `experiments/p2_15_no_uptake.py` blocks every socket. Stop on refusal: not applicable (no calls).

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision, in a terminal, a chat or a question dialog. His odds come only from `ledger/human-odds.jsonl` (the cockpit's downloads, committed); if a direction has no line there when its bet is pre-registered, the bet proceeds marked "no human odds". A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit. Sean's judgment is recorded and scored as steers in `ledger/steers.jsonl`: seed questions, vetoes, added questions and architecture decisions.

## 0. The bet

| field | value |
|---|---|
| bet id | `om-p2-15` |
| referee | `model` |
| bet type | `standard` |
| direction | P2-15 (`map/program-2-map.md`, "Follow-ups (remap 2026-11-05)"; `map/other-minds.json` node P2-15; cockpit card in `map/cockpit-cards.jsonl` since the remap commit `a42a149`) |
| source | literature: the om-p2-4 audit's finding that its gate was met by a know-nothing predictor (`ledger/audits/om-p2-4.md`, B9) |
| engine odds, P(pass) | **18**, from a fresh context under rule 14 (template v2), stated 2026-11-05 10:05 America/Denver before this commit: prior **0.32** (`ledger/prior.md` at `73eb5cf`), adjustment **−0.14**, reason: "other-minds 0/7 and literature 2/15 rows; dry run passes only below ~7.5 points of prediction noise against an 8.85-point no-uptake error, with a 16-item bootstrap." The map's odds were **55** (remap 2026-11-05, `a42a149`, one pass, not v2). A first fresh context, given the design with uptake units as the primary (before the dry run moved it to rating points), said 0.32 − 0.12 = **0.20**; it is kept as `odds_v2_first_design`, not used. `engine_odds_first` 0.55, `engine_odds` 0.18. |
| human odds, P(pass) | **70** (`ho-20261105-061152-bxe`, recorded 2026-11-05 06:11:52 on the cockpit; copied by `python3 ledger/human_odds_match.py other-minds P2-15`, run immediately before this commit). His card's event is the map's: "On Haiku, self-prediction error on the uptake cells is below the always-no-uptake predictor's, BCa 95% upper bound of the difference below 0." This bet's event is that event, with the error measured in rating points (§4); he is scored on this bet's outcome. |
| models | `claude-haiku-5-5` only, not all three (rule 12), because no model is in the loop: this is an archive test of om-p2-4's committed Haiku predictions of Haiku's measured program 1 behaviour. The same question on Sonnet and Opus needs new calls; it is P2-14's territory. |
| budget | $0 API · 0 QPU s · minutes of laptop time |
| lesson | Correcting P3 and P15: om-p2-4's gate was passed by a know-nothing predictor. This bet scores self-prediction against the no-uptake guess in rating points, chosen after a dry run on program 1's measured cells showed uptake units let tiny displacements decide, and its odds are 18% (from 55% on the map) because zero is strong where shifts are small. |
| prior work | Nisbett & Wilson (1977) and Nisbett & Bellows (1977), as read in `map/reads/d-first-third-person.md`: subjects' predictions of their own reactions are no more accurate than observers', and both are often wrong; neither paper compares against a "no effect" guess. Binder et al. (2024, "Looking Inward", arXiv 2410.13787): models fine-tuned to predict their own behaviour beat other models trained on the same behaviour, and untuned models do little better than simple baselines on hypothetical self-prediction. Our own record: om-p2-4's published table gives the self arm's six uptake effects within 0.03 of measured on own-source cells (effect level), so the effect-level version of this question is already answered in our own archive and is reported here only as a secondary; the cell-level question in §4 is not in print anywhere we looked. |
| design review | before the analysis, a fresh auditor dry-runs this design (oversight-testbed `operators/design-review.md`) → `ledger/design-reviews/om-p2-15.md`, verdict go / fix-first / redesign. The analysis is not run before a go. |
| pre-mortem | "If this fails, the most likely reason is that self-predictions miss individual cells by about 8 rating points or more (noise or per-cell bias), which equals the no-uptake guess's error because most measured shifts are small." Kind: `world`. Checkable: the primary's MAE(self) against 8.85 points, and the own/other split. |
| auditor | fresh session per oversight-testbed `operators/auditor.md`, after results, in a stripped clone with a sealed plant draw (`operators/plant.md`) |

**What the lesson rests on** (read at oversight-testbed `73eb5cf`, 2026-11-05 09:50 America/Denver): `ledger/bets.jsonl` (66 bets; 37 scored, 12 hits; program 2: om-p2-1, -2, -3b, -5, -6, -6r, -7 scored, 0 hits; om-p2-3 untestable, om-p2-4 undetermined); `ledger/brier.md` (engine Brier 0.188 on 37; hit rate 12/37 = 0.32); `ledger/prior.md` at `73eb5cf` (prior 0.32); `ledger/audits/` (newest: `ng-p3-18.md`, `4f07a2f`; newest in program 2: `om-p2-7.md`, `399df63`; the parent's audit `om-p2-4.md`); `ledger/lessons.jsonl` (P1–P17). How each pattern applies:
- **P3 (no dumb baseline).** The bet *is* a dumb-baseline test: the om-p2-4 audit showed its gate and r bar were met by a predictor that assumes no uptake. The no-uptake guess is the comparator; a second dumb predictor (copy the shown number) is reported.
- **P15 (dry run on assumed spreads).** The dry run (§6, `experiments/p2-15-dryrun-output.txt`) uses program 1's measured cells (published, and used to freeze om-p2-4), with synthetic predictions; the P2-4 prediction cache was not opened. It found that the map's unit, uptake as a fraction of displacement, divides prediction noise by displacements as small as 0.05, so a self-predictor that knows its true shift exactly fails at 10 points of noise because of a few tiny-displacement cells. The primary is therefore in rating points; uptake units are a secondary.
- **P12 / D11 (the bet must go either way).** In the dry run: P(pass) 1.00 for a self-predictor that knows its shift with 5 points of noise, 0.79 at 7.5, 0.00 at 10; 0.99 for half its shift at 5 points; 0.00 for any predictor that knows nothing. Haiku's per-cell prediction error on this task has never been measured, so both outcomes are live.
- **P13 (a boundary in plain float).** An upper bound within 1e-9 of 0 is not below 0; the dry run checks 0.0, 0.3 − 0.1 − 0.2 and −1e-4.
- **P10 (one item decides).** Leave-one-vignette-out re-applies the rule with its own BCa interval; a flip appends a frozen sentence.
- **P14 (items sharing a template bootstrapped as independent).** The resampling unit is the vignette (16), which carries both its statements and every displacement and source.
- **P2 (null rule without power).** Not a null rule: the pass is a detection. A fail is reported as "did not show", never as "no better than no effect".
- **P8 (more than the named factor differs).** The two predictors are scored on the same cells against the same measured re-ratings; only the prediction differs.
- **P4, P5, P6, P7, P11, P16, P17:** no manipulation, no fitted rival families, no control band, no calls, no leave-one-out labels inside a score, no item-property baseline, no design-review fix yet. They do not apply.

## 1. In plain English

Program 1 measured how far a number shown to Haiku moves its next rating: a number presented as its own earlier answer pulls it a long way, another person's number barely moves it. In om-p2-4, Haiku was shown those same conversations and asked what it would answer. The audit of om-p2-4 found that its test could not tell whether those self-predictions were any good, because a predictor that simply assumes the shown number has no effect passed its checks too. This bet asks the plain question: cell by cell, are Haiku's predictions of its own re-ratings closer to what it actually did than the guess "no effect, it gives its usual rating"? We use only the saved predictions and the saved measurements; nothing new is asked of any model. A pass means its self-predictions carry real information about how it moves. A fail means they did not detectably beat assuming no movement. The rival reading of a pass is that Haiku simply re-runs the judgment when shown the transcript ("simulation by doing"); this test cannot separate that from self-knowledge, and does not try.

## 2. Material

- **Archives (read-only, committed):** om-p2-4's prediction cache `results/p2-4-calls.json` (SHA-256 prefix `a711ab441d69124d`), keys `U|a|…` (self), `U|b|…` (Sam), `U|c|…` (one-line observer), 5 predictions per cell; program 1's measured cells through `p2_4_interpersonal.load()` (bm0's lag-0 cells with bm1 and run 3, `programs/entangled-mind/results/`, base ratings from `exp4-run-3-calls.json`, SHA-256 prefix `bdeef6909a6208c4`). Fields read: `A`, `r1`, the base, and each prediction's `value`.
- **Cells:** 16 items × 2 statements × d ∈ {±10, ±30, ±60} × source {own, other} = 384; program 1's drop rule (|A − base| < 0.05) leaves **324** (counted in the dry run from program 1's archive alone).
- **Predictors per cell:** self (a) = mean of its 5 predictions, each clipped to 0–100, divided by 100; Sam (b) and one-line observer (c) the same; **no uptake** = the statement's base rating; **copy** = the shown number A.
- **Seed** (operators/hardware.md): CURBY-Q latest completed round **28297**, result pulse 2025-08-22 13:42 America/Denver (checked 2026-11-05 09:55 with `experiments/curby_seed.mjs check`, before this commit). That is more than 24 hours old, so CURBY-Q is **stalled**. **Seed: the first CURBy-RNG pulse timestamped after this commit.** seed = the first 8 bytes of SHA-256(randomness ‖ `om-p2-15`) by `ledger/seed.py --purpose boot`; its `seed32` seeds the bootstrap. The seed is used only for the bootstrap; nothing is drawn. *Filled in by the seed commit, before any analysis:*
  `chain:` CURBy-RNG · `pulse index:` 1592485 · `pulse_time:` 2026-11-05 10:01:00 America/Denver · `previous pulse time:` 10:00:00 (index 1592484, before the 10:00:07 commit) · `randomness:` 19b96a769e2c616fbd5bf25e9f77e6802a3d559a31e68658b8fb6eb0ffac96c862f3bda6a4dc1daff573b52f3395c56871781efa6bb83f50d0914c9112834bbd · `client:` @buff-beacon-project/curby-client@1.2.0 via `experiments/curby_seed.mjs` · `certificate_verified:` false · `seed (boot):` 12951094005506331256 · `seed32 (boot):` 1390760568. Record: `data/p2-15-seed.json`.
- **Scale:** one direction (0 = certainly false, 100 = certainly true), as in every archived conversation.

## 3. Calls

None. One analysis run of `python experiments/p2_15_no_uptake.py` (program 1's interpreter), writing `results/p2-15-no-uptake.json` and `results/p2-15-tables.md`.

## 4. Statistics

- **Primary statistic:** Δ = MAE(self) − MAE(no uptake), where MAE is the mean, over the kept cells (both sources, all six displacements, pooled cell-weighted), of |predicted re-rating − measured re-rating| in rating points (0–100). For the no-uptake predictor this is |measured re-rating − base| (mean 8.85 points in the dry run, from program 1's archive).
- **Uncertainty:** item bootstrap over the 16 vignettes (each vignette carries all its cells), 10,000 resamples by multinomial counts from `seed32 (boot)`; **BCa** 95% interval (bias correction from the share of resamples below the point, acceleration from the leave-one-vignette-out jackknife). The percentile interval is printed beside it.
- **Split:** none; nothing is fitted.
- **Secondary statistics (reported, never promoted):** Δ by source (own, other) and by |d| (10, 30, 60); Δ in uptake units (the map's and om-p2-4's unit, |u_pred − u_meas| with u = (rating − base)/(A − base)); Sam (b), one-line observer (c) and copy each against no uptake; self against copy; self against Sam (P2-14's comparison, on this archive's 5 repeats, descriptive only); the effect-level version over om-p2-4's six uptake effects, MAE(self) − mean|measured effect|, with its BCa interval (already implied by om-p2-4's published table; reported for completeness).
- **Multiple comparisons:** one primary; secondaries descriptive and uncorrected, labelled so.
- **Robustness committed now:** leave-one-vignette-out, each re-applying the full rule with its own 10,000-resample BCa interval (seeds `seed32 + 1 + i`).

## 5. Pre-registered reading

1. **Untestable:** fewer than 300 cells survive the drop rule, or more than 2% of kept cells have no self-prediction. Sentence: "The test could not be run as pre-registered: {why}."
2. **Pass:** the BCa 95% upper bound of Δ is below 0 (by more than 1e-9). Sentence (frozen in `SENTENCES`): "The pre-registered event occurred. On Haiku, across the {n} uptake cells, the model's predictions of its own re-ratings missed its measured re-ratings by {ea} rating points on average, against {ez} for a guess that the shown number has no pull; the difference is {d}, 95% BCa interval [{lo}, {hi}], wholly below 0. Its self-predictions carry information about how far a shown number moves it, beyond assuming no effect."
3. **Fail:** otherwise. Sentence: "The pre-registered event did not occur. … not wholly below 0. This test did not show that its self-predictions beat assuming no effect."
4. **Leave-one-out sentence**, appended in every case: "Leaving out any one of the 16 vignettes leaves the label unchanged." or "Leaving out one vignette changes the label: without {items}, the rule reads {other}. The label rests on {k} of 16 vignettes." A flip does not change the label; it is reported.
5. **Reported in every case:** both MAEs, Δ with BCa and percentile intervals, the secondaries table, the leave-one-out result.

A pass is reported as **pass, unreplicated** (one model, one archive, one task).

## 6. What it cannot do

- It cannot say *why* the self-predictions are good or bad: a model shown the transcript may simply redo the judgment, so a pass is not evidence of privileged self-access (Nisbett & Wilson's criterion needs an observer, which is P2-14).
- Self arm (a) is "you, in a fresh context, reading the transcript", not the model in its own conversation.
- One model, one task (planted-number uptake on program 1's 16 vignettes), one prediction prompt. No "every" or "all".
- The no-uptake guess is strong where measured shifts are small (most other-source cells), so the pooled result depends on the own/other mix of this archive; the split is reported.
- The dry run (`experiments/p2-15-dryrun-output.txt`) used program 1's measured cells and synthetic predictions; its noise model (Gaussian, the same in every cell) is an assumption, which is why the odds are not taken from it.

## 7. Stop rules

- No calls; sockets blocked in code. Any exception stops the run and is reported.
- The analysis runs once after the design review's go. A crash is re-run on the same code and seed; no part of the design changes after the cache is opened.

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "om-p2-15", "program": "other-minds", "direction": "P2-15", "title": "Do the model's predictions of its own quirks beat a guess of no effect?", "source": "literature", "referee": "model", "bet_type": "standard", "budget_usd": 0, "cost_usd": 0, "lesson": "ls-om-p2-15", "design_review": {"path": "ledger/design-reviews/om-p2-15.md", "verdict": null}, "verdict": "open"}
```

## 9. Checklist before the analysis

- [x] This file is committed on its own; the P2-4 prediction cache has not been opened for this analysis (the dry run read program 1's measured cells only).
- [x] Lesson in §0 after reading bets.jsonl, brier.md, prior.md, audits/ and lessons.jsonl; the same sentence goes to `ledger/lessons.jsonl` as `ls-om-p2-15`.
- [ ] Design review go (or fix-first confirmed) before the analysis.
- [x] Cockpit card committed before this file (`a42a149`); `ledger/human-odds.jsonl` read immediately before this commit (`human_odds_match.py`: 0.70).
- [x] Engine odds from a fresh context under rule 14 (prior.md at `73eb5cf`), stated before this commit.
- [x] The §5 rule can be applied by a stranger; verdict sentences frozen in code.
- [x] Pre-mortem is one sentence with its kind.
- [x] Seed rule in §2; the seed commit follows before any analysis.
- [x] Budget $0; sockets blocked in code.
- [x] DEVIATIONS.md D17.
