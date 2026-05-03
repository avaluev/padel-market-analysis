#!/usr/bin/env python3
"""Append a structured defect entry to evidence/<run>/defects.jsonl when a
gate fails. Used by run_pipeline.sh on non-zero check.
"""

import argparse
import json
import pathlib
import sys
import time


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--phase", required=True)
    ap.add_argument("--check", required=True)
    ap.add_argument("--message", required=True)
    a = ap.parse_args()
    p = pathlib.Path(f"evidence/{a.run_id}/defects.jsonl")
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                {
                    "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "phase": a.phase,
                    "check": a.check,
                    "message": a.message,
                }
            )
            + "\n"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
