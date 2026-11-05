import sys, json, time
import numpy as np
sys.path.insert(0, ".")
import world as w
m = w.m
if __name__ != "__main__": NREP = 0; NB = 0; which = ["none"]
else: NREP = int(sys.argv[1]); NB = int(sys.argv[2]); which = sys.argv[3:]
worlds = {
 "W0 extremity only (logit mid-scale + tie saturation)": dict(kap=0.0),
 "W0b extremity only, plus mid-scale format deviations": dict(kap=0.0, fx=0.5),
 "W0c extremity only, plus mid-scale on both sides": dict(kap=0.0, fx=0.5, ox=0.5),
 "W1 shared kap=0.25": dict(kap=0.25),
 "W1 shared kap=0.5": dict(kap=0.5),
 "W1 shared kap=0.75": dict(kap=0.75),
 "W1 shared kap=1.0": dict(kap=1.0),
}
def draw2(rng, kap=0.0, fx=0.0, ox=0.0):
    # fx/ox: extra dependence of the format-deviation SD / order SD on the common latent's extremity |T|
    a = 0.5
    u = rng.normal(0, 1, w.N); v1, v2 = rng.normal(0, 1, w.N), rng.normal(0, 1, w.N)
    ext = np.abs(w.T); ext = (ext - ext.mean()) / ext.std()
    sig = a * np.exp(1.3 * v1 + kap * u - ox * ext)
    means = w.expit(w.xo[:, None] + sig[:, None] * rng.normal(0, 1, (w.N, 4))) * 100
    means = np.clip(means + rng.normal(0, 1, (w.N, 4)) * (w.WR / np.sqrt(10))[:, None], 0, 100)
    S = means.max(1) - means.min(1)
    sd = 1.4 * np.exp(0.5 * v2 + kap * u - fx * ext)
    t = w.T[:, None] + sd[:, None] * rng.normal(0, 1, (w.N, 5))
    F = np.zeros((w.N, 6)); F[:, 0] = w.FM[:, 0]
    F[:, 1] = rng.binomial(10, w.expit(2.6 + 2.5 * t[:, 0])) / 10
    F[:, 2] = rng.binomial(10, w.expit(-2.2 + 1.6 * t[:, 1])) / 10
    F[:, 3] = rng.binomial(10, w.expit(2.4 + 1.0 * t[:, 2])) / 10
    F[:, 4] = np.clip(np.round(w.expit(t[:, 3, None] - 0.3 + 0.8 * rng.normal(0, 1, (w.N, 10))) * 110 - 6), 0, 100).mean(1)
    F[:, 5] = ((t[:, 4, None] + 0.35 * rng.logistic(0, 1, (w.N, 10)))[..., None] > w.CUT6).sum(-1).mean(1)
    G, _ = m.format_measures(F, F[:, 0])
    return S, G
out = {}
for name, kw in worlds.items():
    if which and not any(name.startswith(x) for x in which): continue
    t0 = time.time(); rng = np.random.default_rng(abs(hash(name)) % 2**32)
    v, rho, prho, plo, rlo = [], [], [], [], []
    for _ in range(NREP):
        S, G = draw2(rng, **kw)
        r = m.analyse(S, G, w.E, w.WR, w.ITEMS, int(rng.integers(2**62)), nboot=NB)
        v.append(r["verdict"]); rho.append(r["rho"]); prho.append(r["partial_rho"]); plo.append(r["partial_rho_ci"][0]); rlo.append(r["rho_ci"][0])
    v = np.array(v)
    res = dict(P_pass=float((v == "pass").mean()), med_rho=float(np.median(rho)), med_partial=float(np.median(prho)),
               P_rho_ge_030=float((np.array(rho) >= 0.3).mean()), P_partial_lo_gt0=float((np.array(plo) > 0).mean()), med_partial_lo=float(np.median(plo)))
    out[name] = res
    print(f"{name}: P(pass) {res['P_pass']:.3f}  median rho {res['med_rho']:+.2f}  P(rho>=.30) {res['P_rho_ge_030']:.2f}  median partial {res['med_partial']:+.2f}  P(partial lo>0) {res['P_partial_lo_gt0']:.2f}  [{NREP} reps, {time.time()-t0:.0f}s]", flush=True)
json.dump(out, open(f"sim-{NREP}-{NB}-{'_'.join(which) or 'all'}.json", "w"), indent=1)
