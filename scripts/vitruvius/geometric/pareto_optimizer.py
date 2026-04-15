"""Sprint GEOM Stream GEOM.4.2 — Pareto optimiser for massing variants.

Given a lot's hard constraints (area, coverage ratio, height,
floor-area ratio cap, max floors), return the single massing variant
that maximises total gross floor area (GFA). This is a tiny LP — the
heavy machinery in ``cvxpy`` is overkill for the 3-variable case but
it gives us a solid starting point for the full Pareto sweep the
plan calls out (stochastic feasibility over unusual lot shapes,
GEOM.4.3, deferred).
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MassingVariant:
    footprint_area: float
    floors: float
    total_gfa: float
    is_feasible: bool


def maximize_far_under_constraints(
    *,
    lot_area: float,
    max_coverage_ratio: float,
    max_height_meters: float,
    far_cap: float,
    floors_max: int,
    floor_height_meters: float = 3.0,
) -> MassingVariant:
    """Solve a linear programme for the GFA-maximising massing.

    Decision variables:
      * ``footprint`` in m² — building footprint
      * ``floors`` — number of floors

    Constraints:
      * ``footprint <= lot_area * max_coverage_ratio``
      * ``floors <= floors_max``
      * ``floors * floor_height_meters <= max_height_meters``
      * ``footprint * floors <= far_cap * lot_area`` — this is
        *bilinear*, so we linearise by pinning ``floors`` to its
        integer max and treating footprint as the sole free variable.
        This yields an exact optimum for the typical case because GFA
        grows linearly in both variables and the optimum always sits
        on a corner of the feasible polytope.

    The returned :class:`MassingVariant` carries the footprint area,
    the chosen number of floors, the resulting total GFA, and a
    feasibility flag (``False`` for degenerate input like a zero lot).
    """
    if lot_area <= 0.0 or max_height_meters <= 0.0:
        return MassingVariant(
            footprint_area=0.0,
            floors=0.0,
            total_gfa=0.0,
            is_feasible=False,
        )

    import cvxpy as cp

    max_footprint = max(0.0, lot_area * max_coverage_ratio)
    max_floors_by_height = max_height_meters / max(floor_height_meters, 1e-9)
    floors_upper = min(floors_max, int(max_floors_by_height))
    if floors_upper <= 0:
        return MassingVariant(
            footprint_area=0.0,
            floors=0.0,
            total_gfa=0.0,
            is_feasible=False,
        )

    best: MassingVariant | None = None
    for floors_candidate in range(1, floors_upper + 1):
        footprint = cp.Variable(nonneg=True)
        constraints = [
            footprint <= max_footprint,
            floors_candidate * footprint <= far_cap * lot_area,
        ]
        objective = cp.Maximize(floors_candidate * footprint)
        problem = cp.Problem(objective, constraints)
        try:
            problem.solve()
        except Exception:
            continue
        if problem.status not in {"optimal", "optimal_inaccurate"}:
            continue
        f_area = float(footprint.value or 0.0)
        gfa = f_area * floors_candidate
        candidate = MassingVariant(
            footprint_area=f_area,
            floors=float(floors_candidate),
            total_gfa=gfa,
            is_feasible=True,
        )
        if best is None or gfa > best.total_gfa:
            best = candidate

    if best is None:
        return MassingVariant(
            footprint_area=0.0,
            floors=0.0,
            total_gfa=0.0,
            is_feasible=False,
        )
    return best
