---
bet: om-p2-2
program: other-minds (program 2)
prereg_commit: fc00c58
results_commit: df4adee
auditor_session: audit2 worktree, subagent audit of om-p2-2 (clean copy of df4adee in scratchpad om-p2-2/repo)
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5 (fc00c58 and df4adee both carry "Co-Authored-By: Claude Opus 5.5")
same_model_family: true
date: 2026-11-04 15:26 America/Denver
claims_checked: 34
holes_found: 11
overclaims_cut: 13
reproduced: true
verdict_claimed: null            # pre-registered label is "fail" (§5.2: Q < 0.80); the template has no "fail", so it is entered as null = predicted event absent
verdict_after_audit: null        # "fail" stands; the explanations attached to it do not
verdict_stands: true
canary: unknown
false_alarms: 0
failed: true
failure_reason: The pooled Q fails because in about a quarter of true-belief stories the third-person attribution keeps Noor's old belief although she saw the change, and the second-person world-judgment does not; most of those stories state the outcome she saw, so this is the model, not the filter. Kind world.
failure_kind: world
premortem_score: kind_only
risk_seen: null
---

# Audit of om-p2-2: Perspective-filter equivalence

## In plain English

The verdict stands. Even on the pooled statistic the pre-registration chose as the primary (and said in advance was the lenient one), the two renderings score Q = 0.50 against a bar of 0.80. The table regenerates byte for byte from the archive. All calls fall between the pre-registration commit and the results commit, and the second-person stories that first appear in the results commit were made by the pre-registered step-1 model calls. They match the cache exactly and change grammatical person only. What does not stand is most of the explanation the write-up builds on the fail:
- The exploratory claim that the high true-belief attributions are "cause-only perception" stories, and so "part of this failure is the design's", is contradicted by the items. Of the 48 such stories, 25 state the outcome Noor saw ("Amara discovers the hairline crack", rated 96), and only 15 name a cause alone. Removing the cause-only stories moves Q from 0.50 to 0.55. Removing the outcome-named stories moves it to 0.62.
- "The attributions are more extreme than the world-judgments" is false on true-belief stories and on the FB − TB gaps.
- The "+9-point curse of knowledge" is a typical 5-point pull at a ceiling, plus two stories that flip by 92 points each.
- The order-arm contrast ("moves the attribution but not the world-judgment") rests on two or three items per cell and survives no correction.

Pooling deserves one more line. A predictor that knew only whether Noor saw the change would already score Q = 0.48 against rendering (i). The 0.50 "story-by-story" agreement is almost all the TB/FB split.

## The case that this result is false

The headline says attributing a belief is not the same as judging the world from the agent's evidence. Three things could make that false while leaving Q at 0.50. First, the filter: rendering (ii) keeps the event in true-belief stories whenever the agent "sees" something. Where she perceives only a cause, (ii) gives "you" more evidence than Noor had, so a mismatch there is built into the design, not the model. The results file concedes this itself. Second, the question wording: (i) asks "how likely is it that Noor believes X", and in 162 of 200 stories the text states "Noor believes X" verbatim. The model may simply be reading back a sentence, which is a property of the prompt, not of attribution. Nothing in the design separates question wording from person (§6). Third, the statistic: pooled Q is driven by the TB/FB split, and rendering (i) has only 47% of its variance between conditions. A modest number of anomalous items could then sink Q without any general difference between the two operations, and the within-condition Qs sit on floors (25% of TB (ii) ratings are 0) and ceilings (median FB (i) 94.5) that restrict range. If the anomalous items are the cause-only stories, then "fail" reflects the filter, not the hypothesis. The verdict should then read "untestable as built", not "attribution is a different operation".

What the checks found. The first and third parts of this case fail on the record. Most of the anomalous TB items state the outcome, so the filter is not the main cause. Single-item deletion barely moves Q (0.496–0.510). Making TB agreement perfect would pass (0.86), while making FB agreement perfect would not (0.63). The fail is real on this set, and it is a TB phenomenon. The second part (wording and verbatim read-back) cannot be ruled out by this design and is the best live rival for *why* (i) behaves as it does. It does not rescue equivalence, because equivalence as pre-registered is a claim about these two renderings.

## Claims checked

