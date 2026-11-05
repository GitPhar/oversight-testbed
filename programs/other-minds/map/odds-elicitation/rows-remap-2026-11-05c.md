# Rows handed to the odds elicitors, remap 2026-11-05c

Each fresh context received the template v2 instructions, `ledger/prior.md` at `34d6b1f` verbatim, and exactly one row below (the whole prompt is reproducible from `ledger/prior.md` at that commit plus the row). Nothing else: no earlier odds on the direction, no earlier bet on it, no audit or review notes beyond the parent's one-sentence finding, no human odds, no other follow-up's odds.

### P2-18

Title: Were Haiku's scattered guesses about another person's number a one-off? A fresh self-prediction run with a base arm
Assumption at stake: Haiku's over-scattered predictions of how another person's number moves its rating (om-p2-15: 17.2 against 8.8 points from its usual rating) are a stable feature of its self-model, not one session's scatter or a misjudged base rating.
Cheapest test (design): Re-run om-p2-4's self arm (a) on the 162 other-person uptake cells, 5 repeats, plus a base arm (32 statements, 5 repeats, no number shown), on Haiku.
Score om-p2-15's frozen rule over all 324 cells (the 162 own-source cells from om-p2-4's archive), and, as a secondary, the self-predicted shift against the self-predicted base.
Models: claude-haiku-5-5 — Haiku only: no archive holds Sonnet's or Opus's measured re-ratings on the other-person cells (P2-14 measures own-source cells only), so their truth would have to be measured first (about $1 on Sonnet); deferred until Haiku shows whether the scatter recurs.
Cost: about $0.065: (162 x 5 = 810 self-arm calls + 32 x 5 = 160 base calls) = 970 Haiku calls x $0.0000652 per call (om-p2-4's actual $0.899 / 13,796 calls) = $0.063; $0 QPU, no laptop hours
Draft pass rule (the event you give P(pass) for): On claude-haiku-5-5, over om-p2-15's 324 uptake cells (162 own-source cells from om-p2-4's archive; 162 other-person cells re-run fresh at 5 repeats), MAE(self-predicted re-rating) minus MAE(always-no-uptake predictor), in rating points, has a BCa 95% upper bound below 0 (om-p2-15's frozen rule, unchanged). Scoreable: yes.
What its parent result found (one sentence): On Haiku, self-predictions had about half the observer arm's error but the test could not tell (om-p2-4), and cell by cell they did not beat a no-effect guess because they scattered too widely on another person's number (om-p2-15).
Prior work line (what published work predicts for this test): No prior statement found for re-running a self-prediction to see whether its scatter recurs. Nearest: Blandfort and Pawar 2026 (arXiv 2609.09899) find prompted sycophancy self-predictions under-dispersed (per-condition SD at most 0.09), the opposite of om-p2-15's over-scatter; Singh, Linzen and Ravfogel 2026 (arXiv 2605.26242) require beating an input-only baseline, as this rule does. Adds: a fresh Haiku run and a base arm.
Its row on each table of prior.md: program = other-minds; referee = model; cost tier = under $1; source = literature; layer = layer 2.

### P2-19

Title: Does 'Sam moves more than self' appear on Sonnet once the planted answers are built from Sonnet's own usual ratings?
Assumption at stake: Haiku's 'Sam moves more than self' is Haiku's alone: it does not appear on a larger model even when the planted answers are built from that model's own usual ratings (om-p2-5r's null was not an artefact of Haiku's anchors).
Cheapest test (design): om-p2-5r's 568 prompts per repeat on Sonnet, 2 repeats, with each statement's anchor m set to Sonnet's own om-p2-6r base rating; Opus on 8 beacon-drawn vignettes at 1 repeat, reported.
Pre-step at $0: re-split om-p2-5r's archive by the side of each model's om-p2-6r base; then om-p2-5r's rule (gap_up, gap_down, dU) on the new cells.
Models: claude-sonnet-5-5, claude-opus-5-5 — Haiku is left out because om-p2-5 already ran it with its own anchors (program 1's Haiku ratings); Opus runs on 8 vignettes at 1 repeat because each call costs about 2.6 times Sonnet's (om-p2-5r).
Cost: about $1.80: Sonnet 568 x 2 = 1,136 calls x $0.000951 (om-p2-5r's $1.0804 / 1,136) = $1.08; Opus 284 calls (8 vignettes: REF 16 + 16, OWN self 84 + Sam 84, SWAP Sam 84) x 1 repeat x $0.002478 (om-p2-5r's $2.8152 / 1,136) = $0.70; anchors from om-p2-6r's archive (Sonnet 32 statements x 3, Opus x 2) $0; total $1.78
Draft pass rule (the event you give P(pass) for): On claude-sonnet-5-5, with m set to the mean of its om-p2-6r base repeats per statement (V = clip(m + d, 2, 98), d in +/-10, 30, 60, cells with |V - m| < 5 dropped), gap_up = U_sam(OWN) - U_self(OWN) on upward plants, gap_down on downward plants, and dU = U_sam(OWN) - U_sam(SWAP) each have a 95% vignette-bootstrap lower bound above 0 (om-p2-5r's rule); Opus reported, not scored. Scoreable: yes.
What its parent result found (one sentence): On Haiku a planted own answer swayed what it said a stranger thinks more than its own new answer (om-p2-5); on Sonnet and Opus, with planted answers built from Haiku's opinions, it did not (om-p2-5r).
Prior work line (what published work predicts for this test): No prior statement found on Sam-minus-own under a model's own anchors. Both nearest reads predict fail: Huang et al. 2025 (arXiv 2505.15392) find larger and reasoning models anchored on fewer questions (GPT-4o 27.3%, DeepSeek-R1 25.0%), so small gaps; Lee and Morewedge 2021 (Psychological Science) find noisier judgments take up anchors more, so Sam above self but Alex's number pulling Sam too, failing dU. Adds: Sonnet's own anchors.
Its row on each table of prior.md: program = other-minds; referee = model; cost tier = $1 to under $5; source = literature; layer = layer 2.
