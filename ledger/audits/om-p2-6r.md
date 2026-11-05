---
bet: om-p2-6r
program: other-minds
prereg_commit: ddb6c92
results_commit: 9bdbf08          # the clone's head: its re-commit of the results commit (author time 2026-11-05 05:09:41)
auditor_session: fresh auditor subagent launched by the om-p2-6r author session, working only in /Users/seanpharris/oversight-testbed-audit-om-p2-6r
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true          # and the auditor was launched by the author's own session (weaker independence than an engine-launched audit)
date: 2026-11-05 05:16 America/Denver
claims_checked: 20
holes_found: 2
overclaims_cut: 3
reproduced: true
verdict_claimed: null            # the pre-registered label is "fail" (§5.4); the template has no "fail", so it is entered as null = predicted event absent (convention of om-p2-1, om-p2-2, om-p2-3b, om-p2-6)
verdict_after_audit: null        # "fail" stands on every re-analysis; P's upper CI end is +0.09 (Sonnet) and +0.03 (Opus), far below the 0.15 bar
verdict_stands: true
canary: unknown
false_alarms: 0
design_review_missed: ["D1: the review checked EPS handling in model_reading() but not the |D| >= 0.05 pair filter in item_uptakes(). That filter is a plain float comparison, and §4 ('a pair with |D| < 0.05 is dropped') keeps |D| = 0.05. One Opus pair sits exactly at the boundary (co-lin10, statement X, -30 display: shown 55, baseline mean 60; 0.55 - 0.60 = -0.04999999999999993). The comparison drops it, and that alone switches on the frozen Opus no-own-pull sentence. The same artefact class was caught as F6 in the ng-p3-16 review the same morning."]
failed: true
failure_reason: "Both models took up the shown number far less than Haiku in every cell (Sonnet +0.10 to +0.23, Opus +0.02 to +0.07, against Haiku +0.14 to +0.45), so P stayed at +0.05 and +0.02, far below the 0.15 bar; on Sonnet the pooled label effect also exceeded position. Kind world."
failure_kind: world
premortem_score: named
risk_seen: null
---

# Audit of om-p2-6r: does "position over label" hold on Sonnet 5.5 and Opus 5.5?

## In plain English

The verdict stands: by the pre-registered rule this replication **failed** on both models, and nothing I tried comes close to changing that. The tables regenerate exactly from the archived calls. My own independent re-implementation gives the same numbers. Position stays far below the 0.15 bar under other bootstrap seeds, single repeats, statement and direction splits, and leave-one- and leave-two-items-out (best case +0.06 on Sonnet, +0.03 on Opus).

Three sentences in the write-up have to change, and none of them touches the verdict:
- **Opus "no own pull".** The frozen sentence was printed only because a floating-point comparison dropped one pair that §4's rule keeps. Kept, Opus's own-turn, own-label uptake is +0.08 [+0.01, +0.14], so that sentence does not apply.
- **Opus item count.** For the same reason, Opus has 14 items kept in both directions, not 13.
- **Sonnet "order flipped".** Sonnet's label-over-position ordering comes entirely from the −30 displays. On the +30 displays alone, position was the larger, though the data cannot tell the two apart there.

What could still overturn the reading behind the verdict (though not the scored fail) is a test of the ordering alone, without an absolute bar, at more repeats.

## The case that this result is false

The headline is a fail, so the case against it is that the replication holds and the design could not see it. The 0.15 bar is an absolute share of the displacement, sized on Haiku, who took up 0.45 of an own-turn value. The pre-registration's own dry run says the bet cannot pass once uptake falls to half of Haiku's. So the fail may only say that Sonnet and Opus take up less, which DM4 already said, not that the turn stops mattering more than the label.

The cross-model comparison is also confounded (P8):
- Sonnet ran with `between_tools` thinking, Opus with thinking on at low effort, Haiku with thinking off.
- On Opus, the planted assistant turn has no thinking block.
- The displays are Haiku's anchors ±30, not each model's own. Opus's baseline is up to 52 points from Haiku's anchor on some statements.
- Baselines are means of 2 or 3 calls against Haiku's 20, so the frozen measure's b is noisy.

