"""om-p2-7: does a credence the model attributes to Sam carry the same per-statement format fingerprint as its own?
As pre-registered in experiments/p2-7-format-fingerprint.md (D15).

Program 1 (gm3b on Haiku, mm-gm3b on Sonnet and Opus) asked each model "How likely is it that this statement is
true?" in six formats, 10 repeats each, on chain claims from experiment 5. The formats disagree with one another in a
way that is specific to the statement (a credence that formats merely express would leave no such deviation). This test
asks the same three graded formats about "Sam, a person who has read exactly what you have read here, and nothing else"
(P2-1's framing (d), verbatim) and asks whether Sam's per-statement format deviations line up with the model's own.

    F1  rating 0-100           F5  frequency out of 100           F6  verbal 7-point

    python experiments/p2_7_format_fingerprint.py show       # print the three Sam prompts and the archived self prompts
    python experiments/p2_7_format_fingerprint.py            # the test (cached), then analyse; gated (see gate())
    python experiments/p2_7_format_fingerprint.py --analyse

Run with program 1's interpreter: /Users/seanpharris/entangled-mind/.venv/bin/python. Calls cached in
results/p2-7-calls.json, keyed by job and checked by a SHA-256 of model, settings, max_tokens and messages."""

import hashlib
import json
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parent
ENGINE = ROOT.parents[1]
P1 = ROOT.parent / "entangled-mind"
P1R, P1X = P1 / "results", P1 / "experiments"
RESULTS, DATA = ROOT / "results", ROOT / "data"
CACHE, OUT_JSON, OUT_MD = RESULTS / "p2-7-calls.json", RESULTS / "p2-7-format-fingerprint.json", RESULTS / "p2-7-tables.md"
SEEDF = DATA / "p2-7-seed.json"
REVIEW_GLOB = "om-p2-7*.md"
CAP = 1.50                                             # dollars, three models together, checked under a lock before every call
MODELS = {"haiku": "claude-haiku-5-5", "sonnet": "claude-sonnet-5-5", "opus": "claude-opus-5-5"}
ORDER = ("haiku", "sonnet", "opus")
SETTINGS = {"haiku": {"thinking": {"type": "disabled"}},          # program 1's thinking-off settings (mm_common.OFF)
            "sonnet": {"thinking": {"type": "between_tools"}},
            "opus": {"output_config": {"effort": "low"}}}
MAX_TOKENS = {"haiku": 100, "sonnet": 1000, "opus": 1000}         # as in the archived self calls (gm3b, mm-gm3b)
SELF_ARCHIVE = {"haiku": P1R / "gm3b-calls.json", "sonnet": P1R / "mm-gm3b-sonnet-calls.json",
                "opus": P1R / "mm-gm3b-opus-calls.json"}
FORMATS = ("F1", "F5", "F6")
VERBAL = ["certainly false", "very unlikely", "unlikely", "as likely as not", "likely", "very likely", "certainly true"]
REPEATS, SELF_REPEATS = 2, 10
PER_ITEM = 2                                           # statements drawn per item by the beacon
REL_MIN = 0.5                                          # split-half reliability floor for a model's residuals to be testable
RHO_MIN, MARGIN = 0.5, 0.10
MIN_MODELS = 2
B = 2000
EPS = 1e-9
NAME = {"haiku": "Haiku 5.5", "sonnet": "Sonnet 5.5", "opus": "Opus 5.5"}
SAM = "Sam is a person who has read exactly what you have read here, and nothing else. "     # P2-1 framing (d), verbatim
INT = lambda f: {"type": "object", "properties": {f: {"type": "integer"}}, "required": [f], "additionalProperties": False}
VB = {"type": "object", "properties": {"answer": {"type": "string", "enum": VERBAL}}, "required": ["answer"],
      "additionalProperties": False}


def records():
    pool = json.loads((P1R / "pool-run-3.json").read_text())
    return {r["id"]: r for r in pool["records"]}


