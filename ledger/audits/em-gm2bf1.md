---
bet: em-gm2bf1
program: entangled-mind
prereg_commit: e65b1d5
results_commit: 99a0476            # the audit clone's re-commit of the results commit (author time 2026-11-05T07:15:22-07:00)
auditor_session: fresh auditor subagent, audit clone /Users/seanpharris/oversight-testbed-audit-em-gm2bf1 (scratch copy and scripts under /private/tmp/claude-501/-Users-seanpharris-oversight-testbed/e93ce59f-1dc3-4451-8206-bee8c0537bfa/scratchpad/audit-gm2bf1/; nothing in the clone written)
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 07:26 America/Denver
claims_checked: 16
holes_found: 6
overclaims_cut: 5                  # Required cuts 1-5, all in the hand-written plain-English section
reproduced: true                   # the bet's script, re-run on a scratch copy of the archive with the beacon seed, gives a JSON identical to the committed one and an identical md below the hand-written section (program 1's full reproduce.py not run; its registration at 99a0476 runs exactly this script and seed)
verdict_claimed: pass              # reported "pass, unreplicated"
verdict_after_audit: pass-unreplicated
verdict_stands: true               # the operative rule (D71, dated and confirmed before the primary was computed) gives pass, and that pass survives bootstrap seeds 1-5, every single-item drop, and linear instead of squared covariates. But the pass is fragile: the guard as frozen at e65b1d5 fails on these data, and so do two-item drops, random tie order and dropping F3. The holes are that this is not disclosed, plus wording that overclaims
canary: unknown
false_alarms: 0
design_review_missed: [D3]         # the F1 fix replaced the frozen guard rather than adding to it, so it could not be guaranteed to tighten; on these data it loosened (frozen fails, D71 passes), against the direction of every world in the review's own dry run
failed: false
failure_reason: "None: em-gm2bf1 passed under its operative (D71) rule. Had it failed, my most likely reason: the order archive's rating noise W carries the whole link. Allowing for W alone, the partial is +0.076 [-0.094, +0.260], and the frozen guard (E and W) gives +0.085 [-0.089, +0.270]. Kind world."
failure_kind: null
premortem_score: not_failed
risk_seen: true                    # the named risk ("once extremity and rating noise are allowed for ... share nothing") is what the frozen guard shows: +0.085, interval through 0. Only the D71 guard, which adds the order archive's extremity, leaves a shared part
---

# Audit of em-gm2bf1: do claims that move with question order also move with answer format? (Haiku, archive)

## In plain English

The verdict stands as **pass, unreplicated**. The table regenerates exactly from the archive with the beacon seed. The rule that produced it (D71) was dated, reviewed and confirmed before the primary was computed. The primary correlation (+0.336) and the D71 guard (+0.246, lower bound +0.092) survive dropping any single item and changing the bootstrap seed.

The pass is much more fragile than the write-up says, though:
- The guard frozen in the pre-registration commit (partial given E and W) **fails** on these data: +0.085 [−0.089, +0.270]. The pass exists only because D71 replaced that guard. D71 described the replacement as a tightening, and in the dry run's worlds it was one. On these data it was looser.
- Allowing for rating noise alone removes the link.
- The link is absent in gm2's 10 items (ρ −0.09) and lives entirely in gm2b's 30.
- Dropping two items (h126, h158), randomising the order of tied format means, or dropping the bet format F3 each puts ρ below the 0.30 bar.

Five plain-English sentences have to be rewritten so that the result says this. The cheapest thing that could break it is a fresh order-chain run on all 40 items (about $0.45 on Haiku), with the frozen guard and the D71 guard both required.

## The case that this result is false

*(Written before the checklist, from the pre-registration and the results file only.)*

The headline is a correlation of 0.336 against a bar of 0.30, so a small change moves it below. Its interval reaches 0.16. The format spread G is an SD of percentile ranks over six formats, and three of the formats are binary with ten repeats. In F2 and F4, 90 of 160 claims sit on one tied all-yes block. So for more than half the claims, G partly measures where a continuous format puts the claim relative to a block midrank. That is a tie-handling choice, not movement. The order span S is a max-minus-min of four noisy means, so it grows with rating noise almost by construction.

