---
bet: em-qwalk
program: entangled-mind
prereg_commit: 680f128
seed_commit: 34bad77
reviewer_session: design-review em-qwalk (fresh subagent launched by the engine session; worktree at 34bad77; no chat, transcript or author message read)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-04 20:05 America/Denver
checks: {D1: holds, D2: holds, D3: flaw, D4: flaw, D5: flaw, D6: holds (no calls; pre-mortem kind world), D7: flaw, D8: flaw, D9: holds, D10: flaw}
flaws: 6
pilot_usd: 0.00
verdict: redesign
confirmed_at: null
---

# Design review of em-qwalk

## In plain English

As built, this test would not answer its question, because both scores leak the hidden direction's own label. Each direction is scored by walks started from "all the other hits" and "all the other kills", and each set is normalised to total weight one. So a hidden hit always has one hit seed fewer than a hidden kill has. The quantum walk's coherent start makes its mass at a node grow with the number of seeds, so this leak pushes the quantum score *against* the hidden node's own label. PageRank averages over its seeds, and on a graph with a labelled hub the same leak pushes PageRank's score *towards* the hidden node's own label. Program 1's graph is mostly one hub (`oe`, degree 19, labelled hit). On a synthetic star with random labels, which carry no information at all, the frozen rule says "classical" in 200 of 200 graphs. The dry run that set the false-pass rate (2.7%) and the evidence that "neither wins by construction" used random forests with no such hub. The quantum walk's dry-run "win" on depth-alternating labels is a walk scoring below chance (median AUROC 0.37) beating a PageRank further below chance, and a constant score would have beaten PageRank by more. Repairing this changes the statistic's null, the pass rule, the seeding, the dry run, the odds and the lesson's central claim ("exact classical twin"). That is a new design, not a fix, so the bet should be withdrawn and placed again.

Disclosure: when I listed `ledger/design-reviews/` to choose my output path, the directory listing and a header-sample command showed me the header of another review of this bet, `em-qwalk-1b.md` (verdict fix-first, 7 flaws, check list). I read no further into it. Everything below comes from my own runs, and none of it was taken from that file.

## Checks

Worktree: `git worktree add .../scratchpad/review-em-qwalk 34bad77`. Every predictor run below is on graphs and labels I built. On the real graph I ran only `--graph-counts 680f128`, `build_graph` (nodes, edges, labels, components, degrees) and the parent-only edge diff. I computed no quantum or PageRank score, no AUROC and no Δ on the real graph, and I did not run `--run`. My test scripts are in the reviewer's scratchpad (`tests/t1_star.py` … `t6_power.py`). They are not committed.

**D1. A stranger can apply the rule: holds.** `verdict()` was run on eight synthetic tables: pass (Δ 0.2, [0.05, 0.35]), classical (−0.2, [−0.35, −0.05]), null (0.1, [−0.05, 0.25]), null (0, [0, 0]), untestable (n_hit 4), untestable (n_zero 13 of 25), pass at n_zero exactly 12.5 (not "more than half"), and null (Δ 0, lo 0.01). Each returned exactly one verdict, and each matches §5's text. (The last case is the right answer under "Δ > 0 and lo > 0", because Δ = 0.)

**D2. Every knob takes effect: holds.**
- `--dry-run` reproduces §4's table exactly: random labels 2.7 / 4.4 / 93.0%, width 0.246; branch-shared 0.3 / 3.5 / 96.2%, width 0.181; depth-alternating 56.3 / 0 / 43.7%, width 0.276.
- τ moves the quantum score by 0.142 and PageRank by 0.143. The two methods differ by up to 0.038 on one graph, and quantum mass sums to 1.000.
- `parent_only` drops exactly three edges on the real graph (e5–oe, g–h34, h2–h34: rule 2). Rule 3 adds **no** edge that a parent link does not already give: every `replication_of` duplicates a map parent. So the "parent links only" sensitivity differs from the primary by three edges.
- The coherent/incoherent switch changes scores.
- **Exact time average:** I checked it independently against a direct time integral (my own scaling-and-squaring matrix exponential, midpoint rule over 60τ, 6,000 steps). The error is 1.4e-6 on a random forest, on a star (a degenerate spectrum: 0, 1×7, 2) and on a 6-cycle with an isolated node. The formula is right, including degenerate eigenspaces and singletons. §2's stated Monte Carlo error "0.0024 at 4,000 draws" does not reproduce: the committed dry run prints 0.0062. That is noise in the check, not an error in the formula.
- **PageRank identity:** `classical()` matches power-iteration PageRank to 4e-16, and matches a direct quadrature of the classical walk s·exp(−t L_rw) at an exponential time to 2e-5. The PageRank-equals-exponentially-stopped-classical-walk identity holds.

