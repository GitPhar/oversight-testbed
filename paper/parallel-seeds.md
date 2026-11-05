# Two seeds, one engine: the design for path dependence (proposal.md Q4)

Written 2026-11-05 by a fresh session on the `proposer` branch, from `proposal.md` Q4, `ARCHITECTURE.md` (`path_dependence_test`), the two archive attempts (`om-p2-path`, withdrawn, other-minds D19a; `om-p2-path2`, parked, D21b) and `ledger/loop-check.md`. It is a design, not a pre-registration: nothing here has odds, a seed or a run date. It sits on the map as direction `P2-parallel` under `P2-path` in `map/other-minds.json`, with a cockpit card and no engine odds. It opens only on two `choose_seed` steers from Sean, one per seed question.

## In plain English

The proposal's fourth question asks whether the engine's research agenda depends on where it starts. Give the same machine two different starting questions and the same rules, and watch: do the two maps grow toward each other, do the same kinds of direction get killed, do the two ledgers look alike? The engine tried to answer this twice today from saved data and could not, for a reason that is itself the finding: program 2 was seeded by program 1, so they were never two independent starts, and most of the recorded traps came from program 1, so any shared trap was program 1's by construction (`programs/other-minds/DEVIATIONS.md` D19a, D21b). The only honest version is the one the proposal wrote: two seed questions, run from scratch, in parallel, by sessions that share the rules and nothing else.

The design below adds one thing the proposal left out. Two sessions given the *same* seed will not produce the same map either: a fresh session is a new draw, and metascience's many-analysts studies found that teams handed one data set and one hypothesis reach different answers through defensible choices (Silberzahn et al. 2018, *Advances in Methods and Practices in Psychological Science*; Breznau et al. 2022, *PNAS*; neither opened by this session, no number taken). So the question is not "do seeds A and B differ" but "do A and B differ more than two runs of A differ". That needs at least three runs, and the clean version needs four.

## The runs

| run | seed | session | what it shares with the others |
|---|---|---|---|
| A1 | seed A | fresh session 1 | the rules snapshot only |
| A2 | seed A | fresh session 2 | the rules snapshot only |
| B1 | seed B | fresh session 3 | the rules snapshot only |
| B2 | seed B | fresh session 4 | the rules snapshot only (the cheapest version drops B2) |

**The rules snapshot.** One commit on `main`, named in the pre-registration, from which four worktrees are made. Each worktree holds: `CONTEXT.md` sections 0, 1, 3, 6, 7 and 9 only (the rules and the operators; not sections 2, 4, 5 and 8, which describe the other programs' results, maps and steers); `ARCHITECTURE.md`; every file under `operators/`; `ledger/prior.md` frozen at that commit; the pattern lines of `ledger/lessons.jsonl` (rule 9 requires them, so they are rules); the checks (`ledger/check_prereg.py`, `check_remap.py`, `seed.py`, `plants.py`, `merge_inbox.py`); the site code. It does not hold `programs/`, `related-work/`, `map/`, the results files, the audits, `ledger/bets.jsonl`'s rows or `ledger/human-odds.jsonl`. "Share the rules and nothing else" is then a property of the checkout, not a promise.

**What each run does.** The ordinary loop, once: scout (full reads, searches recorded, Prior work lines), map with rule-14 odds elicited from the frozen `prior.md`, cockpit cards, wave 1 of three bets under a $5 program cap on the three models (rule 12), lessons, design reviews, runs, Novelty lines, audits with sealed plants, scoring, and a remap. Its ledger rows go to its own inbox file and are **not folded** until every run's wave 1 is settled, so no run's `prior.md` or odds can see another run's outcomes. The design reviewer and the auditor for each bet are launched by the main-checkout session, never by the run's own session, and are given only that run's worktree (`ledger/loop-check.md` E5).

**The seeds.** Two questions never scouted by the engine. Sean chooses both from the cockpit (`operators/propose.md` Step 5): the proposals of 2026-11-05 are three candidates, and any pair of them, or any two questions of his own, serve. The design does not name them; it only requires that neither seed is a follow-up of an existing program, so neither inherits a map.

## What is measured

Pre-registered before any worktree is made, with the codebook and the scorer committed first:

1. **Map overlap.** Each run's ten highest-weighted directions after the remap are tagged by a blind classifier (a fresh no-tool subagent given the direction's title, assumption at stake and cheapest test, with run and seed names removed) into mechanism classes from a fixed codebook written before the runs from the existing maps' nodes (for example: order of questions, own-turn position, answer format, stated threshold, penalty or stake, audience cue, item property). The distance between two runs is one minus the Jaccard overlap of their tag sets. A second classifier (Sonnet where the first is Opus) is run for agreement, reported.
2. **Kills recurring.** For each pair of runs, the share of run X's rules-out sentences that cover a direction mapped, bet or killed in run Y, judged blind by the same classifier from the rules-out sentence and the candidate direction's title. Distance is one minus that share, averaged over both orderings.
3. **Ledger divergence.** Each run's wave-1 hit rate with its Wilson interval, Brier, withdrawals before data, and the patterns cited and recurred (P ids). Reported, not tested: three bets per run cannot carry a test.
4. **Crossing.** Directions that carry the same mechanism tag in two runs with engine odds on opposite sides of the frozen prior. Counted and listed.

