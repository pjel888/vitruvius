"""Stream H.8 — tensor factorisation scaffold."""

from __future__ import annotations

import dataclasses

import pytest

from vitruvius.graph.contract import GraphEdge, GraphNode, GraphSnapshot
from vitruvius.graph.tensor_factorisation import (
    MIN_JURISDICTIONS,
    InsufficientJurisdictionsError,
    TensorFactorisationReport,
    _infer_jurisdiction,
    factorise_snapshot,
)


def _n(id_: str) -> GraphNode:
    return GraphNode(
        id=id_,
        type="concept",
        slug=id_.split("-", 1)[-1] or "x",
        trust_level="derived",
        last_updated_utc="2026-04-14T00:00:00Z",
    )


def _e(from_id: str, to_id: str, *, type_: str = "governs",
       evidence: str = "rel-x") -> GraphEdge:
    return GraphEdge(
        from_id=from_id,
        to_id=to_id,
        type=type_,
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


def _mock_classifier_two(evidence_id: str) -> str:
    # First half of the evidence ids → jurisdiction "a", rest → "b".
    return "a" if evidence_id.endswith("-a") else "b"


def test_single_jurisdiction_raises() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b")],
        [_e("concept-a", "concept-b", evidence="rel-1")],
    )
    with pytest.raises(InsufficientJurisdictionsError):
        factorise_snapshot(snap)


def test_happy_path_with_two_jurisdictions() -> None:
    nodes = [_n(f"concept-{c}") for c in "abcd"]
    edges = [
        _e("concept-a", "concept-b", type_="governs", evidence="rel-a"),
        _e("concept-b", "concept-c", type_="affects", evidence="rel-b"),
        _e("concept-c", "concept-d", type_="governs", evidence="rel-a"),
        _e("concept-d", "concept-a", type_="affects", evidence="rel-b"),
    ]
    snap = _snap(nodes, edges)
    report = factorise_snapshot(snap, classifier=_mock_classifier_two)
    assert report.n_jurisdictions == 2


def test_tensor_shape_matches_expected_dims() -> None:
    nodes = [_n(f"concept-{c}") for c in "abcd"]
    edges = [
        _e("concept-a", "concept-b", type_="governs", evidence="rel-a"),
        _e("concept-b", "concept-c", type_="affects", evidence="rel-b"),
    ]
    snap = _snap(nodes, edges)
    report = factorise_snapshot(snap, classifier=_mock_classifier_two)
    # 4 subjects, 2 predicates, 4 objects, 2 jurisdictions.
    assert report.tensor_shape == (4, 2, 4, 2)


def test_singular_values_non_negative_and_descending() -> None:
    nodes = [_n(f"concept-{c}") for c in "abcde"]
    edges = [
        _e("concept-a", "concept-b", type_="governs", evidence="rel-a"),
        _e("concept-b", "concept-c", type_="affects", evidence="rel-b"),
        _e("concept-c", "concept-d", type_="cites", evidence="rel-a"),
        _e("concept-d", "concept-e", type_="governs", evidence="rel-b"),
    ]
    snap = _snap(nodes, edges)
    report = factorise_snapshot(snap, classifier=_mock_classifier_two)
    sv = list(report.singular_values)
    assert all(v >= 0.0 for v in sv)
    for i in range(len(sv) - 1):
        assert sv[i] >= sv[i + 1]


def test_explained_variance_sums_near_one() -> None:
    nodes = [_n(f"concept-{c}") for c in "abcde"]
    edges = [
        _e("concept-a", "concept-b", type_="governs", evidence="rel-a"),
        _e("concept-b", "concept-c", type_="affects", evidence="rel-b"),
        _e("concept-c", "concept-d", type_="cites", evidence="rel-a"),
        _e("concept-d", "concept-e", type_="governs", evidence="rel-b"),
    ]
    snap = _snap(nodes, edges)
    report = factorise_snapshot(snap, classifier=_mock_classifier_two)
    total = sum(report.explained_variance_ratio)
    assert abs(total - 1.0) < 1e-6


def test_frozen_return_and_default_classifier_triggers_guard() -> None:
    # Default classifier maps all current rel-* → "national".
    assert _infer_jurisdiction("rel-anything") == "national"
    snap = _snap(
        [_n("concept-a"), _n("concept-b")],
        [_e("concept-a", "concept-b", evidence="rel-national-1")],
    )
    with pytest.raises(InsufficientJurisdictionsError):
        factorise_snapshot(snap)

    nodes = [_n(f"concept-{c}") for c in "ab"]
    edges = [
        _e("concept-a", "concept-b", evidence="rel-a"),
        _e("concept-b", "concept-a", evidence="rel-b"),
    ]
    snap2 = _snap(nodes, edges)
    report = factorise_snapshot(snap2, classifier=_mock_classifier_two)
    assert dataclasses.is_dataclass(report)
    assert isinstance(report, TensorFactorisationReport)
    with pytest.raises(dataclasses.FrozenInstanceError):
        report.n_jurisdictions = 999  # type: ignore[misc]
    assert MIN_JURISDICTIONS == 2
