---
bet: em-qwalk
program: entangled-mind
prereg_commit: 680f128
seed_commit: 34bad77
reviewer_session: design-review em-qwalk, second reviewer "1b" (fresh subagent launched by the engine session; no chat, transcript or author message read; output path em-qwalk-1b.md at the coordinator's instruction, the stricter of the two reviews binds)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-04 19:55 America/Denver
checks: {D1: holds, D2: holds, D3: flaw, D4: flaw, D5: flaw, D6: holds (no calls; no execution risk), D7: flaw, D8: flaw, D9: flaw, D10: flaw, E23: holds (internal; pulse not refetched, no network), E25: flaw (P3 not done as its do_this asks; P1's stated reason for raising odds is void; P9 nouns), rule-6 revival: holds (not a revival), hardware/quantum-advantage: holds}
flaws: 7
pilot_usd: 0.00
verdict: fix-first
confirmed_at: null
---

# Design review of em-qwalk (reviewer 1b)

## In plain English

As built, this test could have come back a "pass" when the simulated quantum walk was **worse than a coin**. It was enough for the walk to be less wrong than PageRank. That is what happens in the author's own dry-run case where "the quantum walk wins" (labels alternating with depth). There the walk's average AUROC is 0.34 and PageRank's is 0.20, so both rank the settled directions backwards, and a one-line rule ("the opposite of your neighbours") scores 0.96. The same thing happens on program 1's real graph. I gave it made-up labels in which directions that grew children count as hits, which is how research trees tend to look. The frozen rule passed the quantum walk 33% of the time with both walks below chance, while "count the node's children" scored 0.89. On the real graph with shuffled labels, the false-pass rate is about 4.3%, not the 2.7% measured on synthetic forests. The question itself is fine: it is not a revival of program 1's error-prediction encoding, and it claims no quantum advantage. The fixes are these:
- require the walk to beat chance and every one-bit or degree rule before a pass counts;
- add the leave-one-cluster-out check;
- fix the gate in the code;
- reword the verdict sentences;
- restate the odds, because the route to a pass that the odds rested on was the artefact.
With the tightened rule, shuffled labels pass 0.2% of the time, and one realistic made-up pattern ("hits sit near the root") still passes 2%. So the test stays fair and possible to pass.

## Scope note

The engine's brief described this bet as predicting "which claims the model gets wrong" on a claim/contradiction graph. The pre-registration does something else. Its nodes are program 1's **research directions** (`map/entangled-mind.json`), its edges are parent, same-record-row and ledger links, and its labels are bet outcomes (hit or killed). No model answer, claim web or circuit is used. I reviewed the pre-registration as written. That difference is the reason the rule-6 check holds (below), and the reason "claim graph" is the wrong noun (F6).

## What I ran (all $0, no network, real labels never used)

Scripts are in `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/19f84df9-a6ff-48ba-89d6-d3f43e5d1747/scratchpad/rev/`. Each one loads the author's `qwalk.py` as a module and builds the real graph at 680f128. Each keeps only the **set** of labelled node ids, deletes the label dict before any computation, and then assigns random or structure-made labels. The real primary statistic was never computed.
- `qwalk.py --graph-counts 680f128`: 41 nodes, 38 edges, 25 labelled (11 hit, 14 kill), 5 components.
- `qwalk.py --dry-run`: reproduces the pre-registration's §4 table exactly (random 2.7% / 4.4% / 93.0%; branch-shared 0.3% / 3.5% / 96.2%; depth-alternating 56.3% pass). One small mismatch: the exact-against-Monte-Carlo error prints 0.0062 at 4,000 draws, not the 0.0024 in §2. The run is deterministic, so the §2 figure is stale. This is cosmetic.
- `graphshape.py` (structure only): components are {h1}; {h2, h34, g, v2, v21, son} (6 labelled, nothing else); {h5, gm7, gm8, gm11} (1 labelled); {e3}; and a 29-node component (16 labelled). That last one contains a hub, `oe`, with 19 neighbours. Its 3 non-parent edges (e5–oe, g–h34, h2–h34) all come from rule 2. Every ledger link either duplicates a map parent edge or points to a bet with no node. Two labelled nodes are isolates (h1, e3), and 8 of the 25 labelled nodes have children.
- `probe.py`, `probe2.py`, `probe3.py` (verdict rates under random and structured synthetic labels, on the real topology and on synthetic forests); `probe4.py`, `probe5.py` (knobs, `verdict()` cases, star localisation).

## Checks

**D1. A stranger can apply the rule. Holds.** I fed `verdict()` six synthetic tables: pass; lo exactly 0 (null); classical; Δ = 0 (null); n_hit < 5 (untestable); n_zero > half (untestable). It returned exactly one verdict each time, matching §5. The §5.5 "dumb baseline" sentence is ambiguous about direction (see F2).

**D2. Every manipulation takes effect. Holds.**
- The parameters the run will use are ALPHA 0.85, TAU 5.667, B 10,000 and ROUND 12, which match §2 and §4.
- τ moves both predictors (0.142 and 0.143), the two walks differ (0.038), and the PageRank identity holds to 5.6e-17.
- Quantum mass is 1 at every α in the sensitivity grid. The parent-only graph drops 3 edges (38 to 35).
- Coherent and incoherent seeding differ (0.0025) when the seeds share a component. (They are identical, 8e-17, when the seeds sit in different components, as they should be.)
- Every free choice is frozen in code before the labels: L_sym as the Hamiltonian, equal real positive seed amplitudes, the exponential stopping time, and α fixed at 0.85 with τ tied to it. I found no free t and no tunable node encoding.
- Context, not a flaw: on a star, the quantum walk keeps 90% of a leaf seed's mass on that leaf, against PageRank's 17%. The real graph's 19-neighbour hub `oe` makes this the dominant difference between the two walks there.

**D3. Every control can fail. Flaw (F4).** The PageRank identity check fails for a mismatched τ, so that control is sound. The stated false-pass rate is the problem. It was measured on random recursive forests: maximum degree about 5, no isolates, no 6-node all-labelled island. On the real topology with 11/14 labels placed at random, the frozen rule passes 15/400, 29/600 and 24/600 across three seeds, which is 68/1600 ≈ 4.3% against a nominal 2.5%. The 2.7% in §4 and in the lesson does not describe this graph.

**D4. Rivals are matched. Flaw (F1).**
- PageRank is the right classical twin: it is the exponentially stopped heat kernel of L_rw, which is similar to L_sym. A fixed-time heat kernel would be a worse match, because the quantum side is also averaged over the exponential time.
- What fails is the claim that "neither wins by construction". The pre-registration's only evidence that the quantum walk can win is the depth-alternating condition, and there both walks are below chance:

| condition (synthetic labels) | frozen rule: pass | mean AUROC quantum | mean AUROC PageRank | best oriented one-bit/degree rule |
|---|---|---|---|---|
| forests, depth-alternating | 60.5% | 0.336 | 0.199 | neighbour vote reversed, 0.955 |
| real topology, hit iff has a child (10% flip) | 33–39% | 0.364 | 0.244 | child count 0.889, degree 0.872 |
| real topology, hit iff leaf (10% flip) | 36.5% | 0.351 | 0.232 | child count 0.889 |
| real topology, random 11/14 | 4.0–4.8% | 0.471 | 0.479 | 0.59–0.62 (selection noise) |
| real topology, homophily on parent links | 0% | 0.830 | 0.826 | neighbour vote 0.818 |
| real topology, shared within component | 0.5% | 0.796 | 0.792 | neighbour vote 0.781 |
| real topology, hit iff depth ≤ 1 | 8.5% | 0.729 | 0.699 | (see below) |

- Among frozen-rule passes, the quantum walk's AUROC was below 0.5 in 53 of 74 (has-a-child labels) and in 14 of 29 (random labels).
- The rule, as frozen, rewards being less anti-predictive. On anti-homophilous structure (parity, parent and leaf), diffusion is strongly wrong and the quantum walk, which stays near its seeds, is less wrong.
- No condition I tried makes PageRank win. Where labels follow the links (homophily, components), the two tie.

**D5. A dumb baseline is beaten. Flaw (F2).**
- The phase bit and the neighbour vote are pre-registered, but only as a reported sentence, not in the rule. That is P3's failure mode: its do_this says "make the rule 'beat it by a margin'".
- Both baselines are compared raw. A rule with AUROC 0.05 is as informative as one at 0.95, and on the parity case the raw neighbour vote is 0.045 and is never flagged.
- Degree and child count are missing. They are the dumbest predictors on a research tree, and on the realistic has-a-child structure they score 0.87–0.89.
- The null-side check holds: §5.4 states the smallest visible gap (half the interval width, filled at run time). This is not a "no difference" pass rule, so P2's margin requirement is met by the stated minimum detectable effect.

**D6. Execution risks are piloted. Holds.** There are no API calls, no hardware and no refusal-prone content, and the pre-mortem is of kind `world`. No pilot is needed.

**D7. Comparisons match. Flaw (F3), on leakage (auditor B8/B12).**
- Within the quantum-against-PageRank comparison, the conditions are matched: same graph, seeds, stopping time and scoring. The remaining differences are unitary against diffusive dynamics, coherent seeding with a fixed positive phase, and the Born-rule readout. The incoherent-seed secondary separates seeding from path interference. That part of P8 is done.
- The graph is the problem. It is not independent of the labels. A direction's children (gm2b and dm4 under gm2, dm2 and gm3c under gm3, dm3 under gm1, bm0 under bm1, and the phase-A children) were opened after, and largely because of, the parent's outcome: replications follow passes, and follow-ups follow interesting results.
- So the edges carry outcome information. That is circular for a claim worded as prediction ("which were going to fail", "later killed").
- No edge is built by the judge whose errors are predicted, because no model's errors are predicted here.
- The contamination is confirmed by the has-a-child rows in the D4 table: on outcome-shaped edges both walks go below chance, and the frozen rule still passes.

**D8. Verdict sentences are written. Flaw (F6).** The §5 sentences exist, but the pass sentence uses nouns the design cannot carry:
- "claim graph": the nodes are research directions, and "claim" collides with program 1's closed claim web.
- "later killed": the edges partly postdate the outcomes, and each score uses every other outcome.
- "no hardware ... would help": untested.
- "its exact classical twin": acceptable as "matched", but "exact" overstates it given the seeding and readout differences.
- The sentences carry no other "quantum" wording beyond the simulated walk, and none says "advantage". §6 rules out "every", "all" and "quantum advantage".

**D9. One item cannot decide it. Flaw (F5).**
- Leave-one-label-out is pre-registered, and so is its consequence ("fragile, hanging on <node>"). That part holds.
- Leave-one-cluster-out is not pre-registered. The graph has one 6-node island, {h2, h34, g, v2, v21, son}, that is entirely labelled. These are program 1's quantum-against-classical directions, and they score only off each other.
- On random labels on the real topology, every frozen-rule pass (29 of 29) was fragile by leave-one-label-out, and 27 of 29 flipped when one component's labels were dropped.
- So at this n, "fragile" is the expected state of any pass, and §5 should say so.

**D10. Machinery. Flaw (F7).**
- These parts hold:
  - The code has no network or API import (only argparse, json, os, re, subprocess for `git show`, sys and numpy).
  - Budget, stop-on-refusal and scale direction are not applicable.
  - The inputs are read at the pre-registration commit.
  - `--run` refuses without `--seed`.
  - The lesson is present and matches: `check_prereg.py`'s L1–L3 pass, and R1 fails only because no `em-qwalk.md` exists yet.
- The flaw: `review_says_go()` reads only `ledger/design-reviews/em-qwalk.md`. There are two reviews, and the stricter one binds, so the code would let `--run` through on the other review's go even with this one at fix-first.

**E23. Seed. Holds, from the record.**
- §2 records CURBY-Q round 28297 (2025-08-22), so the chain is stalled by the 24-hour rule, and CURBy-RNG was named correctly.
- The pulse is 1591631 at 2026-11-05T02:47:00.160Z. The pre-registration author time is 19:46:46 −07:00 (02:46:46Z), and the previous pulse, 1591630 at 02:46:00.253Z, predates it.
- `python3 ledger/seed.py a7ee…a771 em-qwalk --purpose bootstrap` gives 16001949444733414920, matching the record.
- The code passes the seed only to `default_rng` for the bootstrap (seed+1 for the chance intervals). The analysis is otherwise deterministic, and `results/qwalk.json` does not exist.
- Cannot check: I could not refetch pulses 1591630 and 1591631 (no network) to confirm they are the first after the commit and that the randomness matches.

**E25. Lesson. Flaw (covered by F1, F2, F6).** The read block matches the ledger at 680f128: 14 scored, Brier 0.246 (`brier.md`), 5/14, running 6/16 = 0.375, and `ss-b1.md` as the newest audit (cdce1ba, 19:13). Pattern by pattern:
- **P1** (odds from the base rate, moved for a named reason): the move to 0.125 for the reference class and then down is reasoned. The stated reason for raising 0.04 to 0.05 ("a label pattern where the quantum walk wins 56%") is the below-chance artefact of F1, so it is void. The odds must be restated before data.
- **P3** (beat the dumbest predictor by a margin): not done. The baselines are reported only, compared raw, and degree and child count are missing (F2).
- **P8** (list every difference): done within the walk comparison. The leakage is a separate issue (F3).
- **P2** (state the minimum detectable effect): done.
- **P9** (sentences in §5): written, with wrong nouns (F6).
- **P10** (leave-one-out and its consequence): done, and extended by F5.

**Rule 6 (no revival of the quantum error-prediction encoding). Holds.** That encoding put one model's competing claims on qubits to flag its wrong answers. This bet:
- uses no model output, claim web or circuit;
- predicts outcomes of the research record, not model errors;
- uses a walk on a graph of directions, not a learned encoding.
The six error-prediction directions appear only as labelled nodes, which reads the record and does not reopen it.

**Hardware and quantum advantage. Holds.** The bet is laptop numpy only, with 0 QPU s and no chip. It claims no quantum advantage, and §6 forbids the phrase. Only the "would help" clause overreaches (F6).

## Required fixes

All of these go in **one dated DEVIATIONS row** (the next free number, D56 if unused), written before any data, naming `ledger/design-reviews/em-qwalk-1b.md`. Each fix tightens the rule or adds a report. None lowers the bar.

**F1 (D4). A pass must beat chance.** In `verdict()`:
- read pass as: `diff > 0 and lo > 0 and q_chance_lo > 0.5 and auroc_quantum > best_dumb` (F2);
- read classical symmetrically: `diff < 0 and hi < 0 and p_chance_lo > 0.5 and auroc_pagerank > best_dumb`;
- anything else that is not untestable is null;
- use the same function inside leave-one-label-out and leave-one-cluster-out.

`q_chance_lo` is the lower end of the existing stratified-bootstrap chance interval for the quantum walk, as §4 secondary 1 already computes it; `p_chance_lo` is the same for PageRank.

Add to §5.4 the sentence: *"The simulated quantum-walk score beat PageRank (Δ [lo, hi]) only by being less wrong: it did not beat chance, or <rule> (AUROC x) did as well, so by the rule it does not count."*

Re-run the dry run under the new rule, adding the real topology with shuffled labels, and report it in the row. My figures: shuffled labels 0.2% pass (1/600); has-a-child 0%; depth-alternating 0%; hit-iff-depth ≤ 1 2.0%.

Restate the odds as a revision before data, keeping 0.04, 0.07 and 0.05 on record. The reason given for 0.05 is void, and under the tightened rule the best route to a pass I found is 2%. I recommend 0.04 or lower; the number is the author's to state.

**F2 (D5, P3). Oriented dumb baselines, inside the rule.** Add **degree** and **child count** (number of map directions whose `parent` is the node) to the phase bit and the neighbour vote. Define `best_dumb` as the maximum over these four of max(AUROC, 1 − AUROC). Report each raw and oriented. Rewrite §5.5's dumb-baseline sentence to quote the oriented AUROC and the orientation.

**F3 (D7/B8). State the leakage and add a prospective sensitivity.**
- Add a §6 bullet: *"Many links were made after, and because of, the outcomes they connect (replications and follow-ups open under hits). So the graph is a record of the outcomes as much as a predictor of them."*
- Add a reported, never-promoted sensitivity, "prospective": when scoring hidden node i, delete i's edges to its own descendants (map directions with i as an ancestor via `parent`) and to nodes whose bets cite i's bet in `replication_of` or `rebet_of`.
- Report Δ, the CI and the verdict under it, beside the parent-links-only sensitivity.

**F4 (D3). Correct the stated false-pass rate.** In the DEVIATIONS row, state that the frozen rule's false-pass rate on the real topology with shuffled labels is about 4.3% (68/1600, three seeds). The 2.7% was measured on synthetic forests. Give the new rule's figure from F1's re-run. Fix the stale Monte Carlo figure as well (0.0062 at 4,000 draws, not 0.0024).

**F5 (D9). Leave-one-cluster-out.**
- Add a reported robustness check: drop all labels in one cluster and recompute with the full verdict function. The clusters are each connected component with at least one label, and each subtree hanging off `oe` in the 29-node component.
- Any verdict change adds: *"The verdict hangs on one cluster: without <cluster>'s labels it would read <verdict>."*
- Add to §5.5: *"With 25 labels, a pass is expected to be fragile: on shuffled labels every pass hung on one direction."*

**F6 (D8, P9). Pass sentence, exact replacement.**

*"On program 1's direction graph (N research directions linked by parent, same-run and ledger links; n settled), a simulated quantum-walk score separated the settled directions that were killed from those that hit better than PageRank did on the same links, seeds and stopping time, by Δ [lo, hi] in AUROC, and it also beat chance and every one-bit and degree rule. Many links were recorded after the outcomes, so this is a pattern in the record, not a forecast. This is one graph from one program: pass, unreplicated. It does not say the ideas are quantum or entangled, and no hardware was used."*

In the classical and null sentences, write "program 1's direction graph" wherever "claim graph" appears, and "separated" for "ranked … below".

**F7 (D10). The review gate reads both reviews.** `review_says_go()` must require every file matching `ledger/design-reviews/em-qwalk*.md` (at least `em-qwalk.md` and `em-qwalk-1b.md`) to be go, or fix-first with `confirmed_at` set, and must refuse if either file is missing.

When the DEVIATIONS row and the code changes are committed, I confirm them in an addendum to this file and set `confirmed_at`. Until then, `--run` must not start.
