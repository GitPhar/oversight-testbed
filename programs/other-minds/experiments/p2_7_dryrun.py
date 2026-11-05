"""Dry run for om-p2-7 with every call stubbed (no API key needed, no paid call). Output:
experiments/p2-7-dryrun-output.txt. Synthetic Sam data only, built from each model's archived self data (program 1's
gm3b and mm-gm3b, already analysed and audited there). The beacon seed is not used here (a fixed stand-in seed draws
the statements); the run draws them from the beacon.

    python experiments/p2_7_dryrun.py > experiments/p2-7-dryrun-output.txt"""

import json
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p2_7_format_fingerprint as T  # noqa: E402

sys.path.insert(0, str(T.P1X))
sys.path.insert(0, str(T.P1 / "src"))
recs = T.records()
STAND_IN = 424242
stmts = T.draw_statements(STAND_IN)

print("# om-p2-7 dry run (every call stubbed; synthetic Sam data only)\n")
print("## 1. Settings, statements, calls, cost (D2/D10)")
for mk in T.ORDER:
    print(f"- {mk}: {T.MODELS[mk]}, {json.dumps(T.SETTINGS[mk])}, max_tokens {T.MAX_TOKENS[mk]}, repeats {T.REPEATS}")
print(f"- shared items: {len(T.shared_items())} ({', '.join(T.shared_items())})")
print(f"- statements drawn with a stand-in seed: {len(stmts)} ({T.PER_ITEM} per item)")
J = T.jobs(stmts, 7)
print(f"- jobs: {len(J)}; per model " + ", ".join(f"{mk} {sum(j[1] == mk for j in J)}" for mk in T.ORDER)
      + f"; distinct keys {len(set(j[0] for j in J))}")
est = {"haiku": 0.000043, "sonnet": 0.00086, "opus": 0.0044}
tot = sum(est[j[1]] for j in J)
print(f"- cost estimate at program 1's archived full-price per graded-format call (Haiku $0.000043, Sonnet $0.00086, "
      f"Opus $0.0044): ${tot:.2f}; the Sam prompts are one sentence longer, so about ${tot * 1.1:.2f} "
      f"(cap ${T.CAP:.2f}, ratio {T.CAP / (tot * 1.1):.2f})")

print("\n## 2. The self prompts reproduce program 1's archived prompts exactly; Sam differs only by the framing (P4, P8)")
try:
    import gm3b_format_invariance as g
    ok = all(T.self_prompt(recs[q], k, f) == g.prompt(recs[q], k, f, 0)[0] for q, k in stmts for f in T.FORMATS)
    print(f"- self_prompt == gm3b prompt for all {len(stmts) * 3} (statement, format) pairs: {ok}")
except Exception as e:      # pragma: no cover
    print(f"- could not import gm3b: {e!r}")
q, k = stmts[0]
for f in T.FORMATS:
    s, m = T.self_prompt(recs[q], k, f), T.sam_prompt(recs[q], k, f)[0]
    print(f"- {f}: Sam prompt adds {len(m) - len(s):+d} characters; the shared head is identical: {m.startswith(T.head(recs[q], k))}")
print(f"- the same content hash for two models? {T.content_hash('haiku', [{'role': 'user', 'content': 'x'}], {}) == T.content_hash('opus', [{'role': 'user', 'content': 'x'}], {})} (must be False)")

print("\n## 3. Gate")
print(f"- gate now: {T.gate()}")
with tempfile.TemporaryDirectory() as t:
    t = Path(t)
    (t / "seed.json").write_text("{}")
    (t / "om-p2-7.md").write_text("---\nverdict: fix-first\nconfirmed_at: null\n---\n")
    print(f"- fix-first, unconfirmed: {T.gate(t, t / 'seed.json')}")
    (t / "om-p2-7.md").write_text("---\nverdict: go\nconfirmed_at: null\n---\n")
    print(f"- go: {T.gate(t, t / 'seed.json')}")

print("\n## 4. Stop rules with a stub")


class FakeRefusal(Exception):
    request_id, call, stop_details = "req_stub", "stub", "stub"


def stub(refuse_at=None, cost=0.01):
    n = {"i": 0}

    def call(mk, msgs, schema):
        n["i"] += 1
        if refuse_at and n["i"] == refuse_at:
            raise FakeRefusal()
        return ({"answer": "likely"} if "answer" in schema["properties"] else {next(iter(schema["properties"])): 50}), cost, f"r{n['i']}"
    call.refusal_error = FakeRefusal
    return call, n


