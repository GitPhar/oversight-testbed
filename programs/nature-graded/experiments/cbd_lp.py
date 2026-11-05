"""Contextuality-by-Default 2.0 for systems of binary random variables: the exact linear program and CNT2.

Sources, read in full before this code was written (P3-9's debt on the map):
  - Dzhafarov & Kujala 2016, "Contextuality-by-Default 2.0: Systems with Binary Random Variables",
    arXiv:1604.04799 (Definitions 1-3; Theorem 1: a binary connection's multimaximal coupling exists, is unique,
    and puts mass only on the k+1 "threshold" strings; Theorem 3: subsystems of noncontextual systems are noncontextual).
  - Kujala & Dzhafarov 2019, "Measures of contextuality and noncontextuality", Phil. Trans. R. Soc. A 377:20190149,
    arXiv:1903.07170 (sections 3-5: reduced probability vector p = (p_l, p_b, p_c); a system is noncontextual iff
    M x = p* has a solution x >= 0 (eq. 29); CNT2 = min ||p*_b - M_b x||_1 over x >= 0 with M_l x = p*_l and
    M_c x = p*_c (eq. 38-40)).

Encoding (fixed here, before any data): each random variable is 0/1 with 1 meaning the observable's eigenvalue -1
was recorded (the ancilla bit as measured). p_l holds the 1-marginals Pr[R = 1]; p_b holds, for every context and every
subset of its variables with two or more members, Pr[all members = 1] (the bunch k-marginals, k >= 2); p_c holds
the connections' pairwise Pr[both = 1] under their multimaximal couplings (section 3.8: k > 2 is redundant for
connections). Whether the LP is feasible (CNT2 = 0) does not depend on this encoding; CNT2's size does.

Reduction used (exact, not an approximation): by Theorem 1 every coupling x that meets M_l x = p*_l and M_c x = p*_c
puts zero mass on any joint value in which some connection is not one of its threshold strings. So the LP's columns
are the product of the connections' threshold strings (3^9 = 19,683 for a 6-context Peres-Mermin system, instead of
2^18 = 262,144), and M_l x = p*_l with M_c x = p*_c become: each connection's threshold-string masses equal
(p_1, p_2 - p_1, ..., 1 - p_k) with the p's sorted. `full_lp=True` builds the unreduced 2^N LP for checking.

The chip is never a computational resource here: this file is classical analysis code run on a laptop.
"""

from __future__ import annotations

import itertools

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csc_matrix

TOL = 1e-6          # CNT2 at or below this is "zero" (P13: a named boundary is never compared in plain floating point)


class System:
    """contexts: list of tuples of content names; bunches: dict context index -> array of 2^k probabilities over the
    context's variables, index = sum(bit_j << j) with bit_j the j-th variable of the context (1 = eigenvalue -1)."""

    def __init__(self, contexts, bunches):
        self.contexts = [tuple(c) for c in contexts]
        self.bunches = {i: np.asarray(bunches[i], float) for i in range(len(self.contexts))}
        for i, c in enumerate(self.contexts):
            p = self.bunches[i]
            assert p.shape == (2 ** len(c),), (i, p.shape)
            assert np.all(p >= -1e-12) and abs(p.sum() - 1) < 1e-9, (i, p.sum())
        self.vars = [(i, q) for i, c in enumerate(self.contexts) for q in c]
        self.contents = sorted({q for c in self.contexts for q in c})
        self.conn = {q: [(i, c.index(q)) for i, c in enumerate(self.contexts) if q in c] for q in self.contents}

    def marginal(self, i, j):
        """Pr[variable j of context i = 1]."""
        p = self.bunches[i]
        return float(sum(p[s] for s in range(len(p)) if (s >> j) & 1))

    def subset_all_ones(self, i, js):
        p = self.bunches[i]
        return float(sum(p[s] for s in range(len(p)) if all((s >> j) & 1 for j in js)))


