from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .contract import GraphSnapshot


@dataclass(frozen=True)
class MCMCStationaryDistribution:
    seed_id: str
    alpha: float
    steps: int
    visit_frequency: tuple[tuple[str, float], ...]


def _build_adjacency(snapshot: GraphSnapshot) -> dict[str, list[str]]:
    adj: dict[str, list[str]] = {node.id: [] for node in snapshot.nodes}
    for edge in snapshot.edges:
        if edge.from_id in adj:
            adj[edge.from_id].append(edge.to_id)
    for neighbors in adj.values():
        neighbors.sort()
    return adj


def mcmc_random_walk(
    snapshot: GraphSnapshot,
    *,
    seed_id: str,
    alpha: float = 0.85,
    steps: int = 10_000,
    rng_seed: int = 0,
) -> MCMCStationaryDistribution:
    node_ids = {n.id for n in snapshot.nodes}
    if seed_id not in node_ids:
        raise KeyError(f"seed_id {seed_id!r} not in snapshot")

    adjacency = _build_adjacency(snapshot)
    rng = np.random.default_rng(rng_seed)
    visits: dict[str, int] = {nid: 0 for nid in node_ids}
    current = seed_id

    for _ in range(steps):
        visits[current] += 1
        out_neighbors = adjacency.get(current, [])
        # Teleport on (1 - alpha) OR when no outgoing edges exist.
        if not out_neighbors or rng.random() >= alpha:
            current = seed_id
        else:
            idx = int(rng.integers(0, len(out_neighbors)))
            current = out_neighbors[idx]

    total = sum(visits.values()) or 1
    freq = {nid: count / total for nid, count in visits.items()}
    sorted_freq = tuple(
        sorted(freq.items(), key=lambda item: (-item[1], item[0]))
    )

    return MCMCStationaryDistribution(
        seed_id=seed_id,
        alpha=alpha,
        steps=steps,
        visit_frequency=sorted_freq,
    )
