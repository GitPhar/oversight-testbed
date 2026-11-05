# TASKS.md — open items, decisions made, and what is waiting on whom

Read after CONTEXT.md. The nightly updater rewrites this file from the day's commits; the morning operator builds the wave from it. Done items move to the bottom with their commit. Nothing is deleted.

Last rewritten: 2026-11-04 17:10 America/Denver, by hand, from the founding session.

## Standing rules learned from Sean (apply every day)

- Never ask Sean to create a repo, click a button, or run a git command. The engine creates what it needs. Programs live inside this repo as `programs/<name>/` so no repo creation is ever needed.
- Never tell Sean to close a tab. Each session's report ends with its `✻ … done` line; he decides.
- Read session state from the repos (commits, results files) and say what landed; never ask him to paste terminal output.
- No pacing decisions on his behalf ("tomorrow's wave"): anything worth doing goes in the next wave now. He works long days.
- Human bets are at direction level only: "is this worth about $X? will it come back a hit?" Technical sub-bets are engine-only.
- Every reply to Sean: plain English first, TL;DR of three lines max, then "YOU, NOW" with one step. One paste per terminal tab, the first message folded into the launch command.
- Costs under $10/month are the engine's call. Above that: the number and a one-sentence recommendation.
- QPU budget rulings under the 420 s hard stop are the engine's call (Sean, 2026-11-04, st-13). Each hardware bet still needs its pre-registration, lesson and design-review go; the engine logs its budget ruling as a steer citing st-13.
- No midday check-in. Morning and nightly only.
- Quantum hardware is a referee and a seed source, never a computational resource; every mention states its limits first.
- The project's title is still open; sessions do not propose names unless asked. Placeholder slug `oversight-testbed`.

## Decisions made (do not reopen)

- Programs are folded into this repo under `programs/` with their git histories imported (subtree), entangled-mind included; the standalone `GitPhar/entangled-mind` repo is left untouched as program 1's historical record. No separate program repos, ever.
- Program 3 wave-2 repeat test (ng-p3-15) approved, full design, ≤10 QPU s (about 6.8 s planned), two runs ≥3 h apart (st-11, st-13).
- P2-3 re-bet on lower-severity stories approved, under lesson + design-review rules.
- D46 relabelled exploratory. Experiment 5 re-issued CLASSICAL under its own rule on single-scale q. Probe result verified by DP2.
- Feedback loop (operators/learn.md) and design review (operators/design-review.md) are mandatory for every pre-registration from 2026-11-04 17:00.
- The No Credence paper's title and claims are scoped to what replicated (Haiku holds, Sonnet partly, Opus contradicted on formats).

## Open now (engine work, no human needed)

1. ~~Fold the programs into `programs/`~~ done 2026-11-04 17:40 (all four, entangled-mind included). Still to do: the morning and nightly task prompts (cloud routines) to the new paths; subtree-pull any late commits from the old folders as their sessions report.
2. Program 4 (settled-science, the published-record referee): running; item-writer and bettor separated, bettor has no web; ≥60 post-cutoff items primary; $5 cap.
3. ~~Site fixes~~ done 2026-11-04 (15ec83d, rebuilt after the fold): gauges regenerate on every push (54 s, 1 of 8 reversed, API from ledger/spend.jsonl); map hover shows cheapest test and cost; cockpit "Next to run" strip.
4. Program 3: corrected P3-5 pre-registered; simulator fix (D8) audited before reuse; wave-2 repeat test run.
5. Program 2: P2-3 re-bet; P2-5 onward as mapped, each with lesson + design review.
6. Ledger: link the founding-week audits (entangled-mind audits/) into ledger/audits/; score the scored-veto shadows as they resolve; plant pl-002 drawn at random this time.
7. Engine paper: fold in program 4's design and the referee comparison as suggestive; keep every number traceable to a file.
8. Application folder: keep the walkthrough script and checklist current with the ledger.

## Waiting on Sean (only these)

- Cockpit: enter gut odds on a few open cards (Program 2 or 3), download, and tell any session "commit my odds". The human column on the site is empty until then.
- OSF: create a free account at osf.io and say so; a session registers the pre-registration files.
- Support ticket to Anthropic for the two `reasoning_extraction` refusals (request IDs in `programs/entangled-mind/results/refusal-sonnet-replication*.md`) and the one `general_harms` refusal (om-p2-3).
- "Why Anthropic?" essay, 200–400 words, in his own words; a session polishes.
- The project's title, when it comes to him.

## Deliverables by 2026-11-22

1. Engine repo with the five commitments, the ledger (engine + human + Brier by referee), audit log, kill log, lessons, the site (map, cockpit, instruments, calibration, record, papers).
2. Paper: the engine (formal, related work, H1–H5), with the first two weeks of ledger as evidence.
3. Paper: No Credence to Read (scoped), and The Entangled Mind (short negative result).
4. Programs 2, 3, 4 each with ≥10 settled bets; the three-referee comparison stated as suggestive.
5. Application: research-interest answer, one-page proposal, Why Anthropic (Sean), ten-minute walkthrough recorded by Sean.
6. Reproducibility: one command per program.

## Done (most recent first)

- 2026-11-04 17:00 Feedback loop, design review, plant pl-001 caught (1/1), site gauges for both (oversight-testbed f0fbe9c).
- 2026-11-04 16:5x Program 3 audit follow-ups, simulator bug fixed, P3-1 re-run still fail (nature-graded f63bc4f).
- 2026-11-04 16:4x day-two.md; audit round 2 scored; paper + application merged (9b2040b).
- 2026-11-04 afternoon Cockpit, instruments, scored veto, plant procedure, pre-mortem, hardware doc; programs 2 and 3 wave 1; probe rerun DP2 verified.
- 2026-11-04 13:10 Site live at gitphar.github.io/oversight-testbed; engine repo public.
- 2026-11-04 morning Eleven overnight tests; three robustness runs; multi-model replication; first full audit (38/39 overclaims, 0 reversals); audit cuts applied (D51–D54).
- 2026-11-03 Program 1 built and run end to end; hardware witness certified 3/3; quantum error-prediction closed negative on two models.
