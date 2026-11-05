"""em-gm2bf1f1 (map gm2bf1-f1): with fresh question-order conversations, do the claims that move with question order
still move with answer format, under both noise guards? Pre-registered in experiments/gm2bf1f1-fresh-order.md.

    python experiments/gm2bf1f1_fresh_order.py --selftest           # guards, verdict, groups; synthetic data; no calls
    python experiments/gm2bf1f1_fresh_order.py --dry-run            # P(pass) in worlds built from em-gm2bf1's archives; no calls
    python experiments/gm2bf1f1_fresh_order.py --run                # paid run (Batches API; cap $1.00 in code; stop on refusal)
    python experiments/gm2bf1f1_fresh_order.py --analyse --seed S   # S must be the recorded beacon seed

Order measures, format measures and the D71 guard are imported unchanged from experiments/gm2bf1_order_vs_format.py
(em-gm2bf1); the chain prompts from experiments/gm2q_questions_only.py (gm2's shown chain, unchanged).
- Haiku (primary): fresh shown chains on all 40 experiment-5 items, O1-O4, 10 per order; format spread from
  results/gm3b-calls.json (Haiku, six formats, 160 claims).
- Sonnet (secondary): fresh shown chains on em-dm2's 20 items, 3 per order; format spread from
  results/mm-gm3b-sonnet-calls.json (80 claims).
- Opus (secondary): no new calls; em-gm2q2's fresh Opus shown chains on gm2's 10 items (6 per order,
  results/gm2q2-conversations.json); format spread from results/mm-gm3b-opus-calls.json (40 claims).
Calls cached in results/gm2bf1f1-conversations.json; refusal record results/refusal-gm2bf1f1.md."""

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))
sys.path.insert(0, str(HERE))
import gm2bf1_order_vs_format as b1                     # em-gm2bf1: order/format measures and the D71 guard, unchanged
import gm2q_questions_only as q1                        # gm2's shown chain prompts, unchanged
from scipy.stats import rankdata

H, S, O = "claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"
SHORT = {H: "haiku", S: "sonnet", O: "opus"}
ORDERS = q1.ORDERS
REPS = {H: 10, S: 3}
CAP, RESERVE, DISCOUNT, MARGIN = 1.00, 0.05, 0.5, 1.10
MAXTOK = {H: 200, S: 1000}                              # gm2's Haiku setting; em-dm4's Sonnet setting
OFFP = {H: {"thinking": {"type": "disabled"}}, S: {"thinking": {"type": "between_tools"}}}
PRICES = {H: (0.10, 0.50), S: (2.00, 10.00)}
EST = {H: 0.000026, S: 0.000526}                        # per request at the batch rate (em-dm4 / gm2 chains)
RHO_BAR, TOL, NBOOT = 0.30, 1e-9, 10000
MIN_CLAIMS = 120                                        # Haiku: fewer usable claims -> untestable (em-gm2bf1's floor)
SEED_RECORDED = None                                    # filled in by the seed commit
RESULTS = HERE.parent / "results"
CACHE, BATCHLOG = RESULTS / "gm2bf1f1-conversations.json", RESULTS / "gm2bf1f1-batches.json"
REFUSAL = RESULTS / "refusal-gm2bf1f1.md"
OUT_JSON, OUT_MD = RESULTS / "gm2bf1f1-fresh-order.json", RESULTS / "gm2bf1f1-fresh-order-tables.md"
GM2 = HERE / "gm2-planted-values.json"
GM2B = HERE / "gm2b-planted-values.json"
SPLIT = HERE / "split-exp5.json"
POOL = RESULTS / "pool-run-3.json"


def item_sets():
    split = json.loads(SPLIT.read_text())
    cand = split["candidates"]
    return {"haiku": list(cand), "sonnet": cand[0:10] + cand[20:30],          # mm_gm3b.items20()
            "opus": sorted(json.loads(GM2.read_text())["items"]), "gm2": sorted(json.loads(GM2.read_text())["items"])}


def chains():
    recs = {r["id"]: r for r in json.loads(POOL.read_text())["records"]}
    planted = json.loads(GM2B.read_text())["items"]
    split = json.loads(SPLIT.read_text())
    for q in split["candidates"]:
        assert [int(k) for k in planted[q]["chain_claims"]] == [int(k) for k in split["chain_claims"][q]], q
    return recs, {q: planted[q]["chain_claims"] for q in planted}


