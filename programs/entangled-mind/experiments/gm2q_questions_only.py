"""em-gm2q (map gm2-f1): does question order still move the final rating when the four sub-questions sit in one user
message, with no answer turns and no placeholder? Pre-registered in experiments/gm2q-questions-only.md (D62).

    python experiments/gm2q_questions_only.py --print-prompts      # the exact messages, one item, all conditions; no calls
    python experiments/gm2q_questions_only.py --selftest           # estimator, verdict and boundary checks; no calls, no archive
    python experiments/gm2q_questions_only.py --dry-run            # P(pass)/P(fail) in worlds built from the gm2 and em-dm4 archives
    python experiments/gm2q_questions_only.py --run                # the paid run (cap $3.50 in code, stop on any refusal)
    python experiments/gm2q_questions_only.py --analyse --seed S   # analysis of the cache with the beacon seed

Conditions (gm2's 10 items, chains O1-O4, anchor (a) only, R = 10):
- shown:   gm2's turn-by-turn chain, the model sees its own real answers (the reference);
- qonly:   ONE user message: the opening, the four sub-questions verbatim in the chain's order, then the main question;
           the model returns only the main rating. No answer turns, no placeholder;
- redacted (Haiku only, secondary): gm2's "[rating recorded]" chain, re-run alongside for a same-day comparison.
Calls cached by key in results/gm2q-conversations.json; refusal record results/refusal-gm2q.md; never results/refusal.md."""

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


def items():
    planted = json.loads(PLANTED.read_text())["items"]
    recs = {r["id"]: r for r in json.loads(POOL.read_text())["records"]}
    return {q: (recs[q], v["chain_claims"]) for q, v in planted.items()}


# --- calls ----------------------------------------------------------------------------------------------------------

class Refused(Exception):
    def __init__(self, model, resp):
        self.model, self.request_id = model, getattr(resp, "_request_id", None)
        self.stop_details = getattr(resp, "stop_details", None)
        super().__init__(f"refusal: model {model}, request {self.request_id}")


def call(client, model, messages):
    resp = client.messages.create(model=model, max_tokens=MAXTOK[model], messages=messages, thinking=THINKING_OFF[model],
                                  output_config={"format": {"type": "json_schema", "schema": RATING}})
    pin, pout = PRICES[model]
    cost = (resp.usage.input_tokens * pin + resp.usage.output_tokens * pout) / 1e6
    rid = getattr(resp, "_request_id", None)
    if resp.stop_reason == "refusal":
        raise Refused(model, resp)
    if resp.stop_reason == "max_tokens":
        return None, None, cost, rid
    text = "".join(b.text for b in resp.content if b.type == "text")
    try:
        return min(100, max(0, int(json.loads(text)["rating"]))), text, cost, rid
    except Exception:
        return None, text, cost, rid


def converse(client, model, rec, claims, order, cond):
    cost, rids = 0.0, []
    if cond == "qonly":
        r, raw, c, rid = call(client, model, [{"role": "user", "content": qonly_message(rec, claims, order)}])
        return {"turns": [{"kind": "M", "claim": None, "rating": r, "raw": raw}], "cost": c, "request_ids": [rid],
                "missing": r is None}
    msgs, out = [], []
    for kind, k, text in chain_turns(rec, claims, order):
        msgs.append({"role": "user", "content": text})
        r, raw, c, rid = call(client, model, msgs)
        cost += c
        rids.append(rid)
        out.append({"kind": kind, "claim": k, "rating": r, "raw": raw})
        if r is None:                               # no usable answer: the conversation stops and counts as missing
            return {"turns": out, "cost": cost, "request_ids": rids, "missing": True}
        msgs.append({"role": "assistant", "content": raw if cond == "shown" else "[rating recorded]"})
    return {"turns": out, "cost": cost, "request_ids": rids, "missing": False}


