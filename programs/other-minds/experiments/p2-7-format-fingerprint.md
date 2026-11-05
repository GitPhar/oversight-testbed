# P2-7. Shared format fingerprint: does a credence attributed to Sam deviate across formats the way the model's own does? (pre-registration)

Written and frozen in its own commit; the commit's author time (America/Denver) is the freeze time (D3, D6). Before any call. DEVIATIONS.md D15. Budget **$1.50** for the three models together, enforced in code (`CAP` in `experiments/p2_7_format_fingerprint.py`, checked under a lock before every call). Stop on any refusal: the request ID goes to `results/refusal.md`, nothing is reworded or retried, no refused call is re-sent to another model (no server-side fallback), and no later run starts on a cache that holds a refused call. **No call runs before every design review says go**; the code's `gate()` refuses to call until each `ledger/design-reviews/om-p2-7*.md` says `go`, or `fix-first` with `confirmed_at` set, and the seed file exists.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision, in a terminal, a chat or a question dialog. His odds come only from `ledger/human-odds.jsonl` (the cockpit's downloads, committed); if a direction has no line there when its bet is pre-registered, the bet proceeds marked "no human odds". A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit. Sean's judgment is recorded and scored as steers in `ledger/steers.jsonl`: seed questions, vetoes, added questions and architecture decisions.

## 0. The bet

| field | value |
|---|---|
| bet id | `om-p2-7` |
| referee | `model` |
| bet type | `standard` |
| direction | P2-7 (`map/program-2-map.md`, rank 7, "Three-model version") |
| source | literature + program 1: L (A8, A11, A13, A14, A5, B2, D17) + P1 (F4), as the map states |
| engine odds, P(pass) | **20**, revised before data by this bet's lesson, from **25** (the map's three-model P2-7 odds, written 2026-11-04 23:45 and committed as found at `ca4a39e`; copied, not restated). Both kept: `engine_odds_first` 0.25, `engine_odds` 0.20. The map gains a line saying so in this commit. The event is §5 rule 3. Disclosed: the author read Sean's cockpit line for P2-7 (70%, committed 05:19) before writing this lesson; the move is away from it and rests only on the reasons in the lesson. |
| human odds, P(pass) | **70** (`ho-20261105-051140-gfv`, recorded 2026-11-05 05:11 on the cockpit, committed `24fb0f4`; copied by `ledger/human_odds_match.py other-minds P2-7`). His card asked the map's original event ("the self and Sam residuals … correlate at ≥ 0.5 of the split-half ceiling", one model, about $0.24). This bet's event is stricter (every tested model of three, and a margin over the generic-link rival). He is scored on this bet's outcome, as the ledger scores every bet; his card's event is reported beside it as a secondary (`card_event`, §5.6), never scored. |
| budget | $1.50 API (estimate about $1.19) · 0 QPU s · minutes of laptop time |
| lesson | Correcting P13 and P12: om-p2-6r's sentence hung on a plain float at the rule's boundary, and a bet must go either way. Every threshold uses one tolerance, and the dry run spans pass 1.00 to 0.00, and its odds are 20% (from 25% on the map) because Opus held in 2 of 60 dry runs with Sam hedged toward 50. |
| design review | pending. Before the first call, a fresh auditor dry-runs this design (oversight-testbed `operators/design-review.md`) → `ledger/design-reviews/om-p2-7.md`, verdict go / fix-first / redesign. No call runs before a go. |
| pre-mortem | "If this fails, the most likely reason is that Sam's ratings are hedged toward 50, so on Opus the self–Sam residual correlation does not beat the generic-link rival by 0.10." Kind: `world`. Checkable: a fail reading on Opus (fail-generic or fail-ceiling), with Sam's format means nearer 0.5 than self's. |
| auditor | fresh session per oversight-testbed `operators/auditor.md`, after results, in a stripped clone with a sealed plant draw (`operators/plant.md`) |

