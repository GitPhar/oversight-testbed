---
bet: ss-b14
program: settled-science
prereg_commit: e3ed649
seed_commits: 35fc122, 338acdc   # seed and its correction (D64, D66)
reviewer_session: fresh design-review subagent launched by the engine session; no chat, transcript or author message read; worktree oversight-testbed-ss-wave4 at 1181659 (code unchanged since e3ed649 except the seed line)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true          # reviewer, author, bettor, flattery rater and leakage checker are all Claude models
date: 2026-11-05 10:28 America/Denver
checks: {D1: holds, D2: holds, D3: flaw, D4: flaw, D5: holds, D6: holds, D7: holds, D8: flaw, D9: flaw, D10: holds, D11: flaw, D12: holds}
prior_work_search: "language models predict study outcomes bias toward positive significant results publication bias shortcut original vs altered abstract" (one web search, 2026-11-05)
papers_opened: 2
flaws: 5
pilot_usd: 0.00
verdict: redesign
confirmed_at: null
---

# Design review of ss-b14

## In plain English

As built, this test cannot run. The items come from round 2's model-psychology arXiv query and window, taking results 600 to 1799. But that query has only **686 results** in the window (arXiv `opensearch:totalResults`, checked 2026-11-05 10:26). Round 2 already took the first 600.

I ran the free item steps the pre-registration allows after the seed commit:
- `--fetch` returned 86 papers: results 600–685, and the pages starting at 900, 1200 and 1500 were empty;
- `--build` made **9 candidate items** from those 86;
- `--order` ordered the 9.

The rule needs at least 50 leakage-clean items. So the bet ends untestable whatever the bettor knows: P(pass) = 0 and P(fail) = 0 (D11). The pool size was assumed, not measured (pattern P15). Nothing in the rule can fix that, so the verdict is **redesign**. The bet is withdrawn before data and re-bet on a pool whose size is measured before pre-registration.

The rest of the design is close to sound, and the re-bet should carry four fixes:
- a scale gate on the flattery rater: as built, a rater that reads its scale backwards makes the bet pass;
- the false-pass rate from the flattery rater's noise, measured here from round 2, stated in the write-up (or a stricter leg added);
- a leave-one-swap-pair-out check that does not report a "flip" only because too few items remain;
- one untestable sentence that names its real cause.

## Checks

**What I ran.** Commands ran from `programs/settled-science`, with no paid call. The only network requests were arXiv reads: `--fetch`'s four API requests, plus one API request with `max_results=1` to read `totalResults`. Nothing ran beyond `--order`, so there was no `--leak`, `--freeze` or `--bet`. The only files written in the program tree are `items/f2/pool.json`, `candidates.jsonl`, `build-log.json` and `order.json`, all from the free steps. I did not read the candidate sentences.

Scratch scripts are in `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed-ss-wave4/859c1100-007c-4362-bb3e-7f15b3131c61/scratchpad/`:
- `r2nums.py`: round 2's measured rows;
- `d11.py`: worlds from those rows;
- `h0.py`: a noisy same-signal rater;
- `recal.py`: a sharpened-rater bettor.

The worlds use round 2's archive (P15):
- `items/r2/items.jsonl`;
- `bettor/r2-bets.jsonl`, 92 Opus primaries;
- `bettor/r2-valence.jsonl`, 92 ratings from the same `valence-v2` prompt and the same Opus setting;
- round 2's per-field candidate yield and leak keep rate.

**D1. A stranger can apply the rule: holds.** §5 and `score_f2.passes`/`verdict` agree: C1 < 0.25, and C2 and C3 < −0.01, at the upper bound, on both bootstraps, with EPS, n ≥ 50 for the Opus bettor and the rater, and untestable on any refusal or error. `score_f2.py --synthetic coin oracle uprule flatcopy` gives one verdict each: fail, pass, fail, fail. An empty item set gives untestable with its sentence, and so does a status file with a refusal.

**D2. Every manipulation takes effect: holds.**
- **Settings.** `f2.py --dry-run` prints the plan: 4 requests, results 600–1799, 120 (+40) leak checks, 60 frozen, a $1.25 cap. The template self-test passes.
- **Job construction.** I ran `f2.jobs()` in-process on a scratch `masked.jsonl` of 60 round-2 items, with `F2` pointed at the scratchpad:
  - four steps (Opus bettor, Opus flattery, Sonnet, Haiku), 60 unique keys each;
  - option_b first on 29 of 60;
  - the same option order for the rater and all three bettors;
  - the rater's user text is byte for byte `valence.py`'s (`Field: …\n\nOption 1: …\nOption 2: …`), with `valence.SYSTEM`, tag `valence-v2` and `B.SCHEMA == V.SCHEMA`.
