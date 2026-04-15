"""Sprint CLEANUP-1 Stream C4.3 — regex + LLM candidate merger tests."""

from __future__ import annotations

from vitruvius.relationships.llm_proposer import ProposedCandidate
from vitruvius.relationships.phase_5e_merger import merge_regex_and_llm


def test_merge_regex_only() -> None:
    regex_candidates = [
        {"from": "a", "type": "governs", "to": "b", "occurrences": 2, "sections": ["sec-1"], "examples": ["evidence"]}
    ]
    llm_candidates: list[ProposedCandidate] = []
    merged = merge_regex_and_llm(regex_candidates, llm_candidates)
    assert len(merged) == 1
    assert merged[0]["from"] == "a"
    assert merged[0].get("source") in (None, "regex")


def test_merge_llm_only() -> None:
    regex_candidates: list[dict] = []
    llm_candidates = [
        ProposedCandidate(
            from_id="section-701",
            predicate="defines",
            to_id="concept-occupancy-classification",
            evidence="The occupancy group...",
            confidence=0.85,
        )
    ]
    merged = merge_regex_and_llm(regex_candidates, llm_candidates)
    assert len(merged) == 1
    assert merged[0]["from"] == "section-701"
    assert merged[0]["type"] == "defines"
    assert merged[0]["source"] == "llm_proposer"


def test_merge_deduplicates_overlapping_endpoints() -> None:
    """If regex and LLM both propose the same (from, to, predicate), merge into one.
    Regex wins on overlap (more trusted baseline)."""
    regex_candidates = [
        {"from": "a", "type": "governs", "to": "b", "occurrences": 2, "sections": ["sec-1"], "examples": ["regex-ev"]}
    ]
    llm_candidates = [
        ProposedCandidate(
            from_id="a",
            predicate="governs",
            to_id="b",
            evidence="llm-ev",
            confidence=0.8,
        )
    ]
    merged = merge_regex_and_llm(regex_candidates, llm_candidates)
    assert len(merged) == 1  # deduped
    # Regex wins
    assert merged[0]["source"] in (None, "regex")
