"""om-p2-6r: does P2-6's position-over-label result hold on Sonnet 5.5 and Opus 5.5? As pre-registered in
experiments/p2-6r-replication.md (D14).

On Haiku (om-p2-6, audited, stands), a value in the assistant turn was taken up more than the same value in the user
turn, by +0.23 [+0.13, +0.34] of the displacement, while the label ("your" / "Sam's") changed uptake by +0.08. This
script runs the same 16 items at +/-30, the same four 2 x 2 cells and the no-value baseline, with P2-6's prompt
builders imported unchanged (the fifth, user's-own cell is dropped for budget), on two more models:

    claude-sonnet-5-5   thinking {"type": "between_tools"} (Sonnet 5.5 rejects "disabled"; program 1's thinking-off)
    claude-opus-5-5     output_config effort "low" (Opus 5.5 cannot turn thinking off; program 1's setting)

    python experiments/p2_6r_replication.py show        # print one conversation per cell and the call settings
    python experiments/p2_6r_replication.py             # the test (cached), then analyse; gated (see gate())
    python experiments/p2_6r_replication.py --analyse

Run with program 1's interpreter: /Users/seanpharris/entangled-mind/.venv/bin/python. Calls cached in
results/p2-6r-calls.json, keyed by job and checked by a SHA-256 of model, settings, max_tokens and messages."""

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
import p2_6_position_label as base  # noqa: E402  (P2-6's items, anchors, shown_value and messages, unchanged)

ROOT = HERE.parent
ENGINE = ROOT.parents[1]
RESULTS, DATA = ROOT / "results", ROOT / "data"
CACHE, OUT_JSON, OUT_MD = RESULTS / "p2-6r-calls.json", RESULTS / "p2-6r-replication.json", RESULTS / "p2-6r-tables.md"
SEEDF = DATA / "p2-6r-seed.json"
REVIEW_GLOB = "om-p2-6r*.md"
HAIKU_JSON = RESULTS / "p2-6-position-or-label.json"
CAP = 4.00                                             # dollars, both models together, checked under a lock before every call
MODELS = {"sonnet": "claude-sonnet-5-5", "opus": "claude-opus-5-5"}
ORDER = ("sonnet", "opus")                             # Sonnet runs first, then Opus
SETTINGS = {"sonnet": {"thinking": {"type": "between_tools"}},
            "opus": {"output_config": {"effort": "low"}}}
MAX_TOKENS = {"sonnet": 200, "opus": 4000}             # Opus's thinking counts toward max_tokens
REPEATS = {"sonnet": 3, "opus": 2}
DISTANCES = (-30, 30)
MIN_D = 0.05
MARGIN = 0.15
MIN_ITEMS = 12
B = 2000
EPS = 1e-9
CELLS = ("AY", "AS", "UY", "US")
NAME = {"sonnet": "Sonnet 5.5", "opus": "Opus 5.5"}


def content_hash(model_key, msgs):
    return hashlib.sha256(json.dumps({"model": MODELS[model_key], "settings": SETTINGS[model_key],
                                      "max_tokens": MAX_TOKENS[model_key], "messages": msgs},
                                     sort_keys=True).encode()).hexdigest()


def jobs(its, anc, seed32_order):
    """Model by model (ORDER); within a model, repeat index outermost, so a stop leaves whole repeats; within a
    repeat, a beacon-drawn order of its 288 jobs (the same permutation for both models)."""
    out = []
    for mk in ORDER:
        rng = np.random.default_rng(seed32_order)
        for r in range(REPEATS[mk]):
            block = []
            for it in its:
                for o in ("X", "Y"):
                    block.append((f"{mk}|base|{it['id']}|{o}|0|{r}", mk, "base", it, o, None))
                    for d in DISTANCES:
                        A = base.shown_value(anc[it["id"]][f"m_{o}"], d)
                        for c in CELLS:
                            block.append((f"{mk}|{c}|{it['id']}|{o}|{d}|{r}", mk, c, it, o, A))
            out += [block[i] for i in rng.permutation(len(block))]
    return out


def job_messages(job):
    _, _, cell, it, o, A = job
    return base.messages(cell, it, o, A)