| # | claim (quoted or paraphrased) | check run | outcome |
|---|---|---|---|
| 1 | Pre-registered in fc00c58 "before any call" | request-ID decode, `work/timing.py` | holds: first call 14:53:23, 11 s after 14:53:12 |
| 2 | 11,070 calls | cache count, rid count | number holds as cache entries; 13,050 API requests (hole 9) |
| 3 | $0.61 of the $1.25 cap | sum of cost fields | holds, $0.6054 |
| 4 | no refusal, no missing answers | cache scan; no `results/refusal.md` | holds: 0 missing, 0 non-int, 0 out of range |
| 5 | 195 of 200 rewrites passed the frozen check | independent re-implementation of `rewrite_ok` | holds: 59, 68, 97, 117, 184 fail, all "name in pre" |
| 6 | failures "kept the name as an appositive: 'You, Olumide, …'" | read the five rewrites | partly wrong: 117 and 184 are "You are Leonardo Martinez", "You are Dalia" (hole 10) |
| 7 | pooled Q 0.499 [0.414, 0.589], ρ 0.994 / 0.999 | `work/indep.py` (own bootstrap, seed 7: [0.415, 0.589]) | holds |
| 8 | TB Q 0.070 [0.011, 0.184]; FB Q 0.092 [0.003, 0.254] | indep.py | holds; both r positive (+0.26, +0.30) |
| 9 | means 32.9/13.0, 87.7/81.6; shifts −20.0, −6.1 with CIs | indep.py | holds |
| 10 | r = 0.70; LOO Q 0.496–0.510 | indep.py | holds |
| 11 | FB − TB gaps 54.8 and 68.6 with CIs | indep.py | holds |
| 12 | "pooled test would be easy … any model that tracks seeing should pass" | label-only predictor Q | does not hold: label-only Q = 0.477 (hole 3) |
| 13 | "the two versions share 50% of their story-by-story variation" | condition-centred pooled Q | misleading: 0.076 after removing condition means (hole 3) |
| 14 | "Both versions are highly repeatable (reliability 0.99)" | indep.py | holds (0.987–0.996) |
| 15 | "the two questions rank the stories differently" | Spearman within condition | holds (ρ_s +0.37 TB, +0.12 FB) |
| 16 | TB: "1-in-3 chance … mean 33"; "a quarter above 50, some at 100" | indep.py | numbers hold (24.6% > 50; 4 at 100; median 15) |
| 17 | "The filtered first-person version gives 13" | code reading | mislabel: second person, and unfiltered in TB (hole 8) |
| 18 | exploratory: high TB attributions are cause-only perception stories | all 48 TB (i) > 50 read, `work/tb_high.out` | does not hold: 25 outcome, 15 cause, 8 ambiguous (hole 1) |
| 19 | Ivana, Hiro, Xiomara rated 100 | indep.py | numbers hold; Hiro's aware sentence names the result and (ii) = 100 too (hole 1) |
| 20 | "part of this failure is the design's, not the model's" | `work/cause_split.py` | overclaim: cause-only removal 0.50 → 0.55; outcome-named removal → 0.62 (hole 1) |
| 21 | FB: attribution 6 points higher (88 vs 82) | indep.py | holds |
| 22 | 2 × 2 means 89.0 / 98.2 / 14.3 / 83.5; TB 33.7 / 11.3 | indep.py | holds |
| 23 | 3f − i +9.2 [+4.7, +15.8], "curse of knowledge … about 9 points" | `work/secondary.py` | number holds; size overstated: median 5.0, drop-2 mean 5.6 (hole 4) |
| 24 | ii − 3f −14.7; "surer about what Noor believes than about the world on the same evidence" | design reading; verbatim-sentence count | mechanism not identified (hole 7) |
| 25 | ii − 2u +69.2; 2u − i −74.7 | indep.py | holds |
| 26 | order arm four effects with CIs | indep.py | numbers hold |
| 27 | "moves the attribution but not the filtered world-judgment" | i − ii contrast; LOO; Bonferroni | not supported (hole 5) |
| 28 | "secondary results point the same way" | as 27 | not supported (hole 5) |
| 29 | "Three things separate them" (curse, confidence gap, seeing) | holes 1, 2, 4 | rank and content drift (hole 6) |
| 30 | "(2) A confidence gap: the attributions are more extreme" | extremity \|m − 50\| | false on TB: 37.2 vs 40.9; gaps 55 vs 69 (hole 2) |
| 31 | FB (i): 8% below 50; TB (i): 57% below 20, median 15 | indep.py | holds |
| 32 | primary verdict fail (§5) | re-applied rule; untestable gates | holds: 195 ≥ 150, ρ ≥ 0.5, 0 missing |
| 33 | "The seed hypothesis … does not hold in this simple form" | scope | unscoped (hole 11) |
| 34 | "On this model and these stories … by the test the map set" | scope | holds |

