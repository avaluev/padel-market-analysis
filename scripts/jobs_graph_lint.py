#!/usr/bin/env python3
"""Phase 05: jobs_graph.json is a DAG with >=1 critical chain marked."""

import argparse
import json
import pathlib
import sys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    a = ap.parse_args()
    p = pathlib.Path(f"evidence/{a.run_id}/05_jobs_graph.json")
    if not p.exists():
        print(f"[jobs_graph_lint] FAIL: missing {p}", file=sys.stderr)
        return 1
    try:
        g = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[jobs_graph_lint] FAIL: {e}", file=sys.stderr)
        return 1
    nodes = g.get("nodes", [])
    edges = g.get("edges", [])
    if not isinstance(nodes, list) or len(nodes) < 5:
        print("[jobs_graph_lint] FAIL: need >= 5 nodes", file=sys.stderr)
        return 1
    if not isinstance(edges, list) or len(edges) < 4:
        print("[jobs_graph_lint] FAIL: need >= 4 edges", file=sys.stderr)
        return 1
    ids = {n.get("id") for n in nodes if isinstance(n, dict)}
    for e in edges:
        if e.get("from") not in ids or e.get("to") not in ids:
            print(f"[jobs_graph_lint] FAIL: dangling edge {e}", file=sys.stderr)
            return 1
    cc = g.get("critical_chains", [])
    if not isinstance(cc, list) or not cc:
        print("[jobs_graph_lint] FAIL: at least one critical_chain required", file=sys.stderr)
        return 1
    print(f"[jobs_graph_lint] ok ({len(nodes)} nodes, {len(edges)} edges)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
