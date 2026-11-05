---
bet: ss-b4
also_covers: [ss-b5]
program: settled-science
prereg_commit: 29e8769
seed_commit: e8f921e
reviewer_session: design-review ss-b4/ss-b5 (fresh subagent launched by the engine session; no chat, transcript or author message read)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-04 19:39 America/Denver
checks: {D1: holds, D2: holds, D3: holds, D4: holds, D5: flaw, D6: holds, D7: flaw, D8: flaw, D9: flaw, D10: flaw, E23: holds (internal; pulse not refetched), template-before-fetch: cannot check (no fetch timestamp in the record)}
flaws: 7
pilot_usd: 0.00
verdict: redesign
verdict_by_bet: {ss-b4: redesign, ss-b5: fix-first}
confirmed_at: null
---

# Design review of ss-b4 and ss-b5

## In plain English

**ss-b4 can't answer its question as built.** 76 of the 97 frozen template items (78%) have the "up" word ("more", "higher", "better", "outperforms") in the published sentence. So a rule that never reads past that word clears ss-b4's bar. Seven of the trivial predictors I tried pass it on the 92 items that will actually be bet (one of them I wrote after reading the items), including the author's own up-word rule (Brier 0.177 against the 0.25 bar). A pass would show only that abstracts report gains. That is P3's failure exactly, and design-review.md calls it a **redesign**: ss-b4 should be withdrawn before data, not scored.

**ss-b5 is a real test and can go ahead after fixes.** None of the dumb predictors I could fit without using the test answers passes it. The best of them is a rule that knows only which comparative word was flipped (fit on the 146 dropped items). It scores 0.165 on the 92, a little better than the up-word comparator's 0.177. So the bettor should have to beat that rule too. The ss-b5 wording also has to shrink. The test can't tell knowing the result apart from reasoning inside the sentence, or from spotting which wording reads like real abstract prose. Because round 2 changes the item format as well as the writer, neither verdict can say whether round 1's pass came from its Claude writer. Seven fixes are listed below. None of them changes the items, the bettor or the draw.

## The question the engine session asked about each point, answered first

- **"Passable by the up-word rule" (D5).** True, and if anything understated. On the 97, the up-word rule scores 0.171 (it passes ss-b4 and is null on ss-b5), which matches §4. On the 92 drawn by the beacon, it scores 0.177 and still passes ss-b4. See D5 for the full table.
- **Leakage (D7, P8).** The rule was fixed before it ran on round 2. The protocol at `5ce075d` says claude-sonnet-5-5, the round-1 prompt, drop and never rewrite. `leakcheck.py`'s only change, in `4cdd8e4`, is the file paths: `git diff a585a88 4cdd8e4` shows nothing else, and the SYSTEM prompt is byte-identical. The drop does not track direction:
  - Items with the up word were flagged 121 of 197 times (61%), and items without it 25 of 46 (54%). Fisher's exact test gives p = 0.41.
  - The up share is 81% in the candidates and 78% in the survivors.
  - Page 1 and page 2 have similar up shares (0.80 and 0.82).

  The drop does differ by field, from 49% in model psychology to 68% in scalable oversight. Survivors carry fewer numbers: 17 of 97 have a digit, against 54 of 146 flagged items. Some survivors still carry cues of the kind §6 says the checker acted on. r2-029 has "the strongest baseline". r2-021 has "higher performance with fewer student updates". Some can be answered from the sentence or from textbook knowledge: r2-005, r2-022, r2-084. Some flips are nonsense or non-findings: r2-068 "requires less than a correct final answer", r2-003, r2-060. Paper-identifying names do appear (r2-016 "Claude Opus 4.8", r2-034, r2-039 "PICTURE", r2-054 "MLCP"). They matter only if a pre-cutoff version exists, and r2-041 is the one candidate for that (F7). These residual cues are why ss-b5's sentence must not claim knowledge of results (F3). I do **not** ask for items to be removed. A reviewer pruning frozen items by judgment would put a Claude back into the selection.