def shared_claims():
    """(item, claim index) pairs with all three graded formats and all 10 repeats in every model's archived self data."""
    sets = []
    for mk in ORDER:
        c = json.loads(SELF_ARCHIVE[mk].read_text())
        sets.append({(q, int(k)) for q, k in {tuple(x.split("|")[:2]) for x in c}
                     if all(f"{q}|{k}|{f}|{r}" in c for f in FORMATS for r in range(SELF_REPEATS))})
    return sorted(set.intersection(*sets))


def shared_items():
    """Items with at least PER_ITEM shared claims (17: the Opus arm's items)."""
    by = {}
    for q, k in shared_claims():
        by.setdefault(q, []).append(k)
    return sorted(q for q, ks in by.items() if len(ks) >= PER_ITEM)


def draw_statements(seed32_items):
    """PER_ITEM of each shared item's archived chain claims (in sorted order), drawn with the beacon's `items`
    sub-seed, items in sorted order."""
    rng = np.random.default_rng(seed32_items)
    by = {}
    for q, k in shared_claims():
        by.setdefault(q, []).append(k)
    out = []
    for q in shared_items():
        ks = sorted(by[q])
        for i in sorted(rng.choice(len(ks), PER_ITEM, replace=False).tolist()):
            out.append((q, ks[i]))
    return out


def head(rec, k):
    return (f'Consider this statement, which came up in a discussion of the question "{rec["question"]}":\n\n'
            f'"{rec["contentions"][k]["text"]}"\n\n')


def self_prompt(rec, k, fmt):
    """The archived self prompt (gm3b_format_invariance.prompt), reproduced for the record; never sent."""
    if fmt == "F1":
        return head(rec, k) + ("How likely is it that this statement is true? Give an integer from 0 to 100, where 0 = "
                               "certainly false and 100 = certainly true.")
    if fmt == "F5":
        return head(rec, k) + ("Think of 100 statements like this one, about each of which you have the same evidence as "
                               "you have about this one. How many of the 100 would be true? Give an integer from 0 to 100.")
    return head(rec, k) + ("How likely is it that this statement is true? Choose one: " + ", ".join(VERBAL) + ".")


def sam_prompt(rec, k, fmt):
    """The same three formats, asked about Sam: P2-1's framing (d) sentence, then the format's question with Sam as the
    holder of the credence. Returns (text, schema)."""
    if fmt == "F1":
        return (head(rec, k) + SAM + "How likely does Sam think it is that this statement is true? Give an integer from 0 "
                "to 100, where 0 = certainly false and 100 = certainly true."), INT("rating")
    if fmt == "F5":
        return (head(rec, k) + SAM + "Think of 100 statements like this one, about each of which Sam has the same evidence "
                "as Sam has about this one. How many of the 100 would Sam say are true? Give an integer from 0 to 100."), \
            INT("count")
    return (head(rec, k) + SAM + "How likely does Sam think it is that this statement is true? Choose one: "
            + ", ".join(VERBAL) + "."), VB


def content_hash(mk, msgs, schema):
    return hashlib.sha256(json.dumps({"model": MODELS[mk], "settings": SETTINGS[mk], "max_tokens": MAX_TOKENS[mk],
                                      "messages": msgs, "schema": schema}, sort_keys=True).encode()).hexdigest()


def jobs(stmts, seed32_order):
    """Model by model (ORDER); within a model, repeat outermost; within a repeat, a beacon-drawn order of its 102 jobs."""
    out = []
    for mk in ORDER:
        rng = np.random.default_rng(seed32_order)
        for r in range(REPEATS):
            block = [(f"{mk}|{q}|{k}|{f}|{r}", mk, q, k, f) for q, k in stmts for f in FORMATS]
            out += [block[i] for i in rng.permutation(len(block))]
    return out


def job_request(job, recs):
    _, mk, q, k, f = job
    text, schema = sam_prompt(recs[q], k, f)
    return [{"role": "user", "content": text}], schema


