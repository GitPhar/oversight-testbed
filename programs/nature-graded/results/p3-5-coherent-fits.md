# P3-5 result: on two of three archived qubit pairs, a blurring model fits better than a steering model with the same number of knobs; both kinds of error are present on every pair

> Audited 2026-11-04 (round 2, entangled-mind audit2 8091d01, audits/ng-p3-5.md): verdict stands (fail, "incoherent better" as the §5.2 count; the reading "blur, not steering" does not stand); 11 required cuts applied in D5.

Pre-registration: `experiments/p3-5-coherent-fits.md` (commit `ff2c7e7`, 15:39; seed commit `1593b09`, CURBy-RNG pulse 1591384 at 15:40). Run 2026-11-04 on the laptop: $0, 0 QPU s. **Verdict: fail, "incoherent better"** (audited in round 2; see above): a 2–1 split; the third pair favours steering by 63, and no uncertainty was pre-registered. Engine odds were 0.42. Human odds were not recorded.

## In plain English

We went back to program 1's detailed entanglement measurements: three pairs of qubits, nine ways of looking at each pair, 4,000 shots per look. We asked which kind of error explains them better. *Steering* errors rotate the qubits' state a little, the same way each time. *Blurring* errors scramble it randomly. Each explanation got seven adjustable knobs, and each started from the P3-1 simulator's state (which, it turns out, kept FakeFez's T1/T2 rather than the job's). The knobs are not equally capable: steering cannot make a state more mixed, and the chip's states are more mixed than the simulator's on all three pairs, so blurring starts with an advantage.

**On two of the three pairs, blurring fits clearly better.** The margins are 44 and 35 on a scale where 10 counts as clear; bootstrap 95% intervals are [−65, −19] and [−76, +4], and the second rests mostly on one of nine settings (XX). On the third pair, steering fits better, by 63. The bet needed steering to win on at least two, so it fails. Read plainly: on these three pairs, the chip's states were more mixed than the simulator predicts, and only the blurring model can produce that. When both kinds are allowed together, steering terms still improve the fit clearly on every pair (by 22, 89 and 116). One pair went the other way, and neither explanation fits the data perfectly.

Two details matter for what comes next.
- Where blurring wins, it lowers the predicted entanglement: to 0.139 against the chip's 0.147 on h221, and to 0.035 against the chip's 0.063 on h088 (an overshoot). On the one pair where steering wins on fit, the fitted steering errors leave the entanglement almost untouched (0.111, against the chip's 0.067). So steering explains some pattern in that pair's counts, but not the entanglement loss.
- These data were taken with no error scrambling (twirling) and no decoupling. That is the condition the bet asked about. P3-2 now asks the device directly.

## Tables

**Primary** (reference: the P3-1-corrected simulator's reduced state (T1/T2 not overwritten from the snapshot: FakeFez values; with them overwritten, ΔlogL −41.8, −29.3, +86.0); readout through each item's archived hardware assignment matrix; best of 21 starts per fit, seed32 2090756689):

| item (physical qubits) | logL ρ_ref | logL coherent (i) | logL incoherent (ii) | saturated | **ΔlogL (i − ii)** | ≥ 10? |
|---|---|---|---|---|---|---|
| h221 (10, 9) | −39,279.8 | −39,239.6 | −39,196.1 | −39,167.7 | **−43.5** | no |
| h088 (44, 37) | −46,530.1 | −46,427.3 | −46,392.4 | −46,271.7 | **−34.9** | no |
| h268 (4, 16) | −43,492.3 | −43,319.4 | −43,382.4 | −43,258.7 | **+63.0** | yes |

- Items with ΔlogL ≥ 10: **1 of 3**, so the bet **fails**.
- Items with ΔlogL ≤ −10: 2 of 3, so the pre-registered label is **"incoherent better"**.
- All six best fits report optimiser success. With 251 starts, the coherent fits improve by 0.9 (h221) and 4.1 (h268), giving ΔlogL −42.7, −34.9, +67.1; the verdict is unchanged. Neither family reaches the saturated likelihood: the best family is 28, 121 and 61 below it.

**Negativity** of the fitted states (secondary; hardware values are the archived readout-mitigated ones):

| item | ρ_ref (corrected sim) | coherent fit | incoherent fit | hardware (archived) | program 1 noisy sim (archived) |
|---|---|---|---|---|---|
| h221 | 0.179 | 0.176 | 0.139 | 0.147 | 0.171 |
| h088 | 0.112 | 0.122 | 0.035 | 0.063 | 0.149 |
| h268 | 0.103 | 0.111 | 0.039 | 0.067 | 0.118 |

**Fitted parameters** (secondary): ZZ phase φ = −0.009, −0.086 and +0.049 rad. Global depolarising p = 0.011, 0.011 and 0.000. The incoherent fits put their weight on local Pauli errors of 5–10% (largest per qubit): on qubit 9 for h221 (p_X 0.053); on qubits 44 (p_Z 0.073) and 37 (p_X 0.096) for h088; on qubit 16 (p_X 0.103) for h268.

**Secondary: ideal (noiseless) state as reference.** ΔlogL = −73.8, −438.7 and −191.6, so incoherent wins all three. That is expected: starting from a state with no decay at all, only the blurring family can supply decay. The reference choice matters for h268, whose sign flips.

**Not pre-registered, noticed in the table.** The corrected simulator's own negativity for h088 and h268 (0.112, 0.103) sits below program 1's noisy-sim values (0.149, 0.118). Unlike the Stage 1 circuit, these circuits may idle long enough for scheduling to matter. That was not tested here and should not be read as a result.

**Pre-mortem** ("the lost negativity comes mostly from depolarising-type decay, which the incoherent family's global depolarising term captures …"; kind `world`).

Data: `results/p3-5-coherent-fits.json`. Code: `experiments/p3_5_fits.py`.
