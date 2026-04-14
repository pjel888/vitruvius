"""Stream L.5 — Z3 SMT evaluator for parametric spatial constraints.

Imports z3 lazily inside evaluate_constraint so the module can be
imported without z3-solver installed (keeps pytest collection fast and
flag-off paths unbroken).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


_KNOWN_OPERATORS = frozenset({">=", "<=", "==", ">", "<"})


@dataclass(frozen=True)
class ParametricConstraint:
    concept_id: str
    variable: str
    operator: str
    threshold: float


@dataclass(frozen=True)
class EvaluationResult:
    concept_id: str
    variable: str
    observed: float | None
    passed: bool
    reason: str


def _sat_to_bool(z3_mod, solver) -> bool:
    return solver.check() == z3_mod.sat


def evaluate_constraint(
    constraint: ParametricConstraint,
    observed: float,
) -> EvaluationResult:
    if constraint.operator not in _KNOWN_OPERATORS:
        raise ValueError(
            f"unknown operator {constraint.operator!r}; expected one of {sorted(_KNOWN_OPERATORS)}"
        )

    try:
        import z3
    except ImportError as exc:
        raise RuntimeError(
            "z3-solver is not installed; run `pip install z3-solver` to enable Stream L.5"
        ) from exc

    observed_f = float(observed)
    threshold_f = float(constraint.threshold)

    solver = z3.Solver()
    obs_var = z3.Real(f"{constraint.variable}_obs")
    thr_var = z3.Real(f"{constraint.variable}_thr")
    solver.add(obs_var == observed_f)
    solver.add(thr_var == threshold_f)
    if constraint.operator == ">=":
        solver.add(obs_var >= thr_var)
    elif constraint.operator == "<=":
        solver.add(obs_var <= thr_var)
    elif constraint.operator == "==":
        solver.add(obs_var == thr_var)
    elif constraint.operator == ">":
        solver.add(obs_var > thr_var)
    elif constraint.operator == "<":
        solver.add(obs_var < thr_var)

    passed = _sat_to_bool(z3, solver)
    reason = (
        f"Z3 SAT: {constraint.variable}={observed_f} {constraint.operator} {threshold_f}"
        if passed
        else f"Z3 UNSAT: {constraint.variable}={observed_f} {constraint.operator} {threshold_f}"
    )
    return EvaluationResult(
        concept_id=constraint.concept_id,
        variable=constraint.variable,
        observed=observed_f,
        passed=passed,
        reason=reason,
    )


def evaluate_batch(
    constraints: Sequence[ParametricConstraint],
    observations: Mapping[str, float],
) -> list[EvaluationResult]:
    results: list[EvaluationResult] = []
    for constraint in constraints:
        if constraint.variable not in observations:
            results.append(
                EvaluationResult(
                    concept_id=constraint.concept_id,
                    variable=constraint.variable,
                    observed=None,
                    passed=False,
                    reason=f"missing observation for variable {constraint.variable!r}",
                )
            )
            continue
        results.append(evaluate_constraint(constraint, observed=observations[constraint.variable]))
    return results


import re as _re

from ..parsers.parametric_ner import Parameter as _Parameter


def _slugify(value: str) -> str:
    lowered = value.strip().lower()
    slug = _re.sub(r"[^a-z0-9]+", "-", lowered)
    return slug.strip("-")


def parameters_to_constraints(
    parameters: Sequence[_Parameter],
) -> list[ParametricConstraint]:
    out: list[ParametricConstraint] = []
    for param in parameters:
        entity_slug = _slugify(param.entity)
        concept_id = f"concept-{entity_slug}" if entity_slug else "concept-unknown"
        unit_suffix = param.unit or "unitless"
        variable = f"{entity_slug}_{unit_suffix}" if entity_slug else unit_suffix
        out.append(
            ParametricConstraint(
                concept_id=concept_id,
                variable=variable,
                operator=param.operator,
                threshold=float(param.value),
            )
        )
    return out
