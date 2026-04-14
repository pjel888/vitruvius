from __future__ import annotations

from dataclasses import dataclass

import networkx as nx

from .contract import GraphSnapshot


MAX_TDA_NODES = 100


class TDACapacityError(ValueError):
    """Raised when a snapshot has more nodes than MAX_TDA_NODES."""


@dataclass(frozen=True)
class BettiNumbers:
    b0: int
    b1: int
    epsilon: float


@dataclass(frozen=True)
class TDAReport:
    snapshot_size: int
    betti: BettiNumbers
    loop_candidates: tuple[tuple[str, ...], ...]


def _to_undirected(snapshot: GraphSnapshot) -> nx.Graph:
    g = nx.Graph()
    for node in snapshot.nodes:
        g.add_node(node.id)
    for edge in snapshot.edges:
        if edge.from_id != edge.to_id:
            g.add_edge(edge.from_id, edge.to_id)
    return g


def compute_betti_numbers(
    snapshot: GraphSnapshot,
    *,
    epsilon: float = 1.0,
) -> TDAReport:
    n_nodes = len(snapshot.nodes)
    if n_nodes > MAX_TDA_NODES:
        raise TDACapacityError(
            f"TDA capped at {MAX_TDA_NODES} nodes (got {n_nodes})"
        )

    if n_nodes == 0:
        return TDAReport(
            snapshot_size=0,
            betti=BettiNumbers(b0=0, b1=0, epsilon=epsilon),
            loop_candidates=(),
        )

    graph = _to_undirected(snapshot)
    b0 = nx.number_connected_components(graph)
    cycles = nx.cycle_basis(graph)
    b1 = len(cycles)

    loop_candidates = tuple(
        tuple(sorted(cycle)) for cycle in cycles
    )

    return TDAReport(
        snapshot_size=n_nodes,
        betti=BettiNumbers(b0=b0, b1=b1, epsilon=epsilon),
        loop_candidates=loop_candidates,
    )
