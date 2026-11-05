"""qwalk (bet em-qwalk): a simulated quantum walk against personalised PageRank on program 1's claim graph.

Laptop only: no API call, no QPU second, no network. numpy only. Pre-registration: experiments/qwalk.md.

    python3 qwalk.py --dry-run            # synthetic graphs only; never reads the real graph or its labels
    python3 qwalk.py --graph-counts <c>   # prints node, edge and label COUNTS at commit <c> (design review); no predictor run
    python3 qwalk.py --run <c> --seed <n> # the pre-registered analysis at commit <c>; refuses without a design-review go

Paths are relative to the engine repo root (found from this file's location).

The two predictors share one generator, one seed set and one exponential stopping time:
  classical (personalised PageRank, damping a):  p = (1-a) s (I - a P)^-1 = s (I + tau L_rw)^-1,  tau = a/(1-a)
  quantum (continuous-time walk):                 P(i) = E_t |<i| exp(-i L_sym t) |psi_S>|^2,  t ~ Exponential(mean tau)
with L_rw = I - D^-1 A, L_sym = I - D^-1/2 A D^-1/2 (similar matrices, same spectrum), s uniform on the seeds,
psi_S the equal-amplitude superposition of the seeds. The exponential average is exact:
  P(i) = sum_{k,l} V_ik V_il c_k c_l / (1 + (lam_k - lam_l)^2 tau^2),  c = V^T psi_S.
"""
import argparse
import json
import os
import re
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
BET = "em-qwalk"
ALPHA = 0.85                      # PageRank damping (the conventional default; not tuned)
TAU = ALPHA / (1 - ALPHA)         # 5.667: the matched exponential stopping time
B = 10_000                        # bootstrap resamples
ROUND = 12                        # scores rounded to 1e-12 before ranking (exact zeros stay zeros)
SENS_ALPHAS = [0.5, 0.7, 0.85, 0.95]
HIT = {"pass", "pass-unreplicated"}
KILL = {"null", "classical", "tie", "fail"}
EXCLUDE_NODES = {"qwalk"}         # this bet's own node


# ---------------------------------------------------------------- graph construction (frozen rule, prereg §2)

def git_show(commit, path):
    return subprocess.run(["git", "-C", REPO, "show", f"{commit}:{path}"], check=True,
                          capture_output=True, text=True).stdout


def record_times(source):
    """'record.md 15:14, 19:27' -> {'15:14', '19:27'}; other sources -> empty."""
    if not isinstance(source, str) or not source.startswith("record.md"):
        return set()
    return set(re.findall(r"\b\d\d:\d\d\b", source))


def build_graph(mapdoc, bets, parent_only=False):
    dirs = [d for d in mapdoc["directions"] if d["id"] not in EXCLUDE_NODES]
    ids = [d["id"] for d in dirs]
    idx = {n: i for i, n in enumerate(ids)}
    bet_node = {}
    for d in dirs:
        for b in d.get("bets", []) or []:
            bet_node[b] = d["id"]
    edges = set()

    def add(a, b, why):
        if a in idx and b in idx and a != b:
            edges.add(tuple(sorted((a, b))))

    # rule 1: map parent links
    for d in dirs:
        if d.get("parent"):
            add(d["id"], d["parent"], "parent")
    if not parent_only:
        # rule 2: phase-A nodes citing the same record.md row time
        times = {d["id"]: record_times(d.get("source")) for d in dirs if not d.get("bets")}
        tl = list(times)
        for i, a in enumerate(tl):
            for b in tl[i + 1:]:
                if times[a] & times[b]:
                    add(a, b, "record")
        # rule 3: ledger links between bets (parent, replication_of, rebet_of)
        for bet in bets:
            src = bet_node.get(bet["id"])
            if not src:
                continue
            for f in ("parent", "replication_of", "rebet_of"):
                t = bet.get(f)
                if not t:
                    continue
                tgt = bet_node.get(t, t if t in idx else None)
                if tgt:
                    add(src, tgt, f)
    n = len(ids)
    A = np.zeros((n, n))
    for a, b in edges:
        A[idx[a], idx[b]] = A[idx[b], idx[a]] = 1.0
    # labels (frozen rule, prereg §2)
    byid = {b["id"]: b for b in bets}
    labels = {}
    for d in dirs:
        if d.get("bets"):
            vals = set()
            for b in d["bets"]:
                row = byid.get(b)
                if row is None:
                    vals.add(None)
                    continue
                v = row.get("verdict_after_audit") or row.get("verdict")
                vals.add(1 if v in HIT else 0 if v in KILL else None)
            if len(vals) == 1 and None not in vals:
                labels[d["id"]] = vals.pop()
        else:
            s = d.get("status")
            if s == "hit":
                labels[d["id"]] = 1
            elif s == "killed":
                labels[d["id"]] = 0
    phase_b = {d["id"]: 1 if d.get("bets") else 0 for d in dirs}
    return ids, A, labels, sorted(edges), phase_b


