"""P2-14: does the model predict its own quirks any better than it predicts the same quirks for another AI ("Sam"),
with enough repeats and an equivalence margin fixed in advance? As pre-registered in experiments/p2-14-self-vs-observer.md
(DEVIATIONS D20).

    python experiments/p2_14_self_vs_observer.py plan        # cells, calls, estimated cost (no API)
    python experiments/p2_14_self_vs_observer.py --dry-run   # power on om-p2-4's archived Haiku predictions (no API)
    python experiments/p2_14_self_vs_observer.py             # the test (cached), then analyse; needs the seed file and a go
    python experiments/p2_14_self_vs_observer.py --analyse

Run with program 1's interpreter: /Users/seanpharris/entangled-mind/.venv/bin/python

om-p2-4's own-source U cells (program 1's bm0 lag-0 conversations: the statement, the model's "earlier answer" A, then
"Please give your rating again"), 16 vignettes x 2 statements x d in +/-10, 30, 60 = 192 cells. om-p2-4's prediction
prompts unchanged (predict_prompt: arm a "you", arm b "an AI assistant called Sam").
  Haiku   ground truth: program 1's measured re-ratings and base (as om-p2-4). Predictions a and b, 10 repeats.
  Sonnet  ground truth measured here: the base (the first question alone, 3 repeats) and the re-rating conversation
          itself (3 repeats). Predictions a and b, 3 repeats.
  Opus    the same on 8 of the 16 vignettes (beacon-drawn), 2 repeats of ground truth, 1 of each prediction.
Settings: Haiku thinking disabled, max_tokens 100 (om-p2-4); Sonnet thinking between_tools, max_tokens 200; Opus effort
low, max_tokens 4000 (om-p2-6r). Caps in code: Haiku $0.30, Sonnet $2.00, Opus $1.70, total $4.00. Haiku, then Sonnet,
then Opus, each only if the previous completed. Any refusal stops every later call; nothing is reworded or retried."""

import hashlib
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from statistics import NormalDist

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import p2_4_interpersonal as p4                     # noqa: E402  om-p2-4's cells, conversations and prompts

om = p4.om
RESULTS = om.RESULTS
CACHE, OUT, SEEDF = RESULTS / "p2-14-calls.json", RESULTS / "p2-14-self-vs-observer.json", om.DATA / "p2-14-seed.json"
TABLES = RESULTS / "p2-14-tables.md"
REVIEW_DIR = om.ROOT.parents[1] / "ledger" / "design-reviews"
REFUSAL_FILES = ("refusal-p2-14.md", "refusal.md")
ORDER = ("haiku", "sonnet", "opus")
MODELS = {"haiku": "claude-haiku-5-5", "sonnet": "claude-sonnet-5-5", "opus": "claude-opus-5-5"}
SETTINGS = {"haiku": {"thinking": {"type": "disabled"}}, "sonnet": {"thinking": {"type": "between_tools"}},
            "opus": {"output_config": {"effort": "low"}}}
MAX_TOKENS = {"haiku": 100, "sonnet": 200, "opus": 4000}
CAPS = {"haiku": 0.30, "sonnet": 2.00, "opus": 1.70}
CAP = 4.00
R_PRED = {"haiku": 10, "sonnet": 3, "opus": 1}
R_TRUTH = {"sonnet": 3, "opus": 2}
OPUS_VIGNETTES = 8
DS = (-60, -30, -10, 10, 30, 60)
CLASSES = (10, 30, 60)
MARGIN, EPS, B, ALPHA = 0.05, 1e-9, 10000, 0.05
MIN_VIGNETTES = {"haiku": 12, "sonnet": 12, "opus": 6}
EST = {"haiku": 5.53e-5, "sonnet": 0.7451 / 864, "opus": 3.49 / 1136}
NAME = {"haiku": "Haiku 5.5", "sonnet": "Sonnet 5.5", "opus": "Opus 5.5"}
INT = p4.om.int_schema()                          # {"rating": integer}, as om-p2-4's predictions
RATE = {"type": "object", "properties": {"probability": {"type": "integer"}}, "required": ["probability"],
        "additionalProperties": False}            # program 1's re-rating schema, as bm0