def run():
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
    spent = lambda: sum(v["cost"] for v in cache.values())

    def work(job):
        key, model, q, order, cond = job
        if key in cache or stop.is_set():
            return
        with lock:
            if spent() + RESERVE >= CAP - TOL:      # cap in code: never start a conversation within $0.10 of $3.50
                state["cap"] = True
                stop.set()
                return
        rec, claims = its[q]
        try:
            res = converse(client, model, rec, claims, order, cond)
        except Refused as e:
            state["refusal"] = state["refusal"] or (key, e)
            stop.set()
            return
        except Exception as e:
            state["error"] = state["error"] or (key, repr(e))
            stop.set()
            return
        with lock:
            cache[key] = res
            if len(cache) % 50 == 0:
                CACHE.write_text(json.dumps(cache))
                print(f"gm2q: {len(cache)} done, ${spent():.3f}", flush=True)

    for model in MODELS:                            # Haiku first, then Sonnet; within a model qonly, shown, (redacted)
        for cond in CONDS[model]:
            jobs = [(f"{SHORT[model]}|{q}|{o}|{cond}|{r}", model, q, o, cond) for q in its for o in ORDERS for r in range(R)]
            with ThreadPoolExecutor(max_workers=WORKERS) as ex:
                list(ex.map(work, jobs))
            CACHE.write_text(json.dumps(cache))
            print(f"gm2q: {SHORT[model]} {cond} finished; total ${spent():.4f}", flush=True)
            if stop.is_set():
                break
        if stop.is_set():
            break
    CACHE.write_text(json.dumps(cache))
    if state["refusal"]:
        key, e = state["refusal"]
        REFUSAL.write_text(f"# em-gm2q stopped on a refusal\n\nJob `{key}`, model `{e.model}`\n\nRequest ID: `{e.request_id}`\n\n"
                           f"Exact stop details:\n\n```\n{e.stop_details}\n```\n\nNothing was reworded or retried; no further call "
                           "was started.\n")
        sys.exit(f"STOPPED on a refusal: {e}")
    if state["error"]:
        sys.exit(f"gm2q: stopped on an error: {state['error']}")
    if state["cap"]:
        sys.exit(f"gm2q: budget cap ${CAP} (reserve ${RESERVE}) reached; stopped. Spent ${spent():.4f}")
    print(f"gm2q: complete, {len(cache)} conversations, ${spent():.4f}")


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


def perm_p(data, qs, seed):
    rng = np.random.default_rng(seed)
    T = sum(vc(data[q])[1] for q in qs)
    hits = 0
    for _ in range(N_PERM):
        t = 0.0
        for q in qs:
            g = data[q]
            allv = rng.permutation(np.concatenate([np.asarray(x, float) for x in g]))
            t += vc(np.split(allv, np.cumsum([len(x) for x in g])[:-1]))[1]
        hits += t >= T - TOL
    return (1 + hits) / (N_PERM + 1)


def ratio_boot(dq, ds, qs, seed):
    """R = OE(qonly)/OE(shown) and its 95% item-bootstrap percentile interval (items resampled with replacement;
    resamples where OE(shown) is 0 are dropped and counted)."""
    rng = np.random.default_rng(seed)
    point = oe(dq, qs) / oe(ds, qs) if oe(ds, qs) > 0 else float("nan")
    vals, dropped = [], 0
    for _ in range(N_BOOT):
        s = list(rng.choice(qs, len(qs)))
        den = oe(ds, s)
        if den <= 0:
            dropped += 1
            continue
        vals.append(oe(dq, s) / den)
    lo, hi = (map(float, np.percentile(vals, [2.5, 97.5])) if vals else (float("nan"), float("nan")))
    return {"R": point, "lo": lo, "hi": hi, "dropped": dropped}


def model_label(gate_shown, p_q, r_lo, usable_ok):
    """Pre-registered per-model reading (§5). Every comparison carries TOL (P13)."""
    if not usable_ok or not (gate_shown <= ALPHA - TOL):
        return "untestable"
    if p_q <= ALPHA - TOL and r_lo == r_lo and r_lo >= BAR - TOL:
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


def finals(cache, model, q, order, cond):
    out = []
    for r in range(R):
        c = cache.get(f"{SHORT[model]}|{q}|{order}|{cond}|{r}")
        if c and not c["missing"]:
            out.append(c["turns"][-1]["rating"])
    return out


