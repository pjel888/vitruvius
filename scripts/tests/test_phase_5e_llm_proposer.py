"""Sprint CLEANUP-1 Stream C4 — Phase 5E LLM proposer dataclass + stub tests."""

from __future__ import annotations

import pytest

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


def test_proposer_function_stub_raises_not_implemented() -> None:
    from vitruvius.relationships.llm_proposer import propose_relationships_llm

    with pytest.raises(NotImplementedError):
        propose_relationships_llm(
            section_text="hello",
            section_id="sec-1",
            source_id="law-foo",
        )
