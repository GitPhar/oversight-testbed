"""Program 7, direction SV-12 (NOT pre-registered; parked 2026-11-05, see experiments/sv12-record-check.md): does program 1's "no single belief on Haiku" go away under Smolin and
Wilder's looser published scoring (one latent belief per statement, read through each format with its own offset and
slope, scored by held-out-format concordance)?

Archive only: program 1's six-format calls (programs/entangled-mind/results/gm3b-calls.json for Haiku; the
multi-model arms mm-gm3b-sonnet-calls.json and mm-gm3b-opus-calls.json for Sonnet and Opus, secondary). No API call,
no model, no network; standard library and numpy only (program 1's own fit needs scipy, so it is not reused).

  python3 sv_b5.py worlds [sims]   design-review check D11 on synthetic data only (no cache is read)
  python3 sv_b5.py analyse         the pre-registered statistic from the archive; writes results/sv-b5-analysis.json;
                                   refuses to start unless ledger/design-reviews/sv-b5.md says go (or fix-first confirmed)

The model (pre-registration experiments/sv-b5.md, section 4):
  latent   mu_i per statement (logit scale), prior N(0, 3^2) (program 1's PRIOR_SD)
  F1       rating 0-100: logit((v + 1) / 102) ~ N(mu, s1^2)                 (the anchor: offset 0, slope 1)
  F5       frequency /100: logit((v + 1) / 102) ~ N(a5 + b5 mu, s5^2)
  F6       verbal 7-point, index 0-6: ~ N(a6 + b6 mu, s6^2)
  F2       yes/no: P(yes) = sigmoid(a2 + b2 mu)
  F3       buy a $100 ticket at price p: P(buy) = sigmoid(a3[p] + b3 mu), one offset per price (Smolin and Wilder:
           each threshold is its own prompt)
  F4       statement vs a coin: P(statement) = sigmoid(a4[o] + b4 mu), one offset per presentation order
Held-out-format prediction (as program 1's gm3c): five folds of whole questions; for each format f and fold k the model
is fitted on even repeats with f removed for fold k's statements, so their mu comes from the other five formats; the
target is each of f's odd repeats on its own (one response per statement, as Smolin and Wilder score one response per
case), per sub-condition (price, order); the mean of the odd repeats is a secondary.
Concordance (Harrell's C): over pairs of statements whose targets differ within one sub-condition and repeat, the
share ordered the same way by mu (ties in mu count one half); a format's C is the mean over its (sub-condition, repeat)
targets with at least MIN_SIDE statements on each side of the target's median split; the headline is the mean over
the six formats (macro).
"""

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
P7 = HERE.parent                                   # programs/said-vs-did
P1 = P7.parent / "entangled-mind"                  # programs/entangled-mind
RESULTS = P7 / "results"
DATA = P7 / "data"
BET = "sv-b5"   # the id the bet would have taken; no bet sv-b5 exists (the direction was parked before pre-registration)
FORMATS = ["F1", "F2", "F3", "F4", "F5", "F6"]
NAMES = {"F1": "rating 0-100", "F2": "yes/no", "F3": "bet", "F4": "pairwise vs coin", "F5": "frequency /100",
         "F6": "verbal 7-point"}
VERBAL = ["certainly false", "very unlikely", "unlikely", "as likely as not", "likely", "very likely", "certainly true"]
GAUSS, BINARY = ("F1", "F5", "F6"), ("F2", "F3", "F4")
R = 10
PRIOR_SD = 3.0
FOLDS = 5
MIN_SIDE = 10              # a sub-condition counts if both halves of its target hold >= 10 statements
BAR = 0.85                 # Smolin and Wilder's capable-model range starts at 0.8; the map's draft bar
MARGIN = 0.10              # over the one-bit "is it SimpleQA trivia?" baseline (pattern P3), CI lower end > 0
BOOT_B, BOOT_SEED = 2000, 8009
SEED_FILE = DATA / "sv-b5-seed.json"               # the seed commit writes {"split": <seed>} (CURBy-RNG, "split")
OUT = RESULTS / "sv-b5-analysis.json"
CACHES = {"claude-haiku-5-5": P1 / "results" / "gm3b-calls.json",
          "claude-sonnet-5-5": P1 / "results" / "mm-gm3b-sonnet-calls.json",
          "claude-opus-5-5": P1 / "results" / "mm-gm3b-opus-calls.json"}


