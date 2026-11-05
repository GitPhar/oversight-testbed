# ss-b6: the valence comparator for round 2 (pre-registration)

Written 2026-11-04 (America/Denver; the commit time is the record, D9). It is committed on its own, before any valence call. The budget is the program's shared **$5.00** cap, enforced in code. $3.40 has been spent, and this bet should cost about $0.45. Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

## 0. The bet

| field | value |
|---|---|
| bet id | `ss-b6` |
| referee | `published-record` (the sentence as printed in the arXiv abstract) |
| bet type | `standard` |
| direction | `ss-b6` (map/settled-science.json), parent `ss-b5` |
| source | `engine`: the ss-b5 audit's cheapest reversal test |
| engine odds, P(pass) | **25**, stated in commit `d97a485`, before any valence call |
| human odds | not recorded (rule 11) |
| budget | at most $1.60, the rest of the $5.00 cap · 0 QPU s |
| pre-mortem | "If this fails, the most likely reason is that the valence rater picks the flattering sentence as reliably as the bettor picks the published one, because most published sentences report the paper's win." Kind: `world`. |
| lesson | Correcting P3 and P10's cousin: ss-b5's margin rested on 21 down-word items where a flatter-the-paper rule may also win. This bet adds that rule as a comparator and pre-registers the down-word subset; its odds are 25% because the audit found the down-word hits were mostly the paper's wins. Read: 15 scored bets, Brier 0.267, base rate 6/15 (running 7/17 = 0.41), newest audit ledger/audits/ss-b5.md. |
| design review | a fresh session that the **engine session** launches; written to `ledger/design-reviews/ss-b6.md` |
| auditor | fresh session per operators/auditor.md, after results |

## 1. In plain English

In round 2 the bettor picked the published sentence over its one-word-flipped twin on 86 of 92 items, and beat two dumb rules. The audit pointed out a rival it does not rule out: most published sentences report the paper's win, so a bettor that simply picks "the version that makes the paper look good" would do well without knowing any result. This bet measures that rival directly. A fresh session of the same model, with no tools, is asked a different question about the same sentence pairs: which one makes the paper's own method or result look better? It is never told that one is real. Its probability on the published sentence becomes a third dumb rule. If the bettor beats it, round 2's pass is more than flattery-picking. If not, the pass may reduce to it.

## 2. Material

- **Items:** the same 92 drawn round-2 items as ss-b5 (`items/r2/items.jsonl`, the draw by `bettor/r2-seed.json`, sub-seed `items`), unchanged.
- **Valence rater:** claude-opus-5-5, one fresh call per item, no tools, at the bettor's setting (adaptive thinking at effort low, hidden; max_tokens 4000; D18). It shows the two options in **the same order as the bettor's primary call** (sub-seed `order`), and nothing else: no field, question, methods or forecasting frame. The prompt is verbatim in `bettor/valence.py` (`SYSTEM`; the user text is "Option 1: … / Option 2: …"). The scale: 1 means Option 2 clearly makes the paper look better, 99 means Option 1 clearly does. No other provider's key was looked for: this session's permission rules block credential exploration. The audit named claude-opus-5-5 at the same setting as the fallback.
- **Bettor ratings:** the existing ss-b5 primary calls (`bettor/r2-bets.jsonl`). No new bettor call is made.
- **Seed:** **no new random draw.** The items, the option order and the bootstrap seed (20261104) are all fixed already. So this bet has no beacon commit, and the pre-registration says so instead of drawing a seed that decides nothing. The reviewer may require otherwise.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | valence rating, each of the 92 items | 92 | about $0.45 |

Every call is cached by content hash (`bettor/r2-valence-cache.json`). Ratings are saved on every exit.

## 4. Statistics

- **Primary statistic:** the paired difference, the mean over items of (1 − p_true)² − (1 − v_true)². Here p_true is the bettor's primary probability on the published sentence, and v_true is the valence rater's probability that the published sentence is the one that flatters the paper. Percentile bootstrap, 10,000 resamples, seed 20261104 (numpy, D16).
- **Also reported:** the valence rule's Brier and accuracy, with a CI.
- **Pre-registered subsets** (reported, not tested): the up-word items (71) and the down-word items (21), each with both Briers and the paired difference.
- **Robustness:** leave-one-item-out and leave-one-query-bucket-out on the label. Any flip makes it "fragile", and a remainder under 60 is untestable (D28).
- **Dry run, before this commit**, with synthetic valence raters against the real ss-b5 bettor ratings (`score.py --b6 --synthetic`):
  - coin (Brier 0.250): pass;
  - up-word (0.177): pass;
  - copy-of-bettor (0.070): null;
  - oracle (0.010): null.

  So the rule can come out either way, and a rater as good as the bettor makes it null.

## 5. Pre-registered reading

1. **Pass:** at least 60 items have both ratings, and the paired difference's upper bound is below 0. Sentence: *"On n round-2 sentence pairs, the bettor picked the published sentence better than the same model asked only which sentence makes the paper look better (paired Brier difference d [lo, hi]; valence rule Brier v). Round 2's pass is not only picking the flattering version, though this does not separate knowing the result from reasoning within the sentence."*
2. **Null:** at least 60 items, and the upper bound is 0 or more. Sentence: *"On n round-2 sentence pairs, the bettor was not shown to pick the published sentence better than the same model asked only which sentence makes the paper look better (d [lo, hi]; valence rule Brier v). Round 2's pass may reduce to picking the flattering version."*
3. **Untestable:** fewer than 60 items with both ratings. Sentence: *"Too few valence ratings were returned to test it (n of 92; reason)."*
4. **Fragile:** if any one item or query bucket flips the label, append *"; this label rests on <item / bucket> (name): without it the label would be <other label>."*
5. **Scope (D20), beside the verdict:** *"Both the bettor and the valence rater ran as claude-opus-5-5 with adaptive thinking at effort low, with reasoning hidden; the result is about that setting."*

A pass is **pass, unreplicated**.

## 6. What it cannot do

- **The valence rater is the same model as the bettor**, which knows the same things. Asked "which flatters the paper", it may still draw on what it knows of the results. That would make it a stronger comparator, so a null result is the more ambiguous outcome.
- **"Flatters the paper" is the model's judgment, not a fixed rule.** A different prompt might score differently, and only this prompt is tested.
- **The test covers only the round-2 template items.** It says nothing about round 1.

## 7. Stop rules

The shared $5.00 cap, in code. Stop on any refusal or API error.

## 8. Ledger entry (completed after audit)

```json
{"id": "ss-b6", "program": "settled-science", "direction": "ss-b6", "title": "Round 2b: the bettor beats the valence comparator", "source": "engine",
 "engine_odds": 0.25, "engine_odds_at": "2026-11-04 20:09 America/Denver", "human_odds": null, "prereg_commit": "<this commit>", "budget_usd": 5.0,
 "referee": "published-record", "bet_type": "standard", "seed_source": "inherited (ss-b4 seed e8f921e; no new draw)",
 "premortem": "If this fails, the most likely reason is that the valence rater picks the flattering sentence as reliably as the bettor picks the published one, because most published sentences report the paper's win.",
 "premortem_kind": "world", "verdict": "open"}
```

## 9. Checklist

- [x] Committed on its own; no valence call made.
- [x] Engine odds on record before any call (`d97a485`).
- [x] Pass, null, untestable and fragile sentences written (§5).
- [x] Dumb-rule dry run reported (§4).
- [ ] Design review **go**, launched by the engine session.
