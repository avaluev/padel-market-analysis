#!/usr/bin/env python3
"""Phase 10: monetization plan with primary, hedge, expansion + price benchmarks."""
import argparse, json, pathlib, sys

REQUIRED = ("primary_model", "hedge_model", "expansion_model",
            "price_benchmarks", "geo_price_localization", "unit_economics_assumptions")

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--run-id", required=True)
    a = ap.parse_args()
    p = pathlib.Path(f"evidence/{a.run_id}/10_monetization.json")
    if not p.exists():
        print(f"[check_monetization] FAIL: missing {p}", file=sys.stderr); return 1
    try: d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[check_monetization] FAIL: {e}", file=sys.stderr); return 1
    miss = [k for k in REQUIRED if k not in d]
    if miss: print(f"[check_monetization] FAIL: missing keys {miss}", file=sys.stderr); return 1
    bm = d.get("price_benchmarks") or []
    if not isinstance(bm, list) or len(bm) < 4:
        print("[check_monetization] FAIL: need >= 4 price benchmarks", file=sys.stderr); return 1
    for b in bm:
        if not b.get("source_url"):
            print(f"[check_monetization] FAIL: benchmark missing source_url: {b.get('vendor')}", file=sys.stderr); return 1
    print("[check_monetization] ok"); return 0

if __name__ == "__main__":
    sys.exit(main())
