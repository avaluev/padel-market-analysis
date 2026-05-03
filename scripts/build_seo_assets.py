#!/usr/bin/env python3
"""Build the AI-search-optimisation assets for the public site.

Generates these files under ``reports/final/``:

- ``robots.txt`` — AI-crawler-aware allow/disallow per the 2026 reference
  template. Allows GPTBot, OAI-SearchBot, ClaudeBot family, PerplexityBot,
  Google-Extended, Applebot-Extended; blocks the deprecated Claude-Web
  and the no-respect Bytespider crawler.
- ``llms.txt`` — concise machine-readable index per the llmstxt.org spec.
- ``llms-full.txt`` — full plain-text concatenation of every published
  page's body content, for LLM training and citation use.
- ``sitemap.xml`` — XML sitemap with lastmod from the file mtime.
- ``humans.txt`` — human credit file.
- ``feed.xml`` — RSS feed of pages.
- ``.well-known/security.txt`` — RFC 9116 security policy.
- ``manifest.webmanifest`` — minimal PWA manifest.

Sources for the AI-crawler list and llms.txt format are documented in
``evidence/research/ai-search-optimization/SUMMARY.md``.

Usage::

    python3 scripts/build_seo_assets.py

Idempotent. Safe to re-run.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FINAL = ROOT / "reports/final"

SITE_ORIGIN = "https://avaluev.github.io/padel-market-analysis"
SITE_TITLE = "Padel Coaching Tech Research"
SITE_AUTHOR = "Alexandr Valuev"
SITE_DESCRIPTION = (
    "Independent, evidence-graded research on padel coaching technology — "
    "competitor landscape, subscription economics, MVP design, and operating plan. "
    "Every claim cites a verifiable source URL."
)
LICENSE_URL = "https://www.apache.org/licenses/LICENSE-2.0"

# Page registry. Order matters for sitemap and llms.txt.
# Entries: (filename, title, summary, lastmod_overide_or_None)
PAGES: list[tuple[str, str, str]] = [
    (
        "index.html",
        "Padel Coaching Tech Research — Home",
        "Landing page for the research portfolio. Links to the strategic brief, the evidence map, the competitor analysis, the subscription economics work, and the MVP design.",
    ),
    (
        "padel-ai-coach-research.html",
        "Padel AI Coaching Platform — Strategic Brief",
        "The full strategic brief: market sizing, jobs to be done, competitive landscape, defensibility analysis, go-to-market thinking, risk register, and pivot triggers. Eighteen sections, every numeric claim cited.",
    ),
    (
        "evidence-map.html",
        "Evidence Map — Source Trace",
        "Source trace for the strategic brief. Every claim cross-referenced to the verbatim source quote and the URL fetched at runtime.",
    ),
    (
        "methodology.html",
        "Methodology — How This Research Was Built",
        "The pipeline that produced the research: multi-agent orchestration, multi-model fan-out, evidence gates, mobile-first rendering, adversarial review.",
    ),
    (
        "competitor-landscape.html",
        "Padel Coaching Tech: Competitor Landscape",
        "Independent analysis of padel coaching apps, club-management software, and racket-sport AI. Who has data moats, where the white space is, what failed and why.",
    ),
    (
        "subscription-economics.html",
        "Padel App Subscription Economics: Pricing, Churn, LTV/CAC",
        "How a padel coaching subscription would price against eight verified anchors, with monthly churn, LTV/CAC by channel, and four geographic scenarios.",
    ),
    (
        "mvp-design.html",
        "Padel AI MVP Design: Capture, Insight, Practice Loop",
        "Visual-first MVP design: a three-stage product loop, three pilot tracks compared, a decision tree, and a five-row risk register. Plain language, no jargon.",
    ),
    (
        "90-day-plan.html",
        "Padel AI Platform: First 90 Days Operating Plan",
        "Twelve testable hypotheses, a metric tree from headline number to weekly leading indicators, and a risk register with named exit criteria.",
    ),
    (
        "model-provenance.html",
        "Model Provenance: Every AI Model Used",
        "Full disclosure of every model invoked across the pipeline, the role each played, and the billing class.",
    ),
]


def _abs(href: str) -> str:
    return f"{SITE_ORIGIN}/{href}"


def _file_lastmod_iso(name: str) -> str:
    p = FINAL / name
    if p.exists():
        ts = dt.datetime.fromtimestamp(p.stat().st_mtime, tz=dt.UTC)
        return ts.strftime("%Y-%m-%dT%H:%M:%SZ")
    return dt.datetime.now(tz=dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------- robots.txt

ROBOTS_TXT = f"""\
# robots.txt — AI search visibility profile (2026)
#
# Goal: stay citable in ChatGPT, Claude, Perplexity, Gemini, and Copilot
# search surfaces, while opting out of training-only ingestion where the
# crawler is a separate user agent.
#
# References:
#   - https://developers.openai.com/api/docs/bots
#   - https://privacy.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
#   - https://llmstxt.org/

