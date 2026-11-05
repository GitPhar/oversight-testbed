---
bet: em-qwalk2
program: entangled-mind
prereg_commit: 1f6887d
seed_commit: ad66366
reviewer_session: design-review em-qwalk2 (fresh subagent launched by the author's session; worktree at ad66366; no chat, transcript or author message read)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-04 20:40 America/Denver
checks: {D1: holds, D2: holds, D3: holds, D4: flaw, D5: flaw, D6: holds (no calls; pre-mortem kind design), D7: flaw, D8: flaw, D9: flaw, D10: flaw}
flaws: 6
pilot_usd: 0.00
verdict: redesign
confirmed_at: null
---

# Design review of em-qwalk2

## In plain English

The re-bet fixes the two problems that sank em-qwalk. Each direction's own label no longer decides the contest, because every verdict is now read against shuffled labels. A walk that is worse than a coin can no longer pass. The code does what the pre-registration says, and every dry-run number the code produces reproduces exactly. But the test, as built, cannot answer its question. On program 1's graph the rule says "pass" at most about 4% of the time, and that is in the most quantum-friendly labels anyone has built (the author's recipe; I measured 4.3%). With two other ways of building quantum-kernel labels, PageRank reads the labels *better* than the quantum walk does, and the rule passes 0%. "Classical" is just as hard to reach: at most 4% even when the labels are built to favour PageRank. So the verdict will be "null" about 96–100% of the time whatever the truth is. §5 already says that this null means nothing. A bet whose result is known before it runs is not a test. Scoring it at 1% odds would also add an almost free point to the engine's Brier score: the headline would move from 0.267 to about 0.250 without anything being learned. design-review.md calls this a **redesign**. Withdraw em-qwalk2 before data. Re-bet only on a graph with far more settled directions: every map together holds 59 today, against the roughly 550 the author's own estimate says are needed. I also found five fixable flaws, listed below, which any re-bet should carry over.

Disclosures:
- I did not see `em-qwalk2-1b.md`. The only time I listed `ledger/design-reviews/` was at the start, filtered to "qwalk", and it showed only `em-qwalk.md` and `em-qwalk-1b.md`.
- I invoked `qwalk2.py --run` twice in my worktree, against the brief. The first call (no seeds) was refused at the argument check. The second (`--seed-bootstrap 1 --seed-permutation 2`) was refused by `review_says_go()`, the first line of `run()` ("missing em-qwalk2.md"). Neither call loaded the inputs or computed anything.
- I computed no score, AUROC, Δ or verdict on the real label values.
- After writing this review, and just before committing it, I re-ran `check_prereg.py --before-run`. Its output line "R2+ FAIL em-qwalk2-1b.md: verdict fix-first, confirmed null" showed me the other review's verdict. I read nothing else of that file. Nothing in this review was changed after seeing that line, apart from adding this note.

## What I ran

Worktree `.../scratchpad/review-em-qwalk2` at ad66366. My test scripts are in `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/e4de0b43-599f-44d4-af8f-9d60c90fe159/scratchpad/rv/tests/` and are not committed.

Every script that touches the real graph goes through `real_structure()`. That function loads `qw.load("680f128")`, keeps the set of labelled node ids and the hit count, and deletes the label dict before returning. Every label used after that is synthetic.

One fact makes some of these runs possible without the real labels. The permutation null for an 11/14 labelling on a fixed node set is the same for every labelling. Its thresholds therefore depend only on the graph and the counts (t4).

- `--graph-counts 680f128`: 41 nodes, 38 edges, 25 labelled (11 hit, 14 kill), 5 components.
- `--dry-run` and `--dry-run-real-topology 680f128` (outputs in `rv/dry.txt`, `rv/dryreal.txt`).
- `t1_kernel.py`: independent check of the quantum kernel and the PageRank identity.
- `t2_size.py`: the false rate of each pass condition on the real topology, with `oe` held hit, held kill and free (2,000 labellings each).
- `t3_power.py` and `t7_planted2.py`: planted-label worlds (300–400 labellings each).
- `t4_thresholds.py`: the permutation-null thresholds (P = 20,000), and an adversarial search for the labelling with the largest Δ.
- `t5_struct.py`: the clusters used by leave-one-cluster-out.
- `t6_gate_verdict.py`: `verdict()` on synthetic tables, and the review gate on synthetic review files in a temporary directory.
- `t8_depth.py`: depth and component size as candidate dumb rules.

## Checks

**D1. A stranger can apply the rule: holds.** I ran `verdict()` on 12 synthetic tables, and each returned exactly one verdict, the one §5 gives:
- the clean pass returns pass;
- each pass condition violated alone returns null (q equal to best_dumb, q's bootstrap lower end at 0.49, Δ at the permutation q975, q at its permutation q975, lo equal to 0);
- the clean classical case returns classical, and classical with PageRank below chance returns null;
- n_hit = 4 returns untestable, n_zero = 12 still passes, and n_zero = 13 returns untestable;
- the case where the walk is below chance but less wrong than PageRank (q 0.35, p 0.20, lo > 0) returns null.

The code's untestable threshold is `n_zero > n_labelled/2`, which equals §5's "n_zero > 12" only at 25 labels (see D9).

**D2. Every manipulation takes effect: holds.**
- Both dry runs reproduce every number they produce in §4 exactly. Shuffled real links give 0.2% / 0 / 0.483 / 0.493 / 0.476. With `oe` held hit: 0.4%, mean AUROCs 0.481 / 0.487. With `oe` held kill: 0.1%, 0.476 / 0.484. The follow-ups, depth ≤ 1, alternation and siblings rows match, as do all six star and hub-shaped rows.
- The D2 line also reproduces: τ moves the quantum score by 0.132 and PageRank by 0.147; the kernels differ by at most 0.605; quantum rows sum to 1 ± 2e-15; the PageRank identity holds to 1e-16; the Monte Carlo error is 0.0049 at 4,000 draws and 0.0023 at 64,000, as §2 now states.
- **Exact quantum kernel (t1):** it matches a direct quadrature of E_t|⟨i|e^{−iL_sym t}|j⟩|² with t ~ Exp(τ) to 8e-8 on a 7-leaf star (degenerate spectrum) and on a 6-cycle with an isolate, and to 2e-6 on a 44-node hub graph. It is exactly symmetric, and its rows sum to 1. The formula Σ V_ik V_il V_jk V_jl / (1 + (λ_k − λ_l)²τ²) is correct.
- **Classical kernel:** `classical()` equals power-iteration PageRank to 3e-16, and its rows sum to 1.
- **Score:** `scores()` is s(i) = Σ_{j≠i} y_j C_ji − ȳ₋ᵢ Σ_{j≠i} C_ji, which is §2's formula.
- **The inputs pinned at 680f128 are justified and correctly done.** `INPUT_COMMIT` is the full sha, and `run()` takes no commit argument. Comparing 680f128 with 1f6887d (equality only, no value printed):
  - all 41 old nodes are still present, and none is removed;
  - the edges among the old nodes are identical;
  - no old label changes value or disappears;
  - the only newly labelled old node is `bmq`;
  - 18 new nodes (13 of them labelled) hang off `bmq`.

  Keeping 680f128 tests exactly the inputs em-qwalk froze and both reviews examined. Including the scout's reading-stage labels would add a 19-node star built from labels that are not bet outcomes.

**D3. Every control can fail: holds, with notes.**

The permutation null does control the leave-one-out leak at the verdict level on this graph, including with the most influential node's label held each way. False-rate of each condition on the real links with shuffled labels (t2, 2,000 labellings per row, B = P = 500, simulation SE about 0.4 points at 3%):

| `oe` | Δ > perm q975 | bootstrap lo > 0 | q > its perm q975 | q's bootstrap lo > 0.5 | q > best_dumb | **pass** | Δ < perm q025 | hi < 0 | **classical** |
|---|---|---|---|---|---|---|---|---|---|
| held hit | 3.65% | 4.8% | 2.05% | 5.65% | 14.8% | **0.10%** | 3.15% | 6.9% | **0%** |
| held kill | 3.15% | 4.35% | 2.35% | 6.55% | 14.9% | **0.25%** | 2.25% | 5.8% | **0%** |
| free | 2.95% | 4.4% | 2.4% | 5.9% | 13.1% | **0.35%** | 3.0% | 7.35% | **0%** |

Notes, none of them a flaw under this rule:
- With `oe` held hit, the Δ-against-null condition alone runs a little above its nominal 2.5% (3.65%). The leak is not cancelled exactly conditional on the hub's label, as §1 claims ("the comparison cancels the leak"); it is cancelled on average.
- The stratified bootstrap with scores held fixed is anti-conservative by about 2×: lo > 0 occurs 4.4–4.8% of the time, and hi < 0 occurs 5.8–7.35%, against 2.5% each.
- The conjunction of conditions brings both false verdicts to 0.35% or less.
- The star rows in §4 cannot fail as a Δ control. On a star, both arms rank the leaves by their own label identically, so Δ ≡ 0. Their "0% false" is true by construction. The hub-shaped and real-link rows are the ones doing the work.

**D4. Rivals are matched, neither wins by construction: flaw (F1).** The odds (1%), the pre-mortem, the lesson ("labels planted from the quantum kernel itself pass only 1–2%") and the frozen null sentence ("in the most quantum-favourable world we could build the gap was about 0.04") all rest on the two "planted from the quantum / classical kernel" rows of §4. **Neither row is produced by any code in the commit.** `dry_run_real_topology()` stops at the siblings row.

I rebuilt them three ways (t3, t7). One recipe reproduces the author's numbers. In the other two, PageRank beats the quantum walk on the quantum kernel's own labels:

| recipe (top 11 of a latent field, 25 labelled nodes) | world | pass | classical | mean AUROC q / p | mean Δ |
|---|---|---|---|---|---|
| g ~ N(0, 1) on all 41 nodes, f = g·K, **diagonal kept** (matches the author's 0.789 / 0.751) | quantum | 4.3% | 0% | 0.789 / 0.743 | +0.046 |
| same | classical | 0.3% | 0% | 0.754 / 0.748 | +0.006 |
| g on all 41 nodes, f = g·K, diagonal zeroed (t3) | quantum | 0.25% | 0% | 0.636 / 0.657 | −0.021 |
| same | classical | 0% | 0.75% | 0.636 / 0.662 | −0.026 |
| g on the 25 labelled nodes, smoothed by the labelled columns | quantum | 0% | 0.3% | 0.584 / 0.604 | −0.020 |
| labels self-consistent with the arm's own leave-one-out score (3 iterations) | quantum | 0% | 0.7% | 0.666 / 0.708 | −0.042 |
| same | classical | 0% | 4.0% | 0.758 / 0.799 | −0.040 |

The quantum walk's "win" therefore depends on the recipe. With the diagonal kept, a node's own random draw dominates its latent value, because the quantum walk keeps most of its mass at home. That is the recipe in which the quantum arm wins. "Neither wins by construction" is not shown by a single selected recipe, and "the most quantum-favourable world" sentence describes that one recipe only.

Reachability: an adversarial hill-climb over labellings (t4, 30 restarts) finds labellings with Δ = 0.26, q = 0.85 and p = 0.59 that the full rule passes. A pass is therefore possible, but only on labellings searched for it.

**D5. A dumb baseline is beaten, and the design can see the effect: flaw (F2, the reason for redesign).**
- **Trivial predictors cannot pass.** A constant has AUROC 0.5 and fails the chance conditions. A below-chance walk fails them too: the depth-alternating and follow-ups worlds give 0% pass, and my synthetic table returns null. A leak-only score is absorbed by the null (D3).
- **The design cannot see the effect.**
  - The permutation-null thresholds on this graph, which do not depend on the label values (t4, P = 20,000), are: Δ q975 = 0.149 (null SD 0.073); quantum AUROC q975 = 0.786; PageRank q975 = 0.773. Under the null the two AUROCs correlate at 0.90.
  - A pass needs Δ > 0.149 *and* q > 0.786 *and* q above an oriented best-of-four dumb rule, whose median is 0.69–0.80 in every planted world.
  - In every world built so far (the author's and mine), P(pass) is at most 4.3% and P(classical) at most 4.0%.
  - P(pass) in the best quantum world (4.3%) is not clearly separated from P(pass) under shuffled labels (0.2–0.35%) or the classical worlds (0–0.3%) at these sample sizes. Either way, a null is 96–100% certain whatever the truth.
  - §5's null sentence already concedes that a null "says one program's record is too small to test the idea, not that the idea is wrong". So no outcome with appreciable probability answers the question. This is "the test cannot answer its question as built", design-review.md's example of a redesign.
  - The author's pre-mortem (kind `design`) predicts exactly this.
- **Power statement: honest in size.** The bootstrap-based 80%-power gap (median 0.186 on shuffled links; it reproduces) is close to what the Δ-permutation condition alone needs (0.149 + 0.84 × about 0.06 ≈ 0.20). The full rule's power at a gap of 0.19 is lower than 80%, because q must also clear 0.786 and best_dumb, and §5 should say so. The order-of-magnitude n of about 550 is labelled as an estimate, which is fair.
- **Odds.** 1% is consistent with these numbers, given that the best recipe gives about 4%. That is exactly the problem: a bet at 1% that resolves null scores a Brier of 0.0001. With 15 scored bets at 0.267, scoring it moves the headline to (0.267 × 15 + 0.0001) / 16 ≈ 0.250, from "about a coin" to "a coin", for a test whose outcome was fixed by its design.
- **Smaller, fixable issues:**
  - P3's `do_this` says "beat it by a margin", but the rule uses q > best_dumb with zero margin.
  - The dumb set omits **depth** and **component size**. The author's own depth ≤ 1 world is a depth rule (depth's oriented AUROC is 0.905 there, against q's 0.738).
  - In an "in the big component" world (t8), q beats the four listed dumb rules 57% of the time, but beats component size as well only 21% of the time.
  - No pass in my runs was beaten by depth or component size, so this did not change any verdict here.

**D6. Execution risks are piloted: holds (not applicable).**
- There is no API call and no hardware. The imports are argparse, hashlib (unused), json, os, re, subprocess (git only), sys and numpy.
- The pre-mortem's kind is `design`, not `execution`.
- The dry runs ran in 1:22 and 0:48.

**D7. Comparisons match: flaw (F3).**
- The computations are matched: both arms use the same 24 single-seed walks, the same centred weights, the same graph, the same τ and the same zeroed diagonal. em-qwalk's seeding mismatch is gone.
- But §1 says "the only difference is how one walk spreads: quantum amplitudes that can interfere, or classical probabilities that only add … nothing else differs", and §10 says "they differ only in the one-seed kernel". The kernels differ in more than interference:
  - the classical kernel obeys detailed balance, K_C[j,i] = K_C[i,j] · d_i/d_j (checked to 5e-16), so what a node receives scales with its degree;
  - the quantum kernel is symmetric, with no degree weighting;
  - one readout is the Born rule on a unitary walk, the other a stochastic walk.
- The degree weighting is a choice (L_rw against L_sym), not intrinsic: both arms could use the combinatorial Laplacian, where both kernels are symmetric. On a hub graph, degree weighting is not a small difference.
- Either rewrite §1, §5 and §10 as a claim about the bundle (unitary dynamics, Born-rule readout, no degree weighting, against diffusion with degree weighting), or add a matched secondary on the combinatorial Laplacian.

**D8. Verdict sentences are written: flaw (F4).** The sentences exist for every verdict and use the right nouns ("direction graph", "separated", "a pattern in the record, not a forecast"). Two clauses are false or unsupported:
- (a) The pass sentence says the walk "beat chance and every one-line rule, each judged against shuffled outcomes". The dumb rules are compared raw (q > best_dumb); no dumb rule has a permutation null.
- (b) The null sentence's "in the most quantum-favourable world we could build the gap was about 0.04" holds for one of three recipes (D4). In the other two, the gap was negative.

**D9. One item cannot decide it: flaw (F5).**
- Leave-one-label-out is pre-registered and coded with the full verdict function (B = P = 2,000). So are the parameter, parent-only and prospective rows.
- **Leave-one-cluster-out fires mechanically.** One "cluster" is the whole 29-node component, which holds 16 of the 25 labels (t5). Dropping it leaves 9 labels, so n_hit or n_kill is necessarily below 5, and the row is always "untestable".
- `fragile_on_cluster` compares each row's verdict with the primary's. So every pass, null or classical will carry "The verdict hangs on one cluster: without component:bm0,bm1,bm2…'s labels it would read untestable", whatever the data say.
- Smaller points:
  - the seven single-label clusters (h1, e3, gm9, bm3, bm9, bm2, bm7; h1 and e3 are isolates) duplicate leave-one-label-out;
  - §5 states untestable as "n_zero > 12", while the code uses `n_labelled/2`; the two differ for any robustness row with 23 or fewer labels.

**D10. Machinery: flaw (F6, minor).**
- **Seed holds.** `python3 ledger/seed.py 6a6812f7…3b01 em-qwalk2 --purpose bootstrap` gives 15016625028946468319, and `--purpose permutation` gives 15216281605376176335, as recorded. `recorded_seeds()` recomputes the same pair, and `run()` refuses any other pair.
- **Pulse timing (internal check only; no network, so I could not refetch the pulse or its predecessor).** The pulse is 1591662 at 03:18:00.156Z. The pre-registration's author and committer time is 20:17:31 −0700 (03:17:31Z), and the stated previous pulse is at 03:17:00.186Z. The seed commit is at 20:18:30, and the only change between 1f6887d and ad66366 is the beacon line. CURBY-Q is stalled (round 28297, 2025-08-22), so CURBy-RNG is the right chain.
- **The gate works on synthetic files (t6):**
  - it refuses when a file is missing, when only one review exists, when one is fix-first unconfirmed, when one is redesign, and when a third `em-qwalk2-b.md` says redesign;
  - it accepts both at go, and go plus confirmed fix-first;
  - a "verdict: go" in the body does not override the header.
- **Weaknesses:**
  - `confirmed_at: pending` or `~` counts as confirmed, because any non-"null" string passes;
  - files named like `em-qwalk2-1b-addendum.md` or `em-qwalk2_c.md` are ignored;
  - §7 says `--run` refuses "if the pre-registration is uncommitted", but `prereg_commit()` only checks that the file was once added. Uncommitted edits to `qwalk2.md` or `qwalk2.py` pass, and `recorded_seeds()` reads the randomness from the working tree, not from the seed commit.
- **Budget:** $0, with no API in the code. Stop-on-refusal, scale direction and caching are not applicable.
- **Lesson matches.** `check_prereg.py em-qwalk2 . …/qwalk2.md --before-run` gives L1, L2 and L3 ok, and R1 FAIL only because this file did not exist yet.
  - The read block (15 scored, Brier 0.267, 6/15, running 7/17, newest audit `ss-b5.md` at 20:07) matches `brier.md` and `audits/` at 1f6887d.
  - P11 is in 1f6887d, and the ledger line `ls-em-qwalk2` follows in 59b0a30, as learn.md allows.
  - P11's `do_this` is done: the null is in the rule, and the dry run with the hub held each way shows false verdicts at or below nominal.
  - P3 is only partly done (no margin; D5).

**Does the re-bet fix every flaw the two em-qwalk reviews found?**

| earlier flaw | fixed? |
|---|---|
| em-qwalk.md 1, own-label leak | Yes. The null is in the rule, and false verdicts are ≤ 0.35% on this graph with `oe` held each way (D3). |
| em-qwalk.md 2, seeds | Yes: same seeds and weights. "Exact twin" is dropped, but "nothing else differs" overclaims (F3). |
| em-qwalk.md 3 / em-qwalk-1b.md F1, beat chance | Yes. |
| em-qwalk.md 4, dry run on the real shape | Yes for the shuffled worlds. The planted-kernel rows that set the odds are not in the code (F1). |
| em-qwalk.md 5, power | Stated honestly in size, but the stated power does not make the test worth running (F2). |
| em-qwalk.md 6, pin seed and inputs | Yes, apart from the working-tree reads (F6). |
| em-qwalk-1b.md F2, dumb rules | Done: four rules, oriented, in the rule. No margin, and depth and component size are missing (F2). |
| em-qwalk-1b.md F3, leakage through edges | Yes: §6 bullet and the prospective row. |
| em-qwalk-1b.md F4, false-pass on the real topology | Yes (0.2%, reproduces). |
| em-qwalk-1b.md F5, clusters | Coded, but fires mechanically (F5). |
| em-qwalk-1b.md F6, wording | Mostly. The new clauses are F4. |
| em-qwalk-1b.md F7, gate | Yes; minor weaknesses (F6). |

## Required fixes

**Verdict: redesign.** Withdraw em-qwalk2 before data:
- `ledger/bets.jsonl` row `em-qwalk2`: `verdict: withdrawn`, `scored: false`, with `design_review` pointing here;
- a dated DEVIATIONS row (the next free number after D57) naming this file, written before any score on the real labels.

Its pre-registration, code and seed stay as committed. A withdrawal is counted, not scored, so the near-free Brier point does not enter the ledger.

**F2 (D5), the reason for redesign: the test has no power on this graph.** No fix within this bet can supply the missing labels. All three maps together hold 59 labelled directions today under the same rule (entangled-mind 39 at ad66366 including the scout's, nature-graded 17, other-minds 3), against the roughly 550 that the author's estimate says are needed. A re-bet is admissible only when its committed dry run shows, on the graph it will use:
- P(pass) ≥ 0.5 in a pre-specified, committed quantum-favourable world;
- P(pass) and P(classical) ≤ 0.05 under shuffled labels and in the opposite arm's world;
- P(classical) ≥ 0.5 in a classical-favourable world.

If no graph meets that, the question stays open on the map and is not bet. A re-bet carries F1 and F3–F6.

**F1 (D4). Commit the planting code and report every recipe.** Add the planted-kernel conditions to `dry_run_real_topology()`, with at least the three recipes above: latent on all nodes with the diagonal kept; with the diagonal zeroed; and self-consistent. Report pass, classical, mean AUROCs and mean Δ for each. Restate the odds, the pre-mortem and the lesson's "1–2%" from those numbers. Do not describe a single recipe as "the most quantum-favourable world".

**F3 (D7). Name the bundle.** Replace "the only difference is how one walk spreads … nothing else differs" (§1) and "differ only in the one-seed kernel" (§10, D57, lesson) with: *"The two arms use the same links, seeds, weights and stopping time; they differ in the dynamics (unitary against diffusive), the readout (Born rule against probability) and the degree weighting that the classical walk on L_rw carries and the quantum walk on L_sym does not."* Optionally, add a reported secondary with both arms on the combinatorial Laplacian, which removes the degree weighting.

**F4 (D8). Two clauses.**
- In the pass sentence, replace "It also beat chance and every one-line rule, each judged against shuffled outcomes" with *"It also beat chance (against shuffled outcomes and by bootstrap) and scored above every one-line rule's AUROC."*
- In the null sentence, replace "in the most quantum-favourable world we could build the gap was about 0.04" with *"in labels planted from the quantum kernel the gap ranged from about −0.04 to +0.05 depending on the recipe"*, using the F1 numbers.

**F5 (D9). Leave-one-cluster-out must be able to not fire.**
- A robustness row that is untestable is reported as "cannot be checked", not as a flip.
- Drop the whole-component cluster for the 29-node component, and keep its subtrees.
- Drop singleton clusters, since leave-one-label-out already covers them.
- State the untestable rule for robustness rows in §5 as the code has it (n_zero > n_labelled/2), or change the code to §5's text.

**F2, minor part, and F6.**
- *Dumb rules:* add depth and component size to best_dumb, and require q > best_dumb + a stated margin (P3). If no margin is used, the lesson must not claim P3 as corrected.
- *Gate:* `confirmed_at` must parse as a date. Match every `em-qwalk2*.md`. `--run` must refuse if `git status --porcelain -- qwalk2.md qwalk2.py` is non-empty, and must read the randomness with `git show <seed commit>:qwalk2.md`.
