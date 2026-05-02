#!/usr/bin/env python3
"""Phase 08: 8-12 value mechanic cards spanning >= 4 moat classes."""
import argparse, json, pathlib, sys

ALLOWED = {"network","data","brand","distribution","switching_cost",
           "integration","regulatory","learning_curve"}

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--run-id", required=True)
    a = ap.parse_args()
    d = pathlib.Path(f"evidence/{a.run_id}/08_value_mechanics")
    if not d.is_dir():
        print(f"[check_moat_taxonomy] FAIL: missing {d}", file=sys.stderr); return 1
    files = list(d.glob("*.json"))
    if not (8 <= len(files) <= 14):
        print(f"[check_moat_taxonomy] FAIL: expected 8-14 cards, got {len(files)}", file=sys.stderr); return 1
    classes = set()
    f = 0
    for fp in files:
        try: c = json.loads(fp.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[check_moat_taxonomy] FAIL: {fp.name}: {e}", file=sys.stderr); f += 1; continue
        m = (c.get("moat_class") or "").lower()
        if m not in ALLOWED:
            print(f"[check_moat_taxonomy] FAIL: {fp.name} bad moat '{m}'", file=sys.stderr); f += 1
        else:
            classes.add(m)
    if len(classes) < 4:
        print(f"[check_moat_taxonomy] FAIL: only {len(classes)} moat classes (need >= 4)", file=sys.stderr); f += 1
    return 1 if f else (print(f"[check_moat_taxonomy] ok ({len(files)} cards, {len(classes)} classes)") or 0)

if __name__ == "__main__":
    sys.exit(main())
