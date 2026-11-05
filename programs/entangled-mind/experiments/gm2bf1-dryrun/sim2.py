# As sim.py, plus: an independence world (G permuted) to check the guard's false-positive rate, and an
# alternative guard (covariates E, Eo=|order level-50|, W, and squared ranks of each) read under the same bootstrap.
import sys, json, time
import numpy as np
from scipy.stats import rankdata
sys.path.insert(0, ".")
import world as w
from sim import draw2
m = w.m
EO = np.abs(w.LEV - 50)
def pcorr(a, b, covs):
    cols = [np.ones(len(a))]
    for c in covs:
        rc = rankdata(c); rc = (rc - rc.mean()) / rc.std(); cols += [rc, rc**2]
    Z = np.column_stack(cols); ra, rb = rankdata(a), rankdata(b)
    ea = ra - Z @ np.linalg.lstsq(Z, ra, rcond=None)[0]; eb = rb - Z @ np.linalg.lstsq(Z, rb, rcond=None)[0]
    return float(np.corrcoef(ea, eb)[0, 1])
by_item = [np.arange(4*i, 4*i+4) for i in range(40)]
def alt(S, G, rng, nb):
    p = pcorr(S, G, [w.E, EO, w.WR]); B = []
    for _ in range(nb):
        idx = np.concatenate([by_item[j] for j in rng.integers(0, 40, 40)])
        B.append(pcorr(S[idx], G[idx], [w.E[idx], EO[idx], w.WR[idx]]))
    return p, float(np.percentile(B, 2.5))
NREP, NB = int(sys.argv[1]), int(sys.argv[2]); ONLY = int(sys.argv[3]) if len(sys.argv) > 3 else None
worlds = {
 "I independent (G permuted)": dict(kap=0.0, perm=True),
 "W0 extremity only": dict(kap=0.0),
 "W0b extremity only + mid-scale format deviations (fx .5)": dict(kap=0.0, fx=0.5),
 "W0c extremity only + mid-scale both sides (fx .5, ox .5)": dict(kap=0.0, fx=0.5, ox=0.5),
 "W0d extremity only + mid-scale both sides (fx .8, ox .8)": dict(kap=0.0, fx=0.8, ox=0.8),
 "W1 shared kap .25": dict(kap=0.25),
 "W1 shared kap .5": dict(kap=0.5),
 "W1 shared kap .75": dict(kap=0.75),
 "W1 shared kap 1.0": dict(kap=1.0),
 "W1c shared kap .5 + mid-scale both sides (.5)": dict(kap=0.5, fx=0.5, ox=0.5),
}
out = {}
for wi, (name, kw) in enumerate(worlds.items()):
    if ONLY is not None and wi != ONLY: continue
    t0 = time.time(); rng = np.random.default_rng(sum(map(ord, name)))
    perm = kw.pop("perm", False)
    rows = []
    for _ in range(NREP):
        S, G = draw2(rng, **kw)
        if perm: G = G[rng.permutation(w.N)]
        r = m.analyse(S, G, w.E, w.WR, w.ITEMS, int(rng.integers(2**62)), nboot=NB)
        ap, alo = alt(S, G, rng, NB)
        rows.append((r["verdict"] == "pass", r["rho"], r["rho_ci"][0], r["partial_rho"], r["partial_rho_ci"][0], ap, alo,
                     r["rho"] >= 0.3 - 1e-9 and r["rho_ci"][0] > 1e-9 and alo > 1e-9))
    a = np.array(rows, float)
    res = dict(n=NREP, P_pass=a[:, 0].mean(), med_rho=np.median(a[:, 1]), P_rho_ge_030=(a[:, 1] >= 0.3).mean(),
               med_partial=np.median(a[:, 3]), P_partial_lo_gt0=(a[:, 4] > 0).mean(),
               med_alt_partial=np.median(a[:, 5]), P_alt_lo_gt0=(a[:, 6] > 0).mean(), P_pass_alt=a[:, 7].mean())
    out[name] = res
    print(f"{name}: P(pass) {res['P_pass']:.3f} | med rho {res['med_rho']:+.2f} P(rho>=.30) {res['P_rho_ge_030']:.2f} | "
          f"med partial {res['med_partial']:+.2f} P(lo>0) {res['P_partial_lo_gt0']:.3f} | alt guard: med {res['med_alt_partial']:+.2f} "
          f"P(lo>0) {res['P_alt_lo_gt0']:.3f} P(pass) {res['P_pass_alt']:.3f} [{time.time()-t0:.0f}s]", flush=True)
json.dump(out, open(f"sim2-{NREP}-{NB}-{ONLY}.json", "w"), indent=1)
