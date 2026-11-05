"""qwalk2 (bet em-qwalk2): a simulated quantum walk against personalised PageRank on program 1's direction graph.

Laptop only: no API call, no QPU second, no network. numpy only. Pre-registration: experiments/qwalk2.md.
Re-bet of em-qwalk (withdrawn before data, D56). The graph and label rule are em-qwalk's, unchanged.

    python3 qwalk2.py --dry-run                     # synthetic graphs and labels only
    python3 qwalk2.py --dry-run-real-topology <c>   # the real links and labelled-node set, label VALUES discarded
    python3 qwalk2.py --dry-run-planted <c>         # planted-kernel worlds on the real links (values discarded)
    python3 qwalk2.py --null-thresholds <c>         # permutation-null pass thresholds, 40 seeds x 10,000 shuffles
    python3 qwalk2.py --graph-counts <c>            # node, edge, label, component counts; no predictor
    python3 qwalk2.py --run --seed-bootstrap <n> --seed-permutation <n>   # inputs fixed at INPUT_COMMIT (680f128)

Both arms seed one walk per settled direction and sum the walks with weights centred on the others' hit rate,
so the arms differ only in the one-seed kernel over the same links and stopping time:
  classical  K_C[j, i] = [(I + tau L_rw)^-1]_{j i}           (personalised PageRank from j, damping tau/(1+tau))
  quantum    K_Q[j, i] = E_t |<i| exp(-i L_sym t) |j>|^2,  t ~ Exponential(mean tau)   (exact, per component)
  score(i)   = sum_{j labelled, j != i} (y_j - ybar_{-i}) K[j, i],  ybar_{-i} = mean label of the other settled nodes
The hidden node's label still shapes its score through ybar_{-i} and the others' composition (the leave-one-out leak,
pattern P11); the label-permutation null on the frozen graph carries the same leak, and the verdict is read against it.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
BET = "em-qwalk2"
PREREG_FILE = "programs/entangled-mind/experiments/qwalk2.md"
INPUT_COMMIT = "680f128b156efe9c4a7e401232d328be45e53b7a"   # em-qwalk's pre-registration: the graph both reviews examined (qwalk2.md §2)
ALPHA = 0.85                      # PageRank damping (the conventional default; not tuned)
TAU = ALPHA / (1 - ALPHA)         # 5.667: the matched exponential stopping time
B = 10_000                        # bootstrap resamples (primary)
P = 10_000                        # label permutations (primary)
P_ROB = 2_000                     # permutations in sensitivity and robustness rows
B_ROB = 2_000
ROUND = 12                        # scores rounded to 1e-12 before ranking (exact zeros stay zeros)
SENS_ALPHAS = [0.5, 0.7, 0.85, 0.95]
HIT = {"pass", "pass-unreplicated"}
KILL = {"null", "classical", "tie", "fail"}
EXCLUDE_NODES = {"qwalk"}         # the direction this bet tests (em-qwalk, em-qwalk2)


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
    # D56 (design review em-qwalk-1b F2, F3, F5): structure used by the dumb baselines,
    # the prospective sensitivity and leave-one-cluster-out. Never uses a label.
    parent = {d["id"]: (d.get("parent") if d.get("parent") in idx else None) for d in dirs}
    children = {n: sum(1 for m in ids if parent[m] == n) for n in ids}

    def ancestors(n):
        out = []
        while parent[n]:
            n = parent[n]
            out.append(n)
        return out

    desc = {n: set() for n in ids}
    for m in ids:
        for a in ancestors(m):
            desc[a].add(m)
    citers = {n: set() for n in ids}           # nodes whose bets cite n's bet in replication_of / rebet_of
    for bet in bets:
        src = bet_node.get(bet["id"])
        if not src:
            continue
        for f in ("replication_of", "rebet_of"):
            t = bet.get(f)
            tgt = bet_node.get(t, t if t in idx else None) if t else None
            if tgt and tgt != src:
                citers[tgt].add(src)
    meta = {"phase_b": {d["id"]: 1 if d.get("bets") else 0 for d in dirs},
            "parent": parent, "children": children, "desc": desc, "citers": citers,
            "depth": {n: len(ancestors(n)) for n in ids}}
    return ids, A, labels, sorted(edges), meta


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



# ---------------------------------------------------------------- kernels and scores

def kernels(A, tau=TAU):
    """Row j: the one-seed walk from j, read at every node. Rows sum to 1 within j's component."""
    W = Walks(A)
    n = len(A)
    KQ, KC = np.zeros((n, n)), np.zeros((n, n))
    for j in range(n):
        KQ[j] = W.quantum([j], tau)
        KC[j] = W.classical([j], tau)
    return KQ, KC, W


