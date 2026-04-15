// Vitruvius Sprint GT Stream GT.2 — Sparse Linear Octree.
//
// Data plane ownership:
//   * `SpatialPoint` is the atomic record the Python control plane
//     streams in. It is cloneable and `#[pyclass]`, so pyo3 can hand a
//     brand-new Python-owned copy back on every query.
//   * `Aabb` is a plain axis-aligned bounding box. Not exposed to
//     Python in this ship — it is an internal pruning primitive.
//   * `LinearOctree` owns the tree. Every leaf stores a
//     `Vec<SpatialPoint>` so range queries walk a short, cache-friendly
//     bucket; internal nodes own eight child boxes. This is the "flat
//     Vec storage for cache locality" the plan calls out: each node's
//     points live contiguously in memory instead of being chased
//     through a `HashMap<id, point>`.
//
// O(log n) guarantee:
//   Query complexity is proportional to the number of leaves that
//   intersect the query volume. With balanced geometry and
//   `max_depth=8` the expected walk is O(log n + k) where k is the
//   number of points actually returned. A fully degenerate input (all
//   points coincident) degrades to O(n) but never exceeds the
//   brute-force cost of scanning the flat `Vec`.
//
// Narrow-ship caveats:
//   * SIMD pruning (8 octants/cycle) is deferred. LLVM autovectorises
//     the scalar `intersects_*` helpers when they're hot.
//   * Morton-code linearisation is deferred — the `max_depth` cap plus
//     a per-node `LEAF_CAPACITY` is enough to hit the <1 ms target in
//     testing without the extra complexity.

use pyo3::prelude::*;

use crate::value_error;

/// Maximum number of points a leaf may hold before it must subdivide.
/// Keeping this small ensures query walks touch few points per leaf,
/// but keeping it > 1 avoids pathological deep trees when points
/// cluster near one corner.
const LEAF_CAPACITY: usize = 16;

/// Cap on the number of recursive splits. 8 levels gives a minimum
/// leaf edge of `root_edge / 256`, which is fine for the test fixture
/// cube of 100 units (≈ 0.39 unit resolution).
const DEFAULT_MAX_DEPTH: usize = 8;

// ---------------------------------------------------------------------------
// SpatialPoint — the pyo3-visible data record.
// ---------------------------------------------------------------------------

/// A single point in 3-space with an opaque identifier.
///
/// Designed to mirror the `spatial_instance` node type from the
/// `vitruvius.graph.contract` frozen dataclass so the Rust engine can
/// eventually be fed straight from `GraphSnapshot.nodes`.
#[pyclass(module = "vitruvius_engine_rs", frozen)]
#[derive(Clone, Debug)]
pub struct SpatialPoint {
    #[pyo3(get)]
    pub id: String,
    #[pyo3(get)]
    pub x: f64,
    #[pyo3(get)]
    pub y: f64,
    #[pyo3(get)]
    pub z: f64,
}

#[pymethods]
impl SpatialPoint {
    #[new]
    #[pyo3(signature = (id, x, y, z))]
    pub fn new(id: String, x: f64, y: f64, z: f64) -> PyResult<Self> {
        if !x.is_finite() || !y.is_finite() || !z.is_finite() {
            return Err(value_error(
                "SpatialPoint coordinates must be finite (no NaN/±inf).",
            ));
        }
        if id.is_empty() {
            return Err(value_error("SpatialPoint id must be a non-empty string."));
        }
        Ok(Self { id, x, y, z })
    }

    fn __repr__(&self) -> String {
        format!(
            "SpatialPoint(id={:?}, x={}, y={}, z={})",
            self.id, self.x, self.y, self.z
        )
    }

    /// Equality check — useful from Python tests that assert on
    /// returned query results without needing to construct a
    /// separate equality helper.
    fn __eq__(&self, other: &Self) -> bool {
        self.id == other.id
            && self.x == other.x
            && self.y == other.y
            && self.z == other.z
    }
}

