"""Performance benchmark for QueryEngine.

These are not strict assertions — they serve as baselines for regression
detection.  On an 8 GB M2 MacBook Pro, the thresholds should be generous.
"""

from __future__ import annotations

import time

import pytest

from vitruvius.kg.enums import EdgeType, InferenceType, NodeType, ValidationState
from vitruvius.kg.json_evidence_store import KgV2Snapshot
from vitruvius.kg.query_engine import QueryEngine
from vitruvius.kg.schemas import CanonicalNode, RelationshipAssertion


def _make_large_snapshot(node_count: int = 1000, assertion_count: int = 2000) -> KgV2Snapshot:
    snap = KgV2Snapshot()
    for i in range(node_count):
        snap.canonical_nodes.append(
            CanonicalNode(
                id=f"concept-node-{i:04d}",
                type=NodeType.CONCEPT,
                label=f"Node {i}",
                slug=f"node-{i}",
            )
        )
    for i in range(assertion_count):
        from_idx = i % node_count
        to_idx = (i + 1) % node_count
        snap.relationship_assertions.append(
            RelationshipAssertion(
                id=f"assert-rel-{i:05d}",
                edge_type=EdgeType.RELATED_TO,
                from_node_id=f"concept-node-{from_idx:04d}",
                to_node_id=f"concept-node-{to_idx:04d}",
                reasoning_summary=f"Reason {i}",
                inference_type=InferenceType.DIRECT_CITATION,
                confidence=0.9,
                validation_status=ValidationState.VALIDATED,
            )
        )
    return snap


class TestQueryEnginePerf:
    def test_build_index_1000_nodes(self) -> None:
        snap = _make_large_snapshot(node_count=1000, assertion_count=0)
        start = time.perf_counter()
        engine = QueryEngine(snap)
        elapsed = time.perf_counter() - start
        assert elapsed < 1.0, f"Index build took {elapsed:.3f}s, expected < 1.0s"

    def test_get_node_by_id_1000_nodes(self) -> None:
        snap = _make_large_snapshot(node_count=1000, assertion_count=0)
        engine = QueryEngine(snap)
        start = time.perf_counter()
        for i in range(1000):
            engine.get_node_by_id(f"concept-node-{i:04d}")
        elapsed = time.perf_counter() - start
        assert elapsed < 0.1, f"1000 lookups took {elapsed:.3f}s, expected < 0.1s"

    def test_search_nodes_by_label_1000_nodes(self) -> None:
        snap = _make_large_snapshot(node_count=1000, assertion_count=0)
        engine = QueryEngine(snap)
        start = time.perf_counter()
        results = engine.search_nodes_by_label("Node 5", limit=10)
        elapsed = time.perf_counter() - start
        assert elapsed < 0.1, f"Search took {elapsed:.3f}s, expected < 0.1s"
        assert len(results) <= 10

    def test_get_assertions_for_node_with_2000_assertions(self) -> None:
        snap = _make_large_snapshot(node_count=1000, assertion_count=2000)
        engine = QueryEngine(snap)
        start = time.perf_counter()
        assertions = engine.get_assertions_for_node("concept-node-0000")
        elapsed = time.perf_counter() - start
        assert elapsed < 0.1, f"Assertion lookup took {elapsed:.3f}s, expected < 0.1s"
        # node-0000 appears in assertions where from_idx == 0 or to_idx == 0
        assert len(assertions) >= 2

    def test_get_node_neighborhood_2000_assertions(self) -> None:
        snap = _make_large_snapshot(node_count=1000, assertion_count=2000)
        engine = QueryEngine(snap)
        start = time.perf_counter()
        neighbors = engine.get_node_neighborhood("concept-node-0000")
        elapsed = time.perf_counter() - start
        assert elapsed < 0.1, f"Neighborhood lookup took {elapsed:.3f}s, expected < 0.1s"
