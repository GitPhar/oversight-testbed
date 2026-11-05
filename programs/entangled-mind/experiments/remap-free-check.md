# Free follow-ups checked before pre-registration (2026-11-05 06:05 America/Denver)

Written by the program 1 follow-up session before any of these directions was pre-registered. Sean's words: program 1 keeps growing as a path of bets. This session takes the remap's free follow-ups (`map/entangled-mind.md`, remap `9773f6a`) in order of the map's odds. Free means archived data or laptop only, with no API spend and no local model loaded. Before betting, each direction was checked against the numbers already published in its parent's results file (pattern P12: a bet whose answer is already known, or that cannot pass at the n available, buys calibration without information). No archive was opened for these checks except where stated.

## In plain English

Four of the ten free follow-ups are not real bets, so they are set aside (parked, unscored) rather than bet on:

- **g-f1, Opus's own confidence flags its errors.** The answer is already published. em-dm3 (`results/mm-gm1-self-knowledge.md`) has Opus rating its own 298 answers: AUROC 0.904, against the event's bar of 0.75. A bet on it could not fail.
- **g-f2, error-flagging unchanged by question order.** It cannot pass on this archive. The archive holds Haiku and Sonnet, not Sonnet and Opus as the remap wrote. Its conversation cells have 68–197 parsed questions, some with as few as 4 errors. A simulation built only from those published counts, in the world most favourable to the event (no true order effect at all), meets the event in 0 of 300 runs. The 95% interval of the order difference is 0.24–0.31 wide, and the event needs it under 0.16 (`remap_free_check.py`). It would need roughly four times the parsed questions per cell.
- **dm6-f1, calibration changes with format on Haiku and Opus.** It is not free. The six-format claims (gm3b, em-dm2) have no truth labels, so a calibration score cannot be computed without new calls. Sonnet's part of the event is already published (−0.143). Parked until a session with an API budget picks it up.
- **gm3c-f2, held-out format recovery on Sonnet.** The answer is already published. `results/mm-gm3b-format-invariance.md` gives Sonnet's recovery Q = 0.69 [0.53, 0.82], whose upper bound is far above the event's 0.5. Opus's arm is incomplete (68 of 80 claims).

Two more are ruled out by this session's brief, not by the data: gm5-f1 and gm5-f2 need an open model loaded on the laptop.

That leaves, in odds order: dm6-f2 (0.55), gm3c-f1 (0.45), gm2b-f1 (0.40), bm9-f1 (0.40, only if the archive holds the structure) and bm9-f2 (0.25). They are bet in that order.

## What was looked at

- Published results files only: `results/mm-gm1-self-knowledge.md`, `results/calibration-under-format.md`, `results/mm-gm3b-format-invariance.md`, `results/gm3c-heldout-format.md`, `results/gm2b-self-conditioning-40.md`, `results/bm9-contrast.md`, and the audits `ledger/audits/em-dm6.md`, `em-gm3c.md`.
- Archive structure only, with no statistic computed: the key format and one record of `results/gm3b-calls.json`, `results/cal-sonnet-conversations.json`, `results/gm2b-conversations.json`, `results/mm-gm2-sonnet-conversations.json`, `results/bm9-contrast.json` and `results/gm3c-heldout-format.json`. Each later pre-registration repeats what it saw.

## Reproduce

`python programs/entangled-mind/experiments/remap_free_check.py` (fixed seed 20261105; numpy and scipy; about 20 s).
