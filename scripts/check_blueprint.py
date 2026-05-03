#!/usr/bin/env python3
"""Phase 00 postcondition: a valid blueprint has been written.

Required artifact: evidence/<run-id>/00_blueprint.json
Required keys: core_jobs (>=3), aura_stage, peer_seed (>=8 entries),
moat_axes (>=4), kill_experiments (>=3).
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

REQUIRED = {
    "core_jobs": (lambda v: isinstance(v, list) and len(v) >= 3, "list with >=3 items"),
    "aura_stage": (
        lambda v: v in {"awareness", "understanding", "readiness", "action"},
        "one of A/U/R/A",
    ),
    "peer_seed": (lambda v: isinstance(v, list) and len(v) >= 8, "list with >=8 entries"),
    "moat_axes": (lambda v: isinstance(v, list) and len(v) >= 4, "list with >=4 axes"),
    "kill_experiments": (
        lambda v: isinstance(v, list) and len(v) >= 3,
        "list with >=3 experiments",
    ),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    args = ap.parse_args()
    p = pathlib.Path(f"evidence/{args.run_id}/00_blueprint.json")
    if not p.exists():
        print(f"[check_blueprint] FAIL: missing {p}", file=sys.stderr)
        return 1
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[check_blueprint] FAIL: invalid JSON: {e}", file=sys.stderr)
        return 1
    fail = 0
    for k, (validator, msg) in REQUIRED.items():
        if k not in data:
            print(f"[check_blueprint] FAIL: missing key '{k}'", file=sys.stderr)
            fail += 1
            continue
        if not validator(data[k]):
            print(f"[check_blueprint] FAIL: '{k}' must be {msg}", file=sys.stderr)
            fail += 1
    return 1 if fail else (print("[check_blueprint] ok") or 0)


if __name__ == "__main__":
    sys.exit(main())
