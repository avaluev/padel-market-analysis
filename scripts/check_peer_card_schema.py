#!/usr/bin/env python3
"""Phase 04: every peer card under evidence/<run-id>/04_peer_cards/ matches
the peer card schema and tags moat class from the canonical taxonomy."""
import argparse, json, pathlib, sys

REQUIRED = ("name","url","archetype","value_prop","pricing","traction_signal",
            "moat_class","moat_evidence_url","gaps","verification_status")
ALLOWED_MOAT = {"network","data","brand","distribution","switching_cost",
                "integration","regulatory","learning_curve","none"}
FORBIDDEN_MOAT = {"ai_powered","better_ux","superior_product","first_mover"}

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--run-id", required=True)
    a = ap.parse_args()
    d = pathlib.Path(f"evidence/{a.run_id}/04_peer_cards")
    if not d.is_dir():
        print(f"[check_peer_card_schema] FAIL: missing {d}", file=sys.stderr); return 1
    files = list(d.glob("*.json"))
    if len(files) < 8:
        print(f"[check_peer_card_schema] FAIL: need >= 8 peer cards, got {len(files)}", file=sys.stderr); return 1
    f = 0
    for fp in files:
        try: c = json.loads(fp.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[check_peer_card_schema] FAIL: {fp.name}: {e}", file=sys.stderr); f += 1; continue
        for k in REQUIRED:
            if k not in c:
                print(f"[check_peer_card_schema] FAIL: {fp.name} missing '{k}'", file=sys.stderr); f += 1
        m = (c.get("moat_class") or "").lower()
        if m in FORBIDDEN_MOAT:
            print(f"[check_peer_card_schema] FAIL: {fp.name} uses forbidden moat '{m}'", file=sys.stderr); f += 1
        if m not in ALLOWED_MOAT and m not in FORBIDDEN_MOAT:
            print(f"[check_peer_card_schema] FAIL: {fp.name} unknown moat '{m}'", file=sys.stderr); f += 1
    return 1 if f else (print(f"[check_peer_card_schema] ok ({len(files)} cards)") or 0)

if __name__ == "__main__":
    sys.exit(main())
