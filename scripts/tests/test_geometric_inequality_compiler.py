"""Sprint GEOM Stream GEOM.1 — inequality compiler tests."""
from __future__ import annotations

import pytest

pytest.importorskip("z3")

from vitruvius.geometric.inequality_compiler import (
    ComplianceVerdict,
    check_compliance,
    compile_parameter_expression,
)
from vitruvius.parsers.parametric_ner import Parameter


def _param(
    entity: str, op: str, value: float, unit: str = "m"
) -> Parameter:
    return Parameter(
        entity=entity,
        operator=op,
        value=value,
        unit=unit,
        start=0,
        end=len(entity),
        evidence=f"{entity} {op} {value}{unit}",
    )


def test_compile_minimum_parameter_produces_ge_expression() -> None:
    param = _param("setback", ">=", 3.0)
    var, expr = compile_parameter_expression(param)
    assert var is not None
    assert expr is not None
    # The Z3 str() form of the expression should contain the comparator.
    assert ">=" in str(expr)
    assert "3" in str(expr)


def test_compile_maximum_parameter_produces_le_expression() -> None:
    param = _param("building height", "<=", 15.0)
    var, expr = compile_parameter_expression(param)
    # Z3 renders `a <= b` as a string containing "<=" or "Not(>=)" etc;
    # simplest contract: the expression is satisfied when the var is
    # less than or equal to the value.
    import z3
    solver = z3.Solver()
    solver.add(expr)
    solver.add(var == 10.0)
    assert solver.check() == z3.sat

    solver2 = z3.Solver()
    solver2.add(expr)
    solver2.add(var == 20.0)
    assert solver2.check() == z3.unsat


def test_compile_equality_parameter_produces_eq_expression() -> None:
    import z3

    param = _param("floor area", "==", 500.0, unit="m2")
    var, expr = compile_parameter_expression(param)
    solver = z3.Solver()
    solver.add(expr)
    solver.add(var == 500.0)
    assert solver.check() == z3.sat

    solver2 = z3.Solver()
    solver2.add(expr)
    solver2.add(var == 499.9)
    assert solver2.check() == z3.unsat


def test_check_compliance_all_satisfied() -> None:
    params = [
        _param("setback", ">=", 3.0),
        _param("building height", "<=", 15.0),
    ]
    verdict = check_compliance(
        params,
        proposals={"setback": 5.0, "building_height": 12.0},
    )
    assert isinstance(verdict, ComplianceVerdict)
    assert verdict.is_satisfied is True
    assert verdict.violations == []


def test_check_compliance_reports_violation() -> None:
    params = [
        _param("setback", ">=", 3.0),
        _param("building height", "<=", 15.0),
    ]
    verdict = check_compliance(
        params,
        proposals={"setback": 2.0, "building_height": 12.0},
    )
    assert verdict.is_satisfied is False
    assert len(verdict.violations) == 1
    assert "setback" in verdict.violations[0]


def test_check_compliance_missing_proposal_is_unknown() -> None:
    params = [_param("setback", ">=", 3.0)]
    verdict = check_compliance(params, proposals={})
    # With no proposal the parameter's variable is unconstrained so
    # there's always a satisfying assignment — the verdict says SAT.
    assert verdict.is_satisfied is True
