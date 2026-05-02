#!/usr/bin/env python3
"""Phase 03: peer discovery yields a deduplicated peer list of >= 16
candidates (8 anchors + >= 8 expansions) with multi-arm evidence.

Expects evidence/<run-id>/03_peers_raw.jsonl (append-only stream from each
research arm) and evidence/<run-id>/03_peers_dedup.json (Opus-reduced
deduplicated list).
"""
import argparse, json, pathlib, sys

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--run-id", required=True)
    a = ap.parse_args()
    raw = pathlib.Path(f"evidence/{a.run_id}/03_peers_raw.jsonl")
    dd = pathlib.Path(f"evidence/{a.run_id}/03_peers_dedup.json")
    if not raw.exists() or not dd.exists():
        print(f"[check_peer_discovery] FAIL: missing raw or dedup file", file=sys.stderr); return 1
    try: deduped = json.loads(dd.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[check_peer_discovery] FAIL: bad JSON: {e}", file=sys.stderr); return 1
    if not isinstance(deduped, list) or len(deduped) < 16:
        print(f"[check_peer_discovery] FAIL: need >= 16 peers, got {len(deduped) if isinstance(deduped,list) else 'n/a'}", file=sys.stderr); return 1
    arms_seen = set()
    for line in raw.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line: continue
        try: o = json.loads(line)
        except: continue
        a_ = o.get("arm") or o.get("source_model")
        if a_: arms_seen.add(a_)
    if len(arms_seen) < 2:
        print(f"[check_peer_discovery] FAIL: peer evidence came from only {len(arms_seen)} arm(s); need >= 2", file=sys.stderr); return 1
    miss_url = [p for p in deduped if not p.get("url")]
    if miss_url:
        print(f"[check_peer_discovery] FAIL: {len(miss_url)} peer(s) without url", file=sys.stderr); return 1
    print(f"[check_peer_discovery] ok ({len(deduped)} peers, {len(arms_seen)} arms)"); return 0

if __name__ == "__main__":
    sys.exit(main())