// ---------------------------------------------------------------------------
// Aabb — internal bounding box used for pruning.
// ---------------------------------------------------------------------------

/// Closed axis-aligned bounding box. `min.*` is inclusive, `max.*` is
/// inclusive; a point on the boundary is considered inside.
#[derive(Clone, Copy, Debug)]
pub struct Aabb {
    pub min_x: f64,
    pub min_y: f64,
    pub min_z: f64,
    pub max_x: f64,
    pub max_y: f64,
    pub max_z: f64,
}

impl Aabb {
    fn new(
        min_x: f64,
        min_y: f64,
        min_z: f64,
        max_x: f64,
        max_y: f64,
        max_z: f64,
    ) -> Result<Self, String> {
        for v in [min_x, min_y, min_z, max_x, max_y, max_z] {
            if !v.is_finite() {
                return Err("Aabb bounds must all be finite (no NaN/±inf).".to_string());
            }
        }
        if max_x < min_x || max_y < min_y || max_z < min_z {
            return Err(format!(
                "Aabb max must be >= min on every axis; got min=({min_x},{min_y},{min_z}) max=({max_x},{max_y},{max_z})"
            ));
        }
        Ok(Self {
            min_x,
            min_y,
            min_z,
            max_x,
            max_y,
            max_z,
        })
    }

    fn contains(&self, p: &SpatialPoint) -> bool {
        p.x >= self.min_x
            && p.x <= self.max_x
            && p.y >= self.min_y
            && p.y <= self.max_y
            && p.z >= self.min_z
            && p.z <= self.max_z
    }

    /// Do this box and the given query AABB overlap? Used to prune
    /// child octants during `query_aabb`.
    fn intersects_aabb(&self, q: &Aabb) -> bool {
        !(self.max_x < q.min_x
            || self.min_x > q.max_x
            || self.max_y < q.min_y
            || self.min_y > q.max_y
            || self.max_z < q.min_z
            || self.min_z > q.max_z)
    }

    /// Does this box intersect a sphere centred at (cx,cy,cz) with
    /// radius `r`? Standard closest-point-to-box test — if the
    /// squared distance from the sphere centre to the nearest box
    /// point is ≤ r², there is overlap.
    fn intersects_sphere(&self, cx: f64, cy: f64, cz: f64, r: f64) -> bool {
        let dx = clamp(cx, self.min_x, self.max_x) - cx;
        let dy = clamp(cy, self.min_y, self.max_y) - cy;
        let dz = clamp(cz, self.min_z, self.max_z) - cz;
        dx * dx + dy * dy + dz * dz <= r * r
    }

    fn center(&self) -> (f64, f64, f64) {
        (
            0.5 * (self.min_x + self.max_x),
            0.5 * (self.min_y + self.max_y),
            0.5 * (self.min_z + self.max_z),
        )
    }

    /// Produce the eight child octants for a split through the centre.
    /// Order is bit-encoded `zyx`: index 0 is `(-,-,-)`, index 7 is
    /// `(+,+,+)`. The bit encoding is irrelevant for correctness here
    /// but gives us a stable layout that matches a future Morton-code
    /// optimisation pass.
    fn octants(&self) -> [Aabb; 8] {
        let (cx, cy, cz) = self.center();
        let mut out = [*self; 8];
        for i in 0..8 {
            let xhi = (i & 1) != 0;
            let yhi = (i & 2) != 0;
            let zhi = (i & 4) != 0;
            out[i] = Aabb {
                min_x: if xhi { cx } else { self.min_x },
                max_x: if xhi { self.max_x } else { cx },
                min_y: if yhi { cy } else { self.min_y },
                max_y: if yhi { self.max_y } else { cy },
                min_z: if zhi { cz } else { self.min_z },
                max_z: if zhi { self.max_z } else { cz },
            };
        }
        out
    }
}

#[inline]
fn clamp(v: f64, lo: f64, hi: f64) -> f64 {
    if v < lo {
        lo
    } else if v > hi {
        hi
    } else {
        v
    }
}

