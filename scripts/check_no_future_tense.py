#!/usr/bin/env python3
"""Forbid time/budget promises in reports. Future-promise patterns:
'will deliver', 'in N weeks', 'by Q[1234]', 'by [month]', '$N budget'.
"""
import argparse, pathlib, re, sys

PATTERNS = [
    re.compile(r"\bwill\s+(deliver|launch|ship|complete|finalize)\b", re.I),
    re.compile(r"\bin\s+\d+\s+(weeks?|months?|days?|sprints?)\b", re.I),
    re.compile(r"\bby\s+(Q[1-4]|January|February|March|April|May|June|July|August|September|October|November|December|H[12]\s+\d{4})\b", re.I),
    re.compile(r"\$\d[\d,\.]*\s*(budget|cost|spend|investment)\b", re.I),
    re.compile(r"\bbudget\s+of\s+\$\d", re.I),
]

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--run-id", required=True); ap.add_argument("--phase", default=None)
    a = ap.parse_args()
    rep = pathlib.Path(f"reports/{a.run_id}")
    if not rep.exists():
        print("[check_no_future_tense] no report yet"); return 0
    fail = 0
    for f in rep.rglob("*"):
        if not f.is_file() or f.suffix.lower() not in {".html", ".md"}: continue
        text = f.read_text(encoding="utf-8", errors="ignore")
        for pat in PATTERNS:
            for m in pat.finditer(text):
                print(f"[check_no_future_tense] FAIL: {f}: {m.group(0)!r}", file=sys.stderr); fail += 1
    return 1 if fail else (print("[check_no_future_tense] clean") or 0)

if __name__ == "__main__":
    sys.exit(main())
