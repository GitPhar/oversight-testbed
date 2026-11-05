"""Unit test for ss-b12's binding recognition rule (score_f4.recognised2; D57, design review ss-b12 F1(d)).

    python3 scoring/test_recog_f4.py     # exits 1 on any wrong label; prints round 2's and round 1's flag counts
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_f4 as F  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SYN = [  # (text, expected) from the design review's D2 section, plus the frozen rule's own phrases
    ("Marks et al. (2024) showed that probes generalise across datasets.", True),
    ("This is the SAEBench study (Karvonen et al. 2025), which found lower scores.", True),
    ("This matches the well-known Anthropic result on sleeper agents.", True),
    ("I recall that the authors found higher fidelity.", True),
    ("I remember this abstract reporting a faster decay.", True),
    ("I'm familiar with this paper; it reported stronger effects.", True),
    ("I do not recognize this study, so I go by plausibility.", False),
    ("I'm not familiar with this paper.", False),
    ("I cannot answer from memory; the wording suggests higher.", False),
    ("I've seen the phrase 'higher fidelity' in many abstracts.", False),
    ("This study was published in a quantum venue, so gains are typical.", False),
    ("This is a known result from prior work on judges.", False),
    ("The effect was recalled as fragile in the discussion.", False),
    ("Papers usually report that their method improves on the baseline.", False),
    ("I can't actually recognise this paper.", False),
    ("Abstracts in this field usually report improvements.", False),
]


def main():
    bad = []
    for t, want in SYN:
        if F.recognised2(t) != want:
            bad.append((t, want))
    rows = {(json.loads(l)["id"], json.loads(l)["kind"]): json.loads(l) for l in (ROOT / "bettor" / "r2-bets.jsonl").read_text().splitlines() if l.strip()}
    items = {json.loads(l)["id"]: json.loads(l) for l in (ROOT / "items" / "r2" / "items.jsonl").read_text().splitlines() if l.strip()}
    for key, want in ((("r2-052", "primary"), True), (("r2-052", "order-check"), True), (("r2-018", "primary"), True),
                      (("r2-016", "order-check"), False)):
        r = rows[key]
        it = items[key[0]]
        itext = " ".join(str(it.get(k, "")) for k in ("question", "option_a", "option_b"))
        if F.recognised2(r["rationale"], itext) != want:
            bad.append((f"{key} archive row", want))
    prim = [r for (i, k), r in rows.items() if k == "primary"]
    n2 = sum(F.recognised2(r["rationale"], " ".join(str(items[r["id"]].get(k, "")) for k in ("question", "option_a", "option_b"))) for r in prim)
    n2f = sum(bool(F.RECOG.search(r["rationale"] or "")) for r in prim)
    r1 = {json.loads(l)["id"]: json.loads(l) for l in (ROOT / "items" / "items.jsonl").read_text().splitlines() if l.strip()}
    b1 = [json.loads(l) for l in (ROOT / "bettor" / "bets.jsonl").read_text().splitlines() if l.strip()]
    pre1 = [b for b in b1 if b["kind"] == "primary" and r1[b["id"]]["side"] == "pre"]
    n1 = sum(F.recognised2(b["rationale"], " ".join(str(r1[b["id"]].get(k, "")) for k in ("question", "option_a", "option_b"))) for b in pre1)
    n1f = sum(bool(F.RECOG.search(b["rationale"] or "")) for b in pre1)
    print(f"round 2 primary rationales flagged: binding rule {n2} of {len(prim)}, frozen rule {n2f}")
    print(f"round 1 pre-cutoff rationales flagged (counts only): binding rule {n1} of {len(pre1)}, frozen rule {n1f} (round-3 audit's regex: 16)")
    if bad:
        print("WRONG:", bad)
        sys.exit(1)
    print(f"all {len(SYN) + 4} labels right")


if __name__ == "__main__":
    main()
