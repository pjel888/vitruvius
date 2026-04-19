"""Tests for CanonicalGraphBuilder."""

from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.kg.canonical_graph_builder import CanonicalGraphBuilder
from vitruvius.kg.canonical_store import CanonicalStore
from vitruvius.kg.enums import NodeType, ValidationState
from vitruvius.kg.json_evidence_store import KgV2Snapshot
from vitruvius.kg.schemas import (
    CanonicalNode,
    DocumentVersion,
    PlacementAssertion,
    RelationshipAssertion,
)


def _make_taxonomy_snapshot(tmp_path: Path) -> Path:
    snap = KgV2Snapshot()
    snap.canonical_nodes.append(
        CanonicalNode(
            id="taxonomy-building-code",
            type=NodeType.TAXONOMY,
            label="Building Code",
            slug="building-code",
            taxonomy_path=["building-code"],
            status=ValidationState.VALIDATED,
            confidence=1.0,
        )
    )
    snap.canonical_nodes.append(
        CanonicalNode(
            id="taxonomy-rules",
            type=NodeType.TAXONOMY,
            label="Rules",
            slug="rules",
            taxonomy_path=["rules"],
            status=ValidationState.VALIDATED,
            confidence=1.0,
        )
    )
    snap.canonical_nodes.append(
        CanonicalNode(
            id="concept-existing",
            type=NodeType.CONCEPT,
            label="Existing Concept",
            slug="existing-concept",
            status=ValidationState.VALIDATED,
            confidence=0.9,
        )
    )
    path = tmp_path / "taxonomy.json"
    snap.write(path)
    return path


def _make_canonical_jsonl(tmp_path: Path) -> Path:
    store = CanonicalStore(base_dir=tmp_path)
    nodes = [
        CanonicalNode(
            id="concept-new",
            type=NodeType.CONCEPT,
            label="New Concept",
            slug="new-concept",
            status=ValidationState.CANDIDATE,
            confidence=0.85,
        )
    ]
    placements = [
        PlacementAssertion(
            id="assert-placement-new",
            node_id="concept-new",
            parent_node_id="taxonomy-building-code",
            reasoning_summary="Placed",
            confidence=0.85,
            validation_status=ValidationState.CANDIDATE,
            evidence_ids=["span-test-001"],
        )
    ]
    path = store.save(nodes, placements, [], run_id="test")
    return path


class TestLoadSources:
    def test_load_taxonomy_snapshot(self, tmp_path: Path) -> None:
        builder = CanonicalGraphBuilder()
        tax_path = _make_taxonomy_snapshot(tmp_path)
        builder.load_taxonomy_snapshot(tax_path)
        assert len(builder._canonical_nodes) == 3
        assert len(builder._taxonomy_nodes) == 2

    def test_load_canonical_jsonl(self, tmp_path: Path) -> None:
        builder = CanonicalGraphBuilder()
        jsonl_path = _make_canonical_jsonl(tmp_path)
        builder.load_canonical_jsonl(jsonl_path)
        assert len(builder._canonical_nodes) == 1
        assert len(builder._placements) == 1


class TestBuild:
    def test_unifies_nodes(self, tmp_path: Path) -> None:
        builder = CanonicalGraphBuilder()
        builder.load_taxonomy_snapshot(_make_taxonomy_snapshot(tmp_path))
        builder.load_canonical_jsonl(_make_canonical_jsonl(tmp_path))
        snapshot = builder.build(run_placement=False, run_merge_adjudication=False)
        ids = {n.id for n in snapshot.canonical_nodes}
        assert ids == {"taxonomy-building-code", "taxonomy-rules", "concept-existing", "concept-new"}

    def test_deduplicates_by_id(self, tmp_path: Path) -> None:
        builder = CanonicalGraphBuilder()
        # Add same node twice
        builder._canonical_nodes.append(
            CanonicalNode(
                id="concept-dup",
                type=NodeType.CONCEPT,
                label="Dup A",
                slug="dup-a",
            )
        )
        builder._canonical_nodes.append(
            CanonicalNode(
                id="concept-dup",
                type=NodeType.CONCEPT,
                label="Dup B",
                slug="dup-b",
            )
        )
        snapshot = builder.build(run_placement=False, run_merge_adjudication=False)
        assert len(snapshot.canonical_nodes) == 1
        assert snapshot.canonical_nodes[0].label == "Dup B"  # last one wins

    def test_preserves_loaded_placements(self, tmp_path: Path) -> None:
        builder = CanonicalGraphBuilder()
        builder.load_taxonomy_snapshot(_make_taxonomy_snapshot(tmp_path))
        builder.load_canonical_jsonl(_make_canonical_jsonl(tmp_path))
        snapshot = builder.build(run_placement=False, run_merge_adjudication=False)
        assert len(snapshot.placement_assertions) == 1
        assert snapshot.placement_assertions[0].node_id == "concept-new"

    def test_materializes_edges(self, tmp_path: Path) -> None:
        builder = CanonicalGraphBuilder()
        builder.load_taxonomy_snapshot(_make_taxonomy_snapshot(tmp_path))
        builder.load_canonical_jsonl(_make_canonical_jsonl(tmp_path))
        snapshot = builder.build(run_placement=False, run_merge_adjudication=False)
        assert len(snapshot.fast_edges) == 1
        assert snapshot.fast_edges[0]["edge_type"] == "BELONGS_TO"

    def test_runs_placement_when_no_placements_loaded(self, tmp_path: Path) -> None:
        builder = CanonicalGraphBuilder()
        builder.load_taxonomy_snapshot(_make_taxonomy_snapshot(tmp_path))
        builder._canonical_nodes.append(
            CanonicalNode(
                id="concept-rule",
                type=NodeType.RULE,
                label="Rule X",
                slug="rule-x",
                primary_assertion_id="assert-rule-001",
            )
        )
        snapshot = builder.build(run_placement=True, run_merge_adjudication=False)
        rule_placements = [p for p in snapshot.placement_assertions if p.node_id == "concept-rule"]
        assert len(rule_placements) >= 1

    def test_runs_merge_adjudication(self, tmp_path: Path) -> None:
        builder = CanonicalGraphBuilder()
        builder._canonical_nodes.extend(
            [
                CanonicalNode(
                    id="concept-a",
                    type=NodeType.CONCEPT,
                    label="Same",
                    slug="same",
                    primary_assertion_id="assert-a-001",
                ),
                CanonicalNode(
                    id="concept-b",
                    type=NodeType.CONCEPT,
                    label="same",
                    slug="same",
                    primary_assertion_id="assert-b-001",
                ),
            ]
        )
        snapshot = builder.build(run_placement=False, run_merge_adjudication=True)
        assert len(snapshot.merge_assertions) == 1


class TestWriteSnapshot:
    def test_roundtrip(self, tmp_path: Path) -> None:
        builder = CanonicalGraphBuilder()
        builder.load_canonical_jsonl(_make_canonical_jsonl(tmp_path))
        snapshot = builder.build(run_placement=False, run_merge_adjudication=False)
        out_path = builder.write_snapshot(tmp_path / "out.json")
        assert out_path.exists()
        loaded = KgV2Snapshot.read(out_path)
        assert len(loaded.canonical_nodes) == len(snapshot.canonical_nodes)
