# P2-5r. Does "Sam moves more than self" hold on Sonnet 5.5 and Opus 5.5, for upward and downward plants separately? (pre-registration)

Written and frozen in its own commit; the commit's author time (America/Denver) is the freeze time. Before any call. DEVIATIONS.md D18. Budget **$5.00** for both models together (Sonnet $1.50, Opus $3.50), enforced in code (`CAP`, `CAPS` in `experiments/p2_5r_replication.py`, checked under a lock before every call); budget ruling br-010 in `ledger/spend.jsonl` (st-16; CONTEXT rule 4). Stop on any refusal: the request ID goes to `results/refusal-p2-5r.md`, nothing is reworded or retried, no refused call is re-sent to another model, and no later run starts on a cache that holds a refused call. **No call runs before every design review says go**: `gate()` refuses until each `ledger/design-reviews/om-p2-5r*.md` says go, or fix-first with `confirmed_at` set, and the seed file exists.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision, in a terminal, a chat or a question dialog. His odds come only from `ledger/human-odds.jsonl` (the cockpit's downloads, committed); if a direction has no line there when its bet is pre-registered, the bet proceeds marked "no human odds". A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit. Sean's judgment is recorded and scored as steers in `ledger/steers.jsonl`: seed questions, vetoes, added questions and architecture decisions.

## 0. The bet

