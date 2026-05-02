#!/usr/bin/env python3
"""Every claim tagged with [VERIFIED]/[INFERRED] in reports must have an
adjacent source citation. Claims tagged [ABSENT] need no source."""
import argparse, pathlib, re, sys

CLAIM_TAG = re.compile(r"\[(VERIFIED|INFERRED|ABSENT)\]")
HAS_LINK  = re.compile(r"https?://[^\s)\]]+")

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--run-id", required=True); ap.add_argument("--phase", default=None)
    a = ap.parse_args()
    rep = pathlib.Path(f"reports/{a.run_id}")
    if not rep.exists():
        print("[check_citations] no report yet; skipping"); return 0
    fail = 0
    for f in rep.rglob("*"):
        if not f.is_file() or f.suffix.lower() not in {".md", ".html"}: continue
        text = f.read_text(encoding="utf-8", errors="ignore")
        # Scan paragraph by paragraph.
        for blk in re.split(r"\n\s*\n", text):
            tags = CLAIM_TAG.findall(blk)
            if any(t in ("VERIFIED","INFERRED") for t in tags):
                if not HAS_LINK.search(blk):
                    snippet = blk.strip().replace("\n"," ")[:140]
                    print(f"[check_citations] FAIL: {f}: VERIFIED/INFERRED claim without URL :: {snippet}", file=sys.stderr); fail += 1
    return 1 if fail else (print("[check_citations] ok") or 0)

if __name__ == "__main__":
    sys.exit(main())
