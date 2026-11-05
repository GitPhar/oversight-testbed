# qwalk: can a quantum walk over program 1's ideas tell its failures from its hits? Not testable yet

**Audited:** `ledger/audits/em-qwalk.md` (9c9c139; plant pl-005 clean): the withdrawal and "untestable at this scale" stand; its 8 cuts are applied (D59).

**Laptop minutes only: no quantum hardware, no QPU seconds, no API calls, $0.** Every quantum walk here was a numpy simulation on a laptop. Bets em-qwalk and em-qwalk2, direction `qwalk`, Sean's steer st-13. Both bets were withdrawn before data. Neither is scored.

**This is not program 1's quantum error-prediction encoding, and it does not revive it** (CONTEXT §3 rule 6). That encoding put a language model's competing claims on qubits to flag the model's wrong answers, and it stays closed. This question was about the research record: whether the links between program 1's research directions carry a signal about which directions were killed and which hit. It used no model answer, claim web or circuit.

## In plain English

Sean asked (steer st-13) whether program 1's ideas, treated as a connected quantum system, could tell which of them were going to fail, better than ordinary link-ranking can. Quantum would count only if it beat the classical method. Beating chance would not count.

We built the cheapest test we could. It took program 1's 41 research directions as points and their 38 links as connections (each direction to the one it grew out of, plus shared data runs). 25 of the directions have a settled outcome: 11 hits and 14 kills. We hide one settled direction at a time, let a simulated quantum walk and PageRank spread outward from the others, and ask which method better separates the hidden kills from the hidden hits.

**Two versions of that test were designed. Independent reviewers stopped both before any outcome was looked at.**

1. **The first version (em-qwalk) leaked.** Hiding one direction changed how many hits or kills were left to start the walks from. That alone made each method's score lean toward or away from the hidden direction's own outcome. On a simple star-shaped graph with outcomes assigned at random, it declared PageRank the winner 200 times out of 200. A second reviewer found it could also pass a quantum walk that was worse than a coin, as long as PageRank was even worse.
2. **The second version (em-qwalk2) fixed both problems.** Both methods were started the same way. Every verdict was judged against the same graph with the outcomes shuffled at random, so the leak is carried by the shuffled outcomes and cancels on average. The quantum walk also had to beat chance and four simple one-line rules. Under random outcomes it now gave a false verdict at most 0.4% of the time.

   But the reviewer then showed that it could not answer the question either. The graph is too small. With 25 settled directions, the quantum walk would need to beat PageRank by about 0.15 in AUROC just to clear the shuffled-outcome bar. We built made-up worlds where the outcomes were generated from the quantum walk's own kernel. In the recipe the author chose, the quantum walk beat PageRank by only about 0.04 and the test passed at most about 4% of the time. In the reviewer's other recipes PageRank came out ahead. In worlds built to favour PageRank, it declared PageRank the winner at most 5% of the time. In every world anyone built from a model of how the outcomes might arise, the test would have said "not detectably different" at least 95% of the time; only labellings searched for the purpose passed. A result known in advance is not a test, and scoring it at 1% would have improved the engine's calibration score for free. So it was withdrawn too.

**What this says.** On the record we have, no test of this design could tell a quantum walk from PageRank; neither was ever scored on the real outcomes. The two methods differ mainly in how they spread from each starting point. On a graph of 41 points, mostly one hub with short branches, that difference is too small to show through 25 outcomes. As a rough estimate, a fair test needs roughly 550 settled directions. The reviewer counted 59 labelled directions across all maps today, 14 of them the biomimicry scout's reading-stage labels that em-qwalk2 set aside as not tested outcomes. **This does not say Sean's idea is wrong. It says one program's record is far too small to test it.** The idea is parked, not killed, and §5 says exactly what would reopen it.

**What it produced anyway:**
- Two new pattern lines for the engine's lesson file: P11, a leave-one-out score can leak the hidden item's own label; and P12, a bet that cannot pass or cannot fail at the available size buys calibration without information.
- A new design-review check that enforces P12 (D11, added by the engine session in 41a687d).
- A reviewed harness (`experiments/qwalk2.py`), pinned to program 1's graph at 680f128; a future bet would need the D58 (a)–(i) changes before reusing it.

## 1. What was asked, and the rule a pass needed