# ------------------------------------------------------------------ statements and their encoding

def statements():
    """(question id, claim index, is_trivia) for program 1's 160 chain claims, in gm3b's order."""
    split = json.loads((P1 / "experiments" / "split-exp5.json").read_text())
    cat = {r["id"]: r.get("category") for r in json.loads((P1 / "results" / "pool-run-3.json").read_text())["records"]}
    return [(q, k, cat[q] == "simpleqa") for q in split["candidates"] for k in split["chain_claims"][q]], split["candidates"]


def model_statements(model):
    """Haiku: all 160. Sonnet and Opus: program 1's 80 (items 0-9 and 20-29 of the candidate list, mm_gm3b.claims80),
    kept only if every one of their 60 calls is in the cache (Opus completed 68)."""
    st, cand = statements()
    if model != "claude-haiku-5-5":
        keep = set(cand[0:10] + cand[20:30])
        st = [s for s in st if s[0] in keep]
    return st


def stmt_first(r):
    return r % 4 in (0, 1)


def encode(conv, st):
    """Observations per format: statement index c, repeat r, response y, sub-condition g."""
    obs = {f: {"c": [], "r": [], "y": [], "g": []} for f in FORMATS}
    complete = []
    for ci, (q, k, _) in enumerate(st):
        keys = [f"{q}|{k}|{f}|{r}" for f in FORMATS for r in range(R)]
        complete.append(all(x in conv for x in keys))
    st2 = [s for s, ok in zip(st, complete) if ok]
    for ci, (q, k, _) in enumerate(st2):
        for f in FORMATS:
            for r in range(R):
                v = conv[f"{q}|{k}|{f}|{r}"]["value"]
                if f in ("F1", "F5"):
                    x = min(100, max(0, v))
                    y, g = float(np.log((x + 1) / (101 - x))), 0
                elif f == "F2":
                    y, g = float(v == "yes"), 0
                elif f == "F3":
                    y, g = float(v == "yes"), r // 2
                elif f == "F4":
                    y, g = float((v == "A") == stmt_first(r)), 0 if stmt_first(r) else 1
                else:
                    y, g = float(VERBAL.index(v)), 0
                for key, val in (("c", ci), ("r", r), ("y", y), ("g", g)):
                    obs[f][key].append(val)
    return {f: {k: np.asarray(v, float if k == "y" else int) for k, v in d.items()} for f, d in obs.items()}, st2


def subset(d, keep):
    return {k: v[keep] for k, v in d.items()}


def target_scale(f, y):
    """The response on its own scale (0-100 for F1 and F5), for the concordance targets."""
    return 102 / (1 + np.exp(-y)) - 1 if f in ("F1", "F5") else y


# ------------------------------------------------------------------ the single-latent fit (numpy, alternating Newton)

def _sig(z):
    return 1.0 / (1.0 + np.exp(-z))


