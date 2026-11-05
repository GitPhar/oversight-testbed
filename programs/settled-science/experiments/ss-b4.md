# ss-b4 and ss-b5: round 2, items written by a template rather than a model (pre-registration)

Written 2026-11-04 19:23–19:30 (America/Denver; the commit time is the record, D9). It is committed on its own, before any round-2 bettor call. DEVIATIONS.md D22 onward. The budget is the program's shared **$5.00** cap, enforced in code (`common.py`). $2.74 has been spent so far (round 1, plus the round-2 leakage check), and this round should cost about $0.85. Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

## 0. The bets

| field | value |
|---|---|
| bet ids | `ss-b4` (the replication of ss-b1's rule) and `ss-b5` (**the informative test**, see §1) |
| referee | `published-record`: the sentence as printed in the paper's arXiv abstract decides each item |
| bet type | `standard` |
| directions | `ss-b4`, `ss-b5` (map/settled-science.json) |
| source | `engine`: the audit of ss-b1 named it as the cheapest overturning test |
| engine odds, P(pass) | ss-b4 **70**, ss-b5 **35**. Stated 2026-11-04 19:17 in commit `8e87c59`, before any round-2 item existed. **Not revised**, although the dry run (§4) has since shown the up-word rule passes ss-b4: revising now would use knowledge of the items. |
| human odds | not recorded (rule 11: none are asked for in a terminal; none are in `ledger/human-odds.jsonl` for these directions) |
| budget | at most the $2.26 left in the $5.00 cap · 0 QPU s · under 1 laptop hour |
| pre-mortem | "If this fails, the most likely reason is that single template sentences give the bettor little beyond knowing abstracts report improvements, so it ties the up-word rule (ss-b5 null)." Kind: `design`. |
| lesson | Correcting P3, P9 and P1's overcorrection: ss-b1's move toward the pooled base rate cost Brier 0.16 to 0.25. This bet's dry run shows the up-word rule alone passes ss-b4, so ss-b5 is named the informative test; leave-one-field-out and every verdict sentence are pre-registered; odds stay 70% and 35%, referenced to ss-b1, not the pooled rate. Read: 14 scored bets, Brier 0.246, base rate 5/14 (running 6/16 = 0.375), newest audit `ledger/audits/ss-b1.md`. |
| design review | a fresh session that the **engine session** launches (for independence), per operators/design-review.md, before any round-2 bettor call; written to `ledger/design-reviews/ss-b4.md` |
| auditor | fresh session per operators/auditor.md, after results |

## 1. In plain English

In round 1 the bettor beat a coin on findings it could not have read. But the items were written by the bettor's own model family, and that family might have picked findings it finds easy. Round 2 takes the writer away. A fixed rule, written before any paper was opened, picks one comparative result sentence from each recent arXiv abstract. It offers the sentence as published beside the same sentence with its one direction word flipped ("higher" and "lower", "outperforms" and "underperforms"). The bettor, the same tool-less model at the same setting, says which sentence is real.

There is a catch, found in the dry run before this pre-registration. **78% of these sentences carry the "up" word** ("higher", "more", "better", "improves"), because abstracts mostly report gains. So a dumb rule that always leans toward the up word beats a coin too. It scores 0.171 on the frozen pool. **ss-b4 (beat always-50%) therefore cannot show judgment on these items**, even if it passes. It is kept, as the engine session specified, because it is the exact replication of ss-b1's rule, and the write-up will say what it shows. **ss-b5 (beat the up-word rule) is the test of whether the bettor knows which way findings went** beyond "papers report gains".

## 2. Material

- **Writer:** none. `protocol/template-writer.md` and `items/template_writer.py` were committed at `5ce075d`, before any round-2 paper was fetched. The pool was extended once, by D22, under a rule committed at `4cdd8e4` before the second fetch. No other provider's key was looked for: this session's permission rules block credential exploration.
- **Pool:** four fixed arXiv queries, papers with v1 dated 2026-07-02 to 2026-11-03, results 0–599 per field. The template gave 243 items. The leakage checker (claude-sonnet-5-5, the round-1 prompt) flagged 146, which were **dropped, never rewritten**. **97 are frozen** in `items/r2/items.jsonl` and `items/r2/masked.jsonl` (no answers):
  ```
  5aa20488a54a38fef47403221865536cb1fd7dbe8e7187d0023d83533d3d4e92  items/r2/items.jsonl
  e47ac6356bd423fe821dfcea970f2356a9f1eba74178f838230f8888426412d5  items/r2/masked.jsonl
  ```
  By field: model psychology 35, interpretability 27, scalable oversight 21, quantum devices 14. All are post-cutoff.
- **Draw:** a field with more than 30 items gives a beacon-drawn 30 (`bettor.py` `sample_r2`, sub-seed `items`). That leaves **92 items** to bet: model psychology 30, interpretability 27, scalable oversight 21, quantum devices 14.
- **Bettor:** exactly as in ss-b1 after D18–D19: claude-opus-5-5, one fresh call per item, no tools, adaptive thinking at effort low with reasoning hidden, max_tokens 4000, the same `SYSTEM` and `user_text`. The option order and the half that gets an order check are drawn from the beacon sub-seeds `order` and `order-check`.
- **Seed** (operators/hardware.md): CURBY-Q stalled (latest completed round 28297, 2025-08-22 13:42 America/Denver, last checked 16:55 today). **Seed: the first CURBy-RNG pulse timestamped after this commit.** seed = `ledger/seed.py <randomness> ss-b4 --purpose <items|order|order-check>`. Filled in by the seed commit, before any bettor call:
  `chain:` ___ · `pulse_index:` ___ · `pulse_time:` ___ · `randomness:` ___ · `seeds:` ___
- Bootstrap seed 20261104, 10,000 resamples, numpy (D16).

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | primary bettor call, each of the 92 drawn items | 92 | about $0.55 |
| 2 | order check, a drawn half, options reversed (secondary) | 46 | about $0.28 |

Step 1 alone settles both bets. Calls are cached by content hash (`bettor/r2-bettor-cache.json`), and bets are saved on every exit (D14).

## 4. Statistics

- **ss-b4 (primary replication):** Brier over the scored items, (1 − p_true)², with a percentile bootstrap CI.
- **ss-b5 (the informative test):** paired difference, mean of (1 − p_true)² − (1 − u)², where u = 0.75 if the item's `up_side` option is the published one and 0.25 if not, with a percentile bootstrap CI. This rule was fixed in the map (`8e87c59`) before any item existed.
- **Dumb-baseline check, done before this commit** on the frozen 97 with synthetic bettors (`score.py --r2 --synthetic`). Coin: 0.250, null on both. Up-word rule: **0.171, passes ss-b4**, null on ss-b5. Oracle: passes both. Anti-oracle: null on both. So ss-b4 is passable by a trivial predictor, and ss-b5 is not.
- **Robustness, pre-registered:** leave-one-item-out on both labels, and **leave-one-field-out** on both labels, each with any flipping item or field named (D16, D21).
- **Secondary, never a headline:** Brier and the comparison with the up-word rule by field; the calibration table; the order check; round 2 against round 1's post-cutoff Brier (descriptive, because the item types differ).
- **Multiple comparisons:** two bets with their own odds, scored separately; no correction.

## 5. Pre-registered reading

1. **ss-b4 pass:** at least 60 scored and the Brier's upper bound is below 0.25. Sentence: *"On n template-written findings published after its training cutoff, the bettor's probabilities beat always saying 50% (Brier b [lo, hi]); on these items a rule that always picks the 'higher / more / better' wording also does, so this pass alone does not show judgment."*
2. **ss-b4 null:** at least 60 scored, and the upper bound is 0.25 or more. Sentence: *"On these template-written findings the bettor was not shown to beat always saying 50% (Brier b [lo, hi])."*
3. **ss-b5 pass:** at least 60 scored, and the paired difference's upper bound is below 0. Sentence: *"The bettor beat a rule that always picks the 'higher / more / better' wording, on findings written by a template rather than by its own model family."* **ss-b5 null:** *"The bettor was not shown to beat a rule that always picks the 'higher / more / better' wording on template-written findings."*
4. **Untestable:** both bets are untestable if fewer than 60 items are scored. Sentence: *"Too few findings were scored to test the bettor (n scored of 92; reason)."*
5. **Fragile:** if removing any one item or any one field flips a label, append: *"; this label rests on <the item / the field> (name): without it the label would be <other label>."*
6. **Scope (D20), printed beside every verdict:** *"The bettor ran with adaptive thinking at effort low (the least thinking claude-opus-5-5 allows), with its reasoning hidden; every result here is about the bettor at that setting."*
7. **Reported in every case:** n by field, Brier by field with the up-word comparison, the calibration table, the order check, spend, refusals, and the drop counts at each stage of the template and the leakage check.

Every pass is **pass, unreplicated**.

## 6. What it cannot do

- **The leakage checker is a Claude model**, and it dropped 60% of the template's items. The writing contains no Claude, but the final selection still does: Claude decided which template sentences were too leaky to use. Its cues were mostly numbers and contrasting words in the sentence ("1.18% vs. 3.38%", "the strongest baseline").
- **Template items are single sentences with no methods summary.** Some are weak or non-empirical. For example, at least one "quantum-devices" item is about an algorithm, not a device: the field query cannot tell. Round 2 is a different item type from round 1, so the two rounds' Briers are compared only descriptively.
- **The pool is whatever four keyword queries returned.** It is not a sample of each field.
- It scores the published wording, not the truth, and it is one bettor model and one setting.

## 7. Stop rules

- The shared $5.00 cap, in code. Stop on any refusal, with no rewording or retry. Stop on any API error.

## 8. Ledger entries (completed after audit)

```json
{"id": "ss-b4", "program": "settled-science", "direction": "ss-b4", "title": "Round 2 (template writer): post-cutoff Brier beats 0.25", "source": "engine",
 "engine_odds": 0.70, "engine_odds_at": "2026-11-04 19:17 America/Denver", "human_odds": null, "prereg_commit": "<this commit>", "budget_usd": 5.0,
 "referee": "published-record", "bet_type": "standard", "seed_source": "curby-rng",
 "premortem": "If this fails, the most likely reason is that single template sentences give the bettor little beyond knowing abstracts report improvements, so it ties the up-word rule (ss-b5 null).",
 "premortem_kind": "design", "verdict": "open", "note": "passable by the up-word rule (dry run); ss-b5 is the informative test"}
{"id": "ss-b5", "program": "settled-science", "direction": "ss-b5", "title": "Round 2: the bettor beats the up-word rule", "source": "engine",
 "engine_odds": 0.35, "engine_odds_at": "2026-11-04 19:17 America/Denver", "human_odds": null, "prereg_commit": "<this commit>", "budget_usd": 5.0,
 "referee": "published-record", "bet_type": "standard", "seed_source": "curby-rng", "premortem": "(as ss-b4)", "premortem_kind": "design", "verdict": "open"}
```

## 9. Checklist before the first call

- [x] This file is committed on its own, and no round-2 bettor call has been made.
- [x] Engine odds were on record before any item existed (`8e87c59`). Human odds: none (rule 11).
- [x] Pass rules and sentences for every verdict are in §5.
- [x] One pre-mortem sentence, with its kind.
- [x] The dumb baseline is checked, and the result is stated (§4).
- [x] The seed rule names CURBy-RNG by the 24-hour rule.
- [ ] Design review **go**, launched by the engine session.