class GuardedCaller:
    """P2-6's GuardedCaller (D9, D11e) with the model in the job: content-keyed cache; the cap checked under a lock
    before every call; stop at the first refusal or error, nothing reworded or retried; a refused job is written into
    the cache, and no later run starts on a cache holding one or with results/refusal.md present; calls finishing
    after the stop are counted; every entry carries content_hash, asserted on every hit."""

    def __init__(self, cache_path, cap, label, call_fn):
        self.path, self.cap, self.label, self.call_fn = Path(cache_path), cap, label, call_fn
        self.cache = json.loads(self.path.read_text()) if self.path.exists() else {}
        refused = [k for k, v in self.cache.items() if v.get("refused")]
        if refused or (RESULTS / "refusal.md").exists():
            sys.exit(f"{label}: a refusal is on record ({refused[0] if refused else 'results/refusal.md'}); not resumed")
        self.lock, self.stop = threading.Lock(), threading.Event()
        self.refusal, self.errors, self.after_stop, self.capped = {}, [], 0, False

    def spent(self):
        return sum(v["cost"] for v in self.cache.values())

    def run(self, jobs_, workers=8):
        refusal_error = self.call_fn.refusal_error

        def work(job):
            key, mk = job[0], job[1]
            msgs = job_messages(job)
            h = content_hash(mk, msgs)
            if key in self.cache:
                assert self.cache[key].get("sha256") == h, f"cache entry {key} does not match its prompt"
                return
            if self.stop.is_set():
                return
            with self.lock:
                if self.stop.is_set():
                    return
                if self.spent() >= self.cap:
                    self.capped = True
                    self.stop.set()
                    return
            try:
                d, cost, rid = self.call_fn(mk, msgs)
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
                self.cache[key] = {"value": min(100, max(0, int(d["probability"]))), "raw": int(d["probability"]),
                                   "cost": cost, "request_id": rid, "sha256": h}
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


RATE = base.RATE


def real_call():
    import om_common as om
    llm = om.llm

    def call(mk, msgs):
        s = json.loads(json.dumps(SETTINGS[mk]))
        oc = s.pop("output_config", {})
        oc["format"] = {"type": "json_schema", "schema": RATE}
        resp = llm.client().messages.create(model=MODELS[mk], max_tokens=MAX_TOKENS[mk], messages=msgs,
                                            output_config=oc, **s)
        llm._check_stop(resp, f"p2-6r {mk}")          # raises RefusalError on a refusal, RuntimeError on max_tokens
        text = next(b.text for b in resp.content if b.type == "text")
        return json.loads(text), llm._usage(resp).cost, getattr(resp, "_request_id", None)
    call.refusal_error = llm.RefusalError
    return call


def gate(reviews_dir=None, seedf=None):
    """No call before every design review of om-p2-6r says go (or a confirmed fix-first) and the seed file exists."""
    reviews_dir, seedf = Path(reviews_dir or ENGINE / "ledger" / "design-reviews"), Path(seedf or SEEDF)
    if not seedf.exists():
        return f"no seed file at {seedf}"
    files = sorted(reviews_dir.glob(REVIEW_GLOB))
    if not files:
        return f"no design review at {reviews_dir}/{REVIEW_GLOB}"
    for f in files:
        head = f.read_text().split("\n---", 2)[0]
        v = (re.search(r"^verdict:\s*(\S+)", head, re.M) or [None, ""])[1]
        conf = (re.search(r"^confirmed_at:\s*(.+)$", head, re.M) or [None, "null"])[1].strip()
        if not (v == "go" or (v == "fix-first" and conf not in ("", "null"))):
            return f"{f.name}: verdict {v or '?'}" + (" (not confirmed)" if v == "fix-first" else "")
    return None


# --- analysis -------------------------------------------------------------------------------------------------

def verify_cache(its, anc, cache):
    by = {it["id"]: it for it in its}
    for key, v in cache.items():
        mk, cell, q, o, d, _ = key.split("|")
        A = None if cell == "base" else base.shown_value(anc[q][f"m_{o}"], int(d))
        assert v.get("sha256") == content_hash(mk, base.messages(cell, by[q], o, A)), f"cache entry {key} does not match"