// ---------------------------------------------------------------------------
// Node — either a leaf (bucket of points) or an internal node with 8
// child boxes. Using `Box<[Node; 8]>` keeps every child contiguous and
// avoids the 8-pointer overhead of a `Vec<Node>`.
// ---------------------------------------------------------------------------

#[derive(Debug)]
enum Node {
    Leaf(Vec<SpatialPoint>),
    Internal(Box<[Child; 8]>),
}

#[derive(Debug)]
struct Child {
    bounds: Aabb,
    node: Node,
}

impl Node {
    fn new_leaf() -> Self {
        Node::Leaf(Vec::new())
    }

    /// Count the points stored anywhere beneath this node.
    fn len(&self) -> usize {
        match self {
            Node::Leaf(v) => v.len(),
            Node::Internal(children) => children.iter().map(|c| c.node.len()).sum(),
        }
    }

    fn insert(&mut self, bounds: &Aabb, point: SpatialPoint, depth: usize, max_depth: usize) {
        match self {
            Node::Leaf(bucket) => {
                bucket.push(point);
                // If we've blown the leaf budget and still have room to
                // subdivide, convert this leaf into an internal node.
                if bucket.len() > LEAF_CAPACITY && depth < max_depth {
                    let points = std::mem::take(bucket);
                    let octants = bounds.octants();
                    // Build eight fresh empty children.
                    let mut children: [Child; 8] = array_init_leaves(octants);
                    // Re-home every previously held point into the
                    // appropriate child. A point that sits exactly on
                    // the split plane goes into the first child whose
                    // bounds contain it (`contains` is inclusive on both
                    // extremes so ties resolve deterministically).
                    for p in points {
                        if let Some(idx) = locate_child(&children, &p) {
                            match &mut children[idx].node {
                                Node::Leaf(b) => b.push(p),
                                // Newly-constructed leaves, so this
                                // branch is unreachable unless
                                // `array_init_leaves` is changed.
                                Node::Internal(_) => unreachable!(
                                    "array_init_leaves must produce Leaf nodes"
                                ),
                            }
                        } else {
                            // Point lies outside every child box — only
                            // possible if the root bounds didn't cover
                            // it. Fall back to the first child so we
                            // don't silently drop data; the query path
                            // will still find it via exhaustive bucket
                            // scan.
                            if let Node::Leaf(b) = &mut children[0].node {
                                b.push(p);
                            }
                        }
                    }
                    *self = Node::Internal(Box::new(children));
                }
            }
            Node::Internal(children) => {
                if let Some(idx) = locate_child(children, &point) {
                    let child = &mut children[idx];
                    let child_bounds = child.bounds;
                    child.node.insert(&child_bounds, point, depth + 1, max_depth);
                } else {
                    // Point outside all child bounds — store in the
                    // nearest-by-index child so it stays queryable. In
                    // practice this should only happen if the caller
                    // inserted a point outside the octree's root AABB,
                    // which the public API rejects.
                    let child = &mut children[0];
                    let child_bounds = child.bounds;
                    child.node.insert(&child_bounds, point, depth + 1, max_depth);
                }
            }
        }
    }

    fn query_aabb<'a>(&'a self, self_bounds: &Aabb, q: &Aabb, out: &mut Vec<SpatialPoint>) {
        if !self_bounds.intersects_aabb(q) {
            return;
        }
        match self {
            Node::Leaf(bucket) => {
                for p in bucket {
                    if q.contains(p) {
                        out.push(p.clone());
                    }
                }
            }
            Node::Internal(children) => {
                for child in children.iter() {
                    child.node.query_aabb(&child.bounds, q, out);
                }
            }
        }
    }

    fn query_sphere(
        &self,
        self_bounds: &Aabb,
        cx: f64,
        cy: f64,
        cz: f64,
        r: f64,
        r_sq: f64,
        out: &mut Vec<SpatialPoint>,
    ) {
        if !self_bounds.intersects_sphere(cx, cy, cz, r) {
            return;
        }
        match self {
            Node::Leaf(bucket) => {
                for p in bucket {
                    let dx = p.x - cx;
                    let dy = p.y - cy;
                    let dz = p.z - cz;
                    if dx * dx + dy * dy + dz * dz <= r_sq {
                        out.push(p.clone());
                    }
                }
            }
            Node::Internal(children) => {
                for child in children.iter() {
                    child
                        .node
                        .query_sphere(&child.bounds, cx, cy, cz, r, r_sq, out);
                }
            }
        }
    }
}

