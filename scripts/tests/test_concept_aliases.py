"""Tests for the deterministic alias miner (Phase 3C Task 2).

Mines alternate names for concepts from source text using two patterns:
- Parenthetical abbreviations: "National Building Code (NBC)"
- "also known as" / "or" phrases: "Occupancy Classification, also known as use group"

Zero LLM calls. Pure regex.
"""

from vitruvius.concept_aliases import (
    mine_aliases_for_concept,
    parenthetical_abbreviations,
)


# ---------- parenthetical abbreviations ----------

def test_parenthetical_abbreviation_simple():
    text = "The National Building Code (NBC) of the Philippines..."
    pairs = parenthetical_abbreviations(text)
    assert ("national building code", "nbc") in pairs


def test_parenthetical_abbreviation_ignores_short_or_digit_only():
    text = "See chapter (a) and section (1) below."
    pairs = parenthetical_abbreviations(text)
    # "(a)" is too short and "(1)" is digit-only — both rejected
    assert pairs == []


def test_parenthetical_abbreviation_ignores_if_long_form_missing():
    text = "The building permit shall (a) be obtained and (b) maintained..."
    # "(a)" / "(b)" have no meaningful long form preceding them
    pairs = parenthetical_abbreviations(text)
    assert not any(abbrev in {"a", "b"} for _, abbrev in pairs)


def test_parenthetical_multiple_abbreviations():
    text = (
        "The Department of Public Works and Highways (DPWH) and the "
        "Local Government Unit (LGU) shall cooperate."
    )
    pairs = parenthetical_abbreviations(text)
    abbrevs = {abbrev for _, abbrev in pairs}
    assert "dpwh" in abbrevs
    assert "lgu" in abbrevs


def test_parenthetical_handles_dots_in_abbreviation():
    text = "The Fire Code of the Philippines (F.C.P.) shall apply."
    pairs = parenthetical_abbreviations(text)
    # Dots stripped in normalized form
    assert any(abbrev == "fcp" for _, abbrev in pairs)


# ---------- mine_aliases_for_concept ----------

def test_mine_parenthetical_alias_for_matching_concept():
    text = "The National Building Code (NBC) of the Philippines..."
    aliases = mine_aliases_for_concept(text, concept_title="National Building Code")
    assert "nbc" in aliases


def test_mine_also_known_as_phrase():
    text = "Occupancy Classification, also known as use group, determines..."
    aliases = mine_aliases_for_concept(text, concept_title="Occupancy Classification")
    assert "use group" in aliases


def test_mine_alias_capped_at_five():
    text = (
        "The National Building Code (NBC) is also called the building code, "
        "also known as the code, also referred to as the act, NBC 1977, "
        "and PD 1096."
    )
    aliases = mine_aliases_for_concept(text, concept_title="National Building Code")
    assert len(aliases) <= 5


def test_mine_alias_drops_stopwords_and_self_references():
    text = "Occupancy Classification, also known as occupancy classification..."
    aliases = mine_aliases_for_concept(text, concept_title="Occupancy Classification")
    # Self-reference should be filtered out
    assert "occupancy classification" not in aliases


def test_mine_alias_deduplicates():
    text = (
        "National Building Code (NBC). The NBC applies. The National Building Code (NBC) says..."
    )
    aliases = mine_aliases_for_concept(text, concept_title="National Building Code")
    assert aliases.count("nbc") == 1


def test_mine_alias_handles_empty_text():
    assert mine_aliases_for_concept("", concept_title="Anything") == []
