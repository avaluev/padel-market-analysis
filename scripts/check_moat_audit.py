#!/usr/bin/env python3
"""Phase 09: Naval 5-gate filter. Each value mechanic gets a score across
five gates (distribution, network, data, hardware, vertical_depth), and
at least one mechanic is killed or demoted."""
import argparse, json, pathlib, sys

GATES = ("distribution", "network", "data", "hardware", "vertical_depth")

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--run-id", required=True)
    a = ap.parse_args()
    p = pathlib.Path(f"evidence/{a.run_id}/09_moat_audit.json")
    if not p.exists():
        print(f"[check_moat_audit] FAIL: missing {p}", file=sys.stderr); return 1
    try: d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[check_moat_audit] FAIL: {e}", file=sys.stderr); return 1
    rows = d.get("audit", [])
    if not isinstance(rows, list) or len(rows) < 6:
        print(f"[check_moat_audit] FAIL: need >= 6 audit rows", file=sys.stderr); return 1
    f = 0
    for r in rows:
        scores = r.get("scores", {})
        for g in GATES:
            if g not in scores: print(f"[check_moat_audit] FAIL: missing gate '{g}' for '{r.get('mechanic')}'", file=sys.stderr); f += 1
            elif scores[g] not in (0, 1, 2): print(f"[check_moat_audit] FAIL: bad score for '{g}': {scores[g]}", file=sys.stderr); f += 1
        if "verdict" not in r: print(f"[check_moat_audit] FAIL: missing verdict for '{r.get('mechanic')}'", file=sys.stderr); f += 1
        if "naval_citation_url" not in r: print(f"[check_moat_audit] FAIL: missing naval_citation_url for '{r.get('mechanic')}'", file=sys.stderr); f += 1
    killed = [r for r in rows if r.get("verdict") in {"kill", "demote"}]
    if not killed:
        print("[check_moat_audit] FAIL: red team must kill or demote >= 1 mechanic", file=sys.stderr); f += 1
    return 1 if f else (print(f"[check_moat_audit] ok ({len(rows)} rows, {len(killed)} killed/demoted)") or 0)

if __name__ == "__main__":
    sys.exit(main())
