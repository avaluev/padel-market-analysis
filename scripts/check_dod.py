#!/usr/bin/env python3
"""Phase 16: final DoD gate aggregating every prior check."""

import argparse
import subprocess
import sys

CHECKS = [
    ("scripts/check_blueprint.py", []),
    ("scripts/check_job_stories.py", []),
    ("scripts/check_aura.py", []),
    ("scripts/check_peer_discovery.py", []),
    ("scripts/check_peer_card_schema.py", []),
    ("scripts/jobs_graph_lint.py", []),
    ("scripts/check_red_team.py", []),
    ("scripts/check_interview_guide.py", []),
    ("scripts/check_moat_taxonomy.py", []),
    ("scripts/check_moat_audit.py", []),
    ("scripts/check_monetization.py", []),
    ("scripts/check_gtm.py", []),
    ("scripts/check_geo_bands.py", []),
    ("scripts/check_capability_bands.py", []),
    ("scripts/check_canonical_brief.py", []),
    ("scripts/check_section_completeness.py", []),
    ("scripts/check_first_person.py", ["--phase", "16"]),
    ("scripts/check_quote_lengths.py", ["--phase", "16"]),
    ("scripts/check_quote_dedup.py", ["--phase", "16"]),
    ("scripts/check_numeric_claims.py", ["--phase", "16"]),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    a = ap.parse_args()
    fails = []
    for script, extra in CHECKS:
        cmd = ["python3", script, "--run-id", a.run_id] + extra
        r = subprocess.run(cmd, capture_output=True, text=True)
        sys.stdout.write(r.stdout)
        sys.stderr.write(r.stderr)
        if r.returncode != 0:
            fails.append(script)
    # link verifier (bash)
    r = subprocess.run(
        ["bash", "scripts/verify_links.sh", a.run_id], capture_output=True, text=True
    )
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    if r.returncode != 0:
        fails.append("scripts/verify_links.sh")
    if fails:
        print(f"[check_dod] FAIL: {len(fails)} gate(s) failed: {fails}", file=sys.stderr)
        return 1
    print("[check_dod] DoD passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