def fit(obs, nc, iters=400, tol=1e-9, mu0=None):
    """Maximum a posteriori fit of mu (prior N(0, PRIOR_SD^2)) and every format's link. Returns (mu, params)."""
    mu = np.zeros(nc) if mu0 is None else mu0.copy()
    P = {}
    for f in FORMATS:
        ng = int(obs[f]["g"].max()) + 1 if len(obs[f]["g"]) else 1
        P[f] = {"a": np.zeros(ng), "b": 1.0, "s2": 1.0}
    last = -np.inf
    for it in range(iters):
        # links given mu
        for f in FORMATS:
            d = obs[f]
            if not len(d["c"]):
                continue
            m = mu[d["c"]]
            if f == "F1":
                P[f]["s2"] = max(float(np.mean((d["y"] - m) ** 2)), 1e-4)
            elif f in GAUSS:
                X = np.column_stack([np.ones(len(m)), m])
                coef = np.linalg.lstsq(X, d["y"], rcond=None)[0]
                P[f]["a"][:] = coef[0]
                P[f]["b"] = float(coef[1])
                P[f]["s2"] = max(float(np.mean((d["y"] - X @ coef) ** 2)), 1e-4)
            else:
                ng = len(P[f]["a"])
                G = np.zeros((len(m), ng))
                G[np.arange(len(m)), d["g"]] = 1.0
                X = np.column_stack([G, m])
                w = np.concatenate([P[f]["a"], [P[f]["b"]]])
                for _ in range(3):
                    p = _sig(X @ w)
                    g = X.T @ (d["y"] - p) - 1e-3 * w
                    H = (X * (p * (1 - p))[:, None]).T @ X + 1e-3 * np.eye(len(w))
                    step = np.linalg.solve(H, g)
                    nrm = float(np.max(np.abs(step)))
                    w = w + (step if nrm <= 2.0 else step * (2.0 / nrm))     # damped: at most 2 per step
                P[f]["a"], P[f]["b"] = w[:ng], float(w[ng])
        # mu given the links: Newton steps, every statement at once
        for _ in range(3):
            grad = -mu / PRIOR_SD ** 2
            hess = np.full(nc, -1.0 / PRIOR_SD ** 2)
            for f in FORMATS:
                d = obs[f]
                if not len(d["c"]):
                    continue
                a, b = P[f]["a"][d["g"]], P[f]["b"]
                eta = a + b * mu[d["c"]]
                if f in GAUSS:
                    gi, hi = b * (d["y"] - eta) / P[f]["s2"], np.full(len(eta), -b * b / P[f]["s2"])
                else:
                    p = _sig(eta)
                    gi, hi = b * (d["y"] - p), -b * b * p * (1 - p)
                np.add.at(grad, d["c"], gi)
                np.add.at(hess, d["c"], hi)
            mu = np.clip(mu - np.clip(grad / hess, -1.0, 1.0), -15.0, 15.0)   # damped: at most 1 per step
        ll = loglik(obs, mu, P)
        if abs(ll - last) < tol * max(1.0, abs(ll)):
            break
        last = ll
    return mu, P


def loglik(obs, mu, P):
    tot = -0.5 * float(np.sum(mu ** 2)) / PRIOR_SD ** 2
    for f in FORMATS:
        d = obs[f]
        if not len(d["c"]):
            continue
        eta = P[f]["a"][d["g"]] + P[f]["b"] * mu[d["c"]]
        if f in GAUSS:
            tot += float(np.sum(-0.5 * (d["y"] - eta) ** 2 / P[f]["s2"] - 0.5 * np.log(2 * np.pi * P[f]["s2"])))
        else:
            p = np.clip(_sig(eta), 1e-12, 1 - 1e-12)
            tot += float(np.sum(d["y"] * np.log(p) + (1 - d["y"]) * np.log(1 - p)))
    return tot


# ------------------------------------------------------------------ concordance

def harrell(pred, target):
    """Harrell's C over pairs with different targets; ties in pred count one half. nan if no such pair."""
    p, t = np.asarray(pred, float), np.asarray(target, float)
    dt = t[:, None] - t[None, :]
    dp = p[:, None] - p[None, :]
    use = dt > 0
    n = use.sum()
    if n == 0:
        return float("nan")
    return float(((dp > 0) & use).sum() + 0.5 * ((dp == 0) & use).sum()) / float(n)


def sub_targets(obs, f, nc, per_repeat=True):
    """The held-out targets, on the response's own scale. per_repeat=True (primary; Smolin and Wilder score one
    response per case): one target per sub-condition g and odd repeat r, the statement's single response there.
    per_repeat=False (secondary): per sub-condition, the mean of the statement's odd repeats."""
    d = obs[f]
    odd = d["r"] % 2 == 1
    out = {}
    for g in sorted(set(d["g"][odd].tolist())):
        reps = sorted(set(d["r"][odd & (d["g"] == g)].tolist())) if per_repeat else [None]
        for r in reps:
            sel = odd & (d["g"] == g) & ((d["r"] == r) if r is not None else True)
            s, n = np.zeros(nc), np.zeros(nc)
            np.add.at(s, d["c"][sel], target_scale(f, d["y"][sel]))
            np.add.at(n, d["c"][sel], 1)
            out[(g, r)] = np.where(n > 0, s / np.maximum(n, 1), np.nan)
    return out


