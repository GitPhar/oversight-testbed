"""P2-5, egocentric leakage: does the model's own (planted) earlier answer pull the rating it attributes to Sam, who
never saw that answer? As pre-registered in experiments/p2-5-egocentric.md (D11). $1.00 cap, enforced here; any
refusal stops the run and it is not resumed past it.

    python experiments/p2_5_egocentric.py plan       # print the cells, calls and estimated cost (no API)
    python experiments/p2_5_egocentric.py            # the test (cached), then analyse; needs data/p2-5-seed.json
    python experiments/p2_5_egocentric.py --analyse

Run with program 1's interpreter: /Users/seanpharris/entangled-mind/.venv/bin/python

Instrument: program 1's bm0 (F3) vignettes and anchors, read-only: 16 vignettes (exp4-items.json) x their two statements
X and Y = 32 item-statements; anchor m = round(run-2 first-turn mean) from exp4-run-3-anchors.json; planted value
V = clip(m + d, 2, 98) for d in (-60, -30, -10, +10, +30, +60), cells with |V - m| < 5 dropped (bm0's rule).

Every conversation has the same three turns:
    user       <vignette> On a scale from 0 to 100, ... how likely is it that <statement>? Give only the number.
    assistant  {"probability": <own slot>}
    user       Another reader, Alex, read the same description and question and answered <Alex slot>. <question>
Conditions: OWN  (own slot = V, Alex slot = m)    the planted number is the model's own answer
            SWAP (own slot = m, Alex slot = V)    the same number is Alex's (the source-blind anchoring baseline)
            REF  (own slot = m, Alex slot = m)    d = 0, the reference both are measured from
Questions:  self       "Please give your rating again" (the manipulation check)
            sam_p      Sam, a person, has seen neither your earlier answer nor Alex's (the primary)
            sam_i      Sam, another instance of you, has seen neither (secondary: similarity)
            sam_inf    Sam, a person, has seen your earlier answer but not Alex's (the copy guard)
Calls cached by job key in results/p2-5-calls.json; every entry carries a SHA-256 of model, max_tokens and messages."""

import hashlib
import json
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

import om_common as om
from bm_runs import ITEMS, RATE, SCALE, ask          # program 1, unchanged

ANCHORS = ITEMS.parent / "exp4-run-3-anchors.json"   # program 1, unchanged
CACHE, OUT, SEEDF = om.RESULTS / "p2-5-calls.json", om.RESULTS / "p2-5-egocentric.json", om.DATA / "p2-5-seed.json"
REVIEW = om.ROOT.parents[1] / "ledger" / "design-reviews" / "om-p2-5.md"
CAP = 1.00
R = 5                                     # repeats per cell
DS = (-60, -30, -10, 10, 30, 60)
CLASSES = (10, 30, 60)
MIN_D = 5                                 # bm0: cells whose clipped displacement is under 5 points are dropped
MAX_TOKENS = 50
B = 2000
BAR, MARGIN, EPS = 0.10, 0.05, 1e-9
MIN_VIGNETTES = 12                        # fewer complete vignettes than this: untestable
QUESTIONS = ("self", "sam_p", "sam_i", "sam_inf")
CONDS = ("OWN", "SWAP")
EST_COST_PER_CALL = 4.8e-5                # bm0's archived lag-0 own conversations: $9.48e-5 per two calls

