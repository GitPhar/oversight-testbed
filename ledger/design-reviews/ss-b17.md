---
bet: ss-b17
program: settled-science
prereg_commit: ad2d924
reviewer_session: design review ss-b17 (fresh subagent in the ss-wave5 worktree; no chat or transcript read; has not reviewed ss-b10c or ss-b16)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 16:44 America/Denver
checks: {D1: holds, D2: holds, D3: flaw, D4: holds, D5: flaw, D6: holds, D7: holds, D8: flaw, D9: holds, D10: holds, D11: flaw, D12: holds}
prior_work_search: "LLM-as-a-judge pairwise comparison consistency across prompt templates position bias swapped order" (web search, the LLM-evaluation field's words for the mechanism, not the seed question's); found Shi et al., Judging the Judges (arXiv 2406.07791). Not strictly needed, since the line cites a predicted outcome; run because the noise mechanism matters under D11.
papers_opened: 4
flaws: 3
pilot_usd: 0.00
verdict: fix-first
confirmed_at: 2026-11-05 17:10 America/Denver
---

# Design review of ss-b17

## In plain English

As built, the test can answer a narrower question than its sentences claim. The question it can answer: does each model's accuracy stay within 5 points when ss-b10c's flattery question is asked in other words? The machinery is sound:
- the wording is frozen by hash, and the code refuses to run on a mismatch;
- the two wordings differ only in the system text (checked on all 800 jobs);
- C2 compares the wordings item by item on the same 200 items;
- every verdict is reachable.

The bet can both pass and fail (D11) under every noise model I built. But the committed power numbers rest on a noise level that was assumed, not measured (P15), so they are optimistic:
- "Pessimistic" noise in the dry run actually matches about 5 points of call-to-call spread. Heavier spread, which nothing in the archive rules out, takes P(pass) in the null world from 0.95 down to roughly 0.45–0.90.
- The dry run's shift worlds have no noise at all. So "a 5-point drop passes every time" and "an 8-point drop is caught every run" are artefacts of that set-up. With noise, a true 5-point shift passes about half the time.
- Two sentences say more than the design can show. "The shortcut did not depend on the one sentence" is a no-difference claim from a point estimate. And ss-b10c's forecasting prompt, a different question, would itself meet Haiku's rule and miss Sonnet's by 1.2 points.
- On a fail, "ss-b10c's result depends on its sentence" ignores that call noise alone can push a model out of the window.

Three fixes are needed before the first call: measure the noise, put noise into the shift worlds, and rewrite the sentences. None of them changes the rule or the bar.

## Checks

Commands run (all $0, no API calls):
- `cd programs/settled-science && python3 scoring/dry_b16_b17.py --rules` (about 95 s; reproduces the committed numbers exactly: valence-only P(pass) 0.946, bettor-like 0.150, drop 5 1.000, drop 8/10/15 0.000; every score_b17 verdict reached on synthetic rows).
- `/Users/seanpharris/entangled-mind/.venv/bin/python bettor/brainbench_v2.py --dry-run` (hash ok 72c5be33d360; 400 + 400 calls; about $2.09; spent so far $11.567).
- My own scripts, in `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed-ss-wave5/aadb0e9f-7e6b-4ba3-a7d3-8203f13d7b12/scratchpad/review-b17/`:
  - `noise.py` (the archive's p_avg distribution, the dry run's null reproduced, analytic worst case, the conditional rating-level null, and shift worlds with noise);
  - `sym.py` (the symmetric rating-level null);
  - `d2.py` and `d2b.py` (jobs, keys, user text, hash guard);
  - `d3.py` (controls and wrong set-ups through `score_b17.score`).

**Hash.** `bettor/prompts/flattery-v2.txt` unchanged since 4173f67 (`git diff 4173f67 HEAD` empty). SHA-256 of the file with its final newline stripped = `72c5be33d3601a820d2d1cea00bf6630d8afb653aa320e0c43935e0971385d1d` = `WORDING_SHA256` = `SHA256SUMS` = §2. A copy with one word changed makes `wording()` exit ("does not match its frozen hash"), so the guard works.

**D1 (a stranger can apply the rule): holds.**
- §4 and §5 map one-to-one onto `score_b17.score`: C1 is the bootstrap lower bound > 0.634 + EPS; C2 is |mean paired d| ≤ 0.05 + EPS; pass/mixed/fail count the models that meet the rule; untestable is either model with n < 180.
- `--rules` returns pass, mixed, fail, fail (both too high) and untestable on the five synthetic tables, exactly one verdict each.
- Items are restricted to those with both orders under both wordings, as §4 says.

