"""P2-6, is "own" a position or a label? As pre-registered in experiments/p2-6-position-or-label.md (D11).

Program 1's bm0/bm1 found that a number planted as Haiku's own earlier answer pulls its re-rating (uptake +0.44 at
+/-30) and the same number credited to another person does not (-0.11). Those two conditions differed in three things
at once: the label (yours / another person's), the position (assistant turn / user turn) and the wording ("give your
rating again" / "accept or revise"). This test fixes the wording and crosses position with label:

    AY  assistant turn, "The answer above is your earlier answer."
    AS  assistant turn, "The answer above is Sam's earlier answer."
    UY  user turn,      "The answer above is your earlier answer."
    US  user turn,      "The answer above is Sam's earlier answer."
    UU  user turn,      "The answer above is my earlier answer."      (the user's own stated answer)
    base                 the question alone (no value shown): the baseline the uptake is measured from

    python experiments/p2_6_position_label.py show        # print one conversation per cell (no API)
    python experiments/p2_6_position_label.py             # the test (cached), then analyse; gated (see gate())
    python experiments/p2_6_position_label.py --analyse

Run with program 1's interpreter: /Users/seanpharris/entangled-mind/.venv/bin/python. Items: program 1's 16 exp4 items
(programs/entangled-mind/experiments/exp4-items.json) and the archived anchor means m_X, m_Y
(exp4-run-3-anchors.json), the same as bm0. Calls cached in results/p2-6-calls.json, keyed by job and checked by a
SHA-256 of model, max_tokens and messages on every hit and again at analysis."""

import hashlib
import json
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                                     # programs/other-minds
ENGINE = ROOT.parents[1]                               # the engine repo
P1X = ROOT.parent / "entangled-mind" / "experiments"
ITEMS_PATH, ANCHORS_PATH = P1X / "exp4-items.json", P1X / "exp4-run-3-anchors.json"
RESULTS, DATA = ROOT / "results", ROOT / "data"
CACHE, OUT_JSON, OUT_MD = RESULTS / "p2-6-calls.json", RESULTS / "p2-6-position-or-label.json", RESULTS / "p2-6-tables.md"
SEEDF = DATA / "p2-6-seed.json"
REVIEW = ENGINE / "ledger" / "design-reviews" / "om-p2-6.md"
MODEL = "claude-haiku-5-5"
CAP = 0.80                                             # dollars, checked under a lock before every call
MAX_TOKENS = 200                                       # bm0's setting
REPEATS = 20
DISTANCES = (-30, 30)
MIN_D = 0.05                                           # bm0's rule: a (statement, direction) with |D| < 0.05 is dropped
MARGIN = 0.15                                          # the label effect must beat the dumb baselines' 0 by this much
MIN_REPEATS, MIN_ITEMS = 10, 12                        # untestable below these
B = 2000
EPS = 1e-9
CELLS = ("AY", "AS", "UY", "US", "UU")
SCALE = ", where 0 = certainly false and 100 = certainly true"
RATE = {"type": "object", "properties": {"probability": {"type": "integer"}}, "required": ["probability"],
        "additionalProperties": False}
LABEL = {"Y": "The answer above is your earlier answer.",
         "S": "The answer above is Sam's earlier answer.",
         "U": "The answer above is my earlier answer."}


def items():
    return json.loads(ITEMS_PATH.read_text())


def anchors():
    return json.loads(ANCHORS_PATH.read_text())


def shown_value(m, d):
    """bm0's V(): the anchor mean plus the displacement, clipped to [2, 98]."""
    return min(98, max(2, round(m) + d))


def ask(stmt, ctx):
    return f"{ctx}\n\nOn a scale from 0 to 100{SCALE}, how likely is it that {stmt}? Give only the number."


def request(stmt):
    return f"Please give the rating again. On a scale from 0 to 100{SCALE}, how likely is it that {stmt}? Give only the number."


