"""P2-5r: does "Sam moves more than self" (om-p2-5, Haiku) hold on Sonnet 5.5 and Opus 5.5, for upward and for
downward plants separately? As pre-registered in experiments/p2-5r-replication.md (DEVIATIONS D18).

    python experiments/p2_5r_replication.py plan        # cells, calls, estimated cost (no API)
    python experiments/p2_5r_replication.py --dry-run   # stubbed responders, the rule on synthetic data (no API)
    python experiments/p2_5r_replication.py             # the test (cached), then analyse; needs the seed file and a go
    python experiments/p2_5r_replication.py --analyse

Run with program 1's interpreter: /Users/seanpharris/entangled-mind/.venv/bin/python

om-p2-5's instrument, unchanged (cells, conversation, questions from p2_5_egocentric): program 1's 16 vignettes x 2
statements, anchor m = Haiku's run-2 first-turn mean, planted V = clip(m + d, 2, 98), d in +/-10, 30, 60, |V - m| >= 5.
Cells run here (2 repeats per cell, each model):
    REF  (own = m, Alex = m)   questions self, sam_p
    OWN  (own = V, Alex = m)   questions self, sam_p
    SWAP (own = m, Alex = V)   question sam_p only (Alex's number on Sam: the third-party contrast)
Models and settings as om-p2-6r: Sonnet 5.5 thinking between_tools, max_tokens 200; Opus 5.5 effort low, max_tokens 4000.
$5.00 cap in code (Sonnet $1.50, Opus $3.50), checked under a lock before every call. Sonnet runs first; Opus only if
Sonnet's run completed. Any refusal stops every later call; nothing is reworded or retried."""

import hashlib
import json
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import p2_5_egocentric as p5                              # noqa: E402  om-p2-5's cells, messages and questions

om = p5.om
RESULTS = om.RESULTS
CACHE, OUT, SEEDF = RESULTS / "p2-5r-calls.json", RESULTS / "p2-5r-replication.json", om.DATA / "p2-5r-seed.json"
TABLES = RESULTS / "p2-5r-tables.md"
HAIKU_CACHE = RESULTS / "p2-5-calls.json"                # om-p2-5's archive, for the Haiku reference column only
REVIEW_DIR = om.ROOT.parents[1] / "ledger" / "design-reviews"
REFUSAL_FILES = ("refusal-p2-5r.md", "refusal.md")
MODELS = {"sonnet": "claude-sonnet-5-5", "opus": "claude-opus-5-5"}
ORDER = ("sonnet", "opus")
SETTINGS = {"sonnet": {"thinking": {"type": "between_tools"}}, "opus": {"output_config": {"effort": "low"}}}
MAX_TOKENS = {"sonnet": 200, "opus": 4000}
CAPS = {"sonnet": 1.50, "opus": 3.50}
CAP = 5.00
R = 2
DS, CLASSES = p5.DS, p5.CLASSES
B = 4000
EPS = 1e-9
MIN_VIGNETTES = 12
PLAN = {"REF": ("self", "sam_p"), "OWN": ("self", "sam_p"), "SWAP": ("sam_p",)}
EST = {"sonnet": 0.7451 / 864, "opus": 1.4205 / 576}    # om-p2-6r's archived cost per call (same items, same settings)
NAME = {"sonnet": "Sonnet 5.5", "opus": "Opus 5.5", "haiku": "Haiku 5.5 (om-p2-5 archive, 5 repeats)"}

