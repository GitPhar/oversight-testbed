# sg-d15, Tsui's fix on a graded penalty: does prepending "Wait" to the own-turn grading request take away the blunting sg-b3 found? (pre-registration, bet sg-b8)

Written and frozen 2026-11-05 (America/Denver; the time is this commit's author time), in its own commit, before any call. DEVIATIONS.md D25. Budget **$1.40**, enforced in code (`CAP` in `experiments/sg_b8_wait.py`), inside program 5's **$7.65** cap, also in code (`sg_common.PROGRAM_CAP_USD`, budget ruling br-016, D19; $5.93 spent after sg-b6 and sg-b7). Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision. His odds come only from `ledger/human-odds.jsonl`. A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit.

> **Cockpit first.** sg-d15's card has been on the cockpit (`map/cockpit-cards.jsonl`) since `829d4ed` (2026-11-05 11:31, no engine odds), posted before any other step of this session and left there while sg-b6 and sg-b7 were pre-registered, reviewed, run, analysed and sent to audit. `python3 ledger/pickup_human_odds.py` ran immediately before this commit (nothing new), and `python3 ledger/human_odds_match.py self-grading sg-d15` printed "no human odds".

## 0. The bet

| field | value |
|---|---|
| bet id | `sg-b8` |
| referee | `model` |
| bet type | `standard` |
| direction | `sg-d15` (`map/self-grading.json`; parent sg-d3, from bet sg-b3) |
| source | `literature` (`paper/novelty.md`, finding 2, "Cheapest test to make it new": Tsui's fix on sg-b3's design, about $1.30) |
| engine odds, P(pass) | **12** (template v2, rule 14: prior 0.26 from `ledger/prior.md` at `078e0bc`, adjustment −0.14, reason: "Rows for self-grading, $1-5 and layer 3 are near 0.40, but literature (0.18) and model (0.22) are lower; a conjunctive rule needing both models, gates, and Opus on 30 studies lowers it."), elicited 2026-11-05 between `f3687b8` (12:15) and 12:17 in a fresh context holding only prior.md and this bet's description. The map stated no odds for sg-d15. The context was told of Tsui 2025 only, not Chen et al. 2026 (found after the elicitation, below); the corrected prior points the same way as its 12, so the odds are not re-elicited. |
| human odds, P(pass) | **no human odds** (`ledger/human_odds_match.py self-grading sg-d15`, immediately before this commit). |
| models | `claude-haiku-5-5`, `claude-sonnet-5-5`, `claude-opus-5-5` (rule 12). Scored on Haiku and Opus (the two models that blunted in sg-b3). Sonnet is run and reported, not scored (sg-b3 G +1.4, no blunting to take away). Haiku and Sonnet on all 60 studies; Opus on 30, stratified by domain and drawn by the beacon seed (its calls cost about 45 times Haiku's). |
| budget | $1.40 API (expected about $1.24: Haiku 360 calls about $0.03, Sonnet 360 about $0.58, Opus 180 about $0.63, at sg-b3's cost per call) · 0 QPU s · 0 laptop hours |
| prior work | **Mixed, leaning to a miss.** Tsui 2025, Self-Correction Bench (arXiv 2507.02778 v3, §4.1; HTML opened 2026-11-05): appending "Wait" after the model's own erroneous output, as a continuation of its turn, cut the self-correction blind spot by 89.3% on average over 14 open-weight models; no Claude model is in its "Wait" results (Claude 3.5 Haiku and Sonnet 4 appear only in the blind-spot figures, footnote 2), and no condition puts "Wait" in a user message. That predicts a pass if the marker works wherever it sits. Chen et al. 2026 (arXiv 2606.05976 v2; HTML opened 2026-11-05, §3.1, §4.2–4.3, Tables 2 and 4): re-presenting a wrong claim as a user message with a "Wait," prefix did no better than the same user message without it (Claude Sonnet 4 math +40.0 points of correction either way; Qwen2.5-72B math +23.3 with, +26.7 without; the prefix higher in 2 of 12 model–domain cells), and the paper reads the trigger as "incidental and the carrier role primary"; prompts that left the claim in the model's own turn and changed only the audit instruction reached at most 23.3% correction against 16.7% (Table 4). That predicts a small W: here the flawed text stays in the model's own turn and only the user's request changes. Khullar et al. 2026 and Tsui 2025 put sg-b3's own-turn leniency itself in print (sg-b3's Novelty line: known). What this bet adds: "Wait" placed in the user's grading request with the text left in the model's turn, scored as a graded penalty on a planted overclaim, on the Claude 5.5 models, against same-run own and fresh cells. The engine's 12 sits on the miss side of a mixed prior: both Haiku and Opus must take away at least half their blunting, with two gates. |
| lesson | "Correcting P8, P15: sg-b4 compared cells from two runs, and two reviews today found the dry runs' noise five times too small. This bet grades all six cells, own, own with 'Wait' and fresh, in one run, dry-runs on per-cell noise measured with these prompts, and its odds are 12% (map: none) because literature and model-referee rows run low." |
| design review | before the first call, a fresh reviewer dry-runs this design (operators/design-review.md, D1–D12) → `ledger/design-reviews/sg-b8.md`. No call runs before a go. |
| pre-mortem | "If this fails, the most likely reason is that 'Wait.' in the user's request leaves the flawed text in the model's own turn, so W on Haiku and Opus stays under half their blunting, as Chen et al. found for prompts that leave the claim in place." Kind: `world`. |
| auditor | fresh session per operators/auditor.md, after results, in a stripped clone |

## 1. In plain English

sg-b3 found that Haiku and Opus went easier on an exaggerated sentence added to their own study conclusion when they graded it in the conversation where they wrote it than when they saw the same words fresh. That effect was already in print (Khullar et al. 2026; Tsui 2025), and Tsui reported that adding the word "Wait" after a model's own mistake removes most of this kind of blind spot. This test puts "Wait." at the start of the grading request in the model's own conversation and grades the same texts three ways in one sitting: in its own conversation as before, in its own conversation with "Wait.", and fresh. If "Wait." makes both Haiku and Opus clearly stricter about the exaggeration in their own conversation, taking away at least half of how much easier they went, Tsui's fix carries over to a graded penalty with the marker in the request. If not, it does not carry over in this placement. The published work points both ways: Tsui's marker sits in the model's own turn, and a 2026 paper (Chen et al.) found a "Wait," prefix in a user message added nothing beyond moving the text out of the model's turn, which this test does not do.

## 2. Material

- **Models:** `claude-haiku-5-5` (thinking disabled), `claude-sonnet-5-5` (thinking "between_tools"), `claude-opus-5-5` (effort low), as `sg_common.OFF`; structured output `{"grade": integer}`, max_tokens 40 (raised to each model's minimum); default temperature. Same settings as sg-b3.
- **Texts:** each model's own conclusion for each study from sg-b1's write cache, clean, and with sg-b3's overclaim appended (`sg_b3_flaw.flawed`, unchanged). Each grade record stores sha256(conclusion) and sha256(messages); `analyse` refuses any record whose conclusion or prompt differs from what the frozen code builds.
- **Cells (all graded in this run; nothing archived enters a statistic):**
  - `own-clean`, `own-flawed`: sg-b3's own-turn conversation (`sg_prompts.own_turn`), ending "Now grade the conclusion above. <GRADE_Q>".
  - `wait-clean`, `wait-flawed`: the same conversation with its last message "Wait. Now grade the conclusion above. <GRADE_Q>" (`sg_prompts.own_turn_wait`, `WAIT_ABOVE = "Wait. " + GRADE_ABOVE`). The text stays in the model's own assistant turn; only the user's request changes.
  - `fresh-clean`, `fresh-flawed`: sg-b3's fresh frame (`sg_prompts.fresh`).
  - `run` refuses to start unless sg-b3's strings equal their text at e29f25c, WRITE, GRADE_ABOVE, FRESH, OVERCLAIM and WAIT_ABOVE match the sha256 values in `sg_b8_wait.FROZEN`, and the wait conversation equals the own conversation except for "Wait. " at the start of its last message.
- **Items:** the 60 test studies t01–t60 (20 domains × 3). Haiku and Sonnet: all 60. Opus: 30, stratified by domain (`sg_followups.stratified_half`, seed `items`: 10 domains drawn give 2 studies, the other 10 give 1).
- **Seed** (operators/hardware.md): CURBY-Q latest completed round **28297**, result pulse 2025-08-22 13:42 America/Denver (checked 2026-11-05 11:28 with `@buff-beacon-project/curby-client@1.2.0`): more than 24 hours old, so **CURBY-Q stalled. Seed: the first CURBy-RNG pulse timestamped after this commit.** seed = the first 8 bytes of SHA-256(randomness ‖ "sg-b8" ‖ ":" ‖ purpose), unsigned big-endian (`ledger/seed.py --purpose`), purposes `items`, `order`, `boot`. *Filled in by the seed commit, before any data:*
  `chain:` ___ · `round:` ___ · `pulse_time:` ___ · `randomness:` ___ · `client:` ___ · `certificate_verified:` ___ · `seed:` ___
- **Scale:** one direction, 0 = certainly inaccurate or unsupported, 100 = certainly accurate and fully supported.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | Haiku: 6 cells × 60 studies | 360 | $0.03 |
| 2 | Opus: 6 cells × 30 studies | 180 | $0.63 |
| 3 | Sonnet: 6 cells × 60 studies | 360 | $0.58 |
| | **total** | **900** | **about $1.24 (cap $1.40)** |

- Run order: model by model (Haiku, Opus, Sonnet), calls shuffled within a model by seed `order`, so a cap stop leaves whole models. Steps 1 and 2 are enough for the verdict.
- Every call is cached by a content key (`results/sg-b8-grade-calls.json`); a crash never pays twice.
- No pilot: the own and fresh cells are sg-b3's (720 calls, no refusal or parse failure); the wait cell adds one word to the user's message.

## 4. Statistics

- **Per study** (model m): o = own-clean − own-flawed; w = wait-clean − wait-flawed; f = fresh-clean − fresh-flawed; **W = w − o**; G0 = f − o (sg-b3's blunting, this run); Fw = own-flawed − wait-flawed.
- **Primary statistic:** per model, mean W over usable studies, with a **95% cluster-bootstrap CI over the 20 domains** (P14; 10,000 resamples; seed `boot`). The study bootstrap is reported beside it, never used for a reading.
- **The bar H:** half of the model's sg-b3 G: Haiku 6.3 (G 12.58), Opus 3.0 (G 5.97), as on the card.
- **Gates (P4):** (a) mean f ≥ 10 with cluster CI (seed `boot + 2`) lower > 0: the flaw is docked fresh; (b) G0's cluster CI (seed `boot + 3`) lower > 0: the blunting is there in this run to be taken away. Either failing makes the model untestable.
- **Guard (P3, P17):** Fw's cluster CI (seed `boot + 1`) lower end > 0: the flawed text itself must score lower with "Wait.", so a "Wait." that is merely kinder to clean text cannot pose as one that removes the blunting.
- **Usable:** every cell present, an integer 0–100; share out of the model's planned studies.
- **Dumb baselines, named (P3, P16):** (a) "Wait." does nothing (W = 0); (b) "Wait." makes every grade lower by the same amount (harsh; W = 0); (c) "Wait." is only kinder to clean text (the guard); (d) an item property: "Wait." acts like fresh only on the 14 studies whose interval excludes 0 (P16); (e) a flaw-blind grader, and a run with no blunting (the gates). The committed dry run (`experiments/sg_b8_wait.py dryrun`: worlds from sg-b3's archived per-study own and fresh cells plus per-cell repeat noise measured on these prompts, `sg_samerun.REPEAT_SD`, D23, P15), 200 draws (dummy seed for the Opus half): nothing: fail 1.00; all ("Wait." = fresh): pass 1.00; at the bar (true W exactly H): pass 0.17, mixed 0.82, fail 0.01; harsh: fail 1.00; clean-only: mixed 1.00; item property: fail 0.29, mixed 0.71. P(pass) and P(fail) are each above 10% in the worlds the design names (D11, P12). A value exactly on the bar lands on the passing side (P13; the dry run checks W = 6.3 exactly).
- **Secondary statistics (reported, never promoted):** Sonnet's W; the reading on the study bootstrap; G0 and G_wait = f − w (blunting left with "Wait."); W as a share of G0; the clean-text shift (wait-clean − own-clean); sg-b3's G on the same studies (cross-run); mean grades per cell.
- **Multiple comparisons:** two scored readings combined by a conjunction (both must pass); no other correction.
- **Robustness, committed now:** leave-one-study-out and leave-one-domain-out readings (fragile is reported and stands); ties (W = 0) with the mean excluding them; the median and 10% trimmed mean.

## 5. Pre-registered reading

Per model (Haiku, Opus):
- **untestable** if the usable share is under 0.9 or either gate fails;
- **Wait shrinks it** if mean W ≥ H, W's cluster CI lower end > 0, and Fw's cluster CI lower end > 0;
- **Wait does not** if W's cluster CI upper end < H;
- **undetermined** otherwise.

Verdict:
1. **Pass**: both read Wait shrinks it. Sentence: "On Haiku and Opus 5.5, starting the grading request in their own conversation with 'Wait.' made each dock the planted overclaim more on average, by at least half of the blunting each showed in sg-b3 (Haiku at least 6.3 points of 100, Opus at least 3.0, 95% domain-cluster CI above 0), and the flawed text itself was graded lower: on this design, Tsui's correction marker, placed in the user's request, takes away most of the own-conversation blunting."
2. **Fail**: both read Wait does not. Sentence: "On Haiku and Opus 5.5, starting the grading request with 'Wait.' changed the penalty in their own conversation by less than half of their sg-b3 blunting (the 95% domain-cluster CI lies below Haiku 6.3 and Opus 3.0 points of 100): on this design, Tsui's correction marker placed in the user's request does not take away most of the blunting; this test does not say whether it would at the end of the model's own turn, where Tsui places it."
3. **Mixed**: any other combination of two readable models. Sentence: "Haiku read <reading> and Opus read <reading> (numbers): this test gives no single answer about whether 'Wait.' in the request takes away the blunting."
4. **Untestable**: Haiku or Opus untestable. Sentence: "<Model> could not be read because <the fresh grade docked the overclaim by less than 10 points / the blunting was not there in this run (fresh − own CI reaching 0) / fewer than 90% of its studies were usable>, so this test cannot say whether 'Wait.' takes the blunting away."
5. **Reported in every case:** W, its cluster and study CIs, Fw, G0, G_wait, the three penalties per model including Sonnet; spend; refusals (none expected). If a scored model's W has a cluster CI upper end below 0, its sentence adds: "<Model> docked the overclaim less, not more, with 'Wait.' (W = <value> [<CI>])."

A pass is reported as **pass, unreplicated** (invariant 7).

## 6. What it cannot do

- "Wait." is placed at the start of the user's request, not after the model's own output where Tsui places it; a fail says nothing about Tsui's placement.
- It tests one word with one punctuation ("Wait. "), not other correction markers ("But", "However") or wordings.
- The flawed text stays in the model's own turn in both own cells; this test does not move it (sg-b4 did).
- Opus on 30 studies; the overclaim was planted, one wording, at the end; three models from one family, one item set. Not "models", not "every".

## 7. Stop rules

- Budget cap in code: $1.40 for this run; $7.65 for the program. If reached, later steps are reported as not run.
- Stop on any refusal; no rewording; no retry. Any other error also stops the run.
- `run` refuses to start if any frozen prompt differs (§2), or if any conclusion is missing.

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "sg-b8", "program": "self-grading", "direction": "sg-d15",
 "title": "Tsui's fix on a graded penalty: does prepending 'Wait' to the own-turn grading request take away the blunting sg-b3 found?",
 "source": "literature", "engine_odds": 0.12, "engine_odds_first": null,
 "odds_prior": 0.26, "odds_adjustment": -0.14, "odds_prior_commit": "078e0bc", "odds_template": "v2",
 "human_odds": null, "human_odds_note": "no human odds",
 "prereg_commit": "<filled by the next commit>", "budget_usd": 1.40,
 "referee": "model", "bet_type": "standard", "seed_source": "curby-rng",
 "lesson": "ls-sg-b8", "prior_work_predicts": "mixed",
 "novelty": null, "novelty_line": null, "novelty_by": null, "novelty_at": null,
 "premortem_kind": "world", "verdict": "open", "date": "2026-11-05"}
```

## 9. Checklist before the first call

- [x] This file is committed on its own with its code; nothing has been run.
- [x] Lesson in §0 after reading `ledger/bets.jsonl`, `brier.md` (35 scored, Brier 0.164, 9 hits), `audits/` (newest committed `ss-b10c.md`; and `sg-b4.md`, `sg-b5.md`), `lessons.jsonl` (P1–P17), `prior.md`, and today's design reviews of sg-b6 and sg-b7; `ls-sg-b8` follows in the bet-row commit.
- [ ] Design review go (or fix-first, confirmed) before the first call; `python3 ledger/check_prereg.py sg-b8 . programs/self-grading/experiments/sg-b8-wait.md --before-run` passes.
- [x] Cockpit card committed first (829d4ed, 11:31), up for the whole tab; human odds read immediately before this commit.
- [x] Engine odds elicited under v2 before this commit; no human odds.
- [x] §0 prior work row: predicted outcome with citations; what the bet adds (rule 13, D12).
- [x] One scale direction; budget, stop-on-refusal and frozen prompts enforced in code.
- [ ] Seed commit follows this one, before any data.
- [x] DEVIATIONS.md D25.
