"""Vitruvius Sprint GT Streams GT.1 + GT.2 — Rust data plane wrapper.

This package is a thin Python facade over the maturin-built pyo3 crate
``vitruvius_engine_rs``. The crate lives in ``src/`` next to this
file; building it with ``maturin develop --release`` from this
directory installs the compiled extension module into the active
Python's site-packages.

Usage::

    from vitruvius.engine_rs import SpatialPoint, LinearOctree

    tree = LinearOctree(0.0, 0.0, 0.0, 100.0, 100.0, 100.0)
    tree.insert(SpatialPoint("wall-001", 5.0, 5.0, 5.0))
    hits = tree.query_sphere(0.0, 0.0, 0.0, 10.0)

Guard imports with ``pytest.importorskip('vitruvius.engine_rs')`` so
collection stays green on hosts that have not yet built the crate.

The compiled extension raises ``ImportError`` if its ABI does not
match the running CPython; wrap the import in a ``try/except
ImportError`` at call sites that must gracefully fall back to the
pure-Python spatial machinery at ``scripts/vitruvius/spatial/``.
"""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING

__all__ = [
    "SpatialPoint",
    "LinearOctree",
    "build_spatial_adjacency_edges_rs",
    "weight_by_distance_rs",
    "SPRINT_CODENAME",
    "ENGINE_RS_VERSION",
    "ENGINE_RS_AVAILABLE",
]


try:
    _ext = import_module("vitruvius_engine_rs")
except ImportError as exc:  # pragma: no cover - exercised on unbuilt hosts
    _ext = None
    _IMPORT_ERROR: ImportError | None = exc
else:
    _IMPORT_ERROR = None


if _ext is not None:
    SpatialPoint = _ext.SpatialPoint
    LinearOctree = _ext.LinearOctree
    # Sprint RUST-MIG-1 Task 4 — S1 Rust fast path.
    # Lazy getattr so older wheels built before Task 4 still import
    # cleanly (attribute is None, call sites fall back to the pure-
    # Python baseline in spatial/spatial_edge_builder.py).
    build_spatial_adjacency_edges_rs = getattr(
        _ext, "build_spatial_adjacency_edges", None
    )
    # Sprint RUST-MIG-1 Task 5 — S2 Rust fast path.
    # Same lazy-getattr pattern as Task 4: older wheels that predate
    # Task 5 leave this as None and the call site in
    # spatial/proximity_jump.py transparently falls back to the
    # pure-Python ``math.exp`` loop.
    weight_by_distance_rs = getattr(_ext, "weight_by_distance", None)
    SPRINT_CODENAME: str = getattr(_ext, "SPRINT_CODENAME", "GT.1+GT.2")
    ENGINE_RS_VERSION: str = getattr(_ext, "__version__", "0.0.0")
    ENGINE_RS_AVAILABLE = True
else:
    # Keep the names defined so static type checkers and IDEs see
    # them; attempting to use them raises a helpful ImportError
    # directing the caller at the build command.
    _ERR = (
        "vitruvius_engine_rs is not installed. Build the Rust crate "
        "with: cd scripts/vitruvius/engine_rs && "
        "python3.11 -m maturin develop --release"
    )

    class _Unbuilt:
        def __init__(self, *args: object, **kwargs: object) -> None:
            raise ImportError(_ERR) from _IMPORT_ERROR

    SpatialPoint = _Unbuilt  # type: ignore[assignment,misc]
    LinearOctree = _Unbuilt  # type: ignore[assignment,misc]
    # Sprint RUST-MIG-1 Task 4 — stays None when the crate is unbuilt
    # so the fast-path guard in spatial_edge_builder.py short-circuits
    # to the pure-Python path. The feature-flag gate is a separate
    # check, but the `is not None` check alone already protects the
    # non-breaking contract.
    build_spatial_adjacency_edges_rs = None
    # Sprint RUST-MIG-1 Task 5 — same unbuilt-host fallback for the
    # S2 fast path; proximity_jump.py short-circuits on this None.
    weight_by_distance_rs = None
    SPRINT_CODENAME = "GT.1+GT.2"
    ENGINE_RS_VERSION = "0.0.0"
    ENGINE_RS_AVAILABLE = False


if TYPE_CHECKING:  # pragma: no cover - typing only
    # Best-effort hints for IDE users. The real objects are pyo3
    # classes so these protocols are informative, not strict.
    from typing import Protocol

    class SpatialPoint(Protocol):  # type: ignore[no-redef]
        id: str
        x: float
        y: float
        z: float

        def __init__(self, id: str, x: float, y: float, z: float) -> None: ...

    class LinearOctree(Protocol):  # type: ignore[no-redef]
        max_depth: int
        bounds: tuple[float, float, float, float, float, float]

        def __init__(
            self,
            min_x: float,
            min_y: float,
            min_z: float,
            max_x: float,
            max_y: float,
            max_z: float,
            max_depth: int = 8,
        ) -> None: ...

        def insert(self, point: "SpatialPoint | tuple[str, float, float, float]") -> None: ...
        def query_aabb(
            self,
            min_x: float,
            min_y: float,
            min_z: float,
            max_x: float,
            max_y: float,
            max_z: float,
        ) -> list["SpatialPoint"]: ...
        def query_sphere(
            self, cx: float, cy: float, cz: float, radius: float
        ) -> list["SpatialPoint"]: ...
        def query_point(
            self, x: float, y: float, z: float, radius: float
        ) -> list["SpatialPoint"]: ...
        def __len__(self) -> int: ...
        def len(self) -> int: ...
        def live_count(self) -> int: ...
