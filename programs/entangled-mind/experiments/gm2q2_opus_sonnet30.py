"""em-gm2q2 (map gm2q-f3): with only questions in the message, does question order still move the final rating on
claude-opus-5-5 (gm2's 10 items) and on claude-sonnet-5-5 (gm2b's 30 further items), with no single item carrying it?
Pre-registered in experiments/gm2q2-opus-sonnet30.md.

    python experiments/gm2q2_opus_sonnet30.py --print-prompts      # the exact messages, one item per arm; no calls
    python experiments/gm2q2_opus_sonnet30.py --selftest           # rule, flag, leave-one-out and boundary checks; no calls
    python experiments/gm2q2_opus_sonnet30.py --dry-run            # P(pass)/P(fail) in worlds built from archives; no calls
    python experiments/gm2q2_opus_sonnet30.py --run                # the paid run (Batches API; cap $4.00 in code; stop on refusal)
    python experiments/gm2q2_opus_sonnet30.py --analyse --seed S   # analysis of the cache; S must be the recorded beacon seed

The prompts, the order-effect estimator, the permutation gate and the ratio bootstrap are imported unchanged from
experiments/gm2q_questions_only.py (em-gm2q). What differs from em-gm2q (pre-registration §6): the models and items, the
repeats, the Batches API, the wrong-target check also covering the FIRST-listed statement (the em-gm2q audit's D5 miss),
leave-one-item-out inside the pass rule (with the cleaned-cell check recomputed on the remaining items; the audit's
claim-19 code hole), and no redacted arm.
Calls cached by key in results/gm2q2-conversations.json (written after every batch); refusal record
results/refusal-gm2q2.md; a run refuses to start while that record exists."""

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gm2q_questions_only as q1                       # em-gm2q: prompts and estimators, imported unchanged

O, S = "claude-opus-5-5", "claude-sonnet-5-5"
SHORT = {O: "opus", S: "sonnet"}
MODELS = [O, S]
ORDERS, LATIN = q1.ORDERS, q1.LATIN
CONDS = ["qonly", "shown"]
REPS = {O: 4, S: 5}                                     # D82: Opus 6 -> 4 (measured costs)                                     # conversations per model x item x order x condition
CAP, RESERVE, DISCOUNT = 4.25, 0.10, 0.5               # D82: $4.00 -> $4.25 (budget ruling br-011, amended)               # Batches API: 50% of list price
MAXTOK = {O: 1000, S: 1000}                             # em-dm4's settings for both models
OFFP = {O: {"output_config": {"effort": "low"}}, S: {"thinking": {"type": "between_tools"}}}  # mm_common.OFF
PRICES = {O: (4.00, 20.00), S: (2.00, 10.00)}           # config.PRICES, list price per million tokens
EST = {(O, "qonly"): 0.00293, (O, "shown"): 0.009173 / 5, (S, "qonly"): 0.000585, (S, "shown"): 0.000526}
# per request at the batch rate (D82): Opus shown from em-dm4's 80 COMPLETE chains ($0.009173 per chain; the earlier
# $0.0056 averaged in abandoned one-turn stubs); Opus qonly from the design review's 12-call pilot ($0.00293);
# Sonnet shown from em-dm4 ($0.00263 per chain), Sonnet qonly from em-gm2q ($0.00117 direct)
MARGIN = 1.10                                           # remaining-cost projection before every round
N_PERM, N_BOOT = q1.N_PERM, q1.N_BOOT
ALPHA, BAR, TOL, USABLE_MIN, WT_FAR = q1.ALPHA, q1.BAR, q1.TOL, q1.USABLE_MIN, q1.WT_FAR
SEED_RECORDED = 8982550231960562870                     # beacon seed (CURBy-RNG 1592505, seed commit); --analyse asserts it
RATING = q1.RATING

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent / "results"
CACHE = RESULTS / "gm2q2-conversations.json"
BATCHLOG = RESULTS / "gm2q2-batches.json"
OUT_JSON, OUT_MD = RESULTS / "gm2q2-opus-sonnet30.json", RESULTS / "gm2q2-opus-sonnet30-tables.md"
REFUSAL = RESULTS / "refusal-gm2q2.md"
GM2 = HERE / "gm2-planted-values.json"                 # gm2's 10 items (chain_claims only)
GM2B = HERE / "gm2b-planted-values.json"               # all 40 items; the 30 not in gm2 are Sonnet's
POOL = RESULTS / "pool-run-3.json"


def item_sets():
    recs = {r["id"]: r for r in json.loads(POOL.read_text())["records"]}
    g2 = json.loads(GM2.read_text())["items"]
    g2b = json.loads(GM2B.read_text())["items"]
    ten = {q: (recs[q], v["chain_claims"]) for q, v in g2.items()}
    thirty = {q: (recs[q], v["chain_claims"]) for q, v in g2b.items() if q not in g2}
    assert len(ten) == 10 and len(thirty) == 30
    return {O: ten, S: thirty}


def first(claims, order):
    return claims[LATIN[int(order[1]) - 1][0]]