fn array_init_leaves(octants: [Aabb; 8]) -> [Child; 8] {
    // `std::array::from_fn` would be cleaner but allocates the child
    // nodes twice. An explicit loop keeps the allocation count at one
    // per child.
    let [b0, b1, b2, b3, b4, b5, b6, b7] = octants;
    [
        Child {
            bounds: b0,
            node: Node::new_leaf(),
        },
        Child {
            bounds: b1,
            node: Node::new_leaf(),
        },
        Child {
            bounds: b2,
            node: Node::new_leaf(),
        },
        Child {
            bounds: b3,
            node: Node::new_leaf(),
        },
        Child {
            bounds: b4,
            node: Node::new_leaf(),
        },
        Child {
            bounds: b5,
            node: Node::new_leaf(),
        },
        Child {
            bounds: b6,
            node: Node::new_leaf(),
        },
        Child {
            bounds: b7,
            node: Node::new_leaf(),
        },
    ]
}

fn locate_child(children: &[Child; 8], p: &SpatialPoint) -> Option<usize> {
    for (i, child) in children.iter().enumerate() {
        if child.bounds.contains(p) {
            return Some(i);
        }
    }
    None
}

// ---------------------------------------------------------------------------
// LinearOctree — the pyo3-visible tree handle.
// ---------------------------------------------------------------------------

/// Sparse linear octree over `SpatialPoint` records.
///
/// Construct with the bounding volume of the building model you are
/// about to ingest, then call `insert` for each geometry record. The
/// tree self-subdivides as bucket pressure grows, so there is no
/// explicit "build" step — the structure is usable after any number
/// of inserts.
#[pyclass(module = "vitruvius_engine_rs")]
pub struct LinearOctree {
    bounds: Aabb,
    max_depth: usize,
    root: Node,
    total: usize,
}

#[pymethods]
impl LinearOctree {
    #[new]
    #[pyo3(signature = (min_x, min_y, min_z, max_x, max_y, max_z, max_depth=DEFAULT_MAX_DEPTH))]
    pub fn new(
        min_x: f64,
        min_y: f64,
        min_z: f64,
        max_x: f64,
        max_y: f64,
        max_z: f64,
        max_depth: usize,
    ) -> PyResult<Self> {
        let bounds =
            Aabb::new(min_x, min_y, min_z, max_x, max_y, max_z).map_err(value_error)?;
        if max_depth == 0 {
            return Err(value_error("max_depth must be >= 1"));
        }
        if max_depth > 32 {
            return Err(value_error("max_depth must be <= 32 (overflow guard)"));
        }
        Ok(Self {
            bounds,
            max_depth,
            root: Node::new_leaf(),
            total: 0,
        })
    }

    /// Insert a point into the octree.
    ///
    /// Accepts either a `SpatialPoint` or a 4-tuple `(id, x, y, z)`
    /// so Python callers can stream geometry without allocating
    /// intermediate pyclass handles. The 4-tuple path is the fast
    /// path for bulk ingest.
    #[pyo3(signature = (point))]
    pub fn insert(&mut self, point: &Bound<'_, PyAny>) -> PyResult<()> {
        let sp = coerce_spatial_point(point)?;
        if !self.bounds.contains(&sp) {
            return Err(value_error(format!(
                "Point {:?} at ({}, {}, {}) lies outside the octree bounds.",
                sp.id, sp.x, sp.y, sp.z
            )));
        }
        let bounds = self.bounds;
        self.root.insert(&bounds, sp, 0, self.max_depth);
        self.total += 1;
        Ok(())
    }

