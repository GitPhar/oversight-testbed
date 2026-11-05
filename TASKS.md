# TASKS.md — open items, decisions made, and what is waiting on whom

Read after CONTEXT.md. The nightly updater rewrites this file from the day's commits; the morning operator builds the wave from it. Done items move to the bottom with their commit. Nothing is deleted.

Last rewritten: 2026-11-04 18:10 America/Denver, by hand, by the close-founding session (branch `close-founding`).

## Standing rules learned from Sean (apply every day)

- Never ask Sean to create a repo, click a button, or run a git command. The engine creates what it needs. Programs live inside this repo as `programs/<name>/` so no repo creation is ever needed.
- Never tell Sean to close a tab. Each session's report ends with its `✻ … done` line; he decides.
- Read session state from the repos (commits, results files) and say what landed; never ask him to paste terminal output.
- No pacing decisions on his behalf ("tomorrow's wave"): anything worth doing goes in the next wave now. He works long days.
- **Never ask Sean for odds or decisions in a terminal** (CONTEXT §3 rule 11). His odds come only from `ledger/human-odds.jsonl` (cockpit downloads, committed); if a direction has none when its bet is pre-registered, the bet proceeds marked "no human odds". A decision a session would have asked about, it makes under the rules and states in its report, for him to veto from the cockpit. His judgment is recorded and scored as steers: seed questions, vetoes, added questions, architecture decisions.
- Human bets are at direction level only: "is this worth about $X? will it come back a hit?" Technical sub-bets are engine-only.
- **Start every local session with `python3 ledger/pickup_human_odds.py`** (Sean's cockpit answers, saved to ~/Downloads/human-odds.jsonl) and commit what it appends to `ledger/human-odds.jsonl` and `ledger/steers.jsonl`. The cockpit promises him the next session does this.
- Every reply to Sean: plain English first, TL;DR of three lines max, then "YOU, NOW" with one step. One paste per terminal tab, the first message folded into the launch command.
- Costs under $10/month are the engine's call. Above that: the number and a one-sentence recommendation.
- In the shared checkout, commit only your own paths: `git commit -m "…" -- <paths>` (never `git add -A` / `git commit -a` at the root). Before committing a shared ledger file, `git diff <path>` and commit only your own hunks. See CONTEXT.md §2.
- QPU budget rulings under the 420 s hard stop are the engine's call (Sean, 2026-11-04, st-16). Each hardware bet still needs its pre-registration, lesson and design-review go; the engine logs its budget ruling as a steer citing st-16.
- No midday check-in. Morning and nightly only.
- **Morning operator's checklist, remap (from 2026-11-05):** run `python3 ledger/check_remap.py` before building the wave. If it reports any landed or mixed bet that ends the map, or any program's round has settled (every bet has a verdict and a finished audit) since its last "Follow-ups (remap <date>)" section, the wave's first tab is a remap of that program (`operators/remap.md`, launch line there). The wave then draws its bets from the follow-ups, cheapest first. No map may end at a landed bet with no follow-up.
- Quantum hardware is a referee and a seed source, never a computational resource; every mention states its limits first.
- The project's title is still open; sessions do not propose names unless asked. Placeholder slug `oversight-testbed`.

## Decisions made (do not reopen)

- Programs are folded into this repo under `programs/` with their git histories imported (subtree), entangled-mind included; the standalone `GitPhar/entangled-mind` repo is left untouched as program 1's historical record. No separate program repos, ever.
- Program 3 wave-2 repeat test (ng-p3-15) approved, full design, ≤10 QPU s (about 6.8 s planned), two runs ≥3 h apart (st-11, st-16).
- P2-3 re-bet on lower-severity stories approved, under lesson + design-review rules.
- D46 relabelled exploratory. Experiment 5 re-issued CLASSICAL under its own rule on single-scale q. Probe result verified by DP2.
- Feedback loop (operators/learn.md) and design review (operators/design-review.md) are mandatory for every pre-registration from 2026-11-04 17:00.
- The No Credence paper's title and claims are scoped to what replicated (Haiku holds, Sonnet partly, Opus contradicted on formats).

## Open now (engine work, no human needed)

1. The morning and nightly task prompts (cloud routines) to the new `programs/<name>` paths, and to CONTEXT §3 rule 11 (no questions to Sean in a terminal); subtree-pull any late commits from the old folders as their sessions report. (The fold itself is in Done.)
2. Program 4 (settled-science, the published-record referee): running; item-writer and bettor separated, bettor has no web; ≥60 post-cutoff items primary; $5 cap.
3. Site: two subtitle lines in `paper/figures-architecture-v2.svg` (the cockpit and pre-register boxes) run past their boxes; widen the boxes or shorten the lines.
4. Program 3: corrected P3-5 pre-registered; simulator fix (D8) audited before reuse; wave-2 repeat test run.
5. Program 2: P2-3 re-bet; P2-5 onward as mapped, each with lesson + design review.
6. Ledger: score the scored-veto shadows as they resolve; plant pl-002 drawn at random this time. Run `python3 reproduce.py` before every ledger commit.
7. Engine paper: fold in program 4's design and the referee comparison as suggestive; keep every number traceable to a file.
8. Application folder: keep the walkthrough script and checklist current with the ledger.
9. Rule 11 follow-ups: ng-p3-15's F6 gate waits on "Sean's budget ruling". Under rule 11 and the cost rule (under $10 is the session's call), the program 3 session decides it, states it in its commit, and Sean can veto from the cockpit. Program 4's `human/make_form.py --score` still reads `human/answers.md`; make it read the program's lines in `ledger/human-odds.jsonl`.
10. New map items, engine odds stated by this session (not the v1 template; re-elicit before pre-registering): `qwalk`, entangled claims, quantum walk vs PageRank on program 1's claim graph, 0.04, $0; `bmq`, the biomimicry scout, 0.30, $0; `P2-path`, path dependence, 0.50, opens at program 2's 10th settled bet (2 now).

## Waiting on Sean (only these)

- Optional, never asked for: gut odds on any open cockpit card, downloaded and committed to `ledger/human-odds.jsonl`. Bets go ahead without them, marked "no human odds"; the human column on the site is empty until some arrive.
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

- 2026-11-04 ~18:10 close-founding branch, six jobs:
  - Rule: sessions never ask Sean for odds or decisions in a terminal; human odds only from `ledger/human-odds.jsonl`, else "no human odds"; his judgment scored as steers. In CONTEXT §3 rule 11, TASKS, ARCHITECTURE invariant 11, all nine operator docs, the odds template, programs 2–4's forms (`04a9cd2`).
  - Maps: `qwalk` (0.04), `bmq` as a scout item (0.30), `P2-path` (0.50, opens at program 2's 10th settled bet); steers st-13 to st-15 (`cd2308e`).
  - Founding-week audits linked into `ledger/audits/` (`em-<bet>.md`, `SUMMARY-1.md`), verdicts on the 19 em-* bets; em-gm3c pass → undetermined (unscored; Brier still 0.236 on 9); round 2's six program-1 re-audits copied from `audit2` (`73a413b`).
  - `reproduce.py` at the root: ledger tables, brier.md, scores.md, plants and site data rebuilt from archived files, no keys; ALL LEDGER TABLES AND SITE DATA REPRODUCED (`6c4361d`).
  - Architecture diagram on the site home page, referenced from ARCHITECTURE.md (`282142c`).
  - This TASKS update (the commit that carries it).
- 2026-11-04 17:31–17:45 (on main) Design reviews: om-p2-3b fix-first, confirmed (`5b154bd`, `93ec998`), fixes D9 (`9d0d2fb`), pilot 182/182 calls, 0 refusals, $0.0084 (`95f0e77`); ng-p3-15 fix-first, confirmed (`ebd2c80`, `ee3bf05`), fixes D11–D17 (`6e2368c`, `7c3671c`, `cefcb88`), F6 budget gate still open; ng-p3-5c pre-registered and seeded (`930efe8`, `03356ad`) and entered in the ledger (`c53ac3c`).
- 2026-11-04 17:20 settled-science leakage check: 213 calls, $0.47; 184 items frozen with SHA-256 (`4859d3b`).
- 2026-11-04 17:12–17:23 One repository: all four programs folded into `programs/` with full history (`32ca722`, `11de687`, `bf3c7a8`, `ebf7017`); site, docs and ledger point at `programs/<name>` (`5a618f6`, `50b8e0b`); late subtree pulls (`af3c62a`, `91eb2d6`, `065d0f8`); om-p2-3b and ng-p3-15 pre-registered, seeded and entered (`26ee5d2`, `7f9cedf`, `1677a8a`); p3sim points at programs/entangled-mind (`e939ce2`).
- 2026-11-04 17:06 Site fixes: gauges recompute from source on every build, map hovers show cheapest test and cost, cockpit "Next to run" strip (`15ec83d`).

- 2026-11-04 17:00 Feedback loop, design review, plant pl-001 caught (1/1), site gauges for both (oversight-testbed f0fbe9c).
- 2026-11-04 16:5x Program 3 audit follow-ups, simulator bug fixed, P3-1 re-run still fail (nature-graded f63bc4f).
- 2026-11-04 16:4x day-two.md; audit round 2 scored; paper + application merged (9b2040b).
- 2026-11-04 afternoon Cockpit, instruments, scored veto, plant procedure, pre-mortem, hardware doc; programs 2 and 3 wave 1; probe rerun DP2 verified.
- 2026-11-04 13:10 Site live at gitphar.github.io/oversight-testbed; engine repo public.
- 2026-11-04 morning Eleven overnight tests; three robustness runs; multi-model replication; first full audit (38/39 overclaims, 0 reversals); audit cuts applied (D51–D54).
- 2026-11-03 Program 1 built and run end to end; hardware witness certified 3/3; quantum error-prediction closed negative on two models.
