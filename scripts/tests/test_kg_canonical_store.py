"""Tests for CanonicalStore."""

from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.kg.canonical_store import CanonicalStore
from vitruvius.kg.schemas import CanonicalNode, PlacementAssertion, MergeAssertion
from vitruvius.kg.enums import NodeType, ValidationState


def _make_node(node_id: str = "concept-test") -> CanonicalNode:
    return CanonicalNode(
        id=node_id,
        type=NodeType.CONCEPT,
        label="Test",
        slug="test",
        summary="Summary",
        taxonomy_path=[],
        aliases=[],
        status=ValidationState.CANDIDATE,
        confidence=0.9,
        version=1,
        created_at="2026-01-01T00:00:00Z",
        updated_at="2026-01-01T00:00:00Z",
    )


def _make_placement() -> PlacementAssertion:
    return PlacementAssertion(
        id="assert-placement-concept-test-to-root",
        node_id="concept-test",
        parent_node_id="root",
        reasoning_summary="Placed by rule",
        confidence=0.9,
        validation_status=ValidationState.CANDIDATE,
        evidence_ids=[],
        created_at="2026-01-01T00:00:00Z",
        version=1,
    )


def _make_merge() -> MergeAssertion:
    return MergeAssertion(
        id="assert-merge-a-into-b",
        from_node_id="concept-a",
        to_node_id="concept-b",
        reasoning_summary="Exact duplicate",
        confidence=1.0,
        validation_status=ValidationState.REVIEW_REQUIRED,
        evidence_ids=[],
        created_at="2026-01-01T00:00:00Z",
        version=1,
    )


class TestSaveAndLoad:
    def test_roundtrip(self, tmp_path: Path) -> None:
        store = CanonicalStore(base_dir=tmp_path)
        nodes = [_make_node("concept-a")]
        placements = [_make_placement()]
        merges = [_make_merge()]
        path = store.save(nodes, placements, merges, run_id="test-run")

        assert path.exists()
        loaded_nodes, loaded_placements, loaded_merges = store.load(path)
        assert len(loaded_nodes) == 1
        assert loaded_nodes[0].id == "concept-a"
        assert len(loaded_placements) == 1
        assert loaded_placements[0].node_id == "concept-test"
        assert len(loaded_merges) == 1
        assert loaded_merges[0].from_node_id == "concept-a"

    def test_checksum_sidecar(self, tmp_path: Path) -> None:
        store = CanonicalStore(base_dir=tmp_path)
        path = store.save([], [], [], run_id="test-run")
        checksum_path = path.parent / f"{path.name}.sha256"
        assert checksum_path.exists()
        assert len(checksum_path.read_text().strip()) == 64

    def test_empty_lists(self, tmp_path: Path) -> None:
        store = CanonicalStore(base_dir=tmp_path)
        path = store.save([], [], [], run_id="empty-run")
        loaded_nodes, loaded_placements, loaded_merges = store.load(path)
        assert loaded_nodes == []
        assert loaded_placements == []
        assert loaded_merges == []

    def test_multiple_records(self, tmp_path: Path) -> None:
        store = CanonicalStore(base_dir=tmp_path)
        nodes = [_make_node(f"concept-{i}") for i in range(3)]
        placements = [_make_placement() for _ in range(2)]
        merges = [_make_merge() for _ in range(2)]
        path = store.save(nodes, placements, merges, run_id="multi")
        ln, lp, lm = store.load(path)
        assert len(ln) == 3
        assert len(lp) == 2
        assert len(lm) == 2