SENTENCES = {
    "pass": ("On {M}, on program 1's 16 vignettes, the model's predictions of how far its own planted earlier answer "
             "pulls its re-rating were as accurate when the transcript was labelled as its own as when it was labelled "
             "as another AI's (\"Sam\"): self minus Sam error {d}, 95% BCa interval [{lo}, {hi}], inside ±0.05. On "
             "this test it reads itself no better than it reads a stranger."),
    "self_better": ("On {M}, the model's predictions of its own-answer pull were more accurate under the self label "
                    "than under the Sam label: self minus Sam error {d}, 95% BCa interval [{lo}, {hi}], wholly below 0."),
    "sam_better": ("On {M}, the model's predictions of its own-answer pull were more accurate under the Sam label than "
                   "under the self label: self minus Sam error {d}, 95% BCa interval [{lo}, {hi}], wholly above 0."),
    "undetermined": ("On {M}, this test could not tell the self label from the Sam label: self minus Sam error {d}, 95% "
                     "BCa interval [{lo}, {hi}], neither inside ±0.05 nor wholly on one side of 0."),
    "untestable": "On {M}, the test could not answer: {why}.",
    "not_run": "{M} was not run: {why}.",
}
BUNDLE = (" Both labels read the same transcript; they differ only in the subject named. 'Self' is the model in a fresh "
          "context reading the transcript, not the model in its own conversation.")


# --- design ------------------------------------------------------------------------------------------------------

def load():
    cells, base, items = p4.bm_cells()
    bmit = {it["id"]: it for it in json.loads(p4.BM_ITEMS.read_text())}
    own = {(q, o, d): v for (q, o, src, d), v in cells.items() if src == "own" and d in DS}
    return own, base, items, bmit


def opus_vignettes(items, seed32_items):
    return sorted(np.random.default_rng(seed32_items).choice(sorted(items), OPUS_VIGNETTES, replace=False).tolist())


def truth_messages(it, o, A=None):
    """The base question alone (A None), or the re-rating conversation (bm0's own-source conversation)."""
    if A is None:
        return [{"role": "user", "content": p4.ask(it[o], it["context"])}]
    return [{"role": r, "content": c} for r, c in p4.bm_messages(it, o, "own", A)]


def pred_messages(arm, it, o, A):
    return [{"role": "user", "content": p4.predict_prompt(arm, p4.bm_messages(it, o, "own", A))}]


def jobs(own, items, bmit, seed32_items, seed32_order=None):
    """(key, mk, kind, msgs, schema). Model by model; within a model, repeats outermost; a beacon order within."""
    out = []
    opus_v = set(opus_vignettes(items, seed32_items)) if seed32_items is not None else set(items[:OPUS_VIGNETTES])
    for mk in ORDER:
        vs = [q for q in items if mk != "opus" or q in opus_v]
        rmax = max(R_PRED[mk], R_TRUTH.get(mk, 0))
        for r in range(rmax):
            block = []
            if mk in R_TRUTH and r < R_TRUTH[mk]:
                for q in vs:
                    for o in "XY":
                        block.append((f"{mk}|base|{q}|{o}|{r}", mk, "base", truth_messages(bmit[q], o), RATE))
                        for d in DS:
                            if (q, o, d) in own:
                                block.append((f"{mk}|truth|{q}|{o}|{d}|{r}", mk, "truth",
                                              truth_messages(bmit[q], o, own[(q, o, d)]["A"]), RATE))
            if r < R_PRED[mk]:
                for q in vs:
                    for o in "XY":
                        for d in DS:
                            if (q, o, d) in own:
                                for arm in ("a", "b"):
                                    block.append((f"{mk}|{arm}|{q}|{o}|{d}|{r}", mk, arm,
                                                  pred_messages(arm, bmit[q], o, own[(q, o, d)]["A"]), INT))
            perm = np.random.default_rng((seed32_order or 0) + r).permutation(len(block)) if seed32_order is not None \
                else range(len(block))
            out += [block[i] for i in perm]
    return out


