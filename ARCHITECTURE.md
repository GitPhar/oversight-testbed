# ARCHITECTURE.md — the engine, in pseudocode

A scalable-oversight testbed for AI-driven research. The AI proposes, bets, runs and audits; a human steers from a map; both are scored. Built for trust, not volume.

The diagram, as built on 2026-11-04: [`paper/figures-architecture-v2.svg`](paper/figures-architecture-v2.svg) (also on the site's home page). This file is the authority where the two differ.

## Objects

```
Program      = { question, repo, seed_date, status: open|closed, map: [Direction], ledger: [Bet], kills: [Kill] }
Direction    = { id, assumption_at_stake, prior_work: [Read],
                 prior_work_line: "what published work predicts for this exact test, with citations | no prior statement found after <search>",   # rule 13
                 prior_work_predicts: pass|fail|mixed|unknown, what_our_data_say, cheapest_test, cost, weight,
                 novelty: known|partly_new|new, novelty_line }                            # on a landed or mixed node; the site shows it
Bet          = { direction, pass_rule, statistic, budget, engine_odds, odds_prior, odds_adjustment, odds_reason, human_odds, prereg_commit,
                 prior_work: "the §0 row: what the literature predicts for this pass rule, and what this bet adds",   # rule 13; design review D12
                 premortem: "If this fails, the most likely reason is …", premortem_kind: world|design|execution|artefact,
                 premortem_score: named|kind_only|other|not_failed|unclear,              # operators/premortem.md
                 result, novelty: known|partly_new|new, novelty_line, novelty_by,        # rule 13; a fresh session, before the write-up is final; audit F27
                 audit, verdict: pass|classical|tie|null|untestable, scored: bool }
Read         = { paper, read_depth: full|abstract, what_tested, on_whom, result, limits, borrow, next_steps_it_suggests,
                 predicts_for_us: [(direction, pass|fail|no bearing)] }                  # rule 13: the outcome, not the topic; searches recorded
Kill         = { direction, diagnosis, evidence, date }        # nothing disappears
Steer        = { date, human, action: choose_seed|veto|add_question|architecture|budget|override_audit, reason, outcome_later, shadow_id? }   # the human's judgment, recorded and scored
Shadow       = { steer, direction, engine_odds_at_veto, human_odds_at_veto, vetoed_budget, kind: archive_proxy|cheapest_version|none,
                 proxy_strength: direct|partial|weak, prereg_commit, outcome: hit|miss|undecided,
                 veto_value: saved|probably_saved|killed_hit|undecided }   # operators/veto.md; ledger/shadows.jsonl
Audit        = { auditor_session (has not seen the work), claims_checked, holes_found, overclaims_cut, verdict_stands: bool, plant_id }
Plant        = { audit, planter (never the auditor), planted: bool (p = 1/2, secret draw), class: overclaim|miscount,
                 commitment = sha256(plaintext + salt), revealed_after_audit, caught: bool }   # operators/plant.md; ledger/plants.jsonl
Ledger       = engine and human odds vs outcomes; Brier score per side; prior alone vs adjusted odds; published
Prior        = { hit rate of every scored bet, Wilson interval, by program | referee | cost tier | source | layer }   # ledger/prior.py → ledger/prior.md; handed to every odds elicitation
Lesson       = { bet, patterns: [P-id], lesson (one sentence, also in the prereg's §0), design_change,
                 odds_before_lesson, odds_after_lesson, read: {resolved, brier, base_rate, newest_audit}, recurred }  # operators/learn.md; ledger/lessons.jsonl
Pattern      = { id: P<n>, class, evidence from past misses and audit cuts, do_this, cited_by }                  # ledger/lessons.jsonl
DesignReview = { bet, fresh reviewer, checks D1–D12 on a dry run (no paid calls; D12 = is the predicted outcome already in print, and what does the bet add),
                 verdict: go|fix-first|redesign, missed (filled by the post-result audit) }                          # operators/design-review.md
Beacon       = { chain: CURBY-Q (Bell-certified, if live <24 h) | CURBy-RNG (if CURBY-Q stalled; stalled since 2025-08-22), round, pulse_time > prereg_commit, randomness,
                 seed = sha256(randomness ‖ bet_id)[:8] }                        # operators/hardware.md; ledger/seed.py
Tiebreak     = Bet{ bet_type: tiebreak, event: chip agrees with simulator within tolerance, sim_prediction committed first,
                 qpu_s ≤ 60 }                                                     # the chip referees; it never computes
```

## The loop (one program, one cycle)

```
loop(program):
    # 1. SCOUT — all fields, full reads, filtered by cost and falsifiability
    reads = scout(program.question, fields = ALL, depth = full)    # every search written down: terms, where, date
    for r in reads: r.next_steps_it_suggests = extract(r)          # the filter is the point
    candidates = reads.next_steps ∪ program.map ∪ human.added_questions
    reads += scout(mechanism_of(c.cheapest_test) for c in candidates)   # rule 13: search around the test, not only the question's words
    for r in reads: r.predicts_for_us = outcome_predicted(r, candidates)  # the outcome for each draft pass rule, not the topic

    # 2. MAP — rank, with odds stated before any data
    for c in candidates:
        d = Direction(c)
        d.cheapest_test, d.cost = cheapest_falsifier(d)           # cents before dollars; archives before API; API before hardware
        d.prior_work_line = literature.predicts(d.cheapest_test, reads) or "no prior statement found after <search>"   # rule 13, with citations; what this bet adds
        prior.md = run(ledger/prior.py)                            # the engine's own record, counted (rule 14)
        d.odds_prior, d.odds_adjustment, d.odds_reason = fresh_context(prior.md, d.description).P(pass)
                                                                  # fresh context: prior.md + this direction only; nothing of its history
        d.engine_odds = clamp(d.odds_prior + d.odds_adjustment, 0.01, 0.99)   # written down, all three parts
        d.human_odds  = first_line(ledger/human-odds.jsonl, d) or "no human odds"   # cockpit downloads only; never asked in a terminal
        d.weight      = f(surprise_potential, cost, odds, neighbourhood_heat)
    program.map = rank(candidates by weight)

    # 3. PRE-REGISTER — one commit, before the first call or the first archive read
    bet = top(program.map)
    # 3a. LEARN (mandatory) — read the ledger's misses and the audits' cuts first
    read(ledger/bets.jsonl, ledger/brier.md, ledger/audits/, ledger/lessons.jsonl)
    bet.lesson = one_sentence(pattern corrected, design change, odds before → after)            # in §0, committed with the prereg
    bet.lesson.odds_after = fresh_context(prior.md, bet.final_design).P(pass)                       # prior, adjustment, reason; never this session's own number
    bet.engine_odds = bet.lesson.odds_after                                                        # a revision before data; both kept
    bet.premortem = one_sentence("If this fails, the most likely reason is")   # written before the run, never revised
    bet.prior_work = update(bet.direction.prior_work_line) + what_this_bet_adds   # rule 13: §0 row; papers since the map was written
    bet.prereg_commit = commit(pass_rule, statistic, split, seed_rule = first pulse after this commit (CURBY-Q if live, else CURBy-RNG), budget, stop_rules, premortem, prior_work)
    bet.seed = commit(seed(fetch(beacon, first_round_after(bet.prereg_commit)), bet.id))   # before any data; nobody chose it
    # 3b. DESIGN REVIEW (mandatory) — a fresh auditor dry-runs the design before the first call
    review = design_review(bet, by = fresh_session, dry_run = True, paid_calls = 0, pilot ≤ $0.10 if execution risk)   # D1–D11 the design
    review.D12 = opens(bet.prior_work.papers) and (predicted_outcome_in_print(bet) implies bet.says_what_it_adds)   # rule 13; one search of the reviewer's own
    if review.verdict == redesign: withdraw(bet); re-bet with a new lesson                        # counted, not scored
    if review.verdict == fix-first: fix under DEVIATIONS rows dated before data; reviewer confirms
    assert check_prereg(bet) passes                                                                # ledger/check_prereg.py

    # 4. RUN — budget in code; stop-on-refusal; one scale direction; caches so a crash never pays twice
    bet.result = run(bet)
    write_results(plain_english_first, then_tables)
    # 4a. NOVELTY (rule 13) — a fresh session that did not run the bet searches the literature around the result
    if class_of(bet.result) in {landed, mixed}:
        bet.novelty, bet.novelty_line = fresh_session.search_then_verdict(bet.result) ∈ {known, partly_new, new}   # operators/prereg-template.md §10
        append(results_file.plain_english, "Novelty: " + bet.novelty_line); ledger.row(bet).novelty = bet.novelty
        assert "finding" not in results_file unless bet.novelty != known or the prior paper is named in the same sentence
    # the write-up is not final, and not audited, until the Novelty line is in

    # 5. AUDIT — an independent session that has not seen the work tries to break it
    clone = audit_clone(bet.results_commit)                         # history only, no remote, fresh hash every time
    plant = Plant(draw = secret(1/2)); if plant.planted: insert_one_bad_claim(clone.results_file)
    commit(seal(plant))                                              # sealed line for every audit, before the auditor starts
    bet.audit = audit(clone, by = fresh_session, stance = adversarial)
    reveal(plant); score(caught = audit names the planted claim)      # catch rate is published; other findings are the real audit
    if bet.audit.overclaims_cut: rewrite_results(bet, cuts)          # same commit series, never silently
    bet.verdict = decide(bet.result, bet.audit)
    bet.premortem_score = auditor.score(bet.premortem, against = auditor.failure_reason)   # reason written first, then compared
    bet.lesson.recurred = pattern_in(bet.audit, bet.lesson.patterns); review.missed = flaws D1–D12 should have caught
    bet.audit.F27 = opens(bet.novelty_line.papers) and own_search(bet.result.mechanism) finds no prior statement the line missed   # rule 13

    # 6. LEDGER — score both sides
    ledger.record(bet.engine_odds, bet.human_odds, bet.verdict)
    publish(brier(engine), brier(human))                                                   # one scored bet per run (rule 15); every row in a sensitivity row
    if bet.reads_same_run_as(earlier_scored): bet.secondary_of = earlier_scored    # same result file, same raw data, or an audit says so
    publish(brier(bets.odds_prior) vs brier(bets.engine_odds), on bets carrying both)          # the adjustment's value, a number
    rewrite(ledger/prior.md)                                                                   # the next bet starts from this outcome

    # 7. RE-WEIGHT — surprise raises the neighbourhood; a null closes with a diagnosis
    if bet.verdict in {pass} and bet.audit.verdict_stands:
        for d in neighbours(bet.direction): d.weight *= HEAT; scout_more(d)
        queue(replicate(bet, models = [more], designs = [more]))     # a hit is not a hit until it holds elsewhere
    else:
        program.kills.append(Kill(bet.direction, diagnosis(bet)))    # stays on the map, marked closed
        program.map.remove(bet.direction)

    # 7a. REMAP — once the round's results settle, a fresh session turns every result into map entries (operators/remap.md)
    if settled(program.round):                                       # every bet of the round has a verdict and a finished audit
        for b in program.round.bets:
            if class_of(b.verdict) in {landed, mixed}:               # by the ledger's verdict, never by the remap's reading
                rescout = read_literature_around(b.result)            # Step 1b, mandatory: full reads, searches recorded; written before any follow-up
                if b.novelty is None: b.novelty, b.novelty_line = rescout.verdict  # rule 13: results before 2026-11-05 get theirs here
                for f in two_cheapest_not_yet_run(b, sources = [b.audit.break_it_next, rescout.rivals_and_prior_statements, replicate(b, models = RULE_12), neighbours(b)]):
                    f.prior_work_line = rescout.predicts(f.odds_event) or "no prior statement found after <search>"   # rule 13
                    f.engine_odds = engine.P(pass | f)                # one pass, id order, before ranking; never revised after
                    f.human_prompt = "Would you spend about <cost> to find out <what>? Will it come back a hit?"
                    program.map.add(f, parent = b.direction)          # map/<program>.json → the cockpit
            elif class_of(b.verdict) == killed:
                b.direction.rules_out = one_sentence(b)               # "Rules out …", scoped to what was tested
        assert no_landed_leaf(program.map)                           # ledger/check_remap.py: no map ends at a landed bet

    # 8. STEER — the human's hand
    for s in human.steers_since_last_cycle: log(Steer s)             # every veto, question, budget call, override
        if s.action == veto and s.target is a research direction:     # a veto is a bet that the direction would not pay
            schedule(Shadow(s), not_before = +7 days, not_after = +30 days,
                     cheapest = archive_proxy, else cheapest_version(cap = min($2, 10% of vetoed budget)), never QPU)
    for sh in due(shadows): sh.outcome = run(prereg(sh)); score(sh)   # saved money, or killed a hit; never revives the direction by itself
    if human.says_switch_question: program = fork_or_switch(program)

    # 9. CONTEXT — nothing lives only in a chat
    rewrite(CONTEXT.md, from = {ledger, map, kills, steers, results})   # a landed result is listed with its novelty word; "established" never means "first"
    site.map.show(node.novelty for landed or mixed nodes)               # known | partly new | new, in the tooltip, the list and the legend
```

## The engine itself is an experiment

```
path_dependence_test:
    run loop(seed_A) and loop(seed_B) in parallel, same engine, same rules
    measure: do the maps converge, diverge, or cross?  which kills recur?  does the ledger differ?
    this is the order-effect question asked of research itself

referee_test:
    compare calibration(engine | referee = model, programs 1–2) vs calibration(engine | referee = nature, program 3)
    an engine calibrated only when an AI grades it has borrowed its judgment from its grader

learning_test:
    Brier(odds before the lesson) vs Brier(odds after it), paired over scored bets with lessons
    recurrence of each pattern after it is cited; design reviews: flaws found, and flaws missed per later audit
    if the after-lesson odds are no better, the engine is not learning from its own record
    Brier(prior alone) vs Brier(prior + adjustment), paired, on bets whose odds were written in three parts (rule 14)
    if the adjusted odds are no better, the engine's reasoning about a bet adds nothing to its own hit rate

auditor_test:
    catch rate = plants caught / plants planted, Wilson interval, by class; vs 82% (Luo et al. 2025, logs + code)
    the auditor never knows which audit carries a plant; its "stands" is only worth its catch rate

oversight_test:
    compare ledger(engine) vs ledger(human) vs ledger(engine + human)
    report where the human changed the outcome, and whether for the better
    vetoes included: each shadow says whether the veto saved money or killed a hit (ledger/scores.md)
    the honest answer either way is the result
```

## Invariants (never violated)

1. Odds before data, both sides, in writing.
2. Cheapest falsifier first; budget in code; stop rules; stop-on-refusal.
3. No result without an independent audit; the audit is published; the auditor is itself audited by sealed plants.
4. Nothing disappears: kills stay on the map with diagnoses.
5. Every program begins with full reads across all fields.
6. A pre-registered bar is never lowered after data.
7. A hit is not a hit until replicated on more than one model and design.
8. Plain English first in every artifact.
9. Quantum hardware is a referee (simulator-vs-chip tiebreaks, scored as bets) and a seed source (CURBy), never a computational resource.
10. No pre-registration without a lesson from the ledger and a fresh design review that says go before the first call.
11. No session asks the human for odds or decisions in a terminal. Human odds come only from `ledger/human-odds.jsonl` (cockpit downloads); without them a bet proceeds marked "no human odds". The human's judgment is recorded and scored as steers.
12. No map ends at a landed bet with no follow-up: every landed or mixed bet has at least one not-yet-run follow-up on the map (operators/remap.md; `ledger/check_remap.py`).
13. The engine knows what it is testing against: no direction without a Prior work line (what published work predicts for this exact test, with citations, or a described search that found none), no pre-registration whose design review skipped D12, and no landed or mixed result called final before a fresh session that searched the literature has written its Novelty line (known, partly new or new), which the audit checks (F27) and the map and the site show. A known result is reported as a replication of the paper that found it (CONTEXT.md §3 rule 13; `paper/informed-engine.md`).
14. Odds start from the record: every odds elicitation is a fresh context holding `ledger/prior.md` and the bet's own description, nothing of its history, and writes prior, adjustment and a one-line reason; the ledger keeps all three and `ledger/brier.md` scores the prior alone against the adjusted odds (CONTEXT.md §3 rule 14).
15. One scored bet per run: a bet that re-scores a run an earlier scored bet was scored on (same program and result file, or the same raw data with nothing new, or an audit says so) carries `secondary_of`; the primary Brier counts each run once and `ledger/brier.md` shows every row in a Sensitivity row beside it (CONTEXT.md §3 rule 15).

## Repositories

```
oversight-testbed/           # the engine (placeholder slug until the title is chosen; see CONTEXT.md §0)
  README.md                  # the five commitments, the ledger, the map, links to programs
  CONTEXT.md                 # the living brain; rewritten nightly; read first by every session
  TASKS.md                   # open items, decisions made, what waits on whom; read second
  ARCHITECTURE.md            # this file
  proposal.md                # the research proposal for the engine itself
  ledger/                    # bets.jsonl (engine odds, human odds, verdicts), steers.jsonl, shadows.jsonl, plants.jsonl (sealed), lessons.jsonl (patterns + lessons), audits/, design-reviews/;
                             # brier.py → brier.md (calibration), scores.py → scores.md (vetoes, catch rate, pre-mortems, tiebreaks), prior.py → prior.md (the record as the prior; closing reviews due),
                             # plants.py (seal/reveal/verify), seed.py (beacon → seed), check_prereg.py (lesson + review gate)
  map/                       # per-program maps as markdown + json
  operators/                 # morning brief, nightly updater, auditor, plant, scout, veto, premortem, hardware, learn, design-review, pre-registration template
  site/                      # GitHub Pages: papers as pages, record as timeline, calibration chart, map view
  programs/                  # every program lives here, history imported by git subtree add: one repository, no others
    entangled-mind/          # program 1: quantum encoding (closed) → self-reports (open); GitPhar/entangled-mind kept as its historical record
    other-minds/             # program 2: theory of mind as third-person self-report
    nature-graded/           # program 3: the engine's odds graded by nature (ibm_fez as referee)
    settled-science/         # program 4: the engine's odds graded by the published record
```

Paths inside a bet (`result_file`, `test`) are relative to `programs/<name>/`. Commits from before the fold keep their hashes and show files at their pre-fold paths.

## Operators

```
morning  (07:03 America/Denver, cloud):  read CONTEXT.md → read both repos' last 24h → run ledger/prior.py, ledger/check_remap.py, the prior-work and novelty checks → report programs due a closing review → brief + today's wave (one paste per tab)
nightly  (23:33 America/Denver, cloud):  read day's commits → rewrite CONTEXT.md §state, §map, §steers → push
planter  (per audit, before it):         not the auditor; builds the audit clone, draws plant/clean in secret, plants one bad claim, seals it (operators/plant.md)
auditor  (per result, local tab):        fresh session in the audit clone, has not seen the work, instructed to break it, writes ledger/audits/<bet>.md
scout    (per program start, local tab): full reads, all fields, next-steps extracted, candidates ranked with odds; the human's question on each cockpit card
learn    (per prereg, before it):        the betting session reads bets, brier, audits, lessons; writes one lesson line (operators/learn.md)
review   (per prereg, before 1st call):  fresh auditor dry-runs the design, D1–D12 (D12: the predicted outcome in print?), no paid calls; go | fix-first | redesign (operators/design-review.md)
novelty  (per landed or mixed result, before the write-up is final): fresh session searches the literature around the result; writes the Novelty line (known | partly new | new) into the results file and the ledger row (operators/prereg-template.md §10); the remap's re-scout does it for results that predate rule 13
shadow   (per veto, 7–30 days later):    fresh session, argued neither side; pre-registers and runs the cheapest look at a vetoed direction (operators/veto.md)
remap    (per settled round, local tab): fresh session reads every settled result; two cheapest follow-ups per landed or mixed bet, a "rules out" sentence per kill (operators/remap.md)
closing  (per program due, local tab):   fresh session; when ledger/prior.md lists a program whose last three layers hold no landed bet and no partly-new finding: diagnosis, then closed or kept open with a stated reason (operators/remap.md)
session  (any build tab):                reads CONTEXT.md first; obeys the invariants; commits with the deviation row it adds
```

## Staleness guard

```
if age(CONTEXT.md) > 36h: the morning operator says so and makes tab 1 of the wave a rewrite from the repos' current state
if any results file disagrees with CONTEXT.md: the results file wins; CONTEXT.md is corrected and the correction is logged
```
