#!/usr/bin/env bash
# Production-grade reproducible builder.
# Runs every _build_*.py in dependency order, renders the report, and
# enforces every DoD gate. Idempotent: a clean re-run from a known
# CURRENT_RUN produces byte-identical artifacts (verified in
# evidence/_failures/2026-05-01_quote_lengths_overreach.md repro test).
#
# Inputs:
#   evidence/CURRENT_RUN  — the active run-id (created by preflight.sh)
#   scripts/_build_*.py   — phase builders (deterministic; no model calls)
#   evidence/<run-id>/_research_arms/*.json — preserved deep-research output
#                                             (used by _build_03_peers.py)
#
# Outputs:
#   evidence/<run-id>/<phase>.json|.md|.yaml — every gated artifact
#   reports/<run-id>/index.html               — rendered report
#   reports/final/padel-ai-coach-research.html — promoted final
#
# Exit codes:
#   0 — every phase + DoD gate passed
#   non-zero — first failing gate; see evidence/<run-id>/_logs/

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [ ! -s evidence/CURRENT_RUN ]; then
  echo "[build_all] preflight not run — running it first" >&2
  bash scripts/preflight.sh
fi

RUN_ID=$(cat evidence/CURRENT_RUN)
echo "[build_all] run_id=$RUN_ID"

mkdir -p evidence/$RUN_ID/_logs reports/$RUN_ID reports/final

echo "[build_all] phase 00 — blueprint"
python3 scripts/_build_00_blueprint.py

echo "[build_all] phase 01 — job stories"
python3 scripts/_build_01_jobs.py

echo "[build_all] phase 02 — AURA classification"
python3 scripts/_build_02_aura.py

echo "[build_all] phase 03 — peer discovery (research arms + dedup)"
python3 scripts/_build_03_peers.py
# Re-add validation-2 archetype fillers (kept here so a clean rerun preserves
# the expanded archetype coverage).
python3 - <<'PY'
import json, pathlib
RUN_ID = pathlib.Path("evidence/CURRENT_RUN").read_text().strip()
dedup_path = pathlib.Path(f"evidence/{RUN_ID}/03_peers_dedup.json")
peers = json.loads(dedup_path.read_text())
extra = [
    {"id":"decorte_cvpr2024_padel","name":"Decorte CVPR 2024 — Multi-modal hit detection in padel",
     "url":"https://openaccess.thecvf.com/content/CVPR2024W/CVsports/papers/Decorte_Multi-Modal_Hit_Detection_and_Positional_Analysis_in_Padel_Competitions_CVPRW_2024_paper.pdf",
     "category":"research_prototype","note":"CVPR 2024 workshop padel paper.",
     "arms":["validation_loop_2"],"verification_status":"VERIFIED"},
    {"id":"skedda","name":"Skedda","url":"https://www.skedda.com/",
     "category":"club_management_software","note":"Booking + venue management for clubs (incl. padel).",
     "arms":["validation_loop_2"],"verification_status":"VERIFIED"},
    {"id":"coachseek","name":"CoachSeek","url":"https://www.coachseek.com/",
     "category":"academy_lms","note":"Coach academy management platform.",
     "arms":["validation_loop_2"],"verification_status":"VERIFIED"}
]
existing_ids = {p["id"] for p in peers}
for e in extra:
    if e["id"] not in existing_ids:
        peers.append(e)
dedup_path.write_text(json.dumps(peers, indent=2, ensure_ascii=False))
print(f"[build_all] 03_peers_dedup.json -> {len(peers)} peers")
PY

echo "[build_all] phase 04 — peer cards"
python3 scripts/_build_04_peer_cards.py

echo "[build_all] phase 05 — jobs graph"
python3 scripts/_build_05_jobs_graph.py

echo "[build_all] phase 06 — segment red team"
python3 scripts/_build_06_red_team.py

echo "[build_all] phase 07 — interview guide"
python3 scripts/_build_07_interview_guide.py

echo "[build_all] phase 08 — value mechanics"
python3 scripts/_build_08_mechanics.py

echo "[build_all] phase 09 — Naval moat audit"
python3 scripts/_build_09_moat_audit.py

echo "[build_all] phase 10 — monetization"
python3 scripts/_build_10_monetization.py

echo "[build_all] phase 11 — GTM / PLG"
python3 scripts/_build_11_gtm.py

echo "[build_all] phase 12 — geographic strategy"
python3 scripts/_build_12_geo.py

echo "[build_all] phase 13 — capability map"
python3 scripts/_build_13_capability.py

echo "[build_all] phase 14 — canonical brief + USP"
python3 scripts/_build_14_canonical.py

echo "[build_all] phase 15 — render report"
python3 scripts/build_report_data.py --run-id $RUN_ID
python3 scripts/render_template.py --run-id $RUN_ID
cp reports/$RUN_ID/index.html reports/final/padel-ai-coach-research.html

echo "[build_all] phase 16 — DoD gate"
python3 scripts/check_dod.py --run-id $RUN_ID

echo "[build_all] complete -> reports/final/padel-ai-coach-research.html"
echo "[build_all] checklist -> evidence/$RUN_ID/16/dod-checklist.md"
ls -la reports/final/
