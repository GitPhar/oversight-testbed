# em-gm2bf1 dry run (design review F1, D71)

Built by the design reviewer (`ledger/design-reviews/em-gm2bf1.md`, `1d52379`) and committed here unchanged, except that `world.py` now loads `marg.npz` from this folder rather than from the reviewer's scratch path.

- `marg.npz` holds measured marginals only: per claim, the order archive's within-order SD W and level, the six format means, E = |F1 mean − 50| and F1's SD. It never pairs the order span with the format spread.
- `world.py` and `sim.py` build synthetic order spans and format spreads on those marginals. `sim2.py` reads the frozen guard and the D71 guard (E, Eo and W, each as a centred rank plus its square) under the same item bootstrap.
- `sim2-200-1000-<i>.json` holds 200 worlds each, with 1,000 resamples.

| world | P(pass), frozen guard | P(pass), D71 guard |
|---|---|---|
| G permuted (independent) | 0.00 | 0.00 |
| W0 extremity only | 0.01 | 0.01 |
| W0b + mid-scale format deviations | 0.05 | 0.02 |
| W0c + mid-scale both sides (0.5) | 0.21 | 0.06 |
| W0d + mid-scale both sides (0.8) | 0.435 | 0.10 |
| W1 shared κ 0.25 | 0.025 | 0.02 |
| W1 shared κ 0.5 | 0.115 | 0.11 |
| W1 shared κ 0.75 | 0.39 | 0.39 |
| W1 shared κ 1.0 | 0.805 | 0.805 |
| W1c shared κ 0.5 + mid-scale both sides | 0.72 | 0.40 |

With the D71 guard, the extremity-only worlds pass at most 10%, and the shared worlds pass 11–80% from κ 0.5 up (D11).
