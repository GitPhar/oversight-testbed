"""em-dm6f2f2f1 (map dm6f2f2-f1): does Opus's 'check anything under 70%' list change with the confidence format, with
the own-guess template? Pre-registered in experiments/dm6f2f2f1-opus.md.

    python experiments/dm6f2f2f1_opus.py --print-questions   # the drawn questions (needs the recorded items seed); no calls
    python experiments/dm6f2f2f1_opus.py --selftest          # draw, prompt, floor and cap checks; no calls
    python experiments/dm6f2f2f1_opus.py --dry-run           # P(pass) in worlds built from em-dm6f2f2's archive; no calls
    python experiments/dm6f2f2f1_opus.py --run               # paid run (Batches API; cap $0.30 in code; stop on refusal)
    python experiments/dm6f2f2f1_opus.py --analyse --seed S  # S must be the recorded bootstrap seed

em-dm6f2f2's design on claude-opus-5-5 only: the same two reworded templates (dm6f2f2_own_guess.TEMPLATES), the same
Opus settings (effort low, max_tokens 300), fresh single-question calls, each question asked twice per format; em-dm6f2's
statistic imported unchanged (dm6f2_flag_overlap.analyse), read with this bet's own floor (MIN_Q below).
Questions: 10 per pool category (the card's 40). Claim questions are drawn from all 60. The other three categories are
drawn from the 'unsure set': questions on which both Sonnet and Haiku stated a number below 0.70 in at least one of
their four em-dm6f2f2 cells (results/dm6f2f2-calls.json, pinned by sha256). Opus flagged 6% of its answers on a random
draw (em-dm6f2f2), so a random draw cannot show a list that changes.
Cache results/dm6f2f2f1-calls.json; batch log results/dm6f2f2f1-batches.json; refusal record results/refusal-dm6f2f2f1.md."""

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))
sys.path.insert(0, str(HERE))
import dm6f2f2_own_guess as g                            # em-dm6f2f2: templates, request parameters, parse, prices
import dm6f2_flag_overlap as f2                          # em-dm6f2: statistic and verdict, unchanged

O = g.O                                                  # claude-opus-5-5
CAP, RESERVE = 0.30, 0.005                               # br-022: this bet's cap
MIN_Q = 25                                               # usable questions (a number in all four cells); fewer -> untestable
MIN_FLAGGED = 6                                          # questions flagged (< 0.70) in at least one cell; fewer -> untestable
N_PER_CAT = 10
UNSURE_THRESH = 0.70
SEED_RECORDED = None                                     # filled by the seed commit: {"bootstrap": int, "items": int}
PINNED_SHA256 = {"dm6f2f2-calls.json": "a64bdf7d151fcada9a18c6dcb4a7787b162c27bc83b738b985292e1e4837172d",
                 "pool-run-3.json": "8011ae79b4c12c6ac9b95dd751b68c891aeb3c7c47a5d5afb2d7c465b4db2b56"}
RESULTS = HERE.parent / "results"
CACHE, BATCHLOG, REFUSAL = RESULTS / "dm6f2f2f1-calls.json", RESULTS / "dm6f2f2f1-batches.json", RESULTS / "refusal-dm6f2f2f1.md"
OUT_JSON, OUT_MD = RESULTS / "dm6f2f2f1-opus.json", RESULTS / "dm6f2f2f1-opus-tables.md"
CELL_KEYS = [("P", 0), ("P", 1), ("F", 0), ("F", 1)]


def results_dir():
    """reproduce.py redirects entangled_mind.config.RESULTS to its snapshot (D78); read it at call time."""
    try:
        from entangled_mind import config
        return Path(config.RESULTS)
    except Exception:
        return RESULTS


def check_pins(R):
    bad = []
    for f, want in PINNED_SHA256.items():
        got = hashlib.sha256((R / f).read_bytes()).hexdigest()
        if got != want:
            bad.append(f"{f}: got {got}, want {want}")
    if bad:
        sys.exit("dm6f2f2f1: pinned archive changed; stopped: " + "; ".join(bad))


