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
        ts = dt.datetime.fromtimestamp(p.stat().st_mtime, tz=dt.timezone.utc)
        return ts.strftime("%Y-%m-%dT%H:%M:%SZ")
    return dt.datetime.now(tz=dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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


class _HtmlToMarkdown(HTMLParser):
    """Convert the <main> region of a published page into clean Markdown.

    Preserves heading hierarchy (h1–h6), paragraphs, bullet and numbered
    lists (with nesting), tables (as Markdown tables), blockquotes, code
    blocks, links, bold, italic, inline code, and horizontal rules.

    Skips entire subtrees of: ``<nav>``, ``<header>``, ``<footer>``,
    ``<aside>``, ``<noscript>``, ``<svg>``, ``<style>``, ``<script>``.
    """

    SKIP_TAGS = frozenset({"nav", "header", "footer", "aside", "noscript", "svg",
                           "style", "script"})

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_main = False
        self.skip_depth = 0
        self.out: list[str] = []
        # Per-block state.
        self.list_stack: list[str] = []  # "ul" or "ol"
        self.ol_counters: list[int] = []
        self.in_pre = False
        self.in_code = False
        self.in_blockquote = False
        # Table state.
        self.in_table = False
        self.table_rows: list[list[str]] = []
        self.in_thead = False
        self.in_tr = False
        self.cell_buf: list[str] = []
        self.in_cell = False
        # Inline state — buffer until we hit a block boundary.
        self.text_buf: list[str] = []
        # Link state.
        self.link_stack: list[str] = []  # list of href attrs
        # Heading state.
        self.heading_level: int | None = None

    # --- helpers ---------------------------------------------------------

    def _flush_paragraph(self) -> None:
        text = "".join(self.text_buf).strip()
        self.text_buf = []
        if not text:
            return
        # Inside a list item / blockquote / cell, append to the current
        # context. Otherwise emit as a paragraph.
        if self.in_cell:
            self.cell_buf.append(text)
            return
        if self.list_stack:
            indent = "  " * (len(self.list_stack) - 1)
            marker = "-" if self.list_stack[-1] == "ul" else f"{self.ol_counters[-1]}."
            if self.list_stack[-1] == "ol":
                self.ol_counters[-1] += 1
            # Collapse all internal whitespace runs to a single space.
            text = re.sub(r"\s+", " ", text)
            self.out.append(f"{indent}{marker} {text}")
            return
        if self.in_blockquote:
            for line in text.splitlines():
                self.out.append(f"> {line}")
            self.out.append("")
            return
        # Plain paragraph — preserve line breaks at sentence-ish boundaries
        # but collapse runs of whitespace within sentences.
        text = re.sub(r"[ \t]+", " ", text)
        self.out.append(text)
        self.out.append("")

    def _emit_blank(self) -> None:
        if self.out and self.out[-1] != "":
            self.out.append("")

    # --- start tags ------------------------------------------------------

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        t = tag.lower()
        if t == "main":
            self.in_main = True
            return
        if not self.in_main:
            return
        if t in self.SKIP_TAGS:
            self.skip_depth += 1
            return
        if self.skip_depth > 0:
            return
        if t in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._flush_paragraph()
            self._emit_blank()
            self.heading_level = int(t[1])
            return
        if t == "p":
            self._flush_paragraph()
            return
        if t == "br":
            self.text_buf.append("  \n")
            return
        if t == "hr":
            self._flush_paragraph()
            self._emit_blank()
            self.out.append("---")
            self._emit_blank()
            return
        if t == "ul":
            self._flush_paragraph()
            self._emit_blank()
            self.list_stack.append("ul")
            return
        if t == "ol":
            self._flush_paragraph()
            self._emit_blank()
            self.list_stack.append("ol")
            self.ol_counters.append(1)
            return
        if t == "li":
            self._flush_paragraph()
            return
        if t == "blockquote":
            self._flush_paragraph()
            self._emit_blank()
            self.in_blockquote = True
            return
        if t == "pre":
            self._flush_paragraph()
            self._emit_blank()
            self.in_pre = True
            self.out.append("```")
            return
        if t == "code" and not self.in_pre:
            self.text_buf.append("`")
            self.in_code = True
            return
        if t == "table":
            self._flush_paragraph()
            self._emit_blank()
            self.in_table = True
            self.table_rows = []
            return
        if t == "thead":
            self.in_thead = True
            return
        if t == "tr":
            self.in_tr = True
            self.table_rows.append([])
            return
        if t in {"th", "td"}:
            self.in_cell = True
            self.cell_buf = []
            return
        if t in {"strong", "b"}:
            self.text_buf.append("**")
            return
        if t in {"em", "i"}:
            self.text_buf.append("*")
            return
        if t == "a":
            href = ""
            for k, v in attrs:
                if k.lower() == "href" and v:
                    href = v
                    break
            self.link_stack.append(href)
            self.text_buf.append("[")
            return
        if t == "div":
            # Many pages use <div class="stat"><div class="item">…</div></div>
            # to display key/value pairs. Treat each div boundary as a soft
            # paragraph break so the items don't run together as one line.
            self._flush_paragraph()
            return
        if t == "figure":
            self._flush_paragraph()
            self._emit_blank()
            return
        if t == "figcaption":
            self.text_buf.append("*")
            return

    # --- end tags --------------------------------------------------------

    def handle_endtag(self, tag: str) -> None:
        t = tag.lower()
        if t == "main":
            self._flush_paragraph()
            self.in_main = False
            return
        if not self.in_main:
            return
        if t in self.SKIP_TAGS:
            if self.skip_depth > 0:
                self.skip_depth -= 1
            return
        if self.skip_depth > 0:
            return
        if t in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            text = re.sub(r"\s+", " ", "".join(self.text_buf).strip())
            self.text_buf = []
            if text and self.heading_level is not None:
                hashes = "#" * self.heading_level
                self.out.append(f"{hashes} {text}")
                self.out.append("")
            self.heading_level = None
            return
        if t == "p":
            self._flush_paragraph()
            return
        if t == "ul":
            self._flush_paragraph()
            if self.list_stack and self.list_stack[-1] == "ul":
                self.list_stack.pop()
            if not self.list_stack:
                self._emit_blank()
            return
        if t == "ol":
            self._flush_paragraph()
            if self.list_stack and self.list_stack[-1] == "ol":
                self.list_stack.pop()
                if self.ol_counters:
                    self.ol_counters.pop()
            if not self.list_stack:
                self._emit_blank()
            return
        if t == "li":
            self._flush_paragraph()
            return
        if t == "blockquote":
            self._flush_paragraph()
            self.in_blockquote = False
            self._emit_blank()
            return
        if t == "pre":
            # Whatever's in text_buf is pre content.
            content = "".join(self.text_buf).strip("\n")
            self.text_buf = []
            for line in content.splitlines():
                self.out.append(line)
            self.out.append("```")
            self._emit_blank()
            self.in_pre = False
            return
        if t == "code" and self.in_code and not self.in_pre:
            self.text_buf.append("`")
            self.in_code = False
            return
        if t == "table":
            # Render the accumulated rows as a Markdown table.
            if self.table_rows:
                # Pick the widest row to define column count.
                cols = max((len(r) for r in self.table_rows), default=0)
                if cols > 0:
                    # Pad each row to `cols` cells.
                    norm = [r + [""] * (cols - len(r)) for r in self.table_rows]
                    header = norm[0] if norm else [""] * cols
                    body = norm[1:] if len(norm) > 1 else []
                    self.out.append("| " + " | ".join(header) + " |")
                    self.out.append("|" + "|".join(["---"] * cols) + "|")
                    for r in body:
                        self.out.append("| " + " | ".join(r) + " |")
                    self._emit_blank()
            self.in_table = False
            self.table_rows = []
            return
        if t == "thead":
            self.in_thead = False
            return
        if t == "tr":
            self.in_tr = False
            return
        if t in {"th", "td"}:
            cell_text = re.sub(r"\s+", " ", "".join(self.cell_buf).strip())
            cell_text = cell_text.replace("|", "\\|")
            if self.table_rows:
                self.table_rows[-1].append(cell_text)
            self.in_cell = False
            self.cell_buf = []
            return
        if t in {"strong", "b"}:
            self.text_buf.append("**")
            return
        if t in {"em", "i"}:
            self.text_buf.append("*")
            return
        if t == "a":
            href = self.link_stack.pop() if self.link_stack else ""
            if href:
                self.text_buf.append(f"]({href})")
            else:
                self.text_buf.append("]")
            return
        if t == "div":
            self._flush_paragraph()
            return
        if t == "figure":
            self._flush_paragraph()
            self._emit_blank()
            return
        if t == "figcaption":
            self.text_buf.append("*")
            return

    # --- text ------------------------------------------------------------

    def handle_data(self, data: str) -> None:
        if not self.in_main or self.skip_depth > 0:
            return
        if self.in_cell:
            self.cell_buf.append(data)
            return
        if self.in_pre:
            self.text_buf.append(data)
            return
        # Strip leading/trailing newlines added by HTML formatting; keep
        # internal whitespace structure for inline.
        self.text_buf.append(data)

    def to_markdown(self) -> str:
        self._flush_paragraph()
        # Tidy: collapse 3+ blank lines, strip trailing whitespace.
        out = "\n".join(self.out)
        out = re.sub(r"[ \t]+$", "", out, flags=re.MULTILINE)
        out = re.sub(r"\n{3,}", "\n\n", out)
        return out.strip()


def _sanitise_md(text: str) -> str:
    """Apply the same defensive scrubs the public pages already pass.
    Defence-in-depth: even if a stray reference slipped through the page,
    it must not appear in llms-full.txt."""
    # Run-IDs.
    text = re.sub(r"\b\d{8}T\d{6}Z\b", "", text)
    # Internal IDs (VM-001, CH-006, …).
    text = re.sub(r"\b(?:VM|CH|RL|PB|PLG|FM|DG|JS|SEG|CC|MM|SC|UC|FE)-\d{1,3}\b", "", text)
    # Broken sanitisation residue.
    text = text.replace(
        "the published evidence published evidence", "the published evidence"
    )
    text = re.sub(r"reports/(?:interview_pack|sources)/the published evidence(?: published evidence)?",
                  "the published evidence file", text)
    # Empty bold / italic from <strong></strong> or <em></em>.
    text = re.sub(r"\*\*\*\*", "", text)
    text = re.sub(r"(?<!\*)\*\*(?!\*)", "", text) if False else text  # leave non-paired ** alone
    # Lines that are nothing but emphasis markers.
    text = re.sub(r"^[\s\*_]+$", "", text, flags=re.MULTILINE)
    # Collapse extra whitespace.
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# Map output slug → optional source markdown file. When present, the
# source markdown is used directly (cleaner structure, citation density)
# in preference to round-tripping through the rendered HTML.
SOURCE_MARKDOWN: dict[str, str] = {
    "competitor-landscape.html": "01_competitor_intelligence.md",
    "subscription-economics.html": "02_subscription_economics.md",
    "mvp-design.html": "03_mvp_loop_design.md",
    "90-day-plan.html": "04_30_60_90_plan.md",
    "model-provenance.html": "06_model_provenance.md",
}


def _markdown_for_page(name: str, title: str) -> str:
    """Return the Markdown body for a single page, choosing the cleanest
    available source: the original markdown when we have it, the rendered
    HTML's <main> region otherwise."""
    src_md = SOURCE_MARKDOWN.get(name)
    if src_md:
        src_path = ROOT / "reports/sources/deliverables" / src_md
        if src_path.exists():
            text = src_path.read_text(encoding="utf-8")
            # Strip the H1 (the consumer page already prints the page title).
            text = re.sub(r"^#\s+.+\n+", "", text, count=1)
            # Strip the boilerplate metadata block (Deliverable, Audience, …).
            text = re.sub(
                r"(?:^\*\*(?:Deliverable|Audience|Voice|Posture|Backing data|Anchor evidence|Run anchor):\*\*[^\n]*\n)+",
                "",
                text,
                flags=re.MULTILINE,
            )
            return _sanitise_md(text)
    # Fall back to extracting <main> from the rendered HTML.
    html_path = FINAL / name
    if not html_path.exists():
        return ""
    converter = _HtmlToMarkdown()
    try:
        converter.feed(html_path.read_text(encoding="utf-8"))
    except Exception:
        return ""
    return _sanitise_md(converter.to_markdown())


def build_llms_full_txt() -> str:
    """Render llms-full.txt as a clean Markdown corpus.

    Per llmstxt.org, ``llms-full.txt`` is the comprehensive single-file
    reference. Markdown structure is preserved so retrieval contexts can
    chunk on headings, lists, and tables rather than flat prose.
    """
    sections: list[str] = []
    sections.append(f"# {SITE_TITLE} — Full Reference\n")
    sections.append(f"> {SITE_DESCRIPTION}\n")
    sections.append(
        f"_Author: {SITE_AUTHOR}. License: Apache 2.0._  "
        f"_Repository: <https://github.com/avaluev/padel-market-analysis>._\n"
    )
    sections.append(
        "_This file concatenates every published page in markdown for "
        "retrieval contexts. Page boundaries are marked by `# Page: …` "
        "headings. The original page lives at the canonical URL noted "
        "directly under each heading._\n"
    )
    sections.append("\n---\n")

    for name, title, summary in PAGES:
        # The site landing page is mostly nav links; skip it.
        if name in {"index.html", "404.html"}:
            continue
        body = _markdown_for_page(name, title)
        if not body:
            continue
        canonical = _abs(name)
        sections.append(f"\n## Page: {title}\n")
        sections.append(f"_Canonical: <{canonical}>_\n")
        sections.append(f"> {summary}\n")
        sections.append("\n" + body + "\n")
        sections.append("\n---\n")

    return "\n".join(sections).strip() + "\n"
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
    now = dt.datetime.now(tz=dt.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
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