**D2 (the manipulation takes effect): holds.**
- All 800 jobs carry one system text, equal to the frozen file and different from `brainbench.FLATTERY`.
- The user text equals ss-b10c's flattery user text for the same item and order on 800/800 jobs. The order flag matches the text.
- There are 800 distinct keys. None collides with `bb-cache.json`, `bbb-cache.json` or `bbb-opus-cache.json`. The tag is `bb-flattery-v2`, and the cache `bbv2-cache.json` is new and listed in `common.CACHES`.
- All 800 first-wording comparator calls exist in the archives.
- The `call` argument ("bb-flattery-v2" against "bb-flattery") is only an error label in `common.structured` and is not sent.

**D3 (every control can fail): flaw (folded into F3).** C1 rejects the wrong set-ups it must reject. Run through `score_b17.score` with the first wording as comparator:

| set-up | verdict | Haiku acc | Sonnet acc |
|---|---|---|---|
| constant 50 | fail | 0.500 | 0.500 |
| always Option 1 at 70 (position only) | fail | 0.500 | 0.500 |
| scale reversed (100 − p) | fail | 0.237 | 0.117 |
| copy of the first wording (the null) | pass | | |
| **ss-b10c's archived forecasting (bettor) prompt as the "second wording"** | mixed | 0.810, d +4.8 [−1.8, +11.3]: **meets the rule** | 0.945, d +6.2: misses C2 by 1.2 points |

The last row is the problem. A prompt that asks a different question ("which abstract was published") meets the second-wording rule on Haiku and nearly meets it on Sonnet. So C2, which compares accuracy levels, cannot reject "a different route to a similar accuracy". A pass shows the accuracy level survives the change of sentence. It does not show that the shortcut, or the item-level picks, survive. The design states this limit for valence against plausibility (§6) but not here. Fix in F3.

**D4 (rivals matched): holds.** No rival families compete; each model is compared with itself under two wordings.

**D5 (dumb baseline; power of a no-difference rule): flaw (F2).**
- *Dumb baselines:* constant and position-only responders score 0.500 and fail C1 (table above). Holds.
- *A no-difference claim is made.* The pass sentence says "So the shortcut did not depend on the one sentence ss-b10c used". The rule has a margin (±5 points) and a committed power calculation, so it is not P2's "no margin, no power". But the power calculation is wrong in the two places that carry the claim.
  1. **The shift worlds have no noise.** `drop k` removes exactly round(k·n) right items, so d is exactly −k. Drop 5 lands on the inclusive boundary (|−0.05| ≤ 0.05 + EPS) and "passes" 100%. Drop 8 lands outside and "fails" 100%. With the dry run's own null noise added, P(C2 holds) is:

     | true shift | Haiku | Sonnet |
     |---|---|---|
     | ±3 | 0.77 | 0.86 |
     | ±5 | 0.49 | 0.50 |
     | ±6 | 0.36 | 0.29 |
     | ±8 | 0.13 | 0.05 |
     | ±10 | 0.03 | 0.003 |

     Under the worst-case resampling spread, the ±8 row is 0.24 (Haiku) and 0.18 (Sonnet). The shift at which the window catches 80% is about 7.3 to 8.6 points for Haiku and about 6.5 to 7.7 for Sonnet. That is above the 5-point margin. So a true 5-point move passes as "no difference" about half the time.
  2. **The shift worlds are one-sided.** The rule is two-sided, and an upward move is caught only by C2. Haiku's C1 already fails near −7 (dry run: P(C1) 0 at drop 8), so on Haiku a downward move is caught by C1 as well, and the effective window is about [−7, +5].
- *Why not a redesign.* A true equivalence test (90% paired interval inside ±0.05, TOST) needs |d| ≤ about 0.006 on Haiku at the dry run's noise (paired SD 0.027), and is impossible at the worst case (SD 0.043). That would take P(pass | null) to about 0.1 or below, failing D11. With n fixed at all 200 items, the honest fix is to state what the point-estimate window can see (F2 numbers into §4, F3 sentences). It is not a different rule.

