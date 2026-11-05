---
bet: em-qwalk2
program: entangled-mind
prereg_commit: 1f6887d
seed_commit: ad66366
ledger_commit: 59b0a30
reviewer_session: design-review em-qwalk2, second reviewer "1b" (fresh subagent launched by the engine session; reviewed em-qwalk as em-qwalk-1b.md; no chat, transcript or author message read; the stricter of em-qwalk2.md and this file binds)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-04 20:25 America/Denver
checks: {D1: holds, D2: holds, D3: holds, D4: flaw, D5: holds, D6: holds (no calls), D7: holds, D8: flaw, D9: holds, D10: flaw, E23: holds (internal; pulses not refetched, no network), E25: holds, P11: holds, pinning: holds, rule-6 revival: holds, hardware/quantum-advantage: holds}
flaws: 3
pilot_usd: 0.00
verdict: fix-first
confirmed_at: null
---

# Design review of em-qwalk2 (reviewer 1b)

## In plain English

This re-bet repairs the faults that sank em-qwalk.
- **No direction sees its own outcome.** A direction's score no longer depends on its own outcome at all: flipping its label changes its own score by exactly 0, in both walks and in the neighbour vote.
- **The leftover leak is cancelled.** A small leak remains, because the total of 11 hits is fixed. Every verdict is now read against shuffled outcomes on the same graph, which carry that leak too.
- **Shuffled outcomes almost never pass.** On program 1's real links with shuffled outcomes, the rule passed 4 times in 3,000 (0.13%) and never said "classical".
- **No made-up structure passes beyond chance.** I built ten patterns from the graph's structure, not from any judgment of the work: "has follow-ups", "is a leaf", "near the root", alternating depth, the date bit, "has several links", shared along branches, shared within a component, shared within an `oe` subtree, and so on. None passes more than 0.4%.
- **Walks below chance can no longer pass.** On the "has follow-ups" pattern, the old rule passed 33–39%; this rule passes 0%.
- **Each walk can win in its own made-up world, rarely.** On labels grown from the quantum kernel, the quantum walk wins 1.4–3.2% of the time. On labels grown from a few sources by the classical kernel, PageRank wins 5% of the time.

Three small things need fixing before the run:
- The made-up "planted" worlds that the 1% odds and the pre-mortem rest on are not in the committed code, and one claim drawn from them is wrong.
- The pass sentence says the one-line rules were "judged against shuffled outcomes", which they are not.
- The run gate ignores review files with unusual names.

None of these changes what is tested.

## Scope and disclosure