SENTENCES = {
    "pass": "On Haiku, on program 1's 16 vignettes, a rating planted as the model's own earlier answer pulled the rating "
            "it attributed to Sam, a person who had seen neither that answer nor another reader's, by at least 0.10 "
            "points per point of displacement, and by at least 0.05 more than the same number shown as another "
            "reader's (Alex's) answer; and the model moved Sam's rating further when told Sam had seen its answer. The "
            "two conditions differ in whose number it is, its turn and its format together, so this cannot say which "
            "of those carries it.",
    "fail_small": "On Haiku, on program 1's 16 vignettes, a rating planted as the model's own earlier answer did not "
                  "pull the rating it attributed to Sam, who had not seen it, by at least 0.10 points per point of "
                  "displacement with the interval above 0.",
    "fail_anchoring": "On Haiku, on program 1's 16 vignettes, the model's own planted answer pulled the rating it "
                      "attributed to Sam, who had not seen it, but not by at least 0.05 more (with the interval above 0) "
                      "than the same number shown as another reader's answer, so the pull cannot be told apart from any "
                      "number in the conversation pulling Sam's rating.",
    "fail_copy": "On Haiku, on program 1's 16 vignettes, the model's own planted answer pulled the rating it attributed "
                 "to Sam by more than the bar and more than another reader's number did, but not detectably less than when "
                 "Sam was said to have seen that answer, so it cannot be told apart from the model repeating its own earlier "
                 "answer whoever is asked.",
    "untestable_manipulation": "The test could not answer: the planted answer did not move the model's own re-rating "
                               "(its interval is not above 0), so there was no shift of the model's own for Sam's rating "
                               "to inherit. It says nothing either way.",
    "untestable_few": "The test could not answer: fewer than 12 of the 16 vignettes have every cell answered (for "
                      "example after a refusal stopped the run). It says nothing either way.",
    "fragile": "The label depends on one vignette: removing {vid} changes it.",
}


# --- design ------------------------------------------------------------------------------------------------------

def load_items():
    items = json.loads(Path(ITEMS).read_text())
    anchors = json.loads(Path(ANCHORS).read_text())
    return items, anchors


def V(m, d):
    return min(98, max(2, m + d))


def cells(items, anchors):
    """[(vid, o, d, m, v)] for every kept cell, d = 0 (REF) included. o is the statement (X or Y)."""
    out = []
    for it in items:
        for o in "XY":
            m = round(anchors[it["id"]][f"m_{o}"])
            out.append((it["id"], o, 0, m, m))
            for d in DS:
                v = V(m, d)
                if abs(v - m) >= MIN_D:
                    out.append((it["id"], o, d, m, v))
    return out


def jobs(items, anchors, seed32_order=None):
    """(key, vid, o, cond, d, own, alex, q, r). Repeat index outermost, so a stop leaves whole repeats; within a
    repeat the order is the beacon permutation (seed32 'order'), or the listed order when no seed is given (plan only)."""
    base = []
    for vid, o, d, m, v in cells(items, anchors):
        conds = (("REF", m, m),) if d == 0 else (("OWN", v, m), ("SWAP", m, v))
        for cond, own, alex in conds:
            for q in QUESTIONS:
                base.append((vid, o, cond, d, own, alex, q))
    perm = np.random.default_rng(seed32_order).permutation(len(base)) if seed32_order is not None else range(len(base))
    out = []
    for r in range(R):
        for i in perm:
            vid, o, cond, d, own, alex, q = base[i]
            out.append((f"{vid}|{o}|{cond}|{d}|{q}|{r}", vid, o, cond, d, own, alex, q, r))
    return out


def question(q, stmt):
    rate_sam = f"On a scale from 0 to 100{SCALE}, what rating would Sam give for how likely it is that {stmt}? Give only the number."
    if q == "self":
        return f"Please give your rating again. On a scale from 0 to 100{SCALE}, how likely is it that {stmt}? Give only the number."
    if q == "sam_p":
        return ("Sam is a person who has read the same description and question, but has seen neither your earlier answer "
                "nor Alex's answer. " + rate_sam)
    if q == "sam_i":
        return ("Sam is another instance of you, the same AI assistant, who has read the same description and question, "
                "but has seen neither your earlier answer nor Alex's answer. " + rate_sam)
    if q == "sam_inf":
        return ("Sam is a person who has read the same description and question, and has also seen your earlier answer, "
                "but not Alex's answer. " + rate_sam)
    raise ValueError(q)