**D3. Every control can fail: flaw.** The only negative control is the dry run's random-label false-pass rate, and it was measured on 7-root random forests. The real graph is a different shape: `--graph-counts` gives 41 nodes, 38 edges, 25 labels (11 hit, 14 kill) and 5 components. Inspection shows one hub `oe` of degree 19 (labelled hit) carrying 29 of the 41 nodes. The other components are a 6-node tree, a 4-node star whose only label is its centre `h5`, and two labelled singletons (`h1`, `e3`). The control was never run on graphs of this shape, and when it is, it fails:
- On a pure star (20 leaves, random labels, `t1_star.py`, 200 graphs each), the frozen rule returns **classical in 200 of 200** whether the hub is unlabelled, a hit or a kill. Mean AUROCs are quantum 0.000 / 0.023 / 0.041 and PageRank 0.500 / 0.895 / 0.912.
- On hub-shaped graphs I built (one hub with 19 spokes, 4 of them with 1–4 children, a 6-node tree, a 4-node star and two singletons; 11 hit and 14 kill placed at random; `t5_hubshape.py`, 300 graphs), it returns **classical 10.0%**, pass 2.3% and null 87.7%. The nominal rate on each side is 2.5%. Mean AUROCs are quantum 0.428 and PageRank 0.438, both below chance with no signal present.
- The run itself contains no label-permutation control that would expose this. §4 says "the hidden node's label never reaches its own score". On these graphs that is false (D4).

The same hub-shaped graphs, run in three conditions (120 graphs each, random labels; about 2,000 graphs would be needed to pin these rates down):

| condition | frozen rule: false classical | frozen rule: false pass | label-permutation rule (200 permutations): classical | label-permutation rule: pass |
|---|---|---|---|---|
| hub unlabelled | 10.8% | 1.7% | not run | not run |
| hub labelled hit (as `oe` is) | 15.0% | 0.8% | 6.7% | 0.8% |
| hub labelled kill | 5.8% | 5.0% | 1.7% | 2.5% |

A permutation null (Δ compared with its distribution under shuffled labels) moves both tails toward the nominal 2.5%. In this small test it does not obviously close the gap with the hub labelled hit (8 of 120). So the re-bet has to show its own control passing on this shape, not assume it.

**D4. Rivals are matched: flaw.** The PageRank side of the "exact classical twin" claim checks out: same graph, L_rw is similar to L_sym, the exponential stopping time is the same, and the identity holds (D2). **The seeds are not matched.**
- PageRank starts from the probability mixture s = 1/|S| on each seed. Its mass at a node is the *average* of single-seed PageRanks, which does not grow with |S|.
- The quantum walk starts from the coherent superposition 1/√|S| on each seed. Same-phase seeds add in amplitude, so the mass at a non-seed node grows roughly *in proportion to* |S|. On a star with all seeds as leaves it is exactly |S|·E|u(t)|².
- Leave-one-node-out then removes the hidden node from its own class, so |H| − |K| differs by 2 between a hidden hit and a hidden kill. The quantum score therefore carries −2·E|u|² times the hidden node's own label.
- Minimal example: a 6-leaf star, 3 hit and 3 kill leaves, hub unlabelled. Every hit leaf scores −0.0401 and every kill leaf +0.0401, so the quantum AUROC is exactly 0.000. PageRank gives every leaf 0.0, so its AUROC is 0.500.
- PageRank's own leak runs the other way: when the hub is a seed, a hidden node's removal raises the hub's weight 1/|S| in its own class. This gives PageRank AUROC 0.90 on random labels.

So the contest is decided by seed normalisation interacting with leave-one-out, and on a hub graph PageRank wins by construction. §4's D4 evidence ("on depth-alternating labels the quantum walk wins, so neither rival wins by construction") does not show what it claims. On those labels (`t2_forest.py`, 150 forests), mean AUROC is quantum 0.344, PageRank 0.195 and incoherent quantum 0.274. Among the quantum "passes", 90% have a quantum AUROC at or below 0.5, and 100% have a lower bound against chance at or below 0.5. No synthetic case was shown where PageRank wins while beating chance, or where the quantum walk does.

