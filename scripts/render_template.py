#!/usr/bin/env python3
"""Render examples/report-template.html using reports/<run-id>/data.json.

Substitution mode: simple {{path.to.key}} replacements only. Lists are
rendered via {{#each path}} ... {{/each}} blocks (Mustache-flavoured but
implemented with regex; no third-party dep).
"""

import argparse
import html as htmllib
import json
import pathlib
import re
import sys


def get(d, path):
    cur = d
    for p in path.split("."):
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        elif isinstance(cur, list):
            try:
                cur = cur[int(p)]
            except:
                return ""
        else:
            return ""
    return cur


def render_each(template: str, data) -> str:
    pat = re.compile(r"\{\{#each\s+([\w\.]+)\}\}(.*?)\{\{/each\}\}", re.DOTALL)

    def repl(m):
        path, body = m.group(1), m.group(2)
        items = get(data, path)
        if not isinstance(items, list):
            return ""
        out = []
        for it in items:
            sub = body
            for var_m in re.finditer(r"\{\{this\.([\w\.]+)\}\}", body):
                sub = sub.replace(
                    var_m.group(0), htmllib.escape(str(get(it, var_m.group(1)) or ""))
                )
            sub = sub.replace(
                "{{this}}", htmllib.escape(str(it) if not isinstance(it, (dict, list)) else "")
            )
            out.append(sub)
        return "".join(out)

    while pat.search(template):
        template = pat.sub(repl, template)
    return template


def render_vars(template: str, data) -> str:
    """Render {{path.to.key}} with HTML-escaping. A triple-brace
    {{{path.to.key}}} variant emits the value as raw HTML — used for
    fields the data-builder pre-escapes (summary_html, narrative blocks
    that need inline anchors).
    """

    def repl_raw(m):
        v = get(data, m.group(1))
        if v is None:
            return ""
        if isinstance(v, (dict, list)):
            return ""
        return str(v)

    def repl(m):
        v = get(data, m.group(1))
        if v is None:
            return ""
        if isinstance(v, (dict, list)):
            return ""
        return htmllib.escape(str(v))

    template = re.sub(r"\{\{\{([\w\.]+)\}\}\}", repl_raw, template)
    return re.sub(r"\{\{([\w\.]+)\}\}", repl, template)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    a = ap.parse_args()
    tpl = pathlib.Path("examples/report-template.html").read_text(encoding="utf-8")
    data = json.loads(pathlib.Path(f"reports/{a.run_id}/data.json").read_text(encoding="utf-8"))
    rendered = render_each(tpl, data)
    rendered = render_vars(rendered, data)
    out = pathlib.Path(f"reports/{a.run_id}/index.html")
    out.write_text(rendered, encoding="utf-8")
    print(f"[render_template] wrote {out} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
