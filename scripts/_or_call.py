#!/usr/bin/env python3
"""Tiny OpenRouter helper. Reads --model, --system, --user, and writes the
full JSON response to --out. No third-party deps, just urllib.

Usage:
  python3 scripts/_or_call.py \
    --model perplexity/sonar-deep-research \
    --system 'system prompt' \
    --user 'user prompt' \
    --max-tokens 4000 \
    --out evidence/RUN/_logs/sonar_deep_arm.json
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

API = "https://openrouter.ai/api/v1/chat/completions"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--system", default="")
    ap.add_argument("--user", required=True)
    ap.add_argument("--max-tokens", type=int, default=2400)
    ap.add_argument("--temperature", type=float, default=0.2)
    ap.add_argument("--out", required=True)
    ap.add_argument(
        "--reasoning",
        default=None,
        help="Optional reasoning effort: low|medium|high (Anthropic models).",
    )
    args = ap.parse_args()

    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("[_or_call] FAIL: OPENROUTER_API_KEY not set", file=sys.stderr)
        return 1

    msgs = []
    if args.system:
        msgs.append({"role": "system", "content": args.system})
    msgs.append({"role": "user", "content": args.user})

    body = {
        "model": args.model,
        "messages": msgs,
        "max_tokens": args.max_tokens,
        "temperature": args.temperature,
    }
    if args.reasoning:
        body["reasoning"] = {"effort": args.reasoning}

    req = urllib.request.Request(
        API,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://padel-research-os.local",
            "X-Title": "padel-research-os",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        print(f"[_or_call] HTTP {e.code}: {body_text[:600]}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"[_or_call] error: {e}", file=sys.stderr)
        return 3

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    print(f"[_or_call] wrote {out} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
