"""Fetch the first CURBy-RNG pulse after a pre-registration commit and derive the bet's seeds.

    python3 experiments/seed_commit.py <bet-id> <prereg-commit> <purpose> [<purpose> ...]

Writes data/<bet-id>-seed.json and prints the filled §2 beacon line. Uses experiments/curby_seed.mjs
(@buff-beacon-project/curby-client@1.2.0, path in $CURBY_CLIENT) and oversight-testbed/ledger/seed.py.
"""
import json
import os
import subprocess
import sys
import datetime as dt
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
SEED_PY = "/Users/seanpharris/oversight-testbed/ledger/seed.py"
DEN = ZoneInfo("America/Denver")


def denver(utc_iso):
    return dt.datetime.fromisoformat(utc_iso.replace("Z", "+00:00")).astimezone(DEN).strftime("%Y-%m-%d %H:%M:%S")


def main():
    bet, commit, purposes = sys.argv[1], sys.argv[2], sys.argv[3:]
    commit_time = subprocess.check_output(["git", "-C", str(ROOT), "log", "-1", "--format=%aI", commit], text=True).strip()
    chk = json.loads(subprocess.check_output(["node", str(ROOT / "experiments/curby_seed.mjs"), "check"], text=True))
    import time
    for _ in range(36):   # the next pulse is at most a minute away; give up after 3 minutes
        r = subprocess.run(["node", str(ROOT / "experiments/curby_seed.mjs"), "rng", commit_time], text=True, capture_output=True)
        if r.returncode == 0:
            break
        time.sleep(5)
    else:
        raise SystemExit("no CURBy-RNG pulse after the commit within 3 minutes: " + r.stderr)
    rng = json.loads(r.stdout)
    out = dict(rng, seed_source="curby-rng", bet_id=bet, prereg_commit=commit, prereg_time=commit_time,
               pulse_time_denver=denver(rng["pulse_time_utc"]), previous_time_denver=denver(rng["previous_time_utc"]),
               curbyq_latest_completed_round=chk["latest_completed_round"],
               curbyq_round_time_denver=denver(chk["result_pulse_time_utc"]))
    for p in purposes:
        lines = subprocess.check_output(["python3", SEED_PY, rng["randomness"], bet, "--purpose", p], text=True).split()
        out[f"seed_{p}"], out[f"seed32_{p}"] = int(lines[1]), int(lines[3])
    out["code"] = (f"experiments/curby_seed.mjs rng {commit_time}; then oversight-testbed/ledger/seed.py "
                   f"<randomness> {bet} --purpose <p> for p in {purposes}")
    (ROOT / "data" / f"{bet.removeprefix('ng-')}-seed.json").write_text(json.dumps(out, indent=1))
    seeds = " · ".join(f"`seed ({p}):` {out['seed_' + p]} · `seed32 ({p}):` {out['seed32_' + p]}" for p in purposes)
    print(f"  `chain:` CURBy-RNG · `pulse index:` {rng['pulse_index']} · `pulse_time:` {out['pulse_time_denver']} America/Denver"
          f" · `previous pulse:` index {rng['previous_index']} at {out['previous_time_denver']} (before the commit at "
          f"{denver(dt.datetime.fromisoformat(commit_time).astimezone(dt.timezone.utc).isoformat())})"
          f" · `randomness:` {rng['randomness']} · `client:` {rng['client']} via `experiments/curby_seed.mjs`"
          f" · `certificate_verified:` false · {seeds}. Record: `data/{bet.removeprefix('ng-')}-seed.json`.")


if __name__ == "__main__":
    os.environ.setdefault("CURBY_CLIENT", "/private/tmp/claude-501/-Users-seanpharris-nature-graded/"
                          "7c25cca6-08e1-4553-93b5-cba221e5441d/scratchpad/curby/node_modules/@buff-beacon-project/curby-client")
    main()
