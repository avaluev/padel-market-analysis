#!/usr/bin/env python3
"""Phase 06: segment red team produces verdicts; at least one non-pass."""
import argparse, json, pathlib, sys

ALLOWED = {"pass", "pass_with_caveats", "fail", "false_segment"}

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--run-id", required=True)
    a = ap.parse_args()
    p = pathlib.Path(f"evidence/{a.run_id}/06_red_team.json")
    if not p.exists():
        print(f"[check_red_team] FAIL: missing {p}", file=sys.stderr); return 1
    try: d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[check_red_team] FAIL: {e}", file=sys.stderr); return 1
    verdicts = d.get("verdicts", [])
    if not isinstance(verdicts, list) or len(verdicts) < 4:
        print(f"[check_red_team] FAIL: need >= 4 segment verdicts, got {len(verdicts) if isinstance(verdicts,list) else 'n/a'}", file=sys.stderr); return 1
    bad = [v for v in verdicts if v.get("verdict") not in ALLOWED]
    if bad:
        print(f"[check_red_team] FAIL: bad verdict values: {bad}", file=sys.stderr); return 1
    if not any(v.get("verdict") in {"fail","false_segment","pass_with_caveats"} for v in verdicts):
        print("[check_red_team] FAIL: yes-man pattern (every verdict is pass)", file=sys.stderr); return 1
    print(f"[check_red_team] ok ({len(verdicts)} verdicts)"); return 0

if __name__ == "__main__":
    sys.exit(main())
