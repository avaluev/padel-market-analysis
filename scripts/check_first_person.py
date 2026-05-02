#!/usr/bin/env python3
"""Block first-person pronouns from generated reports and synthesis files.

The contract: reports/<run-id>/** and the synthesized canonical brief MUST
NOT contain first-person pronouns. Prompt files, agent definitions, and
operating policy are OUT of scope (those are instructions to the model).

Allow-list: code blocks (text inside ``` fences) are skipped because they
may contain quoted source material, JSON keys named "we_believe", etc.
"""
from __future__ import annotations
import argparse, pathlib, re, sys

PRONOUNS = re.compile(
    r"(?<![A-Za-z'])(I|I'm|I've|I'll|I'd|we|We|we're|we've|we'll|we'd|"
    r"my|My|mine|Mine|our|Our|ours|Ours|us|Us|me|Me|myself|Myself|"
    r"ourselves|Ourselves)(?![A-Za-z'])"
)

CODE_FENCE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]*`")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
URL_RX = re.compile(r"https?://[A-Za-z0-9._/?=&%#:+~,@\-]+")
HTML_TAG = re.compile(r"<[^>]+>")
HTML_ATTR = re.compile(r"\s(href|src|alt|title|aria-[a-z]+|class|id|name|action|content|value|data-[a-z0-9_-]+)\s*=\s*\"[^\"]*\"", re.I)

# Strings that legitimately contain pronoun substrings (allow them through):
ALLOWED_TOKENS = {
    "API", "AI", "UI", "USP", "CI", "MVI", "MVP",  # acronyms
    "Italy", "Iberian", "iOS",  # geos / platforms
}

def strip_safe(text: str) -> str:
    text = CODE_FENCE.sub("", text)
    text = INLINE_CODE.sub("", text)
    text = HTML_COMMENT.sub("", text)
    text = URL_RX.sub(" ", text)
    text = HTML_ATTR.sub(" ", text)
    return text

def scan_file(path: pathlib.Path) -> list[tuple[int,str,str]]:
    hits = []
    try:
        raw = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return hits
    cleaned = strip_safe(raw)
    for i, line in enumerate(cleaned.splitlines(), 1):
        for m in PRONOUNS.finditer(line):
            tok = m.group(1)
            if tok in ALLOWED_TOKENS:
                continue
            hits.append((i, tok, line.strip()[:160]))
    return hits

def targets_for(run_id: str) -> list[pathlib.Path]:
    roots = [
        pathlib.Path(f"reports/{run_id}"),
        pathlib.Path(f"evidence/{run_id}/canonical_brief.json"),
        pathlib.Path(f"evidence/{run_id}/canonical_brief.md"),
    ]
    out: list[pathlib.Path] = []
    for r in roots:
        if r.is_dir():
            out.extend(p for p in r.rglob("*") if p.is_file()
                       and p.suffix.lower() in {".md", ".html", ".txt", ".json", ".yaml", ".yml"})
        elif r.is_file():
            out.append(r)
    return out

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--phase", default=None)
    args = ap.parse_args()

    files = targets_for(args.run_id)
    if not files:
        print(f"[check_first_person] no target files yet for run {args.run_id} (ok in early phases)")
        return 0

    total = 0
    for f in files:
        hits = scan_file(f)
        if hits:
            for ln, tok, snippet in hits:
                print(f"[check_first_person] {f}:{ln}: '{tok}' :: {snippet}", file=sys.stderr)
            total += len(hits)

    if total > 0:
        print(f"[check_first_person] FAIL: {total} first-person pronoun(s) found.", file=sys.stderr)
        return 1
    print("[check_first_person] clean.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