**What the lesson rests on** (read at oversight-testbed `2efed51`, 2026-11-05 05:30 America/Denver): `ledger/bets.jsonl` (52 bets; 20 scored, 8 hits; program 2: om-p2-1, -2, -3b, -5, -6, -6r scored, 0 hits); `ledger/brier.md` (engine Brier 0.249 on 20; running base rate (8 + 1) / (20 + 2) = 0.41); `ledger/audits/` (newest: `sg-b1.md`, `f0a577f`, another program's; newest in program 2: `om-p2-6r.md`, `d6999a8`); `ledger/lessons.jsonl` (P1–P13; ls-om-p2-6r scored, recurred). How each pattern applies:
- **P13 (a boundary the rule names, compared in plain float; new from om-p2-6r's audit).** Every threshold in `model_reading()` (rel ≥ 0.5, ρ ≥ 0.5, Δ ≥ 0.10, CI > 0) uses the same 1e-9 tolerance; the dry run (§6) feeds values exactly on each boundary, computed as sums that land a hair below (0.3 − 0.2 = 0.0999…), and shows each lands on the pass side, and a value 1e-4 below lands on the fail side. There is no data filter with a threshold.
- **P12 / D11 (the bet must go either way).** Dry run §7: P(pass) 1.00 if Sam carries the model's own means, 0.62 if 70% of the fingerprint is shared, 0.17 if Sam is pulled 30% toward 50, 0.01 if half is shared, 0.00 if Sam's deviations are independent of the model's own.
- **P1 (odds on a story).** The map's 0.25 already sat below the base rate (0.41) for named reasons (a conjunction over models, a margin over a dumb rival, Opus's small residuals). The lesson moves it further for a dry-run and archive reason: in the hedged-Sam world Opus held in 2 of 60 runs, and P2-1 found that on Haiku the "Sam" framing shared only 0.67 of its reproducible item variation with "how confident are you" (all P2-1's cross-framing Qs lay between 0.56 and 0.77). om-p2-6r adds that Sonnet and Opus did not behave like Haiku on P2-6's design.
- **P3 (dumb predictor).** The generic-link rival is the dumb responder: each format's overall shape, no statement-specific deviation. The rule must beat it by 0.10; in the dry run it never passes (0.00; 0.06 untestable). A shuffled-statement null is reported.
- **P8 (more than the named factor differs).** Self and Sam differ in date, batch versus direct calls, repeats (10 against 2), and the Sam sentence; listed in §6. The archived self prompts are reproduced exactly (dry run §2), so the wording differs only by the Sam sentence and the holder of the credence.
- **P9 (wrong noun).** Every verdict sentence is in §5 and frozen in `SENTENCES`; no "theory of mind", "represented credence" or "simulation".
- **P10 (one item decides).** Leave-one-item-out on each tested model re-applies the overall rule; a flip appends a frozen sentence.
- **P4 (manipulation never took).** The dry run prints every setting and checks the self prompts against program 1's builder.
- **P7 (unpiloted execution risk).** These statements were rated thousands of times per model in program 1 with no refusal and no token-cap stop (gm3b, mm-gm3b); not piloted. A refusal stops the run (§7).
- **P2, P5, P6, P11:** no null rule, no rival families fitted against each other, no control band, no labels in a leave-one-out score. They do not apply.

## 1. In plain English

**The question.** Program 1 found that a model's 0–100 rating, its "how many of 100 statements like this would be true" count, and its verbal answer ("likely", "very unlikely" …) do not read out one stored credence: for many statements the formats disagree with one another in a way that is specific to the statement (program 1's F4). If the credence the model attributes to someone else is built the same way, then when it is asked what "Sam, a person who has read exactly what you have read here" thinks, the formats should disagree with each other on the *same* statements, in the *same* direction. That is the shared format fingerprint.

**What we do.** Take 34 statements (2 drawn by the public beacon from each of the 17 items for which all three models have archived self data in all formats). Ask each model, in the same three graded formats, what Sam thinks, twice. Compare each statement's format-by-format deviation from one shared credence for Sam with the same deviation in the model's own archived answers (program 1, 10 repeats).

**What would count.** On every model whose deviations are reproducible enough to test (at least two models), the self–Sam correlation of those deviations must reach half of what the noise allows, and beat by at least 0.10 a dumb rival that keeps each format's overall shape but no statement-specific deviation.

**The rival.** A match could come from the formats' shared overall shape rather than from statement-specific deviations: if, say, the verbal scale saturates at both ends, every responder's deviations from a straight-line link would correlate. The generic-link rival is built to carry exactly that shape and nothing else, and the bet must beat it.

## 2. Material

- **Models and settings** (program 1's thinking-off settings, `programs/entangled-mind/experiments/mm_common.py` OFF; the archived self calls used the same; structured output):
  - `claude-haiku-5-5`, `thinking: {"type": "disabled"}`, `max_tokens` 100 (as gm3b);
  - `claude-sonnet-5-5`, `thinking: {"type": "between_tools"}`, `max_tokens` 1,000 (as mm-gm3b);
  - `claude-opus-5-5`, `output_config.effort: "low"`, `max_tokens` 1,000 (as mm-gm3b; 0 token-cap stops in its 4,080 archived calls).
  - Direct (not batch) calls at the full rate.
- **Self data (archived, read-only, no new self calls):** `programs/entangled-mind/results/gm3b-calls.json` (Haiku), `mm-gm3b-sonnet-calls.json`, `mm-gm3b-opus-calls.json`: formats F1 (rating 0–100), F5 (frequency out of 100) and F6 (verbal 7-point), 10 repeats per (claim, format). Fields read: the key and `value`. The yes/no, bet and pairwise formats (F2–F4) are not used: they need many repeats per statement to show a per-statement deviation.
- **Items:** the 68 (item, claim) pairs that all three archives hold with all three formats and all 10 repeats (17 items × 4 chain claims; the Opus arm's items). Statements: 2 of each item's 4, drawn with the beacon's `items` sub-seed, items in sorted order (`draw_statements()`): **34 statements**.
- **Sam prompts** (`sam_prompt()`): the archived self prompt's head, word for word (`Consider this statement, which came up in a discussion of the question "…":\n\n"…"\n\n`), then P2-1's framing (d) sentence verbatim, "Sam is a person who has read exactly what you have read here, and nothing else.", then the format's question with Sam as the holder:
  - F1: "How likely does Sam think it is that this statement is true? Give an integer from 0 to 100, where 0 = certainly false and 100 = certainly true."
  - F5: "Think of 100 statements like this one, about each of which Sam has the same evidence as Sam has about this one. How many of the 100 would Sam say are true? Give an integer from 0 to 100."
  - F6: "How likely does Sam think it is that this statement is true? Choose one: certainly false, very unlikely, unlikely, as likely as not, likely, very likely, certainly true."
  The dry run checks that `self_prompt()` reproduces program 1's archived prompts exactly.
- **Repeats:** 2 per (statement, format): 34 × 3 × 2 = **204 calls a model, 612 in all**.
- **Scale:** one direction (0 = certainly false, 100 = certainly true; the verbal scale runs false → true; F5 counts true statements).
- **Seed** (oversight-testbed `operators/hardware.md`): CURBY-Q's latest completed round is **28297**, result pulse 2025-08-22 13:42 America/Denver (checked 2026-11-05 05:19 America/Denver with `experiments/curby_seed.mjs check`, `@buff-beacon-project/curby-client@1.2.0`). That is more than 24 hours old: **CURBY-Q stalled (latest completed round 28297, 2025-08-22 13:42). Seed: the first CURBy-RNG pulse timestamped after this commit.** seed = the first 8 bytes of SHA-256(randomness ‖ bet-id), read as an unsigned big-endian integer; sub-seeds per purpose as `ledger/seed.py` derives them, purposes `items` (the statement draw), `order` (the run order within each repeat, the same permutation on every model) and `boot` (the bootstrap; `boot` + 1 for the shuffled-statement null). *Filled in by the seed commit, before any data* (`data/p2-7-seed.json`):
  `chain:` CURBy-RNG · `round:` pulse 1592214 (previous 1592213 at 05:29:00, before this file's commit at 05:29:59) · `pulse_time:` 2026-11-05 05:30:00 America/Denver · `randomness:` 8caed94e7e0a7210ff99187f4eab49f2653128ff03bdaa5115065a1310339577f773fcba9298fd2f6447ae3b60bc000edc8b527b85f0c5878e04dbaa35e7a9bc · `client:` @buff-beacon-project/curby-client@1.2.0 · `certificate_verified:` false · `seed:` 3738687062774756507; `items` 3655526655814506593 (seed32 717985889); `order` 13533806480269411703 (seed32 3814098295); `boot` 9867349086274622913 (seed32 3928790465)

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | Haiku, 2 repeats × 34 statements × 3 formats | 204 | about $0.01 |
| 2 | Sonnet, the same | 204 | about $0.19 |
| 3 | Opus, the same | 204 | about $0.99 |

Per-call estimates are program 1's archived graded-format calls at the full rate (Haiku $0.000043, Sonnet $0.00086, Opus $0.0044), plus 10% for the longer Sam prompt. **Run order:** Haiku, then Sonnet, then Opus; within a model, repeat 0 complete before repeat 1; within a repeat, a beacon-drawn order of its 102 jobs. **Caching:** every call cached in `results/p2-7-calls.json` with a SHA-256 of model, settings, `max_tokens`, messages and schema, asserted on every hit and re-checked at analysis.

## 4. Statistics

Per model:
- **Encoding:** every response on 0–1: F1/100, F5/100, F6 = its position on the 7-point scale / 6. Cell value = the mean over repeats (self: 10; Sam: 2).
- **One-credence model:** X[s, f] = a_f + b_f c_s + e[s, f], one latent credence c per statement, each format a linear read-out with its own offset and slope; fitted by least squares (exactly: a = the format means, b c′ = the first singular term of the column-centred matrix). The residuals e are the statement-by-format deviations, the **fingerprint**. Fitted separately to self and to Sam.
- **Statistic:** r = the correlation of self and Sam residuals over the 34 × 3 cells. **Ceiling:** the Spearman–Brown split-half reliability of each source's residuals (self: even vs odd repeats; Sam: repeat 0 vs repeat 1, each half fitted on its own). **ρ = r / √(rel_self · rel_sam).**
- **The dumb rival (P3), the generic-link responder:** Sam's own latent credences put through a cubic link per format, fitted across statements (`generic_link()`), so it has each format's overall shape and offset but no statement-specific deviation; r_g its residuals' correlation with self's, ρ_g = r_g / the same ceiling. **Δ = ρ − ρ_g.**
- **Gate:** a model is *testable* only if rel_self ≥ 0.5 and rel_sam ≥ 0.5.
- **Uncertainty:** percentile 95% CIs from 2,000 bootstrap resamples of the 17 items (each with its two statements), every statistic refitted in each resample, seeded by the beacon's `boot` sub-seed.
- **Dry run** (`experiments/p2-7-dryrun-output.txt`, every call stubbed, Sam data built from each model's archived self data with its archived per-call noise, 60 runs a world): if Sam carries the model's own means, P(pass) 1.00; Sam pulled 30% toward 50, 0.17 (Opus fails the margin); 70% of the fingerprint shared, 0.62; half shared, 0.01; independent deviations, 0.00; the generic rival itself, 0.00 (0.06 untestable); no deviation at all, untestable. Self-residual reliabilities in the archive: Haiku 0.97, Sonnet 0.97, Opus 0.94 (residual SD 0.17, 0.11, 0.04).
- **Secondary** (reported, never promoted): raw r and r_g; the reliabilities; residual SDs; the format means of self and Sam; mean |self − Sam|; a shuffled-statement null for r (Sam's residual rows permuted, 2,000 times, `boot` + 1).
- **Multiple comparisons:** one primary rule, decided once, a conjunction over the testable models (no correction: a conjunction only makes passing harder). The secondaries are uncorrected and labelled.
- **Robustness committed now:** leave-one-item-out on each model (17 refits with their own bootstrap, the other models held at their full-data readings), re-applying the overall rule.

## 5. Pre-registered reading

Applied by `analyse_cache()`; the sentences are frozen in the code's `SENTENCES` and are the only verdict sentences the results file may use.

1. **Each model's reading**, in this order:
   - **incomplete** (that model is not tested): any of its 204 Sam calls missing (a refusal, an error or the cap).
   - **unreliable** (that model is not tested): rel_self < 0.5 or rel_sam < 0.5. Sentence: "On {M}, the residuals were not reliable enough to test (split-half reliability self {rel_self}, Sam {rel_sam}; the floor is 0.5), so {M} is not tested."
   - **fail-ceiling**: ρ < 0.5. Sentence: "On {M}, the self–Sam residual correlation was {rho} of its ceiling, below 0.5."
   - **holds**: Δ ≥ 0.10 and the CI lower end of Δ > 0. Sentence: "On {M}, the self–Sam residual correlation was {rho} of its ceiling, {delta} above the generic-link rival."
   - **fail-generic**: otherwise. Sentence: "On {M}, the self–Sam residual correlation was {rho} of its ceiling, but it did not beat the generic-link rival by the pre-registered 0.10 with its interval above 0 (difference {delta}), so the match may come from the formats' shared shape rather than from statement-specific deviations."
2. **Untestable** (not scored): fewer than 2 models tested. Sentence: "The test could not answer its question as run: {why}. No verdict is drawn."
3. **Pass** (scored 1): every tested model reads **holds** (at least 2 tested). Sentence: "On {models}, on 34 statements from 17 of program 1's experiment-5 items and three graded formats, the rating the model gave for Sam, a person who has read exactly what it has read, deviated from one shared credence in the same statement-by-statement way as the model's own archived rating: on each model the self–Sam residual correlation reached at least 0.5 of its reliability ceiling and beat a generic-link rival by at least 0.10 ({per_model}). On this design, the format fingerprint of an attributed credence matches the model's own." Reported as **pass** across the tested models (one design).
4. **Fail** (scored 0): otherwise. Sentence: "On {models}, on 34 statements from 17 of program 1's experiment-5 items and three graded formats, the format fingerprint of the rating given for Sam did not match the model's own on every model tested by the pre-registered rule (a self–Sam residual correlation of at least 0.5 of its reliability ceiling, beating a generic-link rival by at least 0.10 with its 95% interval above 0)." It is followed by each model's reading sentence.
5. **Fragile** (P10; dropping one item on one model alone changes the overall verdict): "Dropping item {item} alone on {M} changes the overall verdict to "{v}", so it rests on that item." Scored by the full-data rule; the label is then written "<verdict>, fragile (one item)".

6. **Card event** (secondary, never scored): ρ ≥ 0.5 on every tested model, the event Sean's cockpit card asked (`card_event`).

**Reported in every case:** calls, cost and refusals per model; every reading; ρ, Δ, r, r_g, ρ_g, both reliabilities with CIs; residual SDs; format means; the shuffled-statement null; leave-one-item-out flips.

## 6. What it cannot do

- **Self and Sam differ in more than whose credence it is** (P8): the self data are program 1's, asked as "how likely is it" (P2-1's impersonal framing (a), not "how confident are you"), in batches, on 2026-11-04, 10 repeats; the Sam data are asked today, directly, 2 repeats, with one added sentence. A mismatch may come from any of these; a match survives them. P2-1 found the same "how likely" wording reproduced across sessions at Q = 0.96 on Haiku.
- **Three formats, not six.** The fingerprint here is the graded formats' only. With three formats, each statement's residuals have two degrees of freedom.
- **Each model under its own setting** (thinking disabled, between_tools, low effort), as in the archive.
- **One family, one item set:** 34 statements from program 1's chain claims (trivia and technical questions), one Sam wording. "Every", "all", "models", "LLMs" and "language models" will not appear in the write-up.
- **No mechanism words:** a shared fingerprint shows the two reports are produced alike on this design; it does not show a "represented credence", a "theory of mind" or "simulation".

## 7. Stop rules

- Budget cap in code: $1.50 for the three models. If reached, the run stops; a model with any Sam cell missing is not tested (§5.1).
- Stop on any refusal: no rewording, no retry, no fallback to another model; the refused job is written into the cache, `results/refusal.md` is written with its request ID, and no later run starts on that cache. A refusal on Haiku means Sonnet and Opus are never called.
- A stop on a non-refusal API error (including a `max_tokens` stop) may be resumed from cache; the error is logged in the results.
- No call before every design review's go (or confirmed fix-first) and before the seed file exists (`gate()`).

## 8. Ledger entry (filled now, completed after audit)

```json
{
 "id": "om-p2-7",
 "program": "other-minds",
 "map": "program-2-map",
 "direction": "P2-7",
 "title": "Shared format fingerprint on Haiku, Sonnet and Opus: do the formats' statement-specific deviations for Sam match the model's own?",
 "source": "literature",
 "referee": "model",
 "bet_type": "standard",
 "engine_odds_first": 0.25,
 "engine_odds": 0.2,
 "engine_odds_at": "this commit (lesson ls-om-p2-7); 0.25 at ca4a39e",
 "odds_event": "on every tested model (at least 2 of claude-haiku-5-5, claude-sonnet-5-5, claude-opus-5-5 with split-half reliability >= 0.5 for self and Sam residuals): rho = r(self, Sam residuals)/ceiling >= 0.5, and delta = rho - rho(generic-link rival) >= 0.10 with its 95% item-bootstrap CI lower end > 0",
 "human_odds": 0.7,
 "human_odds_at": "ho-20261105-051140-gfv (2026-11-05T05:11:40-07:00)",
 "human_odds_note": "Sean's cockpit card asked the map's original event (rho >= 0.5, one model, about $0.24); scored on this bet's outcome; card event reported as a secondary",
 "prereg_commit": "<this commit>",
 "budget_usd": 1.5,
 "seed_source": "curby-rng",
 "beacon": null,
 "seed": null,
 "tiebreak": null,
 "lesson": "ls-om-p2-7",
 "design_review": {
  "path": "ledger/design-reviews/om-p2-7.md",
  "verdict": null,
  "commit": null,
  "reviewer_model": null,
  "fix_deviations": [],
  "missed": null
 },
 "premortem": "If this fails, the most likely reason is that Sam's ratings are hedged toward 50, so on Opus the self–Sam residual correlation does not beat the generic-link rival by 0.10.",
 "premortem_kind": "world",
 "premortem_at": "<this commit>",
 "failed": null,
 "failure_reason": null,
 "failure_kind": null,
 "premortem_score": null,
 "verdict": "open",
 "date": "2026-11-05",
 "test": "experiments/p2-7-format-fingerprint.md",
 "deviation": "D15",
 "result": null,
 "audit": null,
 "diagnosis": null
}
```

## 9. Checklist before the first call

- [x] This file is committed on its own with its code and stubbed dry run; nothing has been run against the API.
- [x] The lesson row in §0 is filled after reading ledger/bets.jsonl, brier.md, audits/ and lessons.jsonl; the same sentence goes to `ledger/lessons.jsonl` as `ls-om-p2-7`.
- [ ] A fresh auditor's design review has returned **go**, or fix-first with every fix logged in DEVIATIONS and confirmed; `python3 ledger/check_prereg.py om-p2-7 . programs/other-minds/experiments/p2-7-format-fingerprint.md --before-run` passes.
- [x] Engine odds on record in the map before this commit (0.25, `ca4a39e`); human odds copied from `ledger/human-odds.jsonl` (0.70, `ho-20261105-051140-gfv`).
- [x] The rule in §5 can be applied by a stranger (`model_reading()`, `overall()`; dry run §6).
- [x] The pre-mortem in §0 is one sentence, names a checkable mechanism, and carries its kind.
- [x] One scale direction in every prompt.
- [x] §2 records CURBY-Q's latest completed round and names the chain by the 24-hour rule; the seed commit follows this one before any data.
- [x] Budget and stop-on-refusal enforced in code.
- [x] DEVIATIONS.md row D15 added.
- [x] Commit message: `Pre-register om-p2-7: shared format fingerprint on Haiku, Sonnet and Opus (D15)`.
