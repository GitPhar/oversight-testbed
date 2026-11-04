#!/usr/bin/env bash
# Lays out the static site for GitHub Pages. Copies files only: there is no build step.
#
#   site/assemble.sh <out-dir> <entangled-mind-checkout> [<nature-graded-checkout>]
#
# Result:
#   <out>/                       the pages in site/
#   <out>/data/ledger/           the engine's ledger/   (bets.jsonl, steers.jsonl, brier.md, audits/)
#   <out>/data/map/              the engine's map/      (one JSON per program)
#   <out>/data/engine/           README.md, proposal.md and CONTEXT.md (front page; the instruments page reads the budget line)
#   <out>/data/programs/entangled-mind/paper/   that repo's paper/ folder (papers, record, figures)
#   <out>/data/programs/entangled-mind/audits/SUMMARY.md, results/ibm-usage.json, results/api-usage.md  (instruments page)
#   <out>/data/programs/nature-graded/map/      program 3's map JSON and odds-elicitation README, if a checkout is given
#   <out>/data/manifest.json     what was copied, because Pages cannot list a folder
#
# Local preview:  site/assemble.sh /tmp/site ../entangled-mind && python3 -m http.server -d /tmp/site 8000
# LEDGER_DIR and MAP_DIR override where ledger/ and map/ are read from (for previewing another branch's data).
set -euo pipefail

out="${1:?usage: site/assemble.sh <out-dir> <entangled-mind-checkout>}"
em="${2:?usage: site/assemble.sh <out-dir> <entangled-mind-checkout>}"
ng="${3:-}"
root="$(cd "$(dirname "$0")/.." && pwd)"
ledger="${LEDGER_DIR:-$root/ledger}"
map="${MAP_DIR:-$root/map}"

mkdir -p "$out/data/ledger" "$out/data/map" "$out/data/engine" "$out/data/programs/entangled-mind/paper"
cp -R "$root/site/." "$out/"
rm -f "$out/assemble.sh"
[ -d "$ledger" ] && cp -R "$ledger/." "$out/data/ledger/"
[ -d "$map" ] && cp -R "$map/." "$out/data/map/"
cp "$root/README.md" "$root/proposal.md" "$root/CONTEXT.md" "$out/data/engine/"
[ -d "$em/paper" ] && cp -R "$em/paper/." "$out/data/programs/entangled-mind/paper/"
# The instruments page: program 1's audit summary and its two usage ledgers (API dollars, QPU seconds).
emd="$out/data/programs/entangled-mind"
mkdir -p "$emd/audits" "$emd/results"
[ -f "$em/audits/SUMMARY.md" ] && cp "$em/audits/SUMMARY.md" "$emd/audits/"
for f in ibm-usage.json api-usage.md; do [ -f "$em/results/$f" ] && cp "$em/results/$f" "$emd/results/"; done
# Program 3 (nature-graded): the chip-graded side of the referee comparison. Optional.
if [ -n "$ng" ] && [ -f "$ng/map/program-3-map.json" ]; then
  mkdir -p "$out/data/programs/nature-graded/map/odds-elicitation"
  cp "$ng/map/program-3-map.json" "$out/data/programs/nature-graded/map/"
  [ -f "$ng/map/odds-elicitation/README.md" ] && cp "$ng/map/odds-elicitation/README.md" "$out/data/programs/nature-graded/map/odds-elicitation/"
fi

python3 - "$out" "$em" "$root" "$ng" <<'PY'
import json, os, subprocess, sys, datetime
out, em, root = sys.argv[1], sys.argv[2], sys.argv[3]
d = lambda *p: os.path.join(out, "data", *p)
ls = lambda p, ext: sorted(f for f in os.listdir(p) if f.endswith(ext)) if os.path.isdir(p) else []
def head(repo):
    try:
        return subprocess.check_output(["git", "-C", repo, "log", "-1", "--format=%h %ad", "--date=format:%Y-%m-%d %H:%M"], text=True).strip()
    except Exception:
        return None
m = {
    "map": ls(d("map"), ".json"),
    "papers": ls(d("programs", "entangled-mind", "paper"), ".md"),
    "audits": ls(d("ledger", "audits"), ".md"),
    "assembled": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    "engine_commit": head(root),
    "entangled_mind_commit": head(em),
    "nature_graded": os.path.isfile(d("programs", "nature-graded", "map", "program-3-map.json")),
    "nature_graded_commit": head(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4] else None,
}
json.dump(m, open(d("manifest.json"), "w"), indent=1)
print(f"assembled {out}: {len(m['map'])} map file(s), {len(m['papers'])} paper file(s), {len(m['audits'])} audit(s)")
PY
