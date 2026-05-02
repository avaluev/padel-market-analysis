#!/usr/bin/env bash
# Tally token spend per agent from evidence/<run>/usage.jsonl
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
RUN_ID="${1:-$(cat evidence/CURRENT_RUN)}"
LOG="evidence/$RUN_ID/usage.jsonl"
if [ ! -f "$LOG" ]; then echo "no usage log at $LOG"; exit 0; fi
python3 - <<PY
import json, collections
totals = collections.defaultdict(lambda: {"in":0,"out":0,"calls":0,"usd":0.0})
for ln in open("$LOG", encoding="utf-8"):
    ln = ln.strip()
    if not ln: continue
    try: o = json.loads(ln)
    except: continue
    m = o.get("model","unknown")
    t = totals[m]
    t["in"]   += o.get("input_tokens",0)
    t["out"]  += o.get("output_tokens",0)
    t["calls"]+= 1
    t["usd"]  += float(o.get("cost_usd",0) or 0)
print(f"{'model':<55}{'calls':>8}{'in':>12}{'out':>12}{'usd':>10}")
for m, t in sorted(totals.items()):
    print(f"{m:<55}{t['calls']:>8}{t['in']:>12}{t['out']:>12}{t['usd']:>10.4f}")
PY