**D5. A dumb baseline is beaten: flaw.** The pass rule "Δ > 0 and lo > 0" does not require the quantum walk to beat chance. A **constant score** (AUROC 0.5) passes it whenever PageRank's AUROC is reliably below 0.5. On this graph's shape, leave-one-out pushes PageRank below 0.5 with no signal present (mean 0.438 on hub graphs, 0.473 on forests), and the depth-alternating case pushes it further (0.195). Among dry-run passes on structureless random labels, 60% have a quantum AUROC at or below 0.5, and 80% have a chance lower bound at or below 0.5. §5's pass sentence ("ranked the directions that were later killed below those that hit better than PageRank did") would then be false. The phase-bit and neighbour-vote baselines are reported but cannot block a pass. Note also that a strongly anti-predictive baseline (neighbour vote on alternating labels has AUROC ≈ 0) "does not match or beat" under §4's wording, although it is perfectly informative. Power: this is not a "no difference" rule, so no equivalence margin is needed, but see D8 for the stated visible gap.

**D6. Execution risks piloted: holds (not applicable).** No API, no hardware. The imports are argparse, json, os, re, subprocess (git only), sys and numpy. The pre-mortem is of kind `world`. `--graph-counts` and `build_graph` ran on the real inputs without error, and isolated nodes are handled (they score exact zeros).

**D7. Comparisons match: flaw.** The differences between the two arms are:
1. stochastic against unitary dynamics (the named factor);
2. L_rw against L_sym (similar matrices; fine);
3. a probability-mixture start against a coherent equal-amplitude start, which brings the seed-count scaling of D4;
4. stationary weight ∝ degree against a zero mode ∝ √degree, which follows from (1) and (2).

Item 3 is not "interference" in the sense the claim uses ("if the quantum walk wins, it wins by interference, not by a different graph or a longer walk"). Combined with leave-one-out, it lets the hidden node's own label into its score. The incoherent-seed secondary is the matched arm for item 3, but it is not the primary. Either the seeding is matched, or the claim must be about the bundle (unitary dynamics *and* coherent count-scaled seeding), and §1, §5 and the lesson's "exact classical twin (same generator, seeds, stopping time)" must say so.

**D8. Verdict sentences: flaw.**
- (a) The pass sentence asserts that the quantum walk "ranked … killed below those that hit". Under the frozen rule this can be true of a below-chance walk (D5).
- (b) The null sentence and §1/§6 say the test "could only have seen a gap of about 0.12 or more". 0.12 is half the median 95% width, which is the gap detected about half the time, not reliably. In a power simulation using the frozen `boot_diff` at n = 11/14 (`t6_power.py`, correlated latent scores, median width 0.28), a true gap of 0.119 passes 41% of the time and 0.169 passes 68%. Scaled to the dry run's width of 0.246, the 80%-power gap is about 1.43 × 0.123 ≈ 0.18. The sentence must give that number.

**D9. One item cannot decide it: holds.** Leave-one-label-out is pre-registered (§4) and coded (`run()`, each label removed from both seeding and scoring, verdict recomputed). §5 states the consequence: the verdict stands but is reported as fragile, hanging on the named node.

**D10. Machinery: flaw.**
- The seed recomputes: `python3 ledger/seed.py a7ee3f40…a771 em-qwalk --purpose bootstrap` gives 16001949444733414920, as recorded.
- The pulse time (02:47:00.160Z) is after the pre-registration's author and committer time (19:46:46 −0700 = 02:46:46Z), and the recorded previous pulse (02:46:00.253Z) predates it. I could not refetch the pulse (no network), so the randomness value and the "first pulse" claim are checked only internally.
- CURBY-Q was stalled for more than 24 hours, so CURBy-RNG is the right chain under the hardware.md rule.
- The lesson matches: `check_prereg.py em-qwalk . …/qwalk.md --before-run` gives L1, L2 and L3 ok, and R1 fails only because this file did not exist yet.
- The budget is $0 and the code contains no API. Stop-on-refusal, the scale and caching do not apply.
- The run gate works on synthetic review files (`t4_gate.py`): missing → refuse; go → run; fix-first with `confirmed_at: null` → refuse; fix-first confirmed → run; redesign → refuse; "verdict: go" outside the header → refuse; a review saved only as `em-qwalk-b.md` → refuse.
- **Flaw:** §7 says `--run` refuses "without the CURBy seed", but the code refuses only when `--seed` is missing. It accepts any integer, so a seed could be re-drawn. It also accepts any `<commit>` for the inputs, although §2 freezes them at 680f128. hardware.md E23 requires "the split in the code uses that seed and no other".

