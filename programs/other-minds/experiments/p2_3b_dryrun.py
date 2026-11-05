"""Dry run of P2-3b with every API call stubbed (no network, no cost). Written with the pre-registration (D8), so the
design reviewer can re-run it. Checks the machinery (counts, run order, cap, stop-on-refusal and what a stop leaves),
the conditions' text, the dumb baselines the pass rule must reject, and the power of the rule on synthetic data.
D9 adds: the letter-avoider baselines (F1), a re-run after a refusal makes no call (F3a), calls finishing after a stop
are counted (F3d), the pilot and test gates (F3b), a tampered cache entry is caught (F4), an exact 0.10 passes (F2).

    /Users/seanpharris/entangled-mind/.venv/bin/python experiments/p2_3b_dryrun.py [--quick]

Synthetic data only. Nothing here is test data; output goes to a temporary directory and to stdout."""

import json
import sys
import tempfile
import time
from pathlib import Path
from types import SimpleNamespace

import numpy as np

import om_common as om
import p2_3_simpletom as base
import p2_3b_simpletom_lowsev as t

QUICK = "--quick" in sys.argv
TMP = Path(tempfile.mkdtemp(prefix="p2-3b-dryrun-"))
om.RESULTS = TMP                                         # Caller writes refusal.md here, not in results/


def no_network(*a, **k):
    raise RuntimeError("dry run: network call attempted")


om.llm.client = no_network


def letter(it, q, wrong):
    return t.aware_letter(it, q) if wrong else it[q]["correct"]


# --- 1. population --------------------------------------------------------------------------------------------
items = json.loads(t.ITEMS.read_text())
test, pilot = t.split(items)
print("1. population:", json.dumps({"stories": len(items), "severity<=2": len(test) + len(pilot), "pilot": len(pilot),
                                    "test": len(test), "test cores": len({i["core_id"] for i in test}),
                                    "test letter-match": sum(i["wrong_ms"] == t.aware_letter(i) for i in test)}))
assert all(i["severity"] <= 2 for i in test + pilot) and not set(map(id, test)) & set(map(id, pilot))

# --- 2. conditions' text (D2, D7) -----------------------------------------------------------------------------
it = next(i for i in test if i["id"] == "potato_chip_food_sev1")
m5, _ = base.messages(it, "c5_planted_own", "action", "B")
m6, _ = base.messages(it, "c6_planted_other", "action", "B")
m4, _ = base.messages(it, "c4_remind_own", "action", "B")
print("\n2. c5 vs c6 on", it["id"])
for k, (a, b) in enumerate(zip(m5, m6)):
    print(f"   turn {k} ({a['role']}): {'same' if a == b else 'DIFFERS'}")
    if a != b:
        print("     c5:", json.dumps(a["content"])[:200])
        print("     c6:", json.dumps(b["content"])[:200])
assert m4[1]["content"] == json.dumps({"answer": "B"}), "c4 must show the model's own answer"
assert m5[1]["content"] == json.dumps({"answer": it["wrong_ms"]})
assert "Another reader answered that question: (" + it["wrong_ms"] + ") Yes" in m6[2]["content"]

# --- 3. machinery: counts, order, cap, stop-on-refusal ------------------------------------------------------
seed_o, seed_b = 12345, 67890                             # dry-run seeds only; the test's come from the beacon
ordered = t.run_order(test, seed_o)
calls = []


def stub_factory(refuse_id=None, cost=4.5e-5):
    def stub(msgs, schema, call, max_tokens=100, **k):
        story = msgs[0]["content"].split("\n\n")[0]
        sid = STORY2ID[story]
        calls.append((sid, len(msgs)))
        if sid == refuse_id:
            raise om.llm.RefusalError(call, SimpleNamespace(stop_details="stub refusal", model="stub",
                                                             _request_id="req_stub"))
        return {"answer": "A"}, cost, "req_stub"
    return stub


