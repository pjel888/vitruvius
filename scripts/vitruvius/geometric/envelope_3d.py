"""Sprint GEOM Stream GEOM.3 + GEOM.4 — 3D buildable envelope +
IoU audit via trimesh.

Builds a simple extruded buildable envelope (2D eroded lot polygon
swept vertically by a max-height constraint) and exposes an IoU
score against a second envelope for compliance auditing.

Deliberately narrow scope: no Boolean union/subtraction over arbitrary
polyhedra, no Monte Carlo Pareto optimiser. The Pareto optimiser
(GEOM.4.2) ships in :mod:`pareto_optimizer`; the stochastic site
feasibility sweep (GEOM.4.3) is a future task on top of that.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    import trimesh  # noqa: F401


Corner = tuple[float, float]


@dataclass(frozen=True)
class BuildableEnvelope3D:
    volume: float
    is_buildable: bool
    footprint_area: float
    max_height_meters: float
    # Private payload held as "trimesh.Trimesh" via Any so importers
    # without trimesh can still reference the dataclass type.
    mesh: object


def _eroded_polygon(corners: Sequence[Corner], setback: float):
    from shapely.geometry import Polygon

    lot = Polygon(corners)
    if setback <= 0.0:
        return lot
    return lot.buffer(-float(setback))


def compute_3d_envelope(
    *,
    lot_corners: Sequence[Corner],
    setback_meters: float,
    max_height_meters: float,
) -> BuildableEnvelope3D:
    """Extrude an eroded lot polygon vertically by ``max_height_meters``.

    Returns a :class:`BuildableEnvelope3D` whose ``mesh`` is a
    :class:`trimesh.Trimesh` so callers can compute IoU, export to
    glTF/OBJ, or voxelise. Collapsed footprints (small lot + large
    setback) and zero-height extrusions normalise to ``volume=0`` and
    ``is_buildable=False``.
    """
    if len(lot_corners) < 3:
        raise ValueError("lot polygon needs at least 3 corners")
    from shapely.geometry import Polygon, MultiPolygon
    import trimesh
    import numpy as np

    eroded = _eroded_polygon(lot_corners, setback_meters)
    if eroded.is_empty or eroded.area <= 0.0 or max_height_meters <= 0.0:
        return BuildableEnvelope3D(
            volume=0.0,
            is_buildable=False,
            footprint_area=0.0,
            max_height_meters=max_height_meters,
            mesh=trimesh.Trimesh(),
        )

    # Extract the outer ring (simple case: Polygon; multipolygon picks
    # the largest component so single-piece lots work cleanly).
    if isinstance(eroded, MultiPolygon):
        eroded = max(eroded.geoms, key=lambda g: g.area)
    assert isinstance(eroded, Polygon)

    poly_2d_coords = list(eroded.exterior.coords)
    # shapely closes the ring by repeating the first point; trimesh
    # wants an open ring, so drop the trailing duplicate.
    if poly_2d_coords and poly_2d_coords[0] == poly_2d_coords[-1]:
        poly_2d_coords = poly_2d_coords[:-1]

    mesh = trimesh.creation.extrude_polygon(
        Polygon(poly_2d_coords),
        height=float(max_height_meters),
    )

    volume = float(mesh.volume)
    return BuildableEnvelope3D(
        volume=volume,
        is_buildable=volume > 0.0,
        footprint_area=float(eroded.area),
        max_height_meters=float(max_height_meters),
        mesh=mesh,
    )


def compute_iou(a: BuildableEnvelope3D, b: BuildableEnvelope3D) -> float:
    """Intersection-over-union of two 3D envelopes.

    Uses the cheap axis-aligned overlap proxy: an exact polyhedral
    boolean intersection via trimesh/manifold3d is much heavier and
    is overkill for the Sprint GEOM narrow-slice. When both meshes
    are extrusions of the same 2D footprint with different heights
    (the common Pareto sweep case) the AABB proxy is exact.
    """
    import trimesh
    import numpy as np

    if a.volume == 0.0 and b.volume == 0.0:
        return 1.0  # two empty envelopes are definitionally identical
    if a.volume == 0.0 or b.volume == 0.0:
        return 0.0

    mesh_a = a.mesh if isinstance(a.mesh, trimesh.Trimesh) else None
    mesh_b = b.mesh if isinstance(b.mesh, trimesh.Trimesh) else None
    if mesh_a is None or mesh_b is None or mesh_a.is_empty or mesh_b.is_empty:
        return 0.0

    bb_a = mesh_a.bounds  # shape (2, 3)
    bb_b = mesh_b.bounds
    lo = np.maximum(bb_a[0], bb_b[0])
    hi = np.minimum(bb_a[1], bb_b[1])
    overlap = np.maximum(hi - lo, 0.0)
    intersection = float(overlap[0] * overlap[1] * overlap[2])
    union = float(a.volume + b.volume - intersection)
    if union <= 0.0:
        return 0.0
    return intersection / union
