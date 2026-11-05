---
bet: exp5-verdict-reissue (D52)
program: entangled-mind
prereg_commit: 2c2ef6c (experiment 5, D22; §7.3 and §7.5 as frozen 2026-11-03 20:15)
results_commit: 077f42e (2026-11-04 13:18)
auditor_session: audit2 lead auditor (branch audit2)
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5 (commit trailers)
same_model_family: true
date: 2026-11-04 15:00 America/Denver
claims_checked: 11
holes_found: 3
overclaims_cut: 7
reproduced: true
verdict_claimed: classical
verdict_after_audit: mixed
verdict_stands: false
canary: unknown
false_alarms: 0
failed: true
failure_reason: the pre-registered design pools counterbalanced anchors, and the per-direction QQ departures (opposite signs) cannot separate a QQ violation from a direction-dependent response artefact, so the post-hoc label is not earned
failure_kind: design
premortem_score: null        # pre-registration predates operators/premortem.md (e287cb3, 14:41); it has no pre-mortem
risk_seen: null
---

# Audit of exp5-verdict-reissue (D52): experiment 5 re-labelled from TIE to CLASSICAL

## In plain English

The arithmetic holds. Recomputed with independent code, run 1's anchor-(a) mean q is −0.345 [−0.505, −0.166] on 32 large-order-effect pairs. Anchor (b) gives +0.241 [+0.111, +0.362], and the pooled value is +0.005 [−0.054, +0.068]. The anchor-(a) contradiction survives leave-one-item-out: no single dropped item brings the CI to 0. It also survives dropping the five most negative items (−0.235 [−0.388, −0.074]).

**The label does not hold.** The re-issue applies the §7.5 rule to a subset the pre-registration did not choose, and the pre-registration chose pooling on purpose:
- §7.3 binarises "after anchor recoding" over both directions.
- §8 item 4 names anchor reversal as the design's control for "scale and label artefacts".
- The two directions depart from q = 0 with opposite signs. That is the pattern counterbalancing exists to cancel, so it cannot by itself tell a QQ violation from a direction-dependent response artefact.
- The only pre-registered single-direction QQ data, run 2 (D33, 10 items, anchor a), do not meet the contradiction condition: q = −0.146 [−0.439, +0.137]. Its own pre-registered reading was "near-zero q survives: True".

So CLASSICAL is a post-hoc reading. The pre-registered verdict is TIE. The honest statement is the one this project's first audit recommended in `audits/SUMMARY.md` ("What the main session should cut first", item 5): tie on the pre-registered pooled analysis; the single-direction data contradict QQ in both directions with opposite signs; tie versus classical is unsettled. README, record and papers now state CLASSICAL as *the* verdict, re-issued "under its own §7.5 rule". That wording should go.

The first audit carries part of the blame. Its exp5-run-1 audit and SUMMARY line 198 called the pooled q an "artefact" and the single-direction label "classical, not tie". The pre-registration's own §8 item 4 cuts against that, and it was not quoted there.

## The case that this result is false

The re-issue's logic is that the pooled q ≈ 0 is "an artefact of mixing anchors (a) and (b)", so the honest q is the single-direction one. Turn that around. The pre-registration knew the two anchors might push ratings around, and that is why it counterbalanced them (§8 item 4: "Scale and label artefacts. These are handled by anchor reversal"). It analysed the binarised response after recoding, pooled. If anchor (a) yields q = −0.35 and anchor (b) yields q = +0.24, then the departure from QQ flips sign when only the labelling of the scale changes. A process that genuinely violated QQ would have no reason to violate it in opposite directions under a relabelling. A direction-dependent response bias in where ratings fall relative to the 50 cut would. That is exactly what counterbalancing averages out: run 1's baseline M ratings average 33.8 under "0 = false" against 71.3 under "0 = true" (`paper/gold-map.md:188`).

On that reading, the pooled q is the artefact-controlled estimate, and the single-direction q's are the artefacts. Picking anchor (a) after seeing both is a post-hoc choice of the subset that moves the label. The only single-direction QQ data collected under a pre-registration (run 2) return a CI that includes 0.

So the case that the re-issued verdict is false: the pre-registered verdict is TIE, nothing pre-registered contradicts QQ, and CLASSICAL rests on discarding half of a counterbalanced design after the data.

The case has limits. Both single directions contradict, so no choice of direction would give TIE; only pooling does. And run 2's 10-item non-contradiction is underpowered: run 1's anchor-(a) data restricted to the same 10 items also give a CI including 0 (−0.154 [−0.435, +0.135], 12 pairs). So the data do not favour TIE either. They leave the label undetermined between the two readings.

## Claims checked