**The statistic.** For measures 1 and 2: `D_between`, the mean distance over the between-seed pairs (A1–B1, A2–B1; and A1–B2, A2–B2 with four runs), minus `D_within`, the mean over the within-seed pairs (A1–A2; and B1–B2). The null is built by permuting run labels over the tagged units within each pair of runs (10,000 shuffles), which gives an interval on the difference even with three runs.

**What counts as path dependence.** The pre-registered rule: path dependence is shown on a measure if `D_between − D_within` is at least 0.20 with its 95% permutation interval above 0, on both measures 1 and 2. **Convergence** is shown if `D_between` is within 0.10 of `D_within` on both, with the interval inside plus or minus 0.20. Anything else is undetermined and says so. The pass sentence, the fail sentence and the undetermined sentence are written in the pre-registration before the first worktree exists (P9).

**What would make it untestable.** A run that does not settle three bets (refusal, cap, crash) within the window; a classifier agreement below 0.6 on the tags; a rules snapshot that leaks (a run's session found reading another program's files, checked from its transcript where kept).

## What it costs

| item | per run | three runs | four runs |
|---|---|---|---|
| scout and map (web reads, a session) | $0 | $0 | $0 |
| wave 1, three bets on three models | up to $5 (cap in code) | $15 | $20 |
| design-review pilots | at most $0.30 | $0.90 | $1.20 |
| audits, plants, remap, classification | $0 (fresh subagents) | $0 | $0 |
| session time | about three hours | about nine hours, in parallel | about twelve |
| chip | 0 QPU s | 0 | 0 |

About $16 for three runs and $21 for four, inside the $200 month; each run is its own program under rule 4's $10, but the whole thing is above $10, so the number is stated here for Sean rather than decided by the engine. Nothing else in the engine runs beside it: the handoff's rule that a local-model job runs alone applies in spirit, since four scouts and four waves at once is the load that crashed the Mac on 4 November with nine sessions and two local models.

## What the answer changes

- **Seed-locked** (path dependence shown): choosing the seed is the human's largest lever, larger than any odds he gives, and `operators/steers.md` should weight `choose_seed` steers by what their programs landed; the import rule is not pulling the maps together; the proposal's Q4 answer is that the engine is a mirror of its question.
- **Convergent**: the engine's agenda is robust to where it starts, the rules and the reads do the work, and a single seed's program can be read as representative; the human's lever is elsewhere (vetoes, budgets, the rules).
- **Undetermined**: the within-seed noise is as large as the between-seed difference, which is itself the finding the many-analysts literature predicts; the next test is more runs per seed, not more seeds.

## Limits, stated once

Three or four runs give a permutation interval, not a p-value anyone should lean on. Every session is the same model family, so "two fresh sessions" are two draws from one distribution, not two researchers. The $5 cap per run means every wave 1 is three cheap tests, so maps may converge on cheap mechanisms by construction; the codebook must tag mechanism, not cost. The classifier is also Claude; its agreement rate is published and a disagreement is a reported row. The rules snapshot shares the eighteen patterns, so what is measured is path dependence given the engine's rulebook, which is what Q4 asks.

## How it enters the record

- Direction `P2-parallel` on `map/other-minds.json`, parent `P2-path`, no engine odds (elicited under rule 14 at pre-registration from the frozen `prior.md`), with its Prior work line and this file as its design.
- A cockpit card in `map/cockpit-cards.jsonl` (program `other-minds`, direction `P2-parallel`).
- It opens when `ledger/steers.jsonl` holds two `choose_seed` steers naming its seeds, and the main-checkout session commits the rules snapshot and the pre-registration of the measurement protocol before any worktree is made.

**Prior work line.** No published statement found on whether an AI research agent's map depends on its seed question (`paper/novelty.md` finding 10's search; proposal.md's related-work gap). The nearest work predicts the within-seed arm matters: many-analysts studies in metascience (Silberzahn et al. 2018; Breznau et al. 2022; not opened) found teams given one data set and one hypothesis diverge through defensible choices, which predicts `D_within` well above 0 and makes a three-run design necessary. The engine's own archive attempts (om-p2-path2, D21b) found sibling programs share most recorded traps, which predicts measure 2's distances are small everywhere (convergence direction on kills). *Predicts:* mixed. *Search:* this session read the two archive bets' deviation rows and the proposal; the metascience papers are named from the field, not opened.