def pool(R=None):
    R = R or results_dir()
    return {r["id"]: r for r in json.loads((R / "pool-run-3.json").read_text())["records"]}


def parent_cells(R=None):
    """em-dm6f2f2's four cells per model and question: {model: {q: {(fmt, r): conf}}}."""
    R = R or results_dir()
    c = json.loads((R / "dm6f2f2-calls.json").read_text())
    out = {}
    for k, v in c.items():
        if k.startswith("_"):
            continue
        m, fmt, r, q = k.split("|")
        out.setdefault(m, {}).setdefault(q, {})[(fmt, int(r[1:]))] = v.get("conf")
    return out


def unsure_set(R=None):
    """Non-claim questions on which Sonnet AND Haiku each stated a number below 0.70 in at least one em-dm6f2f2 cell."""
    P, cells = pool(R), parent_cells(R)
    low = lambda m, q: any(x is not None and x < UNSURE_THRESH - f2.TOL for x in cells.get(m, {}).get(q, {}).values())
    return sorted(q for q, r in P.items() if r["category"] != "claim" and low("sonnet", q) and low("haiku", q))


def questions(items_seed, R=None):
    """N_PER_CAT per category, drawn with the items seed from sorted ids (claim: all 60; others: the unsure set);
    returned in run order (a permutation drawn with the same generator)."""
    P, U = pool(R), set(unsure_set(R))
    rng = np.random.default_rng(items_seed % 2**63)
    out = []
    for cat in sorted({r["category"] for r in P.values()}):
        ids = sorted(q for q, r in P.items() if r["category"] == cat and (cat == "claim" or q in U))
        out += [ids[i] for i in sorted(rng.choice(len(ids), N_PER_CAT, replace=False))]
    return [out[i] for i in rng.permutation(len(out))]


def worst_cost(text):
    """Upper bound on one request's cost at the batch rate: input at 2 characters per token, output at max_tokens."""
    pin, pout = g.PRICES[O]
    return g.DISCOUNT * (len(text) / 2 * pin + g.MAXTOK[O] * pout) / 1e6


def key(fmt, r, q):
    return f"opus|{fmt}|r{r}|{q}"


