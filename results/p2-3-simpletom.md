# P2-3. SimpleToM decomposed: results (stopped on a refusal)

Pre-registered in `experiments/p2-3-simpletom.md` (D4), commit `6f17538`. Seed commit `46378b0` (CURBy-RNG pulse 1591352). Both came before any call. `claude-haiku-5-5`. **Stopped on a refusal after 26 calls, $0.001 of the $1.75 cap.** Engine odds 70; Sean's odds not recorded before data. Not yet audited.

> Audited 2026-11-04 (round 2, entangled-mind audit2 8091d01, audits/om-p2-3.md): verdict stands as untestable; 2 required cuts applied in D5.

## In plain English

**What happened.** The run's first step asks the model, for each of SimpleToM's 1,147 stories, whether the character is aware of the hidden fact. Calls ran eight at a time; 26 had completed and been cached when the call for story `gen8_sev3` was refused by the API (category `general_harms`, "restrictions on content related to the development of high-yield explosives"). The story reads: "The box of gourmet chocolates is filled with plastic explosives set to detonate when opened. Emma selects the elegantly wrapped box from the shelf and proceeds to the checkout counter." The question was whether Emma is likely to be aware of that.

**What the rules did.** Stop-on-refusal held. No new call started after the refusal reached the runner. Five calls already in flight (stories 22–26 in run order) completed and are kept. Nothing was reworded, retried, skipped or replaced. The 26 answers already cached are kept. The refusal and its request ID are in `results/refusal-p2-3.md`.

**Pre-registered verdict: untestable.** No story reached the planted-answer conditions, against the 300 the rule requires. The test says nothing either way about whether the "stated but not used" gap is a memory effect.

**The pre-mortem named this.** It read: "If this fails, the most likely reason is a refusal on one of the 552 severity-3 stories (bombs, poison, contaminated food), which stops the run before the planted conditions are complete for 300 stories" (kind: `execution`). The refused story is severity 3 and contains explosives. The auditor scores the pre-mortem; this note only records that the named mechanism occurred.

**What it would take to answer the question.** These are for Sean to decide. None has been done.
- A new, separately pre-registered bet on a subset with lower refusal risk, for example severity 1 and 2 only (595 stories). It would be a different item set, so a new bet, not a retry. Severity-2 stories can still be harmful, so the risk is lower, not zero.
- The support route already pending for program 1's two refusals, asking whether this evaluation use can be exempted.
- Leaving P2-3 untestable on this item set and moving on. P2-4 (separately pre-registered and audited) bears on a related question.

## Tables

| step | planned calls | made | status |
|---|---|---|---|
| 1. own awareness answer | 1,147 | 26 | stopped at `ms\|gen8_sev3` (refused) |
| 2. behaviour × 6 conditions | 6,882 | 0 | not run |
| 3. judgment × 6 conditions | 6,882 | 0 | not run |

- Refused request: `req_011Cgih9NjqNtezArQLWd12p`, category `general_harms`, model `claude-haiku-5-5`, 2026-11-04 (America/Denver).
- Stories with both planted conditions answered: 0 of 1,147 (rule: 300). **Verdict: untestable.**
- Archive: `results/p2-3-calls.json` (26 calls), `results/refusal-p2-3.md`.
