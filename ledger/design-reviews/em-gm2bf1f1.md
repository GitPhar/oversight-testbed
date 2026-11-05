---
bet: em-gm2bf1f1
program: entangled-mind
prereg_commit: df30f78
reviewer_session: fresh design-review subagent, worktree p1-wave3 (seed commit aa34897 also read; it changes only the seed line and SEED_RECORDED)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 11:29 America/Denver
checks: {D1: holds, D2: holds, D3: holds, D4: holds, D5: holds, D6: holds, D7: flaw, D8: flaw, D9: holds, D10: flaw, D11: flaw, D12: holds}
prior_work_search: "attitude strength susceptibility to response effects question order response format same respondents Krosnick Schuman" (WebSearch), then "Krosnick Schuman 1988 susceptibility to response effects abstract"
papers_opened: 3
flaws: 5
pilot_usd: 0.00
verdict: redesign
confirmed_at: null
---

# Design review of em-gm2bf1f1

## In plain English
As built, this test cannot answer its question. Its result is known before it runs.

The question is whether em-gm2bf1's order–format link was "one run's noise". The archive already answers that for free. Two halves of the same run agree on every claim's order span at Spearman 0.95. A separate fresh Haiku run already exists for gm2's 10 items: em-gm2q's shown chains, recorded on a later day with the same prompts and settings. It reproduces the archived spans at 0.95. The link is not sampling noise.

What made em-gm2bf1 fragile is that the frozen guard's partial sits at 0.09 and gm2's ten items show no link (−0.09). A fresh run of the same items reproduces both:
- In the author's own archive world, this rule passes 0 of 100 runs while em-gm2bf1's rule passes 100 of 100.
- On em-gm2q's real fresh run, gm2's group comes out at −0.16. Spliced into the archive, the rule fails.

The only worlds that pass need fresh Haiku to differ systematically from two runs that agree at 0.95. So P(pass) in any world consistent with the data is far below the 10% floor (D11). Under the rule's sentences, the expected fail would also be misread as "em-gm2bf1's pass did not repeat" (D8). The bet should be withdrawn and re-bet on the question the fragility actually raises: specification (is W a confound or the trait itself?) or items (new items), not fresh conversations on the same items.

## Checks

Environment: `/Users/seanpharris/entangled-mind/.venv/bin/python`. The script's `sys.path.insert(0, HERE.parent/"src")` and `(0, HERE)` take effect: `entangled_mind` resolves to `oversight-testbed-p1-wave3/programs/entangled-mind/src/entangled_mind/__init__.py`, and `gm2bf1_order_vs_format`, `gm2q_questions_only`, `gm3b_format_invariance` and `gm3c_heldout_format` all resolve inside this worktree. The scripts I wrote are in the session scratchpad (`repro_parent.py`, `fake_run.py`, `fake_analyse.py`, `dry2.py`, `split.py`, `gm2q_check.py`, `sonnet_free.py`, `st.py`). Nothing under `results/` was written: every fake run had CACHE, BATCHLOG, REFUSAL and OUT paths redirected to the scratchpad.

**Reproduction of the parent first.** This bet's `format_arm`, `partial_frozen`, `b1.partial_spearman` and the archived chains give the parent's published numbers:

| quantity | reproduced | parent's published value |
|---|---|---|
| ρ | 0.336 | 0.336 |
| frozen guard | 0.085 [−0.107, 0.267] | 0.09 [−0.09, 0.27] |
| D71 guard | 0.246 [0.083, 0.365] | 0.246 |
| ρ in gm2's group / gm2b's | −0.088 / 0.423 | −0.09 / 0.42 |
| ρ(S, W) | 0.772 | 0.77 |

G and E are identical to the parent's (`np.allclose`). The imported measures are therefore unchanged, as §4 says.

**D1. Holds.** `--selftest` passes. Its `label()` boundary assertions cover pass, a frozen bound at 0, a negative group, a NaN group, the bar met exactly and just missed, and 119 claims (untestable). Each synthetic table returns exactly one verdict. Minor: §5's "pass, carried by item <id>" label is not produced by `analyse()`, which only lists `loo_item_flips`, so the label would be hand-written.