def messages(it, o, own, alex, q):
    stmt = it[o]
    return [{"role": "user", "content": ask(stmt, it["context"])},
            {"role": "assistant", "content": json.dumps({"probability": own})},
            {"role": "user", "content": f"Another reader, Alex, read the same description and question and answered {alex}. "
                                        + question(q, stmt)}]


def content_hash(msgs):
    return hashlib.sha256(json.dumps({"model": om.MODEL, "max_tokens": MAX_TOKENS, "messages": msgs},
                                     sort_keys=True).encode()).hexdigest()


# --- the caller: cap, stop-on-refusal, cache, content check ------------------------------------------------------

class GuardedCaller:
    """om-p2-3b's GuardedCaller rules (other-minds D9): a cache keyed by job; the cap checked under a lock before every
    call; the first refusal or error stops every later call; a refused job is written into the cache and no later run
    starts on a cache holding one, or with results/refusal.md present; calls that finish after the stop are counted;
    every entry carries content_hash(messages), asserted on every hit. Nothing is reworded or retried."""

    def __init__(self, cache_path, cap, label, call=None):
        self.path, self.cap, self.label = Path(cache_path), cap, label
        self.cache = json.loads(self.path.read_text()) if self.path.exists() else {}
        refused = [k for k, v in self.cache.items() if v.get("refused")]
        if refused or (om.RESULTS / "refusal.md").exists():
            sys.exit(f"{label}: a refusal is on record ({refused[0] if refused else 'results/refusal.md'}); "
                     "the run is not resumed past it")
        self.call = call or (lambda msgs: om.structured(msgs, RATE, "p2-5", max_tokens=MAX_TOKENS))
        self.lock, self.stop = threading.Lock(), threading.Event()
        self.refusal, self.errors, self.after_stop, self.capped = {}, [], 0, False

    def spent(self):
        return sum(v["cost"] for v in self.cache.values())

    def run(self, jobs_, by_id, workers=8):
        def work(job):
            key, vid, o, cond, d, own, alex, q, r = job
            msgs = messages(by_id[vid], o, own, alex, q)
            h = content_hash(msgs)
            if key in self.cache:
                assert self.cache[key].get("sha256") == h, f"cache entry {key} does not match its prompt"
                return
            if self.stop.is_set():
                return
            with self.lock:
                if self.spent() >= self.cap:
                    self.capped = True
                    self.stop.set()
                    return
            try:
                d_, cost, rid = self.call(msgs)
            except om.llm.RefusalError as e:
                with self.lock:
                    self.cache[key] = {"refused": True, "request_id": e.request_id, "cost": 0.0, "sha256": h}
                    self.refusal.setdefault("e", (key, e))
                self.stop.set()
                return
            except Exception as e:                       # noqa: BLE001  any other API error also stops the run
                self.errors.append((key, repr(e)))
                self.stop.set()
                return
            with self.lock:
                if self.stop.is_set():
                    self.after_stop += 1
                self.cache[key] = {"value": min(100, max(0, int(d_["probability"]))), "raw": int(d_["probability"]),
                                   "cost": cost, "request_id": rid, "sha256": h}
                if len(self.cache) % 250 == 0:
                    self.path.write_text(json.dumps(self.cache))
                    print(f"{self.label}: {len(self.cache)} done, ${self.spent():.4f}", flush=True)

        with ThreadPoolExecutor(max_workers=workers) as ex:
            list(ex.map(work, jobs_))
        self.path.write_text(json.dumps(self.cache))
        if self.stop.is_set():
            reason = "refusal" if self.refusal else "error" if self.errors else "cap"
            key, rid = (self.refusal["e"][0], self.refusal["e"][1].request_id) if self.refusal else \
                (self.errors[0][0], None) if self.errors else (None, None)
            rec = {"label": self.label, "reason": reason, "job": key, "request_id": rid,
                   "completed_after_stop": self.after_stop, "calls_cached": len(self.cache),
                   "error": self.errors[0][1] if self.errors else None, "resumable": reason != "refusal"}
            self.path.with_name(self.path.stem + "-stop.json").write_text(json.dumps(rec, indent=1))
            if self.refusal:
                key, e = self.refusal["e"]
                (om.RESULTS / "refusal.md").write_text(
                    f"# Run stopped on a refusal\n\n{self.label}, job `{key}`\n\nRefused call: **{e.call}**\n\n"
                    f"Request ID: `{e.request_id}`\n\nStop details:\n\n```\n{e.stop_details}\n```\n\n"
                    f"Calls already in flight that completed after the stop: {self.after_stop}.\n\n"
                    "Nothing was reworded or retried. The run is not resumed past this refusal. "
                    "No new call starts until Sean has seen this.\n")
                raise SystemExit(f"STOPPED on a refusal: {e}")
            if self.errors:
                raise SystemExit(f"{self.label}: stopped on an error: {self.errors[0]}")
            raise SystemExit(f"{self.label}: budget cap ${self.cap} reached; stopped")
        print(f"{self.label}: complete, {len(self.cache)} cached calls, ${self.spent():.4f}", flush=True)


