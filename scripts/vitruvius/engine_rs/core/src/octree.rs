// Vitruvius Sprint GT Stream GT.2 — Sparse Linear Octree (pure core).
//
// This is the pyo3-free version of the original
// `scripts/vitruvius/engine_rs/src/octree.rs` that shipped in Sprint
// GT. The logic is byte-identical; the only difference is that the
// pyo3 `#[pyclass]` / `#[pymethods]` annotations have been lifted up
// into the `pyo3_shim` crate. That keeps this crate compilable on
// `wasm32-unknown-unknown` where libpython is unavailable.
//
// Errors are returned as `String` (via `AabbError` / `LinearOctreeError`
// type aliases) instead of `pyo3::PyErr`. The shim crate maps those
// to `PyValueError::new_err(...)` one call away, so Python-facing
// behaviour is unchanged.
//
// Original docs preserved verbatim below — see the pre-split commit
// (b782ea3) for blame history.
//
// Data plane ownership:
//   * `SpatialPoint` is the atomic record the Python control plane
//     streams in. It is `Clone + Debug` so pyo3 can wrap it in a
//     newtype and hand a brand-new Python-owned copy back on every
//     query.
//   * `Aabb` is a plain axis-aligned bounding box. Internal pruning
//     primitive; the shim crate does not expose it.
//   * `LinearOctree` owns the tree. Every leaf stores a
//     `Vec<SpatialPoint>` so range queries walk a short, cache-friendly
//     bucket; internal nodes own eight child boxes.
//
// O(log n) guarantee (unchanged from Sprint GT):
//   Query complexity is proportional to the number of leaves that
//   intersect the query volume. With balanced geometry and
//   `max_depth=8` the expected walk is O(log n + k) where k is the
//   number of points actually returned.

/// Maximum number of points a leaf may hold before it must subdivide.
/// Keeping this small ensures query walks touch few points per leaf,
/// but keeping it > 1 avoids pathological deep trees when points
/// cluster near one corner.
const LEAF_CAPACITY: usize = 16;

/// Cap on the number of recursive splits. 8 levels gives a minimum
/// leaf edge of `root_edge / 256`, which is fine for the test fixture
/// cube of 100 units (≈ 0.39 unit resolution).
pub const DEFAULT_MAX_DEPTH: usize = 8;

/// Plain-string error surface. The pyo3 shim maps this to
/// `PyValueError::new_err(...)`; other shims (wasm, CLI) stringify
/// it directly.
pub type AabbError = String;
pub type LinearOctreeError = String;

// ---------------------------------------------------------------------------
// SpatialPoint — pure Rust. The pyo3 shim re-exports a newtype wrapper.
// ---------------------------------------------------------------------------

/// A single point in 3-space with an opaque identifier.
///
/// Mirrors the `spatial_instance` node type from
/// `vitruvius.graph.contract` so the Rust engine can be fed straight
/// from `GraphSnapshot.nodes`.
#[derive(Clone, Debug, PartialEq)]
pub struct SpatialPoint {
    pub id: String,
    pub x: f64,
    pub y: f64,
    pub z: f64,
}