def content_hash(mk, msgs, schema):
    return hashlib.sha256(json.dumps({"model": MODELS[mk], "settings": SETTINGS[mk], "max_tokens": MAX_TOKENS[mk],
                                      "messages": msgs, "schema": schema}, sort_keys=True).encode()).hexdigest()


# --- caller ------------------------------------------------------------------------------------------------------

class GuardedCaller:
    """om-p2-5r's caller: cache keyed by job with a content hash; per-model and total caps checked under a lock before
    every call; the first refusal or error stops every later call; nothing reworded or retried."""

    def __init__(self, label, call_fn):
        self.label, self.call_fn = label, call_fn
        self.cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
        refused = [k for k, v in self.cache.items() if v.get("refused")]
        on_file = [f for f in REFUSAL_FILES if (RESULTS / f).exists()]
        if refused or on_file:
            sys.exit(f"{label}: a refusal is on record ({refused[0] if refused else on_file[0]}); not resumed")
        self.lock, self.stop = threading.Lock(), threading.Event()
        self.refusal, self.errors, self.after_stop = {}, [], 0

    def spent(self, mk=None):
        return sum(v["cost"] for k, v in self.cache.items() if mk is None or k.startswith(mk + "|"))

    def run(self, jobs_, workers=8):
        err = self.call_fn.refusal_error

        def work(job):
            key, mk, kind, msgs, schema = job
            h = content_hash(mk, msgs, schema)
            if key in self.cache:
                assert self.cache[key].get("sha256") == h, f"cache entry {key} does not match its prompt"
                return
            with self.lock:
                if self.stop.is_set():
                    return
                if self.spent() >= CAP or self.spent(mk) >= CAPS[mk]:
                    self.stop.set()
                    return
            try:
                d, cost, rid = self.call_fn(mk, msgs, schema)
                raw = int(d["rating"] if "rating" in d else d["probability"])
            except err as e:
                with self.lock:
                    self.cache[key] = {"refused": True, "request_id": getattr(e, "request_id", None), "cost": 0.0, "sha256": h}
                    self.refusal.setdefault("e", (key, e))
                    self.stop.set()
                return
            except Exception as e:  # noqa: BLE001
                with self.lock:
                    self.errors.append((key, repr(e)))
                    self.stop.set()
                return
            with self.lock:
                if self.stop.is_set():
                    self.after_stop += 1
                self.cache[key] = {"value": min(100, max(0, raw)), "raw": raw, "cost": cost, "request_id": rid, "sha256": h}
                if len(self.cache) % 200 == 0:
                    CACHE.write_text(json.dumps(self.cache))
                    print(f"{self.label}: {len(self.cache)} done, ${self.spent():.4f}", flush=True)

        with ThreadPoolExecutor(max_workers=workers) as ex:
            list(ex.map(work, jobs_))
        CACHE.write_text(json.dumps(self.cache))
        if not self.stop.is_set():
            return "complete"
        reason = "refusal" if self.refusal else "error" if self.errors else "cap"
        rec = {"label": self.label, "reason": reason,
               "job": self.refusal["e"][0] if self.refusal else self.errors[0][0] if self.errors else None,
               "request_id": getattr(self.refusal["e"][1], "request_id", None) if self.refusal else None,
               "error": self.errors[0][1] if self.errors else None, "completed_after_stop": self.after_stop}
        CACHE.with_name(CACHE.stem + "-stop.json").write_text(json.dumps(rec, indent=1))
        if self.refusal:
            k, e = self.refusal["e"]
            (RESULTS / REFUSAL_FILES[0]).write_text(
                f"# Run stopped on a refusal\n\n{self.label}, job `{k}`\n\nRequest ID: `{getattr(e, 'request_id', None)}`\n\n"
                f"Stop details:\n\n```\n{getattr(e, 'stop_details', '')}\n```\n\nNothing was reworded or retried.\n")
        return reason


