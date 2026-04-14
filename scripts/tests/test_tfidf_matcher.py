"""Stream D.1 TF-IDF concept matcher — deterministic, flag-gated, tests <1s."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from vitruvius.features import Features
from vitruvius.concepts.tfidf_matcher import (
    ConceptCandidate,
    MatchReport,
    split_into_sections,
    build_tfidf_matrix,
    score_concept,
    match_concepts,
)


SAMPLE_MARKDOWN = """# PD 1096 Excerpt

## SECTION 804. Stairs, Exits, and Occupant Loads

Every stairway shall have a minimum exit width of 1.12 meters measured clear
of any obstruction. Required exit width shall be computed from the occupancy
load of the floor served. Exit width is a critical life-safety concept.

## SECTION 805. Lighting and Ventilation

Every room intended for human occupation shall be provided with natural
lighting and ventilation. The light and ventilation area shall be a
minimum of ten percent of the floor area.

## SECTION 806. Yards and Open Spaces

Every building shall maintain adequate yards and open courts on all sides
consistent with fire safety, lighting, and ventilation. The minimum yard
depth shall be two meters.
"""


def _write_fixture(tmp_path: Path) -> Path:
    p = tmp_path / "pd1096_excerpt.md"
    p.write_text(SAMPLE_MARKDOWN)
    return p


def test_split_into_sections_parses_atx_headings():
    sections = split_into_sections(SAMPLE_MARKDOWN)
    titles = [title for title, _body in sections]
    assert "SECTION 804. Stairs, Exits, and Occupant Loads" in titles
    assert "SECTION 805. Lighting and Ventilation" in titles
    assert "SECTION 806. Yards and Open Spaces" in titles


def test_tfidf_matches_exit_width_to_stairs_section(tmp_path: Path):
    features = Features(flags={"d_tfidf_concepts": True})
    report = match_concepts(
        features=features,
        concept_slugs=["exit-width"],
        markdown_paths=[_write_fixture(tmp_path)],
        threshold=0.0,
    )
    assert report.below_threshold, "expected at least one candidate"
    top = report.below_threshold[0]
    assert top.concept_slug == "exit-width"
    assert "804" in top.section_title or "Stairs" in top.section_title


def test_tfidf_ignores_common_words(tmp_path: Path):
    """'the', 'shall', 'and' are stopwords; a concept slug 'the-building' should
    not match purely on those tokens."""
    features = Features(flags={"d_tfidf_concepts": True})
    report = match_concepts(
        features=features,
        concept_slugs=["the-building"],
        markdown_paths=[_write_fixture(tmp_path)],
        threshold=0.0,
    )
    # Stopword-only slugs should score effectively zero on every section.
    for cand in report.below_threshold:
        assert cand.score < 0.1, f"common-word slug scored unreasonably high: {cand}"


def test_deterministic_ranking(tmp_path: Path):
    features = Features(flags={"d_tfidf_concepts": True})
    r1 = match_concepts(
        features=features,
        concept_slugs=["exit-width", "yards"],
        markdown_paths=[_write_fixture(tmp_path)],
        threshold=0.0,
    )
    r2 = match_concepts(
        features=features,
        concept_slugs=["exit-width", "yards"],
        markdown_paths=[_write_fixture(tmp_path)],
        threshold=0.0,
    )
    assert [(c.concept_slug, c.section_title, round(c.score, 6)) for c in r1.below_threshold] \
        == [(c.concept_slug, c.section_title, round(c.score, 6)) for c in r2.below_threshold]


def test_writes_candidates_json(tmp_path: Path):
    features = Features(flags={"d_tfidf_concepts": True})
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    report = match_concepts(
        features=features,
        concept_slugs=["exit-width"],
        markdown_paths=[_write_fixture(tmp_path)],
        threshold=0.0,
        runs_dir=runs_dir,
    )
    out = runs_dir / "latest_tfidf_concept_match.json"
    assert out.exists()
    data = json.loads(out.read_text())
    assert "matched" in data and "below_threshold" in data
    assert "threshold" in data


def test_flag_off_is_noop(tmp_path: Path):
    features = Features(flags={})  # flag implicitly false
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    report = match_concepts(
        features=features,
        concept_slugs=["exit-width"],
        markdown_paths=[_write_fixture(tmp_path)],
        threshold=0.0,
        runs_dir=runs_dir,
    )
    assert report.matched == []
    assert report.below_threshold == []
    out = runs_dir / "latest_tfidf_concept_match.json"
    assert not out.exists()


def test_threshold_separates_matched_from_below(tmp_path: Path):
    features = Features(flags={"d_tfidf_concepts": True})
    report = match_concepts(
        features=features,
        concept_slugs=["exit-width"],
        markdown_paths=[_write_fixture(tmp_path)],
        threshold=999.0,  # absurdly high
    )
    assert report.matched == []  # nothing clears 999
    assert len(report.below_threshold) >= 1


def test_score_concept_returns_top_k_sorted(tmp_path: Path):
    sections = split_into_sections(SAMPLE_MARKDOWN)
    vec, mat = build_tfidf_matrix(sections)
    candidates = score_concept(
        concept_slug="exit-width",
        vectorizer=vec,
        matrix=mat,
        sections=sections,
        source_path="pd1096_excerpt.md",
        top_k=2,
    )
    assert len(candidates) == 2
    # Descending by score
    assert candidates[0].score >= candidates[1].score