STORY2ID = {i["story"]: i["id"] for i in items}
om.structured = stub_factory()
c = t.run_items(ordered, TMP / "full.json", t.CAP, "dry full")
want = len(ordered) * 13
print(f"\n3a. full stubbed run: {len(c.cache)} cached jobs (expected {want}); stub cost ${c.spent():.3f}; "
      f"the first 56 calls are the first 8 stories in run order (ms, then behaviour): "
      f"{sorted({x[0] for x in calls[:56]}) == sorted(i['id'] for i in ordered[:8])}")
assert len(c.cache) == want

calls.clear()
om.structured = stub_factory(cost=0.01)
try:
    t.run_items(ordered, TMP / "cap.json", 0.05, "dry cap")
except SystemExit as e:
    print(f"3b. cap at $0.05 with $0.01 calls: stopped ({e}); calls made {len(calls)} (cap + at most 8 in flight)")

for k in (150, 350):
    (TMP / "refusal.md").unlink(missing_ok=True)
    calls.clear()
    om.structured = stub_factory(refuse_id=ordered[k]["id"])
    path = TMP / f"refuse{k}.json"
    try:
        t.run_items(ordered, path, t.CAP, "dry refusal")
    except SystemExit as e:
        cache = json.loads(path.read_text())
        out = t.analyse(ordered, cache, seed_b, b=200, loo=False)
        print(f"3c. refusal stub at run position {k}: stopped ({str(e)[:40]}…); {len(cache)} calls cached; "
              f"complete stories {out['complete_primary']}; verdict {out['primary_verdict']} ({out['verdict_reason']}); "
              f"refusal.md written: {(TMP / 'refusal.md').exists()}; refused story cached: "
              f"{any(ordered[k]['id'] in key and not v.get('refused') for key, v in cache.items())}; "
              f"refused key recorded in cache: {sum(bool(v.get('refused')) for v in cache.values())}; "
              f"completed after the stop: {json.loads((TMP / f'refuse{k}-stop.json').read_text())['completed_after_stop']}")

# D9 F3(d): with call latency, calls already in flight finish after the stop and are counted
(TMP / "refusal.md").unlink(missing_ok=True)


def slow_stub(refuse_id):
    inner = stub_factory(refuse_id=refuse_id)

    def f(msgs, *a, **k):
        if STORY2ID[msgs[0]["content"].split("\n\n")[0]] != refuse_id:
            time.sleep(0.05)
        return inner(msgs, *a, **k)
    return f


calls.clear()
om.structured = slow_stub(ordered[19]["id"])
try:
    t.run_items(ordered, TMP / "slow.json", t.CAP, "dry slow refusal")
except SystemExit:
    rec = json.loads((TMP / "slow-stop.json").read_text())
    print(f"3c. refusal at run position 19 with 50 ms latency: completed after the stop {rec['completed_after_stop']} "
          f"(in-flight calls, kept and counted); stop record {rec['reason']}, resumable {rec['resumable']}")
(TMP / "refusal.md").unlink(missing_ok=True)
om.structured = stub_factory(refuse_id=ordered[350]["id"])
try:
    t.run_items(ordered, TMP / "refuse350.json", t.CAP, "dry refusal again")
except SystemExit:
    pass

# D9 F3(a): a second run after the refusal makes no call, with or without refusal.md
for drop_md in (False, True):
    if drop_md:
        (TMP / "refusal.md").unlink(missing_ok=True)
    calls.clear()
    om.structured = stub_factory()
    try:
        t.run_items(ordered, TMP / "refuse350.json", t.CAP, "dry rerun")
        print("3d. RE-RUN MADE CALLS: FLAW")
    except SystemExit as e:
        print(f"3d. re-run after the refusal ({'refusal.md removed, refused key still in cache' if drop_md else 'refusal.md present'}): "
              f"exited at start ({str(e)[:70]}…); calls made {len(calls)}")
    assert len(calls) == 0