- **Pool extension D22.** It depends only on the count. `fetch(start=300)` uses the same queries, window and sort, and appends only ids it hasn't seen. `build()` reruns the unchanged template over the whole pool. `freeze()` checks only `len(keep) < 60`. Every one of the 131 page-1 candidates and its leakage status is byte-identical between `4cdd8e4` and `29e8769` (scratch comparison of `git show 4cdd8e4:…/candidates.jsonl` and `leakage-status.json` against HEAD). Page 2 added 112 candidates, 40 of them clean, for 57 + 40 = 97.
- **Template fixed before fetch.** I can't check this directly: `build-log.json` and `pool.json` hold no fetch time. The record is consistent with the claim, though:
  - `5ce075d` (19:18:14) adds only `template-writer.md` and `template_writer.py`, and no `items/r2` file.
  - The first round-2 data appear in `4cdd8e4` (19:20:36).
  - Between those commits, `candidate()`, `swap()`, `item_from()`, `PAIRS`, `CUE`, `NEG` and the queries are unchanged (`git diff 5ce075d 29e8769 -- items/template_writer.py` touches only `fetch`, `freeze` and the command-line table). `verify.py` and `protocol/` are unchanged.

  The window is tight: 142 s for four arXiv requests with 5-s sleeps, 131 Sonnet calls, the build and the D22 text. It is possible with six workers. Recommendation, not a flaw: from now on, write the UTC fetch time and the arXiv response `Date` header into `pool.json`.
- **The odds.** They were stated in `8e87c59` (19:17:09), before `5ce075d`, so before any item existed. The map's own reasoning for 70 is that "result sentences in abstracts often state the direction a field expects… and the bettor knows that". So the 70 was a bet on the up-word mechanism from the start. The lesson's "P1's overcorrection" rests on one bet: ss-b1 moved from 0.60 to 0.50 and passed. The ledger still shows P1's problem: the engine's Brier is 0.246, against 0.230 for always saying the base rate. One outcome can't establish an overcorrection. The 35 on ss-b5 sits near the running base rate (0.375) and needs no change. See F5.

## Checks

### D1. A stranger can apply the rule. **Holds.**
I ran `python3 scoring/score.py --r2 --synthetic {coin,upword,oracle,anti}`:

| synthetic bettor | Brier | ss-b4 | ss-b5 |
|---|---|---|---|
| coin | 0.250 | null | null |
| upword | 0.171 | pass | null |
| oracle | 0.010 | pass | pass |
| anti | 0.810 | null | null |

I also checked the edges:
- With 59 primary bets, both bets are untestable ("59 … fewer than 60"). With 60, both are labelled.
- A bettor I made up, which knows only the model-psychology items and follows the up-word rule elsewhere, gets ss-b5 pass with `field_flips: ['model-psychology']` (see D9).

Each table gives exactly one label per bet. A run that stops with 60 or more scored is scored on those, as D14 says. The jobs run in id order, which is field order. So a stop would cut interpretability first, and the results should then give n by field (§5.7 already requires it).

### D2. Every manipulation takes effect. **Holds.**
The manipulation is "no model wrote the items":
- All 97 `option_a` are verbatim substrings of the pool abstract.
- Every `option_b` differs from it in exactly one token, the swap word.
- `true_option` is "a" on all 97, and `up_side` matches the `UP` list (76 a, 21 b).
- `python3 items/template_writer.py --selftest` passes.
- The SHA-256 values of `items.jsonl` (5aa20488…) and `masked.jsonl` (e47ac635…) match §2.
- `masked.jsonl` has exactly `id, field, question, methods, option_a, option_b`. Because `option_a` is always the published sentence, the masked file isn't blind on its own. It is safe only because the bettor reorders by the beacon draw. `bettor.py` never opens `items.jsonl`.

I recomputed the draws in a scratch script, without importing `common.py` (which loads `.env`):
- `sample_r2` with seed 17297228536032390272 keeps 92 items and drops r2-045, -048, -053, -064 and -067 (all model psychology).
- `order` shows option_b first on 41 of the 92.
- `order-check` picks 46.
- The bettor's settings match §2: model claude-opus-5-5, effort low with thinking omitted, max_tokens 4000, and the same `SYSTEM`/`user_text`, key `bettor-v1`.

### D3. Every control can fail. **Holds.**
- The up-word bettor, a set-up with no judgment, is rejected by ss-b5. So is the up-word rule at 0.80, at the dropped-set rate (0.829) and at field rates fit on the dropped items.
- The coin and anti-oracle bettors are rejected by both bets.
- ss-b4's "control", always-50%, is the one that can't do its job: see D5.