**D6 (execution risks piloted): holds.**
- The pre-mortem is of kind `world`.
- The items, user text and settings are ss-b10c's, which made 800 first-wording Haiku and Sonnet calls with no refusal.
- Output is structured. Mean output was 221 and 208 tokens (max 365 and 317) against max_tokens 1000.
- No execution pilot is needed. The pilot asked for in F1 is a noise measurement under D11/P15, not an execution pilot.

**D7 (comparisons match): holds.** Every difference between the conditions C2 compares:

| factor | first wording (comparator) | second wording |
|---|---|---|
| system text | named factor; the claim is declared to be about the bundle of the two sentences (§2) | |
| user text, schema, max_tokens, models, thinking path | identical (checked) | identical |
| recorded thinking setting | Haiku `disabled`, Sonnet `between_tools` on every comparator row | same code path |
| concurrency | 6 workers | 6 workers |
| time | 2026-11-05 14:03–17:50 UTC, pooled from two runs (ss-b10's archive and ss-b10c) | runs after this review |

Model ids are the same. §6 states the time difference. **All-200 against scored subset:** comparing against the all-200 figures (0.762, 0.882) is right.
- v2 runs on all 200 items, and the scorer computes C2 on the intersection of items, item by item. Comparing a 200-item v2 with 77.5% or 89.7% (100 and 126 items) would mix item sets.
- The subsets were chosen by which order ss-b10 happened to hold, not by outcome, so the all-200 figures carry no selection the subset avoids.
- The subset rows are reported, which is correct.

One caveat goes into F1: v1 is one observed draw. Conditional on it, a fresh draw regresses near-threshold items, so E[d | v1] need not be 0.

**Wording leaks and scale (D7, D10):** holds.
- The second wording says "it does not matter which of them, if either, is real". It does not say which version is real or that one was altered (both wordings say the abstracts differ only in their findings), and it names neither BrainBench nor publication.
- Scale direction: 99 means Option 1's findings favour the idea more, 1 means Option 2's, 50 means neither. That is the same direction as ss-b10c and as `p_option_1`.
- The added notion "would please the authors more" is declared (§2).

**D8 (verdict sentences written, nouns the design can carry): flaw (F3).** The sentences exist and are generated verbatim, but two of them use nouns the design cannot carry:
- the pass sentence's "the shortcut did not depend on the one sentence" (D3 and D5 above);
- the fail and mixed sentences' "ss-b10c's result depends on its sentence" / "depends on the sentence as well as the shortcut". Under a no-effect null, call noise alone fails C2 on at least one model in roughly 2–55% of runs, depending on the unmeasured noise (F1).

**D9 (one item cannot decide it): holds.**
- Leave-one-item-out and leave-one-section-out are pre-registered, computed in `model_block` and reported in a sentence. A flip does not change the verdict.
- C2 is a point estimate, so it carries no bootstrap Monte Carlo error.
- C1's lower bound at B = 10,000 has Monte Carlo error of about 0.001, far from the bar unless Haiku drops about 6 points (P18 does not bite).

**D10 (machinery): holds.**
- *Budget:* `BET_CAP` $2.25, checked before every call through `common.Caller` (stops at cap − $0.05), and the program cap. The program total is $11.57 + $5.95 (ss-b16) + $2.25 = $19.77, under the $21.40 cap.
- *Cost margin:* the estimate uses ss-b10c's per-call cost, but the second system text is 778 characters against 587, about 50 more input tokens. That adds about $0.04 on Sonnet, so expect about $2.13–2.14 against a stop at $2.20. Output is already near the 100-word allowance (mean 208 tokens), so an overrun big enough to drop Sonnet below 180 items (about $0.20) is unlikely. Noted, not a flaw.
- *Other machinery:*
  - stop on refusal, error or truncation is in code (`llm._check_stop`, `Caller`);
  - the cache is keyed by a content hash;
  - there is one scale direction;
  - there is no draw, so no beacon seed is needed (bootstrap seed 20261104);
  - the ratings are written on every exit path (`finally: write_out`).
- *Lesson line:* `ls-ss-b17` is in `ledger/inbox/ss-wave5.jsonl` and matches §0 verbatim. Its `design_change` repeats "an 8-point shift caught every run", which F2 corrects. It cites P8 and P2. P15 (a dry run on assumed spreads) is the pattern the null world actually hits, and F1 adds it.
- *Unrelated edit:* the worktree has an uncommitted edit to `programs/settled-science/reproduce.py` (adds ss-b16 and ss-b17 scorer rows; mtime 16:34). It was not made by this review, is not part of the frozen design, and was left alone.

**D11 (the bet can both pass and fail): flaw (F1); the 10% floor is met.** The dry run's valence-only null, which gives P(pass) 0.946, is not shown to be pessimistic:
1. It flips 0/1 item hits uniformly. Real call noise acts on ratings, so flips concentrate on items whose orders-averaged p_avg sits near 0.5:
   - Haiku has 42 items within 0.02 of 0.5 and 65 within 0.05;
   - Sonnet has 20 and 36.

   Shi et al. 2024 find that order inconsistency is driven by the quality gap between the candidates.
2. Its size is borrowed from the disagreement between two different prompts (flattery against forecasting). That is not a measure of test-retest noise in either direction.
3. To keep expected accuracy fixed, it turns wrong items right with probability 0.54 on Haiku and 0.48 on Sonnet, against 0.15 and 0.05 for right items turned wrong. Its net per-item disagreement is 0.22 on Haiku.

Rebuilt at the rating level from the archived ratings:

| null model | per-call SD (points) | Haiku P(C2) | Sonnet P(C2) | P(both C2) |
|---|---|---|---|---|
| symmetric: two fresh draws around the archived ratings | 3 | 0.98 | 1.00 | 0.98 |
| | 5 | 0.96 | 0.99 | 0.95 (the dry run's number) |
| | 8 | 0.93 | 0.98 | 0.91 |
| | 10 | 0.91 | 0.98 | 0.89 |
| | 15 | 0.88 | 0.94 | 0.83 |
| analytic worst case (every item at q = accuracy) | | 0.76 | 0.88 | about 0.67 |
| conditional on the observed v1 (flat-prior predictive of a fresh draw) | 5 | 0.97 (mean d −1.2) | | |
| | 10 | 0.70 (mean d −4.0) | 0.65 | about 0.45 |

In the conditional model, near-threshold right items regress. The order gap bounds call noise at 18.8 points (Haiku) and 11.3 (Sonnet), so these SDs are not excluded. The archive holds no repeat of any Haiku or Sonnet BrainBench call, so this cannot be settled from data.

- **P(pass) in the valence-only world:** somewhere in about 0.45–0.98. The odds subagent was given 0.95.
- **P(fail) in the sentence-tied worlds:**
  - bettor-like: 0.85;
  - a true shift of 8 points or more on both models, with noise: about 0.98 or above;
  - Haiku's C1 alone fails at −8.

  A world where the second wording costs or gains 5 points passes about a quarter of the time on both models (0.49 × 0.50 at the dry-run noise).
- **Both sides clear 10%** in every version, so this is not a redesign. But the committed numbers, the odds rationale and the reading of a fail all depend on a number that P15 says must be measured, not assumed.

**D12 (the predicted outcome in print): holds.**
- (a) The Prior work line (map ss-f10 and §0) states a prediction, "predicts: mixed", with citations. It is weak but it is an outcome, not a topic.
- (b) Each paper says what it is cited for:
  - Mizrahi et al., *State of What Art?* (arXiv 2401.00595, TACL): 6.5M instances, 20 LLMs, 39 tasks; single-instruction results are brittle. As cited.
  - Sclar et al. (arXiv 2310.11324): up to 76 accuracy points from formatting alone, LLaMA-2-13B, few-shot. As cited.
  - Hua et al., *Flaw or Artifact?* (arXiv 2509.01790): 7 LLMs (GPT and Gemini named), 6 benchmarks, 12 templates; much of the sensitivity comes from heuristic evaluation, and LLM-judge grading reduces variance. As cited, with one nuance. Their robustness comes from grading free-text answers by meaning. Here the structured integer output removes answer-matching artefacts altogether, so any sensitivity this bet sees would be the model's, not the grader's. §0's "the setting 2509.01790 finds more robust" is a slight stretch but not wrong.
  - My search found Shi et al., *Judging the Judges* (arXiv 2406.07791): 15 judges, 22 tasks, over 150,000 instances. Position bias is "strongly affected by the quality gap between solutions". This predicts that wording-driven or noise-driven flips concentrate on small-gap items. That supports F1's rating-level noise model and predicts nothing about this pass rule's outcome.
- (c) No paper tests a valence question, BrainBench or a Claude 5 model, so the outcome is not in print. §0 says what the bet adds.
- (d) Not triggered.

## Required fixes

Each fix goes under one dated DEVIATIONS row, written before any data and naming this review: the next free row, D82 unless ss-b16's review takes it. Any ledger change (the lesson's `design_change`, odds) goes through `ledger/inbox/`. If P(pass | null) moves by more than about 0.05, the odds may be revised before data, with both numbers kept. The rule (C1, C2, the 5-point window, 180 items) does not change.

**F1 (D11, P15): measure call-to-call noise and rebuild the null world from it.**
- **The pilot.** Run Haiku with the **first** wording (`brainbench.FLATTERY`, unchanged) on 80 items of `items/brainbench/gpt4-pilot-pool.jsonl`. These are excluded from the 200, so pilot results are not test data. Each item goes in both orders, two independent draws each: 320 calls, about $0.08, at most $0.10, under its own spend row and cache. No second-wording call is made.
- **Report** the per-call SD of `p_option_1` between draws and the share of items whose orders-averaged pick differs between the two draws.
- **Rebuild** the dry run's ss-b17 valence-only world at the rating level: two independent draws of each archived rating with the measured SD, int-rounded and clipped to 1–99, symmetric as in `sym.py`. Report the conditional version beside it (a fresh draw against the observed v1), and the analytic worst case as a bound.
- **Sonnet:** if no Sonnet repeats fit the $0.10, use the Haiku SD and also report SD 8, 10 and 15.
- **State** the source of each number beside the world (P15), and add P15 to `ls-ss-b17`'s patterns.
- **Odds:** if the rebuilt P(pass | null) differs from 0.95 by more than 0.05, re-elicit the odds with a fresh v2 context and keep both.

**F2 (D5, P2): give the shift worlds noise and both signs, and correct the power claims.**
- In `scoring/dry_b16_b17.py`, `b17()`'s `drop k` worlds become `shift ±k` for k = 3, 5, 6, 8, 10. Each applies the true shift on top of the F1 null noise, not as an exact removal of right items. Print per-model P(C1), P(C2), P(meets), the joint P(pass), and the shift at which each model's window catches 80%.
- Replace §4's sentence "if it costs 5 points, 1.00; 8, 10 or 15 points, 0.00. So the window can see a shift of 8 points or more" with the new table and this sentence: "C2 is a point estimate: a true 5-point move in either direction passes about half the time; the window catches a move of about <k80> points 80% of the time on Haiku and <k80> on Sonnet; on Haiku a drop of about 7 points also fails C1."
- Correct `ls-ss-b17`'s `design_change` ("an 8-point shift caught every run") through the inbox to the same numbers.

**F3 (D8, P9, with D3's evidence): rewrite the verdict sentences to the nouns the design carries.** Change `score_b17.sentences` and §5 to match.
- **Pass.** Replace "So the shortcut did not depend on the one sentence ss-b10c used; this design still cannot tell valence from plausibility or memory of the papers." with:

  > "So ss-b10c's accuracy was not tied to its one sentence, to within what 200 items can show: C2 is a point estimate, and a true move of 5 points would pass about half the time (paired intervals as above). The models' picks agreed across the two wordings on <Haiku same-pick>% and <Sonnet same-pick>% of items, against about <floor>% expected from call-to-call noise alone (F1's pilot). ss-b10c's forecasting prompt, a different question, also comes within 5 points of the first wording on Haiku, so a pass shows that the accuracy survives a change of sentence, not that the second wording is answered the same way item by item. This design still cannot tell valence from plausibility or memory of the papers."
- **Mixed.** Replace "so on <other> ss-b10c's result depends on the sentence as well as the shortcut" with "so on <other> ss-b10c's accuracy did not survive the change of sentence (call-to-call noise alone takes a model outside the 5-point window in about <p>% of the dry run's null runs)".
- **Fail.** Replace "so ss-b10c's result depends on its sentence" with "so ss-b10c's accuracy did not survive the change of sentence on either model (call-to-call noise alone takes both models outside in about <p>% of the dry run's null runs)".
- **Wiring.** <floor> and <p> come from F1's rebuilt null and are fixed in the scorer before any call. Add the bettor-prompt comparison (`d3.py`'s last row: Haiku d +4.8, meets; Sonnet d +6.2) to §4's secondary statistics as a reported reference row.

## Addendum: fixes confirmed (2026-11-05 17:10 America/Denver)

Read at commits 453d718 (D82, pilot), b5787de (D83, fixes) and 773b566 (odds revised). No paid call was made; the only repo write is this addendum.

**F1: holds.**
- **Pilot data checked independently** (`bettor/bbv2-pilot.jsonl`):
  - 320 rows, all `claude-haiku-5-5`, first wording;
  - 80 items, none of them among the 200 test items;
  - each item in both orders, two draws each;
  - cost $0.0774.
- **Draw-to-draw differences:** n = 160, symmetrised SD 15.47 points, 39.4% identical. These match D83.
- **The author's choice of main null is right.**
  - The main null treats each wording as a fresh draw around the archived ratings, with per-call error equal to the pilot difference divided by √2.
  - Two such draws differ by exactly the measured draw-to-draw spread, and by symmetry the mean shift is zero (−0.001). This is the symmetric null I asked for.
  - The other version adds a whole difference to the already-noisy observed v1 and compares against that fixed v1. That is a flat-prior predictive, and it overstates regression of near-threshold items. Keeping it as the pessimistic bound is the right use of it.
- **The numbers agree with my own simulation.**
  - Main null: P(pass) 0.91.
  - Pessimistic bound: 0.70.
  - Analytic worst case beside them: 0.76 and 0.88 per model.
  - My Gaussian symmetric null at a per-call SD of 10–12 gave 0.86–0.89. The empirical, heavy-tailed noise (39% identical) plausibly gives slightly more.
- **Rerun:** I reran `scoring/dry_b16_b17.py --rules`. Its output is byte-identical to `scoring/dry_b16_b17.txt` at b5787de.
- **Odds:** re-elicited from a fresh context, 0.37 → 0.45, with the first number kept (773b566). The `<re-elicited>` placeholder in `ls-ss-b17`'s `lesson_revised` is filled, and P15 is added.
- **Remaining limit:** Sonnet is given Haiku's noise, not its own. D83 says so, and Sonnet's worst case (0.88) is reported.

**F2: holds.**
- **The shift worlds now carry the measured noise and run in both directions.** Per model, P(C2 holds) at a true shift of ±5 is 0.51–0.53, at ±8 it is 0.09–0.14, and the 80%-catch point is about 8 points either way.
- **The text is corrected.** §4's replacement sentence is in D83, and `ls-ss-b17`'s `design_change` is corrected through the inbox.
- **One new fact:** on Haiku, P(C1) is only 0.46 at a true 5-point drop. This is because noisy draws pull Haiku's expected accuracy about 2 points below the observed 0.762. D83 states it.

**F3: holds.**
- **The pass sentence** now says "accuracy … not tied to its one sentence, to within what 200 items can show (a point estimate; a true 5-point move passes about 53% of the time)", and adds the forecasting-prompt caveat.
- **The mixed and fail sentences** now say "accuracy did not survive the change of sentence", with the null-run rates: 9.1% main, 30.3% pessimistic.
- **Same-pick sentence and reference row:** the same-pick sentence prints the noise floor, and the forecasting-prompt reference row is computed and printed.
- **The constants are fixed in `score_b17.py` before any call.**
- **One non-blocking note.** The dry run's noise floor (0.818 Haiku, 0.888 Sonnet) is the share of items with the same item score (0, 0.5 or 1). The scorer's `same_pick` counts tie-versus-wrong as the same pick. Under the same null that definition gives 0.838 and 0.898. So the printed floor is 1–2 points lower than the scorer's statistic would show from noise alone.
  - It affects a reported sentence only, not the rule or the verdict. The auditor should read the same-pick comparison with this in mind.
  - Either matching the definitions or adding a one-line note before the run would remove it. Neither is a condition of this confirmation.

**Worktree state (not part of this confirmation).** When this addendum was written, the shared worktree had another session's uncommitted edits:
- `scoring/dry_b16_b17.py`, `score_b16.py`, `reproduce.py` and `ledger/design-reviews/ss-b16.md`;
- `scoring/dry_b16_b17.txt`, which was **empty on disk**, mid-rewrite.

ss-b17's design is confirmed as committed at b5787de and 773b566; `score_b17.py` has no uncommitted change. Whoever commits the dry-run output next should check its line count (62 lines at b5787de) and must not commit an empty file.

**Verdict: fix-first, confirmed. The run may start.**
