from __future__ import annotations

from typing import Sequence

from ..graph.contract import GraphSnapshot
from ..graph.mcmc import mcmc_random_walk


def rank_answer_entities(
    entities: Sequence[str],
    *,
    snapshot: GraphSnapshot,
    seed_id: str,
    alpha: float = 0.85,
    steps: int = 10_000,
    rng_seed: int = 0,
) -> list[tuple[str, float]]:
    if not entities:
        return []
    distribution = mcmc_random_walk(
        snapshot,
        seed_id=seed_id,
        alpha=alpha,
        steps=steps,
        rng_seed=rng_seed,
    )
    freq_map = dict(distribution.visit_frequency)
    scored = [(entity, freq_map.get(entity, 0.0)) for entity in entities]
    scored.sort(key=lambda item: (-item[1], item[0]))
    return scored