def usable(t, idx):
    v = t[idx]
    v = v[~np.isnan(v)]
    if len(v) < 2 * MIN_SIDE:
        return False
    med = np.median(v)
    lo, hi = (v < med).sum(), (v > med).sum()
    # a binary or heavily tied target: count each side of the split, ties going to the smaller side
    lo2, hi2 = (v <= med).sum(), (v >= med).sum()
    return max(min(lo, hi2), min(lo2, hi)) >= MIN_SIDE


def format_c(score, targets, idx, orient=False):
    """Mean over usable sub-conditions of Harrell's C of `score` against the target, on the statements in idx.
    orient=True takes each sub-condition's C in its better direction (flatters a baseline on purpose)."""
    cs = []
    for g, t in targets.items():
        if not usable(t, idx):
            continue
        ok = idx[~np.isnan(t[idx])]
        c = harrell(score[ok], t[ok])
        cs.append(max(c, 1 - c) if orient else c)
    return float(np.mean(cs)) if cs else float("nan"), len(cs)


# ------------------------------------------------------------------ held-out-format prediction

def fold_assign(st, seed32):
    qs = sorted({q for q, _, _ in st})
    order = list(np.random.default_rng(seed32).permutation(qs))
    per = int(np.ceil(len(qs) / FOLDS))
    fq = {q: i // per for i, q in enumerate(order)}
    return np.array([fq[q] for q, _, _ in st]), fq


def heldout_mu(obs, nc, fold, iters=400):
    """mu_hat[f][i]: statement i's latent from the other five formats (f removed for i's fold), even repeats only."""
    even = {f: subset(d, d["r"] % 2 == 0) for f, d in obs.items()}
    full_mu, _ = fit(even, nc, iters)
    out = {}
    for f in FORMATS:
        mh = np.full(nc, np.nan)
        for k in range(FOLDS):
            test = fold == k
            if not test.any():
                continue
            mod = {ff: (subset(d, ~test[d["c"]]) if ff == f else d) for ff, d in even.items()}
            mu, _ = fit(mod, nc, iters, mu0=full_mu)
            mh[test] = mu[test]
        out[f] = mh
    return out


def scores(mu_hat, targets, trivia, idx):
    lat, bit, used = {}, {}, {}
    for f in FORMATS:
        lat[f], used[f] = format_c(mu_hat[f], targets[f], idx)
        bit[f], _ = format_c(trivia, targets[f], idx, orient=True)
    ml = float(np.nanmean(list(lat.values())))
    mb = float(np.nanmean(list(bit.values())))
    return {"macro_c": ml, "macro_c_trivia_bit": mb, "margin": ml - mb, "by_format": lat, "trivia_by_format": bit,
            "subconditions_used": used}


def analyse_model(model, seed32, boot=True):
    conv = json.loads(CACHES[model].read_text())
    st0 = model_statements(model)
    obs, st = encode(conv, st0)
    nc = len(st)
    trivia = np.array([1.0 if s[2] else 0.0 for s in st])
    fold, fq = fold_assign(st, seed32)
    mu_hat = heldout_mu(obs, nc, fold)
    targets = {f: sub_targets(obs, f, nc) for f in FORMATS}
    means = {f: sub_targets(obs, f, nc, per_repeat=False) for f in FORMATS}
    allidx = np.arange(nc)
    res = {"statements": nc, "statements_expected": len(st0), "trivia_statements": int(trivia.sum()),
           "questions": len(fq), **scores(mu_hat, targets, trivia, allidx),
           "secondary_per_statement_mean_targets": scores(mu_hat, means, trivia, allidx)}
    if boot:
        qs = sorted(fq)
        by_q = {q: [i for i, s in enumerate(st) if s[0] == q] for q in qs}
        rng = np.random.default_rng(BOOT_SEED)
        mc, mm = [], []
        for _ in range(BOOT_B):
            idx = np.array([i for q in rng.choice(qs, len(qs)) for i in by_q[q]])
            s = scores(mu_hat, targets, trivia, idx)
            mc.append(s["macro_c"])
            mm.append(s["margin"])
        res["macro_c_ci95"] = [float(np.nanpercentile(mc, 2.5)), float(np.nanpercentile(mc, 97.5))]
        res["margin_ci95"] = [float(np.nanpercentile(mm, 2.5)), float(np.nanpercentile(mm, 97.5))]
        # secondaries: within question type (P16), the card's event alone, leave-one-question-out
        res["within_type"] = {lab: scores(mu_hat, targets, trivia, np.flatnonzero(trivia == v))
                              for lab, v in (("simpleqa", 1.0), ("other_types", 0.0))}
        loo = {}
        for q in qs:
            keep = np.array([i for i in allidx if st[i][0] != q])
            s = scores(mu_hat, targets, trivia, keep)
            loo[q] = s["macro_c"]
        res["loo_question_macro_c"] = {"min": float(min(loo.values())), "max": float(max(loo.values()))}
        res["loo_flip_questions"] = sorted(q for q, v in loo.items() if (v >= BAR) != (res["macro_c"] >= BAR))
    res["passes"] = bool(res["macro_c"] >= BAR and res["margin"] >= MARGIN and res.get("margin_ci95", [0])[0] > 0)
    res["card_event_passes"] = bool(res["macro_c"] >= BAR)
    return res


def seed():
    if not SEED_FILE.exists():
        sys.exit(f"no seed yet: the seed commit writes {SEED_FILE}")
    return int(json.loads(SEED_FILE.read_text())["split"]) % 2 ** 32


def analyse(gate=True):
    """gate=False only for reproduce.py, which re-runs an analysis already gated and committed."""
    if gate:
        sys.path.insert(0, str(HERE))
        import svd_common as C
        C.review_gate(BET)       # no archive read for analysis before the design review says go (operators/design-review.md)
    s = seed()
    res = {"bet": BET, "seed32_split": s, "bar": BAR, "margin": MARGIN, "models": {}}
    for m in CACHES:
        res["models"][m] = analyse_model(m, s)
    h = res["models"]["claude-haiku-5-5"]
    res["verdict"] = "untestable" if h["statements"] < h["statements_expected"] else ("pass" if h["passes"] else "fail")
    res["card_event"] = "pass" if h["card_event_passes"] else "fail"
    OUT.write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps(res, indent=1))
    return res


