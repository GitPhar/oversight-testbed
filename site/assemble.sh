#!/usr/bin/env bash
# Lays out the static site for GitHub Pages. Copies files only: there is no build step.
#
#   site/assemble.sh <out-dir> [<entangled-mind-dir>] [<nature-graded-dir>]     (defaults: programs/entangled-mind, programs/nature-graded)
#
# Result:
#   <out>/                       the pages in site/
#   <out>/data/ledger/           the engine's ledger/   (bets.jsonl, steers.jsonl, brier.md, audits/)
#   <out>/data/map/              the engine's map/      (one JSON per program)
#   <out>/data/engine/           README.md, proposal.md and CONTEXT.md (front page; the instruments page reads the budget line)
#   <out>/data/engine/paper/     the engine's figures, paper/*.svg (the home page's architecture diagram), and paper/plain-words.md
#   <out>/data/engine/application/one-page-plain.md   (Papers page)
#   <out>/data/programs/entangled-mind/paper/   that repo's paper/ folder (papers, record, figures)
#   <out>/data/programs/entangled-mind/audits/SUMMARY.md, results/ibm-usage.json, results/api-usage.md  (instruments page)
#   <out>/data/programs/nature-graded/map/      program 3's map JSON and odds-elicitation README, if a checkout is given
#   <out>/data/manifest.json     what was copied, because Pages cannot list a folder
#
# Local preview:  site/assemble.sh /tmp/site && python3 -m http.server -d /tmp/site 8000
# LEDGER_DIR and MAP_DIR override where ledger/ and map/ are read from (for previewing another branch's data).
set -euo pipefail

out="${1:?usage: site/assemble.sh <out-dir> [<entangled-mind-dir>] [<nature-graded-dir>]}"
root="$(cd "$(dirname "$0")/.." && pwd)"
em="${2:-$root/programs/entangled-mind}"
ng="${3:-$root/programs/nature-graded}"
ledger="${LEDGER_DIR:-$root/ledger}"
map="${MAP_DIR:-$root/map}"

mkdir -p "$out/data/ledger" "$out/data/map" "$out/data/engine" "$out/data/programs/entangled-mind/paper"
cp -R "$root/site/." "$out/"
rm -f "$out/assemble.sh"
[ -d "$ledger" ] && cp -RL "$ledger/." "$out/data/ledger/"   # -L: ledger/audits/em-*.md are links into programs/entangled-mind/audits/
[ -d "$map" ] && cp -R "$map/." "$out/data/map/"
cp "$root/README.md" "$root/proposal.md" "$root/CONTEXT.md" "$out/data/engine/"
# The engine's figures (the home page shows the architecture diagram).
mkdir -p "$out/data/engine/paper" && for f in "$root"/paper/*.svg; do [ -f "$f" ] && cp "$f" "$out/data/engine/paper/"; done
# The plain-words pages, listed first on the Papers page.
[ -f "$root/paper/plain-words.md" ] && cp "$root/paper/plain-words.md" "$out/data/engine/paper/"
mkdir -p "$out/data/engine/application" && { [ -f "$root/application/one-page-plain.md" ] && cp "$root/application/one-page-plain.md" "$out/data/engine/application/"; true; }
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
    "ledger": sorted(f for f in os.listdir(d("ledger")) if os.path.isfile(d("ledger", f))) if os.path.isdir(d("ledger")) else [],
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
