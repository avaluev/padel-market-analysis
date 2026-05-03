#!/usr/bin/env python3
"""Unified quality gate for the public site under ``reports/final/``.

Runs every content and SEO check the project promises to enforce. Each
check returns a list of structured violations; the script aggregates and
prints a JSON report. Exits 1 if any check finds a violation, 0 otherwise.

Usage::

    python3 scripts/check_quality.py             # check all
    python3 scripts/check_quality.py --json      # machine-readable output
    python3 scripts/check_quality.py --check h1  # run a specific check
    python3 scripts/check_quality.py --list      # list available checks

The exit code makes this CI-friendly. Add it to ``run_pipeline.sh`` and
to the GitHub Actions ``quality-gates.yml`` workflow.

Each check is defined below as ``check_<name>`` and registered in the
``CHECKS`` table. To add a new check, write a function that takes a
``Path`` and returns ``Iterable[Violation]``, then add it to ``CHECKS``.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections.abc import Callable, Iterable
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FINAL = ROOT / "reports/final"

# Files outside reports/final/ that are part of the public site.
WELL_KNOWN_FILES = [
    "robots.txt",
    "sitemap.xml",
    "llms.txt",
    "llms-full.txt",
    "feed.xml",
    "humans.txt",
    "manifest.webmanifest",
    "favicon.svg",
    ".well-known/security.txt",
]


# All HTML pages in the public site (relative to FINAL).
def all_html_pages() -> list[Path]:
    return sorted(FINAL.glob("*.html"))


def _rel(path: Path) -> str:
    """Render ``path`` relative to ROOT when possible, else as a string."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


@dataclass
class Violation:
    check: str
    file: str
    line: int = 0
    message: str = ""
    severity: str = "error"  # error | warn | info

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------- helpers


def find_lines(text: str, pattern: re.Pattern[str]) -> list[tuple[int, str]]:
    """Return (line_no, matched_text) for every regex match."""
    out: list[tuple[int, str]] = []
    for i, line in enumerate(text.splitlines(), start=1):
        for m in pattern.finditer(line):
            out.append((i, m.group(0)))
    return out


def html_text_outside(tags_to_skip: set[str], html: str) -> str:
    """Return the text content of ``html`` with the named tags' contents
    elided. Used to make checks ignore content inside <script>/<style>/<code>/<pre>."""

    class Filter(HTMLParser):
        def __init__(self) -> None:
            super().__init__()
            self.skip_depth = 0
            self.parts: list[str] = []

        def handle_starttag(self, tag, attrs):
            if tag.lower() in tags_to_skip:
                self.skip_depth += 1

        def handle_endtag(self, tag):
            if tag.lower() in tags_to_skip and self.skip_depth > 0:
                self.skip_depth -= 1

        def handle_data(self, data):
            if self.skip_depth == 0:
                self.parts.append(data)

    f = Filter()
    f.feed(html)
    return "".join(f.parts)


# ---------------------------------------------------------------- checks


def check_h1_uniqueness(path: Path) -> Iterable[Violation]:
    text = path.read_text(encoding="utf-8")
    h1s = re.findall(r"<h1\b[^>]*>.*?</h1>", text, re.IGNORECASE | re.DOTALL)
    if len(h1s) > 1:
        # Find line numbers for each H1 to make the violation actionable.
        for i, line in enumerate(text.splitlines(), start=1):
            if re.search(r"<h1\b", line, re.IGNORECASE):
                yield Violation(
                    "h1_uniqueness",
                    _rel(path),
                    i,
                    "Multiple <h1> tags found; expected exactly one",
                )


def check_no_run_id(path: Path) -> Iterable[Violation]:
    text = path.read_text(encoding="utf-8")
    pat = re.compile(r"\b\d{8}T\d{6}Z\b")
    for line_no, match in find_lines(text, pat):
        yield Violation(
            "no_run_id",
            _rel(path),
            line_no,
            f"Run-ID timestamp leaked into public page: {match}",
        )


def check_no_candidate(path: Path) -> Iterable[Violation]:
    text = html_text_outside({"code", "pre", "script", "style"}, path.read_text(encoding="utf-8"))
    pat = re.compile(r"\b[Cc]andidate(s)?\b")
    # Note: we strip code/pre, but match positions reference the original text.
    raw = path.read_text(encoding="utf-8")
    for line_no, match in find_lines(raw, pat):
        # Only flag if the match also appears in the stripped text (a
        # reasonable proxy for "outside code blocks").
        if pat.search(text):
            yield Violation(
                "no_candidate",
                _rel(path),
                line_no,
                f"'candidate' framing leaked into prose: {match}",
            )
            break  # one violation per file is enough; user fixes them in bulk


