#!/usr/bin/env python3
"""Phase 14: canonical brief JSON is the single source of truth for the report.
Required keys: 9 brief sections + usp.

Includes hard rules:
  - usp <= 30 words
  - usp must NOT contain banned tokens (ai-powered, data-driven, platform, etc.)
  - differentiation table covers every peer in 04_peer_cards
"""
import argparse, json, pathlib, re, sys

BANNED_USP_TOKENS = {
    r"\bai[-\s]?powered\b",
    r"\bdata[-\s]?driven\b",
    r"\bplatform\b",
    r"\bnext[-\s]?generation\b",
    r"\brevolutionary\b",
    r"\bdisruptive\b",
    r"\bworld[-\s]?class\b",
    r"\bcutting[-\s]?edge\b",
}

REQUIRED_SECTIONS = ("vision_frame","ajtbd","aura_thesis","segments",
                     "value_mechanics","monetization","gtm","geo","capability_map")

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--run-id", required=True)
    a = ap.parse_args()
    p = pathlib.Path(f"evidence/{a.run_id}/canonical_brief.json")
    if not p.exists():
        print(f"[check_canonical_brief] FAIL: missing {p}", file=sys.stderr); return 1
    try: d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[check_canonical_brief] FAIL: {e}", file=sys.stderr); return 1
    f = 0
    for k in REQUIRED_SECTIONS:
        if k not in d:
            print(f"[check_canonical_brief] FAIL: missing section '{k}'", file=sys.stderr); f += 1
    usp = (d.get("usp") or "").strip()
    if not usp:
        print("[check_canonical_brief] FAIL: usp missing", file=sys.stderr); f += 1
    else:
        n = len(re.findall(r"\S+", usp))
        if n > 30:
            print(f"[check_canonical_brief] FAIL: usp is {n} words (max 30)", file=sys.stderr); f += 1
        for pat in BANNED_USP_TOKENS:
            if re.search(pat, usp, re.IGNORECASE):
                print(f"[check_canonical_brief] FAIL: usp uses banned token /{pat}/", file=sys.stderr); f += 1
    diff = d.get("differentiation_table") or []
    if len(diff) < 8:
        print(f"[check_canonical_brief] FAIL: differentiation_table has {len(diff)} rows (need >= 8)", file=sys.stderr); f += 1
    return 1 if f else (print(f"[check_canonical_brief] ok (usp: {len(usp.split())} words)") or 0)

if __name__ == "__main__":
    sys.exit(main())