old = T.RESULTS
with tempfile.TemporaryDirectory() as t:
    T.RESULTS = Path(t)
    fn, n = stub(refuse_at=15)
    c = T.GuardedCaller(Path(t) / "c.json", 99, "stub", fn, recs)
    st = c.run(J)
    cache = json.loads((Path(t) / "c.json").read_text())
    print(f"- refusal at call 15: status {st}; calls entered {n['i']}; refused entries {sum(bool(v.get('refused')) for v in cache.values())}; "
          f"refusal.md {(Path(t) / 'refusal.md').exists()}; any Sonnet or Opus call {any(k.split('|')[0] != 'haiku' for k in cache)}")
    try:
        T.GuardedCaller(Path(t) / "c.json", 99, "stub", stub()[0], recs)
        print("- re-run: STARTED (wrong)")
    except SystemExit as e:
        print(f"- re-run on that cache: exits ({e})")
with tempfile.TemporaryDirectory() as t:
    T.RESULTS = Path(t)
    fn, n = stub(cost=0.01)
    c = T.GuardedCaller(Path(t) / "c.json", 0.40, "stub", fn, recs)
    print(f"- cap $0.40 at $0.01 a call: status {c.run(J)}; calls {n['i']}; spent ${c.spent():.2f}")
    fn, n = stub(cost=0.0)
    c2 = T.GuardedCaller(Path(t) / "d.json", 99, "stub", fn, recs)
    c2.run(J)
    full = json.loads((Path(t) / "d.json").read_text())
    k0 = next(iter(full))
    full[k0]["sha256"] = "0" * 64
    try:
        T.analyse_cache(full, recs, stmts, 1)
        print("- tampered entry: NOT caught (wrong)")
    except AssertionError as e:
        print(f"- tampered entry: caught ({str(e)[:50]})")
T.RESULTS = old

print("\n## 5. The archived self data the worlds are built from (34 stand-in statements)")
SELF, NOISE = {}, {}
for mk in T.ORDER:
    S, Sh = T.self_matrices(mk, stmts)
    arch = json.loads(T.SELF_ARCHIVE[mk].read_text())
    sds = []
    for (q_, k_) in stmts:
        for f in T.FORMATS:
            v = [T.encode(f, arch[f"{q_}|{k_}|{f}|{r}"]["value"]) for r in range(10)]
            sds.append(np.std(v))
    SELF[mk], NOISE[mk] = S, float(np.mean(sds))
    es = T.one_credence_residuals(S)[0]
    rel = T.sb(T.corr(T.one_credence_residuals(Sh[0])[0], T.one_credence_residuals(Sh[1])[0]))
    print(f"- {mk}: residual SD {es.std():.3f}; split-half reliability of self residuals {rel:.2f}; mean per-call SD {NOISE[mk]:.3f}")


def grid(f, x):
    x = np.clip(x, 0, 1)
    return np.round(x * 6) / 6 if f == "F6" else np.round(x * 100) / 100


def sam_world(mk, world, rng):
    S = SELF[mk]
    e, (a, b, c) = T.one_credence_residuals(S)
    fit = S - e
    if world == "shared":
        mu = S
    elif world == "shared-hedged":
        mu = 0.5 + 0.7 * (S - 0.5)
    elif world.startswith("mix:"):
        w = float(world.split(":")[1])
        mu = fit + w * e + (1 - w) * e[rng.permutation(len(e))]
    elif world == "independent":
        mu = fit + e[rng.permutation(len(e))]
    elif world == "generic":
        mu = T.generic_link(S)
    elif world == "no-deviation":
        mu = fit
    return mu


def simulate(mk, world, rng, noise_mult=1.0):
    mu = sam_world(mk, world, rng)
    reps = []
    for r in range(T.REPEATS):
        X = np.empty_like(mu)
        for j, f in enumerate(T.FORMATS):
            X[:, j] = grid(f, mu[:, j] + rng.normal(0, NOISE[mk] * noise_mult, mu.shape[0]))
        reps.append(X)
    return np.mean(reps, 0), reps


def reading(mk, world, rng, seed, noise_mult=1.0, boot=400):
    S, Sh = T.self_matrices(mk, stmts)
    M, Mh = simulate(mk, world, rng, noise_mult)
    st = T.model_stats(S, Sh, M, Mh)
    old_b = T.B
    T.B = boot
    ci = T.boot_model(S, Sh, M, Mh, [q for q, _ in stmts], seed)
    T.B = old_b
    return T.model_reading(st, ci), st


