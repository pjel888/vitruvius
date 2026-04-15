# Spatial Comprehension Protocol

## Purpose
This protocol defines how the Vitruvius AEC engine represents, reasons about, and emits spatial data. It is the architectural contract for the spatial kernel: it governs voxel CSG, voxel resolution hierarchy, heightmap topography, raycasting, the 3-Layer Execution Stack, the static / dynamic spatial index split, Wave Function Collapse usage, and the binary output format. It exists to make one thing structurally impossible — drawing a building before proving it.

## Scope
This protocol applies to:
- voxel constructive solid geometry (carving, boolean operations, resolution hierarchy)
- heightmap topography representation and ingestion
- raycasting, DDA traversal, and gravity enforcement
- the 3-Layer Execution Stack (Topological Graph → Analytical Arena → Explicit Instantiation)
- loose-octree versus tightly-packed BVH spatial index separation
- Wave Function Collapse usage rules for layout generation
- the binary spatial output format

This protocol does **not** govern:
- the ECS component schema that stores spatial data — see `02_ECS_AND_COMPONENT_DESIGN_RULES.md`
- the Z3 verification step that certifies Layer 2 — see `06_FORMAL_VERIFICATION_AND_Z3_PROTOCOL.md`
- IFC export and interoperability — see `07_BOUNDARY_TRANSLATION_PROTOCOL.md`
- audit trail and determinism of spatial operations — see `08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md`
- per-kernel implementation discipline — see `RUST/02_RUST_KERNEL_DEVELOPMENT_PROTOCOL.md`

## Core Principle
Vitruvius carves, it does not build. Geometry is the last thing the engine emits, never the first. Every spatial fact the engine holds in RAM is either a voxel that has survived a rule sweep, an analytical primitive under verification, or a coordinate that has already been proven compliant — nothing else.

---

## 1. The Constraint Satisfaction Reframing

### Rule 1.1
Architecture MUST be posed as a Constraint Satisfaction Problem, not as a drawing task.

### Rule 1.2
The spatial representation MUST be discrete mathematics (voxels, graphs, vectors, arithmetic predicates). Pretty drawings are not a representation; they are an export format.

### Rule 1.3
The question "is this building valid?" MUST reduce to "is this constraint system satisfiable?" — a question with a formal, decidable, machine-checkable answer.

### Rule 1.4
Any spatial routine that cannot be reframed as a constraint over discrete primitives does not belong in the spatial kernel.

---

## 2. Voxel CSG Rules

### 2.1 Carving, Not Building
- The engine MUST treat an empty lot as a solid block of voxel data.
- The engine MUST carve the envelope by sweeping and deleting forbidden voxels.
- The engine MUST NOT instantiate any geometry before the envelope is carved.
- What remains after the sweep is the **Maximum Buildable Envelope**. It is the only legitimate starting point for Layer 2.
- The spatial kernel MUST NOT contain any code path named, structured, or conceptually equivalent to "add a wall," "place a slab," or "extrude a volume" before envelope carving is complete.

### 2.2 Resolution Hierarchy
The spatial kernel MUST select voxel resolution per task, never globally:

| Resolution | Use |
|---|---|
| 25 cm | urban planning, lot yield, site-scale feasibility |
| 10 cm | default — massing, envelope carving, setback verification |
| 5 cm  | schematic design, code envelope refinement |
| 1 cm  | detail design, MEP routing — per-task only, never site-wide |

- 10 cm is the default. Any deviation MUST be justified in the kernel's data contract.
- 1 cm resolution MUST be scoped to a bounded routing domain (one shaft, one room, one plant). Holding a 1 cm grid for an entire site is forbidden.
- A kernel MUST NOT hold a single fine-resolution grid for an entire site under any circumstance.
- Coarse-to-fine refinement is the pattern: carve the envelope at 10 cm, then densify locally where Layer 2 requires tighter clash geometry.

### 2.3 Storage Strategy
- Outdoor space, sky volumes, and empty interior air MUST use sparse storage (OpenVDB-style or the current Rust-native equivalent). Empty voxels MUST cost zero bytes.
- Dense `ndarray`-style storage is permitted only inside a bounded interior routing domain where occupancy is high and sparse overhead is wasted.
- Every voxel crate adopted MUST be evaluated against the Wasm compatibility matrix before it enters the kernel.
- The kernel MUST expose a single voxel grid trait so that sparse and dense backends are interchangeable at the kernel boundary.

### 2.4 Allowed Boolean Operations
The spatial kernel MUST support exactly four boolean operations over voxel grids:
- **Union** — combining two envelopes.
- **Intersection** — the overlap of setback, daylight, and height envelopes.
- **Difference** — carving forbidden zones.
- **Symmetric Difference** — diff-style change visualization only.