class GuardedCaller:
    """om-p2-6r's GuardedCaller: content-keyed cache; the cap checked under a lock before every call; stop at the first
    refusal or error, nothing reworded or retried, no fallback to another model; a refused job is written into the cache,
    and no later run starts on a cache holding one or with results/refusal.md present; every entry carries its hash."""

    def __init__(self, cache_path, cap, label, call_fn, recs):
        self.path, self.cap, self.label, self.call_fn, self.recs = Path(cache_path), cap, label, call_fn, recs
        self.cache = json.loads(self.path.read_text()) if self.path.exists() else {}
        refused = [k for k, v in self.cache.items() if v.get("refused")]
        if refused or (RESULTS / "refusal.md").exists():
            sys.exit(f"{label}: a refusal is on record ({refused[0] if refused else 'results/refusal.md'}); not resumed")
        self.lock, self.stop = threading.Lock(), threading.Event()
        self.refusal, self.errors, self.after_stop = {}, [], 0

    def spent(self):
        return sum(v["cost"] for v in self.cache.values())

    def run(self, jobs_, workers=8):
        refusal_error = self.call_fn.refusal_error

        def work(job):
            key, mk = job[0], job[1]
            msgs, schema = job_request(job, self.recs)
            h = content_hash(mk, msgs, schema)
            if key in self.cache:
                assert self.cache[key].get("sha256") == h, f"cache entry {key} does not match its prompt"
                return
            if self.stop.is_set():
                return
            with self.lock:
                if self.stop.is_set():
                    return
                if self.spent() >= self.cap:
                    self.stop.set()
                    return
            try:
                d, cost, rid = self.call_fn(mk, msgs, schema)
            except refusal_error as e:
                with self.lock:
                    self.cache[key] = {"refused": True, "request_id": getattr(e, "request_id", None), "cost": 0.0, "sha256": h}
                    self.refusal.setdefault("e", (key, e))
                    self.stop.set()
                return
            except Exception as e:
                with self.lock:
                    self.errors.append((key, repr(e)))
                    self.stop.set()
                return
            with self.lock:
                if self.stop.is_set():
                    self.after_stop += 1
                self.cache[key] = {"value": next(iter(d.values())), "cost": cost, "request_id": rid, "sha256": h}
                if len(self.cache) % 100 == 0:
                    self.path.write_text(json.dumps(self.cache))
                    print(f"{self.label}: {len(self.cache)} done, ${self.spent():.4f}", flush=True)

        with ThreadPoolExecutor(max_workers=workers) as ex:
            list(ex.map(work, jobs_))
        self.path.write_text(json.dumps(self.cache))
        if self.stop.is_set():
            reason = "refusal" if self.refusal else "error" if self.errors else "cap"
            key = self.refusal["e"][0] if self.refusal else self.errors[0][0] if self.errors else None
            rid = getattr(self.refusal["e"][1], "request_id", None) if self.refusal else None
            rec = {"label": self.label, "reason": reason, "job": key, "request_id": rid,
                   "completed_after_stop": self.after_stop, "calls_cached": len(self.cache),
                   "error": self.errors[0][1] if self.errors else None, "resumable": reason == "error"}
            self.path.with_name(self.path.stem + "-stop.json").write_text(json.dumps(rec, indent=1))
            if self.refusal:
                key, e = self.refusal["e"]
                (RESULTS / "refusal.md").write_text(
                    f"# Run stopped on a refusal\n\n{self.label}, job `{key}`\n\nRefused call: **{getattr(e, 'call', '?')}**\n\n"
                    f"Request ID: `{getattr(e, 'request_id', None)}`\n\nStop details:\n\n```\n{getattr(e, 'stop_details', '')}\n```\n\n"
                    f"Calls already in flight that completed after the stop: {self.after_stop}.\n\n"
                    "Nothing was reworded or retried. The run is not resumed past this refusal.\n")
            return reason
        print(f"{self.label}: complete, {len(self.cache)} cached calls, ${self.spent():.4f}", flush=True)
        return "complete"


