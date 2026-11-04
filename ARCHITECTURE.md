# ARCHITECTURE.md — the engine, in pseudocode

A scalable-oversight testbed for AI-driven research. The AI proposes, bets, runs and audits; a human steers from a map; both are scored. Built for trust, not volume.

## Objects

```
Program      = { question, repo, seed_date, status: open|closed, map: [Direction], ledger: [Bet], kills: [Kill] }
Direction    = { id, assumption_at_stake, prior_work: [Read], what_our_data_say, cheapest_test, cost, weight }
Bet          = { direction, pass_rule, statistic, budget, engine_odds, human_odds, prereg_commit,
                 result, audit, verdict: pass|classical|tie|null|untestable, scored: bool }
Read         = { paper, read_depth: full|abstract, what_tested, on_whom, result, limits, borrow, next_steps_it_suggests }
Kill         = { direction, diagnosis, evidence, date }        # nothing disappears
Steer        = { date, human, action: add_question|veto|budget|override_audit|choose_seed, reason, outcome_later, shadow_id? }
Shadow       = { steer, direction, engine_odds_at_veto, human_odds_at_veto, vetoed_budget, kind: archive_proxy|cheapest_version|none,
                 proxy_strength: direct|partial|weak, prereg_commit, outcome: hit|miss|undecided,
                 veto_value: saved|probably_saved|killed_hit|undecided }   # operators/veto.md; ledger/shadows.jsonl
Audit        = { auditor_session (has not seen the work), claims_checked, holes_found, overclaims_cut, verdict_stands: bool }
Ledger       = engine and human odds vs outcomes; Brier score per side; published
```

## The loop (one program, one cycle)

```
loop(program):
    # 1. SCOUT — all fields, full reads, filtered by cost and falsifiability
    reads = scout(program.question, fields = ALL, depth = full)
    for r in reads: r.next_steps_it_suggests = extract(r)          # the filter is the point
    candidates = reads.next_steps ∪ program.map ∪ human.added_questions

    # 2. MAP — rank, with odds stated before any data
    for c in candidates:
        d = Direction(c)
        d.cheapest_test, d.cost = cheapest_falsifier(d)           # cents before dollars; archives before API; API before hardware
        d.engine_odds = engine.P(real_result | d)                 # written down
        d.human_odds  = ask(human, d)                             # written down separately, before data
        d.weight      = f(surprise_potential, cost, odds, neighbourhood_heat)
    program.map = rank(candidates by weight)

    # 3. PRE-REGISTER — one commit, before the first call or the first archive read
    bet = top(program.map)
    bet.prereg_commit = commit(pass_rule, statistic, split, seed, budget, stop_rules)

    # 4. RUN — budget in code; stop-on-refusal; one scale direction; caches so a crash never pays twice
    bet.result = run(bet)
    write_results(plain_english_first, then_tables)

    # 5. AUDIT — an independent session that has not seen the work tries to break it
    bet.audit = audit(bet.result, by = fresh_session, stance = adversarial)
    if bet.audit.overclaims_cut: rewrite_results(bet, cuts)          # same commit series, never silently
    bet.verdict = decide(bet.result, bet.audit)

    # 6. LEDGER — score both sides
    ledger.record(bet.engine_odds, bet.human_odds, bet.verdict)
    publish(brier(engine), brier(human))

    # 7. RE-WEIGHT — surprise raises the neighbourhood; a null closes with a diagnosis
    if bet.verdict in {pass} and bet.audit.verdict_stands:
        for d in neighbours(bet.direction): d.weight *= HEAT; scout_more(d)
        queue(replicate(bet, models = [more], designs = [more]))     # a hit is not a hit until it holds elsewhere
    else:
        program.kills.append(Kill(bet.direction, diagnosis(bet)))    # stays on the map, marked closed
        program.map.remove(bet.direction)

    # 8. STEER — the human's hand
    for s in human.steers_since_last_cycle: log(Steer s)             # every veto, question, budget call, override
        if s.action == veto and s.target is a research direction:     # a veto is a bet that the direction would not pay
            schedule(Shadow(s), not_before = +7 days, not_after = +30 days,
                     cheapest = archive_proxy, else cheapest_version(cap = min($2, 10% of vetoed budget)), never QPU)
    for sh in due(shadows): sh.outcome = run(prereg(sh)); score(sh)   # saved money, or killed a hit; never revives the direction by itself
    if human.says_switch_question: program = fork_or_switch(program)

    # 9. CONTEXT — nothing lives only in a chat
    rewrite(CONTEXT.md, from = {ledger, map, kills, steers, results})
```

## The engine itself is an experiment

```
path_dependence_test:
    run loop(seed_A) and loop(seed_B) in parallel, same engine, same rules
    measure: do the maps converge, diverge, or cross?  which kills recur?  does the ledger differ?
    this is the order-effect question asked of research itself

oversight_test:
    compare ledger(engine) vs ledger(human) vs ledger(engine + human)
    report where the human changed the outcome, and whether for the better
    vetoes included: each shadow says whether the veto saved money or killed a hit (ledger/scores.md)
    the honest answer either way is the result
```

## Invariants (never violated)

1. Odds before data, both sides, in writing.
2. Cheapest falsifier first; budget in code; stop rules; stop-on-refusal.
3. No result without an independent audit; the audit is published.
4. Nothing disappears: kills stay on the map with diagnoses.
5. Every program begins with full reads across all fields.
6. A pre-registered bar is never lowered after data.
7. A hit is not a hit until replicated on more than one model and design.
8. Plain English first in every artifact.

## Repositories

```
oversight-testbed/           # the engine (placeholder slug until the title is chosen; see CONTEXT.md §0)
  README.md                  # the five commitments, the ledger, the map, links to programs
  CONTEXT.md                 # the living brain; rewritten nightly; read first by every session
  ARCHITECTURE.md            # this file
  proposal.md                # the research proposal for the engine itself
  ledger/                    # bets.jsonl (engine odds, human odds, verdicts), steers.jsonl, shadows.jsonl, audits/;
                             # brier.py → brier.md (calibration), scores.py → scores.md (vetoes, catch rate, pre-mortems)
  map/                       # per-program maps as markdown + json
  operators/                 # morning brief, nightly updater, auditor, scout, pre-registration templates
  site/                      # GitHub Pages: papers as pages, record as timeline, calibration chart, map view
programs/
  entangled-mind/            # program 1 (own repo, already exists): quantum encoding (closed) → self-reports (open)
  <program-2>/               # own repo: theory of mind as third-person self-report
```

## Operators

```
morning  (07:03 America/Denver, cloud):  read CONTEXT.md → read both repos' last 24h → brief + today's wave (one paste per tab)
nightly  (23:33 America/Denver, cloud):  read day's commits → rewrite CONTEXT.md §state, §map, §steers → push
auditor  (per result, local tab):        fresh session, has not seen the work, instructed to break it, writes ledger/audits/<bet>.md
scout    (per program start, local tab): full reads, all fields, next-steps extracted, candidates ranked with odds; a form for the human's odds
shadow   (per veto, 7–30 days later):    fresh session, argued neither side; pre-registers and runs the cheapest look at a vetoed direction (operators/veto.md)
session  (any build tab):                reads CONTEXT.md first; obeys the invariants; commits with the deviation row it adds
```

## Staleness guard

```
if age(CONTEXT.md) > 36h: the morning operator says so and makes tab 1 of the wave a rewrite from the repos' current state
if any results file disagrees with CONTEXT.md: the results file wins; CONTEXT.md is corrected and the correction is logged
```
