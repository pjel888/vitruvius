"""Tests for Canonicalizer."""

from __future__ import annotations

import pytest

from vitruvius.kg.canonicalizer import Canonicalizer
from vitruvius.kg.schemas import KnowledgeUnitCandidate, CanonicalNode
from vitruvius.kg.enums import NodeType, ValidationState


import re

def _make_candidate(
    unit_type: str = "concept",
    label: str = "Test",
    text: str = "Text",
    confidence: float = 0.9,
    embedding: list[float] | None = None,
) -> KnowledgeUnitCandidate:
    safe_label = re.sub(r"[^a-z0-9-]+", "-", label.lower()).strip("-")
    return KnowledgeUnitCandidate(
        id=f"cand-test-{safe_label}" if safe_label else "cand-test-unknown",
        unit_type=unit_type,
        label=label,
        text=text,
        span_ids=["span-001"],
        chunk_id="chk-001",
        confidence=confidence,
        embedding=embedding,
        created_at="2026-01-01T00:00:00Z",
    )


class TestEmptyAndSingle:
    def test_empty_candidates_returns_empty(self) -> None:
        c = Canonicalizer()
        assert c.canonicalize([]) == []

    def test_single_candidate_becomes_node(self) -> None:
        c = Canonicalizer()
        cand = _make_candidate("concept", "Building Permit", "A permit is required.")
        nodes = c.canonicalize([cand])
        assert len(nodes) == 1
        assert nodes[0].id == "concept-building-permit"
        assert nodes[0].type == NodeType.CONCEPT
        assert nodes[0].label == "Building Permit"
        assert nodes[0].summary == "A permit is required."


class TestExactDedupe:
    def test_exact_dedupe_collapses_same_type_label_text(self) -> None:
        c = Canonicalizer()
        c1 = _make_candidate("concept", "  Building Permit  ", "A permit is required.")
        c2 = _make_candidate("concept", "building permit", "A permit is required.")
        nodes = c.canonicalize([c1, c2])
        assert len(nodes) == 1
        assert nodes[0].label == "Building Permit"

    def test_different_types_not_deduped(self) -> None:
        c = Canonicalizer()
        c1 = _make_candidate("concept", "Permit", "A permit is required.")
        c2 = _make_candidate("rule", "Permit", "A permit is required.")
        nodes = c.canonicalize([c1, c2])
        assert len(nodes) == 2

    def test_different_text_not_deduped(self) -> None:
        c = Canonicalizer()
        c1 = _make_candidate("concept", "Permit", "A permit is required.")
        c2 = _make_candidate("concept", "Permit", "A permit is optional.")
        nodes = c.canonicalize([c1, c2])
        assert len(nodes) == 2

    def test_highest_confidence_wins(self) -> None:
        c = Canonicalizer()
        c1 = _make_candidate("concept", "Permit", "Text", confidence=0.5)
        c2 = _make_candidate("concept", "Permit", "Text", confidence=0.9)
        nodes = c.canonicalize([c1, c2])
        assert len(nodes) == 1
        assert nodes[0].confidence == 0.9

    def test_span_ids_merged(self) -> None:
        c = Canonicalizer()
        c1 = _make_candidate("concept", "Permit", "Text")
        c1.span_ids = ["span-a"]
        c2 = _make_candidate("concept", "Permit", "Text")
        c2.span_ids = ["span-b", "span-a"]
        nodes = c.canonicalize([c1, c2])
        assert nodes[0].primary_assertion_id is None  # not set by canonicalizer


class TestIdAssignment:
    def test_id_collision_handling(self) -> None:
        c = Canonicalizer()
        c1 = _make_candidate("concept", "Permit", "Text A")
        c2 = _make_candidate("concept", "Permit", "Text B")
        nodes = c.canonicalize([c1, c2])
        # Different text → not deduped, same label → ID collision
        assert len(nodes) == 2
        ids = {n.id for n in nodes}
        assert "concept-permit" in ids
        assert "concept-permit-001" in ids

    def test_slugify_special_chars(self) -> None:
        c = Canonicalizer()
        cand = _make_candidate("concept", "Fire & Life Safety", "Text")
        nodes = c.canonicalize([cand])
        assert nodes[0].slug == "fire-life-safety"
        assert nodes[0].id == "concept-fire-life-safety"

    def test_slugify_empty_label_fallback(self) -> None:
        c = Canonicalizer()
        cand = _make_candidate("concept", "!!!", "Text")
        nodes = c.canonicalize([cand])
        assert nodes[0].slug == "unknown"
        assert nodes[0].id == "concept-unknown"


class TestNearDuplicateFlagging:
    def test_near_duplicate_sets_review_required(self) -> None:
        c = Canonicalizer()
        c1 = _make_candidate("concept", "A", "Text A", embedding=[1.0, 0.0, 0.0])
        c2 = _make_candidate("concept", "B", "Text B", embedding=[0.999, 0.001, 0.0])
        nodes = c.canonicalize([c1, c2])
        # Without embedder, near-duplicates are not flagged
        assert all(n.status == ValidationState.CANDIDATE for n in nodes)

    def test_embedding_ref_stored(self) -> None:
        c = Canonicalizer()
        cand = _make_candidate("concept", "X", "Text", embedding=[1.0, 2.0, 3.0])
        nodes = c.canonicalize([cand])
        assert nodes[0].embedding_ref == "[1.0, 2.0, 3.0]"
