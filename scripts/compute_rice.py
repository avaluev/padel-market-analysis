#!/usr/bin/env python3
"""RICE = (Reach * Impact * Confidence) / Effort.
Reads value mechanic cards and emits a sorted RICE table.
"""
import argparse, json, pathlib, sys

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--run-id", required=True)
    a = ap.parse_args()
    d = pathlib.Path(f"evidence/{a.run_id}/08_value_mechanics")
    if not d.is_dir():
        print(f"[compute_rice] no value mechanics dir; skipping"); return 0
    rows = []
    for fp in sorted(d.glob("*.json")):
        c = json.loads(fp.read_text(encoding="utf-8"))
        r = c.get("rice", {})
        try:
            R = float(r.get("reach", 0)); I = float(r.get("impact", 0))
            C = float(r.get("confidence", 0)); E = float(r.get("effort", 1))
            score = (R * I * C) / max(E, 0.0001)
        except Exception:
            score = 0.0
        rows.append({"mechanic": c.get("name") or fp.stem, "rice": round(score, 3)})
    rows.sort(key=lambda x: -x["rice"])
    out = pathlib.Path(f"evidence/{a.run_id}/08_rice.json")
    out.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(f"[compute_rice] wrote {out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
