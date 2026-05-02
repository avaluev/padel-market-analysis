#!/usr/bin/env python3
"""Phase 11: GTM/PLG plan with channels, CAC anchors, >=4 PLG loops, distribution-as-moat thesis."""
import argparse, json, pathlib, sys

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--run-id", required=True)
    a = ap.parse_args()
    p = pathlib.Path(f"evidence/{a.run_id}/11_gtm.json")
    if not p.exists():
        print(f"[check_gtm] FAIL: missing {p}", file=sys.stderr); return 1
    try: d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[check_gtm] FAIL: {e}", file=sys.stderr); return 1
    f = 0
    ch = d.get("channels") or []
    if not isinstance(ch, list) or len(ch) < 5:
        print("[check_gtm] FAIL: need >= 5 channels ranked", file=sys.stderr); f += 1
    cac_missing = [c for c in ch if not c.get("cac_anchor_url")]
    if cac_missing:
        print(f"[check_gtm] FAIL: {len(cac_missing)} channel(s) missing CAC source URL", file=sys.stderr); f += 1
    loops = d.get("plg_loops") or []
    if len(loops) < 4:
        print(f"[check_gtm] FAIL: need >= 4 PLG loops, got {len(loops)}", file=sys.stderr); f += 1
    if not d.get("distribution_as_moat"):
        print("[check_gtm] FAIL: distribution_as_moat thesis missing", file=sys.stderr); f += 1
    return 1 if f else (print("[check_gtm] ok") or 0)

if __name__ == "__main__":
    sys.exit(main())