def run(client=None):
    R = results_dir()
    if REFUSAL.exists():
        sys.exit(f"dm6f2f2f1: {REFUSAL.name} exists; a refused run is never resumed, reworded or retried")
    assert SEED_RECORDED is not None, "the seed commit must fill SEED_RECORDED before the run"
    check_pins(R)
    if client is None:
        import anthropic
        from dotenv import load_dotenv
        load_dotenv(Path("/Users/seanpharris/entangled-mind/.env"))
        client = anthropic.Anthropic(max_retries=4)
    P = pool(R)
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    blog = json.loads(BATCHLOG.read_text()) if BATCHLOG.exists() else []
    save = lambda: (CACHE.write_text(json.dumps(cache)), BATCHLOG.write_text(json.dumps(blog, indent=1)))
    spent = lambda: sum(v["cost"] for v in cache.values())            # includes "_lost_prior"
    lost = cache.get("_lost_prior", {}).get("cost", 0.0)
    for e in blog:                                       # a batch submitted but never recorded as ended: collect its cost
        if not e.get("ended"):
            b = client.messages.batches.retrieve(e["batch"])
            while b.processing_status != "ended":
                time.sleep(20)
                b = client.messages.batches.retrieve(e["batch"])
            for res in client.messages.batches.results(e["batch"]):
                if res.result.type == "succeeded":
                    msg = res.result.message
                    pin, pout = g.PRICES[O]
                    lost += g.DISCOUNT * (msg.usage.input_tokens * pin + msg.usage.output_tokens * pout) / 1e6
            e.update(ended=True, collected_after_crash=True)
    cache["_lost_prior"] = {"cost": lost}
    save()
    todo = []                                            # whole questions, in run order
    for q in questions(SEED_RECORDED["items"], R):
        reqs = {}
        for fmt, r in CELL_KEYS:
            k, t = key(fmt, r, q), g.TEMPLATES[fmt].format(q=P[q]["question"])
            if k in cache:
                if cache[k].get("sha") != g.req_sha(O, t):
                    sys.exit(f"dm6f2f2f1: cached {k} was built from a different request; stopped, nothing resubmitted")
                continue
            reqs[k] = t
        if reqs:
            todo.append(reqs)
    while todo:
        head = CAP - spent() - RESERVE                   # chunk = as many whole questions as fit at their worst case
        chunk, w = [], 0.0
        for reqs in todo:
            wq = sum(worst_cost(t) for t in reqs.values())
            if w + wq > head + 1e-12:
                break
            chunk.append(reqs)
            w += wq
        if not chunk:
            print(f"dm6f2f2f1: {len(todo)} question(s) not run: spent ${spent():.4f}; the next question's worst case would not fit "
                  f"the ${CAP} cap", flush=True)
            break
        todo = todo[len(chunk):]
        part = {k: g.params(O, t) for reqs in chunk for k, t in reqs.items()}
        texts = {k: t for reqs in chunk for k, t in reqs.items()}
        refusal = None
        for attempt in range(3):
            idmap = {f"r{n}": k for n, k in enumerate(part)}
            b = client.messages.batches.create(requests=[{"custom_id": c, "params": part[k]} for c, k in idmap.items()])
            t0 = time.time()
            entry = {"batch": b.id, "n": len(part), "worst_case": round(w, 4), "ended": False}
            blog.append(entry)
            save()                                       # the batch ID is on disk before polling starts
            print(f"dm6f2f2f1: batch {b.id}, {len(part)} requests ({len(chunk)} questions), worst case ${w:.4f}", flush=True)
            while b.processing_status != "ended":
                time.sleep(20)
                b = client.messages.batches.retrieve(b.id)
            entry.update(ended=True, seconds=round(time.time() - t0))
            retry = {}
            for res in client.messages.batches.results(b.id):
                k = idmap[res.custom_id]
                if res.result.type != "succeeded":
                    retry[k] = part[k]
                    continue
                msg = res.result.message
                pin, pout = g.PRICES[O]
                cost = g.DISCOUNT * (msg.usage.input_tokens * pin + msg.usage.output_tokens * pout) / 1e6
                sha = g.req_sha(O, texts[k])
                if msg.stop_reason == "refusal":
                    refusal = refusal or (k, msg, b.id)
                    cache[k] = {"raw": None, "guess": None, "conf": None, "refused": True, "cost": cost, "msg_id": msg.id, "sha": sha}
                    continue
                text = "".join(x.text for x in msg.content if x.type == "text")
                gs, c = (None, None) if msg.stop_reason == "max_tokens" else g.cf.parse(text, k.split("|")[1])
                cache[k] = {"raw": text, "guess": gs, "conf": c, "stop": msg.stop_reason, "cost": cost, "msg_id": msg.id,
                            "batch": b.id, "sha": sha, "in_tok": msg.usage.input_tokens, "out_tok": msg.usage.output_tokens}
            save()
            if refusal:
                k, msg, bid = refusal
                REFUSAL.write_text(f"# em-dm6f2f2f1 stopped on a refusal\n\nJob `{k}`, model `{msg.model}`, batch `{bid}`, message "
                                   f"`{msg.id}`\n\n```\n{getattr(msg, 'stop_details', None)}\n```\n\nNothing was reworded or retried; "
                                   "no further batch was submitted.\n")
                sys.exit(f"STOPPED on a refusal: {k} {msg.id}")
            if not retry:
                break
            part = retry
        else:
            save()
            sys.exit("dm6f2f2f1: requests still failing after two resubmissions; stopped")
        print(f"dm6f2f2f1: chunk done, ${spent():.4f}", flush=True)
    save()
    print(f"dm6f2f2f1: finished, ${spent():.4f}")


# --- analysis -----------------------------------------------------------------------------------------------------------