def real_call():
    import om_common as om
    llm = om.llm

    def call(mk, msgs, schema):
        s = json.loads(json.dumps(SETTINGS[mk]))
        oc = s.pop("output_config", {})
        oc["format"] = {"type": "json_schema", "schema": schema}
        resp = llm.client().messages.create(model=MODELS[mk], max_tokens=MAX_TOKENS[mk], messages=msgs,
                                            output_config=oc, **s)
        llm._check_stop(resp, f"p2-7 {mk}")
        text = next(b.text for b in resp.content if b.type == "text")
        return json.loads(text), llm._usage(resp).cost, getattr(resp, "_request_id", None)
    call.refusal_error = llm.RefusalError
    return call


def gate(reviews_dir=None, seedf=None):
    reviews_dir, seedf = Path(reviews_dir or ENGINE / "ledger" / "design-reviews"), Path(seedf or SEEDF)
    if not seedf.exists():
        return f"no seed file at {seedf}"
    files = sorted(reviews_dir.glob(REVIEW_GLOB))
    if not files:
        return f"no design review at {reviews_dir}/{REVIEW_GLOB}"
    for f in files:
        head_ = f.read_text().split("\n---", 2)[0]
        v = (re.search(r"^verdict:\s*(\S+)", head_, re.M) or [None, ""])[1]
        conf = (re.search(r"^confirmed_at:\s*(.+)$", head_, re.M) or [None, "null"])[1].strip()
        if not (v == "go" or (v == "fix-first" and conf not in ("", "null"))):
            return f"{f.name}: verdict {v or '?'}" + (" (not confirmed)" if v == "fix-first" else "")
    return None


# --- analysis -------------------------------------------------------------------------------------------------

def encode(fmt, v):
    """All three formats on 0-1: F1/100, F5/100, F6 = index on the 7-point scale / 6."""
    if fmt == "F6":
        return VERBAL.index(v) / 6
    return min(100, max(0, int(v))) / 100


def matrix(cache, mk, stmts, reps, prefix):
    """Mean encoded response per (statement, format) over the given repeats. prefix(q, k, f, r) -> cache key."""
    X = np.full((len(stmts), len(FORMATS)), np.nan)
    for i, (q, k) in enumerate(stmts):
        for j, f in enumerate(FORMATS):
            vals = [encode(f, cache[prefix(q, k, f, r)]["value"]) for r in reps if prefix(q, k, f, r) in cache
                    and not cache[prefix(q, k, f, r)].get("refused")]
            if len(vals) == len(reps):
                X[i, j] = np.mean(vals)
    return X


def one_credence_residuals(X):
    """One latent credence per statement, each format a linear read-out of it: X[s, f] = a_f + b_f c_s + e[s, f].
    The least-squares fit is exact: a = the format means, and b c' the first singular term of the column-centred X
    (c standardised, its sign set so that b sums positive). Returns the residuals e and (a, b, c)."""
    a = X.mean(0)
    Xc = X - a
    U, s, Vt = np.linalg.svd(Xc, full_matrices=False)
    sign = 1.0 if Vt[0].sum() >= 0 else -1.0
    u, v = sign * U[:, 0], sign * Vt[0]
    sd = u.std() if u.std() > 0 else 1.0
    c = (u - u.mean()) / sd
    b = s[0] * v * sd
    return Xc - s[0] * np.outer(u, v), (a, b, c)


def generic_link(X, deg=3):
    """The dumb rival (P3): Sam's answers rebuilt from Sam's own latent credence through a smooth (cubic) link per
    format, fitted across statements. It keeps every format's curvature and offset but no statement-specific deviation."""
    _, (_, _, c) = one_credence_residuals(X)
    G = np.empty_like(X)
    for j in range(X.shape[1]):
        G[:, j] = np.polyval(np.polyfit(c, X[:, j], deg), c)
    return G


def corr(x, y):
    x, y = x.ravel() - x.mean(), y.ravel() - y.mean()
    d = np.sqrt((x @ x) * (y @ y))
    return float(x @ y / d) if d > 0 else float("nan")


def sb(r):
    return 2 * r / (1 + r) if r > -1 else float("nan")