The bet's own lesson says the boring driver is "mid-scale, noisy claims", and the guard was added to rule it out. The guard was rewritten after the design review (D71), by a reviewer who had computed S and G per claim, together with their covariates, from the archives. If the rewrite happened to be the version that passes, the pass is a specification choice. The pre-mortem's own story would then be true: once noise and extremity are allowed for in the way first frozen, nothing is left.

Finally, 160 claims from two order archives (gm2's 10 items, run one night, and gm2b's 30, run the next) are pooled. A correlation pooled over two batches can be carried by one batch.

## Claims checked

| # | claim (quoted or paraphrased from the results file) | check run | outcome |
|---|---|---|---|
| 1 | table: ρ +0.336 [+0.159, +0.487], partial +0.246 [+0.092, +0.368], pass | re-ran the script with seed 12485997366771242721 on a scratch copy of the archive | identical JSON and md table |
| 2 | "Spearman ρ = 0.34 [0.16, 0.49] (40 items carrying their claims...)" | JSON | holds |
| 3 | "The bar was 0.30 with the interval above 0." | §5 and D71 | holds; the interval also reaches 0.16, below the bar (see cut 2) |
| 4 | "The correlation survives the boring explanation ... as do noisy ones." | partial with W alone, E+W (frozen), and D71 covariates | **overclaim**: allowing for noise alone gives +0.076 [−0.094, +0.260]; the frozen guard gives +0.085 [−0.089, +0.270] (cut 1) |
| 5 | "Allowing for ... both archives, and ... order conversations, it is 0.25 [0.09, 0.37]." | JSON | holds |
| 6 | "Dropping any one item does not change the verdict." | leave-one-item-out, then greedy leave-two-out | holds for one item (lowest ρ 0.305 without h126); dropping h126 and h158 gives 0.272, fail (cut 2) |
| 7 | redacted secondary: "0.33, and 0.20 after the allowance" | JSON | holds (lower bound of the partial +0.026) |
| 8 | "ρ 0.77 with the within-order SD", "−0.79 with extremity in the order archive", "0.38 and −0.23" | JSON | holds |
| 9 | "The link between the two spreads is the part left over." | guard variants | holds only for the D71 covariate set; with W alone nothing is left (cut 1) |
| 10 | "partly go together, beyond how mid-scale or noisy a claim is" | as 4, plus format-call noise (F1 SD) as an extra covariate | **overclaim**: noise is allowed for only in the order conversations, and allowing for it alone removes the link (cut 4) |
| 11 | "worlds with no shared instability still pass this rule 6–10% of the time" | dry-run README and JSONs; my re-simulation of 5 dry-run worlds, 150 draws each | **inaccurate**: the no-shared worlds pass 0–10% (6% and 10% only in W0c and W0d). In all 750 simulated draws the D71 guard sits *below* the frozen guard (median −0.01 to −0.12); on the real data it sits +0.161 *above*. The real data are outside the dry run's family (cut 3) |
| 12 | "Two binary formats put 90 claims on one tied rank" | per-format tie blocks | holds (F2 and F4: 90 claims each at 1.0); its effect is not quantified (cut 5) |
| 13 | "One model (Haiku), these 160 claims." | scope | holds |
| 14 | verdict sentence (D71 wording, ρ filled in) | code SENTENCES and D71 | holds verbatim |
| 15 | secondaries line, medians, sha256 prefixes | JSON; sha256 of the clone's archives | holds |
| 16 | "pass, unreplicated" | invariant 7 | holds |

## Checklist

**A. Was it pre-registered as claimed?**

1. **holds.** Author times:
   - pre-registration `e65b1d5` 06:43:25;
   - seed `14d6c9e` 06:44:40;
   - ledger entry `f46a2f7` 06:49:24;
   - design review fix-first `1d52379` 07:10:23;
   - fixes `f09824e` 07:12:50;
   - confirmation `28cc32b` 07:14:54;
   - results `99a0476` 07:15:22.

   None of the archives (`gm2-conversations.json`, `gm2b-conversations.json`, `gm3b-calls.json`), `split-exp5.json`, `gm3b_format_invariance.py` or `gm3c_heldout_format.py` changed in `e65b1d5..99a0476` (`git log` on those paths is empty). The sha256 values recorded in the JSON match the clone's files. The results commit message says the run happened at 07:14:54, the second of the confirmation commit, so the run and a roughly 400-word hand-written paragraph fit into 28 seconds. That is tight, but my run took 12 s of CPU (33 s wall), so it is possible. The clone's file mtimes are the clone's, so nothing else can date the run (*cannot check* beyond the commit times).