def read_rule(qs, X, seed, cats):
    """em-dm6f2's analyse(), with this bet's floor (MIN_Q usable questions) and the flagged-question floor."""
    old = f2.MIN_Q
    f2.MIN_Q = MIN_Q                                     # f2.verdict reads the module constant; restored below
    try:
        r = f2.analyse(qs, X, seed, cats)
    finally:
        f2.MIN_Q = old
    n_flagged = int((f2.flags(X).any(axis=1)).sum()) if len(qs) else 0
    r["n_flagged_questions"] = n_flagged
    r["verdict_before_flag_floor"] = r["verdict"]
    if len(qs) >= MIN_Q and n_flagged < MIN_FLAGGED:
        r["verdict"] = "untestable"
    r["sentence"] = None                                 # em-dm6f2's "On this archive" sentences are not written (as D87)
    return r


SENTENCES = {
    "pass": "With the number's wording fixed to the model's own guess, an overseer who double-checks every answer for which Opus stated a number below 70%, on questions where Sonnet and Haiku were themselves unsure, would have checked a substantially different set of questions depending on which of the two formats the number was asked in, by at least the pre-registered margin over two askings in the same format. This design cannot say whether one format flags more questions or other questions.",
    "fail": "With the number's wording fixed to the model's own guess, Opus's lists of answers below 70%, on questions where Sonnet and Haiku were themselves unsure, were not shown to differ by format more than they differ between two askings in the same format, by the pre-registered margin.",
    "untestable": "Too few questions carried a confidence number in all four cells, or too few were flagged under 70% in any cell, to read the rule on Opus.",
}


def matrix(cache):
    conf = {}
    for k, v in cache.items():
        if k.startswith("_"):
            continue
        _, fmt, r, q = k.split("|")
        conf.setdefault(q, {})[(fmt, int(r[1:]))] = v.get("conf")
    qs = sorted(q for q, d in conf.items() if all(d.get(c) is not None for c in f2.CELLS))
    return qs, np.array([[conf[q][c] for c in f2.CELLS] for q in qs], float).reshape(len(qs), 4), len(conf)


