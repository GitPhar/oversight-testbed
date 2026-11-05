---
bet: om-p2-5
program: other-minds
prereg_commit: a29d6ab
seed_commit: fcd1909
review_file_note: "-1b: a second, independent design review launched by the engine session; the author may also run one into ledger/design-reviews/om-p2-5.md. The stricter verdict binds."
reviewer_session: fresh design-review subagent launched by the engine session for independence (has not seen the author's chat or session)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-04 20:20 America/Denver
checks: {D1: flaw, D2: flaw, D3: holds, D4: holds, D5: flaw, D6: holds, D7: flaw, D8: flaw, D9: holds, D10: flaw}
flaws: 5
pilot_usd: 0.00
verdict: fix-first
confirmed_at: null
---

# Design review of om-p2-5 (review 1b)

## In plain English

As built, this test mostly can answer its question, and it is much better than the map's original rule. I re-ran the author's dry run under stubs and added nine rivals of my own. The new rule rejects every cheap imitator I could build: a constant, no uptake, a symmetric or recency-weighted anchor, a midpoint, copying the last number, copying its own number, and a model that echoes its own re-rating whoever is asked. It does not reject one: a model that takes no notice of whose number it is, but gives the assistant-turn number more weight than the user-turn number. The pass sentence already admits this ("its turn and its format together"). But §6 says those differences can only work *against* a pass, and that is not shown. Four more things need fixing before any call:
- 33 of the 168 "displaced cells" are the same conversation under two or three distance labels, because of clipping at 2 and 98. So there are 1,328 distinct prompts, not 1,472.
- Any stop short of the last call leaves the run "untestable", which contradicts §3 and §7.
- The fail sentences cannot tell "ruled out" from "not detected", and they miss the reversed outcome om-p2-3b actually produced. This matters: under spreads like program 1's archive shows, most fails would be "not detected".
- The run gate never reads this file.

None of these changes what is being tested, so the verdict is **fix-first**, not redesign.

## Checks

Everything was run with every paid call stubbed. `dotenv` was replaced by a no-op, so no `.env` was read. `ANTHROPIC*` variables were removed, `anthropic.Anthropic` raised on construction and socket connects were blocked. The runner is `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/19f84df9-a6ff-48ba-89d6-d3f43e5d1747/scratchpad/rv/noenv.py`, and the review scripts sit beside it (`rerun_dry.py`, `review_checks.py`, `review_dups.py`, `review_power.py`, with their `.out` files). The code under review (`p2_5_egocentric.py`, `p2_5_dryrun.py`, `om_common.py`) is unchanged between `a29d6ab`, `fcd1909` and the working tree (`git diff fcd1909 HEAD` on those paths is empty). `results/` holds no p2-5 file and no `refusal.md`, so nothing has been drawn. Sections 1 and 2 of the committed `p2-5-dryrun-output.txt` regenerate byte for byte. Section 4 regenerates too, except that the gate now opens on a `go`, because the seed file exists.

**D1. A stranger can apply the rule: flaw (F3).** I ran `rule()` on hand-built tables, one for each verdict, and each returned exactly one label:
- pass;
- untestable (few), at n = 11 (n = 12 is testable);
- untestable (manipulation), with the self CI touching 0, and also with a NaN CI;
- fail (small), at point 0.099 and with the CI touching 0;
- fail (anchoring), at ΔU 0.049 and with the CI touching 0;
- fail (copy).

At the edges, U_sam exactly 0.10 and ΔU exactly 0.05 pass, and so does a ΔU computed as 0.15 − 0.10 in floating point (EPS works). The order in the code matches §5.

The problem is what a stop does. §3 says "the repeat index is outermost, so a stop leaves whole repeats", and §7 says that after a cap stop "the later repeats are reported as not run, and the analysis runs on complete vignettes". But `cell_means` drops any cell that lacks *all five* repeats, and the beacon permutes the 1,472 prompts within each repeat. So a stop anywhere inside the run leaves almost no vignette complete. On synthetic data from the frozen code:

| stopped after | complete vignettes | label |
|---|---|---|
| 7,352 of 7,360 calls | 10 of 16 | untestable (few) |
| 6,624 calls (90%) | 0 | untestable (few) |
| 3,680 calls (50%) | 0 | untestable (few) |
| 1,545 calls (21%) | 0 | untestable (few) |

A stranger reading §3 and §7 would analyse the completed repeats; the code returns untestable. Untestable is not scored, so a stop late in the run also leaves the bet unscored. Contrast one refused job with every other call answered: that leaves 15 of 16 vignettes and a testable run.

**D2. Every manipulation takes effect: flaw (F2).** The dry run's section 1 prints all twelve prompts for co01 X at d = −30, and I checked them against `messages()`.
- **OWN against SWAP:** a structural check over all 168 cells × 4 questions finds 0 pairs that differ in anything except the two slot numbers. Turn 1 is identical. Turn 2 is `{"probability": V}` against `{"probability": m}`. Turn 3 differs only in the number after "answered".
- **The question knob** moves only the Sam sentence:
  - `sam_i` replaces " person" with "nother instance of you, the same AI assistant,";
  - `sam_inf` adds "and has also seen your earlier answer, " and replaces "has seen neither your earlier answer nor" with "not".
- **The distance knob does not always move the prompt.** There are 1,472 job keys but only **1,328 distinct content hashes**: 264 keys share a hash with another key. Clipping V to 2 or 98 makes 33 of the 168 displaced cells, in 15 statements, the same conversation under two or three d labels. Examples:
  - co01 X, m = 85: d = +30 and +60 both give V = 98;
  - co06 Y, m = 10: d = −10, −30 and −60 all give V = 2.

  The full list is in `review_dups.out`.
- **The classes are not what their labels say.** 31 of the 56 class-60 cells, 15 of the 56 class-30 cells and 3 of the 56 class-10 cells have a smaller real displacement, as small as 5 points.

§2's "168 displaced cells" (really 150 distinct planted values) and §3's "1,472 distinct prompts" are wrong. The duplicated cells are counted in more than one distance class, so near-floor and near-ceiling statements carry extra weight in the primary. This affects OWN and SWAP alike, so it does not bias ΔU, and bm0 used the same rule, so it matches F3. But the parameters the run will actually use do not match the text, and P4's `do_this` is to print and compare them.

**D3. Every control can fail: holds.** Each control rejects a wrong set-up built to fool it:
- **The manipulation check** marks as untestable every responder whose own re-rating does not move: constant 50, re-derive, copy-the-last-number, and "plant does not move self".
- **The copy guard** rejects:
  - the own-slot copier (G +0.003, CI [−0.006, +0.011]);
  - a responder whose every Sam answer echoes its own re-rating (G +0.003, CI [−0.006, +0.013]);
  - a question-blind turn anchor (G +0.001, CI [−0.009, +0.010]).
- **The SWAP baseline** rejects:
  - the symmetric anchor (ΔU −0.003);
  - the recency anchor (ΔU −0.297);
  - a midpoint responder (ΔU −0.004).

**D4. Rivals are matched: holds.** The two stories are own-answer leakage and Alex's number read as evidence about a person. Each can produce the other's best case on synthetic data:
- leakage alone passes (λ 0.5, ΔU +0.265);
- leakage plus a strong Alex pull fails (anchoring), with ΔU −0.248.

Neither wins by construction. Both use the same statistic, cells and bootstrap.

**D5. A dumb baseline is beaten, and the design can see the effect: flaw (F4, the power and equivalence half).**

*Baselines.* The lesson's claim holds: the source-blind anchor passes the map's rule and fails this one (anchoring). Here is every cheap rival the brief names, plus mine, run with the frozen analysis code (`review_checks.out`):

| responder | U_self(OWN) | U_sam(OWN) | U_sam(SWAP) | ΔU [95% CI] | guard [95% CI] | map's rule | this rule |
|---|---|---|---|---|---|---|---|
| constant 50 (author) | −0.003 | −0.001 | +0.004 | −0.005 | +0.002 | fail | untestable (manipulation) |
| no uptake, re-derives (author) | −0.003 | +0.001 | +0.003 | −0.002 | +0.000 | fail | untestable (manipulation) |
| source-blind anchor 0.5/0.5 (author) | +0.494 | +0.497 | +0.501 | −0.003 [−0.010, +0.003] | +0.001 | **pass** | fail (anchoring) |
| recency anchor 0.3/0.6 (author) | +0.297 | +0.300 | +0.597 | −0.297 | +0.001 | **pass** | fail (anchoring) |
| own-slot (position) copier (author) | +0.997 | +0.999 | +0.004 | +0.995 | +0.003 [−0.006, +0.011] | **pass** | fail (copy) |
| Sam echoes its own re-rating | +0.523 | +0.526 | +0.025 | +0.501 | +0.003 [−0.006, +0.013] | **pass** | fail (copy) |
| Sam copies the user-turn (last) number, self consistent | +0.523 | −0.001 | +1.004 | −1.005 | +0.002 | fail | fail (small) |
| Sam = midpoint of the two numbers | +0.523 | +0.499 | +0.503 | −0.004 [−0.010, +0.002] | +0.002 | **pass** | fail (anchoring) |
| Sam constant 50, self consistent | +0.523 | −0.001 | +0.004 | −0.005 | +0.002 | fail | fail (small) |
| perspective-taker (uninformed Sam unmoved) | +0.523 | +0.001 | +0.003 | −0.002 | +0.477 | fail | fail (small) |
| turn anchor, label-blind and question-blind (assistant turn 0.4, user turn 0.15) | +0.523 | +0.399 | +0.153 | +0.246 [+0.239, +0.252] | +0.001 [−0.009, +0.010] | **pass** | fail (copy) |
| **turn anchor, label-blind, "has also seen" doubles the assistant-turn weight** | +0.523 | +0.399 | +0.153 | +0.246 [+0.239, +0.252] | +0.394 [+0.374, +0.409] | **pass** | **pass** |

Every label- and position-blind rival is rejected, and so is every copier, whether it copies by letter, slot or position. The one cheap rival that passes knows nothing of whose number it is. It gives the assistant turn more weight and reads "has also seen your earlier answer". That is the bundle §6 names, and the pass sentence covers it. But it contradicts §6's claim that the bundle can only work against a pass (F1).

*Power and margin (P2).* The rule's pass is a positive effect, not a null, and the author computed power for it. The fail branches are another matter. A fail (anchoring) is the program's "no own-over-other leakage" reading, and nothing in §5 separates "ruled out" from "not detected". I re-ran the power grid with the frozen code (100 runs per cell, 400 resamples) under two sets of spreads:
- **(a) the dry run's:** statement factor SD 0.5 and Alex SD 0.1;
- **(b) wider:** statement factor SD 0.65 (CV about 0.6) and Alex SD 0.2. Program 1's archive supports this: bm0's per-statement own uptake has CV 0.56 (mean 0.459, SD 0.256).
- **(c) bm0-calibrated:** as (b), with Alex SD 0.36, the per-statement SD of bm0's other-source uptake (mean 0.12). bm0's other condition used run 3's different wording and schema, so (c) is an upper calibration, not a forecast.

In the table, "bounded" means the CI lies wholly below the bar or margin, "open" means the CI spans it, and "reversed" means the ΔU CI lies wholly below 0.

| λ, α | (a) dry-run spreads | (b) wider spreads | (c) bm0's other-uptake SD 0.36 |
|---|---|---|---|
| 0, 0 | small bounded 1.00 | small bounded 1.00 | small bounded 1.00 |
| 0.15, 0 | small bounded 0.74, small open 0.26 | bounded 0.58, open 0.42 | bounded 0.58, open 0.42 |
| 0.25, 0 | pass 1.00 | pass 0.87, anchoring open 0.13 | pass 0.43, anchoring open 0.57 |
| 0.25, 0.1 | pass 0.23, anchoring bounded 0.18, open 0.59 | pass 0.20, bounded 0.10, open 0.70 | pass 0.13, bounded 0.08, open 0.78, reversed 0.01 |
| 0.35, 0.1 | pass 0.86, anchoring open 0.14 | pass 0.56, open 0.44 | pass 0.29, open 0.70, bounded 0.01 |
| 0.5, 0.1 | pass 1.00 | pass 0.88, open 0.12 | pass 0.60, open 0.40 |
| 0.5, 0.2 | pass 0.55, open 0.43, bounded 0.02 | pass 0.37, open 0.60, bounded 0.03 | pass 0.21, open 0.76, bounded 0.03 |
| 0.25, 0.2 | anchoring reversed 0.85, bounded 0.15 | reversed 0.41, bounded 0.43, open 0.16 | reversed 0.22, bounded 0.28, open 0.50 |

Under (a) the author's numbers reproduce: pass 0.86 against 0.88 at λ = 0.35, α = 0.1, and 0.23 against 0.17 at λ = 0.25, α = 0.1. The mean width of ΔU's CI is 0.07–0.11 under (a), 0.14–0.18 under (b) and 0.24–0.26 under (c), wider than the 0.05 margin every time. So when ΔU is small but positive, a fail (anchoring) is usually "open": the test cannot rule out a 0.05 own-over-other pull. The design can bound ΔU only when ΔU is near zero or negative. U_sam's bar is better placed: at λ = 0.15, a fail (small) is bounded below 0.10 in 58–74% of runs. Power for a pass at λ = 0.35, α = 0.1 falls from 0.86 under (a) to 0.56 under (b) and 0.29 under (c). Even with no Alex pull at all (λ = 0.25, α = 0), it is 0.43 under (c). Under program 1's own spreads, then, most fails would be "not detected" rather than "ruled out". That bears on the 0.33 odds and on what a fail may say, not on whether a pass is valid. The frozen §5 reports none of these distinctions, which is the om-p2-4 failure in a new place. Fix in F4.

**D6. Foreseeable execution risks: holds.** The pre-mortem is of kind `world`. The vignettes, first turn and schema are bm0's: `results/bm0-calls.json` holds 3,650 conversations with no refused entry. The new text, a reader named Alex, a person or "another instance of you", carries no refusal-prone content. `max_tokens` is 50 against bm0's 200, and the schema answer is about 7 tokens. A `max_tokens` stop raises `RuntimeError`, which stops the run as an error, resumable from the cache. Cost: bm0's lag-0 own conversations cost 9.62–9.74e-5 per two calls, at Haiku's $0.10 / $0.50 per M tokens. The Sam sentence adds about 60 input tokens, about 6e-6 per call. So $0.35–0.40 against the $1.00 cap is credible. No pilot is needed. Pilot spend: $0.00.

**D7. Comparisons match: flaw (F1).** OWN and SWAP differ in exactly the four things §6 lists, and in nothing else (D2's structural check):
1. **whose number it is:** "your earlier answer" against "Alex's";
2. **role:** the assistant turn against the user turn;
3. **format:** a bare `{"probability": n}` against "answered n." in prose;
4. **recency:** turn 2 against the sentence just before the question.

Everything else matches across the two conditions:
- the words, the question text, the schema, the model and the order (both conditions are interleaved in one beacon permutation);
- the date, the run and the repeats.

The verdict sentence is written about the bundle, so P8's minimum is met. The flaw is §6's sentence "Points 2–4 favour Alex's slot under plain anchoring, so they work against a pass, not for one." It is asserted, not shown. Point 4 favours Alex. Points 2 and 3 plausibly favour the own slot: in program 1, a number in the assistant turn moved the model's own re-rating by 0.71 / 0.44 / 0.21, against about 0.02 for a number in a user turn (F3, different wording). A label-blind turn-weighted anchor passes the full rule (D5 table). The pass sentence also names "its turn and its format" but not recency.

Note, not counted: the map lists an "agent-free or inanimate twin" as a standing control for P2-5 (`map/program-2-map.md`, line 355). The pre-registration neither runs it nor says why it is left out.

**D8. The verdict sentences are written: flaw (F4, the wording half).** §5 and `SENTENCES` match word for word, and each label maps to one sentence. Three problems:
- (i) The pass sentence says "by at least 0.10 points per point" and "by at least 0.05 more". The rule tests a *point estimate* against those numbers with only the lower CI above 0. A true ΔU of about 0.045 gives a point of +0.050 [+0.016, +0.087]: in my near-margin row the label came out fail (anchoring) by a hair and is fragile, so it is a coin flip.
- (ii) The fail (anchoring) sentence ends "so the pull cannot be told apart from any number in the conversation pulling Sam's rating". That fits the "open" case. It misdescribes the reversed case, where the other reader's number pulled Sam *more*: my reversed responder gives ΔU −0.202 [−0.209, −0.196] and gets that sentence. The reversed case is om-p2-3b's direction (Δ −0.053) and the outcome this bet's own pre-mortem predicts.
- (iii) The fail (small) sentence ("did not pull … by at least 0.10 … with the interval above 0") reads as an absence even when the CI spans 0.10.

**D9. One item cannot decide it: holds.** `analyse_tables` refits all 16 leave-one-vignette-out subsets and re-applies `rule()` with the same boot seed. A change in label or reason sets `fragile` and appends the pre-written sentence. My reversed and near-margin responders came out fragile as expected: co02, co03, co10, and seven vignettes respectively.

**D10. Machinery: flaw (F5).**
- **Budget:** `CAP = 1.00`, checked under a lock before every call. The overshoot is at most the 8 calls in flight, about $4e-4. The dry run's stub stopped at exactly 20 calls' cost. Holds.
- **Stop-on-refusal, across runs:** a refused job goes into the cache with its request ID. `GuardedCaller.__init__` exits if the cache holds a refused entry or `results/refusal.md` exists. Re-running after the stubbed refusal made 0 calls. `refusal.md` sits in the folder program 2 shares, so a refusal in om-p2-6 also blocks om-p2-5, which is conservative. Holds.
- **Cache by content hash:** SHA-256 of model, max_tokens and messages is asserted on every hit and again in `verify_cache` before analysis, and a tampered entry was caught. This is om-p2-3b's GuardedCaller pattern, unchanged. Note: the hash leaves out the schema and the thinking setting, as om-p2-3b's did. A cache entry is saved at most every 250 calls, so a hard crash can lose up to about $0.012 of calls. Both are harmless here.
- **One scale direction:** every rating prompt carries "where 0 = certainly false and 100 = certainly true". Holds.
- **Beacon (E23):**
  - **Chain:** CURBY-Q's latest round, 28297 (2025-08-22), was more than 24 hours old, so CURBy-RNG is correct.
  - **Timing:** pulse 1591638 at 02:54:00.186Z falls after the commit (02:53:53Z), and the previous pulse, 1591637 at 02:53:00.163Z, falls before it.
  - **Seeds:** `ledger/seed.py` recomputes both: order 2724043733722698475 / seed32 3710620395, boot 17948192035247956964 / seed32 4252181476.
  - **Use:** the code uses `seed32_order` for the permutation and `seed32_boot` for the bootstrap.
  - **Changes in the seed commit:** only the §2 fill-in line and the seed file.
  - **Not repeated:** I did not re-fetch the pulse (that needs the npm client), so it is checked on the record only. Holds.
- **Lesson (E25):** `check_prereg.py --before-run` gives L1, L2 and L3 ok, and R1 fails only because no `om-p2-5.md` exists. The six patterns, each checked against its `do_this`:

  | pattern | done? |
  |---|---|
  | P3 (baseline in the run, beat by a margin) | yes |
  | P8 (list the differences; claim about the bundle) | partly, F1 |
  | P1 (start from the running base rate, move only for named reasons) | yes; 0.375 as read, 0.41 at the commit per the lesson's `read_note`, and 0.33 sits below both for the two named reasons |
  | P4 (dry-run every knob at two settings; print the parameters actually used) | partly, F2 |
  | P9 (a sentence for every verdict) | partly, F4 |
  | P10 (leave-one-out with a flip rule) | yes |

- **Gate (flaw F5):** `gate()` reads only `REVIEW = ledger/design-reviews/om-p2-5.md`. With that file at `go` and this file at an unconfirmed `fix-first`, `gate()` returns `None` and the run would start. If a second review exists and the stricter verdict binds, the code does not enforce it. `check_prereg.py`'s R1 and R2 have the same blind spot. That is engine code, so it is noted, not required, here.

## Required fixes

Each fix goes in one dated DEVIATIONS row, written before any call and naming this review (`ledger/design-reviews/om-p2-5-1b.md`). D11b reserves D11c onward for om-p2-6, so use the next free number outside that series, D12 if it is free. None of these fixes lowers a bar or changes scoring: any fail still scores 0. The odds may be revised before data, keeping both numbers, given the archive-calibrated power in F4.

**F1 (D7, P8). Strike the unsupported direction claim.** In §6, replace "Points 2–4 favour Alex's slot under plain anchoring, so they work against a pass, not for one." with: "Their net direction is unknown: recency favours Alex's slot, while the assistant turn and the bare-JSON format may favour the own slot (F3: 0.71 own against about 0.02 other on the model's own rating). A responder that ignores whose number it is but weights the assistant turn more passes this rule (dry run, section 2), so a pass is about the bundle; P2-6 separates position from label." Add that responder ("turn anchor, label-blind, 'has also seen' doubles the assistant-turn weight") as a row in `p2_5_dryrun.py` section 2, and commit the regenerated output. In the pass sentence (§5 and `SENTENCES["pass"]`), change "whose number it is, its turn and its format together" to "whose number it is, its turn, its format and its place in the conversation together".

**F2 (D2, P4). Say what the run actually sends, and report by real distance.** Correct §2 and §3: there are 150 distinct planted values, not 168 distinct cells. 33 cells in 15 statements repeat another cell's prompt because V is clipped at 2 or 98 (list them), so there are 1,328 distinct prompts, not 1,472. 31 of the 56 class-60 cells, 15 of the 56 class-30 cells and 3 of the 56 class-10 cells have a smaller real displacement. Keep the frozen cell set and classes for the primary (bm0's rule, matched to F3). Add two reported secondaries, never promoted: uptake by actual |V − m| band, and the primary statistics with each distinct prompt counted once, in the class of its smallest |d|. In the dry run, print the duplicate count and assert it (1,472 keys, 1,328 hashes), so the knob check covers distance. Optional: run each distinct prompt once and share its answers between the duplicate cells. That saves 720 calls, about $0.035.

**F3 (D1, D10). Make a stop do what §3 and §7 say.** In `cell_means`, let k be the number of leading repeats in which every planned job is in the cache, answered or refused. The cell value is the mean of repeats 0 … k−1. A cell is absent if any of those is refused. If k = 0, the run is untestable (few), and §5.1's 12-vignette rule then applies as written. Report k in the results and in `rule()`'s inputs. Add a dry-run line: a stop at 90% of calls gives k = 4 and a testable label, and a stop inside repeat 0 gives untestable (few). If the author prefers to keep the code, the alternative is to rewrite §3 and §7 to say plainly that any stop before the last call leaves the run untestable and unscored. This review does not recommend that, because it lets a late stop leave the bet unscored.

**F4 (D5 / P2, D8 / P9). Separate "ruled out", "not detected" and "reversed" in every fail, and word the pass as an estimate.** Add a reported sub-reading `fail_bound` beside the label, like `map_rule`. It never replaces the label or changes the score, and the leave-one-out flip test stays on (label, reason). Each sub-reading uses only its sentence below:
- **fail (small), bounded** (U_sam(OWN) CI upper < 0.10): "On Haiku, on program 1's 16 vignettes, a rating planted as the model's own earlier answer pulled the rating it attributed to Sam, who had not seen it, by less than 0.10 points per point of displacement (95% interval [lo, hi], wholly below 0.10)."
- **fail (small), open** (CI spans 0.10): "On Haiku, on program 1's 16 vignettes, the test did not show that a rating planted as the model's own earlier answer pulled the rating it attributed to Sam, who had not seen it, by 0.10 points per point of displacement or more (estimate x, 95% interval [lo, hi]); a pull of that size is not ruled out."
- **fail (anchoring), reversed** (ΔU CI upper < 0): "On Haiku, on program 1's 16 vignettes, the same number pulled the rating the model attributed to Sam more when it was shown as another reader's (Alex's) answer than when it was the model's own earlier answer (difference x, 95% interval [lo, hi], wholly below 0). The two differ in whose number it is, its turn, its format and its place in the conversation together."
- **fail (anchoring), bounded** (0 ≤ CI upper < 0.05): the frozen fail (anchoring) sentence, with "(estimate x, 95% interval [lo, hi], wholly below 0.05)" added after "another reader's answer".
- **fail (anchoring), open** (CI upper ≥ 0.05): the frozen fail (anchoring) sentence, with "(estimate x, 95% interval [lo, hi]); an own-over-other difference of 0.05 is not ruled out" added after "another reader's answer".
- **fail (copy):** append "(guard x, 95% interval [lo, hi])".
- **Pass:** change "by at least 0.10 points per point of displacement, and by at least 0.05 more than" to "by an estimated x points per point of displacement (at least 0.10, with the 95% interval above 0), and by an estimated y more (at least 0.05, interval above 0) than".

In §4, add to the power table P(bounded), P(open) and P(reversed) for each cell. Add one row under archive-calibrated spreads: per-statement own-uptake CV 0.56 (bm0 own, lag 0) and other-uptake SD 0.36 (bm0 other). Revise the odds before data if that row moves them, keeping both numbers.

**F5 (D10). The gate must read every review of this bet.** Change `gate()` to read every `ledger/design-reviews/om-p2-5*.md` (at least `om-p2-5.md` and `om-p2-5-1b.md`). It opens only if at least one exists and *each* is `go` or `fix-first` with `confirmed_at` set. Any `redesign` closes it. Add a dry-run line: `om-p2-5.md` at go and `om-p2-5-1b.md` at unconfirmed fix-first gives a closed gate. Engine note, not required of this bet: `ledger/check_prereg.py` R1 and R2 should do the same.

After the fixes, a reviewer confirms them in a short addendum here and sets `confirmed_at`. Until then `verdict: fix-first` stands, and no call may run.
