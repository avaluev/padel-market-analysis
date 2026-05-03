#!/usr/bin/env python3
"""Sanitise the top-level published HTML pages.

This script applies the same content-cleanup transforms that
``scripts/build_pages.mjs`` applies to the rebuilt pages, but operates on
hand-edited static pages: index.html, methodology.html,
padel-ai-coach-research.html, evidence-map.html, 404.html.

The script is **idempotent** — running it twice produces the same result.
It is also intentionally narrow: it only does mechanical replacements that
match patterns the quality gates will later block. It does not rewrite
sentences for flow; that is a manual pass.

Transforms:
- Strip run-id timestamps (``20260501T135005Z`` style) from text and links.
- Replace ``the candidate`` framing with neutral nouns or drop the qualifier.
- Replace ``kill experiment`` / ``kill threshold`` / ``kill metric`` jargon
  with plain English.
- Remove the AI-marketing badge block (``100% link-verified``,
  ``12 specialist agents``, etc).
- Remove the unverified bundle-size and stat-grid claims from index.html.
- Remove the ``Run`` fingerprint span from author footers.

Exit code: 0 always (this script is a fixer, not a checker).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FINAL = ROOT / "reports/final"

# --- regex bank --------------------------------------------------------------

RUN_ID = re.compile(r"\b\d{8}T\d{6}Z\b")

# Header/footer fingerprint blocks built around the run-id.
HEADER_RUN_SPAN = re.compile(
    r'\s*<span class="ext">Run\s+\d{8}T\d{6}Z</span>',
    re.MULTILINE,
)
HERO_RUN_META = re.compile(
    r'\s*<p class="meta">[^<]*Run\s+\d{8}T\d{6}Z[^<]*</p>',
    re.MULTILINE,
)
FOOTER_RUN_LINE = re.compile(
    r"\s*<span>Run\s+<code>\d{8}T\d{6}Z</code></span>\s*"
    r'<span class="dot-sep" aria-hidden="true">·</span>\s*',
    re.MULTILINE,
)

# Inline evidence/<run-id>/ paths.
RUN_PATH = re.compile(r'evidence/\d{8}T\d{6}Z/[^\s"<>)\]]+')
RUN_BARE_PATH = re.compile(r"`evidence/\d{8}T\d{6}Z/`")

# "Candidate" framing.
CANDIDATE_FULL_LINES = [
    re.compile(r"[Tt]he candidate is not a padel player\.\s*"),
    re.compile(r"[Tt]he candidate has no domain expertise[^.]*\.\s*"),
]
CANDIDATE_POSSESSIVE = re.compile(r"\b([Tt]he|[Aa]|[Aa]n)\s+candidate's\s+")
CANDIDATE_QUALIFIER = re.compile(
    r"\b([Tt]he|[Aa]|[Aa]n|[Tt]hat|[Tt]his|[Tt]hose|[Tt]hese|[Ee]very|"
    r"[Ss]ix|[Tt]wo|[Tt]hree|[Ff]our|[Ff]ive|[Ee]ight|[Tt]en|[Ee]leven)"
    r"\s+candidate\s+(?=[A-Za-z])"
)
CANDIDATE_FOLLOWED_BY_LOWER = re.compile(r"\bcandidate\s+(?=[a-z])")
CANDIDATE_PLURAL = re.compile(r"\bcandidates\b")
CANDIDATE_BARE = re.compile(r"\b[Cc]andidate\b")

# Jargon.
JARGON_PAIRS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bkill experiment(s)?\b", re.IGNORECASE), r"stop test\1"),
    (re.compile(r"\bkill criteri(?:on|a)\b", re.IGNORECASE), "exit criteria"),
    (re.compile(r"\bkill threshold(s)?\b", re.IGNORECASE), r"exit threshold\1"),
    (re.compile(r"\bkill signal(s)?\b", re.IGNORECASE), r"stop signal\1"),
    (re.compile(r"\bkill metric(s)?\b", re.IGNORECASE), r"stop metric\1"),
    (re.compile(r"\bnorth star metric\b", re.IGNORECASE), "the one number that matters"),
    (re.compile(r"\bnorth star\b", re.IGNORECASE), "headline metric"),
    (re.compile(r"\bred[- ]team(?:ed|ing)?\b", re.IGNORECASE), "adversarial review"),
    (re.compile(r"\bWizard of Oz\b"), "manual prototype"),
    (re.compile(r"\banti[- ]pattern(s)?\b", re.IGNORECASE), r"wrong move\1"),
    (re.compile(r"\bdata_gaps?\b"), "data gaps"),
    (re.compile(r"\bB2B2C\b"), "business-to-business-to-consumer"),
    (re.compile(r"\bB2B\b"), "business-to-business"),
    (re.compile(r"\bB2C\b"), "business-to-consumer"),
    (re.compile(r"\bGTM\b"), "go-to-market"),
]

# Marketing badges to remove. Each tuple is (pattern, expected-text-only).
BADGE_BLOCK = re.compile(
    r'<span class="badge[^"]*">(?:100% link-verified|Zero LLM arithmetic|'
    r"12 specialist agents|4\+ frontier models|7 quality gates|"
    r"Mobile-first audited)</span>\s*",
    re.MULTILINE,
)
# After stripping individual badges, an empty <div class="badges"></div> may
# remain. Collapse it.
EMPTY_BADGES_DIV = re.compile(
    r'<div class="badges">\s*</div>\s*',
    re.MULTILINE,
)
# The "By the numbers" stat grid in index.html. Match the full balanced block:
# <div class="stat">  ...  </div>  </div> ...  </div></div> — the closing
# count must equal opening count. We use a stricter handcrafted matcher.
STAT_GRID_HEADER = re.compile(
    r"<h2>By the numbers</h2>\s*",
)
STAT_GRID_OPEN = re.compile(r'<div class="stat">')

# Bundle size items that sometimes survive other passes.
BUNDLE_SIZE_ITEM = re.compile(
    r'\s*<div class="item"><div class="label">Bundle size[^<]*</div>'
    r'<div class="value">[^<]*</div></div>\s*',
    re.MULTILINE,
)
# Methodology / index also have other suspicious "stat" items with unverified
# counts. Strip the entire stat block on these pages.
ALL_STAT_GRID = re.compile(
    r'<h2>By the numbers</h2>\s*<div class="stat">[\s\S]*?</div>\s*</div>\s*',
)
# Bundle size / model-count claims in prose.
PROSE_BUNDLE_SIZE = re.compile(
    r"\.\s*Loads under 50\s*KB gzip\.",
)
PROSE_BUNDLE_SIZE_2 = re.compile(
    r"Loads under 50\s*KB gzip\.\s*",
)
# "Run" prefixes in plain text fingerprints (footer).
RUN_PREFIX_BARE = re.compile(r"\bRun\s+\d{8}T\d{6}Z\b")

# Internal IDs anywhere in the rendered prose (defensive).
INTERNAL_IDS = re.compile(r"\b(?:VM|CH|RL|PB|PLG|FM|DG|JS|SEG|CC|MM|SC|UC|FE)-\d{1,3}\b")


def replace_candidate(text: str) -> str:
    for full in CANDIDATE_FULL_LINES:
        text = full.sub("", text)
    text = CANDIDATE_POSSESSIVE.sub(r"\1 ", text)
    text = CANDIDATE_QUALIFIER.sub(r"\1 ", text)
    text = CANDIDATE_FOLLOWED_BY_LOWER.sub("", text)
    text = CANDIDATE_PLURAL.sub("options", text)
    text = CANDIDATE_BARE.sub("", text)
    return text


def strip_run_ids(text: str) -> str:
    text = HEADER_RUN_SPAN.sub("", text)
    text = HERO_RUN_META.sub("", text)
    text = FOOTER_RUN_LINE.sub("", text)
    text = RUN_BARE_PATH.sub("`the published evidence directory`", text)
    text = RUN_PATH.sub("the published evidence file", text)
    text = RUN_PREFIX_BARE.sub("", text)
    text = RUN_ID.sub("", text)
    return text


def strip_jargon(text: str) -> str:
    for pat, repl in JARGON_PAIRS:
        text = pat.sub(repl, text)
    return text


def _balanced_div_block(text: str, start_idx: int) -> int:
    """Return end-index (exclusive) of the balanced ``<div ...>...</div>``
    block starting at ``start_idx`` (which must point at a ``<div``)."""
    pos = start_idx
    depth = 0
    open_re = re.compile(r"<div\b", re.IGNORECASE)
    close_re = re.compile(r"</div>", re.IGNORECASE)
    while pos < len(text):
        next_open = open_re.search(text, pos)
        next_close = close_re.search(text, pos)
        if next_close is None:
            return -1  # unbalanced
        if next_open and next_open.start() < next_close.start():
            depth += 1
            pos = next_open.end()
        else:
            depth -= 1
            pos = next_close.end()
            if depth == 0:
                return pos
    return -1


def _strip_stat_grid(text: str) -> str:
    m = STAT_GRID_HEADER.search(text)
    if not m:
        return text
    open_m = STAT_GRID_OPEN.search(text, m.end())
    if not open_m:
        return text
    end = _balanced_div_block(text, open_m.start())
    if end == -1:
        return text
    # Also drop any trailing whitespace.
    while end < len(text) and text[end] in " \t\n":
        end += 1
    return text[: m.start()] + text[end:]


def strip_marketing(text: str) -> str:
    text = BADGE_BLOCK.sub("", text)
    text = EMPTY_BADGES_DIV.sub("", text)
    text = _strip_stat_grid(text)
    text = BUNDLE_SIZE_ITEM.sub("", text)
    text = PROSE_BUNDLE_SIZE.sub(".", text)
    text = PROSE_BUNDLE_SIZE_2.sub("", text)
    return text


def strip_internal_ids(text: str) -> str:
    return INTERNAL_IDS.sub("", text)


def normalise_whitespace(text: str) -> str:
    # Collapse trailing spaces.
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    # Collapse 3+ blank lines to 2.
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Collapse double-spaces.
    text = re.sub(r"  +", " ", text)
    return text


def sanitise_one(path: Path, *, dry_run: bool = False) -> tuple[bool, dict[str, int]]:
    original = path.read_text(encoding="utf-8")
    out = original
    out = strip_run_ids(out)
    out = replace_candidate(out)
    out = strip_jargon(out)
    out = strip_marketing(out)
    out = strip_internal_ids(out)
    out = normalise_whitespace(out)
    changed = out != original
    if changed and not dry_run:
        path.write_text(out, encoding="utf-8")
    # Stats
    stats: dict[str, int] = {
        "run_ids_removed": len(RUN_ID.findall(original)) - len(RUN_ID.findall(out)),
        "candidate_removed": (
            len(CANDIDATE_BARE.findall(original)) - len(CANDIDATE_BARE.findall(out))
        ),
        "internal_ids_removed": (
            len(INTERNAL_IDS.findall(original)) - len(INTERNAL_IDS.findall(out))
        ),
        "bytes_removed": max(0, len(original) - len(out)),
    }
    return changed, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Report only.")
    parser.add_argument(
        "--targets",
        nargs="*",
        default=None,
        help="Specific files (relative to reports/final/) to process.",
    )
    args = parser.parse_args()

    default_targets = [
        "index.html",
        "methodology.html",
        "padel-ai-coach-research.html",
        "evidence-map.html",
        "404.html",
    ]
    targets = args.targets if args.targets else default_targets

    total_changed = 0
    for name in targets:
        p = FINAL / name
        if not p.exists():
            print(f"[skip] {name} (not found)", file=sys.stderr)
            continue
        changed, stats = sanitise_one(p, dry_run=args.dry_run)
        verb = "would change" if args.dry_run else "changed" if changed else "unchanged"
        print(f"[{verb}] {name}: " + ", ".join(f"{k}={v}" for k, v in stats.items()))
        if changed:
            total_changed += 1

    print(f"\nTotal {'would-be-modified' if args.dry_run else 'modified'}: {total_changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