All four operations:
- MUST be O(n) in voxel count.
- MUST be parallelizable.
- MUST be deterministic across runs (same input, same output, bitwise).
- MUST preserve the sparse-versus-dense backend choice of the input grid.

### 2.5 Forbidden Voxel Patterns
- Starting from an empty grid and adding voxels to "build" a mass is forbidden.
- Mixing resolutions inside a single grid without an explicit LOD boundary is forbidden.
- Caching a global fine-resolution grid "just in case" is forbidden.
- Allocating a dense grid larger than the bounded interior routing domain is forbidden.

---

## 3. Heightmap Topography Rules

### 3.1 Representation
- Topography MUST be stored as a 2.5 D heightmap.
- The heightmap MUST be a single contiguous `f64` array.
- Row-major or column-major ordering MUST be chosen once, documented in the kernel data contract, and never mixed inside the kernel.
- Sub-cell elevation queries MUST use bilinear interpolation against the four surrounding cells.
- A 3D Triangulated Irregular Network (TIN) MUST NOT appear in any spatial hot path.

### 3.2 Escape Hatch
- Overhangs, caves, and vertical cliffs MAY fall back to a mesh representation.
- The mesh escape hatch is opt-in per site, never the default.
- Any site that trips the escape hatch MUST be flagged in the site metadata so downstream kernels can branch deterministically.

### 3.3 Ingestion Pipeline
Topography enters the engine through exactly one of two pipelines:
- **LiDAR / LAS / LAZ** — ingest via `las` crate → classify ground returns → downsample to target resolution → grid into an `f64` array.
- **DWG / LandXML contours** — parse contour polylines in Python orchestrator → grid into an `f64` array.

Both pipelines MUST:
- write the final `f64` array to RocksDB under `terrain:{site_id}:{resolution}`.
- record the resolution, source file hash, and ingestion timestamp in the audit trail (cross-reference 08).
- produce byte-identical output for byte-identical input.

### 3.4 Resolution Rules
- 0.5 m horizontal resolution is the schematic-grade default.
- 1.0 m horizontal resolution is the urban-scale default.
- Finer-than-0.5 m resolution MUST be justified per site; the cache footprint MUST be computed and documented.

---

## 4. Raycasting and Gravity Rules

### 4.1 Vertical Ray Queries
- Vertical rays from building corners MUST resolve against the heightmap in O(1).
- Every placed footprint MUST fire one ray per corner before Layer 2 accepts it.
- The corner-elevation delta MUST be computed and stored as a first-class fact, not recomputed on demand.

### 4.2 General Ray Traversal
- General ray traversal MUST use a DDA (digital differential analyzer) walk over heightmap cells.
- The ray traversal MUST be branchless in the inner loop where possible.
- Traversal cost MUST be O(log n) or better in the number of cells crossed.

### 4.3 Gravity Enforcement
- Retaining walls, pilotis, and foundation stilts MUST be derived from raycast deltas, never assumed.
- A flat site assumption MUST NOT exist in the spatial kernel; any such assumption is a bug and a red-line.
- Cut-and-fill volume calculations feed the Pareto financial layer (cross-reference 09) and MUST be deterministic.

---

## 5. The 3-Layer Execution Stack

The spatial kernel MUST execute in three strictly ordered layers. Layer N MUST NOT proceed until Layer N−1 has certified its output.

### 5.1 Layer 1 — Topological Graph
- Use `petgraph` to determine what connects to what.
- Nodes are programmatic spaces, fixtures, and equipment. Edges are required connections.
- Layer 1 MUST resolve before Layer 2 begins.
- Layer 1 MUST NOT contain coordinates, dimensions, or geometry of any kind.
- Examples of Layer 1 facts: "fixtures connect to stacks," "breakers connect to outlets," "supply ducts connect to diffusers."
- Layer 1 output MUST be a fully connected, cycle-checked graph, or the pipeline halts with a diagnostic.

### 5.2 Layer 2 — Analytical Arena
- Coordinates are introduced here and nowhere earlier.
- Spatial primitives MUST be limited to `VectorSegment`, `ClearanceCapsule`, and `AABB` (see 02 for the ECS component contract).
- Clash checks MUST use segment-segment distance math, not triangle-triangle tests.
- Code checks MUST run against analytical primitives, not meshes.
- 3D meshes MUST NOT appear in Layer 2 under any condition.
- Layer 2 iterates until the configuration is clash-free, code-compliant, and Z3-certified (cross-reference 06).
- Layer 2 output is the verified coordinate set plus the proof artifact.

