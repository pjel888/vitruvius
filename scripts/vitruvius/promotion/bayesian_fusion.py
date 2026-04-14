from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

DEFAULT_PRIOR: float = 0.10

DEFAULT_BAYES_FACTORS: dict[str, float] = {
    "regex_match": 6.0,
    "tfidf_match": 1.4,
    "crf_tag": 1.1,
    "llm_agreement": 1.06,
}


@dataclass(frozen=True)
class EvidenceSignal:
    source: str
    observed: bool
    bayes_factor: float | None = None


@dataclass(frozen=True)
class FusionResult:
    prior: float
    posterior: float
    log_odds: float
    applied_signals: tuple[str, ...]


def _logit(p: float) -> float:
    p = min(max(p, 1e-12), 1 - 1e-12)
    return math.log(p / (1 - p))


def _sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def _resolve_factor(
    signal: EvidenceSignal,
    bayes_factors: dict[str, float],
) -> float:
    if signal.bayes_factor is not None:
        return signal.bayes_factor
    try:
        return bayes_factors[signal.source]
    except KeyError as exc:
        raise KeyError(
            f"unknown evidence source {signal.source!r}; either add it to "
            f"bayes_factors or set EvidenceSignal.bayes_factor explicitly"
        ) from exc


def fuse_evidence(
    signals: Iterable[EvidenceSignal],
    *,
    prior: float = DEFAULT_PRIOR,
    bayes_factors: dict[str, float] = DEFAULT_BAYES_FACTORS,
) -> FusionResult:
    """Combine evidence signals into a posterior via log-odds update.

    Each observed signal adds ``log(bayes_factor)`` to the running log-odds.
    Non-observed signals are skipped. Order is irrelevant (addition commutes).
    """
    log_odds = _logit(prior)
    applied: list[str] = []

    for signal in signals:
        if not signal.observed:
            continue
        factor = _resolve_factor(signal, bayes_factors)
        log_odds += math.log(factor)
        applied.append(signal.source)

    return FusionResult(
        prior=prior,
        posterior=_sigmoid(log_odds),
        log_odds=log_odds,
        applied_signals=tuple(applied),
    )