- **The order seed moves the draw.** Changing it changes 29 of 60 orders.
- **Seeds reproduce.** SHA-256(randomness ‖ "ss-b14:" ‖ purpose), first 8 bytes, gives items 16180817909411768102 and order 12026579425415227515, and `ledger/seed.py` agrees. Pulse 1592501 (10:17:00) is the first after e3ed649 (10:16:06); the previous pulse was at 10:16:00. D66's correction came before any draw.
- **Budget.** `cap()` = spent_total − own + 1.25 = $8.996, so the bet cap binds over both caches.

**D3. Every control can fail: flaw (F2).** Coin, up-rule and a flatcopy bettor are rejected. A rater set up wrong is not:
- I scored the real round-2 bettor against the real round-2 rater with its scale inverted (100 − p). `score_f2` returns **pass**: C3 −0.498, cluster CI [−0.586, −0.446], rater Brier 0.568.
- The rater's up-word share (0.26) is printed in the table, but nothing acts on it.
- ss-b6 carried exactly this gate (G1, D34). It was dropped here without a word.
- Separately, `up_word_share`'s denominator counts non-50 ratings over every flattery row, not only the frozen items.

**D4. Rivals are matched: flaw (F3).** C3 compares the bettor's raw probabilities with the rater's raw ratings. ss-b6's review (F2) and the ss-b6 audit (B9) both showed what that comparison does: a rater that carries only the bettor's own signal, plus noise, loses to it. ss-b6 added a recalibrated leg, and ss-b7 added a null-world margin m*. ss-b14 keeps neither and leans on the fixed 0.01 margin and the cluster bootstrap.

I measured what those buy. On round 2, SD(logit rater − logit bettor) = 0.83, on all 92 items and on the 30 model-psychology items alike. I set the rater to the bettor's rating plus N(0, σ) in logit, drew 60 items, and applied the full rule on both bootstraps, 300 draws each:

| null world (bettor knows only what the rater reports) | σ 0.25 | σ 0.5 | σ 0.89 | σ 1.2 |
|---|---|---|---|---|
| P(pass), round-2 all-fields rows | 0.00 | 0.00 | **0.16** | 0.33 |
| P(pass), round-2 model-psychology rows | 0.00 | 0.01 | **0.03** | 0.16 |

A second no-knowledge bettor, the rater sharpened (logit × 1.5 or × 2), passes 0.07–0.10 in the all-fields world and 0.00 in the model-psychology world.

So the margin cuts ss-b6's 58% to about 3–16% at the measured noise. That is not a pass by construction. But a pass is not "skill beyond these shortcuts" either: it is that, **as this rater judged it**, at a false-pass rate the pre-registration never states. §6 names only the channel that biases toward a null (shared judgment), not the one that biases toward a pass.

**D5. A dumb baseline is beaten, and the design can see the effect: holds.**
- Always-50%, the up-word rule (Brier 0.177 on round 2) and a constant 0.8 copied to the rater all fail.
- The swap-pair rule is reported.
- This is not a no-difference rule, so no equivalence margin is needed.

**D6. Foreseeable execution risks are piloted: holds (no pilot).** The pre-mortem's kind is `world`. The same prompts on the same template parsed 138 of 138 bettor calls and 92 of 92 rater calls in round 2, with no refusal. Medians are far below the 4000-token cap, and per-call costs match §3. The real execution risk was the pool, covered under D11.

**D7. Comparisons match: holds, with a note.**
- The rival is the bettor's comparator by design: the same model, setting, option order and field line; no question or methods; a different SYSTEM. That is the named factor.
- Sonnet and Haiku differ from Opus in thinking (D18), and the scorer's notes say so.
- Note for the re-bet: round 2 gave a paper matching several queries to the first field. `f2.build` runs only the model-psychology query and never checks the other three, so papers that round 2 would have filed as scalable-oversight can enter. This is immaterial at the pool's real size, but a widened pool should apply round 2's rule.

**D8. The verdict sentences are written: flaw (F3, F5).**
- The pass sentence says "the bettor's skill is more than these shortcuts". Given D4 it needs "as this rater judged it" (ss-b6 N4) and the false-pass rate.
- An untestable verdict caused by a refusal in a *reported* step prints "Too few model-psychology findings were scored to test the bettor (items 92; Opus bettor 92; flattery rater 92; …; haiku-bettor: refusal)". That is checked by scoring the oracle with a Haiku refusal in the status. "Too few … were scored" is false there.