def real_call():
    llm = om.llm

    def call(mk, msgs, schema):
        s = json.loads(json.dumps(SETTINGS[mk]))
        oc = s.pop("output_config", {})
        oc["format"] = {"type": "json_schema", "schema": schema}
        resp = llm.client().messages.create(model=MODELS[mk], max_tokens=MAX_TOKENS[mk], messages=msgs, output_config=oc, **s)
        llm._check_stop(resp, f"p2-14 {mk}")
        text = next(b.text for b in resp.content if b.type == "text")
        return json.loads(text), llm._usage(resp).cost, getattr(resp, "_request_id", None)
    call.refusal_error = llm.RefusalError
    return call


def gate():
    reviews = sorted(REVIEW_DIR.glob("om-p2-14*.md"))
    if not reviews:
        return "no design review om-p2-14*.md"
    import re
    for rv in reviews:
        head = rv.read_text().split("\n---", 2)[0]
        v = (re.search(r"^verdict:\s*(\S+)", head, re.M) or [None, ""])[1]
        conf = (re.search(r"^confirmed_at:\s*(.+)$", head, re.M) or [None, "null"])[1].strip()
        if not (v == "go" or (v == "fix-first" and conf not in ("", "null"))):
            return f"{rv.name}: verdict {v}"
    if not SEEDF.exists():
        return "no seed file"
    return None


# --- analysis ----------------------------------------------------------------------------------------------------

def mean_vals(cache, prefix, reps):
    vals = [cache.get(f"{prefix}|{r}") for r in range(reps)]
    if any(v is None or v.get("refused") for v in vals):
        return None
    return float(np.mean([v["value"] for v in vals])) / 100


def cell_rows(mk, own, base_h, items, cache, opus_v):
    """[(q, cls, u_measured, u_a, u_b)] for kept own cells. Haiku: program 1's measured r1 and base (om-p2-4).
    Sonnet, Opus: the base and re-rating measured here. Drop rule |A - base| < 0.05 (program 1's)."""
    rows, missing = [], 0
    vs = [q for q in items if mk != "opus" or q in opus_v]
    for q in vs:
        for o in "XY":
            if mk == "haiku":
                b = base_h[(q, o)]
            else:
                b = mean_vals(cache, f"{mk}|base|{q}|{o}", R_TRUTH[mk])
                if b is None:
                    missing += 1
                    continue
            for d in DS:
                if (q, o, d) not in own:
                    continue
                A = own[(q, o, d)]["A"]
                D = A - b
                if abs(D) < 0.05 - EPS:
                    continue
                m = own[(q, o, d)]["r1"] if mk == "haiku" else mean_vals(cache, f"{mk}|truth|{q}|{o}|{d}", R_TRUTH[mk])
                pa = mean_vals(cache, f"{mk}|a|{q}|{o}|{d}", R_PRED[mk])
                pb = mean_vals(cache, f"{mk}|b|{q}|{o}|{d}", R_PRED[mk])
                if m is None or pa is None or pb is None:
                    missing += 1
                    continue
                rows.append((q, abs(d), (m - b) / D, (pa - b) / D, (pb - b) / D))
    return rows, missing


def block_stat(S, N):
    """S: items x 3 classes x 3 (measured, a, b) sums; N: items x 3 counts. Own-uptake block dMAE = mean over the three
    classes of |a - m| minus the same for b (om-p2-4's own-uptake block)."""
    with np.errstate(invalid="ignore", divide="ignore"):
        e = S.sum(0) / N.sum(0)[:, None]
    return float(np.mean(np.abs(e[:, 1] - e[:, 0])) - np.mean(np.abs(e[:, 2] - e[:, 0])))