def messages(cell, it, o, A):
    """One wording for every cell. The value is the JSON string the model itself returns, '{"probability": A}'.
    Assistant position: the value is the assistant turn; the label and the request follow in the next user turn.
    User position: question, value, label and request in one user turn, in the same order and the same words."""
    stmt, ctx = it[o], it["context"]
    if cell == "base":
        return [{"role": "user", "content": ask(stmt, ctx)}]
    pos, lab = cell[0], cell[1]
    val = json.dumps({"probability": A})
    if pos == "A":
        return [{"role": "user", "content": ask(stmt, ctx)}, {"role": "assistant", "content": val},
                {"role": "user", "content": f"{LABEL[lab]} {request(stmt)}"}]
    return [{"role": "user", "content": f"{ask(stmt, ctx)}\n\n{val}\n\n{LABEL[lab]} {request(stmt)}"}]


def content_hash(msgs):
    return hashlib.sha256(json.dumps({"model": MODEL, "max_tokens": MAX_TOKENS, "messages": msgs},
                                     sort_keys=True).encode()).hexdigest()


def jobs(its, anc, seed32_order):
    """Repeat index outermost, so a stop leaves whole repeats; within a repeat, a beacon-drawn order of its 352 jobs."""
    rng = np.random.default_rng(seed32_order)
    out = []
    for r in range(REPEATS):
        block = []
        for it in its:
            for o in ("X", "Y"):
                block.append((f"base|{it['id']}|{o}|0|{r}", "base", it, o, None))
                for d in DISTANCES:
                    A = shown_value(anc[it["id"]][f"m_{o}"], d)
                    for c in CELLS:
                        block.append((f"{c}|{it['id']}|{o}|{d}|{r}", c, it, o, A))
        out += [block[i] for i in rng.permutation(len(block))]
    return out


def job_messages(job):
    _, cell, it, o, A = job
    return messages(cell, it, o, A)


class GuardedCaller:
    """Program 2's rules (om_common.Caller, as tightened for om-p2-3b in D9): content-keyed cache; the cap checked
    under a lock before every call; stop at the first refusal or error, nothing reworded or retried; a refused job is
    written into the cache and no later run starts on a cache holding one or with results/refusal.md present; calls
    finishing after the stop are counted; every entry carries content_hash(messages), asserted on every hit."""

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
            key = job[0]
            msgs = job_messages(job)
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
                d, cost, rid = self.call_fn(msgs)
            except refusal_error as e:
                with self.lock:
                    self.cache[key] = {"refused": True, "request_id": getattr(e, "request_id", None), "cost": 0.0, "sha256": h}
                    self.refusal.setdefault("e", (key, e))
                self.stop.set()
                return
            except Exception as e:
                self.errors.append((key, repr(e)))
                self.stop.set()
                return
            with self.lock:
                if self.stop.is_set():
                    self.after_stop += 1
                self.cache[key] = {"value": min(100, max(0, int(d["probability"]))), "raw": int(d["probability"]),
                                   "cost": cost, "request_id": rid, "sha256": h}
                if len(self.cache) % 250 == 0:
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
                return "refusal"
            return reason
        print(f"{self.label}: complete, {len(self.cache)} cached calls, ${self.spent():.4f}", flush=True)
        return "complete"


def real_call():
    sys.path.insert(0, str(HERE))
    import om_common as om

    def call(msgs):
        return om.structured(msgs, RATE, "p2-6", max_tokens=MAX_TOKENS)
    call.refusal_error = om.llm.RefusalError
    return call


def gate(review=None, seedf=None):
    """No call before the design review's go (or a confirmed fix-first) and before the seed commit's seed file."""
    review, seedf = Path(review or REVIEW), Path(seedf or SEEDF)
    if not seedf.exists():
        return f"no seed file at {seedf}"
    if not review.exists():
        return f"no design review at {review}"
    head = review.read_text().split("\n---", 2)[0]
    v = (re.search(r"^verdict:\s*(\S+)", head, re.M) or [None, ""])[1]
    conf = (re.search(r"^confirmed_at:\s*(.+)$", head, re.M) or [None, "null"])[1].strip()
    if not (v == "go" or (v == "fix-first" and conf not in ("", "null"))):
        return f"design review verdict {v or '?'}" + (" (not confirmed)" if v == "fix-first" else "")
    return None


