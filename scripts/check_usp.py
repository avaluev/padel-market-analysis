#!/usr/bin/env python3
"""Standalone USP check (also covered inside check_canonical_brief.py)."""

import argparse
import json
import pathlib
import re
import sys

BANNED = (
    r"\bai[-\s]?powered\b",
    r"\bdata[-\s]?driven\b",
    r"\bplatform\b",
    r"\bnext[-\s]?generation\b",
    r"\brevolutionary\b",
    r"\bdisruptive\b",
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    a = ap.parse_args()
    p = pathlib.Path(f"evidence/{a.run_id}/canonical_brief.json")
    if not p.exists():
        print("[check_usp] no brief yet; skipping")
        return 0
    d = json.loads(p.read_text(encoding="utf-8"))
    usp = (d.get("usp") or "").strip()
    if not usp:
        print("[check_usp] FAIL: usp missing", file=sys.stderr)
        return 1
    n = len(re.findall(r"\S+", usp))
    if n > 30:
        print(f"[check_usp] FAIL: {n} words (max 30)", file=sys.stderr)
        return 1
    for pat in BANNED:
        if re.search(pat, usp, re.IGNORECASE):
            print(f"[check_usp] FAIL: banned token /{pat}/", file=sys.stderr)
            return 1
    print(f"[check_usp] ok ({n} words)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
