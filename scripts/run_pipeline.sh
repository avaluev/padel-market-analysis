#!/usr/bin/env bash
# Pipeline runner. Sequences prompts 00 -> 16. Each phase is a gate.
# A phase MUST NOT proceed if its precompletion checks fail.
#
# This script does NOT call models directly. It is the orchestration entry
# point for Claude Code: it prints the prompt path, the model assignment,
# and the postcondition checks. Claude Code drives execution; this script
# enforces sequencing and verifies postconditions.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

bash scripts/preflight.sh
RUN_ID="$(cat evidence/CURRENT_RUN)"
LOG_DIR="evidence/$RUN_ID/_logs"
mkdir -p "$LOG_DIR"

# Phase table: id | prompt file | model class | required check script
# model class is informational; Claude Code reads the prompt's frontmatter
# for the actual model assignment.
PHASES=(
  "00|prompts/00_master_blueprint.md|opus-thinking|scripts/check_blueprint.py"
  "01|prompts/01_ajtbd_restatement.md|opus-thinking|scripts/check_job_stories.py"
  "02|prompts/02_aura_classification.md|opus-thinking|scripts/check_aura.py"
  "03|prompts/03_peer_discovery.md|deep-research|scripts/check_peer_discovery.py"
  "04|prompts/04_peer_deep_dive.md|haiku-swarm|scripts/check_peer_card_schema.py"
  "05|prompts/05_segment_canvas.md|sonnet|scripts/jobs_graph_lint.py"
  "06|prompts/06_segment_red_team.md|opus-thinking|scripts/check_red_team.py"
  "07|prompts/07_interview_guide.md|sonnet|scripts/check_interview_guide.py"
  "08|prompts/08_value_mechanics.md|sonnet|scripts/check_moat_taxonomy.py"
  "09|prompts/09_naval_filter.md|opus-thinking|scripts/check_moat_audit.py"
  "10|prompts/10_monetization.md|sonnet|scripts/check_monetization.py"
  "11|prompts/11_gtm_plg_distribution.md|sonnet|scripts/check_gtm.py"
  "12|prompts/12_geo_strategy.md|sonnet|scripts/check_geo_bands.py"
  "13|prompts/13_capability_map.md|sonnet|scripts/check_capability_bands.py"
  "14|prompts/14_synthesis_usp.md|opus-thinking|scripts/check_canonical_brief.py"
  "15|prompts/15_html_render.md|haiku|scripts/check_section_completeness.py"
  "16|prompts/16_final_red_team.md|opus-thinking|scripts/check_dod.py"
)

run_phase() {
  local entry="$1"
  IFS='|' read -r id prompt model check <<< "$entry"

  printf "\n========================================================\n"
  printf "PHASE %s\n" "$id"
  printf "  prompt : %s\n" "$prompt"
  printf "  model  : %s\n" "$model"
  printf "  check  : %s\n" "$check"
  printf "========================================================\n"

  if [ ! -f "$prompt" ]; then
    printf "[runner] FAIL: prompt file missing: %s\n" "$prompt" >&2
    return 1
  fi

  # Surface the prompt to the user (Claude Code reads it next).
  printf "\n--- BEGIN PROMPT %s ---\n" "$id"
  cat "$prompt"
  printf "\n--- END PROMPT %s ---\n" "$id"

  # The runner pauses here. Claude Code executes the prompt, writes outputs
  # under reports/$RUN_ID/<id>_* and evidence/$RUN_ID/, then signals done by
  # touching evidence/$RUN_ID/_phase_${id}.done.
  printf "[runner] Awaiting completion marker: evidence/%s/_phase_%s.done\n" "$RUN_ID" "$id"

  # Postcondition check. Each check script returns 0 on pass, non-zero on fail.
  if [ -f "$check" ]; then
    if ! python3 "$check" --run-id "$RUN_ID"; then
      printf "[runner] FAIL: postcondition check %s did not pass for phase %s.\n" "$check" "$id" >&2
      return 1
    fi
  else
    printf "[runner] WARN: check script %s is missing; skipping postcondition.\n" "$check"
  fi

  # Universal checks across every phase.
  python3 scripts/check_first_person.py --phase "$id" --run-id "$RUN_ID" || return 1
  python3 scripts/check_quote_lengths.py --phase "$id" --run-id "$RUN_ID" || return 1
  python3 scripts/check_quote_dedup.py --phase "$id" --run-id "$RUN_ID" || return 1
  python3 scripts/check_numeric_claims.py --phase "$id" --run-id "$RUN_ID" || return 1
  bash   scripts/verify_links.sh "$RUN_ID" || return 1

  printf "[runner] phase %s complete.\n" "$id"
}

START_PHASE="${1:-00}"
SKIP=true
for entry in "${PHASES[@]}"; do
  IFS='|' read -r id _ _ _ <<< "$entry"
  if [ "$id" = "$START_PHASE" ]; then SKIP=false; fi
  if [ "$SKIP" = "true" ]; then continue; fi
  run_phase "$entry"
done

printf "\n[runner] Pipeline finished for run %s.\n" "$RUN_ID"
printf "[runner] Final report: reports/%s/index.html\n" "$RUN_ID"