def wrong_target(rating, s1_mean, s4_mean, final_mean):
    """em-gm2q's D70 flag (nearer the listed statement's mean shown rating than the reference final, and more than 20
    points from that final), applied to the 4th-listed AND the 1st-listed statement (the audit's D5 miss). The reference
    final here is the mean shown final rating IN THE SAME ORDER (em-gm2q used the item's mean over all four orders; with
    a large real order effect that flags answers that agree with turn by turn in that order: pre-registration §6, §8)."""
    return q1.wrong_target(rating, s4_mean, final_mean) or q1.wrong_target(rating, s1_mean, final_mean)


# --- calls (Batches API) ---------------------------------------------------------------------------------------------

def params(model, messages):
    p = {"model": model, "max_tokens": MAXTOK[model], "messages": messages}
    extra = json.loads(json.dumps(OFFP[model]))
    oc = extra.pop("output_config", {})
    oc["format"] = {"type": "json_schema", "schema": RATING}
    p["output_config"] = oc
    p.update(extra)
    return p


def cost_of(model, usage):
    pin, pout = PRICES[model]
    return DISCOUNT * (usage.input_tokens * pin + usage.output_tokens * pout) / 1e6


def parse(msg):
    text = "".join(b.text for b in msg.content if b.type == "text")
    try:
        return min(100, max(0, int(json.loads(text)["rating"]))), text
    except Exception:
        return None, text


def spent_of(cache):
    return sum(v.get("cost", 0.0) for v in cache.values())


def job_keys(its):
    for m in MODELS:
        for cond in CONDS:
            for q in its[m]:
                for o in ORDERS:
                    for r in range(REPS[m]):
                        yield f"{SHORT[m]}|{q}|{o}|{cond}|{r}", m, q, o, cond