impl SpatialPoint {
    pub fn new(id: String, x: f64, y: f64, z: f64) -> Result<Self, String> {
        if !x.is_finite() || !y.is_finite() || !z.is_finite() {
            return Err("SpatialPoint coordinates must be finite (no NaN/±inf).".to_string());
        }
        if id.is_empty() {
            return Err("SpatialPoint id must be a non-empty string.".to_string());
        }
        Ok(Self { id, x, y, z })
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
    pub fn new(
        min_x: f64,
        min_y: f64,
        min_z: f64,
        max_x: f64,
        max_y: f64,
        max_z: f64,
    ) -> Result<Self, AabbError> {
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

    pub fn contains(&self, p: &SpatialPoint) -> bool {
        p.x >= self.min_x
            && p.x <= self.max_x
            && p.y >= self.min_y
            && p.y <= self.max_y
            && p.z >= self.min_z
            && p.z <= self.max_z
    }

    /// Do this box and the given query AABB overlap?
    pub fn intersects_aabb(&self, q: &Aabb) -> bool {
        !(self.max_x < q.min_x
            || self.min_x > q.max_x
            || self.max_y < q.min_y
            || self.min_y > q.max_y
            || self.max_z < q.min_z
            || self.min_z > q.max_z)
    }

    /// Does this box intersect a sphere centred at (cx,cy,cz) with
    /// radius `r`?
    pub fn intersects_sphere(&self, cx: f64, cy: f64, cz: f64, r: f64) -> bool {
        let dx = clamp(cx, self.min_x, self.max_x) - cx;
        let dy = clamp(cy, self.min_y, self.max_y) - cy;
        let dz = clamp(cz, self.min_z, self.max_z) - cz;
        dx * dx + dy * dy + dz * dz <= r * r
    }

    pub fn center(&self) -> (f64, f64, f64) {
        (
            0.5 * (self.min_x + self.max_x),
            0.5 * (self.min_y + self.max_y),
            0.5 * (self.min_z + self.max_z),
        )
    }

    /// Produce the eight child octants for a split through the centre.
    /// Order is bit-encoded `zyx`.
    pub fn octants(&self) -> [Aabb; 8] {
        let (cx, cy, cz) = self.center();
        let mut out = [*self; 8];
        for (i, slot) in out.iter_mut().enumerate() {
            let xhi = (i & 1) != 0;
            let yhi = (i & 2) != 0;
            let zhi = (i & 4) != 0;
            *slot = Aabb {
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
// Node — leaf bucket or internal octant, unchanged from Sprint GT.
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
                if bucket.len() > LEAF_CAPACITY && depth < max_depth {
                    let points = std::mem::take(bucket);
                    let octants = bounds.octants();
                    let mut children: [Child; 8] = array_init_leaves(octants);
                    for p in points {
                        if let Some(idx) = locate_child(&children, &p) {
                            match &mut children[idx].node {
                                Node::Leaf(b) => b.push(p),
                                Node::Internal(_) => {
                                    unreachable!("array_init_leaves must produce Leaf nodes")
                                }
                            }
                        } else if let Node::Leaf(b) = &mut children[0].node {
                            b.push(p);
                        }
                    }
                    *self = Node::Internal(Box::new(children));
                }
            }
            Node::Internal(children) => {
                if let Some(idx) = locate_child(children, &point) {
                    let child = &mut children[idx];
                    let child_bounds = child.bounds;
                    child
                        .node
                        .insert(&child_bounds, point, depth + 1, max_depth);
                } else {
                    let child = &mut children[0];
                    let child_bounds = child.bounds;
                    child
                        .node
                        .insert(&child_bounds, point, depth + 1, max_depth);
                }
            }
        }
    }

    fn query_aabb(&self, self_bounds: &Aabb, q: &Aabb, out: &mut Vec<SpatialPoint>) {
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

    #[allow(clippy::too_many_arguments)]
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
// LinearOctree — pure core handle.
// ---------------------------------------------------------------------------

/// Sparse linear octree over `SpatialPoint` records.
#[derive(Debug)]
pub struct LinearOctree {
    bounds: Aabb,
    max_depth: usize,
    root: Node,
    total: usize,
}

impl LinearOctree {
    pub fn new(
        min_x: f64,
        min_y: f64,
        min_z: f64,
        max_x: f64,
        max_y: f64,
        max_z: f64,
        max_depth: usize,
    ) -> Result<Self, LinearOctreeError> {
        let bounds = Aabb::new(min_x, min_y, min_z, max_x, max_y, max_z)?;
        if max_depth == 0 {
            return Err("max_depth must be >= 1".to_string());
        }
        if max_depth > 32 {
            return Err("max_depth must be <= 32 (overflow guard)".to_string());
        }
        Ok(Self {
            bounds,
            max_depth,
            root: Node::new_leaf(),
            total: 0,
        })
    }

    pub fn insert(&mut self, point: SpatialPoint) -> Result<(), LinearOctreeError> {
        if !self.bounds.contains(&point) {
            return Err(format!(
                "Point {:?} at ({}, {}, {}) lies outside the octree bounds.",
                point.id, point.x, point.y, point.z
            ));
        }
        let bounds = self.bounds;
        self.root.insert(&bounds, point, 0, self.max_depth);
        self.total += 1;
        Ok(())
    }

    pub fn total(&self) -> usize {
        self.total
    }

    pub fn live_count(&self) -> usize {
        self.root.len()
    }

    pub fn max_depth(&self) -> usize {
        self.max_depth
    }

    pub fn bounds_tuple(&self) -> (f64, f64, f64, f64, f64, f64) {
        (
            self.bounds.min_x,
            self.bounds.min_y,
            self.bounds.min_z,
            self.bounds.max_x,
            self.bounds.max_y,
            self.bounds.max_z,
        )
    }

    pub fn query_aabb(
        &self,
        min_x: f64,
        min_y: f64,
        min_z: f64,
        max_x: f64,
        max_y: f64,
        max_z: f64,
    ) -> Result<Vec<SpatialPoint>, LinearOctreeError> {
        let q = Aabb::new(min_x, min_y, min_z, max_x, max_y, max_z)?;
        let mut out = Vec::new();
        self.root.query_aabb(&self.bounds, &q, &mut out);
        Ok(out)
    }

    pub fn query_sphere(
        &self,
        cx: f64,
        cy: f64,
        cz: f64,
        radius: f64,
    ) -> Result<Vec<SpatialPoint>, LinearOctreeError> {
        if !cx.is_finite() || !cy.is_finite() || !cz.is_finite() {
            return Err("query_sphere centre must be finite (no NaN/±inf).".to_string());
        }
        if !radius.is_finite() || radius < 0.0 {
            return Err("query_sphere radius must be a finite non-negative number.".to_string());
        }
        let r_sq = radius * radius;
        let mut out = Vec::new();
        self.root
            .query_sphere(&self.bounds, cx, cy, cz, radius, r_sq, &mut out);
        Ok(out)
    }
}