### 5.3 Layer 3 — Explicit Instantiation
- 3D geometry MUST be generated only after Layer 2 verification passes.
- The Python orchestrator extrudes cylinders, blocks, and surfaces from the verified coordinates.
- Layer 3 is a visualization of the truth, not the truth itself.
- Layer 3 MUST NOT feed back into Layer 1 or Layer 2. Feedback from Layer 3 to Layer 2 is a red-line.

### 5.4 Layer Ordering Rule
- The ordering is Topological → Analytical → Explicit. No other ordering is permitted.
- Any kernel that emits 3D geometry before Layer 2 verification has completed is a red-line violation and MUST be rejected at review.

---

## 6. Octree Static / Dynamic Layer Separation

### 6.1 Static Index
- Concrete beams, floor slabs, structural walls, and any other session-static entity MUST live in a tightly-packed BVH.
- The static index is built once per session and queried millions of times.
- The static index MUST NOT be rebuilt during Layer 2 iteration unless the structural topology itself changes.

### 6.2 Dynamic Index
- Pipes, cables, ducts, and any other entity being actively routed MUST live in a loose octree.
- Loose-octree node bounds MUST extend roughly 2× their canonical size so that small movements do not trigger re-linking.
- The dynamic index is cheap to update and is rebuilt as routing iterates.

### 6.3 Query Rules
- Spatial queries MUST check both indices and union the results.
- A single unified spatial query API MUST hide the static / dynamic split from Layer 2 solvers.
- The spatial index MUST NOT be rebuilt inside any routing inner loop — A*, Dijkstra, MILP routing, or otherwise. Rebuild belongs at the outer iteration boundary.
- Broad-phase and narrow-phase responsibilities MUST be separated; broad-phase against the BVH or octree, narrow-phase against capsule-capsule math.

### 6.4 Index Parity
- The static index and dynamic index MUST agree on the coordinate frame, units, and tolerance policy declared in the kernel's data contract.
- Mixing `f32` and `f64` across the two indices is forbidden.

---

## 7. Wave Function Collapse Usage Rules

### 7.1 Default Layout Method
- WFC is the default layout generator inside a verified envelope.
- WFC MUST only run against the Maximum Buildable Envelope produced by Section 2.
- WFC MUST NOT run against a raw lot or an un-carved voxel grid.

### 7.2 Applicability
- WFC is appropriate when the tile vocabulary is small and the adjacency rules are local.
- WFC is appropriate for multi-family housing, hotels, hospitals, offices, and similar repeated-typology buildings.
- WFC is NOT appropriate for one-off custom architecture (museums, sports venues, signature facilities). Those cases MUST fall back to an alternative method.

### 7.3 Fallback Hierarchy
- **Primary**: WFC with custom volumetric tile vocabulary.
- **Fallback**: mixed-integer programming (MILP) for small, high-stakes layouts (~50–100 rooms or fewer).
- **Research-only**: graph grammars. Graph grammars MUST NOT be placed on the production critical path.
- **Never**: raw generative adversarial networks or diffusion models as the primary layout generator — they do not guarantee constraint satisfaction and MUST only appear as proposers whose output is verified.

### 7.4 Verification Rule
- WFC output MUST pass Z3 verification before promotion to Layer 2 acceptance (cross-reference 06).
- A WFC result is a *proposal*, not a decision, until Z3 returns `unsat` against the negation of validity.
- A kernel that emits a WFC result without an accompanying Z3 proof artifact is in red-line violation.

---

## 8. Output Format Rules

### 8.1 Internal Binary Format
- FlatBuffers is the preferred internal binary format (zero-copy deserialization, schema-based).
- Cap'n Proto is an acceptable alternative only with documented justification.
- Protocol Buffers MUST NOT appear inside the kernel — reserved for external system interop.

### 8.2 Interoperability Format
- IFC is the interoperability format for external AEC tools.
- IFC conversion MUST happen at the boundary (cross-reference 07), never inside the spatial kernel.
- The spatial kernel MUST NOT depend on any IFC type directly.

### 8.3 Emission Ordering
- No 3D geometry MUST be emitted before Layer 2 verification succeeds.
- No binary output MUST be written before Z3 has returned `unsat` against the negation of validity.
- The output is pure binary truth, not a pretty `.3dm` or `.dwg`.

### 8.4 Payload Contents
The compressed binary output MUST contain exactly:
- validated coordinate arrays (envelope vertices, capsule endpoints, voxel deltas for carved space)
- the topological relationships from Layer 1 (which room connects to what, which pipe connects to which fixture)
- a cryptographic proof of verification — unsat core or hash of the verified rule set, with timestamp and rule version (cross-reference 08)