def run(client=None):
    if REFUSAL.exists():
        sys.exit(f"gm2q2: {REFUSAL.name} exists; a refused run is never resumed, reworded or retried")
    if client is None:
        import anthropic
        from dotenv import load_dotenv
        for env in (HERE.parent / ".env", Path("/Users/seanpharris/entangled-mind/.env")):
            if env.exists():
                load_dotenv(env)
        client = anthropic.Anthropic(max_retries=4)
    its = item_sets()
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    blog = json.loads(BATCHLOG.read_text()) if BATCHLOG.exists() else []
    convs = {}

    def save():                                          # unfinished chains' billed cost is kept under "_unfinished"
        cache["_unfinished"] = {"cost": sum(c["cost"] for k, c in convs.items() if k not in cache),
                                "n": sum(1 for k in convs if k not in cache)}
        CACHE.write_text(json.dumps(cache))
        BATCHLOG.write_text(json.dumps(blog, indent=1))                                           # key -> in-progress state
    for key, m, q, o, cond in job_keys(its):
        rec, claims = its[m][q]
        texts = ([q1.qonly_message(rec, claims, o)] if cond == "qonly"
                 else [t for _, _, t in q1.chain_turns(rec, claims, o)])
        h = hashlib.sha256(json.dumps([m, texts, params(m, [])], sort_keys=True).encode()).hexdigest()
        if key in cache and cache[key].get("done"):          # a resumed run keeps every finished conversation
            if cache[key].get("req_sha256") not in (None, h):
                sys.exit(f"gm2q2: cached {key} was built from different requests; not resumed (D82)")
            continue
        kinds = [("M", None)] if cond == "qonly" else [(k, c) for k, c, _ in q1.chain_turns(rec, claims, o)]
        convs[key] = {"model": m, "cond": cond, "texts": texts, "kinds": kinds, "msgs": [], "turns": [], "cost": 0.0,
                      "ids": [], "batches": [], "req_sha256": h}
    # D82: billed cost of earlier runs' unfinished chains is carried forward, never overwritten; a batch logged as
    # submitted but never recorded as ended is collected first and its billed cost added to that total
    prior_lost = cache.pop("_unfinished", {}).get("cost", 0.0) + cache.pop("_lost_prior", {}).get("cost", 0.0)
    for e in blog:
        if not e.get("ended"):
            b = client.messages.batches.retrieve(e["batch"])
            while b.processing_status != "ended":
                time.sleep(20)
                b = client.messages.batches.retrieve(e["batch"])
            lost = 0.0
            for res in client.messages.batches.results(e["batch"]):
                if res.result.type == "succeeded":
                    msg = res.result.message
                    lost += cost_of(msg.model if msg.model in PRICES else O, msg.usage)
            e.update(ended=True, collected_after_crash=True, billed_usd=lost)
            prior_lost += lost
            print(f"gm2q2: collected batch {e['batch']} from an earlier run; ${lost:.4f} billed, results not used", flush=True)
    cache["_lost_prior"] = {"cost": prior_lost}
    save()                                               # D82: the carried-forward total is on disk before any exit
    # whole-run projection before the first batch: refuse to start if it cannot fit
    proj = sum(len(c["texts"]) * EST[(c["model"], c["cond"])] for c in convs.values())
    if spent_of(cache) + proj + RESERVE > CAP + TOL:
        sys.exit(f"gm2q2: projected ${proj:.3f} does not fit the ${CAP} cap with the ${RESERVE} reserve; not started")
    rnd = 0
    while True:
        live = {k: c for k, c in convs.items() if len(c["turns"]) < len(c["texts"]) and not c.get("ended")}
        if not live:
            break
        rnd += 1
        reqs = {}
        for k, c in live.items():
            c["msgs"].append({"role": "user", "content": c["texts"][len(c["turns"])]})
            reqs[k] = params(c["model"], list(c["msgs"]))
        def per_req(m, cond):                            # observed mean per request once that arm has spent, else EST
            xs = [c["cost"] / len(c["turns"]) for c in convs.values() if c["model"] == m and c["cond"] == cond and c["turns"]]
            return max(EST[(m, cond)], float(np.mean(xs))) if xs else EST[(m, cond)]
        remaining = sum((len(c["texts"]) - len(c["turns"])) * per_req(c["model"], c["cond"]) for c in live.values())
        this_round = sum(per_req(c["model"], c["cond"]) for c in live.values())
        spent = spent_of({k: v for k, v in cache.items() if k != "_unfinished"}) + sum(c["cost"] for k, c in convs.items() if k not in cache)
        # (spent includes _lost_prior: every billed cost of earlier runs' unfinished chains and collected batches, D82)
        if spent + this_round * MARGIN + RESERVE > CAP + TOL or spent + remaining + RESERVE > CAP + TOL:
            save()                                       # the next batch (x1.10), or all that remains, would not fit
            sys.exit(f"gm2q2: cap ${CAP}: spent ${spent:.3f}, next batch ${this_round:.3f} x{MARGIN}, remaining ${remaining:.3f}; "
                     f"stopped before round {rnd}")
        part, refusal = reqs, None
        for attempt in range(3):
            idmap = {f"r{n}": k for n, k in enumerate(part)}
            b = client.messages.batches.create(requests=[{"custom_id": cid, "params": part[k]} for cid, k in idmap.items()])
            t0 = time.time()
            entry = {"round": rnd, "batch": b.id, "n": len(part), "ended": False}
            blog.append(entry)
            save()                                       # D82: the batch ID is on disk before polling starts
            print(f"gm2q2: round {rnd} batch {b.id} submitted, {len(part)} requests", flush=True)
            while b.processing_status != "ended":
                time.sleep(20)
                b = client.messages.batches.retrieve(b.id)
            entry.update(ended=True, seconds=round(time.time() - t0), counts=str(b.request_counts))
            retry = {}
            for res in client.messages.batches.results(b.id):
                k = idmap[res.custom_id]
                c = convs[k]
                if res.result.type != "succeeded":
                    retry[k] = part[k]
                    continue
                msg = res.result.message
                cst = cost_of(c["model"], msg.usage)
                c["cost"] += cst
                c["ids"].append(msg.id)
                c["batches"].append(b.id)
                kind, claim = c["kinds"][len(c["turns"])]
                if msg.stop_reason == "refusal":
                    refusal = refusal or (k, msg, b.id)
                    c["turns"].append({"kind": kind, "claim": claim, "rating": None, "raw": None, "refused": True})
                    c["ended"] = True
                    continue
                r, raw = (None, None) if msg.stop_reason == "max_tokens" else parse(msg)
                c["turns"].append({"kind": kind, "claim": claim, "rating": r, "raw": raw})
                if r is None:
                    c["ended"] = True                    # no usable answer: the conversation stops, counts as missing
                else:
                    c["msgs"].append({"role": "assistant", "content": raw})
            for k, c in convs.items():
                if (len(c["turns"]) == len(c["texts"]) or c.get("ended")) and not (k in cache and cache[k].get("done")):
                    cache[k] = {"turns": c["turns"], "cost": c["cost"], "msg_ids": c["ids"], "batches": c["batches"], "req_sha256": c["req_sha256"],
                                "missing": c["turns"][-1]["rating"] is None or len(c["turns"]) < len(c["texts"]),
                                "done": True}
            save()
            if refusal:
                k, msg, bid = refusal
                REFUSAL.write_text(f"# em-gm2q2 stopped on a refusal\n\nJob `{k}`, model `{msg.model}`\n\nBatch `{bid}`, "
                                   f"message ID `{msg.id}`\n\nExact stop details:\n\n```\n{getattr(msg, 'stop_details', None)}\n```\n\n"
                                   "Nothing was reworded or retried, and no further batch was submitted.\n")
                sys.exit(f"STOPPED on a refusal: {k} {msg.id}")
            if not retry:
                break
            print(f"gm2q2: {len(retry)} errored/expired requests resubmitted unchanged", flush=True)
            part = retry
        else:
            save()
            sys.exit("gm2q2: requests still failing after two resubmissions; stopped")
        print(f"gm2q2: round {rnd} done; spent ${spent_of(cache):.4f}", flush=True)
    save()
    print(f"gm2q2: complete, ${spent_of(cache):.4f}")


# --- analysis -------------------------------------------------------------------------------------------------------

