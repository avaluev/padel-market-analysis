#!/usr/bin/env python3
"""Phase 02: AURA classification artifact present and valid.

Expects evidence/<run-id>/02_aura.json with:
  stage, entry_signals (>=2), exit_signals (>=2), kill_experiments (>=3),
  rationale (>=200 chars), risks (>=2)
"""
import argparse, json, pathlib, sys

ALLOWED = {"awareness", "understanding", "readiness", "action"}

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--run-id", required=True)
    a = ap.parse_args()
    p = pathlib.Path(f"evidence/{a.run_id}/02_aura.json")
    if not p.exists():
        print(f"[check_aura] FAIL: missing {p}", file=sys.stderr); return 1
    try: d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[check_aura] FAIL: {e}", file=sys.stderr); return 1
    f = 0
    if d.get("stage") not in ALLOWED: print("[check_aura] FAIL: bad stage", file=sys.stderr); f += 1
    for k, m in [("entry_signals", 2), ("exit_signals", 2), ("kill_experiments", 3), ("risks", 2)]:
        v = d.get(k)
        if not isinstance(v, list) or len(v) < m:
            print(f"[check_aura] FAIL: '{k}' needs >= {m} items", file=sys.stderr); f += 1
    if not isinstance(d.get("rationale"), str) or len(d["rationale"]) < 200:
        print("[check_aura] FAIL: rationale too short (<200 chars)", file=sys.stderr); f += 1
    return 1 if f else (print("[check_aura] ok") or 0)

if __name__ == "__main__":
    sys.exit(main())
