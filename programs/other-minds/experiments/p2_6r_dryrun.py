"""Dry run for om-p2-6r with every call stubbed (no API key needed, no paid call). Output:
experiments/p2-6r-dryrun-output.txt. Synthetic data only; Haiku's archived P2-6 run (results/p2-6-calls.json and
p2-6-position-or-label.json, already analysed and audited) supplies the baselines, item uptakes and call noise the
simulated worlds are built from.

    python experiments/p2_6r_dryrun.py > experiments/p2-6r-dryrun-output.txt"""

import json
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p2_6r_replication as R  # noqa: E402
import p2_6_position_label as base  # noqa: E402

its, anc = base.items(), base.anchors()
hcache = json.loads((R.RESULTS / "p2-6-calls.json").read_text())
hres = json.loads((R.RESULTS / "p2-6-position-or-label.json").read_text())
HU = {q: {c: hres["item_uptakes"][q][c] for c in R.CELLS} for q in hres["items"]}
B0 = {(it["id"], o): np.mean([hcache[f"base|{it['id']}|{o}|0|{r}"]["value"] for r in range(20)])
      for it in its for o in "XY"}


def haiku_call_sd():
    sds = []
    for it in its:
        for o in "XY":
            for d in R.DISTANCES:
                for c in R.CELLS:
                    sds.append(np.std([hcache[f"{c}|{it['id']}|{o}|{d}|{r}"]["value"] for r in range(20)]))
    return float(np.mean(sds)), float(np.median(sds))


def world(name):
    """Per-item true uptakes per cell, and an assistant-turn hedge toward 50 that ignores the shown value."""
    U = {q: dict(u) for q, u in HU.items()}
    hedge = 0.0
    if name == "haiku":
        pass
    elif name.startswith("scaled"):
        k = float(name.split(":")[1])
        U = {q: {c: k * v for c, v in u.items()} for q, u in U.items()}
    elif name == "no-position":
        U = {q: {"AY": (u["AY"] + u["UY"]) / 2, "UY": (u["AY"] + u["UY"]) / 2,
                 "AS": (u["AS"] + u["US"]) / 2, "US": (u["AS"] + u["US"]) / 2} for q, u in U.items()}
    elif name == "label-only:0.25":
        U = {q: {"AY": 0.35, "UY": 0.35, "AS": 0.10, "US": 0.10} for q in U}
    elif name == "null":
        U = {q: {c: 0.0 for c in R.CELLS} for q in U}
    elif name == "copy:0.3":
        U = {q: {c: 0.3 for c in R.CELLS} for q in U}
    elif name == "hedge-A:0.5":
        U = {q: {c: 0.0 for c in R.CELLS} for q in U}
        hedge = 0.5
    return U, hedge


def simulate(mk, wname, sd, rng):
    U, hedge = world(wname)
    cache = {}
    for it in its:
        q = it["id"]
        for o in "XY":
            b0 = B0[(q, o)]
            for r in range(R.REPEATS[mk]):
                cache[f"{mk}|base|{q}|{o}|0|{r}"] = {"value": int(np.clip(round(b0 + rng.normal(0, sd)), 0, 100)), "cost": 0}
                for d in R.DISTANCES:
                    A = base.shown_value(anc[q][f"m_{o}"], d)
                    for c in R.CELLS:
                        y = b0 + U[q][c] * (A - b0) + (hedge * (50 - b0) if c[0] == "A" else 0) + rng.normal(0, sd)
                        cache[f"{mk}|{c}|{q}|{o}|{d}|{r}"] = {"value": int(np.clip(round(y), 0, 100)), "cost": 0}
    return cache


def reading_of(mk, cache, seed):
    nrep = R.complete_repeats(mk, its, cache)
    up, up_s, _, _ = R.item_uptakes(mk, its, anc, cache, nrep)
    if len(up) < R.MIN_ITEMS or len(up_s) < R.MIN_ITEMS:
        return "untestable"
    U = np.array([[up[q][c] for c in R.CELLS] for q in up])
    Us = np.array([[up_s[q][c] for c in R.CELLS] for q in up_s])
    return R.model_reading(R.summarise(U, seed), R.summarise(Us, seed))


def rates(wn_sonnet, wn_opus, sd, n=150, seed=7):
    rng = np.random.default_rng(seed)
    out = {"pass": 0, "fail": 0, "untestable": 0}
    per = {"sonnet": {}, "opus": {}}
    for i in range(n):
        rd = {}
        for mk, wn in (("sonnet", wn_sonnet), ("opus", wn_opus)):
            rd[mk] = reading_of(mk, simulate(mk, wn, sd, rng), 1000 + i)
            per[mk][rd[mk]] = per[mk].get(rd[mk], 0) + 1
        v = "untestable" if "untestable" in rd.values() else R.overall(rd)
        out[v] += 1
    return {k: v / n for k, v in out.items()}, per


