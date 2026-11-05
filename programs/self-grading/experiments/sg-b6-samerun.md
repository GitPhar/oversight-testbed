# sg-d13, same-run re-grade: does sg-b4's turn-role reading hold when the own-reply and quoted-copy grades come from one run? (pre-registration, bet sg-b6)

Written and frozen 2026-11-05 (America/Denver; the time is this commit's author time), in its own commit, before any call. DEVIATIONS.md D20. Budget **$0.80**, enforced in code (`CAP` in `experiments/sg_b6_samerun.py`), inside program 5's **$7.65** cap, also in code (`sg_common.PROGRAM_CAP_USD`, raised from $5.00 by budget ruling br-016, D19; $4.69 spent). Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision. His odds come only from `ledger/human-odds.jsonl`. A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit.

> **Cockpit first.** sg-d13's card is in `map/cockpit-cards.jsonl` (posted by the remap session 2026-11-05b, no engine odds, at `4bddc82`), committed before this file. `python3 ledger/pickup_human_odds.py` ran immediately before this commit; it brought in Sean's line for this direction (committed at `a8a5c43`), and `python3 ledger/human_odds_match.py self-grading sg-d13` printed it.

## 0. The bet

| field | value |
|---|---|
| bet id | `sg-b6` |
| referee | `model` |
| bet type | `standard` |
| direction | `sg-d13` (`map/self-grading.json`; parent sg-d12, from bet sg-b4) |
| source | `literature` (sg-b4's audit, "What would break it next", the cheapest overturning test) |
| engine odds, P(pass) | **16** (template v2, rule 14: prior 0.26 from `ledger/prior.md` at `078e0bc`, adjustment −0.10, reason: "Rows under $1 (0.17), literature (0.18), model (0.22), layer 4 (0/3) sit below the prior; parent's 6.8 barely clears bar 6.3, median 5.5, plus conjunctive F and gate."), elicited 2026-11-05 between `f5c837b` (11:32) and 11:33 in a fresh context holding only prior.md and this bet's description. The map stated no odds for sg-d13 (remap 2026-11-05b, `engine_odds` null), so there is no earlier number. |
| human odds, P(pass) | **55**, `ho-20261105-112945-5te` (recorded 2026-11-05 11:29:45 on the cockpit, "would spend", committed at `a8a5c43` before this file). His card's event is the event scored here, word for word (§5, Haiku). His card priced the test at about $0.04 (Haiku only); this run adds Sonnet and Opus (rule 12), reported, not scored, so the scored event does not change. |
| models | `claude-haiku-5-5`, `claude-sonnet-5-5`, `claude-opus-5-5` (rule 12). **Scored on Haiku** (the map's and the card's event: the question is Haiku's cross-run margin, sg-b4's weakest link). Opus is read by the same rule at its own bar (3.0) and Sonnet's T is reported: both are the replication sg-b4's Opus and Sonnet numbers owe on a same-run comparison, never promoted to the verdict. Haiku on all 60 studies, every cell twice; Sonnet and Opus on sg-b4's 30 studies, every cell once (Opus calls cost about 45 times Haiku's). |
| budget | $0.80 API (expected about $0.64: Haiku 480 calls about $0.04, Sonnet 120 about $0.19, Opus 120 about $0.41, at the cost per call in sg-b3's and sg-b4's caches) · 0 QPU s · 0 laptop hours |
| prior work | **Predicts T > 0; silent on the 6.3 bar and on cross-run noise as its cause.** Tsui 2025, Self-Correction Bench (arXiv 2507.02778 v3; Claude 3.5 Haiku 52.5%, Sonnet 4 41.4% blind spot) and Khullar, Hopkins, Wang and Roger 2026, Self-Attribution Bias (arXiv 2603.04582; Claude 3.5 Haiku, Sonnet 4, Opus 4.1): text in the model's own assistant turn is let off more than the same text in a user turn, which predicts a positive T in any run. On the noise that this test removes: JudgeSense (Bellibatlu, Raff and Zhang 2026, arXiv 2604.23478 v3) finds LLM judges disagree with themselves on identical prompts, most on graded tasks (Claude Haiku 4.5 coherence −0.206 against its own repeats), and Zhao, Esmaeili and Fard 2026 (arXiv 2604.16790) report two-run consistency of 70–90%; both predict noise of unknown sign, not a direction (`map/reads/remap-2026-11-05b-sg-b4.md`). No paper tests whether a quoted copy's leniency gap survives a same-run comparison. What this bet adds: sg-b4's comparison with every cell graded in one run, Haiku twice, on the 5.5 models, which removes the cross-run confound its audit named. The engine's 16 sits below the papers' direction because the rule needs Haiku's mean to clear a bar its sg-b4 median (5.5) did not. |
| lesson | "Correcting P8, P10: sg-b4 compared quoted grades with own-turn grades from an earlier run, and Haiku's pass rested on a half-point margin and one domain. This bet grades all four cells in one run, Haiku twice each, and reports median and domain drops, and its odds are 16% (map: none) because under-$1, literature and layer-4 rows run low." |
| design review | before the first call, a fresh reviewer dry-runs this design (operators/design-review.md, D1–D12) → `ledger/design-reviews/sg-b6.md`. No call runs before a go. |
| pre-mortem | "If this fails, the most likely reason is that same-run own-turn penalties come out larger than sg-b3's archived ones, shrinking Haiku's T to between 0 and 6.3: sg-b4's half-point margin was cross-run luck." Kind: `world`. |
| auditor | fresh session per operators/auditor.md, after results, in a stripped clone |

## 1. In plain English

sg-b4 showed Haiku its own writing conversation as a quoted copy and found it docked a planted exaggeration 6.8 points (of 100) more there than in its own reply. The bar was 6.3. But the own-reply grades it was compared with came from sg-b3's run an hour earlier, and when 10 of them were re-graded they had moved by about 4 points. So the half-point margin could be run-to-run noise. This test grades all four versions (own reply and quoted copy, clean and with the exaggeration) in one sitting, each twice on Haiku, and compares them only with each other. If Haiku is still stricter in the quoted copy by at least 6.3 points, sg-b4's pass holds without the cross-run comparison; if not, sg-b4's Haiku half reads mixed or layout. The published work (Tsui 2025; Khullar et al. 2026) predicts that Haiku is stricter in the quoted copy, but says nothing about how much. Sonnet and Opus run once each on 30 studies and are reported, so sg-b4's Opus reading also gets a same-run check.

## 2. Material

- **Models:** `claude-haiku-5-5` (thinking disabled), `claude-sonnet-5-5` (thinking "between_tools"), `claude-opus-5-5` (effort low; it cannot disable thinking), as `sg_common.OFF`; structured output `{"grade": integer}`, max_tokens 40 (raised to each model's minimum in `sg_common.MIN_TOKENS`); default temperature. Same settings as sg-b3 and sg-b4.
- **Texts:** each model's own conclusion for each study from sg-b1's write cache (`results/sg-b1-write-calls.json`), clean, and with sg-b3's overclaim appended (`sg_b3_flaw.flawed`, unchanged). Each grade record stores sha256(conclusion) and sha256(messages); `analyse` refuses any record whose conclusion or prompt differs from what the frozen code builds.
- **Cells (all graded in this run; nothing archived enters a statistic):**
  - `own-clean`, `own-flawed`: sg-b3's own-turn conversation (`sg_prompts.own_turn`: the WRITE request, the conclusion in the model's own assistant turn, then "Now grade the conclusion above. <GRADE_Q>").
  - `quoted-clean`, `quoted-flawed`: sg-b4's quoted copy (`sg_prompts.quoted`, one user message, QUOTED as frozen at 65f6f93).
  - `run` refuses to start unless sg-b3's strings equal their text at e29f25c, QUOTED equals its text at 65f6f93, and WRITE, GRADE_ABOVE, QUOTED and OVERCLAIM match the sha256 values in `sg_b6_samerun.FROZEN`.
- **Items:** the 60 test studies t01–t60 (`data/sg-tasks.json`; 20 domains × 3). Haiku: all 60. Sonnet and Opus: sg-b4's 30 studies (read from `results/sg-b4-analysis.json`, `study_sets`): t01, t02, t03, t04, t06, t07, t08, t10, t13, t15, t23, t25, t27, t29, t30, t34, t35, t38, t40, t44, t45, t46, t47, t49, t51, t54, t56, t57, t59, t60. Pilot studies p01–p03 are not used. No study is drawn here, so the seed has no `items` purpose.
- **Repeats:** Haiku grades every cell twice (r1, r2); a study's cell grade is the mean of the two. Sonnet and Opus once.
- **Seed** (operators/hardware.md): CURBY-Q latest completed round **28297**, result pulse 2025-08-22 13:42 America/Denver (checked 2026-11-05 11:28 with `@buff-beacon-project/curby-client@1.2.0`): more than 24 hours old, so **CURBY-Q stalled. Seed: the first CURBy-RNG pulse timestamped after this commit.** seed = the first 8 bytes of SHA-256(randomness ‖ "sg-b6" ‖ ":" ‖ purpose), unsigned big-endian (`ledger/seed.py --purpose`), purposes `order` (the shuffle of calls within a model) and `boot` (bootstrap seeds). *Filled in by the seed commit, before any data:*
  `chain:` CURBy-RNG · `round:` 1592585 (previous 1592584 at 2026-11-05 11:40:00 America/Denver, before the 2026-11-05 11:40:35 America/Denver commit) · `pulse_time:` 2026-11-05 11:41:00 America/Denver · `randomness:` a9d305bd824624178e3a50dd3444cdb391d93f081e0b7478741381ea3c4ee0d3c3508839a9692e6a9d5021a27a2ec19fb575ea78f0a244b4ae0584098c317c66 · `client:` @buff-beacon-project/curby-client@1.2.0 · `certificate_verified:` false · `seed:` order 15078222124198125769, boot 12959117145896730554 (`data/sg-b6-seed.json`)
- **Scale:** one direction, 0 = certainly inaccurate or unsupported, 100 = certainly accurate and fully supported (`sg_common.SCALE`).

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | Haiku: 4 cells × 60 studies × 2 repeats | 480 | $0.036 |
| 2 | Opus: 4 cells × 30 studies | 120 | $0.41 |
| 3 | Sonnet: 4 cells × 30 studies | 120 | $0.19 |
| | **total** | **720** | **about $0.64 (cap $0.80)** |

- Run order: model by model (Haiku, Opus, Sonnet), calls shuffled within a model by seed `order`, so a cap stop leaves whole models. Step 1 alone is enough for the scored verdict.
- Every call is cached by a content key (`results/sg-b6-grade-calls.json`, key `grade|<model>|<study>|<cell>|r<k>`); a crash never pays twice.
- No pilot: the prompts are sg-b3's and sg-b4's, which ran 1,020 calls with no refusal and no parse failure.

## 4. Statistics

- **Per study** (model m; each cell's grade is the mean over its repeats): q = quoted-clean − quoted-flawed; o = own-clean − own-flawed; **T = q − o**; F = own-flawed − quoted-flawed.
- **Primary statistic:** Haiku's mean T over usable studies, with a **95% cluster-bootstrap CI over the 20 domains** (P14; 10,000 resamples; seed `boot`). The bar is read on this interval. The study bootstrap is reported beside it and never used for a reading.
- **The bar H:** Haiku 6.3 (half of sg-b3's G 12.58), as in sg-b4 and on Sean's card. Opus (reported): 3.0 (half of 5.97).
- **Gate (the manipulation takes effect, P4):** mean q ≥ 10 with cluster CI (seed `boot + 2`) lower > 0, else the model is untestable.
- **Guard (P3, sg-b3's D9b, sg-b4's F):** F's cluster CI (seed `boot + 1`) lower end > 0: the flawed text itself must score lower in the quoted copy than in the own turn, so a quoted copy that is merely kinder to the clean text cannot pose as role.
- **Usable:** a study is usable for a model if every cell has every repeat, each an integer 0–100; the usable share is out of the model's planned studies.
- **Dumb baselines, named (P3):** (a) "the quoted copy is graded like the own turn" (T = 0, reads layout); (b) "sg-b4 as run": own = sg-b3's archived cells, quoted = sg-b4's archived cells, i.e. the cross-run result itself (reads turn role on Haiku); (c) "the quoted copy is only kinder to clean text" (the guard rejects it); (d) "a flaw-blind grader" (the gate fires). The committed dry run (`experiments/sg_b6_samerun.py dryrun`: worlds from sg-b3's and sg-b4's archived per-study cells plus sg-b1's measured repeat noise, P15) gives, on Haiku's verdict over 200 draws: as sg-b4: pass 1.00; sg-b4 with sg-b4's measured −4.3 drift in today's own-turn penalty: pass 1.00; layout (quoted = own): fail 1.00; T exactly at the bar: pass 0.185, mixed 0.695, fail 0.12; regression (sg-b4's T less 3 points): fail 1.00; kinder-to-clean only: mixed 0.985, pass 0.015. P(pass) and P(fail) are each above 10% under the worlds the design names (D11, P12). A value exactly on the bar lands on the passing side (P13, tolerance 1e-9 in `sg_followups`; the dry run checks T = 6.3 exactly).
- **Secondary statistics (reported, never promoted):** Opus's reading at 3.0 and Sonnet's T, each with both CIs; the reading on the study bootstrap; T on each repeat alone (r1, r2), the share of Haiku's grades identical across repeats and the SD of r2 − r1 (same-run noise); the clean-text shift (quoted-clean − own-clean); against the archives on the same studies: sg-b4's cross-run T, today's own-turn penalty minus sg-b3's (with cluster CI), and today's quoted penalty minus sg-b4's; mean grades per cell.
- **Multiple comparisons:** one scored reading (Haiku), with a guard and a gate as conjunctions; no correction. Opus and Sonnet are reported and say nothing about the verdict.
- **Robustness, committed now:** leave-one-study-out and leave-one-domain-out readings (a reading that changes is reported as fragile beside the model's numbers; it stands); ties (T = 0) counted, with the mean excluding them; the median and the 10% trimmed mean (sg-b4's audit asked for both).

## 5. Pre-registered reading

Per model (Haiku scored; Opus read the same way at 3.0, reported):
- **untestable** if the usable share is under 0.9 or the gate fails;
- **turn role** if mean T ≥ H, T's cluster CI lower end > 0, and F's cluster CI lower end > 0;
- **layout** if T's cluster CI upper end < H;
- **undetermined** otherwise.

Verdict (Haiku's reading):
1. **Pass** (turn role). Sentence: "On Haiku 5.5, with every grade taken in one run, its own conversation shown as a quoted copy took away at least half of the blunting it showed in sg-b3 on average (by at least 6.3 points of 100, 95% domain-cluster CI above 0), and the flawed text itself was graded lower in the quoted copy than in its own turn: sg-b4's Haiku reading holds without the cross-run comparison."
2. **Fail** (layout). Sentence: "On Haiku 5.5, with every grade taken in one run, the quoted copy took away less than half of its sg-b3 blunting (the 95% domain-cluster CI of the change lies below 6.3 points of 100): sg-b4's Haiku reading did not hold on a same-run comparison, so sg-b4's pass rested on grades from two runs."
3. **Mixed** (undetermined). Sentence: "On Haiku 5.5, with every grade taken in one run, the change was <T> points [CI], which neither clears the 6.3 bar with the guard met nor lies wholly below it: this test cannot say whether sg-b4's Haiku reading holds on a same-run comparison."
4. **Untestable.** Sentence: "Haiku could not be read because <the quoted copy docked the overclaim by less than 10 points / fewer than 90% of its studies were usable>, so this test cannot say whether sg-b4's Haiku reading holds."
5. **Reported in every case:** T, its cluster and study CIs, F, q, o per model; Opus's reading and Sonnet's T; the repeat secondaries; the cross-run secondaries; spend; refusals (none expected).

A pass is reported as **pass, unreplicated** (invariant 7): it repeats sg-b4's design on one model in a new run; it is not a second design.

What a pass or fail does to sg-b4: nothing to its ledger row (its verdict was read on its own rule and audited). The results file and map say in plain words whether sg-b4's Haiku half held on a same-run comparison.

## 6. What it cannot do

- It removes the cross-run confound only. The quoted copy still differs from the own turn in role, message count (1 against 3), the header sentence, the triple-quoted blocks and the grade question sharing the message (sg-b4 D16): a pass is about that bundle, as sg-b4's was.
- Two repeats on Haiku and one on Sonnet and Opus: the repeat noise of Sonnet and Opus is not measured here.
- Opus and Sonnet on 30 studies; their readings are reported, not scored.
- The overclaim was planted in the model's turn, not written by it; one flaw wording, appended at the end.
- Three models from one family, one item set. Not "models", not "every".

## 7. Stop rules

- Budget cap in code: $0.80 for this run; $7.65 for the program. If reached, later steps are reported as not run.
- Stop on any refusal; no rewording; no retry. Any other error also stops the run.
- `run` refuses to start if any frozen prompt differs (§2), or if any conclusion is missing from sg-b1's write cache.

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "sg-b6", "program": "self-grading", "direction": "sg-d13",
 "title": "Same-run re-grade: does sg-b4's turn-role reading on Haiku hold when the own-turn and quoted-copy grades come from one run?",
 "source": "literature", "engine_odds": 0.16, "engine_odds_first": null,
 "odds_prior": 0.26, "odds_adjustment": -0.10, "odds_prior_commit": "078e0bc", "odds_template": "v2",
 "human_odds": 0.55, "human_odds_at": "ho-20261105-112945-5te",
 "prereg_commit": "<filled by the next commit>", "budget_usd": 0.80,
 "referee": "model", "bet_type": "standard", "seed_source": "curby-rng",
 "lesson": "ls-sg-b6", "prior_work_predicts": "unknown",
 "novelty": null, "novelty_line": null, "novelty_by": null, "novelty_at": null,
 "premortem_kind": "world", "verdict": "open", "date": "2026-11-05"}
```

## 9. Checklist before the first call

- [x] This file is committed on its own with its code; nothing has been run.
- [x] Lesson in §0 after reading `ledger/bets.jsonl` (74 rows), `brier.md` (35 scored, Brier 0.164, 9 hits), `audits/` (newest `ss-b10c.md`; and `sg-b4.md`, `sg-b5.md`), `lessons.jsonl` (P1–P17) and `prior.md`; `ls-sg-b6` follows in the bet-row commit.
- [ ] Design review go (or fix-first, confirmed) before the first call; `python3 ledger/check_prereg.py sg-b6 . programs/self-grading/experiments/sg-b6-samerun.md --before-run` passes.
- [x] Cockpit card committed before this file; human odds read immediately before this commit.
- [x] Engine odds elicited under v2 before this commit; human odds copied from `ledger/human-odds.jsonl`.
- [x] §0 prior work row: predicted outcome with citations; what the bet adds (rule 13, D12).
- [x] One scale direction; budget, stop-on-refusal and frozen prompts enforced in code.
- [ ] Seed commit follows this one, before any data.
- [x] DEVIATIONS.md D20.