# ---- Standard search engines ----
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: DuckDuckBot
Allow: /

# ---- OpenAI ----
# GPTBot — foundation-model training crawler
User-agent: GPTBot
Allow: /

# OAI-SearchBot — powers ChatGPT Search citations
User-agent: OAI-SearchBot
Allow: /

# ChatGPT-User — user-initiated fetches
User-agent: ChatGPT-User
Allow: /

# ---- Anthropic (three separate bots; rules are independent) ----
User-agent: ClaudeBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

# Deprecated Anthropic agents
User-agent: anthropic-ai
Disallow: /

User-agent: Claude-Web
Disallow: /

# ---- Google AI ----
# Google-Extended controls only AI training, not Search ranking.
User-agent: Google-Extended
Allow: /

# ---- Perplexity ----
User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

# ---- Apple ----
User-agent: Applebot
Allow: /

User-agent: Applebot-Extended
Allow: /

# ---- Common Crawl (powers many downstream LLMs) ----
User-agent: CCBot
Allow: /

# ---- Cohere ----
User-agent: cohere-ai
Disallow: /

User-agent: cohere-training-data-crawler
Disallow: /

# ---- ByteDance ----
# Poor robots.txt-respect history; block by default.
User-agent: Bytespider
Disallow: /

# ---- Catch-all for unknown crawlers ----
User-agent: *
Allow: /

Sitemap: {SITE_ORIGIN}/sitemap.xml
"""


# ------------------------------------------------------------------ llms.txt


def build_llms_txt() -> str:
    lines = [
        f"# {SITE_TITLE}",
        "",
        f"> {SITE_DESCRIPTION}",
        "",
        f"Author: {SITE_AUTHOR}. License: Apache 2.0. Repository: https://github.com/avaluev/padel-market-analysis.",
        "",
        "## Reports",
    ]
    for name, title, summary in PAGES:
        if name == "index.html":
            continue
        if name == "404.html":
            continue
        lines.append(f"- [{title}]({_abs(name)}): {summary}")
    lines.append("")
    lines.append("## Optional")
    lines.append(
        f"- [Site index]({_abs('index.html')}): Landing page; the report links above are the substantive content."
    )
    lines.append(
        f"- [Full text]({_abs('llms-full.txt')}): All page bodies concatenated for retrieval contexts."
    )
    lines.append("")
    return "\n".join(lines)


# ------------------------------------------------------------ llms-full.txt


class _BodyExtractor(HTMLParser):
    """Extract visible text from <main> only, dropping nav/script/style."""

    SKIP = {"script", "style", "nav", "header", "footer", "aside", "noscript", "svg"}

    def __init__(self) -> None:
        super().__init__()
        self.depth = 0
        self.skip_depth = 0
        self.in_main = False
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        t = tag.lower()
        if t == "main":
            self.in_main = True
            return
        if not self.in_main:
            return
        if t in self.SKIP:
            self.skip_depth += 1
            return
        # Block-level paragraph hint: insert a newline so prose paragraphs split.
        if t in {"p", "h1", "h2", "h3", "h4", "li", "tr", "blockquote", "br", "hr"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        t = tag.lower()
        if t == "main":
            self.in_main = False
            return
        if t in self.SKIP and self.skip_depth > 0:
            self.skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.in_main and self.skip_depth == 0:
            self.parts.append(data)

    def text(self) -> str:
        raw = "".join(self.parts)
        # Collapse runs of whitespace, preserve paragraph breaks.
        out_lines: list[str] = []
        for line in raw.splitlines():
            stripped = re.sub(r"[ \t]+", " ", line).strip()
            if stripped:
                out_lines.append(stripped)
        return "\n\n".join(out_lines)


def build_llms_full_txt() -> str:
    out: list[str] = [f"# {SITE_TITLE} — Full text\n"]
    for name, title, summary in PAGES:
        p = FINAL / name
        if not p.exists():
            continue
        ext = _BodyExtractor()
        try:
            ext.feed(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        body = ext.text()
        if not body:
            continue
        out.append(f"\n\n# {title}\n\nSource URL: {_abs(name)}\n\n{summary}\n\n---\n\n{body}\n")
    return "".join(out)


# ----------------------------------------------------------------- sitemap


def build_sitemap_xml() -> str:
    urlset = ET.Element(
        "urlset",
        attrib={
            "xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9",
            "xmlns:xhtml": "http://www.w3.org/1999/xhtml",
        },
    )
    for name, _title, _summary in PAGES:
        u = ET.SubElement(urlset, "url")
        ET.SubElement(u, "loc").text = _abs(name)
        ET.SubElement(u, "lastmod").text = _file_lastmod_iso(name)
        # Priority: home highest, then strategic brief, then others.
        pr = (
            "1.0"
            if name == "index.html"
            else "0.9"
            if name == "padel-ai-coach-research.html"
            else "0.8"
        )
        ET.SubElement(u, "priority").text = pr
        ET.SubElement(u, "changefreq").text = "monthly"
    # Pretty-print
    ET.indent(urlset, space="  ")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(urlset, encoding="unicode")


# ------------------------------------------------------------------- feed


def build_rss_feed() -> str:
    now = dt.datetime.now(tz=dt.UTC).strftime("%a, %d %b %Y %H:%M:%S +0000")
    items = []
    for name, title, summary in PAGES:
        if name == "index.html":
            continue
        items.append(f"""    <item>
      <title><![CDATA[{title}]]></title>
      <link>{_abs(name)}</link>
      <guid isPermaLink="true">{_abs(name)}</guid>
      <description><![CDATA[{summary}]]></description>
      <pubDate>{now}</pubDate>
    </item>""")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title><![CDATA[{SITE_TITLE}]]></title>
    <link>{SITE_ORIGIN}/</link>
    <atom:link href="{SITE_ORIGIN}/feed.xml" rel="self" type="application/rss+xml" />
    <description><![CDATA[{SITE_DESCRIPTION}]]></description>
    <language>en</language>
    <copyright>Apache 2.0 licensed</copyright>
    <lastBuildDate>{now}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
"""