def check_no_jd_coverage(path: Path) -> Iterable[Violation]:
    text = path.read_text(encoding="utf-8")
    pat = re.compile(r"jd[- ]?coverage[- ]?map", re.IGNORECASE)
    for line_no, match in find_lines(text, pat):
        yield Violation(
            "no_jd_coverage",
            _rel(path),
            line_no,
            f"Reference to deleted jd-coverage-map page: {match}",
        )


JARGON_BLOCKLIST = [
    r"\bkill experiment(s)?\b",
    r"\bkill criteri(?:on|a)\b",
    r"\bkill threshold(s)?\b",
    r"\bkill signal(s)?\b",
    r"\bkill metric(s)?\b",
    r"\bnorth star metric\b",
    r"\bWizard of Oz\b",
    r"\banti[- ]pattern(s)?\b",
    r"\bdata_gaps?\b",
    r"\bred[- ]team(?:ed|ing)?\b",  # "red team" — replace with "adversarial review"
]
JARGON_PATTERN = re.compile("|".join(JARGON_BLOCKLIST), re.IGNORECASE)


def check_jargon(path: Path) -> Iterable[Violation]:
    text = html_text_outside({"code", "pre", "script", "style"}, path.read_text(encoding="utf-8"))
    raw = path.read_text(encoding="utf-8")
    if JARGON_PATTERN.search(text):
        for line_no, match in find_lines(raw, JARGON_PATTERN):
            yield Violation(
                "jargon",
                _rel(path),
                line_no,
                f"Jargon term in user-facing prose: {match!r} — use plain English",
            )


MARKETING_PHRASES = [
    "100% link-verified",
    "Zero LLM arithmetic",
    "12 specialist agents",
    "4+ frontier models",
    "7 quality gates",
    "Mobile-first audited",
    "Bundle size",
    "< 50 KB",
    "<50 KB",
]
MARKETING_PATTERN = re.compile("|".join(re.escape(p) for p in MARKETING_PHRASES))


def check_no_marketing_claims(path: Path) -> Iterable[Violation]:
    text = path.read_text(encoding="utf-8")
    for line_no, match in find_lines(text, MARKETING_PATTERN):
        yield Violation(
            "no_marketing_claims",
            _rel(path),
            line_no,
            f"Unverified marketing badge / claim: {match!r}",
        )


# `<https://...>` literal text outside <code>/<pre> means the markdown
# auto-link syntax was not converted to <a href>.
def check_html_link_syntax(path: Path) -> Iterable[Violation]:
    raw = path.read_text(encoding="utf-8")
    # Strip code blocks and pre blocks before checking — `<https://...>` is
    # legitimate inside escaped code samples.
    stripped = re.sub(r"<code\b[^>]*>.*?</code>", "", raw, flags=re.DOTALL | re.IGNORECASE)
    stripped = re.sub(r"<pre\b[^>]*>.*?</pre>", "", stripped, flags=re.DOTALL | re.IGNORECASE)
    pat = re.compile(r"<https?://[^>\s]+>")
    if pat.search(stripped):
        for line_no, match in find_lines(raw, pat):
            yield Violation(
                "html_link_syntax",
                _rel(path),
                line_no,
                f"Unconverted <URL> markdown auto-link: {match[:60]}",
            )


# Internal ID leaks (VM-001, CH-006, etc) in public-facing prose.
INTERNAL_ID_PATTERN = re.compile(r"\b(?:VM|CH|RL|PB|PLG|FM|DG|JS|SEG|CC|MM|SC|UC|FE)-\d{1,3}\b")


def check_no_internal_ids(path: Path) -> Iterable[Violation]:
    text = html_text_outside({"code", "pre", "script", "style"}, path.read_text(encoding="utf-8"))
    raw = path.read_text(encoding="utf-8")
    if INTERNAL_ID_PATTERN.search(text):
        for line_no, match in find_lines(raw, INTERNAL_ID_PATTERN):
            yield Violation(
                "no_internal_ids",
                _rel(path),
                line_no,
                f"Internal identifier in prose: {match}",
            )