# --- calls ------------------------------------------------------------------------------------------------------------

def params(model, messages):
    p = {"model": model, "max_tokens": MAXTOK[model], "messages": messages,
         "output_config": {"format": {"type": "json_schema", "schema": q1.RATING}}}
    p.update(json.loads(json.dumps(OFFP[model])))
    return p


def run(client=None):
    if REFUSAL.exists():
        sys.exit(f"gm2bf1f1: {REFUSAL.name} exists; a refused run is never resumed, reworded or retried")
    if client is None:
        import anthropic
        from dotenv import load_dotenv
        load_dotenv(Path("/Users/seanpharris/entangled-mind/.env"))
        client = anthropic.Anthropic(max_retries=4)
    recs, cc = chains()
    its = item_sets()
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    blog = json.loads(BATCHLOG.read_text()) if BATCHLOG.exists() else []
    convs = {}
    for m in (H, S):
        for q in its[SHORT[m]]:
            for o in ORDERS:
                for r in range(REPS[m]):
                    key = f"{SHORT[m]}|{q}|{o}|shown|{r}"
                    if key in cache:
                        continue
                    t = q1.chain_turns(recs[q], cc[q], o)
                    convs[key] = {"model": m, "texts": [x[2] for x in t], "kinds": [(x[0], x[1]) for x in t], "msgs": [],
                                  "turns": [], "cost": 0.0, "ids": []}

    prior_lost = cache.pop("_unfinished", {}).get("cost", 0.0) + cache.pop("_lost_prior", {}).get("cost", 0.0)
    for e in blog:                                       # a batch submitted but never recorded as ended: collect its cost
        if not e.get("ended"):
            b = client.messages.batches.retrieve(e["batch"])
            while b.processing_status != "ended":
                time.sleep(20)
                b = client.messages.batches.retrieve(e["batch"])
            lost = 0.0
            for res in client.messages.batches.results(e["batch"]):
                if res.result.type == "succeeded":
                    msg = res.result.message
                    pin, pout = PRICES.get(msg.model, PRICES[S])
                    lost += DISCOUNT * (msg.usage.input_tokens * pin + msg.usage.output_tokens * pout) / 1e6
            e.update(ended=True, collected_after_crash=True, billed_usd=lost)
            prior_lost += lost
    cache["_lost_prior"] = {"cost": prior_lost}

    def save():
        cache["_unfinished"] = {"cost": sum(c["cost"] for k, c in convs.items() if k not in cache)}
        CACHE.write_text(json.dumps(cache))
        BATCHLOG.write_text(json.dumps(blog, indent=1))

    spent_done = lambda: sum(v["cost"] for k, v in cache.items() if k != "_unfinished")   # includes _lost_prior
    save()
    proj = sum(len(c["texts"]) * EST[c["model"]] for c in convs.values())
    if spent_done() + proj + RESERVE > CAP + TOL:
        sys.exit(f"gm2bf1f1: projected ${proj:.3f} does not fit the ${CAP} cap; not started")
    rnd = 0
    while True:
        live = {k: c for k, c in convs.items() if len(c["turns"]) < len(c["texts"]) and not c.get("ended")}
        if not live:
            break
        rnd += 1
        def per_req(m):
            xs = [c["cost"] / len(c["turns"]) for c in convs.values() if c["model"] == m and c["turns"]]
            return max(EST[m], float(np.mean(xs))) if xs else EST[m]
        spent = spent_done() + sum(c["cost"] for k, c in convs.items() if k not in cache)
        this_round = sum(per_req(c["model"]) for c in live.values())
        remaining = sum((len(c["texts"]) - len(c["turns"])) * per_req(c["model"]) for c in live.values())
        if spent + this_round * MARGIN + RESERVE > CAP + TOL or spent + remaining + RESERVE > CAP + TOL:
            save()
            sys.exit(f"gm2bf1f1: cap ${CAP}: spent ${spent:.3f}, next ${this_round:.3f}, remaining ${remaining:.3f}; stopped before round {rnd}")
        part = {}
        for k, c in live.items():
            c["msgs"].append({"role": "user", "content": c["texts"][len(c["turns"])]})
            part[k] = params(c["model"], list(c["msgs"]))
        refusal = None
        for attempt in range(3):
            idmap = {f"r{n}": k for n, k in enumerate(part)}
            b = client.messages.batches.create(requests=[{"custom_id": cid, "params": part[k]} for cid, k in idmap.items()])
            t0 = time.time()
            entry = {"round": rnd, "batch": b.id, "n": len(part), "ended": False}
            blog.append(entry)
            save()                                       # the batch ID is on disk before polling starts
            print(f"gm2bf1f1: round {rnd} batch {b.id}, {len(part)} requests", flush=True)
            while b.processing_status != "ended":
                time.sleep(20)
                b = client.messages.batches.retrieve(b.id)
            entry.update(ended=True, seconds=round(time.time() - t0))
            retry = {}
            for res in client.messages.batches.results(b.id):
                k = idmap[res.custom_id]
                c = convs[k]
                if res.result.type != "succeeded":
                    retry[k] = part[k]
                    continue
                msg = res.result.message
                pin, pout = PRICES[c["model"]]
                c["cost"] += DISCOUNT * (msg.usage.input_tokens * pin + msg.usage.output_tokens * pout) / 1e6
                c["ids"].append(msg.id)
                kind, claim = c["kinds"][len(c["turns"])]
                if msg.stop_reason == "refusal":
                    refusal = refusal or (k, msg, b.id)
                    c["turns"].append({"kind": kind, "claim": claim, "rating": None, "raw": None, "refused": True})
                    c["ended"] = True
                    continue
                text = "".join(x.text for x in msg.content if x.type == "text")
                try:
                    r = None if msg.stop_reason == "max_tokens" else min(100, max(0, int(json.loads(text)["rating"])))
                except Exception:
                    r = None
                c["turns"].append({"kind": kind, "claim": claim, "rating": r, "raw": text})
                if r is None:
                    c["ended"] = True
                else:
                    c["msgs"].append({"role": "assistant", "content": text})
            for k, c in convs.items():
                if (len(c["turns"]) == len(c["texts"]) or c.get("ended")) and k not in cache:
                    cache[k] = {"turns": c["turns"], "cost": c["cost"], "msg_ids": c["ids"],
                                "missing": c["turns"][-1]["rating"] is None or len(c["turns"]) < len(c["texts"])}
            save()
            if refusal:
                k, msg, bid = refusal
                REFUSAL.write_text(f"# em-gm2bf1f1 stopped on a refusal\n\nJob `{k}`, model `{msg.model}`, batch `{bid}`, "
                                   f"message `{msg.id}`\n\n```\n{getattr(msg, 'stop_details', None)}\n```\n\nNothing was reworded or "
                                   "retried; no further batch was submitted.\n")
                sys.exit(f"STOPPED on a refusal: {k} {msg.id}")
            if not retry:
                break
            part = retry
        else:
            save()
            sys.exit("gm2bf1f1: requests still failing after two resubmissions; stopped")
        print(f"gm2bf1f1: round {rnd} done; ${spent_done():.4f}", flush=True)
    save()
    print(f"gm2bf1f1: complete, ${spent_done():.4f}")


