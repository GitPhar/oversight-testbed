# sg-d14, lead-in only: does the closing line "Now grade the conclusion above" carry part of what sg-b4 left between its quoted copy and a fresh grade? (pre-registration, bet sg-b7)

Written and frozen 2026-11-05 (America/Denver; the time is this commit's author time), in its own commit, before any call. DEVIATIONS.md D21. Budget **$0.75**, enforced in code (`CAP` in `experiments/sg_b7_leadin.py`), inside program 5's **$7.65** cap, also in code (`sg_common.PROGRAM_CAP_USD`, raised by budget ruling br-016, D19). Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision. His odds come only from `ledger/human-odds.jsonl`. A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit.

> **Cockpit first.** sg-d14's card is in `map/cockpit-cards.jsonl` (posted by the remap session 2026-11-05b, no engine odds, at `4bddc82`), committed before this file. `python3 ledger/pickup_human_odds.py` ran immediately before this commit, and `python3 ledger/human_odds_match.py self-grading sg-d14` printed Sean's line (committed at `a8a5c43`).

## 0. The bet

| field | value |
|---|---|
| bet id | `sg-b7` |
| referee | `model` |
| bet type | `standard` |
| direction | `sg-d14` (`map/self-grading.json`; parent sg-d12, from bet sg-b4) |
| source | `literature` (sg-b4's audit, "What would break it next", second arm; the remainder its cut 1 names) |
| engine odds, P(pass) | **14** (template v2, rule 14: prior 0.26 from `ledger/prior.md` at `078e0bc`, adjustment −0.12, reason: "Rows under $1 (0.17), literature (0.18) and layer 4 (0/3) sit below 0.26; self-grading (0.40) is outweighed. Both models must pass, and Opus's 0.75 threshold on 30 studies is small."), elicited 2026-11-05 between `f5c837b` (11:32) and 11:33 in a fresh context holding only prior.md and this bet's description. The map stated no odds for sg-d14 (remap 2026-11-05b). |
| human odds, P(pass) | **50**, `ho-20261105-112945-mjj` (recorded 2026-11-05 11:29:45 on the cockpit, "would spend", committed at `a8a5c43` before this file). His card's event is the event scored here, word for word (§5). |
| models | `claude-haiku-5-5`, `claude-sonnet-5-5`, `claude-opus-5-5` (rule 12). Scored on Haiku and Opus (the two models sg-b4 left a remainder on, as on the map and the card). Sonnet is run and reported, not scored: it left no remainder to split (sg-b4's L +0.17); the map left it out, and it is added here under rule 12. Haiku on all 60 studies; Sonnet and Opus on sg-b4's 30 studies; every cell once (Opus calls cost about 45 times Haiku's). |
| budget | $0.75 API (expected about $0.59: Haiku 240 calls about $0.02, Opus 120 about $0.38, Sonnet 120 about $0.19, at sg-b4's cost per call) · 0 QPU s · 0 laptop hours |
| prior work | **Mixed; no lead-in-only test in print.** JudgeSense (Bellibatlu, Raff and Zhang 2026, arXiv 2604.23478 v3): rewording a judge's instruction while keeping its question moves graded verdicts beyond repeat noise (pooled coherence −0.181), direction unstated, which predicts S ≠ 0 of unknown sign. Grossmann and Kross 2014 (Psychological Science 25:1571; adults): a third-person, distancing wording shrank a human self-other gap in reasoning, which predicts that the deictic "Now grade the conclusion above" keeps part of the own-turn frame (S > 0). Khullar, Hopkins, Wang and Roger 2026 (arXiv 2603.04582; Claude 3.5 Haiku, Sonnet 4, Opus 4.1): explicit authorship wording moves leniency by 0.5 of 10 or less, which predicts a small S. Chen et al. 2026 (arXiv 2606.05976 v2; Qwen2.5-72B, math): a label-free boundary carried part of the gain from moving a claim out of the model's own turn and the role tag the rest, which predicts that structure, not one line, carries most of it. Read in `map/reads/remap-2026-11-05b-sg-b4.md`. What this bet adds: the first split of sg-b4's remainder that changes one line only, on the 5.5 models, with both lead-ins graded in one run. The engine's 14 sits below a mixed prior because both Haiku and Opus must clear their bars, and Opus's 0.75 bar sits on a 1.5-point remainder over 30 studies (the dry run: Opus passes under half the time even if the lead-in carries all of it). |
| lesson | "Correcting P8, P12: sg-b4's remainder bundles three differences, and Opus's 0.75 bar on 30 studies is thin. This bet swaps only the closing line, grades both versions in one run, and its dry run shows Opus passing under half the time even if the lead-in carries all; its odds are 14% (map: none) because under-$1, literature and layer-4 rows run low." |
| design review | before the first call, a fresh reviewer dry-runs this design (operators/design-review.md, D1–D12) → `ledger/design-reviews/sg-b7.md`. No call runs before a go. |
| pre-mortem | "If this fails, the most likely reason is that Opus's S on 30 studies lands between 0 and 0.75 or its cluster interval reaches below 0: a 1.5-point remainder is too small to split at this n." Kind: `design`. |
| auditor | fresh session per operators/auditor.md, after results, in a stripped clone |

## 1. In plain English

sg-b4 showed each model its writing conversation again as a quoted copy, ending with the same closing line as in its own conversation, "Now grade the conclusion above". There both Haiku and Opus were stricter about a planted exaggeration than in their own reply, but still a little less strict than when they saw the same words in sg-b3's fresh frame (by 5.8 and 1.5 points of 100). Three things separate the quoted copy from the fresh frame: a header sentence, the User/Assistant labels, and that closing line. This test changes only the closing line, to the fresh frame's plain "Grade the conclusion.", and grades both versions in one sitting. If both models get clearly stricter, by at least half of what was left, the closing line carries part of the remainder; if not, the header or the labels must. The published work points both ways: wording changes move LLM judges (JudgeSense 2026) and a distancing wording shrinks a human self-other gap (Grossmann and Kross 2014), but explicit wording moved Claude monitors little (Khullar et al. 2026).

## 2. Material

- **Models:** `claude-haiku-5-5` (thinking disabled), `claude-sonnet-5-5` (thinking "between_tools"), `claude-opus-5-5` (effort low), as `sg_common.OFF`; structured output `{"grade": integer}`, max_tokens 40 (raised to each model's minimum); default temperature. Same settings as sg-b3 and sg-b4.
- **Texts:** each model's own conclusion for each study from sg-b1's write cache, clean, and with sg-b3's overclaim appended (`sg_b3_flaw.flawed`, unchanged). Each grade record stores sha256(conclusion) and sha256(messages); `analyse` refuses any record whose conclusion or prompt differs from what the frozen code builds.
- **Cells (all graded in this run; nothing archived enters a statistic):**
  - `quoted-clean`, `quoted-flawed`: sg-b4's quoted copy (`sg_prompts.quoted`; QUOTED as frozen at 65f6f93), ending "Now grade the conclusion above. <GRADE_Q>".
  - `plain-clean`, `plain-flawed`: the same message with only that ending replaced by the fresh frame's "Grade the conclusion. <GRADE_Q>" (`sg_prompts.QUOTED_PLAIN = QUOTED[:-len(GRADE_ABOVE)] + PLAIN_LEAD`, `PLAIN_LEAD = "Grade the conclusion. " + GRADE_Q`). The header sentence ("Here is a conversation between a user and an AI assistant.") and the User/Assistant blocks stay.
  - `run` refuses to start unless sg-b3's strings equal their text at e29f25c, QUOTED equals its text at 65f6f93, WRITE, GRADE_ABOVE, QUOTED, QUOTED_PLAIN and OVERCLAIM match the sha256 values in `sg_b7_leadin.FROZEN`, and the plain message equals the quoted message with GRADE_ABOVE replaced by PLAIN_LEAD (and differs from it).
- **Items:** the 60 test studies t01–t60 (20 domains × 3). Haiku: all 60. Sonnet and Opus: sg-b4's 30 studies (`results/sg-b4-analysis.json`, `study_sets`; the same list as sg-b6's §2), because the bars are halves of sg-b4's L on exactly those studies. No study is drawn here.
- **Seed** (operators/hardware.md): CURBY-Q latest completed round **28297**, result pulse 2025-08-22 13:42 America/Denver (checked 2026-11-05 11:28 with `@buff-beacon-project/curby-client@1.2.0`): more than 24 hours old, so **CURBY-Q stalled. Seed: the first CURBy-RNG pulse timestamped after this commit.** seed = the first 8 bytes of SHA-256(randomness ‖ "sg-b7" ‖ ":" ‖ purpose), unsigned big-endian (`ledger/seed.py --purpose`), purposes `order` and `boot`. *Filled in by the seed commit, before any data:*
  `chain:` ___ · `round:` ___ · `pulse_time:` ___ · `randomness:` ___ · `client:` ___ · `certificate_verified:` ___ · `seed:` ___
- **Scale:** one direction, 0 = certainly inaccurate or unsupported, 100 = certainly accurate and fully supported.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | Haiku: 4 cells × 60 studies | 240 | $0.018 |
| 2 | Opus: 4 cells × 30 studies | 120 | $0.38 |
| 3 | Sonnet: 4 cells × 30 studies | 120 | $0.19 |
| | **total** | **480** | **about $0.59 (cap $0.75)** |

- Run order: model by model (Haiku, Opus, Sonnet), calls shuffled within a model by seed `order`, so a cap stop leaves whole models. Steps 1 and 2 are enough for the verdict.
- Every call is cached by a content key (`results/sg-b7-grade-calls.json`); a crash never pays twice.
- No pilot: the plain cell is sg-b4's quoted cell with sg-b3's fresh lead-in, both already run without refusal or parse failure.

## 4. Statistics

- **Per study** (model m): p = plain-clean − plain-flawed; q = quoted-clean − quoted-flawed; **S = p − q**; F = quoted-flawed − plain-flawed.
- **Primary statistic:** per model, mean S over usable studies, with a **95% cluster-bootstrap CI over the 20 domains** (P14; 10,000 resamples; seed `boot`). The study bootstrap is reported beside it, never used for a reading.
- **The bar B:** half of the model's sg-b4 L: Haiku 2.9 (L 5.77), Opus 0.75 (L 1.50), as on the map and on Sean's card.
- **Gate (P4):** mean q ≥ 10 with cluster CI (seed `boot + 2`) lower > 0, else the model is untestable.
- **Guard (P3, P17):** F's cluster CI (seed `boot + 1`) lower end > 0: the flawed text itself must score lower with "Grade the conclusion." than with "Now grade the conclusion above.", so a plain lead-in that is merely kinder to clean text cannot pose as the lead-in carrying the gap.
- **Usable:** every cell present, an integer 0–100; share out of the model's planned studies.
- **Dumb baselines, named (P3, P16):** (a) "the closing line does nothing" (plain = quoted, S = 0); (b) "the closing line carries all of L" (plain = sg-b3's fresh cells); (c) "the plain lead-in is only kinder to clean text" (guard); (d) "an item property": the plain lead-in acts like fresh only on the 14 studies whose interval excludes 0 (P16); (e) "a flaw-blind grader" (gate). The committed dry run (`experiments/sg_b7_leadin.py dryrun`: worlds from sg-b4's quoted and sg-b3's fresh archived cells plus sg-b1's measured repeat noise, P15), 200 draws: does nothing: fail 0.255, mixed 0.745 (Haiku reads not the lead-in in every draw; Opus undetermined in 148); carries all of L: pass 0.435, mixed 0.565 (Haiku carries part in every draw; Opus in 87); S exactly at each bar: pass 0.085, mixed 0.91, fail 0.005; kinder to clean only: mixed 1.00; item property: mixed 0.97, fail 0.03. P(pass) and P(fail) are each above 10% in the worlds the design names (D11, P12): pass 0.435 where the hypothesis holds, fail 0.255 where it does not. Opus is the binding conjunct, and the odds say so. A value exactly on the bar lands on the passing side (P13; the dry run checks S = 2.9 exactly).
- **Secondary statistics (reported, never promoted):** Sonnet's S; the reading on the study bootstrap; S as a share of sg-b4's L; the clean-text shift (plain-clean − quoted-clean); today's quoted penalty minus sg-b4's on the same studies (a cross-run check of the quoted cell, with cluster CI); mean grades per cell.
- **Multiple comparisons:** two scored readings combined by a conjunction (both must pass); no other correction.
- **Robustness, committed now:** leave-one-study-out and leave-one-domain-out readings (fragile is reported and stands); ties (S = 0) with the mean excluding them; the median and 10% trimmed mean.

## 5. Pre-registered reading

Per model (Haiku, Opus):
- **untestable** if the usable share is under 0.9 or the gate fails;
- **lead-in carries part** if mean S ≥ B, S's cluster CI lower end > 0, and F's cluster CI lower end > 0;
- **not the lead-in** if S's cluster CI upper end < B;
- **undetermined** otherwise.

Verdict:
1. **Pass**: both read lead-in carries part. Sentence: "On Haiku and Opus 5.5, replacing only the quoted copy's closing line 'Now grade the conclusion above.' with 'Grade the conclusion.' made each dock the planted overclaim more on average, by at least half of what sg-b4 left between the quoted copy and the fresh frame (Haiku at least 2.9 points of 100, Opus at least 0.75, 95% domain-cluster CI above 0), and the flawed text itself was graded lower: on this design, the closing line carries part of sg-b4's remainder."
2. **Fail**: both read not the lead-in. Sentence: "On Haiku and Opus 5.5, swapping the closing line changed the penalty by less than half of sg-b4's remainder (the 95% domain-cluster CI lies below Haiku 2.9 and Opus 0.75 points of 100): on this design, the closing line does not carry most of the remainder; the header sentence or the User/Assistant labels must."
3. **Mixed**: any other combination of two readable models. Sentence: "Haiku read <reading> and Opus read <reading> (numbers): this test gives no single answer about whether the closing line carries sg-b4's remainder."
4. **Untestable**: Haiku or Opus untestable. Sentence: "<Model> could not be read because <the quoted copy docked the overclaim by less than 10 points / fewer than 90% of its studies were usable>, so this test cannot say whether the closing line carries sg-b4's remainder."
5. **Reported in every case:** S, its cluster and study CIs, F, p, q per model including Sonnet; spend; refusals (none expected).

A pass is reported as **pass, unreplicated** (invariant 7).

## 6. What it cannot do

- It splits the remainder only between the closing line and everything else; the header sentence and the labels are not separated from each other.
- The swap also changes "above" (a pointer back to the text) and "Now" (a cue of continuing): the claim is about that one line, not about either word.
- The comparison is with sg-b4's L as a bar; the L itself was measured across runs (sg-b4's quoted cells against sg-b3's fresh cells). The plain cell is never compared with sg-b3's fresh cell here.
- Opus and Sonnet on 30 studies; Opus's remainder is small (1.5 points), so this test can miss a real share on Opus (the dry run says so).
- The overclaim was planted, one wording, appended at the end. Three models from one family, one item set. Not "models", not "every".

## 7. Stop rules

- Budget cap in code: $0.75 for this run; $7.65 for the program. If reached, later steps are reported as not run.
- Stop on any refusal; no rewording; no retry. Any other error also stops the run.
- `run` refuses to start if any frozen prompt differs (§2), or if any conclusion is missing.

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "sg-b7", "program": "self-grading", "direction": "sg-d14",
 "title": "Lead-in only: does the closing line 'Now grade the conclusion above' carry part of what sg-b4 left between its quoted copy and a fresh grade?",
 "source": "literature", "engine_odds": 0.14, "engine_odds_first": null,
 "odds_prior": 0.26, "odds_adjustment": -0.12, "odds_prior_commit": "078e0bc", "odds_template": "v2",
 "human_odds": 0.50, "human_odds_at": "ho-20261105-112945-mjj",
 "prereg_commit": "<filled by the next commit>", "budget_usd": 0.75,
 "referee": "model", "bet_type": "standard", "seed_source": "curby-rng",
 "lesson": "ls-sg-b7", "prior_work_predicts": "mixed",
 "novelty": null, "novelty_line": null, "novelty_by": null, "novelty_at": null,
 "premortem_kind": "design", "verdict": "open", "date": "2026-11-05"}
```

## 9. Checklist before the first call

- [x] This file is committed on its own with its code; nothing has been run.
- [x] Lesson in §0 after reading `ledger/bets.jsonl` (74 rows), `brier.md` (35 scored, Brier 0.164, 9 hits), `audits/` (newest `ss-b10c.md`; and `sg-b4.md`, `sg-b5.md`), `lessons.jsonl` (P1–P17) and `prior.md`; `ls-sg-b7` follows in the bet-row commit.
- [ ] Design review go (or fix-first, confirmed) before the first call; `python3 ledger/check_prereg.py sg-b7 . programs/self-grading/experiments/sg-b7-leadin.md --before-run` passes.
- [x] Cockpit card committed before this file; human odds read immediately before this commit.
- [x] Engine odds elicited under v2 before this commit; human odds copied from `ledger/human-odds.jsonl`.
- [x] §0 prior work row: predicted outcome with citations; what the bet adds (rule 13, D12).
- [x] One scale direction; budget, stop-on-refusal and frozen prompts enforced in code.
- [ ] Seed commit follows this one, before any data.
- [x] DEVIATIONS.md D21.