| # | claim (results file or record) | check run | outcome |
|---|---|---|---|
| 1 | anchor (a) q −0.345 [−0.517, −0.181], 32 pairs (verdict basis) | independent code (`scratchpad/d52/qq.py`), own bootstrap | holds: −0.345 [−0.505, −0.166], 32 pairs on 26 items |
| 2 | frozen `qq_check`, anchor (a): −0.339 [−0.510, −0.168], 33 pairs | reproduce.py regenerates `exp5-verdict-reissue.md` | holds (regenerated byte-identical; see A/B below) |
| 3 | anchor (b) +0.241 [+0.118, +0.370], 47 pairs | independent code | holds: +0.241 [+0.111, +0.362], 47 pairs |
| 4 | pooled +0.005 [−0.058, +0.065], 60 pairs | independent code | holds: +0.005 [−0.054, +0.068], 60 pairs |
| 5 | "In one direction the statistic is clearly negative; in the other it is clearly positive" | rows 1, 3 | holds |
| 6 | "Run 2 had already called that average an artefact" | `results/exp5-run-2.md:50` | holds, as a reading in run 2's prose; run 2's own pre-registered reading was "near-zero q survives: True" (`:39`) |
| 7 | "The pre-registered rule calls that a contradicted signature" | `2c2ef6c` §7.3 | **hole**: the rule is pre-registered, but its input (anchor-a subset) is not; §7.3 pools "after anchor recoding" |
| 8 | verdict CLASSICAL under §7.5 | §7.5 table, `exp5_reissue.verdict` | follows from rows 1–2 *given* the subset; not the pre-registered verdict (hole 1) |
| 9 | "Using the single-direction subset is a choice made after the data" | — | holds; stated in the results file and D52, but dropped in README:161, record:89, v3:67/614, paper:19 |
| 10 | robustness of the anchor-(a) contradiction | leave-one-item-out over 26 items; drop k most-negative items | holds: every LOIO CI upper end in [−0.265, −0.156]; dropping 5 most negative items −0.235 [−0.388, −0.074] |
| 11 | "What changes is the label, not the conclusion: no quantum advantage and no quantum signature" | primary +67 [−34, +212]; Kvam not present | holds |

## Checklist

**A. Pre-registration**
1. *Prereg predates analysis.* Holds for the frozen rule (`2c2ef6c`, 2026-11-03 20:15). D52 itself is dated 13:18 on 11-04, after the data and after the first audit. It is a post-hoc re-analysis, and says so in the results file (line 13) and in D52 ("What is post hoc").
2. *Analysis matches prereg word for word.* **Hole.** §7.3: "For each pair, the binarised response is yes = rating ≥ 50 (after anchor recoding)." The pairs are over all conversations of both anchors (R = 40 per order, 20 per anchor direction; §5 QQ block). The re-issue restricts to anchor (a). The DEVIATIONS row (D52) was written after the data. By this audit standard (A2, A3), a changed analysis with a deviation row written after the data is a hole, whatever the reason.
3. *Bar not lowered.* Holds in the narrow sense: the bar (CI excludes 0) is unchanged and the change makes the label harsher on the quantum model, not kinder. But invariant 6's purpose is to stop post-hoc choices from moving labels, in either direction. A post-hoc subset moved this one.
4. *Primary is the pre-registered primary.* Holds: the primary (F5 − A5, TIE) is unchanged.

**B. Is the number real?**
5. *Ties.* q is computed from binarised ratings at a cut of 50; a rating of exactly 50 is "yes" under both anchors after recoding (raw 50 → 50). That is symmetric. The pre-registration's robustness cuts (30, 40, 60, 70) were not re-run per anchor: **cannot check from the results file**; the per-pair `q_by_cut` exists inside `qq_check` but is not reported for the re-issue.
6. *Pooling.* This is the whole question. Pooled vs unpooled flips the label. The pre-registration pooled by design (counterbalancing), so unpooling is the post-hoc step here, not the pooling (hole 1).
7. *Few items.* Holds for anchor (a): no single item, and not the five most negative items, carry the contradiction (claims row 10).
8. *Circularity.* Holds: no fitting.
9. *Baselines.* Not applicable to a parameter-free check.
10. *Uncertainty.* Item bootstrap, as pre-registered. Holds.
11. *Multiple comparisons.* Three q's are now reported (pooled, a, b), and the verdict was re-issued on one chosen after seeing all three. The results file does not say the label depends on that choice. **Hole (minor)**, folded into hole 1.
12. *Leakage.* Not applicable.

**C. Write-up**
13. *Scope drift.* Holds within the results file. README:161 and record:89 drop "post hoc".
14. *Rank drift.* **Hole.** A post-hoc re-analysis is presented as *the* verdict in README:161, record:89, paper:19 and v3:67/614. The pre-registered verdict is called "superseded".
15. *Mechanism drift.* The results file says the pooled q "sat near zero" because it averaged opposite signs. That is arithmetic and holds. README:161 says run 2 "showed [it] to be an artefact". Run 2 showed the single-direction q differs from the pooled one; it did not show which is the artefact. The pre-registration's §8 item 4 says the opposite (that per-direction effects are the artefacts that pooling controls).
16. *Plain English vs table.* "the statistic is −0.345 … The pre-registered rule calls that a contradicted signature": the rule is pre-registered, its application to this subset is not (cut 1).
17. *Citations.* No external citations.
18. *Negatives stated plainly.* Holds: "no quantum advantage and no quantum signature, in either reading".

