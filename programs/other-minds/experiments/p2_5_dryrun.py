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
# D12 (review om-p2-5 F2, review om-p2-5-1b F4): archive-calibrated spreads. Per-statement own uptake by distance class
# from bm0's archived rows (own, lag 0; averaged over the two signs; the class mean where a statement has none).
_BM0 = json.loads((om.P1 / "results" / "bm0-source-distance-lag.json").read_text())["rows"]
ARCH = {}
for _r in _BM0:
    if _r["src"] == "own" and _r["lag"] == 0:
        ARCH.setdefault((_r["item"], _r["o"], abs(_r["d"])), []).append(_r["u"])
ARCH = {k: float(np.mean(v)) for k, v in ARCH.items()}
ARCH_CLASS = {c: float(np.mean([v for k, v in ARCH.items() if k[2] == c])) for c in (10, 30, 60)}


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

    def __init__(self, kind, lam=0.5, alpha=0.0, het=0.5, seed=DRY_SEED, noise=1.0, asd=0.1, archive=False, cell=None):
        """cell = (sigma_sam, sigma_alex, ref_sd): D12 (review om-p2-5 F2) per-cell noise, fixed across repeats: Sam's
        uptake in a displaced cell is lambda x own + N(0, sigma_sam), Alex's pull alpha + N(0, sigma_alex), and each REF
        cell is offset N(0, ref_sd); `noise` is then the per-call SD."""
        self.kind, self.lam, self.alpha, self.het, self.noise, self.archive = kind, lam, alpha, het, noise, archive
        self.cell, self.cellrng, self.cellv = cell, np.random.default_rng(seed + 7), {}
        rng = np.random.default_rng(seed)
        self.off = {(it["id"], o): rng.normal(0, 3) for it in items for o in "XY"}
        self.fac = {(it["id"], o): max(0.0, 1 + rng.normal(0, het)) for it in items for o in "XY"}
        self.afac = {(it["id"], o): rng.normal(0, asd) for it in items for o in "XY"}
        self.rng = np.random.default_rng(seed + 1)
        self.m_of = {it["context"]: it for it in items}

    FIRST = {P.ask(it[o], it["context"]): ((it["id"], o), round(anchors[it["id"]][f"m_{o}"])) for it in items for o in "XY"}

    def key_m(self, stmt_q):
        return self.FIRST[stmt_q]

    def u_own(self, k, D):
        """The model's own uptake at displacement D: F3's profile x the statement factor, or (archive) bm0's archived
        per-statement uptake for the nominal class nearest |D|."""
        if not self.archive:
            return u_f3(D) * self.fac[k]
        c = min((10, 30, 60), key=lambda c: abs(abs(D) - c))
        return ARCH.get((k[0], k[1], c), ARCH_CLASS[c])

    def value(self, msgs):
        own, alex, q, sq = parse(msgs)
        k, m = self.key_m(sq)
        prior = m + self.off[k]
        Do, Da = own - m, alex - m
        own_shift = self.u_own(k, Do) * Do + 0.02 * Da
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
        elif kd == "turn_anchor":       # D12 (review 1b F1): label-blind, assistant turn weighs more; "has also seen" doubles it
            y = prior + (0.8 if q == "sam_inf" else 0.4) * Do + 0.1 * Da
        elif kd == "sam_over_self":     # D12 (review om-p2-5 F1): Sam pulled more than the model's own re-rating
            y = prior + {"self": 0.017, "sam_p": 0.145, "sam_i": 0.145, "sam_inf": 0.30}[q] * Do
        elif kd == "fixed_nudge":       # D12 (review om-p2-5 F4): a fixed 4-point nudge toward the own slot (8 if Sam saw it)
            y = prior + (8 if q == "sam_inf" else 4) * np.sign(Do)
        elif kd == "no_manipulation":
            y = prior + (0.5 * Da if q != "self" else 0.0)
        elif kd == "leak" and self.cell:
            ss, sa, rsd = self.cell
            cv = lambda key, sd: self.cellv.setdefault(key, self.cellrng.normal(0, sd))
            if Do == 0 and Da == 0:
                y = prior + cv((k, q, "ref"), rsd)
            elif q == "self":
                y = prior + own_shift
            else:
                uo = self.u_own(k, Do)
                lam_q = max(0.9, self.lam) if q == "sam_inf" else self.lam
                y = prior + (lam_q * uo + cv((k, q, own, alex, "s"), ss)) * Do + (self.alpha + cv((k, q, own, alex, "a"), sa)) * Da
        elif kd in ("leak", "leak_plus_alex"):
            a_pull = (u_f3(Da) * Da * (1 + self.afac[k])) if kd == "leak_plus_alex" else (self.alpha + self.afac[k]) * Da
            uo = self.u_own(k, Do) * Do
            if q == "self":
                y = prior + own_shift
            elif q in ("sam_p", "sam_i"):
                y = prior + self.lam * uo + a_pull
            else:   # informed Sam saw the model's answer
                y = prior + max(0.9, self.lam) * uo + a_pull
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
    return {"label": lab, "reason": why, "point": point, "ci": ci, "map_rule": P.map_rule(point, ci),
            "fail_bound": P.fail_bound(lab, why, point, ci)[0]}


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
    keys0 = [j for j in js if j[-1] == 0]
    hashes0 = {P.content_hash(P.messages(by_id[j[1]], j[2], j[5], j[6], j[7])) for j in keys0}
    dups = P.duplicate_cells(items, anchors)
    assert len(keys0) == 1472 and len(hashes0) == 1328 and len(dups) == 18, (len(keys0), len(hashes0), len(dups))
    print(f"Distance (D12, review 1b F2): {len(keys0)} job keys per repeat but {len(hashes0)} distinct prompts; "
          f"{len(dups)} displaced cells repeat a smaller-|d| cell's prompt because V is clipped at 2 or 98 "
          f"({len(dups) * 8} prompts per repeat). Asserted. The cells (vignette, statement, d, m, V, same prompt as d):")
    for x in dups:
        print(f"  {x}")
    print()
    print(f"Planned calls: {len(js)}; job keys per repeat: {len({j[0].rsplit('|', 1)[0] for j in js})} x {P.R} repeats "
          f"({len(hashes0)} distinct prompts each); "
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
            ("label-blind turn anchor (assistant turn 0.4, Alex 0.1; 0.8 if Sam saw it)", Responder("turn_anchor")),
            ("Sam pulled more than its own re-rating (own 0.017, Sam 0.145)", Responder("sam_over_self")),
            ("fixed 4-point nudge toward its own answer (8 if Sam saw it)", Responder("fixed_nudge")),
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
    print("\nThe map's event as measured on this design (U_sam(OWN) >= 0.10, CI above 0) is passed by the source-blind and "
          "recency anchors, the own-slot copier, the turn anchor, the Sam-over-self responder and the fixed nudge. The "
          "full rule rejects the anchors (anchoring), the copier (copy) and the Sam-over-self responder (not inherited, "
          "D12a: its Sam-minus-own interval is above 0). It does NOT reject the label-blind turn anchor or the fixed "
          "4-point nudge, whose Sam uptake equals their own: a pass is about the bundle (whose number, turn, format, "
          "place) and 'points per point' is an average over the three distance classes.\n")


def section3(nsim=50, nboot=400):
    print(f"## 3. Power of the full rule ({nsim} synthetic runs per cell, {nboot} resamples each)\n")
    print("Sam's uptake in OWN is lambda x the model's own; Alex's pull on Sam is alpha wherever the displaced number is "
          "Alex's (SWAP). True U_sam(OWN) is about lambda x the mean own uptake; true dU is that minus alpha. Noise models:\n"
          "- synthetic: own uptake on F3's profile x 1 + N(0, 0.5) per statement; Alex N(0, 0.1) per statement; call SD 1;\n"
          "- D12 (review om-p2-5 F2), own uptake per statement and class from bm0's archived lag-0 cells, with per-cell "
          "noise (sigma Sam, sigma Alex, REF SD, call SD): 'moderate' (0.3, 0.3, 2, 3) and 'bm0-like' (0.43, 0.6, 3, 5).\n\n"
          "Columns after P(pass) are the shares of each sub-reading (fail_bound; D12, review om-p2-5-1b F4).\n")
    subs = ("pass", "small_bounded", "small_open", "anchoring_reversed", "anchoring_bounded", "anchoring_open", "copy",
            "not_inherited", None)
    print("| noise | alpha | lambda | P(pass) | " + " | ".join(str(x) for x in subs[1:]) + " |")
    print("|---|---|---|---|" + "---|" * (len(subs) - 1))
    models = {"synthetic": {}, "moderate": dict(archive=True, cell=(0.3, 0.3, 2), noise=3),
              "bm0-like": dict(archive=True, cell=(0.43, 0.6, 3), noise=5)}
    for model, kw in models.items():
        for a in (0.0, 0.1):
            for lam in (0.0, 0.25, 0.35, 0.5, 0.75):
                counts = {x: 0 for x in subs}
                for sd_ in range(nsim):
                    x = evaluate(Responder("leak", lam=lam, alpha=a, seed=DRY_SEED + 100 + sd_, **kw), nboot=nboot, loo=False)
                    counts[x["fail_bound"]] += 1
                print(f"| {model} | {a} | {lam} | " + " | ".join(f"{counts[x] / nsim:.2f}" for x in subs) + " |", flush=True)
    print(f"\nArchive own uptake by class (bm0 means): { {k: round(v, 3) for k, v in ARCH_CLASS.items()} }; under the "
          f"archive models the true U_sam(OWN) is about lambda x {np.mean(list(ARCH_CLASS.values())):.3f}.\n")


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
        cache.unlink()
        try:
            P.GuardedCaller(cache, P.CAP, "dry malformed", call=lambda m: ({"probability": "x"}, 4.8e-5, "req")).run(js[:5], by_id, workers=1)
        except SystemExit as e:
            print(f"- malformed value (D12, F5a): stops cleanly ({e}); stop record written: "
                  f"{(Path(td) / 'p2-5-calls-stop.json').exists()}")
        # D12 (review 1b F3): a stop after whole repeats leaves a testable run
        full = synth_cache(Responder("leak", lam=0.5))
        alljobs = P.jobs(items, anchors, seed32_order=DRY_SEED)
        for frac in (0.9, 0.1):
            keep = {j[0] for j in alljobs[:int(len(alljobs) * frac)]}
            part = {k_: v for k_, v in full.items() if k_ in keep}
            k = P.complete_repeats(items, anchors, part)
            M = P.cell_means(items, anchors, part, k)
            vids, keys, S, N, complete = P.uptake_table(items, anchors, M)
            idx = np.flatnonzero(complete)
            point, ci = P.boot(S, N, keys, DRY_SEED, idx, n=200) if len(idx) else (None, None)
            lab = P.rule(point, ci, len(idx)) if len(idx) >= P.MIN_VIGNETTES else ("untestable", "few")
            print(f"- stop after {frac:.0%} of the calls: k = {k} complete repeats, {len(idx)} complete vignettes, label {lab}")
        # D12 (review 1b F5): the gate reads every om-p2-5*.md
        print(f"- gate with no design review file: {P.gate(Path(td))}")
        (Path(td) / "om-p2-5.md").write_text("---\nverdict: go\nconfirmed_at: null\n---\n")
        (Path(td) / "om-p2-5-1b.md").write_text("---\nverdict: fix-first\nconfirmed_at: null\n---\n")
        print(f"- gate with om-p2-5.md go and om-p2-5-1b.md unconfirmed fix-first: {P.gate(Path(td))}")
        (Path(td) / "om-p2-5-1b.md").write_text("---\nverdict: redesign\nconfirmed_at: null\n---\n")
        print(f"- gate with om-p2-5-1b.md redesign: {P.gate(Path(td))}")
        (Path(td) / "om-p2-5-1b.md").write_text("---\nverdict: fix-first\nconfirmed_at: 2026-11-04 20:40\n---\n")
        print(f"- gate with go and a confirmed fix-first (seed file present: {P.SEEDF.exists()}): {P.gate(Path(td))}")
    om.RESULTS = real
    print()


if __name__ == "__main__":
    print("# P2-5 dry run (every call stubbed; synthetic data only)\n")
    section1()
    section2()
    section3()
    section4()