def complete_repeats(mk, its, cache):
    n = 0
    for r in range(REPEATS[mk]):
        keys = [f"{mk}|base|{it['id']}|{o}|0|{r}" for it in its for o in "XY"] + \
               [f"{mk}|{c}|{it['id']}|{o}|{d}|{r}" for it in its for o in "XY" for d in DISTANCES for c in CELLS]
        if all(k in cache and not cache[k].get("refused") for k in keys):
            n += 1
        else:
            break
    return n


def item_uptakes(mk, its, anc, cache, nrep):
    """P2-6's two uptake measures (§4 and D11d), per item and cell, on the first nrep complete repeats.
    Frozen: sum over kept (statement, direction) pairs of the shift toward the shown value / sum of |D|.
    Shift-invariant: sum over statements kept in both directions of (r(+30) - r(-30)) / (A(+30) - A(-30))."""
    out, out_s, kept, dropped = {}, {}, 0, 0
    for it in its:
        q = it["id"]
        num, den = {c: 0.0 for c in CELLS}, 0.0
        num_s, den_s = {c: 0.0 for c in CELLS}, 0.0
        for o in "XY":
            b = np.mean([cache[f"{mk}|base|{q}|{o}|0|{r}"]["value"] for r in range(nrep)]) / 100
            rb, As, ok = {}, {}, {}
            for d in DISTANCES:
                A = base.shown_value(anc[q][f"m_{o}"], d) / 100
                D = A - b
                ok[d], As[d] = abs(D) >= MIN_D, A
                rb[d] = {c: np.mean([cache[f"{mk}|{c}|{q}|{o}|{d}|{r}"]["value"] for r in range(nrep)]) / 100 for c in CELLS}
                if not ok[d]:
                    dropped += 1
                    continue
                kept += 1
                den += abs(D)
                for c in CELLS:
                    num[c] += (rb[d][c] - b) * np.sign(D)
            if all(ok.values()):
                den_s += As[30] - As[-30]
                for c in CELLS:
                    num_s[c] += rb[30][c] - rb[-30][c]
        if den > 0:
            out[q] = {c: num[c] / den for c in CELLS}
        if den_s > 0:
            out_s[q] = {c: num_s[c] / den_s for c in CELLS}
    return out, out_s, kept, dropped


def contrasts(U):
    AY, AS, UY, US = (U[:, i] for i in range(4))
    return {"L": ((AY - AS) + (UY - US)) / 2, "P": ((AY - UY) + (AS - US)) / 2,
            "L_A": AY - AS, "L_U": UY - US, "I": (AY - AS) - (UY - US),
            "P_minus_L": ((AY - UY) + (AS - US)) / 2 - ((AY - AS) + (UY - US)) / 2,
            "AY": AY, "AS": AS, "UY": UY, "US": US}


def summarise(U, seed32_boot):
    n = U.shape[0]
    C = contrasts(U)
    idx = np.random.default_rng(seed32_boot).integers(0, n, (B, n))
    return {k: [float(v.mean()), float(np.percentile(v[idx].mean(1), 2.5)), float(np.percentile(v[idx].mean(1), 97.5))]
            for k, v in C.items()}


def p_meets(s):
    """The position conditions on one measure: P >= 0.15 and its CI lower end > 0."""
    P, Pl, _ = s["P"]
    return P >= MARGIN - EPS and Pl > EPS


def model_reading(s, ss):
    """§5 for one model, in this order. s: frozen measure; ss: shift-invariant measure."""
    L, Ll, Lh = s["L"]
    P, Pl, Ph = s["P"]
    if p_meets(s) and P > abs(L) + EPS:
        return "holds" if p_meets(ss) else "fail-shift"
    if P <= -MARGIN + EPS and Ph < -EPS:
        return "fail-reversed"
    if L >= MARGIN - EPS and Ll > EPS and abs(L) >= abs(P) - EPS:
        return "fail-label"
    return "fail-small"


def overall(readings):
    return "pass" if all(v == "holds" for v in readings.values()) else "fail"


def fmt(x):
    return f"{x[0]:+.2f} [{x[1]:+.2f}, {x[2]:+.2f}]"