def check_meta_tags(path: Path) -> Iterable[Violation]:
    text = path.read_text(encoding="utf-8")
    required: list[tuple[str, re.Pattern[str], str]] = [
        ("title", re.compile(r"<title>[^<]+</title>", re.IGNORECASE), "missing <title>"),
        (
            "description",
            re.compile(
                r'<meta\s+name=["\']description["\']\s+content=["\'][^"\']+["\']', re.IGNORECASE
            ),
            "missing meta description",
        ),
        (
            "canonical",
            re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\'][^"\']+["\']', re.IGNORECASE),
            "missing canonical link",
        ),
        (
            "og:title",
            re.compile(r'<meta\s+property=["\']og:title["\']', re.IGNORECASE),
            "missing og:title",
        ),
        (
            "og:description",
            re.compile(r'<meta\s+property=["\']og:description["\']', re.IGNORECASE),
            "missing og:description",
        ),
        (
            "og:url",
            re.compile(r'<meta\s+property=["\']og:url["\']', re.IGNORECASE),
            "missing og:url",
        ),
        (
            "viewport",
            re.compile(r'<meta\s+name=["\']viewport["\']', re.IGNORECASE),
            "missing viewport",
        ),
        (
            "robots",
            re.compile(r'<meta\s+name=["\']robots["\']', re.IGNORECASE),
            "missing meta robots",
        ),
    ]
    for tag, pat, msg in required:
        if not pat.search(text):
            yield Violation(
                "meta_tags",
                _rel(path),
                0,
                f"{msg} (required for AI-search optimisation)",
                severity="error" if tag in {"title", "description", "canonical"} else "warn",
            )


def check_jsonld(path: Path) -> Iterable[Violation]:
    text = path.read_text(encoding="utf-8")
    blocks = re.findall(
        r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>',
        text,
        re.DOTALL | re.IGNORECASE,
    )
    if not blocks:
        yield Violation(
            "jsonld",
            _rel(path),
            0,
            "No JSON-LD structured data found (required for AI-search citations)",
        )
        return
    for i, block in enumerate(blocks):
        try:
            data = json.loads(block.strip())
        except json.JSONDecodeError as e:
            yield Violation(
                "jsonld",
                _rel(path),
                0,
                f"JSON-LD block {i + 1} is invalid: {e}",
            )
            continue
        if not isinstance(data, (dict, list)):
            continue
        items = data if isinstance(data, list) else [data]
        for item in items:
            if isinstance(item, dict) and item.get("@context") != "https://schema.org":
                yield Violation(
                    "jsonld",
                    _rel(path),
                    0,
                    f"JSON-LD block {i + 1} missing @context=https://schema.org",
                    severity="warn",
                )


def check_image_attrs(path: Path) -> Iterable[Violation]:
    text = path.read_text(encoding="utf-8")
    # Find every <img> tag.
    for m in re.finditer(r"<img\b([^>]*)>", text, re.IGNORECASE):
        attrs = m.group(1)
        line_no = text[: m.start()].count("\n") + 1
        if not re.search(r"\balt\s*=", attrs, re.IGNORECASE):
            yield Violation(
                "image_attrs",
                _rel(path),
                line_no,
                "<img> missing alt attribute (accessibility + LLM context)",
            )
        if not re.search(r"\bwidth\s*=", attrs, re.IGNORECASE):
            yield Violation(
                "image_attrs",
                _rel(path),
                line_no,
                "<img> missing width (Core Web Vitals — CLS)",
                severity="warn",
            )


def check_internal_links(path: Path) -> Iterable[Violation]:
    text = path.read_text(encoding="utf-8")
    # Find every internal link (href without scheme).
    for m in re.finditer(r'href=["\']([^"\']+)["\']', text):
        href = m.group(1)
        if href.startswith(("http://", "https://", "mailto:", "tel:", "#", "/")):
            continue
        if "#" in href:
            href = href.split("#", 1)[0]
        if not href:
            continue
        target = (FINAL / href).resolve()
        if not target.exists():
            line_no = text[: m.start()].count("\n") + 1
            yield Violation(
                "internal_links",
                _rel(path),
                line_no,
                f"Broken internal link: {m.group(1)} -> {href}",
            )


def check_nav_consistency(path: Path) -> Iterable[Violation]:
    """Every page should have the same set of nav links."""
    text = path.read_text(encoding="utf-8")
    nav_match = re.search(
        r'<nav[^>]*class="nav-links"[^>]*>(.*?)</nav>', text, re.DOTALL | re.IGNORECASE
    )
    if not nav_match:
        yield Violation(
            "nav_consistency",
            _rel(path),
            0,
            "Page is missing the standard <nav class='nav-links'> block",
        )
        return
    hrefs = set(re.findall(r'href=["\']([^"\']+)["\']', nav_match.group(1)))
    expected = {
        "index.html",
        "padel-ai-coach-research.html",
        "evidence-map.html",
        "competitor-landscape.html",
        "subscription-economics.html",
        "mvp-design.html",
        "90-day-plan.html",
        "methodology.html",
        "model-provenance.html",
    }
    missing = expected - hrefs
    extra = hrefs - expected
    if missing:
        yield Violation(
            "nav_consistency",
            _rel(path),
            0,
            f"Nav missing links: {sorted(missing)}",
        )
    if extra:
        yield Violation(
            "nav_consistency",
            _rel(path),
            0,
            f"Nav has unexpected links: {sorted(extra)}",
            severity="warn",
        )


