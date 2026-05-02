#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
RUN_ID="${1:-$(cat evidence/CURRENT_RUN)}"
python3 scripts/build_report_data.py --run-id "$RUN_ID"
python3 scripts/render_template.py --run-id "$RUN_ID"
echo "[render_report] done -> reports/$RUN_ID/index.html"
