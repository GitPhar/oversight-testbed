"""Regenerate ledger/prior.md from the committed ledger and maps. No network, no keys, standard library only.

    python3 ledger/prior.py

In plain English: before the engine states odds on a new bet, it should start from its own record: how often
bets like this one have come true. This script counts that record. For every scored bet (stated odds before data,
an outcome decided by its pre-registered rule, `scored: true`) it tallies hits by program, by referee, by cost,
by where the bet came from (source) and by how deep in its program's map the bet sits (layer). Each count gets a
95% Wilson interval, because most cells hold a handful of bets. The file it writes, ledger/prior.md, is the one
thing every odds elicitation is handed (CONTEXT.md section 3 rule 14; operators/scout.md, operators/learn.md).

It also lists, per program, whether a closing review is due (operators/remap.md, "Closing a program"): a program
whose last three layers with settled bets hold no landed bet and no finding labelled partly new or new.

Inputs: ledger/bets.jsonl; map/*.json (layer depth and, where the bet row has none, source); programs/*/map/*.json
(source only). The root folder is the parent of this file's folder, or the first argument.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parent

LANDED = {"pass", "pass-unreplicated", "hit"}
UNSETTLED = {"", "open", "running", "withdrawn", "none"}
NOVEL = {"partly new", "new"}
SOURCE_WORD = {"literature": "literature", "l": "literature", "engine": "engine", "e": "engine",
               "human": "human", "p1": "P1-derived"}
SOURCE_ORDER = ["literature", "engine", "human", "P1-derived", "unrecorded"]
TIERS = ["free ($0)", "under $1", "$1 to under $5", "$5 or more", "unrecorded"]
REFEREE_WORD = {"model": "another model", "nature": "the quantum chip (nature)",
                "published-record": "the published record", "mathematics": "mathematics"}


def wilson(k, n, z=1.96):
    if n == 0:
        return None
    ph = k / n
    d = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / d
    h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def verdict(b):
    return str(b.get("verdict_after_audit") or b.get("verdict") or "").strip().lower()


def load_jsonl(p):
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def load_maps():
    """Engine maps (map/*.json) by program, and every program's own map JSON, for source lookups."""
    engine, own = {}, {}
    for f in sorted((ROOT / "map").glob("*.json")):
        m = json.loads(f.read_text())
        engine[m.get("program") or f.stem] = m
    for f in sorted((ROOT / "programs").glob("*/map/*.json")):
        try:
            m = json.loads(f.read_text())
        except json.JSONDecodeError:
            continue
        own.setdefault(f.parts[-3], []).append(m)
    return engine, own


def node_for(b, m):
    if not m:
        return None
    nodes = m.get("directions") or []
    for n in nodes:
        ids = [n["bets"]] if isinstance(n.get("bets"), str) else (n.get("bets") or [])
        if b["id"] in ids:
            return n
    for n in nodes:
        if str(n.get("id")) == str(b.get("direction")):
            return n
    return None


def depth(m, nid):
    """1 for a direction with no parent; one more for each parent step. A parent outside the map counts as one step."""
    nodes = {str(n.get("id")): n for n in (m.get("directions") or [])}
    d, seen, cur = 1, set(), str(nid)
    while True:
        p = nodes.get(cur, {}).get("parent")
        if p is None or str(p) in seen:
            return d
        seen.add(cur)
        d += 1
        if str(p) not in nodes:
            return d
        cur = str(p)


def layer_of(b, bets_by_id, engine_maps, _stack=()):
    m = engine_maps.get(b["program"])
    n = node_for(b, m)
    if n is not None:
        return depth(m, n.get("id")), "map"
    # Not on the engine map: a replication or re-bet sits one layer under the bet it repeats.
    for key in ("replication_of", "parent_bet", "rebet_of"):
        pid = b.get(key)
        if pid in bets_by_id and pid not in _stack:
            d, _ = layer_of(bets_by_id[pid], bets_by_id, engine_maps, _stack + (b["id"],))
            if d is not None:
                return d + (0 if key == "rebet_of" else 1), key
    return None, "none"


def source_of(b, engine_maps, own_maps):
    s = str(b.get("source") or "").strip().lower()
    if s in SOURCE_WORD:
        return SOURCE_WORD[s], "bet row"
    for m in [engine_maps.get(b["program"])] + own_maps.get(b["program"], []):
        n = node_for(b, m)
        if n is not None:
            s = str(n.get("source") or "").strip().lower()
            if s in SOURCE_WORD:
                return SOURCE_WORD[s], "map node"
    return "unrecorded", "none"


def dollars_of(b, bets_by_id):
    """Dollars of API the bet's decisive run cost: its own cost_usd, else (a bet decided by another bet's run) that
    run's cost_usd, else its pre-registered budget_usd. QPU seconds and laptop hours are not dollars."""
    if isinstance(b.get("cost_usd"), (int, float)):
        return float(b["cost_usd"]), "cost_usd"
    par = bets_by_id.get(b.get("parent"))
    if par and isinstance(par.get("cost_usd"), (int, float)):
        return float(par["cost_usd"]), f"cost_usd of {par['id']} (same run)"
    if isinstance(b.get("budget_usd"), (int, float)):
        return float(b["budget_usd"]), "budget_usd"
    return None, "none"


def tier(x):
    if x is None:
        return "unrecorded"
    if x == 0:
        return "free ($0)"
    if x < 1:
        return "under $1"
    if x < 5:
        return "$1 to under $5"
    return "$5 or more"


def fmt_ci(ci):
    return "—" if ci is None else f"[{ci[0]:.2f}, {ci[1]:.2f}]"


def table(rows, label, order=None, total=None):
    """rows: list of (key, outcome, engine_odds). Returns markdown lines and per-key stats."""
    keys = order or sorted({k for k, _, _ in rows}, key=str)
    out = [f"| {label} | scored bets | hits | hit rate | 95% interval | engine's mean odds | engine's Brier |",
           "|---|---|---|---|---|---|---|"]
    stats = {}
    for k in keys + ([total] if total else []):
        cell = [(o, p) for kk, o, p in rows if k == total or kk == k]
        n = len(cell)
        if n == 0:
            if order:
                out.append(f"| {k} | 0 | — | — | — | — | — |")
            continue
        h = sum(o for o, _ in cell)
        mp = sum(p for _, p in cell) / n
        br = sum((p - o) ** 2 for o, p in cell) / n
        ci = wilson(h, n)
        stats[k] = (n, h, ci, mp)
        name = f"**{k}**" if k == total else str(k)
        out.append(f"| {name} | {n} | {h} | {h / n:.2f} | {fmt_ci(ci)} | {mp:.2f} | {br:.3f} |")
    return out, stats


def closing_reviews(bets, bets_by_id, engine_maps):
    """Per program: the three deepest layers holding a settled bet, and whether any of them holds a landed bet or a
    finding labelled partly new or new. A closing review on the map (closing_review, with bets_reviewed) answers the
    flag until a settled bet it did not see appears in those layers."""
    out = []
    for prog in sorted({b["program"] for b in bets}):
        settled = [b for b in bets if b["program"] == prog and verdict(b) not in UNSETTLED]
        by_layer = {}
        for b in settled:
            d, _ = layer_of(b, bets_by_id, engine_maps)
            by_layer.setdefault(d if d is not None else 0, []).append(b)
        layers = sorted(k for k in by_layer if k)
        last = layers[-3:]
        inlast = [b for k in last for b in by_layer[k]]
        m = engine_maps.get(prog) or {}
        node_nov = {}
        for b in inlast:
            n = node_for(b, m)
            if n is not None and n.get("novelty"):
                node_nov[b["id"]] = str(n["novelty"]).strip().lower()
        nov = {b["id"]: str(b.get("novelty") or node_nov.get(b["id"]) or "").strip().lower() for b in inlast}
        landed = [b["id"] for b in inlast if verdict(b) in LANDED]
        novel = [i for i, v in nov.items() if v in NOVEL]
        unrec = [i for i, v in nov.items() if not v]
        rev = m.get("closing_review") or {}
        seen = set(rev.get("bets_reviewed") or [])
        unseen = [b["id"] for b in inlast if b["id"] not in seen]
        if len(last) < 3:
            due, why = "no", f"{len(layers)} layer{'s' if len(layers) != 1 else ''} with settled bets; the rule needs three"
        elif landed or novel:
            due, why = "no", "landed: " + (", ".join(landed) or "none") + "; partly new or new: " + (", ".join(novel) or "none")
        elif rev and not unseen:
            due, why = "no", f"reviewed {rev.get('date', '?')} ({rev.get('decision', '?')}); no settled bet since"
        else:
            due = "**yes**"
            why = "no landed bet and no partly-new or new finding in the last three layers"
            if rev:
                why += f"; settled since the {rev.get('date', '?')} review: {', '.join(unseen)}"
        out.append((prog, layers, last, inlast, unrec, due, why))
    return out


def main():
    bets = load_jsonl(HERE / "bets.jsonl")
    bets_by_id = {b["id"]: b for b in bets}
    engine_maps, own_maps = load_maps()
    scored = [b for b in bets if b.get("scored") and b.get("outcome") in (0, 1) and b.get("engine_odds") is not None]
    n, hits = len(scored), sum(b["outcome"] for b in scored)
    ci = wilson(hits, n)
    rate = hits / n if n else None
    meta = {}
    for b in scored:
        d, how_d = layer_of(b, bets_by_id, engine_maps)
        s, how_s = source_of(b, engine_maps, own_maps)
        x, how_x = dollars_of(b, bets_by_id)
        meta[b["id"]] = dict(layer=d, how_layer=how_d, source=s, how_source=how_s, dollars=x, how_dollars=how_x,
                             tier=tier(x), referee=b.get("referee") or "model")

    def rows(key):
        return [(key(b), b["outcome"], b["engine_odds"]) for b in scored]

    L = []
    w = L.append
    w("# The prior: the engine's own record, counted")
    w("")
    w("Generated by `python3 ledger/prior.py` from `ledger/bets.jsonl` and the maps (`map/*.json`). "
      "Do not edit by hand; edit the ledger and rerun. `python3 reproduce.py` checks this file byte for byte.")
    w("")
    w("## In plain English")
    w("")
    w(f"Before a new bet, the engine states its odds starting from this page: how often its own past bets came true. "
      f"So far **{hits} of {n} scored bets came true ({rate:.2f}, 95% interval {fmt_ci(ci)})**. "
      "The tables below split that record five ways: by program, by what decided the outcome (the referee), "
      "by how many dollars the test cost, by where the bet came from, and by how deep in its program's map it sat. "
      "Each row's interval is wide because each row holds few bets; a row with fewer than five bets says almost nothing.")
    w("")
    w("**How an odds elicitation uses this page** (CONTEXT.md §3 rule 14; `operators/scout.md`, Step 4). "
      "A fresh context is handed this file and the bet's own description (its design, models, cost, pass rule, "
      "and which row it falls in on each table), and nothing about the bet's history: no earlier odds for it, "
      "no earlier bet on its direction or their outcomes, no human odds. It writes three things:")
    w("")
    w(f"1. **prior**: the hit rate of all scored bets, as printed here ({rate:.2f}), with this file's commit;")
    w("2. **adjustment**: a signed number added to the prior (the result, kept between 0.01 and 0.99, is the engine's odds);")
    w("3. **reason**: one line naming the rows below, or the feature of the design, that justify the adjustment.")
    w("")
    w("The ledger stores all three (`odds_prior`, `odds_adjustment`, `odds_reason`), and `ledger/brier.md` scores the "
      "prior alone against the adjusted odds on every bet that carries them. If the adjusted odds score no better, "
      "the adjustments are not adding judgment, and that page says so.")
    w("")

    w("## By program")
    w("")
    w("Which research program the bet belongs to. Programs differ in question, referee and design habits, "
      "so this is the first place to look for a reason to move off the prior.")
    w("")
    progs = sorted({b["program"] for b in bets})
    t, st = table(rows(lambda b: b["program"]), "program", order=progs, total="all programs")
    L.extend(t)
    w("")
    zero = [p for p in progs if p in st and st[p][1] == 0]
    unsc = [p for p in progs if p not in st]
    w("Programs with scored bets and no hit: " + (", ".join(f"{p} (0 of {st[p][0]})" for p in zero) or "none") + "."
      + (" Programs with no scored bet yet: " + ", ".join(unsc) + "." if unsc else ""))
    w("")

    w("## By referee")
    w("")
    w("What decided whether the bet came true: another model's output graded by a pre-registered rule, the quantum "
      "chip, or the published record. An engine that is calibrated only when a model grades it has borrowed its "
      "judgment from its grader (ARCHITECTURE.md, referee_test).")
    w("")
    refs = sorted({m["referee"] for m in meta.values()})
    t, st = table([(meta[b["id"]]["referee"], b["outcome"], b["engine_odds"]) for b in scored], "referee", order=refs)
    L.extend(t)
    w("")
    w("; ".join(f"{r} means {REFEREE_WORD.get(r, r)}" for r in refs) + ".")
    w("")

    w("## By cost tier")
    w("")
    w("Dollars of API the decisive run cost: the bet's `cost_usd`; for a bet decided by another bet's run, that run's "
      "`cost_usd`; otherwise its pre-registered `budget_usd`. Chip seconds and laptop hours are not dollars, so the "
      "chip bets sit in the free row. Whether cheap tests fail more often is the question this table can start to answer.")
    w("")
    t, st = table([(meta[b["id"]]["tier"], b["outcome"], b["engine_odds"]) for b in scored], "cost tier", order=TIERS[:4])
    L.extend(t)
    w("")
    borrowed = [b["id"] for b in scored if meta[b["id"]]["how_dollars"].startswith("cost_usd of")]
    if borrowed:
        w("Priced from the run that decided them: " + ", ".join(
            f"{i} ({meta[i]['how_dollars'].replace('cost_usd of ', '').replace(' (same run)', '')}'s run)" for i in borrowed) + ".")
        w("")

    w("## By source")
    w("")
    w("Where the bet came from: a paper's own next steps (literature), the engine's own idea (engine), a logged steer "
      "from Sean (human), or a follow-up from program 1's results (P1-derived). This is proposal.md's Q5. "
      "The bet row's `source` is used; where it has none, the map node's; where neither says, the bet is unrecorded.")
    w("")
    t, st = table([(meta[b["id"]]["source"], b["outcome"], b["engine_odds"]) for b in scored], "source", order=SOURCE_ORDER)
    L.extend(t)
    w("")
    if "unrecorded" in st:
        unr = [b["id"] for b in scored if meta[b["id"]]["source"] == "unrecorded"]
        w(f"{len(unr)} scored bets have no recorded source ({', '.join(unr)}); they are counted, not guessed.")
        w("")

    w("## By layer depth")
    w("")
    w("How many steps from its program's first map the bet's direction sits: layer 1 is a direction the scout mapped "
      "with no parent; each follow-up of a follow-up adds one. A bet missing from the map but repeating another bet "
      "sits one layer under it. Whether later layers, built on earlier results, come true more often is what this "
      "table watches.")
    w("")
    lay = sorted({m["layer"] for m in meta.values() if m["layer"] is not None})
    t, st = table([(f"layer {meta[b['id']]['layer']}" if meta[b["id"]]["layer"] else "not on a map", b["outcome"], b["engine_odds"])
                   for b in scored], "layer", order=[f"layer {d}" for d in lay])
    L.extend(t)
    w("")
    fb = [b["id"] for b in scored if meta[b["id"]]["how_layer"] not in ("map", "none")]
    if fb:
        w("Placed by the bet they repeat (not on the map themselves): " + ", ".join(fb) + ".")
        w("")

    w("## Closing reviews due")
    w("")
    w("A program whose last three layers with settled bets hold no landed bet and no finding labelled partly new or "
      "new is due a closing review by a fresh session (`operators/remap.md`, \"Closing a program\"). The review writes "
      "a diagnosis and either marks the seed question closed on the map or keeps it open with a stated reason. "
      "Settled means a verdict other than open or withdrawn; landed means pass, pass-unreplicated or hit; novelty is the "
      "bet's `novelty` field (rule 13), else its map node's.")
    w("")
    w("| program | layers with settled bets | last three | settled bets in them | novelty not recorded | due | why |")
    w("|---|---|---|---|---|---|---|")
    for prog, layers, last, inlast, unrec, due, why in closing_reviews(bets, bets_by_id, engine_maps):
        w(f"| {prog} | {', '.join(map(str, layers)) or '—'} | {', '.join(map(str, last)) or '—'} | {len(inlast)} | "
          f"{len(unrec)} | {due} | {why} |")
    w("")

    w("## What is not counted")
    w("")
    notsc = [b for b in bets if b not in scored]
    w(f"{len(notsc)} of the {len(bets)} bets in the ledger are not in these tables: they are open, withdrawn before data, "
      "untestable, undetermined after audit, or stated no odds (`ledger/brier.md`, \"What is not scored, and why\").")
    (HERE / "prior.md").write_text("\n".join(L) + "\n")
    print(f"prior {rate:.2f} ({hits}/{n}, 95% {fmt_ci(ci)}); closing reviews due: "
          + (", ".join(p for p, *_, due, _w in closing_reviews(bets, bets_by_id, engine_maps) if due != "no") or "none"))


if __name__ == "__main__":
    main()