print("\n## 6. D1: one reading per table")
fake = {"rel_self": 0.8, "rel_sam": 0.7}
for name, rho, d, dl in (("holds", 0.7, 0.3, 0.1), ("fail-ceiling", 0.3, 0.2, 0.05), ("fail-generic (small)", 0.7, 0.05, -0.1),
                         ("fail-generic (CI)", 0.7, 0.2, -0.02)):
    st = dict(fake, rho=rho, delta=d)
    print(f"- {name}: {T.model_reading(st, {'delta': [dl, dl + 0.4]})}")
for name, st, dl in (("boundary: rel 0.5, rho 0.5, delta 0.10 exactly (computed as sums)", {"rel_self": 0.2 + 0.3, "rel_sam": 0.1 * 5, "rho": 0.1 + 0.4, "delta": 0.3 - 0.2}, 0.05),
                     ("just below: rho 0.4999", {"rel_self": 0.8, "rel_sam": 0.8, "rho": 0.4999, "delta": 0.3}, 0.1),
                     ("just below: delta 0.0999", {"rel_self": 0.8, "rel_sam": 0.8, "rho": 0.7, "delta": 0.0999}, 0.01),
                     ("just below: rel_sam 0.4999", {"rel_self": 0.8, "rel_sam": 0.4999, "rho": 0.7, "delta": 0.3}, 0.1)):
    print(f"- P13 {name}: {T.model_reading(st, {'delta': [dl, 1.0]})}   (0.3 - 0.2 = {0.3 - 0.2!r})")
print(f"- unreliable: {T.model_reading({'rel_self': 0.3, 'rel_sam': 0.9, 'rho': 0.9, 'delta': 0.5}, {'delta': [0.2, 0.8]})}")
print(f"- overall: all hold {T.overall({'haiku': 'holds', 'sonnet': 'holds', 'opus': 'holds'})}; one unreliable, two hold "
      f"{T.overall({'haiku': 'holds', 'sonnet': 'holds', 'opus': 'unreliable'})}; two unreliable "
      f"{T.overall({'haiku': 'holds', 'sonnet': 'unreliable', 'opus': 'unreliable'})}; one fails {T.overall({'haiku': 'holds', 'sonnet': 'fail-generic', 'opus': 'holds'})}")

print("\n## 7. D11 / D5: readings under named worlds (60 simulated runs a world and model, bootstrap B = 400 here)")
print("Worlds for Sam's true means: 'shared' = the model's own archived means; 'shared-hedged' = the same pulled 30% "
      "toward 0.5 (an affine hedge); 'mix:w' = the one-credence fit plus w of the model's own residuals and (1 − w) of "
      "its residuals shuffled across statements; 'independent' = mix:0; 'generic' = the dumb rival itself (a smooth "
      "link from the latent credence: shared format shape, no statement-specific deviation); 'no-deviation' = the "
      "one-credence fit alone. Call noise: the model's archived per-call SD, rounded to each format's grid.")
worlds = ["shared", "shared-hedged", "mix:0.7", "mix:0.5", "independent", "generic", "no-deviation"]
rng = np.random.default_rng(11)
table = {}
for mk in T.ORDER:
    for w in worlds:
        cnt = {}
        for i in range(60):
            v, _ = reading(mk, w, rng, 500 + i)
            cnt[v] = cnt.get(v, 0) + 1
        table[(mk, w)] = cnt
print("| world | " + " | ".join(T.ORDER) + " |")
print("|---|" + "---|" * len(T.ORDER))
for w in worlds:
    print(f"| {w} | " + " | ".join(str(table[(mk, w)]) for mk in T.ORDER) + " |")
print("\nOverall P(pass) if every model is in the same world (readings assumed independent across models):")
for w in worlds:
    ph = {mk: table[(mk, w)].get("holds", 0) / 60 for mk in T.ORDER}
    pu = {mk: table[(mk, w)].get("unreliable", 0) / 60 for mk in T.ORDER}
    # exact over the 3^3 reading patterns: holds / unreliable / other
    import itertools
    pp = pt = 0.0
    for pat in itertools.product(("h", "u", "o"), repeat=3):
        pr = 1.0
        for mk, x in zip(T.ORDER, pat):
            pr *= ph[mk] if x == "h" else pu[mk] if x == "u" else 1 - ph[mk] - pu[mk]
        tested = [x for x in pat if x != "u"]
        if len(tested) < 2:
            pt += pr
        elif all(x == "h" for x in tested):
            pp += pr
    print(f"- {w}: P(pass) {pp:.2f}, P(untestable) {pt:.2f}, P(fail) {1 - pp - pt:.2f}")