SENTENCES = {
    "pass": ("On {M}, on program 1's 16 vignettes, the rating the model attributed to Sam, a person who had seen neither "
             "its planted earlier answer nor another reader's, moved further toward that planted answer than the model's "
             "own re-rating did, both for answers planted above its usual rating (Sam minus own {gu}, 95% interval "
             "[{gul}, {guh}]) and for answers planted below it ({gd}, [{gdl}, {gdh}])."),
    "up_only": ("On {M}, Sam's rating moved further toward the model's planted answer than its own re-rating did only "
                "for answers planted above its usual rating ({gu}, [{gul}, {guh}]); for answers planted below, the gap "
                "was {gd} [{gdl}, {gdh}], not detectably above 0."),
    "down_only": ("On {M}, Sam's rating moved further toward the model's planted answer than its own re-rating did only "
                  "for answers planted below its usual rating ({gd}, [{gdl}, {gdh}]); for answers planted above, the gap "
                  "was {gu} [{gul}, {guh}], not detectably above 0."),
    "reversed": ("On {M}, Sam's rating moved less toward the model's planted answer than the model's own re-rating did "
                 "(Sam minus own, both directions together, {g}, 95% interval [{gl}, {gh}], wholly below 0)."),
    "none": ("On {M}, this test did not show Sam's rating moving further toward the model's planted answer than its own "
             "re-rating in either direction (upward {gu} [{gul}, {guh}]; downward {gd} [{gdl}, {gdh}])."),
    "untestable_nothing_moved": ("On {M}, the planted answer did not detectably move either the model's own re-rating "
                                 "or Sam's rating (both intervals reach 0), so there was no pull to compare."),
    "untestable_few": "On {M}, fewer than 12 of the 16 vignettes have every cell answered; the test could not answer.",
    "not_run": "{M} was not run: {why}.",
    "bet_pass": "The pre-registered event occurred: on {models}, Sam moved further than the model's own re-rating in both directions.",
    "bet_fail": "The pre-registered event did not occur: on neither Sonnet 5.5 nor Opus 5.5 did Sam move further than the model's own re-rating in both directions.",
    "bet_untestable": "The test could not answer: neither model gave a testable reading.",
    "fragile": "On {M}, the reading depends on one vignette: removing {vid} changes it to {to}.",
}


# --- design ------------------------------------------------------------------------------------------------------

def base_jobs(items, anchors):
    out = []
    for vid, o, d, m, v in p5.cells(items, anchors):
        conds = (("REF", m, m),) if d == 0 else (("OWN", v, m), ("SWAP", m, v))
        for cond, own, alex in conds:
            for q in PLAN[cond]:
                out.append((vid, o, cond, d, own, alex, q))
    return out


def jobs(items, anchors, seed32_order=None):
    """(key, mk, vid, o, cond, d, own, alex, q, r): model by model; within a model, repeat outermost (a stop leaves whole
    repeats); within a repeat, the beacon permutation (same for both models)."""
    base = base_jobs(items, anchors)
    out = []
    for mk in ORDER:
        perm = np.random.default_rng(seed32_order).permutation(len(base)) if seed32_order is not None else range(len(base))
        for r in range(R):
            for i in perm:
                vid, o, cond, d, own, alex, q = base[i]
                out.append((f"{mk}|{vid}|{o}|{cond}|{d}|{q}|{r}", mk, vid, o, cond, d, own, alex, q, r))
    return out


def content_hash(mk, msgs):
    return hashlib.sha256(json.dumps({"model": MODELS[mk], "settings": SETTINGS[mk], "max_tokens": MAX_TOKENS[mk],
                                      "messages": msgs}, sort_keys=True).encode()).hexdigest()


def job_messages(job, by_id):
    _, _, vid, o, cond, d, own, alex, q, _ = job
    return p5.messages(by_id[vid], o, own, alex, q)


# --- the caller -------------------------------------------------------------------------------------------------