### D4. Rivals are matched. **Holds.**
The comparator is held at 0.75. The bettor can choose its own confidence, but recalibrating the one-bit rule gains nothing: the 0.80 rule beats 0.75 by only 0.0003 [−0.008, +0.009] on the 92. So the bettor can't win by calibration alone.

### D5. A dumb baseline is beaten. **Flaw: F1 (ss-b4, redesign) and F2 (ss-b5).**
These are scratch scripts, not committed. The bootstrap is 10,000 resamples, seed 20261104, with Python's `random`. The results are on the **92 drawn items**. Brier is shown with the 95% interval of the difference from always-50% (ss-b4 passes when its upper end is below 0) and from the 0.75 up-word rule (ss-b5).

| predictor (no judgment) | fit on | Brier | vs 0.5: upper end | ss-b4 | vs up-word 0.75 [95% CI] | ss-b5 |
|---|---|---|---|---|---|---|
| coin 0.5 | — | 0.250 | 0 | null | +0.073 | null |
| up-word 0.75 (the ss-b5 comparator) | fixed in map | 0.177 | −0.030 | **pass** | 0 | null |
| up-word 0.80 | — | 0.177 | −0.021 | **pass** | +0.000 [−0.008, +0.009] | null |
| up-word 0.829 | 146 dropped items | 0.179 | −0.013 | **pass** | +0.003 [−0.011, +0.017] | null |
| up-word, field rate | 146 dropped items | 0.182 | −0.008 | **pass** | +0.005 [−0.012, +0.023] | null |
| **swap-pair rate (shrunk, k = 4)** | **146 dropped items** | **0.165** | −0.033 | **pass** | **−0.012 [−0.030, +0.007]** | null |
| "more" → 0.9, "less" → 0.1, else up-word 0.75 | a-priori | 0.171 | −0.025 | **pass** | −0.006 [−0.020, +0.009] | null |
| down word wins before error/noise/cost/time/… | **written after reading the items** | 0.155 | −0.052 | **pass** | −0.022 [−0.049, +0.000] | null (at the edge) |
| baseline-cue words → 0.9 up | a-priori word list | 0.186 | — | — | +0.009 [−0.005, +0.025] | null |
| longer option 0.6 / shorter option 0.6 | — | 0.245 / 0.264 | — | null | +0.07 / +0.09 | null |
| up-word 0.90 / 0.99 | — | 0.193 / 0.224 | +0.012 / +0.059 | null | +0.016 / +0.047 | null |
| *in-sample swap-pair rate (uses the answers)* | *the 92 themselves* | *0.131* | — | *pass* | *−0.046 [−0.082, −0.011]* | *pass* |

On the full 97 the picture is the same (up-word 0.171; swap-pair from the dropped items 0.158, −0.013 [−0.031, +0.005]).

- **ss-b4:** seven trivial predictors pass. The rule can't show judgment, which §1 itself says. Under P3 and D5 that makes it a redesign, not a pass with a caveat.
- **ss-b5:** nothing fit without the test answers passes, so the rule can fail. But the strongest such predictor, the swap-pair rule, sits 0.012 below the comparator. That is about a third of ss-b5's detectable effect (see power below). An LLM carries the same word-pair prior for free.

  The rule I wrote by hand after reading the items reaches the bound. It is not a fair baseline, but it shows the main rival: "the published sentence is the one that makes the paper look good". Round 1 controlled that rival with the writer's `headline_side` (ss-b2). Round 2 has no such tag ("Tagging it needs judgment"), so ss-b5's baseline is weaker than ss-b2's was. That goes into the wording (F3).

**Power at n = 92** (scratch simulation, 300–400 runs per cell): a share k of items is "known" (p_true 0.85), and the rest follow an up-word prior plus N(0, 0.08) noise.

| k | ss-b4 power | ss-b5 vs up-word | ss-b5 vs both comparators (F2) |
|---|---|---|---|
| 0 | 0.99 | 0.00 | 0.00 |
| 0.2 | — | 0.54–0.71 | 0.04–0.47 |
| 0.3 | — | 0.90–0.93 | 0.34–0.81 |
| 0.4 | — | 0.98–0.99 | 0.73–0.96 |

In each range, the lower number is for a bettor whose unknown items follow the up-word prior, and the higher one for a bettor whose unknown items follow the word-pair prior.

