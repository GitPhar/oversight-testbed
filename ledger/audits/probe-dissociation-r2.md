---
bet: probe-dissociation (DP1), second round; DP2 freeze checked
program: entangled-mind (gold map direction 5)
prereg_commit: 9ef909d (DP1, 07:39:41); DP2 d7de8a2 (probes branch, 14:34:35)
results_commit: 8685008 (DP1, 09:18:09); D53 marking 2161329 (13:19); state audited at main 9042d7f
auditor_session: audit2 lead auditor (branch audit2)
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5 (commit trailers)
same_model_family: true
date: 2026-11-04 15:20 America/Denver
claims_checked: 14
holes_found: 4
overclaims_cut: 4
reproduced: true
verdict_claimed: mixed
verdict_after_audit: untestable
verdict_stands: false
canary: unknown
false_alarms: 0
failed: true
failure_reason: step 3 reused the gate's seeds, so its ratings replayed the selection data and the test was not independent
failure_kind: execution
premortem_score: null        # pre-registration predates operators/premortem.md (e287cb3, 14:41); it has no pre-mortem
risk_seen: null
---

# Second-round audit of probe-dissociation (DP1), after D51 and D53

The first audit (`audits/probe-dissociation.md`) was written on the unmerged `probes` branch. Since then:
- the branch was merged (`3992ad1`) with its D48 renumbered DP1;
- the cut pass (D51) edited the results file;
- D53 marked the result **unverified** and queued a fresh step 3;
- that step was frozen as DP2 (`d7de8a2`, probes branch, 14:34:35) and was **running while this audit was written**: its process started 14:34:39, 4 s after the freeze, writing `results/probe-dissociation-llama3-8b-run-2.json`.

This audit checks the current text, the D53 marking and the DP2 freeze. DP2's result is audited separately if it lands (`audits/probe-dissociation-dp2.md`).

## In plain English

The D53 marking is accurate:
- I re-verified the replay: all 500 shared gate/step-3 keys have identical sub-ratings and M ratings.
- The banner, README:31, the morning brief and gold-map §5 all say "unverified".
- The figure title now says "unverified, D53".

The first round's three listed cuts were applied as written. The text now says "undetermined" where it said "move independently".

Four things are still wrong or missing:
1. **A sentence contradicts the file's own numbers.** `:116` says "the orderings move it more than testimony does relative to that low range". But `:82–85` say order moves the probe 6% of its gap, testimony 12%, "about half as far". This was in the original text; the first audit missed it.
2. **Three first-round holes never became cuts and are not in the file:**
   - the gate passes only uncorrected (2 of 10 under Holm);
   - under the alternative scalings the probe moves *less* than the rating (Q ≈ 0.57 and 0.72);
   - r without h191 is +0.75, and with items held fixed r is [+0.04, +0.57], which is positive.
   The file keeps "in told-range units, the probe moves more than the rating" as its quantitative headline, with no counter-scaling.
3. **`:112` reads a probe as a belief.** "The internal truth signal for the main statement is *not* a fixed belief" names the probe reading a belief. The same bullet list, at `:116`, suggests it "reads stored knowledge more than in-context belief".
4. **README:31, brief:122 and gold-map:270 say the fresh run is "queued".** It was frozen and started at 14:34 on `probes`. That is stale, not wrong when written.

Until DP2 reports, the verdict is **untestable** in the ledger's sense: the label exists, but its test was not independent of selection.

## The case that this result is false

The label PROBE MOVES, BUT NOT WITH THE RATING has two halves.

The first half, "probe moves" (p_P = 0.0001), is a fresh measurement: the probe was not read at the gate. But it is measured on the three items chosen because their *ratings* moved most. And it is 6% of the probe's true–false gap, from a probe that moves only 12% of that gap when told the answer outright. A probe this weakly coupled to context, which still reads the yes-statement as "true" on 80% of told-no trials (first audit, row 6), may be tracking surface features of the preceding text. If so, "the internal truth signal is not a fixed belief" is a statement about a probe direction, not about belief.

The second half, "not with the rating", is a CI that includes 0 on 12 cells from 3 items. Two items track strongly (+0.73, +1.00), and holding items fixed the CI is wholly positive. So the label could be "probe moves, and with the rating" as easily as not.

And the verbal half of the test replayed the selection data, so nothing in step 3 independently confirmed the gate. The case is that neither half of the label is established. The D53 "unverified" marking concedes the second and third points.

## Claims checked