def threshold_strings(ps):
    """Theorem 1: with the connection's members sorted by p_i = Pr[R = 1] ascending, the multimaximal coupling's
    support is the k+1 strings 'first l members 0 (value 2 in the paper), the rest 1', l = 0..k, with masses
    p_1, p_2 - p_1, ..., 1 - p_k. Returns (strings as tuples in the members' original order, masses)."""
    k = len(ps)
    order = np.argsort(ps, kind="stable")
    sp = np.asarray(ps, float)[order]
    masses = np.diff(np.concatenate([[0.0], sp, [1.0]]))
    strings = []
    for l in range(k + 1):
        s = [0] * k
        for rank, member in enumerate(order):
            s[member] = 0 if rank < l else 1
        strings.append(tuple(s))
    return strings, np.clip(masses, 0.0, None)


def _bunch_events(sysm):
    ev = []
    for i, c in enumerate(sysm.contexts):
        for r in range(2, len(c) + 1):
            for js in itertools.combinations(range(len(c)), r):
                ev.append((i, js))
    return ev


def _columns(sysm, full_lp):
    """Every column is an assignment of 0/1 to every variable, stored as dict (i, j) -> bit."""
    if full_lp:
        keys = [(i, sysm.contexts[i].index(q)) for (i, q) in sysm.vars]
        for bits in itertools.product((0, 1), repeat=len(keys)):
            yield dict(zip(keys, bits)), None
        return
    per_conn = []
    for q in sysm.contents:
        members = sysm.conn[q]
        strings, _ = threshold_strings([sysm.marginal(i, j) for i, j in members])
        per_conn.append([(members, s, li) for li, s in enumerate(strings)])
    for combo in itertools.product(*per_conn):
        a, labels = {}, []
        for members, s, li in combo:
            for (i, j), b in zip(members, s):
                a[(i, j)] = b
            labels.append(li)
        yield a, tuple(labels)


def build(sysm, full_lp=False):
    """Returns (A_fix, b_fix, A_b, p_b): equality rows that fix p_l and p_c (or, reduced, the connections' threshold
    masses), and the bunch-event rows with their observed values."""
    bev = _bunch_events(sysm)
    p_b = np.array([sysm.subset_all_ones(i, js) for i, js in bev])
    cols = list(_columns(sysm, full_lp))
    n = len(cols)
    rows_b, cols_b = [], []
    for col, (a, _) in enumerate(cols):
        for r, (i, js) in enumerate(bev):
            if all(a[(i, j)] for j in js):
                rows_b.append(r); cols_b.append(col)
    A_b = csc_matrix((np.ones(len(rows_b)), (rows_b, cols_b)), shape=(len(bev), n))
    rows, cols_f, b_fix = [0] * n, list(range(n)), [1.0]       # row 0: normalisation (the zero-marginal, = 1)
    r = 1
    if full_lp:
        # p_l: every variable's 1-marginal; p_c: every connection pair's Pr[both = 1] under the multimaximal coupling
        for (i, q) in sysm.vars:
            j = sysm.contexts[i].index(q)
            for col, (a, _) in enumerate(cols):
                if a[(i, j)]:
                    rows.append(r); cols_f.append(col)
            b_fix.append(sysm.marginal(i, j)); r += 1
        for q in sysm.contents:
            members = sysm.conn[q]
            ps = [sysm.marginal(i, j) for i, j in members]
            for (m1, (i1, j1)), (m2, (i2, j2)) in itertools.combinations(enumerate(members), 2):
                for col, (a, _) in enumerate(cols):
                    if a[(i1, j1)] and a[(i2, j2)]:
                        rows.append(r); cols_f.append(col)
                b_fix.append(min(ps[m1], ps[m2])); r += 1       # maximal coupling of two binaries: Pr[both 1] = min
    else:
        for ci, q in enumerate(sysm.contents):
            members = sysm.conn[q]
            _, masses = threshold_strings([sysm.marginal(i, j) for i, j in members])
            for li, m in enumerate(masses):
                for col, (_, labels) in enumerate(cols):
                    if labels[ci] == li:
                        rows.append(r); cols_f.append(col)
                b_fix.append(float(m)); r += 1
    A_fix = csc_matrix((np.ones(len(rows)), (rows, cols_f)), shape=(r, n))
    return A_fix, np.array(b_fix), A_b, p_b