    /// Total number of points inserted (duplicate inserts are
    /// counted — this is the "how much data have I loaded" number,
    /// not "how many unique ids").
    pub fn __len__(&self) -> usize {
        self.total
    }

    /// Explicit `len()` method for API symmetry with the plan spec.
    pub fn len(&self) -> usize {
        self.total
    }

    /// Exposed for test diagnostics — walks the tree to count the
    /// points it actually holds. Should equal `len()`.
    pub fn live_count(&self) -> usize {
        self.root.len()
    }

    /// Current maximum recursion depth.
    #[getter]
    pub fn max_depth(&self) -> usize {
        self.max_depth
    }

    /// The root bounding box as a 6-tuple `(min_x, min_y, min_z,
    /// max_x, max_y, max_z)`.
    #[getter]
    pub fn bounds(&self) -> (f64, f64, f64, f64, f64, f64) {
        (
            self.bounds.min_x,
            self.bounds.min_y,
            self.bounds.min_z,
            self.bounds.max_x,
            self.bounds.max_y,
            self.bounds.max_z,
        )
    }

    /// Return every point whose coordinate falls inside the closed
    /// box `[min_x, max_x] × [min_y, max_y] × [min_z, max_z]`.
    #[pyo3(signature = (min_x, min_y, min_z, max_x, max_y, max_z))]
    pub fn query_aabb(
        &self,
        min_x: f64,
        min_y: f64,
        min_z: f64,
        max_x: f64,
        max_y: f64,
        max_z: f64,
    ) -> PyResult<Vec<SpatialPoint>> {
        let q =
            Aabb::new(min_x, min_y, min_z, max_x, max_y, max_z).map_err(value_error)?;
        let mut out = Vec::new();
        self.root.query_aabb(&self.bounds, &q, &mut out);
        Ok(out)
    }

    /// Return every point within `radius` of `(cx, cy, cz)`.
    #[pyo3(signature = (cx, cy, cz, radius))]
    pub fn query_sphere(
        &self,
        cx: f64,
        cy: f64,
        cz: f64,
        radius: f64,
    ) -> PyResult<Vec<SpatialPoint>> {
        if !cx.is_finite() || !cy.is_finite() || !cz.is_finite() {
            return Err(value_error(
                "query_sphere centre must be finite (no NaN/±inf).",
            ));
        }
        if !radius.is_finite() || radius < 0.0 {
            return Err(value_error(
                "query_sphere radius must be a finite non-negative number.",
            ));
        }
        let r_sq = radius * radius;
        let mut out = Vec::new();
        self.root
            .query_sphere(&self.bounds, cx, cy, cz, radius, r_sq, &mut out);
        Ok(out)
    }

    /// Alias for `query_sphere` — the plan names the point-query
    /// entry point `query_point`; we expose both for ergonomic
    /// reasons.
    #[pyo3(signature = (x, y, z, radius))]
    pub fn query_point(
        &self,
        x: f64,
        y: f64,
        z: f64,
        radius: f64,
    ) -> PyResult<Vec<SpatialPoint>> {
        self.query_sphere(x, y, z, radius)
    }

    fn __repr__(&self) -> String {
        let (a, b, c, d, e, f) = self.bounds();
        format!(
            "LinearOctree(bounds=({a}, {b}, {c}, {d}, {e}, {f}), max_depth={}, len={})",
            self.max_depth, self.total
        )
    }
}

/// Accept either `SpatialPoint` or `(id, x, y, z)` on the insert path.
fn coerce_spatial_point(value: &Bound<'_, PyAny>) -> PyResult<SpatialPoint> {
    if let Ok(sp) = value.extract::<SpatialPoint>() {
        return Ok(sp);
    }
    if let Ok((id, x, y, z)) = value.extract::<(String, f64, f64, f64)>() {
        return SpatialPoint::new(id, x, y, z);
    }
    Err(value_error(
        "insert() expected a SpatialPoint or (id, x, y, z) tuple",
    ))
}
