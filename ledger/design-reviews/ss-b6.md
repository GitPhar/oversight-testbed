---
bet: ss-b6
program: settled-science
prereg_commit: c9787f9
lesson_commit: 84e2ff5
map_commit: d97a485
reviewer_session: design-review ss-b6 (fresh subagent launched by the engine session; no chat, transcript or author message read)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true          # reviewer, author, bettor and the planned valence rater are all claude-opus-5-5
date: 2026-11-04 20:22 America/Denver
checks: {D1: holds, D2: holds, D3: flaw, D4: flaw, D5: flaw, D6: holds, D7: flaw, D8: flaw, D9: holds, D10: holds, E23: holds (no draw; no seed needed), E25: holds}
flaws: 5
pilot_usd: 0.00
verdict: fix-first
confirmed_at: null
---

# Design review of ss-b6

## In plain English

As built, this test could not answer the question the ss-b5 audit asked. The audit's rival is "the bettor picks whichever sentence makes the paper look good". The frozen rule compares the bettor's raw probabilities with a valence rater's raw probabilities. Two things make that nearly a pass by construction.

- **The neutral items.** On the many items where the swapped word is neither good nor bad news (about half, by my rough reading), an honest valence rater says 50. On those items the bettor scores about 0.8 from the "papers report more/higher" habit that ss-b5 showed the up-word rule already matches.
- **The scale.** A valence rater is not trying to give a calibrated probability that a sentence was published, so its Brier score partly measures how it uses the scale.

On the real ss-b5 bettor ratings, the frozen rule says **pass** for every one of these synthetic raters: a coin, an "always up" rater at 75 or at 99, the swap-pair rule, a rater with the wrong scale direction, and a valence rater that is perfect wherever valence applies and says 50 elsewhere.

A null is ambiguous in the other direction. The rater is the same model as the bettor, and its prompt still says the two options are "versions of one sentence from a research paper's abstract", so it may answer "which one is real" rather than "which one flatters".

The fixes need no new data and no new calls, and they tighten the bar:
1. reframe the rater's prompt as two hypotheticals, with valence defined;
2. add a second, required leg that compares the two sides only after both are recalibrated the same way, with the up word available to both;
3. add three gates that need no answer labels;
4. pre-register the up/down split and a greedy flip count as a robustness check;
5. rewrite the verdict sentences.

With those fixes, a pass would answer the audit's question for this model and prompt. A null would stay partly ambiguous, because only a rater from a different model family can fully separate valence from knowledge, and none is available here.

## Checks

All runs used program 1's interpreter with a no-op `dotenv` stub first on `PYTHONPATH` (so `.env` was never loaded), `ANTHROPIC_API_KEY` unset, and, for the run tests, a fake `llm.client` with every write sent to the scratchpad. The scratch scripts are in `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/19f84df9-a6ff-48ba-89d6-d3f43e5d1747/scratchpad/` (`check_order.py`, `sim_b6.py`, `sim_b6_more.py`, `sim_b6_fair.py`, `sim_b6_fair2.py`, `stub_run.py`). Nothing in the program tree was written: `git status programs/settled-science` is clean. No paid call was made.

**D1. A stranger can apply the rule: holds (for the rule as frozen).** I applied §5 to the synthetic tables below. Each returns exactly one of pass, null or untestable, plus the "fragile" qualifier. `score_b6` matches §4–§5:
- paired difference (1 − p)² − (1 − v)²;
- numpy percentile bootstrap, seed 20261104, 10,000 resamples;
- `upper < −EPS`;
- n ≥ 60;
- leave-one-item-out, and leave-one-bucket-out by `field` (the round-2 query buckets, as in ss-b5);
- every leave-one-bucket-out remainder is ≥ 62, so none is untestable.

F2 below adds a leg. Its specification is written so that a stranger can apply it too.

**D2. Every manipulation takes effect: holds.**
- **Settings.** `valence.py --dry-run` prints the frozen SYSTEM prompt and 92 jobs. The stubbed request has `model claude-opus-5-5`, `output_config.effort "low"`, `max_tokens 4000`, a JSON schema, and no `tools` or `thinking` field. That is the bettor's D18 setting.
- **Option order.** `check_order.py` shows the rater's `option_1_is` equals the bettor's primary `option_1_is` on 92 of 92 items, the item ids are identical, and the option texts match. The published option is shown first on 51; the up option on 44; 21 items are down-word.
- **Orientation.** `p_true_of` turns each valence row's own `option_1_is` into v_true correctly: a synthetic oracle gives a rater Brier of 0.010 and a coin 0.250.