def cnt2(sysm, full_lp=False, return_x=False):
    """CNT2 (Kujala & Dzhafarov 2019, eq. 39): min 1.d s.t. -d <= p*_b - M_b x <= d, x, d >= 0, M_l x = p*_l, M_c x = p*_c.
    Returns CNT2 (>= 0); 0 (to TOL) means the system is noncontextual."""
    A_fix, b_fix, A_b, p_b = build(sysm, full_lp)
    n, m = A_fix.shape[1], A_b.shape[0]
    from scipy.sparse import hstack, identity, vstack
    I = identity(m, format="csc")
    Z = csc_matrix((A_fix.shape[0], m))
    A_eq = hstack([A_fix, Z]).tocsc()
    #  M_b x - d <= p_b   and   -M_b x - d <= -p_b
    A_ub = vstack([hstack([A_b, -I]), hstack([-A_b, -I])]).tocsc()
    b_ub = np.concatenate([p_b, -p_b])
    c = np.concatenate([np.zeros(n), np.ones(m)])
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_fix, bounds=(0, None), method="highs")
    if res.status != 0:
        raise RuntimeError(f"CNT2 LP did not solve: status {res.status}, {res.message}")
    val = max(0.0, float(res.fun))
    return (val, res.x[:n]) if return_x else val


def feasible(sysm, full_lp=False):
    """Kujala & Dzhafarov 2019 eq. 29: is there x >= 0 with M x = p* (bunches matched exactly)? True = noncontextual."""
    A_fix, b_fix, A_b, p_b = build(sysm, full_lp)
    from scipy.sparse import vstack
    res = linprog(np.zeros(A_fix.shape[1]), A_eq=vstack([A_fix, A_b]).tocsc(), b_eq=np.concatenate([b_fix, p_b]),
                  bounds=(0, None), method="highs")
    return res.status == 0


# --- Peres-Mermin ------------------------------------------------------------------------------------------------

# The square used by Kirchmair et al. 2009 (arXiv:0904.1655) and the map: rows and columns are the six contexts.
SQUARE = (("Z1", "Z2", "Z1Z2"),
          ("X2", "X1", "X1X2"),
          ("Z1X2", "X1Z2", "Y1Y2"))
LINES = [SQUARE[0], SQUARE[1], SQUARE[2],
         tuple(r[0] for r in SQUARE), tuple(r[1] for r in SQUARE), tuple(r[2] for r in SQUARE)]
LINE_NAMES = ["R1", "R2", "R3", "C1", "C2", "C3"]
SIGN = [+1, +1, +1, +1, +1, -1]       # quantum product of each line: +I except column 3 (Z1Z2 . X1X2 . Y1Y2 = -I)


def pm_system(bunches_by_line, reverse=False):
    """A 6-context Peres-Mermin system. bunches_by_line[k]: 8 probabilities over the line's three outcomes in the
    order they were MEASURED (forward: the line's order; reverse: last to first). Variables are re-indexed to the
    line's own order, so every observable is the same conteNt in its row and its column."""
    ctx, bun = [], {}
    for k, line in enumerate(LINES):
        p = np.asarray(bunches_by_line[k], float)
        if reverse:
            q = np.zeros(8)
            for s in range(8):
                b = [(s >> j) & 1 for j in range(3)]           # measured order: b[0] is the line's last observable
                t = b[2] | (b[1] << 1) | (b[0] << 2)
                q[t] += p[s]
            p = q
        ctx.append(line); bun[k] = p
    return System(ctx, bun)


def chi(sysm):
    """The PM sum <R1>+<R2>+<R3>+<C1>+<C2>-<C3> of the line products, with the +/-1 eigenvalue (-1)^bit."""
    tot = 0.0
    for k in range(6):
        p = sysm.bunches[k]
        prod = sum(p[s] * (-1) ** bin(s).count("1") for s in range(8))
        tot += SIGN[k] * prod
    return float(tot)