class GuardedCaller:
    """om-p2-6r's GuardedCaller with a per-model cap as well as the total: content-keyed cache; caps checked under a
    lock before every call; the first refusal or error stops every later call; nothing is reworded or retried; a
    refused job is written into the cache, and no later run starts on a cache holding one or with a refusal file."""

    def __init__(self, cache_path, label, call_fn):
        self.path, self.label, self.call_fn = Path(cache_path), label, call_fn
        self.cache = json.loads(self.path.read_text()) if self.path.exists() else {}
        refused = [k for k, v in self.cache.items() if v.get("refused")]
        on_file = [f for f in REFUSAL_FILES if (RESULTS / f).exists()]
        if refused or on_file:
            sys.exit(f"{label}: a refusal is on record ({refused[0] if refused else 'results/' + on_file[0]}); not resumed")
        self.lock, self.stop = threading.Lock(), threading.Event()
        self.refusal, self.errors, self.after_stop = {}, [], 0

    def spent(self, mk=None):
        return sum(v["cost"] for k, v in self.cache.items() if mk is None or k.startswith(mk + "|"))

    def run(self, jobs_, by_id, workers=8):
        err = self.call_fn.refusal_error
        capped = threading.Event()

        def work(job):
            key, mk = job[0], job[1]
            msgs = job_messages(job, by_id)
            h = content_hash(mk, msgs)
            if key in self.cache:
                assert self.cache[key].get("sha256") == h, f"cache entry {key} does not match its prompt"
                return
            with self.lock:
                if self.stop.is_set():
                    return
                if self.spent() >= CAP or self.spent(mk) >= CAPS[mk]:
                    capped.set()
                    self.stop.set()
                    return
            try:
                d, cost, rid = self.call_fn(mk, msgs)
                raw = int(d["probability"])
            except err as e:
                with self.lock:
                    self.cache[key] = {"refused": True, "request_id": getattr(e, "request_id", None), "cost": 0.0, "sha256": h}
                    self.refusal.setdefault("e", (key, e))
                    self.stop.set()
                return
            except Exception as e:  # noqa: BLE001  any other error also stops the run
                with self.lock:
                    self.errors.append((key, repr(e)))
                    self.stop.set()
                return
            with self.lock:
                if self.stop.is_set():
                    self.after_stop += 1
                self.cache[key] = {"value": min(100, max(0, raw)), "raw": raw, "cost": cost, "request_id": rid, "sha256": h}
                if len(self.cache) % 100 == 0:
                    self.path.write_text(json.dumps(self.cache))
                    print(f"{self.label}: {len(self.cache)} done, ${self.spent():.4f}", flush=True)

        with ThreadPoolExecutor(max_workers=workers) as ex:
            list(ex.map(work, jobs_))
        self.path.write_text(json.dumps(self.cache))
        if not self.stop.is_set():
            print(f"{self.label}: complete, {len(self.cache)} cached, ${self.spent():.4f}", flush=True)
            return "complete"
        reason = "refusal" if self.refusal else "error" if self.errors else "cap"
        key = self.refusal["e"][0] if self.refusal else self.errors[0][0] if self.errors else None
        rid = getattr(self.refusal["e"][1], "request_id", None) if self.refusal else None
        rec = {"label": self.label, "reason": reason, "job": key, "request_id": rid, "completed_after_stop": self.after_stop,
               "calls_cached": len(self.cache), "error": self.errors[0][1] if self.errors else None}
        self.path.with_name(self.path.stem + "-stop.json").write_text(json.dumps(rec, indent=1))
        if self.refusal:
            k, e = self.refusal["e"]
            (RESULTS / REFUSAL_FILES[0]).write_text(
                f"# Run stopped on a refusal\n\n{self.label}, job `{k}`\n\nRefused call: **{getattr(e, 'call', '?')}**\n\n"
                f"Request ID: `{getattr(e, 'request_id', None)}`\n\nStop details:\n\n```\n{getattr(e, 'stop_details', '')}\n```\n\n"
                f"Calls in flight that completed after the stop: {self.after_stop}.\n\nNothing was reworded or retried. "
                "The run is not resumed past this refusal.\n")
        return reason


def real_call():
    llm = om.llm

    def call(mk, msgs):
        s = json.loads(json.dumps(SETTINGS[mk]))
        oc = s.pop("output_config", {})
        oc["format"] = {"type": "json_schema", "schema": p5.RATE}
        resp = llm.client().messages.create(model=MODELS[mk], max_tokens=MAX_TOKENS[mk], messages=msgs, output_config=oc, **s)
        llm._check_stop(resp, f"p2-5r {mk}")
        text = next(b.text for b in resp.content if b.type == "text")
        return json.loads(text), llm._usage(resp).cost, getattr(resp, "_request_id", None)
    call.refusal_error = llm.RefusalError
    return call


def run_all(caller, jobs_, by_id):
    """Sonnet first; Opus only if Sonnet's run completed (a stop on Sonnet means Opus is never called)."""
    status = {}
    for mk in ORDER:
        status[mk] = caller.run([j for j in jobs_ if j[1] == mk], by_id)
        if status[mk] != "complete":
            break
    return status


def gate():
    reviews = sorted(REVIEW_DIR.glob("om-p2-5r*.md"))
    if not reviews:
        return "no design review om-p2-5r*.md"
    for rv in reviews:
        v, conf = p5.review_state(rv)
        if not (v == "go" or (v == "fix-first" and conf not in ("", "null"))):
            return f"{rv.name}: verdict {v or '?'}" + (" (not confirmed)" if v == "fix-first" else "")
    if not SEEDF.exists():
        return "no seed file (the seed commit comes before any call)"
    return None


