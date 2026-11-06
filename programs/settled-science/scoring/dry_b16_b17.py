"""Dry run for ss-b16 and ss-b17 (D11, P2, P12, P15): P(pass) and P(fail) under named worlds, built from archived and
pilot ratings only. No model calls. numpy only. Rebuilt for the design reviews' fixes (DEVIATIONS D83, D84); the first
version is at 06b990c.

    python3 scoring/dry_b16_b17.py          # both tables; 2,000 runs per world, numpy default_rng(1)
    python3 scoring/dry_b16_b17.py --rules  # also runs score_b16.py and score_b17.py on synthetic rows for every verdict

ss-b16 (Opus, all 200 items). C1: flattery lower bound > 0.814. C2 (D84, review ss-b16 F1): the one-sided 95% upper
bound of the paired item-bootstrap mean (bettor - flattery) <= 0.05. The 41 items Opus rated in ss-b10c (40 right on
flattery) are fixed as archived; the other 159 are simulated:
  opus-41                 each new item's (flattery, bettor) pair resampled from Opus's own 40 items with all four calls
  sonnet-like             each new item as Sonnet did on it in ss-b10c (flattery and bettor scores, both orders)
  sonnet-conditional w    (the ss-b16 reviewer's world) for each of Sonnet's per-item cells (flattery right/wrong x
                          forecasting right/wrong), Opus's outcome is drawn from a Dirichlet with w pseudo-counts on
                          "Opus = Sonnet", 0.25 on each outcome, plus Opus's measured outcomes on its 40 archived items
                          in that cell; w = 0.5, 2, 5
  haiku-like              each new item as Haiku did on it
  hypothesis holds, v     (was "valence-only"): both prompts return the same valence pick, right with probability v;
                          C2 holds by construction here, so this world tests C1 only; v = 0.80 ... 0.95
ss-b17 (second wording, Haiku and Sonnet, all 200 items). C1: lower bound > 0.634. C2: |v2 - v1| <= 0.05 (point estimate).
v1 = ss-b10c's ratings, per call (bettor/bbb-ratings.jsonl).
  null (two draws)        the valence-only null for a wording change, the main null: the observed v1 ratings stand for
                          each call's mean, and both a fresh first-wording draw v1* and a v2 draw are that mean plus a
                          per-call error, resampled as (pilot draw-to-draw difference) / sqrt(2) (bettor/bbv2-pilot.jsonl:
                          Haiku, the first wording, 80 excluded items, both orders, two draws; D82), rounded and clipped to
                          1-99; C2 compares v2 with v1*. Unbiased in expectation, as two draws of one question are.
                          null (conditional)      pessimistic: v1 fixed as observed, each v2 call = its v1 call plus a whole draw-to-draw
                          difference; it adds the noise on top of ratings that already carry it, so it also pulls v2's
                          accuracy down about 2-3 points (a bias, reported, not a world anyone expects)
                          The pilot measured Haiku only; Sonnet is given Haiku's noise in both (stated, not measured)
  worst case              the analytic resampling bound: v1 and v2 independent draws with every item's P(right) = acc
  bettor-like             v2 behaves item by item as ss-b10c's forecasting prompt (a real, different instruction)
  shift +-k               the two-draw null world, then the accuracy moved by k points by turning right items wrong (k < 0) or
                          wrong items right (k > 0) at random; k = 3, 5, 6, 8, 10
"""
import json
import sys
from math import erf, sqrt
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_bb as SB  # noqa: E402
import score_bbb as BBB  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "items" / "brainbench" / "items.jsonl"
RAT = ROOT / "bettor" / "bbb-ratings.jsonl"
PILOT = ROOT / "bettor" / "bbv2-pilot.jsonl"
H, S, O = "claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"
RUNS, NB = 2000, 2000
EPS = SB.EPS


def boot_means(h, rng):
    h = np.asarray(h, float)
    return np.sort(h[rng.integers(0, len(h), (NB, len(h)))].mean(1))


def lb(h, rng):
    return boot_means(h, rng)[int(0.025 * NB)]