**D3. Every control can fail: flaw (F3).** The dry run checks the scoring, not the rater. No pre-registered control can reject a rater that is set up wrong:
- **Wrong scale direction.** The scale wording ("1 means Option 2 clearly makes it look better") is an easy one to misread. A rater that reads it backwards gives the frozen rule a large **pass**: an inverted valence rater scores Brier 0.599, d −0.529 [−0.588, −0.465].
- **A rater that is only the up-word rule.** It also gives **pass** (−0.107 [−0.151, −0.064]), and the pass sentence would then claim "not only picking the flattering version".
- **A rater that answers "which is real".** Nothing in the record would show it.

Three checks that need no answer labels are missing (F3).

**D4. Rivals are matched: flaw (F1, F2).** This is the central problem. Synthetic raters were run against the real ss-b5 bettor ratings and scored with the author's own `score_b6` (`sim_b6.py`). To build raters with a known shape, I coded each published sentence roughly by hand:
- 37 flattering: the audit's 10 down-word wins, plus 27 clear method wins carried by up words;
- 6 unflattering: the audit's r2-036, -059, -063, -073, -080 and -083;
- 49 neutral.

This coding is a same-family judgment, used only to build the synthetic raters.

| synthetic rater | rater Brier | frozen rule: d [95% CI] | label | up-word 71: d [CI] |
|---|---|---|---|---|
| coin (50) | 0.250 | −0.180 [−0.200, −0.157] | pass | −0.193 |
| always up, 75 | 0.177 | −0.107 [−0.151, −0.064] | pass | −0.005 [−0.022, +0.014] |
| always up, 99 | 0.224 | −0.154 [−0.239, −0.074] | pass | **+0.057 [+0.040, +0.077]** |
| swap-pair rule | 0.165 | −0.095 [−0.147, −0.046] | pass | +0.017 |
| valence, c = 0.6–0.97 where valenced, **50 where neutral** | 0.190–0.221 | −0.120 to −0.151, all bounds < −0.08 | **pass at every c** | about −0.10 to −0.16 |
| valence where valenced, up word (0.75) where neutral, c = 0.9 | 0.117 | −0.048 [−0.090, −0.010] | pass, fragile | +0.015 |
| copy of the bettor | 0.070 | 0 [0, 0] | null | 0 |
| oracle (90/10) | 0.010 | — | null | — |

1. **A valence-only rater cannot win the frozen leg.** It loses even when it is perfect on every valenced item. Its loss comes entirely from the neutral items, where it rightly says 50 and the bettor's up-word habit scores. ss-b5 already showed that habit ties the up-word rule there (−0.005). So a pass would show "the bettor beats valence alone", which ss-b5's own result already implies. It would not show "beats valence plus the up-word habit", which is the audit's actual rival: the margin over the up-word rule came only from the 21 down-word items, and the question is whether valence explains those.
2. **The verdict depends on how the rival is built, not only on what it knows.** Feed the same synthetic valence rater through three reasonable constructions and you get three answers:
   - the raw rule (frozen): pass;
   - valence, else the up word, with leave-one-out confidence, against the raw bettor: **null** (−0.040 [−0.090, +0.004]), because the calibrated rival also gains from the bettor's known under-confidence (ss-b5: mean confidence 0.81, share right 0.93);
   - both sides recalibrated the same way (F2): pass (−0.056 [−0.107, −0.010]).

   The rival has to be matched to the bettor on scale and given the up word, as the bettor effectively has it.
3. **The same-model rater can collapse toward the bettor (bias toward null).** The frozen SYSTEM text says the options are "two versions of one sentence from a research paper's abstract. They differ in one word." That is close to the bettor's own `methods` line ("the same sentence from the paper's abstract, differing in one word"). It sets up a "spot the original" task, and "abstract" is itself the "abstracts report wins" cue the rival is about.

   The construct "the paper's own method **or result** look better" is also ambiguous for the many evaluation and finding papers here: r2-016, -038, -063 and -069 are model-psychology and bias findings, where a "better" result can mean "more striking". The model can settle that ambiguity using the same judgment of which sentence was published that the bettor uses.

   Recall is unlikely: the audit found no sign of memory on these post-cutoff items. Inference within the sentence is what both share.

   What would separate valence from knowledge: (a) a rater from a different model family, which is not available here (no key may be looked for), so it is the replication path, not a fix; (b) a prompt that presents both options as hypotheticals, drops "abstract" and "versions", and defines valence as good or bad news for the paper's own method (F1); (c) a pre-registered scan of the rationales for "which is real" reasoning (F3). (b) and (c) cost nothing. With them, a pass is informative. A null stays partly ambiguous, and its sentence must say so (F5).

