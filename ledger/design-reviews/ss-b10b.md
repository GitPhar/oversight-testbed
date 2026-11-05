---
bet: ss-b10b
program: settled-science
prereg_commit: 1181659
reviewer_session: design review ss-b10b (fresh subagent; no chat, transcript or author message read)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 10:28 America/Denver
checks: {D1: holds, D2: holds, D3: holds, D4: holds, D5: holds, D6: holds, D7: holds, D8: holds, D9: holds, D10: flaw, D11: flaw, D12: holds}
prior_work_search: "language model distinguishes original from altered abstract by whether result confirms authors' hypothesis, position bias both orders, BrainBench" (web search, 2026-11-05 10:25); nothing found that states an order-balanced flattery or valence score on BrainBench
papers_opened: 2
flaws: 3
pilot_usd: 0.00
verdict: redesign
confirmed_at: null
---

# Design review of ss-b10b

## In plain English

The code does what the pre-registration says. The archived calls are found by the same content-hash keys (974 of 974, no field mismatch), the archive is never written, the caps stop where §3 says, and the Opus step's cap stop is handled as designed. The rule applies cleanly, and a pure "always Option 1" rater fails it.

But the bet's answer is already in ss-b10's archive. Sonnet clears in every world built from that archive. For Haiku, 100 of the 200 items are already fixed at 75.0%, and one of the two orders is already known for each of the other 100. Built from those measured ratings, every world I ran gives Haiku's orders-averaged accuracy about 75% (SD about 2 points) and a pass in 99–100% of runs. Haiku fails only if the 100 new calls go 64 or fewer right where the archive predicts about 75, which is about 2.6–3 SD below.

So P(fail) is about 0–1%, far under D11's 10% floor. A run at the stated 78% odds would be scored on an outcome the archive already gives, which is P12. Verdict: **redesign**. The question can still be asked as a real test if its statistic is restricted to the information not yet seen (below).

## Checks

