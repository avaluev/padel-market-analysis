#!/usr/bin/env python3
"""Enforce: at most ONE direct quote per source URL across the whole run.

The check inspects evidence/<run-id>/citations.jsonl, an append-only log
written by every prompt that pulls a source. Each line is:
    {"url": "...", "quote": "...", "phase": "NN", "file": "..."}

A run-level violation occurs when the same canonical URL appears with two
or more *distinct* quote strings.
"""
from __future__ import annotations
import argparse, json, pathlib, sys, urllib.parse, collections

def canon(url: str) -> str:
    p = urllib.parse.urlparse(url.strip())
    netloc = p.netloc.lower().lstrip("www.")
    path = p.path.rstrip("/")
    return f"{p.scheme}://{netloc}{path}"

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--phase", default=None)
    args = ap.parse_args()

    log = pathlib.Path(f"evidence/{args.run_id}/citations.jsonl")
    if not log.exists():
        print(f"[check_quote_dedup] no citations.jsonl yet (ok early on)")
        return 0

    by_url = collections.defaultdict(set)
    for line in log.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line: continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "quote" not in obj or not obj["quote"]:
            continue
        by_url[canon(obj.get("url", ""))].add(obj["quote"].strip())

    fail = 0
    for url, quotes in by_url.items():
        if len(quotes) > 1:
            print(f"[check_quote_dedup] FAIL: {url} has {len(quotes)} distinct quotes:", file=sys.stderr)
            for q in quotes:
                print(f"  - \"{q[:120]}\"", file=sys.stderr)
            fail += 1
    if fail:
        return 1
    print("[check_quote_dedup] clean.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
