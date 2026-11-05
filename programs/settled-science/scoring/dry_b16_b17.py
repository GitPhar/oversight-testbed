"""Dry run for ss-b16 and ss-b17 (D11, P12, P15): P(pass) and P(fail) under named worlds, built from archived ratings only.
No model calls. numpy only.

    python3 scoring/dry_b16_b17.py          # prints both tables; 2,000 runs per world, numpy default_rng(1)
    python3 scoring/dry_b16_b17.py --rules  # also runs score_b16.py and score_b17.py on synthetic rows for every verdict

ss-b16 (Opus, all 200 items; C1 lower bound > 0.814, C2 bettor - flattery <= 0.05). The 41 items Opus rated in ss-b10c
(40 right on flattery) are fixed as archived; the other 159 items are simulated:
  opus-41      each new item's (flattery, bettor) hit pair resampled from Opus's own 40 items with all four calls
  sonnet-like  each new item behaves as Sonnet did on that item in ss-b10c (its flattery and bettor hits, both orders)
  haiku-like   each new item behaves as Haiku did on that item in ss-b10c
  valence-only v (the null world the launch asked for: the model knows only which version is better news, so both prompts
               return the same valence pick, right with probability v on each new item); v = 0.80, 0.85, 0.88, 0.90, 0.95
ss-b17 (second wording, Haiku and Sonnet, all 200 items; C1 lower bound > 0.634, C2 |v2 - v1| <= 0.05), v1 = ss-b10c's
per-item hits (bbb-ratings.jsonl):
  valence-only  the null world for a wording change: the model answers the same valence question whatever the sentence,
               so each item's v2 pick equals its v1 pick except for rating noise. The archive holds no repeat of these calls
               with the same prompt and order, so the noise is set pessimistically to half the per-item discordance between
               ss-b10c's flattery and forecasting prompts (Haiku 0.305, Sonnet 0.105), with flips balanced so the expected
               accuracy is unchanged
  bettor-like   v2 behaves per item as the forecasting prompt did (a real, different wording and instruction)
  drop k        the shortcut is sentence-specific: v2 loses k points (k = 5, 8, 10, 15) on each model, by turning right
               items wrong at random
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_bb as SB  # noqa: E402
import score_bbb as BBB  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "items" / "brainbench" / "items.jsonl"
RAT = ROOT / "bettor" / "bbb-ratings.jsonl"
H, S, O = "claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"
RUNS, NB = 2000, 2000


def lb(h, rng):
    h = np.asarray(h, float)
    return np.sort(h[rng.integers(0, len(h), (NB, len(h)))].mean(1))[int(0.025 * NB)]


def hits(rows, model, task):
    P = BBB.pairs(rows, model, task)
    return {i: SB.hit(sum(v) / 2) for i, v in P.items()}


def b16(rows, rng):
    ids = sorted(json.loads(l)["id"] for l in ITEMS.read_text().splitlines() if l.strip())
    of, ob = hits(rows, O, "flattery"), hits(rows, O, "bettor")
    known = sorted(of)
    pairs41 = [(of[i], ob[i]) for i in known if i in ob]
    new = [i for i in ids if i not in of]
    hf, hb, sf, sb = hits(rows, H, "flattery"), hits(rows, H, "bettor"), hits(rows, S, "flattery"), hits(rows, S, "bettor")
    worlds = {"opus-41": None, "sonnet-like": (sf, sb), "haiku-like": (hf, hb)}
    worlds.update({f"valence-only v={v}": v for v in (0.80, 0.85, 0.88, 0.90, 0.95)})
    print(f"ss-b16: Opus known items {len(known)} (flattery right {sum(of.values())}), new items {len(new)}; {RUNS} runs per world")
    print(f"{'world':24s} {'P(C1)':>6s} {'P(C2)':>6s} {'P(pass)':>8s} {'P(fail or mixed)':>17s} {'mean acc':>9s}")
    for name, w in worlds.items():
        c1 = c2 = ps = 0
        accs = []
        for _ in range(RUNS):
            F = [of[i] for i in known]
            B = [ob[i] for i in known if i in ob]
            Fk = [of[i] for i in known if i in ob]
            if w is None:
                pick = rng.integers(0, len(pairs41), len(new))
                nf = [pairs41[k][0] for k in pick]
                nb = [pairs41[k][1] for k in pick]
            elif isinstance(w, float):
                nf = list((rng.random(len(new)) < w).astype(float))
                nb = nf
            else:
                nf = [w[0][i] for i in new]
                nb = [w[1][i] for i in new]
                # parameter uncertainty: resample the new items' behaviour from the same model's items
                pick = rng.integers(0, len(new), len(new))
                nf = [nf[k] for k in pick]
                nb = [nb[k] for k in pick]
            allf = F + nf
            d = np.mean(B + nb) - np.mean(Fk + nf)
            a = lb(allf, rng) > SB.LLMS + SB.EPS
            b = d <= 0.05 + SB.EPS
            c1 += a
            c2 += b
            ps += a and b
            accs.append(np.mean(allf))
        print(f"{name:24s} {c1 / RUNS:6.3f} {c2 / RUNS:6.3f} {ps / RUNS:8.3f} {1 - ps / RUNS:17.3f} {np.mean(accs):9.3f}")


def b17(rows, rng):
    print(f"\nss-b17: v1 = ss-b10c's wording on all 200 items; {RUNS} runs per world")
    print(f"{'world':28s} {'model':7s} {'P(C1)':>6s} {'P(C2)':>6s} {'P(meets)':>9s}   {'P(pass)':>8s} {'P(not pass)':>11s}")
    base = {m: hits(rows, m, "flattery") for m in (H, S)}
    bett = {m: hits(rows, m, "bettor") for m in (H, S)}
    worlds = ["valence-only", "bettor-like"] + [f"drop {k}" for k in (5, 8, 10, 15)]
    for w in worlds:
        meets = {}
        res = {}
        for m in (H, S):
            ids = sorted(base[m])
            v1 = np.array([base[m][i] for i in ids])
            vb = np.array([bett[m][i] for i in ids])
            disc = float(np.mean(v1 != vb))
            out = np.zeros((RUNS, 3), bool)
            for r in range(RUNS):
                if w == "valence-only":
                    v2 = v1.copy()
                    right, wrong = v1 == 1, v1 == 0
                    f = disc / 2                                   # half of the cross-prompt discordance as rating noise
                    to_wrong = right & (rng.random(len(v1)) < f)
                    to_right = wrong & (rng.random(len(v1)) < f * right.sum() / max(1, wrong.sum()))
                    v2[to_wrong], v2[to_right] = 0.0, 1.0
                elif w == "bettor-like":
                    pick = rng.integers(0, len(ids), len(ids))
                    v2, v1r = vb[pick], v1[pick]
                else:
                    k = int(w.split()[1]) / 100
                    v2 = v1.copy()
                    right = np.flatnonzero(v1 == 1)
                    n = int(round(k * len(v1)))
                    v2[rng.choice(right, n, replace=False)] = 0.0
                cmp1 = v1r if w == "bettor-like" else v1
                a = lb(v2, rng) > SB.EXPERTS + SB.EPS
                b = abs(np.mean(v2) - np.mean(cmp1)) <= 0.05 + SB.EPS
                out[r] = (a, b, a and b)
            meets[m] = out[:, 2]
            res[m] = out.mean(0)
        both = np.mean(meets[H] & meets[S])
        for k, m in enumerate((H, S)):
            tail = f"   {both:8.3f} {1 - both:11.3f}" if k == 0 else ""
            print(f"{w if k == 0 else '':28s} {m.split('-')[1]:7s} {res[m][0]:6.3f} {res[m][1]:6.3f} {res[m][2]:9.3f}{tail}")
    for m in (H, S):
        ids = sorted(base[m])
        print(f"  {m.split('-')[1]}: v1 accuracy {np.mean([base[m][i] for i in ids]):.3f}; flattery-vs-bettor per-item discordance "
              f"{np.mean([base[m][i] != bett[m][i] for i in ids]):.3f}")


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
            for task, acc in (("flattery", acc_f), ("bettor", acc_b)):
                right = (k * 7919 % 1000) / 1000 < acc
                for order, oi in (("orig-first", 1), ("orig-second", 2)):
                    po = 80 if right else 20
                    rows.append({"id": i, "model": O, "task": task, "order": order, "original_is_option": oi,
                                 "p_option_1": po if oi == 1 else 100 - po, "source": "ss-b16"})
        return rows
    print("\nscore_b16 on synthetic rows:")
    for lab, (af, ab, n) in {"pass": (0.95, 0.96, 200), "mixed (C1 only)": (0.90, 0.99, 200), "mixed (C2 only)": (0.80, 0.82, 200),
                             "fail": (0.80, 0.90, 200), "untestable": (0.95, 0.95, 170)}.items():
        print(f"  {lab:18s} ->", B16.score(items, opus_rows(af, ab, n), v1)["verdict"])
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
    rng = np.random.default_rng(1)
    b16(rows, rng)
    b17(rows, rng)
    if "--rules" in sys.argv:
        rules()


if __name__ == "__main__":
    main()