2. **holds, with a note that becomes hole 1.** The statistic, bar, seed, cluster bootstrap, budget and leave-one-item-out rule match `e65b1d5`, except the guard. D71 changes the guard: it adds Eo, and each covariate enters as its centred rank plus its squared centred rank. D71 also adds the single-item rule and rewords the pass sentence. D71 is a dated DEVIATIONS row, it names the review, and its commit `f09824e` predates the results. So the difference is recorded as required.

3. **hole (1): the D71 replacement loosened the guard on these data, and the record says it tightened it.** D71 says: "The bar ... is unchanged and only the guard is tightened", and "the guard removes false passes, not true ones". design-review.md allows a fix that "may tighten the design but never lower the bar." The D71 guard is not nested in the frozen one: it replaces E+W (linear ranks) with E+Eo+W (ranks and squared ranks). Adding covariates to a partial correlation can raise it (suppression), so the replacement could not be guaranteed to tighten. A conjunction (the frozen guard AND the D71 guard) would have been. On the real data (`scripts/guards.py`, 4,000 resamples, same seed):

   | covariates | partial ρ [95%] | lower bound > 0 |
   |---|---|---|
   | E + W, linear (**frozen at e65b1d5**) | +0.085 [−0.089, +0.270] | **no** |
   | E + W, squared | +0.066 [−0.105, +0.247] | no |
   | W only | +0.076 [−0.094, +0.260] | no |
   | E + Eo + W, linear | +0.192 [+0.046, +0.330] | yes |
   | E + Eo + W, squared (**D71, operative**) | +0.246 [+0.096, +0.369] | yes |
   | E + Eo + W + F1-call SD, squared | +0.246 [+0.093, +0.363] | yes |
   | Eo only | +0.264 [+0.112, +0.402] | yes |

   Under the frozen rule the verdict is fail. Under the conjunction that a tightening requires, it is also fail. The pass comes from the D71 replacement alone.

   This is not an invariant-6 hole on timing. The row was written, reviewed and confirmed before the primary was computed, and I found no evidence that anyone computed ρ(S, G) or the partial before 07:14:54. So the verdict follows D71 and stands. The hole is that the record describes D71 as a tightening, and the results file never says that the pre-registered guard fails. The reader is owed that sentence (cut 1).

   Related record point (hole 5, below): before writing D71, the reviewer had computed S and G per claim (for quantiles and split-half reliabilities), and committed real G's inputs aligned with W and Eo. "Before data" therefore means before the S–G pairing, not before S and G were seen.

4. **holds.** The reported primary is the pre-registered Spearman ρ(S, G). The redacted condition is reported as a secondary and not promoted.

**B. Is the number real?**

5. **hole (4): ties decide whether ρ clears the bar.** G uses midranks (`scipy.stats.rankdata`, average ties), as frozen in the code at `e65b1d5`. That is the principled default. Tie blocks per format:
   - F2: 90 claims at 1.0;
   - F3: 66 at 0;
   - F4: 90 at 1.0;
   - F5: 23 at 0;
   - F6: largest block 25.

   With ties broken at random (1,000 draws), ρ has median 0.244 (95% of draws 0.167–0.316) and reaches 0.30 in only 4.8% of draws. The partial has median 0.195 (0.112–0.276 in 500 draws). Random tie-breaking adds noise to G, so some attenuation is expected. Still, the ρ ≥ 0.30 bar is met only under midranks.

   Format subsets (2,000 or 1,000 resamples), all under the D71 guard:

   | G built without | ρ | partial | verdict |
   |---|---|---|---|
   | F2 and F4 | 0.332 | 0.203 [+0.016, …] | pass |
   | all three binary formats | 0.232 | lower bound −0.026 | fail |
   | F3 | 0.290 | | fail on the bar |
   | any other single format | 0.302–0.360 | | pass |

   The write-up names the tie issue qualitatively but gives no number (cut 5).

