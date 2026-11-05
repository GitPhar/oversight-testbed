"""Sean's 20-item form at direction level (pre-registration §6). Five post-cutoff items per field, drawn with the
beacon sub-seed 'human-form'; options in the same order the bettor saw them. No engine odds, no answers, no ranking.

    python3 human/make_form.py            -> human/form.md
    python3 human/make_form.py --score    -> reads human/answers.md (Sean's filled copy), writes human/score.md
"""
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bettor"))
from bettor import draws  # noqa: E402  (imports common; no call is made)

FIELDS = ("model-psychology", "interpretability", "scalable-oversight", "quantum-devices")


def pick():
    items = sorted((json.loads(l) for l in (ROOT / "items" / "items.jsonl").read_text().splitlines() if l.strip()),
                   key=lambda x: x["id"])
    seeds = json.loads((ROOT / "bettor" / "seed.json").read_text())["seeds"]
    swap, _ = draws(items, seeds)
    rng = random.Random(seeds["human-form"])
    chosen = []
    for f in FIELDS:
        pool = [it["id"] for it in items if it["side"] == "post" and it["field"] == f]
        chosen += rng.sample(pool, 5)
    order = rng.sample(chosen, len(chosen))  # shuffled across fields
    byid = {it["id"]: it for it in items}
    return [(byid[i], swap[i]) for i in order]


def form():
    L = ["# Your 20 calls: which way did the finding go?", "",
         "**Fill this in before you open `results/`, `bettor/` or `items/items.jsonl`.** Those show the answers and the engine's odds.", "",
         "Each item is a real study posted to arXiv between July and November 2026, after the engine's model was trained, so it cannot have read them. "
         "Exactly one of the two options is what the paper reported. For each one, write **1 or 2**, and if you like, **how sure** "
         "from 50 (a coin flip) to 100 (certain). If you leave 'how sure' blank it is scored as 75.", "",
         "Take about a minute each; go with your gut. No session asks you for these in a terminal (engine CONTEXT.md §3 rule 11): "
         "your calls count only once they are committed to `ledger/human-odds.jsonl` from a cockpit download. "
         "If they are not there when the bettor's results are scored, the program proceeds marked 'no human odds'.", ""]
    for n, (it, b_first) in enumerate(pick(), 1):
        o1, o2 = (it["option_b"], it["option_a"]) if b_first else (it["option_a"], it["option_b"])
        L += [f"## H{n:02d} · {it['field']}", "", f"**{it['question']}**", "", f"How it was tested: {it['methods']}", "",
              f"1. {o1}", f"2. {o2}", "", f"Your call (1 or 2): ____   How sure (50–100): ____", "",
              f"<sub>{it['id']}</sub>", ""]
    (ROOT / "human" / "form.md").write_text("\n".join(L))
    print("wrote human/form.md")


def score():
    picked = pick()
    text = (ROOT / "human" / "answers.md").read_text()
    rows, bets = [], {b["id"]: b for b in (json.loads(l) for l in (ROOT / "bettor" / "bets.jsonl").read_text().splitlines())
                      if b["kind"] == "primary"}
    for n, (it, b_first) in enumerate(picked, 1):
        # either the filled form (section '## Hnn', 'Your call (1 or 2): x', 'How sure (50–100): y') or one line 'Hnn: x, y'
        sec = re.search(rf"## H{n:02d}\b(.*?)(?=\n## H\d|\Z)", text, re.S)
        m = sec and re.search(r"Your call \(1 or 2\):\s*([12])\b", sec.group(1))
        s = sec and re.search(r"How sure \(50.100\):\s*(\d{2,3})", sec.group(1))
        if not m:
            m = re.search(rf"^\s*H{n:02d}\s*[:\-]\s*([12])\b(?:\s*[,;]?\s*(\d{{2,3}}))?", text, re.M)
            s = m if (m and m.group(2)) else None
        if not m:
            continue
        call, sure = int(m.group(1)), int(s.group(s.lastindex) if s else 75)
        shown_true = 1 if (("b" if b_first else "a") == it["true_option"]) else 2
        p_true = sure / 100 if call == shown_true else 1 - sure / 100
        b = bets[it["id"]]
        bp = b["p_option_1"] / 100
        bettor_p_true = bp if b["option_1_is"] == it["true_option"] else 1 - bp
        rows.append({"h": f"H{n:02d}", "id": it["id"], "field": it["field"], "sean_right": call == shown_true,
                     "sean_p_true": p_true, "bettor_right": bettor_p_true > 0.5, "bettor_p_true": bettor_p_true})
    br = lambda k: sum((1 - r[k]) ** 2 for r in rows) / len(rows)  # noqa: E731
    out = [f"# Sean vs the bettor on the same {len(rows)} items", "",
           f"Direction right: Sean {sum(r['sean_right'] for r in rows)}/{len(rows)}, bettor {sum(r['bettor_right'] for r in rows)}/{len(rows)}.",
           f"Brier: Sean {br('sean_p_true'):.3f}, bettor {br('bettor_p_true'):.3f} (0.25 = coin).", "",
           "| item | field | Sean right | bettor right |", "|---|---|---|---|"]
    out += [f"| {r['h']} ({r['id']}) | {r['field']} | {'yes' if r['sean_right'] else 'no'} | {'yes' if r['bettor_right'] else 'no'} |" for r in rows]
    (ROOT / "human" / "score.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    score() if "--score" in sys.argv else form()
