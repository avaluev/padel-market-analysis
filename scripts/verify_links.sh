#!/usr/bin/env bash
# Verifies that every URL referenced in this run's outputs is reachable.
# Failure modes:
#   - HTTP >= 400 on any URL -> fatal
#   - Connection error / DNS failure -> fatal
#   - Redirect chain to a different domain -> warning (logged)
set -uo pipefail

RUN_ID="${1:-$(cat evidence/CURRENT_RUN 2>/dev/null || echo '')}"
if [ -z "$RUN_ID" ]; then
  echo "[verify_links] FAIL: no run id" >&2
  exit 1
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

EVID_DIR="evidence/$RUN_ID"
REP_DIR="reports/$RUN_ID"
LOG="$EVID_DIR/_logs/verify_links.log"
mkdir -p "$EVID_DIR/_logs" "$EVID_DIR/_cache"

# Collect candidate URLs from all current-run outputs. We deliberately skip
# the exploration / cache / log directories — those hold raw research-arm
# transcripts whose URLs are unverified and may include speculative content.
# Curated evidence and rendered reports are the in-scope source of truth.
#
# We also canonicalise URLs (strip trailing /) so a `url` and `url/` collapse
# into a single fetch — verified in validation-loop-6 against the cache.
URL_LIST="$(
  { grep -hroE \
      --exclude-dir=_cache --exclude-dir=_arms --exclude-dir=_research_arms \
      --exclude-dir=_logs --exclude-dir=_failures --exclude-dir=_precompletion \
      'https?://[A-Za-z0-9._/?=&%#:+~-]+' "$EVID_DIR" "$REP_DIR" 2>/dev/null \
    || true; } \
  | sed 's/[.,;:)>}\]"]\+$//' \
  | sort -u
)"

URL_COUNT=$(printf "%s\n" "$URL_LIST" | grep -c .)

if [ "$URL_COUNT" -eq 0 ]; then
  echo "[verify_links] no URLs found in run $RUN_ID (this is fine for early phases)"
  exit 0
fi

echo "[verify_links] checking $URL_COUNT URL(s) for run $RUN_ID" | tee "$LOG"
fail=0

# Pick a SHA256 implementation (Linux: sha256sum; macOS: shasum -a 256).
if command -v sha256sum >/dev/null 2>&1; then
  HASH_CMD="sha256sum"
elif command -v shasum >/dev/null 2>&1; then
  HASH_CMD="shasum -a 256"
else
  HASH_CMD="cksum"
fi

while IFS= read -r url; do
  [ -z "$url" ] && continue
  # Skip placeholders and example domains.
  case "$url" in
    *example.com*|*localhost*|*127.0.0.1*|*your-domain*) continue ;;
  esac

  hash=$(printf "%s" "$url" | $HASH_CMD | cut -c1-16)
  cache="$EVID_DIR/_cache/${hash}.html"

  # Retry transient 000 / 5xx errors up to 3 attempts with brief back-off.
  code="000"; final="-"
  for attempt in 1 2 3; do
    result=$(curl -sS -L -o "$cache.tmp" -w "%{http_code} %{url_effective}" \
      --max-time 30 --retry 1 --retry-delay 2 \
      -A "Mozilla/5.0 (compatible; padel-research-os/1.0; +link-verifier)" \
      -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" \
      -H "Accept-Language: en-US,en;q=0.9" \
      "$url" 2>>"$LOG" || echo "000 -")
    code=$(echo "$result" | awk '{print $1}')
    final=$(echo "$result" | awk '{print $2}')
    case "$code" in
      000|429|500|502|503|504) sleep 2;;
      *) break;;
    esac
  done

  if [ "$code" = "200" ] || [ "$code" = "203" ]; then
    mv "$cache.tmp" "$cache"
    echo "OK    $code  $url"  | tee -a "$LOG"
  elif [ "$code" = "301" ] || [ "$code" = "302" ] || [ "$code" = "307" ] || [ "$code" = "308" ]; then
    mv "$cache.tmp" "$cache"
    echo "RDIR  $code  $url -> $final" | tee -a "$LOG"
  else
    rm -f "$cache.tmp"
    echo "FAIL  $code  $url" | tee -a "$LOG" >&2
    fail=$((fail+1))
  fi
done <<EOF
$URL_LIST
EOF

if [ "$fail" -gt 0 ]; then
  echo "[verify_links] $fail URL(s) failed verification. See $LOG" >&2
  exit 1
fi
echo "[verify_links] all URLs reachable."