6. **hole (3, with 7): the two order archives disagree.** The pre-registration pools gm2 (10 items, run 2026-11-04 night) and gm2b (30 items, same design per `experiments/gm2b-self-conditioning-40.md`).
   - gm2's 40 claims: ρ −0.088 [−0.436, +0.246], partial −0.034.
   - gm2b's 120 claims: ρ +0.423 [+0.248, +0.553], partial +0.250 [+0.078, +0.382].
   - The difference (gm2b − gm2) is +0.49, item-cluster 95% interval [+0.12, +0.88].
   - Random 10-item subsets of gm2b give ρ ≤ −0.088 in 0.03% of 4,000 draws.

   The median S, G and W are similar in the two batches. This is one of about 15 splits I ran, so it is not a finding, but the pooled sentence "On Haiku's 160 deliberation claims" hides it. Scale directions and formats are not pooled across directions: every format and both archives run 0 = false to 100 = true.

7. **hole (3, continued): two items take ρ below the bar.** Leave-one-item-out: no single item flips the verdict (lowest ρ 0.305 without h126; lowest partial 0.209 without h291), so "no single item carries it" holds. Greedy leave-two-out: dropping h126 and h158 gives ρ 0.272, and the verdict (bounds shifted as pre-registered) becomes fail. Leave-one-cluster-out is the gm2/gm2b split in item 6. The write-up reports neither (cut 2).

8. **holds, with a note.** Nothing is fitted to the outcome. The covariates share data with the measures:
   - E comes from F1, one of G's six formats;
   - W and Eo come from the same ratings as S.

   That is why S correlates 0.77 with W and −0.79 with Eo, and why the partial depends so heavily on the covariate set (item 3). It is not circular selection.

9. **hole (2): a dumber measure ties, and the dry run that sets the residual false-pass rate does not describe these data.**
   - The order archive's noise W alone correlates more with G (0.377) than S does (0.336), so a "no order effect, just noise" measure would clear the 0.30 bar. The guard exists for exactly this, and under its frozen form the guard says the noise explains the link (item 3).
   - The dry run's worlds give ρ(S, W) 0.37–0.58 against the real 0.77, and ρ(S, Eo) −0.38 to −0.65 against the real −0.79.
   - In all five worlds I re-ran (W0c, W0d, W1 κ 0.5, W1 κ 1.0, W1c; 150 draws each; `scripts/simcheck.py` on a scratch copy of `experiments/gm2bf1-dryrun/` pointed at the scratch code), the D71 guard's partial is below the frozen guard's (median difference −0.12 to −0.01). The difference reached +0.16 in no draw. On the real data it is +0.161.

   So the "6–10%" residual false-pass rate quoted in the plain English comes from worlds that do not behave like the data on the property that decides this verdict (cut 3). Item-block and within-item permutation controls are passed: the item-block permutation gives P(ρ ≥ obs) < 0.0005 and P(partial ≥ obs) 0.0005. The within-item shuffle gives P(ρ ≥ obs) 0.0035 and P(partial ≥ obs) 0.0175. Item-level ρ over the 40 item means is 0.40, and the within-item ρ of deviations from the item mean is 0.24.

10. **holds.** The intervals use a 40-item cluster bootstrap (claims within items). Bootstrap seeds 1–5 (4,000 resamples) all give pass, with ρ lower bound 0.148–0.161 and partial lower bound 0.085–0.093. The claim sits near the edge of the *point* bar (0.336 against 0.30), and the write-up does not say that the interval runs well below 0.30 (cut 2).

11. **holds.** There is one primary conjunction, and the secondaries are labelled "cannot change the verdict". Two guard specifications now exist on record (frozen and D71), and only the operative one is reported (item 3).

