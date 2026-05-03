"""Unit tests for ``scripts/check_quality.py``.

Each gate is exercised with both a known-bad and a known-good fixture so
regressions are caught at the gate level rather than only at integration time.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_quality as cq  # noqa: E402


def write(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return p


# ---------------------------------------------------- check_h1_uniqueness


def test_h1_uniqueness_clean(tmp_path: Path) -> None:
    p = write(tmp_path, "ok.html", "<html><body><h1>One</h1></body></html>")
    assert list(cq.check_h1_uniqueness(p)) == []


def test_h1_uniqueness_duplicate(tmp_path: Path) -> None:
    p = write(tmp_path, "bad.html", "<html><body><h1>One</h1><h1>Two</h1></body></html>")
    violations = list(cq.check_h1_uniqueness(p))
    assert len(violations) >= 1
    assert violations[0].check == "h1_uniqueness"


# ----------------------------------------------------------- run_id


def test_run_id_clean(tmp_path: Path) -> None:
    p = write(tmp_path, "ok.html", "<p>2026-05-03 was the date.</p>")
    assert list(cq.check_no_run_id(p)) == []


def test_run_id_blocked(tmp_path: Path) -> None:
    p = write(tmp_path, "bad.html", "<p>Run 20260501T135005Z generated this.</p>")
    violations = list(cq.check_no_run_id(p))
    assert len(violations) == 1
    assert "20260501T135005Z" in violations[0].message


# ----------------------------------------------------------- candidate


def test_candidate_clean(tmp_path: Path) -> None:
    p = write(tmp_path, "ok.html", "<p>The team operates the platform.</p>")
    assert list(cq.check_no_candidate(p)) == []


def test_candidate_blocked(tmp_path: Path) -> None:
    p = write(tmp_path, "bad.html", "<p>The candidate operates the platform.</p>")
    violations = list(cq.check_no_candidate(p))
    assert len(violations) >= 1


def test_candidate_in_code_block_allowed(tmp_path: Path) -> None:
    p = write(tmp_path, "ok.html", "<p>fine</p><code>candidate variable</code>")
    assert list(cq.check_no_candidate(p)) == []


# ----------------------------------------------------------- jd_coverage


def test_jd_coverage_clean(tmp_path: Path) -> None:
    p = write(tmp_path, "ok.html", "<p>nothing to see here</p>")
    assert list(cq.check_no_jd_coverage(p)) == []


def test_jd_coverage_blocked(tmp_path: Path) -> None:
    p = write(tmp_path, "bad.html", '<p>see <a href="jd-coverage-map.html">map</a></p>')
    violations = list(cq.check_no_jd_coverage(p))
    assert len(violations) == 1


# ----------------------------------------------------------- jargon


def test_jargon_clean(tmp_path: Path) -> None:
    p = write(tmp_path, "ok.html", "<p>The exit criteria are clear.</p>")
    assert list(cq.check_jargon(p)) == []


def test_jargon_blocked(tmp_path: Path) -> None:
    p = write(tmp_path, "bad.html", "<p>The kill experiment will run.</p>")
    violations = list(cq.check_jargon(p))
    assert len(violations) >= 1
    assert "kill experiment" in violations[0].message


# ----------------------------------------------------------- marketing


def test_marketing_clean(tmp_path: Path) -> None:
    p = write(tmp_path, "ok.html", "<p>Some plain prose.</p>")
    assert list(cq.check_no_marketing_claims(p)) == []


def test_marketing_blocked(tmp_path: Path) -> None:
    p = write(tmp_path, "bad.html", '<span class="badge">100% link-verified</span>')
    violations = list(cq.check_no_marketing_claims(p))
    assert len(violations) >= 1


# ----------------------------------------------------------- link_syntax


def test_link_syntax_clean(tmp_path: Path) -> None:
    p = write(tmp_path, "ok.html", '<p><a href="https://x.com">x</a></p>')
    assert list(cq.check_html_link_syntax(p)) == []


def test_link_syntax_blocked(tmp_path: Path) -> None:
    p = write(tmp_path, "bad.html", "<p><https://example.com/page></p>")
    violations = list(cq.check_html_link_syntax(p))
    assert len(violations) >= 1


def test_link_syntax_in_code_block_allowed(tmp_path: Path) -> None:
    p = write(tmp_path, "ok.html", "<p><code>&lt;https://x&gt;</code></p>")
    assert list(cq.check_html_link_syntax(p)) == []


# ----------------------------------------------------------- internal_ids


def test_internal_ids_clean(tmp_path: Path) -> None:
    p = write(tmp_path, "ok.html", "<p>The first mechanic is the rating clarity.</p>")
    assert list(cq.check_no_internal_ids(p)) == []


def test_internal_ids_blocked(tmp_path: Path) -> None:
    p = write(tmp_path, "bad.html", "<p>See VM-001 for details.</p>")
    violations = list(cq.check_no_internal_ids(p))
    assert len(violations) >= 1


# ----------------------------------------------------------- meta_tags


def test_meta_tags_complete(tmp_path: Path) -> None:
    html = """<!doctype html><html><head>
