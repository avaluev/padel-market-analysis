#!/usr/bin/env python3
"""Phase 07: interview guide has all required sections + force mapping."""
import argparse, pathlib, sys

REQUIRED_SECTIONS = ("Recruitment", "Forces", "Past tense", "60-min", "Methodology")

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--run-id", required=True)
    a = ap.parse_args()
    p = pathlib.Path(f"evidence/{a.run_id}/07_interview_guide.md")
    if not p.exists():
        print(f"[check_interview_guide] FAIL: missing {p}", file=sys.stderr); return 1
    t = p.read_text(encoding="utf-8")
    miss = [s for s in REQUIRED_SECTIONS if s.lower() not in t.lower()]
    if miss:
        print(f"[check_interview_guide] FAIL: missing sections {miss}", file=sys.stderr); return 1
    if "push" not in t.lower() or "pull" not in t.lower():
        print("[check_interview_guide] FAIL: force mapping (push/pull) missing", file=sys.stderr); return 1
    print("[check_interview_guide] ok"); return 0

if __name__ == "__main__":
    sys.exit(main())