def columns(K, nodes):
    """C[a, b] = K[nodes[a], nodes[b]], diagonal zeroed: what settled node a sends to settled node b."""
    C = K[np.ix_(nodes, nodes)].copy()
    np.fill_diagonal(C, 0.0)
    return C


def scores(C, Y):
    """Centred leave-one-out scores for one label vector (n,) or many (m, n)."""
    Y = np.asarray(Y, float)
    nl = Y.shape[-1]
    T = Y.sum(-1, keepdims=True) if Y.ndim == 2 else Y.sum()
    R = C.sum(0)
    return np.round(Y @ C - (T - Y) / (nl - 1) * R, ROUND)


def auroc_rows(S, Y):
    """AUROC per row (hits positive), ties one half."""
    S, Y = np.atleast_2d(S), np.atleast_2d(np.asarray(Y, float))
    gt = (S[:, :, None] > S[:, None, :]).astype(float)
    eq = (S[:, :, None] == S[:, None, :]).astype(float)
    M = Y[:, :, None] * (1 - Y)[:, None, :]
    num = ((gt + 0.5 * eq) * M).sum((1, 2))
    den = Y.sum(1) * (Y.shape[1] - Y.sum(1))
    return num / den


def boot(sq, sc, y, rng, b):
    """Stratified bootstrap over settled nodes, scores held fixed: intervals for the difference and each AUROC."""
    sq, sc, y = np.asarray(sq), np.asarray(sc), np.asarray(y)
    pi, ni = np.nonzero(y == 1)[0], np.nonzero(y == 0)[0]
    Pi = rng.choice(pi, size=(b, len(pi)))
    Ni = rng.choice(ni, size=(b, len(ni)))

    def au(s):
        a, c = s[Pi][:, :, None], s[Ni][:, None, :]
        return ((a > c).sum((1, 2)) + 0.5 * (a == c).sum((1, 2))) / (len(pi) * len(ni))

    aq, ac = au(sq), au(sc)
    pc = lambda x: [float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))]
    return pc(aq - ac), pc(aq), pc(ac)


def dumb_scores(A, ids, nodes, y, meta):
    """Oriented dumb rules (em-qwalk-1b F2). The neighbour vote never sees the scored node's own label."""
    lab = dict(zip(nodes, y))
    out = {"phase_bit": [meta["phase_b"][ids[i]] for i in nodes],
           "degree": [int(A[i].sum()) for i in nodes],
           "child_count": [meta["children"][ids[i]] for i in nodes]}
    nv = []
    for i in nodes:
        nb = [lab[j] for j in np.nonzero(A[i])[0] if j in lab and j != i]
        nv.append(round(float(np.mean(nb)), ROUND) if nb else 0.5)
    out["neighbour_vote"] = nv
    return out


def verdict(r):
    if r["n_hit"] < 5 or r["n_kill"] < 5 or r["n_zero_both"] > r["n_labelled"] / 2:
        return "untestable"
    if (r["diff"] > 0 and r["ci95"][0] > 0 and r["diff"] > r["perm_diff_q975"]
            and r["auroc_quantum"] > r["perm_quantum_q975"] and r["ci95_quantum"][0] > 0.5
            and r["auroc_quantum"] > r["best_dumb"]):
        return "pass"
    if (r["diff"] < 0 and r["ci95"][1] < 0 and r["diff"] < r["perm_diff_q025"]
            and r["auroc_pagerank"] > r["perm_pagerank_q975"] and r["ci95_pagerank"][0] > 0.5
            and r["auroc_pagerank"] > r["best_dumb"]):
        return "classical"
    return "null"