def check_seo_assets() -> Iterable[Violation]:
    """Site-wide check: every required SEO asset exists and is non-empty."""
    for name in WELL_KNOWN_FILES:
        p = FINAL / name
        if not p.exists():
            yield Violation(
                "seo_assets",
                _rel(p),
                0,
                f"Required SEO asset missing: {name}",
            )
            continue
        if p.stat().st_size == 0:
            yield Violation(
                "seo_assets",
                _rel(p),
                0,
                f"SEO asset is empty: {name}",
            )
    # Also validate sitemap is parseable XML.
    sm = FINAL / "sitemap.xml"
    if sm.exists():
        try:
            ET.parse(sm)
        except ET.ParseError as e:
            yield Violation(
                "seo_assets", _rel(sm), 0, f"sitemap.xml is malformed: {e}"
            )
    # llms.txt must start with `# ` (H1 per spec).
    llms = FINAL / "llms.txt"
    if llms.exists():
        first = llms.read_text(encoding="utf-8").lstrip().split("\n", 1)[0]
        if not first.startswith("# "):
            yield Violation(
                "seo_assets",
                _rel(llms),
                1,
                "llms.txt must start with H1 ('# Title')",
            )


# ---------------------------------------------------------------- registry

PER_PAGE_CHECKS: dict[str, Callable[[Path], Iterable[Violation]]] = {
    "h1": check_h1_uniqueness,
    "run_id": check_no_run_id,
    "candidate": check_no_candidate,
    "jd_coverage": check_no_jd_coverage,
    "jargon": check_jargon,
    "marketing": check_no_marketing_claims,
    "link_syntax": check_html_link_syntax,
    "internal_ids": check_no_internal_ids,
    "meta": check_meta_tags,
    "jsonld": check_jsonld,
    "images": check_image_attrs,
    "links": check_internal_links,
    "nav": check_nav_consistency,
}

SITE_WIDE_CHECKS: dict[str, Callable[[], Iterable[Violation]]] = {
    "seo_assets": check_seo_assets,
}

ALL_CHECK_NAMES = list(PER_PAGE_CHECKS.keys()) + list(SITE_WIDE_CHECKS.keys())


def run(selected: list[str] | None = None) -> list[Violation]:
    selected = selected or ALL_CHECK_NAMES
    violations: list[Violation] = []
    pages = all_html_pages()
    for check_name, fn in PER_PAGE_CHECKS.items():
        if check_name not in selected:
            continue
        for page in pages:
            for v in fn(page):
                violations.append(v)
    for check_name, fn in SITE_WIDE_CHECKS.items():
        if check_name not in selected:
            continue
        for v in fn():
            violations.append(v)
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="append", help="Run only the named check(s).")
    parser.add_argument("--list", action="store_true", help="List available checks and exit.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    if args.list:
        for name in ALL_CHECK_NAMES:
            scope = "per-page" if name in PER_PAGE_CHECKS else "site"
            print(f"{name:14s}  {scope}")
        return 0

    if args.check:
        unknown = set(args.check) - set(ALL_CHECK_NAMES)
        if unknown:
            print(f"Unknown checks: {sorted(unknown)}", file=sys.stderr)
            return 2

    violations = run(args.check)
    errors = [v for v in violations if v.severity == "error"]

    if args.json:
        payload = {
            "total_violations": len(violations),
            "errors": len(errors),
            "warnings": len([v for v in violations if v.severity == "warn"]),
            "violations": [v.to_dict() for v in violations],
        }
        print(json.dumps(payload, indent=2))
    else:
        # Group by check name for readability.
        from collections import defaultdict

        groups: dict[str, list[Violation]] = defaultdict(list)
        for v in violations:
            groups[v.check].append(v)
        for check_name in sorted(groups.keys()):
            vs = groups[check_name]
            err_count = sum(1 for v in vs if v.severity == "error")
            warn_count = len(vs) - err_count
            print(f"\n[{check_name}] {len(vs)} total ({err_count} error, {warn_count} warn)")
            for v in vs[:20]:  # cap output per check
                loc = f"{v.file}:{v.line}" if v.line else v.file
                marker = "ERR " if v.severity == "error" else "WARN"
                print(f"  {marker} {loc}  {v.message}")
            if len(vs) > 20:
                print(f"  ... and {len(vs) - 20} more")
        if not violations:
            print("All quality gates passed.")
        else:
            print(f"\n{len(errors)} error(s), {len(violations) - len(errors)} warning(s).")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
