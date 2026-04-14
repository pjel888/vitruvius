from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class QueryCitation:
    source_id: str
    source_section_id: str
    evidence_snippet: str
    confidence: float


@dataclass(frozen=True)
class QueryResult:
    question: str
    answer_entities: tuple[str, ...]
    citations: tuple[QueryCitation, ...]
    aggregate_confidence: float
    has_evidence: bool
    query_function: str
    arguments: Mapping[str, str]


def compute_aggregate_confidence(citations: tuple[QueryCitation, ...]) -> float:
    if not citations:
        return 0.0
    return min(c.confidence for c in citations)
