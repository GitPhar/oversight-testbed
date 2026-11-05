---
bet: em-qwalk
program: entangled-mind
prereg_commit: 680f128
results_commit: e6add3a   # the clone's re-commit of the results commit; author time 2026-11-04T20:32:59-07:00
auditor_session: audit em-qwalk (fresh subagent in the planter-built clone /Users/seanpharris/oversight-testbed-audit-em-qwalk, branch audit)
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-04 20:45 America/Denver
claims_checked: 24
holes_found: 10
overclaims_cut: 8
reproduced: false              # every table a committed command produces regenerates exactly; §3's first table (10,000 shuffles) has no committed generator, and its 0.156 is a minority draw
verdict_claimed: untestable    # the ledger row says `withdrawn` (counted, not scored); the results file's verdict is "untestable at this scale"
verdict_after_audit: untestable
verdict_stands: true
canary: unknown
false_alarms: 0
design_review_missed: ["D5 (both em-qwalk reviews): neither tested whether the design could pass in a world where the hypothesis holds. em-qwalk-1b called the fixed rule 'fair and possible to pass' on a 2% route. The power floor that withdrew em-qwalk2 (P12, now D11) applied equally to em-qwalk's identical graph and labels."]
failed: true
failure_reason: Withdrawn before data. Under leave-one-node-out each hidden direction's own label shaped both scores, in opposite directions, so on this hub-shaped graph the frozen rule's verdict was largely fixed by construction (kind design).
failure_kind: design
premortem_score: other
risk_seen: null
---

# Audit of em-qwalk: a simulated quantum walk against PageRank on program 1's direction graph

Scope: this audit covers the whole results file `programs/entangled-mind/results/qwalk.md`, which reports em-qwalk and its re-bet em-qwalk2 together. The header is for em-qwalk. The em-qwalk2 rows are checked as claims of the same file.

## In plain English

The verdict stands. Neither bet was ever run on the real outcomes. Both were withdrawn on design review before data. On program 1's graph, a test of this design could not have told a quantum walk from PageRank. I re-ran every committed dry run, and every number they produce matches the results file exactly. My own permutation-null calculation confirms the bar a pass would have had to clear. What has to go is the wording that says more than that:
- "the friendliest case possible": I found labellings that pass by searching for them, and the reviewers showed that other quantum-kernel recipes favour PageRank.
- "On the record we have, a quantum walk and PageRank cannot be told apart": this reads as a measurement, but nothing was measured on the record.
- the 80%-power sentence: it describes one condition of the rule, not the whole rule.
- "a tested harness ready to rerun": the code is pinned to this graph and still carries flaws the reviews named.
- the threshold 0.156: no committed command produces it, and 0.149 is the usual value.

The finding would break only if a design were shown that has real power on this graph. The reviews and my runs say no such design exists at 25 labels.

## The case that this result is false

The headline is "untestable at this scale, found before data". Here is the strongest case against it.

First, "untestable" is not a pre-registered outcome here. Both pre-registrations define untestable mechanically: n_hit < 5, n_kill < 5, or too many unreachable nodes. Neither condition holds on this graph (11 hits, 14 kills, 3 unreachable). The label was instead reached by a design review's judgment, built on simulated worlds that the author and reviewers chose.

Second, those worlds may not span the truth. A 4% pass rate in a few hand-built "quantum" worlds does not show that the real labelling is not one of the configurations that pass. Low power in the modelled worlds is not impossibility. A 1% bet that resolves null at 96% certainty still carries a little information.

Third, the claim that roughly 550 directions would make the test fair extrapolates one recipe's gap (+0.04). It uses the bootstrap-only power figure, and it assumes a larger graph would keep the same gap. Under the other recipes the gap reverses sign. So "a much larger record would reopen it" may be false: the question may have no answer under any n.

Fourth, the process may have leaked. The em-qwalk pre-registration allowed the design review to run only `--dry-run` and `--graph-counts` on the real graph. One reviewer ran `build_graph` and published all 25 real labels in its review. Both second-round reviewers' scratch scripts (uncommitted) touched the real topology. The withdrawals rest on uncommitted reviewer scripts, so the record cannot show that no one computed a real-label score and withdrew after disliking it.

Fifth, withdrawal is an escape hatch. A bet that would have resolved null is withdrawn, counted and never scored. If the engine can withdraw whenever a reviewer says "redesign", calibration on hard questions is never tested.