def analyse(ids, A, labels, meta, rng_b, rng_p, b=B, p=P, tau=TAU, cols=None, extras=True):
    """cols: optional (CQ, CC) column matrices (the prospective sensitivity builds them per hidden node)."""
    idx = {n: i for i, n in enumerate(ids)}
    nodes = sorted(idx[k] for k in labels)
    y = np.array([labels[ids[i]] for i in nodes], float)
    r = {"n_nodes": len(ids), "n_edges": int(A.sum() / 2), "n_labelled": len(nodes),
         "n_hit": int(y.sum()), "n_kill": int(len(y) - y.sum())}
    if cols is None:
        KQ, KC, _ = kernels(A, tau)
        CQ, CC = columns(KQ, nodes), columns(KC, nodes)
    else:
        CQ, CC = cols
    sq, sc = scores(CQ, y), scores(CC, y)
    r["n_zero_both"] = int(((sq == 0) & (sc == 0)).sum())
    if r["n_hit"] < 2 or r["n_kill"] < 2:
        r.update({"verdict": "untestable", "diff": None})
        return r
    aq, ac = float(auroc_rows(sq, y)[0]), float(auroc_rows(sc, y)[0])
    ci, cq, cc = boot(sq, sc, y, rng_b, b)
    Yp = np.array([rng_p.permutation(y) for _ in range(p)])
    nq, nc = auroc_rows(scores(CQ, Yp), Yp), auroc_rows(scores(CC, Yp), Yp)
    nd = nq - nc
    dumb = {}
    for nm, s in dumb_scores(A, ids, nodes, y, meta).items():
        a = float(auroc_rows(np.array(s, float), y)[0])
        dumb[nm] = {"auroc": a, "oriented": max(a, 1 - a), "orientation": "as is" if a >= 0.5 else "reversed"}
    best = max(dumb, key=lambda k: dumb[k]["oriented"])
    r.update({"auroc_quantum": aq, "auroc_pagerank": ac, "diff": aq - ac, "ci95": ci,
              "ci95_quantum": cq, "ci95_pagerank": cc,
              "perm_diff_q025": float(np.percentile(nd, 2.5)), "perm_diff_q975": float(np.percentile(nd, 97.5)),
              "perm_quantum_q975": float(np.percentile(nq, 97.5)), "perm_pagerank_q975": float(np.percentile(nc, 97.5)),
              "perm_quantum_mean": float(nq.mean()), "perm_pagerank_mean": float(nc.mean()),
              "perm_p_diff_upper": float((1 + (nd >= aq - ac).sum()) / (1 + p)),
              "dumb": dumb, "best_dumb": dumb[best]["oriented"], "best_dumb_rule": best,
              "visible_gap_80pct_power": 1.43 * (ci[1] - ci[0]) / 2})
    r["verdict"] = verdict(r)
    if extras:
        r["scores"] = {ids[i]: {"label": int(yy), "quantum": float(a), "pagerank": float(c)}
                       for i, yy, a, c in zip(nodes, y, sq, sc)}
    return r


KEEP = ("n_labelled", "n_hit", "n_kill", "auroc_quantum", "auroc_pagerank", "diff", "ci95", "ci95_quantum",
        "perm_diff_q975", "perm_quantum_q975", "best_dumb", "best_dumb_rule", "verdict")


def prospective_cols(ids, A, labels, meta, tau=TAU):
    """em-qwalk-1b F3: when node i is scored, its edges to its descendants and to the nodes whose bets cite it are deleted."""
    idx = {n: i for i, n in enumerate(ids)}
    nodes = sorted(idx[k] for k in labels)
    CQ, CC = np.zeros((len(nodes), len(nodes))), np.zeros((len(nodes), len(nodes)))
    for bcol, i in enumerate(nodes):
        cut = {idx[m] for m in meta["desc"][ids[i]] | meta["citers"][ids[i]]}
        Ai = A.copy()
        for j in cut:
            Ai[i, j] = Ai[j, i] = 0.0
        W = Walks(Ai)
        for a, j in enumerate(nodes):
            if j != i:
                CQ[a, bcol] = W.quantum([j], tau)[i]
                CC[a, bcol] = W.classical([j], tau)[i]
    return np.round(CQ, ROUND), np.round(CC, ROUND)


def clusters(ids, A, labels, meta):
    """em-qwalk-1b F5: each connected component holding a label, and each labelled subtree hanging off `oe`."""
    out = {}
    for comp in components(A):
        names = {ids[i] for i in comp}
        if names & set(labels):
            out["component:" + ",".join(sorted(names)[:3]) + ("…" if len(names) > 3 else "")] = names
    for c in ids:
        if meta["parent"].get(c) == "oe" and ({c} | meta["desc"][c]) & set(labels):
            out["oe-subtree:" + c] = {c} | meta["desc"][c]
    return out


