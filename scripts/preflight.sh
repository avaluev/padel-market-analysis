#!/usr/bin/env bash
# Preflight: blocks the pipeline if the environment cannot satisfy the contract.
# MUST exit non-zero on any missing dependency. No silent passes.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

fail=0
warn=0

note() { printf "[preflight] %s\n" "$*"; }
err()  { printf "[preflight] FAIL: %s\n" "$*" >&2; fail=$((fail+1)); }
warn() { printf "[preflight] WARN: %s\n" "$*" >&2; warn=$((warn+1)); }

note "Root: $ROOT"

# ---- Required env vars ------------------------------------------------------
if [ -z "${OPENROUTER_API_KEY:-}" ]; then
  err "OPENROUTER_API_KEY is not set. Export it before running."
fi

if [ -z "${ANTHROPIC_API_KEY:-}" ] && [ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then
  warn "Neither ANTHROPIC_API_KEY nor CLAUDE_CODE_OAUTH_TOKEN is set. Claude Code may already manage auth; continuing."
fi

# ---- Required binaries ------------------------------------------------------
for bin in curl jq python3 bash; do
  if ! command -v "$bin" >/dev/null 2>&1; then
    err "Missing binary: $bin"
  fi
done

# Optional but recommended
for bin in yq sha256sum; do
  if ! command -v "$bin" >/dev/null 2>&1; then
    warn "Recommended binary missing: $bin"
  fi
done

# ---- Required directories ---------------------------------------------------
for d in prompts agents middleware scripts config evidence reports .claude/agents; do
  if [ ! -d "$d" ]; then
    err "Missing directory: $d"
  fi
done

# ---- Required policy files --------------------------------------------------
for f in CLAUDE.md README.md config/peers.yaml config/sources.yaml; do
  if [ ! -f "$f" ]; then
    err "Missing required file: $f"
  fi
done

# ---- Run-id allocation ------------------------------------------------------
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "evidence/$RUN_ID/_cache" "reports/$RUN_ID" "evidence/$RUN_ID/_logs"
echo "$RUN_ID" > evidence/CURRENT_RUN
note "Run id: $RUN_ID"

# ---- OpenRouter reachability check ------------------------------------------
if [ "$fail" -eq 0 ] && [ -n "${OPENROUTER_API_KEY:-}" ]; then
  http_code=$(curl -sS -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer $OPENROUTER_API_KEY" \
    https://openrouter.ai/api/v1/models || echo "000")
  if [ "$http_code" != "200" ]; then
    err "OpenRouter /models returned HTTP $http_code (expected 200)"
  else
    note "OpenRouter reachable (HTTP 200)"
  fi
fi

# ---- Summary ----------------------------------------------------------------
if [ "$fail" -gt 0 ]; then
  printf "[preflight] %d fatal issue(s). Aborting.\n" "$fail" >&2
  exit 1
fi
if [ "$warn" -gt 0 ]; then
  printf "[preflight] %d warning(s).\n" "$warn"
fi
note "Preflight passed."
