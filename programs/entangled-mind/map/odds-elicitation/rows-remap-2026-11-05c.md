# Rows handed to the odds elicitors, remap 2026-11-05c

Each fresh context received the template v2 instructions, `ledger/prior.md` at `34d6b1f` verbatim, and exactly one row below (the whole prompt is reproducible from `ledger/prior.md` at that commit plus the row). Nothing else: no earlier odds on the direction, no earlier bet on it, no audit or review notes beyond the parent's one-sentence finding, no human odds, no other follow-up's odds.

### bm9-f3

Title: Is the main rating less extreme after sub-questions than when asked first, beyond regression to the mean, on Haiku, Sonnet and Opus?
Assumption at stake: bm9's assimilation is a pull toward the number just given; the audit's rival is that the main rating simply becomes less extreme whenever sub-questions come first.
Cheapest test (design): Archive only: per item, the main question asked first (MF arm, turn 1, all four arms) against the main question after four sub-questions (O1-O4 shown chains, no earlier main answer), in gm2 and gm2b (Haiku, 40 items) and em-dm4 (Sonnet and Opus, gm2's 10 items).
Moderation ratio = slope of the after-mean on the first-asked mean from half A of repeats, divided by the slope of the half-B first-asked mean on half A (the regression-to-the-mean baseline); a one-way shift goes to the intercept at 50.
Models: claude-haiku-5-5, claude-sonnet-5-5, claude-opus-5-5 — No new calls; Sonnet and Opus are reported by point estimate only, because em-dm4 holds gm2's 10 items (16 first-asked ratings per item; 16 Sonnet and 8 Opus after-chain ratings per item), too few items for an interval.
Cost: $0 (archive: gm2-conversations.json, gm2b-conversations.json, mm-gm2-sonnet-conversations.json, mm-gm2-opus-conversations.json; no API call, no local model; their $0.55 + $1.68 + $7.08 is already spent)
Draft pass rule (the event you give P(pass) for): On Haiku's 40 items, the moderation ratio (slope of the mean main rating after four sub-questions on the half-A mean of the main rating asked first, divided by the slope of the half-B first-asked mean on the half-A mean, both split directions averaged) is at most 0.85 with item-bootstrap 95% upper bound below 1.0; Sonnet and Opus point estimates reported. Scoreable: yes.
What its parent result found (one sentence): On Haiku, most of the measured lean toward the last sub-rating comes from the main rating being less extreme after a sub-question, and the sub-rating's own level adds little.
Prior work line (what published work predicts for this test): No LLM test of moderation found after WebSearch for dilution, central tendency and multi-turn extremity (2026-11-05). Nearest: Kapetanovic et al. 2026 (arXiv:2608.25869; eight models incl. Claude-4.5-Sonnet) find a prior score lowers ratings almost regardless of its value; Temkit 2026 (arXiv:2605.22714) finds any history shifts Claude 4.x judgments toward no, a shift, not moderation. Adds: a slope against a split-half baseline, on three Claude models.
Its row on each table of prior.md: program = entangled-mind; referee = model; cost tier = free ($0); source = literature; layer = layer 4.

### gm2bf1-f3

Title: Does the order-format link survive a noise guard measured on separate repeats, with the guard's imprecision corrected?
Assumption at stake: The frozen guard removed the order-format link because the noise covariate was computed from the same draws as the order span, not because rating noise is the whole of the link.
Cheapest test (design): Archive only: per claim, order span S from repeats 0-4 and within-order SD W and order-archive extremity Eo from repeats 5-9 (and the reverse, averaged), against gm3b's format spread G on Haiku's 160 claims.
Frozen guard (E + W, linear ranks) and D71 guard computed; W's split-half reliability gives an errors-in-variables partial (Westfall and Yarkoni 2016); the same-half partial is reported beside it.
Models: claude-haiku-5-5 — Archive only, no calls: only Haiku has both the six-format archive and 10-per-order chains on the same 160 claims; Sonnet's order chains in em-dm4 are 4 per order and Sonnet's link is gm2bf1-f2; Opus's format arm is incomplete (68 of 80 claims).
Cost: $0 (archive: gm2-conversations.json, gm2b-conversations.json, gm3b-calls.json; no API call, no local model; the audit's run of the parent script took 33 s wall)
Draft pass rule (the event you give P(pass) for): On Haiku's 160 claims (40 item clusters), with S from repeats 0-4 and E, W from repeats 5-9 and the reverse averaged, the frozen guard's partial Spearman rho(S, G | E, W) has 95% item-cluster lower bound > 0, and the partial corrected for W's split-half reliability also has lower bound > 0. Scoreable: yes.
What its parent result found (one sentence): On Haiku the order-format link passed only under the design review's guard; under the guard first frozen, and under noise alone, it vanished, though a fresh run reproduces the order spans almost exactly.
Prior work line (what published work predicts for this test): No prior statement found on an item-level order-format link after WebSearch on order and format sensitivity, attitude strength, LLM anchoring (2026-11-05). Nearest work predicts a fail: Zhuo et al. 2024 (arXiv:2410.12405), Owusu and Feldman 2026 (ACL Short 174-180) and Temkit 2026 (arXiv:2605.22714) find each manipulation hits low-certainty items hardest, a shared driver the guard removes. Adds: a guard on separate draws, reliability-corrected (Westfall and Yarkoni 2016).
Its row on each table of prior.md: program = entangled-mind; referee = model; cost tier = free ($0); source = literature; layer = layer 6.

### gm3c-f3

Title: Is the format gap the format, or any rewording? Reword two formats and measure how much of the original each recovers
Assumption at stake: The part of each format's answer that the other five formats cannot recover belongs to the format itself, not to the exact wording of the prompt.
Cheapest test (design): New calls: the 0-100 rating and the frequency format, each reworded once with the format and meaning kept (wording fixed and committed before any call), on gm3b's claims, 10 repeats (Opus 4).
Per format, paraphrase recovery Q_para = R2 of the original format's odd repeats from the reworded mean (gm3c's cross-validated monotone link) over the original's split-half ceiling, set beside the same formats' cross-format Q from the archive.
Models: claude-haiku-5-5, claude-sonnet-5-5, claude-opus-5-5 — Haiku is the primary on its 160 archived claims; Sonnet (80 claims) and Opus (68 complete claims, 4 repeats for cost) are reported, not in the pass rule, because their original-format archives (em-dm2) cover fewer claims.
Cost: about $2.00 at measured per-call batch costs: Haiku $0.41/9,600 = $0.0000427 x (160 claims x 2 formats x 10) 3,200 = $0.14; Sonnet $2.04/4,800 = $0.000425 x (80 x 2 x 10) 1,600 = $0.68; Opus $8.88/4,080 = $0.00218 x (68 x 2 x 4) 544 = $1.19; total $2.01
Draft pass rule (the event you give P(pass) for): On Haiku's 160 claims, the mean paraphrase recovery Q_para over the two reworded formats (0-100 rating, frequency) is at least 0.75 and exceeds the same two formats' cross-format Q (recomputed from gm3b-calls.json on the same claims) by at least 0.20, with the item-cluster 95% interval of that difference above 0. Sonnet and Opus reported. Scoreable: yes.
What its parent result found (one sentence): Haiku's six answer formats share well under half of what each format reproducibly says about a statement, while Sonnet's share more.
Prior work line (what published work predicts for this test): No test of this rule found; nearest work leans toward a pass for capable models only. Smolin and Wilder 2026 (arXiv:2609.07943; nine non-Claude models) predict payoff-equivalent decision rewordings zero-shot at pooled R2 about 0.6-0.8 for the most capable; Alhetelah and Ahmad 2026 (WASSA, 2026.wassa-1.5) find Claude 3.7 Sonnet's yes/no answers agree across paraphrases at kappa 0.665. Adds: paraphrase recovery against a same-prompt ceiling, beside cross-format recovery.
Its row on each table of prior.md: program = entangled-mind; referee = model; cost tier = $1 to under $5; source = engine; layer = layer 5.
