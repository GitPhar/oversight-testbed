"""em-gm2q (map gm2-f1): does question order still move the final rating when the four sub-questions sit in one user
message, with no answer turns and no placeholder? Pre-registered in experiments/gm2q-questions-only.md (D64); design-review
fixes D69 (review ledger/design-reviews/em-gm2q.md, fix-first, 5 flaws).

    python experiments/gm2q_questions_only.py --print-prompts      # the exact messages, one item, all conditions; no calls
    python experiments/gm2q_questions_only.py --selftest           # estimator, verdict, target-check and boundary checks; no calls
    python experiments/gm2q_questions_only.py --dry-run            # P(pass)/P(fail) in worlds built from the gm2 and em-dm4 archives
    python experiments/gm2q_questions_only.py --run                # the paid run (cap $3.50 in code, stop on any refusal)
    python experiments/gm2q_questions_only.py --analyse --seed S   # analysis of the cache; S must be the recorded beacon seed

Conditions (gm2's 10 items, chains O1-O4, anchor (a) only, R = 10):
- shown:   gm2's turn-by-turn chain, the model sees its own real answers (the reference);
- qonly:   ONE user message: the opening, the four sub-questions verbatim in the chain's order, then the main question;
           the model returns only the main rating. No answer turns, no placeholder;
- redacted (Haiku only, secondary): gm2's "[rating recorded]" chain, re-run alongside for a same-day comparison.
Calls cached by key in results/gm2q-conversations.json (written after every conversation); refusal record
results/refusal-gm2q.md (never results/refusal.md); a run refuses to start while that record exists."""

import hashlib
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

