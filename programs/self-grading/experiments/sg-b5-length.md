# sg-d11, length-matched overclaim: does a model still go easier on an exaggeration in its own conversation when the exaggeration does not make the answer longer than asked? (pre-registration, bet sg-b5)

Written and frozen 2026-11-05 10:08 (America/Denver), in its own commit, before any call. DEVIATIONS.md D14. Budget **$0.85**, enforced in code (`CAP` in `experiments/sg_b5_length.py`), inside program 5's **$5.00** cap, also in code (`sg_common.PROGRAM_CAP_USD`; $3.63 spent before sg-b4; sg-b4 runs first and may spend up to $0.50, so the program cap may stop this run before its own cap: Opus runs first for that reason). Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). His odds come only from `ledger/human-odds.jsonl`; a decision this session would otherwise ask about, it makes under the written rules and states in its report and commit.

> **Cockpit first.** sg-d11's card is in `map/cockpit-cards.jsonl` (line 10), committed before this file. `python3 ledger/pickup_human_odds.py` ran at 09:52 (nothing new), and `python3 ledger/human_odds_match.py self-grading sg-d11` was read immediately before this commit.

## 0. The bet

| field | value |
|---|---|
| bet id | `sg-b5` |
| referee | `model` |
| bet type | `standard` |
| direction | `sg-d11` (`map/self-grading.json`; parent sg-d3, from bet sg-b3) |
| source | `literature` (the sg-b3 audit's cheapest overturning test) |
| engine odds, P(pass) | **22** (template v2, rule 14: prior 0.32 from `ledger/prior.md` at `73eb5cf`, adjustment −0.10, reason: "Literature (0.13), under-$1 (0.19) and model-referee (0.22) rows outweigh layer 2 (0.67, few bets); conjunctive rule needs Opus, parent 6.0, barely above +5; Sonnet 1.4 unlikely."), elicited 2026-11-05 09:57 in a fresh context holding only prior.md and this bet's description. The map's remap-pass odds were 45 (2026-11-05 05:55, not v2); both are kept, as `engine_odds_first` 0.45 and `engine_odds` 0.22. |
| human odds, P(pass) | **55**, `ho-20261105-061152-u4l` (recorded 2026-11-05 06:11:52, committed before this file). His card's event is this bet's pass rule, except that this pre-registration reads every bar on the 20-domain cluster bootstrap (as the map's engine-only note already said); the bet is scored once, on §5. |
| models | `claude-haiku-5-5`, `claude-sonnet-5-5`, `claude-opus-5-5` (rule 12), all on all 60 studies; Opus is the model at stake, so its studies are not cut. |
| budget | $0.85 API (expected about $0.76: Opus 140 calls about $0.53, Sonnet 140 about $0.22, Haiku 140 about $0.01, at sg-b3's cost per call) · 0 QPU s · 0 laptop hours |
| prior work | **Mixed.** Tsui 2025, Self-Correction Bench (arXiv 2507.02778, v3, COLM 2026; HTML opened 2026-11-05): the identical error is left uncorrected far more often in the assistant turn than in the user turn (Claude 3.5 Haiku 52.5%, Claude Sonnet 4 41.4% blind spot, Table 7), with the same text in both positions and no length cue, which predicts the blunting survives length matching (a pass). Khullar, Hopkins, Wang and Roger 2026, Self-Attribution Bias (arXiv 2603.04582; HTML opened 2026-11-05): turn-position leniency is much stronger for the model's own generations than for planted text, and on planted text in open-ended harmfulness ratings (Table 1, off-policy) Claude 3.5 Haiku shifted lenient (+0.74 of 10) while Claude Opus 4.1 (−0.46) and Sonnet 4 (−0.79) shifted self-critical, which points against a planted-text blunting on the larger models, and Opus is this bet's conjunct. No paper tested a length cue. What this bet adds: it removes the one cue sg-b3's audit could not exclude for Opus, a length breach quoted right above the fresh text, on the 5.5 models; it is also the second design invariant 7 owes sg-b3. The engine's 22 sits with Khullar's off-policy result for the larger models, not with Tsui's pass, because the rule needs Opus and Opus cleared sg-b3's bar by under one point. |
| lesson | "Correcting P14, P8: sg-b3 bootstrapped 20 shared domains as 60 independent studies, and its overclaim also broke the length limit. This bet reads the bar on a 20-domain cluster bootstrap and swaps the last sentence for the overclaim so lengths match, and its odds are 22% (from 45% on the map) because literature, under-$1 and model-referee rows run low." |
| design review | before the first call, a fresh reviewer dry-runs this design (operators/design-review.md, D1–D12) → `ledger/design-reviews/sg-b5.md`. No call runs before a go. |
| pre-mortem | "If this fails, the most likely reason is that Opus's sg-b3 blunting was the length breach: with the overclaim swapped in, Opus docks it alike in both places and G′ falls under 5." Kind: `world`. |
| auditor | fresh session per operators/auditor.md, after results, in a stripped clone |

## 1. In plain English

In sg-b3, Haiku and Opus went easier on an exaggerated sentence added to their own three-sentence study conclusion when they graded it in the conversation where they wrote it than when they graded the same words fresh. But for Opus every exaggerated text was also longer than the three sentences asked for, and the fresh request quotes that limit right above the text, so Opus may simply have noticed the length more when grading fresh. This test swaps the conclusion's last sentence for the exaggeration instead of adding it, so the text is exactly as long, in sentences, as the clean one. If Opus and at least one other model still go easier on it in their own conversation, by at least 5 points of 100, length was not the reason. If Opus grades it alike in both places, Opus's part of sg-b3's result came from the length cue. The published work points both ways: the role effect in Tsui 2025 needs no length cue (a pass), but Khullar et al. 2026 found planted text weakly or oppositely treated by the larger Claude models (against). A rival this design adds: the swapped-out sentence is usually the conclusion's caveat, so the flawed text loses a caveat as well as gaining an exaggeration.

## 2. Material

- **Models and settings:** as sg-b3 (`sg_common.OFF`, `MIN_TOKENS`; structured output `{"grade": integer}`, max_tokens 40, default temperature).
- **Texts:** each model's own sg-b1 conclusion (`results/sg-b1-write-calls.json`; 2 to 4 sentences each: Haiku 46 two and 14 three, Sonnet 2 two and 58 three, Opus 56 three and 4 four). **flawed′** = the conclusion with its last sentence (as `sg_b3_flaw.n_sentences` counts them) replaced by sg-b3's overclaim (`sg_prompts.OVERCLAIM`, unchanged, filled per domain). Every flawed′ has exactly as many sentences as its clean text (checked in code before any call); 60/60 Haiku, 60/60 Sonnet and 56/60 Opus flawed′ are within three sentences (the 4 others are four sentences, as their clean texts are). flawed′ is shorter than the clean text by 59 (Haiku), 17 (Sonnet) and 55 (Opus) characters on average.
- **Prompts:** sg-b3's `own_turn` and `fresh`, word for word (`check_frozen_prompts` against `e29f25c`).
- **New cells:** own-flawedL, fresh-flawedL on all 60 studies per model; drift-own-clean, drift-fresh-clean on 10 drift studies (one from each of 10 distinct domains, drawn by seed `items`; the same 10 for every model).
- **Reused (archived), never re-run:** sg-b3's own-clean and fresh-clean grades (`results/sg-b3-grade-calls.json`), checked by conclusion hash. sg-b3's flawed grades are read only for the secondary G_b3 − G′.
- **Items:** t01–t60 (`data/sg-tasks.json`; 20 domains × 3); p01–p03 pilot only.
- **Seed** (operators/hardware.md): CURBY-Q latest completed round **28297**, result pulse 2025-08-22 13:42 America/Denver (checked 2026-11-05 09:55 with `@buff-beacon-project/curby-client@1.2.0`): **CURBY-Q stalled. Seed: the first CURBy-RNG pulse timestamped after this commit.** seed = the first 8 bytes of SHA-256(randomness ‖ "sg-b5" ‖ ":" ‖ purpose), unsigned big-endian (`ledger/seed.py --purpose`), purposes `items`, `order`, `boot`. *Filled in by the seed commit, before any data:*
  `chain:` CURBy-RNG · `round:` 1592493 (previous 1592492 at 2026-11-05 10:08:00 America/Denver, before the 2026-11-05 10:08:20 America/Denver commit) · `pulse_time:` 2026-11-05 10:09:00 America/Denver · `randomness:` 58e078bb796ecdef238bb43e356d5a940e7ddd4f3857c797e60327c882c0dac121f688ac09fc890e2d1c3654087722f46644b09487db58614d6af119a8e72325 · `client:` @buff-beacon-project/curby-client@1.2.0 · `certificate_verified:` false · `seed:` items 15146642405842228603, order 7987224251921376387, boot 3177965979780855695 (`data/sg-b5-seed.json`)
- **Scale:** one direction, 0 = certainly inaccurate or unsupported, 100 = certainly accurate and fully supported.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | Opus: own-flawedL, fresh-flawedL on 60; drift on 10 | 140 | $0.53 |
| 2 | Haiku: the same | 140 | $0.011 |
| 3 | Sonnet: the same | 140 | $0.22 |
| | **total** | **420** | **about $0.76 (cap $0.85)** |

- Run order: Opus, Haiku, Sonnet (Opus first, because the pass needs it and the program cap may stop the run), cells shuffled within a model by seed `order`. Opus and one other model are enough for a pass; a run stopped before Sonnet leaves Sonnet untestable, reported as not run.
- Every call cached by content key (`results/sg-b5-grade-calls.json`). Optional review pilot: `run --pilot`, p01–p03, Haiku and Opus, cap $0.03 in code.

## 4. Statistics

- **Per study:** G′ = (fresh-clean − fresh-flawedL) − (own-clean − own-flawedL), clean cells archived; fD′ = own-flawedL − fresh-flawedL.
- **Primary statistic:** per model, mean G′ with a **95% cluster-bootstrap CI over the 20 domains** (P14; 10,000 resamples; seed `boot`); the bar is read on it. The study bootstrap is reported beside it, never used for a reading.
- **Gate (P4):** mean (fresh-clean − fresh-flawedL) ≥ 10 with cluster CI lower > 0, else untestable.
- **Guard (sg-b3 D9b, P3, kept whole, P17):** blunted needs fD′'s cluster CI (seed `boot + 4`) lower end > 0.
- **Floor (sg-b3 D9a):** sharpened needs, besides G′ ≤ −5 with CI upper < 0, fD′'s CI upper < 0 and mean fresh-flawedL ≥ 5; below 5, "same" is reported as "not blunted (sharpening not measurable at the floor)".
- **Drift check (P8):** on the 10 drift studies, own-clean − fresh-clean re-graded now minus archived; fires if |mean| ≥ 2 and its bootstrap CI over the 10 (seed `boot + 3`) excludes 0; a fired check makes the model untestable. G′ − drift is reported as `G_adj`.
- **Dumb baselines, named (P3, P16):** (a) "the fresh docking was the length breach" (fresh-flawedL graded like own-flawed: G′ ≈ 0, fail); (b) "own-turn harshness toward the clean text" (G′ > 0 with fD′ ≈ 0: the guard makes it undetermined, shown in the dry run); (c) "drift between runs" (the drift check); (d) an item property (the 14 studies whose interval excludes 0) carrying the effect. The committed dry run (`python3 experiments/sg_b5_length.py dryrun`, worlds from sg-b3's archived cells plus sg-b1's measured repeat noise, P15): blunting survives: pass 0.995; length explains it: fail 1.00; half of sg-b3's gap survives: fail 0.995 (Haiku blunted, Opus same); drift +3: untestable 0.995; item property: fail 1.00. P(pass) and P(fail) each exceed 10% under the worlds the design names (D11, P12); a value exactly on the bar lands on the passing side (P13).
- **Secondaries (reported, never promoted):** the study-bootstrap reading; G_b3 − G′ per model (how much of sg-b3's gap length matching removes) with cluster CI; G′ split by whether the study's interval excludes 0; mean grades per cell; G_adj; the length facts in §2.
- **Multiple comparisons:** three readings under the fixed rule (Opus and two of three); no other correction, and the write-up says so.
- **Robustness, committed now:** leave-one-study-out and leave-one-domain-out readings (a changed reading is reported as fragile; it stands); ties counted.

## 5. Pre-registered reading

Per model: **untestable** (usable share under 0.9, gate fails, or drift fires); **blunted** (G′ ≥ +5, cluster CI lower > 0, fD′ cluster CI lower > 0); **sharpened** (G′ ≤ −5, cluster CI upper < 0, fD′ CI upper < 0, mean fresh-flawedL ≥ 5); **same** (cluster CI strictly inside −5 to +5); **undetermined** otherwise.

Verdict:
1. **Pass**: Opus blunted, at least 2 of 3 blunted, none sharpened. Sentence: "On Haiku, Sonnet and Opus 5.5, with the overclaim replacing the conclusion's last sentence so the text was no longer than the clean one, Opus and <the other model(s)> still penalised it less on average in the conversation that wrote the conclusion than fresh (mean gap at least 5 points of 100, 95% domain-cluster CI above 0, and the flawed text itself graded higher there), and no model penalised it more: on this design, the length breach does not explain sg-b3's blunting."
2. **Fail**: Opus reads same or sharpened. Sentence (same): "On Opus 5.5, with the overclaim replacing the last sentence so the text was no longer than the clean one, the penalty was within 5 points of 100 in its own conversation and fresh (95% domain-cluster CI inside −5 to +5): on this design, Opus's blunting in sg-b3 does not survive length matching." (sharpened: "... Opus penalised it more in its own conversation (mean gap at most −5, CI below 0) ...").
3. **Mixed**: any other readable combination (for example Opus blunted alone, or Opus undetermined). Sentence: "Opus read <reading> and the others <readings> (numbers): this test gives no single answer about whether sg-b3's blunting survives length matching."
4. **Untestable**: Opus untestable, or two models. Sentence: "<Model(s)> could not be read because <the overclaim cost under 10 points fresh / fewer than 90% of studies usable / the archived clean grades drifted by 2 points or more / the cap stopped the run>, so this test cannot say whether sg-b3's blunting survives length matching."
5. **Reported in every case:** G′ with both CIs, fD′, P_fresh′, drift, G_adj, mean grades, G_b3 − G′, per model; spend; refusals.

A pass is reported as **pass, unreplicated** (one more design, one flaw wording, one family).

## 6. What it cannot do

- flawed′ replaces a sentence, usually the conclusion's caveat about how sure one can be: the edit is "a caveat replaced by an overclaim", not "an overclaim added". The claim is about that bundle.
- Four Opus texts are four sentences long, clean and flawed′ alike (over the limit in both places, but not by the flaw).
- The clean cells are from sg-b3's run; the drift check covers 10 studies per model.
- The overclaim is planted in the model's turn, not written by it; one wording, at the end.
- Three models from one family, one item set. Not "models", not "every".

## 7. Stop rules

- Budget cap in code: $0.85 for this run; $5.00 for the program. If reached, later steps are reported as not run.
- Stop on any refusal; no rewording; no retry. Any other error stops the run.
- `run` refuses to start if sg-b3's prompt strings differ from `e29f25c`, if any flawed′ is not length-matched, or if any conclusion or archived clean cell is missing or mismatched.

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "sg-b5", "program": "self-grading", "direction": "sg-d11",
 "title": "Length-matched overclaim: does a model still go easier on an exaggeration in its own conversation when it does not make the answer longer than asked?",
 "source": "literature", "engine_odds": 0.22, "engine_odds_first": 0.45,
 "odds_prior": 0.32, "odds_adjustment": -0.10, "odds_prior_commit": "73eb5cf", "odds_template": "v2",
 "human_odds": 0.55, "human_odds_at": "ho-20261105-061152-u4l",
 "prereg_commit": "<filled by the next commit>", "budget_usd": 0.85,
 "referee": "model", "bet_type": "standard", "seed_source": "curby-rng",
 "lesson": "ls-sg-b5", "prior_work_predicts": "mixed",
 "novelty": null, "novelty_line": null, "novelty_by": null, "novelty_at": null,
 "premortem_kind": "world", "verdict": "open", "date": "2026-11-05"}
```

## 9. Checklist before the first call

- [x] This file is committed on its own with its code; nothing has been run.
- [x] Lesson in §0 after reading the ledger (37 scored, Brier 0.188, 12 hits; newest audit `ng-p3-18.md`; `sg-b3.md`), `lessons.jsonl` (P1–P17) and `prior.md`; `ls-sg-b5` follows in the bet-row commit.
- [ ] Design review go (or fix-first, confirmed) before the first call; `check_prereg.py sg-b5 ... --before-run` passes.
- [x] Cockpit card before this file; human-odds read immediately before this commit.
- [x] Engine odds under v2 before this commit; human odds copied.
- [x] §0 prior work row with citations and what the bet adds (rule 13, D12).
- [x] One scale direction; budget, stop-on-refusal, frozen prompts and length matching enforced in code.
- [ ] Seed commit follows, before any data.
- [x] DEVIATIONS.md D14.