# ---------------------------------------------------------------- predictors

def components(A):
    n = len(A)
    seen, comps = [-1] * n, []
    for s in range(n):
        if seen[s] >= 0:
            continue
        stack, comp = [s], []
        seen[s] = len(comps)
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in np.nonzero(A[u])[0]:
                if seen[v] < 0:
                    seen[v] = len(comps)
                    stack.append(v)
        comps.append(sorted(comp))
    return comps


class Walks:
    """Per-component spectral data, so mass never leaks between components numerically."""

    def __init__(self, A):
        self.A = A
        self.n = len(A)
        self.comps = components(A)
        deg = A.sum(1)
        self.deg = deg
        self.spec = []
        for c in self.comps:
            Ac = A[np.ix_(c, c)]
            dc = deg[c]
            if len(c) == 1:
                Ls = np.zeros((1, 1))
            else:
                dm = 1 / np.sqrt(dc)
                Ls = np.eye(len(c)) - dm[:, None] * Ac * dm[None, :]
            lam, V = np.linalg.eigh(Ls)
            self.spec.append((c, lam, V, Ac, dc))

    def quantum(self, seeds, tau, coherent=True):
        out = np.zeros(self.n)
        if not seeds:
            return out
        seeds = list(seeds)
        if coherent:
            amp = np.zeros(self.n)
            amp[seeds] = 1 / np.sqrt(len(seeds))
            for c, lam, V, _, _ in self.spec:
                psi = amp[c]
                if not psi.any():
                    continue
                cc = V.T @ psi
                W = 1 / (1 + (lam[:, None] - lam[None, :]) ** 2 * tau ** 2)
                M = V * cc[None, :]
                out[c] = np.einsum("ik,kl,il->i", M, W, M)
            return out
        for s in seeds:                       # incoherent mixture of single-seed walks (secondary)
            out += self.quantum([s], tau, True) / len(seeds)
        return out

    def classical(self, seeds, tau):
        """s (I + tau L_rw)^-1 == personalised PageRank with damping tau/(1+tau)."""
        out = np.zeros(self.n)
        if not seeds:
            return out
        s = np.zeros(self.n)
        s[list(seeds)] = 1 / len(seeds)
        for c, _, _, Ac, dc in self.spec:
            sc = s[c]
            if not sc.any():
                continue
            if len(c) == 1:
                out[c] = sc
                continue
            Lrw = np.eye(len(c)) - Ac / dc[:, None]
            out[c] = np.linalg.solve((np.eye(len(c)) + tau * Lrw).T, sc)
        return out

    def pagerank_power(self, seeds, alpha, iters=2000):
        """Textbook power iteration, used only to check classical() equals PageRank."""
        s = np.zeros(self.n)
        s[list(seeds)] = 1 / len(seeds)
        P = np.where(self.deg[:, None] > 0, self.A / np.maximum(self.deg[:, None], 1), 0.0)
        for i in np.nonzero(self.deg == 0)[0]:
            P[i, i] = 1.0
        p = s.copy()
        for _ in range(iters):
            p = (1 - alpha) * s + alpha * p @ P
        return p


def lono_scores(W, labels_idx, method, tau):
    """Leave-one-node-out: node i's label is hidden; seeds are every other labelled node."""
    hits = [i for i, y in labels_idx.items() if y == 1]
    kills = [i for i, y in labels_idx.items() if y == 0]
    sc = {}
    for i in labels_idx:
        H = [h for h in hits if h != i]
        K = [k for k in kills if k != i]
        if method == "quantum":
            v = W.quantum(H, tau)[i] - W.quantum(K, tau)[i]
        elif method == "quantum_incoherent":
            v = W.quantum(H, tau, False)[i] - W.quantum(K, tau, False)[i]
        elif method == "pagerank":
            v = W.classical(H, tau)[i] - W.classical(K, tau)[i]
        else:
            raise ValueError(method)
        sc[i] = round(float(v), ROUND)
    return sc