**D2. Holds.** `run()` was driven with a fake Batches client (scratchpad `fake_run.py`):
- It made 5 rounds of 1,840 requests: 1,600 Haiku conversations and 240 Sonnet.
- The parameter sets it sends match §2: Haiku with `max_tokens` 200 and thinking disabled; Sonnet with `max_tokens` 1000 and thinking `between_tools`; both with the `json_schema` `{"rating": integer}` output.
- The order knob takes effect. In `haiku|h190|O2|shown|0` the claims arrive in the order 2, 4, 5, 0, which is LATIN[1] applied to h190's chain claims [0, 2, 4, 5].
- Prompts, settings and history handling are those of gm2 and gm2q: the same `opening` and `sub_q` text, max_tokens 200, thinking disabled, structured output, raw JSON fed back as the assistant turn.
- The dry run's link knob c moves the outcome: P(pass) is 0.00, 0.01, 0.14, 0.41, 0.70 and 0.98 at c = 0, 0.5, 1, 1.5, 2 and 3 (my 100-run re-run, `dry2.py`).
- `analyse()` runs end to end on the fake cache, the real gm2q2 Opus chains and all three format archives.

**D3. Holds.** The dry run's no-link world (G shuffled within items) passes 0/100. The self-test's noise-only world is rejected, but narrowly: frozen lower bound −0.009, D71 −0.022, with ρ 0.58. A stronger noise-only world (G = 0.012·W + noise, ρ 0.84) is rejected cleanly: frozen [−0.19, 0.16].

**D4. Holds (not applicable).** No rival model families are fitted.

**D5. Holds.** The dumb predictors (no link; link carried only by W) fail. This is not a no-difference rule.

**D6. Holds; no pilot.** The pre-mortem is of kind `world`. The same chains have already run without a refusal on Haiku (gm2, gm2b, gm2q) and on Sonnet (gm2q, gm2q2). The Sonnet parameter set is gm2q2's, which ran on the Batches API. The refusal path was tested with the fake client: the first batch stops, `refusal.md` is written, unfinished costs go to `_unfinished`, and a rerun is refused. The errored path was tested too: after two unchanged resubmissions the run stops.

**D7. Flaw (F3).** §0, §2 and §6 say em-gm2q2's Opus chains are "6 per order". The archive holds 4 per item × order cell: `opus|<item>|<order>|shown|0..3`, 40 keys per order. gm2q2 pre-registered 6, and its results say "4 conversations per cell". The Opus arm is reported only, but the material is misdescribed.

Other differences from the parent are stated in §6: the Batches API, a later day, and a stricter rule.

Not stated: free fresh-order archives already exist for 30 of the 40 Haiku-and-Sonnet items, and they matter for the design (see D11):
- em-gm2q: Haiku and Sonnet shown chains on gm2's 10 items, 10 per order.
- em-gm2q2: Sonnet on gm2b's 30, 5 per order. Ten of these items are in Sonnet's format set.

**D8. Flaw (F2).** The fail sentence ends "em-gm2bf1's pass did not repeat on a fresh run", and §1 says "If it does not, em-gm2bf1's pass was most likely that run's noise." The design cannot carry either noun. In the author's own archive world, where the fresh run behaves exactly like em-gm2bf1's:
- this rule fails 100/100;
- em-gm2bf1's own rule (ρ ≥ 0.30, ρ's lower bound > 0, D71's lower bound > 0) passes 100/100 (`dry2.py`, c = 0).

So a fail here is what a faithful repeat of em-gm2bf1's pass produces.

**D9. Holds.** Leave-one-item-out is pre-registered: bounds are shifted by the point change and groups recomputed (`analyse_arm`), and §5 states what a flip does.