**Label and edge rules applied as written: hold.** I checked by inspection against §2.
- **Nodes:** 41, which is all directions minus `qwalk`. §2 expected about 36, but the rule is mechanical.
- **Rule 2:** h2–h34 (15:14), g–h34 (19:27) and e5–oe (22:24). These are the only shared HH:MM times among phase-A `record.md` sources. Open nodes with gold-map or biomimetic-map sources are correctly excluded.
- **Rule 3:** gm2b, gm3c, bm0, dm2, dm3 and dm4 join their targets. All of these duplicate parent links.
- **Labels:** 13 phase-A nodes give 4 hits and 8 kills, with e4 `mixed` left unlabelled. 12 bet nodes are labelled, and the 6 bets that are mixed or undetermined are left unlabelled. The labelled nodes are h1 1, h2 0, h34 0, h5 1, g 1, v2 0, v21 0, son 0, e3 0, e4r3 0, e5 0, oe 1, gm9 1, gm2 1, gm2b 1, gm3 1 (via em-gm3b), gm3a 0, gm1 0, dm3 0, bm1 1, bm0 1, bm3 0, bm9 1, bm2 0, bm7 0. This is consistent with §2's rules.
- Three labelled nodes (h1, e3 and h5) cannot be reached by any seed, so n_zero is at least 3, well under the untestable threshold.

## Required fixes (redesign: withdraw em-qwalk before data; re-bet with a new pre-registration and a new lesson)

1. **Remove the own-label leak (D3, D4).** Replace or supplement the bootstrap with a **label-permutation null on the frozen graph**: permute the 25 labels with counts fixed, recompute the leave-one-node-out scores of both methods, and take ≥ 2,000 permutations with the CURBy seed. Pass only if Δ is above the permutation null's 97.5th percentile, *and* the bootstrap lower end is above 0. Alternatively, use a seeding under which a hidden node's score provably does not depend on its own label. Either way, show in the dry run that on a synthetic star and on hub-shaped graphs with random labels (hub labelled hit, labelled kill, and unlabelled), both verdict tails are at or below 2.5% within simulation error, with at least 1,000 graphs per condition. My permutation version got the hub-labelled-hit classical tail only to 6.7% (8 of 120), so this must be shown, not assumed.
2. **Match the seeds (D4, D7).** Either make the primary quantum arm's seeding the matched twin of PageRank's mixture (the incoherent-seed walk is one option), or keep the coherent seeding and rewrite §1, §5 and the lesson as a claim about the bundle (unitary dynamics plus coherent, count-scaled seeding). Drop "exact classical twin (same generator, seeds, stopping time)" unless a synthetic star shows both methods give automorphic leaves equal scores whatever the seed counts.
3. **The winner must beat chance (D5).** Pass also requires the quantum walk's AUROC to beat chance, with a lower end above 0.5 against the permutation null of fix 1, not against a constant. "Classical" likewise requires PageRank to beat chance, and every other case is null. State that a baseline whose AUROC is at or below 0.5 is scored by max(AUROC, 1 − AUROC) when it is compared, or say why not.
4. **Re-run the dry run on graphs of the real shape (D3, D4).** Use one hub of degree about 19 with short branches, a few small components and labelled singletons, with 11/14 labels. Report the false-pass and false-classical rates under the new rule. For D4, show one synthetic label structure where each method wins *while beating chance*. Re-derive the odds from these numbers.
5. **State the real power (D8).** Replace "a gap of about 0.12 or more" in §1, §5 and §6 and in the lesson with the 80%-power gap from the new dry run (about 0.18 under the current interval). Have the code print 1.43 × the observed half-width for the null sentence.
6. **Pin the seed and the inputs in code (D10).** `--run` refuses unless `<commit>` equals the pre-registration commit and `--seed` equals the recorded CURBy seed. Ideally it recomputes the seed with `ledger/seed.py` from the randomness recorded in §2.

Ledger: `ledger/bets.jsonl` row `em-qwalk` gets `verdict: withdrawn`, `design_review: {"path": "ledger/design-reviews/em-qwalk.md", "verdict": "redesign", …}`. A DEVIATIONS row in `programs/entangled-mind/DEVIATIONS.md` records the withdrawal before any data, and the re-bet gets a new id, a new lesson line and a new seed.
