"""P2-5 dry run, every call stubbed (no API, no key read for a call). Synthetic data only; nothing here is test data.

    /Users/seanpharris/entangled-mind/.venv/bin/python experiments/p2_5_dryrun.py > experiments/p2-5-dryrun-output.txt

What it shows, with the frozen code in p2_5_egocentric.py:
  1. the prompts the run will send (one vignette, d = +30, every condition and question), and that each knob moves them;
  2. the section 5 rule against synthetic responders, dumb ones first, beside the map's rule alone (P3);
  3. power of the full rule over a grid of true leakage and source-blind pull (P2), with vignette-level heterogeneity;
  4. the machinery: a stubbed refusal is written into the cache and a re-run makes 0 calls; the cap stops the run;
     a tampered cache entry is caught; the gate is closed without a design review or a seed file.
The responders' uptake profile for the model's own re-rating is F3's (bm0: 0.71 / 0.44 / 0.21 at 10 / 30 / 60 points)."""

import json
import re
import tempfile
from pathlib import Path
from types import SimpleNamespace

import numpy as np

import om_common as om
import p2_5_egocentric as P

DRY_SEED = 20261104            # a fixed seed for synthetic data and the dry-run bootstrap; the test uses the beacon's
items, anchors = P.load_items()
by_id = {it["id"]: it for it in items}
F3 = {10: 0.71, 30: 0.44, 60: 0.21}


def parse(msgs):
    own = json.loads(msgs[1]["content"])["probability"]
    last = msgs[2]["content"]
    alex = int(re.search(r"answered (\d+)\.", last).group(1))
    q = ("self" if last.split(". ", 1)[1].startswith("Please") else
         "sam_i" if "another instance of you" in last else
         "sam_inf" if "has also seen your earlier answer" in last else "sam_p")
    stmt_q = msgs[0]["content"]
    return own, alex, q, stmt_q


def u_f3(D):
    a = abs(D)
    return float(np.interp(a, [0, 10, 30, 60], [0.9, F3[10], F3[30], F3[60]]))


class Responder:
    """A synthetic model. kind picks how each question responds to the own slot and the Alex slot. Per item-statement
    prior offset and heterogeneity are fixed by the seed; per-call noise sd 1 point, rounded to an integer."""

    def __init__(self, kind, lam=0.5, alpha=0.0, het=0.5, seed=DRY_SEED, noise=1.0):
        self.kind, self.lam, self.alpha, self.het, self.noise = kind, lam, alpha, het, noise
        rng = np.random.default_rng(seed)
        self.off = {(it["id"], o): rng.normal(0, 3) for it in items for o in "XY"}
        self.fac = {(it["id"], o): max(0.0, 1 + rng.normal(0, het)) for it in items for o in "XY"}
        self.afac = {(it["id"], o): rng.normal(0, 0.1) for it in items for o in "XY"}
        self.rng = np.random.default_rng(seed + 1)
        self.m_of = {it["context"]: it for it in items}

    FIRST = {P.ask(it[o], it["context"]): ((it["id"], o), round(anchors[it["id"]][f"m_{o}"])) for it in items for o in "XY"}

    def key_m(self, stmt_q):
        return self.FIRST[stmt_q]

    def value(self, msgs):
        own, alex, q, sq = parse(msgs)
        k, m = self.key_m(sq)
        prior = m + self.off[k]
        Do, Da = own - m, alex - m
        own_shift = u_f3(Do) * Do * self.fac[k] + 0.02 * Da
        kd = self.kind
        if kd == "constant":
            y = 50
        elif kd == "rederive":
            y = prior
        elif kd == "last_number":
            y = alex
        elif kd == "own_slot_copier":
            y = own
        elif kd == "source_blind":
            y = prior + 0.5 * Do + 0.5 * Da
        elif kd == "recency":
            y = prior + 0.3 * Do + 0.6 * Da
        elif kd == "no_manipulation":
            y = prior + (0.5 * Da if q != "self" else 0.0)
        elif kd in ("leak", "leak_plus_alex"):
            a_pull = (u_f3(Da) * Da * (1 + self.afac[k])) if kd == "leak_plus_alex" else (self.alpha + self.afac[k]) * Da
            if q == "self":
                y = prior + own_shift
            elif q in ("sam_p", "sam_i"):
                y = prior + self.lam * (u_f3(Do) * Do * self.fac[k]) + a_pull
            else:   # informed Sam saw the model's answer
                y = prior + 0.9 * u_f3(Do) * Do * self.fac[k] + a_pull
        else:
            raise ValueError(kd)
        return int(np.clip(round(y + self.rng.normal(0, self.noise)), 0, 100))

    def __call__(self, msgs):
        return {"probability": self.value(msgs)}, 4.8e-5, "req_stub"