# --- analysis ----------------------------------------------------------------------------------------------------

def cell_means(items, anchors, cache, prefix, reps):
    """{(vid, o, cond, d, q): mean over repeats 0..reps-1}; a cell is absent if any repeat is missing or refused."""
    out = {}
    for vid, o, d, m, v in p5.cells(items, anchors):
        for cond in (("REF",) if d == 0 else ("OWN", "SWAP")):
            for q in PLAN[cond]:
                vals = [cache.get(f"{prefix}{vid}|{o}|{cond}|{d}|{q}|{r}") for r in range(reps)]
                if all(x is not None and not x.get("refused") for x in vals):
                    out[(vid, o, cond, d, q)] = float(np.mean([x["value"] for x in vals]))
    return out


KEYS = [(c, q, s, k) for c, q in (("OWN", "self"), ("OWN", "sam_p"), ("SWAP", "sam_p")) for s in ("up", "down")
        for k in CLASSES]


def uptake_table(items, anchors, M, both_only=False):
    """Per vignette, per (cond, q, sign, class): (sum of u, n). u = (y - y_REF(q)) / (V - m). both_only keeps only the
    statement-classes kept in both directions (secondary)."""
    vids = [it["id"] for it in items]
    col = {k: j for j, k in enumerate(KEYS)}
    S, N = np.zeros((len(vids), len(KEYS))), np.zeros((len(vids), len(KEYS)))
    complete = np.ones(len(vids), bool)
    cs = p5.cells(items, anchors)
    kept = {(c[0], c[1], c[2]) for c in cs}
    for vi, vid in enumerate(vids):
        for (_, o, d, m, v) in [c for c in cs if c[0] == vid and c[2] != 0]:
            if both_only and (vid, o, -d) not in kept:
                continue
            for cond, q in (("OWN", "self"), ("OWN", "sam_p"), ("SWAP", "sam_p")):
                y, y0 = M.get((vid, o, cond, d, q)), M.get((vid, o, "REF", 0, q))
                if y is None or y0 is None:
                    complete[vi] = False
                    continue
                j = col[(cond, q, "up" if d > 0 else "down", abs(d))]
                S[vi, j] += (y - y0) / (v - m)
                N[vi, j] += 1
    return vids, S, N, complete


def stats_of(S, N):
    with np.errstate(invalid="ignore", divide="ignore"):
        cls = S.sum(0) / N.sum(0)
    U = lambda c, q, signs: float(np.nanmean([cls[KEYS.index((c, q, s, k))] for s in signs for k in CLASSES]))
    out = {}
    for tag, signs in (("up", ("up",)), ("down", ("down",)), ("all", ("up", "down"))):
        out[f"self_{tag}"] = U("OWN", "self", signs)
        out[f"sam_{tag}"] = U("OWN", "sam_p", signs)
        out[f"swap_{tag}"] = U("SWAP", "sam_p", signs)
        out[f"gap_{tag}"] = out[f"sam_{tag}"] - out[f"self_{tag}"]
        out[f"dU_{tag}"] = out[f"sam_{tag}"] - out[f"swap_{tag}"]
    return out


def boot(S, N, idx, seed, n=B):
    idx = np.asarray(idx)
    point = stats_of(S[idx], N[idx])
    pick = np.random.default_rng(seed).integers(0, len(idx), (n, len(idx)))
    draws = {k: np.empty(n) for k in point}
    for b, p in enumerate(pick):
        st = stats_of(S[idx[p]], N[idx[p]])
        for k in point:
            draws[k][b] = st[k]
    ci = {k: [float(np.nanpercentile(v, 2.5)), float(np.nanpercentile(v, 97.5))] for k, v in draws.items()}
    return point, ci


def reading(point, ci, n_complete):
    """One model's reading, in order. EPS: a bound within 1e-9 of 0 is not above (or below) 0."""
    if n_complete < MIN_VIGNETTES:
        return "untestable_few"
    if not (ci["self_all"][0] > EPS or ci["sam_all"][0] > EPS):
        return "untestable_nothing_moved"
    up, down = ci["gap_up"][0] > EPS, ci["gap_down"][0] > EPS
    if up and down:
        return "pass"
    if up:
        return "up_only"
    if down:
        return "down_only"
    if ci["gap_all"][1] < -EPS:
        return "reversed"
    return "none"


