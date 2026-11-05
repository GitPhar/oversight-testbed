---
bet: ss-b1 (primary), with ss-b2 and ss-b3 (secondary bets, same pre-registration, same run)
program: settled-science (program 4; referee published-record)
prereg_commit: ebd2c80 (author time 2026-11-04 17:31:23; the pre-registration landed inside another session's commit "Design review ng-p3-15", D10); seed commit 1f5c1bf (18:28:39); design review e3efeb5 (18:44:41, fix-first), fixes 954c035 (18:46:26), go 38f2364 (18:50:31), addendum 2 fcc0797 (18:54:16, not go), addendum 3 dbc45ae (18:55:40, go); D20 9d4bcf4 (18:55:41); bettor cleared fc81337 (18:56:32)
results_commit: 7632521 in the audit clone (author time 2026-11-04 18:59:54, "ss-b1 result: pass on all three bets, unreplicated, unaudited"; the clone re-commits, so the engine repo's sha may differ)
auditor_session: fresh auditor subagent launched by the engine session, working only in /Users/seanpharris/oversight-testbed-audit-ss-b1
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5 (item-writer and helper sessions; ledger/lessons.jsonl ls-ss-b1 "model"; the bettor is also claude-opus-5-5)
same_model_family: true          # auditor, author, item-writer, design reviewer and bettor are all claude-opus-5-5
date: 2026-11-04 19:10 America/Denver
claims_checked: 34
holes_found: 7
overclaims_cut: 7                # sentences/rows the auditor requires removed or rewritten (Required cuts 1-7)
reproduced: true                 # scoring/score.py on the archive regenerates scores.json and tables.md byte for byte
verdict_claimed: "[ss-b1] pass (reported 'pass, unreplicated') | [ss-b2] pass (reported 'pass, unreplicated') | [ss-b3] pass (reported 'pass, unreplicated')"
verdict_after_audit: "[ss-b1] pass-unreplicated | [ss-b2] pass-unreplicated | [ss-b3] pass-unreplicated (rests on one field: without model psychology its upper bound is +0.019)"
verdict_stands: true             # every label is the one the results file reports; the cuts are wording, a miscount and a missing robustness sentence
canary: unknown
false_alarms: 0
design_review_missed: ["D9: leave-one-item-out only; no leave-one-field-out (cluster) check on ss-b3, whose label rests on the model-psychology field"]
failed: false
failure_reason: "None: all three bets passed. Had ss-b1 failed, my own most likely reason (written before scoring the pre-mortem, but see the disclosure in that section) was that the bettor's edge on four fields would be uneven, and that a field where it has weak priors (model psychology, whose findings turn on idiosyncratic prompt set-ups) would drag a ~120-item Brier up to the 0.25 line. Kind design."
failure_kind: null
premortem_score: not_failed
risk_seen: false                 # descriptive items were not near 50% (mean confidence 0.68, Brier 0.178); the named shape did appear in one field, model psychology (Brier 0.235 [0.181, 0.293], mean confidence 0.65)
---

# Audit of ss-b1, ss-b2 and ss-b3: the published-record referee, first round

## In plain English

All three passes stand. I re-scored everything from the archived bettor outputs, at no cost, and every table regenerates exactly. The main result (post-cutoff Brier 0.163, 95% interval 0.139 to 0.190) survives everything I tried: clustering by paper, dropping any one field, dropping every paper with a conference or workshop comment, keeping only papers posted in September or later, putting the four moved papers back, and comparing against the best dumb predictors I could build from the item text. None of those came near 0.25. The bettor also beats the publication-bias baseline (ss-b2) under every one of those checks. Seven things must be cut or fixed. (1) The "hidden reasoning used 147 tokens" figure is the total output, not the hidden part; the hidden part is about 35. (2) Four pre-cutoff items, not three, have a post-cutoff first version, and the by-year table puts one of them in the "2026 Jan–Jun" row. (3) "It cannot have read them" says more than the record can support. (4) "Its confidence was too low, not too high" is an exploratory reading, and its interval at the item level touches zero. (5) ss-b3's pass rests on one field: without model psychology it is not shown. Two process lapses are minor. The cheapest thing that could still overturn ss-b1 is an item set written by a non-Claude writer, since the writer and the bettor are the same family.

## The case that this result is false

The bettor and the item-writer are the same model. The writer read the answers, chose which findings to keep, wrote each methods summary, and decided which option was the paper's "headline" side. A model that knows the answer, and writes the setup in its own idiom for a reader that is its twin, can leave cues no outside checker sees. Example: the true option is the sentence the writer composed first, and the false one is a mechanical swap. The leakage checker is a language model too, and it was told which side was true. So "the wording does not leak" is one model's opinion. The "post-cutoff" set is only as clean as the bettor's real training data. The record fixes the cutoff at June 2026 from documentation, but it never says the training data stopped there. Workshop, OpenReview and talk versions of these papers can predate their arXiv v1. The record moved four papers on that ground, and the rule that moved them was written after the design review pointed at specific items, not before. The "publication-bias baseline" is weak by design: it says 0.5 on two-thirds of the items. And the item-writer was told to prefer items whose answer goes against the headline, which handicaps that baseline using knowledge of the answers. Calibration and memory claims are exploratory readings of a 116-item table. Finally, the bettor ran with hidden reasoning, a setting nobody pre-registered, so we cannot see what it did. On this reading, a Brier of 0.163 measures how well one Claude reads another Claude's item-writing, not judgment about science.

The checklist below tests each part of this case. Most of it does not survive: I found no cue a simple predictor can exploit, no sign of post-cutoff recall in the rationales, and no dependence on items near the cutoff. The same-family writer remains open. It is disclosed (§7) and cannot be tested from this archive.

## Claims checked

| # | claim (quoted or paraphrased from the results file) | check run | outcome |
|---|---|---|---|
| 1 | ss-b1 pass: post Brier 0.163 [0.139, 0.190], n = 116 | `scoring/score.py` in a scratch copy; diff against committed tables/scores | holds (byte-identical) |
| 2 | 76% right on the 116 | recomputed | holds (88 right, 1 at exactly 50) |
| 3 | ss-b2: beat the headline baseline by 0.068 [0.036, 0.099]; baseline 0.232 | recomputed; paper-cluster bootstrap; strongest dumb predictors | holds |
| 4 | Against-headline items: 6 of 10 right | recomputed | holds |
| 5 | Pre-cutoff 68 items, Brier 0.105, 90% right; pre − post −0.059 [−0.098, −0.019] | recomputed; cluster bootstrap | holds |
| 6 | ss-b3 "consistent with memory (or … easier; cannot separate)" | leave-one-field-out; rationale recognition split | label holds; rests on one field (hole 5) |
| 7 | Field table (MP 0.235 [0.181, 0.293], 62%; SO 90%, interp 84%) | recomputed | holds |
| 8 | "Its confidence was too low, not too high" | hit − confidence gap, item bootstrap; recalibration slope | overstated (hole 4) |
| 9 | 70–80% calls right 91% (39 of 43); 70%+ right 93% (56 of 60); 60–70% right 57% | recomputed | holds |
| 10 | Mean confidence about 69% | recomputed (0.692) | holds |
| 11 | Engine Brier on the three bets 0.388; 0.358 with pre-lesson odds | arithmetic | holds |
| 12 | "Here that moved the odds the wrong way" / "too pessimistic" | one run, three correlated outcomes | wording (cut 7) |
| 13 | "first posted after the model's training cutoff (July–November 2026), so it cannot have read them" | v1 dates vs arxiv-meta; venue comments; §7 | overclaim (hole 3) |
| 14 | "Three of them (ss-026, ss-027, ss-094) have a first arXiv version after the cutoff" | scanned all pre items' v1 dates | false: four, ss-152 too (hole 2) |
| 15 | By-year row "2026, Jan–Jun … 22" and "moved to pre (D12) … 3" | year_bin on every item | ss-152 (v1 2026-08-27) sits in the Jan–Jun row (hole 2) |
| 16 | "Its hidden reasoning used a median of 147 output tokens per call" | usage fields vs visible JSON length | wrong: 147 is total output (hole 1) |
| 17 | D20 scope sentence present | grep results | present, but once, not beside the verdict sentences (hole 7, minor) |
| 18 | Option order beacon-drawn; order check: same side 95%, \|p+p′−100\| 4.9, pull −0.4 [−1.2, 0.4] | redrew from seed.json; recomputed | holds |
| 19 | Rewritten 0.159 [0.097, 0.234] n = 17; clean 0.164 [0.138, 0.193] n = 99 | recomputed from leakage-status.json | holds |
| 20 | Up-word rule 57/116 post, 40/68 pre | recomputed | holds |
| 21 | Option 1 was reported on 55 of 116 | recomputed | holds |
| 22 | 0 out-of-range probabilities; 0 rationales over 100 words | recomputed (max 100 words) | holds |
| 23 | LOO (10,000 resamples per bound): no flips on any label | scores.json fragile_items | holds |
| 24 | Spend: leakage $0.47, pilot $0.006, primary $1.03, order check $0.52, total $2.02, 490 calls | summed caches; checked one call against the $4/$20 price | holds |
| 25 | 0 refusals | 276/276 jobs have bets; no results/refusal.md | holds |
| 26 | All post items v1 on or after 2026-07-01 | arxiv-meta `published` vs items | holds (earliest 2026-07-31) |
| 27 | D12 moves made before any bettor call, not shaped by outcomes | commit order; effect of the moves | holds |
| 28 | Masked file carries no answer, id or title | key set; text equality with items.jsonl | holds |
| 29 | Seed: CURBy-RNG 1591496, first pulse after 17:31:23 | ledger/seed.py; cross-check with ng-p3-5c's seed commit | holds (re-fetch not done) |
| 30 | Lesson ls-ss-b1 read block (9 bets, Brier 0.236, base rate 0.22, newest audit) | ledger at ebd2c80 | base rate mismatch (hole 6, minor) |
| 31 | Odds 60 → 50 recorded before data | map at 4963270 | holds |
| 32 | "the field closest to itself" (MP) | descriptive aside | stands as an aside; no test claimed |
| 33 | "Most of its skill sits in the items it was more confident about" | calibration table | holds (descriptive) |
| 34 | Design review go before first test call | commit times; request-id ordering | holds as far as the record can show (see E26) |

## Checklist

**A. Was it pre-registered as claimed?**

1. **Holds.** The pre-registration is in `ebd2c80` (author time 17:31:23). The 213 leakage-check calls ran before it (17:17–17:20), as recorded in D5. They are item construction, their rule was committed first (`d3996c9`), and their outputs (`4859d3b`) were committed before the pre-registration. Every bettor call came after. The bettor cache and bets first appear in the results commit. The cache has no timestamps, so the start time of the run comes from E26's evidence below. The text's "Written and frozen 18:45" is wrong. D9 corrects it to the git time, and the order of events holds.
2. **Holds, with dated deviations.** Statistic, unit, bootstrap seed, pass rules and beacon draws are as pre-registered. Every difference has a DEVIATIONS row dated and committed before the run:
   - D11: §9 budget typo; $5 governs.
   - D12: post-cutoff set 119 → 116.
   - D15: verdict sentences use the scored n.
   - D16: LOO on every bet, 10,000 resamples, numpy bootstrap, 1e-12 tolerance.
   - D18: thinking "off" → adaptive at effort low, max_tokens 400 → 4000.
   - D19: stop check restored.
   - D20: scope sentence.
   I confirmed D18's premise in the claude-api reference that D18 cites: on claude-opus-5-5, `{type: "disabled"}` returns 400 at every effort, omitting `thinking` runs adaptive thinking, and effort is the only control. D18 changes the object measured: the bettor reasons, hiddenly, before answering. The change is recorded, scoped by D20, and lowers no bar.
3. **Holds.** No bar moved. D12 and D16 only tighten.
4. **Holds.** The headline is the post-cutoff Brier, as pre-registered. ss-b2 and ss-b3 are reported as their own bets, and secondaries are labelled descriptive.

**B. Is the number real?**

5. **Holds.** Brier has no ties. One post item sits at exactly 50, and accuracy counts it as half. The LOO flags use a 1e-12 tolerance, and no label is near its line: the ss-b1 upper bound is 0.190 against a bar of 0.25.
6. **Holds.** The pre-registered pooling is across four fields and two option orders.
   - **Order:** no first-shown pull (−0.4 [−1.2, 0.4]), and the same side was chosen on 95% of the 92 reversed pairs.
   - **Fields, unpooled:** ss-b1 passes in three of four fields alone. Model psychology alone is null (0.235 [0.181, 0.293]), and the results file says so.
   - **Leave one field out:**

   | field dropped | ss-b1 Brier [CI] | ss-b2 diff [CI] | ss-b3 upper bound |
   |---|---|---|---|
   | interpretability | 0.174 [0.144, 0.205] | −0.055 [−0.088, −0.020] | −0.027 |
   | model psychology | 0.139 [0.114, 0.168] | −0.089 [−0.124, −0.052] | **+0.019** |
   | quantum devices | 0.159 [0.133, 0.189] | −0.071 [−0.107, −0.036] | −0.014 |
   | scalable oversight | 0.181 [0.150, 0.215] | −0.058 [−0.098, −0.018] | −0.026 |

7. **Hole for ss-b3; holds for ss-b1 and ss-b2.** No single item flips any label (pre-registered LOO, recomputed). ss-b1 is far from fragile: dropping the 10 best-scored post items gives an upper bound of 0.205, and dropping the 30 best gives 0.238. The cluster-level check (item 7's "leave-one-cluster-out") breaks ss-b3, though. Without the model-psychology field its upper bound is +0.019, so it would be null. Pre MP is 0.076 and post MP is 0.235, and that one field carries the gap. The results file calls every label "not fragile" and does not report this (cut 5).
8. **Holds.** Nothing is fitted. The baseline's `headline_side` tags were written by a writer who knew the answers, before any bet, and rewrites could not change them. That gives the baseline information the bettor has to infer. It favours the baseline, so it is not circular against the bettor.
9. **Holds.** No dumb predictor ties the bettor. The design review ran a similar set at n = 119 and none passed. My own runs on the 116 post items, in a scratch script, gave:

   | dumb predictor | post Brier | ties the bettor? |
   |---|---|---|
   | constant 0.5 | 0.250 | no |
   | headline baseline, h = 0.75 (pre-registered) | 0.2317 | no |
   | headline baseline, best h in hindsight (0.74) | 0.2316 | no |
   | per-field prior on the "up" direction (leave one out) | 0.263 | no |
   | per-field prior on "the direction the question names first" (leave one out) | 0.258 | no |
   | headline tag + question-order field prior | 0.241 | no |
   | logistic regression on question order, up-word, headline tag and option length difference (leave one out, symmetrised so it cannot use the a/b label) | 0.233 | no |

   - **Bettor against that logistic:** −0.070 [−0.104, −0.035].
   - **Single cues:** the "up" option was true on 57 of 116, the first-named direction on 53 of 102, and the longer option on 26 of 67. None carries a usable cue.
   - **Writer habit:** the writer put the true answer as option_a on 72 of 116 post items and named option_a's direction first in 93 of 102 questions. The bettor never sees a/b, the order is beacon-drawn, and question order does not predict truth (53/102), so the habit does not leak.
   - **"Item length":** length alone cannot pick a direction. Option length difference is in the logistic and adds nothing.
   - **Verdict on ss-b2:** the publication-bias baseline is close to the strongest fair one-bit rule, and the bettor's margin over it holds against everything above.
   - **One honest limit:** the item-spec told writers to prefer items whose answer is on the non-headline side, using the answers. That weakens any publication-bias predictor by construction. It is disclosed in item-spec.md but not in the results file's ss-b2 paragraph. Note added to cut 6.
10. **Holds.** The intervals are at item level. Eight post papers contribute two items each. Bootstrapping by paper (108 post papers) gives the same intervals:
   - ss-b1: [0.139, 0.190].
   - ss-b2: [−0.102, −0.035].
   - ss-b3: [−0.097, −0.019].
11. **Holds (stated).** Three bets, each scored separately, with no correction, as pre-registered. Many secondary tables, all labelled descriptive. ss-b1's margin would survive any reasonable correction. ss-b3's upper bound of −0.019 is the closest to its line.
12. **Leakage: holds, with two cannot-checks.**
   - **Masked file:** carries only id, field, question, methods and options, text-identical to `items.jsonl`. The bettor code never opens `items.jsonl`.
   - **Wording cues:** none exploitable (B9). Rewritten and clean items score the same (0.159 against 0.164).
   - **Hidden thinking (D18):** it adds computation, not information. The request still has no tools and no other message. On the post items no rationale recognises the specific paper. Three post rationales name prior work, and in the one that guessed a "known study" (ss-083) the guess was wrong (p_true 0.35). By contrast, 19 of 68 pre-cutoff rationales say "this matches the … paper", "I recall", and so on. That shows masking does not stop identification of papers the model has read. It cannot help on papers it has not read.
   - **Cutoff split:** every post item's `v1_date` equals the arXiv API `published` field in `arxiv-meta.json`. The earliest is 2026-07-31. 105 of 116 are September or later, and 84 are October or later.
   - **Signs of near-cutoff leakage:** none. Brier by month shows no trend: Spearman of date against squared error is 0.002. Restricted to September+ items, ss-b1 is 0.159 [0.133, 0.187] and ss-b2 is [−0.106, −0.040]. Restricted to October+, ss-b1 is 0.163 [0.134, 0.194].
   - **Venue comments:** 19 post items carry a venue comment (NeurIPS 2026 main/Evaluations & Datasets/workshops, EMNLP 2026, COLM 2026, CoRL/AACL workshops, "under review"). D12's claim that these became public only after June is not verified in the record. In particular, OpenReview visibility for the NeurIPS Evaluations & Datasets track and COLM is asserted, not shown. Dropping all 19: 0.155 [0.129, 0.183], and ss-b2 still passes.
   - **D12 and outcomes:** D12 came before any bettor output existed, so bettor outcomes could not shape it. The writer knew the answers, but the effect is nil: the moved items score 0.179, worse than the post mean, and putting all four post-dated pre items back gives 0.163 [0.138, 0.189].
   - **Writer exclusions (D8) and leakage drops:** four writer exclusions (quote or hedge reasons, recorded before any leakage call) and three leakage drops (all post-cutoff, by the checker's flag).
   - **Cannot check:** (a) the bettor's actual training-data cutoff. The claude-api reference gives claude-opus-5-5's *knowledge* cutoff as June 2026 and states no training-data cutoff. The September+ result covers a cutoff up to the end of August. (b) Whether any post paper had a public precursor its arXiv comment does not name.

**C. Does the write-up say only what the data say?**

13. **Hole (cut 3).** "so it cannot have read them" contradicts the pre-registration's own §7 ("Earlier talks, blog posts or workshop versions could have reached training data"). The scope elsewhere is careful: "for this model on these items", "one model, one prompt, one item set".
14. **Hole (cut 4).** The calibration reading "Its confidence was too low, not too high" is a bold-faced finding drawn from a descriptive table.
   - Item-level gap between hit rate and mean confidence: +0.071 [−0.002, 0.142].
   - A logistic recalibration slope of 1.81 [1.33, 2.48] does point to underconfidence on the whole.
   - The 0.6–0.7 bin (42 items, the second largest) was overconfident: 0.63 confidence, 0.57 right.
   - None of this was pre-registered as a test.
15. **Holds, mostly.** ss-b3's memory reading uses the pre-registered either/or sentence. The archive offers more than the write-up says. The 19 pre items with explicit recognition score 0.022 (19/19 right). The other 49 pre items score 0.137, against 0.163 post: a difference of −0.027 [−0.073, 0.022], which is not shown. So the gap that passes ss-b3 sits mainly on items the bettor says it recognises. That points to memory over "easier items". It is an exploratory split, a recommendation and not a cut. The aside "which is the field closest to itself" (model psychology) hints at a cause no test addresses. It is left as an aside.
16. **Holes (cuts 1, 2, 7).** Sentences the tables do not support:
   - **"Its hidden reasoning used a median of 147 output tokens per call."** Median `output_tokens` is 147, but that includes the visible JSON rationale (median about 112 tokens at 4 characters per token). The hidden part is a median of about 35 tokens. That matches the design review's pilot estimate (about 50 of 162). The API bills omitted thinking inside output tokens, and this is the source of the error.
   - **"Three of them (ss-026, ss-027, ss-094) have a first arXiv version after the cutoff."** Four do: ss-152 (2608.27340, v1 2026-08-27) was moved to pre-cutoff by the writer (D8, ICML 2026 MI workshop). The by-year table's "2026, Jan–Jun … 22" row contains ss-152, and the "moved (D12) … 3" row omits it. The design review flagged this label as non-blocking, and D17 relabelled only the three D12 items.
   - **"The engine's own odds … were too pessimistic … Here that moved the odds the wrong way."** True of this one run's Brier. But three correlated outcomes from one run cannot show the odds were miscalibrated, or that a move toward the base rate was wrong.
17. **Holds as far as checked.** The results file cites only the record (DEVIATIONS, design review, the protocol). D18's API claim checks out against the claude-api reference. I did not open the arXiv abstracts. Each item's evidence quote is recorded verbatim, and the design review's `verify.py` checked the quotes against the API. I spot-read ten random post items. Each quote settles the stated direction, and no methods summary states the result.
18. **Holds.** The model-psychology null and the 28 items where the baseline beats the bettor are stated plainly.

**D. Process**

19. **Holds.** The $5.00 cap is in code (`common.BUDGET_USD`), shared across all three caches. Actual spend is $2.0273, reported as $2.02. One call checked: 636 input and 202 output tokens at $4/$20 per MTok = $0.006584, as recorded.
20. **Holds.** 0 refusals. All 276 jobs have a bet with a unique request ID matching the cache. The D19-restored stop check could not be inspected end to end: `llm._check_stop` lives in program 1's module outside the clone. **Cannot check** that code. D19 and addendum 3 record a stub test.
21. **Holds.** One scale: p_option_1, where 99 means Option 1 was reported.
22. **Holds.** Every bet is reported as "pass, unreplicated".

**E. Engine records**

23. **Seed: holds, re-fetch not done.**
   - `ledger/seed.py` recomputes all three sub-seeds from the recorded randomness: order 13309338689196222401, order-check 16683013961078861871, human-form 14605333098254812962.
   - The bettor's option order and order-check set match the draws for all 184 items.
   - The same pulse 1591496 and the same randomness were recorded independently at 17:32:18 by ng-p3-5c's seed commit `03356ad`. That supports both the value and its time (00:32:00Z, first after 00:31:23Z).
   - I did not re-fetch the pulse or the round before it.
   - Sharing one pulse across two bets is harmless, because the bet id enters the hash.
   - The seed commit came about 56 minutes after the pulse. Nothing drawn in that gap could matter: the draws are fixed by the pulse, and no bettor call ran.
24. **n/a** (not a tiebreak bet).
25. **Lesson: minor hole.**
   - The lesson row is in the pre-registration commit, and §0 carries the sentence.
   - At `ebd2c80`, `lessons.jsonl` held only the sentence's first part. `d36855d` (18:30) set it to §0 verbatim, before data.
   - **Read block:** 9 resolved bets ✓, Brier 0.236 ✓ (`brier.md` at `ebd2c80`), newest audit `om-p2-1-blind-pl-001.md` ✓ (16:51, the latest under `ledger/audits/` at that commit). But "base rate 0.22" is the raw 2/9. learn.md and P1 define the running base rate as (2+1)/(9+2) = 0.27, and the other lessons at that time say 0.27. The read block therefore does not match the ledger's running base rate. The ledger session noted it and did not change it.
   - **Patterns' do_this:** P3 (a dumb baseline as its own bet, ss-b2) ✓; P9 (verdict sentences in §5) ✓; P10 (LOO with its consequence) ✓; P1 (start from the base rate) ✓ in direction.
   - **The odds change:** 0.60 → 0.50 is recorded as `engine_odds_first`/`engine_odds` in the map at `4963270` (16:59), before any item was read. It moves toward the base rate, which learn.md allows without a further reason. Scored against the outcome, the lesson's move cost Brier 0.25 against 0.16 on this bet. That belongs in `ledger/scores.md`'s paired before/after Brier and does not count as a hole.
26. **Design review: holds; one miss.**
   - `e3efeb5` (fix-first, 18:44) came after the pre-registration. The five fixes are D12–D16 (18:46), confirmed go at 18:50.
   - The post-go settings change (D18) was re-reviewed: not go (G1, a removed stop check), fixed in D19, confirmed go at 18:55:40 (addendum 3; its typed "19:00" is wrong against the commit).
   - **Did the test calls follow the go?** The cache carries no timestamps, so the record cannot show the first test call's time to the second. Indicative evidence: Anthropic request IDs appear time-ordered. Calibrating the IDs on the leakage calls (about 17:20) and the D18 pilot (before 18:52:17) places the first test-set call about 3.8 minutes after the pilot. That is near 18:55:40–18:56 for a pilot at about 18:52:00, and the run lasted about 2 minutes. Addendum 3 also records an empty cache at its check.
   - **Cannot check further** without the API usage log. Recommendation: confirm from the Anthropic console that no claude-opus-5-5 call other than the pilot and the failed 400 preceded 00:55:40Z on 5 November, and that no claude-sonnet-5-5 call preceded 00:17:16Z. The design review asked for the second check.
   - **Flaws D1–D10 should have caught:** D9 asked for LOO on every label but not for leave-one-field-out. The four fields are the obvious clusters, and ss-b3 rests on one of them. Listed in `design_review_missed`.
   - The reviewer also flagged ss-152's year label as non-blocking, and that surfaced as hole 2.
   - Addendum 3's wording requirements were only partly carried out (hole 7, minor). The D20 sentence appears once, not "beside every §5 verdict sentence". The §6 sentence ("Both Sean and the bettor could reason before answering; neither could look anything up") is not on `human/form.md`, which was committed before the addendum.

## The pre-mortem, scored

**Disclosure.** While locating the pre-registration I ran a `grep` for "pre-mortem" on it. That printed the pre-mortem sentence before the checklist was done, which breaks auditor.md's order. The one-line reason in the header was still written as my own account, but it was not written blind. The ledger session should weigh this score with that in mind.

**My own reason, had it failed:** the bettor's skill would be uneven across fields. One field where it has weak priors (model psychology) would pull a ~120-item Brier to the 0.25 line. Kind `design`.

**The pre-mortem:** *"If this fails, the most likely reason is that the bettor, without wording cues, sits near 50% on most descriptive items, so a Brier near 0.23 leaves the upper bound above 0.25."* Kind `design`.

**Score: `not_failed`, `risk_seen: false`.** On the 78 descriptive post items the bettor's mean confidence was 0.68, and only 14% of its calls were below 60%. Their Brier was 0.178, well clear of 0.23. The named shape did appear in one field. Model psychology had mean confidence 0.65 and Brier 0.235, with an upper bound of 0.293 above 0.25. It did not sink the bet.

## Required cuts

1. **Remove** "(D18, D20: the model cannot run with thinking off. Its hidden reasoning used a median of 147 output tokens per call.)" **Replace with:** "(D18, D20: the model cannot run with thinking off. Its calls used a median of 147 output tokens in all, of which the visible answer was about 110, so its hidden reasoning was short, roughly 35 tokens per call.)"
2. **Rewrite** "Three of them (ss-026, ss-027, ss-094) have a first arXiv version after the cutoff. They were moved to pre-cutoff before any bet because a workshop or TMLR version may have been public earlier (D12)." **To:** "Four of them have a first arXiv version after the cutoff: ss-152 (moved by the writer, D8, ICML 2026 workshop) and ss-026, ss-027, ss-094 (moved by D12). They were moved to pre-cutoff before any bet because a workshop or TMLR version may have been public earlier." **In the by-year table**, move ss-152 out of "2026, Jan–Jun" into the moved row (Jan–Jun: n = 21; moved: n = 4). Regenerate both rows from `score.py` with `year_bin` keyed on `v1_date ≥ 2026-07-01` rather than `side_note`.
3. **Rewrite** "The 116 that count were first posted after the model's training cutoff (July–November 2026), so it cannot have read them." **To:** "The 116 that count were first posted on arXiv after the bettor's stated knowledge cutoff of June 2026 (31 July to 3 November 2026; 105 of them in September or later), so it should not have read them, though an earlier talk, workshop copy or blog post cannot be ruled out (§7)."
4. **Rewrite** "**Its confidence was too low, not too high.** On the new findings it was right 76% of the time while its average confidence in its chosen side was about 69%." **To:** "**On the whole its confidence looked low rather than high (exploratory, not a pre-registered test).** On the new findings it was right 76% of the time at an average confidence of about 69%; the gap's 95% interval by item is −0.002 to 0.142, so it is not established, and its 60–70% calls were overconfident (right 57% of the time)."
5. **After** "Leave-one-item-out (D16, 10,000 resamples per bound): no single item flips any of the three labels, so none is fragile." **Add:** "By field, ss-b1 and ss-b2 pass with any one field removed, but ss-b3 does not: without the model-psychology items its upper bound is +0.019, so the memory gap rests on that one field (pre 0.076 against post 0.235). This check was not pre-registered (audit)."
6. **In the ss-b2 paragraph, after** "A predictor that only leaned 75% toward that side scored 0.232." **Add:** "Item-writers, who saw the answers, were told to prefer findings that went against the headline (item-spec), which makes this baseline weaker than it would be on a random sample of papers."
7. **Rewrite** "**The engine's own odds on these three bets were too pessimistic.** … Here that moved the odds the wrong way." **To:** "**All three passed against the engine's odds of 50%, 30% and 35%.** Three correlated outcomes from one run cannot show the odds were miscalibrated. The lesson line had moved the main bet from 60% to 50% toward the ledger's base rate (pattern P1); on this outcome that move cost Brier 0.25 against 0.16."

Also (minor, process): repeat the D20 sentence beside the verdict table, as addendum 3 required. Add addendum 3's §6 sentence to `human/form.md` before Sean's calls are scored.

## What would break it next

1. **A different item-writer** (the results file's own item 2, and the strongest open rival): 60 post-cutoff items written to the same spec by a non-Claude model or a person, with the same bettor and prompt. About $0.55 of bettor calls (60 primary calls at about $0.0056, plus a 30-item order check), plus the writer's cost. If the post Brier rises above 0.25 or loses its margin over the headline baseline, the same-family writer was doing the work. This is the cheapest test that could overturn ss-b1.
2. **Memory vs easiness for ss-b3, free:** pre-register the recognition split on the next round. Code whether the rationale names or recalls a specific study, before scoring. Test the pre/post gap on non-recognised pre items only. On this archive, exploratory, that gap is −0.027 [−0.073, 0.022].
3. **The usage-log check** (free): confirm from the Anthropic console that no test-set call preceded the 18:55:40 go, and no leakage call preceded 17:17:16.
4. **A model-psychology replication** (the results file's item 3): 60 more model-psychology post items, about $0.40. It decides both whether ss-b1's weakest field is real and whether ss-b3's single-field dependence is real.