- **What I ran.** I used the author's code (`qwalk2.py` at 1f6887d, unchanged in the working tree) on the graph pinned at 680f128. I kept only the set of settled nodes and the count of 11 hits, deleted the label values, and assigned synthetic labels. I never computed either arm's score on the real labels.
- **What I read.** To check where labels and edges come from, I read the pinned map's entries, so I have seen phase-A statuses (as the author had). That reading fed no computation.
- **Scripts:** `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/19f84df9-a6ff-48ba-89d6-d3f43e5d1747/scratchpad/rev2/` (`q2probe.py`, `p11.py`, `gate.py`, `d1.py`; the author's dry-run outputs are in `dry_real.txt` and `dry_synth.txt`).

## Checks

**P11 (the held-out direction's own label must not shape its score). Holds.**
- **Own label.** `p11.py` flips one settled node's label and leaves the other 24 alone, over 200 random label vectors and every node, on the real links. The maximum change in that node's own score is 0.00e+00 for the quantum arm, the PageRank arm and the neighbour vote. `scores()` uses ȳ₋ᵢ = (T − yᵢ)/(n − 1), which is the other nodes' mean, so each score is a function of the others' labels only.
- **Remaining leak.** The leak that remains comes through the fixed count (11 of 25). The permutation null, with counts fixed, reproduces it: on a star with the hub labelled, both arms reach AUROC 0.91–0.93 on random labels, the null mean is 0.92, and the verdict is null in 300 of 300.
- **The hub held fixed.** P11's do_this asks for the most influential item held each way. Holding `oe` as a hit or as a kill gives 0.4% and 0.1% pass (author's run, reproduced exactly).

**The other review's redesign reasons (em-qwalk.md, flaws 1–6). All answered.**
1. **Own-label leak:** answered as above.
2. **Unmatched seeding:** both arms use the same formula and the same centred weights. `scores(CQ, y)` and `scores(CC, y)` differ only in the kernel matrix.
3. **Beating chance:** checked under F1 below.
4. **Dry run on the real shape:** the real-topology dry run exists and reproduces exactly.
5. **Real power stated:** the 80%-power gap is 0.186 (median), printed by the code and quoted in §5.4.
6. **Seed and inputs pinned:** `INPUT_COMMIT` is hard-coded, and `run()` recomputes both seeds from the recorded randomness and refuses a mismatch.

**My em-qwalk flaws F1–F7, checked against the code, not against §10's map:**

| em-qwalk-1b flaw | status in qwalk2 | evidence |
|---|---|---|
| F1: a pass must beat chance | holds | `verdict()` requires the bootstrap lower end above 0.5 and AUROC(quantum) above the permutation 97.5th percentile. In `d1.py`, "below chance, less wrong" (0.40 against 0.20) gives null. On real links, has-a-child and leaf labels pass 0/500 each (quantum 0.32, PageRank 0.24), and depth-alternating passes 0/499 |
| F2: oriented dumb rules inside the rule | holds | four rules (phase bit, neighbour vote, degree, child count), each max(A, 1 − A), with `auroc_quantum > best_dumb` in `verdict()`. "Dumb rule ties at 0.8" gives null. Classical is mirrored |
| F3: prospective-edges sensitivity | holds | `prospective_cols` cuts the hidden node's edges to its descendants and its citers. Cut sizes are oe 25, h2 4, gm3 4, h5 3, v2 2, gm2 2, gm1 1, bm1 1. One gap, a recommendation rather than a flaw: see "Pinned labels and edges" below |
| F4: false-pass rate on the real topology | holds | 4/3,000 = 0.13% pass and 0 classical (mine); 0.2% (author, reproduced) |
| F5: leave-one-cluster-out | holds | `clusters()` gives the 5 components plus 9 labelled subtrees off `oe`, each run through the full verdict, with the sentence in §5.5. Dropping the 29-node component leaves 9 labels and therefore "untestable", so any testable verdict will be reported as hanging on that component. That is correct, and the write-up should expect it |
| F6: wording | mostly holds | "direction graph", "separated", "a pattern in the record, not a forecast" and "no hardware was used" are all in. One new overclaim: see F-B |
| F7: gate reads every review | partial | requires `em-qwalk2.md` and `em-qwalk2-1b.md`, and every file matching `em-qwalk2(-[A-Za-z0-9]+)?\.md`, to be go or confirmed fix-first. Not every `em-qwalk2*.md`: see F-C |

**D1. A stranger can apply the rule. Holds.** I fed `verdict()` nine synthetic tables (`d1.py`): all conditions met (pass); Δ inside the permutation null, quantum below its null, quantum bootstrap lower end 0.5, a dumb rule tying, and below chance but less wrong (each null); the classical mirror (classical); too few kills and too many zeros (untestable). It returned exactly one verdict each time, matching §5.

**D2. Every manipulation takes effect. Holds.** From `--dry-run` (seed 20261104):
- τ moves both kernels (0.132 and 0.147);
- the two kernels differ (max 0.605);
- quantum rows sum to 1 ± 2e-15;
- the PageRank identity holds to 1.1e-16;
- the exact average matches Monte Carlo (0.0049 at 4,000 draws, 0.0023 at 64,000), which matches §2.

Every setting is frozen in code: α = 0.85, τ tied to it, B = P = 10,000, the inputs, and the seeds. There is no free t and no free node encoding.

**D3. Every control can fail. Holds.** The permutation null rejects a pure-leak "signal": on a star, raw AUROC is 0.91 and the verdict is null in 300 of 300. The chance and dumb-rule conditions reject below-chance and trivial wins (D1 cases; has-a-child 0%). The seed check refuses a mismatch.

**D4. Rivals are matched. Flaw (F-A).** My own label worlds on the real links (B = P = 500, `q2probe.py`):

| synthetic labels (real links) | n | pass | classical | AUROC quantum / PageRank | best oriented dumb rule |
|---|---|---|---|---|---|
| shuffled 11/14 | 3,000 | 0.13% | 0% | 0.475 / 0.483 | 0.663 |
| has a child / is a leaf (10% flip) | 500 each | 0% | 0% | 0.323 / 0.243 | 0.897 |
| depth ≤ 1 | 500 | 0.4% | 0% | 0.728 / 0.694 | 0.850 |
| depth alternating | 499 | 0% | 0% | 0.331 / 0.304 | 0.786 |
| phase bit | 500 | 0% | 0% | 0.808 / 0.776 | 0.905 |
| degree ≥ 2 | 500 | 0% | 0% | 0.393 / 0.389 | 0.902 |
| homophily on parent links | 346 | 0% | 0% | 0.830 / 0.833 | 0.831 |
| shared within component | 318 | 0% | 0% | 0.802 / 0.808 | 0.821 |
| shared within an `oe` subtree | 493 | 0.4% | 0% | 0.735 / 0.737 | 0.722 |
| quantum kernel × Gaussian field | 500 | 3.2% | 0% | 0.799 / 0.754 | 0.732 |
| same, 10% flip | 500 | 1.4% | 0% | 0.703 / 0.673 | 0.694 |
| classical kernel × Gaussian field | 500 | 0.6% | 0.2% | 0.764 / 0.758 | 0.759 |
| quantum kernel × 6 random sources | 500 | 0.8% | 0.2% | 0.887 / 0.869 | 0.829 |
| classical kernel × 6 random sources | 500 | 0% | **5.0%** | 0.752 / 0.777 | 0.826 |

What the table shows:
- Neither arm wins by construction.
- Each arm can win in a world built from its own kernel, rarely.
- No structural, non-judgment pattern passes above 0.4%.

The flaw is in the record, not the rule:
- **Not reproducible.** §4's planted-kernel rows (quantum 2% / 1%, classical 0.5% / 1%) are the stated basis of the 1% odds, the pre-mortem's "about 0.04 AUROC" and D4's "classical essentially cannot happen". No committed code produces them: `qwalk2.py` has no planted-world function, and `grep -i plant` finds nothing.
- **One claim drawn from them is false.** "On labels made from the classical kernel, the arms tie … so a 'classical' verdict essentially cannot happen." With sources planted through the classical kernel, the rule says classical 5.0% of the time.

**D5. A dumb baseline is beaten, and the design can see the effect. Holds.**
- The four oriented rules are inside the rule.
- best_dumb is compared without a null adjustment, but on this graph the quantum arm's null mean is 0.476, below 0.5, so the comparison is conservative here.
- Power is stated two ways: the 80%-power gap of about 0.19, and the planted-world pass rates. The null sentence carries both. This is not a "no difference" pass rule.

**D6. Execution risks are piloted. Holds.** The bet makes no calls and uses no hardware.

**D7. Comparisons match. Holds.**
- The arms differ only in the one-seed kernel: same links, settled set, weights, stopping time, score formula, bootstrap draws and permutation draws (both arms are scored on the same shuffles). The coherent "bundle" is a labelled secondary.
- Edge leakage is disclosed in §6 and handled by the prospective sensitivity (see "Pinned labels and edges").

**D8. Verdict sentences are written. Flaw (F-B).** The pass sentence says it "also beat chance and every one-line rule, each judged against shuffled outcomes". Only chance and the walk comparison are judged against shuffled outcomes. The one-line rules are a raw point-estimate comparison (`auroc_quantum > best_dumb`). Everything else in §5 carries only nouns the design supports: "a quantum-walk score simulated on a laptop", "direction graph", "a pattern in the record, not a forecast", "pass, unreplicated", and no "advantage", "entangled" or "every".

**D9. One item cannot decide it. Holds.** Leave-one-label-out and leave-one-cluster-out are pre-registered with the full verdict and their sentences, plus "a pass is expected to be fragile".

**D10. Machinery. Flaw (F-C).**
- These parts hold:
  - The code imports nothing that touches the network (argparse, hashlib, json, os, re, subprocess for `git`, sys, numpy).
  - `INPUT_COMMIT` is pinned.
  - Both seeds are recomputed from the recorded randomness, and they match.
  - `--run` refuses an uncommitted pre-registration.
  - `check_prereg.py` passes L1–L3; R1 fails only because `em-qwalk2.md` does not exist yet.
- **Gate behaviour** (`gate.py`, on synthetic review files in a temporary root):

| review files present | gate result |
|---|---|
| none | refuse |
| author's review only | refuse |
| both go | run |
| 1b fix-first, `confirmed_at` null | refuse |
| 1b fix-first, confirmed | run |
| a third review `em-qwalk2-2c.md` saying redesign | refuse |
| "verdict: go" only in the body | refuse |
| a redesign saved as `em-qwalk2_extra.md` | **run** |
| `em-qwalk2-1b-r2.md`-style names | **ignored** |

So the gate does not read every `em-qwalk2*.md`, which is what em-qwalk-1b F7 asked for.

**E23. Seed. Holds, from the record.**
- §2 records CURBY-Q round 28297 (2025-08-22), so the chain is stalled and CURBy-RNG is correct.
- The pulse is 1591662 at 03:18:00.156Z. The pre-registration author time is 20:17:31 −07:00 (03:17:31Z), and the previous pulse, 1591661 at 03:17:00.186Z, predates it. The seed commit, ad66366, follows at 20:18:30.
- `ledger/seed.py` gives bootstrap 15016625028946468319 and permutation 15216281605376176335, matching the record and `recorded_seeds()`.
- `results/qwalk2.json` does not exist.
- Cannot check: I could not refetch the pulses (no network).

**E25. Lesson. Holds.**
- §0's lesson matches `ls-em-qwalk2` (check_prereg L2). The ledger line was added at 59b0a30, the engine commit that adds the bet row, as learn.md allows.
- The read block matches the ledger at 1f6887d: 15 scored, Brier 0.267 (`brier.md`), 6/15, running 7/17 = 0.41, and `ss-b5.md` as the newest audit (1335a0f, 20:07).
- Each pattern's do_this is in the design:
  - **P11:** the permutation null, plus the hub held each way.
  - **P3:** the oriented dumb rules are inside the rule.
  - **P1:** the move from 0.41 to 0.01 is reasoned from the dry run, though that reasoning rests on uncommitted code (F-A).
  - **P2:** the gap is stated.
  - **P8:** the arms differ only in the kernel.
  - **P9:** the §5 sentences are written (F-B is one phrase in them).
  - **P10:** both leave-out checks are in.

**Pinning at 680f128, and the provenance of labels and edges.** Pinning is sound:
- 680f128 is the input em-qwalk froze before any score, and both reviews examined that graph.
- The only change since then to a node of the pinned graph is `bmq`'s status. I checked parent, status, bets and source for all 41 nodes, printing only what changed.
- No `em-*` bet row was edited between 680f128 and 1f6887d, and none of the 19 `em-*` rows has `verdict_after_audit` different from `verdict`.
- The 18 bmq-scout nodes postdate the question (st-13, 18:00) and carry reading-stage labels rather than tested ones, so leaving them out is the conservative choice. It is not a choice made from scores, since none exist.

Labels and edges made after, or because of, outcomes:
- **Labels.** Each label is its own direction's test outcome (map status at the row where it resolved, or its own bet's verdict). None is set from a neighbour's outcome, and no audit changed one.
- **Edges cut by the prospective sensitivity.** Follow-up and replication edges exist because of the parent's outcome: gm2b and dm4 under gm2; gm3c and dm2 under gm3; dm3 under gm1; bm0 under bm1; g opened at 15:15 under h2, which resolved at 15:14. Most of all, `oe`'s 19-way star exists because `oe` hit (its map result reads "The live finding grew from here"). For a child, its edge to the parent carries an outcome known before the child opened, which is legitimate. For the parent, the edge carries a later outcome, and that is exactly what the prospective cut removes when the parent is scored.
- **Edges not cut by the prospective sensitivity.** The 3 rule-2 edges (h2–h34, g–h34, e5–oe) join directions whose outcomes were written in the same `record.md` row. They are made at outcome time. The parent-links-only sensitivity removes them, but never together with the prospective cut.
- **Recommendation, not required:** add a reported row "prospective, parent links only" (the prospective cut applied to the parent-only graph). §6 already says the prospective cut cannot remove every outcome-made link.

