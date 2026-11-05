# ss-b13 (direction ss-f1): do Haiku and Sonnet, as bettors, beat always-50% and two shortcut rules on the findings Opus scored? (pre-registration)

Written and frozen 2026-11-05 10:13 America/Denver, in its own commit, before any call. DEVIATIONS.md D62. Budget **$0.70**, enforced in code (`bettor/f1.py` `BET_CAP`; program cap raised from $8.25 to $8.95 by budget ruling br-007, `ledger/spend.jsonl`). Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). Sean's odds come only from `ledger/human-odds.jsonl`. This direction was on the cockpit before 05:11 and he answered it (`ho-20261105-051140-ruf`, 0.65, "would spend"); `python3 ledger/pickup_human_odds.py` (10:00, nothing new) and `python3 ledger/human_odds_match.py settled-science ss-f1` were run immediately before this commit. His line answers the card's event, which is condition C1 alone; this bet's rule adds C2 and C3 (P3) and a cluster bootstrap (P14), so it is stricter for the bettors. His odds are scored on this bet's outcome, and the card's event is reported as a row (as om-p2-7 and ss-b11 did).

> **One run, one scored bet** (Sean's decision 1 in `operators/handoff-2026-11-05.md` §2, steer logged by Tab A). Every other number below (Sonnet alone, the card's event, round 2, Opus's archive) is a reported row and is never scored as a separate bet.

## 0. The bet

| field | value |
|---|---|
| bet id | `ss-b13` |
| referee | `published-record`: each item's answer is the direction its arXiv abstract reported |
| bet type | `standard` |
| direction | `ss-f1` (map/settled-science.json; programs/settled-science/map/settled-science.md, "Follow-ups (remap 2026-11-05)") |
| source | `engine` (the remap's rule-12 replication) |
| engine odds, P(pass) | 45 on the map (remap one pass, 2026-11-05T04:45, not v2); **18 after the lesson**, from a fresh v2 context: prior 0.32, adjustment −0.14, reason "Below settled-science (0.75) and published-record (1.00) rows despite them: Haiku and Sonnet must both clear good-news by 0.01 upper bound; Opus itself margined only 0.036." (prior.md at bd3bbb5). Both kept. |
| human odds, P(pass) | 0.65 (`ho-20261105-051140-ruf`, 2026-11-05T05:11:40), answering the card's event (C1 only); scored on this bet's outcome |
| models | `claude-haiku-5-5` and `claude-sonnet-5-5` new; `claude-opus-5-5` from the archive (bettor/bets.jsonl, r2-bets.jsonl), scored by the same code as a reference row. Rule 12 is met: the question is whether the smaller two match the archived Opus. |
| budget | $0.70 API (estimate $0.51 by characters; about $0.55 at round 1's measured Opus token counts priced for Sonnet): Haiku about $0.03, Sonnet about $0.52. 0 QPU s, 0 laptop hours. |
| prior work | Copied from the map and brought up to date: BrainBench (Luo et al. 2024, *Nature Human Behaviour*, arXiv 2403.03230) predicts **pass** for smaller models: every one of 15 open LLMs beat experts, 7B models matched larger ones, and chat-tuned variants scored below base models; those are perplexity-scored open models on neuroscience abstracts. SciPredict (Sehwag et al. 2026, arXiv 2604.10718) finds frontier models at 14–26% on its tasks, with accuracy flat against stated confidence, which predicts **fail** for verbal probabilities. No paper reports Haiku or Sonnet, or verbalised probabilities on masked post-cutoff findings, against a publication-bias rule. **What this bet adds:** the rule-12 replication the six program-4 passes owe (all on Opus), against two shortcut rules, with a cluster bootstrap. |
| lesson | "Correcting P3, P14: the card's 0.25 bar is nearly cleared by the good-news rule (Brier 0.232), and items were bootstrapped as independent. This bet must beat the up-word and good-news rules by 0.01 Brier on item and paper-cluster bootstraps, and its odds are 18% (from 45% on the map) because both models must clear what Opus cleared by 0.036." |
| design review | before the first call, a fresh auditor dry-runs this design (operators/design-review.md) → `ledger/design-reviews/ss-b13.md`. No call runs before a go. |
| pre-mortem | "If this fails, the most likely reason is that Haiku's Brier on the 116 items is not 0.01 below the good-news rule's 0.232: its weaker priors leave it close to the publication-bias shortcut." Kind: `world`. |
| auditor | fresh session per operators/auditor.md, after results |

## 1. In plain English

In round 1, the strongest Claude model (Opus), with no internet and no titles, picked which way 116 newly published findings went 76% of the time. Nobody has tried the two smaller models. If they do as well, knowing which way new research goes is not a property of the strongest model only.

We run the same prompt, unchanged, on Haiku and Sonnet, on the same 116 findings in the same option order Opus saw. **A hit means both smaller models beat three things**: always saying 50%, a rule that bets on the "higher / more" wording, and a rule that bets on whichever option says the paper's own method works (the item-writer's tag, the program's round-1 flattery rule). The last two must be beaten by more than 0.01 in Brier, and every bound must hold when papers, not items, are resampled. The rival explanation is that the smaller models only know that papers report their own success; the good-news rule is that rival, made into a predictor.

The same models also bet on round 2's 92 template sentence pairs. On those, always-50% is not a meaningful bar (a dumb rule clears it), so they are compared with the up-word rule, the swap-pair rule and the archived Opus flattery rater, as reported rows.

## 2. Material

- **Models.** `claude-haiku-5-5` (thinking `disabled`) and `claude-sonnet-5-5` (thinking `between_tools` with no tools, D6), through `common.structured`. Each call records the setting used. Structured output `{rationale, p_option_1}`, `max_tokens` 4000 (as the Opus bettor), no tools field, no temperature set. The Opus bettor could not run with thinking off and ran at effort low (D18), so the comparison with Opus differs in thinking as well as model.
- **Prompt.** `bettor/bettor.py` `SYSTEM` and `user_text`, verbatim and unchanged (rounds 1 and 2).
- **Items.** Round 1: the 116 post-cutoff items of `items/items.jsonl` (`side: post`; SHA-256 in `items/SHA256SUMS`, f924db16… after D12); the bettor sees `items/masked.jsonl` only. Round 2: the 92 drawn items of `items/r2/items.jsonl` (`bettor.sample_r2`). No item is added, dropped or rewritten.
- **Option order.** The order Opus saw in its primary call, from the archived seeds (`bettor/seed.json` `order` over all 184 round-1 items; `bettor/r2-seed.json` `items` and `order`). `bettor/f1.py --dry-run` checks it against the archive: 116 of 116 and 92 of 92 match. No new draw, so no beacon seed: `seed_source: fixed` (the bootstrap seed, 20261104).
- **Up-word rule (round 1).** `scoring/score_f1.py` `up_side_r1`, from the two options only: the option whose differing words are the up member of their direction pair (higher, more, larger, increased, better, stronger, faster, longer, greater, above, …) gets 0.75; a pair with no up side (earlier/later, easier/harder, closer/farther) or slots that disagree get 0.5. It gives `a` on 99, `b` on 15 and none on 2 of the 116 (answer-free count).
- **Good-news rule (round 1).** `scoring/score.py` `headline_p`: 0.75 on the item-writer's `headline_side`, 0.5 where untagged (78 of 116 untagged). This is ss-b2's publication-bias baseline. The writers saw the answers and were told to prefer against-headline findings, which weakens it (ss-b1 audit).
- **Round-2 comparators (reported).** The up-word rule (0.75 on `up_side`), the swap-pair rule (`score.SWAP_PAIR_P`, D24) and the archived Opus flattery rater (`bettor/r2-valence.jsonl`, ss-b6's prompt, same option order).
- **Scale.** One direction: 1 = Option 1 almost certainly not reported, 99 = almost certainly reported, 50 = cannot tell.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | Haiku, round 1, primary | 116 | $0.01 |
| 2 | Haiku, round 2, primary | 92 | $0.01 |
| 3 | Sonnet, round 1, primary | 116 | $0.29 |
| 4 | Sonnet, round 2, primary | 92 | $0.20 |
| | **total** | 416 | about $0.51 (cap $0.70) |

- Run order as listed. Steps 1 and 3 alone carry the pass rule. If a cap stops the run, later steps are reported as not run.
- Every call is cached by a content hash (`bettor/f1-cache.json`, registered in `common.CACHES`), so a crash never pays twice. Before every call `common.Caller` checks this bet's cap and the program cap ($8.95).
- No order check, to stay at the card's price; the order-check rows Opus has are not repeated.

## 4. Statistics

- **Primary statistic, per model, on the 116 round-1 items:** p_true = the probability on the reported option (`score.p_true_of`, clipped 1–99). Three quantities, each a mean over items: (C1) Brier, mean (1 − p_true)²; (C2) Brier minus the up-word rule's Brier, item by item; (C3) Brier minus the good-news rule's Brier, item by item. Unit: the item.
- **Uncertainty:** a percentile item bootstrap (10,000, `numpy.random.default_rng(20261104)`, indices int(0.025n) and int(0.975n) − 1), and **a paper-cluster bootstrap** (P14: resample arXiv papers with replacement, 108 papers, at most two items each; same seed and indices; `score_f1.cluster_ci`). **The bar is read on both:** each condition must hold on each bootstrap. Tolerance 1e-12 on every bound (P13).
- **Split:** none. Nothing is fitted.
- **Secondary statistics** (reported, never the verdict): accuracy; the card's event (C1 on the item bootstrap); Sonnet's and Haiku's labels alone; round 2's Brier and its paired differences against the up-word, swap-pair and Opus-flattery rules on item and swap-pair-cluster bootstraps, with "beats by the margin" for each; Opus's archive scored by the same code on both rounds.
- **Multiple comparisons:** one conjunction (2 models × 3 conditions × 2 bootstraps), no correction; requiring every one is the strict reading.
- **Robustness checks committed now** (P10, D21): leave-one-item-out and leave-one-field-out on each model's label. A flip is reported in a sentence ("rests on …"); neither changes the verdict.

## 5. Pre-registered reading

Per model, "meets the rule" means C1 upper bound < 0.25, C2 upper bound < −0.01 and C3 upper bound < −0.01, on both the item and the paper-cluster bootstrap. The sentences are generated by `scoring/score_f1.py` (`sentences`), verbatim:

1. **Pass:** both meet it. Reported as **pass, unreplicated**. *"On round 1's 116 findings posted after the models' training cutoff, both Haiku and Sonnet, with the bettor's prompt unchanged, beat always saying 50% and beat both the up-word rule and the good-news rule by more than 0.01 in Brier, on item and paper-cluster bootstraps (<numbers>). Knowing which way these findings went is not only the strongest model's; this does not separate knowing results from reasoning within the item, and the items were written by a Claude model."*
2. **Mixed:** exactly one meets it; not a pass. *"On round 1's 116 post-cutoff findings, <model> met the rule (always-50%, the up-word rule and the good-news rule all beaten, the last two by more than 0.01 in Brier) but <other> was not shown to (<numbers>), so the bettor's skill holds on one of the two smaller models only."*
3. **Fail:** neither. *"On round 1's 116 post-cutoff findings, neither Haiku nor Sonnet was shown to beat always-50%, the up-word rule and the good-news rule by the pre-registered margin (<numbers>), so on these items the bettor's skill was not shown beyond the strongest model."*
4. **Untestable:** fewer than 100 of the 116 round-1 items scored on either model (a refusal, an error, the cap). *"Too few findings were scored to test the smaller bettors (<model>: n of 116 scored; at least 100 needed)."*
5. **Reported in every case**, after the main sentence: which conditions each failing model missed; leave-one-item-out and leave-one-field-out clauses; *"The cockpit card's event (Brier upper bound below 0.25 on both models, item bootstrap only) was met | not met; it is reported, not the rule."*; *"Both models ran with thinking off, which the Opus bettor could not (it ran at its least-thinking setting), so the comparison with Opus's archive differs in thinking as well as model."*; the round-2 table; Opus's archive rows.
6. **Scoring for the ledger:** outcome 1 if pass, 0 if mixed or fail. Untestable is not scored. One scored bet for the run.

## 6. What it cannot do

- **Knowing vs reasoning.** The items give a methods summary; a model can reason toward a direction without knowing the result. Nothing here separates the two.
- **The writer.** Round 1's items were written by Claude Opus sessions that saw the answers; a writer from the bettors' family may have chosen findings this family finds easy (ss-b1 audit). Round 2 is model-free but is reported only.
- **A weakened good-news rule.** The writers preferred against-headline findings, so the good-news rule is weaker here than on a random sample of papers; beating it is easier than beating the real publication bias.
- **The up-word rule is weak on round 1** (Brier 0.316, worse than a coin, because the writers often put the reported result on the "down" side): C2 adds little there; C1 and C3 carry the rule.
- **Thinking.** Haiku and Sonnet ran with thinking off; Opus could not. "Smaller models do as well" would be about these settings.
- **Two models, one prompt, one item set.** No "LLMs", "every model" or "all" sentence will appear.

## 7. Stop rules

- Budget caps in code: $0.70 for this bet and $8.95 for the program. If a cap is reached, later steps are reported as not run.
- Stop on any refusal: no rewording, no retry, `results/refusal.md` written.
- Stop on any error or truncation (`llm._check_stop`). The ratings made so far are written to `bettor/f1-bets.jsonl` on every exit path.

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "ss-b13", "program": "settled-science", "direction": "ss-f1", "map": "map/settled-science.json",
 "title": "Haiku and Sonnet as bettors on round 1's 116 post-cutoff findings, against always-50%, the up-word rule and the good-news rule", "source": "engine",
 "odds_event": "For both claude-haiku-5-5 and claude-sonnet-5-5 on round 1's 116 post-cutoff items: Brier upper bound < 0.25, and Brier minus the up-word rule's and minus the good-news (headline-tag) rule's each with upper bound < -0.01, every bound on both the item and the paper-cluster bootstrap.",
 "engine_odds": "<odds_after_lesson>", "engine_odds_first": 0.45, "human_odds": 0.65, "human_odds_at": "ho-20261105-051140-ruf (2026-11-05T05:11:40-07:00)",
 "prereg_commit": "<this commit>", "budget_usd": 0.70, "referee": "published-record", "bet_type": "standard", "seed_source": "fixed",
 "lesson": "ls-ss-b13", "premortem_kind": "world", "verdict": "open"}
```

## 9. Checklist before the first call

- [x] This file is committed on its own; nothing has been run.
- [x] §0's prior work row states predicted outcomes with citations and what this bet adds.
- [x] The lesson row is filled after reading ledger/bets.jsonl, brier.md (37 scored, Brier 0.188, 12/37), audits/ (newest ng-p3-18.md) and lessons.jsonl; the same sentence goes to `ledger/lessons.jsonl` as `ls-ss-b13`.
- [ ] A fresh design review has returned go, or fix-first confirmed.
- [x] The direction's card was on the cockpit and answered before 05:11 (it has dropped off as answered); `ledger/human-odds.jsonl` was read immediately before this commit.
- [x] Engine odds are on record with an earlier timestamp (the map, b42b3d6); human odds copied from `human_odds_match.py`.
- [x] One scale direction in every prompt.
- [x] No draw, so no beacon seed (`seed_source: fixed`); stated in §2.
- [x] Budget and stop-on-refusal are enforced in code.
- [x] DEVIATIONS.md D62.
