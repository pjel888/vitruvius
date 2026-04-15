"""Sprint HP Stream HP.4 + Sprint Z S4 prep — Wasm spatial kernel loader.

This module loads the compiled ``vitruvius_engine_rs_core.wasm`` module
via `wasmtime` and exposes a thin Python wrapper around the exported
functions.

The Wasm kernel is produced by building the ``core`` crate of the
``scripts/vitruvius/engine_rs/`` workspace with the
``wasm32-unknown-unknown`` target::

    cd scripts/vitruvius/engine_rs/core
    cargo build --release --target wasm32-unknown-unknown

The resulting artifact lands at::

    scripts/vitruvius/engine_rs/target/wasm32-unknown-unknown/release/vitruvius_engine_rs_core.wasm

Narrow ship surface
-------------------
HP.4 exposes a single exported function — ``aabb_intersects`` — so the
Python ↔ Wasm roundtrip can be verified end-to-end before the surface
is grown to cover octree inserts / queries in a follow-on commit. The
wrapper defers all `wasmtime` imports until `WasmSpatialKernel` is
instantiated; that lets callers import this module even on hosts where
the wasmtime wheel is not installed (the class constructor will raise a
helpful ImportError).

Feature-flag gating
-------------------
The kernel is opt-in via the ``hp_wasm_kernels`` feature flag in
``config/vitruvius.yaml``. Call sites must check the flag before
instantiating ``WasmSpatialKernel``; the module itself is side-effect
free and safe to import regardless of the flag state.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover - typing only
    import wasmtime  # noqa: F401


# --------------------------------------------------------------------------- #
# Default wasm artifact path.                                                 #
# --------------------------------------------------------------------------- #
#
# Computed once at import time so callers can inspect it before
# instantiating a kernel. The path is relative to the repository root
# (3 parents up from this file: compound/ -> vitruvius/ -> scripts/ -> repo).
_REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_WASM_PATH: Path = (
    _REPO_ROOT
    / "scripts"
    / "vitruvius"
    / "engine_rs"
    / "target"
    / "wasm32-unknown-unknown"
    / "release"
    / "vitruvius_engine_rs_core.wasm"
)


def wasm_artifact_available(path: Path | None = None) -> bool:
    """Return True if the compiled wasm kernel is present on disk.

    Test helpers use this to decide whether to skip the integration
    tests — the wasm file is produced by a Rust build step that is
    optional on hosts without rustup + the wasm32 target.
    """
    candidate = path if path is not None else DEFAULT_WASM_PATH
    return candidate.is_file()


# --------------------------------------------------------------------------- #
# WasmSpatialKernel — the Python-facing handle.                               #
# --------------------------------------------------------------------------- #


class WasmSpatialKernel:
    """Thin wrapper around the ``vitruvius_engine_rs_core.wasm`` module.

    Instantiate with the path to a pre-built wasm file (defaults to
    :data:`DEFAULT_WASM_PATH`). The constructor eagerly instantiates
    the module so that any linking / wasmtime import errors surface
    immediately; the per-call overhead is just a C-ABI function
    dispatch.
    """

    def __init__(self, *, wasm_path: Path | None = None) -> None:
        # Defer wasmtime import until the class is actually used so
        # importing this module remains cheap on hosts without the
        # wheel.
        try:
            import wasmtime as _wasmtime
        except ImportError as exc:  # pragma: no cover - tested via importorskip
            raise ImportError(
                "wasmtime is required to load the Vitruvius wasm spatial "
                "kernel. Install with: "
                "/opt/homebrew/opt/python@3.11/bin/pip3.11 install wasmtime"
            ) from exc

        resolved = wasm_path if wasm_path is not None else DEFAULT_WASM_PATH
        if not resolved.is_file():
            raise FileNotFoundError(
                f"Wasm artifact not found at {resolved}. Build it with: "
                f"cd scripts/vitruvius/engine_rs/core && "
                f"cargo build --release --target wasm32-unknown-unknown"
            )

        self._wasm_path: Path = resolved
        self._engine: Any = _wasmtime.Engine()
        self._module: Any = _wasmtime.Module.from_file(self._engine, str(resolved))
        self._store: Any = _wasmtime.Store(self._engine)
        self._instance: Any = _wasmtime.Instance(self._store, self._module, [])

        exports = self._instance.exports(self._store)
        try:
            self._aabb_intersects: Any = exports["aabb_intersects"]
        except KeyError as exc:  # pragma: no cover - defensive
            available = list(exports._extern_map.keys()) if hasattr(
                exports, "_extern_map"
            ) else []
            raise RuntimeError(
                f"Wasm kernel at {resolved} does not export 'aabb_intersects'. "
                f"Available exports: {available}"
            ) from exc

    # -- Properties ------------------------------------------------------- #

    @property
    def wasm_path(self) -> Path:
        """Return the filesystem path of the loaded wasm artifact."""
        return self._wasm_path

    # -- Exported kernels ------------------------------------------------- #

    def aabb_intersects(
        self,
        a_min: tuple[float, float, float],
        a_max: tuple[float, float, float],
        b_min: tuple[float, float, float],
        b_max: tuple[float, float, float],
    ) -> bool:
        """Return True if two closed AABBs intersect.

        Inclusive semantics: boxes that share exactly one face plane
        are considered intersecting. Matches the pure-Python fallback
        at ``scripts/vitruvius/spatial/`` and the native Rust
        :func:`vitruvius_engine_rs.LinearOctree.query_aabb` path.
        """
        if len(a_min) != 3 or len(a_max) != 3 or len(b_min) != 3 or len(b_max) != 3:
            raise ValueError(
                "aabb_intersects expects 3-tuples for every corner; got "
                f"a_min={a_min}, a_max={a_max}, b_min={b_min}, b_max={b_max}"
            )

        result = self._aabb_intersects(
            self._store,
            float(a_min[0]), float(a_min[1]), float(a_min[2]),
            float(a_max[0]), float(a_max[1]), float(a_max[2]),
            float(b_min[0]), float(b_min[1]), float(b_min[2]),
            float(b_max[0]), float(b_max[1]), float(b_max[2]),
        )
        # Wasm i32 → Python int; contract is 0 or 1.
        return bool(result)


__all__ = [
    "DEFAULT_WASM_PATH",
    "WasmSpatialKernel",
    "wasm_artifact_available",
]