## Checklist

**A1. Pre-registration predates the first call and the archive read.** Holds. fc00c58 author date 2026-11-04T14:53:12−07:00. Request IDs (`/Users/seanpharris/entangled-mind-audit2/audits/tools/ridtime.py -k`, plus my own `work/timing.py`) decode as follows: rewrites 14:53:23–14:54:06 (200), primary 14:54:07–15:07:43 (7,900), 2 × 2 15:07:43–15:09:22 (990), order 15:09:22–15:16:10 (3,960). There are 13,050 unique IDs and none missing, in one continuous run (no gap over 20 s, steps strictly in pre-registered order), ending 78 s before the results commit at 15:17:29. Working-tree mtimes, read-only: `data/p2-2-second-person.json` 14:54:07 (written by `run()` straight after step 1), `results/p2-2-calls.json` 15:16:11, `results/p2-2-perspective.json` 15:16:13, results .md 15:17:18. Note: the prereg text says "Written and frozen 2026-11-04 15:20", which is after its own commit and after the results. D3 (0ee0ee9, 15:04:37, before the results) discloses this and makes the commit time authoritative. Not a hole.

**The second-person file (`data/p2-2-second-person.json`).** Holds. The prereg (§2) says how it is made: one Haiku call per template (step 1, `rewrite_prompt`), filtered by the frozen `rewrite_ok`, and archived to this path. It is data produced by model calls after the pre-registration. All 200 rewrite request IDs fall at 14:53:23–14:54:06. The file equals the cached step-1 outputs (`cache["rewrite|t"]["value"]`) for all 200 templates, so there was no hand edit or later regeneration. It was written before any rating call (mtime 14:54:07, first rating 14:54:07). Selection: the five exclusions are recomputed by my own implementation of the frozen check, and all five fail it for "name in pre", which no one chose after seeing ratings. Fidelity: a word-level diff (`work/fidelity.py`) maps names, pronouns and articles and ignores auxiliaries and agreement. It leaves 7 differences in 780 passages, all typo fixes or agreement ("tat" → "that", "stes" → "set", "goes" → "go"). Length ratios are 0.80–1.02. No information was added or removed. `data/p2-2-items.json` (committed at fc00c58) regenerates byte-identically from the BigToM CSV with the frozen `parse()`, run offline (`work/guarded_run.py runcopy items`; CSV sha256 a14884fb…).

**A2. Pass rule, statistic, split, seed and budget match.** Holds. The code is unchanged between fc00c58 and df4adee (`git diff fc00c58 df4adee -- experiments/p2_2_perspective.py experiments/om_common.py` is empty). The other parameters also match the prereg: Q = r² ÷ (ρ_i ρ_ii) pooled over TB and FB; bootstrap 2,000 over templates, seed 2201; subset seed 2202 (regenerates to the archived 50); cap 1.25; R = 10; max_tokens 100/1,000; no system prompt. The untestable gates are applied as written. Minor: the prereg says "'you' appears"; the code checks `pre` only. Immaterial, since all 200 rewrites have "you" in pre, aware and not_aware.

**A3. Bar not lowered.** Holds. 0.80, no deviation row after data.

**A4. Reported primary is the pre-registered primary.** Holds. The pooled Q is primary in §4, and the prereg says before data that it is the lenient test and that the within-condition Qs are secondary and reported beside it. The results table labels them correctly. "Fail" is the §5.2 label for the §4 statistic.

**B5. Ties and floating point.** Holds for the primary: Pearson on item means, no tie-breaking. Floors and ceilings: 25% of TB (ii) ratings are 0 and 25% of TB (ii) items have zero repeat variance. 71% of 3f ratings are 100, and 41% of 3f items average exactly 100. Range restriction from these floors and ceilings may depress the within-condition Qs (Spearman exceeds Pearson in TB: +0.37 vs +0.26). It would not raise the pooled Q to the bar.