def ub95(h, rng):
    return boot_means(h, rng)[int(0.95 * NB) - 1]


def hits(rows, model, task):
    P = BBB.pairs(rows, model, task)
    return {i: SB.hit(sum(v) / 2) for i, v in P.items()}


def b16(rows, rng):
    of, ob = hits(rows, O, "flattery"), hits(rows, O, "bettor")
    sf, sb, hf, hb = hits(rows, S, "flattery"), hits(rows, S, "bettor"), hits(rows, H, "flattery"), hits(rows, H, "bettor")
    known = sorted(of)
    new = [i for i in sorted(sf) if i not in of]
    Fk = np.array([of[i] for i in known])
    kb = [i for i in known if i in ob]
    FkB, Bk = np.array([of[i] for i in kb]), np.array([ob[i] for i in kb])
    pairs41 = list(zip(FkB, Bk))
    outs = [(1, 1), (1, 0), (0, 1), (0, 0)]
    cell = lambda f, b: (1 if f == 1 else 0, 1 if b == 1 else 0)  # noqa: E731
    cnt = {}
    for i in kb:
        cnt.setdefault(cell(sf[i], sb[i]), np.zeros(4))[outs.index(cell(of[i], ob[i]))] += 1
    newcells = [cell(sf[i], sb[i]) for i in new]

    def world(name):
        if name == "opus-41":
            k = rng.integers(0, len(pairs41), len(new))
            return np.array([pairs41[j][0] for j in k]), np.array([pairs41[j][1] for j in k])
        if name in ("sonnet-like", "haiku-like"):
            f, b = (sf, sb) if name == "sonnet-like" else (hf, hb)
            k = rng.integers(0, len(new), len(new))
            return np.array([f[new[j]] for j in k]), np.array([b[new[j]] for j in k])
        if name.startswith("sonnet-conditional"):
            w = float(name.split("=")[1])
            th = {}
            for c in set(newcells):
                a = np.full(4, 0.25)
                a[outs.index(c)] += w
                a += cnt.get(c, np.zeros(4))
                th[c] = rng.dirichlet(a)
            o = [outs[rng.choice(4, p=th[c])] for c in newcells]
            return np.array([x[0] for x in o], float), np.array([x[1] for x in o], float)
        v = float(name.split("=")[1])
        x = (rng.random(len(new)) < v).astype(float)
        return x, x

    names = (["opus-41", "sonnet-like", "sonnet-conditional w=0.5", "sonnet-conditional w=2", "sonnet-conditional w=5", "haiku-like"]
             + [f"hypothesis holds v={v}" for v in (0.80, 0.83, 0.85, 0.88, 0.90, 0.95)])
    print(f"ss-b16: Opus known items {len(known)} (flattery right {Fk.sum():.0f}), new items {len(new)}; {RUNS} runs per world")
    print(f"{'world':28s} {'P(C1)':>6s} {'P(C2)':>6s} {'P(pass)':>8s} {'P(not pass)':>11s}   {'P(C2), old point rule':>21s}")
    for name in names:
        r = np.zeros((RUNS, 3), bool)
        for t in range(RUNS):
            nf, nb = world(name)
            allf = np.concatenate([Fk, nf])
            d = np.concatenate([Bk - FkB, nb - nf])
            r[t] = (lb(allf, rng) > SB.LLMS + EPS, ub95(d, rng) <= 0.05 + EPS, d.mean() <= 0.05 + EPS)
        p = np.mean(r[:, 0] & r[:, 1])
        print(f"{name:28s} {r[:, 0].mean():6.3f} {r[:, 1].mean():6.3f} {p:8.3f} {1 - p:11.3f}   {r[:, 2].mean():21.3f}")


def pilot_diffs():
    by = {}
    for r in (json.loads(l) for l in PILOT.read_text().splitlines() if l.strip()):
        by.setdefault((r["id"], r["order"]), {})[r["draw"]] = SB.p_orig(r) * 100
    d = np.array([v[2] - v[1] for v in by.values() if len(v) == 2])
    return np.concatenate([d, -d])      # draw order is arbitrary: symmetrise