**D9. One item cannot decide it: flaw (F4).** Leave-one-item-out and leave-one-swap-pair-out are pre-registered. But `loco` calls `passes()`, which returns False whenever fewer than 50 items remain.
- "more/less" holds 45 of round 2's 92 items (17 of the 30 model-psychology items).
- So dropping it always "changes the label". The oracle bettor (Brier 0.010) prints "Leaving out the swap pair(s) more/less changes the label."
- On round 2's real data, 7 of 10 pairs are reported as flips.
- The check reports the n floor, not fragility.

**D10. Machinery: holds, with notes.**
- **Budget.** In code: `BET_CAP` over both caches, `common.BUDGET_USD` (now 13.40 after D65; §7 says $10.20, but the bet cap binds).
- **Stops and caching.** Stop on refusal or error via `Caller` and `_check_stop`; a checksum check before `--bet`; caching by content hash; every cache listed in `common.CACHES`.
- **Records.** One scale direction; the beacon rule kept (certificate_verified false, as precedent).
- **Lesson.** `ls-ss-b14` matches §0 verbatim (62 words, noted over the 60-word rule).

**D11. The bet can both pass and fail: flaw (F1).**
- **As built:** P(pass) = 0 and P(fail) = 0; P(untestable) = 1. The window holds 686 results, round 2 took 0–599, and the 86 that remain give 9 candidates. Drops: 67 with no candidate sentence, 8 already in the program, 2 with an ICML/TMLR comment. At most 9 clean items, against 50 needed.
- **Why it was missed (P15).** The design assumed 1,200 more results and never read `totalResults`. Round 2's measured yield is 69 candidates from 600 papers (11.5%) and 35 of 69 clean (51%). So 60 clean items need about 1,050 new eligible papers, and about 1,300 with headroom.
- **If the pool existed.** With 60 items drawn from round 2's measured rows: P(pass) = 0.30 in the all-fields world (H1) and 0.24 in the model-psychology world (H1). In the exchangeable null (bettor and rater swapped at random) it is 0.00, and 0.03–0.16 in the noisy-rater null of D4. At n = 50 it is 0.29. The binding leg is C3 on the cluster bootstrap: 0.28–0.33. A re-bet at this n could both pass and fail, and the engine's 27 sits inside that range.

**D12. The predicted outcome is not already in print, or the bet says what it adds: holds, with a note.**
- **(a) The line states predicted outcomes.** §0 and the map's `prior_work_line` give a predicted outcome with citations: fail (Wen et al.) and pass (BrainBench). They also say what the bet adds: a field-specific check, with the shortcut rivals and model-free items.
- **(b) Each paper says what it is cited for.** I opened the abstract and HTML of each.
  - **Wen, Si, Chen, He and Feng 2025, arXiv 2506.00794.** The task is which of two AI-research ideas scores higher, on 1,585 post-cutoff test pairs. NLP experts score 48.9% by majority vote, o3 is "no better than random guessing", and fine-tuned GPT-4.1 plus retrieval scores 77% (64.4% on NLP). Off-the-shelf GPT-4.1 is 51.4% in Table 4 but 51.9% in the §4.2 text. The paper tests recency, length and lab-name shortcuts, not valence. Cited correctly: it predicts **fail** for an untuned bettor, on a different task.
  - **Luo et al. 2024, arXiv 2403.03230 (BrainBench).** The task is to pick the original Journal of Neuroscience abstract over an altered one. LLMs score 81.4% and experts 63.4% (66.2% for the top 20% by expertise), and "LLMs outperformed human experts in every subfield". Cited correctly; it predicts **pass**.
  - **Note.** Its task, original versus results-altered text, is nearly this template's task. "If the task transfers" undersells how direct the prediction is. Neither paper tests a valence rival, so the bet's addition stands.
- **(c) Odds against the prior.** No paper predicts this exact rule's outcome on these models. The odds of 27 sit between the two predictions and are tied to ss-b6's thin margin, which is the right anchor.
- **(d) My own search** (the terms in the header, in publication-bias and spin words):
  - Liu and Shah 2023, *ReviewerGPT?* (arXiv 2306.00622): an LLM favoured the abstract reporting significance in near-identical abstract pairs;
  - an LLM "spin" study (medRxiv 10.1101/2025.05.05.25326991; Northeastern): LLMs detect spin in abstracts but are swayed by it more than clinicians.

  Both support the pre-mortem's rival, that a model prefers the positive or flattering version. Neither predicts this pass rule. I recommend that the re-bet's prior work row cite one of them for the rival.

