#!/usr/bin/env python3
"""Phase 12: geo strategy assigns every seed country to P0/P1/P2/P3/deferred."""
import argparse, json, pathlib, sys

ALLOWED = {"P0", "P1", "P2", "P3", "deferred"}

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--run-id", required=True)
    a = ap.parse_args()
    p = pathlib.Path(f"evidence/{a.run_id}/12_geo.json")
    if not p.exists():
        print(f"[check_geo_bands] FAIL: missing {p}", file=sys.stderr); return 1
    try: d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[check_geo_bands] FAIL: {e}", file=sys.stderr); return 1
    rows = d.get("geographies") or []
    if len(rows) < 12:
        print(f"[check_geo_bands] FAIL: need >= 12 country rows", file=sys.stderr); return 1
    f = 0
    for r in rows:
        if r.get("band") not in ALLOWED:
            print(f"[check_geo_bands] FAIL: bad band for {r.get('country')}: {r.get('band')}", file=sys.stderr); f += 1
        if not r.get("evidence_url"):
            print(f"[check_geo_bands] FAIL: {r.get('country')} missing evidence_url", file=sys.stderr); f += 1
    if not any(r.get("band") == "P0" for r in rows):
        print("[check_geo_bands] FAIL: at least one P0 country required", file=sys.stderr); f += 1
    return 1 if f else (print(f"[check_geo_bands] ok ({len(rows)} countries)") or 0)

if __name__ == "__main__":
    sys.exit(main())
