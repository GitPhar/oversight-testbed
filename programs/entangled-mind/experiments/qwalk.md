# qwalk: a simulated quantum walk against PageRank on program 1's claim graph (pre-registration)

Written and frozen 2026-11-04 19:50 (America/Denver), in its own commit, before the claim graph is opened for analysis. DEVIATIONS.md D55. **Laptop only: $0 API, 0 QPU seconds, no chip, no API call of any kind; laptop minutes.** The quantum walk is a numpy simulation on the laptop (invariant 9: hardware is never a computational resource). Stop rules in §7.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision, in a terminal, a chat or a question dialog. His odds come only from `ledger/human-odds.jsonl` (the cockpit's downloads, committed); if a direction has no line there when its bet is pre-registered, the bet proceeds marked "no human odds". A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit. Sean's judgment is recorded and scored as steers in `ledger/steers.jsonl`: seed questions, vetoes, added questions and architecture decisions.

**This is not the quantum error-prediction encoding, and it does not revive it** (CONTEXT §3 rule 6). That encoding put one model's competing claims on qubits to flag the model's wrong answers. It is closed. This bet asks a different question, about the research record: whether the way program 1's *research directions* link to each other carries a signal about which directions were killed and which hit, and whether a quantum walk reads that signal better than PageRank does. No language-model answer, claim web or circuit from program 1 is used.

## 0. The bet

| field | value |
|---|---|
| bet id | `em-qwalk` |
| referee | `mathematics` (an exact computation on archived labels decides it; no model call, no chip) |
| bet type | `standard` |
| direction | `qwalk` (map/entangled-mind.json) |
| source | `human` (Sean, 2026-11-04, steer st-13) |
| engine odds, P(pass) | map: 4, stated 2026-11-04T18:30 in map/entangled-mind.json (no template; "re-elicit with v1 before pre-registration"). Re-elicited 2026-11-04 19:40 under the v1 template (a fresh subagent holding only the direction's question, cheapest test and draft pass rule, no outcomes): **7**, rationale "about 25 labelled nodes on a sparse forest, noisy AUROC difference; PageRank captures locality directly". After the lesson: **5** (below). |
| human odds, P(pass) | **no human odds** (`ledger/human-odds.jsonl` has no line for `qwalk`; never asked for) |
| budget | $0 API · 0 QPU s · under 10 laptop minutes |
| lesson | Correcting P1, P3, P8: program 1's classical twins matched all six quantum comparisons, and past rivals were trivial or unmatched. PageRank here is the walk's exact classical twin (same generator, seeds, stopping time), a one-bit date rule is reported, and odds are 5% (from 4% on the map; fresh v1 7%) because random labels pass 2.7% in the dry run. Also applied: P2 (the null sentence states the smallest visible gap, about 0.12 AUROC), P9 (verdict sentences in §5), P10 (leave-one-label-out). Read: 14 scored bets, Brier 0.246, base rate 5/14 (running 6/16 = 0.375), newest audit `ledger/audits/ss-b1.md`. |
| design review | before the analysis, a fresh subagent dry-runs this design (operators/design-review.md) → `ledger/design-reviews/em-qwalk.md`. `qwalk.py --run` refuses unless that file says go (or fix-first, confirmed). |
| pre-mortem | "If this fails, the most likely reason is that program 1's labels cluster by branch (whole subtrees killed together), where the dry run shows both walks rank alike, so the gap sits inside the ±0.12 interval." Kind: `world`. |
| auditor | fresh subagent per operators/auditor.md, after results, in a planter-built clone (operators/plant.md) |

**Odds, stated once.** Map 0.04 (18:30), v1 0.07 (19:40), in force 0.05 (this commit). Reason for 0.05: the running base rate is 0.375, but the nearest reference class in the ledger is program 1's six quantum-against-classical comparisons (h2, h34, v2, v21, son, e5), all matched or won by the classical side: (0 + 1)/(6 + 2) = 0.125 by P1's rule. Lower again because the dry run (§4) puts the rule's false-pass rate on random labels at 2.7% and its smallest visible gap at about 0.12 AUROC on 25 labels. Raised slightly from 0.04 because the same dry run shows a label pattern (alternation with depth) where the quantum walk wins 56% of the time, so a route to a pass exists.

## 1. In plain English

Program 1 tried about thirty-five research directions. Each grew out of an earlier one, and some shared data. About twenty-five have a settled outcome: the direction's test came back a hit, or the direction was killed. Sean's idea (steer st-13) is to treat that web of linked ideas as a quantum system and ask whether it can tell which ideas were going to fail.

We test it the cheapest way. We hide one settled direction at a time. From the others, a simulated quantum walk spreads out over the links twice: once from the known hits and once from the known kills. The hidden direction is scored by how much more of the walk reaches it from the hits than from the kills. Then we do exactly the same with PageRank, the classical link-ranking method search engines use, on the same links from the same starting points.

PageRank is the classical twin of this quantum walk in a strict sense. PageRank with damping 0.85 is a classical random walk that stops at a random time averaging 5.67 steps. The quantum walk here uses the same links, the same starting points and the same random stopping time. The only difference is that its spreading is quantum (amplitudes that can interfere) instead of classical (probabilities that only add). So if the quantum walk wins, it wins by interference, not by a different graph or a longer walk.

**Quantum counts only if it beats PageRank.** Beating chance does not count. With about twenty-five labelled directions the test is weak: it can only see a difference of about 0.12 in AUROC or more. A smaller edge either way would go undetected, and the write-up will say so.

## 2. Material

- **Inputs, frozen at this commit.** `map/entangled-mind.json` and `ledger/bets.jsonl`, read with `git show <this commit>:<path>`, so later ledger edits (this bet's own row included) cannot change the graph.
- **Disclosure: what the author has seen.** Before writing this, the author read the required files: `map/entangled-mind.json` (node statuses visible), `programs/entangled-mind/paper/record.md`, `gold-map.md`, `biomimetic-map.md` and `ledger/brier.md` (which list some em-* outcomes). So the labels are not hidden from the author. No predictor has been computed on the real graph, and no node, edge or label has been counted by code. The dry run (§4) used synthetic forests only. The protection is that the graph rule, the walk, the baseline, the statistic and the reading are fixed here, with no tuning knob left. Both methods use the same graph, so an edge rule cannot favour one method except through its shape, and the parent-links-only graph is reported as a sensitivity.
- **Nodes.** Every entry of `directions` in `map/entangled-mind.json` except `qwalk` itself (this bet). Open, mixed and moved-to nodes stay in the graph as unlabelled nodes. Expected: about 36 nodes.
- **Edges (undirected, unweighted, duplicates merged).**
  1. *Parent links:* each direction to its `parent`.
  2. *Same record row:* two phase-A nodes (no `bets` field) whose `source` begins `record.md` and cites at least one identical `HH:MM` time (the same row of `paper/record.md`, i.e. the same data run).
  3. *Ledger links:* for each bet listed on a node, its `parent`, `replication_of` and `rebet_of` fields in `ledger/bets.jsonl`, joined to the node listing the target bet (or to the node with that id).
- **Labels (hit 1, killed 0).**
  - Phase-A nodes (no `bets` field): map `status` `hit` → 1, `killed` → 0, anything else unlabelled. (The map's `killed` includes inconclusive and untestable phase-A directions, such as e3 and e4r3. That is the map's label, taken as is.)
  - Nodes with `bets`: each listed bet's `verdict_after_audit`, else `verdict`. `pass` or `pass-unreplicated` → 1; `null`, `classical`, `tie`, `fail` → 0; anything else (`mixed`, `undetermined`, `untestable`, `open`, missing) → unlabelled. If a node's bets disagree or any is unlabelled, the node is unlabelled.
  - Expected: about 25 labelled nodes. **That is the power problem:** with about 25 labels, the 95% interval on the AUROC difference is about ±0.12 wide (dry run, §4).
- **The two predictors** (`experiments/qwalk.py`; numpy 2.3.1, no other dependency). A = adjacency, D = degree, L_rw = I − D⁻¹A, L_sym = I − D^-½ A D^-½ (similar matrices, same spectrum; isolated nodes get zero rows). Seeds S: the labelled hits (or kills), minus the hidden node.
  - **PageRank (the classical baseline):** personalised PageRank with damping α = 0.85 (the standard default, not tuned) and teleport uniform on S: p = (1 − α) s (I − αP)⁻¹, P = D⁻¹A. This equals s (I + τ L_rw)⁻¹ with τ = α/(1 − α) = 5.667, a classical continuous-time walk stopped at an exponential time of mean τ (identity checked to 1e-16 in the dry run).
  - **Quantum walk:** a continuous-time quantum walk with Hamiltonian L_sym, started in the equal-amplitude superposition of S, read out as the probability at each node averaged over an exponential stopping time of the same mean τ = 5.667. Computed exactly: P(i) = Σ_kl V_ik V_il c_k c_l / (1 + (λ_k − λ_l)² τ²), with L_sym = V Λ Vᵀ per connected component and c = Vᵀψ_S (checked against Monte Carlo over t: error 0.0024 at 4,000 draws, 0.0003 at 64,000).
  - **Score** of hidden node i, for each method: (mass at i from the hit seeds) − (mass at i from the kill seeds), rounded to 1e-12 so that nodes no seed can reach score exactly 0 under both methods.
- **Seed.** CURBY-Q latest completed round 28297, result pulse 2025-08-22 13:42 America/Denver (checked 19:44 today with `DIRNGClient.latest()`, client 1.2.0): stalled. **Seed: the first CURBy-RNG pulse timestamped after this commit.** seed = `python3 ledger/seed.py <randomness> em-qwalk --purpose bootstrap` (the full 64-bit integer, passed to `numpy.random.default_rng`). Its only use is the bootstrap: leave-one-node-out is deterministic, so there is no split or sample to shop for. Filled in by the seed commit, before any analysis:
  `chain:` ___ · `pulse_index:` ___ · `pulse_time:` ___ · `randomness:` ___ · `client:` ___ · `certificate_verified:` ___ · `seed:` ___
- **Scale.** Not applicable: no graded prompt, no model call.

## 3. Calls

None. One local command after the design review says go: `python3 programs/entangled-mind/experiments/qwalk.py --run <this commit> --seed <seed>`, which writes `programs/entangled-mind/results/qwalk.json`. The design review may also run `--dry-run` (synthetic only) and `--graph-counts <this commit>` (prints node, edge, label and component counts, no predictor); nothing else touches the real graph before the go.

## 4. Statistics

- **Primary statistic:** Δ = AUROC(quantum walk) − AUROC(PageRank), each AUROC computed over the labelled nodes from their leave-one-node-out scores (hits positive), ties counted as one half (Mann–Whitney).
- **Uncertainty:** stratified bootstrap over labelled nodes (hits and kills resampled separately, sizes kept), B = 10,000, scores held fixed, the CURBy seed; 95% percentile interval [lo, hi].
- **Unit:** the labelled direction. **Split:** leave-one-node-out; the hidden node's label never reaches its own score.
- **Secondary (reported, never promoted to the headline):**
  1. Each method's AUROC against chance (bootstrap against a constant score). *Beating chance does not count.*
  2. **Dumb baselines (P3):** the phase bit (1 if the node carries ledger bets, 0 if it is a phase-A node; a one-bit "was it tested before or after the ledger began") and the neighbour vote (mean label of labelled neighbours, 0.5 if none). If either matches or beats the quantum walk's AUROC, the write-up says the walk adds nothing over that rule.
  3. Quantum walk with incoherent seeds (each seed walked alone, probabilities averaged): separates interference between seeds from interference along paths.
  4. The number of labelled nodes no seed can reach (score 0 under both methods).
- **Sensitivity (reported, never promoted):** damping α ∈ {0.5, 0.7, 0.85, 0.95}, each with its matched τ = α/(1 − α); the graph with parent links only (edge rules 2 and 3 dropped).
- **Robustness (P10), pre-registered:** leave-one-label-out. Each labelled node in turn is made unlabelled (no longer a seed, no longer scored) and everything is recomputed. If any single removal changes the verdict, the verdict stands by the frozen rule but is reported as **fragile, hanging on <node>**.
- **Multiple comparisons:** one primary test. The secondaries and sensitivities are descriptive and uncorrected, and they are labelled so.
- **Dry run on synthetic forests (done before this commit; no real data).** `qwalk.py --dry-run`: 37-node random forests with 7 roots and 3 extra edges, 25 labelled nodes, B = 2,000, about 300 graphs per condition:

| synthetic labels | pass | classical | null | median 95% interval width | mean Δ |
|---|---|---|---|---|---|
| random (no structure) | 2.7% | 4.4% | 93.0% | 0.246 | −0.002 |
| shared along branches (20% flip per link) | 0.3% | 3.5% | 96.2% | 0.181 | −0.016 |
| alternating with depth | 56.3% | 0% | 43.7% | 0.276 | +0.141 |

  So: the rule's false-pass rate on structureless labels is about 3%; the smallest gap it can see is about 0.12 AUROC (half the median interval width); on branch-shared labels the two walks rank alike; and on depth-alternating labels the quantum walk wins, so neither rival wins by construction (check D4). D2: the stopping time moves both predictors (max change 0.14), the two methods differ (max 0.04 on one graph), quantum probability sums to 1.

## 5. Pre-registered reading

With Δ and its interval [lo, hi], n_hit and n_kill labelled hits and kills, and n_zero labelled nodes no seed reaches:

1. **Untestable:** n_hit < 5, or n_kill < 5, or n_zero > half the labelled nodes. Sentence: *"The test cannot answer: program 1's graph has too few settled directions of one kind, or too many out of reach of every other, for the two walks to be compared."*
2. **Pass:** Δ > 0 and lo > 0. Sentence: *"On program 1's claim graph (N directions, n settled), a quantum walk simulated on a laptop ranked the directions that were later killed below those that hit better than PageRank did, by Δ [lo, hi] in AUROC. This is one graph from one program: pass, unreplicated. It says the link pattern of program 1's directions carries something a quantum walk reads better than its exact classical twin; it does not say the ideas are quantum or entangled, and no hardware was used or would help."*
3. **Classical:** Δ < 0 and hi < 0. Sentence: *"PageRank ranked program 1's killed directions below its hits better than the simulated quantum walk did, by Δ [lo, hi] in AUROC. On this graph the classical walk wins."*
4. **Null:** otherwise. Sentence: *"The simulated quantum walk and PageRank were not detectably different at telling program 1's killed directions from its hits (Δ [lo, hi] in AUROC). With n settled directions this test could only have seen a gap of about <half-width> or more, so a smaller edge either way is not ruled out. The quantum walk did not beat the classical baseline, so by the rule it does not count."*
5. **Added in every case, as they apply:**
   - fragile: *"The verdict hangs on one direction: without <node>'s label it would read <verdict>."*
   - dumb baseline: *"A one-bit rule (<phase bit | neighbour vote>, AUROC x) predicts as well as or better than the quantum walk, so the walk adds nothing over that rule."*
   - chance: each method's AUROC against chance, with the words *"beating chance does not count"*.
6. **Reported in every case:** N, number of edges, n_hit, n_kill, n_zero, both AUROCs, Δ and [lo, hi], every secondary, sensitivity and leave-one-label-out row, and the full node-by-node score table.

## 6. What it cannot do

- **The labels are not blind to the author** (§2). Everything is fixed here, but the edge rules were written by someone who had read the outcomes.
- **One graph, about 25 labels.** A null is not evidence of no difference; the visible gap is about 0.12 AUROC.
- **The bootstrap holds leave-one-node-out scores fixed.** Each score depends on every other label, so the interval understates the uncertainty somewhat. It is the rule anyway, as pre-registered.
- **Labels are coarse.** "Killed" pools refuted, inconclusive and untestable directions (the map's phase-A label); "hit" pools rule-passing descriptive tests. The graph also mixes three kinds of link.
- **Even a pass would say nothing about minds, models or physics:** only that this walk ranks this graph's labels better than PageRank. No "every", "all" or "quantum advantage" will appear in the write-up.
- **It is not program 1's encoding** and cannot reopen it (CONTEXT §3 rule 6).

## 7. Stop rules

- No API call and no hardware anywhere in the code; the run is local numpy.
- `--run` refuses without a design-review go and without the CURBy seed.
- If the code fails on the real graph, the failure is reported as is; any fix is a dated DEVIATIONS row naming what changed, and the verdict rule does not change.

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "em-qwalk", "program": "entangled-mind", "direction": "qwalk",
 "title": "Entangled claims: a simulated quantum walk against PageRank on program 1's claim graph", "source": "human",
 "engine_odds": 0.05, "engine_odds_first": 0.04, "engine_odds_v1": 0.07, "engine_odds_at": "2026-11-04T19:50",
 "human_odds": null, "human_odds_note": "no human odds",
 "prereg_commit": "<filled by the next commit>", "budget_usd": 0, "qpu_s_budget": 0,
 "referee": "mathematics", "bet_type": "standard", "seed_source": "curby-rng", "beacon": null, "seed": null, "tiebreak": null,
 "lesson": "ls-em-qwalk", "design_review": {"path": "ledger/design-reviews/em-qwalk.md", "verdict": null, "commit": null, "reviewer_model": null, "fix_deviations": [], "missed": null},
 "premortem": "If this fails, the most likely reason is that program 1's labels cluster by branch (whole subtrees killed together), where the dry run shows both walks rank alike, so the gap sits inside the ±0.12 interval.", "premortem_kind": "world",
 "steer": "st-13", "verdict": "open", "date": "2026-11-04", "result": null, "audit": null, "diagnosis": null}
```

## 9. Checklist before the analysis

- [x] This file, `qwalk.py` and the D55 row are committed together; nothing has been run on the real graph.
- [x] Lesson in §0 after reading bets.jsonl, brier.md, audits/ and lessons.jsonl; the same sentence goes to `ledger/lessons.jsonl` as `ls-em-qwalk`.
- [ ] Design review returns go (or fix-first, confirmed) before `--run`; `check_prereg.py em-qwalk . programs/entangled-mind/experiments/qwalk.md --before-run` passes.
- [x] Engine odds on record before this commit (map, 18:30; v1, 19:40); no human odds.
- [x] The §5 reading can be applied by a stranger.
- [x] Pre-mortem: one sentence, a checkable mechanism, its kind.
- [x] §2 records CURBY-Q's latest completed round and names CURBy-RNG by the 24-hour rule; the seed commit follows before any analysis.
- [x] No paid call or hardware exists in the code.
- [x] DEVIATIONS.md D55.