SENTENCES = {
    "pass": ("On Sonnet 5.5 and Opus 5.5, as on Haiku 5.5, on program 1's 16 bm0 items at ±30 points, a value in the "
             "assistant turn was taken up more than the same value in the user turn, by at least 0.15 of the "
             "displacement on both uptake measures and by more than the label (\"your\" against \"Sam's\") changed it: "
             "Sonnet position effect {P_sonnet} (label {L_sonnet}), Opus {P_opus} (label {L_opus}). On this design, on "
             "these three Claude models, the pull of an earlier answer follows the turn it sits in more than whose "
             "answer it is said to be."),
    "fail": ("The position-over-label result found on Haiku 5.5 did not hold on both Sonnet 5.5 and Opus 5.5 by the "
             "pre-registered rule (on each model: a position effect of at least 0.15 of the displacement on both "
             "uptake measures, its 95% interval above 0, and larger than the label effect)."),
    "holds": ("On {M}, the position effect held: {P} of the displacement (shift-invariant {P_s}), against a label "
              "effect of {L}."),
    "fail-small": ("On {M}, the position effect did not meet the rule: position {P} (shift-invariant {P_s}), label "
                   "{L}."),
    "fail-shift": ("On {M}, the position effect on the pre-registered measure, {P}, did not hold on the measure that "
                   "compares the +30 and −30 displays directly ({P_s}), so it may come from a change in the rating "
                   "that does not follow the shown number."),
    "fail-label": ("On {M}, the label changed uptake at least as much as the position: label {L}, position {P}."),
    "fail-reversed": ("On {M}, a value in the user turn was taken up more than the same value in the assistant turn: "
                      "position effect {P}."),
    "no_own_pull": ("On {M}, the value labelled as the model's own and placed in its own turn was not taken up "
                    "detectably (uptake {AY}), so the own-answer pull is not present in this wording on {M}, and the "
                    "position effect there has little to split."),
    "fragile": ("Dropping item {item} alone on {M} changes the overall verdict to \"{v}\", so it rests on that item."),
    "untestable": ("The test could not answer its question as run: {why}. No verdict is drawn."),
}


def model_sentence(mk, v, s, ss):
    return SENTENCES[v].format(M=NAME[mk], P=fmt(s["P"]), P_s=fmt(ss["P"]), L=fmt(s["L"]))


def analyse_model(mk, cache, its, anc, seed32_boot):
    nrep = complete_repeats(mk, its, cache)
    res = {"complete_repeats": nrep, "planned_repeats": REPEATS[mk],
           "calls_cached": sum(1 for k in cache if k.startswith(mk + "|")),
           "cost_usd": sum(v["cost"] for k, v in cache.items() if k.startswith(mk + "|")),
           "refused": sum(bool(v.get("refused")) for k, v in cache.items() if k.startswith(mk + "|"))}
    if nrep < 1:
        res["untestable"] = f"{NAME[mk]} has no complete repeat"
        return res
    up, up_s, kept, dropped = item_uptakes(mk, its, anc, cache, nrep)
    res.update(pairs_kept=kept, pairs_dropped=dropped, items_usable=len(up), items_both_directions=len(up_s))
    if len(up) < MIN_ITEMS:
        res["untestable"] = f"{NAME[mk]}: only {len(up)} of 16 items usable (minimum {MIN_ITEMS})"
        return res
    if len(up_s) < MIN_ITEMS:
        res["untestable"] = f"{NAME[mk]}: only {len(up_s)} of 16 items with a statement kept in both directions (minimum {MIN_ITEMS})"
        return res
    ids, ids_s = list(up), list(up_s)
    U = np.array([[up[q][c] for c in CELLS] for q in ids])
    Us = np.array([[up_s[q][c] for c in CELLS] for q in ids_s])
    s, ss = summarise(U, seed32_boot), summarise(Us, seed32_boot)
    v = model_reading(s, ss)
    res.update(items=ids, item_uptakes={q: up[q] for q in ids}, items_s=ids_s, item_uptakes_s={q: up_s[q] for q in ids_s},
               stats=s, stats_shift=ss, reading=v, sentence=model_sentence(mk, v, s, ss))
    if s["AY"][1] <= EPS:
        res["no_own_pull_sentence"] = SENTENCES["no_own_pull"].format(M=NAME[mk], AY=fmt(s["AY"]))
    loo = {}
    for i, q in enumerate(ids):
        sl = summarise(np.delete(U, i, 0), seed32_boot)
        sls = summarise(Us[[j for j, x in enumerate(ids_s) if x != q]], seed32_boot)
        loo[q] = {"P": sl["P"][0], "P_s": sls["P"][0], "L": sl["L"][0], "reading": model_reading(sl, sls)}
    res["loo"] = loo
    res["loo_P_range"] = [min(x["P"] for x in loo.values()), max(x["P"] for x in loo.values())]
    rng = np.random.default_rng(seed32_boot + 1)               # label-swap null (secondary), as in P2-6
    nul = []
    for _ in range(B):
        flip = rng.integers(0, 2, (len(ids), 2)).astype(bool)
        dA = np.where(flip[:, 0], -1, 1) * (U[:, 0] - U[:, 1])
        dU = np.where(flip[:, 1], -1, 1) * (U[:, 2] - U[:, 3])
        nul.append(((dA + dU) / 2).mean())
    res["label_swap_null"] = {"p_ge_obs": float(np.mean(np.array(nul) >= s["L"][0] - EPS)), "q975": float(np.percentile(nul, 97.5))}
    return res


