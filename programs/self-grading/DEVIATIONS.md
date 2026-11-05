# DEVIATIONS — program 5 (self-grading)

Every departure from a pre-registration, dated (America/Denver), written before the result it affects. Rows are never deleted.

| row | date | bet | what changed | why | written before data? |
|---|---|---|---|---|---|
| D0 | 2026-11-05 | — | The program session crashed at 2026-11-04 23:44 while starting; it was resumed from the two files it left (starting point 753e334). | Mac crash. No API call had been made. | yes |
| D1 | 2026-11-05 | sg-b1 | Pre-registration of sg-b1 (experiments/sg-b1-placement.md), with its code (sg_b1_placement.py, sg_prompts.py) and the pilot set enlarged from 2 to 6 studies (sg_items.py) so a design-review pilot can measure grading noise. A fresh-versus-fresh re-grade arm (fresh2) is added beyond the map row, as the dumb-baseline gate; the cap rises from the map's $1.10 to $1.35 for it. | Pattern P3 (dumb baseline) and P12 (noise known before the bar). | yes |
| D2 | 2026-11-05 | all | sg_common.program_spent() now sums results/*-calls*.json, not *-calls.json, so pilot caches (*-calls-pilot.json) count toward the $5.00 program cap. | Found by the author before any call; the old glob would have let pilot spend escape the program cap. Tightens a budget; no bar changes. | yes |
| D3 | 2026-11-05 | sg-b1 | sg_b1_placement.per_model(): the usable share is now out of the 60 test studies (6 pilot), as §5.1 says, not out of the studies that received any grade. | Found by the author before any call: a run cut short by the cap would otherwise have looked complete. Code brought into line with the frozen text; no bar changes. | yes |
| D4 | 2026-11-05 | sg-b1 | The design-review pilot is capped in code at $0.035 (write) + $0.055 (grade) and uses p01-p03 only. The draft used a fifth of the run caps ($0.27), above the $0.10 a pilot may spend. | operators/design-review.md D6 limit. Pilot data are never test data. | yes |
