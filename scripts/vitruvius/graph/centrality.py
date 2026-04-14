from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import networkx as nx

from .contract import GraphSnapshot


CentralityKind = Literal["degree", "betweenness", "pagerank"]

_ALLOWED_KINDS: frozenset[str] = frozenset({"degree", "betweenness", "pagerank"})


@dataclass(frozen=True)
class CentralityReport:
    kind: CentralityKind
    scores: tuple[tuple[str, float], ...]


def _to_digraph(snapshot: GraphSnapshot) -> nx.DiGraph:
    g = nx.DiGraph()
    for node in snapshot.nodes:
        g.add_node(node.id)
    for edge in snapshot.edges:
        g.add_edge(edge.from_id, edge.to_id)
    return g


def _sorted_scores(raw: dict[str, float]) -> tuple[tuple[str, float], ...]:
    return tuple(sorted(raw.items(), key=lambda item: (-item[1], item[0])))


def compute_centrality(
    snapshot: GraphSnapshot,
    *,
    kind: CentralityKind = "pagerank",
    alpha: float = 0.85,
) -> CentralityReport:
    if kind not in _ALLOWED_KINDS:
        raise ValueError(
            f"unknown centrality kind {kind!r}; expected one of {sorted(_ALLOWED_KINDS)}"
        )
    if not snapshot.nodes:
        return CentralityReport(kind=kind, scores=())

    graph = _to_digraph(snapshot)

    if kind == "degree":
        raw = nx.degree_centrality(graph)
    elif kind == "betweenness":
        raw = nx.betweenness_centrality(graph)
    else:
        raw = nx.pagerank(graph, alpha=alpha)

    return CentralityReport(kind=kind, scores=_sorted_scores(raw))
