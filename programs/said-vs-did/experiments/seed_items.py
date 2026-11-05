"""Seed commit for wave 1 (operators/hardware.md): turn sv-b1's beacon pulse into the item draw. No network, no keys.

    python3 seed_items.py <pulse.json from curby_seed.mjs rng>

Writes data/sv-wave1-items.json: the beacon block, the derived seed (ledger/seed.py, purpose "items"), seed32 = seed mod 2^32,
and the shuffled order of the 300 sorted hard-pool ids (random.Random(seed32).shuffle). Sonnet uses the first 150, Opus
the first 80. Nothing else is drawn."""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[2] / "ledger"))
import seed as ledger_seed  # noqa: E402
import svd_common as C  # noqa: E402
import svd_wave1 as W  # noqa: E402

pulse = json.loads(Path(sys.argv[1]).read_text())
s = ledger_seed.derive(pulse["randomness"], "sv-b1", "items")
order = W.draw_order(s % 2 ** 32)
C.DATA.mkdir(exist_ok=True)
W.SEED_FILE.write_text(json.dumps({"bet": "sv-b1", "purpose": "items", "beacon": pulse, "seed": s, "seed32": s % 2 ** 32,
                                   "order": order, "sonnet": order[:150], "opus": order[:80]}, indent=1))
print(json.dumps({"seed": s, "seed32": s % 2 ** 32, "first5": order[:5]}))