def analyse_model(cache, model, qs, seed):
    d = {cond: {q: [finals(cache, model, q, o, cond) for o in ORDERS] for q in qs} for cond in CONDS[model]}
    usable = {cond: sum(len(x) for q in qs for x in d[cond][q]) / (len(qs) * 4 * R) for cond in CONDS[model]}
    usable_ok = all(usable[c] >= USABLE_MIN - TOL for c in ("shown", "qonly"))
    if not usable_ok or any(len(x) < 2 for c in ("shown", "qonly") for q in qs for x in d[c][q]):
        return {"usable": usable, "label": "untestable", "reason": "usable share below 0.90 or a cell with < 2 ratings"}
    out = {"usable": usable,
           "gate_shown_p": perm_p(d["shown"], qs, seed + 1),
           "qonly_p": perm_p(d["qonly"], qs, seed + 2),
           "OE": {c: oe(d[c], qs) for c in CONDS[model]},
           "ratio": ratio_boot(d["qonly"], d["shown"], qs, seed + 3)}
    out["label"] = model_label(out["gate_shown_p"], out["qonly_p"], out["ratio"]["lo"], usable_ok)
    out["within_sd"] = {c: float(np.sqrt(np.mean([np.var(x, ddof=1) for q in qs for x in d[c][q] if len(x) > 1])))
                        for c in CONDS[model]}
    out["per_item"] = {q: {c: {"OE": float(np.sqrt(vc(d[c][q])[0])), "means": [float(np.mean(x)) for x in d[c][q]]}
                           for c in CONDS[model]} for q in qs}
    # pattern agreement: correlation of order-mean deviations, shown vs qonly, pooled over items
    dev = lambda c: np.concatenate([np.array(out["per_item"][q][c]["means"]) - np.mean(out["per_item"][q][c]["means"]) for q in qs])
    out["pattern_r_shown_qonly"] = float(np.corrcoef(dev("shown"), dev("qonly"))[0, 1])
    if "redacted" in CONDS[model] and usable.get("redacted", 0) >= USABLE_MIN - TOL:
        out["ratio_redacted_shown"] = ratio_boot(d["redacted"], d["shown"], qs, seed + 4)
        out["ratio_qonly_redacted"] = ratio_boot(d["qonly"], d["redacted"], qs, seed + 5)
    # leave-one-item-out: the label with each item dropped (same seeds)
    loo = {}
    for q in qs:
        s = [x for x in qs if x != q]
        g, p = perm_p(d["shown"], s, seed + 1), perm_p(d["qonly"], s, seed + 2)
        rb = ratio_boot(d["qonly"], d["shown"], s, seed + 3)
        loo[q] = {"label": model_label(g, p, rb["lo"], True), "R": rb["R"], "lo": rb["lo"], "qonly_p": p, "gate": g}
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
    cache = json.loads(CACHE.read_text())
    qs = list(items())
    seed = seed % (2 ** 63)
    res = {"seed": seed, "n_conversations": len(cache), "cost_usd": sum(v["cost"] for v in cache.values()),
           "cache_sha256": hashlib.sha256(CACHE.read_bytes()).hexdigest(),
           "models": {SHORT[m]: analyse_model(cache, m, qs, seed) for m in MODELS}}
    res["verdict"] = bet_verdict({m: v["label"] for m, v in res["models"].items()})
    res["archived"] = archived_secondaries(qs)
    OUT_JSON.write_text(json.dumps(res, indent=1))
    write_tables(res)
    return res


def write_tables(r):
    f = lambda x: f"{x:.2f}"
    L = ["# em-gm2q tables (generated by experiments/gm2q_questions_only.py --analyse; do not edit)", "",
         f"{r['n_conversations']} conversations, ${r['cost_usd']:.4f}; seed {r['seed']}; cache sha256 `{r['cache_sha256']}`.", "",
         "| model | usable shown / qonly | gate p (shown) | p (qonly) | OE shown | OE qonly | **R = qonly / shown** | label | LOO flips |",
         "|---|---|---|---|---|---|---|---|---|"]
    for m, v in r["models"].items():
        if "OE" not in v:
            L.append(f"| {m} | {v['usable']} | — | — | — | — | — | {v['label']} | — |")
            continue
        ra = v["ratio"]
        L.append(f"| {m} | {v['usable']['shown']:.0%} / {v['usable']['qonly']:.0%} | {v['gate_shown_p']:.4f} | {v['qonly_p']:.4f} | "
                 f"{v['OE']['shown']:.1f} | {v['OE']['qonly']:.1f} | **{f(ra['R'])} [{f(ra['lo'])}, {f(ra['hi'])}]** | {v['label']} | "
                 f"{', '.join(v['loo_flips']) or 'none'} |")
    L += ["", f"**Bet verdict (pre-registered rule): {r['verdict']}**", "", "## Secondary (reported, never promoted)", ""]
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