**B6. Pooling.** Hole (write-up, not verdict); hole 3. The pooled Q is almost entirely between-condition variance. Condition alone explains 47.7% (disattenuated) of rendering (i)'s pooled item-mean variance and 79.6% of (ii)'s. A predictor that knows only the condition gives Q(i, label) = 0.477, against the observed 0.499. With condition means removed, the pooled Q is 0.076. Unpooled, the result is worse (0.07, 0.09), so pooling flatters rather than manufactures the result. "Fail" is robust in both directions. But the plain-English line "share 50% of their story-by-story variation", and the claim that "any model that tracks seeing should pass", misdescribe the statistic. A perfect seeing-tracker scores 0.48, because rendering (i) itself has large within-condition variance. Decomposition (`work/which_condition.py`): replacing (ii)'s FB items with (i)'s (perfect FB agreement) gives 0.627, still a fail. Replacing (ii)'s TB items with (i)'s gives 0.856, a pass. The fail is a TB phenomenon.

**B7. Few items.** Primary holds: LOO 0.496–0.510, within TB 0.056–0.085, within FB 0.064–0.114. Secondaries: hole (holes 4 and 5).
- 3f − i: mean +9.20, median +5.0, 10% trimmed mean +5.2. Two templates (67, 39) go from 4.3 and 3.9 in (i) to 97.9 and 95.9 in 3f, and carry 40% of the sum. Dropping those 2 gives +5.6, dropping the top 5 gives +4.2, and 28 of 49 items lie within ±5. The direction is robust (Wilcoxon p = 3.7e-8). The size is not "about 9 points".
- Order arm: the attribution effects are carried by 2–3 items each flipping by about 90 points (TB −98.5, −92.1, −82.8; FB +91.1, +90.2, +48.6). The medians are −1.0 (TB) and +0.6 (FB). Without the top 3 the means are −4.4 and +1.1.

**B8. Circular estimators.** Holds. Nothing is fitted. The subset is a seeded draw, and the rewrite filter is frozen and blind to ratings.

**B9. Baselines.** Hole (part of hole 3). The obvious dumb baseline (condition label only) ties the observed pooled Q (0.477 vs 0.499) and is not reported. It does not change the verdict.

**B10. Uncertainty.** Holds. Template-cluster bootstrap as pre-registered, and my own bootstrap with a different seed reproduces the CIs to ±0.01. Ratings are aggregated to item means before any statistic.

**B11. Multiple comparisons.** Hole for the order arm (hole 5). The prereg calls the secondaries descriptive and uncorrected, and the results file does not say they are uncorrected. I count 14 secondaries (2 within-Qs, 2 shifts, 2 gaps, 4 2 × 2 effects, 4 order effects). At Bonferroni α = 0.0036, the 2 × 2 effects and the shifts survive: 3f − i t-test p = 0.0014, Wilcoxon 3.7e-8. None of the four order effects survives on the t-test: i TB p = 0.017, i FB p = 0.044. The direct contrast (i effect − ii effect) is −8.9 [−17.8, −0.6] in TB and +2.8 [−3.6, +12.2] in FB. And "not the filtered world-judgment" depends on the test: ii FB Wilcoxon p = 0.0009.

**B12. Leakage.** Holds. Nothing is fitted.

**C13. Scope.** Mostly holds: "On this model and these stories" and "One model; BigToM" are stated. Hole 11: "The seed hypothesis … does not hold in this simple form" is unscoped. The commit headline "Attributing Noor's belief is not judging the world from Noor's evidence" is unscoped, and it is also not what was tested on the file's own account: the file says the filter did not hold Noor's evidence fixed.

**C14. Rank drift.** Hole 6. "What this means" lists "three things separate them" as findings. (1) is a secondary (holes 4 and 7). (2) is false on half the data (hole 2). (3) is an exploratory post-hoc reading of items, and it is wrong (hole 1). The commit headline puts the secondary "+9 points" next to the primary. The exploratory label is given once, in the plain English, but "So part of this failure is the design's, not the model's" is set in bold as a conclusion.

**C15. Mechanism drift.** Hole 7, plus the mechanism parts of holes 1 and 4.
- "That is a curse of knowledge": 3f deletes both the event and the "does not see/realize" sentence. In 42 of 49 subset stories the 3f text then ends with the verbatim "Noor believes that X", the exact proposition the question asks about. Recency or verbatim read-back cannot be separated from knowledge leakage.
- "The model is surer about what Noor believes than about the world on the same evidence" (ii − 3f): the prereg §6 says nothing separates question wording from person, and the belief question is answered by a sentence in the story.
- "The model's attribution respects that distinction" (cause vs result): contradicted by the outcome-named items.

