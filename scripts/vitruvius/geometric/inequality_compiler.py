"""Sprint GEOM Stream GEOM.1 — inequality compiler.

Takes :class:`vitruvius.parsers.parametric_ner.Parameter` records
(already extracted from legal text by Stream B.4) and compiles them
into Z3 ``Real`` variables + comparison expressions. Given a set of
proposed numeric values, :func:`check_compliance` reports whether all
parameter constraints are jointly satisfied.

This is the narrow "GEOM.1 inequality extraction" deliverable from
phase-15. The full phase-15 scope (3D Boolean polygon envelope,
Pareto optimizer, multimodal IoU audit) is deferred until trimesh,
cvxpy, and libigl are installed on the ops host.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from ..parsers.parametric_ner import Parameter


def _slugify(text: str) -> str:
    """Normalise ``text`` into a lowercased underscore-separated slug."""
    t = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return t or "var"


def compile_parameter_expression(
    param: Parameter,
) -> tuple[Any, Any]:
    """Compile a :class:`Parameter` into a ``(z3_var, z3_expression)`` pair.

    The variable is a :class:`z3.Real` named after the parameter's
    slug. The expression is a comparison between that variable and
    the parameter's numeric value using the parameter's operator
    (``>=`` / ``<=`` / ``==``).
    """
    import z3

    var = z3.Real(_slugify(param.entity))
    value = float(param.value)
    if param.operator == ">=":
        expr = var >= value
    elif param.operator == "<=":
        expr = var <= value
    elif param.operator == "==":
        expr = var == value
    else:
        raise ValueError(
            f"unsupported operator {param.operator!r} in parameter {param!r}"
        )
    return var, expr


@dataclass(frozen=True)
class ComplianceVerdict:
    is_satisfied: bool
    violations: list[str]


def check_compliance(
    parameters: Iterable[Parameter],
    *,
    proposals: Mapping[str, float],
) -> ComplianceVerdict:
    """Check whether ``proposals`` satisfy every compiled parameter.

    ``proposals`` is keyed by parameter-entity slug
    (``_slugify(parameter.entity)``). A proposal that is not present
    in the map leaves the corresponding Z3 variable unconstrained, so
    the solver is free to pick any satisfying value — the verdict
    stays SAT. To make a missing proposal count as a violation, the
    caller should pin the variable to a sentinel before calling
    :func:`check_compliance`.

    Uses Z3's incremental solver: constraints are added one at a time
    and on UNSAT the failing parameter is recorded in
    :attr:`ComplianceVerdict.violations`. Constraint order is
    preserved from ``parameters``.
    """
    import z3

    violations: list[str] = []
    solver = z3.Solver()

    for param in parameters:
        var, expr = compile_parameter_expression(param)
        slug = _slugify(param.entity)
        solver.push()
        solver.add(expr)
        if slug in proposals:
            solver.add(var == float(proposals[slug]))
        if solver.check() == z3.unsat:
            violations.append(
                f"{slug} violates {param.operator} {param.value}{param.unit} "
                f"(proposal={proposals.get(slug, 'unconstrained')})"
            )
            solver.pop()
        else:
            # Keep the satisfying constraint in the cumulative context
            # so subsequent parameters see all assignments that came
            # before. Pop+re-add lets us keep the constraint on the
            # happy path.
            solver.pop()
            solver.add(expr)
            if slug in proposals:
                solver.add(var == float(proposals[slug]))

    return ComplianceVerdict(
        is_satisfied=not violations,
        violations=violations,
    )