# ---------------------------------------------------------------- pinning, gate, the real run

def prereg_commit():
    out = subprocess.run(["git", "-C", REPO, "log", "--diff-filter=A", "--format=%H", "--", PREREG_FILE],
                         capture_output=True, text=True, check=True).stdout.split()
    return out[-1] if out else None


def recorded_seeds():
    """Recompute both seeds from the randomness recorded in the pre-registration's beacon line (seed commit)."""
    text = open(os.path.join(REPO, PREREG_FILE)).read()
    m = re.search(r"`randomness:`\s*([0-9a-f]{128})", text)
    if not m:
        return None
    sys.path.insert(0, os.path.join(REPO, "ledger"))
    from seed import derive
    return {p: derive(m.group(1), BET, p) for p in ("bootstrap", "permutation")}


def review_says_go():
    """Every ledger/design-reviews/em-qwalk2*.md must be go or confirmed fix-first; both named reviews must exist."""
    d = os.path.join(REPO, "ledger", "design-reviews")
    # D58 (em-qwalk2-1b F-C): every file starting em-qwalk2 and ending .md, and refuse any without a readable verdict
    files = sorted(f for f in os.listdir(d) if f.startswith(BET) and f.endswith(".md"))
    for need in (f"{BET}.md", f"{BET}-1b.md"):
        if need not in files:
            return False, f"missing {need}"
    for f in files:
        text = open(os.path.join(d, f)).read()
        head = text.split("---")[1] if text.startswith("---") else ""
        v = re.search(r"^verdict:\s*(\S+)", head, re.M)
        conf = re.search(r"^confirmed_at:\s*(.+)$", head, re.M)
        if not v:
            return False, f"{f}: no readable verdict line"
        if v and v.group(1) == "go":
            continue
        if v and v.group(1) == "fix-first" and conf and conf.group(1).strip() not in ("null", ""):
            continue
        return False, f"{f}: verdict {v.group(1) if v else None}"
    return True, "all reviews go or confirmed: " + ", ".join(files)


def load(commit, parent_only=False):
    mapdoc = json.loads(git_show(commit, "map/entangled-mind.json"))
    bets = [json.loads(l) for l in git_show(commit, "ledger/bets.jsonl").splitlines() if l.strip()]
    return build_graph(mapdoc, bets, parent_only)


