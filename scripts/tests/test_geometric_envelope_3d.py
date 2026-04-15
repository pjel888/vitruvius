"""Sprint GEOM Stream GEOM.3 — 3D buildable envelope tests (trimesh)."""
from __future__ import annotations

import pytest

pytest.importorskip("trimesh")
pytest.importorskip("shapely")

from vitruvius.geometric.envelope_3d import (
    BuildableEnvelope3D,
    compute_3d_envelope,
    compute_iou,
)


def test_envelope_3d_from_lot_and_height() -> None:
    lot = [(0.0, 0.0), (20.0, 0.0), (20.0, 20.0), (0.0, 20.0)]
    envelope = compute_3d_envelope(
        lot_corners=lot,
        setback_meters=2.0,
        max_height_meters=15.0,
    )
    assert isinstance(envelope, BuildableEnvelope3D)
    # 16*16*15 = 3840 m^3 after setback
    assert envelope.volume == pytest.approx(3840.0, rel=1e-3)
    assert envelope.is_buildable is True


def test_envelope_3d_zero_height_collapses() -> None:
    lot = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0)]
    envelope = compute_3d_envelope(
        lot_corners=lot,
        setback_meters=0.0,
        max_height_meters=0.0,
    )
    assert envelope.volume == 0.0
    assert envelope.is_buildable is False


def test_envelope_3d_small_lot_collapses_on_large_setback() -> None:
    lot = [(0.0, 0.0), (3.0, 0.0), (3.0, 3.0), (0.0, 3.0)]
    envelope = compute_3d_envelope(
        lot_corners=lot,
        setback_meters=2.0,
        max_height_meters=10.0,
    )
    assert envelope.volume == 0.0
    assert envelope.is_buildable is False


# ---------------------------------------------------------------------------
# Stream GEOM.4 — IoU audit
# ---------------------------------------------------------------------------
def test_iou_identical_envelopes_is_one() -> None:
    lot = [(0.0, 0.0), (20.0, 0.0), (20.0, 20.0), (0.0, 20.0)]
    envelope = compute_3d_envelope(
        lot_corners=lot, setback_meters=2.0, max_height_meters=15.0,
    )
    score = compute_iou(envelope, envelope)
    assert score == pytest.approx(1.0, abs=1e-6)


def test_iou_smaller_subset_is_fraction() -> None:
    big = compute_3d_envelope(
        lot_corners=[(0.0, 0.0), (20.0, 0.0), (20.0, 20.0), (0.0, 20.0)],
        setback_meters=0.0,
        max_height_meters=10.0,  # volume 4000
    )
    small = compute_3d_envelope(
        lot_corners=[(0.0, 0.0), (20.0, 0.0), (20.0, 20.0), (0.0, 20.0)],
        setback_meters=0.0,
        max_height_meters=5.0,  # volume 2000 — fully contained within big
    )
    # IoU = intersection / union = 2000 / 4000 = 0.5
    score = compute_iou(small, big)
    assert score == pytest.approx(0.5, abs=1e-3)
