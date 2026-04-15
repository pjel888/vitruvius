# ECS and Component Design Rules

## Purpose
This document defines the mandatory discipline for Entity-Component-System architecture in the Vitruvius AEC engine. It governs how components must be designed, how archetypes must be protected, how the three classic ECS traps (floating-point precision collapse, god component anti-pattern, spatial index thrashing) must be avoided, and how the Rust ECS layer (`bevy_ecs`) must remain structurally separated from persistence, knowledge, and LLM concerns. This is the architectural contract for every Rust-side entity, component, and system in the Vitruvius Compound AI engine.

## Scope
This file governs:
- ECS crate choice and the conditions under which alternatives are acceptable
- Component granularity and the atomic-data rule
- Archetype discipline and the structure-of-arrays layout contract
- Hot-path protection — what is forbidden inside system loops
- The three ECS traps in AEC (precision, god components, spatial index thrashing)
- The IFC-as-tag pattern and its enforcement
- The persistence boundary between `bevy_ecs` (in-memory) and RocksDB (durable state)
- Required test classes and archetype-fragmentation regression checks
- Red-line conditions that stop ECS work immediately

This file does NOT govern:
- Rust-language implementation style (see `RUST/07`)
- Spatial kernel math, broadphase/narrowphase algorithms, or pathfinding inner loops (see `03_SPATIAL_COMPREHENSION_PROTOCOL.md`)
- Rule AST storage, versioning, or temporal semantics (see `04_KNOWLEDGE_VAULT_AND_RULE_AST_CONTRACT.md`)
- Cross-language boundary and IFC translation (see `07_BOUNDARY_TRANSLATION_PROTOCOL.md`)
- Engineering solver kernels (per-kernel specs written against `RUST/08`)

## Core Principle
Data-oriented design is an architectural commitment, not a style choice. Cache locality is a correctness property of the Vitruvius engine, not an optimization. A component that forces irrelevant bytes into cache is a design defect, not a performance smell.

---

## 1. ECS Crate Choice

### 1.1 Prescribed Default
- `bevy_ecs` is the prescribed default ECS crate for the Vitruvius AEC engine.
- `bevy_ecs` MUST be used headless — the render, window, asset, and input subsystems of `bevy` MUST NOT be pulled into the engine crate graph.
- The archetype-based storage model of `bevy_ecs` MUST be treated as the physical layout contract. Any component design that defeats this layout is a boundary violation.

### 1.2 When Alternatives Are Acceptable
- `hecs` is acceptable ONLY when the dependency surface must stay minimal (e.g. a standalone audit crate, an embedded verifier) AND no parallel system scheduling is needed.
- `flecs_ecs` is acceptable ONLY when native entity-relationship modelling is a load-bearing requirement that cannot be expressed efficiently as component composition. This justification MUST be recorded in an AD.
- `specs`, `legion`, `apecs`, `shipyard`, and `planck_ecs` are NOT permitted for new work.
- Any non-default choice MUST be recorded as an AD in `.ai/10_state/decisions.md` before implementation.

### 1.3 Wasm Compatibility Rules
- The Wasm target MUST run `bevy_ecs` single-threaded for the MVP profile.
- Parallel scheduling on Wasm MUST be gated behind cross-origin isolation headers and the `atomics` + `bulk-memory` target features, and MUST be introduced only after the single-threaded profile is stable.
- A system MUST NOT assume thread affinity. Any system that depends on running on a specific worker thread is a defect.
- The Wasm build of the ECS layer MUST NOT pull in any pyo3, maturin, or host-FS dependencies (see `RUST/04`).

---

## 2. Component Design Rules

### 2.1 Components Are Pure Plain Data
- Components MUST be pure plain data: structs with fields, no methods, no inheritance, no meshes, no hidden references.
- Components MUST NOT carry behavior. Behavior lives in systems. Data lives in components.
- Components MUST NOT embed heap-owned collections (`Vec`, `HashMap`, `String`) unless the collection is the component's reason to exist AND a cache-locality waiver is recorded in the component doc.
- Components MUST NOT reference other components by Rust reference or lifetime. Use `Entity` IDs only.
- Components MUST derive `Clone` and the serialization traits required by the persistence boundary (see Section 8).