ss-b4 has about 99% power **at k = 0**, which is the problem. Against the up-word rule, ss-b5's detectable effect at 80% power is about −0.035 to −0.04. Round 1's bettor beat its headline baseline by 0.068, so the 92 items are enough for a round-1-sized effect.

### D6. Execution risks are piloted. **Holds.**
The pre-mortem is of kind `design`. The bettor setting was piloted in D18. Round 1 made 276 calls of similar content with 0 refusals. The most sensitive items (r2-073 biosecurity probes, r2-069 cessation medication for teen personas) are factual comparisons. Spend from the caches is $2.7389 ($2.26 left). 138 calls at round 1's $0.0056 cost about $0.77, inside the cap.

### D7. Comparisons match. **Flaw: F3 (scope) and F4 (field labels).**
Round 2 differs from round 1 in all of the following:
1. **Writer:** Opus 5.5 sessions, against a regex template.
2. **Selection:** in round 1 the writer chose each paper's finding. In round 2 the item is the first sentence after the opening one that passes the template. Some are background or known facts (r2-022 "LLM-as-a-Judge is faster and cheaper than human evaluation", r2-084 hyperbolic embedding of trees), or opinion (r2-060).
3. **Item format:** round 1 had an item-specific question, a methods summary of about 49 words, and two paraphrased results of about 11 words each. Round 2 has one fixed question, a fixed 19-word "no summary" note, and the verbatim sentence (about 24 words) beside its one-word flip. The bettor's `SYSTEM` still promises "a summary of the study's methods".
4. **Leakage handling:** round 1 rewrote flagged items once and dropped 3 of 187 (1.6%). Round 2 drops every flagged item: 146 of 243 (60%).
5. **Baseline:** round 1 used the writer-tagged headline side, on 38 of 116 items. Round 2 uses a word-list up side on all items.
6. **Field mix:** round 1's post-cutoff set had 28–30 per field. The 92 drawn are model psychology 30, interpretability 27, scalable oversight 21 and quantum devices 14.
7. **Field labels:** round 1's were checked by the writer. Round 2's are query buckets with off-topic papers (F4).
8. **Dates:** round 1 is 66% October. The round-2 draw is 41% October and 37% July–August, closer to the cutoff, because each query took its newest 600 papers. So model psychology starts on 07-21 and scalable oversight on 07-08.
9. **Draw:** round 1 used every item. Round 2 caps each field at 30 by beacon.
10. **No pre-cutoff arm** in round 2 (no ss-b3 analogue).
11. **Same in both:** bettor model, effort low, max_tokens 4000, `SYSTEM`, `user_text`, leakage model and prompt, venue regex.

More than the writer differs. So round 2 is not the audit's proposed test, which was a non-Claude writer "to the same spec", and a result can't be attributed to the writer. §4 already makes the round-2 vs round-1 Brier descriptive, which is right. But §0 ("the audit … named it as the cheapest overturning test") and §1 ("whether the bettor knows which way findings went") claim more than that.

### D8. Verdict sentences are written. **Flaw: F3.**
A sentence exists for every verdict, including untestable, fragile and the D20 scope sentence. But they use P9's wrong nouns:
- "findings" for template sentences, some of which are not findings;
- "written by a template rather than by its own model family", which leaves out that a Claude model chose 97 of the 243;
- §1's "knows which way findings went", a mechanism the design can't separate from in-sentence reasoning or recognising the published wording.

The ss-b5 sentences also give no numbers (d [lo, hi]).

### D9. One item cannot decide it. **Flaw (minor): F6.**
Leave-one-item-out (`bet_labels`) and leave-one-field-out (`score_r2`) both run, and the crafted bettor's field flip is caught. But `score_r2` sets `label_reported = "<label>, fragile"` only for item flips. The table prints "**pass**; … field flips: model-psychology". So a reader of `r2-tables.md` sees "pass", and the §5.5 sentence depends on someone noticing the field flip.

Two more points:
- Leave-one-field-out doesn't apply the 60-item minimum to what remains. That's harmless at 92, where the smallest remainder is 62, but not after a short stop.
- "Field" here means query bucket (F4).

