# P2-2. Perspective-filter equivalence: results

Pre-registered in `experiments/p2-2-perspective.md` (D2), commit `fc00c58`, before any call. `claude-haiku-5-5`, 11,070 calls (200 rewrites, 8,000 primary, 1,000 for the 2 × 2, 2,000 two-turn order conversations, less the cells of the 5 templates that failed the rewrite check), **$0.61** of the $1.25 cap, no refusal, no missing answers. Engine odds 55; Sean's odds not recorded before data. Audited in round 2 (see the next line).

> Audited 2026-11-04 (round 2, entangled-mind audit2 8091d01, audits/om-p2-2.md): verdict stands as fail; 13 required cuts applied in D5.

## In plain English

**The question.** Is saying what Noor believes the same as judging the world from only what Noor saw? We asked "how likely is it that Noor believes X?" about each whole BigToM story. Separately, we retold the story to the model as if it were Noor, leaving out what Noor did not see, and asked "how likely is X?".

**Pre-registered verdict: fail, even on the lenient test.**
- The pre-registration said in advance that the pooled test would be easy: most of the variation is the gap between stories where Noor saw the change and stories where she did not. It did not. Rendering (i) varies a lot within each kind of story, so even a rendering that tracked only seeing would have scored about 0.48. Allowing for noise between repeats, the two versions share **50%** of their variation across the 390 story-and-condition items, and almost all of that is the seen/not-seen split (with each condition's mean removed, 8%) (Q = 0.50 [0.41, 0.59]; the bar was 80%).
- Within each kind of story, they share almost nothing: Q = 0.07 for stories where Noor saw the change and 0.09 where she did not. Both versions are highly repeatable (reliability 0.99), so this is not noise. The two questions rank the stories differently.
- Both versions do separate "saw" from "didn't see": a 55-point gap in the attribution version and 69 points in the filtered version.

**Where they differ.**
- **When Noor saw the change**, the attribution version still gives about a 1-in-3 chance that she holds her old belief (mean 33). The second-person world-judgment (in these stories nothing is filtered) gives 13. In a quarter of these stories the attribution is above 50, and some are at 100.
  - Exploratory (not pre-registered, auditor's count): of the 48 such stories, 15 name only a cause ("Ivana feels the earthquake"), where the filtered story gives "you" more than Noor perceived; 25 state the outcome itself ("Amara discovers the hairline crack", rated 96). Dropping the 15 cause-only stories raises Q only to 0.55. The mismatch is mostly the attribution ignoring a stated perception, not the filter.
- **When Noor did not see the change**, the attribution is 6 points *higher* than the filtered world-judgment (88 against 82).
  - The 2 × 2 on 49 stories separates the parts. Deleting the unseen event from the third-person story raises "Noor believes X" from 89 to 98 (+9 [+5, +16]). This is consistent with a curse of knowledge, though deleting the event also deletes the "does not see" sentence and leaves the story ending on "Noor believes X". The typical story moves about 5 points (median); two stories that flip from about 4 to about 97 carry 40% of the mean.
  - With the event deleted in both versions, "Noor believes X" (98) is still above "X is true, from your view" (84): −15 [−18, −12]. This contrast changes person and question together and cannot say which matters; in 42 of 49 stories the filtered third-person text ends with the sentence the belief question asks about.
- **Order.** Asking first about the opposite state moves the attribution (−10 [−18, −3] when Noor saw the change, +6 [+1, +12] when she did not) but not the filtered world-judgment (−1 [−4, +2] and +3 [−2, +7]). These are uncorrected; none survives correction for the 14 secondary tests; the attribution effects come from two or three stories that flip by about 90 points (medians −1 and +1), and the attribution-minus-world-judgment contrast is clear on neither kind of story. Secondary, on 49 stories.

**What this means.**
- On this model and these stories, attributing a belief is **not** the same operation as judging the world from the other person's evidence, by the test the map set.
- Secondary and exploratory results suggest where they differ (uncorrected, 49 stories for the 2 × 2): (1) A curse-of-knowledge leak of about 9 points. (2) On false-belief stories only, the attribution is higher than the world-judgment (88 vs 82; 98 vs 84 with the event deleted from both). On true-belief stories the world-judgment is the more extreme (13 vs 33). (3) A difference in what counts as having seen something. In 15 of the 48 high true-belief stories this is a flaw in how the filtered stories were built; in most it is not.
- On Haiku and these BigToM stories, the seed hypothesis in this simple form is not supported.

**Limits.**
- The second-person stories were rewritten by Haiku itself. 195 of 200 passed the frozen check. The five that failed kept the name ("You, Olumide, …") and were dropped from both versions.
- The two versions change grammatical person, filtering and the question (belief against world) at once. The 2 × 2 separates person from filtering on false-belief stories only; nothing separates the question wording from the person.
- One model; BigToM's templated, model-generated stories. The engine expected a pass (55). This was a miss.

## Tables

### Primary and within-condition (item = template × condition; 195 templates; 10 repeats; CIs from 2,000 resamples of templates)

| | n | Q(i, ii) | ρ_i | ρ_ii | mean (i) | mean (ii) | shift ii − i |
|---|---|---|---|---|---|---|---|
| **pooled (primary)** | 390 | **0.499 [0.414, 0.589]** | 0.994 | 0.999 | | | |
| true belief (TB) | 195 | 0.070 [0.011, 0.184] | 0.990 | 0.996 | 32.9 | 13.0 | −20.0 [−24.9, −15.0] |
| false belief (FB) | 195 | 0.092 [0.003, 0.254] | 0.987 | 0.992 | 87.7 | 81.6 | −6.1 [−9.1, −3.0] |

- Raw correlation of item means, pooled: r = 0.70. Leave-one-template-out Q range: 0.496 to 0.510.
- FB − TB gap: (i) 54.8 [49.6, 59.9]; (ii) 68.6 [64.8, 72.0].
- **Primary verdict (§5): fail** (Q < 0.80).

### 2 × 2 on false-belief stories (49 templates of the seeded 50 that passed the rewrite check)

| | full story | filtered story |
|---|---|---|
| third person, "how likely is it that Noor believes X" | i: 89.0 | 3f: 98.2 |
| second person, "how likely is it that X" | 2u: 14.3 | ii: 83.5 |

| effect | points [95% CI] |
|---|---|
| filtering, third person (3f − i): the curse of knowledge | +9.2 [+4.7, +15.8] |
| filtering, second person (ii − 2u) | +69.2 [+63.5, +74.6] |
| person and question, filtered (ii − 3f) | −14.7 [−17.8, −12.1] |
| person and question, full (2u − i) | −74.7 [−81.1, −66.9] |

(TB means on the same 49: i 33.7, ii 11.3.)

### Order arm (turn 2 after a question about the complementary state, minus single turn; 49 templates)

| rendering | TB | FB |
|---|---|---|
| (i) third person, belief | −9.7 [−17.8, −2.7] | +5.7 [+1.1, +11.8] |
| (ii) second person, filtered, world | −0.9 [−4.2, +2.3] | +2.8 [−2.3, +6.6] |

### Exploratory (not pre-registered)

- TB, rendering (i): 25% of templates have a mean above 50; 57% are below 20; the median is 15. The highest are stories whose "aware" sentence names a cause rather than the outcome: "Ivana feels the earthquake" (X = the ice is thick and solid, rated 100); "Xiomara witnesses the underwater landslide" (X = the coral colony is healthy, 100).
- FB, rendering (i): 8% of templates are below 50.
- Rewrite-check failures: templates 59, 68, 97, 117, 184 (the name kept as an appositive: "You, Olumide, …").

Archive: `results/p2-2-calls.json`, `data/p2-2-second-person.json`, `results/p2-2-perspective.json`. Regenerate with `python experiments/p2_2_perspective.py --analyse`.
