from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping, Sequence


PIPELINE_STATES: tuple[str, ...] = (
    "scanned",
    "converted",
    "refined",
    "canonicalized",
    "extracted",
    "reviewed",
    "promoted",
    "errored",
)


@dataclass(frozen=True)
class HMMModel:
    states: tuple[str, ...]
    transition_matrix: tuple[tuple[float, ...], ...]
    state_to_index: Mapping[str, int]


def _uniform_row(n: int) -> tuple[float, ...]:
    if n == 0:
        return ()
    share = 1.0 / n
    return tuple(share for _ in range(n))


def fit_hmm_from_registry(
    history: Sequence[tuple[str, str]],
    *,
    states: tuple[str, ...] = PIPELINE_STATES,
) -> HMMModel:
    n = len(states)
    index_by_state = {state: idx for idx, state in enumerate(states)}
    counts: list[list[float]] = [[0.0] * n for _ in range(n)]

    for pair in history:
        if not isinstance(pair, tuple) or len(pair) != 2:
            continue
        from_state, to_state = pair
        if from_state not in index_by_state or to_state not in index_by_state:
            continue
        i = index_by_state[from_state]
        j = index_by_state[to_state]
        counts[i][j] += 1.0

    matrix: list[tuple[float, ...]] = []
    for i in range(n):
        total = sum(counts[i])
        if total == 0.0:
            matrix.append(_uniform_row(n))
            continue
        row = tuple(counts[i][j] / total for j in range(n))
        matrix.append(row)

    return HMMModel(
        states=states,
        transition_matrix=tuple(matrix),
        state_to_index=MappingProxyType(dict(index_by_state)),
    )


def predict_next_state(
    model: HMMModel,
    current_state: str,
) -> dict[str, float]:
    if current_state not in model.state_to_index:
        raise KeyError(f"unknown state {current_state!r}")
    idx = model.state_to_index[current_state]
    row = model.transition_matrix[idx]
    return {state: row[j] for j, state in enumerate(model.states)}