def selftest():
    import exp5_run as er
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
    assert model_label(0.05, 0.01, 0.9, True) == "untestable"
    assert model_label(0.01, 0.05, 0.9, True) == "fail"
    assert model_label(0.01, 0.0499, 0.5, True) == "pass"
    assert model_label(0.01, 0.0499, 0.5 - 1e-6, True) == "fail"
    assert model_label(0.01, 0.01, float("nan"), True) == "fail"
    assert model_label(0.01, 0.01, 0.9, False) == "untestable"
    for labels, want in [({"h": "pass", "s": "pass"}, "pass"), ({"h": "pass", "s": "fail"}, "mixed"),
                         ({"h": "untestable", "s": "pass"}, "mixed"), ({"h": "fail", "s": "fail"}, "fail"),
                         ({"h": "fail", "s": "untestable"}, "untestable"), ({"h": "untestable", "s": "untestable"}, "untestable")]:
        assert bet_verdict(labels) == want, (labels, want)
    print("selftest: all checks hold")


def archive_world(model):
    """Measured per-item order means (shown and redacted) and the pooled within-order SD, from the archives (P15)."""
    qs = list(json.loads(PLANTED.read_text())["items"])
    if model == H:
        conv, reps = json.loads((RESULTS / "gm2-conversations.json").read_text()), 10
    else:
        conv, reps = json.loads((RESULTS / "mm-gm2-sonnet-conversations.json").read_text()), 4
    w = {}
    for cond in ("shown", "redacted"):
        data = {q: [[conv[f"{q}|{o}|{cond}|{r}"]["turns"][-1]["rating"] for r in range(reps) if f"{q}|{o}|{cond}|{r}" in conv]
                    for o in ORDERS] for q in qs}
        w[cond] = {"means": {q: [float(np.mean(x)) for x in data[q]] for q in qs},
                   "sd": float(np.sqrt(np.mean([np.var(x, ddof=1) for q in qs for x in data[q]]))),
                   "data": data}
    return qs, w


def simulate(qs, shown_means, q_means, sd, rng):
    draw = lambda m: list(np.clip(np.rint(rng.normal(m, sd, R)), 0, 100))
    ds = {q: [draw(m) for m in shown_means[q]] for q in qs}
    dq = {q: [draw(m) for m in q_means[q]] for q in qs}
    return ds, dq


def dry_run(n_sims=100):
    """P(pass) per model and for the bet, in worlds built from measured archive numbers. Analysis seeds fixed (dry run)."""
    rng = np.random.default_rng(20261105)
    worlds = ["null (no order effect)", "half of shown", "equal to shown", "archived redacted pattern"]
    out = {}
    for model in MODELS:
        qs, w = archive_world(model)
        sm, sd = w["shown"]["means"], w["shown"]["sd"]
        grand = {q: float(np.mean(sm[q])) for q in qs}
        scale = lambda a: {q: [grand[q] + a * (x - grand[q]) for x in sm[q]] for q in qs}
        qm = {worlds[0]: scale(0.0), worlds[1]: scale(0.5), worlds[2]: scale(1.0), worlds[3]: w["redacted"]["means"]}
        out[SHORT[model]] = {"within_sd_shown": sd, "within_sd_redacted": w["redacted"]["sd"]}
        for name, means in qm.items():
            labs = []
            for i in range(n_sims):
                ds, dq = simulate(qs, sm, means, sd, rng)
                N_saved = globals()["N_PERM"], globals()["N_BOOT"]
                globals()["N_PERM"], globals()["N_BOOT"] = 400, 400
                try:
                    g, p = perm_p(ds, qs, i), perm_p(dq, qs, i + 1)
                    rb = ratio_boot(dq, ds, qs, i + 2)
                finally:
                    globals()["N_PERM"], globals()["N_BOOT"] = N_saved
                labs.append(model_label(g, p, rb["lo"], True))
            out[SHORT[model]][name] = {k: labs.count(k) / n_sims for k in ("pass", "fail", "untestable")}
            print(f"dry run {SHORT[model]:6s} {name:28s} " + "  ".join(f"{k} {v:.2f}" for k, v in out[SHORT[model]][name].items()),
                  flush=True)
    for name in worlds:
        ph, ps = out["haiku"][name]["pass"], out["sonnet"][name]["pass"]
        print(f"dry run bet  {name:28s} P(pass, both, independent) {ph * ps:.2f}")
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
        json.dump(dry_run(), sys.stdout, indent=1)
    elif "--run" in a:
        run()
    elif "--analyse" in a:
        analyse(int(a[a.index("--seed") + 1]))
    else:
        print(__doc__)