# ------------------------------------------------------------------ the write-up's tables (rebuilt by reproduce.py)

BEGIN, END = "<!-- sv_b5.py report: generated from results/sv-b5-analysis.json -->", "<!-- end of generated block -->"
SHORT = {"claude-haiku-5-5": "haiku", "claude-sonnet-5-5": "sonnet", "claude-opus-5-5": "opus"}


def _f(x, nd=3, sign=False):
    return "—" if x is None or (isinstance(x, float) and np.isnan(x)) else \
        format(x, ("+" if sign else "") + f".{nd}f").replace("-", "−")


def report(res=None):
    res = res or json.loads(OUT.read_text())
    h = res["models"]["claude-haiku-5-5"]
    L = [BEGIN, "", f"**Verdict (pre-registered reading, Haiku): {res['verdict']}.** Sean's card event (C ≥ 0.85 alone): "
         f"{res['card_event']}.", "",
         "| model | statements (questions) | macro C [95% CI] | trivia-bit C | margin [95% CI] | passes the rule | "
         "C with per-statement mean targets |", "|---|---|---|---|---|---|---|"]
    for m, r in res["models"].items():
        L.append(f"| {SHORT[m]} | {r['statements']} of {r['statements_expected']} ({r['questions']}) | {_f(r['macro_c'])} "
                 f"[{_f(r['macro_c_ci95'][0])}, {_f(r['macro_c_ci95'][1])}] | {_f(r['macro_c_trivia_bit'])} | "
                 f"{_f(r['margin'], sign=True)} [{_f(r['margin_ci95'][0], sign=True)}, {_f(r['margin_ci95'][1], sign=True)}] | "
                 f"{'yes' if r['passes'] else 'no'} | {_f(r['secondary_per_statement_mean_targets']['macro_c'])} |")
    L += ["", "| model | " + " | ".join(NAMES[f] for f in FORMATS) + " |", "|---|" + "---|" * len(FORMATS)]
    for m, r in res["models"].items():
        L.append(f"| {SHORT[m]} | " + " | ".join(f"{_f(r['by_format'][f])} ({r['subconditions_used'][f]})" for f in FORMATS) + " |")
    L += ["", "Per format: Harrell's C of the latent from the other five formats (number of single-response targets "
          "counted).", "",
          "| model | within SimpleQA statements | within other statements | leave-one-question-out C (min to max) | "
          "questions whose removal flips C ≥ 0.85 |", "|---|---|---|---|---|"]
    for m, r in res["models"].items():
        w = r["within_type"]
        L.append(f"| {SHORT[m]} | {_f(w['simpleqa']['macro_c'])} | {_f(w['other_types']['macro_c'])} | "
                 f"{_f(r['loo_question_macro_c']['min'])} to {_f(r['loo_question_macro_c']['max'])} | "
                 f"{', '.join(r['loo_flip_questions']) or 'none'} |")
    L += ["", END]
    out = "\n".join(L)
    print(out)
    return out


