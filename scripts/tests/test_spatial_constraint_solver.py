"""Stream L.5 — Z3 constraint solver tests."""
from __future__ import annotations

import pytest

z3 = pytest.importorskip("z3")

from vitruvius.spatial.constraint_solver import (
    EvaluationResult,
    ParametricConstraint,
    evaluate_batch,
    evaluate_constraint,
)


def test_min_setback_passes() -> None:
    c = ParametricConstraint(
        concept_id="concept-setback",
        variable="setback_m",
        operator=">=",
        threshold=2.0,
    )
    result = evaluate_constraint(c, observed=3.0)
    assert isinstance(result, EvaluationResult)
    assert result.passed is True
    assert result.observed == 3.0
    assert result.concept_id == "concept-setback"
    assert result.variable == "setback_m"


def test_min_setback_fails() -> None:
    c = ParametricConstraint(
        concept_id="concept-setback",
        variable="setback_m",
        operator=">=",
        threshold=2.0,
    )
    result = evaluate_constraint(c, observed=1.0)
    assert result.passed is False
    assert result.observed == 1.0


def test_max_footprint_passes() -> None:
    c = ParametricConstraint(
        concept_id="concept-lot-occupancy",
        variable="footprint_percent",
        operator="<=",
        threshold=60.0,
    )
    result = evaluate_constraint(c, observed=50.0)
    assert result.passed is True


def test_max_footprint_fails() -> None:
    c = ParametricConstraint(
        concept_id="concept-lot-occupancy",
        variable="footprint_percent",
        operator="<=",
        threshold=60.0,
    )
    result = evaluate_constraint(c, observed=70.0)
    assert result.passed is False


def test_equal_operator() -> None:
    c = ParametricConstraint(
        concept_id="concept-floor-count",
        variable="floors",
        operator="==",
        threshold=3.0,
    )
    assert evaluate_constraint(c, observed=3.0).passed is True
    assert evaluate_constraint(c, observed=4.0).passed is False


def test_evaluate_batch() -> None:
    setback = ParametricConstraint(
        concept_id="concept-setback",
        variable="setback_m",
        operator=">=",
        threshold=2.0,
    )
    footprint = ParametricConstraint(
        concept_id="concept-lot-occupancy",
        variable="footprint_percent",
        operator="<=",
        threshold=60.0,
    )
    observations = {"setback_m": 3.0, "footprint_percent": 50.0}
    results = evaluate_batch([setback, footprint], observations)
    assert len(results) == 2
    assert all(r.passed for r in results)


def test_evaluate_batch_missing_observation() -> None:
    setback = ParametricConstraint(
        concept_id="concept-setback",
        variable="setback_m",
        operator=">=",
        threshold=2.0,
    )
    results = evaluate_batch([setback], observations={})
    assert len(results) == 1
    assert results[0].passed is False
    assert "missing observation" in results[0].reason.lower()


def test_evaluation_result_is_frozen() -> None:
    c = ParametricConstraint(
        concept_id="concept-x",
        variable="x",
        operator=">",
        threshold=0.0,
    )
    result = evaluate_constraint(c, observed=1.0)
    with pytest.raises(Exception):
        result.passed = False  # type: ignore[misc]


def test_unknown_operator_raises() -> None:
    c = ParametricConstraint(
        concept_id="concept-x",
        variable="x",
        operator="~=",
        threshold=0.0,
    )
    with pytest.raises(ValueError, match="operator"):
        evaluate_constraint(c, observed=1.0)
