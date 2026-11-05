# sg-b8: Tsui's fix on a graded penalty, does prepending "Wait" to the own-turn grading request take away the blunting sg-b3 found? (result)

Pre-registered in `experiments/sg-b8-wait.md` (`98d403a`, 2026-11-05 12:20 America/Denver), direction sg-d15. The seed is CURBy-RNG pulse 1592625 (`1389f07`). The direction's cockpit card went up first (`829d4ed`, 11:31).
- **Design review** (`ledger/design-reviews/sg-b8.md`): fix-first with 1 flaw (`06bbb46`), no pilot. The fix is D28 (`8b65ee9`), confirmed go at 12:32, before the first call.
- **Run:** 2026-11-05, 12:33:09 to 12:37:18 America/Denver. **900 calls, complete, no refusal, $1.219** of the $1.40 cap. The program has spent **$7.15 of $7.65** (budget ruling br-019, D19).
- **Odds:** engine 12 (v2; the map stated none). No human odds.
- **Audit:** `ledger/audits/sg-b8.md` (`9bbca4a`). The verdict stands as fail, with 4 required cuts, all applied under D30 (plant pl-043: clean).

## In plain English

**Pre-registered verdict: fail.** In the pre-registered words (§5.2, as D28 reads them):

> On Haiku and Opus 5.5, starting the grading request with 'Wait.' changed the penalty in their own conversation by less than half of their sg-b3 blunting (the 95% domain-cluster CI lies below Haiku 6.3 and Opus 3.0 points of 100) (in this run W was −0.34 of Haiku's G0 = +13.0 [+9.9, +16.2] and 0.14 of Opus's G0 = +6.0 [+4.9, +7.1]): on this design, Tsui's correction marker placed in the user's request does not take away half of the blunting sg-b3 measured; this test does not say whether it would at the end of the model's own turn, where Tsui places it. Haiku docked the overclaim less, not more, with 'Wait.' (W = −4.45 [−8.07, −0.73]).

**What was done.**
- sg-b3 found that Haiku and Opus went easier on an exaggerated sentence added to their own conclusion when they graded it in the conversation that wrote it than when they saw it fresh. That was already in print, and Tsui 2025 reported that adding "Wait" after a model's own mistake removes most of this kind of blind spot.
- Here each model graded the same texts three ways in one sitting: in its own conversation as before; in its own conversation with "Wait." at the start of the grading request; and fresh. Haiku and Sonnet on all 60 studies, Opus on 30.
- The measure, W, is how much more the exaggeration cost with "Wait." than without it, both in the model's own conversation.

**What the numbers say.**
- **The blunting was there to remove.** In this run, fresh minus own was +13.0 points on Haiku [+9.9, +16.2] and +6.0 on Opus [+4.9, +7.1], about sg-b3's size (12.6 and 5.4 on the same studies).
- **Haiku:** without "Wait." the exaggeration cost 67.0 points in its own conversation; with it, 62.5. W = −4.5 [−8.1, −0.7]: "Wait." made Haiku more lenient, not less. The flawed text itself scored 4.5 points higher with "Wait." (Fw −4.50 [−7.97, −1.00]); the clean text did not move (+0.05).
- **Opus:** 77.9 without, 78.7 with. W = +0.9 [−0.4, +2.1], well below its 3.0 bar: "Wait." took away about a seventh of its blunting, if any.
- **Sonnet** (reported): W = −0.25 [−1.3, +0.7]; no blunting to take away (+1.5).

**How strong it is.**
- Neither reading is fragile: no single study or domain changes either. Haiku's median W is −3.0 (9 ties), Opus's 0.0 (4 ties).
- Both readings are the same on the study bootstrap.
- The spread of W across studies is larger than the dry run's measured noise implied (SD 11.6 on Haiku against about 8.3; 4.4 on Opus against about 2.9): either the studies differ in how "Wait." moves them, or the wait cells are noisier than the own-turn repeats the dry run borrowed for them (no repeat of a wait cell is archived); this test cannot tell which. Both intervals still lie wholly below their bars.
- Opus's grades with "Wait." cost the same as without it ($0.0039 against $0.0038 per flawed call), so "Wait." did not set it thinking longer.