def run(seed_b, seed_p):
    ok, why = review_says_go()
    if not ok:
        sys.exit(f"refused: design review is not go ({why})")
    pc = prereg_commit()
    if not pc:
        sys.exit(f"refused: {PREREG_FILE} is not committed")
    commit = INPUT_COMMIT
    seeds = recorded_seeds()
    if not seeds or seeds != {"bootstrap": seed_b, "permutation": seed_p}:
        sys.exit(f"refused: seeds do not match the beacon recorded in {PREREG_FILE}: {seeds}")
    print("gate:", why, "| prereg", pc[:7], "| inputs", commit[:7], "| seeds", seeds)
    ids, A, labels, edges, meta = load(commit)
    rb, rp = np.random.default_rng(seed_b), np.random.default_rng(seed_p)
    res = analyse(ids, A, labels, meta, rb, rp)
    res.update({"prereg_commit": pc, "input_commit": commit, "seeds": seeds, "alpha": ALPHA, "tau": TAU, "B": B, "P": P,
                "edges": [list(e) for e in edges], "unlabelled": [n for n in ids if n not in labels]})
    W = Walks(A)
    k = [ids.index(n) for n in sorted(labels) if labels[n] == 1][:3]
    res["pagerank_identity_maxdiff"] = float(np.abs(W.classical(k, TAU) - W.pagerank_power(k, ALPHA)).max())
    sub = lambda: (np.random.default_rng(seed_b), np.random.default_rng(seed_p))
    sens = {}
    for a in SENS_ALPHAS:
        sens[f"alpha={a}"] = {k2: v for k2, v in analyse(ids, A, labels, meta, *sub(), B_ROB, P_ROB,
                                                         tau=a / (1 - a), extras=False).items() if k2 in KEEP}
    ids2, A2, labels2, _, meta2 = load(commit, parent_only=True)
    sens["parent_links_only"] = {k2: v for k2, v in analyse(ids2, A2, labels2, meta2, *sub(), B_ROB, P_ROB,
                                                            extras=False).items() if k2 in KEEP + ("n_edges",)}
    sens["prospective"] = {k2: v for k2, v in analyse(ids, A, labels, meta, *sub(), B_ROB, P_ROB,
                                                      cols=prospective_cols(ids, A, labels, meta),
                                                      extras=False).items() if k2 in KEEP}
    sens["prospective_parent_links_only"] = {k2: v for k2, v in analyse(ids2, A2, labels2, meta2, *sub(), B_ROB, P_ROB,
                                                      cols=prospective_cols(ids2, A2, labels2, meta2),
                                                      extras=False).items() if k2 in KEEP}   # D58, optional row
    res["sensitivity"] = sens
    res["secondary_coherent_seeds"] = coherent_secondary(ids, A, labels, np.random.default_rng(seed_p))
    lolo = {}
    for nme in sorted(labels):
        l2 = {k2: v for k2, v in labels.items() if k2 != nme}
        lolo[nme] = {k2: v for k2, v in analyse(ids, A, l2, meta, *sub(), B_ROB, P_ROB, extras=False).items() if k2 in KEEP}
    res["leave_one_label_out"] = lolo
    res["fragile_on"] = [k2 for k2, v in lolo.items() if v["verdict"] != res["verdict"]]
    lco = {}
    for nm, members in clusters(ids, A, labels, meta).items():
        l2 = {k2: v for k2, v in labels.items() if k2 not in members}
        lco[nm] = {"dropped": sorted(members & set(labels)),
                   **{k2: v for k2, v in analyse(ids, A, l2, meta, *sub(), B_ROB, P_ROB, extras=False).items() if k2 in KEEP}}
    res["leave_one_cluster_out"] = lco
    res["fragile_on_cluster"] = [k2 for k2, v in lco.items() if v["verdict"] != res["verdict"]]
    out = os.path.join(HERE, "..", "results", "qwalk2.json")
    json.dump(res, open(out, "w"), indent=1, sort_keys=True)
    print(json.dumps({k2: res[k2] for k2 in ("n_nodes", "n_edges", "n_zero_both", "dumb", "perm_quantum_mean",
                                              "perm_pagerank_mean", "perm_p_diff_upper", "visible_gap_80pct_power")
                      + KEEP + ("fragile_on", "fragile_on_cluster")}, indent=1))
    print("wrote", os.path.relpath(out, REPO))


def coherent_secondary(ids, A, labels, rng, p=500):
    """Reported only: em-qwalk's coherent, count-scaled seeding (the bundle), scored hit-minus-kill, with its own permutation null."""
    W = Walks(A)
    idx = {n: i for i, n in enumerate(ids)}
    nodes = sorted(idx[k] for k in labels)
    y = np.array([labels[ids[i]] for i in nodes])

    def sc(yv):
        out = []
        for a, i in enumerate(nodes):
            H = [j for b2, j in enumerate(nodes) if b2 != a and yv[b2] == 1]
            K = [j for b2, j in enumerate(nodes) if b2 != a and yv[b2] == 0]
            out.append(round(float(W.quantum(H, TAU)[i] - W.quantum(K, TAU)[i]), ROUND))
        return np.array(out)

    obs = float(auroc_rows(sc(y), y)[0])
    null = np.array([auroc_rows(sc(yp), yp)[0] for yp in (rng.permutation(y) for _ in range(p))])
    return {"auroc": obs, "perm_mean": float(null.mean()), "perm_q975": float(np.percentile(null, 97.5)), "P": p}


def graph_counts(commit):
    ids, A, labels, edges, _ = load(commit)
    print(json.dumps({"n_nodes": len(ids), "n_edges": len(edges), "n_labelled": len(labels),
                      "n_hit": sum(labels.values()), "n_kill": len(labels) - sum(labels.values()),
                      "n_components": len(components(A))}, indent=1))


# ---------------------------------------------------------------- dry runs (synthetic labels only)

def star(n_leaf):
    A = np.zeros((n_leaf + 1, n_leaf + 1))
    A[0, 1:] = A[1:, 0] = 1
    return A


