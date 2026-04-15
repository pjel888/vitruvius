"""Sprint CLEANUP-1 Stream C4 — Phase 5E LLM proposer dataclass + stub tests."""

from __future__ import annotations

from unittest.mock import patch

from vitruvius.relationships.llm_proposer import (
    ALLOWED_PREDICATES,
    ProposedCandidate,
)


def test_allowed_predicates_matches_registry() -> None:
    """Closed vocabulary guard — drift between the proposer constant and the registry
    should be caught by a failing test."""
    assert ALLOWED_PREDICATES == {
        "governs", "defines", "requires", "depends_on", "limits", "affects", "supersedes"
    }


def test_proposed_candidate_dataclass_shape() -> None:
    c = ProposedCandidate(
        from_id="section-701",
        predicate="defines",
        to_id="concept-occupancy-classification",
        evidence="The occupancy group...",
        confidence=0.85,
    )
    assert c.from_id == "section-701"
    assert c.predicate == "defines"
    assert c.source == "llm_proposer"  # default value


def test_proposer_parses_valid_json_response() -> None:
    fake_ollama_response = """[
        {
            "from": "section-701",
            "type": "defines",
            "to": "concept-occupancy-classification",
            "evidence": "The occupancy group of a building shall be determined by its primary use.",
            "confidence": 0.85
        }
    ]"""

    with patch(
        "vitruvius.relationships.llm_proposer._call_ollama",
        return_value=fake_ollama_response,
    ):
        from vitruvius.relationships.llm_proposer import propose_relationships_llm

        result = propose_relationships_llm(
            section_text="The occupancy group of a building shall be determined by its primary use.",
            section_id="section-701",
            source_id="law-national-building-code-of-the-philippines",
        )
        assert len(result) == 1
        assert result[0].from_id == "section-701"
        assert result[0].predicate == "defines"
        assert result[0].confidence == 0.85


def test_proposer_returns_empty_on_malformed_json() -> None:
    with patch(
        "vitruvius.relationships.llm_proposer._call_ollama",
        return_value="not valid json at all",
    ):
        from vitruvius.relationships.llm_proposer import propose_relationships_llm

        result = propose_relationships_llm(
            section_text="foo",
            section_id="sec-1",
            source_id="law-foo",
        )
        assert result == []


def test_proposer_filters_disallowed_predicates() -> None:
    fake_response = """[
        {"from": "a", "type": "governs", "to": "b", "evidence": "...", "confidence": 0.9},
        {"from": "c", "type": "invented_predicate", "to": "d", "evidence": "...", "confidence": 0.9}
    ]"""

    with patch(
        "vitruvius.relationships.llm_proposer._call_ollama",
        return_value=fake_response,
    ):
        from vitruvius.relationships.llm_proposer import propose_relationships_llm

        result = propose_relationships_llm(
            section_text="foo",
            section_id="sec-1",
            source_id="law-foo",
        )
        assert len(result) == 1
        assert result[0].predicate == "governs"


def test_proposer_returns_empty_on_ollama_connection_error() -> None:
    with patch(
        "vitruvius.relationships.llm_proposer._call_ollama",
        side_effect=ConnectionError("Ollama not running"),
    ):
        from vitruvius.relationships.llm_proposer import propose_relationships_llm

        result = propose_relationships_llm(
            section_text="foo",
            section_id="sec-1",
            source_id="law-foo",
        )
        assert result == []