# --- analysis -----------------------------------------------------------------------------------------------------------

def partial_frozen(a, b, covs):
    """em-gm2bf1's guard as first frozen (its pre-registration §4): Pearson correlation of the ranks' residuals after
    least squares on the plain ranks of the covariates (E and W)."""
    Z = np.column_stack([np.ones(len(a))] + [rankdata(c) for c in covs])
    ra, rb = rankdata(a), rankdata(b)
    ea = ra - Z @ np.linalg.lstsq(Z, ra, rcond=None)[0]
    eb = rb - Z @ np.linalg.lstsq(Z, rb, rcond=None)[0]
    return float(np.corrcoef(ea, eb)[0, 1])


def stats3(S_, G, E, W, Eo, idx):
    return (b1.spearman(S_[idx], G[idx]), partial_frozen(S_[idx], G[idx], [E[idx], W[idx]]),
            b1.partial_spearman(S_[idx], G[idx], [E[idx], Eo[idx], W[idx]]))


def label(n, rho, rho_lo, pf_lo, pd_lo, groups, min_claims=MIN_CLAIMS):
    """§5: rho >= 0.30, rho's lower bound > 0, both guards' lower bounds > 0, and rho > 0 in each item group."""
    if n < min_claims:
        return "untestable"
    if (rho >= RHO_BAR - TOL and rho_lo > TOL and pf_lo > TOL and pd_lo > TOL
            and all(g == g and g > TOL for g in groups.values())):
        return "pass"
    return "fail"


