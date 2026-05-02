#!/usr/bin/env python3
"""Phase 15: rendered HTML contains all 16 mandated sections by id."""
import argparse, pathlib, re, sys

REQUIRED_IDS = (
    "executive-summary","market-size","ajtbd","aura","segments","peers",
    "value-mechanics","naval-filter","monetization","gtm-plg","geo",
    "capability-map","kill-experiments","risks","triz-pain-extraction",
    "retention-drivers","usp","analyst-sources",
)

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--run-id", required=True)
    a = ap.parse_args()
    p = pathlib.Path(f"reports/{a.run_id}/index.html")
    if not p.exists():
        print(f"[check_section_completeness] FAIL: missing {p}", file=sys.stderr); return 1
    html = p.read_text(encoding="utf-8")
    miss = []
    for sid in REQUIRED_IDS:
        if not re.search(rf'id\s*=\s*"{re.escape(sid)}"', html):
            miss.append(sid)
    if miss:
        print(f"[check_section_completeness] FAIL: missing section ids: {miss}", file=sys.stderr); return 1
    size = p.stat().st_size
    if size > 600_000:
        print(f"[check_section_completeness] FAIL: report is {size} bytes (cap 600KB)", file=sys.stderr); return 1
    print(f"[check_section_completeness] ok ({size} bytes, all ids present)"); return 0

if __name__ == "__main__":
    sys.exit(main())
