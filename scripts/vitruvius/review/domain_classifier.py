"""Stream Y2.1 — deterministic domain classifier for a relationship candidate.

Maps (subject, predicate, object) tuples into one of 6 semantic domains.
Used by ``slm_router.route_with_moe`` (Y2.2) to pick domain-specialised
models. Intentionally simple — later we can swap in a trained multinomial
classifier once enough audit data accumulates, but deterministic regex
is sufficient for the initial ship.
"""
from __future__ import annotations

import re
from enum import Enum


class Domain(str, Enum):
    GEOMETRIC = "geometric"
    ADMINISTRATIVE = "administrative"
    OCCUPANCY = "occupancy"
    SAFETY = "safety"
    FEES = "fees"
    OTHER = "other"


_PREDICATE_PATTERNS: list[tuple[re.Pattern[str], Domain]] = [
    # FEES is checked first so a candidate with both "fee" and "permit"
    # (e.g. "permit fee: 5000 PHP") lands in FEES rather than being
    # swallowed by the ADMINISTRATIVE "permit" match.
    (re.compile(r"fee|cost|charge|payment|bond|deposit|PHP", re.I), Domain.FEES),
    (re.compile(r"setback|height|width|depth|area|diameter|distance", re.I), Domain.GEOMETRIC),
    (re.compile(r"occupan|load|capacity|persons|people|residents", re.I), Domain.OCCUPANCY),
    (re.compile(r"fire|safety|hazard|emergency|escape|alarm", re.I), Domain.SAFETY),
    (re.compile(r"permit|notify|clearance|apply|submit|approval|certify|issue", re.I), Domain.ADMINISTRATIVE),
]


def classify_domain(*, subject: str, predicate: str, object_: str) -> Domain:
    """Deterministically classify a relationship candidate into a domain.

    Returns :class:`Domain.OTHER` when no pattern matches. Case-insensitive.
    """
    haystack = f"{subject} {predicate} {object_}"
    for pattern, domain in _PREDICATE_PATTERNS:
        if pattern.search(haystack):
            return domain
    return Domain.OTHER