The checklist below finds most of this case answered:
- The untestable finding rests on tables that regenerate exactly from committed code.
- The bar a pass must clear depends only on the graph and the counts, and I recomputed it independently.
- Withdrawal on a redesign is the written rule (design-review.md; ARCHITECTURE.md line 66).
- At odds of 0.05 and 0.01, a scored null would have *helped* the engine's Brier, so withdrawing cost the engine rather than saving it.

What survives of the case is wording. The file oversells the planted worlds ("friendliest case possible"), the power, and the harness. And the 550 figure is a rough extrapolation, which the file does label as such in §3.

## Claims checked

| # | claim (quoted or paraphrased from results/qwalk.md) | check run | outcome |
|---|---|---|---|
| 1 | "$0", no QPU, no API calls; numpy simulation | imports of qwalk.py and qwalk2.py (argparse, hashlib, json, os, re, subprocess, sys, numpy); no network library; ledger rows cost_usd 0, qpu_s_used 0 | holds |
| 2 | Both bets withdrawn before data; neither scored | ledger rows em-qwalk and em-qwalk2: `verdict: withdrawn`, `scored: false`; no `results/qwalk*.json` anywhere in history (`git log --all`); both `--run` gates refuse (called `review_says_go()` directly: "verdict redesign"; "em-qwalk2-1b.md: verdict fix-first") | holds (as far as the committed record can show) |
| 3 | 41 directions, 38 links, 25 settled (11 hit, 14 kill), 5 components | `qwalk.py --graph-counts 680f128` and `qwalk2.py --graph-counts 680f128` | holds |
| 4 | hub `oe` with 19 neighbours; mostly one hub | auditor script: oe degree 19; component sizes [1, 6, 4, 1, 29] | holds |
| 5 | links are parent plus shared data runs | em-qwalk.md D2: rule 3 adds no edge beyond parent links; parent-only drops 3 edges | holds |
| 6 | star, random outcomes: frozen rule says "classical" 200 of 200 | auditor re-run with qwalk.py's `analyse` on a 20-leaf star, B = 2,000: classical 100/100 for each of hub unlabelled, hit, kill | holds |
| 7 | frozen rule passes a below-chance walk: about 57%, mean AUROC 0.33 against 0.20 | `qwalk.py --dry-run`: depth-parity pass 56.3%; the AUROC means come from em-qwalk.md (0.344/0.195) and em-qwalk-1b.md (0.336/0.199) | holds |
| 8 | frozen rule's false-pass rate on the real links with shuffled outcomes is about 4% (4.3%, 68 of 1,600) | auditor re-run, 1,600 shuffles at B = 10,000: 56 pass (3.5%), 123 classical (7.7%); at B = 2,000, 34/1,200 (2.8%) | holds ("about 4%" is within noise of 3.5%). Not reported: the false *classical* rate there is about 8% |
| 9 | "3.8% of 600 … cannot be regenerated from the record" | qwalk2.md §10 states 3.8% with no n and no code | holds as disclosed (cannot check) |
| 10 | em-qwalk2: false verdict at most 0.4% under random outcomes | `qwalk2.py --dry-run` and `--dry-run-real-topology 680f128`: 0.2 / 0.4 / 0.1% real links; 0.2 / 0 / 0.1% hub graphs; classical 0% throughout | holds |
| 11 | §3 table rows (real links, hub graphs, four planted worlds, flips) | the same two commands plus `--dry-run-planted 680f128`: every row matches to the printed digit (e.g. quantum field 2% / 1%, 0.789 / 0.751; classical sources classical 4.0% (0.5%), 0.675 / 0.690) | holds |
| 12 | Δ must exceed the null's q975 = 0.156 (review: 0.149) | no committed command computes it. Auditor script, P = 10,000, real links with values discarded, 40 seeds: 0.149 in 34, 0.143 in 3, 0.156 in 2, 0.150 in 1 | **hole**: not regenerable; 0.149 is the usual value |
| 13 | quantum AUROC q975 0.779 (review 0.786) | same script: 0.786 in 21 of 40 seeds, 0.779 in 16 | holds as a range (0.779–0.786); not regenerable from a committed command |
| 14 | null mean AUROC 0.478 / 0.485 | same script: quantum 0.473–0.479 (mean 0.476), PageRank mean 0.484 | holds |
| 15 | 80%-power gap about 0.19 (median, shuffled real links) | `--dry-run-real-topology`: median_visible_gap_80 0.186 | holds as a bootstrap figure. The plain sentence "the test sees about 0.19 at 80% power" is a **hole** (C16) |
| 16 | quantum-kernel worlds "the friendliest case possible"; "the friendliest quantum world separates … 0.04" | em-qwalk2.md D4: two other recipes give Δ −0.02 to −0.04. Auditor hill-climb over 11/14 labellings on the real links (10 restarts, label values discarded): Δ 0.21–0.34 reached; 2 of 10 pass the full em-qwalk2 rule (Δ 0.29, q 0.81; Δ 0.21, q 0.83) | **hole**: overclaim |
| 17 | "Whatever the truth, the test would almost always have said 'not detectably different'" | as #16: true in every *modelled* world, false for searched labellings | **hole**: overclaim |
| 18 | "On the record we have, a quantum walk and PageRank cannot be told apart" | nothing was computed on the real outcomes (#2) | **hole**: reads as an empirical finding |
| 19 | 25 × (0.19 / 0.04)² ≈ 564, roughly 550 | arithmetic 564.06; labelled "order-of-magnitude" in §3 | holds (as a labelled estimate) |
| 20 | "The reviewer counted 59 across all of the testbed's maps today" | em-qwalk2.md F2: 39 + 17 + 3. `qwalk2.py --graph-counts ad66366`: 39 labelled, of which 14 are the bmq scout's reading-stage labels that D57 set aside as not tested outcomes | **hole** (minor): 59 overstates the tested outcomes |
| 21 | "so the leak cancels" | em-qwalk2.md D3: the Δ condition runs at 3.65% with `oe` held hit, so the leak cancels on average, not exactly | **hole** (minor) |
| 22 | "A tested harness (`qwalk2.py`) ready to rerun when the ledger is large enough" | `INPUT_COMMIT` hard-coded to 680f128; `clusters()` still includes the whole 29-node component (fires mechanically, em-qwalk2.md F5); `confirmed_at: pending` still counts as confirmed; `prereg_commit()` and `recorded_seeds()` still read the working tree (F6); D58 (a)–(i) outstanding | **hole**: overclaim |
| 23 | pre-mortems quoted in §4 | compared with 680f128 §0 and 1f6887d §0: identical | holds |
| 24 | record table §7 (commits and what each did) | `git log` 680f128..e6add3a: each hash exists with the stated content | holds |

## Checklist

**A. Was it pre-registered as claimed?**

1. **Pre-registration predates any call or analysis: holds.**
   - Author times: 680f128 at 19:46:46 −07:00; the seed (34bad77) at 19:47:34; the bet row (c0850f1) at 19:48:11; the reviews 3244dbb at 19:57:51 and 6635276 at 20:05:20; the withdrawal (c9b2f3b) at 20:08:16.
   - There are no API calls. No `results/qwalk*.json` exists in any commit (`git log --all -- 'programs/entangled-mind/results/qwalk*.json'` is empty).
   - The author disclosed having read the map's outcomes before writing the rules (§2). That is allowed and stated.
2. **Rule, statistic, seed and budget match word for word: holds.**
   - The §1 table's pass rule for em-qwalk ("Δ AUROC > 0, bootstrap lower end > 0") matches 680f128 §5.2.
   - The budget ($0, 0 QPU s) and seed purpose (bootstrap) match.
   - Every departure has a DEVIATIONS row dated before data: D56 (withdrawal), D57 (re-bet), D58 (second withdrawal).
3. **The bar was not lowered: holds.** em-qwalk2 raised it: permutation null, chance conditions, four oriented dumb rules. It was a new pre-registration with its own seed and lesson, not an edit.
4. **The primary was not swapped: holds (not applicable).** No primary statistic was computed on real data, and no secondary is promoted.
- **A, extra: the design review exceeded §3. Hole (minor).** 680f128 §3 says the design review "may also run `--dry-run` … and `--graph-counts` …; nothing else touches the real graph before the go."
   - em-qwalk.md ran `build_graph` and the parent-only edge diff on the real graph, and printed all 25 real labels in its committed review.
   - em-qwalk-1b ran structure probes and random-label runs on the real topology (label values deleted).
   - No DEVIATIONS row records this.
   - Consequence: none for the verdict. The labels were already public in the map and known to the author, and no predictor was computed on them.

**B. Is the number real?**

The results file reports no real-data statistic. Every number is a synthetic dry run, and those are what I checked.

5. **Ties: holds.** AUROC counts ties as ½ in both qwalk.py (`auroc`) and qwalk2.py (`auroc_rows`). Scores are rounded to 1e-12 so that unreachable nodes tie exactly at 0. The star rows with an unlabelled hub are reported as untestable for exactly that reason.
6. **Pooling: holds.** The shuffled real-link rows are reported separately for `oe` held hit, held kill and free. The hub-graph rows are split the same way.
7. **Few items: holds (not applicable).** There is no real result. Both designs pre-registered leave-one-label-out, and em-qwalk2 added leave-one-cluster-out.
8. **Circular estimators: holds.**
   - em-qwalk2's score is free of the item's own label: I flipped each settled node's label over 200 random labellings, and the maximum change in its own score was 0.0 for both arms.
   - The remaining leak runs through the fixed count, and the permutation null carries it.
   - Edges made after, and because of, outcomes are disclosed (qwalk2.md §6) and given a prospective sensitivity.
9. **Baselines: holds.** em-qwalk2 puts four oriented dumb rules inside the rule. The untestable claim needs no baseline.
10. **Uncertainty: holds, with a note.**
    - Planted-world rates rest on 200 graphs each (SE about 1 point at 2–4%), and shuffled rates on 1,000 (SE about 0.2 points). "At most 4%" is the maximum over about 15 noisy rates. That biases it upward, which is conservative for the untestable claim.
    - The stratified bootstrap with scores held fixed is anti-conservative by about 2× (em-qwalk2.md D3). This affects only the bootstrap conditions, and the conjunction with the permutation null absorbs it.
11. **Multiple comparisons: holds (not applicable).** There is no headline test.
12. **Leakage: holds.** No real label reached any fitting step. Every dry run deletes the label dict after `load()`: `dry_run_real_topology` and `dry_run_planted` call `del labels` before any computation (read in the code).
- **B, extra: reproduction. Hole.**
    - Ran `qwalk.py --dry-run` (13 s): it regenerates 680f128 §4 exactly (2.7 / 4.4 / 93.0%; 0.3 / 3.5 / 96.2%; 56.3%).
    - Ran `qwalk2.py --dry-run` (65 s), `--dry-run-real-topology 680f128` and `--dry-run-planted 680f128`: every §3 row in the second table matches.
    - The first §3 table ("quantity (10,000 shuffles)") has no committed generator. §6 lists no command for it, and qwalk2.py has no function that runs P = 10,000 on the real topology outside `--run`.
    - My independent computation (script `null_seeds.py`, below) gives Δ q975 = 0.149 in 34 of 40 seeds and 0.156 in 2. The file headlines the minority draw, and plain English rounds it to "about 0.16".
    - The verdict does not hinge on it.

**C. Does the write-up say only what the data say?**

13. **Scope drift: hole.** "On the record we have, a quantum walk and PageRank cannot be told apart." Nothing was measured on the record. The finding is about the design's power on this graph. See cut 4.
14. **Rank drift: holds.** P11, P12 and D11 are listed as process products, not findings.
15. **Mechanism drift: hole (minor).** "So the leak cancels" states exact cancellation. The reviewer measured cancellation on average only (Δ condition at 3.65% with `oe` held hit). "Differ mainly in how they spread" is acceptable. The fuller description is unitary against diffusive dynamics, Born-rule against probability readout, and degree weighting (em-qwalk2.md F3).
16. **Plain English against the table: hole.** Sentences the tables do not support:
    - (a) "the friendliest case possible" and "The friendliest quantum world …". Only one recipe gives +0.04. The reviewer's other recipes give PageRank the edge, and searched labellings reach Δ 0.21–0.34 with passes (claim 16). em-qwalk2.md F4(b) had already asked that this phrase not be used.
    - (b) "Whatever the truth, the test would almost always have said 'not detectably different'". True only of the modelled worlds.
    - (c) "The test sees about 0.19 at 80% power". That is the bootstrap condition alone. The full rule also needs q above about 0.786 and above best_dumb, so its power at 0.19 is lower (em-qwalk2.md D5).
    - (d) "about 0.16" (see B, extra).
    - (e) "A tested harness … ready to rerun when the ledger is large enough". The code is pinned to 680f128 and carries unfixed review flaws (claim 22). §5 of the same file lists the changes a rerun would need.
    - (f) "59" counts the bmq scout's 14 reading-stage labels, which D57 excluded as not tested outcomes.
17. **Citations: holds, with one exception.** No external paper is cited. Each cited review and DEVIATIONS row says what it is cited for, except that em-qwalk2.md explicitly asks *not* to call one recipe "the most quantum-favourable world", and the results file does so (16a).
18. **Negative results stated plainly: holds.** Both withdrawals and the untestable outcome are stated first, in bold, with "This does not say Sean's idea is wrong".

**D. Process**

19. **Budget: holds.** $0 by construction: no API or hardware code exists, the ledger shows cost 0 and qpu_s_used 0, and the dry runs took laptop minutes.
20. **Stop-on-refusal: holds (not applicable).**
21. **Scale direction: holds (not applicable).** There is no graded prompt.
22. **Replication: holds (not applicable).** No hit is claimed.

**E. Engine records**

23. **Seed: holds internally; the pulse could not be checked.**
    - `python3 ledger/seed.py a7ee3f40…a771 em-qwalk --purpose bootstrap` gives 16001949444733414920, as recorded.
    - The pulse is 1591631 at 02:47:00.160Z; the pre-registration's author time is 02:46:46Z; the recorded previous pulse is at 02:46:00.253Z. CURBY-Q is stalled (round 28297), so CURBy-RNG is correct.
    - The code passes the seed only to the bootstrap (seed + 1 for the chance intervals).
    - Not checked: refetching pulses 1591630 and 1591631. The brief confines this audit to the clone.
24. **Tiebreak: not applicable.**
25. **Lesson: hole, caught before data.**
    - These parts hold. The §0 lesson is in 680f128. `ls-em-qwalk` (c916490, 19:48:41) matches it (`check_prereg.py em-qwalk … --before-run`: L1, L2, L3 ok). The read block matches the ledger at 680f128: 14 scored, Brier 0.246, 5/14 (`git show 680f128:ledger/brier.md`), and `ss-b1.md` is the newest audit (19:13:41).
    - The lesson's central claim, "exact classical twin (same generator, seeds, stopping time)", was false on the seeding (em-qwalk.md D4).
    - P3's `do_this` ("beat it by a margin") was not in the design: the baselines were reported, not ruled on.
    - The stated reason for moving the odds from 0.04 to 0.05 (the 56% depth-alternating route) was the below-chance artefact.
    - All three were caught by the design reviews and resolved by withdrawal, so no odds revision was owed.
26. **Design review: holds.**
    - Both reviews were committed after 680f128 and before any analysis (`check_prereg.py`: R1 ok, 6635276 at 20:05:30).
    - The binding verdict was redesign, and the bet was withdrawn (D56) as design-review.md requires.
    - Missed: neither em-qwalk review asked whether the fixed design could pass in a hypothesis-true world. em-qwalk-1b concluded "the test stays fair and possible to pass" on a 2% route. The power floor that later sank em-qwalk2 on the same graph (P12, now D11) was already present (see `design_review_missed`).

Independence notes:
- My scratchpad directory belongs to the same session id (19f84df9…) that the em-qwalk-1b and em-qwalk2-1b reviewers used for their scripts (`…/scratchpad/rev/`, `…/rev2/`, named in their reviews). So this audit was launched from the session that launched the second reviewers. I did not open those directories; my scripts are in `…/scratchpad/audit-em-qwalk/scripts/`.
- To find the output path, I listed `/Users/seanpharris/oversight-testbed/ledger/audits/` and ran `git status` in that checkout. I read no file there except `operators/auditor.md`, as the launch line directs.
- I read the pre-mortems before the checklist. That could not be avoided: they sit in 680f128's §0 table, which A2 requires reading, and in the results file's §4.

## The pre-mortem, scored

**My reason, written from the checklist evidence:** em-qwalk failed as a design. Under leave-one-node-out, each hidden direction's own label shaped both scores in opposite directions, so on this hub-shaped graph the frozen rule's verdict was largely fixed by construction (classical 300 of 300 on stars in my re-run; false classical about 8% and false pass about 3.5% on the real links with shuffled labels). It was withdrawn before data. **Kind: design.** (Disclosure: as noted above, the pre-mortem was visible to me before this line was written.)

**The pre-mortem (680f128 §0):** "If this fails, the most likely reason is that program 1's labels cluster by branch (whole subtrees killed together), where the dry run shows both walks rank alike, so the gap sits inside the ±0.12 interval." Kind: `world`.

**Score: other.** The pre-mortem names a world mechanism: branch-clustered labels on which the walks tie. The bet failed through a design mechanism it does not name, the own-label leak, of a different kind. (For the record, em-qwalk2's pre-mortem, of kind `design`, named the power failure that withdrew it. em-qwalk2 is not the bet scored here.)

## Required cuts

All in `programs/entangled-mind/results/qwalk.md`. Mirror cuts 2, 4 and 5 in the st-13 `outcome` line of `ledger/steers.jsonl`, which repeats "nearly indistinguishable" and "ready to rerun when the ledger is large enough".

1. Plain English, item 2, second paragraph. Replace *"We built made-up worlds where the outcomes were generated by the quantum walk itself, the friendliest case possible. Even there, the quantum walk beat PageRank by only about 0.04, and the test passed at most about 4% of the time."* with: *"We built made-up worlds where the outcomes were generated from the quantum walk's own kernel. In the recipe the author chose, the quantum walk beat PageRank by only about 0.04 and the test passed at most about 4% of the time. In the reviewer's other recipes PageRank came out ahead."*
2. Same paragraph. Replace *"Whatever the truth, the test would almost always have said "not detectably different"."* with: *"In every world anyone built from a model of how the outcomes might arise, the test would have said "not detectably different" at least 95% of the time; only labellings searched for the purpose passed."*
3. Same paragraph. Replace *"by about 0.16 in AUROC"* with *"by about 0.15 in AUROC"*. In §3's first table, replace *"0.156 (the review's run: 0.149)"* with *"0.149 (auditor, 34 of 40 seeds; 0.143–0.156 across seeds)"* and *"0.779 (the review's run: 0.786)"* with *"0.779–0.786"*. Either commit the generator and name it in §6, or cite this audit's script for that table.
4. "What this says". Replace *"On the record we have, a quantum walk and PageRank cannot be told apart."* with: *"On the record we have, no test of this design could tell a quantum walk from PageRank; neither was ever scored on the real outcomes."*
5. "What it produced anyway". Replace *"A tested harness (`experiments/qwalk2.py`) ready to rerun when the ledger is large enough."* with: *"A reviewed harness (`experiments/qwalk2.py`), pinned to program 1's graph at 680f128; a future bet would need the D58 (a)–(i) changes before reusing it."*
6. §3, last paragraph. Replace *"The friendliest quantum world separates the two arms by about 0.04 AUROC (0.789 − 0.751). The test sees about 0.19 at 80% power."* with: *"In the author's quantum-kernel field world the arms separate by about 0.04 AUROC (0.789 − 0.751); other recipes give between about −0.04 and +0.05. The bootstrap condition alone sees about 0.19 at 80% power; the full rule, which also needs the quantum AUROC above about 0.78 and above every one-line rule, sees less."*
7. Plain English, item 2, first paragraph. Replace *"so the leak cancels"* with *"so the leak is carried by the shuffled outcomes and cancels on average"*.
8. "What this says". Replace *"The reviewer counted 59 across all of the testbed's maps today."* with: *"The reviewer counted 59 labelled directions across all maps today, 14 of them the biomimicry scout's reading-stage labels that em-qwalk2 set aside as not tested outcomes."*

## What would break it next

The verdict is "untestable at this scale". It would break if a design existed that has real power on program 1's 25 labels, and no reviewer has found one. The cheapest test ($0, laptop minutes, no real labels) has three parts:
- Pre-register a sweep over a committed family of planted worlds: field, sources and self-consistent recipes, each at several signal strengths, plus the combinatorial-Laplacian arm pair that removes the degree weighting.
- Search for any statistic, among a pre-declared short list (Δ AUROC, rank correlation of scores, a likelihood-ratio on the kernel), whose P(pass) ≥ 0.5 in some committed quantum-favourable world and ≤ 0.05 under shuffled labels.
- If one exists, em-qwalk3 becomes a real bet on this graph, and "untestable at this scale" was premature. If none does, the D58 bar stands.

A second, also $0 check targets the "roughly 550" estimate. Run the same planted-world simulation on synthetic hub-and-branch graphs at n = 100, 250 and 550 settled nodes, and see whether P(pass) actually reaches 0.5 or stays flat because the arms' gap shrinks with size. If it stays flat, §5's "the likeliest way there is a much larger record" is wrong and should say so.

Auditor scripts (not committed; label values deleted after `load()` in every one):
- `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/19f84df9-a6ff-48ba-89d6-d3f43e5d1747/scratchpad/audit-em-qwalk/scripts/null_thresholds.py`
- `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/19f84df9-a6ff-48ba-89d6-d3f43e5d1747/scratchpad/audit-em-qwalk/scripts/null_seeds.py`
- `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/19f84df9-a6ff-48ba-89d6-d3f43e5d1747/scratchpad/audit-em-qwalk/scripts/checks.py` (gates, star, frozen_real, ownlabel, hillclimb)