def cell(cache, model, q, order, cond):
    out = []
    for r in range(REPS[model]):
        c = cache.get(f"{SHORT[model]}|{q}|{order}|{cond}|{r}")
        if c and not c["missing"]:
            out.append(c)
    return out


def label_on(d, clean, qs, seed, n_perm=None, n_boot=None):
    """The §5 per-model reading on item set qs (all parts recomputed on qs, including the cleaned-cell check).
    Returns (label, parts) with label pass|fail|untestable before leave-one-item-out."""
    if any(len(x) < 2 for c in ("shown", "qonly") for q in qs for x in d[c][q]):
        return "untestable", {"why": "a shown or qonly cell with fewer than 2 ratings"}
    g = q1.perm_p(d["shown"], qs, seed + 1, n_perm)
    pq = q1.perm_p(d["qonly"], qs, seed + 2, n_perm)
    ok = all(len(x) >= 2 for q in qs for x in clean[q])
    pc = q1.perm_p(clean, qs, seed + 6, n_perm) if ok else None
    rb = q1.ratio_boot(d["qonly"], d["shown"], qs, seed + 3, n_boot)
    lab = q1.model_label(g, pq, pc, rb["lo"], True)
    first_fail = (None if lab == "pass" else "shown gate" if lab == "untestable" else
                  "qonly gate" if not pq <= ALPHA - TOL else
                  "wrong-target check (a cleaned cell kept < 2)" if pc is None else
                  "cleaned qonly gate" if not pc <= ALPHA - TOL else "ratio lower bound")
    return lab, {"gate_shown_p": g, "qonly_p": pq, "qonly_p_clean": pc, "clean_ok": ok, "ratio": rb, "first_fail": first_fail}


def final_label(full, loo):
    """Pass needs the full-set label pass AND every leave-one-item-out label pass (pre-registration §5)."""
    if full != "pass":
        return full
    return "pass" if all(v == "pass" for v in loo.values()) else "fail"


def analyse_model(cache, model, its, seed, n_perm=None, n_boot=None, light=False):
    qs, claims = list(its), {q: v[1] for q, v in its.items()}
    convs = {cond: {q: [cell(cache, model, q, o, cond) for o in ORDERS] for q in qs} for cond in CONDS}
    d = {cond: {q: [[c["turns"][-1]["rating"] for c in x] for x in convs[cond][q]] for q in qs} for cond in CONDS}
    usable = {cond: sum(len(x) for q in qs for x in d[cond][q]) / (len(qs) * 4 * REPS[model]) for cond in CONDS}
    if not all(usable[c] >= USABLE_MIN - TOL for c in CONDS):
        return {"usable": usable, "label": "untestable", "first_fail": "usable share below 0.90"}
    stmt = {q: {k: float(np.mean([t["rating"] for x in convs["shown"][q] for c in x for t in c["turns"]
                                  if t["kind"] == "S" and t["claim"] == k] or [np.nan])) for k in claims[q]} for q in qs}
    fin = {q: float(np.mean([r for x in d["shown"][q] for r in x])) for q in qs}
    fin_o = {q: [float(np.mean(x)) for x in d["shown"][q]] for q in qs}
    flag = lambda cond: {q: [[wrong_target(r, stmt[q][first(claims[q], o)], stmt[q][q1.fourth(claims[q], o)], fin_o[q][j])
                              for r in d[cond][q][j]] for j, o in enumerate(ORDERS)] for q in qs}
    fq = flag("qonly")
    clean = {q: [[r for r, b in zip(d["qonly"][q][j], fq[q][j]) if not b] for j in range(4)] for q in qs}
    lab, parts = label_on(d, clean, qs, seed, n_perm, n_boot)
    out = {"usable": usable, **parts, "label_full": lab}
    loo = {}
    if lab == "pass":
        for q in qs:
            s = [x for x in qs if x != q]
            ll, pp = label_on(d, clean, s, seed, n_perm, n_boot)
            loo[q] = ll
            if ll != "pass":
                out.setdefault("loo_break_parts", {})[q] = pp.get("first_fail") or pp.get("why") or ll
            if light and ll != "pass":
                break
    out["loo"] = loo
    out["loo_breakers"] = [q for q, v in loo.items() if v != "pass"]
    out["label"] = final_label(lab, loo)
    if out["label"] == "fail" and lab == "pass":
        out["first_fail"] = "leave-one-item-out (" + ", ".join(f"{q}: {out['loo_break_parts'].get(q, '?')}" for q in out["loo_breakers"]) + ")"
    if light:
        return out
    fs = flag("shown")
    share = lambda f: float(np.mean([b for q in qs for x in f[q] for b in x]))
    out["wrong_target_share"] = {"qonly": share(fq), "shown": share(fs)}
    out["clean_cells_below_2"] = [f"{q} {ORDERS[j]}" for q in qs for j in range(4) if len(clean[q][j]) < 2]
    out["OE"] = {c: q1.oe(d[c], qs) for c in CONDS}
    out["within_sd"] = {c: float(np.sqrt(np.mean([np.var(x, ddof=1) for q in qs for x in d[c][q] if len(x) > 1]))) for c in CONDS}
    out["per_item"] = {q: {c: {"OE": float(np.sqrt(q1.vc(d[c][q])[0])), "means": [float(np.mean(x)) for x in d[c][q]]}
                           for c in CONDS} for q in qs}
    tot = sum(q1.vc(d["qonly"][q])[0] for q in qs)
    out["qonly_vc_share"] = {q: (q1.vc(d["qonly"][q])[0] / tot if tot > 0 else 0.0) for q in qs}
    dev = lambda c: np.concatenate([np.array(out["per_item"][q][c]["means"]) - np.mean(out["per_item"][q][c]["means"]) for q in qs])
    out["pattern_r_shown_qonly"] = float(np.corrcoef(dev("shown"), dev("qonly"))[0, 1])
    # secondaries (reported, never promoted)
    if all(len(x) >= 1 for q in qs for x in clean[q]):
        out["ratio_clean_qonly"] = q1.ratio_boot({q: [x if len(x) else [fin[q]] for x in clean[q]] for q in qs}, d["shown"], qs, seed + 4)
    far = lambda cond: {q: [[r for r in x if abs(r - fin[q]) <= WT_FAR + TOL] for x in d[cond][q]] for q in qs}
    fa, fb = far("qonly"), far("shown")
    if all(len(x) >= 2 for c in (fa, fb) for q in qs for x in c[q]):
        out["ratio_trim20_both"] = q1.ratio_boot(fa, fb, qs, seed + 5)          # the em-gm2q audit's sensitivity
    else:
        out["ratio_trim20_both"] = None
    return out


