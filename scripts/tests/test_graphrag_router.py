"""Stream I.2 — GraphRAG community router."""

from __future__ import annotations

import dataclasses

import pytest

from vitruvius.graph.community import Community, CommunityReport
from vitruvius.query.graphrag_router import (
    RoutingDecision,
    classify_query_macro_vs_specific,
    route_query,
)


def _report(community_ids: list[int]) -> CommunityReport:
    return CommunityReport(
        communities=tuple(
            Community(
                community_id=cid,
                node_ids=(f"concept-{cid}",),
                summary=f"Community {cid}",
            )
            for cid in community_ids
        ),
        modularity=0.5,
    )


def test_classify_macro_overarching_themes() -> None:
    assert classify_query_macro_vs_specific(
        "What are the overarching themes?"
    ) == "macro"


def test_classify_macro_what_concepts() -> None:
    assert classify_query_macro_vs_specific(
        "What concepts exist in building law?"
    ) == "macro"


def test_classify_macro_summarize() -> None:
    assert classify_query_macro_vs_specific(
        "Summarize building permits",
    ) == "macro"
    assert classify_query_macro_vs_specific(
        "Summarise building permits",
    ) == "macro"


def test_classify_specific_direct_entity() -> None:
    assert classify_query_macro_vs_specific(
        "What governs concept-building-permit?"
    ) == "specific"


def test_route_macro_returns_all_community_ids() -> None:
    report = _report([0, 1, 2, 3])
    decision = route_query(
        "What are the overarching themes?",
        community_report=report,
    )
    assert decision.route == "community"
    assert decision.target_community_ids == (0, 1, 2, 3)
    assert "macro" in decision.reason


def test_route_specific_returns_empty_communities() -> None:
    report = _report([0, 1])
    decision = route_query(
        "What governs building permit?",
        community_report=report,
    )
    assert decision.route == "specific"
    assert decision.target_community_ids == ()


def test_route_empty_report_falls_back() -> None:
    report = _report([])
    decision = route_query(
        "What are the overarching themes?",
        community_report=report,
    )
    assert decision.route == "community"
    assert decision.target_community_ids == ()


def test_routing_decision_frozen() -> None:
    decision = RoutingDecision(
        route="specific",
        target_community_ids=(),
        reason="x",
    )
    assert dataclasses.is_dataclass(decision)
    with pytest.raises(dataclasses.FrozenInstanceError):
        decision.route = "community"  # type: ignore[misc]