| # | claim (current `results/probe-dissociation.md` unless noted) | check | outcome |
|---|---|---|---|
| 1 | banner: "500 of 500 identical" | compared `…-gate.json` with `…-run.json` keys and ratings | holds: 500 shared keys, 500 identical (sub-ratings and M) |
| 2 | banner: "Validity check V4 therefore tested nothing" | follows from 1 | holds |
| 3 | banner: "A fresh step 3 … is queued … to be frozen as DP2 before it runs" | probes branch `d7de8a2` 14:34:35; process start 14:34:39 | holds as written at 13:19; now stale (frozen and running) |
| 4 | figure title changed (D53) | `probe_dissociation_figure.py:49`, svg | holds: "(in told-range units; unverified, D53)" |
| 5 | round-1 cut at :13 (probe "by more") | text :15 | applied as written |
| 6 | round-1 cut at :14 ("move independently") | text :16 | applied as written |
| 7 | round-1 cut at :16 ("not a stable belief…") | text :18 | applied as written |
| 8 | :45 "Llama's spans are comparable to Haiku's on most items" | first audit row 3 (7 of 10 at least as large) | holds |
| 9 | :116 "the orderings move it more than testimony does relative to that low range" | :82–85 of the same file | **contradicted**: order 6% of the gap, told 12%; ":85 Yet order moves it about half as far as testimony does" |
| 10 | :112 "the internal truth signal … is *not* a fixed belief under an order-dependent readout" | first audit rows 6, 7; :116 | **overclaim**: the probe reading is not invariant to order; "belief" is the open question (:116) |
| 11 | :43 "The gate passes on Llama, at exactly its threshold" | first audit hole 4; DP2 §6 reproduces "under Holm, 2 of 10" | holds as the frozen (uncorrected) rule; **omission**: the Holm result is not stated |
| 12 | Q row "in told-range units, the probe moves more than the rating" | first audit row 11; DP2 §6 reproduces Q_sep 0.57, Q_b0 0.72 | holds in its units; **omission**: under both alternative scalings the probe moves less |
| 13 | :16 "two track closely, one does not" | first audit row 12; DP2 §6 reproduces r without h191 +0.75, items-fixed [+0.03, +0.55] | holds, but the items-fixed interval (wholly positive) is not stated |
| 14 | README:31, brief:122, gold-map:270 mark DP1 unverified | grep | holds |

## Checklist (changes since round 1 only; round 1's A1–D22 stand)

- **A1–A4.** Unchanged (DP1 pre-registration holds; timing not checkable beyond git order).
- **B7 few items.** Unchanged: r's interval is set by h191 (round 1). Still not stated in the file (row 13).
- **B9 baselines / units.** **Hole, carried over.** The Q headline uses the one scaling under which the probe moves more (row 12).
- **B11 multiple comparisons.** **Hole, carried over.** The gate is uncorrected over 10 tests and fails under Holm (row 11).
- **C15 mechanism.** **Hole.** "Belief" for a probe direction (row 10).
- **C16 plain English vs table.** **Hole.** Row 9 contradicts the file's own numbers.
- **D22 replication.** DP1 is unverified, and DP2 is the replication. **DP2 freeze, checked:**
  - It is in its own commit, before any fresh conversation.
  - The replay check runs first, with a stop rule (> 50% identical → stop), and the namespace leaves 0 of 700 seeds shared.
  - DP1's `compute()` and rule are unchanged.
  - The secondaries include every first-round counter-scaling (Holm gate, Q_sep, Q_b0, r without h191, items-fixed r).
  - The output names were changed from the queue's `-fresh` to `-run-2`, with the reason given.
- **Design weakness to state before DP2 reports.** With three gate items, r's percentile interval is close to the range of the three per-item r's (round 1, hole 2). So the label "NOT WITH THE RATING" is close to guaranteed whenever V4 passes and any one gate item fails to track. "DP1 VERIFIED" would therefore mean the label replicated. It would not mean that independence of probe and rating was shown. DP2's pre-registered items-fixed interval (secondary E) is the informative number.

## The pre-mortem, scored

The pre-registration has no pre-mortem: it was frozen before `operators/premortem.md` entered the standard (`e287cb3`, 14:41). So `premortem_score: null`. The auditor's own one-line failure account is in the front matter (`failure_reason`, `failure_kind`).

**E23–E24.** Not applicable: no beacon seed, and not a tiebreak bet.

## Required cuts

- `results/probe-dissociation.md:116`: "So its in-context sensitivity is low, and the orderings move it more than testimony does relative to that low range." → "So its in-context sensitivity is low. Order moves it about half as far as testimony does (6% against 12% of its true–false gap)."
- `results/probe-dissociation.md:112`: "On this model, the internal truth signal for the main statement is *not* a fixed belief under an order-dependent readout, which was the gold map's \"clean dissociation\"." → "On this model, the truth-probe reading for the main statement is not invariant to chain order (about 6% of its true–false gap), so the gold map's \"clean dissociation\" (an order-invariant probe under an order-dependent rating) was not seen. Whether the probe reads in-context belief is itself open (see below)."
- `results/probe-dissociation.md` Q row (step 3 table) or the paragraph after it: add "In units of each measure's true–false gap, the probe moves less than the rating: Q ≈ 0.57 (held-out separation against the 0–100 range) or 0.72 (B0 true-minus-false gaps)."
- `results/probe-dissociation.md:43`: append "Under a Holm correction across the ten items, 2 of 10 pass (h191, p = 0.013, fails), which would fail the gate; the frozen gate was uncorrected."
- `results/probe-dissociation.md:16`: append "Holding the three items fixed and resampling repeats only, r is +0.04 to +0.57; without h191 it is +0.75."
- `README.md:31`, `paper/morning-brief.md:122`, `paper/gold-map.md:270`: "a fresh run on new seeds is queued" → "a fresh step 3 on new seeds was frozen as DP2 (`d7de8a2`, branch `probes`) and run" (on merge of `probes`).

## What would break it next

DP2 is already the right test, at $0. The one addition worth pre-registering is an in-context probe control at $0: train the probe at layer 13 on statements *preceded by* a told-yes/told-no context, then rerun DP2's cells. If order still moves that probe by about 6% of its gap while it now moves most of its gap under testimony, the probe-moves half is about belief. If order's movement vanishes, it was about text.
