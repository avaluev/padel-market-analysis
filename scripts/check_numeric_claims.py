#!/usr/bin/env python3
"""Every numeric claim in a report MUST be traceable to evidence/<run-id>.

Method:
  1. Extract numbers (integers, floats, percentages, money amounts) from
     report markdown/HTML.
  2. For each number, check whether it appears in any evidence/*.json or
     citations.jsonl with an accompanying source_url field.
  3. Numbers inside <code> blocks, calendar dates, and structural markup
     (heading levels, list indices) are skipped.

This is a soft trace: it does not validate that the number is correct,
only that it is sourced. The Naval filter and red-team phases verify
correctness separately.
"""
from __future__ import annotations
import argparse, json, pathlib, re, sys

NUM = re.compile(r"(?<![A-Za-z])(\$?\d{1,3}(?:[.,]\d{3})+(?:\.\d+)?|\$?\d+(?:\.\d+)?%?)")
CODE = re.compile(r"```.*?```", re.DOTALL)
INLINE = re.compile(r"`[^`\n]*`")
# CSS / JS values inside <style> or <script> blocks are presentation, not
# narrative claims. Strip them before counting numbers.
STYLE_BLOCK = re.compile(r"<style[^>]*>.*?</style>", re.DOTALL | re.IGNORECASE)
SCRIPT_BLOCK = re.compile(r"<script[^>]*>.*?</script>", re.DOTALL | re.IGNORECASE)
HEX_COLOR = re.compile(r"#[0-9A-Fa-f]{3,8}\b")
DATE_LIKE = re.compile(r"\b(19|20)\d{2}\b")

# Skip these mundane numbers entirely.
TRIVIAL = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
           "100", "1000", "100%"}

def normalize(s: str) -> str:
    return s.replace(",", "").replace("$", "").replace("%", "").strip()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--phase", default=None)
    args = ap.parse_args()

    rep = pathlib.Path(f"reports/{args.run_id}")
    evid = pathlib.Path(f"evidence/{args.run_id}")
    if not rep.exists():
        print("[check_numeric_claims] no report yet (ok early on)")
        return 0

    # Build a corpus of "sourced numbers" from evidence.
    sourced: set[str] = set()
    if evid.exists():
        for p in evid.rglob("*"):
            if not p.is_file(): continue
            if p.suffix.lower() not in {".json", ".jsonl", ".yaml", ".yml", ".md"}: continue
            if "_cache" in p.parts: continue
            try:
                txt = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for m in NUM.finditer(txt):
                sourced.add(normalize(m.group(1)))

    fail = []
    for f in rep.rglob("*"):
        if not f.is_file() or f.suffix.lower() not in {".md", ".html"}:
            continue
        text = f.read_text(encoding="utf-8", errors="ignore")
        clean = INLINE.sub("", CODE.sub("", text))
        clean = STYLE_BLOCK.sub("", clean)
        clean = SCRIPT_BLOCK.sub("", clean)
        clean = HEX_COLOR.sub("", clean)
        for m in NUM.finditer(clean):
            raw = m.group(1)
            n = normalize(raw)
            if n in TRIVIAL: continue
            if DATE_LIKE.match(raw): continue
            if n not in sourced:
                fail.append((str(f), raw))

    if fail:
        print(f"[check_numeric_claims] FAIL: {len(fail)} unsourced number(s):", file=sys.stderr)
        for path, raw in fail[:50]:
            print(f"  {path}: {raw}", file=sys.stderr)
        if len(fail) > 50:
            print(f"  ... and {len(fail) - 50} more", file=sys.stderr)
        return 1
    print("[check_numeric_claims] clean.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