def hubgraph(rng):
    """Shaped like program 1's graph: a hub with 19 neighbours, short branches, a 6-node island, a 4-node star, 2 isolates."""
    edges, n = [], 1
    for _ in range(19):
        ch = n
        edges.append((0, ch)); n += 1
        for _ in range(int(rng.choice([0, 0, 0, 1, 2]))):
            edges.append((ch, n)); n += 1
    isl = list(range(n, n + 6)); n += 6
    for a, b in [(0, 1), (0, 2), (1, 3), (1, 4), (1, 5), (0, 5)]:
        edges.append((isl[a], isl[b]))
    c4 = list(range(n, n + 4)); n += 4
    for k in range(1, 4):
        edges.append((c4[0], c4[k]))
    n += 2
    A = np.zeros((n, n))
    parent = [-1] * n
    for a, b in edges:
        A[a, b] = A[b, a] = 1
        parent[b] = a
    return A, parent, c4


def depth_of(parent, i):
    d = 0
    while parent[i] >= 0:
        i, d = parent[i], d + 1
    return d


def tally(rs):
    vs = [r["verdict"] for r in rs]
    ok = [r for r in rs if r.get("diff") is not None]
    f = lambda v: round(vs.count(v) / len(vs), 4)
    return {"n": len(vs), "pass": f("pass"), "classical": f("classical"), "null": f("null"), "untestable": f("untestable"),
            "mean_auroc_quantum": round(float(np.mean([r["auroc_quantum"] for r in ok])), 3),
            "mean_auroc_pagerank": round(float(np.mean([r["auroc_pagerank"] for r in ok])), 3),
            "mean_perm_quantum": round(float(np.mean([r["perm_quantum_mean"] for r in ok])), 3),
            "median_visible_gap_80": round(float(np.median([r["visible_gap_80pct_power"] for r in ok])), 3)}


def synth_meta(n, parent):
    return {"phase_b": {f"n{i}": 0 for i in range(n)}, "children": {f"n{i}": parent.count(i) for i in range(n)}}


def dry_run(N=1000, b=500, p=500, seed=20261104):
    rng = np.random.default_rng(seed)
    rep = {}
    A = hubgraph(rng)[0]
    W = Walks(A)
    s = [0, 3, 5]
    rep["D2_tau_moves_quantum"] = float(np.abs(W.quantum(s, 1.0) - W.quantum(s, 20.0)).max())
    rep["D2_tau_moves_pagerank"] = float(np.abs(W.classical(s, 1.0) - W.classical(s, 20.0)).max())
    KQ, KC, _ = kernels(A)
    rep["D2_kernels_differ_maxdiff"] = float(np.abs(KQ - KC).max())
    rep["D2_kernel_rows_sum_quantum"] = [float(KQ.sum(1).min()), float(KQ.sum(1).max())]
    rep["D2_pagerank_identity_maxdiff"] = float(np.abs(W.classical(s, TAU) - W.pagerank_power(s, ALPHA)).max())
    # exact exponential average against Monte Carlo over t, one seed, largest component
    c, lam, V, _, _ = max(W.spec, key=lambda x: len(x[0]))
    ex = Walks(A[np.ix_(c, c)]).quantum([0], TAU)
    psi = np.zeros(len(c)); psi[0] = 1
    for nmc in (4000, 64000):
        ts = rng.exponential(TAU, nmc)
        amp = (np.exp(-1j * np.outer(ts, lam)) * (V.T @ psi)) @ V.T
        rep[f"D2_exact_vs_montecarlo_{nmc}"] = float(np.abs((np.abs(amp) ** 2).mean(0) - ex).max())

    def go(make):
        rs = []
        for _ in range(N):
            A, parent, lab, meta = make()
            ids = [f"n{i}" for i in range(len(A))]
            rs.append(analyse(ids, A, {f"n{k}": int(v) for k, v in lab.items()}, meta, rng, rng, b, p, extras=False))
        return tally(rs)

    def fixed_hub(y_hub):
        def make_star():
            A = star(24 if y_hub is not None else 25)
            nodes = list(range(25)) if y_hub is not None else list(range(1, 26))
            v = np.array([1] * 11 + [0] * 14)
            if y_hub is None:
                rng.shuffle(v)
            else:
                rest = np.array([1] * (11 - y_hub) + [0] * (13 + y_hub)); rng.shuffle(rest)
                v = np.concatenate([[y_hub], rest])
            parent = [-1] + [0] * (len(A) - 1)
            return A, parent, dict(zip(nodes, v)), synth_meta(len(A), parent)

        def make_hub():
            A, parent, c4 = hubgraph(rng)
            cand = [i for i in range(1, len(A)) if i not in c4[1:]]
            k = 24 if y_hub is not None else 25
            nodes = sorted(rng.choice(cand, k, replace=False).tolist())
            v = np.array([1] * 11 + [0] * 14)
            if y_hub is None:
                rng.shuffle(v)
            else:
                nodes = [0] + nodes
                rest = np.array([1] * (11 - y_hub) + [0] * (13 + y_hub)); rng.shuffle(rest)
                v = np.concatenate([[y_hub], rest])
            return A, parent, dict(zip(nodes, v)), synth_meta(len(A), parent)
        return make_star, make_hub

    for nm, yh in (("hub_hit", 1), ("hub_kill", 0), ("hub_unlabelled", None)):
        ms, mh = fixed_hub(yh)
        rep[f"star_random_labels_{nm}"] = go(ms)
        rep[f"hubgraph_random_labels_{nm}"] = go(mh)
    print(json.dumps(rep, indent=1))
    return rep


