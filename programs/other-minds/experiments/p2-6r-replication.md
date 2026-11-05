# P2-6r. Does "position over label" hold on Sonnet 5.5 and Opus 5.5? (pre-registration)

Written and frozen in its own commit; the commit's author time (America/Denver) is the freeze time (D3, D6). Before any call. DEVIATIONS.md D14. Budget **$4.00** for both models together, enforced in code (`CAP` in `experiments/p2_6r_replication.py`, checked under a lock before every call). Stop on any refusal: the request ID goes to `results/refusal.md`, nothing is reworded or retried, no refused call is re-sent to another model (no server-side fallback), and no later run starts on a cache that holds a refused call. **No call runs before every design review says go** (oversight-testbed `operators/design-review.md`); the code's `gate()` refuses to call until each `ledger/design-reviews/om-p2-6r*.md` says `go`, or `fix-first` with `confirmed_at` set, and the seed file exists.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision, in a terminal, a chat or a question dialog. His odds come only from `ledger/human-odds.jsonl` (the cockpit's downloads, committed); if a direction has no line there when its bet is pre-registered, the bet proceeds marked "no human odds". A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit. Sean's judgment is recorded and scored as steers in `ledger/steers.jsonl`: seed questions, vetoes, added questions and architecture decisions.

## 0. The bet

| field | value |
|---|---|
| bet id | `om-p2-6r` |
| referee | `model` |
| bet type | `standard` (a replication, invariant 7) |
| direction | P2-6r (`map/program-2-map.md`, under P2-6) |
| source | program 2: om-p2-6's audited result, and its audit's "What would break it next" ("re-run on … Sonnet … to test whether position dominance is Haiku-specific") |
| engine odds, P(pass) | **25**, revised before data by this bet's lesson, from **40** (the map's P2-6r odds, written 2026-11-04 23:45 and committed as found at `ca4a39e`; copied, not restated). Both kept: `engine_odds_first` 0.40, `engine_odds` 0.25. The map gains a line saying so in this commit. The event is §5 rule 2. |
| human odds, P(pass) | no human odds: `ledger/human-odds.jsonl` is empty at this commit. Never asked for. |
| budget | $4.00 API (estimate $3.27) · 0 QPU s · minutes of laptop time |
| lesson | Correcting P1 and P12: odds once rested on a story, and a bet must be able to go either way. This bet's dry run passes about 100% in a Haiku-like world and about 0% if uptake halves, and its odds are 25% (from 40% on the map) because DM4's planted pull on Sonnet and Opus was 0.46 and 0.15 of Haiku's. |
| design review | pending. Before the first call, a fresh auditor dry-runs this design (oversight-testbed `operators/design-review.md`) → `ledger/design-reviews/om-p2-6r.md`, verdict go / fix-first / redesign. No call runs before a go. |
| pre-mortem | "If this fails, the most likely reason is that Opus 5.5 takes up shown earlier answers far less than Haiku in every cell, so its position effect stays below 0.15." Kind: `world`. Checkable: Opus reading `fail-small`, with Opus's AY uptake below Haiku's +0.45 and P below 0.15. |
| auditor | fresh session per oversight-testbed `operators/auditor.md`, after results, in a stripped clone with a sealed plant draw (`operators/plant.md`) |