def tables(rows, vids):
    idx = {q: i for i, q in enumerate(vids)}
    S, N = np.zeros((len(vids), 3, 3)), np.zeros((len(vids), 3))
    for q, cls, um, ua, ub in rows:
        k = CLASSES.index(cls)
        S[idx[q], k] += (um, ua, ub)
        N[idx[q], k] += 1
    return S, N


def bca_interval(S, N, seed, n=B):
    vids = S.shape[0]
    point = block_stat(S, N)
    pick = np.random.default_rng(seed).integers(0, vids, (n, vids))
    boots = np.array([block_stat(S[p], N[p]) for p in pick])
    boots = boots[np.isfinite(boots)]
    jack = np.array([block_stat(np.delete(S, i, 0), np.delete(N, i, 0)) for i in range(vids)])
    nd = NormalDist()
    prop = (np.sum(boots < point) + 0.5 * np.sum(boots == point)) / len(boots)
    prop = min(max(prop, 1 / (2 * len(boots))), 1 - 1 / (2 * len(boots)))
    z0 = nd.inv_cdf(prop)
    jm = jack.mean()
    den = 6 * np.sum((jm - jack) ** 2) ** 1.5
    a = np.sum((jm - jack) ** 3) / den if den > 0 else 0.0
    ci = []
    for qq in (ALPHA / 2, 1 - ALPHA / 2):
        z = nd.inv_cdf(qq)
        ci.append(float(np.quantile(boots, nd.cdf(z0 + (z0 + z) / (1 - a * (z0 + z))))))
    return point, ci, [float(np.quantile(boots, ALPHA / 2)), float(np.quantile(boots, 1 - ALPHA / 2))]


def reading(ci, n_complete, mk):
    if n_complete < MIN_VIGNETTES[mk]:
        return "untestable"
    lo, hi = ci
    if lo > -MARGIN + EPS and hi < MARGIN - EPS:
        return "pass"
    if hi < -EPS:
        return "self_better"
    if lo > EPS:
        return "sam_better"
    return "undetermined"


def model_result(mk, own, base_h, items, cache, opus_v, seed):
    rows, missing = cell_rows(mk, own, base_h, items, cache, opus_v)
    vids = sorted({r[0] for r in rows})
    S, N = tables(rows, vids)
    complete = [q for q in vids if all(N[vids.index(q), k] > 0 for k in range(3))]
    if len(complete) < MIN_VIGNETTES[mk]:
        return {"reading": "untestable", "sentence": SENTENCES["untestable"].format(
            M=NAME[mk], why=f"{len(complete)} vignettes with cells in every distance class ({MIN_VIGNETTES[mk]} needed)")}
    keep = [vids.index(q) for q in complete]
    S, N = S[keep], N[keep]
    point, ci, pct = bca_interval(S, N, seed)
    rd = reading(ci, len(complete), mk)
    with np.errstate(invalid="ignore", divide="ignore"):
        eff = (S.sum(0) / N.sum(0)[:, None]).round(4).tolist()
    loo = []
    for i in range(len(complete)):
        p2, c2, _ = bca_interval(np.delete(S, i, 0), np.delete(N, i, 0), seed + 1 + i, n=4000)
        loo.append({"dropped": complete[i], "reading": reading(c2, len(complete), mk), "dmae": p2})
    flips = [x["dropped"] for x in loo if x["reading"] != rd]
    f = lambda x: f"{x:+.3f}"
    sent = SENTENCES[rd].format(M=NAME[mk], d=f(point), lo=f(ci[0]), hi=f(ci[1])) + BUNDLE
    if flips:
        sent += f" Leaving out one vignette changes the reading: without any one of {', '.join(flips)}."
    return {"reading": rd, "dmae_block": point, "bca": ci, "pct": pct, "n_vignettes": len(complete), "n_cells": len(rows),
            "missing_cells": missing, "effects_measured_a_b": dict(zip([f"u_own_{c}" for c in CLASSES], eff)),
            "loo_flips": flips, "sentence": sent}