def fmt(point, ci, M):
    f = lambda x: f"{x:+.3f}"
    return dict(M=M, g=f(point["gap_all"]), gl=f(ci["gap_all"][0]), gh=f(ci["gap_all"][1]),
                gu=f(point["gap_up"]), gul=f(ci["gap_up"][0]), guh=f(ci["gap_up"][1]),
                gd=f(point["gap_down"]), gdl=f(ci["gap_down"][0]), gdh=f(ci["gap_down"][1]))


def model_result(items, anchors, M, seed, label):
    vids, S, N, complete = uptake_table(items, anchors, M)
    idx = np.flatnonzero(complete)
    if len(idx) < MIN_VIGNETTES:
        return {"reading": "untestable_few", "n_complete": int(len(idx)),
                "sentence": SENTENCES["untestable_few"].format(M=label)}
    point, ci = boot(S, N, idx, seed)
    rd = reading(point, ci, len(idx))
    loo = []
    for drop in idx:
        p2, c2 = boot(S, N, idx[idx != drop], seed)
        loo.append({"dropped": vids[drop], "reading": reading(p2, c2, len(idx)), "gap_up": p2["gap_up"],
                    "gap_down": p2["gap_down"]})
    flips = [x for x in loo if x["reading"] != rd]
    _, Sb, Nb, cb = uptake_table(items, anchors, M, both_only=True)
    pb, cib = boot(Sb, Nb, np.flatnonzero(cb), seed)
    sent = SENTENCES[rd].format(**fmt(point, ci, label))
    if flips:
        sent += " " + " ".join(SENTENCES["fragile"].format(M=label, vid=x["dropped"], to=x["reading"]) for x in flips)
    return {"reading": rd, "n_complete": int(len(idx)), "point": point, "ci": ci, "loo": loo,
            "loo_flips": [x["dropped"] for x in flips], "both_directions_only": {"point": pb, "ci": cib,
            "reading_would_give": reading(pb, cib, int(cb.sum()))}, "sentence": sent}


def bet_reading(per_model):
    tested = [mk for mk in ORDER if mk in per_model and not per_model[mk]["reading"].startswith(("untestable", "not_run"))]
    passed = [mk for mk in tested if per_model[mk]["reading"] == "pass"]
    if passed:
        return "pass", SENTENCES["bet_pass"].format(models=" and ".join(NAME[m] for m in passed))
    if tested:
        return "fail", SENTENCES["bet_fail"]
    return "untestable", SENTENCES["bet_untestable"]


def analyse_cache(cache, items, anchors, seed_boot, status=None):
    per = {}
    for mk in ORDER:
        mc = {k: v for k, v in cache.items() if k.startswith(mk + "|")}
        planned = [j for j in jobs(items, anchors) if j[1] == mk]
        if not mc or (status and status.get(mk) not in (None, "complete") and len(mc) < len(planned)):
            why = "the run stopped before it" if not mc else f"{len(planned) - len(mc)} of {len(planned)} calls missing ({(status or {}).get(mk)})"
            if len(mc) < len(planned):
                per[mk] = {"reading": "not_run", "sentence": SENTENCES["not_run"].format(M=NAME[mk], why=why),
                           "calls": len(mc)}
                continue
        M = cell_means(items, anchors, cache, mk + "|", R)
        per[mk] = model_result(items, anchors, M, seed_boot, NAME[mk])
        per[mk]["calls"], per[mk]["cost_usd"] = len(mc), sum(v["cost"] for v in mc.values())
    label, sent = bet_reading(per)
    return {"label": label, "sentence": sent, "per_model": per}


def haiku_reference(items, anchors, seed_boot):
    """Secondary: the same statistics on om-p2-5's Haiku archive (5 repeats; its cache keys have no model prefix)."""
    if not HAIKU_CACHE.exists():
        return None
    cache = json.loads(HAIKU_CACHE.read_text())
    M = cell_means(items, anchors, cache, "", 5)
    return model_result(items, anchors, M, seed_boot, NAME["haiku"])