def auroc(scores, y):
    scores, y = np.asarray(scores, float), np.asarray(y)
    pos, neg = scores[y == 1], scores[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    gt = (pos[:, None] > neg[None, :]).sum()
    eq = (pos[:, None] == neg[None, :]).sum()
    return float((gt + 0.5 * eq) / (len(pos) * len(neg)))


def boot_diff(sq, sp, y, rng, b=B):
    """Stratified bootstrap over labelled nodes (hits and kills resampled separately); scores held fixed."""
    sq, sp, y = np.asarray(sq), np.asarray(sp), np.asarray(y)
    pi, ni = np.nonzero(y == 1)[0], np.nonzero(y == 0)[0]
    P = rng.choice(pi, size=(b, len(pi)))
    N = rng.choice(ni, size=(b, len(ni)))

    def au(s):
        a, c = s[P][:, :, None], s[N][:, None, :]
        return ((a > c).sum((1, 2)) + 0.5 * (a == c).sum((1, 2))) / (len(pi) * len(ni))

    d = au(sq) - au(sp)
    return float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))


def verdict(diff, lo, hi, n_hit, n_kill, n_zero, n_lab):
    if n_hit < 5 or n_kill < 5 or n_zero > n_lab / 2:
        return "untestable"
    if diff > 0 and lo > 0:
        return "pass"
    if diff < 0 and hi < 0:
        return "classical"
    return "null"


def analyse(ids, A, labels, rng, tau=TAU, with_extras=True, b=B):
    W = Walks(A)
    idx = {n: i for i, n in enumerate(ids)}
    lab = {idx[k]: v for k, v in labels.items()}
    order = sorted(lab)
    y = [lab[i] for i in order]
    sq = lono_scores(W, lab, "quantum", tau)
    sp = lono_scores(W, lab, "pagerank", tau)
    q = [sq[i] for i in order]
    p = [sp[i] for i in order]
    aq, ap = auroc(q, y), auroc(p, y)
    lo, hi = boot_diff(q, p, y, rng, b)
    n_zero = sum(1 for i in order if sq[i] == 0 and sp[i] == 0)
    out = {"n_nodes": len(ids), "n_edges": int(A.sum() / 2), "n_labelled": len(order),
           "n_hit": int(sum(y)), "n_kill": int(len(y) - sum(y)), "n_zero_both": n_zero,
           "auroc_quantum": aq, "auroc_pagerank": ap, "diff": aq - ap, "ci95": [lo, hi],
           "verdict": verdict(aq - ap, lo, hi, int(sum(y)), int(len(y) - sum(y)), n_zero, len(order))}
    if with_extras:
        out["scores"] = {ids[i]: {"label": lab[i], "quantum": sq[i], "pagerank": sp[i]} for i in order}
    return out, W, lab, order, y, q, p


# ---------------------------------------------------------------- the real run

def review_says_go():
    path = os.path.join(REPO, "ledger", "design-reviews", f"{BET}.md")
    if not os.path.exists(path):
        return False, "no design review file"
    head = open(path).read().split("---")[1] if open(path).read().startswith("---") else ""
    v = re.search(r"^verdict:\s*(\S+)", head, re.M)
    conf = re.search(r"^confirmed_at:\s*(.+)$", head, re.M)
    if v and v.group(1) == "go":
        return True, "go"
    if v and v.group(1) == "fix-first" and conf and conf.group(1).strip() not in ("null", ""):
        return True, "fix-first, confirmed"
    return False, f"verdict {v.group(1) if v else None}"


def load(commit, parent_only=False):
    mapdoc = json.loads(git_show(commit, "map/entangled-mind.json"))
    bets = [json.loads(l) for l in git_show(commit, "ledger/bets.jsonl").splitlines() if l.strip()]
    return build_graph(mapdoc, bets, parent_only)


