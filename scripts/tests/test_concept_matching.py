from __future__ import annotations

from pathlib import Path

from vitruvius.concept_matching import (
    find_concepts_in_text,
    load_concept_term_map,
    normalize_match_text,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_normalize_match_text_collapses_punctuation_and_spacing() -> None:
    assert normalize_match_text("Fire-resistive_construction!!") == "fire resistive construction"


def test_find_concepts_in_text_is_boundary_aware_and_ordered(tmp_path: Path) -> None:
    concepts_dir = tmp_path / "concepts"
    _write(
        concepts_dir / "building-permit.md",
        "---\ntitle: Building Permit\n---\n",
    )
    _write(
        concepts_dir / "yards.md",
        "---\ntitle: Yards\naliases:\n  - yard\n---\n",
    )
    concept_map = load_concept_term_map(concepts_dir)

    text = "A building permit is required. The permit process applies. Front yard requirements remain."
    found = find_concepts_in_text(text, concept_map)

    assert found == ["concept-building-permit", "concept-yards"]


def test_find_concepts_in_text_does_not_match_word_substrings(tmp_path: Path) -> None:
    concepts_dir = tmp_path / "concepts"
    _write(
        concepts_dir / "building-permit.md",
        "---\ntitle: Building Permit\n---\n",
    )
    concept_map = load_concept_term_map(concepts_dir)

    text = "Permitted work shall proceed after review."
    found = find_concepts_in_text(text, concept_map)

    assert found == []


def test_load_concept_term_map_uses_aliases(tmp_path: Path) -> None:
    concepts_dir = tmp_path / "concepts"
    _write(
        concepts_dir / "socialized-housing-projects.md",
        (
            "---\n"
            "title: Socialized Housing Projects\n"
            "aliases:\n"
            "  - economic and socialized housing projects\n"
            "---\n"
        ),
    )
    concept_map = load_concept_term_map(concepts_dir)
    found = find_concepts_in_text(
        "The standards apply to economic and socialized housing projects in urban areas.",
        concept_map,
    )
    assert found == ["concept-socialized-housing-projects"]