def write_tables(res):
    L = ["# P2-5r tables (generated by experiments/p2_5r_replication.py; do not edit)", "",
         f"**Bet: {res['label']}.** {res['sentence']}", ""]
    cols = [(mk, res["per_model"].get(mk)) for mk in ORDER] + [("haiku", res.get("haiku_reference"))]
    L += ["| statistic | " + " | ".join(NAME[m] for m, _ in cols) + " |", "|---|" + "---|" * len(cols)]
    names = [("self_all", "own re-rating uptake (OWN), both directions"), ("sam_all", "Sam's uptake (OWN), both"),
             ("gap_all", "Sam minus own, both"), ("gap_up", "Sam minus own, upward plants (primary)"),
             ("gap_down", "Sam minus own, downward plants (primary)"), ("self_up", "own, upward"),
             ("self_down", "own, downward"), ("sam_up", "Sam, upward"), ("sam_down", "Sam, downward"),
             ("swap_all", "Sam's uptake of Alex's number (SWAP), both"), ("dU_all", "Sam: own minus Alex's number, both")]
    for k, nm in names:
        cells = []
        for _, r in cols:
            if not r or "point" not in r:
                cells.append("—")
            else:
                cells.append(f"{r['point'][k]:+.3f} [{r['ci'][k][0]:+.3f}, {r['ci'][k][1]:+.3f}]")
        L.append(f"| {nm} | " + " | ".join(cells) + " |")
    L += ["", "| model | reading | vignettes complete | leave-one-out flips | statements kept in both directions: reading |",
          "|---|---|---|---|---|"]
    for m, r in cols:
        if r:
            L.append(f"| {NAME[m]} | {r['reading']} | {r.get('n_complete', '—')} | {r.get('loo_flips', '—')} | "
                     f"{r.get('both_directions_only', {}).get('reading_would_give', '—')} |")
    L += ["", "Per-model sentences:", ""] + [f"- {r['sentence']}" for _, r in cols if r]
    TABLES.write_text("\n".join(L) + "\n")


def analyse(status=None):
    items, anchors = p5.load_items()
    by_id = {it["id"]: it for it in items}
    cache = json.loads(CACHE.read_text())
    for j in jobs(items, anchors):
        if j[0] in cache:
            assert cache[j[0]].get("sha256") == content_hash(j[1], job_messages(j, by_id)), f"{j[0]} does not match"
    assert not set(cache) - {j[0] for j in jobs(items, anchors)}, "cache holds keys the design does not"
    seed = json.loads(SEEDF.read_text())
    res = analyse_cache(cache, items, anchors, seed["seed32_boot"], status)
    res["haiku_reference"] = haiku_reference(items, anchors, seed["seed32_boot"])
    stopf = CACHE.with_name(CACHE.stem + "-stop.json")
    res["stop_record"] = json.loads(stopf.read_text()) if stopf.exists() else None
    res["calls"], res["cost_usd"] = len(cache), sum(v["cost"] for v in cache.values())
    res["refused"] = sum(1 for v in cache.values() if v.get("refused"))
    res["out_of_range"] = sum(1 for v in cache.values() if not v.get("refused") and v["raw"] != v["value"])
    OUT.write_text(json.dumps(res, indent=1))
    write_tables(res)
    print(TABLES.read_text())
    return res


# --- plan and dry run --------------------------------------------------------------------------------------------

def plan():
    items, anchors = p5.load_items()
    js = jobs(items, anchors)
    for mk in ORDER:
        n = sum(1 for j in js if j[1] == mk)
        print(f"{mk}: {n} calls ({n // R} per repeat x {R}); est ${n * EST[mk]:.2f} (cap ${CAPS[mk]:.2f})")
    print(f"total est ${sum(sum(1 for j in js if j[1] == mk) * EST[mk] for mk in ORDER):.2f} (cap ${CAP:.2f})")


def stub_value(world, job, rng, vf):
    """A synthetic responder for one job: the own re-rating moves `self` of the way from m to the planted answer; Sam
    moves sam_up / sam_down (by the plant's sign) toward the model's own planted answer and `alex` toward Alex's
    number; noise sd points per call; a per-vignette factor (sd vsd) on every pull."""
    _, _, vid, o, cond, d, own, alex, q, _ = job
    m = alex if cond == "OWN" else own                       # REF and SWAP: own slot is m; OWN: Alex's slot is m
    f = vf.setdefault(vid, 1 + rng.normal(0, world.get("vsd", 0.3)))
    if q == "sam_p":
        a = world["sam_up"] if d > 0 else world["sam_down"]
        y = m + f * a * (own - m) + world["alex"] * (alex - m)
    else:
        y = m + f * world["self"] * (own - m) + world["alex_self"] * (alex - m)
    return int(round(min(100, max(0, y + rng.normal(0, world["sd"])))))


