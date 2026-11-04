# Program 3 reads

There are 81 Read records in five clusters. Each was written by one reader session working from `scout-brief.md`, on 2026-11-04. They used web reads only: no model API calls of their own, no paid services, no hardware.

| file | cluster | records | full | partial | abstract |
|---|---|---|---|---|---|
| `a-local-friendliness.md` | Wigner's friend, local friendliness | 13 | 7 | 3 | 3 |
| `b-contextuality-cbd.md` | sequential contextuality, Contextuality-by-Default | 14 | 8 | 5 | 1 |
| `c-leggett-garg-randomness.md` | Leggett–Garg, NSIT, clumsiness, certified randomness | 17 | 12 | 3 | 2 |
| `d-device-physics.md` | why `from_backend` misses Heron r2; twirling, DD, TLS, crosstalk | 20 | 9 | 8 | 3 |
| `e-other-foundations.md` | real vs complex, ψ-ontology, Born rule, superdeterminism, no-signalling, Darwinism | 17 | 11 | 5 | 1 |
| **total** | | **81** | **47** | **24** | **10** |

Counts are taken from the `read_depth` lines. A few further sources have one-line "does not transfer" notes and are not counted.

## Read-depth debts before any paper cites these

- **Fetched through an extraction tool.** Several "full" reads went through a fetch tool that extracts or summarises, rather than a plain text dump. The files say which ones. Any number from those reads must be checked against the source before it appears in a write-up.
- **Our own arithmetic.** Numbers marked **[our calc]** or **(my calc)** are the readers' own calculations, not the authors' values.
- **Sources not as briefed.** Each file opens with the cases where a named source turned out not to be what the brief said. Examples:
  - Nigg et al. 2016 is a trapped-ion experiment, not superconducting.
  - Knee et al. 2016 does not use ideal negative measurements.
  - McKay et al. 2023's Heron device is ibm_montecarlo.
  - arXiv:2407.08828 is Proctor et al., not Hashim et al.
- **Not obtained.** Etxezarreta Martinez et al. 2021 was behind a login, and Hines et al. 2023 could not be verified. CbD 2.0 (Dzhafarov & Kujala) was read at abstract depth only, yet it is the definition P3-9's analysis depends on. It must be read in full before P3-9 is pre-registered.

## Two readers, one disputed fact, reconciled

The local-friendliness reader and the other-foundations reader both read Bednorz et al. 2025 (arXiv:2506.08940). One summarised its signalling result as "several IBM groups"; the other summarised it as "Eagle, but not Heron r2". The record texts agree once the devices are named:
- signalling appeared on ibm_brisbane and ibm_sherbrooke (Eagle) and on ibm_torino (Heron r1);
- none appeared beyond statistical error on ibm_kingston (Heron r2).

`ibm_fez` is a Heron r2 and has not been screened (direction P3-6).