**What the lesson rests on** (read at oversight-testbed `f9fc45a`, 2026-11-05 04:45 America/Denver): `ledger/bets.jsonl` (42 bets; 19 scored, 8 hits; program 2: om-p2-1, om-p2-2, om-p2-3b, om-p2-5, om-p2-6 scored, 0 hits); `ledger/brier.md` (engine Brier 0.259 on 19; always the observed hit rate 0.244; running base rate (8 + 1) / (19 + 2) = 0.43); `ledger/audits/` (newest: `ng-p3-5c.md`, `249e0af`; and `om-p2-6.md`, whose "What would break it next" names this test); `ledger/lessons.jsonl` (P1–P12 and the scored lessons, ls-om-p2-6's `recurred: false` among them). How each pattern applies:
- **P1 (odds too high on a story) and its overcorrection.** The map's 0.40 sat just under the base rate on the story that a clean Haiku result should travel. The archive says otherwise for the one thing this event depends on, the size of the own-turn pull: in program 1's DM4 (`programs/entangled-mind/results/mm-gm2-self-conditioning.md`), a planted earlier answer pulled the next rating 5.4 points on Haiku, 2.5 [−0.5, 5.5] on Sonnet and 0.8 [−1.5, 2.9] on Opus. The odds move *away* from the base rate for that archived reason, not for a new story. Against it: DM4 planted a value inside a five-question chain, while bm0's single re-rating took up 0.45 on Haiku, so the two need not scale alike. Hence 0.25, not lower.
- **P12 / design-review D11 (the bet must be able to go either way).** The dry run (`experiments/p2-6r-dryrun-output.txt` §7, 150 runs a world) puts P(pass) at 0.97–1.00 if both models behave like Haiku, 0.46–0.95 if all uptakes are three-quarters of Haiku's, and 0.00 if they are half (DM4's Sonnet ratio) or less. Each of P(pass) and P(fail) is above 10% in some plausible world.
- **P3 (a dumb predictor passes).** For this event the dumb responders are a copier that takes up the same share in every cell, no uptake at all, a label-only responder, and an assistant-turn hedge toward 50 that ignores the shown value. Each fails in 100% of dry runs (§7), the hedge on the shift-invariant conjunct.
- **P8 (more than the named factor differs).** Across models, more differs than the model: Sonnet runs with `between_tools` thinking, Opus with thinking on at low effort, Haiku (om-p2-6) with thinking disabled; 3, 2 and 20 repeats. The verdict is per model, each under its own setting; §6 lists the bundle, and no sentence compares a model with Haiku as if only the model differed.
- **P9 (wrong noun).** Every verdict sentence is in §5 and frozen in the code (`SENTENCES`).
- **P10 (one item decides).** Leave-one-item-out on each model re-applies the full rule; §5 says what happens on a flip.
- **P4 (manipulation never took).** The dry run prints the settings the run will use and checks that the cells differ only as stated (§2 of the output). AY uptake is reported, with a frozen "no own pull" sentence.
- **P7 (unpiloted execution risk).** These are program 1's 16 everyday probability vignettes (Linda the bank teller and its kin), run 9,000+ times on Haiku with no refusal; never run on Sonnet or Opus. The refusal risk is low and is not piloted; the stop rule stands. The token-cap risk on Opus (thinking counts toward `max_tokens`) is met by `max_tokens` 4,000; program 1's 4,080 Opus format calls at 1,000 had no token-cap stop.
- **P2, P5, P6, P11:** no null rule, no rival families, no control band, no leave-one-out scoring from labels. They do not apply.

## 1. In plain English

**The question.** On Haiku, P2-6 found that a number shown as an earlier answer pulls the model's new rating mostly because of *where* it sits (in the model's own turn rather than inside the user's message), not because of *whose* it is said to be ("yours" or "Sam's"). Position took up +0.23 of the displacement, the label +0.08. A finding on one model is not a finding (invariant 7). Does the same pattern hold on Sonnet 5.5 and Opus 5.5?

**What we do.** Exactly P2-6's 16 items, ±30-point displacements and wording, with P2-6's own prompt-building code, in the four cells of its 2 × 2 (assistant turn or user turn × "yours" or "Sam's") plus the no-value baseline, on Sonnet (3 repeats) and Opus (2 repeats). P2-6's fifth cell, the user's own answer, is dropped: it was secondary, and Opus's calls cost about 100 times Haiku's.

**What would count.** The bet passes only if, on *both* models, the position effect is at least 0.15 of the displacement on both of P2-6's uptake measures, with its 95% interval above 0, and larger than the label effect. Otherwise it fails, and the result says which model failed and how.

