# em-gm2bf1 dry run (design review F1, D71)

Built by the design reviewer (`ledger/design-reviews/em-gm2bf1.md`, `1d52379`) and committed here unchanged, except that `world.py` now loads `marg.npz` from this folder rather than from the reviewer's scratch path.

- `marg.npz` holds, per claim, the order archive's within-order SD W and level, the **real** six format means (so the real format spread G can be recovered from it), E = |F1 mean − 50| and F1's SD. The first version of this README called these "measured marginals only"; the em-gm2bf1 audit corrected that (D75). The file does not hold the order span S. The dry-run worlds synthesise S and G and never pair the real S with the real G, but nothing in the record shows that the reviewer, who had also computed the per-claim spans, did not pair them before the run.
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

**Audit note (D75).** In all 750 draws the auditor re-simulated from these worlds, the D71 guard came out below the frozen guard. On the real data it came out 0.161 above, and these worlds understate how closely the order span follows rating noise (ρ 0.37–0.58 against the real 0.77). The table's false-pass rates are therefore not measured rates for these data.