print("# om-p2-6r dry run (every call stubbed; synthetic data only)\n")

print("## 1. Settings the run will use (D2/D10: printed, compared with the pre-registration)")
for mk in R.ORDER:
    print(f"- {mk}: model {R.MODELS[mk]}, settings {json.dumps(R.SETTINGS[mk])}, max_tokens {R.MAX_TOKENS[mk]}, "
          f"repeats {R.REPEATS[mk]}")
print(f"- cap ${R.CAP:.2f} (both models), margin {R.MARGIN}, min items {R.MIN_ITEMS}, bootstrap B {R.B}")
J = R.jobs(its, anc, 12345)
print(f"- jobs: {len(J)} total; sonnet {sum(j[1] == 'sonnet' for j in J)}, opus {sum(j[1] == 'opus' for j in J)}; "
      f"first opus job at index {next(i for i, j in enumerate(J) if j[1] == 'opus')} (Sonnet first)")
print(f"- distinct job keys: {len(set(j[0] for j in J))}")
est = {"sonnet": 0.00085, "opus": 0.0044}
tot = sum(est[j[1]] for j in J)
print(f"- cost estimate at program 1's archived full-price per call (mm-gm3b, batch cost x 2): sonnet $0.00085, opus "
      f"$0.0044 -> ${tot:.2f} (cap ${R.CAP:.2f}, ratio {R.CAP / tot:.2f})")

print("\n## 2. The cells differ only as stated (P4)")
it = its[0]
A = base.shown_value(anc[it['id']]['m_X'], 30)
for c in ("base",) + R.CELLS:
    m = base.messages(c, it, "X", None if c == "base" else A)
    print(f"- {c}: {len(m)} message(s); roles {[x['role'] for x in m]}; last 70 chars: {m[-1]['content'][-70:]!r}")
ay, aS = base.messages("AY", it, "X", A), base.messages("AS", it, "X", A)
uy, us = base.messages("UY", it, "X", A), base.messages("US", it, "X", A)
print(f"- AY vs AS differ only in the owner word: {ay[2]['content'].replace('your', 'Sam' + chr(39) + 's') == aS[2]['content']}")
print(f"- UY vs US differ only in the owner word: {uy[0]['content'].replace('your earlier', 'Sam' + chr(39) + 's earlier') == us[0]['content']}")
print(f"- the same content hash for both models? {R.content_hash('sonnet', ay) == R.content_hash('opus', ay)} (must be False)")

print("\n## 3. Gate (no call before a go and the seed file)")
print(f"- gate now: {R.gate()}")
with tempfile.TemporaryDirectory() as t:
    t = Path(t)
    (t / "seed.json").write_text("{}")
    (t / "om-p2-6r.md").write_text("---\nverdict: fix-first\nconfirmed_at: null\n---\n")
    print(f"- fix-first, unconfirmed: {R.gate(t, t / 'seed.json')}")
    (t / "om-p2-6r.md").write_text("---\nverdict: fix-first\nconfirmed_at: 2026-11-05 05:00\n---\n")
    print(f"- fix-first, confirmed: {R.gate(t, t / 'seed.json')}")
    (t / "om-p2-6r-1b.md").write_text("---\nverdict: redesign\nconfirmed_at: null\n---\n")
    print(f"- a second review saying redesign: {R.gate(t, t / 'seed.json')}")
    (t / "om-p2-6r-1b.md").write_text("---\nverdict: go\nconfirmed_at: null\n---\n")
    print(f"- both go / confirmed: {R.gate(t, t / 'seed.json')}")

print("\n## 4. Stop rules with a stub (refusal, cap, tampering)")


class FakeRefusal(Exception):
    request_id = "req_stub"
    call = "stub"
    stop_details = "stub"


def stub(refuse_at=None, cost=0.01):
    n = {"i": 0}

    def call(mk, msgs):
        n["i"] += 1
        if refuse_at and n["i"] == refuse_at:
            raise FakeRefusal()
        return {"probability": 50}, cost, f"req_{n['i']}"
    call.refusal_error = FakeRefusal
    return call, n


old = R.RESULTS
with tempfile.TemporaryDirectory() as t:
    R.RESULTS = Path(t)
    fn, n = stub(refuse_at=20)
    c = R.GuardedCaller(Path(t) / "c.json", 99, "stub", fn)
    st = c.run(J[:200])
    cache = json.loads((Path(t) / "c.json").read_text())
    print(f"- refusal at call 20: status {st}; calls entered {n['i']}; refused entries {sum(bool(v.get('refused')) for v in cache.values())}; "
          f"refusal.md written {(Path(t) / 'refusal.md').exists()}")
    try:
        R.GuardedCaller(Path(t) / "c.json", 99, "stub", stub()[0])
        print("- re-run on that cache: STARTED (wrong)")
    except SystemExit as e:
        print(f"- re-run on that cache: exits ({e})")
