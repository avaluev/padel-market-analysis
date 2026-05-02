#!/usr/bin/env bash
# Lightweight YAML lint for evidence outputs. Uses python yaml if available.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
RUN_ID="${1:-$(cat evidence/CURRENT_RUN)}"
python3 - "$RUN_ID" <<'PY'
import sys, pathlib
try:
    import yaml
except ImportError:
    print("[validate_yaml] PyYAML not installed; skipping (install pyyaml for strict checks)")
    sys.exit(0)
run_id = sys.argv[1]
fail = 0
for p in pathlib.Path(f"evidence/{run_id}").rglob("*.y*ml"):
    try:
        list(yaml.safe_load_all(p.read_text(encoding="utf-8")))
    except yaml.YAMLError as e:
        print(f"[validate_yaml] FAIL: {p}: {e}", file=sys.stderr); fail += 1
sys.exit(1 if fail else 0)
PY