12. **hole (5): `experiments/gm2bf1-dryrun/marg.npz` is not "measured marginals only".** It holds, per claim and aligned by claim, the six real format means (from which real G follows exactly: `format_measures(fm)` equals the run's G, `np.allclose` True), real W, the real order-archive level (so real Eo; also checked equal) and E. The README says it "holds measured marginals only ... It never pairs the order span with the format spread". That is literally true, since S is not in it. But G's pairings with every guard covariate, which are this bet's secondaries (ρ(G, W) 0.377, ρ(G, E), ρ(G, Eo)), were computable from it before the guard was rewritten. The design review separately computed per-claim S from the archives for its quantiles and split-half reliability. The review states that it never paired S or G with each other or with E or W. I cannot check that (*cannot check* whether it was used). The record's description is inaccurate, and it should say what the file contains. No test-set label reaches a fitting step: nothing is fitted.

**C. Does the write-up say only what the data say?**

13. **holds.** The write-up says "On Haiku's 160 deliberation claims" and "One model (Haiku), these 160 claims"; no "models" or "all".
14. **holds.** The redacted condition is reported as a secondary, "about the same".
15. **holds.** "This design does not show one cause"; the ambiguity rival is named.
16. **hole (6): plain English against the table.** These sentences are not supported:
    - "The correlation survives the boring explanation, that claims rated near the middle wobble more in both, as do noisy ones." Allowing for noise alone removes it, and so does the frozen guard (item 3).
    - "Dropping any one item does not change the verdict." True, but without the two-item and gm2/gm2b numbers it implies robustness the data do not have (items 6–7).
    - "In the design review's dry run, built on measured numbers, worlds with no shared instability still pass this rule 6–10% of the time." The range is 0–10%, and the data lie outside those worlds (item 9).
    - "On these claims, being unstable under question order and being unstable under answer format partly go together, beyond how mid-scale or noisy a claim is." Noise is allowed for only in the order conversations, and only with Eo alongside.
    - "Two binary formats put 90 claims on one tied rank, so part of the format spread is tie position." True, but it needs its number (item 5).
17. **holds (n/a).** No external source is cited.
18. **hole (folded into 1).** The negative half of the record, that the pre-registered guard fails, is not stated at all. It has to be stated as plainly as the pass (cut 1).

**D. Process**

19. **holds.** Budget $0. The run path has no API call: `main()` never calls `gm3b_format_invariance.run()`. The cost is reported as $0.
20. **holds (n/a).** No calls were made.
21. **holds.** Every format and both archives use one scale direction (0 = certainly false, 100 = certainly true; F1 decoding checked: `102·expit(log((v+1)/(101−v))) − 1 = v`).
22. **holds.** The write-up says "pass, unreplicated" (one model, one claim set).

**E. Engine records**

23. **holds, except one part I cannot check.**
    - CURBY-Q was stalled (round 28297, 2025-08-22), so CURBy-RNG is right by the 24-hour rule.
    - Pulse 1592288 at 06:44:00 comes after the pre-registration commit at 06:43:25. The recorded previous pulse 1592287 at 06:43:00.220 predates it.
    - `python3 ledger/seed.py <randomness> em-gm2bf1 --purpose bootstrap` gives 12485997366771242721, as recorded.
    - The code uses that seed for the primary and seed + 1 for the redacted secondary, as §4 says.
    - The seed commit changes only the beacon line.
    - *Cannot check:* I did not fetch the pulses myself; that would need installing the npm client. The seed drives only the bootstrap, and seeds 1–5 give the same verdict (item 10).
24. **n/a.** This is not a tiebreak bet.
25. **holds.**
    - The §0 lesson row is in `e65b1d5`.
    - `ls-em-gm2bf1` in `ledger/lessons.jsonl` (added in the bet-row commit `f46a2f7`, 06:49, before data, as learn.md says) has the same sentence.
    - The read block matches `ledger/brier.md` at `08331f8`: 27 scored, Brier 0.209, observed hit rate 8/27 (9/29 = 0.31 running), newest audit `ta-b1r2.md` (06:31).
    - P3 and P8 exist.
    - The design change (a partial-correlation guard) is in the design.
    - The odds change 0.40 → 0.24 → 0.25 is recorded before data.
    - Rule 14 (odds only from a fresh context) was committed at 06:51, after this pre-registration, so it does not apply.
    - `check_prereg.py`: L1–L3, R1, R2 and H1 ok. R3 warns only that it found no result commit.
26. **holds on procedure; one miss.**
    - The review `1d52379` (07:10) postdates the pre-registration, with verdict fix-first.
    - The fixes are under D71 (`f09824e`, 07:12, before data).
    - The review was confirmed in `28cc32b` (07:14), before the run.

    *Missed (D3):* the F1 fix replaced the control instead of adding to it, so it could not be shown to "only tighten", and on the real data it loosened. Requiring both the frozen guard and the new one would have been a true tightening. The confirmation also accepted a dry run whose worlds never show the D71 guard above the frozen one. A check of the dry run's ρ(S, W) against the archive would have flagged this before data, but it means pairing S with a covariate, which the reviewer chose not to do.

## The pre-mortem, scored

**Disclosure first.** The pre-mortem sits in the pre-registration's §0 table, which A2 required me to read, so I saw it before the checklist. My own line was written with the guard table (item 3) in front of me, not from the pre-mortem.

**My account.** The bet did not fail under its operative rule. Had it failed, the most likely reason would be that the order archive's rating noise W carries the whole order-span/format-spread link (the frozen guard gives +0.085, interval through 0). Kind: `world`.

**The pre-mortem**: "If this fails, the most likely reason is that once extremity and rating noise are allowed for, order span and format spread share nothing, because both only track how unsure Haiku is about the claim. Kind: `world`."

**Score: `not_failed`; risk_seen: true.** The verdict is pass, unreplicated. The named risk did show up, though. Under the guard frozen with the pre-mortem (E and W), the shared part is +0.085 [−0.089, +0.270], and it survives only under D71's covariate set.

## Required cuts

All five are in the hand-written "In plain English" section of `programs/entangled-mind/results/gm2bf1-order-vs-format.md`. The generated table and the pre-registered reading stay as they are.

1. Replace "The correlation survives the boring explanation, that claims rated near the middle wobble more in both, as do noisy ones. Allowing for how extreme each claim's rating was in both archives, and how noisy its ratings were in the order conversations, it is 0.25 [0.09, 0.37]." with:
   "Allowing for how extreme each claim's rating was in both archives and how noisy its ratings were in the order conversations (the guard as fixed by the design review, D71), it is 0.25 [0.09, 0.37]. The guard as first frozen in the pre-registration, which allowed only for the format archive's extremity and the order noise, gives 0.09 [−0.09, 0.27] and would have failed. Allowing for the order noise alone gives 0.08 [−0.09, 0.26]. So the pass depends on which allowance is made, and noise alone accounts for the link."

2. Replace "Dropping any one item does not change the verdict." with:
   "Dropping any one item does not change the verdict, but dropping two (h126 and h158) takes ρ to 0.27, below the bar, and ρ's interval runs down to 0.16. The link is in gm2b's 30 items (ρ 0.42) and absent from gm2's 10 (ρ −0.09)."

3. Replace "In the design review's dry run, built on measured numbers, worlds with no shared instability still pass this rule 6–10% of the time." with:
   "In the design review's dry run, worlds with no shared instability passed this rule 0–10% of the time (6–10% where mid-scale claims wobble more in both). Those worlds understate how closely the order span follows rating noise (ρ 0.37–0.58 against the real 0.77), and in none of them did the review's guard come out above the original one, as it does here. So that rate is not a measured false-pass rate for these data."

4. Replace "On these claims, being unstable under question order and being unstable under answer format partly go together, beyond how mid-scale or noisy a claim is." with:
   "On these claims, being unstable under question order and being unstable under answer format partly go together after allowing for extremity in both archives and for rating noise in the order conversations. Allowing for that noise alone, they do not."

5. Replace "Two binary formats put 90 claims on one tied rank, so part of the format spread is tie position." with:
   "Two binary formats put 90 claims on one tied rank, so part of the format spread is tie position. With those ties broken at random instead of shared, ρ falls to about 0.24 (0.17–0.32) and reaches the 0.30 bar in 5% of tie orders; without the bet format (F3), ρ is 0.29."

Record fixes (not counted as cuts):
- D71's "only the guard is tightened" and "the guard removes false passes, not true ones" should be annotated, in a new DEVIATIONS row, as true in the dry run but not on the data (frozen guard fail, D71 pass).
- `experiments/gm2bf1-dryrun/README.md`'s "measured marginals only" should say that `marg.npz` holds the real per-claim format means (hence real G), W and the order-archive level.

## What would break it next

**Cheapest decisive test: a fresh replication of the order chains.** Haiku re-runs the shown O1–O4 chains on all 40 items at R = 10: 1,600 conversations, about $0.45 at gm2b's rate. The new order spans S′ are correlated with the archived G.
- The pass rule has to require **both** guards: the frozen E+W guard and the D71 guard.
- It also has to hold in each of the old gm2 and gm2b item groups (sign only).

That separates a real claim-level instability from today's specification-dependent partial, and from the gm2b batch. If both guards have to clear zero, I expect it to fail. A free precursor: compute S from repeats 0–4 and G from repeats 5–9, and the reverse, so that noise in S cannot be shared with W's own repeats. That cannot overturn the verdict, but it shows how much of S's link to W is the same draws.
