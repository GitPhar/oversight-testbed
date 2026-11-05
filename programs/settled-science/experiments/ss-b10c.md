# ss-b10c (direction ss-f8): the flattery rule on BrainBench in both option orders, read on the items not yet rated both ways (pre-registration)

Written and frozen 2026-11-05 10:37 America/Denver, in its own commit, before any new call. DEVIATIONS.md D70. It re-bets ss-b10b, withdrawn before any call by its design review (D68: half of Haiku's statistic was already in ss-b10's archive, so the rule would pass in 99–100% of runs, P12). Budget **$3.20**, enforced in code (`bettor/brainbench_b.py` `BET_CAP`, with Opus's `OPUS_CAP` $1.50 inside it; budget ruling br-009, carried from ss-b10b, which spent nothing; program cap $13.40). Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This direction's card went on the cockpit first (`f368453`, 10:09, no engine odds), before its map node (`b42b3d6`, 10:12) and this file. `python3 ledger/pickup_human_odds.py` and `python3 ledger/human_odds_match.py settled-science ss-f8` were run immediately before this commit: "no human odds". The card is on this branch; it reaches the live cockpit when the branch is merged into main.

> **One run, one scored bet** (Sean's decision 1, `operators/handoff-2026-11-05.md` §2). Opus's numbers, the forecasting prompt and every other secondary are reported rows, never separate bets.

> **Reuse, and what is scored.** ss-b10's 974 calls are reused wherever this design asks the same call (same model, prompt and user text, so the same content-hash key): Haiku flattery 300 of 400, Sonnet flattery 274 of 400, Haiku and Sonnet forecasting 200 of 400 each. The orders-averaged flattery accuracy on items ss-b10 already rated both ways is published (Haiku 75.0% on 100, Sonnet 85.8% on 74), so **the rule is read only on the items ss-b10 rated in one order: Haiku 100, Sonnet 126**, each completed now by one new call. The full 200 and the already-known half are reported rows. This is the ss-b10b review's fix (D11).

## 0. The bet

| field | value |
|---|---|
| bet id | `ss-b10c` |
| referee | `model`: a language model's ratings, scored against BrainBench's published labels (which abstract is the original), as ss-b10 |
| bet type | `standard` |
| direction | `ss-f8` (map/settled-science.json; programs/settled-science/map/settled-science.md, "Wave 4") |
| source | `literature` (the ss-b10 audit's "What would break it next", first item) |
| engine odds, P(pass) | **70**, from a fresh v2 context handed the committed dry run (`scoring/dry_b10c.py`, 06c1fff): prior 0.32, adjustment +0.38, reason "Committed dry run gives P(pass) 0.71-0.89, and the settled-science row (0.75) agrees; the model-referee (0.22) and literature (0.13) rows argue against, so I shaded toward the dry run's lower end." ss-b10b's 78 (map b42b3d6) was for the withdrawn rule; both kept. |
| human odds, P(pass) | no human odds (`ledger/human_odds_match.py settled-science ss-f8`, before this commit; card f368453 posted minutes earlier and not yet on the live cockpit) |
| models | `claude-haiku-5-5` and `claude-sonnet-5-5` (the rule); `claude-opus-5-5` as a secondary on as many items as $1.50 allows (rule 12; it cannot turn thinking off, so it runs at effort low, D18, at about 40 times Haiku's cost per call here). |
| budget | $3.20 API: Haiku 300 new calls about $0.08, Sonnet 326 new calls about $1.62 (ss-b10's measured $0.00025 and $0.00497 per call, as its audit asked), Opus up to $1.50 (estimated $0.0115 per call, about 32 items at four calls each; not measured, so the Opus count is whatever the cap allows). 0 QPU s, 0 laptop hours. |
| prior work | BrainBench (Luo et al. 2024, *Nature Human Behaviour*, arXiv 2403.03230; read for ss-b10): LLMs 81.4%, 171 neuroscientists 63.4%, models scored by perplexity (no option order), controls for local and shuffled context, none for valence, flattery or position. Lee 2026, "LLMs Have Made Failure Worth Publishing" (arXiv 2604.06236, HTML v1 read 2026-11-05): proposes, without data, testing whether LLMs overestimate success on 200–500 completed ClinicalTrials.gov trials, with and without failure records in context, plus a cross-field publication-bias correlation and an OpenReview comparison; it does not mention BrainBench or a valence shortcut. No prior statement of an order-balanced flattery rule's score on BrainBench was found (search: the ss-b10 and ss-b5 novelty searches of 2026-11-05 and this paper's protocols). Predicts: unknown. **What this bet adds:** ss-b10's audit's overturning test, with the position habit removed, scored only on information not yet seen, plus a third model. |
| lesson | "Correcting P12, P8: ss-b10b's rule included ratings already published, so its outcome was known before it ran. This bet reads the rule only on items ss-b10 rated once, completed in the other order, with an archive-built dry run, and its odds are 70% (from 78% on the map) because that dry run gives 0.71–0.89." |
| design review | before the first call, a fresh auditor dry-runs this design (operators/design-review.md) → `ledger/design-reviews/ss-b10c.md`. No call runs before a go. |
| pre-mortem | "If this fails, the most likely reason is that Haiku's new reversed-order ratings flip more items away from the original than the checked half did, leaving its 100-item lower bound under 0.634." Kind: `world`. |
| auditor | fresh session per operators/auditor.md, after results |

## 1. In plain English

BrainBench (Luo et al., 2024) shows a real neuroscience abstract beside a copy an expert rewrote so the results come out differently. Language models picked the real one 81.4% of the time and neuroscientists 63.4%, read as "AI beats experts at predicting science."

In ss-b10 we asked two Claude models a question that needs no knowledge of results: which version is better news for the paper's own idea? Sonnet picked the real abstract 81.8% of the time; Haiku 68.0%, short of the experts. But Haiku mostly picks whichever version it is shown first: right 92.9% of the time when the real one came first and 44.1% when it came second. One order per item could not see past that habit.

So now every item is shown both ways round, and the two answers are averaged, which cancels a first-position habit. Because ss-b10 had already rated half the items both ways, the test is read only on the other items (Haiku 100, Sonnet 126), where the second answer is new. **A hit means the "better news" question alone clearly beats the neuroscientists' 63.4% on those items, on both Haiku and Sonnet.** We also run the program's forecasting prompt both ways round on the same items, compare with the published 81.4%, keep five text-only rules beside them, and ask Opus on as many items as $1.50 buys. The rival explanation for a hit is memory: BrainBench and its abstracts were public before these models were trained. Another is plausibility: a model may pick the version that fits prior biology, which this question cannot separate from good news.

## 2. Material

- **Models and settings.** ss-b10's, unchanged (`bettor/brainbench.py`, imported): Haiku thinking `disabled`, Sonnet `between_tools` with no tools, max_tokens 1000; Opus adaptive at effort low, max_tokens 4000; structured output `{rationale, p_option_1}`.
- **Prompts.** `brainbench.FLATTERY` and `brainbench.BETTOR` with their user texts, unchanged (`brainbench.job`), so a call ss-b10 made has the same key.
- **Items.** BrainBench's 200 human-written items, `items/brainbench/items.jsonl` (SHA-256 `0a9acfeb…`, frozen at `e97fe46`). All 200, no filter.
- **Orders.** For every item and prompt, two calls: the original as Option 1 (`orig-first`) and as Option 2 (`orig-second`). No order draw.
- **Scored items.** Per model, the items whose flattery rating `bettor/bb-cache.json` holds in exactly one order (Haiku 100, Sonnet 126), fixed by the archive before any new call (`score_bbb.archived_orders`).
- **Opus items.** All 200 ids, sorted, then shuffled by the beacon sub-seed `opus-order`; Opus takes items in that order, four calls each (flattery and forecasting, both orders), until its cap. Its scored set is the items with both flattery orders (flattery) and with all four calls (the forecasting comparison).
- **Seed** (operators/hardware.md). CURBY-Q stalled: latest completed round 28297, result pulse 2025-08-22 13:42 America/Denver (checked 2026-11-05 09:58). Seed: the first CURBy-RNG pulse timestamped after this commit. seed = the first 8 bytes of SHA-256(randomness ‖ "ss-b10c" ‖ ":" ‖ purpose), unsigned big-endian (`ledger/seed.py --purpose opus-order`). The seed commit writes `bettor/bbc-seed.json`. *Filled in by the seed commit, before any data:*
  `chain:` ___ · `round:` ___ · `pulse_time:` ___ · `randomness:` ___ · `client:` @buff-beacon-project/curby-client@1.2.0 · `certificate_verified:` false · `seed:` ___
- **Archive.** `bettor/bb-cache.json` (ss-b10), read only; new calls go to `bettor/bbb-cache.json` and `bettor/bbb-opus-cache.json` (in `common.CACHES`). `bettor/bbb-ratings.jsonl` holds every rating used, each tagged `source: ss-b10 archive | ss-b10c`.
- **Published comparators.** 0.634 (experts) and 0.814 (LLMs, perplexity), from Luo et al. as read for ss-b10.
- **Scale.** One direction in both prompts: 1 = Option 2, 99 = Option 1, 50 = cannot tell or no difference.

## 3. Calls

| step | what | new calls | est. cost |
|---|---|---|---|
| 1 | Haiku, flattery, both orders (300 from ss-b10) | 100 | $0.03 |
| 2 | Sonnet, flattery, both orders (274 from ss-b10) | 126 | $0.63 |
| 3 | Haiku, forecasting, both orders (200 from ss-b10) | 200 | $0.05 |
| 4 | Sonnet, forecasting, both orders (200 from ss-b10) | 200 | $0.99 |
| 5 | Opus, both prompts, both orders, in the beacon order, until $1.50 | about 128 | up to $1.50 |
| | **total** | about 754 | about $3.20 (cap $3.20) |

- Run order as listed; steps 1 and 2 alone carry the pass rule, and run first, so no secondary can stop them (ss-b10b review D10-a). Opus runs with 2 workers, so calls in flight cannot carry it far past its cap (D10-b); its measured cost per call is reported. If a cap stops the run, later steps are reported as not run; step 5 stopping at its own cap is its design, not a stop. Each step's ending is recorded in `bettor/bbb-run-status.json`.

## 4. Statistics

- **Primary statistic, per model, on its scored items:** for each item, p_avg = the mean of the two flattery calls' probabilities on the original (each p_option_1 clipped to 1–99, divided by 100, or 1 minus that when the original is Option 2). The item scores 1 if p_avg > 0.5, 0.5 if p_avg = 0.5, 0 otherwise. Accuracy = the mean over the scored items (Haiku 100, Sonnet 126). Unit: the item.
- **Uncertainty:** percentile item bootstrap, 10,000 resamples, `default_rng(20261104)`, bounds at int(0.025n) and int(0.975n) − 1. **The bar is read on the item bootstrap.** A bootstrap over the five *Journal of Neuroscience* sections (P14; `score_f1.cluster_ci`) is reported beside it, with a sentence if it disagrees. Tolerance 1e-12 (P13).
- **Split:** none. Nothing is fitted.
- **D11 dry run, committed** (`scoring/dry_b10c.py`, P12, P15): each scored item's missing order is simulated from ss-b10's both-ways items (matched on order and single-order hit, or nearest 10 on probability), 2,000 runs: P(Haiku clears) 0.89 and 0.71, P(Sonnet clears) 1.00 and 1.00, so P(pass) 0.71–0.89 and P(fail) 0.11–0.29. The same simulation on all 200 gives P(fail) 0–1% (why ss-b10b was withdrawn).
- **Secondary statistics** (reported, never the verdict): the orders-averaged flattery accuracy on all 200 items, per model; the forecasting prompt's orders-averaged accuracy per model, the paired difference from flattery and the share matched (ss-b10's S1, S2), each against 0.814 (S3); per prompt and model, accuracy with the original first and second, the Option-1 pull, and counts right in both orders, first only, second only; the five text-only rules and the always-Option-1 rule (0.5 by construction); by section; the archive split (items whose two flattery orders were both in ss-b10's archive against the rest); Opus's flattery accuracy (both orders) on its items, its forecasting accuracy where all four calls ran, and Haiku's and Sonnet's flattery accuracy on the same items.
- **Multiple comparisons:** one conjunction (two models), no correction.
- **Robustness checks committed now** (P10, P14): leave-one-item-out and leave-one-section-out on each model's condition; a flip is reported in a sentence and does not change the verdict.

## 5. Pre-registered reading

Per model, "clears" means the orders-averaged flattery accuracy on its scored items has an item-bootstrap lower bound above 0.634. Sentences generated by `scoring/score_bbb.py` (`sentences`), verbatim:

1. **Pass:** both clear; **pass, unreplicated**. *"On the BrainBench abstract pairs that ss-b10 had rated in one order only (Haiku n, Sonnet m of 200), with each now shown in both orders and the two ratings averaged, a model asked only which version is better news for the paper's own idea picked the published abstract more often than the 171 neuroscientists in the original study did (63.4%), on both Haiku (a% [lo, hi]) and Sonnet (b% [lo, hi]); the published average for LLMs, scored by perplexity rather than by asking, was 81.4%. This design cannot tell whether the models answered by valence, by plausibility or from memory of the papers, and it does not show that the LLMs in the original study used such a rule."*
2. **Mixed:** exactly one clears; not a pass. *"… beat the neuroscientists' published 63.4% on <model> (a% [lo, hi]) but was not shown to on <other> (b% [lo, hi]), so even with the position habit averaged out this prompt beats the experts' published rate on one of the two models only."*
3. **Fail:** neither clears. *"… was not shown to beat the neuroscientists' published 63.4% on either Haiku (a% [lo, hi]) or Sonnet (b% [lo, hi]), so this valence prompt does not account for BrainBench's 'LLMs beat experts' result on these models. This says nothing about how the LLMs in the original study, other models scored by perplexity, reached 81.4%."*
4. **Untestable:** on either model, fewer than 90% of its scored items end with both flattery orders. *"Too few items were rated in both orders to test it (<model>: n of its m scored items with both orders; at least 90% needed)."*
5. **Reported in every case**, in this order after the main sentence: per model the all-200 row (*"On all 200 items in both orders (a reported row; half of it was in ss-b10's archive), <model>'s flattery accuracy was x% [lo, hi], which clears | does not clear the experts' 63.4%."*); per model the forecasting-prompt sentence (*"With the program's forecasting prompt instead (a different instruction, a question line, and a note that one version was altered by an expert), also in both orders, <model> picked the published abstract x% [lo, hi] of the time, d points more|less than with the flattery prompt (difference [lo, hi]); the flattery prompt's above-chance accuracy was s% [lo, hi] of the forecasting prompt's."*); per model *"<model>'s orders-averaged flattery accuracy was below | above | not shown different from the published 81.4% for LLMs (interval [lo, hi])."*; leave-one-out and section clauses; the text-only-rule sentence if any clears 0.634; the Opus sentence (*"Opus, asked the flattery question in both orders on n beacon-drawn items (as many as its $1.50 cap allowed; a secondary, not part of the rule), picked the published abstract x% [lo, hi] of the time; on the same items Sonnet's flattery rule was right y% and Haiku's z%, and Opus's forecasting prompt w% [lo, hi] on the m items where both of its prompts ran."*); always the memory, settings and reuse sentence (*"BrainBench and its source abstracts (Journal of Neuroscience, 2023) were public before these models' training data were collected, so either prompt may draw on memory of the benchmark or of the papers; Haiku and Sonnet ran with thinking off and Opus at its least-thinking setting, and the prompts asked for a rating, not the perplexity the original study used. Of each model's 400 flattery ratings, those in ss-b10's archive (Haiku 300, Sonnet 274) were reused, not asked again."*).
6. **Scoring for the ledger:** outcome 1 if pass, 0 if mixed or fail; untestable not scored. One scored bet. ss-b10 keeps its own verdict (mixed); this bet does not re-score it.

## 6. What it cannot do

- **Memory and plausibility.** Nothing here separates a valence judgment from recognising the paper or from prior biological plausibility (ss-b10 audit: 31 of Sonnet's 43 flagged words were "plausib…").
- **Averaging is a repair, not a test of judgment.** An item counts as right when the model's lean toward the original outweighs its lean toward Option 1; that is still the model's answer to one prompt.
- **One order known before data.** On every scored item one of the two flattery ratings is ss-b10's, already published; only the reversed-order rating is new. The rule reads items, not new calls, so the archive's known single-order hits (Haiku: right on 94% of its once-rated original-first items, 40% of original-second) shape the result; the dry run includes them.
- **Not the original study's method** (perplexity on base models), one benchmark, one wording of each prompt, one model family.
- **Opus is a small secondary** (about 30 items); its interval will be wide.
- No "LLMs", "every model" or "all" sentence will appear.

## 7. Stop rules

- Caps in code: $3.20 for this bet, $1.50 for Opus inside it, $13.40 for the program. If a cap stops steps 1–4, later steps are reported as not run.
- Stop on any refusal: no rewording, no retry, `results/refusal.md` written. Stop on any error or truncation. The ratings so far are written to `bettor/bbb-ratings.jsonl` on every exit path. ss-b10's archive is never written.

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "ss-b10c", "program": "settled-science", "direction": "ss-f8", "map": "map/settled-science.json",
 "title": "The flattery rule on BrainBench in both option orders, read on the items ss-b10 rated once (Haiku 100, Sonnet 126; Opus secondary)", "source": "literature",
 "odds_event": "On the BrainBench items ss-b10 rated in one flattery order only (claude-haiku-5-5: 100, claude-sonnet-5-5: 126), each completed in the other order and the two ratings averaged, for both models the flattery rater's accuracy has a 95% item-bootstrap lower bound above 0.634 (the published human-expert mean).",
 "engine_odds": 0.70, "human_odds": null, "prereg_commit": "<this commit>", "budget_usd": 3.20, "referee": "model",
 "bet_type": "standard", "seed_source": "curby-rng", "replication_of": "ss-b10", "rebet_of": "ss-b10b", "lesson": "ls-ss-b10c", "premortem_kind": "world", "verdict": "open"}
```

## 9. Checklist before the first call

- [x] This file is committed on its own; no new call has been made.
- [x] §0's prior work row states the prior work, what the April 2026 paper asked for, and what this bet adds.
- [x] The lesson row is filled after reading ledger/bets.jsonl, brier.md (37 scored, Brier 0.188, 12/37), audits/ (newest ng-p3-18.md; and ss-b10.md) and lessons.jsonl; the same sentence goes to `ledger/lessons.jsonl` as `ls-ss-b10c`.
- [ ] A fresh design review has returned go, or fix-first confirmed.
- [x] The card (`f368453`) was committed before this file; `ledger/human-odds.jsonl` was read immediately before this commit.
- [x] Engine odds on record earlier (map b42b3d6).
- [x] One scale direction in every prompt.
- [x] §2 records CURBY-Q's latest completed round; the seed commit follows this one before any data.
- [x] Budget and stop-on-refusal enforced in code.
- [x] DEVIATIONS.md D70.
- [x] The committed dry run shows P(pass) and P(fail) each at least 10% (D11).
