"""Dry run for P2-6 (experiments/p2-6-position-or-label.md), every call stubbed: no API, no key, synthetic data only.

    python3 experiments/p2_6_dryrun.py > experiments/p2-6-dryrun-output.txt

It checks, before any call:
  1. the six conversations the frozen code will send (one per cell), and that each manipulation takes effect (D2);
  2. the rule on dumb baselines: constant copy, position-only (bm0's own/other numbers), recency, noise-only: none
     may pass (P3, D5); and the rivals a label-only pass cannot exclude (Sam-distrust), with the fifth cell's reading;
  3. power: pass rate at true label effects 0.15, 0.25, 0.38 and 0.55 with no position effect, with item spread taken
     from bm0's archive (item SD of one own-other contrast 0.43);
  4. the machinery: the cap stops the run, a refusal is written into the cache and stops every later run, a changed
     prompt cannot reuse a cache entry, a stop before 10 complete repeats is untestable, and the gate is closed.
The seed used here is a fixed dry-run constant, never the beacon's."""

import json
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p2_6_position_label as p  # noqa: E402

ITS, ANC = p.items(), p.anchors()
DRY_SEED = 12345


def synth_cache(mu, rng, item_sd=0.30, common_sd=0.30, noise=0.06, nrep=p.REPEATS, hedge=None):
    """Ratings from: b = anchor mean + item noise; rating = b + u * (A - b) + hedge[cell] * (0.5 - b) + noise,
    u = mu[cell] + item effects. hedge (D11d): a pull toward 50 that ignores the shown value (the design review's case)."""
    hedge = hedge or {}
    cache = {}
    for it in ITS:
        q = it["id"]
        a = rng.normal(0, common_sd)
        u = {c: mu[c] + a + rng.normal(0, item_sd) for c in p.CELLS}
        for o in "XY":
            m = ANC[q][f"m_{o}"] / 100
            b = float(np.clip(m + rng.normal(0, 0.05), 0.01, 0.99))
            for r in range(nrep):
                cache[f"base|{q}|{o}|0|{r}"] = {"value": int(np.clip(round(100 * (b + rng.normal(0, noise))), 0, 100)), "cost": 0.0}
                for d in p.DISTANCES:
                    A = p.shown_value(ANC[q][f"m_{o}"], d) / 100
                    for c in p.CELLS:
                        y = b + u[c] * (A - b) + hedge.get(c, 0.0) * (0.5 - b) + rng.normal(0, noise)
                        cache[f"{c}|{q}|{o}|{d}|{r}"] = {"value": int(np.clip(round(100 * y), 0, 100)), "cost": 0.0}
    return cache


def scen(AY, AS, UY, US, UU):
    return dict(AY=AY, AS=AS, UY=UY, US=US, UU=UU)


SCENARIOS = {
    "constant copy (u 0.40 in every cell)": scen(.4, .4, .4, .4, .4),
    "position-only, bm0's numbers (assistant 0.44, user -0.11)": scen(.44, .44, -.11, -.11, -.11),
    "recency (user turn 0.60, assistant 0.20)": scen(.2, .2, .6, .6, .6),
    "noise only (u 0 everywhere)": scen(0, 0, 0, 0, 0),
    "label-only at bm0's gap (yours 0.44, Sam's -0.11, user's 0.20)": scen(.44, -.11, .44, -.11, .2),
    "Sam-distrust (yours 0.30, user's 0.30, Sam's -0.20)": scen(.3, -.2, .3, -.2, .3),
    "label 0.25 with position 0.30": scen(.2 + .125 + .15, .2 - .125 + .15, .2 + .125 - .15, .2 - .125 - .15, .05),
    "hedge 0.5 toward 50 on 'yours' cells only, uptake 0.2 everywhere (D11d)": (scen(.2, .2, .2, .2, .2), {"AY": .5, "UY": .5}),
    "hedge 0.8 toward 50 on 'yours' cells only, uptake 0.2 everywhere (D11d)": (scen(.2, .2, .2, .2, .2), {"AY": .8, "UY": .8}),
    "power: label 0.15, no position": scen(.275, .125, .275, .125, .2),
    "power: label 0.25, no position": scen(.325, .075, .325, .075, .2),
    "power: label 0.38, no position": scen(.39, .01, .39, .01, .2),
    "power: label 0.55, no position": scen(.475, -.075, .475, -.075, .2),
}


