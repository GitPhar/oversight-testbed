# qwalk2: a simulated quantum walk against PageRank on program 1's direction graph (pre-registration; re-bet of em-qwalk)

Written and frozen 2026-11-04 (America/Denver) in its own commit; that commit's author time is the freeze time. DEVIATIONS.md D57. **Laptop only: $0 API, 0 QPU seconds, no chip, no API call of any kind; laptop minutes.** The quantum walk is a numpy simulation (invariant 9: hardware is never a computational resource).

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision, in a terminal, a chat or a question dialog. His odds come only from `ledger/human-odds.jsonl` (the cockpit's downloads, committed); if a direction has no line there when its bet is pre-registered, the bet proceeds marked "no human odds". A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit. Sean's judgment is recorded and scored as steers in `ledger/steers.jsonl`: seed questions, vetoes, added questions and architecture decisions.

**This is not program 1's quantum error-prediction encoding and does not revive it** (CONTEXT §3 rule 6). That encoding put a model's competing claims on qubits to flag the model's wrong answers, and it is closed. This bet uses no model answer, claim web or circuit. It asks whether the links between program 1's *research directions* carry a signal about which directions were killed and which hit, and whether a quantum walk reads that signal better than PageRank.

**Why a re-bet.** em-qwalk (680f128) was withdrawn before data (D56). Its design review said redesign (`ledger/design-reviews/em-qwalk.md`): leave-one-node-out let each direction's own label shape its score. A second review said fix-first, 7 flaws (`em-qwalk-1b.md`): a walk worse than a coin could pass by being less wrong than PageRank. No score was computed on the real graph. This pre-registration fixes every flaw both reviews named (§10).

## 0. The bet

| field | value |
|---|---|
| bet id | `em-qwalk2` |
| referee | `mathematics` (an exact computation on archived labels decides it) |
| bet type | `standard` |
| direction | `qwalk` (map/entangled-mind.json); re-bet of `em-qwalk` (withdrawn, D56) |
| source | `human` (Sean, 2026-11-04, steer st-13) |
| engine odds, P(pass) | before this lesson: 5 (em-qwalk's, in the map; map 4 at 18:30, v1 re-elicitation 7 at 19:40). After this lesson: **1**. |
| human odds, P(pass) | **no human odds** (`ledger/human-odds.jsonl` has no `qwalk` line; never asked for) |
| budget | $0 API · 0 QPU s · under 15 laptop minutes |
| lesson | Correcting P11 (new), P3, P1: em-qwalk's leave-one-out scores leaked each direction's own label, and a below-chance walk could pass. This bet seeds both walks alike, reads every verdict against a label-permutation null, requires beating chance and four oriented dumb rules, and its odds are 1% (from 5%) because labels planted from the quantum kernel itself pass only 1–2%. Also applied: P2 (80%-power gap about 0.19 AUROC stated), P8 (the arms differ only in the one-seed kernel), P9, P10 (leave-one-label-out and leave-one-cluster-out). Read: 15 scored bets, Brier 0.267, base rate 6/15 (running 7/17 = 0.41), newest audit `ledger/audits/ss-b5.md`. |
| design review | two fresh reviewers before the run → `ledger/design-reviews/em-qwalk2.md` (launched by the author's session) and `em-qwalk2-1b.md` (launched by the engine session); the stricter binds. `qwalk2.py --run` refuses unless both are go or confirmed fix-first. |
| pre-mortem | "If this fails, the most likely reason is that on 25 labels the two one-seed kernels rank directions almost alike (planted quantum-kernel labels separate them by about 0.04 AUROC), far below the 0.19 the test can see." Kind: `design`. |
| auditor | a fresh subagent launched by the engine session (not by the planter or the author), operators/auditor.md's launch line verbatim, in a planter-built clone |

**Odds, stated once.** The running base rate is 0.41. Program 1's six quantum-against-classical comparisons (h2, h34, v2, v21, son, e5), every one matched or won by the classical side, give (0 + 1)/(6 + 2) = 0.125 by P1's rule. Both are ceilings here, because the dry run (§4) measures the test's reach directly. Even when the labels are made from the quantum walk's own kernel, the rule passes only 2% (no noise) and 1% (10% of labels flipped). On shuffled labels it passes 0.1–0.4%. So P(pass) cannot be much above 0.02 even if program 1's record were quantum-shaped, and there is no reason in the ledger to think it is: **1%**.

## 1. In plain English

Program 1 tried 41 research directions. Each grew out of an earlier one, and some shared data. 25 have a settled outcome: the direction's test came back a hit, or the direction was killed. Sean's idea (steer st-13) is to treat that web of linked ideas as a quantum system and ask whether it can tell the failures from the hits.

We hide one settled direction at a time. Every other settled direction then sends out a walk along the links, and the walks are added up, counting a hit's walk as plus and a kill's walk as minus. The hidden direction's score is how much more "hit" than "kill" reaches it. We do this twice: once with a simulated quantum walk, and once with PageRank, the classical link-ranking that search engines use. Both use the same links, the same starting points, the same weights and the same random stopping time (5.67 steps on average). The only difference is how one walk spreads: quantum amplitudes that can interfere, or classical probabilities that only add. The quantum walk's spreading is still averaged over a random stopping time, but nothing else differs.

**Quantum counts only if it beats PageRank.** It must also beat chance, and beat four one-line rules: the date bit, the neighbours' vote, the number of links and the number of follow-ups. Every comparison is judged against what the same graph gives when the 25 outcomes are shuffled at random. Shuffling is needed because hiding one direction at a time leaks a little of its own outcome into its score. The shuffled outcomes leak exactly the same way, so the comparison cancels the leak.

**The test is weak, and we say so first.** With 25 settled directions it can only reliably see a difference of about 0.19 in AUROC. In the most favourable world we could build, where the outcomes were made by the quantum walk itself, the gap was about 0.04. The likeliest result is "not detectably different". That would mean one program's record is far too small to test the idea. It would not mean the idea is wrong.

## 2. Material

- **Inputs, frozen.** `map/entangled-mind.json` and `ledger/bets.jsonl` **as of commit 680f128** (em-qwalk's pre-registration), read with `git show`. The code has `INPUT_COMMIT` hard-coded and accepts no other. Why not this commit: at 20:00 today the bmq scout session added 18 directions under `bmq`, 14 with labels (`af3266b`, `1376571`). Those labels come from the scout's reading stage, not from tested bets. They postdate the question (st-13, 18:00), and including them would add a new labelled star to the graph. Both reviews examined the 680f128 graph, so this bet keeps it. Between 680f128 and this commit, the only change to a node of the 680f128 graph is that `bmq` (unlabelled then) now carries its scout's label; every other label is unchanged. That was checked by code that printed only which nodes were added, newly labelled, or equal in value, never a value.
- **What the author has seen.** As in em-qwalk §2: the required reading showed node statuses and some em-* outcomes. The author has computed no score, AUROC or Δ on the real graph. Every dry run used synthetic labels, or the real links with the label values discarded (only the counts, 11 hits and 14 kills, were kept).
- **Graph and labels.** Exactly em-qwalk's rule (680f128 §2): 41 nodes (every direction except `qwalk`), 38 undirected edges (parent links, same `record.md` row, ledger `parent`/`replication_of`/`rebet_of`), 25 labelled (hit: `pass`/`pass-unreplicated`, or map status `hit`; kill: `null`/`classical`/`tie`/`fail`, or map status `killed`). Five components. The hub `oe` has 19 neighbours. Counts are from `--graph-counts 680f128` and the reviews.
- **The two kernels** (numpy 2.3.1; `experiments/qwalk2.py`). L_rw = I − D⁻¹A and L_sym = I − D^-½ A D^-½, with isolated nodes given zero rows; τ = α/(1 − α) = 5.667, α = 0.85.
  - Classical: K_C[j, i] = [(I + τ L_rw)⁻¹]_{ji}. This is personalised PageRank from j with damping 0.85 (identity checked to 1e-16).
  - Quantum: K_Q[j, i] = E_t |⟨i| e^{−i L_sym t} |j⟩|², with t exponential of mean τ. It is computed exactly per component as Σ_kl V_ik V_il V_jk V_jl / (1 + (λ_k − λ_l)² τ²) (Monte Carlo over t agrees: 0.0049 at 4,000 draws, 0.0023 at 64,000).
  - Both kernels' rows sum to 1 within a component.
- **The score**, the same for both arms. For hidden direction i: s(i) = Σ_{j settled, j ≠ i} (y_j − ȳ₋ᵢ) K[j, i], where ȳ₋ᵢ is the mean label of the other 24. It is rounded to 1e-12, so nodes no seed reaches score exactly 0.
- **Seed.** CURBY-Q latest completed round 28297, result pulse 2025-08-22 13:42 America/Denver (checked this evening): stalled. **Seed: the first CURBy-RNG pulse timestamped after this commit.** Two sub-seeds come from `python3 ledger/seed.py <randomness> em-qwalk2 --purpose bootstrap` and `--purpose permutation`, each the full 64-bit integer passed to `numpy.random.default_rng`. Leave-one-out is deterministic, so the seeds fix only the resampling and the shuffles. `--run` recomputes both seeds from the randomness recorded below and refuses any other. Filled in by the seed commit, before any analysis:
  `chain:` ___ · `pulse_index:` ___ · `pulse_time:` ___ · `randomness:` ___ · `client:` ___ · `certificate_verified:` ___ · `seeds:` ___

## 3. Calls

None. One local command after both reviews say go: `python3 programs/entangled-mind/experiments/qwalk2.py --run --seed-bootstrap <n> --seed-permutation <n>`. It writes `programs/entangled-mind/results/qwalk2.json`. Before the go, reviewers may run `--dry-run`, `--dry-run-real-topology 680f128` and `--graph-counts 680f128`, and synthetic tests of their own. They may not compute either arm's scores on the real labels.

## 4. Statistics

- **Primary statistic:** Δ = AUROC(quantum) − AUROC(PageRank), over the 25 settled directions' leave-one-out scores, with hits as positives and ties counted as ½.
- **Uncertainty, two ways, both in the rule.**
  1. A stratified bootstrap over settled directions (hits and kills resampled separately), B = 10,000, scores held fixed. It gives 95% percentile intervals for Δ and for each AUROC.
  2. A label-permutation null on the frozen graph: the 25 labels shuffled with counts fixed, all scores recomputed, P = 10,000. It gives the null's 2.5th and 97.5th percentiles for Δ and for each AUROC, and a one-sided p for Δ.
- **Oriented dumb rules (P3), in the rule.** The phase bit (the node carries ledger bets), the neighbour vote (the mean label of settled neighbours, never the node's own), degree, and child count. Each is scored as max(AUROC, 1 − AUROC), and best_dumb is the largest.
- **Secondary (reported, never promoted):** each arm's permutation-null mean, which shows the size of the leak on this graph. Also em-qwalk's coherent, count-scaled seeding, kept as "the bundle", with its own permutation null (P = 500). And the visible gap at 80% power, printed as 1.43 × the bootstrap half-width.
- **Sensitivity (reported, never promoted; B = P = 2,000):**
  - damping α ∈ {0.5, 0.7, 0.85, 0.95}, with τ matched;
  - parent links only;
  - **prospective**: while node i is scored, its edges to its descendants and to the nodes whose bets cite its bet are deleted. Links made after an outcome, and because of it, cannot then carry that outcome.
- **Robustness (P10, em-qwalk-1b F5; B = P = 2,000), each with the full verdict function:**
  - leave-one-label-out, for each of the 25;
  - leave-one-cluster-out: each component holding a label, and each labelled subtree off `oe`.
- **Multiple comparisons:** one primary verdict. The rest is descriptive.
- **Dry runs (done before this commit; the full rule; B = P = 500; synthetic labels only).**

| condition | graphs | pass | classical | mean AUROC quantum / PageRank | permutation-null mean (quantum) |
|---|---|---|---|---|---|
| star, 25 random labels, hub labelled hit | 1,000 | 0% | 0% | 0.909 / 0.909 | 0.920 |
| star, hub labelled kill | 1,000 | 0% | 0% | 0.929 / 0.929 | 0.920 |
| star, hub unlabelled | 1,000 | untestable 100% (every score ties at 0) | | 0.5 / 0.5 | 0.5 |
| hub-shaped graph like program 1's, hub hit | 1,000 | 0.2% | 0% | 0.460 / 0.460 | 0.456 |
| hub-shaped, hub kill | 1,000 | 0% | 0% | 0.459 / 0.461 | 0.455 |
| hub-shaped, hub unlabelled | 1,000 | 0.1% | 0% | 0.458 / 0.447 | 0.457 |
| **real links, shuffled 11/14** | 1,000 | 0.2% | 0% | 0.483 / 0.493 | 0.476 |
| real links, shuffled, `oe` held hit | 1,000 | 0.4% | 0% | 0.481 / 0.487 | 0.476 |
| real links, shuffled, `oe` held kill | 1,000 | 0.1% | 0% | 0.476 / 0.484 | 0.476 |
| real links, hit iff the node has follow-ups (10% flip) | 300 | 0% | 0% | 0.315 / 0.233 | 0.479 |
| real links, hit iff depth ≤ 1 (10% flip) | 300 | 0.3% | 0% | 0.733 / 0.698 | 0.478 |
| real links, alternating with depth (10% flip) | 300 | 0% | 0% | 0.330 / 0.297 | 0.478 |
| real links, siblings share a label (10% flip) | 300 | 0% | 0.3% | 0.562 / 0.569 | 0.479 |
| real links, labels planted from the **quantum** kernel | 200 | 2% (1% with 10% flip) | 0% | 0.789 / 0.751 | 0.477 |
| real links, labels planted from the **classical** kernel | 200 | 0.5% (1%) | 0% | 0.749 / 0.744 | 0.476 |

  What the table says:
  - **The leak is real and the null carries it.** On a star with a labelled hub, both arms score about 0.91 AUROC on random labels, and so does the shuffled null; on program 1's shape the null sits near 0.48. False verdicts stay at or below 0.4% everywhere, inside the 2.5% budget, with the hub held hit, held kill or unlabelled.
  - **Below-chance wins no longer pass.** On follow-ups and on depth alternation, the frozen em-qwalk rule passed 39% and 57%; this rule passes 0%.
  - **The rivals are matched but hardly separable (D4).** On labels made from the quantum kernel, the quantum arm wins by about 0.04 AUROC and passes 1–2%. On labels made from the classical kernel, the arms tie (0.749 against 0.744), so a "classical" verdict essentially cannot happen. Neither arm wins by construction. On 25 labels neither can win often.
  - **Power:** the visible gap at 80% power is about 0.18–0.21 AUROC (median over shuffled real-link runs: 0.186). A true gap of 0.04 needs very roughly 25 × (0.19/0.04)² ≈ 550 settled directions. That is an order-of-magnitude estimate, not a computed power.
  - D2: τ moves both kernels (0.13, 0.15); the kernels differ (max 0.60, the quantum walk's stay-at-home mass); quantum rows sum to 1.

## 5. Pre-registered reading

With n_hit, n_kill, n_zero (settled directions scored 0 by both arms), Δ and its bootstrap interval [lo, hi], the permutation percentiles, and best_dumb:

1. **Untestable:** n_hit < 5, or n_kill < 5, or n_zero > 12. *"The test cannot answer: program 1's direction graph has too few settled directions of one kind, or too many out of reach of the others."*
2. **Pass:** every one of these holds:
   - Δ > 0 and lo > 0;
   - Δ is above the permutation null's 97.5th percentile for Δ;
   - AUROC(quantum) is above its permutation null's 97.5th percentile, and its bootstrap lower end is above 0.5;
   - AUROC(quantum) > best_dumb.

   *"On program 1's direction graph (41 research directions linked by parent, same-run and ledger links; 25 settled), a quantum-walk score simulated on a laptop separated the directions that were killed from those that hit better than PageRank did on the same links, seeds, weights and stopping time, by Δ [lo, hi] in AUROC. It also beat chance and every one-line rule, each judged against shuffled outcomes. Many links were recorded after the outcomes, so this is a pattern in the record, not a forecast. One graph from one program: pass, unreplicated. It does not say the ideas are quantum or entangled, and no hardware was used."*
3. **Classical:** the mirror image (Δ < 0, hi < 0, Δ below the null's 2.5th percentile, PageRank above its null's 97.5th percentile with a bootstrap lower end above 0.5, and PageRank > best_dumb). *"PageRank separated program 1's killed directions from its hits better than the simulated quantum walk did, by Δ [lo, hi] in AUROC, and beat chance and every one-line rule. On this graph the classical walk wins."*
4. **Null:** anything else. *"The simulated quantum walk and PageRank were not detectably different at separating program 1's killed directions from its hits (Δ [lo, hi] in AUROC; shuffled outcomes give Δ between <q025> and <q975>). With 25 settled directions this test reliably sees only a gap of about <gap80> or more, and in the most quantum-favourable world we could build the gap was about 0.04. So this says one program's record is too small to test the idea, not that the idea is wrong. The quantum walk did not beat the classical baseline, so by the rule it does not count."*
   - If Δ > 0 and lo > 0 but another pass condition fails, add: *"The quantum score beat PageRank (Δ [lo, hi]) only by being less wrong, or no better than <rule> (AUROC x): it did not beat chance, or that one-line rule did as well, so it does not count."*
5. **Added in every case, as they apply:**
   - one label: *"The verdict hangs on one direction: without <node>'s label it would read <verdict>."*
   - one cluster: *"The verdict hangs on one cluster: without <cluster>'s labels it would read <verdict>."*
   - always, for a pass: *"With 25 labels, a pass is expected to be fragile."*
   - prospective: *"With each direction's links to its own follow-ups removed while it is scored, the verdict reads <verdict>."*
6. **Reported in every case:** every number in §4, the node-by-node score table, and both arms' permutation-null means.

## 6. What it cannot do

- **The labels are not blind to the author** (§2). The rule is em-qwalk's graph plus both reviews' fixes, with no knob left.
- **Many links were made after, and because of, the outcomes they connect.** Replications and follow-ups open under hits. So the graph is a record of the outcomes as much as a predictor of them. The prospective sensitivity removes the most direct case; it cannot remove all of them.
- **25 labels.** A null is not evidence of no difference. The gap visible at 80% power is about 0.19.
- **Labels are coarse.** "Killed" pools refuted, inconclusive and untestable directions; "hit" pools rule-passing descriptive tests.
- **Even a pass says nothing about minds, models or physics**, only that this walk separates this graph's labels better than PageRank. No "every", "all" or "quantum advantage" will appear in the write-up.
- **Not program 1's encoding** (CONTEXT §3 rule 6).

## 7. Stop rules

- No API call and no hardware anywhere in the code.
- `--run` refuses without both reviews at go (or confirmed fix-first), and if the pre-registration is uncommitted or the seeds differ from the recorded beacon's. The inputs are fixed at 680f128.
- A code failure on the real graph is reported as is; any fix is a dated DEVIATIONS row; the verdict rule never changes.

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "em-qwalk2", "program": "entangled-mind", "direction": "qwalk", "rebet_of": "em-qwalk",
 "title": "Entangled claims, re-bet: a simulated quantum walk against PageRank on program 1's direction graph", "source": "human", "steer": "st-13",
 "engine_odds": 0.01, "engine_odds_first": 0.05,
 "human_odds": null, "human_odds_note": "no human odds",
 "budget_usd": 0, "qpu_s_budget": 0, "referee": "mathematics", "bet_type": "standard", "seed_source": "curby-rng",
 "lesson": "ls-em-qwalk2", "premortem_kind": "design", "verdict": "open"}
```

## 9. Checklist before the run

- [x] This file, `qwalk2.py`, pattern line P11 and the D57 row are committed together; nothing has been scored on the real labels.
- [x] Lesson in §0 after reading bets.jsonl, brier.md, audits/ and lessons.jsonl; the same sentence goes to `ledger/lessons.jsonl` as `ls-em-qwalk2`.
- [ ] Both design reviews go or confirmed fix-first; `check_prereg.py em-qwalk2 . programs/entangled-mind/experiments/qwalk2.md --before-run` passes.
- [x] Engine odds before this commit (the map); no human odds.
- [x] Pre-mortem: one sentence, a checkable mechanism, its kind.
- [x] §2 records CURBY-Q's latest round and names CURBy-RNG; the seed commit follows.
- [x] No paid call or hardware exists in the code.

## 10. How each review flaw is answered

| review | flaw | answer here |
|---|---|---|
| em-qwalk.md | 1. own-label leak | label-permutation null in the rule (§4–5); dry runs on stars and hub graphs with the hub labelled hit, labelled kill and unlabelled (1,000 graphs each): false verdicts ≤ 0.4% |
| em-qwalk.md | 2. seeds not matched | both arms use the same per-seed mixture and weights; they differ only in the one-seed kernel; "exact classical twin" dropped; coherent seeding is a labelled "bundle" secondary |
| em-qwalk.md | 3. winner must beat chance | permutation and bootstrap chance conditions in the rule; dumb rules oriented |
| em-qwalk.md | 4. dry run on the real shape | real links with values discarded, `oe` held both ways; planted-kernel worlds for each arm (§4); odds re-derived from them |
| em-qwalk.md | 5. state the real power | 80%-power gap about 0.19 in §1, §4, §5 and §6, and printed by the code |
| em-qwalk.md | 6. pin the seed and inputs | `INPUT_COMMIT` fixed; seeds recomputed from the recorded randomness; any mismatch refuses |
| em-qwalk-1b.md | F1 below-chance pass | as flaw 3 above; the em-qwalk wording sentence is kept in §5.4 |
| em-qwalk-1b.md | F2 dumb rules | degree and child count added; all four oriented, inside the rule |
| em-qwalk-1b.md | F3 leakage through edges | §6 bullet; prospective sensitivity |
| em-qwalk-1b.md | F4 false-pass on the real topology | measured on the real links (0.2%; the frozen em-qwalk rule gave 3.8% in the author's run, 4.3% in the review's); the Monte Carlo figure restated from this code's output |
| em-qwalk-1b.md | F5 clusters | leave-one-cluster-out with the full verdict, and the fragility sentence |
| em-qwalk-1b.md | F6 wording | "direction graph", "separated", "a pattern in the record, not a forecast", "no hardware was used" |
| em-qwalk-1b.md | F7 gate | `--run` requires every `em-qwalk2*.md` to be go or confirmed, and both named files to exist |