**D1. The rule can be applied by a stranger: holds.** `python3 scoring/score_bbb.py --synthetic coin position strong haikulike split` gave fail, fail, pass, pass and mixed, one verdict each. I also built an untestable world (Sonnet's second order dropped on 60 items, so 140 of 200 had both orders): it returned `untestable`, with §5's sentence 4 ("Sonnet: 140 of 200 items with both orders; at least 150 needed"). The verdict function reads only "item-bootstrap lower bound > 0.634 + 1e-12 on both", with `MIN_N` 150, as §5 says. Ties are exact: for every p in 1–99, `(p/100 + (1 − p/100))/2 == 0.5` holds in floating point, and no unequal pair lands on 0.5 (checked over all 99×99 pairs). So a pure position answer scores 0.5, as §4 says.

**D2. Every manipulation takes effect: holds.** The one knob is option order. `both_orders` builds `orig-first` (original as Option 1) and `orig-second` jobs. Their user texts differ and their `original_is_option` is 1 or 2. ss-b10's archived rows carry the same `original_is_option` as the new plan's job for the same key (974 checked, 0 mismatches). Averaging takes effect: a rater fixed at p_option_1 = 80 scores 1.0 on the orig-first half alone and 0.5 when the orders are averaged (`pairs` → `acc_block`). The dry run prints what the run will use: 300/274/200/200 archived and 100/126/200/200 new for steps 1–4; Opus 800 jobs, 0 archived; first Opus items bb-141, bb-103, bb-033, bb-094, bb-032.

**D3. Every control can fail: holds.** The wrong set-up the averaging must reject is a pure position rater: it gives 0.5 on both models, so the verdict is fail (above). The always-Option-1 baseline is fixed at 0.5 by construction. The five text-only rules are computed per item and are flagged if any clears 0.634 (ss-b10: 0.482–0.505). The section-cluster bootstrap (`score_f1.cluster_ci`, 5 clusters) is reported beside the item bootstrap, and a sentence is printed if the two disagree.

**D4. Rivals are matched: holds (not a contest).** Haiku and Sonnet form a conjunction, not rivals. Flattery against forecasting is a secondary, and its sentence names the three-way bundle (D54 F3, as audited for ss-b10).

**D5. A dumb baseline is beaten and the design can see the effect: holds.** The dumbest passer would be a position rater. It is cancelled by the averaging and fails (D3). The rule is not a null rule, so no equivalence margin is needed.

**D6. Execution risks piloted: holds; no pilot run.** The pre-mortem is of kind `world`. The texts are ss-b10's: 974 calls, 0 refusals, 0 errors, and Haiku's output averaged 216–220 tokens against a 1000 cap. Opus's per-call cost on these abstracts has never been measured. Elsewhere in the program it measured $0.0048–0.0058 per call on about 600-token inputs (733 calls in five caches). Scaled to about 1,450 input tokens at $4/$20 per million, that is about $0.009–0.012, against the $0.0115 estimate. A wrong estimate only changes how many Opus items fit; Opus is a secondary and runs last. So no pilot is needed.

**D7. Comparisons match: holds.** Every difference is named in a sentence:
- the experts' 63.4% and the LLMs' 81.4% are other measurements (perplexity, other models);
- forecasting against flattery is a bundle;
- Opus runs at adaptive effort low, the other two with thinking off;
- archived calls came from 07:03–07:10 and new ones come later, with the same model id and settings, and the archive split is reported.

**D8. The verdict sentences are written: holds.** `sentences()` gives §5's text for pass, mixed, fail and untestable, plus the always-reported clauses. Each uses only nouns the design carries: "not shown to", "on these models", and no "LLMs" or "all".

**D9. One item cannot decide it: holds.** Leave-one-item-out and leave-one-section-out are pre-registered (§4) and coded. A flip is reported in a sentence and does not change the verdict (§4, §5).

**D10. Machinery: flaw (two small items); otherwise holds.**
- *Caching and archive.* Checked:
  - every key in `bettor/bb-cache.json` (974; SHA-256 prefix 233581ea…) is a key of a job in `brainbench_b.plan()`;
  - the archive is a subset of ss-b10's 1,050-job plan rebuilt from `bb-seed.json`;
  - there are 0 id, model, task or `original_is_option` mismatches;
  - `run()` sends only keys not in the archive to `Caller`, which writes only its own cache;
  - `write_out` reads the archive and tags each row `source`.

  In four stubbed full runs (my harness at `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed-ss-wave4/859c1100-007c-4362-bb3e-7f15b3131c61/scratchpad/capsim.py`, with `BB.fn` replaced, the caches redirected to the scratchpad and no call made), the archive's hash was unchanged every time.
- *Caps.* All four runs:
  - **Measured costs:** 753 new calls; Haiku and Sonnet $1.689; Opus stopped at $1.463 (Caller's cap − 0.05); bet total $3.151. Status was `cap` for the Opus step, `main` exited 0 ("stopped at its cap, as pre-registered") and wrote 1,727 rows. The Opus flattery set was exactly the first 32 items of the beacon order (31 with all four calls).
  - **Sonnet at twice its measured cost:** stopped in step 4 at $3.165, re-raised, Opus not run, the primary complete.
  - **Refusal stub in step 5:** stopped, re-raised, `refusal.md` written (to the scratch root).
  - **Opus at $0.03 a call:** stopped at $1.507, with the bet at $3.200.

  The program cap ($13.40, $7.746 spent) cannot bind. The Opus scored sets are §2's: flattery is the items with both flattery orders, and the forecasting comparison is the items with all four calls (`opus_block`: `fids`, and `ids = F ∩ B`).
- **Flaw D10-a (run order):** step 2 (Haiku forecasting, a secondary) runs before step 3 (Sonnet flattery, half of the rule). Any refusal, error or truncation in step 2 stops the run. Sonnet would then hold only ss-b10's 74 both-order items, so the bet would be **untestable**. ss-b10 lost pre-registered steps to an ordering like this (its audit, D19). Fix: run 1, 3, 2, 4, 5.
- **Flaw D10-b (Opus overshoot):** with 6 workers, up to 6 Opus calls are in flight when the stop trips. At $0.03 a call this ran $0.007 over `OPUS_CAP`. At Opus's 4,000-token ceiling (about $0.09 a call) it could run about $0.40 over. Fix: `workers=2` for the Opus step, or a margin of 6 × the largest Opus call seen so far.
- Holds: stop-on-refusal (common.Caller); one scale direction (1 = Option 2, 99 = Option 1, in both prompts); the beacon seed (pulse 1592503 at 10:19:00 follows 1181659 at 10:18:42; `seed.derive(…, 'ss-b10b', 'opus-order')` = 13824542590128467770, matching `bbb-seed.json`); code unchanged since the pre-registration (`git diff 1181659 HEAD -- bettor/ scoring/ common.py` touches only the seed file); and the lesson line `ls-ss-b10b`, the same in §0 and lessons.jsonl (61 words, noted).
- A stop in step 4 leaves no `bbb-run-status.json` entry for step 5. The scorer prints "Opus (secondary) did not run", which covers it.

**D11. The bet can both pass and fail: flaw (below the floor).** The worlds are built from ss-b10's measured archive (P15), as the brief allows. Script: `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed-ss-wave4/859c1100-007c-4362-bb3e-7f15b3131c61/scratchpad/d11sim.py`.

What the archive already fixes:
- **Haiku.** 100 items have both orders: 75.0% averaged. On the 100 items rated once, the known order is orig-first on 52 (94.2% right; on the checked half, that order is 90.5% right) and orig-second on 48 (39.6% right; checked half 43.5%). The once-rated half is a beacon-random half and looks like the checked half.
- **Sonnet.** 74 items have both orders: 85.8% averaged. Of its 126 once-rated items, 64 are orig-first (96.1% right) and 62 orig-second (66.1% right).

How Haiku's missing order was simulated for each once-rated item, three ways:
- **(a)** drawn from checked-half items with the same order and the same single-order hit, with the checked half resampled to carry parameter uncertainty;
- **(b)** the same, matched on the nearest 10 known probabilities;
- **(c)** drawn independently from the checked half's marginal for that order.

| world (from the archive) | Haiku mean accuracy (SD) | P(Haiku clears) | Sonnet mean (SD) | P(Sonnet clears) | P(pass) | P(fail) |
|---|---|---|---|---|---|---|
| (a) matched on order and hit | 0.756 (0.017) | 1.000 | 0.865 (0.015) | 1.000 | 1.00 | 0.00 |
| (b) nearest-neighbour on p | 0.746 (0.020) | 0.992 | 0.851 (0.020) | 1.000 | 0.99 | 0.01 |
| (c) independent orders | 0.764 (0.017) | 1.000 | 0.895 (0.014) | 1.000 | 1.00 | 0.00 |

2,000 simulations each; the lower bound is a 2,000-resample percentile bootstrap, which tracks the scorer's 10,000.

With Haiku's 75 of 100 fixed, the scorer's own `boot` clears 0.634 only if the new 100 score 65 or more (64 gives a lower bound of 0.630; 65 gives 0.635). The archive predicts 74.6–76.4. The design's own failure world (the pre-mortem: the once-rated half "falls well below the checked half's 75%") is therefore about 2.6–3 SD out, with nothing in the archive pointing to it.

So P(fail) is about 0–1% in every world the archive supports. The bet cannot fail at this n with this statistic: its outcome is known before it runs (P12). The stated 78% is also far from what the bet's own data imply (99% or more), and §0 does not say why. The `haikulike` synthetic world (0.75/0.80 with a 12-point pull) is an assumed spread, not this archive (P15), and the pre-registration has no committed P(pass)/P(fail) calculation.

*What would pass the floor:* the same rule read only on the items whose flattery statistic is not yet known, i.e. Haiku's 100 once-rated items. Under worlds (a) and (b), P(Haiku clears at n = 100) is 0.885 and 0.727, so P(fail) is 0.12 and 0.27, mean 0.74–0.76 (SD 0.035–0.041). Sonnet's 126 once-rated items clear in 100% of runs, so the conjunction is in effect Haiku's. That clears D11 narrowly, and the odds must be stated from that calculation.

*Is reusing the archive fair?* As measurement, yes. Each archived call is the same request (model, settings, system and user text) as the planned one, sampled once at the default temperature; asking again would draw from the same distribution. The reuse is disclosed, tagged per row, and the halves are reported apart. The problem is not the reuse but the selection: this follow-up was chosen after its audit saw 75% on the checked half, and the scored statistic includes that half. Reuse is fair for secondaries and description. The scored rule should not include data that were read before the bet was chosen.

**D12. The predicted outcome is not already in print, or the bet says what it adds: holds.**
- (a) §0 and the map's Prior work line state "predicts: unknown" with citations and a described search.
- (b) Papers opened:
  - **Luo et al. 2024** (arXiv 2403.03230v4 HTML): LLMs 81.4% and experts 63.4% (171 of 202 retained) on 200 human-written items. Models were scored by perplexity of each abstract, so there is no option order. Chat and instruction models did worse than base models. There is no control for valence, flattery or position. This is as cited.
  - **Lee 2026**, "LLMs Have Made Failure Worth Publishing" (arXiv 2604.06236v1 HTML): a conceptual paper with no data, proposing ClinicalTrials.gov experiments (200–500 trials, LLM success probabilities, five context conditions). It does not mention BrainBench, flattery or option order. This is as cited.
- (c) Not applicable in the literature sense: no paper predicts this pass rule.
- (d) My own search, in other words around the mechanism (a model telling the real abstract from the altered one by whether the result confirms the hypothesis, tested in both orders), found BrainBench and its follow-ups. One is Luo, Ramscar and Love on forward and backward text (arXiv 2411.11061): it notes position effects inside the model, but not option-order balancing or a valence rule. Nothing states this outcome.

The prediction that matters is in this repository: ss-b10's archive and audit. That is treated under D11, not here.

## Required fixes

Verdict **redesign**: per operators/design-review.md, ss-b10b is withdrawn before any call (`ledger/bets.jsonl` `verdict: withdrawn`, not scored), and re-bet under a new pre-registration with a new lesson, a new seed and a new design review. The flaws:

1. **D11 (redesign).** Withdraw ss-b10b. Re-bet with the scored statistic read only on data whose flattery outcome was not seen when the direction was chosen:
   - per model, orders-averaged flattery accuracy on the items ss-b10 rated in one order only (Haiku 100, Sonnet 126);
   - item-bootstrap lower bound above 0.634 on both;
   - the full-200 orders-averaged accuracy and the archived half become reported rows.

   Or choose another statistic or model set (for example Opus as a rule model on a fixed n). Either way, the new pre-registration commits a dry run built from `bettor/bb-cache.json` (P12, P15) showing P(pass) and P(fail) each at least 10%. Its odds come from a fresh v2 context handed that calculation.

   DEVIATIONS text: "| D67 | 2026-11-05 hh:mm | **ss-b10b withdrawn before any call** (design review `ledger/design-reviews/ss-b10b.md`, D11). Built from ss-b10's archive (Haiku 75.0% on 100 items rated both ways, one order already known on the other 100; Sonnet clearing on every check), the pre-registered rule passes in 99–100% of simulated runs (P(fail) about 0–1%). The result is known before it runs (P12). Not scored; counted as withdrawn in `ledger/bets.jsonl`. Re-bet as ss-b10c, with the scored statistic on the items ss-b10 rated in one order only, and a committed archive-built dry run. No call was made under ss-b10b. | Design review ss-b10b, verdict redesign. |"
2. **D10-a (carry into the re-bet).** Run order 1 Haiku flattery, 2 Sonnet flattery, 3 Haiku forecasting, 4 Sonnet forecasting, 5 Opus, so that no secondary can stop the rule's calls.

   DEVIATIONS text (in the re-bet's row, or its own row if ss-b10b were kept): "Run order changed before any call: both flattery steps (the rule) before both forecasting steps (secondaries), so a stop in a secondary cannot make the bet untestable (design review ss-b10b, D10-a)."
3. **D10-b (carry into the re-bet).** In the Opus step, call `Caller(...).run(todo, BB.fn, workers=2)`, or stop at cap − 6 × the largest Opus call seen so far. Report Opus's measured per-call cost in the results.

   DEVIATIONS text: "The Opus step runs with 2 workers so that calls in flight cannot carry spend past OPUS_CAP by more than the 0.05 margin (design review ss-b10b, D10-b; stubbed run overshot by $0.007 at $0.03 a call)."