def analyse_arm(S_, G, E, W, Eo, items_of, groups_of, seed, min_claims, nboot=NBOOT):
    ok = ~(np.isnan(S_) | np.isnan(G) | np.isnan(E) | np.isnan(W) | np.isnan(Eo))
    idx = np.where(ok)[0]
    n = len(idx)
    res = {"n_claims": n}
    if n < 10:
        res["label"] = "untestable"
        return res
    rho, pf, pd = stats3(S_, G, E, W, Eo, idx)
    items = sorted({items_of[i] for i in idx})
    by = {it: np.array([i for i in idx if items_of[i] == it]) for it in items}
    rng = np.random.default_rng(seed % 2**63)
    B = np.array([stats3(S_, G, E, W, Eo, np.concatenate([by[items[j]] for j in rng.integers(0, len(items), len(items))]))
                  for _ in range(nboot)])
    lo, hi = np.percentile(B, 2.5, axis=0), np.percentile(B, 97.5, axis=0)
    groups = {}
    for gname in sorted({groups_of[i] for i in idx}):
        gi = np.array([i for i in idx if groups_of[i] == gname])
        groups[gname] = b1.spearman(S_[gi], G[gi]) if len(gi) >= 4 else float("nan")
    lab = label(n, rho, lo[0], lo[1], lo[2], groups, min_claims)
    flips = []
    for it in items:
        keep = np.array([i for i in idx if items_of[i] != it])
        r1, f1, d1 = stats3(S_, G, E, W, Eo, keep)
        g1 = {gn: (b1.spearman(S_[[i for i in keep if groups_of[i] == gn]], G[[i for i in keep if groups_of[i] == gn]])
                   if sum(1 for i in keep if groups_of[i] == gn) >= 4 else float("nan")) for gn in groups}
        if label(n, r1, lo[0] + r1 - rho, lo[1] + f1 - pf, lo[2] + d1 - pd, g1, min_claims) != lab:
            flips.append(it)
    res.update(n_items=len(items), rho=rho, rho_ci=[float(lo[0]), float(hi[0])], partial_frozen=pf,
               partial_frozen_ci=[float(lo[1]), float(hi[1])], partial_d71=pd, partial_d71_ci=[float(lo[2]), float(hi[2])],
               groups=groups, label=lab, loo_item_flips=flips,
               rho_S_W=b1.spearman(S_[idx], W[idx]), rho_G_W=b1.spearman(G[idx], W[idx]),
               median_span=float(np.nanmedian(S_[idx])))
    return res


def format_arm(cache_file, claim_list):
    """Per-claim format spread G and extremity E among claim_list, from a six-format cache (em-gm3b's decoder)."""
    import gm3b_format_invariance as g
    import gm3c_heldout_format as h
    conv = {k: v for k, v in json.loads(cache_file.read_text()).items() if isinstance(v, dict) and v.get("value") is not None}
    obs, nc = g.encode(conv)
    allc = g.claims()
    fm = np.column_stack([h.claim_means(h.observed_scale(f, obs[f]), obs[f]["c"], nc) for f in g.FORMATS])
    rows = np.array([allc.index(c) for c in claim_list])
    sub = fm[rows]
    keep = ~np.isnan(sub).any(axis=1)
    G, E = np.full(len(claim_list), np.nan), np.full(len(claim_list), np.nan)
    if keep.sum() >= 4:
        Gk, Ek = b1.format_measures(sub[keep], sub[keep, 0])
        G[keep], E[keep] = Gk, Ek
    return G, E