**C16. Plain English against the table.** Hole; holes 1, 2, 3, 8, 9 and 10.
- Hole 1, cause-only claim. I read all 48 TB stories with (i) > 50 (`work/tb_high.out`; my classification is fixed in `work/cause_split.py`). 25 name the outcome Noor perceived. Examples: 57 "Kwame discovers the termite-infested wood" (99); 95 "Amara discovers the hairline crack in the marble slab" (96); 147 "Haruki notices the collapsed passage" (96); 23 "Amaury notices the jar swap" (96); 93 "Naledi notices the water and puts it back" (95). 15 name only a cause and 8 are ambiguous. Mean (i) is 92.3 in the outcome group and 91.7 in the cause group, indistinguishable. Removing the 15 cause-only templates raises pooled Q to 0.548; dropping 15 random templates gives 0.500 [0.474, 0.528]. Removing the 25 outcome-named templates raises it to 0.624. The file's second example, Hiro, names the result ("witnesses the gust of wind snapping off the branches") and is rated 100 by rendering (ii) too, so it is not a discrepancy at all.
- Hole 2, confidence gap. Mean |m − 50|: TB i 37.2 vs ii 40.9; FB i 42.8 vs ii 32.8. The FB − TB gap is larger in (ii) (68.6 vs 54.8).
- Hole 3, pooling: see B6.
- Hole 8: "the filtered first-person version gives 13" refers to the second-person rendering, which in TB is unfiltered.
- Hole 9: "11,070 calls" counts cache entries. The pre-registration's §3 counts each two-turn conversation as two calls (4,000 for step 4); on that unit the run made 13,050 API requests.
- Hole 10: two of the five rewrite failures are "You are <Name>", not appositives.

**C17. Citations.** Cannot check in full (no network). The results file cites only BigToM. The local copy's LICENSE is MIT, © 2023 Gandhi, Fränken, Gerstenberg, Goodman, consistent with the prereg. The map's literature claims (A7, B20 and others) are not used in the results file.

**C18. Negative stated plainly.** Holds. "Fail" is the first verdict line, and "The engine expected a pass (55). This was a miss."

**D19. Budget.** Holds. `om_common.Caller` checks `spent() >= cap` under a lock before every job, with 8 threads, so the overshoot is at most a few calls. Spend was $0.6054 against the $1.25 cap (estimate $0.41). Costs come from program 1's `config.PRICES` for claude-haiku-5-5 ($0.10/$0.50 per M); billed spend cannot be checked offline.

**D20. Stop-on-refusal.** Holds. `llm._check_stop` raises on `stop_reason == "refusal"` and the Caller stops. There is no `results/refusal.md`. Each key has exactly one entry with unique request IDs, and the single continuous run shows no restart or retry.

**D21. One scale direction.** Holds. Every rating question ends with `TAIL` ("0 = certainly false and 100 = certainly true"), including both turns of the order arm.

**D22. Replication.** Not applicable (no hit claimed). One model, one item set.

**E23. Seed.** Not applicable. Fixed seeds 2201/2202 were frozen in the prereg; this prereg predates the beacon rule adopted from P2-4 (D3).

**E24. Tiebreak.** Not applicable.

**Reproduction.** Run offline with the socket and the Anthropic client patched to raise and the dotenv load disabled (`work/guarded_run.py`), on a separate copy (`om-p2-2/runcopy`). `python -I work/guarded_run.py runcopy --analyse` regenerates `results/p2-2-perspective.json` byte-identical to the archived file, and `items` regenerates `data/p2-2-items.json` byte-identical. My independent code (`work/indep.py`, no project imports) reproduces every number in both tables to the printed precision.

## The pre-mortem, scored

My failure reason, written before reading the pre-mortem: the pooled Q fails because in about a quarter of true-belief stories the third-person attribution keeps Noor's old belief although she saw the change, and the second-person world-judgment does not; most of those stories state the outcome she saw, so this is the model, not the filter. Kind: world.

Pre-mortem (prereg line 17, verbatim): "If this fails, the likeliest reason is curse-of-knowledge leakage: on false-belief stories, reading the whole story pulls "what Noor believes" toward what the reader knows happened, which the filtered story removes by construction." No kind is tagged; from its mechanism (a real model behaviour) it is `world`.

Score: **kind_only**. The named mechanism appears in the 2 × 2 (3f − i +9.2, median +5) but is not why the bet failed. On FB the attribution sits *above* the filtered world-judgment (87.7 vs 81.6), which is the opposite sign to the pre-mortem's prediction for the primary. Perfect FB agreement would still fail (Q 0.627), while perfect TB agreement would pass (0.856). Record notes, not counted as holes: the pre-mortem is a paragraph below the §0 table rather than in it, it says "the likeliest" rather than "the most likely", and it carries no kind tag (operators/premortem.md). D3 says the pre-mortem-with-kind rule applies from P2-4 on.