| field | value |
|---|---|
| bet id | `om-p2-5r` |
| referee | `model` |
| bet type | `standard` (a replication, invariant 7) |
| direction | P2-5r (`map/other-minds.json`, added with its cockpit card at `9099bdd`, before this file) |
| source | literature: `paper/novelty.md` finding 6 and "Ranked: the three replications", item 3 ("the egocentric-leakage design on Sonnet and Opus at 2 repeats per cell, with the upward-versus-downward split pre-registered this time"); the om-p2-5 audit's "What would break it next" (pre-register 5b separately by sign) |
| engine odds, P(pass) | **12**, from a fresh context under rule 14 (template v2), stated 2026-11-05 10:09 America/Denver before this commit: prior **0.32** (`ledger/prior.md`), adjustment **−0.20**, reason: "other-minds 0/7, literature 0.13 and model referee 0.22 outweigh layer-2/$1-5 rows; parent's downward gap was null, Opus uptake ~0.07, and Haiku-like dry run passes only 0.23." No map odds were stated for P2-5r. |
| human odds, P(pass) | no human odds: `python3 ledger/human_odds_match.py other-minds P2-5r`, run immediately before this commit, finds no line (the card went up at `9099bdd`). Never asked for. |
| models | `claude-sonnet-5-5` and `claude-opus-5-5`, not Haiku, because Haiku already ran this design (om-p2-5, 5 repeats); its archive is analysed by the same code as a reference column, never scored. Opus at 2 repeats like Sonnet (both at 2, as the novelty page specifies); Opus costs about 2.9 times Sonnet per call here. |
| budget | $5.00 API (estimate $3.78: Sonnet $0.98, Opus $2.80, from om-p2-6r's archived per-call cost on these vignettes) · 0 QPU s · minutes of laptop time |
| lesson | Correcting P10 and P1: om-p2-5's pooled gap hid that only upward plants carried it, and a novelty story is not odds. This bet scores each plant direction as its own conjunct on Sonnet and Opus, with a dry run passing 0.85 at a clear two-way gap and 0.23 Haiku-like, and its odds are 12% (none on the map) because the downward gap was null. |
| prior work | Choi, Hong and Kim (2024, "People will agree what I think", NAACL Findings 2025): feeding a model one option as its own choice shifts its estimate of how many peers choose it (false consensus, about 20 points on Claude 3 Opus), generally less than in Ross et al. (1977)'s people. They did not compare the pull on others with the pull on the model's own re-rating, nor show a third party's number. Nothing we found predicts the sign of Sam minus self. Program 2's own record: on Haiku, Sam minus self +0.14 [+0.10, +0.19] pooled, +0.22 upward, +0.04 [−0.02, +0.10] downward (om-p2-5 and its audit); om-p2-6r found Opus 5.5 takes up a planted own answer only about 0.07 on these vignettes. |
| design review | pending: a fresh auditor dry-runs this design → `ledger/design-reviews/om-p2-5r.md`. No call before a go. |
| pre-mortem | "If this fails, the most likely reason is that Sam's excess over the model's own re-rating comes only from upward plants on both models, as on Haiku, so the downward-plant gap's interval reaches 0." Kind: `world`. Checkable: readings `up_only` on the tested models. |
| auditor | fresh session per oversight-testbed `operators/auditor.md`, after results, in a stripped clone with a sealed plant draw (`operators/plant.md`) |

**What the lesson rests on** (read at oversight-testbed `9099bdd`, 2026-11-05 10:10 America/Denver): `ledger/bets.jsonl` (67 bets; 37 scored, 12 hits; program 2 0 of 7 scored); `ledger/brier.md` (Brier 0.188 on 37; hit rate 12/37 = 0.32); `ledger/prior.md` (prior 0.32); `ledger/audits/` (newest: `ng-p3-18.md`; program 2's `om-p2-5.md`, whose split this bet pre-registers, and `om-p2-6r.md`, the last replication on these models); `ledger/lessons.jsonl` (P1–P17). How each pattern applies:
- **P1 (odds on a story).** The story is the novelty page's: "Sam moves more than self" would be new. The archive says the Haiku excess was upward-only, and Opus barely takes up its own planted answer; the fresh odds are 0.12.
- **P10 / pooling (B6 in the om-p2-5 audit).** The pooled gap hid that one direction carried it. Here each direction is its own conjunct, and the pass needs both.
- **P12 / D11 (can go either way).** Dry run (`experiments/p2-5r-dryrun-output.txt`, one model, 60 synthetic runs a world, 400 resamples): pass 0.85 with a clear +0.15 gap both ways; 0.23 in a Haiku-like world (down gap +0.04); 0.15 at +0.08 both ways; about 0 when Sam equals own, when Sam is half of own (read `reversed` 1.00), or with an Opus-like weak pull; `untestable_nothing_moved` 0.95 when nothing moves.
- **P8 (more than the named factor differs).** Between models, settings differ (Sonnet thinking between_tools, Opus effort low, Haiku thinking disabled) and repeats (2, 2, 5); each model's reading is its own, and no sentence compares models as if only the model differed. Within a model, own and Sam differ in the question asked (the om-p2-5 audit's wording rival, P2-17's territory): this design does not remove it, and §6 says so.
- **P13.** Every bound is compared with a 1e-9 tolerance; the dry run checks 0.0, 0.3 − 0.1 − 0.2 and 1e-4.
- **P14.** The resampling unit is the vignette (16; X and Y share one).
- **P15 (dry run on assumed spreads).** The noise (2–3 points a call) and vignette factor (SD 0.3, and 0.6 as a check: no change) are assumptions; om-p2-5's Haiku archive had a median within-cell SD of 0, and om-p2-6r found Sonnet's take-up varies widely by vignette, which the 0.6 world approximates.
- **P7.** These vignettes ran 1,440 times on Sonnet and Opus in om-p2-6r with no refusal and no token-cap stop; not piloted.
- **P2, P3, P4, P5, P6, P11, P16, P17:** no null rule (a fail is "did not show"); the dumb responders are the dry-run worlds (Sam = own, nothing moves) and the SWAP contrast; the manipulation is om-p2-5's, which moved Haiku; no fitted rivals, no control band, no leave-one-out labels, no item-property baseline, no fix yet.

## 1. In plain English

On Haiku, when we planted a number in the conversation as the model's own earlier answer, the rating it said another person, Sam, would give (Sam had seen neither answer) moved further toward that number than the model's own new rating did. That is odd: if Sam's rating were just the model's own view carried over, it should move no more than the model's own. But the extra movement came only from numbers planted above the model's usual rating, which could be a quirk of the scale rather than anything about other minds. This bet runs the same conversations on Sonnet 5.5 and Opus 5.5, twice per cell, and asks the question separately for numbers planted above and below. A hit means that on at least one of the two models Sam's rating moves further than the model's own in both directions. If Sam moves less than the model's own, the Haiku result is killed cleanly on that model. The rival explanation the design cannot remove is wording: "give your rating again" and "what would Sam give" are different questions.

## 2. Material

- **Models and settings** (as om-p2-6r): `claude-sonnet-5-5`, `{"thinking": {"type": "between_tools"}}` (Sonnet 5.5 rejects "disabled"), max_tokens 200; `claude-opus-5-5`, `{"output_config": {"effort": "low"}}` (Opus 5.5 cannot turn thinking off), max_tokens 4000. Structured output program 1's `RATE` schema `{"probability": integer}`, values clipped to 0–100. No system prompt.
- **Items, anchors, cells, conversation, questions:** om-p2-5's, unchanged, imported from `experiments/p2_5_egocentric.py` (`cells`, `messages`, `question`): program 1's 16 vignettes × 2 statements, anchor m = Haiku's run-2 first-turn mean (`exp4-run-3-anchors.json`), V = clip(m + d, 2, 98) for d ∈ {±10, ±30, ±60}, cells with |V − m| < 5 dropped (25 statements for each negative d, 31 for each positive d). The anchors are Haiku's for both models: m is "the number shown as its usual answer", and uptake is measured from each model's own REF cell, not from m.
- **Cells run** (each × 2 repeats, each model): REF (own = m, Alex = m), questions `self` and `sam_p`: 64; OWN (own = V, Alex = m), `self` and `sam_p`: 336; SWAP (own = m, Alex = V), `sam_p` only: 168. 568 prompts a repeat, 1,136 calls a model, 2,272 in all. om-p2-5's `sam_i` and `sam_inf` questions and the SWAP `self` cells are not run (budget; none enters this bet's rule).
- **Seed** (operators/hardware.md): CURBY-Q latest completed round **28297**, result pulse 2025-08-22 13:42 America/Denver (checked 2026-11-05 09:55 with `experiments/curby_seed.mjs check`, before this commit): stalled. **Seed: the first CURBy-RNG pulse timestamped after this commit.** seed = the first 8 bytes of SHA-256(randomness ‖ `om-p2-5r` ‖ ":" ‖ purpose) by `ledger/seed.py --purpose`, two purposes: `order` (its seed32 seeds the within-repeat permutation of the 568 prompts, the same for both models) and `boot` (its seed32 seeds the bootstrap). *Filled in by the seed commit, before any call:*
  `chain:` CURBy-RNG · `pulse index:` 1592495 · `pulse_time:` 2026-11-05 10:11:00 America/Denver · `previous pulse time:` 10:10:00 (index 1592494, before the 10:10:34 commit) · `randomness:` 1f2e67c928021ae5a33d3db212c30ffc65842b64d2390f8eb3c3eb5b96dbff332b7cb4cdf537615d0040856d35ab3eb29ec92e9797cc022ac8dd9f1110039e79 · `client:` @buff-beacon-project/curby-client@1.2.0 via `experiments/curby_seed.mjs` · `certificate_verified:` false · `seed (order):` 17032111488475197643 · `seed32 (order):` 2775183563 · `seed (boot):` 17171329045277636285 · `seed32 (boot):` 18806461. Record: `data/p2-5r-seed.json`.
- **Scale:** one direction in every prompt, 0 = certainly false, 100 = certainly true.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | Sonnet 5.5, 568 prompts × 2 repeats | 1,136 | $0.98 |
| 2 | Opus 5.5, the same | 1,136 | $2.80 |
| | total | 2,272 | $3.78 (cap $5.00) |

- Sonnet runs first; Opus runs only if Sonnet's run completed (a refusal, error or cap stop on Sonnet means no Opus call). Within a model, the repeat index is outermost.
- Every call is cached in `results/p2-5r-calls.json`, keyed by job, with a SHA-256 of model, settings, max_tokens and messages asserted on every hit and re-checked before the analysis.

## 4. Statistics

- **Cell value:** the mean of the 2 repeats; a cell with a repeat missing or refused is absent; a vignette with any absent cell is incomplete.
- **Uptake** of a displaced cell for question q: u = (y_cell − y_REF(q)) / (V − m).
- **U(cond, q, sign):** the mean over the three distance classes of the pooled mean uptake in that class, for upward (d > 0) or downward (d < 0) plants; "both" averages the six (sign, class) means.
- **Primary statistics, per model:** **gap_up** = U(OWN, sam_p, up) − U(OWN, self, up) and **gap_down**, the same for downward plants.
- **Uncertainty:** 95% percentile bootstrap, 4,000 resamples of complete vignettes with replacement (seed32 boot), every statistic recomputed per resample.
- **Secondary (reported, never promoted):** gap pooled over both signs; own and Sam uptake by sign; Sam's uptake of Alex's number (SWAP) and Sam's own-minus-Alex difference; the same statistics restricted to statement-classes kept in both directions; the Haiku archive (om-p2-5, 5 repeats) through the same code, as a reference column.
- **Multiple comparisons:** the bet is one conjunction per model, read on two models with "at least one" (no correction; the dry run's false-pass rates are the check: about 0 when Sam equals own). Secondaries uncorrected and descriptive.
- **Robustness committed now:** leave-one-vignette-out per model, each re-applying the model's reading.

## 5. Pre-registered reading

Per model, in order (`reading()`; EPS 1e-9):
1. **untestable_few:** fewer than 12 of 16 vignettes complete.
2. **untestable_nothing_moved:** neither U(OWN, self, both) nor U(OWN, sam_p, both) has its lower bound above 0.
3. **pass:** gap_up and gap_down each have their lower bound above 0.
4. **up_only** / **down_only:** only one of them does.
5. **reversed:** the pooled gap's upper bound is below 0 (Sam moves less than the model's own).
6. **none:** otherwise.

A model not run (Sonnet stopped, so Opus never started) or stopped mid-run is **not_run**.

**The bet:** **pass** if at least one model reads pass; **fail** if at least one model is tested (any reading other than untestable or not_run) and none passes; **untestable** if no model is tested. Pass is reported as **pass, unreplicated** beyond the model(s) that passed. Outcome 1 for pass, 0 for fail; untestable is not scored.

**Leave-one-out:** if dropping one vignette changes a model's reading, the frozen fragile sentence is appended ("On {M}, the reading depends on one vignette: removing {vid} changes it to {to}."); the reading stands.

**Frozen sentences** (`SENTENCES` in the code), the only plain-English sentences the write-up uses for the verdict:
- pass: "On {M}, on program 1's 16 vignettes, the rating the model attributed to Sam, a person who had seen neither its planted earlier answer nor another reader's, moved further toward that planted answer than the model's own re-rating did, both for answers planted above its usual rating (Sam minus own {gu}, 95% interval [{gul}, {guh}]) and for answers planted below it ({gd}, [{gdl}, {gdh}])."
- up_only: "On {M}, Sam's rating moved further toward the model's planted answer than its own re-rating did only for answers planted above its usual rating ({gu}, [{gul}, {guh}]); for answers planted below, the gap was {gd} [{gdl}, {gdh}], not detectably above 0." (down_only mirrors it.)
- reversed: "On {M}, Sam's rating moved less toward the model's planted answer than the model's own re-rating did (Sam minus own, both directions together, {g}, 95% interval [{gl}, {gh}], wholly below 0)."
- none: "On {M}, this test did not show Sam's rating moving further toward the model's planted answer than its own re-rating in either direction (upward {gu} [{gul}, {guh}]; downward {gd} [{gdl}, {gdh}])."
- untestable_nothing_moved, untestable_few, not_run, and the three bet sentences: as in the code.

None says "false consensus", "curse of knowledge", "theory of mind" or "belief".

**Reported in every case:** the per-model table (own, Sam, gap by sign and pooled; SWAP), readings, leave-one-out flips, calls, cost, refusals, and the Haiku reference column.

## 6. What it cannot do

- **Wording.** Own and Sam answer different questions ("give your rating again" vs "what would Sam give"); a gap may belong to the wording (the om-p2-5 audit's rival; P2-17 tests it). A pass is reported as "Sam's rating moved further", never as attribution.
- **Anchors** are Haiku's usual ratings, not Sonnet's or Opus's; the planted displacement V − m is from Haiku's m. Uptake is measured from each model's REF cell, but "above its usual rating" means above Haiku's usual rating for that statement.
- **Clipping.** Low anchors clip at 2, so downward classes hold fewer statements (25 against 31); the both-directions secondary restricts to statement-classes kept in both.
- Two models, one item set, two repeats; settings and repeats differ from Haiku's run. No "every", "all" or "models".

## 7. Stop rules

- Caps in code: $5.00 total, $1.50 Sonnet, $3.50 Opus. A cap stop on Sonnet means Opus is not run; a cap stop on Opus leaves Opus `not_run` if its repeats are incomplete.
- Stop on any refusal; no rewording; no retry; nothing re-sent to another model.
- Any other API error stops the run; it is resumed from cache only after the error is recorded, never past a refusal.

## 8. Ledger entry

Appended in the commit after the seed commit: id `om-p2-5r`, direction P2-5r, engine odds 0.12 (prior 0.32, adjustment −0.20, `odds_template` v2), human odds null ("no human odds"), budget $5.00, models Sonnet and Opus, lesson `ls-om-p2-5r`.

## 9. Checklist before the first call

- [x] This file is committed on its own; nothing has been run.
- [x] Lesson after reading the ledger (`ls-om-p2-5r`).
- [ ] Design review go (or fix-first confirmed); `gate()` enforces it.
- [x] Cockpit card committed before this file (`9099bdd`); `human-odds.jsonl` read immediately before this commit.
- [x] Engine odds from a fresh rule-14 context before this commit.
- [x] §5 rule applicable by a stranger; sentences frozen in code.
- [x] Pre-mortem one sentence with its kind.
- [x] Seed rule in §2; seed commit before any call.
- [x] Budget and stop-on-refusal in code; budget ruling br-010.
- [x] DEVIATIONS.md D18.
