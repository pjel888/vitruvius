from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from ..graph.community import CommunityReport


RouteKind = Literal["community", "specific"]
QueryScope = Literal["macro", "specific"]


_MACRO_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\boverarching\b", re.IGNORECASE),
    re.compile(r"\bthemes?\b", re.IGNORECASE),
    re.compile(r"\bsummari[sz]e\b", re.IGNORECASE),
    re.compile(r"\bwhat concepts\b", re.IGNORECASE),
    re.compile(r"\bhigh[- ]level\b", re.IGNORECASE),
    re.compile(r"\boverview\b", re.IGNORECASE),
    re.compile(r"\ball\b.*\bconcepts?\b", re.IGNORECASE),
    re.compile(r"\bwhat are the\b", re.IGNORECASE),
    re.compile(r"\bcluster", re.IGNORECASE),
    re.compile(r"\btopics?\b", re.IGNORECASE),
)


@dataclass(frozen=True)
class RoutingDecision:
    route: RouteKind
    target_community_ids: tuple[int, ...]
    reason: str


def classify_query_macro_vs_specific(question: str) -> QueryScope:
    for pattern in _MACRO_PATTERNS:
        if pattern.search(question):
            return "macro"
    return "specific"


def route_query(
    question: str,
    *,
    community_report: CommunityReport,
) -> RoutingDecision:
    scope = classify_query_macro_vs_specific(question)
    if scope == "macro":
        ids = tuple(c.community_id for c in community_report.communities)
        if not ids:
            return RoutingDecision(
                route="community",
                target_community_ids=(),
                reason="macro query with no communities available",
            )
        return RoutingDecision(
            route="community",
            target_community_ids=ids,
            reason="macro query — routed to all communities",
        )
    return RoutingDecision(
        route="specific",
        target_community_ids=(),
        reason="specific query — routed to entity-level engine",
    )
