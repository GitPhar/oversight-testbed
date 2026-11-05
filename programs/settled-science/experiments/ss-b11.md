# ss-b11 (direction ss-f3): does the round-1 bettor beat a rule that knows each field's own rate of good news? (pre-registration)

Written and frozen 2026-11-05 06:41 America/Denver, in its own commit, before the archive is opened for this analysis. DEVIATIONS.md D52. Budget **$0** (archive only: no model call, no QPU second, no local model).

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). Sean's odds come only from `ledger/human-odds.jsonl`. This direction's card was on the cockpit before this file (map/cockpit-cards.jsonl, "ss-f3"). `ledger/human_odds_match.py settled-science ss-f3` at 06:31 printed his line `ho-20261105-061152-k9a` (0.65, recorded 06:11:52, committed 9a75cc2 at 06:16:31). Both times are before this commit, so the bet carries it.

## 0. The bet

| field | value |
|---|---|
| bet id | `ss-b11` |
| referee | `model`: graded against the published record (round 1's abstracts), program 4 |
| bet type | `standard` |
| direction | `ss-f3` (map/settled-science.json; remap 2026-11-05) |
| source | `literature` (the remap, from ss-b2's audit) |
| engine odds, P(pass) | 50, stated 2026-11-05T04:45 in map/settled-science.json by the remap (one pass, not v1); **70 after the lesson** (both kept) |
| human odds, P(pass) | **65**: `ho-20261105-061152-k9a` (2026-11-05T06:11:52-07:00, committed 9a75cc2). He answered the map's event; this bet's event is the same statistic against a baseline fitted in-sample, a stricter version (§4). |
| models | none new: archive only. claude-opus-5-5's committed round-1 answers (ss-b1's run). Haiku and Sonnet as bettors are ss-f1's job. |
| budget | $0 API · 0 QPU s · minutes of laptop time |
| lesson | "Correcting P11, P1: leave-one-out baselines leak against themselves, and remap odds sat near the base rate without reading the archive's margin. This bet fits field rates on all items (favouring the rule), adds field up-word rates for untagged items, and its odds are 70% (from 50% on the map) because ss-b2 beat the flat rule by 0.068 [0.036, 0.099]." |
| design review | before the archive is opened, a fresh auditor dry-runs this design on synthetic data (operators/design-review.md) → `ledger/design-reviews/ss-b11.md`. Nothing is scored before a go. |
| pre-mortem | "If this fails, the most likely reason is that field rates fitted in-sample on about 20 items per field cell overfit enough to bring the rule's Brier near the bettor's 0.163." Kind: `design`. |
| auditor | fresh session per operators/auditor.md, after results |

## 1. In plain English

In round 1, the strongest Claude model said which way 116 newly published findings went, and it beat a shortcut that says "papers usually report that their own method works" (ss-b2). A cleverer shortcut might do better: some fields report good news more often than others, and a rule that knew each field's habit might match the model without knowing any result. We build that rule from the answers themselves. For each of the four fields it uses how often the paper's own "it works" side was the real one, and, for findings with no such side, how often the "higher / more / better" version was the real one. Fitting the rule on the very items it is scored on gives it an unfair advantage, and that is deliberate: if the model still wins, its edge is not just knowing which fields report good news. If it does not win, its round-1 edge may be no more than that. No new data are collected: this re-scores the committed round-1 answers.

## 2. Material

- **Archive** (read-only, unchanged since ss-b1): `items/items.jsonl` (fields read: `id`, `side`, `field`, `true_option`, `headline_side`, `option_a`, `option_b`) and `bettor/bets.jsonl` (fields read: `id`, `kind`, `option_1_is`, `p_option_1`; primary calls only). The 116 items with `side: post` are scored. Pre-cutoff items are not used.
- **Code**: `scoring/score_f3.py`, committed with this file's predecessor (`--synthetic <world>` runs on generated data and never reads the archive).
- **Seed**: no beacon draw. Nothing random decides which data the test sees. The bootstrap uses the program's fixed constant, `numpy.random.default_rng(20261104)` (operators/hardware.md allows a fixed constant stated in the pre-registration). `seed_source: fixed`.
- **Scale**: as archived (bettor p_option_1, 1–99, one direction).

## 3. Calls

None. One script run, after a design review's go: `python3 scoring/score_f3.py` → `scoring/f3-scores.json`, `scoring/f3-tables.md`.

## 4. Statistics

- **Baseline (pre-registered; it replaces the map's leave-one-out wording with a stricter in-sample fit):**
  - Tagged items (`headline_side` set): p(headline side) = (k_f + 4r) / (n_f + 4). Here n_f is the number of the field's tagged post-cutoff items, k_f how many of them went the headline way, and r the pooled rate over all tagged post-cutoff items.
  - Untagged items whose swapped word in one option, and only that option, is in `UP_WORDS` (`score_f3.py`, a fixed list, answer-free): p(up option) = (u_f + 4q) / (m_f + 4), from the field's untagged items with an up option, with q pooled the same way.
  - Every other item: 0.5.
  - The rates include the scored item itself, which favours the rule. This avoids the leave-one-out leak of P11, in which an item's own label pushes its prediction the wrong way and handicaps the rule.
- **Primary statistic:** d = mean over the 116 items of (1 − p_bettor)² − (1 − p_rule)², where p is each side's probability on the reported option. The unit is the item.
- **Uncertainty:** a paired percentile bootstrap over items, 10,000 resamples, `default_rng(20261104)`. Bounds are the sorted values at int(0.025 n) and int(0.975 n) − 1.
- **Secondary (reported, never the headline):** each side's Brier with its CI; ss-b2's flat 0.75 rule beside them; the baseline's composition (tagged, untagged with an up option, at 0.5); by-field rates and differences; the leave-one-out version of the rule (each item's own label excluded from every rate it uses); a field-cluster jackknife interval on d (P14: four clusters, wide by construction).
- **Multiple comparisons:** one primary test, no correction.
- **Robustness, committed now:** leave-one-item-out (the rule is refitted without the item, and the label is recomputed) and leave-one-field-out. Any flip is named in the sentence as fragile. Neither changes the verdict.

## 5. Pre-registered reading

1. **Pass:** the upper bound of d is below 0 (tolerance 1e-12). Reported as **pass, unreplicated**. Sentence (generated): *"On 116 findings published after its training cutoff, the bettor's probabilities beat a rule that knows each field's own rate of good-news results (Brier difference d [lo, hi]; the field-aware rule scored b), so its edge over the publication-bias shortcut (ss-b2) is more than knowing which fields usually report good news. The rule's rates were fitted on the same items it was scored on, which favours the rule."*
2. **Null:** the upper bound is at or above 0. Sentence: *"On 116 findings published after its training cutoff, the bettor was not shown to beat a rule that knows each field's own rate of good-news results (Brier difference d [lo, hi]; the field-aware rule scored b), so its round-1 edge over the publication-bias shortcut may come from knowing which fields report good news."*
3. **Untestable:** fewer than 60 post-cutoff items scored. This cannot happen on the committed archive, which has 116, but the rule is written anyway: *"Too few findings were scored to test the bettor (n scored of 116)."*
4. **Appended in every case:** the fragile clauses; *"One bettor (claude-opus-5-5 at effort low), one round-1 run already scored for ss-b1 to ss-b3; this re-scores that run against a stronger rule and adds no new answers."*
5. **Ledger:** outcome 1 on pass, 0 on null.

## 6. What it cannot do

- **The same run is scored a fourth time.** ss-b1, ss-b2 and ss-b3 already scored it. This bet is not independent evidence about the bettor. It is evidence about one shortcut.
- **"Field" means the four query buckets of round 1.** A finer field split, by subfield or method, could do better. Four fields of about 29 items cannot carry a finer one.
- **The headline tags and the up-word list are fallible.** The tags were written by the item-writer. The up-word list is a fixed word list that leaves some items at 0.5.
- **One model, one prompt, one item set.**

## 7. Stop rules

None needed (no calls). If the archive files differ from their committed versions (`items/SHA256SUMS`, `git diff`), the bet is untestable and the reason is stated.

## 8. Ledger entry

```json
{"id": "ss-b11", "program": "settled-science", "direction": "ss-f3", "map": "map/settled-science.json",
 "title": "Round-1 bettor vs a field-aware good-news baseline (archive)", "source": "literature",
 "odds_event": "On round 1's 116 post-cutoff items, the bettor's Brier minus the field-aware rule's (field headline rates for tagged items, field up-word rates for untagged items, fitted in-sample, shrunk with weight 4 to the pooled rate) has a paired 95% bootstrap upper bound below 0.",
 "engine_odds": 0.70, "engine_odds_first": 0.50, "engine_odds_at": "2026-11-05T04:45",
 "human_odds": 0.65, "human_odds_at": "ho-20261105-061152-k9a (2026-11-05T06:11:52-07:00)",
 "budget_usd": 0, "referee": "model", "bet_type": "standard", "seed_source": "fixed", "lesson": "ls-ss-b11", "verdict": "open"}
```

## 9. Checklist

- [x] This file is committed on its own; the archive has not been opened for this analysis (only `--synthetic` runs).
- [x] Lesson read and written; `ls-ss-b11` follows.
- [ ] A design review's go (on synthetic data) before the archive is scored.
- [x] Cockpit card before this file; `ledger/human-odds.jsonl` read at 06:31; Sean's line copied.
- [x] Engine odds on record before this commit (remap, 04:45).
- [x] DEVIATIONS.md D52.