**So, on this test:** a "Wait." at the start of the grading request did not take away half of the own-conversation blunting on either model (Opus's interval runs from none to about a third of this run's blunting, +2.15 of +6.0; Haiku's lies wholly on the wrong side of zero). On Opus it barely moved the penalty, and on Haiku it moved it the wrong way: Haiku went easier on the exaggeration with "Wait." than without it. This is the placement Tsui's paper did not test: the word came from the user, not as a continuation of the model's own reply, and the flawed text stayed in the model's own turn. Opus's near-zero change agrees with Chen et al. 2026, who found a "Wait," prefix added nothing beyond moving the claim out of the model's turn (a different placement: there the claim itself moved into the user's message); Haiku's move to more leniency fits neither Chen nor Tsui, and this test, which never moves the text, cannot say why either model responded as it did.

**What this does not show** (§6, D28):
- "Wait." was placed at the start of the user's request, not after the model's own output where Tsui places it: this says nothing about Tsui's placement.
- A user-written "Wait." can also read as the user doubting the conclusion; this test does not separate that from a self-correction trigger.
- One word with one punctuation; not "But", "However" or other wordings.
- The flawed text stayed in the model's own turn throughout.
- Opus on 30 studies; the exaggeration was planted, one wording, at the end; three models from one family, one item set. Not "models", not "every".
- **Multiplicity:** two scored readings by conjunction; no correction. Haiku's reversal is not a pre-registered reading; it is reported, uncorrected, because §5 item 5 commits to it.

**Novelty:** partly new. Tsui (2025, arXiv 2507.02778 v3, abstract and §4.1, HTML read) appended "Wait" after the model's own erroneous output and reports it cut the self-correction blind spot by 89.3% across 14 open-source non-reasoning models, with no Claude model in its "Wait" results and no condition putting the marker in a user message; Chen et al. (2026, arXiv 2606.05976 v2, Tables 1 and 2, HTML read) found a user message "Wait, c⋆" beat the same user message without the prefix in only 2 of 12 model–domain cells and state "the trigger is incidental and the carrier role primary", but there the claim itself moved into the user turn, and no "Wait" gain in their Table 2 fell below the audit-only baseline. This test's placement, the marker at the start of the user's grading request with the flawed text left in the model's own turn, scored as a graded penalty on a planted overclaim on the Claude 5.5 models, was not found in print: Opus's near-zero change agrees with Chen et al.'s reading, while Haiku's move to more leniency points the other way from both papers. The rival reading, a user turn read as doubt, has prior work on answer flipping (Laban et al. 2023, arXiv 2311.08596, abstract only: ten LLMs flipped answers 46% of the time when challenged with "Are you sure?") and on LLM evaluators swayed by user rebuttals (Kim and Khashabi 2025, EMNLP Findings, arXiv 2509.16533, abstract only), but none found tests a bare "Wait." in a grading request. Search: WebSearch plus arXiv abs/HTML reads, 2026-11-05, on "Wait" correction marker in the user turn versus the assistant turn; "Are you sure?" answer flipping and sycophancy to user doubt; LLM judge sycophancy under user rebuttal; "Wait" or reflection cues and leniency or score inflation in LLM self-evaluation; intrinsic self-correction (Huang et al. 2024, ICLR, arXiv 2310.01798, abstract only); structured reflection in clinical diagnosis (Mamede et al., search snippets only, not cited); full HTML reads of 2507.02778 v3 and 2606.05976 v2. By a fresh claude-opus-5-5 Novelty session (subagent).

## Tables

| model | studies | W | 95% CI (20 domains) | 95% CI (studies) | Fw | Fw 95% CI (domains) | penalty, own turn | penalty, own turn with 'Wait' | penalty, fresh | G0 = fresh − own | G0 95% CI (domains) | reading |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Haiku | 60 | −4.45 | [−8.07, −0.73] | [−7.32, −1.53] | −4.50 | [−7.97, −1.00] | 67.0 | 62.5 | 80.0 | +13.02 | [+9.90, +16.20] | **Wait does not** |
| Opus | 30 | +0.87 | [−0.42, +2.15] | [−0.63, +2.47] | +1.07 | [−0.10, +2.23] | 77.9 | 78.7 | 83.9 | +6.00 | [+4.94, +7.10] | **Wait does not** |
| Sonnet | 60 | −0.25 | [−1.30, +0.72] | [−1.23, +0.73] | +0.07 | [−0.83, +0.97] | 86.5 | 86.3 | 88.0 | +1.48 | [+0.35, +2.70] | reported only |

|  | Haiku | Opus | Sonnet |
|---|---|---|---|
| blunting left with 'Wait' (fresh − wait) | +17.47 | +5.13 | +1.73 |
| W as a share of G0 | -0.34 | 0.14 | -0.17 |
| sg-b3's G on the same studies (cross-run) | +12.58 | +5.43 | +1.37 |
| clean text, wait − own (points) | +0.05 | −0.20 | −0.32 |
| reading on the study bootstrap | Wait does not | Wait does not | — |
| fragile, one study dropped | no | no | — |
| fragile, one domain dropped | no | no | — |
| ties (W = 0) | 9 | 4 | — |
| median W | −3.00 | 0.00 | — |

|  | Haiku | Opus | Sonnet | total |
|---|---|---|---|---|
| test run | $0.026 | $0.628 | $0.565 | **$1.219** |

- W = (clean − flawed) with "Wait." − (clean − flawed) without it, per study, both in the model's own conversation; G0 = (clean − flawed) fresh − (clean − flawed) own; Fw = own flawed − wait flawed. Penalties are clean − flawed, in points of 100.
- **The bars:** Haiku 6.3, Opus 3.0 (half of each model's sg-b3 G). **Verdict** (§5): Haiku and Opus both read Wait does not → **fail**. Score 0 against engine odds 0.12.

Raw data: `results/sg-b8-grade-calls.json` (committed `a4b3d2a`, before this analysis). The analysis is `results/sg-b8-analysis.json`, regenerated by `python3 experiments/sg_b8_wait.py analyse` with no calls. The tables above are printed by `sg_b8_wait.tables()`.
