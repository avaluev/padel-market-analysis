#!/usr/bin/env python3
"""Hard ceiling on direct quotes: <= 15 words per quote.

The contract is about *direct verbatim quotes from a verified source URL* —
not every double-quoted string in a JSON property. An earlier implementation
flagged every long string in evidence/<run-id>/*.json because JSON values are
syntactically wrapped in straight double quotes; that was an over-reach
documented in evidence/_failures/2026-05-01_quote_lengths_overreach.md.

Current scope:
  - .md / .markdown : markdown blockquote lines (`> …`), <blockquote> blocks,
                      and curly-quoted pull-quotes ("…") inside narrative text.
                      Lines that are inside fenced code (``` …  ``` ) are skipped.
  - .html           : <blockquote>…</blockquote> contents only. HTML attribute
                      strings and anchor labels are not "direct quotes."
  - .json / .yaml / .yml / .txt: never scanned (structured data, not narrative).

This change preserves the original intent: an explicit quoted citation in
authored prose still trips the gate at >15 words, but property values inside
structured evidence files do not.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

CQUOTE_RX = re.compile(r"“([^”\n]{3,})”")
BLOCK_RX = re.compile(r"<blockquote[^>]*>(.*?)</blockquote>", re.DOTALL | re.IGNORECASE)
MD_BLOCK_RX = re.compile(r"(?:^|\n)(>\s+[^\n]+(?:\n>\s+[^\n]+)*)", re.MULTILINE)
CODE_FENCE = re.compile(r"```.*?```", re.DOTALL)

LIMIT = 15
NARRATIVE_SUFFIXES = {".md", ".markdown", ".html"}


def words(s: str) -> int:
    return len([w for w in re.split(r"\s+", s.strip()) if w])


def scan(path: pathlib.Path) -> list[tuple[str, int]]:
    suffix = path.suffix.lower()
    if suffix not in NARRATIVE_SUFFIXES:
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    if suffix in {".md", ".markdown"}:
        # Strip fenced code blocks before scanning.
        text = CODE_FENCE.sub("", text)
    findings: list[tuple[str, int]] = []
    # Curly-quoted pull-quotes — used as deliberate quoted material.
    for m in CQUOTE_RX.finditer(text):
        q = m.group(1).strip()
        n = words(q)
        if n > LIMIT:
            findings.append((q[:160], n))
    # HTML <blockquote> blocks.
    for m in BLOCK_RX.finditer(text):
        q = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        n = words(q)
        if n > LIMIT:
            findings.append((q[:160], n))
    # Markdown blockquote lines (groups of `> …`).
    if suffix in {".md", ".markdown"}:
        for m in MD_BLOCK_RX.finditer(text):
            q = re.sub(r"^>\s+", "", m.group(1), flags=re.MULTILINE).strip()
            n = words(q)
            if n > LIMIT:
                findings.append((q[:160], n))
    return findings


def targets(run_id: str) -> list[pathlib.Path]:
    out: list[pathlib.Path] = []
    for root in (pathlib.Path(f"reports/{run_id}"), pathlib.Path(f"evidence/{run_id}")):
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix.lower() not in NARRATIVE_SUFFIXES:
                continue
            if "_cache" in p.parts or "_arms" in p.parts or "_logs" in p.parts:
                continue
            out.append(p)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--phase", default=None)
    args = ap.parse_args()
    fail = 0
    for f in targets(args.run_id):
        for q, n in scan(f):
            print(f'[check_quote_lengths] {f}: {n} words :: "{q}"', file=sys.stderr)
            fail += 1
    if fail:
        print(
            f"[check_quote_lengths] FAIL: {fail} over-length quote(s) (>{LIMIT} words).",
            file=sys.stderr,
        )
        return 1
    print("[check_quote_lengths] clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