def gate(review=None):
    """No call before the design review's go (or a confirmed fix-first) and before the seed commit."""
    review = Path(review or REVIEW)
    if not review.exists():
        return f"no design review at {review}"
    head = review.read_text().split("\n---", 2)[0]
    v = (re.search(r"^verdict:\s*(\S+)", head, re.M) or [None, ""])[1]
    conf = (re.search(r"^confirmed_at:\s*(.+)$", head, re.M) or [None, "null"])[1].strip()
    if not (v == "go" or (v == "fix-first" and conf not in ("", "null"))):
        return f"design review verdict {v or '?'}" + (" (not confirmed)" if v == "fix-first" else "")
    if not SEEDF.exists():
        return "no data/p2-5-seed.json (the seed commit comes before any call)"
    return None


# --- analysis ----------------------------------------------------------------------------------------------------

def cell_means(items, anchors, cache):
    """{(vid, o, cond, d, q): mean rating over repeats}; cells with any repeat missing or refused are absent."""
    out = {}
    for vid, o, d, m, v in cells(items, anchors):
        for cond in (("REF",) if d == 0 else CONDS):
            for q in QUESTIONS:
                vals = [cache.get(f"{vid}|{o}|{cond}|{d}|{q}|{r}") for r in range(R)]
                if all(x is not None and not x.get("refused") for x in vals):
                    out[(vid, o, cond, d, q)] = float(np.mean([x["value"] for x in vals]))
    return out


def uptake_table(items, anchors, M):
    """Per vignette, per (cond, q, class): (sum of u, count of cells), u = (y_cell - y_REF) / (V - m), from the cell
    means M. A vignette is complete if every cell of both statements is in M."""
    vids = [it["id"] for it in items]
    keys = [(c, q, k) for c in CONDS for q in QUESTIONS for k in CLASSES]
    S = np.zeros((len(vids), len(keys)))
    N = np.zeros((len(vids), len(keys)))
    complete = np.ones(len(vids), bool)
    col = {k: j for j, k in enumerate(keys)}
    for vi, vid in enumerate(vids):
        for (vid_, o, d, m, v) in [c for c in cells(items, anchors) if c[0] == vid]:
            if d == 0:
                continue
            for cond in CONDS:
                for q in QUESTIONS:
                    y, y0 = M.get((vid, o, cond, d, q)), M.get((vid, o, "REF", 0, q))
                    if y is None or y0 is None:
                        complete[vi] = False
                        continue
                    j = col[(cond, q, abs(d))]
                    S[vi, j] += (y - y0) / (v - m)
                    N[vi, j] += 1
    return vids, keys, S, N, complete


