"""Sprint GEOM Stream GEOM.3 (2D subset) — shapely buildable envelope tests."""
from __future__ import annotations

import pytest

pytest.importorskip("shapely")

from vitruvius.geometric.envelope_2d import (
    BuildableEnvelope2D,
    compute_buildable_envelope,
)


def test_envelope_shrinks_lot_by_setback() -> None:
    lot_corners = [(0.0, 0.0), (20.0, 0.0), (20.0, 20.0), (0.0, 20.0)]
    envelope = compute_buildable_envelope(lot_corners, setback_meters=2.0)
    assert isinstance(envelope, BuildableEnvelope2D)
    # Original lot is 20×20 = 400 m²; 2m setback shrinks to 16×16 = 256 m²
    assert envelope.area == pytest.approx(256.0, abs=1e-6)
    assert envelope.is_buildable is True


def test_envelope_on_small_lot_collapses_to_nothing() -> None:
    """A 3x3 lot with a 2m setback leaves zero area (buffer collapses)."""
    lot_corners = [(0.0, 0.0), (3.0, 0.0), (3.0, 3.0), (0.0, 3.0)]
    envelope = compute_buildable_envelope(lot_corners, setback_meters=2.0)
    assert envelope.is_buildable is False
    assert envelope.area == 0.0


def test_envelope_preserves_lot_on_zero_setback() -> None:
    lot_corners = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0)]
    envelope = compute_buildable_envelope(lot_corners, setback_meters=0.0)
    assert envelope.area == pytest.approx(100.0, abs=1e-6)
    assert envelope.is_buildable is True


def test_envelope_rejects_degenerate_polygon() -> None:
    with pytest.raises(ValueError, match="at least 3"):
        compute_buildable_envelope([(0.0, 0.0), (1.0, 1.0)], setback_meters=1.0)
