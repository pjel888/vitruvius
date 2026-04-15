"""Sprint HP Stream HP.5 — GraphSAGE embeddings + structural loopholes detector."""

from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("torch_geometric")

from vitruvius.graph.contract import GraphEdge, GraphNode, GraphSnapshot
from vitruvius.graph.graphsage import (
    GraphSAGEReport,
    LoopholesReport,
    compute_graphsage_embeddings,
    find_structural_loopholes,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _n(id_: str, type_: str = "concept") -> GraphNode:
    return GraphNode(
        id=id_,
        type=type_,
        slug=id_.split("-", 1)[-1] or "x",
        trust_level="derived",
        last_updated_utc="2026-04-14T00:00:00Z",
    )


def _e(from_id: str, to_id: str, *, evidence: str = "rel-x") -> GraphEdge:
    return GraphEdge(
        from_id=from_id,
        to_id=to_id,
        type="governs",
        evidence_id=evidence,
        status="verified",
    )


def _snap(nodes: list[GraphNode], edges: list[GraphEdge]) -> GraphSnapshot:
    return GraphSnapshot(
        schema_version="1.0.0",
        generated_at_utc="2026-04-14T00:00:00Z",
        node_count=len(nodes),
        edge_count=len(edges),
        nodes=nodes,
        edges=edges,
    )


# ---------------------------------------------------------------------------
# Task HP.5.1 — structural embeddings
# ---------------------------------------------------------------------------


def test_empty_snapshot_returns_empty_report() -> None:
    """Empty GraphSnapshot → empty embeddings dict, dim preserved."""
    snap = _snap([], [])
    report = compute_graphsage_embeddings(snap, dim=64, num_layers=2, random_state=42)
    assert isinstance(report, GraphSAGEReport)
    assert report.embeddings == {}
    assert report.dim == 64


def test_embeddings_have_expected_shape() -> None:
    """5-node graph → 5 embeddings, each shape (64,), dtype float32."""
    nodes = [_n(f"concept-{i}") for i in "abcde"]
    edges = [
        _e("concept-a", "concept-b", evidence="rel-1"),
        _e("concept-b", "concept-c", evidence="rel-2"),
        _e("concept-c", "concept-d", evidence="rel-3"),
        _e("concept-d", "concept-e", evidence="rel-4"),
    ]
    snap = _snap(nodes, edges)
    report = compute_graphsage_embeddings(snap, dim=64, num_layers=2, random_state=42)
    assert report.dim == 64
    assert set(report.embeddings.keys()) == {f"concept-{i}" for i in "abcde"}
    for node_id, vec in report.embeddings.items():
        assert isinstance(vec, np.ndarray), f"{node_id} embedding is not a numpy array"
        assert vec.shape == (64,), f"{node_id} shape {vec.shape} != (64,)"
        assert vec.dtype == np.float32, f"{node_id} dtype {vec.dtype} != float32"


def test_embeddings_are_deterministic() -> None:
    """Two calls with the same random_state return np.allclose results."""
    nodes = [
        _n("concept-a"),
        _n("rule-b", type_="rule"),
        _n("concept-c"),
        _n("rule-d", type_="rule"),
        _n("concept-e"),
    ]
    edges = [
        _e("concept-a", "rule-b", evidence="rel-1"),
        _e("rule-b", "concept-c", evidence="rel-2"),
        _e("concept-c", "rule-d", evidence="rel-3"),
        _e("rule-d", "concept-e", evidence="rel-4"),
    ]
    snap = _snap(nodes, edges)
    r1 = compute_graphsage_embeddings(snap, dim=32, num_layers=2, random_state=7)
    r2 = compute_graphsage_embeddings(snap, dim=32, num_layers=2, random_state=7)
    assert set(r1.embeddings.keys()) == set(r2.embeddings.keys())
    for node_id in r1.embeddings:
        assert np.allclose(
            r1.embeddings[node_id],
            r2.embeddings[node_id],
            rtol=1e-5,
            atol=1e-6,
        ), f"{node_id} embedding is non-deterministic across calls"


# ---------------------------------------------------------------------------
# Task HP.5.3 — structural loopholes detector
# ---------------------------------------------------------------------------


_HAS_SENTENCE_TRANSFORMERS = pytest.importorskip(
    "sentence_transformers",
    reason="sentence_transformers not installed; skipping loophole tests",
)


def test_loopholes_detects_distant_semantically_similar_pair() -> None:
    """6-node chain where two far-apart nodes share near-identical text.

    The chain a–b–c–d–e–f places ``concept-a`` and ``concept-f`` at BFS
    distance 5. We seed the concept text so those two nodes describe the
    same setback rule in near-identical language, while the middle nodes
    describe unrelated topics. The loopholes detector must surface the
    ``(concept-a, concept-f)`` pair.
    """
    nodes = [_n(f"concept-{i}") for i in "abcdef"]
    edges = [
        _e("concept-a", "concept-b", evidence="rel-1"),
        _e("concept-b", "concept-c", evidence="rel-2"),
        _e("concept-c", "concept-d", evidence="rel-3"),
        _e("concept-d", "concept-e", evidence="rel-4"),
        _e("concept-e", "concept-f", evidence="rel-5"),
    ]
    snap = _snap(nodes, edges)

    text_by_id = {
        "concept-a": (
            "The maximum building setback shall be ten meters from the "
            "front property line in all residential zones."
        ),
        "concept-b": (
            "Floor area ratio for commercial zones is limited to three-to-one."
        ),
        "concept-c": (
            "Restaurants must install grease interceptors per the plumbing code."
        ),
        "concept-d": (
            "Urban heat island mitigation requires reflective rooftops on "
            "new construction."
        ),
        "concept-e": (
            "Heritage trees near construction sites must be protected "
            "with tree wells."
        ),
        "concept-f": (
            "Maximum building setback must be ten meters from the front "
            "property boundary for residential zones."
        ),
    }

    report = find_structural_loopholes(
        snap,
        concept_text_by_id=text_by_id,
        semantic_similarity_threshold=0.70,
        topological_distance_min=3,
        max_pairs=50,
    )

    assert isinstance(report, LoopholesReport)
    assert report.pairs, "expected at least one loophole pair, got none"
    # The (a, f) pair must be in the report — lex-ordered so ``concept-a``
    # appears first.
    pair_ids = {(a, b) for (a, b, _score, _dist) in report.pairs}
    assert ("concept-a", "concept-f") in pair_ids

    # And the pair's topological distance must be the shortest-path length
    # in the chain, which is 5.
    chosen = [p for p in report.pairs if p[0] == "concept-a" and p[1] == "concept-f"][0]
    assert chosen[3] == 5
    # Cosine similarity of near-identical sentences must comfortably
    # clear the 0.70 threshold — in practice MiniLM scores ~0.94 here.
    assert chosen[2] >= 0.80


def test_loopholes_respects_topological_distance_min() -> None:
    """Raising the min distance threshold must drop the (a, f) pair.

    Same 6-node chain as above; with ``topological_distance_min=6``
    the only candidate pair sits at distance 5 and therefore fails the
    threshold → no pairs returned.
    """
    nodes = [_n(f"concept-{i}") for i in "abcdef"]
    edges = [
        _e("concept-a", "concept-b", evidence="rel-1"),
        _e("concept-b", "concept-c", evidence="rel-2"),
        _e("concept-c", "concept-d", evidence="rel-3"),
        _e("concept-d", "concept-e", evidence="rel-4"),
        _e("concept-e", "concept-f", evidence="rel-5"),
    ]
    snap = _snap(nodes, edges)

    text_by_id = {
        "concept-a": (
            "The maximum building setback shall be ten meters from the "
            "front property line in all residential zones."
        ),
        "concept-b": "Floor area ratio for commercial zones is three-to-one.",
        "concept-c": "Restaurants must install grease interceptors.",
        "concept-d": "Urban heat island mitigation requires reflective roofs.",
        "concept-e": "Heritage trees must be protected with tree wells.",
        "concept-f": (
            "Maximum building setback must be ten meters from the front "
            "property boundary for residential zones."
        ),
    }

    # Threshold strictly greater than the chain's diameter (5) → no pairs.
    report = find_structural_loopholes(
        snap,
        concept_text_by_id=text_by_id,
        semantic_similarity_threshold=0.70,
        topological_distance_min=6,
        max_pairs=50,
    )
    assert isinstance(report, LoopholesReport)
    assert report.pairs == [], (
        "expected no pairs when topological_distance_min exceeds the "
        "chain diameter, got: " + repr(report.pairs)
    )