def dry_run_real_topology(commit, N=1000, b=500, p=500, seed=20261104):
    """The real links and set of settled nodes; label VALUES discarded (only the counts 11/14 kept).
    Every label below is synthetic. Also the structured conditions for D4 (who can win while beating chance)."""
    ids, A, labels, _, meta = load(commit)
    nodes = sorted(labels)
    n_hit = sum(labels.values())
    del labels
    rng = np.random.default_rng(seed)
    rep = {}

    def go(make, n=N):
        return tally([analyse(ids, A, make(), meta, rng, rng, b, p, extras=False) for _ in range(n)])

    def shuffled():
        v = [1] * n_hit + [0] * (len(nodes) - n_hit)
        rng.shuffle(v)
        return dict(zip(nodes, v))

    def oe_fixed(yo):
        def make():
            rest = [1] * (n_hit - yo) + [0] * (len(nodes) - n_hit - 1 + yo)
            rng.shuffle(rest)
            others = [n for n in nodes if n != "oe"]
            return {"oe": yo, **dict(zip(others, rest))}
        return make

    def noisy(rule, flip=0.1):
        return lambda: {n: (rule(n) if rng.random() > flip else 1 - rule(n)) for n in nodes}

    rep["real_topology_shuffled"] = go(shuffled)
    rep["real_topology_shuffled_oe_hit"] = go(oe_fixed(1))
    rep["real_topology_shuffled_oe_kill"] = go(oe_fixed(0))
    par = meta["parent"]
    sib_val = {}
    def sibling_rule(n):          # siblings share a label drawn per parent; roots draw their own
        key = par[n] or n
        if key not in sib_val:
            sib_val[key] = int(rng.random() < 0.45)
        return sib_val[key]
    def sib():
        sib_val.clear()
        return {n: (sibling_rule(n) if rng.random() > 0.1 else 1 - sibling_rule(n)) for n in nodes}
    rep["real_topology_has_child_flip0.1"] = go(noisy(lambda n: int(meta["children"][n] > 0)), 300)
    rep["real_topology_depth_le1_flip0.1"] = go(noisy(lambda n: int(meta["depth"][n] <= 1)), 300)
    rep["real_topology_depth_parity_flip0.1"] = go(noisy(lambda n: meta["depth"][n] % 2), 300)
    rep["real_topology_siblings_share_flip0.1"] = go(sib, 300)
    print(json.dumps(rep, indent=1))
    return rep