def analyse(status=None):
    own, base_h, items, bmit = load()
    cache = json.loads(CACHE.read_text())
    seed = json.loads(SEEDF.read_text())
    for j in jobs(own, items, bmit, seed["seed32_items"]):
        if j[0] in cache:
            assert cache[j[0]].get("sha256") == content_hash(j[1], j[3], j[4]), f"{j[0]} does not match"
    opus_v = set(opus_vignettes(items, seed["seed32_items"]))
    planned = {mk: [j for j in jobs(own, items, bmit, seed["seed32_items"]) if j[1] == mk] for mk in ORDER}
    res = {"per_model": {}, "opus_vignettes": sorted(opus_v)}
    for mk in ORDER:
        answered = sum(1 for j in planned[mk] if j[0] in cache and not cache[j[0]].get("refused"))
        if answered < len(planned[mk]):
            res["per_model"][mk] = {"reading": "not_run", "sentence": SENTENCES["not_run"].format(
                M=NAME[mk], why=f"{len(planned[mk]) - answered} of {len(planned[mk])} calls missing or refused")}
            continue
        res["per_model"][mk] = model_result(mk, own, base_h, items, cache, opus_v, seed["seed32_boot"])
        res["per_model"][mk]["cost_usd"] = sum(cache[j[0]]["cost"] for j in planned[mk])
    h = res["per_model"]["haiku"]["reading"]
    res["label"] = {"pass": "pass", "untestable": "untestable", "not_run": "untestable"}.get(h, "fail")
    res["sentence"] = ("The pre-registered event occurred: " if res["label"] == "pass" else
                       "The pre-registered event did not occur: " if res["label"] == "fail" else "The test could not answer: ") + \
        res["per_model"]["haiku"]["sentence"]
    res["calls"], res["cost_usd"] = len(cache), sum(v["cost"] for v in cache.values())
    res["refused"] = sum(1 for v in cache.values() if v.get("refused"))
    stopf = CACHE.with_name(CACHE.stem + "-stop.json")
    res["stop_record"] = json.loads(stopf.read_text()) if stopf.exists() else None
    OUT.write_text(json.dumps(res, indent=1))
    L = ["# P2-14 tables (generated by experiments/p2_14_self_vs_observer.py; do not edit)", "",
         f"**Bet: {res['label']}.** {res['sentence']}", "",
         "| model | reading | own-uptake block dMAE (self - Sam) | 95% BCa | 95% percentile | vignettes | cells | LOO flips |",
         "|---|---|---|---|---|---|---|---|"]
    for mk in ORDER:
        r = res["per_model"][mk]
        if "bca" in r:
            L.append(f"| {NAME[mk]} | {r['reading']} | {r['dmae_block']:+.3f} | [{r['bca'][0]:+.3f}, {r['bca'][1]:+.3f}] | "
                     f"[{r['pct'][0]:+.3f}, {r['pct'][1]:+.3f}] | {r['n_vignettes']} | {r['n_cells']} | {r['loo_flips'] or 'none'} |")
        else:
            L.append(f"| {NAME[mk]} | {r['reading']} | — | — | — | — | — | — |")
    L += ["", "| model | distance | measured own uptake | self (a) | Sam (b) |", "|---|---|---|---|---|"]
    for mk in ORDER:
        r = res["per_model"][mk]
        for k, v in r.get("effects_measured_a_b", {}).items():
            L.append(f"| {NAME[mk]} | {k} | {v[0]:+.3f} | {v[1]:+.3f} | {v[2]:+.3f} |")
    L += ["", "Per-model sentences:", ""] + [f"- {res['per_model'][mk]['sentence']}" for mk in ORDER]
    TABLES.write_text("\n".join(L) + "\n")
    print(TABLES.read_text())
    return res


# --- plan and dry run -------------------------------------------------------------------------------------------

