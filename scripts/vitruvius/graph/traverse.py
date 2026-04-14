from __future__ import annotations

from collections import deque
from typing import Literal

from .contract import GraphEdge, GraphNode, GraphSnapshot


Direction = Literal["out", "in", "both"]


def _nodes_by_id(snapshot: GraphSnapshot) -> dict[str, GraphNode]:
    return {n.id: n for n in snapshot.nodes}


def neighbors(
    snapshot: GraphSnapshot,
    node_id: str,
    *,
    direction: Direction = "out",
) -> list[GraphNode]:
    by_id = _nodes_by_id(snapshot)
    neighbor_ids: set[str] = set()
    for edge in snapshot.edges:
        if direction in ("out", "both") and edge.from_id == node_id:
            neighbor_ids.add(edge.to_id)
        if direction in ("in", "both") and edge.to_id == node_id:
            neighbor_ids.add(edge.from_id)
    result: list[GraphNode] = []
    for nid in sorted(neighbor_ids):
        node = by_id.get(nid)
        if node is not None:
            result.append(node)
    return result


def typed_edges(
    snapshot: GraphSnapshot,
    node_id: str,
    predicate: str,
) -> list[GraphEdge]:
    matched = [
        e
        for e in snapshot.edges
        if e.type == predicate and (e.from_id == node_id or e.to_id == node_id)
    ]
    matched.sort(key=lambda e: (e.from_id, e.to_id, e.evidence_id))
    return matched


def evidence_joined_paths(
    snapshot: GraphSnapshot,
    from_id: str,
    to_id: str,
    *,
    max_depth: int = 3,
) -> list[list[GraphEdge]]:
    if from_id == to_id:
        return []
    if max_depth < 1:
        return []

    adjacency: dict[str, list[GraphEdge]] = {}
    for edge in snapshot.edges:
        adjacency.setdefault(edge.from_id, []).append(edge)
    for edges in adjacency.values():
        edges.sort(key=lambda e: (e.to_id, e.type, e.evidence_id))

    results: list[list[GraphEdge]] = []
    queue: deque[tuple[str, list[GraphEdge], frozenset[str]]] = deque()
    queue.append((from_id, [], frozenset({from_id})))

    while queue:
        current, path, visited = queue.popleft()
        if len(path) >= max_depth:
            continue
        for edge in adjacency.get(current, []):
            if edge.to_id in visited:
                continue
            new_path = path + [edge]
            if edge.to_id == to_id:
                results.append(new_path)
                continue
            queue.append((edge.to_id, new_path, visited | {edge.to_id}))

    results.sort(
        key=lambda p: (
            len(p),
            tuple((e.from_id, e.type, e.to_id, e.evidence_id) for e in p),
        )
    )
    return results