def main():
    print("# P2-6 dry run (every call stubbed; synthetic data only)\n")
    print("## 1. The conversations the frozen code sends (item co01, statement X, d = -30)\n")
    it = ITS[0]
    A = p.shown_value(ANC[it["id"]]["m_X"], -30)
    msgs = {c: p.messages(c, it, "X", None if c == "base" else A) for c in ("base",) + p.CELLS}
    for c, m in msgs.items():
        print(f"### {c}\n```\n{json.dumps(m, indent=1, ensure_ascii=False)}\n```")
    texts = {c: json.dumps(m) for c, m in msgs.items()}
    print("\nD2 checks on the prompts:")
    print("  - every cell's prompt differs from every other's:", len(set(texts.values())) == 6)
    print("  - assistant cells have 3 messages, user cells 1:", all(len(msgs[c]) == 3 for c in ("AY", "AS")) and
          all(len(msgs[c]) == 1 for c in ("UY", "US", "UU")))
    val = json.dumps({"probability": A})
    print(f"  - the value string {val} appears exactly once in every non-baseline cell:",
          all(texts[c].count(val.replace('"', '\\"')) == 1 for c in p.CELLS))
    print("  - AY and AS differ only in the label sentence:", texts["AY"].replace(p.LABEL["Y"], "#") == texts["AS"].replace(p.LABEL["S"], "#"))
    print("  - UY, US and UU differ only in the label sentence:",
          len({texts[c].replace(p.LABEL[c[1]], "#") for c in ("UY", "US", "UU")}) == 1)
    print("  - the request sentence is identical in all five:", all(p.request(it["X"]) in texts[c] for c in p.CELLS))
    print("  - the baseline is the first user message of the assistant cells:", msgs["base"][0] == msgs["AY"][0])

    print("\n## 2-3. The rule on synthetic data (200 simulated runs per scenario; item SD from bm0)\n")
    print("| scenario | true L | true P | mean L̂ | mean L̂_s | verdicts (share of 200) | fifth-cell reading (share) |")
    print("|---|---|---|---|---|---|---|")
    rng = np.random.default_rng(DRY_SEED)
    for name, mu in SCENARIOS.items():
        mu, hedge = mu if isinstance(mu, tuple) else (mu, None)
        Lt = ((mu["AY"] - mu["AS"]) + (mu["UY"] - mu["US"])) / 2
        Pt = ((mu["AY"] - mu["UY"]) + (mu["AS"] - mu["US"])) / 2
        V, Ls, Lss, UR = {}, [], [], {}
        for _ in range(200):
            r = p.analyse_cache(synth_cache(mu, rng, hedge=hedge), ITS, ANC, int(rng.integers(0, 2**32)), check=False)
            V[r["verdict"]] = V.get(r["verdict"], 0) + 1
            UR[r["user_reading"]] = UR.get(r["user_reading"], 0) + 1
            Ls.append(r["stats"]["L"][0])
            Lss.append(r["stats_shift"]["L"][0])
        vs = ", ".join(f"{k} {v / 200:.2f}" for k, v in sorted(V.items(), key=lambda x: -x[1]))
        us = ", ".join(f"{k} {v / 200:.2f}" for k, v in sorted(UR.items(), key=lambda x: -x[1]))
        print(f"| {name} | {Lt:+.2f} | {Pt:+.2f} | {np.mean(Ls):+.2f} | {np.mean(Lss):+.2f} | {vs} | {us} |")

    print("\n## 4. Machinery\n")
    tmp = Path(tempfile.mkdtemp())
    p.RESULTS = tmp
    jobs = p.jobs(ITS, ANC, DRY_SEED)
    print(f"- jobs: {len(jobs)} (expected {p.REPEATS * (32 + 32 * 2 * 5)}); first repeat's jobs all carry repeat 0:",
          all(j[0].endswith("|0") for j in jobs[:352]))
    rng = np.random.default_rng(1)

    class Refused(Exception):
        request_id, call, stop_details = "req_DRYRUN", "p2-6", "stub"

    def stub(msgs, refuse_at=None, counter=[0]):
        counter[0] += 1
        if refuse_at and counter[0] == refuse_at:
            raise Refused()
        return {"probability": int(rng.integers(0, 101))}, 5e-5, f"req_stub_{counter[0]}"
    stub.refusal_error = Refused

    c = p.GuardedCaller(tmp / "cap.json", 0.01, "dry cap", stub)
    st = c.run(jobs, workers=8)
    print(f"- cap $0.01 at $0.00005 a call: status {st}, cached {len(c.cache)}, spent ${c.spent():.5f}, "
          f"calls finishing after the stop {c.after_stop}")
    cache = json.loads((tmp / "cap.json").read_text())
    print("  analysis of the capped cache:", p.analyse_cache(cache, ITS, ANC, 7, check=True)["verdict"],
          "-", p.analyse_cache(cache, ITS, ANC, 7, check=False).get("why"))

    def stub_ref(msgs, counter=[0]):
        counter[0] += 1
        if counter[0] == 50:
            raise Refused()
        return {"probability": 50}, 5e-5, f"req_{counter[0]}"
    stub_ref.refusal_error = Refused
    c = p.GuardedCaller(tmp / "ref.json", 1.0, "dry refusal", stub_ref)
    st = c.run(jobs[:400], workers=8)
    refused = [k for k, v in c.cache.items() if v.get("refused")]
    print(f"- refusal at call 50: status {st}, refused entries {len(refused)}, refusal.md written: {(tmp / 'refusal.md').exists()}, "
          f"cached {len(c.cache)}, after stop {c.after_stop}")
    try:
        p.GuardedCaller(tmp / "ref.json", 1.0, "dry refusal rerun", stub_ref)
        print("- re-run after the refusal: STARTED (wrong)")
    except SystemExit as e:
        print(f"- re-run after the refusal: exits before any call ({e})")
    (tmp / "refusal.md").unlink()
    try:
        p.GuardedCaller(tmp / "ref.json", 1.0, "dry refusal rerun 2", stub_ref)
        print("- re-run with refusal.md removed but the refused entry kept: STARTED (wrong)")
    except SystemExit:
        print("- re-run with refusal.md removed but the refused entry kept: exits before any call")

    full = synth_cache(SCENARIOS["noise only (u 0 everywhere)"], np.random.default_rng(3))
    for k, v in full.items():
        cell, q, o, d, _ = k.split("|")
        A = None if cell == "base" else p.shown_value(ANC[q][f"m_{o}"], int(d))
        v["sha256"] = p.content_hash(p.messages(cell, {i["id"]: i for i in ITS}[q], o, A))
    k0 = next(k for k in full if k.startswith("AS|"))
    full[k0]["sha256"] = "0" * 64
    try:
        p.verify_cache(ITS, ANC, full)
        print("- tampered cache entry: NOT caught (wrong)")
    except AssertionError as e:
        print(f"- tampered cache entry: caught ({e})")
    nine = {k: v for k, v in full.items() if int(k.split("|")[-1]) < 9}
    print("- a stop after 9 complete repeats:", p.analyse_cache(nine, ITS, ANC, 7, check=False)["verdict"])
    ten = {k: v for k, v in full.items() if int(k.split("|")[-1]) < 10}
    print("- a stop after 10 complete repeats:", p.analyse_cache(ten, ITS, ANC, 7, check=False)["verdict"], "(analysed)")
    # D11e (F3): can a call start after a refusal? spent() slowed so workers queue on the lock; refusal at call 20.
    import threading, time
    entered, lock_n, refused_at = [], threading.Lock(), {}

    def stub_race(msgs, counter=[0]):
        with lock_n:
            counter[0] += 1
            n = counter[0]
            entered.append((n, time.perf_counter()))
        time.sleep(0.002)
        if n == 20:
            refused_at["t"] = time.perf_counter()
            raise Refused()
        return {"probability": 50}, 5e-5, f"req_race_{n}"
    stub_race.refusal_error = Refused
    (tmp / "refusal.md").unlink(missing_ok=True)
    c = p.GuardedCaller(tmp / "race.json", 1.0, "dry race", stub_race)
    orig = c.spent
    c.spent = lambda: (time.sleep(0.003), orig())[1]
    c.run(jobs[:400], workers=8)
    after = [n for n, t in entered if t > refused_at["t"]]
    print(f"- refusal race (spent() slowed 3 ms, refusal at call 20, 8 workers): calls entering the model after the refusal "
          f"was raised: {len(after)} (at most workers - 1 = 7 may already have cleared the locked gate; none may start later); "
          f"total calls entered {len(entered)}")
    print("- gate now:", p.gate())
    r = p.analyse_cache(synth_cache(SCENARIOS["noise only (u 0 everywhere)"], np.random.default_rng(4)), ITS, ANC, 7, check=False)
    print(f"- pairs kept / dropped for |D| < 0.05 on synthetic baselines: {r['pairs_kept']} / {r['pairs_dropped']}; "
          f"items usable {r['items_usable']}")
    print(f"- displacements actually shown (A - anchor mean, after clipping to [2, 98]), points:")
    disp = {f"{q}|{o}|{d}": p.shown_value(ANC[q][f'm_{o}'], d) - round(ANC[q][f'm_{o}']) for q in ANC for o in 'XY' for d in p.DISTANCES}
    small = {k: v for k, v in disp.items() if abs(v) < 5}
    print(f"  {sum(abs(v) == 30 for v in disp.values())} of 64 at the full 30; {len(small)} under 5 points after clipping: {sorted(small)}")


if __name__ == "__main__":
    main()