# ------------------------------------------------------------------ dry run (D11), synthetic only

# Measured inputs, all published (programs/entangled-mind/results/gm3b-format-invariance.md, gm3c-heldout-format.md):
# 160 statements in 40 questions (21 SimpleQA), ten repeats; program 1's fitted slopes on fold 0 (F2 1.28, F3 0.56,
# F4 0.55, F5 0.94; F6 is an ordinal link there, here a Gaussian on the index, slope set to give F6's split-half
# Spearman); each format's split-half Spearman ceiling (0.88-0.98); the cross-format Spearman from the other five
# (0.41-0.76), which the "measured" world is tuned to reproduce. Not measured, so spanned: how much of a statement's
# belief its question type (trivia or not) carries.
SLOPE = {"F2": 1.28, "F3": 0.56, "F4": 0.55, "F5": 0.94, "F6": 1.2}
NOISE = {"F1": 0.45, "F5": 0.5, "F6": 0.45}          # call-to-call SD on the encoded scale
BSCALE = 2.5                                           # binary links sharpened so split-half ceilings match gm3c


def simulate(rng, tau, type_shift, n_q=40, per_q=4, n_trivia_q=21):
    """tau: SD of statement-by-format deviations from the one latent (0 = one belief); type_shift: how far trivia
    statements' latent sits below the others, and a format-specific trivia offset of the same size (P16)."""
    nc = n_q * per_q
    trivia = np.repeat((np.arange(n_q) < n_trivia_q).astype(float), per_q)
    qeff = np.repeat(rng.normal(0, 0.8, n_q), per_q)
    mu = rng.normal(0.4, 1.3, nc) + qeff - type_shift * trivia
    fmt_type = {f: rng.normal(0, type_shift / 2 + 1e-9) for f in FORMATS}
    obs = {f: {"c": [], "r": [], "y": [], "g": []} for f in FORMATS}
    prices = np.log(np.array([0.1, 0.3, 0.5, 0.7, 0.9]) / (1 - np.array([0.1, 0.3, 0.5, 0.7, 0.9])))
    for f in FORMATS:
        dev = rng.normal(0, tau, nc) + fmt_type[f] * trivia
        for r in range(R):
            for ci in range(nc):
                m = mu[ci] + dev[ci]
                if f == "F1":
                    y, g = m + rng.normal(0, NOISE["F1"]), 0
                elif f == "F5":
                    y, g = 0.3 + SLOPE["F5"] * m + rng.normal(0, NOISE["F5"]), 0
                elif f == "F6":
                    y, g = float(np.clip(np.round(3 + SLOPE["F6"] * m + rng.normal(0, NOISE["F6"])), 0, 6)), 0
                elif f == "F2":
                    y, g = float(rng.random() < _sig(0.2 + BSCALE * SLOPE["F2"] * m)), 0
                elif f == "F3":
                    g = r // 2
                    y = float(rng.random() < _sig(BSCALE * SLOPE["F3"] * (m - prices[g])))
                else:
                    g = 0 if stmt_first(r) else 1
                    y = float(rng.random() < _sig(1.0 + BSCALE * SLOPE["F4"] * m + (0.3 if g == 0 else -0.3)))
                for key, val in (("c", ci), ("r", r), ("y", y), ("g", g)):
                    obs[f][key].append(val)
    obs = {f: {k: np.asarray(v, float if k == "y" else int) for k, v in d.items()} for f, d in obs.items()}
    st = [(f"q{ci // per_q:03d}", ci % per_q, bool(trivia[ci])) for ci in range(nc)]
    return obs, st, trivia


