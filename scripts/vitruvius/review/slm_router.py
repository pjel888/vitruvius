"""SLM complexity router — deterministic rules for Ollama model selection (Task F.2)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Mapping


ComplexityLevel = Literal["simple", "medium", "complex"]

DEFAULT_MODEL_MAP: dict[ComplexityLevel, str] = {
    "simple": "qwen2.5:3b-instruct-q4_K_M",
    "medium": "qwen2.5:7b-instruct-q4_K_M",
    "complex": "gemma4:31b",
}

_COMPLEX_EVIDENCE_CHAR_THRESHOLD = 2000
_MEDIUM_EVIDENCE_CHAR_THRESHOLD = 500
_COMPLEX_SENTENCE_THRESHOLD = 5
_MEDIUM_CRF_CONFIDENCE_THRESHOLD = 0.6


@dataclass(frozen=True)
class ComplexitySignals:
    predicate: str
    evidence_char_count: int
    sentence_count: int
    has_negation: bool
    crf_confidence: float | None
    regex_pattern_id: str


@dataclass(frozen=True)
class RoutingDecision:
    level: ComplexityLevel
    model_name: str
    reason: str


def _complex_reason(signals: ComplexitySignals) -> str:
    reasons: list[str] = []
    if signals.evidence_char_count > _COMPLEX_EVIDENCE_CHAR_THRESHOLD:
        reasons.append(f"evidence_char_count={signals.evidence_char_count} > {_COMPLEX_EVIDENCE_CHAR_THRESHOLD}")
    if signals.sentence_count > _COMPLEX_SENTENCE_THRESHOLD:
        reasons.append(f"sentence_count={signals.sentence_count} > {_COMPLEX_SENTENCE_THRESHOLD}")
    if signals.has_negation:
        reasons.append("negation present")
    return "complex: " + ", ".join(reasons) if reasons else "complex"


def _medium_reason(signals: ComplexitySignals) -> str:
    reasons: list[str] = []
    if signals.crf_confidence is None:
        reasons.append("CRF confidence missing")
    elif signals.crf_confidence < _MEDIUM_CRF_CONFIDENCE_THRESHOLD:
        reasons.append(f"crf_confidence={signals.crf_confidence:.2f} < {_MEDIUM_CRF_CONFIDENCE_THRESHOLD}")
    if signals.evidence_char_count > _MEDIUM_EVIDENCE_CHAR_THRESHOLD:
        reasons.append(f"evidence_char_count={signals.evidence_char_count} > {_MEDIUM_EVIDENCE_CHAR_THRESHOLD}")
    return "medium: " + ", ".join(reasons) if reasons else "medium"


def _simple_reason(signals: ComplexitySignals) -> str:
    return (
        "simple: short evidence, "
        f"crf_confidence={signals.crf_confidence:.2f}, no negation"
        if signals.crf_confidence is not None
        else "simple: short evidence, no negation"
    )


def classify_complexity(signals: ComplexitySignals) -> ComplexityLevel:
    if (
        signals.evidence_char_count > _COMPLEX_EVIDENCE_CHAR_THRESHOLD
        or signals.sentence_count > _COMPLEX_SENTENCE_THRESHOLD
        or signals.has_negation
    ):
        return "complex"
    if (
        signals.crf_confidence is None
        or signals.crf_confidence < _MEDIUM_CRF_CONFIDENCE_THRESHOLD
        or signals.evidence_char_count > _MEDIUM_EVIDENCE_CHAR_THRESHOLD
    ):
        return "medium"
    return "simple"


def route(
    signals: ComplexitySignals,
    *,
    model_map: Mapping[ComplexityLevel, str] = DEFAULT_MODEL_MAP,
) -> RoutingDecision:
    level = classify_complexity(signals)
    if level == "complex":
        reason = _complex_reason(signals)
    elif level == "medium":
        reason = _medium_reason(signals)
    else:
        reason = _simple_reason(signals)
    return RoutingDecision(
        level=level,
        model_name=model_map[level],
        reason=reason,
    )


# ---------------------------------------------------------------------------
# Stream Y2.2 — domain-aware MoE router (append-only extension; the original
# complexity-only `route()` function above is unchanged).
# ---------------------------------------------------------------------------
from typing import Any, Mapping as _Mapping  # noqa: E402 — append-only

from .domain_classifier import Domain, classify_domain  # noqa: E402


@dataclass(frozen=True)
class MoEVerdict:
    """Result of :func:`route_with_moe` — which model to dispatch and why."""

    model: str
    domain: Domain


def route_with_moe(
    *,
    candidate: _Mapping[str, Any],
    moe_policy: _Mapping[Domain, str],
) -> MoEVerdict:
    """Pick a model by the classified domain of a relationship candidate.

    Does NOT replace the legacy ``route`` function — composes with it.
    Callers that still want complexity-only routing stay on ``route``;
    new callers that want domain routing call ``route_with_moe``.

    Falls back to ``moe_policy[Domain.OTHER]`` if the classified domain
    is missing from the policy map, so partial policies still produce a
    deterministic model pick.
    """
    subject = str(candidate.get("subject", ""))
    predicate = str(candidate.get("predicate", ""))
    obj = str(candidate.get("object", ""))

    domain = classify_domain(subject=subject, predicate=predicate, object_=obj)
    model = moe_policy.get(domain) or moe_policy[Domain.OTHER]
    return MoEVerdict(model=model, domain=domain)