# D9 F4: a cache entry whose prompt no longer matches is caught on the hit and at analysis
full = json.loads((TMP / "full.json").read_text())
assert all("sha256" in v for v in full.values())
t.verify_cache(ordered, full)
bad = dict(full)
k0 = f"action|c5_planted_own|{ordered[0]['id']}"
bad[k0] = dict(bad[k0], sha256="0" * 64)
(TMP / "bad.json").write_text(json.dumps(bad))
calls.clear()
om.structured = stub_factory()
try:
    t.run_items(ordered, TMP / "bad.json", t.CAP, "dry tampered")
    print("3e. TAMPERED ENTRY NOT CAUGHT: FLAW")
except AssertionError as e:
    print(f"3e. tampered cache entry caught on its cache hit: {e}; calls made {len(calls)}")
try:
    t.verify_cache(ordered, bad)
    print("3e. TAMPERED ENTRY NOT CAUGHT AT ANALYSIS: FLAW")
except AssertionError as e:
    print(f"3e. and at analysis: {e}")

# D9 F3(b): the gates
rv = TMP / "review.md"
pf = TMP / "pilot.json"
print("3f. gates:")
print(f"   the real review file now (fix-first, unconfirmed): pilot -> {t.gate('pilot')}; test -> {t.gate('test')}")
for head, pilot_rec in ((("go", "null"), None), (("fix-first", "2026-11-04 18:30"), None),
                        (("go", "null"), {"made": 182, "planned_calls": 182, "refusals": 0}),
                        (("go", "null"), {"made": 100, "planned_calls": 182, "refusals": 0}),
                        (("redesign", "null"), {"made": 182, "planned_calls": 182, "refusals": 0})):
    rv.write_text(f"---\nbet: om-p2-3b\nverdict: {head[0]}\nconfirmed_at: {head[1]}\n---\n")
    pf.unlink(missing_ok=True)
    if pilot_rec:
        pf.write_text(json.dumps(pilot_rec))
    print(f"   review {head[0]}, confirmed {head[1]}, pilot {pilot_rec and str(pilot_rec['made']) + '/' + str(pilot_rec['planned_calls'])}: "
          f"pilot gate -> {t.gate('pilot', rv, pf) or 'open'}; test gate -> {t.gate('test', rv, pf) or 'open'}")

# D9 F2: an exact 0.10 passes (34/300 - 4/300 evaluates to 0.0999...)
st = {"delta": 34 / 300 - 4 / 300, "delta_mismatch": 0.1, "delta_match": 0.1}
print(f"3g. exact 0.10 at n = 300: delta = {st['delta']!r} -> {t.rule(st, {'delta': 0.01}, 300, 0.2)}")
assert t.rule(st, {"delta": 0.01}, 300, 0.2)[0] == "pass"


# --- 4. synthetic answer models ----------------------------------------------------------------------------------
def synth(order, model, rng):
    """cache for `order` from a model: fn(it, q, cond, u) -> letter; u is the story's shared uniform."""
    cache = {}
    for it in order:
        u = rng.random()
        cache[f"ms|{it['id']}"] = {"value": it["aware"]["correct"], "cost": 0.0}
        for q in base.QS:
            for cond in base.CONDS:
                cache[f"{q}|{cond}|{it['id']}"] = {"value": model(it, q, cond, u, rng), "cost": 0.0}
    return cache


def uptake(rates, comonotone=True):
    """y = 1 with probability rates[cond]; comonotone uses the story's shared uniform (least variance)."""
    def f(it, q, cond, u, rng):
        p = rates[cond]
        return letter(it, q, (u if comonotone else rng.random()) < p)
    return f


BASE = {"c1_not_asked": 0.30, "c2_filler": 0.30, "c3_redacted": 0.15, "c4_remind_own": 0.05,
        "c5_planted_own": 0.20, "c6_planted_other": 0.20}


def with_delta(d, other=0.20):
    r = dict(BASE)
    r["c6_planted_other"], r["c5_planted_own"] = other, other + d
    return r


