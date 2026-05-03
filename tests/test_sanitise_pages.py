"""Tests for ``scripts/sanitise_pages.py`` content transforms."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import sanitise_pages as sp  # noqa: E402

# --- candidate replacement ---------------------------------------------------


def test_candidate_qualifier_dropped() -> None:
    assert sp.replace_candidate("the candidate beachhead") == "the beachhead"


def test_candidate_possessive_dropped() -> None:
    assert sp.replace_candidate("the candidate's MVP") == "the MVP"


def test_candidate_followed_by_verb_dropped() -> None:
    assert sp.replace_candidate("a candidate operates here") == "a operates here"


def test_candidate_a_qualifier_dropped() -> None:
    assert sp.replace_candidate("a candidate value mechanic") == "a value mechanic"


def test_candidate_full_sentence_dropped() -> None:
    text = "The candidate is not a padel player. The product is."
    assert "candidate" not in sp.replace_candidate(text)


def test_candidates_plural_replaced() -> None:
    assert sp.replace_candidate("six candidates passed") == "six options passed"


# --- run-id stripping --------------------------------------------------------


def test_run_id_in_paragraph_stripped() -> None:
    text = "<p>see Run 20260501T135005Z</p>"
    assert "20260501T135005Z" not in sp.strip_run_ids(text)


def test_run_id_in_path_stripped() -> None:
    text = "see evidence/20260501T135005Z/file.json"
    out = sp.strip_run_ids(text)
    assert "20260501T135005Z" not in out
    assert "the published evidence file" in out


def test_run_id_header_span_stripped() -> None:
    text = '<header><span class="ext">Run 20260501T135005Z</span></header>'
    out = sp.strip_run_ids(text)
    assert "20260501T135005Z" not in out


# --- jargon ------------------------------------------------------------------


def test_kill_experiment_replaced() -> None:
    out = sp.strip_jargon("kill experiment results")
    assert "kill" not in out.lower() or "kill" not in out
    assert "stop test" in out


def test_red_team_replaced() -> None:
    out = sp.strip_jargon("after a red-team review")
    assert "adversarial review" in out


def test_b2b_expanded() -> None:
    out = sp.strip_jargon("a B2B sales motion")
    assert "business-to-business" in out


# --- marketing ---------------------------------------------------------------


def test_marketing_badge_removed() -> None:
    text = '<div><span class="badge good">100% link-verified</span></div>'
    out = sp.strip_marketing(text)
    assert "100% link-verified" not in out


def test_bundle_size_item_removed() -> None:
    text = (
        '<div class="stat">'
        '<div class="item"><div class="label">Bundle size</div>'
        '<div class="value">&lt; 50 KB</div></div></div>'
    )
    out = sp.strip_marketing(text)
    assert "Bundle size" not in out


def test_full_stat_grid_removed() -> None:
    text = """
<h2>By the numbers</h2>
<div class="stat">
  <div class="item"><div class="label">A</div><div class="value">1</div></div>
  <div class="item"><div class="label">B</div><div class="value">2</div></div>
</div>
<p>after</p>
""".strip()
    out = sp.strip_marketing(text)
    assert "By the numbers" not in out
    assert "after" in out


# --- internal IDs -----------------------------------------------------------


def test_vm_id_stripped() -> None:
    out = sp.strip_internal_ids("see VM-001 for details")
    assert "VM-001" not in out


def test_seg_id_stripped() -> None:
    out = sp.strip_internal_ids("the SEG-002 group passed")
    assert "SEG-002" not in out


# --- whitespace normalisation -----------------------------------------------


def test_triple_blank_lines_collapsed() -> None:
    out = sp.normalise_whitespace("a\n\n\n\nb")
    assert out == "a\n\nb"


def test_double_spaces_collapsed() -> None:
    out = sp.normalise_whitespace("foo  bar")
    assert out == "foo bar"


def test_trailing_spaces_stripped() -> None:
    out = sp.normalise_whitespace("foo   \nbar")
    assert "foo\nbar" in out
