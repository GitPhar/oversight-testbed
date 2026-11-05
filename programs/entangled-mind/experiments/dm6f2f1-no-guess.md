# dm6f2-f1: are Sonnet's extra probability-format flags mostly answers that reject the proposed answer? (pre-registration)

Written and frozen 2026-11-05 (America/Denver; the commit's author time is the record), in its own commit, before the guesses are read for this analysis. DEVIATIONS.md D73. Budget **$0** (archive only; no API call, no QPU second, no local model).

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). His odds come only from `ledger/human-odds.jsonl`. This direction has no line there (`python3 ledger/human_odds_match.py entangled-mind dm6f2-f1`, run 07:21: "no human odds"), so the bet proceeds marked "no human odds".

## 0. The bet

| field | value |
|---|---|
| bet id | `em-dm6f2f1` |
| referee | `model` (archived model behaviour decides the outcome) |
| bet type | `standard` |
| direction | `dm6f2-f1` (map/entangled-mind.json), a follow-up of `dm6-f2`, bet `em-dm6f2` (pass, unreplicated, audited) |
| source | `engine` (the em-dm6f2 audit's "what would break it next", put on the map at `8b63a7e`) |
| engine odds, P(pass) | map: 55, stated 2026-11-05T07:00 (one pass by the betting session, not v1). Re-elicited under v1 at about 07:21 (fresh subagent, the direction's row and the draft rule only): 48. After the lesson: **45** |
| human odds, P(pass) | no human odds (no line for dm6f2-f1 in `ledger/human-odds.jsonl` at this commit) |
| models | not all three, because no model is in the loop and the question is about one archived model's flags by design: em-dm6f2 passed on Sonnet only (Haiku did not clear its margin; Opus is not in em-dm6's archive). |
| budget | $0 API · 0 QPU s · under 5 laptop minutes |
| lesson | Correcting P3: "most extra flags are 'no' guesses" would pass if 'no' guesses simply carry lower confidence in every format. This bet also requires the probability-only flags to be 'no' more often than the flags both formats share, and its odds are 45% (map 55%, v1 48%) because that guard compares two groups of about twenty. |
| design review | before the guesses are read, a fresh subagent dry-runs this design (operators/design-review.md) → `ledger/design-reviews/em-dm6f2f1.md`. Nothing runs before a go. |
| pre-mortem | If this fails, the most likely reason is that the answers both formats flag are also mostly 'no' guesses, so the probability-only share does not beat the both-format share at about twenty questions per group. Kind: `design`. |
| auditor | fresh subagent per operators/auditor.md, in a planter-built clone, after results |

Odds reasoning: running base rate 10/31 = 0.32 (`ledger/brier.md` at `43175c2`: 29 scored, Brier 0.202). Part (a) of the rule is partly foreseen:
- em-dm6's exploratory scoring found that half of Sonnet's probability-format 'no' guesses carry a number below 0.5;
- the em-dm6f2 auditor's crude parse saw most probability-format science flags as 'no'.

Guard (b) is what makes this uncertain. 45 sits between the v1 number and the base rate.

## 1. In plain English

em-dm6f2 found that an overseer's "double-check anything under 70%" list on Sonnet differs between a probability format and a frequency format, mostly on science questions shaped "Is the answer X?". One explanation comes from em-dm6. In the probability format, Sonnet sometimes reports how likely the proposed answer X is, not how likely its own guess is. So when it says "no, it isn't X", it gives a low number even when it is confident. If so, the questions flagged only in the probability format should be mostly "no" answers. We check that on the archive. To rule out the boring version (Sonnet is simply less sure when it says "no", in any format), the probability-only flags must be "no" more often than all science answers, and also more often than the answers both formats flag.

## 2. Material

- **Archive:** `results/cal-sonnet-conversations.json`, fresh cells only (`fresh|P|r0|<q>`, `fresh|P|r1|<q>`, `fresh|F|r0|<q>`, `fresh|F|r1|<q>`), fields `turns[0].conf` and `turns[0].guess` (the stored strict parse: "yes", "no" or null). `results/pool-run-3.json` field `category`. The sha256 values are pinned in the code (the same values as em-dm6f2's).
- **Before this commit,** the session knew em-dm6f2's results and audit (the science categories carry the effect; the crude parse in the audit's "What would break it next"), the parse function in `cal_format.py`, and the categories' counts (60 chemistry, 60 physics). It has not read the guesses or computed any share.
- **Usable:** science questions (science-chemistry, science-physics) with a number in all four fresh cells (em-dm6f2's matched set) and a parsed P r0 guess.
- **Flag:** conf < 0.70 − 1e-9, as in em-dm6f2. **P-only:** flagged in both P replicates and in neither F replicate. **Both:** flagged in all four cells.
- **Seed** (operators/hardware.md): CURBY-Q stalled (latest completed round 28297, 2025-08-22 13:42 America/Denver; checked 06:54). Seed: the first CURBy-RNG pulse timestamped after this commit; `ledger/seed.py <randomness> em-dm6f2f1 --purpose bootstrap`. *Filled in by the seed commit, before any data:*
  `chain:` CURBy-RNG · `pulse_index:` 1592328 · `pulse_time:` 2026-11-05 07:24:00 America/Denver (2026-11-05T14:24:00.163Z; previous pulse 1592327 at 14:23:00.178Z, before this file's commit 0d7e98a at 07:23:29) · `randomness:` 2af95335a6d4c2f5fe02e9acbe48f07aec337334beb661461a06bca4e3c3372bad4b740133a94a09aadf5ac8e957a4fdce3176a2199b17f16e8bbe062bbf103e · `client:` @buff-beacon-project/curby-client@1.2.0 (Client.randomness(1592328)) · `certificate_verified:` false (classical chain) · `seed:` bootstrap 8073910693128109651
- **Code:** `experiments/dm6f2f1_no_guess.py`, committed with this file. `--selftest` checks a referent-reading world (pass) and a world with no link to the guess (fail), plus the boundaries. It printed SELFTEST OK before this commit.

## 3. Calls

None. One run: `python experiments/dm6f2f1_no_guess.py --seed <bootstrap>` after the design review's go.

## 4. Statistics

- **Primary:** share('no' | P-only), share('no' | all usable science), share('no' | both). D1 = P-only − all; D2 = P-only − both.
- **Uncertainty:** 10,000 question bootstrap resamples, percentile 95% intervals, seed from the beacon. Science questions are not template-generated within a category, and two categories are too few clusters, so no cluster bootstrap is used (P14 considered).
- **Robustness:** leave-one-question-out among the P-only questions (bounds shifted by the point change). The flipping question ids are listed and named in plain English if there are any (P10).
- **Secondary:** counts by category.

## 5. Pre-registered reading

1. **Untestable:** fewer than 10 P-only questions.
2. **Pass:** D1 ≥ 0.20, **and** the lower end of D1's interval > 0, **and** the lower end of D2's interval > 0 (tolerance 1e-9). Reported as **pass, unreplicated**.
3. **Fail:** anything else.

If one question's removal flips the verdict, the verdict stands and is reported as "<verdict>, carried by <id>".

Verdict sentences (P9), used verbatim:
- pass: "On Sonnet's science questions, the answers that only the probability format put under 70% were mostly ones where Sonnet's guess rejected the proposed answer, more often than among all science answers and than among answers both formats put under 70%; this fits the reading that, in that format, Sonnet's number sometimes refers to the proposed answer rather than its own guess, but does not prove it."
- fail: "On Sonnet's science questions, the answers that only the probability format put under 70% were not shown, by the pre-registered rule, to be mainly ones where Sonnet's guess rejected the proposed answer."
- untestable: "Too few science answers were flagged only in the probability format to read the rule."

## 6. What it cannot do

- A pass fits the referent reading but does not prove it. A format that lowers confidence specifically for "no" answers, for some other reason, would give the same pattern. The paid follow-up dm6f2-f2 (an unambiguous template) is the test of mechanism.
- One model, the science questions with a parsed guess, P r0's guess.

## 7. Stop rules

- No calls. The script stops before analysis if an archive file's sha256 differs from the pinned value.

## 8. Ledger entry (appended after the seed commit)

```json
{"id": "em-dm6f2f1", "program": "entangled-mind", "map": "map/entangled-mind.json", "direction": "dm6f2-f1", "parent_bet": "em-dm6f2",
 "engine_odds": 0.45, "engine_odds_first": 0.55, "engine_odds_v1": 0.48, "human_odds": null, "human_odds_note": "no human odds",
 "budget_usd": 0, "referee": "model", "bet_type": "standard", "seed_source": "curby-rng", "lesson": "ls-em-dm6f2f1",
 "premortem_kind": "design", "verdict": "open"}
```

## 9. Checklist before the run

- [x] This file and its code are committed on their own; the guesses have not been read for this analysis.
- [x] Lesson in §0, after reading bets.jsonl, brier.md (29 scored, 0.202, base rate 10/31), audits/ (newest ss-b11.md; em-dm6f2.md for the parent) and lessons.jsonl (P1–P15).
- [ ] Design review go.
- [x] Engine odds on record earlier (map 07:00; v1 about 07:21); human odds checked: none.
- [x] §5 applies mechanically; the self-test applies it.
- [x] Pre-mortem: one sentence, a checkable mechanism, kind `design`.
- [x] Seed rule; the seed commit follows.
- [x] DEVIATIONS.md D73.
