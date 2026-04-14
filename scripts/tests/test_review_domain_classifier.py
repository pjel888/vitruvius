"""Stream Y2.1 — domain classifier unit tests."""
from __future__ import annotations

import pytest

from vitruvius.review.domain_classifier import classify_domain, Domain


@pytest.mark.parametrize(
    "predicate, subject, obj, expected",
    [
        ("has_setback", "building", "3 meters", Domain.GEOMETRIC),
        ("has_height_limit", "structure", "15 meters", Domain.GEOMETRIC),
        ("requires_permit", "construction", "building official", Domain.ADMINISTRATIVE),
        ("must_notify", "owner", "barangay", Domain.ADMINISTRATIVE),
        ("has_occupancy_load", "floor", "50 persons", Domain.OCCUPANCY),
        ("must_comply_with", "building", "fire code", Domain.SAFETY),
        ("has_fee", "permit", "5000 PHP", Domain.FEES),
        ("relates_to", "term1", "term2", Domain.OTHER),
    ],
)
def test_classify_domain_by_predicate(predicate, subject, obj, expected) -> None:
    domain = classify_domain(subject=subject, predicate=predicate, object_=obj)
    assert domain == expected


def test_classify_domain_is_deterministic() -> None:
    a = classify_domain(subject="x", predicate="has_setback", object_="y")
    b = classify_domain(subject="x", predicate="has_setback", object_="y")
    assert a == b
