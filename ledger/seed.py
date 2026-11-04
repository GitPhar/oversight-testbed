"""Derive a bet's seed from a beacon pulse (operators/hardware.md). No network, no keys.

    python3 ledger/seed.py <randomness-hex> <bet-id> [--purpose split]

seed = first 8 bytes of SHA-256(randomness bytes || bet-id), unsigned big-endian.
With --purpose, SHA-256(randomness || bet-id || ":" || purpose), so one pulse gives
independent sub-seeds per draw (split, items, order). seed32 is seed mod 2**32 for
tools that only take 32-bit seeds; state in the pre-registration which one is used.
"""
import argparse
import hashlib


def derive(randomness_hex, bet_id, purpose=None):
    data = bytes.fromhex(randomness_hex.strip().removeprefix("0x")) + bet_id.encode()
    if purpose:
        data += b":" + purpose.encode()
    return int.from_bytes(hashlib.sha256(data).digest()[:8], "big")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("randomness_hex")
    ap.add_argument("bet_id")
    ap.add_argument("--purpose")
    a = ap.parse_args()
    s = derive(a.randomness_hex, a.bet_id, a.purpose)
    print(f"seed {s}")
    print(f"seed32 {s % 2 ** 32}")


if __name__ == "__main__":
    main()