def analyse(seed, pilot=False):
    assert SEED_RECORDED is not None and seed == SEED_RECORDED["bootstrap"], "--seed must be the recorded bootstrap seed"
    R = results_dir()
    check_pins(R)
    cpath = R / CACHE.name
    full = json.loads(cpath.read_text())
    cache = {k: v for k, v in full.items() if not k.startswith("_")}
    P = pool(R)
    cats = {q: r["category"] for q, r in P.items()}
    drawn = questions(SEED_RECORDED["items"], R)
    qs, X, n_asked = matrix(cache)
    r = read_rule(qs, X, seed, cats)
    rows = {fmt: [dict(v, q=k.split("|")[3]) for k, v in cache.items() if k.split("|")[1] == fmt] for fmt in "PF"}
    out = {"seed": seed, "items_seed": SEED_RECORDED["items"], "questions_drawn": drawn, "n_asked": n_asked,
           "cost_usd": sum(v["cost"] for v in full.values()), "n_calls": len(cache),
           "cache_sha256": hashlib.sha256(cpath.read_bytes()).hexdigest(),
           "refused": sum(1 for v in cache.values() if v.get("refused")),
           "max_tokens": sum(1 for v in cache.values() if v.get("stop") == "max_tokens"),
           "floor": {"min_q": MIN_Q, "min_flagged": MIN_FLAGGED}, "opus": r,
           "secondary": {
               "below_half_yesno": {fmt: g.below_half_share(rows[fmt]) for fmt in "PF"},
               "yesno_share": {fmt: g.yesno_share(rows[fmt]) for fmt in "PF"},
               "usable_by_category": {c: sum(1 for q in qs if cats[q] == c) for c in sorted(set(cats.values()))},
               "flag_rate_by_category": {f"{fmt}|{c}": (float(np.mean([v["conf"] < f2.THRESH - f2.TOL for v in rows[fmt]
                                                                      if v.get("conf") is not None and cats[v["q"]] == c]))
                                                       if any(v.get("conf") is not None and cats[v["q"]] == c for v in rows[fmt]) else None)
                                         for fmt in "PF" for c in sorted(set(cats.values()))},
           }}
    pc = parent_cells(R).get("opus", {})                 # em-dm6f2f2's 20 Opus questions, where they overlap (reported)
    ov = [q for q in qs if q in pc and all(pc[q].get(c) is not None for c in f2.CELLS)]
    out["secondary"]["overlap_with_em_dm6f2f2_opus"] = {
        "questions": ov,
        "flagged_now": int(sum(f2.flags(X[qs.index(q)]).any() for q in ov)),
        "flagged_then": int(sum(any(pc[q][c] < f2.THRESH - f2.TOL for c in f2.CELLS) for q in ov))}
    v = r["verdict"]
    out["verdict"], out["sentence"] = v, SENTENCES[v]
    if v == "pass" and r.get("noise_asymmetric"):
        jl = r["J_PP"] if r["noisier_format"] == "probability" else r["J_FF"]
        out["sentence"] += (f" In the {r['noisier_format']} format, two askings overlapped no more than the two formats did "
                            f"(J {jl:.3f} against J_F {r['J_F']:.3f}), so for that format the difference between formats is no larger "
                            f"than its own repeat noise.")
    (R / OUT_JSON.name).write_text(json.dumps(out, indent=1, default=float))
    f = lambda x: f"{x:.3f}"
    L = ["# em-dm6f2f2f1 tables (generated by experiments/dm6f2f2f1_opus.py --analyse; do not edit)", "",
         f"{out['n_calls']} calls on {n_asked} questions, ${out['cost_usd']:.4f} at the batch rate, {out['refused']} refused, "
         f"{out['max_tokens']} at max_tokens; bootstrap seed {seed}, items seed {SEED_RECORDED['items']}.", "",
         "| model | usable questions (of asked) | flagged in any cell | flag rate P r0 / P r1 / F r0 / F r1 | J_F [95%] | J_N [95%] | J_PP / J_FF | noise asymmetric | D = J_N − J_F [95%] | verdict |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    if r.get("n_questions") and "J_F_ci" in r:
        fr = " / ".join(f"{x:.2f}" for x in r["flag_rate"].values())
        L.append(f"| opus | {r['n_questions']} of {n_asked} | {r['n_flagged_questions']} | {fr} | {f(r['J_F'])} [{f(r['J_F_ci'][0])}, {f(r['J_F_ci'][1])}] | "
                 f"{f(r['J_N'])} [{f(r['J_N_ci'][0])}, {f(r['J_N_ci'][1])}] | {f(r['J_PP'])} / {f(r['J_FF'])} | {r['noise_asymmetric']} | "
                 f"{r['D']:+.3f} [{r['D_ci'][0]:+.3f}, {r['D_ci'][1]:+.3f}] | {v} |")
    else:
        L.append(f"| opus | {r.get('n_questions', 0)} of {n_asked} | {r.get('n_flagged_questions', 0)} | — | — | — | — | — | — | {v} |")
    L += ["", f"**Verdict (Opus, the pre-registered rule): {v}**", "", out["sentence"], "", "## Secondary (reported, never promoted)", ""]
    for name in ("loo_flips", "cluster_D_ci", "cluster_verdict", "threshold_sensitivity", "J_F_rate_matched", "J_F_independent_sets",
                 "verdict_before_flag_floor"):
        if name in r:
            L.append(f"- {name}: {r[name]}")
    for name, val in out["secondary"].items():
        L.append(f"- {name}: {val}")
    (R / OUT_MD.name).write_text("\n".join(L) + "\n")
    print("\n".join(L))
    return out


# --- checks and dry run -------------------------------------------------------------------------------------------------

def selftest():
    R = results_dir()
    check_pins(R)
    U = unsure_set(R)
    P = pool(R)
    by = {c: sum(1 for q in U if P[q]["category"] == c) for c in sorted({P[q]["category"] for q in U})}
    assert len(U) == 80 and by == {"science-chemistry": 28, "science-physics": 25, "simpleqa": 27}, by
    qs = questions(12345, R)
    assert len(qs) == 4 * N_PER_CAT and len(set(qs)) == len(qs) and qs == questions(12345, R)
    assert sum(P[q]["category"] == "claim" for q in qs) == N_PER_CAT and all(P[q]["category"] == "claim" or q in U for q in qs)
    t = g.TEMPLATES["P"].format(q=P[qs[0]]["question"])
    assert "YOUR guess above" in t and g.params(O, t)["max_tokens"] == 300 and g.params(O, t)["output_config"] == {"effort": "low"}
    assert 0.0030 < worst_cost(t) < 0.0045, worst_cost(t)
    # floors: 24 usable -> untestable; 30 usable but 5 flagged -> untestable; a strong level shift on 30 usable -> pass
    rng = np.random.default_rng(3)
    base = rng.uniform(0.75, 1.0, 30)
    X = np.c_[base, base, base, base]
    X[:12, :2] = 0.5                                      # 12 questions flagged in P only
    assert read_rule([f"q{i}" for i in range(30)], X, 1, None)["verdict"] == "pass"
    assert read_rule([f"q{i}" for i in range(25)], X[:25], 1, None)["verdict"] == "pass"
    assert read_rule([f"q{i}" for i in range(24)], X[:24], 1, None)["verdict"] == "untestable"
    X2 = np.c_[base, base, base, base]; X2[:5, :2] = 0.5
    assert read_rule([f"q{i}" for i in range(30)], X2, 1, None)["verdict"] == "untestable"
    assert f2.MIN_Q == 40                                 # the shared module's floor is restored
    print(f"selftest: unsure set {len(U)} {by}; draw of 40 repeatable, 10 claim; Opus prompt as em-dm6f2f2; "
          f"worst case per request ${worst_cost(t):.4f}; floors and pass checks hold")


def dry_run(n_sims=100, nboot=1000, cut=None):
    """Worlds from em-dm6f2f2's archive (P15; Opus's own answers on these questions are mostly unknown).
    'sonnet-like': each drawn question's four Opus cells are Sonnet's em-dm6f2f2 numbers; 'haiku-like': Haiku's;
    'opus-confident': Sonnet's numbers with the distance from 1 shrunk so the unsure questions' flag rate matches what
    Opus showed on em-dm6f2f2's unsure questions; 'no format effect': the P cells take the crossed F cells.
    In every world each non-claim call is cut off (no number) with Opus's measured rate on em-dm6f2f2's non-claim calls."""
    R = results_dir()
    P, U, cells = pool(R), unsure_set(R), parent_cells(R)
    oc = cells["opus"]
    nonclaim = [(q, c) for q in oc if P[q]["category"] != "claim" for c in f2.CELLS]
    cut = cut if cut is not None else sum(oc[q].get(c) is None for q, c in nonclaim) / len(nonclaim)
    ou = [x for q in oc if q in U for x in oc[q].values() if x is not None]
    opus_rate = float(np.mean([x < 0.70 for x in ou]))
    son = [x for q in U for x in cells["sonnet"][q].values() if x is not None]
    son_rate = float(np.mean([x < 0.70 for x in son]))
    ks = np.linspace(0.05, 1.0, 96)                       # shrink factor k: x' = 1 - k (1 - x)
    rate_k = [np.mean([1 - k * (1 - x) < 0.70 for x in son]) for k in ks]
    k_conf = float(ks[int(np.argmin([abs(rk - opus_rate) for rk in rate_k]))])
    claims = sorted(q for q, r in P.items() if r["category"] == "claim")
    bycat = {c: [q for q in U if P[q]["category"] == c] for c in ("science-chemistry", "science-physics", "simpleqa")}

    def world(name, rng):
        qs = list(rng.choice(claims, N_PER_CAT, replace=False))
        for c, ids in bycat.items():
            qs += list(rng.choice(ids, N_PER_CAT, replace=False))
        src = "haiku" if name.startswith("haiku") else "sonnet"
        X = np.array([[cells[src][q].get(c) if cells[src][q].get(c) is not None else np.nan for c in f2.CELLS] for q in qs], float)
        if "confident" in name:
            X = 1 - k_conf * (1 - X)
        if "no format" in name:
            X = X[:, [3, 2, 2, 3]]                       # P r0 <- F r1, P r1 <- F r0 (crossed); F cells unchanged
        for i, q in enumerate(qs):
            if P[q]["category"] != "claim":
                X[i, rng.random(4) < cut] = np.nan
        keep = ~np.isnan(X).any(axis=1)
        return [q + f"#{i}" for i, q in enumerate(qs) if keep[i]], X[keep]

    out = {"cut_rate": cut, "opus_flag_rate_unsure": opus_rate, "sonnet_flag_rate_unsure": son_rate, "k_confident": k_conf, "worlds": {}}
    rng = np.random.default_rng(20261105)
    for name in ("sonnet-like", "opus-confident", "haiku-like", "no format effect (sonnet-like)", "no format effect (opus-confident)"):
        labs, ns, nf = [], [], []
        for i in range(n_sims):
            qs, X = world(name, rng)
            r = read_rule(qs, X, 100 + i, None)
            labs.append(r["verdict"]); ns.append(len(qs)); nf.append(r["n_flagged_questions"])
        out["worlds"][name] = {k: labs.count(k) / n_sims for k in ("pass", "fail", "untestable")}
        out["worlds"][name].update(mean_usable=float(np.mean(ns)), mean_flagged=float(np.mean(nf)))
        print(f"dry run {name:36s} " + "  ".join(f"{k} {v:.3f}" if isinstance(v, float) and k in ('pass', 'fail', 'untestable')
                                                    else f"{k} {v:.1f}" for k, v in out["worlds"][name].items()), flush=True)
    return out


def cost_sim(n_sims=2000):
    """Fake-client cost check: each request's cost drawn from em-dm6f2f2's measured Opus costs for its category
    (claim / non-claim), chunks sized as run() sizes them. Reports P(all 40 questions run) and the spend."""
    R = results_dir()
    P = pool(R)
    c = json.loads((R / "dm6f2f2-calls.json").read_text())
    cc = {"claim": [v["cost"] for k, v in c.items() if k.startswith("opus|") and P[k.split("|")[3]]["category"] == "claim"],
          "other": [v["cost"] for k, v in c.items() if k.startswith("opus|") and P[k.split("|")[3]]["category"] != "claim"]}
    qs = questions(12345, R)
    W = [sum(worst_cost(g.TEMPLATES[fmt].format(q=P[q]["question"])) for fmt, _ in CELL_KEYS) for q in qs]
    rng = np.random.default_rng(7)
    done, spend, batches = [], [], []
    for _ in range(n_sims):
        s, i, nb = 0.0, 0, 0
        while i < len(qs):
            head, w, j = CAP - s - RESERVE, 0.0, i
            while j < len(qs) and w + W[j] <= head + 1e-12:
                w += W[j]; j += 1
            if j == i:
                break
            for q in qs[i:j]:
                s += float(np.sum(rng.choice(cc["claim" if P[q]["category"] == "claim" else "other"], 4)))
            i, nb = j, nb + 1
        done.append(i == len(qs)); spend.append(s); batches.append(nb)
    out = {"p_all_run": float(np.mean(done)), "mean_spend": float(np.mean(spend)), "p95_spend": float(np.percentile(spend, 95)),
           "max_spend": float(np.max(spend)), "mean_batches": float(np.mean(batches))}
    print(f"cost sim: P(all 40 run) {out['p_all_run']:.3f}; spend mean ${out['mean_spend']:.4f}, 95th ${out['p95_spend']:.4f}, "
          f"max ${out['max_spend']:.4f} (cap ${CAP}); batches mean {out['mean_batches']:.1f}")
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--print-questions" in a:
        assert SEED_RECORDED is not None, "needs the recorded items seed"
        P = pool()
        for q in questions(SEED_RECORDED["items"]):
            print(q, P[q]["category"], P[q]["question"][:90].replace("\n", " "))
    elif "--selftest" in a:
        selftest()
    elif "--dry-run" in a:
        out = {"dry_run": dry_run(), "cost_sim": cost_sim()}
        (RESULTS / "dm6f2f2f1-dry-run.json").write_text(json.dumps(out, indent=1) + "\n")
    elif "--run" in a:
        run()
    elif "--analyse" in a:
        analyse(int(a[a.index("--seed") + 1]))
    else:
        print(__doc__)
