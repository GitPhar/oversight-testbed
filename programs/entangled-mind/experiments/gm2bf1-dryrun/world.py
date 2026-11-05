# Semi-synthetic worlds: real order-archive level (lev), real W, real F1 means (so E is real);
# synthetic order means (-> S) and synthetic F2..F6 responses (-> G). Real S and real G are never used.
import sys
from pathlib import Path
EM = Path("/Users/seanpharris/oversight-testbed/programs/entangled-mind")
sys.path.insert(0, str(EM/"experiments"))
import numpy as np
from scipy.special import expit, logit
from scipy.stats import spearmanr
import gm2bf1_order_vs_format as m
from pathlib import Path
D = np.load(Path(__file__).resolve().parent / "marg.npz")
LEV, WR, FM, E = D["lev"], D["W"], D["fm"], D["E"]
N = 160
ITEMS = [f"i{i//4}" for i in range(N)]
x1 = logit((FM[:, 0] + 1) / 102); xo = logit((LEV + 1) / 102)
T = (x1 + xo) / 2
CUT6 = np.array([-3.5, -2.2, -1.0, 0.0, 1.2, 2.6])

def draw(rng, kap=0.0, a=0.5, eta=1.3, tau=1.4, eta2=0.5, mid_ext=0.0, ord_logit=True):
    u = rng.normal(0, 1, N)                       # shared claim-specific instability (used only when kap > 0)
    v1, v2 = rng.normal(0, 1, N), rng.normal(0, 1, N)
    # ---- order side
    sig = a * np.exp(eta * v1 + kap * u)
    base = xo
    means = expit(base[:, None] + sig[:, None] * rng.normal(0, 1, (N, 4))) * 100
    means = means + rng.normal(0, 1, (N, 4)) * (WR / np.sqrt(10))[:, None]
    means = np.clip(means, 0, 100); S = means.max(1) - means.min(1)
    # ---- format side: deviations d_if around the common latent T
    sd = tau * np.exp(eta2 * v2 + kap * u)
    d = sd[:, None] * rng.normal(0, 1, (N, 5))
    t = T[:, None] + d
    F = np.zeros((N, 6)); F[:, 0] = FM[:, 0]
    F[:, 1] = rng.binomial(10, expit(2.6 + 2.5 * t[:, 0])) / 10                      # yes/no
    F[:, 2] = rng.binomial(10, expit(-2.2 + 1.6 * t[:, 1])) / 10                     # bet (price-insensitive in archive)
    F[:, 3] = rng.binomial(10, expit(2.4 + 1.0 * t[:, 2])) / 10                      # vs coin
    r5 = np.clip(np.round(expit(t[:, 3, None] - 0.3 + 0.8 * rng.normal(0, 1, (N, 10))) * 110 - 6), 0, 100)
    F[:, 4] = r5.mean(1)
    lat6 = t[:, 4, None] + 0.35 * rng.logistic(0, 1, (N, 10))
    F[:, 5] = (lat6[..., None] > CUT6).sum(-1).mean(1)
    G, Ee = m.format_measures(F, F[:, 0])
    return S, G, F

if __name__ == "__main__":
    rng = np.random.default_rng(2)
    S, G, F = draw(rng)
    print("S q", np.round(np.percentile(S, [0, 10, 25, 50, 75, 90, 100]), 1), "(real 0.2 1.5 4.3 15.1 36.1 61.1 94.6)")
    print("G q", np.round(np.percentile(G, [0, 10, 25, 50, 75, 90, 100]), 3), "(real .037 .076 .103 .165 .228 .281 .378)")
    print("F2 all-yes", (F[:, 1] == 1).sum(), "(90)  F3 all-no", (F[:, 2] == 0).sum(), "(66)  F4 all", (F[:, 3] == 1).sum(), "(90)")
    print("F5 zeros", (F[:, 4] == 0).sum(), "(23)  F6 biggest block", np.unique(F[:, 5], return_counts=True)[1].max(), "(25)")
    print("Spearman matrix\n", np.round(spearmanr(F).statistic, 2))
    print("lev vs formats", np.round([spearmanr(LEV, F[:, j]).statistic for j in range(6)], 2), "(real .82 .67 .62 .40 .49 .72)")
