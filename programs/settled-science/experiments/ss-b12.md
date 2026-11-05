# ss-b12 (direction ss-f4): is the bettor's advantage on older papers recall? (pre-registration)

Written and frozen 2026-11-05 06:45 America/Denver, in its own commit, before any paper for it was fetched and before any call. DEVIATIONS.md D53. Budget **$0.75**, enforced in code (`bettor/f4.py` `BET_CAP`; program cap $7.50 → $8.25 by budget ruling br-005). Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This direction's card was on the cockpit before this file ("ss-f4"). `ledger/human_odds_match.py settled-science ss-f4` at 06:31 printed Sean's line `ho-20261105-061152-uf3` (P = 1.00, recorded 06:11:52, committed 9a75cc2 at 06:16:31), so the bet carries it. His card said "about 30 cents, within the next round". Round 3 does not exist, so this bet builds its own items and costs about $0.60 (br-005, §0 budget).

## 0. The bet

| field | value |
|---|---|
| bet id | `ss-b12` |
| referee | `model`: graded against the published record (each item's own abstract sentence), program 4 |
| bet type | `standard` |
| direction | `ss-f4` (map/settled-science.json; remap 2026-11-05) |
| source | `literature` (the ss-b1 audit's item 2; round-3 audit of ss-b3) |
| engine odds, P(pass) | 25, stated 2026-11-05T04:45 by the remap (one pass, not v1); **20 after the lesson** (both kept) |
| human odds, P(pass) | **100**: `ho-20261105-061152-uf3` (2026-11-05T06:11:52-07:00, committed 9a75cc2). He answered the map's event on "round 3". This bet's event is the same statistic on items built for it. |
| models | `claude-opus-5-5` as bettor only, **not all three**: the question is about one model by design. It asks whether ss-b3's pre-cutoff advantage (Opus's) is recall, and the post-cutoff side is Opus's archived round-2 run. Haiku and Sonnet as bettors are ss-f1. `claude-sonnet-5-5` is the program's fixed leakage checker (fixed rule 1). |
| budget | $0.75 API: leakage check about $0.36 (up to 120 calls), bettor about $0.25 (about 52 calls). 0 QPU s. |
| lesson | "Correcting P8, P14: ss-b3 compared pre- and post-cutoff items chosen by a Claude writer, so fame and ease rode with the date. This bet draws both sides from one model-free template and the same arXiv queries, fixes the recognition code first, adds a field-cluster check, and its odds are 20% (from 25% on the map) because round 2's post side already scores 0.070." |
| design review | before the first fetch or call, a fresh auditor dry-runs this design → `ledger/design-reviews/ss-b12.md`. No fetch or call before a go. |
| pre-mortem | "If this fails, the most likely reason is a ceiling: template items are already 93% right after the cutoff, so a real pre-cutoff advantage of a few hundredths cannot clear zero with about 50 items." Kind: `design`. |
| auditor | fresh session per operators/auditor.md, after results |

## 1. In plain English

In round 1 the model did better on papers posted before its training cutoff than on papers it cannot have read (ss-b3). That could be memory, or the older questions could have been easier, because a Claude model chose which findings to ask about. An audit then found that the older items where the model's own explanation said it remembered the study were the ones it got best. This test asks the question cleanly. We build older items the same way round 2 built newer ones: the same four arXiv searches, the same fixed one-word-swap template with no model writing, and the same leakage check. Before reading any answer, we fix a word rule that marks an explanation as "recognising" the study ("I recall…", "I'm familiar with this paper…"). Then we compare the model's score on older papers it shows no sign of recognising with its score on round 2's newer papers. **A hit means it still does better on older papers it does not say it remembers**, which would point to older findings being easier, or to memory it does not mention. A miss means no advantage beyond what it recalls.

## 2. Material

- **Pre-cutoff items (new), built by code** (`bettor/f4.py`), with no model writing:
  - `--fetch`: the four `template_writer.QUERIES`, unchanged, each in three windows (submittedDate 2024-01-01 to 2024-12-31, 2025-01-01 to 2025-12-31, 2026-01-01 to 2026-06-30), sorted by submission date, newest first, 100 results each. That is 12 requests, giving `items/f4/pool.json`.
  - `--build`: keep a paper only if its first version is dated before 2026-07-01 and it is in neither round 1 (drafts, items) nor round 2 (candidates). Then `template_writer.item_from` (the paper's first candidate sentence and its one-word swap) and `verify.check`, as round 2 ran them. This gives `items/f4/candidates.jsonl`.
  - `--sample`: at most 30 candidates per field, `random.Random(seed_items).sample` over candidate ids in sorted order, giving `items/f4/sample.jsonl`.
  - `--leak`: the round-2 leakage check on the sample (`items/leakcheck.py` SYSTEM, user text, schema and key, claude-sonnet-5-5, thinking off). A flagged item is dropped and never rewritten.
  - `--freeze`: the clean items become `items/f4/items.jsonl` and `masked.jsonl`, with SHA-256 sums.
- **Bettor** (`--bet`): `bettor/bettor.py` SYSTEM, `user_text` and SCHEMA, verbatim. claude-opus-5-5 with adaptive thinking at effort low (D18), max_tokens 4000, primary calls only. The option order per item comes from `random.Random(seed_order).random() < 0.5`, in id order. This gives `bettor/f4-bets.jsonl`.
- **Post-cutoff side (archive, unchanged):** `items/r2/items.jsonl` and the primary rows of `bettor/r2-bets.jsonl` (ss-b5's 92 items). The same bettor prompt, setting and template.
- **Recognition code** (`scoring/score_f4.py` `RECOG`, fixed in this commit's predecessor `8140cf6`, before any f4 rationale exists): a case-insensitive word rule on the bettor's rationale ("I recall", "I remember", "familiar with this paper", "I recognise", "the original abstract says", and others; the exact regex is in the file). It is applied the same way to both sides. It is answer-free: it reads only the rationale.
- **Seed** (operators/hardware.md). CURBY-Q stalled: latest completed round 28297 at 2025-08-22 13:42 America/Denver (checked 06:31). Seed: the first CURBy-RNG pulse timestamped after this commit. Sub-seeds `items` and `order` come from `ledger/seed.py <randomness> ss-b12 --purpose <p>`, written to `bettor/f4-seed.json` by the seed commit. The bootstrap seed is the program's fixed 20261104. *Filled in by the seed commit:*
  `chain:` CURBy-RNG · `round:` pulse 1592290 (previous 1592289 at 06:45:00) · `pulse_time:` 2026-11-05 06:46:00 America/Denver · `randomness:` a1d936cfd8a5b1872d221fbcb0f822868b75d130bffd00bef32b89307ae154087b8badfa7e4e121804553bafb0a64a523906001c0353bd7d05e947b2e19ddf2a · `client:` @buff-beacon-project/curby-client@1.2.0 · `certificate_verified:` false · `seed:` items 2418064898708106585, order 8371102074377508067 (`bettor/f4-seed.json`)
- **Scale:** the bettor's 1–99, one direction.
- **Disclosed:** this session has seen round 2's post-cutoff Brier (0.070, ss-b5) and the ss-b1 audit's exploratory recognition split on round 1. It has seen no pre-cutoff template item.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | arXiv API (free, public) | 12 requests | $0 |
| 2 | leakage check (Sonnet) on the sample | ≤ 120 | about $0.36 |
| 3 | bettor (Opus), primary, on the clean items | about 52 | about $0.25 |

The run order is as listed. A cap stop during step 2 means nothing is frozen and the bet is untestable. A cap stop during step 3 means the scored items are used, if at least 30 are unrecognised. Every call is cached by a content hash, and both caches are in `common.CACHES`.

## 4. Statistics

- **Primary:** d = Brier(pre, not recognised) − Brier(post, not recognised). Brier per item is (1 − p_true)², where p_true is the bettor's probability on the published sentence. The unit is the item.
- **Uncertainty:** a percentile bootstrap that resamples each side independently (two disjoint item sets), 10,000 resamples, `default_rng(20261104)`. Bounds are at int(0.025 n) and int(0.975 n) − 1.
- **Secondary:** the same gap on all items, unfiltered; Brier on recognised older items; the counts flagged on each side; the gap by older window (2024, 2025, 2026H1); by query bucket; and a field-cluster jackknife interval on d (P14).
- **Robustness, committed now:** leave-one-item-out on either side and leave-one-bucket-out. Any flip is named in the sentence.
- **Multiple comparisons:** one primary test.

## 5. Pre-registered reading

1. **Pass:** the upper bound of d is below 0 (tolerance 1e-12). Reported as pass, unreplicated. *"On n older papers whose abstracts it showed no sign of recognising, the bettor still scored better than on m papers posted after its training cutoff (Brier a against b; difference d [lo, hi]), so its advantage on older papers is not only papers it says it remembers. It may still be memory it does not mention, or older findings being easier."*
2. **Null:** the upper bound is at or above 0. *"On n older papers whose abstracts it showed no sign of recognising, the bettor was not shown to score better than on m papers posted after its training cutoff (Brier a against b; difference d [lo, hi]), so this test finds no advantage on older papers beyond recall."*
3. **Untestable:** fewer than 30 unrecognised pre-cutoff items scored, or the leakage check not completed. *"Too few pre-cutoff items the bettor showed no sign of recognising were scored to test it (k; at least 30 needed)."*
4. **Appended in every case:** the fragile clauses, then *"Recognition was coded from the rationale by a fixed word rule (x of n older and y of m newer items flagged); a model can remember without saying so. One bettor (claude-opus-5-5 at effort low), template-written sentence pairs only."*
5. **Ledger:** outcome 1 on pass, 0 on null; untestable is not scored.

## 6. What it cannot do

- **Silent memory.** The word rule only catches recall the model mentions. A pass cannot separate older findings being easier from memory the model does not mention. A null does not show that the round-1 gap was recall, because the item format differs from round 1's.
- **Template items are near ceiling** (93% right after the cutoff), which limits power. That is the pre-mortem.
- **Window sampling.** Newest-first within each window means late-2024, late-2025 and mid-2026 papers. The design does not sample the window evenly.
- **One model, one format.** No "models" or "every" sentence will appear.

## 7. Stop rules

- Caps in code: $0.75 for this bet and $8.25 for the program.
- Stop on any refusal, with no rewording and no retry. Stop on any error or truncation.
- Fewer than 30 clean items after the leakage check: no bettor call, untestable.

## 8. Ledger entry

```json
{"id": "ss-b12", "program": "settled-science", "direction": "ss-f4", "map": "map/settled-science.json",
 "title": "Recall check: pre- vs post-cutoff on items the bettor shows no sign of recognising (template items)",
 "odds_event": "On pre-cutoff template items whose bettor rationale shows no sign of recognising the study (fixed word rule), Brier(pre) minus Brier(post, round 2's 92 items, same rule) has a 95% bootstrap upper bound below 0.",
 "engine_odds": 0.20, "engine_odds_first": 0.25, "engine_odds_at": "2026-11-05T04:45",
 "human_odds": 1.0, "human_odds_at": "ho-20261105-061152-uf3 (2026-11-05T06:11:52-07:00)",
 "budget_usd": 0.75, "budget_ruling": "br-005", "referee": "model", "seed_source": "curby-rng", "lesson": "ls-ss-b12", "verdict": "open"}
```

## 9. Checklist

- [x] Committed on its own; nothing fetched, no call.
- [x] Lesson written; `ls-ss-b12` follows.
- [ ] Design review go before the first fetch or call.
- [x] Card before this file; human odds copied.
- [x] Engine odds on record before (remap 04:45).
- [x] CURBY-Q status recorded; the seed commit follows.
- [x] Caps and stop-on-refusal in code.
- [x] DEVIATIONS.md D53.