def run_world(rng, tau, type_shift, boot_b=200):
    obs, st, trivia = simulate(rng, tau, type_shift)
    nc = len(st)
    fold, fq = fold_assign(st, int(rng.integers(2 ** 32)))
    mu_hat = heldout_mu(obs, nc, fold, iters=150)
    targets = {f: sub_targets(obs, f, nc) for f in FORMATS}
    means = {f: sub_targets(obs, f, nc, per_repeat=False) for f in FORMATS}
    s = scores(mu_hat, targets, trivia, np.arange(nc))
    qs = sorted(fq)
    by_q = {q: [i for i, x in enumerate(st) if x[0] == q] for q in qs}
    mm = []
    for _ in range(boot_b):
        idx = np.array([i for q in rng.choice(qs, len(qs)) for i in by_q[q]])
        mm.append(scores(mu_hat, targets, trivia, idx)["margin"])
    lo = float(np.nanpercentile(mm, 2.5))
    # the cross-format Spearman, per format, to compare with gm3c's published 0.41-0.76
    sp = {}
    for f in FORMATS:
        t = np.nanmean(np.vstack(list(means[f].values())), axis=0)
        a = np.argsort(np.argsort(mu_hat[f]))
        b = np.argsort(np.argsort(t))
        sp[f] = float(np.corrcoef(a, b)[0, 1])
    passes = bool(s["macro_c"] >= BAR and s["margin"] >= MARGIN and lo > 0)
    return passes, s["macro_c"], s["macro_c_trivia_bit"], sp


WORLDS = {"one belief (tau 0)": 0.0, "small deviations (tau 0.5)": 0.5, "measured (tau 1.0)": 1.0,
          "large deviations (tau 1.5)": 1.5}
TYPE = {"type carries little": 0.3, "type carries a lot": 1.2}


def worlds(sims=30, seed=13):
    rng = np.random.default_rng(seed)
    out = {}
    for wn, tau in WORLDS.items():
        for tn, ts in TYPE.items():
            res = [run_world(rng, tau, ts) for _ in range(sims)]
            key = f"{wn}; {tn}"
            out[key] = {"P(pass)": float(np.mean([r[0] for r in res])), "P(fail)": float(1 - np.mean([r[0] for r in res])),
                        "mean macro C": float(np.mean([r[1] for r in res])),
                        "mean trivia-bit macro C": float(np.mean([r[2] for r in res])),
                        "mean cross-format Spearman by format": {f: round(float(np.mean([r[3][f] for r in res])), 2)
                                                                 for f in FORMATS}}
            print(key, json.dumps(out[key]), flush=True)
    print(json.dumps({"bet": BET, "sims": sims, "worlds": out}, indent=1))
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "worlds":
        worlds(int(a[1]) if len(a) > 1 else 30)
    elif a[0] == "analyse":
        analyse()
    elif a[0] == "report":
        report()
    else:
        sys.exit(__doc__)