def dry_run(sims=60):
    items, anchors = p5.load_items()
    js = jobs(items, anchors)
    worlds = {
        "Haiku-like (own .36, Sam up .58 / down .40)": dict(self=0.36, sam_up=0.58, sam_down=0.40, alex=0.02, alex_self=0.07, sd=2),
        "Haiku as measured, up-only gap (Sam up .58 / down .36)": dict(self=0.36, sam_up=0.58, sam_down=0.36, alex=0.02, alex_self=0.07, sd=2),
        "Sam = own (.36)": dict(self=0.36, sam_up=0.36, sam_down=0.36, alex=0.02, alex_self=0.07, sd=2),
        "Sam half of own (reversed)": dict(self=0.36, sam_up=0.18, sam_down=0.18, alex=0.02, alex_self=0.07, sd=2),
        "Opus-like weak pull (own .07, Sam .07)": dict(self=0.07, sam_up=0.07, sam_down=0.07, alex=0.0, alex_self=0.0, sd=3),
        "nothing moves": dict(self=0.0, sam_up=0.0, sam_down=0.0, alex=0.0, alex_self=0.0, sd=3),
        "small gap both ways (+.08)": dict(self=0.30, sam_up=0.38, sam_down=0.38, alex=0.02, alex_self=0.05, sd=3),
        "clear gap both ways (+.15)": dict(self=0.30, sam_up=0.45, sam_down=0.45, alex=0.02, alex_self=0.05, sd=3),
        "Haiku-like, larger vignette spread (vsd .6)": dict(self=0.36, sam_up=0.58, sam_down=0.40, alex=0.02, alex_self=0.07, sd=2, vsd=0.6),
    }
    for name, w in worlds.items():
        counts = {}
        for s in range(sims):
            rng, vf = np.random.default_rng(s), {}
            cache = {j[0]: {"value": stub_value(w, j, rng, vf), "cost": 0.0} for j in js if j[1] == "sonnet"}
            M = cell_means(items, anchors, cache, "sonnet|", R)
            vids, S, N, complete = uptake_table(items, anchors, M)
            idx = np.flatnonzero(complete)
            p, ci = boot(S, N, idx, s, n=400)
            rd = reading(p, ci, len(idx))
            counts[rd] = counts.get(rd, 0) + 1
        print(f"  {name:55s} " + ", ".join(f"{k} {v / sims:.2f}" for k, v in sorted(counts.items())))
    # boundary checks (P13)
    z = {k: [0.0, 0.0] for k in ("self_all", "sam_all", "gap_up", "gap_down", "gap_all")}
    z["self_all"] = [0.1, 0.5]
    assert reading({}, dict(z, gap_up=[0.0, 1], gap_down=[0.3 - 0.1 - 0.2, 1]), 16) == "none"
    assert reading({}, dict(z, gap_up=[1e-4, 1], gap_down=[1e-4, 1]), 16) == "pass"
    assert reading({}, dict(z, gap_up=[1e-4, 1], gap_down=[-1, 1]), 16) == "up_only"
    assert reading({}, dict(z, gap_all=[-1, -1e-4]), 16) == "reversed"
    assert reading({}, dict(z, self_all=[0.0, 1], sam_all=[-0.1, 1]), 16) == "untestable_nothing_moved"
    assert reading({}, z, 11) == "untestable_few"
    print("  boundary and order checks: hold")


def main():
    if "plan" in sys.argv:
        return plan()
    if "--dry-run" in sys.argv:
        return dry_run()
    status = None
    if "--analyse" not in sys.argv:
        why = gate()
        if why:
            sys.exit(f"p2-5r: not running: {why}")
        items, anchors = p5.load_items()
        seed = json.loads(SEEDF.read_text())
        c = GuardedCaller(CACHE, "p2-5r", real_call())
        status = run_all(c, jobs(items, anchors, seed["seed32_order"]), {it["id"]: it for it in items})
        print("run status:", status)
    analyse(status)


if __name__ == "__main__":
    main()