### D10. Machinery. **Flaw: F5 (lesson), plus engine-side pointers.**
- **Budget:** the $5.00 cap is enforced in code, and `CACHES` now includes the r2 leakage and r2 bettor caches. Holds.
- **Stop on refusal:** `structured` calls `llm._check_stop` (`entangled_mind/llm.py:61`: refusal raises `RefusalError`, max_tokens raises an error). `Caller` writes `results/refusal.md` and exits. The code is unchanged since the D19 stub test except for `CACHES`. Holds.
- **One scale direction:** 1 to 99 on Option 1. Holds.
- **Cache:** keyed by the SHA-256 of (`bettor-v1`, model, SYSTEM, user text), in its own file. Holds.
- **Lesson line:** `ls-ss-b4` is present and matches §0 (`check_prereg.py`: L1, L2 and L3 ok). Its read block matches the ledger: 14 scored, Brier 0.246, 5/14, running (5+1)/(14+2) = 0.375, newest audit ss-b1. Two problems, though:
  - It says "Correcting P3", while ss-b4 is P3's failure: a fixed bar a trivial predictor clears.
  - Its P1 reasoning rests on one outcome (F5).
- **ss-b5 pointers:** ss-b5 has no `ls-ss-b5` line and no `design-reviews/ss-b5.md`. So `python3 ledger/check_prereg.py ss-b5 … --before-run` fails R1 and warns on L2. This is engine-side: add pointer files, or teach `check_prereg.py` to read `also_covers`.

### E23. Seed. **Holds, as far as the record shows.**
- Pulse 1591609 is at 02:25:00.150Z. The previous pulse, 1591608, is at 02:24:00.188Z. The pre-registration was committed at 02:24:39Z. With pulses one minute apart, 1591609 is the first after the commit.
- The three seeds recompute with `ledger/seed.py`: items 17297228536032390272, order 17107093521283368216, order-check 9357504176147922809.
- The seed commit (`e8f921e`, 66 s later) touches only `r2-seed.json` and the fill-in line. There is no `r2-bets.jsonl` and no `r2-bettor-cache.json`, so nothing was drawn or called in between.
- I did not refetch the pulse: my brief allows network reads for arXiv only. `certificate_verified` is false.

### Minor notes, not counted as flaws
- §0 says "Written 2026-11-04 19:23–19:30", but the commit is at 19:24:39. The commit is the record, as §0 itself says.
- `score_r2` would score any primary bet in `items.jsonl`, not only the 92. Only drawn items get bets, so this is harmless.

## Required fixes

Each fix needs a dated DEVIATIONS row (D23 onward), written before any round-2 bettor call and naming this review. The reviewer then confirms in an addendum.

**F1 (D5, ss-b4: redesign).** Withdraw ss-b4 before data:
- Add it to `ledger/bets.jsonl` with `verdict: withdrawn` and `design_review: {verdict: redesign}`. Reason: "on template items 78% of published sentences carry the up word; the up-word rule (Brier 0.177 on the 92 drawn) and five other trivial predictors fixed without the test answers pass the ss-b1 bar, so the rule cannot show judgment (P3)".
- Leave it out of the engine's Brier. Count it in the withdrawal rate.
- The bettor's Brier against 0.25 may still appear in the results as a **descriptive secondary**, next to the up-word rule's 0.177, with the sentence "on these items always-50% is not a meaningful bar".
- Keeping ss-b4 as a scored bet at 70 isn't an acceptable alternative. Revising the odds doesn't fix a rule a trivial predictor passes.

**F2 (D5, ss-b5: fix first).** Add a second comparator, fixed now:
- **The rule:** the swap-pair rule. For the swap pair of each item, the probability on the up option is (ups + 4 × 0.829) / (n + 4), counted on the **146 leak-dropped template items only**. The values are: larger/smaller 0.621, more/less 0.850, improve… 0.975, higher/lower 0.634, faster/slower 0.759, increase… 0.789, longer/shorter 0.863, better/worse 0.870, stronger/weaker 0.914, outperform… 0.938.
- **Code:** write it into `score.py` as a second `headline_p`, with a synthetic `--synthetic swappair` bettor that must come out null.
- **Pass rule:** ss-b5 passes only if the paired upper bound is below 0 against **both** the 0.75 up-word rule and the swap-pair rule. Leave-one-item-out and leave-one-field-out run on that combined label.
- **Odds:** they may be revised before data, with both numbers kept.
- **Why:** this tightens the bar and lowers none.
- **Fallback:** if the author prefers to keep the pass rule as it is, the swap-pair comparison must be reported, and the ss-b5 pass sentence must carry the F3 qualifier whenever the swap-pair bound is not below 0.

