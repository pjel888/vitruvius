"""Choquet integral aggregator — non-additive fuzzy-measure signal fusion (Task F.8)."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import chain, combinations
from typing import Iterable, Mapping


@dataclass(frozen=True)
class Signal:
    name: str
    value: float


@dataclass(frozen=True)
class ChoquetResult:
    aggregate: float
    sorted_signals: tuple[Signal, ...]


def _powerset(names: Iterable[str]) -> Iterable[frozenset[str]]:
    names_list = list(names)
    return (
        frozenset(subset)
        for subset in chain.from_iterable(
            combinations(names_list, r) for r in range(len(names_list) + 1)
        )
    )


def additive_measure(signal_names: list[str]) -> dict[frozenset[str], float]:
    n = len(signal_names)
    if n == 0:
        return {frozenset(): 0.0}
    return {subset: len(subset) / n for subset in _powerset(signal_names)}


def _lookup_measure(
    subset: frozenset[str],
    measure: Mapping[frozenset[str], float],
) -> float:
    if subset in measure:
        return float(measure[subset])
    if not subset:
        return 0.0
    # Naive fallback: average of single-element measures if available, else |subset|/|full|.
    single_values = [
        float(measure[frozenset({name})])
        for name in subset
        if frozenset({name}) in measure
    ]
    if single_values:
        return min(1.0, sum(single_values))
    all_known = list(measure.values())
    max_known = max(all_known) if all_known else 1.0
    if max_known == 0.0:
        return 0.0
    return min(1.0, len(subset) / max(1, len(max(measure.keys(), key=len, default=frozenset()))))


def choquet_integral(
    signals: list[Signal],
    *,
    fuzzy_measure: Mapping[frozenset[str], float],
) -> ChoquetResult:
    if not signals:
        return ChoquetResult(aggregate=0.0, sorted_signals=())

    sorted_signals = tuple(sorted(signals, key=lambda s: s.value))
    n = len(sorted_signals)
    prev_value = 0.0
    aggregate = 0.0
    for i, signal in enumerate(sorted_signals):
        # A_i = { names of sorted_signals[i:] } — the elements with value >= current
        upper_set = frozenset(s.name for s in sorted_signals[i:])
        measure_value = _lookup_measure(upper_set, fuzzy_measure)
        delta = signal.value - prev_value
        aggregate += delta * measure_value
        prev_value = signal.value

    aggregate = max(0.0, min(1.0, aggregate))

    return ChoquetResult(aggregate=aggregate, sorted_signals=sorted_signals)