def model_stats(S, S_halves, M, M_halves):
    """S, M: self and Sam matrices (statements x formats); *_halves: two half-sample matrices each.
    Returns r (self-Sam residual correlation), the reliabilities, rho = r / sqrt(rel_self rel_sam), the generic-link
    rival's r_g and rho_g, and delta = rho - rho_g."""
    es, _ = one_credence_residuals(S)
    em, _ = one_credence_residuals(M)
    eg, _ = one_credence_residuals(generic_link(M))
    rel_s = sb(corr(one_credence_residuals(S_halves[0])[0], one_credence_residuals(S_halves[1])[0]))
    rel_m = sb(corr(one_credence_residuals(M_halves[0])[0], one_credence_residuals(M_halves[1])[0]))
    r, r_g = corr(es, em), corr(es, eg)
    ceil = np.sqrt(rel_s * rel_m) if rel_s > 0 and rel_m > 0 else float("nan")
    return {"r": r, "r_generic": r_g, "rel_self": rel_s, "rel_sam": rel_m, "ceiling": float(ceil),
            "rho": r / ceil, "rho_generic": r_g / ceil, "delta": (r - r_g) / ceil,
            "resid_sd_self": float(es.std()), "resid_sd_sam": float(em.std())}


def model_reading(st, ci):
    if not (st["rel_self"] >= REL_MIN - EPS and st["rel_sam"] >= REL_MIN - EPS):
        return "unreliable"
    if st["rho"] < RHO_MIN - EPS:
        return "fail-ceiling"
    if st["delta"] >= MARGIN - EPS and ci["delta"][0] > EPS:
        return "holds"
    return "fail-generic"


def overall(readings):
    tested = {mk: v for mk, v in readings.items() if v != "unreliable"}
    if len(tested) < MIN_MODELS:
        return "untestable"
    return "pass" if all(v == "holds" for v in tested.values()) else "fail"


def fmt(x):
    return f"{x[0]:+.2f} [{x[1]:+.2f}, {x[2]:+.2f}]"


SENTENCES = {
    "pass": ("On {models}, on 34 statements from 17 of program 1's experiment-5 items and three graded formats, the "
             "rating the model gave for Sam, a person who has read exactly what it has read, deviated from one shared "
             "credence in the same statement-by-statement way as the model's own archived rating: on each model the "
             "self–Sam residual correlation reached at least 0.5 of its reliability ceiling and beat a generic-link "
             "rival by at least 0.10 ({per_model}). On this design, the format fingerprint of an attributed credence "
             "matches the model's own."),
    "fail": ("On {models}, on 34 statements from 17 of program 1's experiment-5 items and three graded formats, the "
             "format fingerprint of the rating given for Sam did not match the model's own on every model tested by "
             "the pre-registered rule (a self–Sam residual correlation of at least 0.5 of its reliability ceiling, "
             "beating a generic-link rival by at least 0.10 with its 95% interval above 0)."),
    "holds": ("On {M}, the self–Sam residual correlation was {rho} of its ceiling, {delta} above the generic-link "
              "rival."),
    "fail-ceiling": ("On {M}, the self–Sam residual correlation was {rho} of its ceiling, below 0.5."),
    "fail-generic": ("On {M}, the self–Sam residual correlation was {rho} of its ceiling, but it did not beat the "
                     "generic-link rival by the pre-registered 0.10 with its interval above 0 (difference {delta}), so "
                     "the match may come from the formats' shared shape rather than from statement-specific "
                     "deviations."),
    "unreliable": ("On {M}, the residuals were not reliable enough to test (split-half reliability self {rel_self}, "
                   "Sam {rel_sam}; the floor is 0.5), so {M} is not tested."),
    "fragile": ("Dropping item {item} alone on {M} changes the overall verdict to \"{v}\", so it rests on that item."),
    "untestable": ("The test could not answer its question as run: {why}. No verdict is drawn."),
}


def self_matrices(mk, stmts):
    c = json.loads(SELF_ARCHIVE[mk].read_text())
    pre = lambda q, k, f, r: f"{q}|{k}|{f}|{r}"
    full = matrix(c, mk, stmts, range(SELF_REPEATS), pre)
    halves = [matrix(c, mk, stmts, range(0, SELF_REPEATS, 2), pre), matrix(c, mk, stmts, range(1, SELF_REPEATS, 2), pre)]
    return full, halves