**D10. Flaw (F4, F5).** These parts hold:
- The budget is enforced in code. The fake run's projected $0.84 + $0.05 fits the $1.00 cap, and the per-round check uses ×1.10 + $0.05.
- Stop-on-refusal is in code.
- The scale runs one way: ANCHOR "0 = certainly false, 100 = certainly true".
- The seed checks out. `ledger/seed.py <randomness> em-gm2bf1f1 --purpose bootstrap` gives 10269032153479545163, which equals SEED_RECORDED. Pulse 1592560 (18:16:00Z) is the first after df30f78 (18:15:51Z).
- The lesson row `ls-em-gm2bf1f1` matches §0 word for word.

Two parts fail:
- **F4.** The cache is keyed only by `model|item|order|shown|r`. Unlike gm2q2 (`req_sha256`), it stores no content hash and does not check one on reuse.
- **F5.** `analyse()` builds `fresh = {k.split("|",1)[1]: v ...}`, which strips the model prefix. Sonnet's 240 keys collide with Haiku's for the 20 shared items and reps 0–2, so on the fake run it reports `n_conversations` 1600 instead of 1840, and `n_missing` is undercounted the same way. Reporting only; the verdict is unaffected.

**D11. Flaw (F1), and the reason for redesign.** The design names three worlds: archive (P(pass) 0.00), no link (0.00) and link c = 3 (0.93). It counts c = 3 as its world where the hypothesis holds. That world is not consistent with the data this bet replicates:
1. **Within-run noise is tiny.** Split the archive's 10 repeats into random halves of 5 (40 splits, `split.py`). The order spans of the two halves agree at Spearman 0.951. The implied run-to-run SD for one half (n = 5) is 0.013 for ρ, 0.026 for the frozen partial, 0.024 for D71 and 0.032 for gm2's group. In the resampling world at n = 10, the SDs are 0.012, 0.021 and 0.019.
2. **Between-run shift is just as small, measured.** em-gm2q's Haiku shown chains (commit bbf5b71, 2026-11-05; same `chain_turns`, max_tokens 200, thinking disabled, structured output; 10 per order) are an independent fresh run on gm2's 10 items (`gm2q_check.py`). They match the archive (gm2, earlier):
   - S at Spearman 0.948 and W at 0.944 over the 40 claims;
   - gm2's group ρ(S, G) at −0.164, against −0.088 in the archive.

   Spliced into the archive, the full rule gives ρ 0.329 [0.151, 0.477], frozen 0.103 [−0.064, 0.273], D71 0.242 [0.089, 0.353], gm2 −0.164 and gm2b 0.423: **fail**. On real fresh data, two of the five conjuncts fail exactly as in the parent.
3. **Passing needs a systematic shift that the evidence argues against.** P(pass) reaches 0.14 only at c = 1 (frozen partial 0.20, P(gm2 > 0) 0.14) and 0.41 at c = 1.5. Getting there means the frozen partial moves from 0.09 to at least 0.20, about 5 run-to-run SDs, and gm2's group moves from −0.09/−0.16 to above 0. A fresh run that exists already moved gm2's group the other way. Under c = 3, the archive itself would have passed every conjunct.

So P(pass) is about 0 in the archive world and in a world matching em-gm2q's real fresh run, and well under 10% in any world consistent with two agreeing runs. This holds whether em-gm2bf1's link is real (as observed) or not, so the rule cannot separate the two. This is the em-qwalk2 pattern: the outcome is known before the run, and scoring it at 8% buys Brier points without information.

Rule 13 needs no change here; the problem is that the question "was it one run's noise?" is already answered at $0 (points 1 and 2), and the answer is no. A fresh run cannot change the frozen-guard and gm2-group failures, because they are properties of these 40 items and of the covariate choice, not of the run.

Two further findings:
- The Sonnet arm's $0.63 buys 3 repeats per cell where the archives already hold fresh Sonnet shown chains for all 20 of its items: gm2q has 10 per order on gm2's items and gm2q2 has 5 on cand[20:30]. On those, `sonnet_free.py` gives ρ 0.024 [−0.26, 0.30], label fail, n = 80.
- W is a stable trait of each claim (0.94 across runs), not sampling noise. "Controlling for rating noise" therefore partly removes the claim-level instability the hypothesis is about. Whether the frozen guard is the right control is the open question, and a fresh run cannot settle it.