H, S = "claude-haiku-5-5", "claude-sonnet-5-5"
SHORT = {H: "haiku", S: "sonnet"}
MODELS = [H, S]
ORDERS = ["O1", "O2", "O3", "O4"]
LATIN = [[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]       # exp5_run.LATIN, copied (asserted in --selftest)
CONDS = {H: ["qonly", "shown", "redacted"], S: ["qonly", "shown"]}     # run order within a model
R, CAP, RESERVE, WORKERS = 10, 3.50, 0.10, 8
MAXTOK = {H: 200, S: 1000}                                            # gm2's Haiku setting; em-dm4's Sonnet setting
THINKING_OFF = {H: {"type": "disabled"}, S: {"type": "between_tools"}}  # mm_common.OFF for these two models
PRICES = {H: (0.10, 0.50), S: (2.00, 10.00)}                          # config.PRICES, list price (no batches)
N_PERM, N_BOOT = 5000, 2000
ALPHA, BAR, TOL = 0.05, 0.5, 1e-9                                      # P13: every boundary compared with TOL
USABLE_MIN = 0.90                                                      # per model x condition, else untestable
WT_NEAR, WT_FAR = 5.0, 20.0                                            # D69 fix 1: the wrong-target flag
SEED_RECORDED = 17882636728661590601                                   # beacon seed (1ba7f8c); --analyse asserts it
RATING = {"type": "object", "properties": {"rating": {"type": "integer"}}, "required": ["rating"], "additionalProperties": False}
ANCHOR = "0 = certainly false, 100 = certainly true"

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent / "results"
CACHE = RESULTS / "gm2q-conversations.json"
OUT_JSON, OUT_MD = RESULTS / "gm2q-questions-only.json", RESULTS / "gm2q-questions-only-tables.md"
REFUSAL = RESULTS / "refusal-gm2q.md"
PLANTED = HERE / "gm2-planted-values.json"          # read for chain_claims only (the items' four sub-statements)
POOL = RESULTS / "pool-run-3.json"


# --- prompts --------------------------------------------------------------------------------------------------------

def opening(rec):            # exp5_run.opening(rec, "a"), copied verbatim (asserted in --print-prompts)
    return (f'We are going to think about one question in steps. The question is: "{rec["question"]}". '
            f"I will ask you to rate several statements, one at a time, and the question itself. "
            f"Give each rating as an integer from 0 to 100, where {ANCHOR}.")


def sub_q(rec, k):           # exp5_run.question(rec, "S", k)
    return f"How likely is it that this statement is true? '{rec['contentions'][k]['text']}'"


MAIN_Q = "How likely is it that the answer to the question is yes?"   # exp5_run.question(rec, "M", None)


def qonly_message(rec, claims, order):
    seq = [claims[i] for i in LATIN[int(order[1]) - 1]]
    lines = [f'We are going to think about one question in steps. The question is: "{rec["question"]}". '
             "Below are several statements, in order, and then the question itself. Think about each statement in turn, "
             f"then give a rating for the question itself only, as an integer from 0 to 100, where {ANCHOR}.", ""]
    lines += [f"{n}. {sub_q(rec, k)}" for n, k in enumerate(seq, 1)]
    lines += [f"{len(seq) + 1}. {MAIN_Q}"]
    return "\n".join(lines)


def chain_turns(rec, claims, order):
    seq = [claims[i] for i in LATIN[int(order[1]) - 1]]
    texts = [sub_q(rec, k) for k in seq] + [MAIN_Q]
    texts[0] = opening(rec) + "\n\n" + texts[0]
    return list(zip(["S"] * 4 + ["M"], seq + [None], texts))


def fourth(claims, order):
    return claims[LATIN[int(order[1]) - 1][3]]


def items():
    planted = json.loads(PLANTED.read_text())["items"]
    recs = {r["id"]: r for r in json.loads(POOL.read_text())["records"]}
    return {q: (recs[q], v["chain_claims"]) for q, v in planted.items()}


# --- calls ----------------------------------------------------------------------------------------------------------

class Refused(Exception):
    def __init__(self, model, resp, cost):
        self.model, self.request_id, self.cost = model, getattr(resp, "_request_id", None), cost
        self.stop_details = getattr(resp, "stop_details", None)
        super().__init__(f"refusal: model {model}, request {self.request_id}")


class Aborted(Exception):
    """The stop flag was set (refusal, error or cap elsewhere) before this conversation's next call: it ends unfinished."""
    def __init__(self, cost):
        self.cost = cost
        super().__init__("aborted")


def call(client, model, messages):
    resp = client.messages.create(model=model, max_tokens=MAXTOK[model], messages=messages, thinking=THINKING_OFF[model],
                                  output_config={"format": {"type": "json_schema", "schema": RATING}})
    pin, pout = PRICES[model]
    cost = (resp.usage.input_tokens * pin + resp.usage.output_tokens * pout) / 1e6
    rid = getattr(resp, "_request_id", None)
    if resp.stop_reason == "refusal":
        raise Refused(model, resp, cost)
    if resp.stop_reason == "max_tokens":
        return None, None, cost, rid
    text = "".join(b.text for b in resp.content if b.type == "text")
    try:
        return min(100, max(0, int(json.loads(text)["rating"]))), text, cost, rid
    except Exception:
        return None, text, cost, rid


def converse(client, model, rec, claims, order, cond, stop):
    cost, rids = 0.0, []

    def guarded(msgs):
        nonlocal cost
        if stop.is_set():                           # D69 fix 5: checked before every call, not only between conversations
            raise Aborted(cost)
        try:
            r, raw, c, rid = call(client, model, msgs)
        except Refused as e:
            e.cost += cost
            raise
        cost += c
        rids.append(rid)
        return r, raw

    if cond == "qonly":
        r, raw = guarded([{"role": "user", "content": qonly_message(rec, claims, order)}])
        return {"turns": [{"kind": "M", "claim": None, "rating": r, "raw": raw}], "cost": cost, "request_ids": rids,
                "missing": r is None}
    msgs, out = [], []
    for kind, k, text in chain_turns(rec, claims, order):
        msgs.append({"role": "user", "content": text})
        r, raw = guarded(msgs)
        out.append({"kind": kind, "claim": k, "rating": r, "raw": raw})
        if r is None:                               # no usable answer: the conversation stops and counts as missing
            return {"turns": out, "cost": cost, "request_ids": rids, "missing": True}
        msgs.append({"role": "assistant", "content": raw if cond == "shown" else "[rating recorded]"})
    return {"turns": out, "cost": cost, "request_ids": rids, "missing": False}


def spent_of(cache):
    """Every recorded cost, including conversations that ended unfinished ('_lost|' keys, D69 fix 5)."""
    return sum(v["cost"] for v in cache.values())


def run(client=None):
    if REFUSAL.exists():                            # D69 fix 5: a refusal on record stops every later run
        sys.exit(f"gm2q: {REFUSAL.name} exists; a refused run is never resumed, reworded or retried")
    if client is None:
        import anthropic
        from dotenv import load_dotenv
        for env in (HERE.parent / ".env", Path("/Users/seanpharris/entangled-mind/.env")):   # the key is in the old checkout
            if env.exists():
                load_dotenv(env)
        client = anthropic.Anthropic(max_retries=4)
    its = items()
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    lock, stop = threading.Lock(), threading.Event()
    state = {"refusal": None, "error": None, "cap": False}

    def save():
        CACHE.write_text(json.dumps(cache))

    def work(job):
        key, model, q, order, cond = job
        if key in cache or stop.is_set():
            return
        with lock:
            if spent_of(cache) + RESERVE >= CAP - TOL:   # cap in code: never start a conversation within $0.10 of $3.50
                state["cap"] = True
                stop.set()
                return
        rec, claims = its[q]
        try:
            res = converse(client, model, rec, claims, order, cond, stop)
        except Refused as e:
            stop.set()
            with lock:
                state["refusal"] = state["refusal"] or (key, e)
                cache[f"_lost|{key}"] = {"cost": e.cost, "lost": "refused"}
                save()
            return
        except Aborted as e:
            with lock:
                if e.cost:
                    cache[f"_lost|{key}"] = {"cost": e.cost, "lost": "aborted"}
                    save()
            return
        except Exception as e:
            stop.set()
            with lock:
                state["error"] = state["error"] or (key, repr(e))
            return
        with lock:
            cache[key] = res
            save()                                  # D69 fix 5: after every conversation
            n = sum(1 for k in cache if not k.startswith("_"))
            if n % 50 == 0:
                print(f"gm2q: {n} done, ${spent_of(cache):.3f}", flush=True)

    for model in MODELS:                            # Haiku first, then Sonnet; within a model qonly, shown, (redacted)
        for cond in CONDS[model]:
            jobs = [(f"{SHORT[model]}|{q}|{o}|{cond}|{r}", model, q, o, cond) for q in its for o in ORDERS for r in range(R)]
            with ThreadPoolExecutor(max_workers=WORKERS) as ex:
                list(ex.map(work, jobs))
            save()
            print(f"gm2q: {SHORT[model]} {cond} finished; total ${spent_of(cache):.4f}", flush=True)
            if stop.is_set():
                break
        if stop.is_set():
            break
    save()
    if state["refusal"]:
        key, e = state["refusal"]
        REFUSAL.write_text(f"# em-gm2q stopped on a refusal\n\nJob `{key}`, model `{e.model}`\n\nRequest ID: `{e.request_id}`\n\n"
                           f"Exact stop details:\n\n```\n{e.stop_details}\n```\n\nNothing was reworded or retried; every "
                           "conversation in flight ended before its next call, and no later run starts while this file exists.\n")
        sys.exit(f"STOPPED on a refusal: {e}")
    if state["error"]:
        sys.exit(f"gm2q: stopped on an error: {state['error']}")
    if state["cap"]:
        sys.exit(f"gm2q: budget cap ${CAP} (reserve ${RESERVE}) reached; stopped. Spent ${spent_of(cache):.4f}")
    print(f"gm2q: complete, ${spent_of(cache):.4f}")


# --- analysis -------------------------------------------------------------------------------------------------------

def vc(groups):
    """gm2_self_conditioning.vc, copied: (between-order variance component clipped at 0, MS_between)."""
    groups = [np.asarray(g, float) for g in groups if len(g)]
    n = np.mean([len(g) for g in groups])
    allv = np.concatenate(groups)
    msb = sum(len(g) * (g.mean() - allv.mean()) ** 2 for g in groups) / (len(groups) - 1)
    msw = sum(((g - g.mean()) ** 2).sum() for g in groups) / (len(allv) - len(groups))
    return max(0.0, (msb - msw) / n), msb


def oe(data, qs):
    """data[q] = four lists of final ratings (O1..O4). OE = sqrt(mean over items of the variance component)."""
    return float(np.sqrt(np.mean([vc(data[q])[0] for q in qs])))


def perm_p(data, qs, seed, n_perm=None):
    """Permutation test of sum over items of MS_between, order labels shuffled within item (vectorised; same statistic as
    gm2's loop). p = (1 + #{T* >= T - TOL}) / (n_perm + 1)."""
    n_perm = n_perm or N_PERM
    rng = np.random.default_rng(seed)
    T = sum(vc(data[q])[1] for q in qs)
    null = np.zeros(n_perm)
    for q in qs:
        g = [np.asarray(x, float) for x in data[q] if len(x)]
        v, sizes = np.concatenate(g), np.array([len(x) for x in g])
        pv = v[np.argsort(rng.random((n_perm, len(v))), axis=1)]
        b = np.concatenate([[0], np.cumsum(sizes)])
        means = np.stack([pv[:, b[i]:b[i + 1]].mean(1) for i in range(len(g))], 1)
        null += (sizes * (means - v.mean()) ** 2).sum(1) / (len(g) - 1)
    return float((1 + np.sum(null >= T - TOL)) / (n_perm + 1))


def ratio_boot(dq, ds, qs, seed, n_boot=None):
    """R = OE(qonly)/OE(shown) and its 95% item-bootstrap percentile interval (items resampled with replacement;
    resamples where OE(shown) is 0 are dropped and counted)."""
    n_boot = n_boot or N_BOOT
    rng = np.random.default_rng(seed)
    vq, vs = np.array([vc(dq[q])[0] for q in qs]), np.array([vc(ds[q])[0] for q in qs])
    point = float(np.sqrt(vq.mean()) / np.sqrt(vs.mean())) if vs.mean() > 0 else float("nan")
    idx = rng.integers(0, len(qs), (n_boot, len(qs)))
    num, den = np.sqrt(vq[idx].mean(1)), np.sqrt(vs[idx].mean(1))
    ok = den > 0
    vals = num[ok] / den[ok]
    lo, hi = (map(float, np.percentile(vals, [2.5, 97.5])) if len(vals) else (float("nan"), float("nan")))
    return {"R": point, "lo": lo, "hi": hi, "dropped": int((~ok).sum())}


def model_label(gate_shown, p_q, p_q_clean, r_lo, usable_ok):
    """Pre-registered per-model reading (§5, with D69 fix 1). Every comparison carries TOL (P13).
    p_q_clean is the qonly gate with wrong-target conversations dropped (None if a cell kept < 2 ratings: fail)."""
    if not usable_ok or not (gate_shown <= ALPHA - TOL):
        return "untestable"
    if (p_q <= ALPHA - TOL and p_q_clean is not None and p_q_clean <= ALPHA - TOL
            and r_lo == r_lo and r_lo >= BAR - TOL):
        return "pass"
    return "fail"


def bet_verdict(labels):
    """labels: {model: pass|fail|untestable}. pass: both pass. mixed: exactly one passes. fail: both testable, neither
    passes. untestable: no model passes and at least one is untestable."""
    v = list(labels.values())
    if all(x == "pass" for x in v):
        return "pass"
    if any(x == "pass" for x in v):
        return "mixed"
    if all(x == "fail" for x in v):
        return "fail"
    return "untestable"


def sentence_key(res):
    """Which pre-registered §5 sentence the write-up uses (D69 fix 3)."""
    v, m = res["verdict"], res["models"]
    if v != "fail":
        return v
    gate_any = any(x.get("qonly_p", 1) <= ALPHA - TOL for x in m.values())
    if gate_any:
        return "fail-short"
    red = m.get("haiku", {}).get("ratio_redacted_shown")
    return "fail-dies-placeholder" if red and red["lo"] == red["lo"] and red["lo"] >= BAR - TOL else "fail-dies-no-repeat"


def cell(cache, model, q, order, cond):
    out = []
    for r in range(R):
        c = cache.get(f"{SHORT[model]}|{q}|{order}|{cond}|{r}")
        if c and not c["missing"]:
            out.append(c)
    return out


def wrong_target(rating, stmt_mean, final_mean):
    """D69 fix 1: within 5 points of the 4th-placed statement's mean shown rating and more than 20 points from the
    item's mean shown final rating."""
    return abs(rating - stmt_mean) <= WT_NEAR + TOL and abs(rating - final_mean) > WT_FAR + TOL


def analyse_model(cache, model, qs, claims, seed):
    convs = {cond: {q: [cell(cache, model, q, o, cond) for o in ORDERS] for q in qs} for cond in CONDS[model]}
    d = {cond: {q: [[c["turns"][-1]["rating"] for c in x] for x in convs[cond][q]] for q in qs} for cond in CONDS[model]}
    usable = {cond: sum(len(x) for q in qs for x in d[cond][q]) / (len(qs) * 4 * R) for cond in CONDS[model]}
    usable_ok = all(usable[c] >= USABLE_MIN - TOL for c in ("shown", "qonly"))
    if not usable_ok or any(len(x) < 2 for c in ("shown", "qonly") for q in qs for x in d[c][q]):
        return {"usable": usable, "label": "untestable",
                "reason": "usable share below 0.90, or a shown or qonly cell with fewer than 2 ratings"}
    # today's shown means: each statement's sub-rating, and each item's final rating (D69 fix 1)
    stmt = {q: {k: float(np.mean([t["rating"] for x in convs["shown"][q] for c in x for t in c["turns"]
                                  if t["kind"] == "S" and t["claim"] == k])) for k in claims[q]} for q in qs}
    fin = {q: float(np.mean([r for x in d["shown"][q] for r in x])) for q in qs}
    flag = lambda cond: {q: [[wrong_target(r, stmt[q][fourth(claims[q], o)], fin[q]) for r in d[cond][q][j]]
                             for j, o in enumerate(ORDERS)] for q in qs}
    fq, fs = flag("qonly"), flag("shown")
    share = lambda f: float(np.mean([b for q in qs for x in f[q] for b in x]))
    clean = {q: [[r for r, b in zip(d["qonly"][q][j], fq[q][j]) if not b] for j in range(4)] for q in qs}
    clean_ok = all(len(x) >= 2 for q in qs for x in clean[q])
    out = {"usable": usable,
           "gate_shown_p": perm_p(d["shown"], qs, seed + 1),
           "qonly_p": perm_p(d["qonly"], qs, seed + 2),
           "qonly_p_clean": perm_p(clean, qs, seed + 6) if clean_ok else None,
           "wrong_target_share": {"qonly": share(fq), "shown": share(fs)},
           "OE": {c: oe(d[c], qs) for c in CONDS[model]},
           "ratio": ratio_boot(d["qonly"], d["shown"], qs, seed + 3)}
    out["label"] = model_label(out["gate_shown_p"], out["qonly_p"], out["qonly_p_clean"], out["ratio"]["lo"], usable_ok)
    out["within_sd"] = {c: float(np.sqrt(np.mean([np.var(x, ddof=1) for q in qs for x in d[c][q] if len(x) > 1])))
                        for c in CONDS[model]}
    out["per_item"] = {q: {c: {"OE": float(np.sqrt(vc(d[c][q])[0])), "means": [float(np.mean(x)) for x in d[c][q]]}
                           for c in CONDS[model]} for q in qs}
    dev = lambda c: np.concatenate([np.array(out["per_item"][q][c]["means"]) - np.mean(out["per_item"][q][c]["means"]) for q in qs])
    out["pattern_r_shown_qonly"] = float(np.corrcoef(dev("shown"), dev("qonly"))[0, 1])
    if "redacted" in CONDS[model] and usable.get("redacted", 0) >= USABLE_MIN - TOL:
        out["ratio_redacted_shown"] = ratio_boot(d["redacted"], d["shown"], qs, seed + 4)
        out["ratio_qonly_redacted"] = ratio_boot(d["qonly"], d["redacted"], qs, seed + 5)
    loo = {}
    for q in qs:
        s = [x for x in qs if x != q]
        g, p = perm_p(d["shown"], s, seed + 1), perm_p(d["qonly"], s, seed + 2)
        pc = perm_p(clean, s, seed + 6) if clean_ok else None
        rb = ratio_boot(d["qonly"], d["shown"], s, seed + 3)
        loo[q] = {"label": model_label(g, p, pc, rb["lo"], True), "R": rb["R"], "lo": rb["lo"], "qonly_p": p, "gate": g}
    out["loo"] = loo
    out["loo_flips"] = [q for q, v in loo.items() if v["label"] != out["label"]]
    return out


def archived_secondaries(qs):
    """Reported only: OE in the archived gm2 (Haiku, R = 10) and em-dm4 (Sonnet, R = 4) shown and redacted chains."""
    out = {}
    g2 = json.loads((RESULTS / "gm2-conversations.json").read_text())
    dm4 = json.loads((RESULTS / "mm-gm2-sonnet-conversations.json").read_text())
    for name, conv, reps in (("haiku_gm2", g2, 10), ("sonnet_dm4", dm4, 4)):
        out[name] = {}
        for cond in ("shown", "redacted"):
            data = {q: [[conv[f"{q}|{o}|{cond}|{r}"]["turns"][-1]["rating"] for r in range(reps) if f"{q}|{o}|{cond}|{r}" in conv]
                        for o in ORDERS] for q in qs}
            out[name][cond] = oe(data, qs)
    return out


def analyse(seed):
    assert seed == SEED_RECORDED, f"--seed must be the recorded beacon seed {SEED_RECORDED}"
    cache = json.loads(CACHE.read_text())
    its = items()
    qs, claims = list(its), {q: v[1] for q, v in its.items()}
    seed = seed % (2 ** 63)
    res = {"seed": seed, "n_conversations": sum(1 for k in cache if not k.startswith("_")),
           "n_lost": sum(1 for k in cache if k.startswith("_")), "cost_usd": spent_of(cache),
           "cache_sha256": hashlib.sha256(CACHE.read_bytes()).hexdigest(),
           "models": {SHORT[m]: analyse_model(cache, m, qs, claims, seed) for m in MODELS}}
    res["verdict"] = bet_verdict({m: v["label"] for m, v in res["models"].items()})
    res["sentence"] = sentence_key(res)
    res["archived"] = archived_secondaries(qs)
    OUT_JSON.write_text(json.dumps(res, indent=1))
    write_tables(res)
    return res


def write_tables(r):
    f = lambda x: f"{x:.2f}"
    L = ["# em-gm2q tables (generated by experiments/gm2q_questions_only.py --analyse; do not edit)", "",
         f"{r['n_conversations']} conversations ({r['n_lost']} unfinished), ${r['cost_usd']:.4f}; seed {r['seed']}; "
         f"cache sha256 `{r['cache_sha256']}`.", "",
         "| model | usable shown / qonly | gate p (shown) | p (qonly) | p (qonly, wrong-target dropped) | wrong-target share qonly / shown | OE shown | OE qonly | **R = qonly / shown** | label | LOO flips |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for m, v in r["models"].items():
        if "OE" not in v:
            L.append(f"| {m} | {v['usable']} | — | — | — | — | — | — | — | {v['label']} | — |")
            continue
        ra, wt = v["ratio"], v["wrong_target_share"]
        pc = "— (a cell kept < 2)" if v["qonly_p_clean"] is None else f"{v['qonly_p_clean']:.4f}"
        L.append(f"| {m} | {v['usable']['shown']:.0%} / {v['usable']['qonly']:.0%} | {v['gate_shown_p']:.4f} | {v['qonly_p']:.4f} | "
                 f"{pc} | {wt['qonly']:.1%} / {wt['shown']:.1%} | {v['OE']['shown']:.1f} | {v['OE']['qonly']:.1f} | "
                 f"**{f(ra['R'])} [{f(ra['lo'])}, {f(ra['hi'])}]** | {v['label']} | {', '.join(v['loo_flips']) or 'none'} |")
    L += ["", f"**Bet verdict (pre-registered rule): {r['verdict']}**; §5 sentence: `{r['sentence']}`", "",
          "## Secondary (reported, never promoted)", ""]
    for m, v in r["models"].items():
        if "OE" not in v:
            continue
        L.append(f"- {m}: within-order SD " + ", ".join(f"{c} {s:.1f}" for c, s in v["within_sd"].items())
                 + f"; order-pattern correlation shown vs qonly {v['pattern_r_shown_qonly']:.2f}"
                 + (f"; OE redacted {v['OE']['redacted']:.1f}, R redacted/shown {f(v['ratio_redacted_shown']['R'])} "
                    f"[{f(v['ratio_redacted_shown']['lo'])}, {f(v['ratio_redacted_shown']['hi'])}], R qonly/redacted "
                    f"{f(v['ratio_qonly_redacted']['R'])} [{f(v['ratio_qonly_redacted']['lo'])}, {f(v['ratio_qonly_redacted']['hi'])}]"
                    if "ratio_redacted_shown" in v else ""))
    for name, v in r["archived"].items():
        L.append(f"- archived {name}: OE shown {v['shown']:.1f}, OE redacted {v['redacted']:.1f}")
    for m, v in r["models"].items():
        if "per_item" not in v:
            continue
        conds = list(v["per_item"][next(iter(v["per_item"]))])
        L += ["", f"### Per item, {m}", "", "| item | " + " | ".join(f"OE {c}" for c in conds) + " | " +
              " | ".join(f"final M by order O1–O4, {c}" for c in conds) + " | LOO label (R lo) |",
              "|---|" + "---|" * (2 * len(conds) + 1)]
        for q, pi in v["per_item"].items():
            L.append(f"| {q} | " + " | ".join(f"{pi[c]['OE']:.1f}" for c in conds) + " | " +
                     " | ".join(", ".join(f"{x:.0f}" for x in pi[c]["means"]) for c in conds) +
                     f" | {v['loo'][q]['label']} ({f(v['loo'][q]['lo'])}) |")
    OUT_MD.write_text("\n".join(L) + "\n")
    print("\n".join(L))


# --- self-test and dry run (no calls) -------------------------------------------------------------------------------

def synthetic_cache(rng, qs, claims, stmt_means, shown_means, q_means, sd, wt_frac=0.0, conds=("qonly", "shown")):
    """A cache in the run's format for model H: shown chains with sub-ratings and finals; qonly finals, of which a share
    wt_frac are replaced by the 4th-placed statement's rating (a wrong-target responder)."""
    cache, rnd = {}, lambda m: int(np.clip(np.rint(rng.normal(m, sd)), 0, 100))
    for q in qs:
        for j, o in enumerate(ORDERS):
            for r in range(R):
                if "shown" in conds:
                    seq = [claims[q][i] for i in LATIN[j]]
                    turns = [{"kind": "S", "claim": k, "rating": int(np.clip(np.rint(rng.normal(stmt_means[q][k], 3)), 0, 100))}
                             for k in seq] + [{"kind": "M", "claim": None, "rating": rnd(shown_means[q][j])}]
                    cache[f"haiku|{q}|{o}|shown|{r}"] = {"turns": turns, "cost": 0, "missing": False}
                if rng.random() < wt_frac:
                    v = int(np.clip(np.rint(rng.normal(stmt_means[q][fourth(claims[q], o)], 2)), 0, 100))
                else:
                    v = rnd(q_means[q][j])
                cache[f"haiku|{q}|{o}|qonly|{r}"] = {"turns": [{"kind": "M", "claim": None, "rating": v}], "cost": 0,
                                                     "missing": False}
    return cache


def selftest():
    import exp5_run as er
    global CONDS
    assert er.LATIN == LATIN and er.ANCHORS["a"] == ANCHOR
    rng = np.random.default_rng(0)
    qs = [f"q{i}" for i in range(10)]
    flat = {q: [list(rng.normal(50, 5, R)) for _ in ORDERS] for q in qs}
    shifted = {q: [list(rng.normal(50 + 10 * j, 5, R)) for j in range(4)] for q in qs}
    assert oe(flat, qs) < 3 and 9 < oe(shifted, qs) < 16, (oe(flat, qs), oe(shifted, qs))
    assert perm_p(shifted, qs, 1) < 0.01 and perm_p(flat, qs, 1) > 0.01
    rb = ratio_boot(shifted, shifted, qs, 2)
    assert abs(rb["R"] - 1) < 1e-12 and rb["lo"] <= 1 + 1e-12
    # boundaries exactly on each bar (P13): p = 0.05 is not < 0.05; R lower bound = 0.5 passes
    assert model_label(0.05, 0.01, 0.01, 0.9, True) == "untestable"
    assert model_label(0.01, 0.05, 0.01, 0.9, True) == "fail"
    assert model_label(0.01, 0.01, 0.05, 0.9, True) == "fail"
    assert model_label(0.01, 0.01, None, 0.9, True) == "fail"
    assert model_label(0.01, 0.0499, 0.0499, 0.5, True) == "pass"
    assert model_label(0.01, 0.0499, 0.0499, 0.5 - 1e-6, True) == "fail"
    assert model_label(0.01, 0.01, 0.01, float("nan"), True) == "fail"
    assert model_label(0.01, 0.01, 0.01, 0.9, False) == "untestable"
    assert wrong_target(55, 50, 20) and wrong_target(45, 50, 20) and not wrong_target(55.5, 50, 20)
    assert not wrong_target(50, 50, 30) and wrong_target(50, 50, 29.5)
    for labels, want in [({"h": "pass", "s": "pass"}, "pass"), ({"h": "pass", "s": "fail"}, "mixed"),
                         ({"h": "untestable", "s": "pass"}, "mixed"), ({"h": "fail", "s": "fail"}, "fail"),
                         ({"h": "fail", "s": "untestable"}, "untestable"), ({"h": "untestable", "s": "untestable"}, "untestable")]:
        assert bet_verdict(labels) == want, (labels, want)
    for m, want in [({"haiku": {"qonly_p": 0.3, "ratio_redacted_shown": {"lo": 0.7}}, "sonnet": {"qonly_p": 0.4}}, "fail-dies-placeholder"),
                    ({"haiku": {"qonly_p": 0.3, "ratio_redacted_shown": {"lo": 0.3}}, "sonnet": {"qonly_p": 0.4}}, "fail-dies-no-repeat"),
                    ({"haiku": {"qonly_p": 0.01}, "sonnet": {"qonly_p": 0.4}}, "fail-short")]:
        assert sentence_key({"verdict": "fail", "models": m}) == want
    # D69 fix 1: a no-effect world where 30% of qonly answers are the 4th statement's rating must fail;
    # the same world with a real, aligned order effect and no wrong-target answers must pass.
    CONDS = {**CONDS, H: ["qonly", "shown"]}
    claims = {q: [0, 1, 2, 3] for q in qs}
    stmt = {q: {0: 5, 1: 15, 2: 85, 3: 95} for q in qs}       # two lean no, two lean yes, as the items do
    nul = {q: [50] * 4 for q in qs}
    eff = {q: [50 + 12 * (j - 1.5) * (1 if i % 2 else -1) for j in range(4)] for i, q in enumerate(qs)}
    wt = analyse_model(synthetic_cache(np.random.default_rng(5), qs, claims, stmt, nul, nul, 4, 0.30), H, qs, claims, 11)
    assert wt["qonly_p"] < 0.05 and wt["label"] == "untestable", wt["label"]   # shown has no effect -> untestable
    wt2 = analyse_model(synthetic_cache(np.random.default_rng(6), qs, claims, stmt, eff, nul, 4, 0.30), H, qs, claims, 11)
    assert wt2["qonly_p"] < 0.05, wt2["qonly_p"]
    assert wt2["label"] == "fail", (wt2["label"], wt2["qonly_p_clean"], wt2["wrong_target_share"])
    ok = analyse_model(synthetic_cache(np.random.default_rng(7), qs, claims, stmt, eff, eff, 4, 0.0), H, qs, claims, 11)
    assert ok["label"] == "pass", (ok["label"], ok["ratio"], ok["qonly_p_clean"])
    print("selftest: all checks hold (wrong-target world with 30%: qonly gate", f"{wt2['qonly_p']:.4f}", "raw,",
          f"{wt2['qonly_p_clean']}", "after dropping", f"{wt2['wrong_target_share']['qonly']:.0%}", "flagged -> fail)")


def archive_world(model):
    """Measured numbers from the archives (P15): per item, the shown and redacted order deviations shrunk to the
    variance-corrected order effect (D69 fix 4: sample means at R = 4 or 10 carry noise), each statement's mean shown
    sub-rating, and the pooled within-order SD."""
    its = json.loads(PLANTED.read_text())["items"]
    qs, claims = list(its), {q: v["chain_claims"] for q, v in its.items()}
    if model == H:
        conv, reps = json.loads((RESULTS / "gm2-conversations.json").read_text()), 10
    else:
        conv, reps = json.loads((RESULTS / "mm-gm2-sonnet-conversations.json").read_text()), 4
    w = {"qs": qs, "claims": claims}
    for cond in ("shown", "redacted"):
        data = {q: [[conv[f"{q}|{o}|{cond}|{r}"]["turns"][-1]["rating"] for r in range(reps) if f"{q}|{o}|{cond}|{r}" in conv]
                    for o in ORDERS] for q in qs}
        grand, dev = {}, {}
        for q in qs:
            m = np.array([np.mean(x) for x in data[q]])
            n = np.mean([len(x) for x in data[q]])
            v_c, msb = vc(data[q])
            shrink = np.sqrt(v_c / (msb / n)) if msb > 0 else 0.0
            grand[q], dev[q] = float(m.mean()), list((m - m.mean()) * shrink)
        w[cond] = {"grand": grand, "dev": dev, "oe": oe(data, qs),
                   "sd": float(np.sqrt(np.mean([np.var(x, ddof=1) for q in qs for x in data[q]])))}
    w["stmt"] = {q: {k: float(np.mean([t["rating"] for key, c in conv.items() if key.startswith(f"{q}|O") and "|shown|" in key
                                         for t in c["turns"] if t["kind"] == "S" and t["claim"] == k])) for k in claims[q]}
                 for q in qs}
    return w


def dry_run(n_sims=200, n_perm=400, n_boot=400):
    """P(pass) per model and for the bet, in worlds built from measured archive numbers (D69 fix 4)."""
    global CONDS
    saved = dict(CONDS)
    CONDS = {H: ["qonly", "shown"], S: ["qonly", "shown"]}
    rng = np.random.default_rng(20261105)
    out = {"_note": f"{n_sims} simulated runs per world; {n_perm} permutations, {n_boot} bootstraps; order deviations shrunk "
                    "to the variance-corrected OE; wrong-target answers set to the 4th statement's archived mean rating"}
    worlds = ["null", "half", "0.75", "equal", "redacted pattern", "shuffled items, equal", "shuffled items, 1.5x",
              "wrong-target 0.1", "wrong-target 0.2", "wrong-target 0.3"]
    for model in MODELS:
        w = archive_world(model)
        qs, claims, g, dev = w["qs"], w["claims"], w["shown"]["grand"], w["shown"]["dev"]
        means = lambda a, d=dev: {q: [g[q] + a * x for x in d[q]] for q in qs}
        shown = means(1.0)
        res = {"within_sd_shown": w["shown"]["sd"], "oe_shown_measured": w["shown"]["oe"]}
        for name in worlds:
            labs = []
            for i in range(n_sims):
                if name.startswith("shuffled"):
                    perm = list(rng.permutation(qs))
                    a = 1.5 if "1.5" in name else 1.0
                    qm = {q: [g[q] + a * x for x in dev[p]] for q, p in zip(qs, perm)}
                elif name == "redacted pattern":
                    qm = {q: [g[q] + x for x in w["redacted"]["dev"][q]] for q in qs}
                else:
                    qm = means({"null": 0.0, "half": 0.5, "0.75": 0.75, "equal": 1.0}.get(name, 0.0))
                f = float(name.split()[-1]) if name.startswith("wrong") else 0.0
                c = synthetic_cache(rng, qs, claims, w["stmt"], shown, qm, w["shown"]["sd"], f)
                d = {cond: {q: [[cc["turns"][-1]["rating"] for cc in cell(c, H, q, o, cond)] for o in ORDERS] for q in qs}
                     for cond in ("shown", "qonly")}
                stmt = {q: {k: float(np.mean([t["rating"] for o in ORDERS for cc in cell(c, H, q, o, "shown") for t in cc["turns"]
                                               if t["kind"] == "S" and t["claim"] == k])) for k in claims[q]} for q in qs}
                fin = {q: float(np.mean([r for x in d["shown"][q] for r in x])) for q in qs}
                clean = {q: [[r for r in d["qonly"][q][j] if not wrong_target(r, stmt[q][fourth(claims[q], o)], fin[q])]
                             for j, o in enumerate(ORDERS)] for q in qs}
                pc = perm_p(clean, qs, i + 3, n_perm) if all(len(x) >= 2 for q in qs for x in clean[q]) else None
                rb = ratio_boot(d["qonly"], d["shown"], qs, i + 2, n_boot)
                labs.append(model_label(perm_p(d["shown"], qs, i, n_perm), perm_p(d["qonly"], qs, i + 1, n_perm), pc, rb["lo"], True))
            res[name] = {k: labs.count(k) / n_sims for k in ("pass", "fail", "untestable")}
            print(f"dry run {SHORT[model]:6s} {name:24s} " + "  ".join(f"{k} {v:.3f}" for k, v in res[name].items()), flush=True)
        out[SHORT[model]] = res
    for name in worlds:
        out.setdefault("bet", {})[name] = out["haiku"][name]["pass"] * out["sonnet"][name]["pass"]
        print(f"dry run bet  {name:24s} P(pass, both, independent) {out['bet'][name]:.3f}")
    CONDS = saved
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--print-prompts" in a:
        import exp5_run as er
        its = items()
        rec, claims = its["h190"]
        assert opening(rec) == er.opening(rec, "a") and sub_q(rec, claims[0]) == er.question(rec, "S", claims[0])
        assert MAIN_Q == er.question(rec, "M", None)
        assert [k for _, k, _ in chain_turns(rec, claims, "O2")][:4] == [kk for kind, kk in er.turns_for("O2", claims) if kind == "S"]
        for o in ORDERS:
            print(f"--- qonly {o} ---\n{qonly_message(rec, claims, o)}\n")
        print("--- shown/redacted O1 turns ---")
        for t in chain_turns(rec, claims, "O1"):
            print(t)
        assert len({qonly_message(rec, claims, o) for o in ORDERS}) == 4
        print("prompts: openings and questions match exp5_run; the four qonly messages differ")
    elif "--selftest" in a:
        selftest()
    elif "--dry-run" in a:
        res = dry_run()
        (RESULTS / "gm2q-dry-run.json").write_text(json.dumps(res, indent=1) + "\n")
    elif "--run" in a:
        run()
    elif "--analyse" in a:
        analyse(int(a[a.index("--seed") + 1]))
    else:
        print(__doc__)