**F3 (D7/D8, wording).** Replace these, with any numbers filled from the scorer:
- **§0 source row:** "the audit of ss-b1 named a non-Claude writer to the same item spec as the cheapest overturning test; this round changes the item format as well as the writer, so it is a related test, not that one."
- **§1, the sentence beginning "ss-b5 (beat the up-word rule) is the test of whether the bettor knows…":** "ss-b5 tests whether the bettor picks the published sentence better than rules that know only that abstracts usually report gains and which comparative words they favour. It cannot say whether that comes from knowing the result, from reasoning within the sentence, or from recognising the published wording."
- **ss-b5 pass:** *"On n comparative sentences from arXiv abstracts posted after its training cutoff, each shown beside the same sentence with one direction word flipped (chosen by a fixed template; a Claude leakage checker dropped 146 of 243 candidates), the bettor beat a rule that puts 75% on the 'higher / more / better' wording (paired Brier difference d [lo, hi]) and a rule that uses only which comparative word was flipped (d2 [lo2, hi2]). This does not separate knowing the result from reasoning within the sentence or recognising the published wording, and it does not show whether round 1's items were made easier by their Claude writer."*
- **ss-b5 null:** *"On n comparative sentences from post-cutoff arXiv abstracts, the bettor was not shown to beat a rule that puts 75% on the 'higher / more / better' wording, or one that uses only which comparative word was flipped (d [lo, hi]; d2 [lo2, hi2]). Round 2 changes the item format as well as the writer, so this does not show that round 1's pass came from its Claude writer."*
- **Fallback qualifier for F2:** append *"; it was not shown to beat a rule that uses only which comparative word was flipped (d2 [lo2, hi2])."*
- **§6, add:** *"Unlike round 1 (ss-b2), no baseline here encodes 'the published sentence makes the paper look good'; a bettor using only that would not be excluded."*

**F4 (D7, field labels).** Add to §6, and label every by-field table and leave-one-field-out row "query bucket":
- At least four "scalable-oversight" items are not about AI: r2-015 (astrophysics), r2-018 (solar physics), r2-033 (plasma simulation) and r2-035 (microbial ecology).
- Several "interpretability" items apply probes outside AI interpretability: r2-072 (bird bioacoustics), r2-075 (machine fault diagnosis), r2-092 (weather).

Keep the bettor's prompt and items as frozen.

**F5 (lesson and odds).** Revise `ls-ss-b4` before data and keep the old text:
- It should say that ss-b4 is withdrawn under P3.
- It should say the "P1 overcorrection" rests on one outcome (ss-b1), while the ledger still shows the engine's Brier (0.246) worse than the base-rate reference (0.230). P1's `do_this` therefore stands.

The ss-b5 odds (35) need no change unless F2 is adopted, which allows a revision with both numbers kept. Engine side: add `ls-ss-b5` and `design-reviews/ss-b5.md` pointers, or `also_covers` support in `check_prereg.py`, so R1 and L2 pass for ss-b5.

**F6 (D9, code).** In `score_r2`:
- Set `label_reported = f"{label}, fragile"` when `field_flips` is non-empty.
- Mark a leave-one-field-out remainder under 60 items "untestable" rather than labelling it.
- Rerun the four synthetic bettors, plus one that fails on one field only, and show the fragile label printed.

**F7 (Rule 2, one item).** r2-041's arXiv comment says "Reviewed at Collective Intelligence 2026 (CI 2026) Conference. Revised version…". Fixed-rules Rule 2 moves a paper whose comments name an earlier public version dated before 2026-07-01. The template's regex catches only ICML 2026 and TMLR, so it never checked this one.
- Find the CI 2026 dates and say where they came from.
- If a public version predates 2026-07-01, remove r2-041 from the primary set (n = 91) under a DEVIATIONS row, before the bettor call.
- If not, say so in §6.

## Seen and kept (not flaws)

- The leakage drop does not shape the set by direction (p = 0.41).
- The D22 extension depends only on the count.
- The comparator was fixed in the map before any item existed.
- The beacon draw and the seeds recompute.
- The budget, refusal stop and caches are as in round 1 after D19.
- §4's dry run is correct and openly reported.