**D. Process**
19. *Budget.* $0; no calls. Holds.
20. *Refusals.* Not applicable.
21. *One scale direction.* Experiment 5 run 1 used two by design (pre-dates the project's one-direction rule, which came from run 2). The re-issue imposes the later rule on the earlier design retroactively.
22. *Replication.* The one pre-registered single-direction QQ run (run 2) does not replicate the contradiction (−0.146 [−0.439, +0.137]). It is underpowered (10 items, 12 pairs), so it does not refute it either.

**Holes.**
1. **CLASSICAL is a post-hoc label replacing a pre-registered one.** The pre-registered pooled analysis gives TIE. The pre-registration's own design treats per-direction effects as the artefact. The only pre-registered single-direction test does not meet the contradiction condition.
2. **The verdict basis is a hard-coded constant.** `exp5_reissue.py:20` sets `AUDIT_Q = {... "mean_q": -0.345, "mean_q_ci95": [-0.517, -0.181]}` and the verdict is computed from it (`audit_contra`). reproduce.py therefore "regenerates" the verdict from a number typed into the script, not from the archive. The frozen-code check in the same file is computed and agrees (−0.339 [−0.510, −0.168], contradicted), so the outcome is unaffected. But the computed value, not an auditor's quoted one, should be the verdict basis.
3. **Opposite-signed departures are not discussed as a possible artefact.** Neither the results file nor D52 considers that q flipping sign under a relabelling of the scale is evidence about the binarisation, not about QQ.

## The pre-mortem, scored

The pre-registration has no pre-mortem: it was frozen before `operators/premortem.md` entered the standard (`e287cb3`, 14:41). So `premortem_score: null`. The auditor's own one-line failure account is in the front matter (`failure_reason`, `failure_kind`).

**E23–E24.** Not applicable: no beacon seed, and not a tiebreak bet.

## Required cuts

- `results/exp5-verdict-reissue.md:11`: "The pre-registered rule calls that a contradicted signature, and a contradicted signature with a primary that is not a pass makes the verdict **classical**." → "Applied to this subset, which the pre-registration did not choose (it pooled both directions after recoding, as its control for scale artefacts, §8 item 4), the pre-registered rule would call that a contradicted signature, and the verdict would be **classical**."
- `results/exp5-verdict-reissue.md:13`: add after the first sentence: "The two directions depart from q = 0 with opposite signs, which is also what a direction-dependent response artefact would produce. The only pre-registered single-direction QQ data (run 2, 10 items) do not meet the contradiction condition (−0.146 [−0.439, +0.137]). So the pre-registered verdict remains TIE, and CLASSICAL is a post-hoc reading; which is right is unsettled."
- `README.md:161`: "The verdict, re-issued under its own §7.5 rule (D52, …), is **classical**" → "The pre-registered verdict is a **tie**. A post-hoc re-analysis on one scale direction (D52, …) meets the contradiction condition, which would make it **classical**; because the design pooled the two directions on purpose and they depart in opposite directions, tie versus classical is unsettled."
- `README.md:161`: "It was first issued as a tie on a q pooled over two scale directions, which run 2 showed to be an artefact; that reading is superseded." → "The pooled q (+0.005) averages two opposite-signed directions (−0.345 and +0.241)."
- `paper/record.md:89`: "Experiment 5 is classical (re-issued, D52; first issued as a tie): … the near-zero pooled q came from pooling scale directions." → "Experiment 5: tie as pre-registered; classical on a post-hoc single-direction re-analysis (D52); unsettled between the two."
- `paper/the-entangled-mind-paper.md:19` and `paper/the-entangled-mind-v3.md:67`, `:614`: replace "the verdict … is re-issued as classical (D52)" / "The verdict is classical (re-issued, D52; first issued as a tie, now superseded)" / "Verdict (§7.5): classical, re-issued in D52" with "The pre-registered verdict is a tie; on a post-hoc single-direction re-analysis it would be classical (D52); the two directions depart in opposite directions, so which label is right is unsettled."
- `experiments/exp5_reissue.py:20` (code, not prose; for the owning session): base `verdict_reissued` on the computed `by_anchor["a"]`, and report `AUDIT_Q` as a cross-check only.

## What would break it next

A pre-registered single-direction QQ block on all 40 items, run on **both** anchor directions as separate pre-registered tests. Contradiction would have to hold in each separately with the label decided in advance. 2 anchors × 40 items × 2 pairs × 2 orders × R = 20 = 6,400 two-turn Haiku conversations (12,800 calls), the same size as run 1's QQ block, which the pre-registration's cost table puts at about **$0.52**. If q departs from 0 with opposite signs again, the departure is tied to the scale's labelling and the right label is TIE with a response artefact. If both directions depart with the same sign, CLASSICAL is earned.