### 2.2 Atomic Granularity
- Components MUST be split to atomic data: fields that are used together belong in one component; fields that are used by different systems MUST live in different components.
- A component MUST NOT bundle unrelated fields for storage convenience. A pipe is not one component. A pipe is `VectorSegment` + `ClearanceCapsule` + `FluidDynamics` + `EntityLink` + (optional) `IfcOntology`.
- Before a new component is accepted, the reviewer MUST ask: "Does any single system load a field from this component that it does not use?" If yes, the component MUST be split.
- A component MUST NOT exceed 64 bytes without an explicit cache-line justification. A component with 32 bytes of live data is preferable to a component with 64 bytes of which 40 are used only by one system.

### 2.3 Component Documentation Requirements
Every component MUST carry a doc block that states:
- units for every numeric field (SI unless explicitly waived)
- coordinate frame for every spatial field (absolute world, floating origin, local frame)
- ownership model (who writes it, who reads it, who never touches it)
- expected archetype neighbors (the components it is routinely queried with)
- serialization class (per-component, snapshot-only, or event-sourced)

A component without this doc block MUST fail review.

### 2.4 Canonical Component Set
The canonical Vitruvius components are fixed in the research source (`AEC-ECS-SC_RESEARCH.md` §2.3) and in `01_COMPOUND_AI_OPERATING_CONTRACT.md`. They are: `VectorSegment`, `ClearanceCapsule`, `AABB`, `DomainDiscipline`, `EntityLink`, `IfcOntology`, `LoadBearing`, `ElectricalNode`, `FluidDynamics`. New components outside this set require an AD.

### 2.5 Hot-Path Cost Budget
- A component used in a hot-loop system MUST stay below its system's cache-line budget. The reviewer MUST compute `sizeof(component) * entity_count_per_tick` and compare against the target working set.
- The default target working set for a hot-loop system is the L2 cache of the slowest supported CPU. Components MUST NOT implicitly push the working set beyond L2.
- Components touched in hot paths MUST NOT invoke `Drop` glue. Plain POD composition is required.

---

## 3. The Three Traps

### 3.1 Trap A — Floating-Point Precision Collapse

#### 3.1.1 The Rule
- `f64` is the default for storage of absolute world coordinates.
- `f32` is permitted ONLY inside local-frame inner loops, ONLY after a documented transform into that local frame, and ONLY when the component doc states the rationale.
- SIMD lanes that assume `f32` MUST be reached through a local-frame transformation, not by downcasting a world coordinate in place.
- Any `f32` field on a component that stores world coordinates is a BLOCK-level review failure.

#### 3.1.2 The Floating Origin Point Pattern
- Where `f32` inner-loop speed is load-bearing, the component set MUST use a Floating Origin Point system: every transform carries an explicit origin frame ID, and the origin is re-centered on the building or zone currently under evaluation.
- The origin frame ID MUST be stored as a first-class field. Implicit or global origin state is forbidden.
- A system MUST NOT mix coordinates from two distinct origin frames in the same arithmetic operation.
- The transform into a local frame MUST be a pure function of the origin frame and the world coordinate, and MUST be tested against the round-trip identity `world_to_local(local_to_world(x)) == x` within tolerance.

#### 3.1.3 Canonical Trap Statements (Preserve Verbatim)
- "The game dev way is 32-bit floats because GPUs are fast. The AEC consequence is ghost clashes and missed clashes."
- "A bullet that clips through a wall for one 16 ms frame in Call of Duty costs nothing. A pipe that clips through a structural beam by 2 mm costs a contractor $50,000."

#### 3.1.4 Required Tests — Near-Large-Coordinate Regimes
Every spatial kernel that consumes `VectorSegment`, `ClearanceCapsule`, or `AABB` MUST carry tests at:
- origin (trivial baseline)
- 1 km from origin (city-block scale)
- 20 km from origin (municipal scale — the canonical precision-collapse regime)
- 100 km from origin (regional scale — stress test)

A test that passes at origin but fails at 20 km is a confirmation that the coordinate path is using `f32` somewhere it MUST NOT. This MUST be fixed before merge.

### 3.2 Trap B — God Component Anti-Pattern