**D5. A dumb baseline is beaten, and the design can see the effect: flaw (F2, F4).**
- **Dumb raters are labelled correctly, as pass, under both the frozen rule and F2.** This covers the always-up rater (at 75 and at 99) and the swap-pair rule. Under F2, all of them reduce to the up-word rule after the fit (−0.128 [−0.179, −0.077]; swap-pair −0.120 [−0.172, −0.069]). The copy is exactly null under F2 (0 [0, 0]) and the oracle is null (+0.052). That is correct.
- **The down-word items can decide the result alone.** The always-up-99 rater gives a frozen-rule pass while the bettor is reliably *worse* on the 71 up-word items (+0.057 [+0.040, +0.077]). Greedy removal flips it with 10 items, all down-word; for the swap-pair rule it takes 9, and for the up-word rule 15, all down-word. §4 lists the up/down subsets as "reported, not tested", and nothing in the reading changes if the pass lives only in the 21 down-word items. A genuine pass is expected to sit mostly there, since that is where valence and the published sentence can disagree, but it has to be stated as a pre-registered robustness check with a consequence, not left as a table (F4).
- **Power.** This is not a "no difference" rule, so no equivalence margin is needed. Under my coding the F2 leg sits near its edge (pass, greedy flip 2). That fits odds of 25, and it means the pass sentence has to carry the flip count (F4).

**D6. Foreseeable execution risks: holds; no pilot.** The pre-mortem's kind is `world`, and the items are short technical sentences. The bettor's 138 calls on the same items parsed 138 of 138, with no refusal, a median of 113 output tokens (maximum 358) against the 4000 cap, and a cost of $0.0048 per call on average ($0.0094 at most).

**D7. Comparisons match: flaw (F1).** Differences between the bettor's primary call and the rater's call:
1. the question (forecast vs valence): the named factor;
2. the scale's meaning: part of the named factor;
3. the **field line**, present for the bettor and absent for the rater;
4. the bettor's question and methods lines (the forecasting frame), deliberately dropped;
5. the "from a research paper's abstract … differ in one word" frame, which **both** carry, and which is a contamination route for the rater (D4.3);
6. call date and time (same model id; not controllable);
7. cache key.

Option order, model, effort, max_tokens and schema match. Difference 3 is unnamed and costs nothing to match. Difference 5 is a shared frame that should not be shared. F1 fixes both.

**D8. The verdict sentences are written: flaw (F5).** §5 has pass, null, untestable, fragile and scope sentences, and they use nouns the design can carry. But:
- the null sentence omits the same-model caveat, which §6 itself names;
- the pass sentence would be false if the rater only reproduced the up-word rule;
- the F2–F4 outcomes have no sentences.

**D9. One item cannot decide it: holds.** Leave-one-item-out and leave-one-bucket-out are pre-registered, and a flip appends "fragile" with a written sentence (§5.4). The code implements both. The P10 "cousin" (a few chosen items) is handled under D5 and F4.

**D10. Machinery: holds, with notes.**
- **Budget.** `bettor/r2-valence-cache.json` is added to `common.CACHES`, so the shared $5.00 cap counts it. Spent so far is $3.4017 by summing the five caches, which leaves $1.598. The estimate is 92 × about $0.0048 ≈ $0.44, and the worst case at the bettor's highest observed per-call cost is about $0.86. In the stubbed run with $0.40 calls, the run stopped at the cap after 4 calls ("budget cap $5.0 reached").
  - Note: calls already in flight are not counted before the check, so with 6 workers the cap can be overshot by up to 5 calls (at most about $0.40 at the 4000-token ceiling). That needs per-call costs about 4× the bettor's maximum, so it is not a flaw for this bet.
- **Stop on refusal.** With a stubbed refusal on call 10, the run stopped after 10 calls. Each user text was sent once, nothing was retried, `results/refusal.md` was written (to the scratch root) with the request id, and the 9 earlier ratings were saved. A stubbed `max_tokens` stops with an error. `structured()` calls `llm._check_stop` (restored).
  - Note: the SDK client has `max_retries=4`. That retries transport errors and 429/5xx responses, never a refusal, which is a 200 with `stop_reason: refusal`.
