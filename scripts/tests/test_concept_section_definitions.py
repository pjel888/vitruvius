"""Tests for section-title-based definition extraction (Phase 3C Task 1b).

Complements concept_definitions.extract_definitions_from_text: when the
source text doesn't use explicit "shall mean" anchors, we fall back to
claiming a section body as the definition of any concept whose slug
matches the section title.

Confidence ladder:
- exact title match                   -> 0.85
- title contains the concept phrase   -> 0.75
- header "Classification of X"        -> 0.75
"""

from vitruvius.concept_definitions import (
    DefinitionCandidate,
    extract_definitions_from_sections,
)


KNOWN = {
    "occupancy-classification",
    "building-permit",
    "building-height",
    "setbacks",
}


def test_exact_section_title_match_claims_body():
    text = (
        "SECTION 701 - Occupancy Classification\n\n"
        "Every building shall be classified in accordance with its use or\n"
        "occupancy. Occupancy groups determine the applicable fire-resistive\n"
        "requirements.\n\n"
        "SECTION 702 - Mixed Occupancy\n\n"
        "When a single building has more than one occupancy...\n"
    )
    candidates = extract_definitions_from_sections(
        text,
        source_id="law-pd-1096",
        known_slugs=KNOWN,
    )
    hit = [c for c in candidates if c.concept_slug == "occupancy-classification"]
    assert hit
    assert hit[0].source_section_id == "sec-701"
    assert hit[0].confidence >= 0.80
    assert "use or occupancy" in hit[0].snippet


def test_title_containing_phrase_matches():
    text = (
        "SECTION 301 - Issuance of Building Permit\n\n"
        "No person shall erect any building without first obtaining a\n"
        "building permit from the Building Official.\n"
    )
    candidates = extract_definitions_from_sections(
        text,
        source_id="law-pd-1096",
        known_slugs=KNOWN,
    )
    hit = [c for c in candidates if c.concept_slug == "building-permit"]
    assert hit
    assert hit[0].source_section_id == "sec-301"


def test_unknown_section_title_is_ignored():
    text = (
        "SECTION 999 - Miscellaneous Provisions\n\n"
        "Any matter not covered by other sections shall be resolved...\n"
    )
    candidates = extract_definitions_from_sections(
        text,
        source_id="law-pd-1096",
        known_slugs=KNOWN,
    )
    assert candidates == []


def test_section_snippet_is_truncated_to_reasonable_length():
    body = "A" * 5000
    text = f"SECTION 701 - Occupancy Classification\n\n{body}\n"
    candidates = extract_definitions_from_sections(
        text,
        source_id="law-pd-1096",
        known_slugs=KNOWN,
    )
    assert candidates
    assert len(candidates[0].snippet) <= 600  # reasonable excerpt


def test_multiple_sections_produce_one_candidate_each():
    text = (
        "SECTION 701 - Occupancy Classification\n\nBody one.\n\n"
        "SECTION 801 - Building Height\n\nBody two.\n\n"
        "SECTION 901 - Setbacks and yards\n\nBody three.\n"
    )
    candidates = extract_definitions_from_sections(
        text,
        source_id="law-pd-1096",
        known_slugs=KNOWN,
    )
    slugs = {c.concept_slug for c in candidates}
    assert "occupancy-classification" in slugs
    assert "building-height" in slugs
    assert "setbacks" in slugs