#### 3.2.1 Forbidden Pattern
- A component that bundles unrelated fields (voltage, radius, material, manufacturer ID, IFC class) into a single struct is a god component and is forbidden.
- A god component is a performance cliff disguised as convenience. Every irrelevant byte loaded crowds out a relevant byte from a 64-byte cache line.
- A god component MUST be split on sight. Splitting a god component is not a refactor — it is a defect fix.

#### 3.2.2 Required Pattern — Atomic Components Queried in Isolation
- Components MUST be designed so that each system queries the smallest possible set of component types.
- Spatial systems query `VectorSegment` + `ClearanceCapsule` ONLY. They MUST NOT query `IfcOntology`, `EntityLink`, or any engineering-discipline component.
- Voltage systems query `ElectricalNode` + `VectorSegment` ONLY.
- Fluid systems query `FluidDynamics` + `VectorSegment` ONLY.
- Beam systems query `LoadBearing` + `VectorSegment` ONLY.
- A system that queries more than three component types in a hot loop MUST be reviewed for splitability.

#### 3.2.3 The Review Question
For every new or modified component, the reviewer MUST ask, in writing, in the PR description:
> "Is any system loading a field from this component into cache that it does not use?"

If the answer is yes, the component MUST be split before merge. This is not a style preference. It is the single most important discipline for ECS performance in Vitruvius.

### 3.3 Trap C — Spatial Index Thrashing

#### 3.3.1 Index Layer Separation
- The dynamic layer (entities currently being routed or optimized) MUST use a loose octree, which allows nodes to extend slightly beyond their canonical bounds so that small movements do not trigger node migration.
- The static layer (concrete beams, slabs, structural walls — entities that do not move during routing) MUST use a standard BVH or standard octree, built once per session and queried millions of times.
- The static/dynamic separation is mandatory. A single unified index is forbidden.

#### 3.3.2 No Rebuilds In Inner Loops
- A system MUST NOT rebuild a spatial index inside the A* inner loop, the simulated-annealing inner loop, or any routing hot path.
- Spatial index updates MUST be incremental within the loose-octree layer.
- A full index rebuild MUST be confined to session boundaries, layer swaps, or explicit invalidation events.

#### 3.3.3 Static/Dynamic Classification Is Component-Driven
- Classification as static or dynamic MUST be a marker component (e.g. `Static`, `Dynamic`), not a runtime flag on a shared component.
- Re-classification from dynamic to static MUST be an explicit event handled at a session boundary, not implicitly inside a system.

---

## 4. Archetype Discipline

### 4.1 Structure-of-Arrays Layout Is Load-Bearing
- Archetype-based storage is the physical contract of `bevy_ecs`. Component design MUST respect it.
- Systems MUST be written so that their query archetypes are stable across ticks. An archetype that changes composition every tick is a defect.
- The archetype plan for any new system MUST be documented in the PR description: which components, which archetype, expected entity count, expected cache footprint.

### 4.2 Marker Components Must Be Rare
- Marker components (zero-sized types used as tags) fragment archetypes and MUST be used sparingly.
- A marker component is acceptable for: static/dynamic classification, one-shot event tagging, and lifecycle transitions that are confined to frame boundaries.
- A marker component is NOT acceptable as a substitute for a field. If the tag carries information, it is a field, not a marker.

### 4.3 High-Churn Tags Use Sparse-Set Storage
- Tags that flip on and off frequently (e.g. `Dirty`, `NeedsReroute`, `ClashCandidate`) MUST be declared with sparse-set storage, not table storage, so that high-churn insert/remove does not fragment the dense archetype tables.
- A high-churn tag declared with table storage is a defect.

### 4.4 Required Query-Shape Audits
- Any PR that adds a component MUST include a query-shape audit: the list of systems that will query the new component, the archetype neighbors it will co-occur with, and the expected change in archetype count.
- A PR that increases archetype count without justification MUST be rejected. Archetype fragmentation is a latent performance cliff.

---

## 5. Hot-Path Protection