**D12. Holds**, with one addition recommended. (a) The Prior work line states a predicted outcome for the guarded link ("Predicts: unknown") with citations, and says what the bet adds. That added value (a fresh run) is what D11 shows to be already available for free. (b) The papers opened:
- **Zhu and Griffiths 2024, arXiv:2401.16646.** LLM probability judgments are incoherent, and the mean–variance relation across repeated judgments of the same event is an inverted U. This is cited for "judgment variance follows an inverted U in the mean", which it says. The abstract page does not list the models, so I could not confirm the "GPT-4, GPT-3.5, LLaMA-2" attribution. It speaks to repeated-sampling variance, not order or format.
- **Temkit 2026 (AMEL), arXiv:2605.22714.** Twelve models including Anthropic's Haiku and Opus. Judgments drift toward a conversation's prevailing polarity, most strongly on items uncertain at baseline (d −0.36 against −0.15). Cited for "order drag strongest on uncertain items", which matches. It is about accumulated-history polarity, not question order per se, and it says nothing about format.

(c) Not in print, as far as found. (d) My own search, in survey-methodology words: "attitude strength susceptibility to response effects question order response format same respondents Krosnick Schuman". It found:
- **Krosnick and Schuman 1988** (JPSP 54, 940–952): tested whether intense, important or certain attitudes are less susceptible to response effects. The PDF did not render; the citation and premise come from the search results.
- **Bassili and Krosnick 2000** (Political Psychology), per the search summary: no single strength-related attribute consistently moderates all response effects; different attributes moderate different effects.

This is the human analogue of the item-level link, and it leans toward a weak or inconsistent link between susceptibility to different response effects. It should be cited in a re-bet's Prior work line, and its predicted direction named (fail or mixed). It is not a statement of this bet's predicted outcome on a model.

## Required fixes

The verdict is **redesign**. Withdraw em-gm2bf1f1 before any call (`ledger/bets.jsonl` `verdict: withdrawn`, with a DEVIATIONS row naming this review), and re-bet as a new pre-registration with a new lesson. F2–F5 must not be carried into the re-bet.

- **F1 (D11, redesign).** As built, P(pass) is about 0 in every world consistent with the archive and with em-gm2q's real fresh Haiku run on gm2's items: 0/100 resampled; that real run fails the spliced rule. Two re-bets would ask a question this one cannot:
  - **(a) Specification.** Is W a confound or the trait? Pre-register a cross-fitted guard, with W and Eo taken from repeats disjoint from those giving S (the em-gm2bf1 audit's free precursor). Name in advance which guard reading counts as "beyond noise". Archive only, $0.
  - **(b) Items.** The intervals' width comes from items, not conversations. Run new items that have both six-format and order data.

  Either way, the dry run must include a world consistent with the existing runs (resample, plus em-gm2q's real fresh chains), not only additive-link worlds. If neither fits under $1, withdraw without a re-bet.
- **F2 (D8).** In any re-bet that keeps a stricter rule than em-gm2bf1's, delete "em-gm2bf1's pass did not repeat on a fresh run" and §1's "most likely that run's noise". Add a reported secondary, "em-gm2bf1's own rule on the new data: pass/fail". The fail sentence may then say the parent's pass did not repeat only when that secondary fails.
- **F3 (D7).** Correct "6 per order" for em-gm2q2's Opus shown chains to "4 per order" (reps 0–3) wherever it is used. Wherever "fresh" is claimed, state the existing free order archives: em-gm2q's Haiku and Sonnet on gm2's 10 items, and em-gm2q2's Sonnet on gm2b's 30.
- **F4 (D10).** Store `req_sha256 = sha256(json.dumps([model, texts, params(model, [])], sort_keys=True))` in each cache entry, and refuse to reuse an entry whose hash differs (as `gm2q2_opus_sonnet30.py` lines 145–152 do).
- **F5 (D10).** In `analyse()`, compute `n_conversations` and `n_missing` over the full prefixed keys: `{k: v for k, v in full.items() if not k.startswith("_")}`, not `k.split("|", 1)[1]`. The current code collapses Sonnet's 240 conversations onto Haiku's.