- **Cache.** The key is a content hash, `key_of("valence-v1", MODEL, SYSTEM, user)`, and 92 jobs give 92 unique keys. Any prompt change under F1 gives new keys. The schema and max_tokens are constants, not part of the key.
  - Note: the cache is written every 25 calls and at exit. A hard kill can lose up to 24 paid rows from the spend count. This was inherited and accepted before.
- **One scale direction** (1–99 on Option 1; 99 means Option 1 is better news).
- **Seed.** See E23.
- **Lesson.** See E25.

**E23. Seed: holds; no seed is needed.**
- `valence.jobs()` makes no draw. It reuses `sample_r2` with the ss-b4 beacon's `items` sub-seed and `draws()` with its `order` sub-seed (r2-seed.json, beacon pulse 1591609, recomputed in the ss-b5 audit).
- `valence.py` contains no `random` call.
- `score_b6` uses the fixed bootstrap seed 20261104.
- The F2 leg is a deterministic leave-one-out fit.

There is nothing left for the author to choose by chance, so a new beacon seed would decide nothing. §8's `seed_source` ("inherited … no new draw") is right.

**E25. Lesson: holds, with notes.**
- The §0 row is in c9787f9, and `ls-ss-b6.lesson` matches it exactly (`check_prereg.py`: L1, L2 and L3 ok; R1 fails only because this file did not yet exist).
- The read block matches `ledger/brier.md` at c9787f9: 15 scored, Brier 0.267, 6/15, running (6+1)/(15+2) = 0.41. The newest audit at that commit is `ss-b5.md` (28a8d0b).
- P3's `do_this` (a pre-registered dumb comparator, beaten by a paired bound) is in the design. P10's (leave-one-out, with its consequence) is too.
- The odds are 25 against a running 0.41. The reason given comes from the ledger (the audit's coding of the down-word hits).
- Notes:
  - the line is 64 words against the 60-word rule, as ls-ss-b1 (87) and ls-ss-b4 (71) were, with the "Read:" tail;
  - it omits "(from 25% on the map)";
  - it says it "pre-registers the down-word subset", while §4 only reports that subset. F4 makes the claim true.
- If F2 moves the author's odds, record that move as the review's (`odds_after_review`), not the lesson's (`odds_after_lesson` stays 0.25), as the ss-b5 audit's hole 9 required.

## Required fixes

Each fix needs a DEVIATIONS row in `programs/settled-science/DEVIATIONS.md`, dated before any valence call and naming this review. After the fixes, re-run `valence.py --dry-run` and `score.py --b6 --synthetic` for every kind listed in F2, and paste the output into the rows. The odds may be revised before data, with both numbers kept.

**F1 (D4, D7) → D32. The rater's prompt: hypothetical framing, valence defined, field matched.** Replace `SYSTEM` in `bettor/valence.py` with this text, verbatim:

> You will see the research field and two versions of a sentence reporting a study's result. They differ in one word. Treat both as hypothetical: do not try to judge which one a paper actually contains.
>
> Write a short rationale of at most 100 words. Then give the probability, as a whole number from 1 to 99, that Option 1 is better news than Option 2 for the method, system or approach that the paper itself proposes or defends. 1 means Option 2 is clearly better news for it; 99 means Option 1 clearly is; 50 means the difference is not good or bad news for anything the paper proposes.

Then:
- make the user text `f"Field: {it['field']}\n\nOption 1: {o1}\nOption 2: {o2}"`, which matches the bettor's field line and still has no question, methods or forecasting frame;
- bump the key tag to `"valence-v2"`;
- update §2 and §6 to say that a "more striking finding" (publishability) rival is not tested by this prompt.

**F2 (D4, D5) → D33. A second, required leg: a calibration-matched comparison with the up word on both sides.** The bet passes only if **both** legs have a paired upper bound below 0 on at least 60 items:
- **Leg 1** is the frozen raw comparison, unchanged.
- **Leg 2** is new. For each item, oriented to Option 1 (y = 1 if Option 1 is the published sentence):
  - features for a side with rating r (percent on Option 1): `[logit(clip(r/100, 0.01, 0.99)), u, u·[|r − 50| ≤ 5]]`, where u = +1 if Option 1 is the up option and −1 otherwise;
  - the bettor's features use its primary rating, and the rival's use the valence rating;
  - each side's probability for item i is a logistic regression with **no intercept** (option order is random), fitted by Newton's method (50 iterations, ridge 1e-3) on the other 91 items, then applied to item i;
  - statistic: the mean of (y − p̂_bettor)² − (y − p̂_rival)², with the same percentile bootstrap (seed 20261104, 10,000 resamples) over items and the leave-one-out predictions held fixed;
  - for leave-one-item-out and leave-one-bucket-out, drop rows without refitting.

  The reference code is `fit`, `feats` and `leg2` in the scratch file `sim_b6_fair2.py`.

  Add `--synthetic` kinds `alwaysup99`, `swappair`, `inverted` (100 − a valence-like rater) and `valence50` (the copy's direction on items the bettor rates ≥ 70 or ≤ 30, 50 elsewhere). Report every kind's two legs. The expected labels:

  | synthetic kind | leg 2 | overall |
  |---|---|---|
  | coin, up-word, always-up-99, swap-pair | pass | pass |
  | copy | exactly 0, null | null |
  | oracle | null | null |
  | inverted | the same as the non-inverted rater (leg 2 does not depend on scale direction) | set by gate G1 under F3 |

  Rewrite §1, §4 and §5 to name both legs.

**F3 (D3) → D34. Three gates that need no answer labels, computed and reported before scoring.**
- **G1, scale.** Among valence ratings ≠ 50, the share that favour the up option. If it is **below 0.50**, the rater most likely misread the scale. The verdict is **untestable**, with its sentence. This uses only `up_side`, never `true_option`.
- **G2, up-word copy.** If that share is **at least 0.95**, append the qualifier: *"; the valence rater favoured the up word on x of y items, so it behaved almost as the up-word rule and this result largely repeats ss-b5."*
- **G3, "which is real" reasoning.** Count the rationales that match, case-insensitively, `\b(original|real|actual|actually|published|authentic|genuine|abstract|plausib\w*|edited|altered|modified|likely (?:the )?(?:reported|written|true))\b`. If **at least 10** match, a null gets the qualifier: *"; in m of n rationales the rater reasoned about which version is real, so it may share the bettor's judgment, and this null does not show the pass reduces to flattery."* A pass is unaffected.

**F4 (D5, D9) → D35. The down-word split and the greedy flip count as a robustness check.** For leg 2, pre-register the up-word (71) and down-word (21) paired differences, each with a CI. Then:
- if the label is pass and the up-word subset's **lower** bound is above 0, append *"; on the 71 up-word items the bettor was worse than the comparator (d [lo, hi]), so the pass rests on the 21 down-word items."*;
- always report, and append to a pass, the greedy flip count: remove items in order of largest bettor advantage on leg 2 until the upper bound reaches ≥ 0, then append *"; removing k chosen items (j of them down-word) would flip it."*;
- also report, as a secondary only, the discordant-pair table: items where the bettor's favoured option differs from the rival's (valence if |v − 50| > 5, otherwise the up word), with an exact one-sided sign test.

**F5 (D8) → D36. The verdict sentences.** Replace §5.1–§5.3 with these.

**Pass:**
> *"On n round-2 sentence pairs, the bettor picked the published sentence better than the same model asked only which version is better news for the paper's own method (raw: d₁ [lo, hi], valence rule Brier v), and better than that rating combined with the up word once both were recalibrated the same way (d₂ [lo, hi]). Round 2's pass is not only picking the flattering version or the up word, though this does not separate knowing the result from reasoning within the sentence, and the rater was the same model as the bettor."*

**Null** (either leg's upper bound ≥ 0; name the leg or legs):
> *"On n round-2 sentence pairs, the bettor was not shown to pick the published sentence better than the same model asked only which version is better news for the paper's own method (raw d₁ [lo, hi]; recalibrated with the up word d₂ [lo, hi]). Round 2's pass may reduce to picking the flattering version, or the rater, being the same model, may have used the same judgment of which version is real; this test cannot tell those apart."*

**Untestable:**
> *"Too few valence ratings were returned to test it (n of 92; reason)."*

or, for G1:
> *"The valence rater favoured the up word on only x of y items, which suggests it misread the scale, so the comparison was not run as a test."*

Keep §5.4 (fragile) and §5.5 (scope), and append the qualifiers from F3 and F4 in this order: G2, G3, down-word, greedy, fragile.

### Confirmation

The reviewer confirms the five DEVIATIONS rows and the re-run dry-run output in a short addendum to this file before the go. No valence call runs before that.
