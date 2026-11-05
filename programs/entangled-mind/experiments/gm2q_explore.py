"""em-gm2q EXPLORATORY checks, written after the data (not pre-registered; never promoted to the verdict).

    python experiments/gm2q_explore.py      # prints A-D below from results/gm2q-conversations.json; no calls

A: D69's first wrong-target flag (within 5 of the 4th statement, > 20 from the usual answer), for comparison.
B: R with the D70-flagged answers dropped, on the items where every cell keeps >= 2 ratings.
C: R and the qonly gate without the one item with the largest qonly order effect.
D: each flagged qonly answer in the cells that lost 3 or more, beside the 4th statement's and the usual answer's means."""
import json
import numpy as np
import gm2q_questions_only as g


def main():
    c, its = json.loads(g.CACHE.read_text()), g.items()
    qs, seed = list(its), g.SEED_RECORDED % (2 ** 63)
    for model, short in ((g.H, "haiku"), (g.S, "sonnet")):
        ds = {q: [[x["turns"][-1]["rating"] for x in g.cell(c, model, q, o, "shown")] for o in g.ORDERS] for q in qs}
        dq = {q: [[x["turns"][-1]["rating"] for x in g.cell(c, model, q, o, "qonly")] for o in g.ORDERS] for q in qs}
        stmt = {q: {k: float(np.mean([t["rating"] for o in g.ORDERS for x in g.cell(c, model, q, o, "shown") for t in x["turns"]
                                      if t["kind"] == "S" and t["claim"] == k])) for k in its[q][1]} for q in qs}
        fin = {q: float(np.mean([r for x in ds[q] for r in x])) for q in qs}
        s4 = lambda q, o: stmt[q][g.fourth(its[q][1], o)]
        flag_a = lambda r, q, o: abs(r - s4(q, o)) <= 5 and abs(r - fin[q]) > 20
        cl_a = {q: [[r for r in dq[q][j] if not flag_a(r, q, o)] for j, o in enumerate(g.ORDERS)] for q in qs}
        share_a = np.mean([flag_a(r, q, o) for q in qs for j, o in enumerate(g.ORDERS) for r in dq[q][j]])
        print(f"{short} A: D69 first flag share {share_a:.3f}; qonly gate with those dropped p = {g.perm_p(cl_a, qs, seed + 6):.4f}")
        cl = {q: [[r for r in dq[q][j] if not g.wrong_target(r, s4(q, o), fin[q])] for j, o in enumerate(g.ORDERS)] for q in qs}
        keep = [q for q in qs if all(len(x) >= 2 for x in cl[q])]
        rb = g.ratio_boot(cl, ds, keep, seed + 3)
        print(f"{short} B: D70-flagged dropped, {len(keep)} items kept (out: {[q for q in qs if q not in keep]}): "
              f"R = {rb['R']:.2f} [{rb['lo']:.2f}, {rb['hi']:.2f}], qonly gate p = {g.perm_p(cl, keep, seed + 6):.4f}")
        big = max(qs, key=lambda q: g.vc(dq[q])[0])
        s = [q for q in qs if q != big]
        rb = g.ratio_boot(dq, ds, s, seed + 3)
        print(f"{short} C: without {big}: R = {rb['R']:.2f} [{rb['lo']:.2f}, {rb['hi']:.2f}], qonly gate p = {g.perm_p(dq, s, seed + 2):.4f}")
        for q in qs:
            for j, o in enumerate(g.ORDERS):
                fl = [r for r in dq[q][j] if g.wrong_target(r, s4(q, o), fin[q])]
                if len(fl) >= 3:
                    print(f"{short} D: {q} {o}: answers {dq[q][j]}; flagged {len(fl)}; 4th statement {s4(q, o):.0f}, usual answer "
                          f"{fin[q]:.0f}; statements by position {[round(stmt[q][its[q][1][i]]) for i in g.LATIN[j]]}")


if __name__ == "__main__":
    main()