The odds event (map/entangled-mind.json, `qwalk`): a continuous-time quantum walk on program 1's direction graph, scored leave-one-node-out, separates killed from hit directions with a higher AUROC than personalised PageRank on the same graph and seeds, by a bootstrap 95% interval whose lower end is above 0. Beating chance alone does not count.

| | em-qwalk (680f128) | em-qwalk2 (1f6887d) |
|---|---|---|
| graph | 41 nodes, 38 edges, 25 settled (11 hit, 14 kill), 5 components; hub `oe` with 19 neighbours | the same, inputs pinned at 680f128 |
| seeding | coherent superposition of the hit (or kill) seeds against PageRank's average | the same one-seed walks for both arms, summed with weights centred on the others' hit rate |
| pass rule | Δ AUROC > 0, bootstrap lower end > 0 | that, plus Δ above a 10,000-shuffle permutation null, quantum AUROC above its null and with bootstrap lower end > 0.5, and above four oriented one-line rules |
| engine odds | map 0.04; fresh v1 re-elicitation 0.07; 0.05 at pre-registration | 0.01 |
| human odds | none (no line in ledger/human-odds.jsonl) | none |
| design reviews | redesign (6635276); fix-first, 7 flaws (3244dbb) | redesign (efb4920, disclosure 0417646); fix-first, 3 flaws (04e7f81) |
| outcome | withdrawn before data (D56) | withdrawn before data (D58) |

No score, AUROC, Δ or verdict was ever computed on the real outcomes. Every number below comes from synthetic outcomes, or from the real links with the outcome values discarded (only the counts 11 and 14 kept).

## 2. Why em-qwalk was withdrawn

| finding | number | source |
|---|---|---|
| own-label leak: star, random outcomes, frozen rule says "classical" | 200 of 200 graphs | ledger/design-reviews/em-qwalk.md |
| below-chance pass: the frozen rule passes a quantum walk with AUROC under 0.5 (depth-alternating outcomes) | about 57% of synthetic forests pass, mean AUROC 0.33 against PageRank's 0.20 | `qwalk2.py --dry-run` does not run this; `qwalk.py --dry-run` (680f128) gives 56.3%; em-qwalk-1b.md gives 60.5% |
| false-pass rate of the frozen rule on the real links with shuffled outcomes | about 4%: 4.3% (68 of 1,600 runs) | em-qwalk-1b.md D3. The author's own check gave 3.8% of 600, from uncommitted work-in-progress code, so it cannot be regenerated from the record. |

## 3. Why em-qwalk2 was withdrawn

The permutation null depends only on the graph and the counts 11/14, never on which directions hit. So the bar a pass must clear is known in advance:

| quantity (10,000 shuffles per seed; `qwalk2.py --null-thresholds 680f128`) | value |
|---|---|
| Δ must exceed the null's 97.5th percentile | 0.149 (32 of 40 seeds; 0.143–0.156 across seeds; the audit found 0.149 in 34 of 40) |
| quantum AUROC must exceed its null's 97.5th percentile | 0.779–0.792 across seeds (median 0.786; the audit: 0.779–0.786) |
| null mean AUROC, quantum / PageRank (the leak shows as a mean below 0.5) | 0.476 / 0.484 (medians over 40 seeds) |
| gap the bootstrap sees with 80% power (median, shuffled real-link runs) | about 0.19 AUROC |

How often the full em-qwalk2 rule says pass or classical (`qwalk2.py --dry-run`, `--dry-run-real-topology 680f128` and `--dry-run-planted 680f128`; B = P = 500):

| outcomes | runs | pass | classical | mean AUROC quantum / PageRank |
|---|---|---|---|---|
| real links, shuffled | 1,000 | 0.2% | 0% | 0.483 / 0.493 |
| real links, shuffled, `oe` held hit | 1,000 | 0.4% | 0% | 0.481 / 0.487 |
| real links, shuffled, `oe` held kill | 1,000 | 0.1% | 0% | 0.476 / 0.484 |
| hub-shaped synthetic graphs, random, hub hit / kill / unlabelled | 1,000 each | 0.2% / 0% / 0.1% | 0% each | about 0.46 / 0.46 |
| planted from the quantum kernel (random field) | 200 | 2% (1% with 10% flipped) | 0% | 0.789 / 0.751 |
| planted from the classical kernel (random field) | 200 | 0.5% (1%) | 0% | 0.749 / 0.744 |
| planted from the quantum kernel (3 sources) | 200 | 0% (0%) | 0% | 0.881 / 0.853 |
| planted from the classical kernel (3 sources) | 200 | 0% (0%) | 4.0% (0.5%) | 0.675 / 0.690 |
| other recipes, by the two reviewers | — | at most 4.3% | at most 5% | quantum-minus-PageRank gap between about −0.04 and +0.05 |

