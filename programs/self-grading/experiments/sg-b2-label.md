# sg-d2: does "this conclusion was written by you" earn a kinder grade than "written by another AI model", with the text unchanged? (pre-registration)

Written and frozen 2026-11-05 (America/Denver), in its own commit, before any call of this bet. DEVIATIONS.md D6. Budget **$1.10**, enforced in code, inside the program's $5.00 cap, which is also checked in code before every call. Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). `ledger/human-odds.jsonl` has no line for sg-d2, so this bet proceeds marked "no human odds".

## 0. The bet

| field | value |
|---|---|
| bet id | `sg-b2` |
| referee | `model` |
| bet type | `standard` |
| direction | `sg-d2` (`map/self-grading.json`; `programs/self-grading/map/program-5-map.md`) |
| source | `literature` (Chae et al. 2026, arXiv 2608.18091; Khullar et al. 2026, arXiv 2603.04582; Popov 2026, arXiv 2611.01829) |
| models | `claude-haiku-5-5`, `claude-sonnet-5-5` and `claude-opus-5-5` (rule 12). Same prompts, same 60 studies, the pass rule read per model, two of three needed. |
| engine odds, P(pass) | 13, stated 2026-11-05 04:53 in `map/odds-elicitation/v1.md` (`487642e`). Copied. Elicitation check, in the random half: paraphrase 12, negation P(not pass) 80, so the negation implies 20; spread 8. |
| human odds, P(pass) | no human odds |
| budget | $1.10 API (Haiku about $0.01, Sonnet about $0.29, Opus about $0.56; the cap is on the total) · 0 QPU s · under 1 laptop hour |
| lesson | Correcting P8, P3, P1: past own-versus-other labels changed wording and turn together, and odds once rose on a story. This bet changes one sentence only, gates on a byte-identical repeat of sg-b1's fresh call, and its odds are 13% (from 13% on the map) because om-p2-6's label effect was about a third of its position effect. |
| design review | fresh reviewer before the first call → `ledger/design-reviews/sg-b2.md`; no call before a go |
| pre-mortem | "If this fails, the most likely reason is that any label effect is real but smaller than 3 points, as in Khullar et al. (under 0.5 in 10), so most models read same or undetermined." Kind: `world`. |
| auditor | fresh session after results; plant drawn and sealed first |

## 1. In plain English

The seed question in its plainest form: if you tell a model "you wrote this", does it grade the same words more kindly? Three 2026 studies disagree.
- One found a label alone moves every judge it tested (Chae et al.).
- One found under half a point in ten on Claude models (Khullar et al.).
- One found Sonnet 5.5's label effects small, and their direction changing from document to document (Popov).

**The test.** Each model sees its own conclusion from sg-b1, in a new conversation, three times, with the words unchanged each time:
- once with the sentence "This conclusion was written by you, in an earlier conversation.";
- once with "This conclusion was written by another AI model, in an earlier conversation.";
- once with no sentence.

**A hit:** at least two of the three models grade the "you" version at least 3 points (of 100) higher than the "another AI model" version, and none grades it lower.

The "you" sentence is true for every conclusion here. The "another AI model" sentence is false.

## 2. Material