def synth_cache(resp):
    cache = {}
    for j in P.jobs(items, anchors, seed32_order=DRY_SEED):
        key, vid, o, cond, d, own, alex, q, r = j
        msgs = P.messages(by_id[vid], o, own, alex, q)
        cache[key] = {"value": resp.value(msgs), "cost": 4.8e-5, "sha256": P.content_hash(msgs)}
        cache[key]["raw"] = cache[key]["value"]
    return cache


def evaluate(resp, nboot=P.B, loo=True):
    cache = synth_cache(resp)
    M = P.cell_means(items, anchors, cache)
    vids, keys, S, N, complete = P.uptake_table(items, anchors, M)
    if loo:
        return P.analyse_tables(vids, keys, S, N, complete, DRY_SEED)
    idx = np.flatnonzero(complete)
    point, ci = P.boot(S, N, keys, DRY_SEED, idx, n=nboot)
    lab, why = P.rule(point, ci, len(idx))
    return {"label": lab, "reason": why, "point": point, "ci": ci, "map_rule": P.map_rule(point, ci)}


def fmt(x, c=None):
    return f"{x:+.3f}" + (f" [{c[0]:+.3f}, {c[1]:+.3f}]" if c else "")


def section1():
    print("## 1. The prompts the run sends (vignette co01, statement X, m = 85, d = -30 so V = 55)\n")
    it = by_id["co01"]
    m = round(anchors["co01"]["m_X"])
    for cond, own, alex in (("OWN", m - 30, m), ("SWAP", m, m - 30), ("REF", m, m)):
        for q in P.QUESTIONS:
            msgs = P.messages(it, "X", own, alex, q)
            print(f"### {cond} / {q}")
            for mm in msgs:
                print(f"[{mm['role']}] {mm['content']}")
            print()
    # every knob moves the prompt
    a = P.messages(it, "X", m - 30, m, "sam_p")
    b = P.messages(it, "X", m, m - 30, "sam_p")
    c = P.messages(it, "X", m + 10, m, "sam_p")
    assert parse(a)[:2] == (m - 30, m) and parse(b)[:2] == (m, m - 30) and parse(c)[0] == m + 10
    assert len({P.messages(it, "X", 55, 85, q)[2]["content"] for q in P.QUESTIONS}) == 4
    assert P.messages(it, "Y", 55, 85, "self")[0]["content"] != a[0]["content"]
    print("Checks: OWN and SWAP hold the same two numbers in swapped slots; the own slot moves with d; the four questions "
          "give four different final turns; X and Y give different first turns. All assertions passed.\n")
    js = P.jobs(items, anchors)
    print(f"Planned calls: {len(js)}; distinct prompts: {len({j[0].rsplit('|', 1)[0] for j in js})} x {P.R} repeats; "
          f"estimated ${len(js) * P.EST_COST_PER_CALL:.3f}, cap ${P.CAP:.2f}.\n")


def section2():
    print("## 2. The rule against synthetic responders (P3: the dumb ones first)\n")
    print("U = mean over |d| in {10, 30, 60} of the pooled uptake (y - y_REF) / (V - m); dU = U_sam(OWN) - U_sam(SWAP); "
          "guard = U_inf(OWN) - U_sam(OWN), whose interval must be above 0.\n")
    print("| responder | U_self(OWN) | U_sam(OWN) [95% CI] | U_sam(SWAP) | dU [95% CI] | guard [95% CI] | map's rule | this rule |")
    print("|---|---|---|---|---|---|---|---|")
    rows = [("constant 50", Responder("constant")),
            ("re-derives from the vignette (no pull)", Responder("rederive")),
            ("copies the last number shown (Alex's)", Responder("last_number")),
            ("source-blind anchor (own slot and Alex weigh 0.5 each)", Responder("source_blind")),
            ("recency anchor (own 0.3, Alex 0.6)", Responder("recency")),
            ("own-slot copier (repeats its own answer whoever is asked)", Responder("own_slot_copier")),
            ("planted answer does not move its own re-rating", Responder("no_manipulation")),
            ("egocentric leakage, lambda 0.5, Alex 0", Responder("leak", lam=0.5)),
            ("egocentric leakage, lambda 0.25, Alex 0", Responder("leak", lam=0.25)),
            ("leakage lambda 0.5 plus Alex pulling Sam as much as own pulls self", Responder("leak_plus_alex", lam=0.5))]
    for name, r in rows:
        x = evaluate(r)
        p, c = x["point"], x["ci"]
        lab = x["label"] + (f" ({x['reason']})" if x["reason"] else "") + (f", fragile {x['loo_flips']}" if x["fragile"] else "")
        print(f"| {name} | {p['U_self_own']:+.3f} | {fmt(p['U_sam_own'], c['U_sam_own'])} | {p['U_sam_swap']:+.3f} | "
              f"{fmt(p['dU'], c['dU'])} | {fmt(p['copy_guard'], c['copy_guard'])} | {x['map_rule']} | {lab} |")
    print("\nThe map's rule alone (U_sam(OWN) >= 0.10, CI above 0) is passed by the source-blind and recency anchors and "
          "by the own-slot copier; the full rule rejects all three, and passes the leakage responders that have no "
          "source-blind pull.\n")


