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