# --- analysis ---------------------------------------------------------------------------------------------------

def verify_cache(its, anc, cache):
    by = {it["id"]: it for it in its}
    for key, v in cache.items():
        cell, q, o, d, _ = key.split("|")
        A = None if cell == "base" else shown_value(anc[q][f"m_{o}"], int(d))
        assert v.get("sha256") == content_hash(messages(cell, by[q], o, A)), f"cache entry {key} does not match"


def complete_repeats(its, cache):
    n = 0
    for r in range(REPEATS):
        keys = [f"base|{it['id']}|{o}|0|{r}" for it in its for o in "XY"] + \
               [f"{c}|{it['id']}|{o}|{d}|{r}" for it in its for o in "XY" for d in DISTANCES for c in CELLS]
        if all(k in cache and not cache[k].get("refused") for k in keys):
            n += 1
        else:
            break
    return n


def item_uptakes(its, anc, cache, nrep):
    """Per item: u[cell] = sum over its kept (statement, direction) pairs of the shift toward the shown value,
    divided by the sum of |D|; D = A - b, b = the item-statement's baseline mean. Ratings on 0-1. Only the first
    nrep complete repeats are used. Returns {item: {cell: u}} for usable items, and the pairs kept/dropped."""
    out, kept, dropped = {}, 0, 0
    for it in its:
        q = it["id"]
        num, den = {c: 0.0 for c in CELLS}, 0.0
        for o in "XY":
            b = np.mean([cache[f"base|{q}|{o}|0|{r}"]["value"] for r in range(nrep)]) / 100
            for d in DISTANCES:
                A = shown_value(anc[q][f"m_{o}"], d) / 100
                D = A - b
                if abs(D) < MIN_D:
                    dropped += 1
                    continue
                kept += 1
                den += abs(D)
                for c in CELLS:
                    rbar = np.mean([cache[f"{c}|{q}|{o}|{d}|{r}"]["value"] for r in range(nrep)]) / 100
                    num[c] += (rbar - b) * np.sign(D)
        if den > 0:
            out[q] = {c: num[c] / den for c in CELLS}
    return out, kept, dropped


def contrasts(U):
    """U: array items x 5 (CELLS order). Per-item contrasts."""
    AY, AS, UY, US, UU = (U[:, i] for i in range(5))
    return {"L": ((AY - AS) + (UY - US)) / 2, "P": ((AY - UY) + (AS - US)) / 2,
            "L_A": AY - AS, "L_U": UY - US, "I": (AY - AS) - (UY - US),
            "AY": AY, "AS": AS, "UY": UY, "US": US, "UU": UU,
            "UU_minus_US": UU - US, "UY_minus_UU": UY - UU}