- **Models and settings:** as sg-b1 §2 (`experiments/sg_common.py` `OFF`). Grade max_tokens 40, with a floor of 1000 on Sonnet and Opus; structured output `{"grade": integer}`; default temperature.
- **Prompts:** `experiments/sg_prompts.py` `labelled(study, conclusion, label)`, which is `FRESH` with one sentence inserted before "Grade the conclusion.", from `LABELS`. The `none` arm is byte-identical to sg-b1's `fresh()`, as the dry run checks.
- **Items and the work:** sg-b1's 60 test studies (`data/sg-tasks.json`, drawn with sg-b1's beacon seed). Each model's own conclusion comes from sg-b1's write step (`results/sg-b1-write-calls.json`). Only the conclusion text is read from that file; none of sg-b1's grades enter this bet's primary statistic.
- **The gate:** it reads sg-b1's `fresh` grades (§4).
- **If sg-b1's write step does not complete for a model,** this bet is untestable on that model.
- **Scale:** one direction: 0 = certainly inaccurate or unsupported, 100 = certainly accurate and fully supported.
- **Seed** (operators/hardware.md):
  - CURBY-Q stalled (latest completed round 28297, 2025-08-22 13:42 America/Denver; checked 2026-11-05 04:40).
  - Seed: the first CURBy-RNG pulse timestamped after this commit.
  - seed = the first 8 bytes of SHA-256(randomness ‖ bet-id); sub-seeds by `ledger/seed.py --purpose`: `order` (the call order) and `boot` (the bootstrap; `boot + 1` to `boot + 3` for the secondaries and the gate).
  - *Filled in by the seed commit:* `chain:` ___ · `round:` ___ · `pulse_time:` ___ · `randomness:` ___ · `client:` ___ · `certificate_verified:` ___ · `seeds:` ___ (`data/sg-b2-seed.json`).

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| grade | each model grades its own conclusion under `self`, `other` and `none` | 3 × 180 = 540 | Haiku $0.014, Sonnet $0.29, Opus $0.56 (from sg-b1 pilot cost per grade call: $0.00008, $0.0016, $0.0031); total about $0.86, cap $1.10 |

- **Order:** shuffled by seed `order` across models, studies and arms.
- **Caching:** by key `grade|model|task|arm`.
- **Run order across bets:** this bet runs only after sg-b1's write step is complete.

## 4. Statistics

**Unit:** the study. **Primary statistic, per model:** L = the mean over usable studies of (grade_self − grade_other), with a 95% percentile bootstrap over studies (10,000 resamples, seed `boot`). A study is usable for a model when all three of its grades, and sg-b1's `fresh` grade, are integers in 0–100.

**The dumb baseline (P3) is a free noise-floor gate.** The `none` arm sends exactly sg-b1's `fresh` prompt again. D0 = the mean of (grade_none − sg-b1's grade_fresh), with a bootstrap CI (seed `boot + 3`). If D0's CI excludes 0, two identical calls disagree systematically, and that model is `untestable`. A grader whose labels change nothing has L = 0 and fails.

**What differs between `self` and `other` (P8):** only the one sentence. Its words "by you" and "by another AI model" differ by 3 words, and the sentence is in the same place. Nothing else differs; the dry run checks this byte for byte. The `other` sentence is false and the `self` sentence true. That is part of the manipulation, and §6 states it.

**Secondaries (never promoted):**
- self − none and other − none: the self-inflation and other-deflation split of Chae et al.;
- the mean grade per arm, the share higher and the share tied;
- L by study design;
- the pooled L.

**Multiple comparisons:** the fixed two-of-three rule (§5); no other correction.

**Robustness (P10):** leave-one-study-out L per model; a model whose reading flips under some single drop is reported as "fragile" beside it; the verdict is recomputed with ties excluded.

**Power (P12; D11), from the committed dry run** (`python experiments/sg_b2_label.py dryrun`), at 60 studies, three models, per-study SD of L at 3, 6 or 10. sg-b1's pilot showed per-study spreads of 0.6–3.5, so SD 3 is the most likely.

| world | P(pass) | P(fail-same) | P(fail-harsher) |
|---|---|---|---|
| null | ≤ 0.003 | 1.00 (SD 3), 0.99 (SD 6), 0.25 (SD 10) | — |
| Chae-size +6 on every model | ≥ 0.998 | — | — |
| Khullar-size +2 | 0–0.11 | 0.82 at SD 3 | — |
| Sonnet −3 only, others 0 | — | 0.08–0.52 | ≤ 0.003 |

In each world the rest of the probability is mixed. The bet can pass (a Chae-size world) and fail (a null world).

**Run order and machinery, as sg-b1 after its design review (D5):**
- the jobs run model by model (Haiku, Sonnet, Opus), with studies and arms shuffled within each model by seed `order`, so a cap stop leaves whole models;
- every model gets a reading (no data reads untestable);
- each grade stores sha256 of the conclusion, checked against sg-b1's write cache;
- the gate fires only if D0's CI excludes 0 and |D0| ≥ 1 point;
- the robustness checks (the fragile flag, ties excluded with self = other dropped, L by design, the pooled L, spend per model) are in `experiments/sg_stats.py` with fixed seeds.

## 5. Pre-registered reading

