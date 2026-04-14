"""Tests for the section-title alias dictionary.

Adds coverage for the `_section_title_to_concept` fallback path when
neither exact nor contains-phrase match succeeds but the alias
dictionary has a match.
"""

from vitruvius.concept_definitions import (
    SECTION_TITLE_ALIASES,
    extract_definitions_from_sections,
)


KNOWN = {
    "building-height",
    "lot-occupancy",
    "fire-resistive-construction",
    "open-courts",
    "projections-over-public-ways",
    "occupancy-load",
    "setbacks",
    "yards",
}


def test_alias_dictionary_has_every_entry_point_to_real_slug():
    """Every key in SECTION_TITLE_ALIASES should be a plausible concept slug.

    This is a smoke test against typos — the values are phrasings, the
    keys must be hyphenated slugs.
    """
    import re
    slug_pat = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
    for key in SECTION_TITLE_ALIASES:
        assert slug_pat.match(key), f"key {key!r} is not a valid slug"


def test_building_height_alias_resolves_from_section_title():
    text = "### SECTION 707. Maximum Height of Buildings\n\nNo building shall exceed..."
    candidates = extract_definitions_from_sections(
        text,
        source_id="law-pd-1096",
        known_slugs=KNOWN,
    )
    assert any(c.concept_slug == "building-height" for c in candidates)


def test_lot_occupancy_alias_resolves_from_site_occupancy_title():
    text = "### SECTION 803. Percentage of Site Occupancy\n\nThe maximum allowable..."
    candidates = extract_definitions_from_sections(
        text,
        source_id="law-pd-1096",
        known_slugs=KNOWN,
    )
    assert any(c.concept_slug == "lot-occupancy" for c in candidates)


def test_occupancy_load_alias_resolves_from_occupant_load_title():
    text = "### SECTION 1207. Stairs, Exits, and Occupant Loads\n\nBodies shall..."
    candidates = extract_definitions_from_sections(
        text,
        source_id="law-pd-1096",
        known_slugs=KNOWN,
    )
    slugs = {c.concept_slug for c in candidates}
    assert "occupancy-load" in slugs


def test_projections_alias_resolves_from_balcony_title():
    text = "### SECTION 1003. Projection of Balconies and Appendages Over Streets\n\nSuch projections..."
    candidates = extract_definitions_from_sections(
        text,
        source_id="law-pd-1096",
        known_slugs=KNOWN,
    )
    assert any(c.concept_slug == "projections-over-public-ways" for c in candidates)


def test_alias_not_used_if_slug_not_in_known_set():
    """Alias dictionary should respect the known_slugs filter so unrelated
    concept sets don't get surprise matches.
    """
    text = "### SECTION 707. Maximum Height of Buildings\n\nNo building shall exceed..."
    # Tiny known set that excludes building-height
    candidates = extract_definitions_from_sections(
        text,
        source_id="law-pd-1096",
        known_slugs={"setbacks"},
    )
    assert candidates == []