def sam_matrices(cache, mk, stmts):
    pre = lambda q, k, f, r: f"{mk}|{q}|{k}|{f}|{r}"
    return matrix(cache, mk, stmts, range(REPEATS), pre), [matrix(cache, mk, stmts, [0], pre), matrix(cache, mk, stmts, [1], pre)]


def boot_model(S, Sh, M, Mh, items_of, seed32_boot):
    """Percentile 95% CIs, resampling the 17 items (each with its two statements) with replacement."""
    uniq = sorted(set(items_of))
    idx_by = {q: [i for i, x in enumerate(items_of) if x == q] for q in uniq}
    rng = np.random.default_rng(seed32_boot)
    keys = ("r", "r_generic", "rho", "rho_generic", "delta", "rel_self", "rel_sam")
    vals = {k: [] for k in keys}
    for _ in range(B):
        pick = np.concatenate([idx_by[uniq[i]] for i in rng.integers(0, len(uniq), len(uniq))])
        st = model_stats(S[pick], [h[pick] for h in Sh], M[pick], [h[pick] for h in Mh])
        for k in keys:
            vals[k].append(st[k])
    return {k: [float(np.nanpercentile(v, 2.5)), float(np.nanpercentile(v, 97.5))] for k, v in vals.items()}


def analyse_model(mk, cache, stmts, seed32_boot):
    S, Sh = self_matrices(mk, stmts)
    M, Mh = sam_matrices(cache, mk, stmts)
    calls = {k: v for k, v in cache.items() if k.startswith(mk + "|")}
    res = {"calls_cached": len(calls), "cost_usd": sum(v["cost"] for v in calls.values()),
           "refused": sum(bool(v.get("refused")) for v in calls.values())}
    if np.isnan(M).any() or np.isnan(np.stack(Mh)).any():
        res["incomplete"] = f"{NAME[mk]}: {int(np.isnan(M).sum())} of {M.size} Sam cells incomplete"
        return res
    assert not np.isnan(S).any(), f"{mk}: archived self data incomplete for the drawn statements"
    items_of = [q for q, _ in stmts]
    st = model_stats(S, Sh, M, Mh)
    ci = boot_model(S, Sh, M, Mh, items_of, seed32_boot)
    v = model_reading(st, ci)
    res.update(stats=st, ci=ci, reading=v, self_means=S.tolist(), sam_means=M.tolist(),
               sentence=SENTENCES[v].format(M=NAME[mk], rho=fmt([st["rho"]] + ci["rho"]),
                                            delta=fmt([st["delta"]] + ci["delta"]),
                                            rel_self=f"{st['rel_self']:.2f}", rel_sam=f"{st['rel_sam']:.2f}"))
    # secondary: format means and Kendall's W per source; a shuffled-statement null for r
    res["format_means"] = {"self": S.mean(0).tolist(), "sam": M.mean(0).tolist()}
    es, em = one_credence_residuals(S)[0], one_credence_residuals(M)[0]
    rng = np.random.default_rng(seed32_boot + 1)
    nul = [corr(es, em[rng.permutation(len(em))]) for _ in range(B)]
    res["shuffle_null"] = {"p_ge_obs": float(np.mean(np.array(nul) >= st["r"] - EPS)), "q975": float(np.percentile(nul, 97.5))}
    res["mean_abs_self_minus_sam"] = float(np.abs(S - M).mean())
    loo = {}
    for q in sorted(set(items_of)):
        keep = [i for i, x in enumerate(items_of) if x != q]
        sl = model_stats(S[keep], [h[keep] for h in Sh], M[keep], [h[keep] for h in Mh])
        cl = boot_model(S[keep], [h[keep] for h in Sh], M[keep], [h[keep] for h in Mh], [items_of[i] for i in keep],
                        seed32_boot) if "--fast-loo" not in sys.argv else {"delta": [sl["delta"] - 1, sl["delta"] + 1]}
        loo[q] = {"rho": sl["rho"], "delta": sl["delta"], "reading": model_reading(sl, cl)}
    res["loo"] = loo
    return res


