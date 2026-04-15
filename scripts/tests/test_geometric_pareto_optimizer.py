"""Sprint GEOM Stream GEOM.4.2 — Pareto optimizer tests (cvxpy)."""
from __future__ import annotations

import pytest

pytest.importorskip("cvxpy")
pytest.importorskip("shapely")

from vitruvius.geometric.pareto_optimizer import (
    MassingVariant,
    maximize_far_under_constraints,
)


def test_far_optimizer_maximises_area_under_lot_coverage() -> None:
    """Given lot area 400 m², max coverage 60%, max height 15m, and
    FAR cap 3.0 — the optimizer should pick a massing that saturates
    both the coverage and the FAR cap.
    """
    variant = maximize_far_under_constraints(
        lot_area=400.0,
        max_coverage_ratio=0.60,   # footprint <= 240 m²
        max_height_meters=15.0,
        far_cap=3.0,               # total_gfa <= 1200 m²
        floors_max=10,
    )
    assert isinstance(variant, MassingVariant)
    assert variant.footprint_area <= 240.0 + 1e-6
    assert variant.total_gfa <= 1200.0 + 1e-6
    # The optimal is footprint=240, floors=5 → GFA=1200 (saturates FAR).
    assert variant.total_gfa == pytest.approx(1200.0, rel=1e-3)
    assert variant.is_feasible is True


def test_far_optimizer_reports_infeasible_on_zero_lot() -> None:
    variant = maximize_far_under_constraints(
        lot_area=0.0,
        max_coverage_ratio=0.5,
        max_height_meters=10.0,
        far_cap=2.0,
        floors_max=5,
    )
    assert variant.is_feasible is False
    assert variant.total_gfa == 0.0


def test_far_optimizer_respects_floors_cap() -> None:
    """With a low floor cap the optimizer should hit footprint_max × floors_max
    and never exceed the floor cap regardless of FAR headroom.
    """
    variant = maximize_far_under_constraints(
        lot_area=1000.0,
        max_coverage_ratio=1.0,   # footprint <= 1000
        max_height_meters=100.0,
        far_cap=100.0,            # FAR cap is generous
        floors_max=2,             # binding constraint
    )
    assert variant.floors == pytest.approx(2.0, abs=0.5)
    assert variant.total_gfa <= 2000.0 + 1e-6
