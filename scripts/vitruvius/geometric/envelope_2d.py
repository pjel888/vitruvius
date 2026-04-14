"""Sprint GEOM Stream GEOM.3 (2D subset) — shapely buildable envelope.

Takes a lot polygon's corners and a scalar setback distance, and
returns the 2D buildable area (lot polygon eroded by the setback).
This is the narrow-scope GEOM.3 deliverable — the full phase-15
plan also wants 3D voxel occupation maps and glTF export, both of
which need ``trimesh`` / ``libigl`` that are not installed.

The envelope is built via :meth:`shapely.geometry.Polygon.buffer`
with a negative distance, which is the canonical 2D polygon erosion.
Collapsed envelopes (buffer pushed everything to the origin) yield
an empty geometry; the wrapper normalises this to ``area = 0.0`` and
``is_buildable = False``.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


Corner = tuple[float, float]


@dataclass(frozen=True)
class BuildableEnvelope2D:
    area: float
    is_buildable: bool
    well_known_text: str  # shapely's WKT so downstream can re-parse


def compute_buildable_envelope(
    corners: Sequence[Corner],
    *,
    setback_meters: float,
) -> BuildableEnvelope2D:
    """Erode ``corners`` by ``setback_meters`` and return the buildable
    envelope.

    Raises ``ValueError`` if ``corners`` has fewer than 3 points.
    """
    if len(corners) < 3:
        raise ValueError("a lot polygon needs at least 3 corners")
    from shapely.geometry import Polygon

    lot = Polygon(corners)
    if setback_meters <= 0.0:
        envelope = lot
    else:
        envelope = lot.buffer(-float(setback_meters))

    area = float(getattr(envelope, "area", 0.0))
    is_buildable = bool(not envelope.is_empty and area > 0.0)
    wkt = envelope.wkt if not envelope.is_empty else "POLYGON EMPTY"
    return BuildableEnvelope2D(
        area=area if is_buildable else 0.0,
        is_buildable=is_buildable,
        well_known_text=wkt,
    )
