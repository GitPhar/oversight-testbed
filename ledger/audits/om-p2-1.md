---
bet: om-p2-1
program: other-minds (program 2)
prereg_commit: 8fb40f3
results_commit: 5931024
auditor_session: audit2 worktree, subagent audit of om-p2-1 (clean copy of 5931024 in scratchpad om-p2-1/repo)
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5 (8fb40f3 and 5931024 both carry "Co-Authored-By: Claude Opus 5.5")
same_model_family: true
date: 2026-11-04 14:58 America/Denver
claims_checked: 24
holes_found: 7
overclaims_cut: 4
reproduced: true
verdict_claimed: null            # pre-registered label is "fail" (§5.2: equivalence event Q >= 0.90 and |shift| < 3 not met); the template has no "fail", so it is entered as null = predicted event absent
verdict_after_audit: null        # "fail" stands
verdict_stands: true
canary: unknown
false_alarms: 0
failed: true
failure_reason: Haiku rates a minority of claims very differently under "how confident are you" (18 of 160 move by more than 30 points, against 3 of 160 in the same-wording retest), so Q(a, b) is 0.77; the design was adequate (rho 0.98, retest Q 0.96). Kind world.
failure_kind: world
premortem_score: kind_only
risk_seen: null
---

# Audit of om-p2-1: Whose belief is a rating? The framing check

## In plain English

The verdict stands: "how likely is it that this statement is true" and "how confident are you that this statement is true" do not give interchangeable statement-by-statement ratings on Haiku for this item set. The table regenerates byte for byte from the archive. The number holds under every alternative I tried: other reliability estimates (Q 0.76 to 0.78), rank correlation (ρ² 0.80), a label-swap null for truly interchangeable framings (Q 0.987 [0.955, 1.015], none of 2,000 shuffles at or below 0.772), and within-question centring (0.75). What has to change is the reading. The gap is carried by a minority of claims: removing 7 of the 160 lifts Q to 0.90. The write-up says the wording change "reorders the statements". It does not. Most statements keep their numbers and about one in nine flips. Four sentences need rewriting: the "Sam is not further from you" sentence, which the point estimates contradict; "reorders the statements"; "the wording that names the self", which the design cannot separate from the change of verb; and the "another AI assistant" CIs, which are uncorrected secondaries. The pre-registration's stated freeze time (14:45) is also wrong. Git and the API timeline put the commit 15.7 s before the first call. The cheapest way to break the verdict's interpretation would be a 2 × 2 design (verb × subject) on a second item set with no self-referential claims.

## The case that this result is false

The headline says the two framings are "not interchangeable", and the evidence is one squared, disattenuated Pearson correlation on 160 item means. Those means are bimodal: 43% of framing (a)'s raw ratings are ≤ 5 or ≥ 95, and the top values are 97, 3, 85, 90 and 15. On a bimodal variable Pearson's r depends almost entirely on which mode each item sits in. A few items that cross from one mode to the other therefore cost a lot of r², while hundreds of items that agree closely add little. The flip table in the results shows exactly such crossers (92 → 13, 11 → 84, 7 → 73). Many of them are claims *about an answer or about the writer* ("The part (b) error alone is enough to make the stated answer incorrect", "Without a reliable source, the candidate answer Rollo should not be affirmed"). For those, "how confident are you" can reasonably be read as asking the model about its own stance towards the candidate answer, not about the world. On this reading, the failure is a property of a handful of oddly worded, self-referential items in an item set taken from the model's own reasoning, not a general property of "how likely" against "how confident". By the authors' own exploratory split, the correlation is 0.88 on the claims that are not self-referential. The leave-one-question-out check, the only robustness check reported, removes 4 claims at a time from one question, so it cannot detect a gap spread across 5 to 8 claims in different questions. The 0.90 bar is also strict next to its own reference: even identical wording across sessions reaches only 0.955. Finally, (b) changes two things at once, the verb (likely → confident) and the subject (it → you), so nothing here licenses talk of "the self".

