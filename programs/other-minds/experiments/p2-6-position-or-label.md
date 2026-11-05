# P2-6. Is "own" a position or a label? (pre-registration)

Written and frozen in its own commit; the commit's author time (America/Denver) is the freeze time (D3, D6). Before any call. DEVIATIONS.md D11. Budget **$0.80**, enforced in code (`CAP` in `experiments/p2_6_position_label.py`, checked under a lock before every call). Stop on any refusal: the request ID goes to `results/refusal.md`, nothing is reworded or retried, and no later run starts on a cache that holds a refused call. **No call runs before the design review says go** (oversight-testbed `operators/design-review.md`); the code's `gate()` refuses to call until the review file says `go`, or `fix-first` with `confirmed_at` set, and the seed file exists.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision, in a terminal, a chat or a question dialog. His odds come only from `ledger/human-odds.jsonl` (the cockpit's downloads, committed); if a direction has no line there when its bet is pre-registered, the bet proceeds marked "no human odds". A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit. Sean's judgment is recorded and scored as steers in `ledger/steers.jsonl`: seed questions, vetoes, added questions and architecture decisions.

## 0. The bet

| field | value |
|---|---|
| bet id | `om-p2-6` |
| referee | `model` |
| bet type | `standard` |
| direction | P2-6 (`map/program-2-map.md`, rank 6) |
| source | literature + program 1: P1 (bm0/bm1's own/other caveat) + L (B13, B18, D34, B6, B16), as the map states |
| engine odds, P(pass) | **25**, revised before data by this bet's lesson, from **35** (the map's P2-6 odds, in `map/program-2-map.md` at `11de687`, 2026-11-04 17:12; copied, not restated). Both kept: `engine_odds_first` 0.35, `engine_odds` 0.25. The map gains a line saying so in this commit. The event is §5 rule 2. |
| human odds, P(pass) | no human odds: `ledger/human-odds.jsonl` has no line for P2-6 (it is empty at this commit). Never asked for. |
| budget | $0.80 API · 0 QPU s · minutes of laptop time |
| lesson | Correcting P8, P3 and P1: program 1's own-versus-other gap also differed in wording and turn, and om-p2-3b's own-labelled answer pulled less than another reader's. This bet fixes one wording, crosses turn with label, needs the label effect to beat the position-only baseline by 0.15, and its odds are 25% (from 35% on the map) because om-p2-3b reversed the own pull. Read: 14 scored bets, Brier 0.246, base rate 5/14 (running 6/16 = 0.375), newest audit ledger/audits/ss-b1.md. |
| design review | pending. Before the first call, a fresh auditor dry-runs this design (oversight-testbed `operators/design-review.md`) → `ledger/design-reviews/om-p2-6.md`, verdict go / fix-first / redesign. No call runs before a go. |
| pre-mortem | "If this fails, the most likely reason is that Haiku takes up a value by the turn it sits in, not by whose it is said to be: label effect under 0.15 in both turns." Kind: `world`. Checkable: L_A = AY − AS and L_U = UY − US both below 0.15, and |P| ≥ 0.15. |
| auditor | fresh session per oversight-testbed `operators/auditor.md`, after results, in a stripped clone with a sealed plant draw (`operators/plant.md`) |

**What the lesson rests on** (read at oversight-testbed `dd7cab3`, 2026-11-04 19:51): `ledger/bets.jsonl` (36 bets; 14 scored, 5 hits; program 2: om-p2-1, om-p2-2 and om-p2-3b scored, 0 hits; om-p2-3 untestable; om-p2-4 undetermined), `ledger/brier.md` (engine Brier 0.246 on 14; always the observed hit rate 0.230; running base rate (5 + 1) / (14 + 2) = 0.375), `ledger/audits/` (newest: `ss-b1.md`, `cdce1ba`; and `om-p2-3b.md`, whose "What would break it next" names this test: "P2-6's format-matched contrast (own versus other in the same turn and format)"), `ledger/audits/SUMMARY-2.md` (cross-cutting findings 1–3) and `ledger/lessons.jsonl` (P1–P10, and the scored lessons ls-om-p2-3b and ls-ss-b1). How each pattern applies:
- **P8 (comparing across conditions that differ in more than the named factor):** program 1's own and other conditions differed in label, position and wording ("give your rating again" against "accept or revise"). Here every cell uses one request sentence, one value string and one label sentence that differs only in its owner word; position is crossed with label. What still differs between positions is listed in §6, and the verdict sentences speak of "the turn it sits in", the bundle, never of a narrower cause.
- **P3 (no dumb baseline):** the dumb predictors are a constant uptake (copy any number), a one-bit position predictor (bm0's own 0.44 in the assistant turn, other −0.11 in the user turn) and a recency predictor. Each predicts a label effect of 0. The rule asks the label effect to beat them by a margin of 0.15 with its CI above 0, and to exceed the position effect. The dry run (§4) puts each through the rule: each passes in at most 1% of 200 simulated runs.
- **P1 (odds too high on a story) and its overcorrection (ls-ss-b1 scored: moving toward the pooled rate hurt there):** the odds move *away* from the running base rate (0.375), down, for a reason from the ledger, not from a story: om-p2-3b (audited, stands) found that a planted answer labelled as Haiku's own, in its own turn, pulled behaviour less (+0.060) than the same answer credited to another reader in the user turn (+0.114). That is the one ledger result where own and other were closer to matched than in program 1, and it went the wrong way for the label account. Program 2 also stands at 0 hits in 3 scored bets. Against that, bm0's own-minus-other at ±30 was +0.55 [+0.26, +0.92]; if all of it were label, this bet would pass (dry run: pass rate 1.00). So 35 → 25, not lower.
- **P9 (wrong noun):** every verdict sentence is written below in §5 and frozen in the code (`SENTENCES`); the results file's plain English uses only these, with numbers filled in.
- **P10 (one item decides):** leave-one-item-out re-applies the full rule; §5 says what happens on a flip.
- **P2 (power):** not a null rule, but the power of the pass rule is computed from bm0's archived item spread (§4).
- **P4 (manipulation never took effect):** the dry run prints the conversation each cell sends and checks that the cells differ exactly as stated (§4).
- **P7 (unpiloted execution risk):** these are program 1's 16 everyday probability vignettes (Linda the bank teller and its kin), already run in about 9,000 Haiku conversations by bm0 and bm1 with no refusal. No pilot is needed; the stop rule stands.
- **P5, P6:** no rival model families; the baseline cell is a measurement, not a control band. They do not apply.

## 1. In plain English

**The question.** Program 1 found that when a number is put in Haiku's own previous turn as its "earlier answer", Haiku moves its new rating most of the way to it (it takes up 44% of a 30-point displacement). When the same number is credited to "another person", it does not move (−11%). That looked like the model treating its own record as a commitment. But the two conditions differed in three ways at once: whose answer it was said to be, where the number sat (in the assistant's turn or in the user's message), and the wording of the request. So it is open whether the pull is about the **self** (the label "yours") or about the **position** (the model continuing whatever is in its own turn).

**What we do.** The same 16 items and the same ±30-point displacements as program 1. One request wording in every cell: "Please give the rating again." The number appears either in the assistant turn or inside the user's message, and is labelled either "your earlier answer" or "Sam's earlier answer". A fifth cell has the user say it was "my earlier answer". A sixth, with no number shown, measures Haiku's own rating, which the uptake is measured from.

**What would count.** If the label matters (yours pulls more than Sam's, by at least 15% of the displacement, averaged over both positions, and more than the position matters), the bet passes. If the position matters as much or more, or neither matters, it fails. The engine leans toward position: the model may simply continue its own turn whatever the label says, and om-p2-3b found an answer labelled as the model's own pulling *less* than another reader's.

**What it cannot say.** It is one model, one item set and one wording. A label effect could come from distrust of the stranger "Sam" rather than from the self; the fifth cell (the user's own answer) is there to tell those apart, as a secondary reading.

## 2. Material

- **Model:** `claude-haiku-5-5`, thinking disabled, structured output `{"probability": integer}`, `max_tokens` 200, default temperature (bm0's settings, through `om_common.structured`).
- **Items:** program 1's 16 exp4 vignettes, two statements each (X, Y), `programs/entangled-mind/experiments/exp4-items.json` (licences as recorded there). All 32 statements, no selection.
- **Shown values:** A = clip(round(m) + d, 2, 98), d = ±30, with m the archived anchor mean (`programs/entangled-mind/experiments/exp4-run-3-anchors.json`, fields `m_X`, `m_Y`), exactly bm0's V(). Fields read from archives: those two files only, for the item text and m. No program-1 result is read for analysis.
- **The six conversations** (verbatim builders in `messages()`; ASK = "{context}\n\nOn a scale from 0 to 100, where 0 = certainly false and 100 = certainly true, how likely is it that {statement}? Give only the number."; VAL = `{"probability": A}`; REQ = "Please give the rating again. On a scale from 0 to 100, where 0 = certainly false and 100 = certainly true, how likely is it that {statement}? Give only the number."):
  - `base`: [user: ASK]
  - `AY`: [user: ASK] [assistant: VAL] [user: "The answer above is your earlier answer. " + REQ]
  - `AS`: [user: ASK] [assistant: VAL] [user: "The answer above is Sam's earlier answer. " + REQ]
  - `UY`: [user: ASK + "\n\n" + VAL + "\n\n" + "The answer above is your earlier answer. " + REQ]
  - `US`: [user: ASK + "\n\n" + VAL + "\n\n" + "The answer above is Sam's earlier answer. " + REQ]
  - `UU`: [user: ASK + "\n\n" + VAL + "\n\n" + "The answer above is my earlier answer. " + REQ]
- **Repeats:** 20 per (statement, direction, cell) and 20 baseline calls per statement: 32 × 2 × 5 × 20 + 32 × 20 = **7,040 calls**.
- **Scale:** one direction, 0 = certainly false, 100 = certainly true, in every prompt.
- **Seed** (oversight-testbed `operators/hardware.md`): CURBY-Q's latest completed round is **28297**, result pulse 2025-08-22 13:42 America/Denver (checked 2026-11-04 19:43 America/Denver with `experiments/curby_seed.mjs check`, `@buff-beacon-project/curby-client@1.2.0`). That is more than 24 hours old: **CURBY-Q stalled (latest completed round 28297, 2025-08-22 13:42). Seed: the first CURBy-RNG pulse timestamped after this commit.** seed = the first 8 bytes of SHA-256(randomness ‖ bet-id), read as an unsigned big-endian integer; sub-seeds per purpose as `ledger/seed.py` derives them, purposes `order` (the run order within each repeat) and `boot` (the bootstrap; `boot` + 1 for the label-swap null). *Filled in by the seed commit, before any data* (`data/p2-6-seed.json`):
  `chain:` CURBy-RNG · `round:` pulse 1591640 (previous 1591639 at 19:55:00, before this file's commit at 19:55:35) · `pulse_time:` 2026-11-04 19:56:00 America/Denver · `randomness:` ee41b17e49e277942b9279a44cf3477ab6a91a96b3985bf74d09078c34d924ea9d947c326acdcad660856a6eca2b35fc9cfedef7caaa638021137d8d0819f347 · `client:` @buff-beacon-project/curby-client@1.2.0 · `certificate_verified:` false · `seed:` 97549812358230771; `order` 5841281319203805541 (seed32 1346672997); `boot` 72829155383338239 (seed32 535454975)

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | 20 repeats × (32 baselines + 32 statements × 2 directions × 5 cells) | 7,040 | about $0.35 (bm1's archived $4.7e-5 a call) |

- **Run order:** repeat index outermost (repeat 0 complete before repeat 1 starts, and so on); within each repeat, its 352 jobs in a beacon-drawn permutation (`--purpose order`). A stop leaves whole, balanced repeats; ten complete repeats are enough for the primary (§5.1).
- **Caching:** every call is cached in `results/p2-6-calls.json` under its job key with a SHA-256 of model, `max_tokens` and messages; every cache hit asserts the hash, and the analysis re-checks every entry. A crash never pays twice.

## 4. Statistics

- **Baseline:** b = mean of the 20 baseline ratings of a statement (0–1 scale). D = A/100 − b for each (statement, direction). A pair with |D| < 0.05 is dropped from every cell (bm0's rule; the same pairs in every cell).
- **Uptake per item and cell:** u = Σ (r̄ − b)·sign(D) / Σ |D| over the item's kept pairs, where r̄ is the mean re-rating over repeats. 1 = takes the shown value fully, 0 = ignores it, < 0 = moves away. (Ratio of sums, because single-pair ratios explode when |D| is small; bm0's item spread on this scale is SD 0.43 for one own-minus-other contrast.)
- **Primary statistic: the label effect** L = mean over items of ½[(u_AY − u_AS) + (u_UY − u_US)]. **Compared with it: the position effect** P = mean over items of ½[(u_AY − u_UY) + (u_AS − u_US)]. Unit of analysis: items (16).
- **Uncertainty:** percentile 95% CI from 2,000 bootstrap resamples of items, seeded by the beacon's `boot` sub-seed (32-bit), the same resample indices for every statistic.
- **The dumb baselines and the margin (P3):** constant uptake, a one-bit position predictor and recency each predict L = 0. The rule requires L ≥ 0.15 (beating them by a margin, not merely differing from 0), its CI lower end > 0, and L > |P|. Dry run (`experiments/p2_6_dryrun.py`, output `experiments/p2-6-dryrun-output.txt`, every call stubbed, synthetic data with bm0's item spread, 200 runs each): constant copy passes 1%, position-only (bm0's numbers) 0%, recency 0%, noise only 1%.
- **Power (from the same dry run):** with no position effect, the rule passes 40% of runs at a true label effect of 0.15, 88% at 0.25, 99% at 0.38 and 100% at 0.55 (bm0's whole own-minus-other gap). With label 0.25 and position 0.30 it passes 32%.
- **Split:** none; nothing is fitted.
- **Secondary statistics** (reported, never promoted): the five cell uptakes; the label effect in each position (L_A = AY − AS, L_U = UY − US) and their difference (interaction); in the user turn, user's minus Sam's (UU − US) and yours minus user's (UY − UU), read by the fifth-cell sentences in §5.5; a label-swap null (yours/Sam's swapped at random within item × position, 2,000 times, `boot` + 1): the share of swaps with L at or above the observed; the replication check u_AY against bm0's own uptake at ±30 (+0.44).
- **Multiple comparisons:** one primary rule, decided once. About ten secondary intervals are reported uncorrected and labelled secondary.
- **Robustness committed now:** leave-one-item-out (16 runs, each re-applying the full §5 rule with its own bootstrap); per-position label effects (unpooled); per-item table. No ties arise (means of integers; thresholds compared with a 1e-9 tolerance so an exact 0.15 counts as reaching it).

## 5. Pre-registered reading

Applied in this order by `verdict()`; the sentences are frozen in the code's `SENTENCES` and are the only verdict sentences the results file may use (numbers filled in as point [95% CI]).

1. **Untestable** (not scored): fewer than 10 complete repeats (a refusal, an error or the cap), or fewer than 12 of the 16 items with at least one kept pair. Sentence: "The test could not answer its question as run: {why}. No verdict is drawn."
2. **Pass** (scored 1): L ≥ 0.15 and the CI lower end of L > 0 and L > |P| (points). Sentence: "On Haiku, on program 1's 16 bm0 items at ±30 points, the label mattered more than the position. A value labelled "your earlier answer" was taken up more than the same value labelled "Sam's earlier answer", by {L} of the displacement on average over the assistant and user turns, against a position effect of {P}. On this design the pull of an earlier answer follows whose answer the transcript says it is more than which turn it sits in." Reported as **pass, unreplicated** (invariant 7).
3. **Fail, position** (scored 0): |P| ≥ 0.15 and the CI of P excludes 0 and |P| ≥ |L|. Sentence: "On Haiku, on program 1's 16 bm0 items at ±30 points, the position mattered at least as much as the label. A value in the {assistant/user} turn was taken up more than the same value in the {user/assistant} turn, by {|P|} of the displacement, while the label ("your" against "Sam's") changed uptake by {L}. On this design the pull of an earlier answer follows the turn it sits in, not whose answer it is said to be."
4. **Fail, reversed** (scored 0): L ≤ −0.15 and the CI upper end of L < 0 and |L| > |P|. Sentence: "On Haiku, on program 1's 16 bm0 items at ±30 points, a value labelled "Sam's earlier answer" was taken up more than the same value labelled "your earlier answer", by {−L} of the displacement (position effect {P}). On this design the label works against the model's own answer, the opposite of the self account."
5. **Fail, mixed** (scored 0): L ≥ 0.15 with CI lower end > 0, but not rule 2 or 3 (L ≤ |P| while P is not itself detected). Sentence: "On Haiku, on program 1's 16 bm0 items at ±30 points, the label changed uptake by {L} of the displacement, but the position effect, {P}, was as large, though not itself detected at the 0.15 bar. This test does not separate the two."
6. **Fail, neither** (scored 0): anything else. Sentence: "On Haiku, on program 1's 16 bm0 items at ±30 points, neither the label nor the position changed uptake by the pre-registered 0.15 of the displacement: label effect {L}, position effect {P}. This test does not say which of the two the pull of an earlier answer follows."

**Added in every case where they apply** (frozen sentences, appended after the verdict sentence):
- **No own pull** (when the CI lower end of u_AY ≤ 0): "The value labelled as the model's own and placed in its own turn was not taken up detectably (uptake {AY}), so program 1's own-answer pull did not replicate in this wording, and the comparison above splits an effect that was not present." The verdict stands as the rule gives it.
- **Fragile** (P10; when dropping one item alone changes the verdict category): "Dropping item {item} alone changes this verdict to "{v}", so it rests on that item." The bet is scored by the full-data rule; the label is then written "<verdict>, fragile (one item)".
- **The fifth cell** (secondary, one of three):
  - if UU − US ≥ 0.15 with CI lower end > 0 and the CI of UY − UU includes 0: "In the user turn, the user's own stated answer was taken up more than Sam's (by {UU − US}) and about as much as one labelled "yours" (difference {UY − UU}), so the label effect may be about Sam rather than about the self."
  - else if UY − UU ≥ 0.15 with CI lower end > 0: "In the user turn, a value labelled "yours" was taken up more than the user's own stated answer, by {UY − UU} of the displacement."
  - else: "In the user turn, the user's own stated answer could not be told apart from the other two labels (user's minus Sam's {UU − US}; yours minus user's {UY − UU})."

**Reported in every case:** calls made, cost, refusals, complete repeats, pairs kept and dropped, items usable; the five cell uptakes; L, P, L_A, L_U, the interaction, UU − US, UY − UU with CIs; the label-swap null; the leave-one-item-out range of L and the number of verdict flips; the per-item table.

## 6. What it cannot do

- **Position is a bundle.** Between the assistant and user cells, more differs than "which turn": the assistant cells are three messages with a prefilled assistant turn, the user cells one message; in the assistant cells the label and request are in a later message than the value, in the user cells the same one; and in the user cells the value sits nearer the request (recency). The verdict sentences say "the turn it sits in", meaning this bundle.
- **The label is one word in one sentence.** "Sam" is introduced nowhere. A label effect may be distrust of an unknown name rather than a pull of the self; the fifth cell gives a secondary reading, not a test.
- **One model** (Haiku), one item set (16 everyday probability vignettes), one displacement (±30), one wording. "Every", "all", "models" and "LLMs" will not appear in the write-up.
- **No mechanism words.** "Commitment", "belief", "self-model" and "memory" are not what this measures; it measures uptake of a shown number.
- **The baseline is this run's own unprompted rating**, not program 1's; the shown values are program 1's anchor means ± 30, so |D| may differ from 0.30.

## 7. Stop rules

- Budget cap in code: $0.80. If reached, the run stops; whole repeats completed before it are analysed (§5.1).
- Stop on any refusal: no rewording, no retry; the refused job is written into the cache, `results/refusal.md` is written with its request ID, and no later run starts on that cache. The primary is computed on the repeats complete at the stop, if at least 10.
- A stop on a non-refusal API error may be resumed from cache; the error is logged in the results.
- No call before the design review's go (or confirmed fix-first) and before the seed file exists (`gate()`).

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "om-p2-6", "program": "other-minds", "map": "program-2-map", "direction": "P2-6",
 "title": "Is \"own\" a position or a label? Assistant turn vs user turn x \"yours\" vs \"Sam's\", plus the user's",
 "source": "literature", "referee": "model", "bet_type": "standard",
 "engine_odds_first": 0.35, "engine_odds": 0.25, "engine_odds_at": "this commit (lesson ls-om-p2-6); 0.35 at 11de687",
 "odds_event": "label effect L = mean over items of 1/2[(AY - AS) + (UY - US)] >= 0.15, its 95% item-bootstrap CI lower end > 0, and L > |P| (position effect)",
 "human_odds": null, "human_odds_note": "no human odds",
 "prereg_commit": "<this commit>", "budget_usd": 0.80, "seed_source": "curby-rng", "beacon": null, "seed": null, "tiebreak": null,
 "lesson": "ls-om-p2-6", "design_review": {"path": "ledger/design-reviews/om-p2-6.md", "verdict": null, "commit": null, "reviewer_model": null, "fix_deviations": [], "missed": null},
 "premortem": "If this fails, the most likely reason is that Haiku takes up a value by the turn it sits in, not by whose it is said to be: label effect under 0.15 in both turns.",
 "premortem_kind": "world", "premortem_at": "<this commit>", "human_premortem": null, "human_premortem_kind": null,
 "failed": null, "failure_reason": null, "failure_kind": null, "premortem_score": null, "human_premortem_score": null, "risk_seen": null,
 "verdict": "open", "date": "2026-11-04", "test": "experiments/p2-6-position-or-label.md", "deviation": "D11",
 "result": null, "audit": null, "diagnosis": null}
```

## 9. Checklist before the first call

- [x] This file is committed on its own with its code and stubbed dry run; nothing has been run against the API.
- [x] The lesson row in §0 is filled after reading ledger/bets.jsonl, brier.md, audits/ and lessons.jsonl; the same sentence goes to `ledger/lessons.jsonl` as `ls-om-p2-6`.
- [ ] A fresh auditor's design review has returned **go**, or fix-first with every fix logged in DEVIATIONS and confirmed; `python3 ledger/check_prereg.py om-p2-6 . programs/other-minds/experiments/p2-6-position-or-label.md --before-run` passes.
- [x] Engine odds on record in the map before this commit (0.35, `11de687`); human odds: no human odds.
- [x] The pass rule in §5 can be applied by a stranger (`verdict()`).
- [x] The pre-mortem in §0 is one sentence, names a checkable mechanism, and carries its kind.
- [x] One scale direction in every prompt.
- [x] §2 records CURBY-Q's latest completed round and names the chain by the 24-hour rule; the seed commit follows this one before any data.
- [x] Budget and stop-on-refusal enforced in code.
- [x] DEVIATIONS.md row D11 added.
- [x] Commit message: `Pre-register om-p2-6: is "own" a position or a label? (D11)`.