def U_from(S, N, keys):
    """{(cond, q): U} where U is the mean over the three distance classes of the pooled mean uptake in that class."""
    with np.errstate(invalid="ignore", divide="ignore"):
        cls = S.sum(0) / N.sum(0)
    out = {}
    for c in CONDS:
        for q in QUESTIONS:
            out[(c, q)] = float(np.nanmean([cls[keys.index((c, q, k))] for k in CLASSES]))
    return out


def stats_of(U):
    return {"U_sam_own": U[("OWN", "sam_p")], "U_sam_swap": U[("SWAP", "sam_p")],
            "dU": U[("OWN", "sam_p")] - U[("SWAP", "sam_p")],
            "U_self_own": U[("OWN", "self")], "U_self_swap": U[("SWAP", "self")],
            "U_inf_own": U[("OWN", "sam_inf")], "U_inf_swap": U[("SWAP", "sam_inf")],
            "copy_guard": U[("OWN", "sam_inf")] - U[("OWN", "sam_p")],
            "U_inst_own": U[("OWN", "sam_i")], "U_inst_swap": U[("SWAP", "sam_i")],
            "dU_inst": U[("OWN", "sam_i")] - U[("SWAP", "sam_i")],
            "inst_minus_person_own": U[("OWN", "sam_i")] - U[("OWN", "sam_p")],
            "leak_ratio": (U[("OWN", "sam_p")] / U[("OWN", "self")]) if abs(U[("OWN", "self")]) > 1e-9 else float("nan")}


def boot(S, N, keys, seed, idx=None, n=B):
    """Point and 95% percentile CI of every statistic, resampling vignettes (the cluster: X and Y share a vignette)."""
    idx = np.arange(S.shape[0]) if idx is None else np.asarray(idx)
    point = stats_of(U_from(S[idx], N[idx], keys))
    rng = np.random.default_rng(seed)
    pick = rng.integers(0, len(idx), (n, len(idx)))
    draws = {k: [] for k in point}
    for p in pick:
        st = stats_of(U_from(S[idx[p]], N[idx[p]], keys))
        for k in point:
            draws[k].append(st[k])
    ci = {k: [float(np.nanpercentile(v, 2.5)), float(np.nanpercentile(v, 97.5))] for k, v in draws.items()}
    return point, ci


def rule(point, ci, n_complete):
    """The section 5 reading, in its order. Returns (label, reason)."""
    if n_complete < MIN_VIGNETTES:
        return "untestable", "few"
    if not ci["U_self_own"][0] > EPS:
        return "untestable", "manipulation"
    if not (point["U_sam_own"] >= BAR - EPS and ci["U_sam_own"][0] > EPS):
        return "fail", "small"
    if not (point["dU"] >= MARGIN - EPS and ci["dU"][0] > EPS):
        return "fail", "anchoring"
    if not ci["copy_guard"][0] > EPS:
        return "fail", "copy"
    return "pass", None


def map_rule(point, ci):
    """The map's event alone (no margin, no guard), reported beside the verdict and never in its place."""
    return "pass" if point["U_sam_own"] >= BAR - EPS and ci["U_sam_own"][0] > EPS else "fail"


def analyse_tables(vids, keys, S, N, complete, seed_boot):
    idx = np.flatnonzero(complete)
    point, ci = boot(S, N, keys, seed_boot, idx)
    label, reason = rule(point, ci, len(idx))
    loo = []
    for drop in idx:
        sub = idx[idx != drop]
        p2, c2 = boot(S, N, keys, seed_boot, sub)
        l2, r2 = rule(p2, c2, len(sub))
        loo.append({"dropped": vids[drop], "U_sam_own": p2["U_sam_own"], "dU": p2["dU"], "label": l2, "reason": r2})
    flips = [x["dropped"] for x in loo if (x["label"], x["reason"]) != (label, reason)]
    return {"label": label, "reason": reason, "point": point, "ci": ci, "n_complete_vignettes": int(len(idx)),
            "map_rule": map_rule(point, ci), "loo": loo, "loo_flips": flips,
            "fragile": bool(flips), "sentence": SENTENCES["pass" if label == "pass" else f"{label}_{reason}"]}