What the checklist found: the first half of that case is right about *interpretation* (7 claims carry the gap; the "self" reading is not identified). It is wrong about the *verdict*. The pre-registered rule is an item-level statistic over all 160 claims. The observed Q is far outside what interchangeable framings produce (the label-swap null's 2.5th percentile is 0.955). The flips are not noise: 18 claims move by more than 30 points between (a) and (b), against 3 in the same-wording retest. And the bar is lenient, not strict, next to the null (0.90 sits below the entire null range).

## Claims checked

| # | claim (results file) | check run | outcome |
|---|---|---|---|
| 1 | "6,400 calls, $0.27 of the $0.40 cap" | count, sum of `cost` in archive | holds (6,400; $0.2650) |
| 2 | "no refusal, no missing answers" | all 6,400 values ints in 0–100; no `results/refusal.md` | holds |
| 3 | "Pre-registered … before any call" | git author/reflog time vs request-ID times | holds (commit 14:35:02, first call 14:35:17.7); stated freeze time 14:45 is wrong, hole 5 |
| 4 | "Pre-registered verdict: fail" | rule §5 applied with own code | holds |
| 5 | Q(a,b) 0.772 [0.651, 0.880] | independent recomputation, same seed; seed 777 | holds ([0.645, 0.879] at seed 777) |
| 6 | shift +0.12 [−2.71, +2.81] | independent | holds |
| 7 | "the whole interval is below it" | bootstrap tail | holds at 95% (0.55% of resamples ≥ 0.90; 99% upper 0.903) |
| 8 | all six pairs and the a–p1 Q, shift, r, CIs | independent | holds, all to 3 d.p. |
| 9 | per-framing mean, \|m−50\|, SD, ρ | independent | holds |
| 10 | test–retest Q 0.96 [0.88, 1.01] | independent; prompt, model, max_tokens, schema, thinking compared in `gm3b_format_invariance.py` | holds; fair same-wording cross-session reference |
| 11 | "This is not noise between sessions" | Q(a,p1) − Q(a,b) = 0.183 [0.085, 0.305] | holds as evidence; wording loose (a and b were in the same session), not cut |
| 12 | "changing … reorders the statements" | leave-k-out, greedy removal, Spearman | **overclaim**: ρ_s 0.896; 7 claims removed → Q 0.900; 18 of 160 move > 30 pts |
| 13 | "Some statements flip outright" + exploratory table | own means | holds (all six rows match, rounded) |
| 14 | "makes the answers vaguer: … 31 against 34" | bootstrap | holds: 3.07 [1.57, 4.66] points closer to 50 |
| 15 | "more variable between repeats (SD 8.3 against 5.8)" | bootstrap | holds: +2.60 [0.91, 4.39] |
| 16 | b–d secondary fails, Q 0.67 [0.53, 0.79] | independent | holds |
| 17 | "'Sam' is not further from 'you' than 'how likely' is" | Q(a,b) − Q(b,d) bootstrap | **hole**: point estimates say Sam *is* further (0.667 vs 0.772; diff +0.105 [−0.029, +0.244]) |
| 18 | "all the cross-framing Qs lie between 0.56 and 0.77" | table | holds |
| 19 | "Another AI assistant … CIs excluding 0 against" a, b, d | Bonferroni over the 12 secondary intervals | **hole**: uncorrected; corrected CIs a–c [−1.9, +10.4], b–c [−0.8, +9.3], c–d [−7.5, −0.1] |
| 20 | "the wording that names the self changes which statements get high numbers" | design inspection | **mechanism drift**: (b) changes both verb and subject; (c), (d) do not name the self and differ more |
| 21 | 28 self-referential claims: r 0.71 vs 0.88 | own keyword guess (`writer\|memory\|confirm\|uncertain`) | reproduces approximately (n 28, 0.708 vs 0.881); the rule is not in the record, hole 6 |
| 22 | LOQO range 0.763–0.802, "No single question carries the result" | independent | holds as stated; leaves out that 7 claims across 5 questions carry it (hole 2) |
| 23 | "One model (Haiku), one item set" | scope | holds |
| 24 | "Regenerate with `python experiments/p2_1_framing.py --analyse`" | run offline, network blocked | holds: `p2-1-framing.json` byte-identical (`cmp`) |

## Checklist

**A1. Pre-registration predates the first call.** *Holds, with a record hole.* Author date of 8fb40f3 is 14:35:02 −07:00, and the reflog entry agrees. The first decoded request ID is 14:35:17.739 MST, 15.7 s later. The last is 14:46:14.529, and the results commit is 14:49:28. All 6,400 IDs are unique and none falls outside that window. Repeats run in order, about 65 s each (repeat 0 from 14:35:17 to 14:36:22 … repeat 9 from 14:45:08 to 14:46:14). Framings are interleaved, as the pre-registration states. The analysis output `p2-1-framing.json` has mtime 14:46:59, 45 s after the last call, so it was analysed once. **Hole (5):** the pre-registration text says "Written and frozen 2026-11-04 14:45 … before any call", and D0 and D1 are dated 14:45. A file committed at 14:35:02 cannot have been written at 14:45. Read literally, 14:45 falls during repeat 8, after about 5,100 calls. Git and the server timestamps agree that the commit came first, so I read the stamp as a mis-stated time, not a late freeze. Git author dates are set by the client, and with no remote I cannot confirm the commit time from an independent source. Whether `entangled-mind/results/gm3b-calls.json` was opened before the commit: *cannot check*. Its atime (05:02:07) is not updated under macOS relatime semantics.

**A2. Rule, statistic, split, seed and budget match word for word.** *Holds.* The pre-registration §4–§5 rule (Q ≥ 0.90 **and** |shift| < 3 on point estimates; "pass, imprecise" if Q's lower CI < 0.80; untestable if ρ < 0.5 or > 5% missing) is implemented exactly in `verdict()` at `p2_1_framing.py:103–112`. The seeds are 2101 (Q) and 2102 (shift), via `SEED + 1`. The bootstrap uses 2,000 resamples of the 40 questions. There is no split. The cap is $0.40. `git diff 8fb40f3 5931024 -- experiments DEVIATIONS.md` is empty, so the code that ran is the frozen code. The map's event at a20824d is the same (Q ≥ 0.90 and |shift| < 3, P = 0.60). D1 resolves the map's unstated details before data.

**A3. Bar not lowered.** *Holds.* No deviation row was added in the range.

**A4. Primary is the pre-registered primary.** *Holds.* Q(a,b) and the shift lead, and the secondaries are labelled.

**B5. Ties and floating point.** *Holds.* The primary is Pearson-based and no ranks or tie-breaks enter it. Ratings are coarse (37 distinct values; 97, 3, 85, 90 and 15 dominate). A rank-based variant gives ρ_s(a,b) = 0.896, ρ_s² = 0.80, also below 0.90.

**B6. Pooling.** *Holds.* Unpooled by claim slot within question (40 claims each), Q(a,b) is 0.70, 0.82, 0.82 and 0.73, and the retest is 0.89 to 1.01. With between-question variance removed (question-centred), Q(a,b) is 0.753 against a retest of 0.966. By level, Q is 0.507 on mid-range claims (15 < m_a < 85, n = 52) and 0.813 on extreme ones. The gap is not a between-question or ceiling artefact, and it is larger away from the floor and ceiling.

**B7. Few items driving it.** *Hole (2), interpretive, not verdict-changing.* Leave-one-claim-out gives 0.769 to 0.800 and leave-one-question-out 0.763 to 0.802, as reported. Greedy removal of **7 of 160 claims** (|m_b − m_a| = 80, 73, 64, 66, 61, 55, 48; from 5 questions; the same 7 as the largest |diff|) brings Q to 0.900, and the 6 largest give 0.890. Dropping the 8 largest |diff| gives 0.909, and the 10 largest gives 0.925. Counts of |m_b − m_a| > 20, > 30 and > 50 are 28, 18 and 6. In the same-wording retest they are 6, 3 and 1. The flips are real (far above retest), but they are concentrated. The results file reports only the cluster-level LOO and says "No single question carries the result". That is true, but it hides that about 5% of claims carry the gap. For comparison, the other pairs need 10 (c–d), 17 (b–d) and 22 (a–c, a–d) removals, so "four related questions" holds more strongly for them than for a–b.

**B8. Circular estimators.** *Holds* for the primary, since nothing is fit. The exploratory 28-claim "self-referential" split was chosen after seeing the flips and is labelled exploratory. See hole 6.

**B9. Baselines.** *Holds.* Two references are reported or recomputable. The cross-session same-wording retest gives Q 0.955. A within-session label-swap null, which randomly swaps the a and b labels per claim × repeat (2,000 swaps), gives mean 0.987 and 95% range [0.955, 1.015], and no swap reaches ≤ 0.772. A dumber method, raw r, gives the same verdict (r 0.864, against the r ≈ 0.933 needed for Q = 0.90).

**B10. Uncertainty.** *Holds.* The bootstrap is at question level, the right cluster. The claim sits fairly near its edge: the upper end is 0.880 against the 0.90 bar, 0.55% of resamples are ≥ 0.90, and the 99% upper end is 0.903. The verdict rule uses point estimates, so this does not affect the label. The Q estimator is unbounded (the retest CI reaches 1.006, and 5.9% of retest resamples exceed 1). That is a known property of disattenuation and is harmless here. Reliability robustness: across all 126 distinct 5/5 repeat splits, ρ_a ranges 0.982–0.997 and ρ_b 0.970–0.990. Q(a,b) ranges 0.757–0.785, and the variance-components (ICC) reliability gives 0.768.

**B11. Multiple comparisons.** *Hole (4).* There is one primary, uncorrected and correctly declared. But the plain English presents a secondary as a finding: "another AI assistant … rates about 4 points higher than every other framing, with CIs excluding 0". Those are three of 12 uncorrected secondary intervals. Bonferroni-corrected over the 12 (99.58%), a–c is [−1.9, +10.4], b–c [−0.8, +9.3] and c–d [−7.5, −0.1]. Two of the three include 0.

**B12. Leakage.** *Holds.* Nothing is fit.

**C13. Scope drift.** *Holds.* The headline says "on Haiku", and Limits names one model and one item set. "The four framings act like four related questions" is scoped to "this model".

**C14. Rank drift.** *Hole (4)*, as B11: the uncorrected secondary is in the plain English without its rank. The exploratory items are labelled.

**C15. Mechanism drift.** *Hole (3).* "Here, the wording that names the self changes which statements get high numbers." Framing (b) changes the verb (likely → confident) and the subject (impersonal → you) together, so the design cannot attribute the change to naming the self. Framings (c) and (d) keep "confident" and do not name the self, yet they differ from (a) even more (Q 0.56 and 0.66). Pre-registration §6 itself says the design "cannot say *why* the framings agree or differ".

**C16. Plain English matches the table.** *Hole (1).* "'Sam' is not further from 'you' than 'how likely' is: all the cross-framing Qs lie between 0.56 and 0.77." On the point estimates Sam is further from "you" (Q(b,d) 0.667) than "how likely" is (Q(a,b) 0.772). The difference is +0.105 [−0.029, +0.244] (my bootstrap, 4,000 question resamples). The data support only "not detectably further". "Reorders the statements" is hole 2 (see B7). Every other plain-English number matches the table and my recomputation.

**C17. Citations.** *Holds.* The results file cites no literature. "Program 1's format result (F4)" exists as stated in `entangled-mind/README.md:46` ("formats need separate credences"). Calling this result the same thing is an analogy, which I flag but do not cut.

**C18. Negative result stated plainly.** *Holds.* "The engine expected a pass (60). This was a miss."

**D19. Budget.** *Holds.* `om_common.Caller` checks `spent() >= cap` under a lock before every call. Overshoot is at most the 8 in-flight workers, about $0.0003. Actual spend is $0.2650 against an estimate of $0.26 and a cap of $0.40. Whether the per-call `cost` matches billing: *cannot check*. Token counts are not archived, only the computed cost.

**D20. Stop-on-refusal.** *Holds.* `llm._check_stop` raises on `stop_reason == "refusal"`, and the Caller stops without rewording. There is no refusal file, and 6,400 of 6,400 calls have integer values. Note: the client is built with `anthropic.Anthropic(max_retries=4)`, so the SDK retries transient HTTP errors silently. That is not a refused call and not a violation, but the record cannot show whether any retry happened.

**D21. One scale direction.** *Holds.* All four prompts end with the same `TAIL` ("0 = certainly false and 100 = certainly true"), and the archived gm3b F1 has the same tail.

**D22. Hit not called a hit until replicated.** *Holds / not applicable.* This is a fail. The negative is correctly scoped to one model and one item set.

**E23. Seed.** *Not applicable to a beacon.* The pre-registration names fixed seeds 2101 and 2102, and the code uses them. My re-run at seed 777 gives the same interval to ±0.006.

**E24. Tiebreak.** *Not applicable.*

**Additional hole (6), reproducibility of exploratory claims.** The "28 claims that mention the writer, memory, confirmation or uncertainty" split and the flip table are not generated by any committed code. The results file's "Regenerate with … --analyse" covers only the pre-registered JSON. I could reproduce the split only by guessing the keyword list (`writer|memory|confirm|uncertain` gives n = 28, r 0.708 against 0.881). The rule that defined the 28 must be committed.

**Additional hole (7), pre-mortem form.** `operators/premortem.md` requires the sentence to begin exactly "If this fails, the most likely reason is" and to carry a kind tag. The committed sentence begins "If this fails, the likeliest reason is" and has no kind tag. I score it with the kind inferred.

### Reproduction

- The authors' analysis was run offline on a copy of the scratch repo, with sockets' `connect` and `om_common.llm.client` patched to raise. `analyse()` makes no calls: it reads `results/p2-1-calls.json`, program 1's `split-exp5.json` and `results/gm3b-calls.json`. Its `results/p2-1-framing.json` is **byte-identical** to the committed one.
- Independent code (auditor's own, separate from `om_common`) reproduces every pre-registered number in both tables to the printed precision.
- Scripts are in `/private/tmp/claude-501/-Users-seanpharris-entangled-mind-audit2/bb46787f-112b-4a3c-a1e9-dd87d67b2c75/scratchpad/om-p2-1/work/`: `run_authors.py`, `indep.py`, `indep2.py`, `indep3.py` and `timeline.py`.

## The pre-mortem, scored

My failure reason, written first: Haiku rates a minority of claims very differently under "how confident are you" (about 18 of 160 move by more than 30 points; 7 removals restore Q ≥ 0.90), while the mean is unchanged. The framings are not interchangeable item by item, and the design was able to see it. Kind: **world**.

The pre-mortem (8fb40f3, line 17): "If this fails, the likeliest reason is that 'how confident are you' makes Haiku hedge toward 50 by a few points across the board, so the item ordering survives (Q high) while the mean shift breaks the 3-point bar."

Score: **kind_only**. It predicted a real framing effect, so its kind, which is untagged, is inferred as world. That is the same kind as the actual failure, but by the opposite mechanism. It expected Q to survive and the shift to fail. Instead Q failed and the shift passed (+0.12). The hedging it named did happen: (b) is 3.1 [1.6, 4.7] points closer to 50. But the hedging was symmetric, so it never moved the mean. If the missing kind tag is read as a missing pre-mortem kind, `other` is the defensible alternative.

## Required cuts

1. Replace "'Sam' is not further from 'you' than 'how likely' is: all the cross-framing Qs lie between 0.56 and 0.77." with: "'Sam' is not detectably further from 'you' than 'how likely' is (Q 0.67 against 0.77; difference +0.10 [−0.03, +0.24]). All the cross-framing Qs lie between 0.56 and 0.77."
2. Replace "So the same wording reproduces almost perfectly, while changing 'how likely is it' to 'how confident are you' reorders the statements." with: "So the same wording reproduces almost perfectly, while changing 'how likely is it' to 'how confident are you' moves a minority of statements a long way: 18 of 160 by more than 30 points, against 3 in the retest. Removing the 7 largest movers would bring Q to 0.90."
3. Replace "Here, the wording that names the self changes which statements get high numbers." with: "Here, changing the wording, both the verb ('likely' to 'confident') and the subject ('it' to 'you'), changes which statements get high numbers. The design cannot say which of the two does it, and the third-person framings, which do not name the self, differ from (a) as much or more."
4. Replace "It rates about 4 points higher than every other framing, with CIs excluding 0 against 'how likely', 'you' and 'Sam'." with: "It rates about 4 points higher than every other framing (secondary, uncorrected; the uncorrected CIs exclude 0, but after correction for the 12 secondary intervals only the Sam comparison does, barely)."

Also required, not counted as cuts:
- Under the leave-one-question-out line in Tables, add: "Leave-one-claim-out 0.769–0.800; removing 7 claims (largest |a−b| differences, 5 questions) gives Q 0.90." (hole 2)
- Commit the keyword rule for the exploratory 28-claim split. (hole 6)
- Add a new DEVIATIONS row correcting the "14:45" freeze stamp in the pre-registration and in D0 and D1 to the commit time 14:35:02. Rows are never edited. (hole 5)

## What would break it next

The verdict itself is hard to break on this archive. Its interpretation is not. Cheapest test, as a new bet: a 2 × 2 crossing of verb (likely/confident) × subject (impersonal/you), on a second item set with no claims about an answer, the writer or memory (for example 160 SimpleQA-style factual claims), plus the 7 flipped claims at 30 repeats to confirm the flips are stable. That is 160 × 4 × 10 + 7 × 2 × 30 = 6,820 Haiku calls, about $0.28 at the observed $4.1e-5 per call. Running the same crossing on Sonnet is about 4× the price, roughly $1.10. If Q(a, b) ≥ 0.90 on the non-self-referential set, the fail is a property of self-referential items, not of "how likely" against "how confident".