def run(commit, seed):
    ok, why = review_says_go()
    if not ok:
        sys.exit(f"refused: design review is not go ({why})")
    rng = np.random.default_rng(seed)
    ids, A, labels, edges, phase_b = load(commit)
    res, W, lab, order, y, q, p = analyse(ids, A, labels, rng)
    res["commit"], res["seed"], res["alpha"], res["tau"], res["B"] = commit, seed, ALPHA, TAU, B
    res["edges"] = [list(e) for e in edges]
    res["unlabelled"] = [n for n in ids if n not in labels]
    # secondary (reported, never promoted): matched-twin identity check
    k = [i for i in order if lab[i] == 1][:3]
    res["pagerank_identity_maxdiff"] = float(np.abs(W.classical(k, TAU) - W.pagerank_power(k, ALPHA)).max())
    # secondary: chance comparisons and dumb baselines (P3)
    rng2 = np.random.default_rng(seed + 1)
    names = [ids[i] for i in order]
    res["secondary"] = {}
    for nm, sc in [("quantum", q), ("pagerank", p),
                   ("phase_bit", [phase_b[n] for n in names]),
                   ("neighbour_vote", [round(float(np.mean([lab[j] for j in np.nonzero(A[i])[0] if j in lab]))
                                             if any(j in lab for j in np.nonzero(A[i])[0]) else 0.5, ROUND)
                                       for i in order])]:
        a = auroc(sc, y)
        lo, hi = boot_diff(sc, [0.0] * len(sc), y, rng2)        # AUROC(x) - AUROC(constant) = AUROC(x) - 0.5
        res["secondary"][nm] = {"auroc": a, "ci95_vs_chance": [lo + 0.5, hi + 0.5]}
    qi = lono_scores(W, lab, "quantum_incoherent", TAU)
    res["secondary"]["quantum_incoherent_seeds"] = {"auroc": auroc([qi[i] for i in order], y)}
    # sensitivity (reported, never promoted): damping grid, matched tau; parent-only edges
    res["sensitivity"] = {}
    for a in SENS_ALPHAS:
        r, *_ = analyse(ids, A, labels, np.random.default_rng(seed), tau=a / (1 - a), with_extras=False)
        res["sensitivity"][f"alpha={a}"] = {k2: r[k2] for k2 in ("auroc_quantum", "auroc_pagerank", "diff", "ci95", "verdict")}
    ids2, A2, labels2, _, _ = load(commit, parent_only=True)
    r, *_ = analyse(ids2, A2, labels2, np.random.default_rng(seed), with_extras=False)
    res["sensitivity"]["parent_links_only"] = {k2: r[k2] for k2 in ("n_edges", "auroc_quantum", "auroc_pagerank", "diff", "ci95", "verdict")}
    # robustness (P10): remove one labelled node's label entirely (not a seed, not scored), recompute everything
    flips = {}
    for nme in list(labels):
        l2 = {k2: v for k2, v in labels.items() if k2 != nme}
        r, *_ = analyse(ids, A, l2, np.random.default_rng(seed), with_extras=False)
        flips[nme] = {"diff": r["diff"], "ci95": r["ci95"], "verdict": r["verdict"]}
    res["leave_one_label_out"] = flips
    res["fragile_on"] = [k2 for k2, v in flips.items() if v["verdict"] != res["verdict"]]
    out = os.path.join(HERE, "..", "results", "qwalk.json")
    json.dump(res, open(out, "w"), indent=1, sort_keys=True)
    print(json.dumps({k2: res[k2] for k2 in ("n_nodes", "n_edges", "n_labelled", "n_hit", "n_kill", "n_zero_both",
                                              "auroc_quantum", "auroc_pagerank", "diff", "ci95", "verdict", "fragile_on")}, indent=1))
    print("wrote", os.path.relpath(out, REPO))


def graph_counts(commit):
    ids, A, labels, edges, _ = load(commit)
    print(json.dumps({"n_nodes": len(ids), "n_edges": len(edges), "n_labelled": len(labels),
                      "n_hit": sum(labels.values()), "n_kill": len(labels) - sum(labels.values()),
                      "n_components": len(components(A))}, indent=1))


# ---------------------------------------------------------------- dry run: synthetic graphs only

