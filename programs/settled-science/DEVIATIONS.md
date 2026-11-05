# Deviations

Every departure from the engine's standing procedure or from this program's pre-registration, dated, written before the result it affects.

| row | date (America/Denver) | what | why |
|---|---|---|---|
| D1 | 2026-11-04 17:12 | Engine odds for ss-b1 to ss-b3 were written by the item-writer session in one pass, not in the v1 fresh-context template of `operators/scout.md`. | This program has one engine session, the item-writer. They were written before that session had read any drafted item. |
| D2 | 2026-11-04 17:12 | No human odds on ss-b1 to ss-b3. | Sean's part is the 20-item direction-level form, scored item by item against the same record. |
| D3 | 2026-11-04 17:45 | Budget cap lowered from $6.00 (protocol/fixed-rules.md) to $5.00, before any API call. | The engine's TASKS.md records program 4 with a $5 cap. Tightening only. |
| D4 | 2026-11-04 17:45 | The program moved from its own folder into the engine repo at `programs/settled-science/` (subtree, history kept). | Sean's decision recorded in the engine's TASKS.md: no separate program repositories. Overrides the brief's "push as GitPhar/settled-science". |
| D5 | 2026-11-04 18:40 | The leakage check's 213 calls ($0.47) ran before ss-b1's pre-registration. | Rule 3 requires the check before items are used; it is item construction, not the test. Its exclusion rule was committed first (`d3996c9`, protocol/leakage-check.md), and its full outputs were committed (`4859d3b`) before this pre-registration was written. Agreed with the engine session. |
| D6 | 2026-11-04 18:20 | Thinking is turned off with `{"type": "between_tools"}` instead of `{"type": "disabled"}` for models that reject the latter (the API's 400 message says so); the requests carry no tools, so no thinking happens. Each call records the setting used. | The API changed for claude-sonnet-5-5; recorded before any bettor call. |
| D7 | 2026-11-04 18:00 | Five antonym pairs were added to verify.py's option-parallelism list (easier/harder, an earlier/a later, rose/declined, high/low, deeper/shallower) after the first verification pass, before any leakage call. | Genuine direction swaps missing from the list. The list only governs a mechanical format check, and no answer was consulted. |
| D8 | 2026-11-04 18:05 | Four drafted items were excluded and one paper moved to pre-cutoff by the item-writer before any leakage call (`items/writer-exclusions.json`, each with its reason). | The writers' own flags (a hedged finding; quotes that settle only with context) and an ICML-workshop comment (Rule 2). |
