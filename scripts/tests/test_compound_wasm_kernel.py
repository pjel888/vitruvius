"""Sprint HP Stream HP.4 + Sprint Z S4 prep — wasm spatial kernel tests.

These tests exercise the Python ↔ Wasm roundtrip through
``scripts/vitruvius/compound/wasm_kernel.py``. They are double-guarded:

1. ``pytest.importorskip('wasmtime')`` — skip if the wasmtime Python
   wheel is not installed on this host.
2. ``pytest.mark.skipif(not wasm_artifact_available())`` — skip if the
   compiled ``.wasm`` file is missing (the Rust build step is optional
   on hosts without rustup + the wasm32 target).

Together, the two guards let CI stay green on any host while still
exercising the full stack whenever the prerequisites are present.
"""

from __future__ import annotations

import pytest

# --------------------------------------------------------------------------- #
# Guard 1: wasmtime Python wheel must be importable.                          #
# --------------------------------------------------------------------------- #
wasmtime = pytest.importorskip(
    "wasmtime",
    reason=(
        "wasmtime Python bindings are not installed. Install with "
        "`/opt/homebrew/opt/python@3.11/bin/pip3.11 install wasmtime` "
        "to enable this suite."
    ),
)

from vitruvius.compound.wasm_kernel import (  # noqa: E402
    DEFAULT_WASM_PATH,
    WasmSpatialKernel,
    wasm_artifact_available,
)

# --------------------------------------------------------------------------- #
# Guard 2: compiled .wasm artifact must exist on disk.                        #
# --------------------------------------------------------------------------- #
pytestmark = pytest.mark.skipif(
    not wasm_artifact_available(),
    reason=(
        f"Wasm artifact missing at {DEFAULT_WASM_PATH}. Build it with "
        "`cd scripts/vitruvius/engine_rs/core && cargo build --release "
        "--target wasm32-unknown-unknown` to enable this suite."
    ),
)


# --------------------------------------------------------------------------- #
# Module-loading contract                                                     #
# --------------------------------------------------------------------------- #
def test_kernel_loads_wasm_module() -> None:
    """Constructing WasmSpatialKernel must succeed without raising.

    Verifies the end-to-end pipeline: wasmtime import, module parse,
    store allocation, instance export lookup for ``aabb_intersects``.
    """
    kernel = WasmSpatialKernel()
    assert kernel is not None
    assert kernel.wasm_path == DEFAULT_WASM_PATH
    # The exported function handle must be callable via the
    # public method — tested explicitly in the cases below.


def test_kernel_exposes_wasm_path_property() -> None:
    """The ``wasm_path`` property should return the resolved Path."""
    kernel = WasmSpatialKernel()
    assert kernel.wasm_path.is_file()
    assert kernel.wasm_path.suffix == ".wasm"
    assert kernel.wasm_path.name == "vitruvius_engine_rs_core.wasm"


# --------------------------------------------------------------------------- #
# aabb_intersects contract                                                    #
# --------------------------------------------------------------------------- #
def test_aabb_intersects_overlapping_boxes_returns_true() -> None:
    """Two boxes that share volume must report as intersecting."""
    kernel = WasmSpatialKernel()
    result = kernel.aabb_intersects(
        a_min=(0.0, 0.0, 0.0),
        a_max=(10.0, 10.0, 10.0),
        b_min=(5.0, 5.0, 5.0),
        b_max=(15.0, 15.0, 15.0),
    )
    assert result is True
    # Python return type contract — not an int leaked from wasm.
    assert isinstance(result, bool)


def test_aabb_intersects_disjoint_boxes_returns_false() -> None:
    """Two boxes with no shared volume must report as disjoint."""
    kernel = WasmSpatialKernel()
    result = kernel.aabb_intersects(
        a_min=(0.0, 0.0, 0.0),
        a_max=(1.0, 1.0, 1.0),
        b_min=(10.0, 10.0, 10.0),
        b_max=(20.0, 20.0, 20.0),
    )
    assert result is False
    assert isinstance(result, bool)


def test_aabb_intersects_edge_touching_returns_true() -> None:
    """Boxes sharing exactly one face plane intersect (inclusive rule)."""
    kernel = WasmSpatialKernel()
    # Share the x = 5 plane; no shared volume, but the closed-interval
    # contract treats face-touching boxes as intersecting.
    result = kernel.aabb_intersects(
        a_min=(0.0, 0.0, 0.0),
        a_max=(5.0, 5.0, 5.0),
        b_min=(5.0, 0.0, 0.0),
        b_max=(10.0, 5.0, 5.0),
    )
    assert result is True


def test_aabb_intersects_box_fully_contained() -> None:
    """A box fully inside another must intersect (sanity check)."""
    kernel = WasmSpatialKernel()
    result = kernel.aabb_intersects(
        a_min=(0.0, 0.0, 0.0),
        a_max=(100.0, 100.0, 100.0),
        b_min=(10.0, 20.0, 30.0),
        b_max=(40.0, 50.0, 60.0),
    )
    assert result is True


def test_aabb_intersects_rejects_wrong_length_tuples() -> None:
    """The Python wrapper must reject non-3-tuples at call time."""
    kernel = WasmSpatialKernel()
    with pytest.raises(ValueError, match="3-tuples"):
        kernel.aabb_intersects(
            a_min=(0.0, 0.0),  # type: ignore[arg-type]
            a_max=(1.0, 1.0, 1.0),
            b_min=(0.0, 0.0, 0.0),
            b_max=(2.0, 2.0, 2.0),
        )