def means_pm1(sysm):
    """<A> in +/-1 units for every variable: dict (line index, content) -> mean."""
    return {(i, q): 1 - 2 * sysm.marginal(i, j) for i, c in enumerate(sysm.contexts) for j, q in enumerate(c)}


def delta0(sysm):
    """Masse 2021 eq. 72: (1/2) sum over the 9 connections of |<A^k> - <A^l>| (+/-1 units)."""
    m = means_pm1(sysm)
    tot = 0.0
    for q in sysm.contents:
        (i1, _), (i2, _) = sysm.conn[q]
        tot += abs(m[(i1, q)] - m[(i2, q)])
    return 0.5 * tot


def s_odd(a):
    a = np.asarray(a, float)
    best = -np.inf
    for signs in itertools.product((1, -1), repeat=len(a)):
        if sum(s < 0 for s in signs) % 2 == 1:
            best = max(best, float(np.dot(signs, a)))
    return best


def masse_cntx(sysm):
    """Masse 2021 eq. 71, 111: CNTX = (1/2) max(2 Delta0, s_odd(a1..a6) - 4) - Delta0, a_k the line products.
    Reported for comparison only: the review gives no proof that it is the exact CbD criterion for this system."""
    a = []
    for k in range(6):
        p = sysm.bunches[k]
        a.append(sum(p[s] * (-1) ** bin(s).count("1") for s in range(8)))
    d0 = delta0(sysm)
    return 0.5 * max(2 * d0, s_odd(a) - 4) - d0


def cyclic_system(n, corr, means_first, means_second):
    """Rank-n cyclic system for the KDL check: context i = (q_i, q_{i+1}); corr[i] = <R_i R_{i+1}> in context i;
    means_first[i] = <R_{q_i}> in context i, means_second[i] = <R_{q_{i+1}}> in context i (+/-1 units)."""
    ctx, bun = [], {}
    for i in range(n):
        a, b, e = means_first[i], means_second[i], corr[i]
        # 2x2 table over (bit_a, bit_b), value (-1)^bit
        p = np.zeros(4)
        p[0] = (1 + a + b + e) / 4
        p[1] = (1 - a + b - e) / 4
        p[2] = (1 + a - b - e) / 4
        p[3] = (1 - a - b + e) / 4
        ctx.append((f"q{i}", f"q{(i + 1) % n}")); bun[i] = p
    return System(ctx, bun)


def kdl_contextual(n, corr, means_first, means_second):
    """Kujala, Dzhafarov & Larsson 2015 (PRL 115:150401, arXiv:1412.4724): a cyclic rank-n system is contextual iff
    s_odd(<R_i R_{i+1}>) - sum_i |<R_q^c> - <R_q^c'>| > n - 2."""
    d = sum(abs(means_second[i] - means_first[(i + 1) % n]) for i in range(n))
    return s_odd(corr) - d - (n - 2)


# --- the check on Kirchmair et al. 2009's published numbers (the map's debt before P3-9's pre-registration) --------

# Kirchmair et al. 2009 (Nature 460:494, arXiv:0904.1655), singlet state, as transcribed from the Supplementary
# Material by Masse 2021 (arXiv:2105.13821, section XI.D, eqs. 75-92 and 104-109): every observable's mean in each of
# its two contexts (+/-1 units) and the six line products. The in-context pair correlations were not published.
KIRCHMAIR_MEANS = {  # content: (mean in its row, mean in its column)
    "Z1": (0.031, 0.064), "Z2": (0.0, -0.031), "Z1Z2": (-0.92, -0.95),
    "X2": (-0.013, -0.009), "X1": (0.017, -0.069), "X1X2": (-0.938, -0.918),
    "Z1X2": (-0.027, -0.005), "X1Z2": (-0.007, -0.1), "Y1Y2": (-0.88, -0.893)}
