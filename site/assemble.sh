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
#   <out>/data/numbers.json      every ledger number, from site/numbers.py (the home page's score and findings read it)
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
rm -f "$out/assemble.sh" "$out/numbers.py"
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

# The ledger's numbers, through the same reader the front-page documents use, so no page types one.
python3 "$root/site/numbers.py" --json --ledger "$ledger" > "$out/data/numbers.json"

python3 - "$out" "$em" "$root" "$ng" <<'PY'
import json, os, re, subprocess, sys, datetime
out, em, root = sys.argv[1], sys.argv[2], sys.argv[3]
d = lambda *p: os.path.join(out, "data", *p)

# A program whose map lives only in its own folder, in its own format (programs/<name>/map/<name>.json, e.g.
# program 4), is converted here into the site's map format, so it gets a tab on the map without a hand copy that
# could go stale. A file of the same name in the engine's map/ wins. Verdicts still come from ledger/bets.jsonl.
def convert_program_map(name):
    src = os.path.join(root, "programs", name, "map", name + ".json")
    if not os.path.isfile(src) or os.path.exists(d("map", name + ".json")):
        return
    p = json.load(open(src))
    if p.get("title") or not p.get("directions"):
        return
    readme = open(os.path.join(root, "programs", name, "README.md")).read() if os.path.isfile(os.path.join(root, "programs", name, "README.md")) else ""
    n = re.search(r"\bProgram (\d+) of\b", readme)
    bet_ids = set()
    bets_path = d("ledger", "bets.jsonl")
    if os.path.isfile(bets_path):
        for line in open(bets_path):
            line = line.strip()
            if line:
                try: bet_ids.add(json.loads(line).get("id"))
                except ValueError: pass
    when = lambda s: re.sub(r"^(\d{4}-\d\d-\d\d)[ T](\d\d:\d\d).*$", r"\1T\2", str(s or ""))
    dirs = []
    for x in p["directions"]:
        short = re.sub(r"\s*\([^)]*\)\s*$", "", x.get("title", "")).strip()
        dirs.append({k: v for k, v in {
            "id": x["id"], "parent": x.get("parent"), "title": x.get("title"), "short": short if short != x.get("title") else None,
            "status": x.get("status"), "parked": x.get("status") == "parked" or None, "opened": when(x.get("engine_odds_at")),
            "engine_odds": x.get("engine_odds"), "engine_odds_first": x.get("engine_odds_first"), "cost": x.get("cost"),
            "referee": x.get("referee"), "odds_event": x.get("odds_event"), "diagnosis": x.get("diagnosis"),
            "bets": [x["id"]] if x["id"] in bet_ids else None,
        }.items() if v is not None})
    opened = sorted(x["opened"] for x in dirs if x.get("opened"))
    conv = {
        "program": p.get("program", name),
        "title": f"Program {n.group(1)}: {name.replace('-', ' ').title()}" if n else name,
        "seed_question": p.get("seed_question", ""),
        "seed_date": opened[0] if opened else p.get("scouted", ""),
        "note": f"Converted by site/assemble.sh from programs/{name}/map/{name}.json at deploy; do not edit this copy.",
        "directions": dirs,
    }
    json.dump(conv, open(d("map", name + ".json"), "w"), indent=1)

for name in sorted(os.listdir(os.path.join(root, "programs"))) if os.path.isdir(os.path.join(root, "programs")) else []:
    convert_program_map(name)

# When each commit the ledger names was made, America/Denver wall-clock, so the replay and the record can place a
# bet whose row has no result_time (ss-b5 to ss-b7, ng-p3-5c) or that was withdrawn on a design review. Read from
# git, not typed. The deploy checks out full history for this (pages.yml, fetch-depth 0); a shallow checkout
# finds no hashes and the pages say "landing time not recorded" instead.
def commit_times():
    hashes = set()
    def walk(v):
        if isinstance(v, dict):
            for k, x in v.items():
                if k.endswith("commit") and isinstance(x, str) and re.fullmatch(r"[0-9a-f]{7,40}", x):
                    hashes.add(x)
                walk(x)
        elif isinstance(v, list):
            for x in v: walk(x)
    bets_path = d("ledger", "bets.jsonl")
    if os.path.isfile(bets_path):
        for line in open(bets_path):
            try: walk(json.loads(line))
            except ValueError: pass
    env = dict(os.environ, TZ="America/Denver")
    out = {}
    for h in sorted(hashes):
        try:
            t = subprocess.check_output(["git", "-C", root, "show", "-s", "--format=%cd", "--date=format-local:%Y-%m-%dT%H:%M", h + "^{commit}"],
                                        text=True, env=env, stderr=subprocess.DEVNULL).strip()
            if t: out[h] = t
        except Exception:
            pass
    json.dump(out, open(d("commit-times.json"), "w"), indent=0, sort_keys=True)
    return len(out), len(hashes)
ct = commit_times()

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
print(f"assembled {out}: {len(m['map'])} map file(s), {len(m['papers'])} paper file(s), {len(m['audits'])} audit(s), {ct[0]} of {ct[1]} ledger commit times")
PY