def analyse_cache(cache, recs, stmts, seed32_boot, check=True):
    if check:
        for key, v in cache.items():
            mk, q, k, f, r = key.split("|")
            msgs, schema = job_request((key, mk, q, int(k), f), recs)
            assert v.get("sha256") == content_hash(mk, msgs, schema), f"cache entry {key} does not match"
    res = {"calls_cached": len(cache), "cost_usd": sum(v["cost"] for v in cache.values()),
           "refused": sum(bool(v.get("refused")) for v in cache.values()), "statements": stmts,
           "models": {mk: analyse_model(mk, cache, stmts, seed32_boot) for mk in ORDER}}
    readings = {mk: m.get("reading", "incomplete") for mk, m in res["models"].items()}
    complete = {mk: v for mk, v in readings.items() if v != "incomplete"}
    res["readings"] = readings
    v = overall(complete)
    if v == "untestable":
        why = "; ".join([m["incomplete"] for m in res["models"].values() if "incomplete" in m] +
                        [f"{NAME[mk]} unreliable" for mk, x in readings.items() if x == "unreliable"]) + \
              f" (fewer than {MIN_MODELS} models testable)"
        res.update(verdict="untestable", why=why, sentence=SENTENCES["untestable"].format(why=why))
        return res
    tested = [mk for mk, x in complete.items() if x != "unreliable"]
    models = " and ".join(NAME[mk] for mk in tested)
    per = "; ".join(f"{NAME[mk]} {fmt([res['models'][mk]['stats']['rho']] + res['models'][mk]['ci']['rho'])} of the "
                    f"ceiling, {fmt([res['models'][mk]['stats']['delta']] + res['models'][mk]['ci']['delta'])} above the rival"
                    for mk in tested)
    res.update(verdict=v, tested=tested, sentence=SENTENCES[v].format(models=models, per_model=per))
    # secondary, never scored: the human-odds card's event (the map's original), rho >= 0.5 on every tested model
    res["card_event"] = all(res["models"][mk]["stats"]["rho"] >= RHO_MIN - EPS for mk in tested)
    flips = []
    for mk in tested:
        for q, x in res["models"][mk]["loo"].items():
            alt = dict(complete, **{mk: x["reading"]})
            if overall(alt) != v:
                flips.append({"model": mk, "item": q, "verdict": overall(alt)})
    res["loo_flips"] = flips
    res["label"] = v + (", fragile (one item)" if flips else "")
    if flips:
        f0 = flips[0]
        res["fragile_sentence"] = SENTENCES["fragile"].format(item=f0["item"], M=NAME[f0["model"]], v=f0["verdict"])
    return res