def archived_secondaries():
    out = {}
    its = item_sets()
    conv = json.loads((RESULTS / "mm-gm2-opus-conversations.json").read_text())
    qs = list(its[O])
    ok = lambda c: bool(c) and not c.get("abandoned") and bool(c["turns"]) and c["turns"][-1]["kind"] == "M" and c["turns"][-1]["rating"] is not None
    data = {q: [[conv[f"{q}|{o}|shown|{r}"]["turns"][-1]["rating"] for r in range(4) if ok(conv.get(f"{q}|{o}|shown|{r}"))]
                for o in ORDERS] for q in qs}                                   # D82: complete chains only
    out["opus_dm4_shown_OE"] = q1.oe(data, qs)
    hb = json.loads((RESULTS / "gm2b-conversations.json").read_text())
    qs = list(its[S])
    for cond in ("shown", "redacted"):
        data = {q: [[hb[f"{q}|{o}|{cond}|{r}"]["turns"][-1]["rating"] for r in range(10) if f"{q}|{o}|{cond}|{r}" in hb]
                    for o in ORDERS] for q in qs}
        out[f"haiku_gm2b_30_{cond}_OE"] = q1.oe(data, qs)
    return out


def bet_verdict(labels):
    return q1.bet_verdict(labels)


def analyse(seed):
    assert SEED_RECORDED is not None and seed == SEED_RECORDED, f"--seed must be the recorded beacon seed {SEED_RECORDED}"
    full = json.loads(CACHE.read_text())
    cache = {k: v for k, v in full.items() if not k.startswith("_")}
    its = item_sets()
    seed = seed % (2 ** 63)
    res = {"seed": seed, "n_conversations": len(cache), "n_missing": sum(1 for v in cache.values() if v["missing"]),
           "unfinished_cost_usd": full.get("_unfinished", {}).get("cost", 0.0) + full.get("_lost_prior", {}).get("cost", 0.0),
           "cost_usd": spent_of(full), "cache_sha256": hashlib.sha256(CACHE.read_bytes()).hexdigest(),
           "models": {SHORT[m]: analyse_model(cache, m, its[m], seed) for m in MODELS}}
    res["verdict"] = bet_verdict({m: v["label"] for m, v in res["models"].items()})
    res["archived"] = archived_secondaries()
    OUT_JSON.write_text(json.dumps(res, indent=1))
    write_tables(res)
    return res


