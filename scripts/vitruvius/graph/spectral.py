from __future__ import annotations

from dataclasses import dataclass

import networkx as nx
import numpy as np
from scipy.sparse.linalg import eigsh

from .contract import GraphSnapshot


@dataclass(frozen=True)
class SpectralPartition:
    partition_a: tuple[str, ...]
    partition_b: tuple[str, ...]
    fiedler_value: float
    fiedler_vector: tuple[float, ...]


def _to_undirected(snapshot: GraphSnapshot) -> nx.Graph:
    g = nx.Graph()
    for node in snapshot.nodes:
        g.add_node(node.id)
    for edge in snapshot.edges:
        g.add_edge(edge.from_id, edge.to_id)
    return g


def compute_spectral_partition(snapshot: GraphSnapshot) -> SpectralPartition:
    if not snapshot.nodes:
        raise ValueError("cannot compute spectral partition on empty snapshot")
    if len(snapshot.nodes) < 2:
        raise ValueError("spectral partitioning requires at least two nodes")

    graph = _to_undirected(snapshot)
    # Stable node ordering for the Laplacian rows/cols.
    node_order = sorted(n.id for n in snapshot.nodes)
    laplacian = nx.laplacian_matrix(graph, nodelist=node_order).astype(float)

    n_nodes = len(node_order)
    dense = laplacian.toarray()
    # Symmetric real eigendecomposition; deterministic.
    eigvals, eigvecs = np.linalg.eigh(dense)
    # Sorted ascending by numpy.linalg.eigh → Fiedler is index 1.
    fiedler_value = float(eigvals[1])
    fiedler_vec = eigvecs[:, 1]

    partition_a: list[str] = []
    partition_b: list[str] = []
    for idx, node_id in enumerate(node_order):
        if fiedler_vec[idx] >= 0:
            partition_a.append(node_id)
        else:
            partition_b.append(node_id)

    return SpectralPartition(
        partition_a=tuple(sorted(partition_a)),
        partition_b=tuple(sorted(partition_b)),
        fiedler_value=fiedler_value,
        fiedler_vector=tuple(float(x) for x in fiedler_vec),
    )


# Re-export so `from vitruvius.graph.spectral import eigsh` remains possible
# for downstream overlays that want the sparse path. Not used here after we
# switched to dense eigh for determinism on tiny snapshots.
__all__ = ["SpectralPartition", "compute_spectral_partition", "eigsh"]