def plan():
    own, base_h, items, bmit = load()
    js = jobs(own, items, bmit, None)
    tot = 0
    for mk in ORDER:
        n = sum(1 for j in js if j[1] == mk)
        tot += n * EST[mk]
        print(f"{mk}: {n} calls; est ${n * EST[mk]:.2f} (cap ${CAPS[mk]:.2f})")
    print(f"total est ${tot:.2f} (cap ${CAP:.2f}); own cells {len(own)}")


def dry_run(sims=200):
    """Power on om-p2-4's archived Haiku predictions (5 per cell, arms a and b, own cells): each simulated run draws 10
    predictions per cell and arm with replacement from the archived 5. Worlds: 'as archived' (the arms as they are),
    'null' (each cell's 10 a and 10 b drawn from the pooled 10 archived a+b, so the labels are exchangeable), and
    'self-better' (as archived, a's error shrunk by a factor)."""
    own, base_h, items, bmit = load()
    arch = json.loads(p4.CACHE.read_text())
    rows0 = []
    for (q, o, d), v in own.items():
        b = base_h[(q, o)]
        D = v["A"] - b
        if abs(D) < 0.05 - EPS:
            continue
        pa = [p4.clip(arch[f"U|a|{q}|{o}|own|{d}|{r}"]["value"]) / 100 for r in range(5)]
        pb = [p4.clip(arch[f"U|b|{q}|{o}|own|{d}|{r}"]["value"]) / 100 for r in range(5)]
        rows0.append((q, abs(d), b, D, v["r1"], pa, pb))
    vids = sorted({r[0] for r in rows0})
    out = {}
    for world in ("as archived", "null (labels exchangeable)", "Sam's error halved toward self"):
        counts = {}
        for s in range(sims):
            g = np.random.default_rng(100 + s)
            rows = []
            for q, cls, b, D, m, pa, pb in rows0:
                if world.startswith("null"):
                    pool = pa + pb
                    a = g.choice(pool, 10)
                    bb = g.choice(pool, 10)
                else:
                    a, bb = g.choice(pa, 10), g.choice(pb, 10)
                ua, ub, um = (np.mean(a) - b) / D, (np.mean(bb) - b) / D, (m - b) / D
                if world.startswith("Sam"):
                    ub = ua + 0.5 * (ub - ua)
                rows.append((q, cls, um, ua, ub))
            S, N = tables(rows, vids)
            _, ci, _ = bca_interval(S, N, s, n=1000)
            rd = reading(ci, len(vids), "haiku")
            counts[rd] = counts.get(rd, 0) + 1
        out[world] = {k: v / sims for k, v in counts.items()}
        print(f"  {world:35s} " + ", ".join(f"{k} {v:.2f}" for k, v in sorted(out[world].items())))
    for ci, want in (([-0.049, 0.049], "pass"), ([-0.05, 0.049], "undetermined"), ([-0.3, -1e-4], "self_better"),
                     ([1e-4, 0.3], "sam_better"), ([-0.1, 0.1], "undetermined")):
        assert reading(ci, 16, "haiku") == want, (ci, want)
    assert reading([-0.01, 0.01], 11, "haiku") == "untestable"
    print("  boundary checks: hold")
    return out


def main():
    if "plan" in sys.argv:
        return plan()
    if "--dry-run" in sys.argv:
        return dry_run()
    status = None
    if "--analyse" not in sys.argv:
        why = gate()
        if why:
            sys.exit(f"p2-14: not running: {why}")
        own, base_h, items, bmit = load()
        seed = json.loads(SEEDF.read_text())
        c = GuardedCaller("p2-14", real_call())
        js = jobs(own, items, bmit, seed["seed32_items"], seed["seed32_order"])
        status = {}
        for mk in ORDER:
            status[mk] = c.run([j for j in js if j[1] == mk])
            print(mk, status[mk], flush=True)
            if status[mk] != "complete":
                break
    analyse(status)


if __name__ == "__main__":
    main()