def analyse_cache(cache, its, anc, seed32_boot, check=True):
    if check:
        verify_cache(its, anc, cache)
    res = {"calls_cached": len(cache), "cost_usd": sum(v["cost"] for v in cache.values()),
           "refused": sum(bool(v.get("refused")) for v in cache.values()),
           "models": {mk: analyse_model(mk, cache, its, anc, seed32_boot) for mk in ORDER}}
    why = [m["untestable"] for m in res["models"].values() if "untestable" in m]
    if why:
        res.update(verdict="untestable", why="; ".join(why))
        res["sentence"] = SENTENCES["untestable"].format(why=res["why"])
        return res
    readings = {mk: res["models"][mk]["reading"] for mk in ORDER}
    v = overall(readings)
    kw = {f"{k}_{mk}": fmt(res["models"][mk]["stats"][k]) for mk in ORDER for k in ("P", "L")}
    res.update(readings=readings, verdict=v, sentence=SENTENCES[v].format(**kw))
    flips = []                                                  # P10: one item dropped on one model at a time
    for mk in ORDER:
        for q, x in res["models"][mk]["loo"].items():
            alt = dict(readings, **{mk: x["reading"]})
            if overall(alt) != v:
                flips.append({"model": mk, "item": q, "verdict": overall(alt)})
    res["loo_flips"] = flips
    res["label"] = v + (", fragile (one item)" if flips else "")
    if flips:
        f0 = flips[0]
        res["fragile_sentence"] = SENTENCES["fragile"].format(item=f0["item"], M=NAME[f0["model"]], v=f0["verdict"])
    return res


def haiku_reference():
    if not HAIKU_JSON.exists():
        return None
    h = json.loads(HAIKU_JSON.read_text())
    return {"stats": h["stats"], "stats_shift": h["stats_shift"], "verdict": h["verdict"]}