# ----------------------------------------------------------------- humans

HUMANS_TXT = f"""\
/* TEAM */
Researcher and engineer: {SITE_AUTHOR}
LinkedIn: https://www.linkedin.com/in/valuev/
GitHub:   https://github.com/avaluev
Telegram: https://t.me/ASNKT

/* THANKS */
The work draws on public research, open-source padel computer-vision projects,
and the published pricing pages of every vendor referenced in the brief.
Every quote is verbatim from the cited URL and was fetched at the time of
writing.

/* SITE */
Last update:   {dt.date.today().isoformat()}
Language:      English
Doctype:       HTML5
IDE:           Claude Code
"""


# --------------------------------------------------------------- security

SECURITY_TXT = f"""\
Contact: https://www.linkedin.com/in/valuev/
Expires: {(dt.date.today() + dt.timedelta(days=365)).isoformat()}T00:00:00.000Z
Preferred-Languages: en, ru
Canonical: {SITE_ORIGIN}/.well-known/security.txt
Policy: https://github.com/avaluev/padel-market-analysis/blob/main/SECURITY.md
"""


# ----------------------------------------------------------------- manifest

MANIFEST_JSON = """\
{
  "name": "Padel Coaching Tech Research",
  "short_name": "Padel Research",
  "description": "Evidence-graded research on padel coaching technology.",
  "start_url": "/padel-market-analysis/",
  "scope": "/padel-market-analysis/",
  "display": "browser",
  "background_color": "#ffffff",
  "theme_color": "#0a6cf3",
  "icons": [
    {"src": "favicon.svg", "type": "image/svg+xml", "sizes": "any"},
    {"src": "apple-touch-icon.png", "type": "image/png", "sizes": "180x180"}
  ],
  "lang": "en",
  "dir": "ltr",
  "categories": ["research", "education", "sports"]
}
"""


# ----------------------------------------------------------------- favicon

# Minimal SVG favicon — blue dot, matches the brand colour.
FAVICON_SVG = """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="8" fill="#0a6cf3"/>
  <text x="16" y="22" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="20" fill="#ffffff">P</text>
</svg>
"""


# ------------------------------------------------------------------- main


def write(path: Path, content: str) -> bool:
    """Write only if content differs. Returns True if written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify only, no writes.")
    args = parser.parse_args()

    artifacts: list[tuple[Path, str]] = [
        (FINAL / "robots.txt", ROBOTS_TXT),
        (FINAL / "llms.txt", build_llms_txt()),
        (FINAL / "llms-full.txt", build_llms_full_txt()),
        (FINAL / "sitemap.xml", build_sitemap_xml()),
        (FINAL / "feed.xml", build_rss_feed()),
        (FINAL / "humans.txt", HUMANS_TXT),
        (FINAL / ".well-known" / "security.txt", SECURITY_TXT),
        (FINAL / "manifest.webmanifest", MANIFEST_JSON),
        (FINAL / "favicon.svg", FAVICON_SVG),
    ]

    written = 0
    for path, content in artifacts:
        rel = path.relative_to(FINAL)
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                print(f"[stale] {rel}", file=sys.stderr)
                return 1
            print(f"[ok]    {rel}")
            continue
        did = write(path, content)
        verb = "wrote" if did else "nochange"
        print(f"[{verb}] {rel} ({len(content):,} bytes)")
        if did:
            written += 1

    if not args.check:
        print(f"\nTotal new/changed: {written}/{len(artifacts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