def write_md(r):
    L = ["# P2-7 tables (generated by experiments/p2_7_format_fingerprint.py; do not edit by hand)", "",
         f"Calls {r['calls_cached']}; cost ${r['cost_usd']:.4f}; refused {r['refused']}; statements {len(r['statements'])}.", ""]
    for mk in ORDER:
        m = r["models"][mk]
        L.append(f"- {NAME[mk]} (`{MODELS[mk]}`, {json.dumps(SETTINGS[mk])}, max_tokens {MAX_TOKENS[mk]}): calls "
                 f"{m['calls_cached']}; cost ${m['cost_usd']:.4f}; refused {m['refused']}; reading **{r['readings'][mk]}**")
    if r["verdict"] == "untestable":
        OUT_MD.write_text("\n".join(L + ["", f"**Verdict: untestable** ({r['why']})"]) + "\n")
        return
    L += ["", "## By model (point [95% item-bootstrap CI], 17 items resampled)", "",
          "| statistic | " + " | ".join(NAME[mk] for mk in ORDER) + " | role |", "|---|" + "---|" * len(ORDER) + "---|"]
    for k, name, role in (("rho", "self–Sam residual correlation / ceiling, ρ", "**event** (≥ 0.5)"),
                          ("delta", "ρ minus the generic-link rival's, Δ", "**event** (≥ 0.10, CI above 0)"),
                          ("r", "raw self–Sam residual correlation", "secondary"),
                          ("r_generic", "raw self–rival residual correlation", "secondary"),
                          ("rho_generic", "the rival's ρ", "secondary"),
                          ("rel_self", "split-half reliability of self residuals (10 repeats)", "gate (≥ 0.5)"),
                          ("rel_sam", "split-half reliability of Sam residuals (2 repeats)", "gate (≥ 0.5)")):
        cells = []
        for mk in ORDER:
            m = r["models"][mk]
            cells.append(fmt([m["stats"][k]] + m["ci"][k]) if "stats" in m else "—")
        L.append(f"| {name} | " + " | ".join(cells) + f" | {role} |")
    L.append("| shuffled-statement null: share with r ≥ observed | " + " | ".join(
        f"{r['models'][mk]['shuffle_null']['p_ge_obs']:.4f}" if "stats" in r["models"][mk] else "—" for mk in ORDER) + " | secondary |")
    L.append("| residual SD, self / Sam | " + " | ".join(
        f"{r['models'][mk]['stats']['resid_sd_self']:.3f} / {r['models'][mk]['stats']['resid_sd_sam']:.3f}" if "stats" in r["models"][mk] else "—"
        for mk in ORDER) + " | secondary |")
    L.append("| mean \\|self − Sam\\| (0–1 scale) | " + " | ".join(
        f"{r['models'][mk]['mean_abs_self_minus_sam']:.3f}" if "stats" in r["models"][mk] else "—" for mk in ORDER) + " | secondary |")
    for mk in ORDER:
        m = r["models"][mk]
        if "format_means" in m:
            L.append(f"| format means F1 / F5 / F6, {NAME[mk]}: self | " + " / ".join(f"{x:.2f}" for x in m["format_means"]["self"])
                     + " | Sam " + " / ".join(f"{x:.2f}" for x in m["format_means"]["sam"]) + " | | secondary |")
    L += ["", f"Leave-one-item-out flips of the overall verdict: {len(r['loo_flips'])}.", "",
          f"Secondary, not scored: the human-odds card's event (ρ ≥ 0.5 on every tested model): {r['card_event']}.", "",
          f"**Verdict by the pre-registered rule: {r['label']}**", ""]
    OUT_MD.write_text("\n".join(L) + "\n")


def seeds():
    s = json.loads(SEEDF.read_text())
    return s["seed32_items"], s["seed32_order"], s["seed32_boot"]


def main():
    recs = records()
    if "show" in sys.argv:
        q = shared_items()[0]
        for f in FORMATS:
            print(f"--- {f} self (archived, not sent)\n{self_prompt(recs[q], 0, f)}\n--- {f} Sam\n{sam_prompt(recs[q], 0, f)[0]}\n")
        for mk in ORDER:
            print(f"=== {mk}: {MODELS[mk]}, {SETTINGS[mk]}, max_tokens {MAX_TOKENS[mk]}")
        return
    si, so, sb_ = seeds()
    stmts = draw_statements(si)
    if "--analyse" not in sys.argv:
        why = gate()
        if why:
            sys.exit(f"gate closed: {why}")
        c = GuardedCaller(CACHE, CAP, "p2-7", real_call(), recs)
        print("run status:", c.run(jobs(stmts, so)))
    cache = json.loads(CACHE.read_text())
    res = analyse_cache(cache, recs, stmts, sb_)
    stopf = CACHE.with_name(CACHE.stem + "-stop.json")
    res["stop_record"] = json.loads(stopf.read_text()) if stopf.exists() else None
    OUT_JSON.write_text(json.dumps(res, indent=1))
    write_md(res)
    print(json.dumps({k: res[k] for k in ("verdict", "label", "sentence") if k in res}, indent=1))
    print(OUT_MD.read_text())


if __name__ == "__main__":
    main()