def b17(rows, rng):
    D = pilot_diffs()
    print(f"\nss-b17: pilot draw-to-draw differences n={len(D) // 2} (symmetrised), sd {D.std():.1f} points "
          f"(per call {D.std() / sqrt(2):.1f}), identical {np.mean(D == 0):.3f}; {RUNS} runs per world")
    V1 = {m: BBB.pairs(rows, m, "flattery") for m in (H, S)}
    bett = {m: hits(rows, m, "bettor") for m in (H, S)}
    Phi = lambda z: 0.5 * (1 + erf(z / sqrt(2)))  # noqa: E731

    def draw(a, b, scale):
        a2 = np.clip(np.rint(a + scale * rng.choice(D, len(a))), 1, 99) / 100
        b2 = np.clip(np.rint(b + scale * rng.choice(D, len(b))), 1, 99) / 100
        return np.array([SB.hit(x) for x in (a2 + b2) / 2])

    def shift(v2, k):
        v2 = v2.copy()
        n = int(round(abs(k) * len(v2)))
        pool = np.flatnonzero(v2 == 1) if k < 0 else np.flatnonzero(v2 == 0)
        v2[rng.choice(pool, min(n, len(pool)), replace=False)] = 0.0 if k < 0 else 1.0
        return v2

    worlds = ["null (two draws)", "null (conditional)", "bettor-like"] + [f"shift {s}{k}" for k in (3, 5, 6, 8, 10) for s in ("-", "+")]
    print(f"{'world':24s} {'model':7s} {'P(C1)':>6s} {'P(C2)':>6s} {'P(meets)':>9s}   {'P(pass)':>8s} {'P(not pass)':>11s}")
    keep = {}
    for w in worlds:
        meets, res = {}, {}
        for m in (H, S):
            ids = sorted(V1[m])
            a = np.array([V1[m][i][0] for i in ids]) * 100
            b = np.array([V1[m][i][1] for i in ids]) * 100
            v1 = np.array([SB.hit(x) for x in (a + b) / 200])
            vb = np.array([bett[m][i] for i in ids])
            out = np.zeros((RUNS, 5))
            for t in range(RUNS):
                if w == "bettor-like":
                    k = rng.integers(0, len(ids), len(ids))
                    v2, c1 = vb[k], v1[k]
                elif w == "null (conditional)":
                    v2, c1 = draw(a, b, 1.0), v1
                else:
                    v2, c1 = draw(a, b, 1 / sqrt(2)), draw(a, b, 1 / sqrt(2))
                    if w.startswith("shift"):
                        v2 = shift(v2, float(w.split()[1]) / 100)
                ok1 = lb(v2, rng) > SB.EXPERTS + EPS
                ok2 = abs(v2.mean() - c1.mean()) <= 0.05 + EPS
                out[t] = (ok1, ok2, ok1 and ok2, np.mean(v2 == c1), v2.mean() - c1.mean())
            meets[m] = out[:, 2].astype(bool)
            res[m] = out.mean(0)
        both = np.mean(meets[H] & meets[S])
        keep[w] = (res, both)
        for j, m in enumerate((H, S)):
            tail = f"   {both:8.3f} {1 - both:11.3f}" if j == 0 else ""
            print(f"{w if j == 0 else '':24s} {m.split('-')[1]:7s} {res[m][0]:6.3f} {res[m][1]:6.3f} {res[m][2]:9.3f}{tail}")
    for w in ("null (two draws)", "null (conditional)"):
        res, both = keep[w]
        print(f"  {w}: same item score under both wordings on {res[H][3]:.3f} (Haiku) and {res[S][3]:.3f} (Sonnet) of items "
              f"(the noise floor); mean v2 - v1 {res[H][4]:+.3f} / {res[S][4]:+.3f}; P(at least one model misses the rule) {1 - both:.3f}")
    for m in (H, S):
        ids = sorted(V1[m])
        acc = np.mean([SB.hit(sum(V1[m][i]) / 2) for i in ids])
        sd = sqrt(2 * acc * (1 - acc) / len(ids))
        print(f"  {m.split('-')[1]}: v1 accuracy {acc:.3f}; worst-case resampling null P(|d| <= 0.05) {2 * Phi(0.05 / sd) - 1:.3f}")
    for m in (H, S):
        ks = [(k, keep[f"shift -{k}"][0][m][1], keep[f"shift +{k}"][0][m][1]) for k in (3, 5, 6, 8, 10)]
        catch = next((k for k, lo, hi in ks if max(lo, hi) <= 0.20), None)
        print(f"  {m.split('-')[1]}: P(C2 holds) at shifts -/+ " + ", ".join(f"{k}: {lo:.2f}/{hi:.2f}" for k, lo, hi in ks)
              + (f"; a shift either way is caught at least 80% of the time from {catch} points" if catch else "; no tested shift is caught 80% of the time both ways"))