def synth_forest(rng, n=37, roots=7, extra=3):
    parent = [-1] * roots + [int(rng.integers(0, i)) for i in range(roots, n)]
    A = np.zeros((n, n))
    for i, p in enumerate(parent):
        if p >= 0:
            A[i, p] = A[p, i] = 1
    for _ in range(extra):
        a, b = rng.choice(n, 2, replace=False)
        A[a, b] = A[b, a] = 1
    return A, parent


def depth(parent, i):
    d = 0
    while parent[i] >= 0:
        i, d = parent[i], d + 1
    return d


def dry_run(nsim=300, b=2000):
    rng = np.random.default_rng(20261104)
    rep = {}
    # D2: the knobs take effect
    A, _ = synth_forest(rng)
    W = Walks(A)
    s = [0, 3, 5]
    rep["D2_tau_moves_quantum"] = float(np.abs(W.quantum(s, 1.0) - W.quantum(s, 20.0)).max())
    rep["D2_tau_moves_pagerank"] = float(np.abs(W.classical(s, 1.0) - W.classical(s, 20.0)).max())
    rep["D2_quantum_vs_classical_maxdiff"] = float(np.abs(W.quantum(s, TAU) - W.classical(s, TAU)).max())
    rep["D2_pagerank_identity_maxdiff"] = float(np.abs(W.classical(s, TAU) - W.pagerank_power(s, ALPHA)).max())
    rep["D2_quantum_mass"] = float(W.quantum(s, TAU).sum())
    # exact exponential average vs Monte Carlo over t
    ts = rng.exponential(TAU, 4000)
    c, lam, V, _, _ = max(W.spec, key=lambda x: len(x[0]))
    psi = np.zeros(len(c)); psi[0] = 1
    mc = np.mean([np.abs(V @ (np.exp(-1j * lam * t) * (V.T @ psi))) ** 2 for t in ts], axis=0)
    ex = Walks(A[np.ix_(c, c)]).quantum([0], TAU)
    rep["D2_exact_vs_montecarlo_maxdiff"] = float(np.abs(mc - ex).max())

    def sim(labeller):
        vs, widths, diffs = [], [], []
        for _ in range(nsim):
            A, parent = synth_forest(rng)
            n = len(A)
            lab_nodes = rng.choice(n, 25, replace=False)
            labels = labeller(rng, A, parent, lab_nodes)
            if sum(labels.values()) < 5 or len(labels) - sum(labels.values()) < 5:
                continue
            ids = [f"n{i}" for i in range(n)]
            r, *_ = analyse(ids, A, {f"n{k}": v for k, v in labels.items()}, rng, with_extras=False, b=b)
            vs.append(r["verdict"]); widths.append(r["ci95"][1] - r["ci95"][0]); diffs.append(r["diff"])
        return {"n": len(vs), "pass": vs.count("pass") / len(vs), "classical": vs.count("classical") / len(vs),
                "null": vs.count("null") / len(vs), "untestable": vs.count("untestable") / len(vs),
                "median_ci_width": float(np.median(widths)), "mean_diff": float(np.mean(diffs))}

    def random_labels(rng, A, parent, nodes):
        return {int(k): int(rng.random() < 0.4) for k in nodes}

    def homophily(rng, A, parent, nodes, flip=0.2):
        val = {}
        for i in range(len(A)):
            if parent[i] < 0:
                val[i] = int(rng.random() < 0.4)
            else:
                val[i] = val[parent[i]] if rng.random() > flip else 1 - val[parent[i]]
        return {int(k): val[int(k)] for k in nodes}

    def parity(rng, A, parent, nodes):
        return {int(k): (depth(parent, int(k)) + 1) % 2 for k in nodes}

    rep["null_random_labels"] = sim(random_labels)
    rep["homophily_flip0.2"] = sim(homophily)
    rep["depth_parity"] = sim(parity)
    print(json.dumps(rep, indent=1))
    return rep


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--graph-counts")
    ap.add_argument("--run")
    ap.add_argument("--seed", type=int)
    a = ap.parse_args()
    if a.dry_run:
        dry_run()
    elif a.graph_counts:
        graph_counts(a.graph_counts)
    elif a.run:
        if a.seed is None:
            sys.exit("refused: --seed (the CURBy-derived bootstrap seed) is required")
        run(a.run, a.seed)
    else:
        ap.print_help()
