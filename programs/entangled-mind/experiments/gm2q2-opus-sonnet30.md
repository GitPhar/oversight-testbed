# gm2q-f3: with only questions in the message, does question order still move the final rating on Opus, and on Sonnet across 30 new items, with no single item carrying it? (pre-registration)

Written and frozen 2026-11-05 10:20 (America/Denver; commit 1e0c9c1, author time 10:20:43; first written here as 10:40, a guessed time, corrected by D81 in the seed commit), in its own commit, before any call. DEVIATIONS.md D80. Budget **$4.00**, enforced in code. Stop on any refusal: the message ID goes to `results/refusal-gm2q2.md`, and nothing is reworded or retried.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision. His odds come only from `ledger/human-odds.jsonl`. The direction's cockpit card was committed first (`9da5349`, 09:58, no engine odds) and reached the live site with the push at about 10:00 (`bd3bbb5..e9ca120`); then its map node (`7bb7821`). `python3 ledger/pickup_human_odds.py` then `python3 ledger/human_odds_match.py entangled-mind gm2q-f3`, run immediately before this commit: "no human odds".

## 0. The bet

| field | value |
|---|---|
| bet id | `em-gm2q2` |
| referee | `model` (the models' ratings decide the outcome) |
| bet type | `standard` |
| direction | `gm2q-f3` (map/entangled-mind.json), under `gm2-f1` (bet `em-gm2q`); also follows `gm2q-f2` |
| source | `literature` (the em-gm2q audit's "What would break it next", candidate gm2q-f2, extended to Sonnet; Opus is the layer em-gm2q's pre-registration named next) |
| engine odds, P(pass) | **6** (v2, fresh context at this design: prior 0.23, adjustment −0.17, reason: "Literature row 0.07 and model-referee row 0.17. Both models must pass five gates with leave-one-out, and the parent's single-item, different-pattern effect matches dry-run worlds passing about 1%."; `ledger/prior.md` at `69fb813`). No odds were on the map before this elicitation. |
| human odds, P(pass) | no human odds (no line for gm2q-f3 in `ledger/human-odds.jsonl` at this commit) |
| models | `claude-opus-5-5` (gm2's 10 items) and `claude-sonnet-5-5` (gm2b's 30 further items), not Haiku, because Haiku's questions-only arm on gm2b's 30 items is its own open direction (gm2q-f2, $0.70) and this bet carries the two models the wave named: Opus, never tested, and Sonnet, the one model that passed em-gm2q. |
| budget | $4.00 API in code (Batches API, 50% of list price; planned about $3.6: Opus about $1.6, Sonnet about $1.9) · 0 QPU s · no local model |
| prior work | Order inside one prompt is known to move model outputs: Chen, Chi, Wang and Zhou 2024 (ICML, arXiv:2402.08939) found permuting premise order drops reasoning accuracy by over 30%; Guan et al. 2025 (arXiv:2502.04134) found shuffled inputs lower accuracy in closed models; Hamalainen 2025 (arXiv:2504.20444; ChatGPT, Gemini, Claude, versions unnamed) found list order shifts candidate ratings, model-dependently. That predicts the questions-only gate passes. No paper found compares a one-message order effect with a turn-by-turn chain on graded credences, or asks whether it spreads across items; em-gm2q (Haiku, Sonnet, 10 items, mixed, one item per model) is the only one. So parts (3)–(5) of the rule are unpredicted (predicts: unknown). Adds: Opus; 30 new items on Sonnet; no item allowed to carry it; a wrong-target check at both ends of the list. The odds (6%) sit far below "the gate passes" because the gate is one of five parts and both models must clear all five. |
| lesson | "Correcting P10, P9 and P15: em-gm2q's questions-only effect sat 82–88% on one item, its verdict noun outran the design, and Opus's archive mixes two batches. This bet puts leave-one-item-out inside the pass rule, flags first- and last-listed answers against the same order, builds Opus's dry run per batch, and its odds are 6% because both models must clear five parts." |
| design review | before the first call, a fresh subagent dry-runs this design (operators/design-review.md) → `ledger/design-reviews/em-gm2q2.md`. No call runs before a go. |
| pre-mortem | "If this fails, the most likely reason is that the questions-only effect again sits on a different item-and-order pattern from turn by turn, so the same-order wrong-target check empties a cell." Kind: `design`. |
| auditor | fresh subagent per operators/auditor.md, in a planter-built clone, after results |

## 1. In plain English

em-gm2q put four statements and a question in one message, with no answers in the conversation, and found that the order of the statements still changed the model's final rating on Haiku and Sonnet. But on each model about 85% of that came from a single topic, it fell on different topics and orders from the ordinary turn-by-turn effect, and the strongest model, Opus, was never tested. This bet asks the same question of Opus, on the same 10 topics, and of Sonnet on 30 topics it has never been asked, re-running the turn-by-turn version alongside each as the yardstick. A pass needs, on both models, an order effect with only questions in the message that is real, at least half the turn-by-turn one, not explained by answers sitting on the first- or last-listed statement, and still there when any one topic is left out. Prior work predicts that order inside one prompt matters (Chen et al. 2024; Guan et al. 2025); nothing predicts whether it matches turn by turn in size or spreads across topics, which is what this adds. The rival explanation the design cannot exclude is in §6: one message instead of five turns changes more than the presence of answers.

## 2. Material

- **Items.** Opus: gm2's 10 items (`experiments/gm2-planted-values.json`, `chain_claims` only). Sonnet: gm2b's 30 further items (`experiments/gm2b-planted-values.json`, the 30 not in gm2; `chain_claims` only; the planted values are not used). Question text and contentions from `results/pool-run-3.json`. Four sub-statements per item, as in gm2 and gm2b.
- **Orders.** gm2's Latin square O1–O4. The main question comes last in every order.
- **Conditions** (both models): **qonly**, one user message built by `gm2q_questions_only.qonly_message` unchanged (em-gm2q's wording), the model returns `{"rating": integer}` for the main question only; **shown**, gm2's turn-by-turn chain (`gm2q_questions_only.chain_turns` unchanged), each real reply kept in the history. No redacted arm. `python experiments/gm2q2_opus_sonnet30.py --print-prompts` prints both for one item per arm.
- **Repeats.** Opus 6, Sonnet 5 conversations per item × order × condition. Opus 240 qonly + 240 shown; Sonnet 600 qonly + 600 shown. 1,680 conversations, 5,280 requests.
- **Models and settings.** `claude-opus-5-5`, effort "low" (its thinking-off setting; Opus 5.5 cannot disable thinking; thinking text is never placed in a later turn), max_tokens 1000 (em-dm4's setting); `claude-sonnet-5-5`, thinking `{"type": "between_tools"}`, max_tokens 1000 (em-gm2q's and em-dm4's). Default temperature. Structured output `{"rating": integer}`, clipped to 0–100. **Batches API** at 50% of list price; each turn of every chain is one request in that round's batch (5 rounds; round 1 also carries every qonly request).
- **Missing answers.** A request that hits max_tokens or does not parse ends its conversation, which counts as missing. A model × condition with under 90% usable conversations, or any shown or qonly cell with fewer than 2 ratings, makes that model untestable.
- **Seed** (operators/hardware.md): CURBY-Q's latest completed round is 28297 (checked 10:16 with `DIRNGClient.latest()` via `experiments/curby_seed.mjs check`: stage randomness, result pulse 2025-08-22 13:42 America/Denver). That is far over 24 h old, so the chain is stalled. Seed: the first CURBy-RNG pulse timestamped after this commit. seed = the first 8 bytes of SHA-256(randomness ‖ "em-gm2q2" ‖ ":analysis"), unsigned big-endian (`ledger/seed.py --purpose analysis`), used mod 2^63. The analysis uses seed + 1 (shown gate), + 2 (qonly gate), + 3 (R bootstrap), + 6 (cleaned qonly gate), + 4 and + 5 (secondary ratios); leave-one-item-out uses the same offsets. Nothing in the run is random beyond the models' sampling. *Filled in by the seed commit, before any data:*
  `chain:` CURBy-RNG · `pulse_index:` 1592505 · `pulse_time:` 2026-11-05 10:21:00 America/Denver (2026-11-05T17:21:00.195Z; previous pulse 1592504 at 17:20:00.199Z, before this file's commit 1e0c9c1 at 10:20:43) · `randomness:` 56aa7c3e0434d7ff65bea544bff987c85a495e1628b76fbdc0597bcaa5c25314c441060862d0619327d968d67866bd8ac22fc745a9a77e8c541ef3501750be32 · `client:` @buff-beacon-project/curby-client@1.2.0 (Client.randomness(1592505), `experiments/curby_seed.mjs rng`) · `certificate_verified:` false (classical chain) · `seed:` analysis 8982550231960562870 (below 2^63, so unchanged mod 2^63)
- **Archives read** (dry run and reported secondaries only; all published): `results/mm-gm2-opus-conversations.json` (em-dm4, Opus shown chains on gm2's items), `results/gm2b-conversations.json` (Haiku shown and redacted chains on gm2b's 30 items), `results/gm2q-questions-only.json` (em-gm2q's Sonnet and Haiku shown OE and within-order SD).
- **Scale.** One direction, 0 = certainly false, 100 = certainly true, in every prompt (em-gm2q's openings).

## 3. Calls

| step | what | requests | est. cost (batch rate) |
|---|---|---|---|
| round 1 | every qonly request (Opus 240, Sonnet 600) and turn 1 of every shown chain | 1,680 | about $0.9 |
| rounds 2–5 | turns 2–5 of every shown chain | 3,360 | about $2.7 |

- Per-request estimates: shown from em-dm4's archived chains (Opus $0.0056, Sonnet $0.00263 per 5-request chain at the batch rate); Sonnet qonly from em-gm2q; Opus qonly unmeasured, set at $0.0015. Total about $3.6.
- **Cap in code.** Before the first batch, the whole run's estimate plus a $0.10 reserve must fit $4.00, or nothing starts. Before every round, the next batch's projected cost × 1.10 and the projected cost of everything remaining (observed per-request means once an arm has spent, never below the estimate), each plus the reserve, must fit; otherwise the run stops before that batch and the unfinished chains count as missing. Every finished conversation is cached by key in `results/gm2q2-conversations.json` after every batch; the billed cost of unfinished chains is kept under `_unfinished`. A resumed run never re-pays a finished conversation.
- Batch requests that come back errored or expired (API failures, not model outputs) are resubmitted unchanged, at most twice.

## 4. Statistics

Per model, on the final main rating of each conversation, with em-gm2q's code imported unchanged (`gm2q_questions_only.vc`, `oe`, `perm_p`, `ratio_boot`, `model_label`):
- **Order effect:** per item, VC = max(0, (MS_between − MS_within)/n) over the four orders; OE = √(mean over items of VC).
- **Shown gate:** permutation test of Σ_items MS_between in shown, order labels shuffled within item, 5,000 permutations, p = (1 + #{T* ≥ T − 1e-9})/5,001.
- **qonly gate (the dumb baseline, P3):** the same test in qonly. It rejects a world with no order effect, where the clipped estimator still gives OE > 0.
- **Wrong-target check (the second dumb baseline, P3; em-gm2q's D70 amended twice).** A qonly answer is flagged if it is nearer the mean shown sub-rating of the **first- or the last-listed** statement in that order than the **mean shown final rating in that same order**, and more than 20 points from that final. The **cleaned qonly gate** is the qonly gate on unflagged answers; if any cleaned cell keeps fewer than 2 answers, the model fails. Both amendments are stated in §6 and chosen from the dry run (§8).
- **Primary statistic:** R = OE_qonly / OE_shown (raw ratings, as em-gm2q), 2,000-resample item-bootstrap percentile 95% interval (resamples with OE_shown = 0 dropped and counted).
- **Leave-one-item-out, inside the rule (P10).** With each item left out in turn, every part of the per-model rule (both gates, the cleaned gate with its cell check recomputed on the remaining items, R's interval) is recomputed on the remaining items with the same seeds.
- **Every boundary** is compared with tolerance 1e-9 (P13).
- **Secondary (reported, never promoted):** OE in each condition; within-order SD; wrong-target shares; the cleaned cells below 2; the order-pattern correlation, shown against qonly; each item's share of the qonly between-order variance; R with flagged qonly answers dropped; R with every answer more than 20 points from the item's usual shown final dropped in both arms (the em-gm2q audit's cheapest overturn); archived OE (em-dm4 Opus shown, R = 4; Haiku's gm2b shown and redacted on the 30 items); the per-item table.
- **Multiple comparisons:** two models, each read on its own rule; the bet needs both. No correction: requiring both, and every leave-one-out set, is stricter than either.
- **Clusters.** Items are different questions from one pool with no shared template, so no cluster bootstrap (P14).

## 5. Pre-registered reading

Per model:
1. **Untestable:** under 90% usable conversations in shown or qonly, a shown or qonly cell with fewer than 2 ratings, or the shown gate p ≥ 0.05 on all items.
2. **Pass:** on all items, shown gate p < 0.05, qonly gate p < 0.05, cleaned qonly gate p < 0.05 (no cleaned cell below 2), and R's 95% lower bound ≥ 0.5; **and** with each single item left out, all of these again hold (a leave-one-out set where any part fails, including the shown gate, makes the model fail).
3. **Fail:** testable and not a pass. The code names the first failing part, in the order: qonly gate, wrong-target check (a cell below 2), cleaned qonly gate, ratio lower bound, leave-one-item-out (with the items whose removal breaks it).

The bet:
- **pass:** both models pass. Reported as **pass, unreplicated** (two models, two item sets, one wording).
- **mixed:** exactly one model passes.
- **fail:** both models testable, neither passes.
- **untestable:** no model passes and at least one is untestable.
- Scored outcome 1 for pass, 0 for mixed or fail; untestable is not scored.

Verdict sentences (P9), used verbatim, with only nouns the design can carry:
- **pass:** "With nothing in the message but the questions, their order moved the final rating on both Opus (gm2's 10 items) and Sonnet (gm2b's 30 further items) by at least half as much as answering them turn by turn, not through answers sitting on the first- or last-listed statement, and with no single item carrying it on either model. This shows an order effect of that size without answer turns; it does not show that it is the same effect as turn by turn."
- **mixed:** "With nothing in the message but the questions, their order moved the final rating by the pre-registered rule on <model> but not on <other model>, where the first failing part was <part>."
- **fail:** "With nothing in the message but the questions, neither Opus nor Sonnet met the pre-registered rule (first failing parts: Opus <part>, Sonnet <part>)." Then one sentence per model from this table: qonly gate → "the order of the statements did not detectably move the answer"; wrong-target check or cleaned gate → "the order effect could not be told apart from answers sitting on the first- or last-listed statement"; ratio → "the questions-only effect was not shown to be at least half the turn-by-turn one"; leave-one-item-out → "the effect depended on single items (<ids>)".
- **untestable:** "The turn-by-turn reference showed no order effect on <model(s)>, or too few answers were usable, so the rule could not be read there."

**Reported in every case:** usable shares, both gates, the cleaned gate, OE per condition, R with its interval, the leave-one-out labels and breakers, every secondary in §4, the cost, and the plain-English paragraph says if a single item's removal changed a label.

## 6. What it cannot do

- **Differences from em-gm2q (P8), all deliberate:** models (Opus new; Sonnet on new items); items (Sonnet's 30 have never been run on Sonnet in any condition); repeats (6 and 5, against 10); the Batches API (same model and parameters; batch and direct calls are not expected to differ, but the design cannot check it); no redacted arm; the wrong-target check also covers the first-listed statement (the em-gm2q audit's D5 miss); the flag's reference is the shown final in the same order, not the item's mean over orders; leave-one-item-out is part of the rule. So this bet is not a re-run of em-gm2q, and a different result from em-gm2q's on Sonnet cannot be pinned on any one of these.
- **Why the flag's reference changed.** With em-gm2q's item-mean reference, the dry run built from em-dm4's Opus chains (one batch whose order effect is 34 points, answers swinging between about 3 and 88 by order) flagged answers that agree with turn by turn in the same order, and Opus could not pass even when the questions-only effect equalled the turn-by-turn one (P(pass) 0.00, `results/gm2q2-dry-run.json` was rebuilt after the change; the first version's output is not kept). With the same-order reference it passes. The cost: a large questions-only effect on a **different** item-and-order pattern from turn by turn can now fail through the flag when its answers sit near the first- or last-listed statement (dry run "shuffled items": Sonnet 0.01, Opus 0.00). This is the case em-gm2q's audit could not separate from rating a listed line, and the rule now treats it as not separated.
- **The bundle.** qonly still differs from shown in four ways: no answers; one message instead of five turns; numbered statements; an opening that says to rate only the question. A pass shows an order effect with none of the answers present; it cannot say which of the four removes or keeps it.
- Opus on 10 items and Sonnet on 30, one pool, one wording, two models. "Every", "all" or "models" will not appear in the write-up. It cannot say why order matters (primacy, recency, a listed line read as the question); per-item order means are reported, not tested.

## 7. Stop rules

- Budget cap in code: $4.00 with a $0.10 reserve, checked before the first batch and before every round (§3). Rounds not reached are reported as not run, and their chains count as missing.
- Stop on any refusal: the job key, batch ID, message ID and stop details go to `results/refusal-gm2q2.md`; no further batch is submitted; nothing is reworded or retried; no later run starts while that file exists.
- A batch whose requests still fail after two unchanged resubmissions stops the run; the cache is kept.

## 8. Dry run (committed now, before any call; P12, P15)

`python experiments/gm2q2_opus_sonnet30.py --dry-run` builds worlds from measured archive numbers, draws ratings at this design's repeats, and applies the §5 rule including leave-one-item-out (100 runs per world; 400 permutations and bootstraps):
- **Opus**, from em-dm4's Opus shown chains on gm2's 10 items. Each cell there holds two batches that disagree (repeats 0–1 against 2–3: order effects 4.4 and 34.3 points, within-batch SD 3.5 and 4.9, against a pooled SD of 28.3), so each batch is its own world, A and B, with its within-batch SD (P15: measured, not pooled across batches).
- **Sonnet** on gm2b's 30 items: no Sonnet archive exists there. The per-item shown order deviations are Haiku's (gm2b, R = 10), scaled by Sonnet's to Haiku's shown OE on gm2's 10 items in em-gm2q's same-day run (5.5 / 9.0), with Sonnet's shown within-order SD from that run (7.7) and Haiku's statement means. This is an assumption about Sonnet's item pattern, stated here.

| world (questions-only order means) | Opus A | Opus B | Sonnet | bet (A × Sonnet) | bet (B × Sonnet) |
|---|---|---|---|---|---|
| null: no order effect | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| half the shown deviations | 0.10 | 0.00 | 0.10 | 0.01 | 0.00 |
| 0.75 of them | 0.49 | 1.00 | 0.83 | 0.41 | 0.83 |
| equal to shown | 0.62 | 1.00 | 1.00 | 0.62 | 1.00 |
| the archived redacted pattern | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| shown deviations, items shuffled | 0.00 | 0.00 | 0.01 | 0.00 | 0.00 |
| one item jumps, half elsewhere | 0.00 | 0.00 | 0.01 | 0.00 | 0.00 |
| equal, 20% of answers on the first or last line | 0.07 | 1.00 | 0.21 | 0.01 | 0.21 |

Every world can fail and the equal and 0.75 worlds can pass, so the bet can go either way (D11). It passes only when the questions-only effect is near the turn-by-turn one in size and pattern. In Opus world B a 20% share of first- or last-line answers does not stop a pass (the order effect there is 34 points, so the flag rarely fires); that is a limit of the check on a model with very large order effects. Output committed with this file as `results/gm2q2-dry-run.json`. `--selftest` checks the boundaries, the flag at both ends, a world that passes on all items and fails by leaving one item out, and the verdict table.

## 9. Ledger entry

Appended through `ledger/inbox/p1-wave3.jsonl` (`ledger/merge_inbox.py add bets …`) in the commit after the seed commit, with `prereg_commit` set to this commit's hash; the lesson `ls-em-gm2q2` the same way; the budget ruling in `ledger/spend.jsonl`.
