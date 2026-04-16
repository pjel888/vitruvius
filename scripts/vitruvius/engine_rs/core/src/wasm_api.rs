// Vitruvius Sprint HP Stream HP.4 — Wasm C ABI surface.
//
// These functions are the ONLY symbols the Wasm loader (see
// `scripts/vitruvius/compound/wasm_kernel.py`) calls into. They take
// plain scalar arguments so wasmtime can marshal them with no
// allocator, no heap, no memory layout negotiation.
//
// Narrow ship: `aabb_intersects` is the single entry point. It lets
// the Python ↔ Wasm roundtrip be verified end-to-end before we grow
// the surface to cover octree inserts / queries in a follow-on
// commit.

/// Pure-Rust axis-aligned bounding-box intersection test.
///
/// Both the native `rlib` path and wasm-via-wasmtime path use the
/// same function body; the `#[no_mangle] extern "C"` variant below
/// re-exports it with a C calling convention so wasm loaders can
/// find it by name.
#[inline]
#[allow(clippy::too_many_arguments)]
pub fn aabb_intersects_core(
    a_min_x: f64,
    a_min_y: f64,
    a_min_z: f64,
    a_max_x: f64,
    a_max_y: f64,
    a_max_z: f64,
    b_min_x: f64,
    b_min_y: f64,
    b_min_z: f64,
    b_max_x: f64,
    b_max_y: f64,
    b_max_z: f64,
) -> bool {
    a_min_x <= b_max_x
        && a_max_x >= b_min_x
        && a_min_y <= b_max_y
        && a_max_y >= b_min_y
        && a_min_z <= b_max_z
        && a_max_z >= b_min_z
}

/// Wasm-exported AABB intersection test.
///
/// Returns `1` if the two axis-aligned bounding boxes intersect
/// (sharing at least one boundary point is considered intersection),
/// `0` otherwise. Integer return instead of `bool` because wasm32
/// lacks a native `bool` type — all booleans round-trip as `i32`.
///
/// Called from Python via the wasmtime wrapper at
/// `scripts/vitruvius/compound/wasm_kernel.py::WasmSpatialKernel.aabb_intersects`.
#[no_mangle]
pub extern "C" fn aabb_intersects(
    a_min_x: f64,
    a_min_y: f64,
    a_min_z: f64,
    a_max_x: f64,
    a_max_y: f64,
    a_max_z: f64,
    b_min_x: f64,
    b_min_y: f64,
    b_min_z: f64,
    b_max_x: f64,
    b_max_y: f64,
    b_max_z: f64,
) -> i32 {
    if aabb_intersects_core(
        a_min_x, a_min_y, a_min_z, a_max_x, a_max_y, a_max_z, b_min_x, b_min_y, b_min_z, b_max_x,
        b_max_y, b_max_z,
    ) {
        1
    } else {
        0
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn overlapping_returns_one() {
        assert_eq!(
            aabb_intersects(0.0, 0.0, 0.0, 10.0, 10.0, 10.0, 5.0, 5.0, 5.0, 15.0, 15.0, 15.0,),
            1
        );
    }

    #[test]
    fn disjoint_returns_zero() {
        assert_eq!(
            aabb_intersects(0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 10.0, 10.0, 10.0, 20.0, 20.0, 20.0,),
            0
        );
    }

    #[test]
    fn edge_touching_returns_one() {
        // Boxes share a face plane at x=5. Inclusive intersection.
        assert_eq!(
            aabb_intersects(0.0, 0.0, 0.0, 5.0, 5.0, 5.0, 5.0, 0.0, 0.0, 10.0, 5.0, 5.0,),
            1
        );
    }
}