**5.1 Per model:**
- **kinder:** L ≥ +3 with the CI lower end > 0;
- **harsher:** L ≤ −3 with the CI upper end < 0;
- **same:** the whole CI lies strictly inside (−3, +3);
- **undetermined:** none of the above;
- **untestable:** fewer than 90% of 60 studies usable, or the D0 gate fires.

**5.2 Verdict:**
- **untestable:** at least two models untestable (not scored);
- **pass:** at least two models kinder and none harsher;
- **fail-harsher:** at least two harsher and none kinder;
- **fail-same:** at least two same, and none kinder or harsher;
- **mixed:** anything else.

Pass = 1; fail-harsher, fail-same and mixed = 0. A pass is reported as **pass, unreplicated**.

**5.3 The verdict sentences (P9), the only ones used afterwards:**
- **pass:** "On Haiku, Sonnet and Opus 5.5, on their own conclusions for 60 made-up studies, at least two of the three models graded the same words more kindly on average (mean difference at least 3 points of 100, 95% CI above 0) when told 'this conclusion was written by you' than when told 'written by another AI model', and none graded them more harshly. [Per-model L and CI.]"
- **fail-harsher:** "… at least two of the three models graded the same words more harshly on average (mean difference at most −3, 95% CI below 0) when told they wrote them than when told another AI model did, and none more kindly. [Per-model L and CI.]"
- **fail-same:** "… at least two of the three models graded the same words the same on average (mean difference within 3 points, 95% CI inside −3 to +3) whether told they wrote them or that another AI model did, and none was detectably kinder or harsher. [Per-model L and CI.]"
- **mixed:** "… the three models did not agree [per-model readings], so this test gives no overall answer about the label."
- **untestable:** "… the test could not be read on at least two models [which, and why]."

**5.4 Reported in every case:**
- per model: n usable; L with its CI; self − none and other − none with CIs; D0 with its CI; the mean per arm; the leave-one-out range;
- spend per model.

## 6. What it cannot do

- It labels the model's **own** text only. Whether the label acts the same way on text the model did not write is sg-d4.
- It cannot separate "about me" from "about pleasing the person in the conversation". That is sg-d7.
- **One wording of each label.** "Another AI model" is unnamed; a named rival (Popov's filenames) may act differently.
- **The "other" label is false.** A model that recognises its own text, and so "knows" the label is false, would be reacting to that conflict too. Self-recognition is at chance for Claude-class models (SAD), but that was not measured on these models.
- It speaks only of a fresh conversation, not of grading inside the conversation that wrote the text (sg-b1).
- **No "every" or "all models".**

## 7. Stop rules

- Budget cap in code: $1.10 for this bet, plus the program cap of $5.00.
- Stop on any refusal; no rewording, no retry.
- Any other API error stops the run; it resumes from the cache only after the cause is written in DEVIATIONS.

## 8. Ledger entry

```json
{"id": "sg-b2", "program": "self-grading", "direction": "sg-d2",
 "title": "Does 'written by you' earn a kinder grade than 'written by another AI model', text unchanged?", "source": "literature",
 "engine_odds": 0.13, "engine_odds_at": "2026-11-05T04:53:41-07:00", "human_odds": null, "human_odds_note": "no human odds",
 "prereg_commit": "<this commit>", "budget_usd": 1.10, "referee": "model", "bet_type": "standard", "seed_source": "curby-rng",
 "lesson": "ls-sg-b2", "premortem_kind": "world", "verdict": "open"}
```

## 9. Checklist before the first call

- [x] This file is committed on its own; no call of this bet has been made.
- [x] The lesson was written after reading bets.jsonl, brier.md (19 scored, Brier 0.259, running base rate 0.43), the audits (newest ng-p3-5c.md; om-p2-6.md for the label-versus-position split) and lessons.jsonl.
- [ ] The design review says go before the first call; `check_prereg.py --before-run` passes.
- [x] Engine odds are on record with an earlier time; no human odds.
- [x] §5 can be applied by a stranger (the dry run applies it).
- [x] The pre-mortem is one sentence, with its kind.
- [x] One scale direction.
- [x] The seed rule is stated; the seed commit follows.
- [x] Budget and stop-on-refusal are in code.
- [x] DEVIATIONS D6 is added.
