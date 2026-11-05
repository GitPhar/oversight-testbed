# ss-b14 (direction ss-f2): does the bettor beat always-50% and two shortcut rules on 60 more post-cutoff model-psychology findings? (pre-registration)

Written and frozen 2026-11-05 10:16 America/Denver, in its own commit, before any fetch, any item is built and any call. DEVIATIONS.md D64. Budget **$1.25**, enforced in code (`bettor/f2.py` `BET_CAP`, across its leakage and bettor caches; program cap raised from $8.95 to $10.20 by budget ruling br-008, `ledger/spend.jsonl`). Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). Sean answered this direction's card before 05:11 (`ho-20261105-051140-jc2`, 0.35, "would spend"); `python3 ledger/pickup_human_odds.py` and `python3 ledger/human_odds_match.py settled-science ss-f2` were run immediately before this commit. His line answers the card's event (the Opus bettor's Brier upper bound below 0.25), which is condition C1 alone; on template items a dumb rule clears that bar (ss-b4, withdrawn, P3), so this bet adds C2, C3 and a cluster bootstrap. His odds are scored on this bet's outcome; the card's event is a reported row.

> **One run, one scored bet** (Sean's decision 1, `operators/handoff-2026-11-05.md` §2). Haiku's and Sonnet's numbers and the card's event are reported rows, never separate bets.

## 0. The bet

| field | value |
|---|---|
| bet id | `ss-b14` |
| referee | `published-record`: each item's answer is the sentence its arXiv abstract contains |
| bet type | `standard` |
| direction | `ss-f2` (map/settled-science.json; programs/settled-science/map/settled-science.md) |
| source | `literature` (the ss-b1 audit's item 4) |
| engine odds, P(pass) | 45 on the map (remap one pass, not v2); **27 after the lesson**, from a fresh v2 context: prior 0.32, adjustment −0.05, reason "Settled-science (0.75) and published-record (1.00) rows pull up, but C3 cleared −0.01 by only 0.006 on 92 pairs; 60 items with 8–10 clusters widen that bound. Literature row 0.13." (prior.md at bd3bbb5; map b42b3d6). Both kept. |
| human odds, P(pass) | 0.35 (`ho-20261105-051140-jc2`, 2026-11-05T05:11:40), answering the card's event (C1 only); scored on this bet's outcome |
| models | `claude-opus-5-5` (the rule, as on the card; effort low, D18), `claude-sonnet-5-5` and `claude-haiku-5-5` (reported, thinking off); the flattery rater is `claude-opus-5-5`; the leakage checker `claude-sonnet-5-5` (round 2's). |
| budget | $1.25 API: leakage check about $0.35 (120 calls) to $0.46 (160); Opus bettor about $0.29, Opus flattery rater about $0.29, Sonnet about $0.13, Haiku about $0.01, on 60 items. 0 QPU s, 0 laptop hours. |
| prior work | Copied from the map and brought up to date: Wen et al. 2025 (arXiv 2506.00794) found off-the-shelf models at chance at predicting which of two AI-research ideas scores higher (GPT-4.1 51.4%; o3 near random), NLP experts 48.9%, a fine-tuned GPT-4.1 77% on post-cutoff pairs: for an untuned bettor on findings about models, that predicts **fail**, though its task (idea pairs) differs from calling a published direction. BrainBench (Luo et al. 2024, arXiv 2403.03230) found LLMs above experts in every neuroscience subfield, which predicts **pass** if the task transfers. Neither tests a valence or up-word shortcut. **What this bet adds:** the ss-b1 audit's named check of the bettor's weakest field, with model-free items, against the flattery rater that matched most of round 2 (ss-b6). |
| lesson | "Correcting P3, P14: the card's always-50% bar is cleared by the up-word rule on template items (Brier 0.177), and template items were bootstrapped as independent. This bet must beat the up-word rule and the Opus flattery rater by 0.01 on item and swap-pair bootstraps, and its odds are 27% (from 45% on the map) because ss-b6's edge over that rater was thin." |
| design review | before the first call, a fresh auditor dry-runs this design (operators/design-review.md) → `ledger/design-reviews/ss-b14.md`. No call runs before a go. |
| pre-mortem | "If this fails, the most likely reason is that the Opus bettor's Brier is not 0.01 below the flattery rater's on 60 items: as on round 2, picking the version that flatters the paper matches most of its skill." Kind: `world`. |
| auditor | fresh session per operators/auditor.md, after results |

## 1. In plain English

In round 1 the strongest Claude model, with no internet, picked which way new findings went 76% of the time, but in model psychology (research on how language models behave as minds, the field closest to itself) only 62%, not shown to beat a coin. The round-1 audit asked for 60 more such findings to check.

We take 60 new model-psychology papers posted after the models' training cutoff. A fixed template, with no model involved, takes one result sentence from each abstract and builds a twin with one comparative word flipped ("higher" for "lower"). A Claude checker drops items whose wording gives the answer away. The bettor (on all three models) says which sentence is the published one. **A hit means the Opus bettor beats three things**: always saying 50%, a rule that bets on the "higher / more / better" wording, and the same model asked only which version is better news for the paper's own method; the last two by more than 0.01 in Brier, on item and template-cluster bootstraps. The rival is that the bettor only picks the flattering version; the flattery rater is that rival, made into a predictor.

## 2. Material

- **Items, built after this commit and the seed commit, before any bettor call** (`bettor/f2.py`; `protocol/template-writer.md` unchanged):
  1. `--fetch`: round 2's model-psychology query and window, unchanged (`(cat:cs.CL OR cat:cs.AI) AND (abs:sycophancy OR abs:introspection OR abs:"theory of mind" OR abs:"self-report" OR abs:persona OR abs:"verbalized confidence")`, submitted 2026-07-01 00:00 to 2026-11-04 23:59, newest first), results 600–1799 in four requests of 300 (round 2 took results 0–599). Fetched once; never re-fetched.
  2. `--build`: drop any arXiv id already in the program (round 1 drafts, round 2's whole fetched pool, ss-b12's pool), a first version before 2026-07-01, or an ICML 2026 / TMLR comment (D12); then the template (`template_writer.item_from`: first candidate sentence after the first, 12–45 words, exactly one swap word, a result cue, no banned word, no negation) and `verify.check` as round 2.
  3. `--order`: every candidate in one fixed order from the beacon sub-seed `items` (sorted candidate ids, `random.Random(seed).shuffle`).
  4. `--leak`: round 2's leakage check (`items/leakcheck.py` prompt, `claude-sonnet-5-5`, thinking off; flagged → dropped, never rewritten) on the first 120 in that order; only if fewer than 60 are clean, on the next 40.
  5. `--freeze`: the first 60 clean items in that order (all clean if fewer, at least 50), ids f2-001… by arXiv id; `items/f2/items.jsonl`, `masked.jsonl`, SHA-256 in `items/f2/SHA256SUMS`, **committed before any bettor or rater call**. `--bet` checks the checksums first and makes no call on a mismatch.
- **Prompts.** Bettor: `bettor/bettor.py` `SYSTEM` and `user_text`, unchanged (round 2's question and methods lines are in each item). Flattery rater: `bettor/valence.py` `SYSTEM` (ss-b6's, D32), unchanged, user text `Field: model-psychology` and the two options, in the bettor's option order.
- **Models and settings.** `claude-opus-5-5` adaptive thinking at effort low (D18), max_tokens 4000; `claude-sonnet-5-5` (`between_tools`, no tools) and `claude-haiku-5-5` (`disabled`); structured output `{rationale, p_option_1}`.
- **Seed** (operators/hardware.md). CURBY-Q stalled: latest completed round 28297, result pulse 2025-08-22 13:42 America/Denver (checked 2026-11-05 09:58 with `bettor/curby_seed.mjs check`). Seed: the first CURBy-RNG pulse timestamped after this commit. seed = the first 8 bytes of SHA-256(randomness ‖ "ss-b14" ‖ ":" ‖ purpose), unsigned big-endian (`ledger/seed.py --purpose`). Purposes: `items` (the candidate order) and `order` (per item, whether option_b is shown as Option 1, `random.Random(seed).random() < 0.5` in id order; the same order for every model and the rater). The seed commit writes `bettor/f2-seed.json`. *Filled in by the seed commit, before any data:*
  `chain:` CURBy-RNG · `round:` pulse 1592501 (previous 1592500 at 10:16:00) · `pulse_time:` 2026-11-05 10:17:00 America/Denver · `randomness:` db284398d5db2c8329717cee93a103efa97a21c28375ceca9fa68067d7132ebea1f6c356e0bebd336f38fb8db085c8e823cd9f7c313afada2ed81521e486b9d3 · `client:` @buff-beacon-project/curby-client@1.2.0 · `certificate_verified:` false · `seed:` items 16180817909411768102, order 12026579425415227515 (`bettor/f2-seed.json`)
- **Up-word rule.** 0.75 on the option holding the template's up word (`up_side`), as ss-b5.
- **Scale.** One direction: 1 = Option 1 almost certainly not the published sentence, 99 = almost certainly it, 50 = cannot tell.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | leakage check (Sonnet), batch 1; batch 2 only if needed | 120 (+40) | $0.35 (+$0.12) |
| 2 | Opus bettor | 60 | $0.29 |
| 3 | Opus flattery rater | 60 | $0.29 |
| 4 | Sonnet bettor | 60 | $0.13 |
| 5 | Haiku bettor | 60 | $0.01 |
| | **total** | 360–400 | about $1.10 (cap $1.25) |

- Run order as listed; steps 1–3 carry the pass rule. If a cap stops the run, later steps are reported as not run. Every call cached by content hash (`items/f2/leakage-cache.json`, `bettor/f2-cache.json`, in `common.CACHES`). Each step's ending (complete, cap, refusal, error) is recorded in `bettor/f2-run-status.json`.

## 4. Statistics

- **Primary statistic, on the Opus bettor:** p_true = its probability on the published sentence (clipped 1–99). (C1) Brier; (C2) Brier minus the up-word rule's, item by item; (C3) Brier minus the flattery rater's (its p on the published sentence), item by item. Unit: the item.
- **Uncertainty:** a percentile item bootstrap (10,000, `default_rng(20261104)`, indices int(0.025n), int(0.975n) − 1) and **a template-cluster bootstrap** (P14: resample swap-word pairs, `score.swap_pair`, with their items; same seed and indices; `score_f1.cluster_ci`). **The bar is read on both.** Tolerance 1e-12 (P13).
- **Split:** none. Nothing is fitted.
- **Secondary statistics** (reported, never the verdict): accuracy; the card's event; Sonnet's and Haiku's numbers under the same rule; the swap-pair rule (D24) as a fourth comparator; the flattery rater's Brier, accuracy and up-word share; the share of published sentences with the up word; swap-pair counts.
- **Multiple comparisons:** one conjunction on Opus (3 conditions × 2 bootstraps), no correction.
- **Robustness checks committed now** (P10): leave-one-item-out and leave-one-swap-pair-out on the Opus label; flips reported in a sentence, never changing the verdict.

## 5. Pre-registered reading

"Meets the rule": C1 upper bound < 0.25, C2 upper bound < −0.01 and C3 upper bound < −0.01, on both bootstraps, with at least 50 items scored by the Opus bettor and by the rater. Sentences generated by `scoring/score_f2.py` (`sentences`), verbatim:

1. **Pass:** the Opus bettor meets it; reported as **pass, unreplicated**. *"On n model-psychology findings posted after its training cutoff (one sentence from each abstract beside its one-word flip, chosen by a fixed template; a Claude leakage checker dropped the ones whose wording gave the answer away), the Opus bettor beat always saying 50%, the up-word rule and a same-model rater asked only which version is better news for the paper's own method, the last two by more than 0.01 in Brier (<numbers>). In its weakest field the bettor's skill is more than these shortcuts; this does not separate knowing the result from reasoning within the sentence or recognising the published wording."*
2. **Fail:** it does not. *"On n post-cutoff model-psychology findings (template sentence pairs), the Opus bettor was not shown to beat always saying 50%, the up-word rule and a same-model flattery rater by the pre-registered margin (<numbers>), so in its weakest field the bettor's skill was not shown beyond these shortcuts."* Then *"It missed on <conditions>."*
3. **Untestable:** fewer than 50 clean items are frozen (no bettor call is made), fewer than 50 are scored by the Opus bettor or the rater, or any step ends in a refusal or error. *"Too few model-psychology findings were scored to test the bettor (items n; Opus bettor n; flattery rater n; at least 50 needed; <step>: refusal | error)."*
4. **Reported in every case:** leave-one-out clauses; Sonnet's and Haiku's lines (*"<model>, with the same prompt (reported, not the rule): …; it met | did not meet the rule."*); *"The cockpit card's event (the Opus bettor's Brier upper bound below 0.25, item bootstrap) was met | not met; on template items always-50% is a weak bar (the up-word rule's Brier here is x), so it is reported, not the rule."*
5. **Scoring for the ledger:** outcome 1 if pass, 0 if fail; untestable not scored. One scored bet.

## 6. What it cannot do

- **Knowing vs reasoning vs recognising.** A sentence can carry its own logic; and an earlier talk or workshop copy of a post-cutoff paper cannot be ruled out.
- **A Claude checker.** The leakage checker can drop but never write; still, which items survive depends on a Claude model's sense of leakage.
- **The flattery rater is one prompt** and the same model as the bettor; a bettor and rater from one model may share a sense of which version is real.
- **"Model psychology" is a query bucket**, not a curated field: some papers will be about personas in recommender systems or human self-report.
- **One model in the rule, one item set, one prompt.** No "LLMs" or "all" sentence will appear.

## 7. Stop rules

- Caps in code: $1.25 for this bet and $10.20 for the program; later steps reported as not run.
- Stop on any refusal: no rewording, no retry, `results/refusal.md` written, the bet untestable.
- Stop on any error or truncation (`llm._check_stop`). If the leakage check did not complete, nothing is frozen and no bettor call is made. A checksum mismatch at `--bet` stops before any call.

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "ss-b14", "program": "settled-science", "direction": "ss-f2", "map": "map/settled-science.json",
 "title": "60 more post-cutoff model-psychology template findings: the Opus bettor against always-50%, the up-word rule and the Opus flattery rater", "source": "literature",
 "odds_event": "On the first 60 (at least 50) leakage-clean post-cutoff model-psychology template items, the claude-opus-5-5 bettor's Brier upper bound < 0.25, and Brier minus the up-word rule's and minus the Opus flattery rater's each with upper bound < -0.01, every bound on both the item and the swap-pair-cluster bootstrap; Haiku and Sonnet reported.",
 "engine_odds": 0.27, "engine_odds_first": 0.45, "human_odds": 0.35, "human_odds_at": "ho-20261105-051140-jc2 (2026-11-05T05:11:40-07:00)",
 "prereg_commit": "<this commit>", "budget_usd": 1.25, "referee": "published-record", "bet_type": "standard", "seed_source": "curby-rng",
 "lesson": "ls-ss-b14", "premortem_kind": "world", "verdict": "open"}
```

## 9. Checklist before the first call

- [x] This file is committed on its own; nothing fetched, built or called.
- [x] §0's prior work row states predicted outcomes with citations and what this bet adds.
- [x] The lesson row is filled after reading ledger/bets.jsonl, brier.md (37 scored, Brier 0.188, 12/37), audits/ (newest ng-p3-18.md) and lessons.jsonl; the same sentence goes to `ledger/lessons.jsonl` as `ls-ss-b14`.
- [ ] A fresh design review has returned go, or fix-first confirmed.
- [x] The card was answered before 05:11 (dropped off as answered); `ledger/human-odds.jsonl` was read immediately before this commit.
- [x] Engine odds on record earlier (map b42b3d6, 10:12); human odds copied from `human_odds_match.py`.
- [x] One scale direction in every prompt.
- [x] §2 records CURBY-Q's latest completed round and names the chain by the 24-hour rule; the seed commit follows this one before any data.
- [x] Budget and stop-on-refusal enforced in code; items frozen with SHA-256 before any bettor call.
- [x] DEVIATIONS.md D64.