def section3(nsim=60, nboot=400):
    print(f"## 3. Power of the full rule ({nsim} synthetic runs per cell, {nboot} resamples each)\n")
    print("Sam's uptake in OWN is lambda x the model's own (F3 profile, vignette factor 1 + N(0, 0.5)); Alex's pull on Sam "
          "is alpha + N(0, 0.1) per item-statement wherever the displaced number is Alex's (SWAP). True U_sam(OWN) is "
          "about 0.45 x lambda; true dU is about 0.45 x lambda - alpha.\n")
    lams, alphas = (0.0, 0.15, 0.25, 0.35, 0.5, 0.75), (0.0, 0.1)
    print("| alpha \\ lambda | " + " | ".join(f"{l}" for l in lams) + " |")
    print("|---|" + "---|" * len(lams))
    for a in alphas:
        row = []
        for lam in lams:
            ps = 0
            for s in range(nsim):
                x = evaluate(Responder("leak", lam=lam, alpha=a, seed=DRY_SEED + 100 + s), nboot=nboot, loo=False)
                ps += x["label"] == "pass"
            row.append(f"{ps / nsim:.2f}")
        print(f"| {a} | " + " | ".join(row) + " |")
    print()


def section4():
    print("## 4. Machinery (stubbed calls; a temporary results folder)\n")
    real = om.RESULTS
    with tempfile.TemporaryDirectory() as td:
        om.RESULTS = Path(td)
        cache = Path(td) / "p2-5-calls.json"
        js = P.jobs(items, anchors, seed32_order=DRY_SEED)[:200]
        n = {"calls": 0}

        def refusing(msgs):
            n["calls"] += 1
            if n["calls"] == 10:
                raise om.llm.RefusalError("p2-5", SimpleNamespace(stop_details={"category": "stub"}, model=om.MODEL,
                                                                  _request_id="req_stub_refusal"))
            return {"probability": 50}, 4.8e-5, "req_stub"
        c = P.GuardedCaller(cache, P.CAP, "dry refusal", call=refusing)
        try:
            c.run(js, by_id, workers=1)
        except SystemExit as e:
            print(f"- refusal stub: stopped ({e}); calls made {n['calls']}; refusal.md written: "
                  f"{(Path(td) / 'refusal.md').exists()}; refused entry in cache: "
                  f"{any(v.get('refused') for v in json.loads(cache.read_text()).values())}")
        n["calls"] = 0
        try:
            P.GuardedCaller(cache, P.CAP, "dry rerun", call=refusing).run(js, by_id, workers=1)
        except SystemExit as e:
            print(f"- re-run after the refusal: exits before any call ({e}); calls made {n['calls']}")
        cache.unlink()
        (Path(td) / "refusal.md").unlink()
        try:
            P.GuardedCaller(cache, 4.8e-5 * 20, "dry cap", call=lambda m: ({"probability": 50}, 4.8e-5, "req")).run(js, by_id, workers=1)
        except SystemExit as e:
            print(f"- cap stub (cap = 20 calls' cost): {e}; calls cached {len(json.loads(cache.read_text()))}")
        d = json.loads(cache.read_text())
        k0 = next(iter(d))
        d[k0]["sha256"] = "0" * 64
        cache.write_text(json.dumps(d))
        try:
            P.GuardedCaller(cache, P.CAP, "dry tamper", call=lambda m: ({"probability": 50}, 4.8e-5, "req")).run(js, by_id, workers=1)
            print("- tampered entry: NOT caught")
        except AssertionError as e:
            print(f"- tampered entry caught: {e}")
        print(f"- gate with no design review file: {P.gate(Path(td) / 'none.md')}")
        rv = Path(td) / "rv.md"
        rv.write_text("---\nverdict: fix-first\nconfirmed_at: null\n---\n")
        print(f"- gate with an unconfirmed fix-first: {P.gate(rv)}")
        rv.write_text("---\nverdict: go\nconfirmed_at: null\n---\n")
        print(f"- gate with go (seed file present: {P.SEEDF.exists()}): {P.gate(rv)}")
    om.RESULTS = real
    print()


if __name__ == "__main__":
    print("# P2-5 dry run (every call stubbed; synthetic data only)\n")
    section1()
    section2()
    section3()
    section4()
