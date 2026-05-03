#!/usr/bin/env python3
"""Merge raw peer mentions from multiple research arms into a deduped list.
Dedup key: canonical URL (scheme + host + path, lowercased).
"""

import argparse
import json
import pathlib
import sys
import urllib.parse


def canon(u: str) -> str:
    p = urllib.parse.urlparse(u.strip())
    return f"{p.scheme}://{p.netloc.lower().lstrip('www.')}{p.path.rstrip('/')}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    a = ap.parse_args()
    raw = pathlib.Path(f"evidence/{a.run_id}/03_peers_raw.jsonl")
    out = pathlib.Path(f"evidence/{a.run_id}/03_peers_dedup.json")
    if not raw.exists():
        print(f"[merge_peers] FAIL: missing {raw}", file=sys.stderr)
        return 1
    by_url: dict[str, dict] = {}
    for line in raw.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except:
            continue
        u = o.get("url")
        if not u:
            continue
        k = canon(u)
        if k not in by_url:
            by_url[k] = {**o, "arms": []}
        arm = o.get("arm") or o.get("source_model") or "unknown"
        if arm not in by_url[k]["arms"]:
            by_url[k]["arms"].append(arm)
        by_url[k]["multi_arm"] = len(by_url[k]["arms"]) > 1
    merged = list(by_url.values())
    merged.sort(key=lambda x: (-len(x.get("arms", [])), x.get("name", "")))
    out.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[merge_peers] wrote {out} ({len(merged)} peers)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