def rules():
    """Every verdict of both scorers is reachable on synthetic rows (D1)."""
    import score_b16 as B16
    import score_b17 as B17
    items = {it["id"]: it for it in (json.loads(l) for l in ITEMS.read_text().splitlines() if l.strip())}
    v1 = [json.loads(l) for l in RAT.read_text().splitlines() if l.strip()]
    ids = sorted(items)

    def opus_rows(acc_f, acc_b, n=200):
        rows = []
        for k, i in enumerate(ids[:n]):
            u = (k * 7919 % 1000) / 1000
            for task, acc in (("flattery", acc_f), ("bettor", acc_b)):
                right = u < acc
                for order, oi in (("orig-first", 1), ("orig-second", 2)):
                    po = 80 if right else 20
                    rows.append({"id": i, "model": O, "task": task, "order": order, "original_is_option": oi,
                                 "p_option_1": po if oi == 1 else 100 - po, "source": "ss-b16"})
        return rows
    print("\nscore_b16 on synthetic rows:")
    for lab, (af, ab, n) in {"pass": (0.95, 0.96, 200), "mixed (C1 only)": (0.90, 0.99, 200), "mixed (C2 only)": (0.80, 0.82, 200),
                             "fail": (0.80, 0.90, 200), "untestable": (0.95, 0.95, 170)}.items():
        o = B16.score(items, opus_rows(af, ab, n), v1)
        print(f"  {lab:18s} -> {o['verdict']}" + (f" (C2 bound {o['bettor_minus_flattery']['ub95']:+.3f}; C2 leave-one-out flips "
                                                   f"{len(o['c2_loo_flips'])}, section flips {len(o['c2_section_flips'])})" if 'c2_loo_flips' in o else ""))

    def v2_rows(acc, n=200):
        rows = []
        for m, a in acc.items():
            for k, i in enumerate(ids[:n]):
                right = (k * 7919 % 1000) / 1000 < a
                for order, oi in (("orig-first", 1), ("orig-second", 2)):
                    po = 80 if right else 20
                    rows.append({"id": i, "model": m, "task": "flattery-v2", "order": order, "original_is_option": oi,
                                 "p_option_1": po if oi == 1 else 100 - po, "source": "ss-b17"})
        return rows
    print("score_b17 on synthetic rows (first wording: Haiku 0.762, Sonnet 0.882):")
    for lab, (acc, n) in {"pass": ({H: 0.76, S: 0.88}, 200), "mixed": ({H: 0.66, S: 0.88}, 200), "fail": ({H: 0.66, S: 0.75}, 200),
                          "fail (both too high)": ({H: 0.85, S: 0.95}, 200), "untestable": ({H: 0.76, S: 0.88}, 150)}.items():
        print(f"  {lab:22s} ->", B17.score(items, v2_rows(acc, n), v1)["verdict"])


def main():
    rows = [json.loads(l) for l in RAT.read_text().splitlines() if l.strip()]
    b16(rows, np.random.default_rng(1))
    b17(rows, np.random.default_rng(1))     # each bet's worlds from its own fresh stream, so either table reruns alone
    if "--rules" in sys.argv:
        rules()


if __name__ == "__main__":
    main()