def write_tables(r):
    f = lambda x: "—" if x is None or x != x else f"{x:.2f}"
    L = ["# em-gm2q2 tables (generated by experiments/gm2q2_opus_sonnet30.py --analyse; do not edit)", "",
         f"{r['n_conversations']} conversations ({r['n_missing']} missing), ${r['cost_usd']:.4f} at the batch rate; seed {r['seed']}; "
         f"cache sha256 `{r['cache_sha256']}`.", "",
         "| model | items | usable shown / qonly | gate p (shown) | p (qonly) | p (qonly, wrong-target dropped) | OE shown | OE qonly | **R = qonly / shown** | label on all items | leave-one-out breakers | **label** | first failing part |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for m, v in r["models"].items():
        n = len(v.get("per_item", {})) or "—"
        if "OE" not in v:
            L.append(f"| {m} | {n} | {v['usable']} | — | — | — | — | — | — | {v.get('label_full', v['label'])} | — | {v['label']} | {v.get('first_fail')} |")
            continue
        ra = v["ratio"]
        pc = "— (a cell kept < 2)" if v["qonly_p_clean"] is None else f"{v['qonly_p_clean']:.4f}"
        L.append(f"| {m} | {n} | {v['usable']['shown']:.0%} / {v['usable']['qonly']:.0%} | {v['gate_shown_p']:.4f} | {v['qonly_p']:.4f} | {pc} | "
                 f"{v['OE']['shown']:.1f} | {v['OE']['qonly']:.1f} | **{f(ra['R'])} [{f(ra['lo'])}, {f(ra['hi'])}]** | {v['label_full']} | "
                 f"{', '.join(v['loo_breakers']) or ('none' if v['loo'] else 'not run (label not pass on all items)')} | **{v['label']}** | {v['first_fail'] or '—'} |")
    L += ["", f"**Bet verdict (pre-registered rule): {r['verdict']}**", "", "## Secondary (reported, never promoted)", ""]
    for m, v in r["models"].items():
        if "OE" not in v:
            continue
        top = max(v["qonly_vc_share"], key=v["qonly_vc_share"].get)
        rc, rt = v.get("ratio_clean_qonly"), v.get("ratio_trim20_both")
        L.append(f"- {m}: wrong-target share qonly {v['wrong_target_share']['qonly']:.1%} / shown {v['wrong_target_share']['shown']:.1%}; "
                 f"cleaned cells with < 2 answers: {', '.join(v['clean_cells_below_2']) or 'none'}; within-order SD "
                 + ", ".join(f"{c} {s:.1f}" for c, s in v["within_sd"].items())
                 + f"; order-pattern correlation shown vs qonly {v['pattern_r_shown_qonly']:.2f}; largest item share of qonly "
                 f"between-order variance {top} {v['qonly_vc_share'][top]:.0%}"
                 + (f"; R with flagged qonly answers dropped {f(rc['R'])} [{f(rc['lo'])}, {f(rc['hi'])}]" if rc else "")
                 + (f"; R with every answer > 20 from the usual one dropped in both arms {f(rt['R'])} [{f(rt['lo'])}, {f(rt['hi'])}]" if rt else
                    "; R trimmed at 20 in both arms: not computable (a cell kept < 2)"))
    for k, v in r["archived"].items():
        L.append(f"- archived {k}: {v:.1f}")
    for m, v in r["models"].items():
        if "per_item" not in v:
            continue
        L += ["", f"### Per item, {m}", "", "| item | OE shown | OE qonly | qonly variance share | final M by order O1–O4, shown | final M by order O1–O4, qonly | leave-one-out label |",
              "|---|---|---|---|---|---|---|"]
        for q, pi in v["per_item"].items():
            L.append(f"| {q} | {pi['shown']['OE']:.1f} | {pi['qonly']['OE']:.1f} | {v['qonly_vc_share'][q]:.0%} | "
                     + ", ".join(f"{x:.0f}" for x in pi["shown"]["means"]) + " | " + ", ".join(f"{x:.0f}" for x in pi["qonly"]["means"])
                     + f" | {v['loo'].get(q, '—')} |")
    OUT_MD.write_text("\n".join(L) + "\n")
    print("\n".join(L))


# --- self-test and dry run (no calls) -------------------------------------------------------------------------------

def synth(rng, model, qs, claims, stmt, shown_means, q_means, sd, stmt_sd, wt_frac=0.0, jump=None):
    """A cache in the run's format: shown chains with sub-ratings and finals; qonly finals, a share wt_frac of which are
    replaced by the first- or last-listed statement's rating; jump = (item, order index, value) puts every qonly answer
    in that one cell near value (the em-gm2q pattern)."""
    cache, rnd = {}, lambda mu, s: int(np.clip(np.rint(rng.normal(mu, s)), 0, 100))
    for q in qs:
        for j, o in enumerate(ORDERS):
            for r in range(REPS[model]):
                seq = [claims[q][i] for i in LATIN[j]]
                turns = [{"kind": "S", "claim": k, "rating": rnd(stmt[q][k], stmt_sd)} for k in seq]
                turns.append({"kind": "M", "claim": None, "rating": rnd(shown_means[q][j], sd)})
                cache[f"{SHORT[model]}|{q}|{o}|shown|{r}"] = {"turns": turns, "cost": 0, "missing": False}
                if jump and q == jump[0] and j == jump[1]:
                    v = rnd(jump[2], 4)
                elif rng.random() < wt_frac:
                    v = rnd(stmt[q][seq[0] if rng.random() < 0.5 else seq[3]], stmt_sd)
                else:
                    v = rnd(q_means[q][j], sd)
                cache[f"{SHORT[model]}|{q}|{o}|qonly|{r}"] = {"turns": [{"kind": "M", "claim": None, "rating": v}], "cost": 0,
                                                              "missing": False}
    return cache


def selftest():
    its = item_sets()
    rec, claims = its[O]["h190"]
    assert q1.qonly_message(rec, claims, "O1").count("\n") >= 5
    # the flag: first- or last-listed statement
    assert wrong_target(90, 95, 10, 20) and wrong_target(90, 10, 95, 20) and not wrong_target(30, 95, 90, 20)
    assert final_label("pass", {"a": "pass", "b": "pass"}) == "pass"
    assert final_label("pass", {"a": "pass", "b": "fail"}) == "fail"
    assert final_label("pass", {"a": "untestable"}) == "fail"
    assert final_label("fail", {}) == "fail" and final_label("untestable", {}) == "untestable"
    for labels, want in [({"o": "pass", "s": "pass"}, "pass"), ({"o": "pass", "s": "fail"}, "mixed"),
                         ({"o": "untestable", "s": "pass"}, "mixed"), ({"o": "fail", "s": "fail"}, "fail"),
                         ({"o": "fail", "s": "untestable"}, "untestable")]:
        assert bet_verdict(labels) == want
    # worlds with known answers, on Sonnet's 30 items
    qs = [f"q{i}" for i in range(30)]
    cl = {q: [0, 1, 2, 3] for q in qs}
    st = {q: {0: 5, 1: 15, 2: 85, 3: 95} for q in qs}
    eff = {q: [50 + 7 * (j - 1.5) * (1 if i % 2 else -1) for j in range(4)] for i, q in enumerate(qs)}
    nul = {q: [50] * 4 for q in qs}
    half = {q: [50 + 0.25 * (x - 50) for x in eff[q]] for q in qs}
    fake = {q: (None, cl[q]) for q in qs}
    ok = analyse_model(synth(np.random.default_rng(7), S, qs, cl, st, eff, eff, 5, 8), S, fake, 11, 400, 400)
    assert ok["label"] == "pass", (ok["label"], ok.get("first_fail"))
    one = analyse_model(synth(np.random.default_rng(8), S, qs, cl, st, eff, half, 6, 8, jump=("q3", 0, 95)), S, fake, 11, 400, 400)
    assert one["label"] != "pass", one["label"]
    wt = analyse_model(synth(np.random.default_rng(9), S, qs, cl, st, eff, nul, 6, 8, wt_frac=0.4), S, fake, 11, 400, 400)
    assert wt["label"] != "pass", wt["label"]
    # both arms' effect on one item only: the full set passes, leaving that item out must turn it into a fail
    q10 = qs[:10]
    solo = {q: ([30, 70, 30, 70] if q == "q0" else [50] * 4) for q in q10}
    lo = analyse_model(synth(np.random.default_rng(10), O, q10, cl, {q: {0: 2, 1: 5, 2: 95, 3: 98} for q in q10}, solo, solo, 4, 3),
                       O, {q: (None, cl[q]) for q in q10}, 11, 400, 400)
    assert lo["label_full"] == "pass" and lo["label"] == "fail" and "q0" in lo["loo_breakers"], (lo["label_full"], lo["label"], lo["loo_breakers"])
    print("selftest: all checks hold (equal world passes; one-item-only world passes on all items and leaving q0 out breaks it;"
          " one-item jump world:", one["label"], one.get("first_fail"),
          "; first/last wrong-target world:", wt["label"], wt.get("first_fail"), ")")


def world(model, wave=None):
    """Archive numbers per arm. Opus: em-dm4's Opus shown chains on gm2's 10 items (R = 4). Sonnet on gm2b's 30 further
    items: no Sonnet archive exists there, so the per-item shown order deviations are Haiku's (gm2b, R = 10) scaled by the
    ratio of Sonnet's to Haiku's shown OE on gm2's 10 items in em-gm2q's same-day run, with Sonnet's within-order SD from
    that run; statement means are Haiku's gm2b shown sub-ratings (stated in the pre-registration §8)."""
    its = item_sets()[model]
    qs, claims = list(its), {q: v[1] for q, v in its.items()}
    keep = None
    if model == O:
        # D82: em-dm4's Opus repeats 2-3 are abandoned one-turn stubs; only complete chains are read (ok() below)
        conv, reps, scale, sd_over = json.loads((RESULTS / "mm-gm2-opus-conversations.json").read_text()), 4, 1.0, None
    else:
        conv, reps = json.loads((RESULTS / "gm2b-conversations.json").read_text()), 10
        g = json.loads((RESULTS / "gm2q-questions-only.json").read_text())["models"]
        scale = g["sonnet"]["OE"]["shown"] / g["haiku"]["OE"]["shown"]
        sd_over = g["sonnet"]["within_sd"]["shown"]
    ok = lambda c: bool(c) and not c.get("abandoned") and bool(c["turns"]) and c["turns"][-1]["kind"] == "M" and c["turns"][-1]["rating"] is not None
    conv = {k: v for k, v in conv.items() if ok(v)}
    w = {"qs": qs, "claims": claims}
    for cond in ("shown", "redacted"):
        data = {q: [[conv[f"{q}|{o}|{cond}|{r}"]["turns"][-1]["rating"] for r in (keep or range(reps)) if f"{q}|{o}|{cond}|{r}" in conv
                     and conv[f"{q}|{o}|{cond}|{r}"]["turns"][-1]["rating"] is not None] for o in ORDERS] for q in qs}
        grand, dev = {}, {}
        for q in qs:
            m = np.array([np.mean(x) for x in data[q]])
            n = np.mean([len(x) for x in data[q]])
            v_c, msb = q1.vc(data[q])
            shrink = np.sqrt(v_c / (msb / n)) if msb > 0 else 0.0
            grand[q], dev[q] = float(m.mean()), list((m - m.mean()) * shrink * scale)
        sd = float(np.sqrt(np.mean([np.var(x, ddof=1) for q in qs for x in data[q] if len(x) > 1])))
        w[cond] = {"grand": grand, "dev": dev, "sd": sd_over or sd}
    stm, cells = {}, {}
    for key, c in conv.items():
        q, o, cond, _ = key.split("|")
        if q in claims and cond == "shown" and o.startswith("O") and (keep is None or int(_) in keep):
            for t in c["turns"]:
                if t["kind"] == "S" and t["rating"] is not None:
                    stm.setdefault((q, t["claim"]), []).append(t["rating"])
                    cells.setdefault((q, o, t["claim"]), []).append(t["rating"])
    w["stmt"] = {q: {k: float(np.mean(stm[(q, k)])) for k in claims[q]} for q in qs}
    w["stmt_sd"] = float(np.sqrt(np.mean([np.var(x, ddof=1) for x in cells.values() if len(x) > 1])))
    w["scale"] = scale
    return w


def dry_run(n_sims=100, n_perm=400, n_boot=400):
    rng = np.random.default_rng(20261105)
    worlds = ["null", "half", "0.75", "equal", "redacted pattern", "shuffled items, equal", "one-item jump (half elsewhere)",
              "wrong-target 0.2 (first or last line)"]
    out = {"_note": f"{n_sims} simulated runs per world; {n_perm} permutations, {n_boot} bootstraps; leave-one-item-out "
                    "stops at the first non-pass (it can only turn a pass into a fail)"}
    for arm, model, wave in (("opus", O, None), ("sonnet", S, None)):
        w = world(model, wave)
        qs, claims, g, dev = w["qs"], w["claims"], w["shown"]["grand"], w["shown"]["dev"]
        fake = {q: (None, claims[q]) for q in qs}
        shown = {q: [g[q] + x for x in dev[q]] for q in qs}
        res = {"within_sd_shown": w["shown"]["sd"], "stmt_sd": w["stmt_sd"], "scale": w["scale"]}
        for name in worlds:
            labs = []
            for i in range(n_sims):
                jump, wt = None, 0.0
                if name.startswith("shuffled"):
                    perm = list(rng.permutation(qs))
                    qm = {q: [g[q] + x for x in dev[p]] for q, p in zip(qs, perm)}
                elif name == "redacted pattern":
                    qm = {q: [w["redacted"]["grand"][q] - w["redacted"]["grand"][q] + g[q] + x for x in w["redacted"]["dev"][q]] for q in qs}
                elif name.startswith("one-item"):
                    qm = {q: [g[q] + 0.5 * x for x in dev[q]] for q in qs}
                    tq = qs[int(rng.integers(len(qs)))]
                    jump = (tq, int(rng.integers(4)), 95.0 if g[tq] < 50 else 5.0)
                elif name.startswith("wrong"):
                    qm = {q: [g[q] + x for x in dev[q]] for q in qs}
                    wt = 0.2
                else:
                    a = {"null": 0.0, "half": 0.5, "0.75": 0.75, "equal": 1.0}[name]
                    qm = {q: [g[q] + a * x for x in dev[q]] for q in qs}
                c = synth(rng, model, qs, claims, w["stmt"], shown, qm, w["shown"]["sd"], w["stmt_sd"], wt, jump)
                labs.append(analyse_model(c, model, fake, 1000 + i, n_perm, n_boot, light=True)["label"])
            res[name] = {k: labs.count(k) / n_sims for k in ("pass", "fail", "untestable")}
            print(f"dry run {arm:7s} {name:38s} " + "  ".join(f"{k} {v:.2f}" for k, v in res[name].items()), flush=True)
        out[arm] = res
    out["bet"] = {name: out["opus"][name]["pass"] * out["sonnet"][name]["pass"] for name in worlds}
    for name in worlds:
        print(f"dry run bet  {name:38s} P(pass, both, independent) {out['bet'][name]:.3f}")
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--print-prompts" in a:
        its = item_sets()
        for m in MODELS:
            q = next(iter(its[m]))
            rec, claims = its[m][q]
            print(f"=== {SHORT[m]}, item {q} ===")
            for o in ORDERS:
                print(f"--- qonly {o} ---\n{q1.qonly_message(rec, claims, o)}\n")
            print("--- shown O1 turns ---")
            for t in q1.chain_turns(rec, claims, "O1"):
                print(t)
            print("params (qonly O1):", json.dumps({k: v for k, v in params(m, [{"role": "user", "content": "..."}]).items() if k != "messages"}))
        print("prompts: imported unchanged from gm2q_questions_only (em-gm2q)")
    elif "--selftest" in a:
        selftest()
    elif "--dry-run" in a:
        res = dry_run()
        (RESULTS / "gm2q2-dry-run.json").write_text(json.dumps(res, indent=1) + "\n")
    elif "--run" in a:
        run()
    elif "--analyse" in a:
        analyse(int(a[a.index("--seed") + 1]))
    else:
        print(__doc__)