**The rival.** Larger models may simply take up a shown number less in every cell (program 1's DM4 found much weaker planted-answer pulls on Sonnet and Opus), so the position effect would shrink below the bar even if position still matters more than the label. The engine expects that to be the most likely way this fails.

**Why not Haiku again.** Haiku's run is the result being replicated (om-p2-6, 7,040 calls, audited); it is shown beside these results as the reference, not re-run.

## 2. Material

- **Models and settings** (program 1's thinking-off settings, `programs/entangled-mind/experiments/mm_common.py` OFF; structured output `{"probability": integer}`; default sampling):
  - `claude-sonnet-5-5`, `thinking: {"type": "between_tools"}` (Sonnet 5.5 rejects `disabled`; `between_tools` is its thinking-off mode), `max_tokens` 200;
  - `claude-opus-5-5`, `output_config.effort: "low"` (Opus 5.5 cannot turn thinking off; low effort is the minimum), `max_tokens` 4,000.
  - Direct (not batch) calls, so no waiting loop is needed; priced at the full rate ($2/$10 and $4/$20 per million input/output tokens, thinking billed as output).
- **Items, shown values, conversations:** P2-6's §2 exactly, through its code (`p2_6_position_label.items`, `anchors`, `shown_value`, `messages`, imported unchanged): 16 exp4 vignettes, two statements each; A = clip(round(m) + d, 2, 98), d = ±30; cells `base`, `AY`, `AS`, `UY`, `US`. Cell `UU` is not run.
- **Repeats:** Sonnet 3, Opus 2 per (statement, direction, cell), and the same number of baseline calls per statement: (32 + 32 × 2 × 4) × 3 = 864 Sonnet calls and × 2 = 576 Opus calls, **1,440 in all**.
- **Scale:** one direction, 0 = certainly false, 100 = certainly true, in every prompt (P2-6's builders).
- **Seed** (oversight-testbed `operators/hardware.md`): CURBY-Q's latest completed round is **28297**, result pulse 2025-08-22 13:42 America/Denver (checked 2026-11-05 04:37 America/Denver with `experiments/curby_seed.mjs check`, `@buff-beacon-project/curby-client@1.2.0`). That is more than 24 hours old: **CURBY-Q stalled (latest completed round 28297, 2025-08-22 13:42). Seed: the first CURBy-RNG pulse timestamped after this commit.** seed = the first 8 bytes of SHA-256(randomness ‖ bet-id), read as an unsigned big-endian integer; sub-seeds per purpose as `ledger/seed.py` derives them, purposes `order` (the run order within each repeat, the same permutation on both models) and `boot` (the bootstrap; `boot` + 1 for the label-swap null). *Filled in by the seed commit, before any data* (`data/p2-6r-seed.json`):
  `chain:` ___ · `round:` ___ · `pulse_time:` ___ · `randomness:` ___ · `client:` ___ · `certificate_verified:` ___ · `seed:` ___

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | Sonnet, 3 repeats × (32 baselines + 256 shown-value cells) | 864 | about $0.73 ($0.00085 a call, program 1's mm-gm3b Sonnet calls at full price) |
| 2 | Opus, 2 repeats × the same 288 | 576 | about $2.53 ($0.0044 a call, program 1's mm-gm3b Opus calls at full price) |

- **Run order:** Sonnet complete before Opus starts; within each model, repeat 0 complete before repeat 1 starts; within a repeat, its 288 jobs in a beacon-drawn permutation (`--purpose order`). A stop leaves whole repeats. One complete repeat on a model is enough for its reading (§5.1).
- **Caching:** every call is cached in `results/p2-6r-calls.json` under its job key (model first) with a SHA-256 of model, settings, `max_tokens` and messages; every cache hit asserts the hash, and the analysis re-checks every entry.

## 4. Statistics

Per model, exactly P2-6's, on the k leading complete repeats of that model (k = 3 and 2 when the run completes):
- **Baseline** b = mean baseline rating of a statement; D = A/100 − b; a pair with |D| < 0.05 is dropped from every cell.
- **Frozen uptake** per item and cell: Σ (r̄ − b)·sign(D) / Σ |D| over the item's kept pairs. **Shift-invariant uptake** (P2-6 D11d): Σ (r̄₊₃₀ − r̄₋₃₀) / Σ (A₊₃₀ − A₋₃₀) over the item's statements kept in both directions.
- **Position effect** P = mean over items of ½[(AY − UY) + (AS − US)]; **label effect** L = mean over items of ½[(AY − AS) + (UY − US)]; P_s and L_s the same on the shift-invariant uptake. Unit: items (16).
- **Uncertainty:** percentile 95% CI from 2,000 bootstrap resamples of items, seeded by the beacon's `boot` sub-seed (32-bit), the same indices for every statistic of a model.
- **Dumb responders and power** (dry run, §7 of the output; every call stubbed): copy-everything, no uptake, label-only and an assistant-turn hedge each pass 0%. P(pass) is about 1.00 in a Haiku-like world, about 0.5–0.95 at three-quarters of Haiku's uptakes, about 0 at half. At two or three repeats, call noise matters little next to item spread (Haiku's within-cell SD over 20 repeats: mean 1.9, median 0.7 points).
- **Secondary** (reported, never promoted): the four cell uptakes; L_s; L_A = AY − AS, L_U = UY − US and their difference; P − L with its CI; the label-swap null (as P2-6); Haiku's om-p2-6 numbers in a reference column.
- **Multiple comparisons:** one primary rule, decided once, a conjunction over two models (no correction needed: a conjunction only makes passing harder). About ten secondary intervals per model, uncorrected and labelled secondary.
- **Robustness committed now:** leave-one-item-out on each model (16 + 16 runs, each re-applying that model's reading with its own bootstrap, the other model held at its full-data reading); per-item tables.

## 5. Pre-registered reading

Applied by `analyse_cache()`; the sentences are frozen in the code's `SENTENCES` and are the only verdict sentences the results file may use (numbers filled in as point [95% CI]).

1. **Untestable** (not scored): on either model, no complete repeat (a refusal, an error or the cap), or fewer than 12 of the 16 items with a kept pair, or fewer than 12 with a statement kept in both directions. Sentence: "The test could not answer its question as run: {why}. No verdict is drawn."
2. **Each model's reading**, in this order:
   - **holds**: P ≥ 0.15 and the CI lower end of P > 0 and P > |L| (points), and P_s ≥ 0.15 and the CI lower end of P_s > 0. Sentence: "On {M}, the position effect held: {P} of the displacement (shift-invariant {P_s}), against a label effect of {L}."
   - **fail-shift**: the conditions on P hold but those on P_s do not. Sentence: "On {M}, the position effect on the pre-registered measure, {P}, did not hold on the measure that compares the +30 and −30 displays directly ({P_s}), so it may come from a change in the rating that does not follow the shown number."
   - **fail-reversed**: P ≤ −0.15 and the CI upper end of P < 0. Sentence: "On {M}, a value in the user turn was taken up more than the same value in the assistant turn: position effect {P}."
   - **fail-label**: L ≥ 0.15 and the CI lower end of L > 0 and |L| ≥ |P|. Sentence: "On {M}, the label changed uptake at least as much as the position: label {L}, position {P}."
   - **fail-small**: anything else. Sentence: "On {M}, the position effect did not meet the rule: position {P} (shift-invariant {P_s}), label {L}."
3. **Pass** (scored 1): both models read **holds**. Sentence: "On Sonnet 5.5 and Opus 5.5, as on Haiku 5.5, on program 1's 16 bm0 items at ±30 points, a value in the assistant turn was taken up more than the same value in the user turn, by at least 0.15 of the displacement on both uptake measures and by more than the label ("your" against "Sam's") changed it: Sonnet position effect {P_sonnet} (label {L_sonnet}), Opus {P_opus} (label {L_opus}). On this design, on these three Claude models, the pull of an earlier answer follows the turn it sits in more than whose answer it is said to be." Reported as **pass** (replicated on two more models of one family, one design; still one design, so the auditor reads invariant 7 for the design).
4. **Fail** (scored 0): otherwise. Sentence: "The position-over-label result found on Haiku 5.5 did not hold on both Sonnet 5.5 and Opus 5.5 by the pre-registered rule (on each model: a position effect of at least 0.15 of the displacement on both uptake measures, its 95% interval above 0, and larger than the label effect)." It is followed by each model's own reading sentence.
5. **Added where they apply** (frozen):
   - **No own pull** (a model's AY CI lower end ≤ 0): "On {M}, the value labelled as the model's own and placed in its own turn was not taken up detectably (uptake {AY}), so the own-answer pull is not present in this wording on {M}, and the position effect there has little to split." The verdict stands as the rule gives it.
   - **Fragile** (P10; dropping one item on one model alone changes the overall verdict): "Dropping item {item} alone on {M} changes the overall verdict to "{v}", so it rests on that item." The bet is scored by the full-data rule; the label is then written "<verdict>, fragile (one item)".

**Reported in every case:** calls, cost, refusals and complete repeats per model; pairs kept and dropped; items usable; the four cell uptakes, P, P_s, L, L_s, L_A, L_U, the interaction and P − L per model with CIs; the label-swap null; the leave-one-item-out range of P and the overall verdict flips; per-item tables; Haiku's om-p2-6 numbers for reference.

## 6. What it cannot do

- **Each model under its own setting.** Sonnet with `between_tools` thinking, Opus with thinking on at low effort, Haiku (the reference) with thinking disabled. A difference between models may be the model or its setting; the write-up will not say "model size" or "capability".
- **Fewer repeats.** 3 (Sonnet) and 2 (Opus) against Haiku's 20, so the baseline b is a mean of 3 or 2 calls; item spread dominates the interval, but b is noisier than in om-p2-6.
- **Position is still a bundle** (P2-6 §6): three messages with a prefilled assistant turn against one message; the label in a later message against the same one; the value farther from the request against nearer. The verdict sentences say "the turn it sits in", meaning this bundle.
- **No fifth cell:** the user's own answer is not measured, so a label effect cannot be read as about Sam or about the self.
- **One family, one design:** three Claude models, one item set (16 everyday probability vignettes), ±30 points, one wording. "Every", "all", "models", "LLMs" and "language models" will not appear in the write-up. A pass replicates across models, not across designs.
- **No mechanism words:** "commitment", "belief", "self-model", "memory" are not what this measures; it measures uptake of a shown number.

## 7. Stop rules

- Budget cap in code: $4.00 for both models. If reached, the run stops; whole repeats completed before it are analysed (§5.1).
- Stop on any refusal: no rewording, no retry, no fallback to another model; the refused job is written into the cache, `results/refusal.md` is written with its request ID, and no later run starts on that cache. A refusal on Sonnet means Opus is never called.
- A stop on a non-refusal API error (including a `max_tokens` stop) may be resumed from cache; the error is logged in the results.
- No call before every design review's go (or confirmed fix-first) and before the seed file exists (`gate()`).

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "om-p2-6r", "program": "other-minds", "map": "program-2-map", "direction": "P2-6r",
 "title": "Replication of P2-6 on Sonnet 5.5 and Opus 5.5: does position beat label on both?",
 "source": "engine", "referee": "model", "bet_type": "standard",
 "engine_odds_first": 0.40, "engine_odds": 0.25, "engine_odds_at": "this commit (lesson ls-om-p2-6r); 0.40 at ca4a39e",
 "odds_event": "on both claude-sonnet-5-5 and claude-opus-5-5: position effect P >= 0.15 with its 95% item-bootstrap CI lower end > 0, the shift-invariant P_s likewise, and P > |L| (label effect)",
 "human_odds": null, "human_odds_note": "no human odds",
 "prereg_commit": "<this commit>", "budget_usd": 4.00, "seed_source": "curby-rng", "beacon": null, "seed": null, "tiebreak": null,
 "lesson": "ls-om-p2-6r", "design_review": {"path": "ledger/design-reviews/om-p2-6r.md", "verdict": null, "commit": null, "reviewer_model": null, "fix_deviations": [], "missed": null},
 "premortem": "If this fails, the most likely reason is that Opus 5.5 takes up shown earlier answers far less than Haiku in every cell, so its position effect stays below 0.15.",
 "premortem_kind": "world", "premortem_at": "<this commit>", "human_premortem": null, "human_premortem_kind": null,
 "failed": null, "failure_reason": null, "failure_kind": null, "premortem_score": null, "human_premortem_score": null, "risk_seen": null,
 "verdict": "open", "date": "2026-11-05", "test": "experiments/p2-6r-replication.md", "deviation": "D14",
 "replication_of": "om-p2-6", "result": null, "audit": null, "diagnosis": null}
```

## 9. Checklist before the first call

- [x] This file is committed on its own with its code and stubbed dry run; nothing has been run against the API.
- [x] The lesson row in §0 is filled after reading ledger/bets.jsonl, brier.md, audits/ and lessons.jsonl; the same sentence goes to `ledger/lessons.jsonl` as `ls-om-p2-6r`.
- [ ] A fresh auditor's design review has returned **go**, or fix-first with every fix logged in DEVIATIONS and confirmed; `python3 ledger/check_prereg.py om-p2-6r . programs/other-minds/experiments/p2-6r-replication.md --before-run` passes.
- [x] Engine odds on record in the map before this commit (0.40, `ca4a39e`); human odds: no human odds.
- [x] The rule in §5 can be applied by a stranger (`model_reading()`, `overall()`; dry run §6).
- [x] The pre-mortem in §0 is one sentence, names a checkable mechanism, and carries its kind.
- [x] One scale direction in every prompt.
- [x] §2 records CURBY-Q's latest completed round and names the chain by the 24-hour rule; the seed commit follows this one before any data.
- [x] Budget and stop-on-refusal enforced in code.
- [x] DEVIATIONS.md row D14 added.
- [x] Commit message: `Pre-register om-p2-6r: P2-6 on Sonnet 5.5 and Opus 5.5 (D14)`.
