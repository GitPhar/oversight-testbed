# (working title — see CONTEXT.md §0)

A scalable-oversight testbed for AI-driven research. The AI maps every candidate path and bets on them with stated odds; a human steers; an independent auditor tries to break every result; both the AI and the human are scored on their judgment. Built for trust, not volume.

Read in this order: `CONTEXT.md` (the living brain, rewritten nightly), `ARCHITECTURE.md` (the loop in pseudocode), `proposal.md` (the research proposal for the engine itself).

## The five commitments

1. **Odds before data.** Every bet carries the engine's odds and the human's odds, recorded separately, before any data are seen.
2. **Cheapest falsifier first.** Archives before API, API before hardware; budgets in code; stop rules; stop-on-refusal.
3. **No result without audit.** An independent session that has not seen the work tries to break every result, and its report is published whether or not the result stands.
4. **Nothing disappears.** Every dead direction stays on the map with its diagnosis.
5. **Full reads first, all fields.** Every program starts from adjacent research read in full, its "what to do next" extracted and filtered by cost and falsifiability.

## Programs

- Program 1 — [The Entangled Mind](https://github.com/GitPhar/entangled-mind): a quantum encoding of a model's competing beliefs (closed, negative, with diagnosis) that produced a live finding about what a model's self-reports measure.
- Program 2 — Other Minds (open): does a model's account of another mind behave like its account of its own? First bet om-p2-1 pre-registered.
- Program 3 — Nature-Graded (open): the same engine's odds, graded by a quantum chip instead of a language model. The chip is a referee, never a computational resource (`operators/hardware.md`).

## Ledger, audits, map, site

`ledger/bets.jsonl`, `ledger/steers.jsonl`, `ledger/audits/`, `map/`, `site/` — populated by the operators described in `CONTEXT.md` §7.