def analyse(seed):
    assert SEED_RECORDED is not None and seed == SEED_RECORDED, f"--seed must be the recorded beacon seed {SEED_RECORDED}"
    import gm3b_format_invariance as g
    its = item_sets()
    allc = g.claims()
    full = json.loads(CACHE.read_text())
    fresh = {k.split("|", 1)[1]: v for k, v in full.items() if not k.startswith("_")}   # _unfinished, _lost_prior: costs only
    by_model = {"haiku": {k.split("|", 1)[1]: v for k, v in full.items() if k.startswith("haiku|")},
                "sonnet": {k.split("|", 1)[1]: v for k, v in full.items() if k.startswith("sonnet|")},
                "opus": {k.split("|", 1)[1]: v for k, v in json.loads((RESULTS / "gm2q2-conversations.json").read_text()).items()
                         if k.startswith("opus|") and "|shown|" in k}}
    fmt_file = {"haiku": RESULTS / "gm3b-calls.json", "sonnet": RESULTS / "mm-gm3b-sonnet-calls.json", "opus": RESULTS / "mm-gm3b-opus-calls.json"}
    out = {"seed": seed, "cost_usd": sum(v.get("cost", 0) for v in full.values()),
           "n_conversations": len(fresh), "n_missing": sum(1 for v in fresh.values() if v.get("missing")),
           "sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [CACHE, RESULTS / "gm2q2-conversations.json", *fmt_file.values()]},
           "arms": {}}
    for arm, min_claims in (("haiku", MIN_CLAIMS), ("sonnet", 10), ("opus", 10)):
        cl = [c for c in allc if c[0] in its[arm]]
        conv = {k: v for k, v in by_model[arm].items() if not v.get("missing")}
        S_, W, Eo = b1.order_measures(conv, cl, "shown")
        G, E = format_arm(fmt_file[arm], cl)
        items_of = [q for q, _ in cl]
        groups_of = ["gm2" if q in its["gm2"] else "gm2b" for q in items_of]
        out["arms"][arm] = analyse_arm(S_, G, E, W, Eo, items_of, groups_of, seed + {"haiku": 0, "sonnet": 1, "opus": 2}[arm], min_claims)
    out["verdict"] = out["arms"]["haiku"]["label"]
    OUT_JSON.write_text(json.dumps(out, indent=1, default=float))
    f = lambda x: f"{x:+.3f}"
    L = ["# em-gm2bf1f1 tables (generated by experiments/gm2bf1f1_fresh_order.py --analyse; do not edit)", "",
         f"{out['n_conversations']} fresh conversations ({out['n_missing']} missing), ${out['cost_usd']:.4f} at the batch rate; seed {seed}.", "",
         "| arm | claims (items) | ρ(order span, format spread) [95%] | frozen guard partial ρ [95%] | D71 guard partial ρ [95%] | ρ in gm2's items / gm2b's | label | leave-one-item-out flips |",
         "|---|---|---|---|---|---|---|---|"]
    for arm, r in out["arms"].items():
        if "rho" not in r:
            L.append(f"| {arm} | {r['n_claims']} | — | — | — | — | {r['label']} | — |")
            continue
        gs = " / ".join(f"{r['groups'].get(k, float('nan')):+.2f}" for k in ("gm2", "gm2b"))
        L.append(f"| {arm}{' (primary)' if arm == 'haiku' else ' (secondary)'} | {r['n_claims']} ({r['n_items']}) | {f(r['rho'])} [{f(r['rho_ci'][0])}, {f(r['rho_ci'][1])}] | "
                 f"{f(r['partial_frozen'])} [{f(r['partial_frozen_ci'][0])}, {f(r['partial_frozen_ci'][1])}] | "
                 f"{f(r['partial_d71'])} [{f(r['partial_d71_ci'][0])}, {f(r['partial_d71_ci'][1])}] | {gs} | {r['label']} | {', '.join(r['loo_item_flips']) or 'none'} |")
    L += ["", f"**Verdict (Haiku, the pre-registered rule): {out['verdict']}**", "",
          "Secondary: " + "; ".join(f"{a}: order span vs within-order SD ρ {r.get('rho_S_W', float('nan')):+.2f}, format spread vs within-order SD ρ {r.get('rho_G_W', float('nan')):+.2f}, median span {r.get('median_span', float('nan')):.1f}"
                                     for a, r in out["arms"].items())]
    OUT_MD.write_text("\n".join(L) + "\n")
    print("\n".join(L))
    return out


# --- self-test and dry run ----------------------------------------------------------------------------------------------

