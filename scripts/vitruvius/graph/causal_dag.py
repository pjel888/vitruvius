from __future__ import annotations

from dataclasses import dataclass

import networkx as nx

from .contract import GraphSnapshot


class CyclicGraphError(ValueError):
    """Raised when the snapshot contains cycles (not a DAG)."""


@dataclass(frozen=True)
class InterventionResult:
    intervened_node: str
    descendants_affected: tuple[str, ...]
    intervention_value: float


def _to_digraph(snapshot: GraphSnapshot) -> nx.DiGraph:
    g = nx.DiGraph()
    for node in snapshot.nodes:
        g.add_node(node.id)
    for edge in snapshot.edges:
        g.add_edge(edge.from_id, edge.to_id)
    return g


def assert_is_dag(snapshot: GraphSnapshot) -> None:
    graph = _to_digraph(snapshot)
    if not nx.is_directed_acyclic_graph(graph):
        raise CyclicGraphError(
            "snapshot contains cycles; cannot treat as a causal DAG"
        )


def intervention(
    snapshot: GraphSnapshot,
    *,
    node_id: str,
    value: float,
) -> InterventionResult:
    node_ids = {n.id for n in snapshot.nodes}
    if node_id not in node_ids:
        raise KeyError(f"node_id {node_id!r} not in snapshot")

    graph = _to_digraph(snapshot)
    if not nx.is_directed_acyclic_graph(graph):
        raise CyclicGraphError(
            "snapshot contains cycles; cannot compute do-intervention"
        )

    descendants = tuple(sorted(nx.descendants(graph, node_id)))
    return InterventionResult(
        intervened_node=node_id,
        descendants_affected=descendants,
        intervention_value=value,
    )