## Required fixes

The verdict is **redesign**. The bet is withdrawn before data and re-bet as a new pre-registration with a new lesson. F2–F5 are written so that the re-bet adopts them. Its own review checks them.

**F1 (D11, P15): the pool cannot yield the items.**
- **Fix:** withdraw ss-b14 (`verdict: withdrawn` in `ledger/bets.jsonl`, unscored; Sean's 0.35 stays recorded, unscored). Re-bet only on a pool whose eligible size is measured before pre-registration (`opensearch:totalResults` per query, minus ids already in the program), needing at least about 1,300 eligible post-cutoff papers at round 2's 11.5% × 51% yield, and with the expected clean count stated from those measured numbers. Options:
  - a widened model-psychology query with added terms named in advance, in the same post-cutoff window and with round 2's first-field rule;
  - an n chosen from what the pool can give, with D11 re-run at that n.
- The 86 fetched papers and 9 candidates were touched only by local, answer-free code: no model saw them and no one read the sentences. A re-bet may include them, and must say so.
- **DEVIATIONS text:** "D67 | 2026-11-05 | **ss-b14 withdrawn before data** (design review `ledger/design-reviews/ss-b14.md`, verdict redesign). The model-psychology query holds 686 results in round 2's window (arXiv totalResults, 2026-11-05 10:26); round 2 took results 0–599, so the review's free `--fetch` returned 86 papers (600–685; starts 900, 1200, 1500 empty) and `--build` 9 candidates, below the 50 the rule needs, so the bet could only be untestable. The pool size had been assumed, not measured (P15). No leakage, bettor or rater call was made; $0 spent. `items/f2/pool.json`, `candidates.jsonl`, `build-log.json` and `order.json` (written by the review) are kept as the record. Re-bet as a new pre-registration with a pool measured first. | Design review ss-b14 (D11). |"

**F2 (D3): no scale gate on the flattery rater.**
- **Fix (in the re-bet):** add ss-b6's G1 to `score_f2`. Among the rater's ratings ≠ 50 on the frozen items, if the share favouring the up option is below 0.50, the verdict is untestable, with ss-b6's G1 sentence. Compute it from `up_side` only, before scoring. Also count the denominator over frozen items only.
- **DEVIATIONS text (re-bet):** "Gate G1 (ss-b6 D34) added to the flattery rater: share of non-50 ratings favouring the up option < 0.50 → untestable; design review ss-b14 F2 showed an inverted rater gives C3 −0.498 and a pass."

**F3 (D4, D8): the raw-rater comparison has an unstated false-pass channel.**
- **Fix (in the re-bet):** do one of two things.
  - (a) Add ss-b6's recalibrated leg 2 (`score._feats`, `_loo`; up word on both sides) as a required condition, and re-run D11.
  - (b) Keep C3 and state in §6, and in the pass sentence, the measured false-pass rate. In both, write "as this rater judged it" (ss-b6 N4), and add to §6: "a rater carrying only the bettor's signal plus the noise measured between them on round 2 (logit SD 0.83) passes this rule about 3% (model-psychology rows) to 16% (all fields) of the time."
- (b) is the minimum; (a) or ss-b7's m* is preferred.
- **DEVIATIONS text (re-bet):** "The flattery comparison's false-pass channel stated (design review ss-b14 F3): noisy-same-signal null P(pass) 0.03–0.16 at the measured σ; pass sentence scoped 'as this rater judged it'" (plus the leg, if added).

**F4 (D9): the leave-one-swap-pair-out check reports the n floor as a flip.**
- **Fix (in the re-bet):** in `model_result`, evaluate leave-one-out and leave-one-cluster-out bounds without the `MIN_ITEMS` floor (call the bound test directly). Report "too few items remain (k)" separately where a remainder is below 50.
- **DEVIATIONS text (re-bet):** "Leave-one-out checks no longer apply the n ≥ 50 floor (design review ss-b14 F4: the oracle printed 'leaving out more/less changes the label')."

**F5 (D8): the untestable sentence names the wrong cause.**
- **Fix (in the re-bet):** when the cause is a refusal or error, print "The run stopped on a <refusal | error> at <step>, so the bettor was not tested (items n; Opus bettor n; flattery rater n)." Keep "Too few … were scored" for the count cases. Or, if Sonnet's and Haiku's steps are reported only, state whether a refusal there voids the bet.
- **DEVIATIONS text (re-bet):** "Untestable sentence split by cause (design review ss-b14 F5)."