### 5.1 Forbidden Inside System Loops
The following are forbidden inside any `bevy_ecs` system loop:
- heap allocation (`Box::new`, `Vec::new`, `String::from`, `HashMap::new`, `format!`)
- cloning of large values (anything larger than a handful of words)
- unnecessary boxing or trait-object dispatch
- `println!`, `dbg!`, or any logging macro in release mode
- metadata queries into `IfcOntology`, `EntityLink`, or any provenance component
- string comparisons
- mutex or lock acquisition
- reflection or type-name lookup
- global state access that is not explicitly a `Resource`

### 5.2 Required Shapes
- Systems MUST consume components by shared reference (`&T`) by default and by exclusive reference (`&mut T`) only when mutation is the reason the system exists.
- Systems MUST use `Query` parameters with the narrowest possible component tuple. Over-broad queries are a defect.
- Scratch buffers MUST be allocated once and reused via `Local<T>` or `Resource`, never allocated per-tick.

### 5.3 The Cache Check
For every hot-loop system, the reviewer MUST compute, in the PR description:
- component bytes touched per entity per tick
- expected entity count per tick
- resulting working-set size
- which cache level (L1, L2, L3) the working set fits into

A system whose working set spills to main memory without an explicit trade-off rationale MUST be reworked.

---

## 6. IFC-as-Tag Pattern

### 6.1 Classification Is Metadata, Not Structure
- IFC classification MUST be stored as a lightweight optional metadata component (`IfcOntology`), typically a string or an integer class ID.
- The internal Vitruvius ECS is built around pure mathematical primitives (`VectorSegment`, `ClearanceCapsule`, `AABB`). IFC is a tag layered on top of those primitives, not a replacement for them.
- The research source fixes this pattern: "Build the internal ECS around pure mathematical primitives; treat IFC classification as a lightweight optional component."

### 6.2 Spatial Systems MUST NOT Query IFC
- No spatial system — broadphase, narrowphase, pathfinding, routing, precedence — MUST read `IfcOntology`.
- A system that branches on IFC class is a boundary violation. Branch on `DomainDiscipline` instead.
- `IfcOntology` MUST be absent from every query used in a hot loop.

### 6.3 IFC Is Touched Only At The I/O Boundary
- `IfcOntology` is read ONLY by the IFC translator at the export boundary.
- `IfcOntology` is written ONLY by the IFC importer at the ingestion boundary.
- The full translation rules live in `07_BOUNDARY_TRANSLATION_PROTOCOL.md`. This file enforces only that the ECS hot paths stay free of IFC coupling.

---

## 7. Persistence Boundary

### 7.1 bevy_ecs Is In-Memory Only
- `bevy_ecs` is the in-memory runtime model. It MUST NOT be treated as a source of truth across sessions.
- The source of truth for persistent state is RocksDB (the Knowledge Vault). The ECS layer hydrates from RocksDB on session start and flushes to RocksDB at snapshot or commit boundaries.
- A system MUST NOT call RocksDB inside a hot loop. Persistence is a boundary event, not a per-tick operation.

### 7.2 Serialization Strategy
- Serialization MUST be per-component, not per-entity. Each component type owns its own serializer and its own schema version.
- The global snapshot strategy is acceptable for small models and initial hydration. Event-sourced logs are acceptable for undo/redo and for temporal audit requirements (see `08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md`).
- Serialization formats MUST be deterministic: the same ECS state MUST produce byte-identical output every time.
- Component schema migration MUST be handled at hydration time, not at query time. The ECS runtime MUST NOT carry version-branching code in hot paths.

### 7.3 Undo/Redo Must Not Leak Into Hot Paths
- Undo/redo is an event-sourced concern. The event log MUST NOT be traversed inside a system loop.
- A system MUST NOT inspect or emit undo metadata. Undo is handled at session and commit boundaries.
- Cross-session state reconstruction is a Python-orchestrator concern (see `01_COMPOUND_AI_OPERATING_CONTRACT.md`) and is out of scope for the Rust kernel.

### 7.4 Out Of Scope For The Rust Kernel
- Cross-session state, multi-user concurrency resolution, schema evolution, and tenant isolation are NOT responsibilities of the Rust ECS layer.
- The Rust kernel owns the in-memory model and the serialization contract. Everything else belongs to Python, RocksDB, or the Compound AI orchestration plane.

---

## 8. Required Test Classes

