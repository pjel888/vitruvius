"""Tests for the deterministic definition extractor (Phase 3C Task 1).

The extractor finds definition candidates in canonical source bodies using
regex anchors. Zero LLM calls. Every match emits a DefinitionCandidate
with the concept slug, source ID, section ID, snippet, and a confidence
derived from the anchor strength.
"""

from vitruvius.concept_definitions import (
    DefinitionCandidate,
    extract_definitions_from_text,
    pick_best_definition,
)


KNOWN = {"occupancy-classification", "building-permit", "fire-resistive-construction"}


def test_shall_mean_anchor_produces_highest_confidence():
    text = (
        "Section 701 — Occupancy Classified\n\n"
        "Occupancy Classification shall mean the categorization of a building "
        "by its use or occupancy.\n"
    )
    candidates = extract_definitions_from_text(
        text,
        source_id="law-pd-1096",
        known_slugs=KNOWN,
    )
    assert len(candidates) >= 1
    hit = [c for c in candidates if c.concept_slug == "occupancy-classification"]
    assert hit, f"no hit for occupancy-classification; got {candidates}"
    assert hit[0].confidence >= 0.90
    assert "shall mean" in hit[0].snippet.lower() or "shall mean" in hit[0].anchor


def test_is_defined_as_anchor_is_high_confidence():
    text = (
        "A building permit is defined as a written authorization issued by "
        "the Building Official allowing construction.\n"
    )
    candidates = extract_definitions_from_text(
        text,
        source_id="law-pd-1096",
        known_slugs=KNOWN,
    )
    assert any(c.concept_slug == "building-permit" and c.confidence >= 0.90 for c in candidates)


def test_means_anchor_is_moderate_confidence():
    text = "The term fire-resistive construction means a type of construction with specific fire-resistance ratings."
    candidates = extract_definitions_from_text(
        text,
        source_id="law-pd-1096",
        known_slugs=KNOWN,
    )
    hit = [c for c in candidates if c.concept_slug == "fire-resistive-construction"]
    assert hit
    assert 0.80 <= hit[0].confidence <= 0.95


def test_unknown_concept_is_ignored():
    text = "Parking spaces shall mean areas designated for vehicles."
    candidates = extract_definitions_from_text(
        text,
        source_id="law-pd-1096",
        known_slugs=KNOWN,  # parking-spaces not in the known set
    )
    assert candidates == []


def test_pick_best_definition_prefers_highest_confidence():
    c1 = DefinitionCandidate(
        concept_slug="building-permit",
        source_id="law-pd-1096",
        source_section_id="sec-301",
        snippet="A building permit means a written authorization...",
        anchor="means",
        confidence=0.90,
    )
    c2 = DefinitionCandidate(
        concept_slug="building-permit",
        source_id="law-pd-1096",
        source_section_id="sec-302",
        snippet="Building permit shall mean an authorization...",
        anchor="shall mean",
        confidence=0.95,
    )
    best = pick_best_definition([c1, c2])
    assert best is c2


def test_pick_best_definition_returns_none_on_empty():
    assert pick_best_definition([]) is None


def test_extract_multiple_concepts_from_same_text():
    text = (
        "Building permit shall mean a written authorization. "
        "Occupancy classification is defined as the categorization of buildings."
    )
    candidates = extract_definitions_from_text(
        text,
        source_id="law-pd-1096",
        known_slugs=KNOWN,
    )
    slugs = {c.concept_slug for c in candidates}
    assert "building-permit" in slugs
    assert "occupancy-classification" in slugs
