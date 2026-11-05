# DEVIATIONS — program 7 (said-vs-did)

Every departure from a pre-registration, dated (America/Denver), written before the data it affects. Every pre-registration also gets a row.

| id | date | what | why | affects |
|---|---|---|---|---|
| D1 | 2026-11-05 | Program started. The scout session that opened it crashed at 23:44 on 2026-11-04 with two files uncommitted: the reads README and reader B's first record. Both were kept (e9f0f31) after reader B's 13 numbers were re-checked against the arXiv text. The five other reader files had not been written; the scout was re-run on 2026-11-05 with six readers on disjoint source lists. | crash recovery | scout only; no data existed |
| D2 | 2026-11-05 | Pre-registration of sv-b1 (SV-1, giving way under "are you sure?"), with the shared code (`svd_common.py`, `svd_stats.py`, `svd_wave1.py`), the committed dry runs (`sv-wave1-worlds.txt`) and a copy of `curby_seed.mjs` from settled-science. Odds 45 → 40 before data (lesson ls-sv-b1). | pre-registration | sv-b1; the said step is shared with sv-b2 and sv-b3 |
| D3 | 2026-11-05 | Seed commit for sv-b1: CURBy-RNG pulse 1592195 (05:11:00; the first after the pre-registration commit 0bf2365 at 05:10:14; pulse 1592194 at 05:10:00 precedes it). Item draw written to `data/sv-wave1-items.json` by `experiments/seed_items.py`; sv-b2 and sv-b3 inherit it, with no new draw. No call made. | beacon seed rule | sv-b1, sv-b2, sv-b3 items |