def by_class(S, N, keys, idx):
    with np.errstate(invalid="ignore", divide="ignore"):
        cls = S[idx].sum(0) / N[idx].sum(0)
    return {f"{c}|{q}|{k}": float(cls[keys.index((c, q, k))]) for c in CONDS for q in QUESTIONS for k in CLASSES}


def verify_cache(items, anchors, cache):
    by_id = {it["id"]: it for it in items}
    for j in jobs(items, anchors):
        key, vid, o, cond, d, own, alex, q, r = j
        if key in cache:
            assert cache[key].get("sha256") == content_hash(messages(by_id[vid], o, own, alex, q)), f"{key} does not match"
    extra = set(cache) - {j[0] for j in jobs(items, anchors)}
    assert not extra, f"cache holds keys the design does not: {sorted(extra)[:3]}"


def analyse():
    items, anchors = load_items()
    cache = json.loads(CACHE.read_text())
    verify_cache(items, anchors, cache)
    seed = json.loads(SEEDF.read_text())
    M = cell_means(items, anchors, cache)
    vids, keys, S, N, complete = uptake_table(items, anchors, M)
    res = analyse_tables(vids, keys, S, N, complete, seed["seed32_boot"])
    idx = np.flatnonzero(complete)
    res["by_class"] = by_class(S, N, keys, idx)
    res["calls"] = len(cache)
    res["planned_calls"] = len(jobs(items, anchors))
    res["refused"] = sum(1 for v in cache.values() if v.get("refused"))
    res["cost_usd"] = sum(v["cost"] for v in cache.values())
    res["out_of_range"] = sum(1 for v in cache.values() if not v.get("refused") and v["raw"] != v["value"])
    res["ref_cells"] = {f"{vid}|{o}|{q}": M.get((vid, o, "REF", 0, q)) for vid in vids for o in "XY" for q in QUESTIONS}
    res["anchor_vs_ref_self"] = float(np.mean([M[(vid, o, "REF", 0, "self")] - round(anchors[vid][f"m_{o}"])
                                               for vid in vids for o in "XY" if (vid, o, "REF", 0, "self") in M]))
    res["within_cell_sd_median"] = float(np.median([np.std([cache[f"{vid}|{o}|{c}|{d}|{q}|{r}"]["value"] for r in range(R)])
                                                    for (vid, o, c, d, q) in M]))
    OUT.write_text(json.dumps(res, indent=1))
    print(json.dumps({k: res[k] for k in ("label", "reason", "map_rule", "n_complete_vignettes", "loo_flips", "calls",
                                          "cost_usd")}, indent=1))
    print(json.dumps(res["point"], indent=1))
    print(json.dumps(res["ci"], indent=1))
    return res


def plan():
    items, anchors = load_items()
    cs = cells(items, anchors)
    js = jobs(items, anchors)
    n_by_d = {d: sum(1 for c in cs if c[2] == d) for d in (0,) + DS}
    print(f"item-statements: {len(items) * 2}; kept cells by d: {n_by_d}")
    print(f"calls: {len(js)} ({len(js) // R} per repeat x {R}); estimated ${len(js) * EST_COST_PER_CALL:.3f} (cap ${CAP:.2f})")


def main():
    if "plan" in sys.argv:
        return plan()
    if "--analyse" not in sys.argv:
        why = gate()
        if why:
            sys.exit(f"p2-5: not running: {why}")
        items, anchors = load_items()
        seed = json.loads(SEEDF.read_text())
        by_id = {it["id"]: it for it in items}
        c = GuardedCaller(CACHE, CAP, "p2-5 egocentric")
        c.run(jobs(items, anchors, seed["seed32_order"]), by_id)
    analyse()


if __name__ == "__main__":
    main()