KIRCHMAIR_PRODUCTS = [0.924, 0.931, 0.900, 0.900, 0.895, -0.913]   # R1, R2, R3, C1, C2, C3
MASSE_CNTX = 0.566                                                   # Masse 2021 eq. 115


def _line_means(means, products):
    out = []
    for k, line in enumerate(LINES):
        col = 0 if k < 3 else 1
        out.append(([means[q][col] for q in line], products[k]))
    return out


def completion_bounds(means, products):
    """Min CNT2 over every set of six bunch distributions that match the published means and line products (the pair
    correlations free, subject to every cell >= 0). CNT2 is an LP in the bunch vector, and the bunch vector is linear
    in the free cells, so the minimum is one LP. Returns (min CNT2, max-entropy completion's CNT2, its system)."""
    lm = _line_means(means, products)
    signs = np.array([[(-1) ** ((s >> j) & 1) for j in range(3)] for s in range(8)])
    # max-entropy completion per line (for the reported point value)
    from scipy.optimize import minimize
    bunches = []
    for (mu, t) in lm:
        A = np.vstack([np.ones(8), signs.T, signs.prod(1)])
        b = np.concatenate([[1.0], mu, [t]])
        f = lambda p: float(np.sum(p * np.log(np.clip(p, 1e-15, None))))
        cons = [{"type": "eq", "fun": lambda p, A=A, b=b: A @ p - b}]
        p0 = np.linalg.lstsq(A, b, rcond=None)[0]
        p0 = np.clip(p0, 1e-3, None); p0 /= p0.sum()
        r = minimize(f, p0, constraints=cons, bounds=[(0, 1)] * 8, method="SLSQP", options={"ftol": 1e-12, "maxiter": 500})
        assert r.success and np.allclose(A @ r.x, b, atol=1e-8), r.message
        bunches.append(np.clip(r.x, 0, None) / np.clip(r.x, 0, None).sum())
    sysm = pm_system(bunches)
    me = cnt2(sysm)
    # min over completions: variables x (columns), d (|bunch events|), q (6 x 8 cells)
    A_fix, b_fix, A_b, _ = build(sysm)                      # threshold masses depend only on the published means
    bev = _bunch_events(sysm)
    n, m = A_fix.shape[1], A_b.shape[0]
    from scipy.sparse import hstack, identity, vstack
    Q = np.zeros((m, 48))                                   # p_b = Q q
    for r_, (i, js) in enumerate(bev):
        for s in range(8):
            if all((s >> j) & 1 for j in js):
                Q[r_, 8 * i + s] = 1
    Aq = np.zeros((30, 48)); bq = np.zeros(30)               # each line: normalisation, 3 means, product
    for i, (mu, t) in enumerate(lm):
        Aq[5 * i, 8 * i:8 * i + 8] = 1; bq[5 * i] = 1
        for j in range(3):
            Aq[5 * i + 1 + j, 8 * i:8 * i + 8] = signs[:, j]; bq[5 * i + 1 + j] = mu[j]
        Aq[5 * i + 4, 8 * i:8 * i + 8] = signs.prod(1); bq[5 * i + 4] = t
    I = identity(m, format="csc")
    A_eq = vstack([hstack([A_fix, csc_matrix((A_fix.shape[0], m)), csc_matrix((A_fix.shape[0], 48))]),
                   hstack([csc_matrix((30, n)), csc_matrix((30, m)), csc_matrix(Aq)])]).tocsc()
    b_eq = np.concatenate([b_fix, bq])
    Qs = csc_matrix(Q)
    A_ub = vstack([hstack([A_b, -I, -Qs]), hstack([-A_b, -I, Qs])]).tocsc()
    res = linprog(np.concatenate([np.zeros(n), np.ones(m), np.zeros(48)]), A_ub=A_ub, b_ub=np.zeros(2 * m),
                  A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method="highs")
    if res.status != 0:
        raise RuntimeError(res.message)
    return max(0.0, float(res.fun)), me, sysm