<title>X</title>
<meta name="viewport" content="width=device-width">
<meta name="description" content="d">
<meta name="robots" content="index,follow">
<link rel="canonical" href="https://x.com/">
<meta property="og:title" content="X">
<meta property="og:description" content="d">
<meta property="og:url" content="https://x.com/">
</head></html>"""
    p = write(tmp_path, "ok.html", html)
    assert list(cq.check_meta_tags(p)) == []


def test_meta_tags_missing_canonical(tmp_path: Path) -> None:
    html = """<!doctype html><html><head>
<title>X</title>
<meta name="description" content="d">
<meta name="viewport" content="width=device-width">
</head></html>"""
    p = write(tmp_path, "bad.html", html)
    violations = list(cq.check_meta_tags(p))
    assert any(v.message.startswith("missing canonical") for v in violations)


# ----------------------------------------------------------- jsonld


def test_jsonld_present(tmp_path: Path) -> None:
    html = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebPage"}</script>'
    p = write(tmp_path, "ok.html", html)
    assert list(cq.check_jsonld(p)) == []


def test_jsonld_missing(tmp_path: Path) -> None:
    p = write(tmp_path, "bad.html", "<html></html>")
    violations = list(cq.check_jsonld(p))
    assert len(violations) == 1
    assert violations[0].check == "jsonld"


def test_jsonld_invalid(tmp_path: Path) -> None:
    html = '<script type="application/ld+json">{not valid json</script>'
    p = write(tmp_path, "bad.html", html)
    violations = list(cq.check_jsonld(p))
    assert len(violations) == 1
    assert "invalid" in violations[0].message


# ----------------------------------------------------------- image_attrs


def test_image_attrs_complete(tmp_path: Path) -> None:
    p = write(tmp_path, "ok.html", '<img src="x.png" alt="x" width="100" height="50">')
    assert list(cq.check_image_attrs(p)) == []


def test_image_attrs_missing_alt(tmp_path: Path) -> None:
    p = write(tmp_path, "bad.html", '<img src="x.png">')
    violations = list(cq.check_image_attrs(p))
    assert any("alt" in v.message for v in violations)


# ----------------------------------------------------------- internal_links


def test_internal_links_valid(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "other.html"
    target.write_text("ok")
    p = write(tmp_path, "ok.html", '<a href="other.html">x</a>')
    monkeypatch.setattr(cq, "FINAL", tmp_path)
    monkeypatch.setattr(cq, "ROOT", tmp_path)
    assert list(cq.check_internal_links(p)) == []


def test_internal_links_broken(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    p = write(tmp_path, "bad.html", '<a href="missing.html">x</a>')
    monkeypatch.setattr(cq, "FINAL", tmp_path)
    monkeypatch.setattr(cq, "ROOT", tmp_path)
    violations = list(cq.check_internal_links(p))
    assert len(violations) == 1


# ----------------------------------------------------------- nav_consistency


def test_nav_consistency_complete(tmp_path: Path) -> None:
    nav = (
        '<nav class="nav-links">'
        + "".join(
            f'<a href="{h}">x</a>'
            for h in [
                "index.html",
                "padel-ai-coach-research.html",
                "evidence-map.html",
                "competitor-landscape.html",
                "subscription-economics.html",
                "mvp-design.html",
                "90-day-plan.html",
                "methodology.html",
                "model-provenance.html",
            ]
        )
        + "</nav>"
    )
    p = write(tmp_path, "ok.html", nav)
    violations = list(cq.check_nav_consistency(p))
    assert all(v.severity != "error" for v in violations)


def test_nav_consistency_missing(tmp_path: Path) -> None:
    nav = '<nav class="nav-links"><a href="index.html">Home</a></nav>'
    p = write(tmp_path, "bad.html", nav)
    violations = list(cq.check_nav_consistency(p))
    assert any("missing links" in v.message for v in violations)


# ----------------------------------------------------------- end-to-end run


def test_run_returns_violation_list(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    p = write(tmp_path, "x.html", "<h1>One</h1><h1>Two</h1>")
    monkeypatch.setattr(cq, "FINAL", tmp_path)
    monkeypatch.setattr(cq, "ROOT", tmp_path)
    violations = cq.run(["h1"])
    assert any(v.check == "h1_uniqueness" for v in violations)


def test_run_filter_unknown_check_raises(tmp_path: Path) -> None:
    # The CLI handles this; the run() function just iterates the requested set.
    # An unknown check yields no violations.
    assert cq.run(["nonexistent"]) == []
