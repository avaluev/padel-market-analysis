#!/usr/bin/env python3
"""Phase 13: capability map covers all 5 bands and every capability cites
either an open-source anchor or an API alternative."""
import argparse, json, pathlib, sys

BANDS = {"ship_solo", "ship_solo_with_apis", "requires_partner",
         "requires_capital", "requires_team"}

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--run-id", required=True)
    a = ap.parse_args()
    p = pathlib.Path(f"evidence/{a.run_id}/13_capability_map.json")
    if not p.exists():
        print(f"[check_capability_bands] FAIL: missing {p}", file=sys.stderr); return 1
    try: d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[check_capability_bands] FAIL: {e}", file=sys.stderr); return 1
    rows = d.get("capabilities") or []
    if len(rows) < 12:
        print(f"[check_capability_bands] FAIL: need >= 12 capabilities, got {len(rows)}", file=sys.stderr); return 1
    seen = {b: 0 for b in BANDS}
    f = 0
    for r in rows:
        b = r.get("band")
        if b not in BANDS:
            print(f"[check_capability_bands] FAIL: bad band {b} for {r.get('capability')}", file=sys.stderr); f += 1
        else:
            seen[b] += 1
        if not (r.get("oss_anchor_url") or r.get("api_url")):
            print(f"[check_capability_bands] FAIL: {r.get('capability')} has no oss_anchor_url or api_url", file=sys.stderr); f += 1
    if seen.get("ship_solo", 0) < 3:
        print(f"[check_capability_bands] FAIL: need >= 3 ship_solo items, got {seen.get('ship_solo',0)}", file=sys.stderr); f += 1
    if seen.get("requires_capital", 0) < 1:
        print(f"[check_capability_bands] FAIL: need >= 1 requires_capital item", file=sys.stderr); f += 1
    return 1 if f else (print(f"[check_capability_bands] ok ({seen})") or 0)

if __name__ == "__main__":
    sys.exit(main())