with tempfile.TemporaryDirectory() as t:
    R.RESULTS = Path(t)
    fn, n = stub(cost=0.01)
    c = R.GuardedCaller(Path(t) / "c.json", 0.50, "stub", fn)
    st = c.run(J[:200])
    print(f"- cap $0.50 at $0.01 a call: status {st}; calls made {n['i']}; spent ${c.spent():.2f} (at most cap + 8 in flight)")
R.RESULTS = old
fake = {}
for j in J[:3]:
    fake[j[0]] = {"value": 50, "cost": 0, "sha256": R.content_hash(j[1], R.job_messages(j))}
k0 = J[0][0]
fake[k0]["sha256"] = "0" * 64
try:
    R.verify_cache(its, anc, fake)
    print("- tampered entry: NOT caught (wrong)")
except AssertionError as e:
    print(f"- tampered entry: caught ({str(e)[:60]})")

print("\n## 5. Haiku's archived call noise (input to the worlds below)")
mean_sd, med_sd = haiku_call_sd()
print(f"- within-cell SD of Haiku's 20 repeats: mean {mean_sd:.2f}, median {med_sd:.2f} points")
print("- Haiku item uptakes (om-p2-6): P " + R.fmt(hres["stats"]["P"]) + ", L " + R.fmt(hres["stats"]["L"]))

print("\n## 6. D1: the rule returns exactly one reading per table, with its sentence")
tables = {"holds": (0.25, 0.15, 0.35, 0.08, 0.02, 0.14, 0.25, 0.15, 0.35),
          "fail-shift": (0.25, 0.15, 0.35, 0.05, -0.02, 0.12, 0.08, -0.03, 0.18),
          "fail-label": (0.05, -0.02, 0.12, 0.20, 0.10, 0.30, 0.05, -0.02, 0.12),
          "fail-reversed": (-0.20, -0.30, -0.10, 0.02, -0.03, 0.07, -0.20, -0.30, -0.10),
          "fail-small (P below 0.15)": (0.10, 0.02, 0.18, 0.02, -0.03, 0.07, 0.10, 0.02, 0.18),
          "fail-small (P not above |L|, L not detected)": (0.16, 0.06, 0.26, 0.17, -0.01, 0.35, 0.16, 0.06, 0.26),
          "holds (P above a detected L)": (0.30, 0.20, 0.40, 0.16, 0.06, 0.26, 0.30, 0.20, 0.40)}
for name, (P, Pl, Ph, L, Ll, Lh, Ps, Psl, Psh) in tables.items():
    s, ss = {"P": [P, Pl, Ph], "L": [L, Ll, Lh]}, {"P": [Ps, Psl, Psh], "L": [L, Ll, Lh]}
    v = R.model_reading(s, ss)
    print(f"- {name}: reading {v}: {R.model_sentence('opus', v, s, ss)}")
print(f"- overall, both hold: {R.overall({'sonnet': 'holds', 'opus': 'holds'})}; one fails: {R.overall({'sonnet': 'holds', 'opus': 'fail-small'})}")

print("\n## 7. D11 / D5: P(pass) and P(fail) under named worlds (150 simulated runs each, B = 2,000)")
print("Worlds: 'haiku' = Haiku's own 16 item uptakes; 'scaled:k' = all four uptakes times k (DM4's planted next-rating "
      "pull was 2.5/5.4 = 0.46 of Haiku's on Sonnet and 0.8/5.4 = 0.15 on Opus); 'no-position' = each label's assistant "
      "and user uptakes averaged; 'label-only:0.25' = yours 0.35, Sam's 0.10 in both turns; 'null'; 'copy:0.3' = the "
      "same uptake in every cell (dumb copier); 'hedge-A:0.5' = no uptake, but assistant-turn re-ratings hedge halfway "
      "to 50 whatever the shown value.")
combos = [("haiku", "haiku"), ("scaled:0.75", "scaled:0.75"), ("scaled:0.46", "scaled:0.46"),
          ("scaled:0.46", "scaled:0.15"), ("haiku", "scaled:0.15"), ("no-position", "no-position"),
          ("label-only:0.25", "label-only:0.25"), ("null", "null"), ("copy:0.3", "copy:0.3"),
          ("hedge-A:0.5", "hedge-A:0.5")]
for sd in (3.0, 8.0):
    print(f"\nCall noise SD {sd} points:")
    print("| Sonnet world | Opus world | P(pass) | P(fail) | P(untestable) | Sonnet readings | Opus readings |")
    print("|---|---|---|---|---|---|---|")
    for ws, wo in combos:
        r, per = rates(ws, wo, sd)
        print(f"| {ws} | {wo} | {r['pass']:.2f} | {r['fail']:.2f} | {r['untestable']:.2f} | {per['sonnet']} | {per['opus']} |")