In the author's quantum-kernel field world the arms separate by about 0.04 AUROC (0.789 − 0.751); other recipes give between about −0.04 and +0.05. The bootstrap condition alone sees about 0.19 at 80% power; the full rule, which also needs the quantum AUROC above about 0.78 and above every one-line rule, sees less. The rough size needed is 25 × (0.19 / 0.04)² ≈ 564, roughly 550 settled directions. That is an order-of-magnitude estimate, not a computed power, and other recipes give smaller or reversed gaps.

## 4. What the pre-mortems said

- **em-qwalk:** "If this fails, the most likely reason is that program 1's labels cluster by branch (whole subtrees killed together), where the dry run shows both walks rank alike, so the gap sits inside the ±0.12 interval." Kind `world`. It never ran. The design was withdrawn for a reason it did not name: the leave-one-out leak, a design failure.
- **em-qwalk2:** "If this fails, the most likely reason is that on 25 labels the two one-seed kernels rank directions almost alike (planted quantum-kernel labels separate them by about 0.04 AUROC), far below the 0.19 the test can see." Kind `design`. The design review withdrew it for this reason.

Neither is scored, because neither bet ran. They are recorded for the auditor.

## 5. What would reopen it

From DEVIATIONS D58, all before data:
- a committed dry run showing P(pass) ≥ 0.5 in a pre-specified quantum-favourable world, P(classical) ≥ 0.5 in a classical-favourable one, and both false verdicts ≤ 0.05 under shuffled outcomes and in the opposite arm's world (design-review check D11 now asks for at least 10% each way);
- every planting recipe committed;
- the arms described as a bundle (interference, the classical walk's degree weighting, Born-rule against probability readout), or a matched secondary added;
- the remaining wording, cluster, dumb-rule, gate and pinning fixes listed in D58.

The likeliest way there is a much larger record: the testbed's ledger across all programs, once it holds several hundred settled directions.

## 6. Reproduce

All $0, laptop, no network:

```
python3 programs/entangled-mind/experiments/qwalk.py --dry-run                       # at 680f128: em-qwalk's synthetic table
python3 programs/entangled-mind/experiments/qwalk2.py --dry-run                      # stars and hub graphs
python3 programs/entangled-mind/experiments/qwalk2.py --dry-run-real-topology 680f128
python3 programs/entangled-mind/experiments/qwalk2.py --dry-run-planted 680f128
python3 programs/entangled-mind/experiments/qwalk2.py --null-thresholds 680f128     # §3's first table (D59)
python3 programs/entangled-mind/experiments/qwalk2.py --graph-counts 680f128
```

`--run` refuses: both bets are withdrawn, and the gate requires go or confirmed reviews.

## 7. The record

| commit | what |
|---|---|
| 680f128 | em-qwalk pre-registered (D55) |
| 34bad77 | em-qwalk seed: CURBy-RNG pulse 1591631 |
| c0850f1, c916490 | em-qwalk bet row; lesson ls-em-qwalk |
| 3244dbb, 6635276 | em-qwalk design reviews: fix-first (7); redesign |
| c9b2f3b | em-qwalk withdrawn (D56) |
| 1f6887d | em-qwalk2 pre-registered (D57, pattern P11) |
| ad66366 | em-qwalk2 seed: CURBy-RNG pulse 1591662 |
| 59b0a30 | em-qwalk2 bet row; lesson ls-em-qwalk2 |
| 04e7f81, efb4920, 0417646 | em-qwalk2 design reviews: fix-first (3); redesign; disclosure |
| 13e943a | em-qwalk2 withdrawn (D58); qwalk parked; st-13 outcome; pattern P12 |
| 41a687d | design-review check D11 (power floor), by the engine session |
| 2a7dcc7 | this results file |
| e91e7ff | seal pl-005 (clean) |
| 9c9c139 | audit em-qwalk: stands, 8 cuts |
| (this commit) | cuts applied, pl-005 revealed, `--null-thresholds` committed (D59) |