Under all this, the two strong plain-English claims are the weakest part of the record. One is "the order of the two effects flipped" on Sonnet. The other is "Opus did not detectably take up" its own answer. Either could come from baseline noise, pooling, or a boundary in the filter rather than from the models. And "position over label is a Haiku result" could be overstated if the ordering still holds at a smaller size.

The checklist below finds that the fail itself is robust. P's whole interval sits far under the bar on both models, and even the relative ordering is absent on the pooled pre-registered measure (Opus P − L −0.01 [−0.02, +0.01]; Sonnet −0.03 [−0.06, −0.02]). But two of the secondary claims do rest on what the case above suspects: one on a boundary artefact, one on pooling across the ±30 directions.

## Claims checked

| # | claim (quoted or paraphrased) | check run | outcome |
|---|---|---|---|
| 1 | Pre-registered verdict: fail | `--analyse` re-run; independent re-implementation (`reanalyse.py`) | holds |
| 2 | Sonnet fail-small: P +0.05 [+0.01, +0.09], P_s +0.07 [+0.01, +0.14], L +0.08 [+0.04, +0.13] | independent recompute (+0.045 [+0.007, +0.094]; +0.067 [+0.009, +0.139]; +0.080 [+0.039, +0.134]) | holds |
| 3 | Opus fail-small: P +0.02 [+0.01, +0.03], P_s +0.02 [−0.01, +0.04], L +0.02 [+0.01, +0.04] | independent recompute | holds as computed; under §4's boundary as written, P +0.017 [+0.003, +0.031], L +0.023 [+0.006, +0.040]; reading unchanged |
| 4 | Sonnet P − L −0.03 [−0.06, −0.02], "smaller than the label effect" | recompute; seeds 1–3; ties excluded (−0.043 [−0.069, −0.020]) | holds pooled |
| 5 | Opus no-own-pull: AY +0.07 [−0.01, +0.13], "not detectably taken up" | exact-boundary recompute | **hole**: with the |D| = 0.05 pair kept as §4 says, AY +0.075 [+0.008, +0.136]; CI lower end > 0 at all 200 bootstrap seeds tried |
| 6 | Opus P − L −0.01 [−0.02, +0.01], "could not be told apart" | recompute, both boundary treatments | holds |
| 7 | "On Sonnet the shown number was taken up about half as much as on Haiku" | mean of four cell uptakes: Sonnet 0.16, Haiku 0.32 | holds |
| 8 | "the order of the two effects flipped" (Sonnet) | split by display direction | **hole** (pooling): at −30, P +0.006 vs L +0.138; at +30, P +0.068 vs L +0.048 (P − L +0.020 [−0.027, +0.083]) |
| 9 | Opus cell uptakes +0.02 to +0.07; Haiku +0.14 to +0.45 | table; om-p2-6 JSON | holds |
| 10 | Haiku reference column (P +0.23 [+0.13, +0.34], L +0.08, P_s +0.26, L_s +0.10, cells) | read `results/p2-6-position-or-label.json` | holds; om-p2-6's archive has no boundary mismatch (checked, 0 of 64 pairs) |
| 11 | "So 'position over label' is a Haiku result on this design" | scope rules §6 | holds (one design, three models named) |
| 12 | 1,440 calls (864 + 576), every repeat complete | cache keys, `complete_repeats` | holds |
| 13 | $2.1656 (Sonnet $0.7451, Opus $1.4205), no refusal | sum of per-entry cost; refused flags; results dir | holds |
| 14 | All 16 items usable; Sonnet 15 and Opus 13 with both directions | recompute | Sonnet holds; Opus **13 by the code, 14 under §4** (same artefact as #5) |
| 15 | Pairs kept/dropped 56/8 (Sonnet), 54/10 (Opus) | recompute | holds as computed (Opus 55/9 under §4) |
| 16 | LOO changes no reading; P range +0.029–+0.053 and +0.015–+0.022 | recompute; leave-two-out max P 0.059 and 0.025 | holds |
| 17 | Label-swap null share 0.0000 on both | recompute with seed32_boot + 1 | holds |
| 18 | Design review fix-first (cb9987d), D14a–e, confirmed 6b72777 before the first call | git log author times; run log | holds |
| 19 | Run 05:05:22–05:09:02 | `results/p2-6r-run.log` | holds on the log's word (cache entries carry no timestamps) |
| 20 | Pre-mortem "That happened" (Opus far less in every cell, P < 0.15) | Opus cells vs Haiku | holds |

## Checklist

**A. Pre-registration**
1. *Timing: holds.* Author times, in order:
   - pre-registration `ddb6c92`, 04:45:09;
   - seed `6ec5a8d`, 04:46:31 (pulse 04:46:00);
   - design review `cb9987d`, 04:58:05;
   - fixes `af4905b` (05:01:29) and `791657e` (05:04:25);
   - confirmation `6b72777`, 05:04:59;
   - run start (log), 05:05:22;
   - data commit `3ba5289`, 05:09:21.

   The calls file has no per-entry timestamps, so the start time rests on the run log. The clone's file mtimes are the clone's (05:10).
2. *Rule, statistic, seed, budget match: holds.* `git diff ddb6c92 HEAD` on `p2_6r_replication.py` touches only sentences, the run order (`run_all`), the refusal file and `write_md`. `model_reading`, `overall`, `item_uptakes`, `summarise`, MIN_D, MARGIN, B, CAP and REPEATS are unchanged. Every change has a D14a–D14e row dated before the first call.
3. *Bar not lowered: holds.* MARGIN 0.15 and the conjunction are as frozen.
4. *Primary reported as primary: holds.* P, P_s and L carry the event role. The secondary sentences are labelled secondary.

**B. Is the number real?**

5. *Ties and floating point: **hole**.*
   - **The filter.** `item_uptakes` keeps a pair if `abs(D) >= MIN_D` in floating point. §4 drops only "|D| < 0.05", so |D| = 0.05 is kept.
   - **The pair.** One pair is exactly on the boundary: Opus co-lin10, statement X, −30 display (A = 55, baseline [60, 60], D = −0.04999999999999993 in float). The code drops it. The other boundary pair, Sonnet co-lin06 Y −30, evaluates to exactly −0.05 and is kept, so the two are treated inconsistently.
   - **With it kept, Opus moves:**
     - AY +0.069 [−0.007, +0.135] → +0.075 [+0.008, +0.136]. The CI lower end is above 0 at all of seeds 0–199 and at the beacon seed.
     - Items with both directions: 13 → 14.
     - P +0.017 [+0.003, +0.031], L +0.023 [+0.006, +0.040], P_s +0.015 [−0.016, +0.040], P − L −0.006 [−0.017, +0.006].
   - **Effect.** The frozen no-own-pull sentence (fires when AY's CI lower end ≤ 0) would not be printed. Reading, verdict and secondary-sentence choice are unchanged.
   - **Other tie checks.** On Sonnet, P − L excluding the three exactly-tied items is −0.043 [−0.069, −0.020]: no tie artefact. Scripts: `boundary.py`, `reanalyse_exact.py`, `ay_seeds.py`.

6. *Pooling: **hole** on a secondary claim.*
   - **Sonnet by display direction:**

     | display | P | L | P − L |
     |---|---|---|---|
     | +30 | +0.068 [+0.022, +0.125] | +0.048 [−0.006, +0.113] | +0.020 [−0.027, +0.083] |
     | −30 | +0.006 [−0.027, +0.044] | +0.138 [+0.045, +0.249] | −0.132 [−0.229, −0.057] |

   - **Sonnet by statement:** X gives P +0.048, L +0.108; Y gives P +0.031, L +0.026.
   - **What follows.** Sonnet's "label larger than position" is carried by the −30 displays. The plain-English "the order of the two effects flipped" states it without that qualification.
   - **The primary.** It pools ±30 by the pre-registered design (P2-6's frozen measure), and the fail holds in every split (P ≤ +0.07 everywhere). Models were not pooled.

7. *Few items: holds for the verdict.*
   - **Leave-one-item-out:** max P is 0.053 on Sonnet and 0.022 on Opus.
   - **Leave-two-out:** max P is 0.059 and 0.025.
   - **Sonnet's P − L without its most negative item (co01):** −0.027 [−0.043, −0.011]; without its two most negative, −0.022 [−0.037, −0.007].
   - **Opus's P − L without co07:** −0.002.
   - **One item stands out:** Opus co-lin10 has uptake −0.31 to −0.37 in every cell. Opus's baseline (60) is 25 points under Haiku's anchor (85), and shown 98 it answers 35. That is a real, odd response, not a computing error.

8. *Circular estimators: holds.* No fitting. The baseline b both filters pairs and enters the numerator, by design. The shift-invariant measure, which does not use b, gives the same fail.

9. *Baselines and controls: holds.* The label-swap null is reproduced (share 0.0000 on both). The dumb responders in the dry run each fail. For a fail verdict, no dumb method can "tie" a pass.

10. *Uncertainty: holds.* The bootstrap is over items (16), seeded with `seed32_boot`, and my implementation with the same seed reproduces every CI. Per-repeat P values are below 0.06 (Sonnet) and 0.03 (Opus) on every single repeat, so call noise is not what is driving the result.

11. *Multiple comparisons: holds.* One conjunctive primary. The secondaries are stated as uncorrected, and the plain-English P − L says "(secondary, uncorrected)".

12. *Leakage: holds.* Nothing is fitted. The anchors come from Haiku's exp4 run 3, fixed before this bet.

**C. Write-up**

13. *Scope drift: holds.* "Three Claude models, 16 everyday probability vignettes, ±30 points, one wording". No "all", "LLMs" or "language models".

14. *Rank drift: minor.* The Sonnet ordering (secondary) is promoted into the plain-English summary as "the order of the two effects flipped" without its direction dependence (B6). Covered by cut 3.

15. *Mechanism drift: holds.* No size, capability, belief or memory language. The settings bundle is stated in Scope. The plain-English model-to-Haiku comparisons ("about half as much as on Haiku") are numerical, and the bundle caveat sits in the same file.

16. *Plain English against the table:* three sentences are not supported as written (cuts 1–3). Every other number in the plain-English section matches the generated table, and the results file's tables are byte-identical to `results/p2-6r-tables.md` (one blank line apart).

17. *Citations: holds.* The only quantitative source cited in the results is om-p2-6's archive, checked against `results/p2-6-position-or-label.json`. DM4 is cited in the pre-registration only.

18. *Negative stated plainly: holds.* "Pre-registered verdict: fail" is the first line of the plain English.

**D. Process**

19. *Budget: holds.* CAP $4.00 is checked under a lock before every call. Spend was $2.1656 (sum of per-entry costs).

20. *Stop-on-refusal: holds.* 0 refused entries, no `refusal-p2-6r.md`, and run_all ran Opus only after Sonnet completed (log: 864 complete, then onward to 1,440). One limit: per-call cost is the client's computation, not checked against billing (cannot check).

21. *One scale direction: holds.* `SCALE = ", where 0 = certainly false and 100 = certainly true"` in every builder, and all 1,440 values are in 0–100.

22. *Replication: not applicable* (fail). This bet is itself the replication test of om-p2-6, and it did not replicate.

**E. Engine records**

23. *Seed: holds, except the beacon fetch.*
   - **Recomputed with the clone's `ledger/seed.py`:** seed 17652080689546741571; order seed32 3622963555; boot seed32 201936860. All match `data/p2-6r-seed.json`.
   - **Use in the code:** the boot seed is the one used, since my bootstrap with it reproduces every CI.
   - **Beacon:** per the seed file, the pulse (04:46:00) follows the commit (04:45:09), and the previous pulse (04:45:00) precedes it. *Cannot check* the pulse against the beacon itself: the CURBy client is not installed in the clone, and I made no network fetch. `certificate_verified: false` is recorded honestly.
   - **Order seed:** the cache records no run order, so its use cannot be checked. It does not affect the analysis.

24. *Tiebreak: not applicable.*

25. *Lesson: holds.*
   - `check_prereg.py` reports L1–L3 and R1–R2 ok.
   - The §0 row is in `ddb6c92`. `ls-om-p2-6r` in `lessons.jsonl` has the same sentence (committed `db719b4`, 04:47, before data).
   - The `read` block matches the ledger at `f9fc45a`: 42 bets, Brier 0.259 on 19, newest audit `ng-p3-5c.md` (00de34c, 23:12).
   - P12's do_this (P(pass) under named worlds) is in the dry run.
   - The odds change 0.40 → 0.25 is recorded before data.

26. *Design review: holds* as a process (fix-first, four fixes in D14a–e dated before the first call, confirmed at `6b72777` before the run start). Missed: the float boundary in the |D| filter (B5), under D1. See the header.

## The pre-mortem, scored

**My failure reason, written before scoring.** Both models took up the shown number far less than Haiku in every cell, so position stayed at +0.05 (Sonnet) and +0.02 (Opus) against a 0.15 bar. On Sonnet the pooled label effect was also larger than position. Kind: `world`.

(Disclosure: the pre-mortem sits in the pre-registration's §0 table, which the auditor must read first, so I saw it before the checklist. My failure reason comes from the table, not from it.)

**The pre-mortem:** "If this fails, the most likely reason is that Opus 5.5 takes up shown earlier answers far less than Haiku in every cell, so its position effect stays below 0.15." Kind `world`.

**Score: named.** This is the main mechanism. Opus's cells ran +0.02 to +0.07 against Haiku's +0.14 to +0.45, and its P was +0.02. Sonnet failed by the same mechanism, smaller uptake: its cells were half of Haiku's. The pre-mortem did not foresee Sonnet's label-over-position ordering, but that is secondary, and it depends on direction.

## Required cuts

All in `programs/other-minds/results/p2-6r-replication.md`. The generated `results/p2-6r-tables.md` is left as the code wrote it.

1. **Opus no-own-pull sentence (B5).** In the plain-English Opus bullet, replace

   > Added (D14b): "On Opus 5.5, the value labelled as the model's own and placed in its own turn was not detectably taken up (uptake +0.07 [-0.01, +0.13]): this design did not detect an own-answer pull in this wording on Opus 5.5. The position effect there has little to split."

   with

   > The code also printed the frozen no-own-pull sentence (uptake +0.07 [-0.01, +0.13]). That happened only because a floating-point comparison dropped one pair (co-lin10, statement X, −30 display: shown 55, baseline 60, |D| = 0.05 exactly), and §4 keeps that pair, since it drops only |D| < 0.05. With the pair kept as §4 says, Opus's own-turn, own-label uptake is +0.08 [+0.01, +0.14], so the no-own-pull sentence does not apply: on Opus 5.5 that value was taken up, weakly. The reading (fail-small) and the verdict do not change (audit om-p2-6r).

   In the Tables section, after the bullet that begins "On Opus 5.5, the value labelled as the model's own…", add: "(Withdrawn by audit om-p2-6r: a floating-point artefact; see the plain-English note.)"

2. **Opus item count (B5).** Replace "Sonnet had 15 items with a statement kept in both directions, Opus 13." with "Sonnet had 15 items with a statement kept in both directions, and Opus 13 as the code computed it (14 under §4's rule, because of the floating-point drop noted above)."

3. **Sonnet ordering (B6).** Replace

   > On Sonnet the shown number was taken up about half as much as on Haiku, and the order of the two effects flipped. The label ("your" against "Sam's") moved the rating slightly more than the position did: +0.08 against +0.05, a difference of −0.03 [−0.06, −0.02] (secondary, uncorrected).

   with

   > On Sonnet the shown number was taken up about half as much as on Haiku. On the pooled measure, the label ("your" against "Sam's") moved the rating slightly more than the position did: +0.08 against +0.05, a difference of −0.03 [−0.06, −0.02] (secondary, uncorrected). That ordering comes from the −30 displays (position +0.01, label +0.14). On the +30 displays alone, position was the larger, +0.07 against +0.05, a difference the data cannot tell from 0 (+0.02 [−0.03, +0.08]; audit re-analysis, exploratory).

Also recommended, not required: change `abs(D) >= MIN_D` to `abs(D) >= MIN_D - EPS` in `p2_6r_replication.py` (and P2-6's `item_uptakes`) for later bets, under a deviation row. om-p2-6's own archive has no pair on the boundary, so its result is unaffected.

## What would break it next

The scored fail cannot be overturned without new data. The P intervals end at +0.09 and +0.03, against a bar of 0.15.

What could overturn the reading "position over label is a Haiku result" is a bet that tests the **ordering alone**: P − L > 0 with a margin on each model, no absolute bar, the ±30 directions reported separately and pooled, and displays set ±30 from each model's own baseline rather than Haiku's anchors.
- **Sonnet:** 6 more repeats, 1,728 calls at about $0.00086, about $1.50.
- **Opus:** 4 more repeats, 1,152 calls at about $0.0025, about $2.85.
- **Free first step:** pre-register the margin from this archive's item spread.