def summarise(U, seed32_boot):
    n = U.shape[0]
    C = contrasts(U)
    rng = np.random.default_rng(seed32_boot)
    idx = rng.integers(0, n, (B, n))
    out = {}
    for k, v in C.items():
        bs = v[idx].mean(1)
        out[k] = [float(v.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
    return out


def verdict(s):
    """§5, applied in this order. s: summarise() output (point, lo, hi)."""
    L, Ll, Lh = s["L"]
    P, Pl, Ph = s["P"]
    sigP = abs(P) >= MARGIN - EPS and (Pl > EPS or Ph < -EPS)
    if L >= MARGIN - EPS and Ll > EPS and L > abs(P) + EPS:
        return "pass"
    if sigP and abs(P) >= abs(L) - EPS:
        return "fail-position"
    if L <= -MARGIN + EPS and Lh < -EPS and abs(L) > abs(P) + EPS:
        return "fail-reversed"
    if L >= MARGIN - EPS and Ll > EPS:
        return "fail-mixed"
    return "fail-neither"


SENTENCES = {
    "pass": ("On Haiku, on program 1's 16 bm0 items at ±30 points, the label mattered more than the position. A value "
             "labelled \"your earlier answer\" was taken up more than the same value labelled \"Sam's earlier answer\", by "
             "{L} of the displacement on average over the assistant and user turns, against a position effect of {P}. "
             "On this design the pull of an earlier answer follows whose answer the transcript says it is more than which "
             "turn it sits in."),
    "fail-position": ("On Haiku, on program 1's 16 bm0 items at ±30 points, the position mattered at least as much as "
                      "the label. A value in the {more} turn was taken up more than the same value in the {less} turn, by "
                      "{Pabs} of the displacement, while the label (\"your\" against \"Sam's\") changed uptake by {L}. On "
                      "this design the pull of an earlier answer follows the turn it sits in, not whose answer it is said "
                      "to be."),
    "fail-reversed": ("On Haiku, on program 1's 16 bm0 items at ±30 points, a value labelled \"Sam's earlier answer\" was "
                      "taken up more than the same value labelled \"your earlier answer\", by {Labs} of the displacement "
                      "(position effect {P}). On this design the label works against the model's own answer, the opposite "
                      "of the self account."),
    "fail-mixed": ("On Haiku, on program 1's 16 bm0 items at ±30 points, the label changed uptake by {L} of the "
                   "displacement, but the position effect, {P}, was as large, though not itself detected at the 0.15 bar. "
                   "This test does not separate the two."),
    "fail-neither": ("On Haiku, on program 1's 16 bm0 items at ±30 points, neither the label nor the position changed "
                     "uptake by the pre-registered 0.15 of the displacement: label effect {L}, position effect {P}. This "
                     "test does not say which of the two the pull of an earlier answer follows."),
    "untestable": ("The test could not answer its question as run: {why}. No verdict is drawn."),
    "no_own_pull": ("The value labelled as the model's own and placed in its own turn was not taken up detectably "
                    "(uptake {AY}), so program 1's own-answer pull did not replicate in this wording, and the comparison "
                    "above splits an effect that was not present."),
    "fragile": ("Dropping item {item} alone changes this verdict to \"{v}\", so it rests on that item."),
    "user_like_yours": ("In the user turn, the user's own stated answer was taken up more than Sam's (by {UU_US}) and "
                        "about as much as one labelled \"yours\" (difference {UY_UU}), so the label effect may be about "
                        "Sam rather than about the self."),
    "yours_over_user": ("In the user turn, a value labelled \"yours\" was taken up more than the user's own stated answer, "
                        "by {UY_UU} of the displacement."),
    "user_unclear": ("In the user turn, the user's own stated answer could not be told apart from the other two labels "
                     "(user's minus Sam's {UU_US}; yours minus user's {UY_UU})."),
}


def fmt(x):
    return f"{x[0]:+.2f} [{x[1]:+.2f}, {x[2]:+.2f}]"


def sentence(v, s, extra=None):
    P = s["P"]
    Pabs = P if P[0] >= 0 else [-P[0], -P[2], -P[1]]
    Lneg = [-s["L"][0], -s["L"][2], -s["L"][1]]
    kw = {"L": fmt(s["L"]), "P": fmt(P), "Pabs": fmt(Pabs), "Labs": fmt(Lneg),
          "more": "assistant" if P[0] > 0 else "user", "less": "user" if P[0] > 0 else "assistant"}
    kw.update(extra or {})
    return SENTENCES[v].format(**kw)


def user_reading(s):
    a, b = s["UU_minus_US"], s["UY_minus_UU"]
    kw = {"UU_US": fmt(a), "UY_UU": fmt(b)}
    if a[0] >= MARGIN - EPS and a[1] > EPS and b[1] <= 0 <= b[2]:
        return "user_like_yours", SENTENCES["user_like_yours"].format(**kw)
    if b[0] >= MARGIN - EPS and b[1] > EPS:
        return "yours_over_user", SENTENCES["yours_over_user"].format(**kw)
    return "user_unclear", SENTENCES["user_unclear"].format(**kw)


def analyse_cache(cache, its, anc, seed32_boot, check=True):
    if check:
        verify_cache(its, anc, cache)
    nrep = complete_repeats(its, cache)
    res = {"complete_repeats": nrep, "calls_cached": len(cache), "cost_usd": sum(v["cost"] for v in cache.values()),
           "refused": sum(bool(v.get("refused")) for v in cache.values())}
    if nrep < MIN_REPEATS:
        res.update(verdict="untestable", why=f"only {nrep} complete repeats (minimum {MIN_REPEATS})")
        res["sentence"] = SENTENCES["untestable"].format(why=res["why"])
        return res
    up, kept, dropped = item_uptakes(its, anc, cache, nrep)
    res.update(pairs_kept=kept, pairs_dropped=dropped, items_usable=len(up))
    if len(up) < MIN_ITEMS:
        res.update(verdict="untestable", why=f"only {len(up)} of 16 items usable (minimum {MIN_ITEMS})")
        res["sentence"] = SENTENCES["untestable"].format(why=res["why"])
        return res
    ids = list(up)
    U = np.array([[up[q][c] for c in CELLS] for q in ids])
    s = summarise(U, seed32_boot)
    v = verdict(s)
    res.update(items=ids, item_uptakes={q: up[q] for q in ids}, stats=s, verdict=v, sentence=sentence(v, s))
    loo = {}
    for i, q in enumerate(ids):
        sl = summarise(np.delete(U, i, 0), seed32_boot)
        loo[q] = {"L": sl["L"][0], "P": sl["P"][0], "verdict": verdict(sl)}
    res["loo"] = loo
    res["loo_L_range"] = [min(x["L"] for x in loo.values()), max(x["L"] for x in loo.values())]
    flips = {q: x["verdict"] for q, x in loo.items() if x["verdict"] != v}
    res["loo_flips"] = flips
    if flips:
        q0 = sorted(flips)[0]
        res["fragile_sentence"] = SENTENCES["fragile"].format(item=q0, v=flips[q0])
    if s["AY"][1] <= EPS:
        res["no_own_pull_sentence"] = SENTENCES["no_own_pull"].format(AY=fmt(s["AY"]))
    res["user_reading"], res["user_sentence"] = user_reading(s)
    # label-swap null (secondary): swap yours/Sam's within item x position at random
    rng = np.random.default_rng(seed32_boot + 1)
    Lobs, nul = s["L"][0], []
    for _ in range(B):
        flip = rng.integers(0, 2, (len(ids), 2)).astype(bool)
        dA = np.where(flip[:, 0], -1, 1) * (U[:, 0] - U[:, 1])
        dU = np.where(flip[:, 1], -1, 1) * (U[:, 2] - U[:, 3])
        nul.append(((dA + dU) / 2).mean())
    res["label_swap_null"] = {"p_ge_obs": float(np.mean(np.array(nul) >= Lobs - EPS)),
                              "q975": float(np.percentile(nul, 97.5))}
    return res


def write_md(r):
    lines = ["# P2-6 tables (generated by experiments/p2_6_position_label.py; do not edit by hand)", "",
             f"Complete repeats {r['complete_repeats']} of {REPEATS}; calls {r['calls_cached']}; cost ${r['cost_usd']:.4f}; "
             f"refused {r['refused']}."]
    if r["verdict"] == "untestable":
        OUT_MD.write_text("\n".join(lines + ["", f"**Verdict: untestable** ({r['why']})"]) + "\n")
        return
    s = r["stats"]
    lines += [f"(statement, direction) pairs kept {r['pairs_kept']}, dropped for |D| < {MIN_D}: {r['pairs_dropped']}; "
              f"items usable {r['items_usable']} of 16.", "",
              "## Uptake by cell (share of the displacement taken up; item mean, 95% item-bootstrap CI)", "",
              "| cell | position | label | uptake |", "|---|---|---|---|"]
    names = {"AY": ("assistant", "yours"), "AS": ("assistant", "Sam's"), "UY": ("user", "yours"),
             "US": ("user", "Sam's"), "UU": ("user", "the user's")}
    for c in CELLS:
        lines.append(f"| {c} | {names[c][0]} | {names[c][1]} | {fmt(s[c])} |")
    lines += ["", "## Effects", "", "| statistic | value | role |", "|---|---|---|",
              f"| label effect L = mean of (AY − AS, UY − US) | {fmt(s['L'])} | **primary** |",
              f"| position effect P = mean of (AY − UY, AS − US) | {fmt(s['P'])} | primary (compared with L) |",
              f"| label effect in the assistant turn, AY − AS | {fmt(s['L_A'])} | secondary |",
              f"| label effect in the user turn, UY − US | {fmt(s['L_U'])} | secondary |",
              f"| interaction (AY − AS) − (UY − US) | {fmt(s['I'])} | secondary |",
              f"| user's minus Sam's, UU − US | {fmt(s['UU_minus_US'])} | secondary |",
              f"| yours minus user's, UY − UU | {fmt(s['UY_minus_UU'])} | secondary |",
              f"| label-swap null: share of swaps with L ≥ observed | {r['label_swap_null']['p_ge_obs']:.4f} "
              f"(97.5th percentile {r['label_swap_null']['q975']:+.3f}) | secondary |",
              f"| leave-one-item-out L range | {r['loo_L_range'][0]:+.3f} to {r['loo_L_range'][1]:+.3f}; "
              f"verdict flips: {len(r['loo_flips'])} | robustness |", "",
              f"**Verdict by the pre-registered rule: {r['verdict']}**", "",
              "## Per item (uptake by cell)", "", "| item | AY | AS | UY | US | UU | L | P | LOO verdict |",
              "|---|---|---|---|---|---|---|---|---|"]
    for q in r["items"]:
        u = r["item_uptakes"][q]
        Li = ((u["AY"] - u["AS"]) + (u["UY"] - u["US"])) / 2
        Pi = ((u["AY"] - u["UY"]) + (u["AS"] - u["US"])) / 2
        lines.append(f"| {q} | " + " | ".join(f"{u[c]:+.2f}" for c in CELLS) + f" | {Li:+.2f} | {Pi:+.2f} | {r['loo'][q]['verdict']} |")
    OUT_MD.write_text("\n".join(lines) + "\n")


def seeds():
    s = json.loads(SEEDF.read_text())
    return s["seed32_order"], s["seed32_boot"]


def main():
    its, anc = items(), anchors()
    if "show" in sys.argv:
        it = its[0]
        for c in ("base",) + CELLS:
            print(f"--- {c}\n" + json.dumps(messages(c, it, "X", None if c == "base" else shown_value(anc[it['id']]['m_X'], -30)), indent=1))
        return
    so, sb = seeds()
    if "--analyse" not in sys.argv:
        why = gate()
        if why:
            sys.exit(f"gate closed: {why}")
        c = GuardedCaller(CACHE, CAP, "p2-6 position x label", real_call())
        status = c.run(jobs(its, anc, so))
        print("run status:", status)
    cache = json.loads(CACHE.read_text())
    res = analyse_cache(cache, its, anc, sb)
    res["stop_record"] = json.loads(CACHE.with_name(CACHE.stem + "-stop.json").read_text()) \
        if CACHE.with_name(CACHE.stem + "-stop.json").exists() else None
    OUT_JSON.write_text(json.dumps(res, indent=1))
    write_md(res)
    print(json.dumps({k: res[k] for k in ("verdict", "sentence") if k in res}, indent=1))
    print(OUT_MD.read_text())


if __name__ == "__main__":
    main()