def copy_letter(any_visible):
    def f(it, q, cond, u, rng):
        if cond == "c5_planted_own" or (any_visible and cond == "c6_planted_other"):
            return it["wrong_ms"]
        if cond == "c4_remind_own":
            return it["aware"]["correct"]
        return letter(it, q, u < BASE[cond])
    return f


def avoid_letter(rate):
    """D9 F1: in c5, with probability `rate`, picks the option whose letter is NOT the planted (own) letter."""
    def f(it, q, cond, u, rng):
        if cond == "c5_planted_own" and rng.random() < rate:
            return next(l for l in it[q]["labels"] if l != it["wrong_ms"])
        return letter(it, q, u < BASE[cond])
    return f


baselines = {
    "constant 'A'": lambda it, q, cond, u, rng: "A",
    "always the aware option": lambda it, q, cond, u, rng: t.aware_letter(it, q),
    "coin flip": lambda it, q, cond, u, rng: "A" if rng.random() < 0.5 else "B",
    "no uptake (c5 = c6 = 0.20)": uptake(with_delta(0.0)),
    "copies its own assistant-turn letter (c4, c5)": copy_letter(False),
    "copies any shown letter (c5 and c6)": copy_letter(True),
    "avoids its own assistant-turn letter, 100%": avoid_letter(1.0),
    "avoids its own assistant-turn letter, 50%": avoid_letter(0.5),
    "avoids its own assistant-turn letter, 40%": avoid_letter(0.4),
    "real uptake, delta 0.15 everywhere": uptake(with_delta(0.15)),
    "ceiling (c6 = 0.95, c5 = 1.0)": uptake(with_delta(0.05, other=0.95)),
}
print("\n4. dumb baselines and known answers (one synthetic run each, full test, 2,000 resamples):")
rng = np.random.default_rng(1)
for name, model in baselines.items():
    out = t.analyse(ordered, synth(ordered, model, rng), seed_b, loo=(name.startswith("real")))
    s = out.get("stats", {})
    d, dm, dt = s.get("delta", [np.nan] * 3), s.get("delta_mismatch", [np.nan] * 3), s.get("delta_match", [np.nan] * 3)
    extra = f"; LOO delta {out['loo_core']['delta_range'][0]:+.3f}..{out['loo_core']['delta_range'][1]:+.3f}, label flips {len(out['loo_core']['label_flips'])}" if "loo_core" in out else ""
    print(f"   {name:48s} delta {d[0]:+.3f} [{d[1]:+.3f}, {d[2]:+.3f}]  match {dt[0]:+.3f}  mismatch {dm[0]:+.3f}  "
          f"om-p2-3 rule: {out.get('verdict_under_om_p2_3_rule')}  -> {out['primary_verdict']} ({out['verdict_reason']}){extra}")

# --- 5. power of the pass rule ---------------------------------------------------------------------------------
reps, bb = (40, 500) if QUICK else (200, 1000)
print(f"\n5. power: P(pass) over {reps} synthetic runs per cell, {bb} resamples each, c6 = 0.20; "
      "comonotone = c5 and c6 share a story's uniform (least noise); independent = most noise")
rng = np.random.default_rng(2)
t0 = time.time()
for n in (len(ordered), 300):
    for como in (True, False):
        row = []
        for d in (0.0, 0.05, 0.10, 0.125, 0.15, 0.20):
            hits = 0
            for r in range(reps):
                order = t.run_order(test, int(rng.integers(2 ** 32)))[:n]
                out = t.analyse(order, synth(order, uptake(with_delta(d), como), rng), int(rng.integers(2 ** 32)),
                                b=bb, loo=False)
                hits += out["primary_verdict"] == "pass"
            row.append(f"{d:.3f}: {hits / reps:.2f}")
        print(f"   n={n:3d} {'comonotone ' if como else 'independent'}  " + "  ".join(row))
print(f"   ({time.time() - t0:.0f} s)")
print("\nDry run done. Temporary files:", TMP)