def dry_run_planted(commit, N=200, b=500, p=500, seed=5):
    """D58 (em-qwalk2-1b F-A): the planted-kernel worlds behind qwalk2.md §4's last two rows, on the real links and
    settled set with the label VALUES discarded. Field world: a random normal field smoothed by one arm's kernel,
    the top 11 of 25 settled nodes called hits (then 0% or 10% flipped). Sources world: 3 random source nodes,
    the 11 settled nodes receiving most of that arm's kernel mass called hits."""
    ids, A, labels, _, meta = load(commit)
    nodes = sorted(labels)
    del labels
    idx = {n: i for i, n in enumerate(ids)}
    ni = [idx[n] for n in nodes]
    KQ, KC, _ = kernels(A)
    rng = np.random.default_rng(seed)
    rep = {}

    def field_world(K, flip):
        rs = []
        for _ in range(N):
            z = rng.normal(size=len(A))
            f = (K.T @ z)[ni]
            y = (f > np.quantile(f, 14 / 25)).astype(int)
            y = np.where(rng.random(len(y)) < flip, 1 - y, y)
            rs.append(analyse(ids, A, dict(zip(nodes, y.tolist())), meta, rng, rng, b, p, extras=False))
        return tally(rs)

    def sources_world(K, flip):
        rs = []
        for _ in range(N):
            src = rng.choice(len(A), 3, replace=False)
            f = K[src].sum(0)[ni] + 1e-9 * rng.random(len(ni))
            y = (f >= np.sort(f)[-11]).astype(int)
            y = np.where(rng.random(len(y)) < flip, 1 - y, y)
            if y.sum() < 2 or y.sum() > len(y) - 2:
                continue
            rs.append(analyse(ids, A, dict(zip(nodes, y.tolist())), meta, rng, rng, b, p, extras=False))
        return tally(rs)

    for nm, K in (("quantum", KQ), ("classical", KC)):
        for flip in (0.0, 0.1):
            rep[f"{nm}_field_flip{flip}"] = field_world(K, flip)
    for nm, K in (("quantum", KQ), ("classical", KC)):
        for flip in (0.0, 0.1):
            rep[f"{nm}_sources_flip{flip}"] = sources_world(K, flip)
    print(json.dumps(rep, indent=1))
    return rep


def null_thresholds(commit, seeds=40, p=10_000):
    """D59 (audit em-qwalk cut 3): the permutation null's pass thresholds on the real links. They depend only on the
    graph and the counts 11/14, so one shuffled labelling per seed gives them; label VALUES are discarded."""
    ids, A, labels, _, meta = load(commit)
    nodes = sorted(labels)
    n_hit = sum(labels.values())
    del labels
    KQ, KC, _ = kernels(A)
    idx = {n: i for i, n in enumerate(ids)}
    ni = [idx[n] for n in nodes]
    CQ, CC = columns(KQ, ni), columns(KC, ni)
    rows = []
    for sd in range(seeds):
        rng = np.random.default_rng(sd)
        y = np.array([1.0] * n_hit + [0.0] * (len(nodes) - n_hit))
        Yp = np.array([rng.permutation(y) for _ in range(p)])
        nq, nc = auroc_rows(scores(CQ, Yp), Yp), auroc_rows(scores(CC, Yp), Yp)
        rows.append({"seed": sd, "diff_q975": float(np.percentile(nq - nc, 97.5)), "diff_q025": float(np.percentile(nq - nc, 2.5)),
                     "quantum_q975": float(np.percentile(nq, 97.5)), "pagerank_q975": float(np.percentile(nc, 97.5)),
                     "quantum_mean": float(nq.mean()), "pagerank_mean": float(nc.mean())})
    summ = {k: {"min": min(r[k] for r in rows), "median": float(np.median([r[k] for r in rows])), "max": max(r[k] for r in rows)}
            for k in rows[0] if k != "seed"}
    from collections import Counter
    summ["diff_q975_most_common"] = Counter(round(r["diff_q975"], 3) for r in rows).most_common(3)
    print(json.dumps({"seeds": seeds, "P": p, "summary": summ}, indent=1))
    return rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--dry-run-real-topology", metavar="COMMIT")
    ap.add_argument("--dry-run-planted", metavar="COMMIT")
    ap.add_argument("--null-thresholds", metavar="COMMIT")
    ap.add_argument("--graph-counts")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--seed-bootstrap", type=int)
    ap.add_argument("--seed-permutation", type=int)
    ap.add_argument("--n", type=int, default=1000)
    a = ap.parse_args()
    if a.dry_run:
        dry_run(N=a.n)
    elif a.dry_run_real_topology:
        dry_run_real_topology(a.dry_run_real_topology, N=a.n)
    elif a.dry_run_planted:
        dry_run_planted(a.dry_run_planted)
    elif a.null_thresholds:
        null_thresholds(a.null_thresholds)
    elif a.graph_counts:
        graph_counts(a.graph_counts)
    elif a.run:
        if a.seed_bootstrap is None or a.seed_permutation is None:
            sys.exit("refused: both CURBy-derived seeds are required")
        run(a.seed_bootstrap, a.seed_permutation)
    else:
        ap.print_help()