**Rule 6 and hardware. Hold.** The bet uses no model answer, claim web or circuit; it predicts outcomes of the research record. It is laptop numpy only, with 0 QPU s, and makes no "quantum advantage" claim.

## Required fixes

All three go in **one dated DEVIATIONS row** (the next free number), written before any data, naming `ledger/design-reviews/em-qwalk2-1b.md`. None changes the statistic, the rule's bar or the inputs.

**F-A (D4/D10). Commit the planted-kernel worlds, and correct the claim drawn from them.**
- Add the planted-world dry run that produced §4's last two rows to `qwalk2.py`, for example a `--dry-run-planted 680f128` that uses only the real links and the settled set. Its output must regenerate those rows.
- In the DEVIATIONS row, replace "so a 'classical' verdict essentially cannot happen" with: *"In the classical world built that way the arms tied; in a classical world grown from a few sources (reviewer 1b), the rule said classical 5% of the time. Neither arm wins by construction, and each wins rarely in its own world."*
- If the committed planted runs move the quantum-world pass rate materially (mine: 3.2% with no noise, 1.4% with 10% flips), restate the odds as a revision before data, keeping both numbers.

**F-B (D8). One phrase in the pass sentence.** Replace *"It also beat chance and every one-line rule, each judged against shuffled outcomes."* with *"It also beat chance, judged against shuffled outcomes, and each of four one-line rules (the date bit, the neighbours' vote, the number of links, the number of follow-ups)."* Mirror the change in the classical sentence.

**F-C (D10). The gate reads every `em-qwalk2*.md`.**
- In `review_says_go()`, select files with `f.startswith("em-qwalk2") and f.endswith(".md")`, not the narrower regex.
- Keep the two required names.
- Refuse on any matching file whose YAML header has no parseable `verdict:` line, so that a stray or misnamed review cannot be skipped.
- Addenda go inside the review file they confirm, as design-review.md already says.

When the DEVIATIONS row and the code changes are committed, I confirm them in an addendum to this file and set `confirmed_at`. Until then, `--run` must not start.