### 8.5 Forbidden Payload Contents
- No unverified coordinates.
- No 3D meshes that were used in Layer 2 as a shortcut.
- No intermediate WFC trial states — only the verified final result.
- No raw point clouds — those live in RocksDB under `terrain:{site_id}:{resolution}` and are referenced by hash, not inlined.

---

## 9. Forbidden Patterns

### 9.1 Solid-Build Modeling
Starting with geometry and checking compliance after is forbidden. The sequence is carve-then-verify-then-emit, not emit-then-check.

### 9.2 TIN Surfaces in Hot Paths
Triangulated Irregular Networks MUST NOT appear in the spatial hot path. Only the 2.5 D heightmap is allowed there.

### 9.3 Global Fine-Resolution Grids
A single fine-resolution voxel grid covering an entire site is forbidden regardless of available RAM.

### 9.4 Inner-Loop Index Rebuilds
Rebuilding the spatial index inside a routing inner loop is forbidden. Rebuild at the outer iteration boundary.

### 9.5 Premature 3D Emission
Emitting 3D geometry before Z3 verification is forbidden. Layer 3 is downstream of Layer 2, never parallel to it.

### 9.6 Layer Feedback
Feedback from Layer 3 back into Layer 1 or Layer 2 is forbidden. The stack is one-directional.

### 9.7 WFC Without Z3
Promoting WFC output to Layer 2 acceptance without a Z3 proof artifact is forbidden.

### 9.8 Mesh-as-Default
Treating a 3D mesh as the default representation of any spatial entity is forbidden. Meshes are escape hatches, not defaults.

---

## 10. Red-Line Conditions

A spatial-kernel change MUST be rejected at review if any of the following are true:
- The kernel builds up geometry before the envelope is carved.
- The kernel holds a global fine-resolution voxel grid for an entire site.
- The kernel emits 3D geometry before Layer 2 verification has passed.
- The kernel uses a TIN surface in a spatial hot path.
- The kernel uses a 3D mesh as the default representation of an entity that could be represented as a vector primitive.
- The kernel rebuilds the spatial index inside a routing inner loop.
- The kernel promotes WFC output to Layer 2 acceptance without a Z3 proof artifact.
- The kernel introduces feedback from Layer 3 into Layer 1 or Layer 2.
- The kernel mixes voxel resolutions inside a single grid without an explicit LOD boundary.
- The kernel assumes a flat site and skips raycasting against the heightmap.
- The kernel crosses the static / dynamic index boundary without going through the unified spatial query API.
- The kernel bypasses `07_BOUNDARY_TRANSLATION_PROTOCOL.md` by emitting IFC directly.
- The kernel stores verified coordinates in a non-deterministic container (hash-map iteration order, unsorted vector) such that byte-identical input produces non-byte-identical output.

---

## 11. Cross-References

### Research paper
- `.ai/13_research/AEC-ECS-SC_RESEARCH.md` §3 (full Spatial Comprehension section)
- `.ai/13_research/AEC-ECS-SC_RESEARCH.md` §12.6 (octree and BVH performance considerations)

### Companion AEC_ENGINE files
- `01_COMPOUND_AI_OPERATING_CONTRACT.md` — five-layer boundary contract
- `02_ECS_AND_COMPONENT_DESIGN_RULES.md` — spatial component schema and archetype rules
- `05_MULTI_DISCIPLINARY_COORDINATION_RULES.md` — how Arch/Struct/MEP share the analytical arena
- `06_FORMAL_VERIFICATION_AND_Z3_PROTOCOL.md` — the verification step that gates Layer 3
- `07_BOUNDARY_TRANSLATION_PROTOCOL.md` — IFC export and interop boundary
- `08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md` — determinism and audit obligations on spatial output

### Related RUST pack files
- `RUST/02_RUST_KERNEL_DEVELOPMENT_PROTOCOL.md` — per-kernel lifecycle and data contract discipline
- `RUST/04_RUST_ARCHITECTURE_AND_BOUNDARY_RULES.md` — low-level boundary discipline for spatial kernels crossing the Python/Rust edge
- `RUST/05_RUST_TESTING_BENCHMARKING_AND_VALIDATION.md` — numerical validation, edge-case coverage, and differential-test discipline for collision and distance math

The numerical details for segment-segment distance, capsule math, and related collision routines MUST be specified in the task-local Rust artifact created from `RUST/08_RUST_TASK_TEMPLATE.md`. This pack does not authorize an unnamed or future Rust file by implication.

---

## Final Rule
Geometry is the last thing the engine emits, never the first.