def selftest():
    assert label(160, 0.35, 0.1, 0.05, 0.05, {"gm2": 0.1, "gm2b": 0.4}) == "pass"
    assert label(160, 0.35, 0.1, 0.0, 0.05, {"gm2": 0.1, "gm2b": 0.4}) == "fail"          # frozen guard's bound at 0 fails
    assert label(160, 0.35, 0.1, 0.05, 0.05, {"gm2": -0.1, "gm2b": 0.4}) == "fail"        # one group not positive
    assert label(160, 0.35, 0.1, 0.05, 0.05, {"gm2": float("nan"), "gm2b": 0.4}) == "fail"
    assert label(160, 0.30, 0.1, 0.05, 0.05, {"gm2": 0.1, "gm2b": 0.4}) == "pass"         # bar met exactly
    assert label(160, 0.30 - 1e-6, 0.1, 0.05, 0.05, {"gm2": 0.1, "gm2b": 0.4}) == "fail"
    assert label(119, 0.9, 0.5, 0.5, 0.5, {"gm2": 0.5, "gm2b": 0.5}) == "untestable"
    rng = np.random.default_rng(0)
    n, items = 160, [f"q{i // 4}" for i in range(160)]
    grp = ["gm2" if i < 40 else "gm2b" for i in range(160)]
    W = rng.gamma(4, 2, n); E = rng.uniform(0, 50, n); Eo = rng.uniform(0, 50, n)
    shared = rng.normal(0, 1, n)
    S_ = W * 1.5 + 6 * shared + rng.normal(0, 2, n); G = 0.05 + 0.04 * shared + rng.normal(0, 0.02, n)
    r = analyse_arm(S_, G, E, W, Eo, items, grp, 1, MIN_CLAIMS, nboot=400)
    assert r["label"] == "pass", r
    G2 = 0.05 + 0.004 * W + rng.normal(0, 0.02, n)                                       # link only through noise W
    r2 = analyse_arm(S_ - 6 * shared, G2, E, W, Eo, items, grp, 1, MIN_CLAIMS, nboot=400)
    assert r2["label"] == "fail", r2
    print("selftest: all checks hold (shared-instability world passes; noise-only world fails:", round(r2["partial_frozen"], 3), ")")


def dry_run(n_sims=100, nboot=400):
    """Haiku worlds from em-gm2bf1's archives (P15): fresh chains drawn by resampling the archived conversations within
    each item x order cell (the archive world), and the same with format spread shuffled across claims within item
    (no-link world), and link worlds where each claim's span carries c extra points per SD of its format spread
    (shared instability beyond noise; c = 3, 6, 10). Reports P(pass) for the primary."""
    import gm3b_format_invariance as g
    conv = {}
    for f in ("gm2-conversations.json", "gm2b-conversations.json"):
        conv.update(json.loads((RESULTS / f).read_text()))
    allc = g.claims()
    G, E = format_arm(RESULTS / "gm3b-calls.json", allc)
    its = item_sets()
    items_of = [q for q, _ in allc]
    groups_of = ["gm2" if q in its["gm2"] else "gm2b" for q in items_of]
    cells = {}
    for k, v in conv.items():
        q, o, cond, r = k.split("|")
        if cond == "shown" and o in ORDERS:
            cells.setdefault((q, o), []).append(v)
    rng = np.random.default_rng(20261105)
    out = {}
    zG = (G - np.nanmean(G)) / np.nanstd(G)
    for world in ("archive", "no link (format spread shuffled within item)", "link c=3", "link c=6", "link c=10"):
        labs = []
        for i in range(n_sims):
            sim = {}
            for (q, o), vs in cells.items():
                for r in range(REPS[H]):
                    sim[f"{q}|{o}|shown|{r}"] = vs[int(rng.integers(len(vs)))]
            S_, W, Eo = b1.order_measures(sim, allc, "shown")
            if world.startswith("link"):
                S_ = np.maximum(0.0, S_ + float(world.split("=")[1]) * zG)
            Gw = G.copy()
            if world.startswith("no link"):
                for q in set(items_of):
                    ix = [j for j, x in enumerate(items_of) if x == q]
                    Gw[ix] = Gw[rng.permutation(ix)]
            labs.append(analyse_arm(S_, Gw, E, W, Eo, items_of, groups_of, 1000 + i, MIN_CLAIMS, nboot)["label"])
        out[world] = {k: labs.count(k) / n_sims for k in ("pass", "fail", "untestable")}
        print(f"dry run haiku {world:48s} " + "  ".join(f"{k} {v:.2f}" for k, v in out[world].items()), flush=True)
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        selftest()
    elif "--dry-run" in a:
        (RESULTS / "gm2bf1f1-dry-run.json").write_text(json.dumps(dry_run(), indent=1) + "\n")
    elif "--run" in a:
        run()
    elif "--analyse" in a:
        analyse(int(a[a.index("--seed") + 1]))
    else:
        print(__doc__)