def write_md(r):
    lines = ["# P2-6r tables (generated by experiments/p2_6r_replication.py; do not edit by hand)", "",
             f"Calls {r['calls_cached']}; cost ${r['cost_usd']:.4f}; refused {r['refused']}.", ""]
    for mk in ORDER:
        m = r["models"][mk]
        lines.append(f"- {NAME[mk]} (`{MODELS[mk]}`, {json.dumps(SETTINGS[mk])}, max_tokens {MAX_TOKENS[mk]}): complete repeats "
                     f"{m['complete_repeats']} of {m['planned_repeats']}; calls {m['calls_cached']}; cost ${m['cost_usd']:.4f}; "
                     f"refused {m['refused']}" + (f"; pairs kept {m['pairs_kept']}, dropped {m['pairs_dropped']}; items usable "
                     f"{m['items_usable']}, with both directions {m['items_both_directions']}" if "pairs_kept" in m else ""))
    if r["verdict"] == "untestable":
        OUT_MD.write_text("\n".join(lines + ["", f"**Verdict: untestable** ({r['why']})"]) + "\n")
        return
    h = haiku_reference()
    lines += ["", "## Effects by model (item mean, 95% item-bootstrap CI)", "",
              "| statistic | Sonnet 5.5 | Opus 5.5 | Haiku 5.5 (om-p2-6, reference) | role |", "|---|---|---|---|---|"]
    rows = [("position effect P (frozen measure)", "stats", "P", "**event**"),
            ("position effect P_s (shift-invariant)", "stats_shift", "P", "**event**"),
            ("label effect L", "stats", "L", "**event** (P > \\|L\\|)"),
            ("label effect L_s (shift-invariant)", "stats_shift", "L", "secondary"),
            ("label effect in the assistant turn, AY − AS", "stats", "L_A", "secondary"),
            ("label effect in the user turn, UY − US", "stats", "L_U", "secondary"),
            ("interaction (AY − AS) − (UY − US)", "stats", "I", "secondary"),
            ("position minus label, P − L", "stats", "P_minus_L", "secondary"),
            ("uptake AY (assistant, yours)", "stats", "AY", "secondary (own-pull check)"),
            ("uptake AS (assistant, Sam's)", "stats", "AS", "secondary"),
            ("uptake UY (user, yours)", "stats", "UY", "secondary"),
            ("uptake US (user, Sam's)", "stats", "US", "secondary")]
    for name, block, k, role in rows:
        hv = fmt(h[block][k]) if h else "—"
        lines.append(f"| {name} | {fmt(r['models']['sonnet'][block][k])} | {fmt(r['models']['opus'][block][k])} | {hv} | {role} |")
    lines.append("| label-swap null: share of swaps with L ≥ observed | "
                 + " | ".join(f"{r['models'][mk]['label_swap_null']['p_ge_obs']:.4f}" for mk in ORDER) + " | — | secondary |")
    lines.append("| leave-one-item-out P range | " + " | ".join(
        f"{r['models'][mk]['loo_P_range'][0]:+.3f} to {r['models'][mk]['loo_P_range'][1]:+.3f}" for mk in ORDER) + " | — | robustness |")
    lines += ["", "Readings by model: " + "; ".join(f"{NAME[mk]} **{r['readings'][mk]}**" for mk in ORDER) + ".",
              f"Leave-one-item-out flips of the overall verdict: {len(r['loo_flips'])}.", "",
              f"**Verdict by the pre-registered rule: {r['label']}**", ""]
    for mk in ORDER:
        m = r["models"][mk]
        lines += [f"## Per item, {NAME[mk]} (uptake by cell)", "", "| item | AY | AS | UY | US | L | P | LOO reading |",
                  "|---|---|---|---|---|---|---|---|"]
        for q in m["items"]:
            u = m["item_uptakes"][q]
            Li, Pi = ((u["AY"] - u["AS"]) + (u["UY"] - u["US"])) / 2, ((u["AY"] - u["UY"]) + (u["AS"] - u["US"])) / 2
            lines.append(f"| {q} | " + " | ".join(f"{u[c]:+.2f}" for c in CELLS) + f" | {Li:+.2f} | {Pi:+.2f} | {m['loo'][q]['reading']} |")
        lines.append("")
    OUT_MD.write_text("\n".join(lines) + "\n")


def seeds():
    s = json.loads(SEEDF.read_text())
    return s["seed32_order"], s["seed32_boot"]


def main():
    its, anc = base.items(), base.anchors()
    if "show" in sys.argv:
        it = its[0]
        for mk in ORDER:
            print(f"=== {mk}: model {MODELS[mk]}, settings {SETTINGS[mk]}, max_tokens {MAX_TOKENS[mk]}, repeats {REPEATS[mk]}")
        for c in ("base",) + CELLS:
            print(f"--- {c}\n" + json.dumps(base.messages(c, it, "X", None if c == "base" else base.shown_value(anc[it['id']]['m_X'], -30)), indent=1))
        return
    so, sb = seeds()
    if "--analyse" not in sys.argv:
        why = gate()
        if why:
            sys.exit(f"gate closed: {why}")
        c = GuardedCaller(CACHE, CAP, "p2-6r", real_call())
        print("run status:", c.run(jobs(its, anc, so)))
    cache = json.loads(CACHE.read_text())
    res = analyse_cache(cache, its, anc, sb)
    stopf = CACHE.with_name(CACHE.stem + "-stop.json")
    res["stop_record"] = json.loads(stopf.read_text()) if stopf.exists() else None
    OUT_JSON.write_text(json.dumps(res, indent=1))
    write_md(res)
    print(json.dumps({k: res[k] for k in ("verdict", "label", "sentence") if k in res}, indent=1))
    print(OUT_MD.read_text())


if __name__ == "__main__":
    main()
