from __future__ import annotations

from typing import Iterable

from ..graph.contract import GraphEdge, GraphSnapshot
from .result import QueryCitation, QueryResult, compute_aggregate_confidence


_MAX_SUPERSESSION_HOPS = 5


def _confidence_for(edge: GraphEdge) -> float:
    return 1.0 if edge.status == "verified" else 0.5


def _citation_from_edge(edge: GraphEdge) -> QueryCitation:
    return QueryCitation(
        source_id=edge.from_id,
        source_section_id="",
        evidence_snippet="",
        confidence=_confidence_for(edge),
    )


def _sorted_edges(edges: Iterable[GraphEdge]) -> tuple[GraphEdge, ...]:
    return tuple(
        sorted(
            edges,
            key=lambda e: (e.from_id, e.type, e.to_id, e.evidence_id),
        )
    )


def _build_result(
    *,
    question: str,
    function: str,
    arguments: dict[str, str],
    answer_entities: tuple[str, ...],
    edges: tuple[GraphEdge, ...],
) -> QueryResult:
    citations = tuple(_citation_from_edge(e) for e in edges)
    aggregate = compute_aggregate_confidence(citations)
    return QueryResult(
        question=question,
        answer_entities=answer_entities,
        citations=citations,
        aggregate_confidence=aggregate,
        has_evidence=len(citations) > 0,
        query_function=function,
        arguments=dict(arguments),
    )


def _filter_by_predicate(
    snapshot: GraphSnapshot,
    predicate: str,
    *,
    to_id: str | None = None,
    from_id: str | None = None,
) -> tuple[GraphEdge, ...]:
    matched: list[GraphEdge] = []
    for edge in snapshot.edges:
        if edge.type != predicate:
            continue
        if to_id is not None and edge.to_id != to_id:
            continue
        if from_id is not None and edge.from_id != from_id:
            continue
        matched.append(edge)
    return _sorted_edges(matched)


def _answer_ids(edges: tuple[GraphEdge, ...], *, pick: str) -> tuple[str, ...]:
    seen: set[str] = set()
    out: list[str] = []
    for edge in edges:
        val = edge.from_id if pick == "from" else edge.to_id
        if val not in seen:
            seen.add(val)
            out.append(val)
    return tuple(sorted(out))


def what_governs(subject_id: str, snapshot: GraphSnapshot) -> QueryResult:
    edges = _filter_by_predicate(snapshot, "governs", to_id=subject_id)
    return _build_result(
        question=f"What governs {subject_id}?",
        function="what_governs",
        arguments={"subject": subject_id},
        answer_entities=_answer_ids(edges, pick="from"),
        edges=edges,
    )


def what_requires(subject_id: str, snapshot: GraphSnapshot) -> QueryResult:
    edges = _filter_by_predicate(snapshot, "requires", from_id=subject_id)
    return _build_result(
        question=f"What does {subject_id} require?",
        function="what_requires",
        arguments={"subject": subject_id},
        answer_entities=_answer_ids(edges, pick="to"),
        edges=edges,
    )


def what_limits(subject_id: str, snapshot: GraphSnapshot) -> QueryResult:
    edges = _filter_by_predicate(snapshot, "limits", to_id=subject_id)
    return _build_result(
        question=f"What limits {subject_id}?",
        function="what_limits",
        arguments={"subject": subject_id},
        answer_entities=_answer_ids(edges, pick="from"),
        edges=edges,
    )


def what_defines(subject_id: str, snapshot: GraphSnapshot) -> QueryResult:
    edges = _filter_by_predicate(snapshot, "defines", to_id=subject_id)
    return _build_result(
        question=f"What defines {subject_id}?",
        function="what_defines",
        arguments={"subject": subject_id},
        answer_entities=_answer_ids(edges, pick="from"),
        edges=edges,
    )


def what_depends_on(subject_id: str, snapshot: GraphSnapshot) -> QueryResult:
    edges = _filter_by_predicate(snapshot, "depends_on", from_id=subject_id)
    return _build_result(
        question=f"What does {subject_id} depend on?",
        function="what_depends_on",
        arguments={"subject": subject_id},
        answer_entities=_answer_ids(edges, pick="to"),
        edges=edges,
    )


def what_affects(subject_id: str, snapshot: GraphSnapshot) -> QueryResult:
    matched = [
        e
        for e in snapshot.edges
        if e.type == "affects"
        and (e.from_id == subject_id or e.to_id == subject_id)
    ]
    edges = _sorted_edges(matched)
    other_ids: set[str] = set()
    for edge in edges:
        if edge.from_id == subject_id:
            other_ids.add(edge.to_id)
        else:
            other_ids.add(edge.from_id)
    answer_entities = tuple(sorted(other_ids))
    return _build_result(
        question=f"What affects or is affected by {subject_id}?",
        function="what_affects",
        arguments={"subject": subject_id},
        answer_entities=answer_entities,
        edges=edges,
    )


def supersession_chain(subject_id: str, snapshot: GraphSnapshot) -> QueryResult:
    chain: list[GraphEdge] = []
    visited: set[str] = {subject_id}
    current = subject_id
    by_from: dict[str, list[GraphEdge]] = {}
    for edge in snapshot.edges:
        if edge.type == "supersedes":
            by_from.setdefault(edge.from_id, []).append(edge)
    for edges in by_from.values():
        edges.sort(key=lambda e: (e.to_id, e.evidence_id))

    for _ in range(_MAX_SUPERSESSION_HOPS):
        candidates = by_from.get(current, [])
        next_edge: GraphEdge | None = None
        for edge in candidates:
            if edge.to_id not in visited:
                next_edge = edge
                break
        if next_edge is None:
            break
        chain.append(next_edge)
        visited.add(next_edge.to_id)
        current = next_edge.to_id

    edges = tuple(chain)
    return _build_result(
        question=f"What is the supersession chain of {subject_id}?",
        function="supersession_chain",
        arguments={"subject": subject_id},
        answer_entities=tuple(e.to_id for e in edges),
        edges=edges,
    )


def neighbors_query(
    subject_id: str,
    snapshot: GraphSnapshot,
    *,
    predicate: str | None = None,
) -> QueryResult:
    matched: list[GraphEdge] = []
    for edge in snapshot.edges:
        if predicate is not None and edge.type != predicate:
            continue
        if edge.from_id == subject_id or edge.to_id == subject_id:
            matched.append(edge)
    edges = _sorted_edges(matched)
    other_ids: set[str] = set()
    for edge in edges:
        if edge.from_id == subject_id:
            other_ids.add(edge.to_id)
        else:
            other_ids.add(edge.from_id)
    arguments: dict[str, str] = {"subject": subject_id}
    if predicate is not None:
        arguments["predicate"] = predicate
    return _build_result(
        question=f"What are the neighbors of {subject_id}?",
        function="neighbors",
        arguments=arguments,
        answer_entities=tuple(sorted(other_ids)),
        edges=edges,
    )


def edges_between(a: str, b: str, snapshot: GraphSnapshot) -> QueryResult:
    matched = [
        e
        for e in snapshot.edges
        if (e.from_id == a and e.to_id == b) or (e.from_id == b and e.to_id == a)
    ]
    edges = _sorted_edges(matched)
    other_ids: set[str] = set()
    for edge in edges:
        other_ids.add(edge.from_id)
        other_ids.add(edge.to_id)
    return _build_result(
        question=f"What edges connect {a} and {b}?",
        function="edges_between",
        arguments={"a": a, "b": b},
        answer_entities=tuple(sorted(other_ids)),
        edges=edges,
    )