## Required cuts

1. "Exploratory (not pre-registered): those are stories where Noor's perception names the *cause*, not the result. … The model's attribution respects that distinction. … So **part of this failure is the design's, not the model's**: the two versions do not hold the same evidence in those stories."
   → "Exploratory (not pre-registered, auditor's count): of the 48 such stories, 15 name only a cause ("Ivana feels the earthquake"), where the filtered story gives "you" more than Noor perceived; 25 state the outcome itself ("Amara discovers the hairline crack", rated 96). Dropping the 15 cause-only stories raises Q only to 0.55. The mismatch is mostly the attribution ignoring a stated perception, not the filter."
2. The Hiro example in the Exploratory section ("Hiro witnesses the gust of wind snapping off the branches"): remove it from the cause-only list. It names the result, and rendering (ii) also rates it 100.
3. "(2) A confidence gap: the attributions are more extreme than the world-judgments." → "(2) On false-belief stories only, the attribution is higher than the world-judgment (88 vs 82; 98 vs 84 with the event deleted from both). On true-belief stories the world-judgment is the more extreme (13 vs 33)."
4. "The third is partly a flaw in how the filtered stories were built." → "In 15 of the 48 high true-belief stories this is a flaw in how the filtered stories were built; in most it is not."
5. "Three things separate them." → "Secondary and exploratory results suggest where they differ (uncorrected, 49 stories for the 2 × 2):"
6. "any model that tracks seeing should pass. It did not." → "It did not. Rendering (i) varies a lot within each kind of story, so even a rendering that tracked only seeing would have scored about 0.48."
7. "the two versions share **50%** of their story-by-story variation" → "the two versions share **50%** of their variation across the 390 story-and-condition items, and almost all of that is the seen/not-seen split (with each condition's mean removed, 8%)."
8. "That is a **curse of knowledge**: knowing what happened behind Noor's back pulls the attribution down by about 9 points." → "This is consistent with a curse of knowledge, though deleting the event also deletes the 'does not see' sentence and leaves the story ending on 'Noor believes X'. The typical story moves about 5 points (median); two stories that flip from about 4 to about 97 carry 40% of the mean."
9. "The model is surer about what Noor believes than about the world on the same evidence." → "This contrast changes person and question together and cannot say which matters; in 42 of 49 stories the filtered third-person text ends with the sentence the belief question asks about."
10. "Asking first about the opposite state moves the attribution … but not the filtered world-judgment …" → keep the numbers, add: "These are uncorrected; none survives correction for the 14 secondary tests; the attribution effects come from two or three stories that flip by about 90 points (medians −1 and +1), and the attribution-minus-world-judgment contrast is clear on neither kind of story."
11. "The secondary results point the same way: the attribution is moved by a preceding question and the filtered world-judgment is not." → delete.
12. "The filtered first-person version gives 13." → "The second-person world-judgment (in these stories nothing is filtered) gives 13."
13. "The seed hypothesis ("an account of another mind is a world-judgment run on that mind's transcript") does not hold in this simple form." → "On Haiku and these BigToM stories, the seed hypothesis in this simple form is not supported."

Also, as minor wording fixes not counted in the cuts: "11,070 calls" should read "11,070 cached jobs (13,050 API requests)", and the rewrite failures should read "the name kept ("You, Olumide, …"; "You are Dalia, …")". The commit headline cannot be edited. A follow-up commit should note that "curse of knowledge +9" is a secondary and that "filter partly flawed" covers 15 of 48 stories.

## What would break it next

The fail is not in danger. What is open is *why* rendering (i) keeps the old belief in about 25% of true-belief stories. The cheapest discriminating test (about $0.05, Haiku, 48 + 48 templates × 10) reruns TB rendering (i) two ways. (a) Delete the verbatim initial-belief sentence ("Noor believes X") from the story. (b) Keep it but ask "After this, how likely is it that Noor believes X?". If the high attributions collapse under (a) or (b), the mismatch is verbatim read-back or tense, a wording artefact of rendering (i), and the bet should be re-run with a matched belief question in both renderings. If they survive, attribution on Haiku ignores perceived outcomes in a quarter of stories, a finding about attribution in its own right. A second check, also cheap: rerun (ii) on the 15 cause-only stories with only the cause kept. This would measure the filter flaw directly instead of by inspection. Both need their own pre-registration.