### 8.1 The Core Test Classes
Every component and every system MUST carry the test classes defined in `RUST/05`:
- contract tests (type and shape correctness, legal input acceptance, illegal input rejection)
- edge-case tests (zero-length segments, coincident capsules, degenerate AABBs)
- property-based tests (symmetry, invariants, determinism, bounded output)
- differential tests against a slower, mathematically clearer reference implementation

This file adds two AEC-specific test classes on top of those.

### 8.2 Archetype-Fragmentation Regression Tests
- Every new component MUST carry a test that asserts the expected archetype count after inserting N entities with the expected composition mix.
- A PR that silently grows the archetype count is a regression. The test exists to catch it.
- The test MUST be declarative: "this component set produces K archetypes on N entities," not "this component set is faster than the old one."

### 8.3 Cache-Locality Sanity Benchmarks
- Every new hot-loop system MUST carry a cache-locality sanity benchmark: iterate over its component tuple across the expected working-set size and record ns-per-entity.
- The benchmark MUST be run at origin, at 1 km, at 20 km, and at 100 km from origin, to catch latent precision-induced slowdowns and to confirm the static/dynamic separation.
- Benchmarks live under the Python bench harness per `RUST/05`. The AEC-specific trigger points are defined here.

---

## 9. Forbidden Patterns

The following patterns are forbidden on sight:
- god components (any component bundling fields used by distinct systems)
- metadata queries (`IfcOntology`, `EntityLink`, provenance fields) inside hot loops
- implicit coordinate-frame assumptions (any function that takes a coordinate without an explicit frame ID or an explicit "world coordinate" doc statement)
- stochastic behavior inside deterministic systems (no RNG without an explicit seed sourced from a deterministic `Resource`)
- unbounded heap allocation in a system loop
- component fields whose units are not documented
- coordinate downcasts from `f64` to `f32` without a local-frame justification
- marker components used as de-facto fields
- table-storage tags that flip state on a per-tick basis
- cross-archetype iteration that implicitly walks all archetypes every tick without a `Changed<T>` or `Added<T>` filter

---

## 10. Red-Line Conditions

Stop work immediately and escalate to human review if any of the following are true:
- a proposed component bundles fields used by distinct systems (god component)
- a spatial field lacks an explicit coordinate frame
- a hot-loop system queries `IfcOntology`, `EntityLink`, or any provenance component
- a test at 20 km from origin fails while the test at origin passes
- archetype count grows without a documented query-shape audit
- any dynamic heap allocation is introduced inside a system loop
- a marker component is used to carry data
- a mutation path downcasts world `f64` to `f32` without a local-frame transform
- an RNG is used inside a system without an explicit deterministic seed resource
- persistence code appears inside a hot-loop system
- a system touches `bevy_ecs` and RocksDB in the same call path
- a Wasm build path pulls in threads without the documented atomics + bulk-memory gate
- a new component is declared without a documented unit, coordinate frame, ownership model, or archetype plan

---

## 11. Cross-References

- Research paper: `.ai/13_research/AEC-ECS-SC_RESEARCH.md` §2 (ECS Architecture — full section)
- Companion AEC_ENGINE files:
  - `01_COMPOUND_AI_OPERATING_CONTRACT.md` — the five-layer contract this file enforces Rust-side
  - `03_SPATIAL_COMPREHENSION_PROTOCOL.md` — the spatial kernels that consume these components
  - `07_BOUNDARY_TRANSLATION_PROTOCOL.md` — the IFC import/export boundary that writes and reads `IfcOntology`
  - `08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md` — determinism and event-sourced temporal rules that constrain serialization
- Related RUST pack files:
  - `RUST/02_RUST_KERNEL_DEVELOPMENT_PROTOCOL.md` — the lifecycle every ECS system MUST pass through
  - `RUST/03_RUST_SAFEGUARDS_AND_FAILURE_CONTAINMENT.md` — the safeguard layers, including the ECS-specific anti-patterns list
  - `RUST/04_RUST_ARCHITECTURE_AND_BOUNDARY_RULES.md` — the architecture boundary that keeps `bevy_ecs` out of policy and law
  - `RUST/07_RUST_STYLE_AND_IMPLEMENTATION_RULES.md` — Rust-language rules that apply inside every system

## Final Rule
A god component is a performance cliff disguised as convenience. Split it.
