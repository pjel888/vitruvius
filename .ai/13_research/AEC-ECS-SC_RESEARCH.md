---
title: Vitruvius — Consolidated Research Document
type: RESEARCH
status: REFERENCE
audience: codebase AI agents and human reviewers
version: 1.0
created: 2026-04-15
inputs:
  - Entity-Component-System__ECS__architecture.md
  - Hardcoding_the_AEC_Ontology.md
  - Spatial_Comprehension.md
disclaimer: |
  This document is RESEARCH. It surveys the design space, preserves prior
  conceptual work, and adds expanded technical context. It is NOT an audit,
  NOT an implementation plan, and NOT a directive to write code. Future
  implementation plans must be derived from this research as separate
  artifacts under the Standard Execution Loop.
---

# Vitruvius — Consolidated Research Document

> *Geometry is a derivative of Physics and Law.*

This document consolidates three prior research notes on the Vitruvius project — the headless, mathematically rigorous AEC physics and compliance engine — into a single reference. Every concept, paradigm, algorithm, Rust crate, equation, and architectural decision from the source files is preserved verbatim or paraphrased without loss. The document then expands each topic with additional research on the surrounding technical landscape, alternatives, comparative tradeoffs, related projects, and open questions, so that the codebase AI has a complete knowledge base from which to derive downstream implementation work.

The tone throughout is exploratory and surveying. Where multiple options exist, all are presented. Where the source files prescribe a specific choice, the prescription is preserved and contextualized against alternatives.

---

## Table of Contents

1. Vision and First Principles
2. Entity-Component-System Architecture
3. Spatial Comprehension
4. The Knowledge Vault (RocksDB)
5. The Compound AI System
6. Multi-Disciplinary Coordination
7. Mathematical and Algorithmic Arsenal
8. Engineering Solvers
9. 5D BIM and Financial Optimization
10. Interoperability — IFC, BIM, and the Boundary Translation Protocol
11. International Modular Rule Packages
12. Performance Engineering
13. Use Cases — Multi-Disciplinary Generation and Urban Planning
14. Open Research Questions and Risks
15. Glossary
16. References

---

## 1. Vision and First Principles

### 1.1 The Thesis

Vitruvius is not a 3D modeler. It is a **Multi-Objective Constraint Solver** for the built environment. The legacy AEC industry treats geometry as the primary representation and physics, code, and cost as overlays applied to that geometry. Vitruvius inverts this. Geometry is treated as a *derivative* of physics and law — it is what falls out when constraints are satisfied, not what humans push around with a mouse and then check for compliance after the fact.

The system is built around a single guiding principle that recurs through every architectural decision:

> The Physics are Universal, but the Parameters are Local.

Gravity, fluid dynamics, electrical resistance, and spatial collision behave identically in Manila, Singapore, and New York. A 2.0 m setback requires the same mathematical voxel carving regardless of what language the law is written in. Only the numerical parameters of the law (the actual 2.0 m, the actual fire-rated wall thickness, the actual minimum ceiling clearance) vary by jurisdiction. This separation is the core enabler of international scalability without engine bloat.

A second principle runs alongside the first:

> The computer is blind to human concepts. It only knows lines, points, bounds, and graphs.

Vitruvius treats the human-meaningful taxonomy of "wall," "pipe," "subdivision road," and "structural beam" as **labels attached to mathematical primitives**, never as the primitives themselves. A pipe is a line segment with a clearance radius. A subdivision road is also a line segment with a clearance radius — just with a larger radius. The Rust kernel does not distinguish between them. This is what enables fractal scale agnosticism: the same `aabb_intersects` math routes a fire sprinkler through a ceiling plenum and routes a highway through topography.

### 1.2 The Compound AI System Pattern

Vitruvius is a **Compound AI System** rather than a monolithic LLM. Responsibilities are strictly separated:

- **RocksDB** holds the **Rules** (versioned legal ASTs, jurisdictional parameters, pricing data).
- **Python** holds the **Logic** (orchestration, query routing, Z3 compilation, LLM tool-call dispatch).
- **Rust** holds the **Physics** (compiled deterministic kernels for collision, pathfinding, FEA, fluid dynamics, voxel CSG).
- **The LLM** is the **Mouth and Ears** (translates English into structured tool calls and translates structured results back into English — never does the math).
- **Z3** is the **Adjudicator** (formal verification of whether a proposed configuration satisfies all active constraints).

This separation is what gives the system its claim to **mathematical incapacity to lie about physics or law**. The LLM cannot hallucinate a clearance because it is never permitted to compute one. The Rust kernel cannot bend a law because it has no representation of laws — it receives compiled boundaries from Python and operates within them.

### 1.3 Determinism as the Default

Every layer below Python is deterministic. Given the same RocksDB snapshot and the same input geometry, the Rust kernel produces bit-identical output. This determinism is the foundation of:

- **Retroactive compliance audits** — load a 1995 building, set the clock to 1995, get the same answer the building's original engineers would have gotten.
- **Reproducible disputes** — two parties with the same input data cannot disagree on whether a pipe clashes.
- **Cryptographic proof artifacts** — the Z3 unsat core or sat assignment can be exported and independently verified.

Stochastic elements (simulated annealing, genetic algorithms, MCTS for combinatorial search) are confined to the **optimization loop above the verification layer**. The optimizer proposes; the deterministic kernel verifies; nothing ships unverified.

### 1.4 Hardware Reality

The reference development environment is constrained: an Apple M2 with 8 GB of unified memory, also expected to host a local LLM (Gemma-class, 3B–8B parameters typical, occasionally larger). Every architectural decision is filtered through this constraint. This is why:

- The ECS uses contiguous memory (cache-friendly) rather than pointer-chasing object graphs.
- Pipes are stored as 32-byte capsules rather than several-KB triangle meshes.
- Topography is stored as a 2.5 D heightmap (single contiguous f64 array) rather than as a millions-triangle TIN surface.
- 3D rendering is deferred until after mathematical verification (Layer 3 of the 3-Layer Execution Stack).
- The audit referenced as `RUST-PDF-1` reported a 48× reduction in peak RAM usage when migrating a kernel from Python to Rust.

The constraint also dictates the deployment story: the Rust kernel compiles to WebAssembly so the same code that runs locally on the M2 also runs in the user's browser, with React Three Fiber doing only the rendering and Wasm doing all the math.

### 1.5 What Vitruvius Will and Will Not Do

The candor recorded in the source files matters and is preserved here. Vitruvius will eliminate the dreaded "clash detection coordination meeting" phase of modern BIM. It will not eliminate construction professionals. Two reasons are explicitly named:

- **Constructability (Means and Methods).** A pipe might mathematically fit between a steel beam and a slab with 2 mm of clearance, but a human welder cannot fit a hand and a torch in 2 mm of gap. A crane cannot maneuver a beam into a slot without hitting temporary scaffolding. These are real-world constraints that pure spatial math does not capture.
- **Physical Entropy.** Mathematics assumes perfect rigidity. Real buildings deflect under load, settle into their foundations over years, and expand and contract with thermal cycles. The mathematically perfect 2 mm clearance becomes a physical interference six months after pouring.

Vitruvius elevates engineers from clash-resolution clerks to **Superhuman Editors** who review five clash-free, code-compliant variations the engine produced in microseconds and apply human intuition about what is actually buildable on a rainy Tuesday in Manila.

### 1.6 Domain Specialization

A deliberate strategic choice is recorded: Vitruvius drops any pretense of being domain-agnostic. It is not a general knowledge graph that incidentally handles buildings. It is purpose-built for AEC. This permits:

- **Hardcoding the AEC ontology** into the core. The spatial hierarchy `Site > Building > Floor > Room > Element` is baked into the schema and into the Rust memory layout. Spatial queries get faster because the engine knows what kind of spatial relationships to expect.
- **Dropping flexible parsers** for medical journals, generic legal statutes, or other unrelated corpora. Every line of Rust optimization work is dedicated to spatial geometry, clash detection, and building code compliance.
- **Owning a vertical** rather than competing as one more generic AI wrapper. The market is saturated with horizontal AI tools; deep, mathematically rigorous vertical solutions are rare.

---

## 2. Entity-Component-System Architecture

### 2.1 Why ECS, Not OOP

In Object-Oriented Programming, you think about Things. A `Pipe` object owns its properties (diameter, material, voltage rating) and its methods (`compute_pressure_loss()`, `check_clash()`). The data and behavior live together. This is intuitive for humans but catastrophic for performance at scale.

In Entity-Component-System architecture, you use **Data-Oriented Design**. You think entirely about **Contiguous Memory Arrays**. There are no `Pipe` objects. There is an `Entity` (just an ID number), and there are `Components` (pure plain-data structs) attached to that entity, and there are `Systems` (pure functions that iterate over arrays of components). The data lives separately from the logic, and the data lives in arrays that pack tightly into CPU cache lines.

The performance argument is concrete. When a system needs to check whether any plumbing pipes clash with structural beams, it does not load a list of `Pipe` objects with all their fields. It loads two contiguous arrays: every `VectorSegment` and every `ClearanceCapsule`. The CPU prefetches these arrays linearly and processes them at memory bandwidth. The other fields of those entities (material, manufacturer, voltage rating) never enter the cache and never slow the operation down.

### 2.2 The Core Crate Choice — `bevy_ecs`

The source files prescribe `bevy_ecs`. Bevy is a full game engine, but its underlying ECS crate can be used completely standalone, headless, with no rendering dependencies. Reasons for the choice:

- Most ergonomic, high-performance, and Wasm-compatible ECS in the Rust ecosystem.
- Allows the Rust Data Plane to query millions of vectors in parallel with zero lock contention (parallel system scheduler with automatic data-dependency analysis).
- Active maintenance, large community, mature query API, archetype-based storage that matches the AEC use case (entities of the same component composition stored together).

#### 2.2.1 Alternatives Worth Knowing

The codebase AI should be aware of the alternatives even if `bevy_ecs` is the prescription:

- **`hecs`** — minimalist, single-file ECS by Benjamin Saunders. Simpler API than `bevy_ecs`, fewer features (no parallel scheduler), but excellent if the dependency surface needs to stay tiny. Mentioned alongside `bevy_ecs` in the source files.
- **`flecs` (via the `flecs_ecs` Rust binding)** — C-based ECS with a Rust wrapper. Mature, used in commercial games, supports relationships between entities natively (which has appeal for AEC where "this pipe belongs to this floor belongs to this building" is a constant pattern).
- **`specs`** — older Rust ECS, mature but less actively developed than `bevy_ecs`. Was the canonical choice in the Amethyst era.
- **`legion`** — archetype-based like `bevy_ecs`, was historically a competitor; less actively maintained now.
- **`apecs`**, **`shipyard`**, **`planck_ecs`** — niche options, generally not preferred for new work.

The real architectural question is not *which* ECS but whether ECS is the right paradigm at all for AEC. The arguments in favor are strong (cache locality, parallelism, scale-agnostic data model). The arguments against center on the fact that ECS was invented for video games where the workload is "tick the simulation forward 16 ms" and AEC workloads are more like "answer this query about a static-or-slowly-changing model." For Vitruvius the answer appears to be that ECS is correct because the optimization loop (simulated annealing over thousands of candidate layouts) effectively *is* a tick-based simulation.

#### 2.2.2 Wasm Compatibility

`bevy_ecs` compiles cleanly to `wasm32-unknown-unknown`. The catch is that `bevy_ecs`'s parallel scheduler needs threads, and threads in Wasm require the `wasm32-unknown-unknown` target with the `atomics` and `bulk-memory` features plus the cross-origin isolation headers in the host page. For an MVP, single-threaded execution in Wasm is the safer first target, with parallel scheduling enabled later as a performance optimization.

### 2.3 Components — The Vector Abstraction

Components in Rust must be pure plain data: structs with fields, no methods, no inheritance, no meshes. The source files name the following core components for the Vitruvius ECS:

- **`DomainDiscipline`** — an enum with variants `Arch`, `Struct`, `HVAC`, `Plumbing`, `Elec`. This component dictates the **Hierarchy of Precedence** during clash negotiation (Section 6).
- **`VectorSegment`** — the actual 1D math primitive. Two fields: `start: [f64; 3]` and `end: [f64; 3]`. (The source files write `f32`; this is a known trap — see Section 12 on floating-point precision. The recommendation in this consolidated document is `f64` for absolute world coordinates with a Floating Origin Point system.)
- **`ClearanceCapsule`** — a single `radius: f32` (or `f64` if the precision argument extends here). Represents the physical size of the element plus the legally required buffer space around it. Combined with `VectorSegment`, this defines the geometric capsule used for clash math.
- **`AABB` (Axis-Aligned Bounding Box)** — a coarse 3D box used purely for the broad-phase spatial index (the `LinearOctree`). Stored as `min: [f64; 3]` and `max: [f64; 3]`.
- **`EntityLink`** — a pointer back to the RocksDB vault ID, e.g. `"rule_PD1096_sec804"` or `"asset_HVAC_001"`. Ensures that any mathematical entity can always be traced back to its semantic identity in the knowledge graph.
- **`IfcOntology`** — a lightweight optional component, literally a string or an integer ID, holding the IFC class label (e.g. `"IfcColumn"`). Not used by spatial systems. Used only at the export boundary by the IFC translator.

Engineering ontology components extend this base set:

- **`LoadBearing`** — for structural elements. Stores `material_yield_strength: f64` and `moment_of_inertia: f64`. Roughly 16 bytes per entity. Consumed by the Structural Kernel.
- **`ElectricalNode`** — for electrical elements. Stores `amperage: f32`, `voltage: f32`, `resistance_per_meter: f32`. Roughly 12 bytes per entity. Consumed by the Electrical Kernel.
- **`FluidDynamics`** — for plumbing and HVAC. Stores `flow_rate: f32`, `viscosity: f32`, `friction_coefficient: f32`. Roughly 12 bytes per entity. Consumed by the Plumbing and HVAC Kernels.

The cost of these engineering components on an 8 GB M2 is described as virtually zero. A building with 100,000 elements carrying all three components costs roughly 4 MB — negligible.

### 2.4 Systems — The Mathematical Hot Loops

Systems are pure Rust functions that iterate over arrays of components. The source files name three foundational spatial systems:

- **System 1 — `Broadphase_Octree_Update`.** Grabs all entities with `VectorSegment` and `ClearanceCapsule` components. Computes their `AABB`. Updates the `LinearOctree` (the broad-phase spatial index).
- **System 2 — `Narrowphase_Capsule_Clash`.** Queries the Octree for overlapping AABBs. For each overlapping pair, runs the $O(1)$ "shortest distance between two line segments" computation. If `distance < (radius_A + radius_B)`, generates a `ClashEvent` (an entity tagged with a `ClashEvent` component, or an event in the `bevy_ecs` event system).
- **System 3 — `Precedence_Negotiator`.** Listens for `ClashEvent`s. Inspects the `DomainDiscipline` of both entities involved. Automatically commands the lower-precedence entity to re-route via the A* pathfinder (Section 7).

The pattern generalizes to engineering systems: a `VoltageDropSystem` iterates over entities with `ElectricalNode + VectorSegment`; a `BeamDeflectionSystem` iterates over entities with `LoadBearing + VectorSegment`; a `FluidPressureSystem` iterates over entities with `FluidDynamics + VectorSegment`. Each runs in parallel because their component queries do not overlap.

### 2.5 The Three ECS Traps in AEC

The video game industry is roughly fifteen years ahead of AEC in spatial computing, but stealing ECS architecture from games comes with a critical caveat: **games are designed to lie**. A bullet that clips through a wall for one 16 ms frame in *Call of Duty* costs nothing. A pipe that clips through a structural beam in Vitruvius by 2 mm costs a contractor $50,000 on the job site. The traps below must be designed against from day one.

#### 2.5.1 Trap A — Floating-Point Precision Collapse (Catastrophic Cancellation)

**The Game Dev Way.** Games use 32-bit floats (`f32`) because GPUs process them quickly.

**The AEC Problem.** If a subdivision plot sits at absolute geographic coordinates 20 km from the city's `(0,0,0)` survey origin, an `f32` loses decimal precision. A 50 mm pipe might mathematically register as 48 mm or 53 mm due to rounding. You get **ghost clashes** (false positives) and missed clashes (false negatives).

**The Fix (Two Approaches).**

1. **Strict `f64`** for all absolute world coordinates. Doubles the memory footprint of coordinate data but eliminates the precision class of bugs. On modern x86_64 and ARM64 CPUs, `f64` arithmetic is essentially as fast as `f32` per operation; the cost is bandwidth.
2. **Floating Origin Point system.** Keep coordinates in `f32` but dynamically re-center the `(0,0,0)` origin on the specific building or zone currently under evaluation. This is a well-known game-engine technique used in Star Citizen, Outerra, and similar planet-scale renderers. Adds bookkeeping complexity (every transform needs to know which origin frame it is in) but preserves `f32` performance benefits where they exist (e.g. Wasm SIMD operations).

The recommended default for Vitruvius is `f64` for the storage of world coordinates and `f32` (or `f32` SIMD) for the inner-loop math after coordinates have been brought into a local frame. The combination gives precision where it matters and speed where it matters.

#### 2.5.2 Trap B — The "God Component" Anti-Pattern

**The Problem.** It is tempting to create a `MEP_Element` struct that stuffs voltage, pipe radius, material, and manufacturer ID into one component.

**Why It Fails.** ECS achieves blazing speed through CPU cache locality. If a system that only checks spatial clashes (radius and coordinates) is forced to load the manufacturer ID into cache alongside, memory bandwidth is wasted on data that will never be used. With cache lines of 64 bytes on most modern CPUs, every irrelevant byte loaded crowds out a relevant byte.

**The Fix.** Strip components down to atomic data. A pipe is not one component; it is three: `VectorSegment`, `ClearanceCapsule`, and `SystemVoltage`. Spatial systems query only the first two. The Voltage system queries only the third (plus `VectorSegment` for length). The cache stays hot for whatever the current system needs.

This is the **single most important discipline** for ECS performance and the discipline most often violated by engineers transitioning from OOP. Code review for new components must always ask: "Does any system use these two fields together but not the others? If yes, split them."

#### 2.5.3 Trap C — Spatial Index Thrashing

**The Problem.** As the A* pathfinder moves a pipe around trying to find a clash-free route, it updates coordinates thousands of times per second. If you use a standard Bounding Volume Hierarchy or Octree, rebuilding the tree on every update bottlenecks the entire CPU.

**The Fix (Two Approaches, Combinable).**

1. **Loose Octrees.** A loose octree allows nodes to extend slightly beyond their canonical bounds, so small movements of an entity do not require it to migrate between nodes. The query becomes slightly less efficient (each query may need to check neighboring nodes) but the update becomes vastly cheaper.
2. **Static / Dynamic Layer Separation.** Maintain two separate spatial indices: one for `Static` entities (concrete beams, floor slabs, structural walls — things that do not move during routing optimization) and one for `Dynamic` entities (the pipes and cables currently being routed). The static index is built once per session and queried millions of times; the dynamic index is rebuilt frequently but contains only a small subset of entities.

The combination — loose octree for the dynamic layer, standard octree for the static layer — is the recommended pattern.

### 2.6 The IFC Component Pattern (Tag, Not Structure)

The architectural decision recorded in the source files: **build the internal ECS around pure mathematical primitives, treat IFC classification as a lightweight optional component**, and translate at the I/O boundary. This decision is examined in depth in Section 10 (Interoperability). For ECS purposes, the takeaway is that an entity ingested from IFC carries its IFC class as a string in an `IfcOntology` component, but no spatial system ever queries this component. The IFC class influences only export.

### 2.7 Comparative Survey of AEC ECS Practice

Outside of Vitruvius, very few projects have applied ECS to AEC. Most BIM authoring tools (Revit, ArchiCAD, AECOsim, Vectorworks) use deeply nested OOP class hierarchies — exactly the pattern Vitruvius rejects. Notable exceptions and adjacent projects:

- **Speckle** (open-source AEC interoperability layer) uses a flexible, schema-light JSON-based object model. Not ECS, but shares the philosophy of treating geometry as data rather than as objects.
- **Hypar** (computational AEC platform) uses a function-as-a-service model with typed inputs and outputs. Closer to dataflow than ECS but shares the determinism-first stance.
- **Topologic** (open-source non-manifold topology library) treats spatial relationships as a graph of cells, faces, edges, and vertices. Compatible with an ECS overlay.
- **Bevy itself** has been used for non-game spatial visualization (geographic information systems prototypes, simulation dashboards) confirming that the headless-ECS pattern travels outside games.

The novelty of Vitruvius is the combination: a game-grade ECS, AEC-specific component vocabulary, jurisdictional rule packages, and formal verification via Z3. No prior published project does all four.

### 2.8 Open Questions for ECS Design

- **Persistence model.** `bevy_ecs` is in-memory. Vitruvius needs to persist entity state to RocksDB. What is the serialization strategy? Per-component serializers? A global snapshot? An event-sourced log?
- **Undo/redo.** Architects expect undo. ECS state is mutable. The conventional answer is event sourcing: store the sequence of mutations rather than the state, and reconstruct state on demand. This integrates well with the temporal RocksDB pattern but adds complexity.
- **Multi-user concurrency.** If two architects edit the same building simultaneously, who wins? The game-industry answer (last-writer-wins with optimistic concurrency) is probably acceptable for early prototypes but will need refinement for production.
- **Component versioning.** When `LoadBearing` gains a new field in version 2 of the schema, how are old persisted entities migrated? RocksDB temporality helps here but the ECS-level migration story is unwritten.

---

## 3. Spatial Comprehension

### 3.1 The Constraint Satisfaction Reframing

To make Vitruvius natively understand, comprehend, and output verifiable architecture without relying on a third-party 3D software's physics engine, the representation of space itself must change. Human architects draw lines and surfaces. Computers do not understand lines — to a computer, a line is just an array of two coordinates. If the engine is to inherently *know* whether a building is compliant, it must compute architecture as a **Constraint Satisfaction Problem (CSP)** using discrete mathematics.

This reframing is the central intellectual move of the Vitruvius project. Once the problem is posed as CSP, the entire toolkit of constraint programming, theorem proving, and combinatorial optimization becomes available, and the question of "is this building valid?" reduces to the question of "is this constraint system satisfiable?" — a question with formal, decidable, machine-checkable answers.

### 3.2 Voxelized Boolean Subtraction — Vitruvius Carves, It Does Not Build

Vitruvius does not build up; it **carves down**. An empty lot is treated as a solid block of 3D data, divided into thousands of discrete blocks (voxels) of 10 cm × 10 cm × 10 cm.

When the LLM extracts a legal constraint (a 3 m setback, a 45° daylighting plane) and passes it to the Rust kernel, the kernel translates the rule into a mathematical predicate. It then sweeps through the voxel grid:

- "Is voxel at coordinate (X, Y, Z) within 3 m of the property line?" → if true, delete voxel.
- "Is voxel at (X, Y, Z) penetrating the daylight plane?" → if true, delete voxel.
- "Is voxel at (X, Y, Z) below the minimum required setback from the rear lot line?" → if true, delete voxel.

What remains in the server's RAM is the exact, mathematically proven **Maximum Buildable Envelope**. Vitruvius comprehends the law by converting text into a 3D boolean subtraction array.

#### 3.2.1 Voxel Resolution Tradeoffs

The 10 cm voxel size is a deliberate choice that balances precision against memory:

| Voxel size | Memory for a 50 m × 50 m × 30 m lot | Precision adequate for |
|---|---|---|
| 1 cm | ~7.5 × 10⁹ voxels = ~7.5 GB at 1 byte/voxel | Detail design, MEP routing |
| 5 cm | ~6 × 10⁷ voxels = ~60 MB at 1 byte/voxel | Schematic design, code envelope |
| 10 cm | ~7.5 × 10⁶ voxels = ~7.5 MB at 1 byte/voxel | Massing, setback verification |
| 25 cm | ~4.8 × 10⁵ voxels = ~480 KB at 1 byte/voxel | Urban planning, lot yield |

The right answer is hierarchical: coarse voxels for envelope determination, fine voxels for detail routing, with the resolution chosen per task. The system never holds a single 1 cm voxel grid for an entire site.

#### 3.2.2 Voxel Storage Crates and Tools

- **`building_blocks`** (Rust) — a comprehensive voxel data library with chunked storage, LOD, and meshing. The most relevant Rust-native choice. As of 2024–2025 the project has been partially absorbed into successor projects; the codebase AI should verify the current canonical crate before adopting.
- **`feldspar`** — successor work in the same lineage.
- **OpenVDB** — the industry-standard sparse-voxel library from DreamWorks. C++ with mature Rust bindings (`vdb-rs` and others). Sparse storage means an "empty" voxel costs zero bytes, which is critical for AEC where most of a lot's volume is empty air.
- **`ndarray`** — for dense voxel grids where the lot is mostly occupied (e.g. mid-construction states).

The recommended pattern is sparse storage (OpenVDB-style) for outdoor and undeveloped space, and dense `ndarray` storage for the interior of buildings under detailed routing.

#### 3.2.3 Boolean Operations Beyond Subtraction

Subtraction is the most common operation but the full Constructive Solid Geometry (CSG) toolkit is needed:

- **Union** — combining two zoning envelopes (e.g. a building plus its allowed cantilever).
- **Intersection** — the overlap of a setback envelope with a daylight envelope (the buildable space is the intersection of all envelopes).
- **Difference (Subtraction)** — carving away forbidden zones.
- **Symmetric Difference** — rarely used in AEC but useful for diff-style change visualization.

All four operations are O(n) in voxel count and trivially parallelizable.

### 3.3 Topological Graph Grammar and Wave Function Collapse

Once Vitruvius has the valid envelope, the question becomes: where do the fire stairs, the core, the apartments, and the corridors go? This is **Wave Function Collapse (WFC)** territory.

#### 3.3.1 The Algorithm in Outline

WFC originated in procedural texture generation (Maxim Gumin's original 2016 algorithm) and has been adapted for level design in games (`Townscaper`, `Caves of Qud`). The architectural adaptation:

1. Define a set of "tile" types (programmatic spaces — apartment, corridor, stair core, lobby, mechanical room).
2. Define adjacency rules — which tiles can be neighbors of which other tiles. ("Fire stair must touch exterior wall." "Apartment must touch corridor." "Mechanical room must touch vertical shaft.")
3. Place the tiles on the voxel grid, propagating constraints. When a tile is placed, the set of valid neighbors at adjacent grid cells collapses (hence "wave function collapse" — the analogy to quantum superposition resolving to a definite state).
4. If a contradiction arises (no valid tile can be placed in a cell), backtrack or restart with a different seed.

#### 3.3.2 WFC Implementations in Rust

- **`wfc`** crate — a general-purpose WFC implementation by Stephen Sherratt. Used in roguelike and procedural generation contexts.
- **`wfc-image`** — variant tuned for image generation, less applicable to AEC.
- **`fast-wfc`** bindings — wrapping a C++ implementation that focuses on speed.
- **Custom implementation** — for AEC, a custom WFC that operates on volumetric tiles rather than 2D image patterns is likely required. The existing crates serve as references.

#### 3.3.3 Limitations and Alternatives

WFC is best when the tile vocabulary is small and the adjacency rules are local. AEC layout is plausibly within this regime for typical multi-family housing, hotels, hospitals, and offices — all of which have repeated standard room types. WFC will struggle with one-off custom architecture (museums, sports venues).

Alternatives for layout generation:

- **Graph Grammars** (the term used in the source files) — formal rewrite rules on a graph of programmatic spaces. More flexible than WFC but harder to implement and to debug. Used in academic AEC research (notably by Jose Duarte and the Shape Grammar tradition).
- **Subdivision-based approaches** — recursively subdivide the envelope using constraints (e.g. KD-trees with target room areas at the leaves). Used by TestFit and similar real-estate yield tools.
- **Generative adversarial networks and diffusion models** — pixel-domain layout generation. Fast but does not guarantee constraint satisfaction. Suitable as a *proposer* whose output is then verified and refined by deterministic methods.
- **Mixed-integer programming** — formulate layout as an MILP. Provably optimal but does not scale beyond ~50–100 rooms.

The pragmatic recommendation is WFC as the default with mixed-integer programming as a fallback for small high-stakes layouts and graph grammars as the long-term research direction.

### 3.4 Z3 Theorem Proving as the Ultimate Safety Net

Before Vitruvius ever outputs a result, the final voxel arrangement is translated back into formal logic and fed to the **Z3 Theorem Prover** with the active rules from the RocksDB vault.

The query posed to Z3 is the negation of validity: *"Given the laws in the vault, is it mathematically possible for this specific spatial arrangement to violate any code?"* If Z3 returns `unsat` (no model of the laws exists in which the arrangement is a violation) the geometry is certified as mathematically unassailable. If Z3 returns `sat`, the satisfying assignment is the *witness* — it tells you exactly which rule, with what variable bindings, the arrangement violates.

#### 3.4.1 Z3 Rust Bindings

- **`z3` crate** — the canonical Rust binding to Microsoft Research's Z3. Wraps the C API. Mature and widely used. Requires Z3 to be available as a system library at link time.
- **`z3-sys`** — the lower-level FFI binding underlying `z3`.
- **`z3.rs`** is sometimes used as an informal name; the actual crate name is `z3`.

#### 3.4.2 SMT Alternatives

The codebase AI should be aware of alternatives in case Z3's licensing, link-time dependencies, or performance become problematic:

- **CVC5** — the successor to CVC4, MIT-licensed, often competitive with Z3 on industrial benchmarks. Has a C++ API; Rust bindings exist but are less mature.
- **Yices 2** — SRI International's solver. GPL-licensed (the libre version), commercial license available. Strong on linear arithmetic.
- **Bitwuzla** — successor to Boolector, focused on bit-vectors and floating-point.
- **Pure-Rust SMT solvers** — `smtlib` parser exists; full pure-Rust solvers are research projects (e.g. `kissat-rs` for SAT, but no production-grade SMT). Not yet a viable alternative to Z3 for a serious project.

For Vitruvius, Z3 is the defensible default with CVC5 as a known fallback if needed.

#### 3.4.3 What Z3 Is Good At and Bad At

Z3 is good at:

- Linear arithmetic over integers and reals (ideal for setback rules, ratio constraints, dimensional bounds).
- Boolean combinations of constraints (ideal for "rule A AND rule B AND NOT rule C").
- Quantifier-free formulas (everything in AEC code can be expressed quantifier-free if the entity set is enumerated).
- Producing witnesses (the satisfying or unsatisfying assignment) which can be reported to users.

Z3 is bad at (or simply not suited for):

- Continuous geometry (it does not natively understand "the line from point A to point B intersects the cylinder of radius r centered on..."). The translation from geometry to arithmetic constraints is the engineer's responsibility.
- Optimization (Z3 has an `Optimize` mode but it is much slower than dedicated optimizers; for the financial Pareto search, use `argmin` or similar).
- Very large constraint systems (millions of variables). The strategy is to keep the Z3 query small — verify a single decision at a time, not the entire building at once.

### 3.5 The Output — Pure Binary Truth

Because Vitruvius is headless, its final output is not a pretty `.3dm` or `.skp` or `.dwg` file. It is a highly compressed binary file (FlatBuffer is the preferred format; IFC is the interoperability format) containing:

1. The validated coordinate arrays (vertices of the envelope, capsule endpoints for elements, voxel deltas for carved space).
2. The exact topological relationships (which room connects to what, which pipe connects to which fixture).
3. The cryptographic proof that the layout passed the Z3 legal audit (the unsat core or a hash of the verified rule set with timestamp).

Any 3D software (Rhino, Revit, a web viewer, R3F in the browser) can ingest this binary and render it. The intelligence and verification happened entirely inside the Rust kernel.

#### 3.5.1 Binary Format Tradeoffs

- **FlatBuffers** (Google) — zero-copy deserialization, schema-based, mature Rust support via `flatbuffers` crate. The recommended default for the Vitruvius internal format.
- **Cap'n Proto** — similar to FlatBuffers with arguably cleaner schema syntax. Rust support via `capnp` crate.
- **Protocol Buffers** — the most widely understood option but requires a parsing step (not zero-copy by default). Use only when interfacing with external systems that mandate it.
- **Apache Arrow** — for tabular data interchange (e.g. quantity takeoff exports). Excellent zero-copy story but oriented toward columnar analytics rather than spatial primitives.
- **IFC** — mandatory for export to other AEC tools. Bloated by construction (Section 10).

### 3.6 The Vector Abstraction — Death of the Polygon

In a traditional 3D software setup, a pipe is a cylinder made of hundreds of triangles. To check whether two pipes clash, the computer must check whether *any* triangle in pipe A intersects *any* triangle in pipe B — an $O(N^2)$ computational nightmare.

By using **Vector Abstraction**, a pipe is just a 1D line segment with a numerical radius. Finding a clash is no longer a geometry problem — it is a pure algebra problem. The CPU computes the shortest distance between two lines in a small constant number of operations. The hours-long clash detection process becomes a millisecond calculation.

#### 3.6.1 Memory Survival on Constrained Hardware

The argument is concrete:

- A 3D mesh pipe occupies several KB of memory (vertices, normals, texture coordinates, index buffer).
- A vector pipe (capsule) occupies exactly 32 bytes: two 3D `f32` points and an `f32` radius (or 56 bytes for `f64`).

By stripping 3D meshes during the thinking phase, millions of building components fit in a fraction of a megabyte. The LLM and the Rust spatial engine never have to fight for RAM.

#### 3.6.2 The Capsule Math

Given two capsules (line segment + radius), the clash check is:

```
distance = shortest_distance_between_segments(segA, segB)
clash    = distance < (radius_A + radius_B)
```

The segment-segment distance computation is a textbook routine (Eberly, Real-Time Collision Detection by Christer Ericson) — roughly 30 lines of code, no branches in the hot path, vectorizable with SIMD. Implementations are available in `parry3d` and in `nalgebra`'s extension crates.

For capsule-vs-AABB, capsule-vs-triangle, and capsule-vs-mesh (needed for the rare cases where a static element really must be represented as a mesh), `parry3d` provides the routines.

### 3.7 The 3-Layer Execution Stack

The pipeline that turns the vector abstraction into a working AEC engine has three layers, executed in order:

- **Layer 1 — Topological Graph (0D / 1D).** Use `petgraph` to figure out *how* things connect. The toilet must connect to the sewage stack. The breaker must connect to the outlet. The HVAC supply must connect to the diffuser. The building is treated as a network of nodes (programmatic spaces, fixtures, equipment) and edges (the connections that must exist).
- **Layer 2 — Analytical Arena (Math).** Map those connections to physical 3D coordinates using only lines (`VectorSegment`) and bounding boxes (`AABB`). Inflate lines with their clearance radii (`ClearanceCapsule`). Run clash and code checks on this purely analytical representation. Iterate until clash-free and code-compliant.
- **Layer 3 — Explicit Instantiation (3D Output).** Only *after* Layer 2 mathematically proves the building is clash-free and code-compliant does the system generate actual 3D geometry. The Python orchestrator takes the winning mathematical coordinates and says "extrude a 100 mm cylinder along this line so the human architect can see it."

This three-layer pattern is the operational expression of "geometry as derivative." The 3D model is a *visualization* of an underlying mathematically verified solution, not the solution itself.

### 3.8 The 2.5 D Heightmap — Topography Without Tears

In typical AEC software, topography is imported as a massive 3D mesh (a Triangulated Irregular Network, TIN) with millions of triangles. A collision engine that must check against millions of triangles either grinds or crashes on constrained hardware.

Rust does not use a 3D mesh for topography. It uses a **Heightmap** — a 2.5 D data grid:

- Imagine a spreadsheet where rows are the X axis, columns are the Y axis, and the cell value is the Z axis (elevation).
- Stored in Rust as a single contiguous 1D array of `f64` floats.
- To find ground height at coordinate `[10.5, 20.2]`, the engine performs a rapid bilinear interpolation between four array indices. Lookup time is $O(1)$ — essentially instantaneous.

#### 3.8.1 Heightmap Resolution

Typical surveys provide topography at 1 m or 0.5 m horizontal resolution. A 2-hectare site at 0.5 m resolution is a 200 × 200 grid = 40,000 cells × 8 bytes = 320 KB. A 50-hectare resort at 1 m resolution is 700 × 700 = 490,000 cells × 8 bytes = 3.9 MB. Both fit comfortably in cache.

#### 3.8.2 Limitations of the 2.5 D Model

The 2.5 D heightmap cannot represent caves, overhangs, or vertical cliffs (a single Z per (X, Y)). For 99% of AEC sites this is fine. For the rare site with overhanging rock, the engine would need to fall back to a true 3D mesh representation — preserved as an escape hatch, not the default.

### 3.9 Raycasting and the Law of Gravity

When parametrically planning a subdivision or placing a building, Vitruvius does not just *place* the building. It **raycasts**:

- The algorithm generates a house footprint and shoots mathematical rays straight down from the corners of the house.
- The moment those rays intersect the heightmap array, Rust knows the exact elevation of the terrain beneath each corner.
- If the terrain drops 2 m from the front of the house to the back, the constraint solver instantly knows it must dynamically generate a retaining wall or stilt foundation (pilotis) to maintain a level floor plate.

Raycasting against a heightmap is $O(\log n)$ in the number of grid cells crossed when implemented with a DDA (digital differential analyzer) traversal, and effectively $O(1)$ for the corner-of-house use case (a single vertical ray hits exactly one cell).

### 3.10 The Cut-and-Fill Financial Optimizer

This is where topography integrates with the Pricing Oracle (Section 9). In real-world AEC, moving dirt is expensive. *Cut* is digging dirt out of a hill. *Fill* is dumping dirt into a valley.

Because the Rust engine knows the volume of the building footprint and the volume of the terrain beneath it, it automatically calculates the exact cubic meters of cut and fill required to level the lot.

The Multi-Objective Constraint Solver can now include dirt as an optimization variable:

- **Option A** — Flatten the whole hill. (High cut cost, cheap standard foundation.)
- **Option B** — Leave the hill, build the house on deep concrete stilts. (Zero cut cost, expensive structural concrete.)
- The Python Pricing Oracle evaluates the live price of excavation versus concrete and tells Rust which parametric option yields the better total cost.

This is the same Pareto pattern as the rest of the financial optimization layer — multiple objectives traded off against each other under a hard constraint envelope.

### 3.11 The Ingestion Pipeline (From Reality to Rust)

To make topography work with real-world data:

1. The surveyor delivers a point cloud (LiDAR, photogrammetry) or a topographical survey in DWG or LandXML.
2. The Python orchestrator parses the file. For LiDAR, this means downsampling (raw point clouds are too dense; resample to the target heightmap resolution). For DWG, this means extracting contour polylines and gridding them.
3. The result is a flat `f64` array, stored in RocksDB as a binary value under a key like `terrain:{site_id}:{resolution}`.
4. When the project loads, Rust pulls the array from RocksDB into linear memory and uses it as the absolute lower boundary for all spatial math.

#### 3.11.1 Open Question — Raw Point Clouds vs Pre-Processed Contours

The source files explicitly leave open whether to accept raw LiDAR point clouds directly or to require users to upload pre-processed contours. The tradeoffs:

- **Accepting raw point clouds** — better user experience for surveyors with modern equipment, but adds a heavy preprocessing pipeline (point cloud filtering, classification, ground extraction, gridding). Crates: `las` for LAS/LAZ I/O, custom processing for the rest.
- **Requiring pre-processed contours** — smaller engineering scope, shifts work to the user, may exclude surveyors without GIS tools.

A pragmatic answer is to support both, with raw point cloud ingestion as a Phase 2 deliverable and DWG/LandXML as the Phase 1 default.


---

## 4. The Knowledge Vault — RocksDB

### 4.1 Why RocksDB, Not SQL

The choice of RocksDB rather than PostgreSQL or SQLite for the knowledge vault reflects the access pattern of the engine. The dominant operation is "given a jurisdiction, a domain, and a target entity type, return all applicable rules" — a prefix scan over hierarchically structured keys. SQL solves this via indexes and joins; RocksDB solves it natively via its log-structured merge-tree storage and its prefix iterator.

RocksDB also offers:

- **Append-only write semantics** that align naturally with the temporal-graph requirement (never delete a law, just append the amendment).
- **Compression** (Snappy, Zstd, LZ4) on disk, reducing the storage footprint of large legal corpora.
- **Embedded operation** — no separate server process, which matters for the local-first development workflow on the M2 and for deployment to the browser via Wasm-compatible RocksDB ports (limited but evolving) or alternative embedded KV stores.
- **Mature Rust binding** — `rust-rocksdb`, actively maintained, wraps the C++ RocksDB API.

### 4.2 The Smart Key Schema

The Key in RocksDB is everything. It must allow Python to instantly grab the exact rule it needs without scanning the database. The Vitruvius key is a colon-separated hierarchy:

```
rule:[jurisdiction]:[domain]:[target_entity]:[rule_id]
```

Examples:

- `rule:ph:architectural:setback_front:pd1096_sec804`
- `rule:ph:electrical:voltage_drop:pec_sec210`
- `rule:intl:structural:steel_deflection:aisc_360`

When the Rust ECS moves a concrete beam in Manila, Python issues `prefix("rule:ph:structural:concrete_beam")` and gets every relevant rule in microseconds.

The same hierarchical pattern extends to non-rule data:

- `cost:material:pvc_50mm` → 150.00 (PHP per meter)
- `cost:labor:plumbing_base` → 800.00 (PHP per day)
- `terrain:{site_id}:1m` → binary heightmap blob
- `asset:HVAC_001` → JSON metadata for a specific HVAC unit
- `entity:{building_id}:{entity_id}` → serialized ECS entity state for persistence

### 4.3 The Four-Block JSON Payload

When Python pulls a key, it receives a payload structured into four distinct blocks: **Identity, Temporality, Governance, and Physics**.

```json
{
  "metadata": {
    "rule_id": "ph_pd1096_sec804",
    "source_document": "National Building Code of the Philippines",
    "human_text": "Front setback for R-1 zoning shall not be less than 4.5 meters."
  },
  "temporality": {
    "version": "v2005_irr",
    "effective_date_start": "2005-04-30",
    "effective_date_end": null,
    "supersedes_id": "ph_pd1096_sec804_v1977"
  },
  "governance": {
    "enforcement_level": "statutory_law",
    "stringency_weight": 1.0,
    "waiver_possible": false
  },
  "physics_ast": {
    "constraint_type": "minimum_clearance",
    "parameters": {
      "target": "distance_to_property_line",
      "operator": "greater_than_or_equal",
      "value": 4.5,
      "unit": "meters"
    }
  }
}
```

#### 4.3.1 The Metadata Block (Identity)

The metadata block carries the human-readable provenance: a stable rule ID, the source document name, and the original natural-language text. This block exists for traceability — when a user asks "why is my setback 4.5 m?" the system can quote the actual law back to them with a citation.

#### 4.3.2 The Temporality Block

The temporality block transforms RocksDB into an **Append-Only Temporal Graph**. Old laws are never deleted; they are superseded. The `supersedes_id` field forms a linked list backward through every prior version of a rule. The `effective_date_start` and `effective_date_end` define the validity window.

This enables **Retroactive Compliance Audits**: load a building designed in 1995, set the orchestrator's internal clock to 1995, and Vitruvius will fetch the 1995 version of the ASTs to prove the building *was* compliant at the time it was built. This is enormously valuable for legal disputes, insurance claims, heritage assessments, and forensic engineering.

#### 4.3.3 The Governance Block — Three Enforcement Levels

The governance block dictates *how* the Z3 solver treats the AST:

- **`statutory_law`** (e.g. PD 1096 setbacks) — a hard boundary. If the Rust ECS proposes a violation, Z3 returns `unsat` and the orchestrator refuses to generate the building. No override possible.
- **`industry_standard`** (e.g. ASHRAE duct velocity guidelines) — a soft boundary. If violated, the layout is not destroyed. The Multi-Objective Optimizer heavily penalizes the score of layouts that violate it, preferring conformant routes but allowing exceptions if conformance would force a hard violation elsewhere.
- **`optimization_heuristic`** (e.g. "keep plumbing runs as straight as possible") — used purely by the financial and topological optimizer to reduce costs. Has no compliance implications.

The `stringency_weight` field allows fine-grained tuning of how hard the optimizer pushes against a soft boundary. The `waiver_possible` boolean records whether the rule admits administrative variances (which a human-in-the-loop system might present to a permitting officer).

#### 4.3.4 The Physics AST Block

The Physics AST block is the machine-executable representation of the law. Stored as a small Abstract Syntax Tree:

```json
"physics_ast": {
  "node_id": "rule_nscp_sec_409",
  "domain": "structural",
  "component_target": "concrete_beam",
  "constraint_type": "maximum_deflection",
  "formula_ast": {
    "operator": "divide",
    "left": "span_length",
    "right": 360
  },
  "confidence": 0.98
}
```

The AST decomposes the law into a mathematical tree. The Python Z3 Inequality Compiler walks this tree and translates it into a formal logic boundary: `Max_Deflection = span_length / 360`.

#### 4.3.5 AST Composability

The power of the AST format is composability. If the Plumbing Code says "minimum pipe slope is 2%" and the Architectural Code says "maximum ceiling plenum depth is 400 mm," Python fetches both ASTs, compiles them into a single Z3 constraint matrix, and hands it to Rust. Rust then computes whether it is physically possible to route the water with a 2% drop without bursting through the drywall — a single combined satisfiability query.

Composing ASTs is straightforward when they share variable names. The challenge is variable disambiguation across rules — `length` in one rule may refer to pipe length and in another to span length. The recommended convention is to namespace variable names by their parent rule and to use a translation layer at composition time.

### 4.4 The Absolute Rule — No Code in the Database

A rule from the source files that bears repeating: **never store raw executable code (Python scripts, Rust functions, JavaScript) inside the RocksDB vault**. Storing code in a database and running `eval()` is a massive security risk and kills performance.

Instead:

- **Physics** lives in compiled Rust kernels.
- **Legal constraints** live in RocksDB as strict JSON payloads (the AST format above).
- **Python** acts as the Babel Fish translating between them.

This separation is what makes Vitruvius a Compound AI System rather than a monolithic, brittle script. It is also what makes the system auditable — every rule in the vault can be inspected as JSON without executing anything.

### 4.5 LinkML, SHACL, and JSON Schema for Rule Serialization

The codebase AI should know that the AST format is custom but several adjacent standards exist for related work:

- **JSON Schema** — for validating the structure of the four-block payload itself. Mature, widely supported, recommended for input validation.
- **LinkML** — Linked Data Modeling Language. Schema language with both JSON Schema and OWL/RDF outputs. Useful if Vitruvius ever needs to publish its rule schema to the broader semantic web.
- **SHACL** — Shapes Constraint Language. A W3C standard for expressing constraints over RDF graphs. Closer to the constraint-language side of what Vitruvius needs but RDF-flavored.
- **OCL** (Object Constraint Language) — used in MOF/UML modeling. The IFC validation community uses it. Heavyweight.
- **mvdXML** — Model View Definition XML, used by buildingSMART for IFC validation rules. The closest existing standard to what Vitruvius's AST is doing, but tied to IFC.

A practical approach: define the Vitruvius AST as JSON Schema for input validation, and provide an mvdXML export adapter for users who need to publish their rules to the IFC validation ecosystem.

### 4.6 The LLM Ingestion Pipeline

The vault is populated by an LLM ingestion pipeline that reads PDFs, statutes, and standards documents and emits the four-block JSON. The LLM's job is strictly to *map unstructured text into the schema*. It is never asked to compute, judge, or reason about physics.

A typical extraction prompt structure:

1. Provide the LLM with the JSON Schema for the payload.
2. Provide the source text (a section of the law).
3. Instruct the LLM to emit JSON conforming to the schema.
4. Validate the emitted JSON against the schema.
5. If validation fails, retry with a corrective prompt.
6. Once validated, store with `confidence: <model_score>` in the AST block.

**Constrained generation techniques** make this much more reliable than free-form prompting:

- **OpenAI structured outputs** / **Anthropic tool use** — the LLM is constrained at the decoding level to emit valid JSON conforming to a provided schema.
- **JSON mode** — looser version of the above.
- **Outlines** (Python library) — provides regex- and grammar-constrained decoding for any local LLM.
- **Guidance** (Microsoft) — similar.
- **`grammars`** in `llama.cpp` — GBNF grammar files constrain emission.

For local Gemma-class models, Outlines or llama.cpp grammars are the right tools. The codebase AI should treat schema-constrained extraction as the default and never accept unconstrained LLM output for the vault.

### 4.7 Confidence and Human Review

The `confidence` field in the AST block exists because the LLM is not infallible. A practical workflow:

- High confidence (e.g. > 0.95): auto-accept into the vault, mark for sample review.
- Medium confidence (0.7–0.95): queue for human review before promotion.
- Low confidence (< 0.7): reject and flag for manual extraction.

The threshold values are tunable. The principle is that every rule that affects compliance should have been seen by a human at least once, even if the LLM did the heavy lifting of the initial extraction.

### 4.8 Open Questions for the Vault

- **Sharding.** RocksDB scales to terabytes on a single machine but Vitruvius may eventually want geographic sharding (one RocksDB per jurisdiction). The schema is ready for this; the operational tooling is not.
- **Browser deployment.** RocksDB does not run in the browser. For Wasm deployment, an alternative embedded KV store is needed. Candidates: `sled` (pure Rust, Wasm-compatible), IndexedDB-backed adapters, or simply preloading the relevant subset of the vault into Wasm memory at session start.
- **Distributed updates.** When PD 1096 is amended, every Vitruvius deployment globally needs the update. Push or pull? Signed or unsigned? Versioned snapshots distributed via CDN are the simplest answer.
- **Rule conflicts.** Two rules from different sources may genuinely contradict each other (the Plumbing Code says X mm minimum, the Building Code says Y mm minimum). The governance layer must include conflict resolution semantics — the source files do not yet specify these.

---

## 5. The Compound AI System

### 5.1 The Roles, Recapitulated

The system has five named layers, each with a strict responsibility:

- **The LLM** — *Mouth and Ears*. Translates English to JSON tool calls. Translates JSON results back to English. Never computes.
- **Python (the Orchestrator)** — *Logic*. Routes requests, fetches from RocksDB, compiles ASTs into Z3 constraints, dispatches to Rust kernels.
- **Rust (the Kernels)** — *Physics*. Deterministic, compiled, blazing fast. Owns the ECS, the spatial indices, the engineering solvers.
- **RocksDB** — *Rules*. Versioned, append-only, the single source of truth for laws and standards.
- **Z3** — *Adjudicator*. Formal verification of constraint satisfaction.

### 5.2 The Agentic Bridge — Function Calling

The pattern that connects natural language to deterministic computation is **tool calling** (also called function calling). The LLM is strictly prompted to never answer spatial questions directly. Instead, it translates the English sentence into a structured JSON command that Python understands.

#### 5.2.1 The Worked Example

User input:

> "Can we drop the ceiling in the ground floor lobby by 300 mm to fit a larger AC unit?"

LLM output (structured JSON, validated against tool schema):

```json
{
  "tool": "simulate_spatial_delta",
  "parameters": {
    "entity_target": "ceiling_lobby_GF",
    "delta_z": -300,
    "check_domain": ["architectural_clearance", "clash_detection"]
  }
}
```

Python receives this JSON and routes it to Rust. Rust:

1. Drops the ceiling plane by 300 mm in the ECS memory (a transient overlay; no commit yet).
2. Runs the `aabb_intersects` broadphase check.
3. Sees that the new ceiling height is 2.3 m.
4. Queries RocksDB for `prefix("rule:ph:architectural:lobby_clearance")`.
5. Finds the PD 1096 rule: minimum lobby clearance is 2.4 m.
6. Returns a strict data payload to Python:

```json
{
  "status": "code_violation",
  "rule": "PD1096_Sec_805",
  "max_allowable_drop": 200,
  "current_clearance_m": 2.3,
  "minimum_clearance_m": 2.4
}
```

Python hands this back to the LLM. The LLM formats the friendly conversational response:

> "If we drop it by 300 mm, we violate the National Building Code (PD 1096 Sec 805) which requires a 2.4 m minimum lobby clearance. We can safely drop it by 200 mm maximum. Should I run a quick clash detection to see if the AC unit can fit in that tighter space?"

#### 5.2.2 Why This Pattern Matters

The pattern is what makes Vitruvius **mathematically incapable of lying about physics or law**:

- The LLM cannot hallucinate a clearance value because it is never asked to compute one. Its only valid outputs are tool calls.
- Rust cannot bend a rule because rules are not in Rust — they come in compiled from RocksDB via Python.
- RocksDB cannot generate phantom geometry because it only stores rules.

Each layer is structurally incapable of the failure modes that plague monolithic LLM systems. The Compound AI System is the architectural expression of this defense in depth.

#### 5.2.3 Tool Call Reliability

Tool calling has matured significantly across LLM providers since 2023:

- **Anthropic Claude tool use** (Sonnet, Opus) — strong schema adherence, native streaming of tool calls.
- **OpenAI function calling and structured outputs** (GPT-4, GPT-4o, GPT-5) — schema-guaranteed JSON via constrained decoding.
- **Google Gemini function calling** — comparable.
- **Local models** (Gemma, Llama, Mistral, Qwen, Phi) — tool calling capability varies; Gemma 2 and 3 have improved markedly. For unreliable models, wrap with Outlines or grammar-constrained decoding to enforce schema.

The codebase AI should design the tool surface to be small, well-typed, and well-documented. Tools should be composable (the LLM can chain them) but each individual tool should do one thing.

### 5.3 The Tool Catalog (Sketch)

A non-exhaustive sketch of the tool surface Python should expose to the LLM:

| Tool name | Parameters | Returns |
|---|---|---|
| `simulate_spatial_delta` | entity_target, delta_x/y/z, check_domain | status, violations, allowable bounds |
| `route_mep` | system (plumbing/elec/hvac), source, sink, constraints | path geometry, total length, clash report |
| `compute_envelope` | site_id, jurisdiction, zoning_class | voxel envelope, BHL, FAR utilization |
| `quantity_takeoff` | building_id, system_filter | itemized BOQ |
| `cost_estimate` | building_id, location, currency | itemized cost with topology metadata |
| `verify_compliance` | building_id, rule_filter | sat/unsat, violation list with rule citations |
| `propose_alternative` | building_id, objective, constraint_relaxation | ranked alternatives |
| `temporal_audit` | building_id, as_of_date | compliance report against historical rules |

The codebase AI should treat this as a starting point for design, not as a finished specification.

### 5.4 The Z3 Inequality Compiler

The Z3 Inequality Compiler is a Python module that walks an AST from RocksDB and translates it into Z3 constraint expressions. Sketch of the contract:

- Input: a list of AST objects from RocksDB plus a binding context (current ECS entity state, current jurisdictional parameters).
- Output: a Z3 `Solver` with all constraints asserted and a list of free variables corresponding to the design parameters being solved for.

The compiler must handle:

- **Arithmetic operators** — `+`, `-`, `*`, `/`, `mod`, `min`, `max`.
- **Comparison operators** — `<`, `<=`, `>`, `>=`, `=`, `!=`.
- **Logical operators** — `and`, `or`, `not`, `implies`.
- **Conditional expressions** — `if-then-else`.
- **Domain restrictions** — variable types (int, real, bool), bounds.
- **Composition** — combining multiple ASTs into a conjunctive Z3 query.

This module is the heart of the Python Logic layer. Its correctness is paramount; it deserves a strong test suite of golden ASTs paired with their expected Z3 encodings.

### 5.5 Datalog as an Alternative or Complement

Datalog is a declarative logic-programming language well-suited to expressing rules about graphs and relations. Several Rust Datalog engines exist:

- **`crepe`** — embedded Datalog macro for Rust. Compiles Datalog rules to Rust at build time. Very fast.
- **`ascent`** — similar, with more features (aggregations, lattices).
- **`differential-dataflow`** — incremental Datalog-like computation, scales to millions of facts.

A possible role for Datalog in Vitruvius is the *graph layer* of compliance reasoning — questions like "is every habitable room within 30 m of a fire exit along the egress graph?" are naturally expressed in Datalog. Z3 handles arithmetic constraints; Datalog handles relational ones. The two are complementary.

### 5.6 Local LLM Considerations

Running a local LLM (Gemma 4, Llama 3.1, Qwen 2.5, Mistral) on the M2 alongside everything else is a tight memory budget. Key considerations:

- **Quantization.** 4-bit or 5-bit quantization (GGUF format via llama.cpp) drops a 7B model from ~14 GB to ~4–5 GB at minimal quality cost.
- **Context window.** AEC tool calls and rule extraction can have long contexts (an entire code section). Models with 8k+ context are mandatory; 32k is comfortable.
- **Throughput.** On M2 8 GB, expect 10–30 tokens/sec for a 7B Q4 model. Adequate for interactive use but not for high-volume batch ingestion.
- **Privacy.** A local model means client data never leaves the device, which is a meaningful selling point for Filipino architects working on government projects.
- **Hybrid pattern.** Use the local model for routine tool calls and use a cloud model (Claude, GPT) for heavy ingestion runs. Same JSON schema either way.

---

## 6. Multi-Disciplinary Coordination

### 6.1 The Combinatorial Explosion Problem

Finite Element Analysis for structural engineering is a solved mathematical problem. A* pathfinding for plumbing is a solved problem. The true *boss fight* of AEC software is the **Combinatorial Explosion** — putting all the disciplines in the same 3D computational arena and forcing them to share space without crashing the computer or generating a physics-defying paradox.

The constraint that makes the problem tractable is **typical, standard engineering**. Vitruvius is not designed to solve Zaha Hadid's sweeping, non-uniform curved shells. It is designed for orthogonal grids, standard spans, predictable load paths, off-the-shelf MEP equipment. This turns an infinite-variable nightmare into a discrete, highly solvable algorithm.

### 6.2 The Shared Arena — Global BVH

To combine disciplines, they must all speak the same spatial language. In Rust, this is a **Bounding Volume Hierarchy (BVH)** — a massive, ultra-fast 3D index of every occupied millimeter of the building. The recommended implementation is `parry3d`, which provides production-grade BVHs for collision detection and supports both static and dynamic content.

When the Structural kernel generates a concrete beam, it registers that volume in the BVH as `OCCUPIED_RIGID`. When the Mechanical kernel tries to route a duct, it queries the BVH. The BVH instantly tells it whether the candidate space is free.

The BVH is the *data structure* through which the disciplines communicate. The *protocol* of communication is the Hierarchy of Precedence and the Negotiation Protocol below.

### 6.3 The Hierarchy of Precedence

Vitruvius cannot calculate Architecture, Structural, and MEP simultaneously — that would require solving a million simultaneous equations. Instead, it solves them in a strict **Hierarchy of Physical Inflexibility**:

1. **Architecture (the Bounds).** Defines the legal envelope, vertical shafts, minimum clear ceiling heights. Highly inflexible — dictated by law.
2. **Structural (the Skeleton).** Drops the column grid, spans the beams. Gravity does not compromise.
3. **Mechanical / HVAC (the Lungs).** Large ducts require massive spatial volumes and specific turning radii. Routes next, dodging structural beams.
4. **Plumbing (the Veins).** Waste pipes require strict gravity slopes (e.g. 2% drop). Routes next, weaving through whatever space HVAC left open.
5. **Electrical / Fire (the Nerves).** Cables and small PVC are highly flexible. Route last, snaking through the remaining gaps in the ceiling plenum.

The order is not arbitrary. It reflects the *cost of relocation* for each discipline. Moving a load-bearing column is enormously expensive (and potentially structurally unsafe); moving a cable tray is cheap. The hierarchy minimizes the expected cost of changes during the negotiation phase.

### 6.4 The Negotiation Protocol — Automated Clash Resolution

What happens when the Electrical kernel tries to route a cable tray but the Structural beams and HVAC ducts have taken 100% of the ceiling space? In traditional BIM, a clash is flagged and three engineers argue on a Zoom call for an hour. In Vitruvius, the ECS triggers a **Negotiation Protocol**:

- **Step 1.** Electrical kernel fails to find a path. Sends a `Constraint_Violation` signal to the orchestrator.
- **Step 2.** Orchestrator asks the HVAC kernel: "Can you flatten your duct aspect ratio from 1:1 to 1:3 to save vertical space?" If yes, recalculate.
- **Step 3.** If HVAC cannot compress further, orchestrator asks the Architecture kernel: "Drop the drop-ceiling by 150 mm to create more plenum space."
- **Step 4.** Architecture kernel drops the ceiling. Runs a quick check against the RocksDB vault: "Does dropping the ceiling violate the National Building Code minimum ceiling height?" If it passes the legal check, the conflict is resolved in milliseconds.

The protocol is recursive: any concession by one discipline can trigger renegotiation in the disciplines whose constraints depended on the changed parameter. The orchestrator must detect cycles and either terminate (declaring the configuration infeasible) or escalate to a higher-level optimization (changing structural bay sizing, which ripples back to architectural envelope, which ripples back to subdivision lot count — see the Bi-Directional Feedback Loop below).

### 6.5 The Fractal ECS Architecture — Scale Agnosticism

To the Rust data plane, the system is **fractal**. Vitruvius does not know what a "Subdivision" is or what a "Pipe" is. It only knows about spatial boundaries and flow networks.

- At the **macro scale**, a "Lot" is just a boundary component that cannot overlap with a "Road" component.
- At the **micro scale**, an "HVAC Duct" is just a boundary component that cannot overlap with a "Steel Beam" component.

Because the underlying mathematics — collision detection, boolean subtraction, pathfinding — is exactly the same at every scale, separate engines for urban planning and MEP routing are unnecessary. The same `parry3d` and `bevy_ecs` solve both.

The fractal scale example from the source files is concrete:

- A plumbing pipe is a line with a 0.05 m radius.
- A subdivision road is a line with a 5.0 m radius.

The Rust `engine_rs` kernel literally does not know the difference. It uses the same `aabb_intersects` math to route a highway through topography as it does to route a fire sprinkler pipe through a ceiling plenum. This is **true scale agnosticism**.

### 6.6 Hierarchical Lazy Evaluation — Compute Survival

While the math is the same at every scale, computing the exact 3D path of every plumbing pipe in a 2-hectare subdivision simultaneously is impossible. It would require terabytes of RAM and centuries of CPU time. To solve both scales hand in hand, Vitruvius uses **Hierarchical Lazy Evaluation** — solving the project in cascading resolutions:

- **Resolution 1 — The Macro Envelope.** Vitruvius calculates the subdivision. Buildings are treated as solid empty blocks. The optimizer optimizes for lot yield, road placement, and ROI.
- **Resolution 2 — The Core and Shell.** The system zooms into one building block. It places the structural grid and the vertical MEP shafts.
- **Resolution 3 — The Micro Routing.** The system zooms into a single floor. It runs A* pathfinding to route pipes from the shaft to the fixtures.

Each resolution operates on a different abstraction level of the same fractal model. Resolution 1 sees buildings as bounding boxes; Resolution 2 sees them as bounding boxes with internal shafts; Resolution 3 sees them as full ECS scenes with every component. Memory and compute are spent only at the resolution currently under inspection.

### 6.7 The Bi-Directional Feedback Loop

What happens if Resolution 3 fails — if the pipes physically cannot fit inside the shaft assigned in Resolution 2?

In a *dumb* system, an error is thrown. In Vitruvius, a **pressure signal** is sent back up the chain:

1. The micro-routing algorithm reports: "I need 15% more shaft space to avoid clashes."
2. The structural algorithm receives this, expands the core, pushes the exterior walls out by 0.5 m.
3. The macro subdivision algorithm receives the new building footprint. It realizes the buildings are now too wide for the current lot layout. It automatically recalculates the subdivision grid, dropping the total house count from 120 to 118 to maintain legal setbacks.
4. The Python orchestrator updates the financial model, showing a slight dip in ROI.

The result is a **living, breathing mathematical organism**. A millimeter change in pipe diameter dynamically ripples up to alter the multi-million-dollar ROI of the subdivision.

This bi-directional cascade is the holy grail of AEC technology. By keeping Vitruvius headless and focused strictly on the math, the engine actually executes it. Most legacy BIM tools cannot — their object models are too rigid and their cross-discipline communication is mediated by humans on Zoom calls.

### 6.8 Open Questions for Coordination

- **Convergence guarantees.** Does the Negotiation Protocol always converge, or can it oscillate? The literature on iterative constraint relaxation suggests that with monotone relaxation steps and a finite tile set, convergence is guaranteed. The codebase AI should design termination conditions and oscillation detection from day one.
- **Optimization across resolutions.** When the micro layer pushes back to the macro layer, the macro re-optimization may invalidate other micro decisions. A fixed-point iteration is one approach; a global joint optimization is another but is computationally heavier.
- **Human override.** When the protocol cannot resolve, what happens? A graceful escalation to a human (with all the context of what was tried) is the default. The escalation interface design is open.
- **Parallelism.** Disciplines could in principle be computed in parallel up to the point of negotiation. The scheduler design is non-trivial.

---

## 7. Mathematical and Algorithmic Arsenal

### 7.1 Morton Codes (Z-Order Curves)

**The concept.** A space-filling curve that maps multi-dimensional coordinates to a single integer in a way that preserves locality — points close in 3D space tend to be close in the 1D Morton order.

**How it helps Vitruvius.** Instead of searching a complex 3D tree to find which pipes are near a beam, a Morton code converts an `[x, y, z]` coordinate into a single integer. A standard sorted array of integers can be searched in $O(\log n)$ via binary search, or scanned linearly with full cache-line efficiency. Finding neighboring clashes becomes a blazing-fast linear or binary scan in memory rather than a complex 3D tree traversal.

**Rust implementations.**

- **`morton-encoding`** — pure Rust crate for Morton code encoding/decoding for arbitrary dimensions.
- **`lindel`** — provides Morton (Z-order) and Hilbert curve encoding.
- **`morton`** — older, lighter alternative.

Morton codes pair well with the broad-phase BVH or with Linear Octrees (the data structure named in the source files). A Linear Octree is essentially a sorted array of Morton-coded entity centroids — the "tree" structure is implicit in the integer ordering, with no node objects to allocate.

### 7.2 GJK and EPA — Convex Intersection and Penetration

**The concepts.** The Gilbert-Johnson-Keerthi algorithm is the fastest known method for determining whether two convex shapes intersect. The Expanding Polytope Algorithm extends GJK to compute the exact penetration depth and the minimum translation vector to separate the shapes.

**How they help Vitruvius.** While capsules and lines suffice for pipes, structural elements (custom steel brackets, shear walls, corbels) are convex hulls. GJK answers "do these two convex shapes intersect?" in microseconds. When the Structural kernel detects a violation, EPA mathematically provides the exact **Negotiation Vector** — the direction and distance to push the elements apart to resolve the clash.

**Rust implementations.**

- **`parry3d`** ships with both GJK and EPA implementations.
- **`rapier3d`** (the physics engine built on `parry3d`) uses them internally.
- **Standalone implementations** exist as research code; for production, use `parry3d`.

### 7.3 Simulated Annealing and Monte Carlo Tree Search

**The concepts.** Simulated Annealing (SA) mimics metallurgy. It starts by wildly *guessing* candidate configurations, with high probability of accepting a worse configuration ("high temperature"), and slowly *cools* — making smaller and smaller refinements until it settles in a mathematical global optimum (or a strong local one). Monte Carlo Tree Search (MCTS) builds a search tree where nodes are configurations and edges are decisions, and balances exploitation (deepen promising branches) with exploration (try new branches).

**How they help Vitruvius.** When generating a 2-hectare subdivision, brute-forcing every combination of roads and houses to find maximum ROI is impossible — there are more combinations than atoms in the universe. SA and MCTS *sample* the search space intelligently.

- SA iterates through subdivision layouts, gradually settling on a globally near-optimal one.
- MCTS is more appropriate when each decision has a clear set of discrete options (e.g. "place a road segment going north, east, south, or west").

**Rust implementations.**

- **`argmin`** — comprehensive optimization framework. Supports SA, gradient methods, particle swarm, more.
- **`oxigen`** — genetic algorithm framework.
- **`genevo`** — alternative GA framework.
- **`metaheuristics`** — collection of nature-inspired algorithms.
- **MCTS implementations** are mostly bespoke; no dominant Rust crate yet.

### 7.4 A* Pathfinding in 3D

**The concept.** A* is the canonical heuristic graph search algorithm. Given a start node, a goal node, a graph of moves, and an admissible heuristic estimate of remaining cost, A* finds the optimal path in the smallest number of node expansions of any algorithm guaranteed to find the optimum.

**How it helps Vitruvius.** Vitruvius generates the routing of HVAC ducts through ceiling plenums filled with structural beams and fire sprinklers — this is a 3D maze. The empty space of the building is treated as a 3D grid. A* is given a start (the AC unit) and an end (the vent). It mathematically *grows* a path through the empty voxels. Costs are assigned to certain areas — moving closer than 10 cm to a structural beam costs 10,000 points. The algorithm mathematically guarantees the safest, shortest, clash-free route.

**Variants relevant to AEC.**

- **Jump Point Search (JPS)** — orders-of-magnitude faster than vanilla A* on uniform-cost grids by skipping over symmetric paths.
- **Theta\*** — produces any-angle paths instead of grid-aligned paths. Useful for HVAC and pipes that don't snap to orthogonal grids.
- **Hierarchical Pathfinding A\* (HPA\*)** — precomputes inter-region paths for huge grids. Useful for large buildings.
- **Lazy Theta\*** — variant that delays line-of-sight checks for performance.
- **D\* Lite** — incremental A* that recomputes only what changed when the obstacle map updates. Useful for the negotiation protocol.

**Rust implementations.**

- **`pathfinding`** crate by Samuel Tardieu. A* with admissible heuristic, Dijkstra, BFS, DFS, Yen's k-shortest, more.
- **`bevy_pathfinding`** — Bevy-specific helpers.
- **JPS implementations** exist; verify maintenance status before adopting.

### 7.5 Wave Function Collapse

Already covered in Section 3.3 (Spatial Comprehension). Recapitulated here as part of the algorithmic arsenal: WFC is the recommended algorithm for layout generation within a verified envelope, with graph grammars and MILP as alternatives for cases WFC cannot handle.

### 7.6 Voxel CSG Operations

Boolean operations (union, intersection, difference) on voxel grids are the foundation of envelope determination and of "carving down" semantics. The operations are O(n) in voxel count and trivially parallelizable across cores or SIMD lanes.

**Rust implementations.**

- **`building_blocks`** family — see Section 3.2.2.
- **OpenVDB bindings** — production-grade sparse voxel CSG.
- **`ndarray` with custom kernels** — for small dense grids.

### 7.7 Steiner Tree and Minimum Spanning Tree

**The concepts.** The Steiner Tree problem asks for the minimum-total-length network connecting a set of "terminal" nodes, allowing the introduction of intermediate nodes (Steiner points) to shorten the overall network. It is NP-hard in general but has good approximation algorithms. The Minimum Spanning Tree (MST) is a special case (no intermediate points allowed).

**How they help Vitruvius.** MEP routing is *literally* a Steiner Tree problem in disguise. Given a set of plumbing fixtures (terminals) and a stack location (root), find the minimum-length pipe network connecting them all, allowing branch joints (Steiner points) anywhere in the building. The same applies to electrical conduits and HVAC ducts. The optimal MEP layout is the optimal Steiner Tree on the routing graph.

**Rust implementations.**

- **`petgraph`** — provides MST algorithms (Kruskal, Prim).
- **Steiner tree solvers** are typically bespoke; the `lp_modeler` and `good_lp` crates support the LP formulation.
- For exact small-instance solutions, MILP via `good_lp` is workable. For larger instances, approximation algorithms (e.g. the 2-approximation via MST on a complete metric closure) are the standard.

### 7.8 Z3 Inequality Compilation

Already covered in Section 5.4. The arsenal entry: Z3 transforms compositional rule reasoning from an O(rules²) all-pairs interaction problem into a single satisfiability query.

### 7.9 Pareto Multi-Objective Optimization

**The concept.** When an optimization has multiple competing objectives (maximize ROI, minimize construction time, minimize embodied carbon), there is no single optimum — there is a *Pareto frontier* of solutions where no objective can be improved without worsening another. The user picks from the frontier.

**How it helps Vitruvius.** The financial layer (Section 9) is intrinsically multi-objective. Returning a single "best" subdivision suppresses important tradeoffs. Returning the Pareto frontier (or its top-k extracted solutions) gives the developer real choice.

**Rust implementations.**

- **NSGA-II** — Non-dominated Sorting Genetic Algorithm II. The dominant Pareto algorithm. Several Rust implementations exist as research code; `oxigen` and `argmin` can be configured for it.
- **MOEA/D** — Multi-Objective Evolutionary Algorithm based on Decomposition. Alternative.
- **Particle swarm with Pareto archive** — another option, less common in academia but sometimes faster in practice.

### 7.10 Linear Programming and Mixed-Integer Linear Programming

**The concepts.** LP solves problems with linear objective and linear constraints over continuous variables in polynomial time. MILP adds integer variable support and is NP-hard but routinely solved at industrial scale. AEC layout problems can often be formulated as MILP for exact-optimal small-instance solutions.

**Rust bindings.**

- **`good_lp`** — high-level LP/MILP modeling library, supports multiple solver backends (Coin CBC, Highs, SCIP).
- **`lp_modeler`** — alternative modeler.
- **`coin_cbc`** — direct binding to the Coin-OR CBC solver.
- **`highs`** — bindings to the HiGHS solver (currently the strongest open-source LP/MILP).

For Vitruvius, LP/MILP is appropriate for resource allocation problems (apartment mix optimization, parking allocation) and for small layout problems. Larger problems use the heuristics in 7.3 and 7.7.

### 7.11 Computational Geometry Library — `parry3d`

The geometric workhorse. Provides:

- AABB and BVH construction and queries.
- GJK and EPA convex collision and penetration.
- Capsule, sphere, cylinder, cone, triangle mesh, convex hull, compound shape primitives.
- Ray casting, point-in-shape queries, closest-point queries.
- Continuous collision detection (CCD) for swept volumes — relevant for crane swing analysis and equipment movement clearances.

`parry3d` is the foundation of the Rust physics engine `rapier3d` (Bevy's default physics) and is mature, actively maintained, and battle-tested.

### 7.12 Linear Algebra — `nalgebra` and `glam`

- **`nalgebra`** — comprehensive linear algebra (matrices, transforms, decompositions, geometry primitives). Heavier API surface but feature-complete.
- **`glam`** — game-focused linear algebra. Faster small matrix operations, leaner API, SIMD-optimized. Used by Bevy.
- **`ndarray`** — multi-dimensional array (NumPy equivalent). For voxel grids and statistical computation.

The recommendation is `nalgebra` for the kernel where breadth matters and `glam` for the rendering and Wasm hot path where small-matrix speed matters. Both can coexist.

### 7.13 B-Rep CAD Kernel — `truck`

For structural engineering, simple meshes or voxels aren't always accurate enough to compute shear loads or moments of inertia. Mathematical curves and exact volumes are needed.

`truck` is an open-source, open-architecture CAD kernel written entirely in Rust. It allows Vitruvius to perform exact boolean operations (cutting a hole in a steel beam) and compute the precise volume and center of mass of structural elements without a third-party software license.

`truck` is younger than `parry3d` and the OpenCascade ecosystem (which is the C++ industry standard). The codebase AI should evaluate `truck`'s coverage of B-Rep operations against project needs and budget for the possibility of falling back to OpenCascade via FFI if `truck` lacks a critical feature.

### 7.14 Petgraph and the Graph Layer

`petgraph` is the gold-standard Rust crate for graph data structures and algorithms. Vitruvius uses it for:

- The MEP topology layer (Layer 1 of the 3-Layer Execution Stack).
- The egress graph for fire safety analysis.
- The dependency graph between rules in the vault.
- The negotiation graph (which discipline can yield to which).

Algorithms used: shortest path (Dijkstra, Bellman-Ford), MST (Kruskal, Prim), connected components, topological sort, max-flow (for HVAC airflow balancing), strongly connected components (for cycle detection in the rule graph).

### 7.15 Differential Equations and FEA

For structural dynamics, fluid simulation, and thermal modeling, ordinary and partial differential equations are unavoidable.

**Rust crates.**

- **`ode_solvers`** — ODE solvers (Runge-Kutta family, multistep methods).
- **`peroxide`** — numerical analysis library with statistics, calculus, ODEs.
- **`diffeq`** — newer ODE/DAE solver.
- **FEA-specific Rust crates are immature.** The realistic path is FFI to established C/C++ FEA solvers (CalculiX, Code_Aster, OpenFOAM for CFD) called from Python.

The Vitruvius philosophy of "Rust does the math" is preserved by writing the Rust kernel that *prepares* the FEA inputs (mesh, boundary conditions, loads) and *interprets* the outputs. The actual large sparse matrix solves can defer to mature C/Fortran solvers.

</CHUNK_EOF
echo "---"
wc -w /mnt/user-data/outputs/VITRUVIUS_RESEARCH.md
---

## 8. Engineering Solvers

### 8.1 The "Legal-to-Math" Bridge — A Worked Electrical Example

The legal data extracted from building codes is the secret sauce. Laws are not hardcoded in Rust — they live as ASTs in RocksDB, and the Z3 Theorem Prover (or the equivalent Rust solver) enforces them. The flow:

1. **The Law (RocksDB).** Python extracts a rule from the electrical code: *"Maximum allowable voltage drop for a branch circuit is 3%."* Stored as an AST in the vault.
2. **The Spatial Reality (Rust).** The Rust pathfinding algorithm routes a wire from the breaker box to a light fixture. It computes the topological distance: 45 m.
3. **The Computation (Rust).** The Rust electrical kernel runs the standard physics equation:

   $$V_{drop} = 2 \times L \times R \times I$$

   where $L$ is one-way length, $R$ is resistance per meter, $I$ is current. For a 45 m run carrying 20 A on 12 AWG copper, the result is roughly 4.5%.

4. **The Parametric Adjustment.** Rust recognizes the code violation. Instead of failing, the Multi-Objective Solver parametrizes the result: it automatically increases the wire gauge (lowering resistance per meter) until the voltage drop hits, say, 2.9%. The recommended gauge becomes the kernel's output, along with the certified compliance proof.

Vitruvius did not just route the wire. It *legally and mathematically sized it*.

### 8.2 The Structural Kernel — Euler-Bernoulli Beam Theory

For a simply-supported beam of length $L$ carrying a uniformly distributed load $w$, the maximum bending moment at midspan is:

$$M_{max} = \frac{w L^2}{8}$$

The maximum deflection is:

$$\delta_{max} = \frac{5 w L^4}{384 E I}$$

where $E$ is the modulus of elasticity and $I$ is the moment of inertia of the cross-section.

If the user stretches a room from 5 m to 8 m wide, the spatial length of the ceiling beam increases. The Rust kernel instantly computes the new bending moment, checks the deflection against the code limit (typically $L/360$ for live load), and dynamically deepens the concrete beam from, say, 400 mm to 600 mm to keep deflection within the limit.

#### 8.2.1 When Euler-Bernoulli Is Not Enough

Euler-Bernoulli assumes thin beams where shear deformation is negligible relative to bending deformation. For deep beams, short-span heavy beams, or beams with significant shear, **Timoshenko beam theory** is required:

$$\frac{d^2}{dx^2}\left(EI \frac{d^2 w}{dx^2}\right) - q + \rho A \frac{\partial^2 w}{\partial t^2} = \frac{EI}{\kappa A G} \frac{\partial^4 w}{\partial x^2 \partial t^2}$$

For most typical Philippine residential and small commercial work, Euler-Bernoulli suffices. The kernel should detect the regime (depth-to-span ratio threshold) and switch to Timoshenko or to a full 3D FEA solve when needed.

### 8.3 The Plumbing Kernel — Hazen-Williams Equation

For water flow in pipes, the Hazen-Williams formula gives the head loss due to friction:

$$h_f = \frac{10.67 L Q^{1.852}}{C^{1.852} D^{4.87}}$$

where $h_f$ is head loss (m), $L$ is pipe length (m), $Q$ is volumetric flow rate (m³/s), $C$ is the Hazen-Williams roughness coefficient (dimensionless, depends on pipe material), $D$ is internal diameter (m).

As water travels through pipes and elbows, it loses pressure due to friction. If the architectural floor-to-floor height increases, the plumbing kernel computes the new static head pressure (additional $\rho g h$ contribution) and automatically resizes the booster pump on the roof.

#### 8.3.1 Limitations of Hazen-Williams

Hazen-Williams is empirical and accurate for water in the typical AEC flow regime. For non-water fluids, very high or very low Reynolds numbers, or compressible flow (steam, gas), the **Darcy-Weisbach equation** is preferred:

$$h_f = f \frac{L}{D} \frac{v^2}{2g}$$

with the friction factor $f$ computed from the Colebrook-White equation or its explicit approximations. Vitruvius's plumbing kernel should support both.

### 8.4 The Electrical Kernel — Beyond Voltage Drop

Voltage drop is the most common code-driven calculation but not the only one. The electrical kernel should also handle:

- **Conductor ampacity** — given a current, what is the minimum conductor size that does not exceed temperature limits? Tables in the PEC and NEC provide ampacity by gauge and insulation type.
- **Short-circuit current calculation** — for breaker sizing.
- **Grounding resistance** — for safety compliance.
- **Demand load calculations** — for service entrance sizing. Diversity factors apply.
- **Fault current and selective coordination** — ensuring upstream breakers do not trip before downstream ones during a fault.

Each of these reduces to a deterministic formula or a table lookup. The codebase AI should structure the electrical kernel as a collection of pure functions with clearly defined inputs (entity properties + jurisdiction context) and outputs (sized component, compliance status).

### 8.5 The HVAC Kernel — Airflow, Loads, and Ducts

HVAC sizing is a chain of calculations:

- **Heat load calculation** — ASHRAE methods (CLTD/CLF, RTSM) compute the cooling and heating load per zone given climate, envelope, internal gains, and occupancy.
- **Airflow requirement** — load divided by temperature differential and air properties gives required CFM per zone.
- **Duct sizing** — the equal-friction method or static-regain method sizes ducts to deliver the required airflow within velocity and noise limits.
- **Pressure loss calculation** — friction in straight ducts plus dynamic loss at fittings (computed via loss coefficients $K$ from ASHRAE tables).
- **Fan selection** — total static pressure and CFM determine fan size.

Many of these calculations depend on local climate data. Philippine cities have published bin data and design temperatures available from PAGASA and from ASHRAE Climate Data 2021. The vault should hold this data as a per-location dataset.

### 8.6 The Egress Kernel — Fire Safety

The Philippine Fire Code (RA 9514) and the Building Code (PD 1096) define requirements for:

- **Maximum travel distance to an exit** — typically 30 m to 60 m depending on occupancy and sprinklering.
- **Minimum number of exits** — function of occupant load.
- **Exit width** — minimum width per occupant (typically 5 mm to 7.5 mm per person for stairs, 3.8 mm for level travel).
- **Dead-end corridors** — limited length.
- **Common path of travel** — limited length.

These are graph problems on the egress network. `petgraph` shortest-path algorithms compute travel distances. Capacity flow algorithms verify that exit width is sufficient for the occupant load. The kernel should produce both pass/fail compliance and a visualization of the longest-travel-path so designers can see *why* a configuration fails.

### 8.7 The FEA Bridge

For loads, materials, and geometry beyond the closed-form solutions above, finite element analysis is the answer. The Vitruvius pattern is:

- The Rust kernel prepares the FEA input (mesh from the parametric model, boundary conditions from the load analysis, material properties from the vault).
- An external FEA solver (CalculiX, Code_Aster) runs the solve.
- The Rust kernel ingests the solver output (stresses, deflections) and feeds them back into the constraint check.

Open-source FEA solvers are mature but operationally complex. A pragmatic intermediate is to defer FEA to a Phase 3 capability and do *closed-form* approximations (Euler-Bernoulli, simple plate theory) for early phases.

### 8.8 The Beauty of the Architecture

A note from the source material that bears preserving: the academic formulas (Hazen-Williams, Euler-Bernoulli, Ohm's Law, Manning, Bernoulli) have existed for over a century. The legal codes exist in textbooks. By feeding the legal codes into RocksDB via the LLM ingestion pipeline and programming the established physics formulas into Rust kernels, Vitruvius does not invent new physics. It merely acts as the ultra-fast calculator that aligns the two.

This is what makes the system feasible. The mathematical risk is low because the math is centuries old. The engineering risk is in the integration — keeping the engine fast, the data correct, and the orchestration reliable.

---

## 9. 5D BIM and Financial Optimization

### 9.1 The Effortless Part — Quantity Takeoffs

Because the Rust ECS already computes the exact `VectorSegment` length and `ClearanceCapsule` volume for every component to run clash detection, the **Bill of Quantities (BOQ)** is essentially free. Rust can parse the global BVH and emit "14,532 m of 50 mm PVC" and "450 m³ of 3000 PSI concrete" in a fraction of a millisecond.

If costing were simply quantity multiplied by static material price, the work would be done. It is not.

### 9.2 The Reality Check — Topological and Labor Costs

Real construction costs are nonlinear:

- **The Elbow Penalty.** A 10 m straight pipe is cheap. A 10 m pipe that zigzags four times to avoid structural beams requires four elbow joints, sealant, cutting, and welding. Each elbow can cost as much as a meter of pipe.
- **Labor Routing Complexity.** Installing a duct in a wide-open basement goes fast. Installing the same duct in a cramped, multi-disciplinary ceiling plenum takes a crew three times as long. Labor is usually the most expensive variable on a job site.
- **Waste Factors.** You cannot buy 3.2 m of rebar. You buy a standard 6 m length and cut it, with the offcut becoming waste.

If the A* pathfinder routes a plumbing line like a snake to avoid a minor structural clash, the raw material volume might increase only 5%, but the custom fittings and labor cost can spike 40%.

### 9.3 The Architectural Solution — Cost as a Math Weight

To keep the Rust Data Plane blazing fast, **dollar signs and pesos are never hardcoded into the ECS components**. Cost is treated as a mathematical weight in the optimization loop above the kernel.

#### 9.3.1 Topological Metadata

When the Rust engine routes a system, it does not just output the raw length. It counts nodes in the graph and emits a JSON summary:

```json
{
  "material": "PVC",
  "diameter_mm": 50,
  "length_m": 100,
  "directional_changes": 14,
  "elbow_count_90deg": 12,
  "elbow_count_45deg": 2,
  "junction_count": 3,
  "density_zone": "high",
  "shaft_passages": 2
}
```

The metadata is *topological* — it describes the shape of the network, not its dollar value.

#### 9.3.2 The Python Pricing Oracle

Python takes the metadata and queries the pricing database in RocksDB:

- `cost:material:pvc_50mm` → 150.00 (PHP per meter)
- `cost:fitting:pvc_elbow_90_50mm` → 45.00 (PHP each)
- `cost:fitting:pvc_elbow_45_50mm` → 35.00 (PHP each)
- `cost:labor:plumbing_base` → 800.00 (PHP per crew-day)
- `cost:labor:density_multiplier:high` → 1.5

It calculates base material cost, adds fitting cost from the elbow and junction counts, applies a labor multiplier based on density zone, and returns the total.

#### 9.3.3 The Budget Constraint

This is where the Multi-Objective Constraint Solver flexes. A hard rule like "Maximum Project Cost: 150 Million PHP" becomes a constraint on the optimizer. As Simulated Annealing iterates through subdivision layouts or MEP routes, it constantly scores them financially.

The engine might mathematically discover that spending an extra 500,000 PHP on deeper structural beams allows the HVAC ducts to run perfectly straight, saving 1.2 million PHP in custom sheet metal fabrication and labor. **Vitruvius optimizes the *total* system cost, not individual parts.** This is the core argument for integrated 5D BIM.

### 9.4 Localized Live Pricing

A live, localized pricing database is what transforms Vitruvius from a "cool technical achievement" into a **highly disruptive enterprise financial engine**. When developers build subdivisions or high-rises in Quezon City, the design is almost always dictated by the current cost of materials. If rebar prices spike, they switch to shear walls. If concrete spikes, they look at steel framing.

By having Python act as the **Pricing Oracle**, an air-gap is created between the physics and the finances — the perfect architectural design.

The key-value structure of pricing data in RocksDB:

- `cost:material:{material_code}` → PHP per unit
- `cost:labor:{trade}_{level}` → PHP per crew-day
- `cost:equipment:{equipment_code}` → PHP per day rental
- `cost:overhead:{category}` → PHP percentage
- `cost:tax:{category}` → percentage
- `cost:permit:{permit_type}` → PHP fixed fee

All of these can carry a `temporality` block similar to the legal AST: prices change over time, and historical pricing is needed for forensic cost reconstruction.

### 9.5 Crawl, Walk, Run — Labor Cost Maturity

Labor and topological costs are inherently inaccurate at first. The Crawl, Walk, Run progression:

- **Phase 1 (Crawl).** Compute exact raw material cost. Apply a flat percentage multiplier for labor and waste (e.g. material_cost × 1.35).
- **Phase 2 (Walk).** Introduce heuristics from Rust's metadata. If the Rust payload shows 300 elbows for only 100 m of pipe, Python flags the layout as "high density / high complexity" and bumps the labor multiplier to 1.50.
- **Phase 3 (Run).** Once Vitruvius has generated hundreds of buildings, train a small dedicated machine learning model (or use a local LLM as a regressor) to predict exact labor hours from the topological graph output.

By keeping the financial logic entirely in Python, the system can upgrade from Phase 1 to Phase 3 without ever rewriting or recompiling the lightning-fast Rust spatial physics kernel.

### 9.6 Pareto Optimization for Urban Planning

For urban planning use cases, the financial optimization is intrinsically multi-objective:

- **Hard constraints (Law).** PD 1096 and subdivision rules — minimum 30% open space, roads minimum 10 m wide, setbacks. The Z3 solver treats these as unbreakable walls. Layouts that violate are slaughtered.
- **Fitness functions (Business).** Maximize lot yield, minimize linear meters of expensive road paving, target ROI of 24 months, minimize earthwork.

Because the Rust kernel evaluates geometry in milliseconds, it does not draw one subdivision. It uses a genetic algorithm or NSGA-II to draw *ten thousand* subdivisions, throws away the illegal ones, scores the remaining legal ones against the financial targets, and hands the developer the top three layouts that maximize profit while mathematically guaranteeing legal compliance. **Algorithmic Real Estate.**

### 9.7 The Cut-and-Fill Optimizer (Cross-Reference)

Section 3.10 covers cut-and-fill optimization in topographic context. The financial layer integrates by treating dirt-moving as a cost line (excavation per cubic meter, hauling per cubic meter, fill compaction per cubic meter) and adding it to the multi-objective score. The Pricing Oracle's RocksDB keys for excavation are jurisdiction-specific (Manila excavation rates differ from Cebu).

### 9.8 Open Questions for the Financial Layer

- **Currency and locale.** Prices are quoted in PHP for the Philippines. The same engine should handle USD for ARE training, SGD for Singapore expansion, etc. Currency should be a first-class field in pricing entries.
- **Inflation modeling.** A 24-month ROI target depends on inflation assumptions. The pricing layer should support time-varying prices, not just snapshot prices.
- **Tax and permit fees.** Often a significant percentage of total cost. Should be in the same vault under their own key prefix.
- **Risk-adjusted optimization.** Real developers care about downside risk, not just expected return. The optimizer should be able to compute risk-adjusted measures (CVaR, semi-variance) on top of the deterministic cost.

---

## 10. Interoperability — IFC, BIM, and the Boundary Translation Protocol

### 10.1 The Million-Dollar Question

Should Vitruvius consider BIM and IFC standards? **Yes, absolutely.** Should the internal ECS architecture be built around them? **Absolutely not.** This is the architectural decision recorded in the source files and it is preserved as the recommendation here.

### 10.2 Why IFC Cannot Be the Core Schema

IFC (Industry Foundation Classes) is an incredible standard for interoperability and a computational nightmare for performance. IFC was designed in the 1990s using strict, deeply nested OOP. To define a single wall in IFC, the data structure is:

```
IfcRoot
  → IfcObjectDefinition
    → IfcObject
      → IfcProduct
        → IfcElement
          → IfcBuildingElement
            → IfcWallStandardCase
```

Mapping this seven-level inheritance tree into the Rust ECS would instantly destroy cache locality and memory speed. The heavy baggage of legacy BIM would be dragged into the lightning-fast mathematical arena. Beyond the inheritance depth, IFC entities carry many fields that have no relevance to the spatial math (manufacturer info, warranty data, material certificates, history of edits) — exactly the God Component Anti-Pattern (Section 2.5.2) writ large.

### 10.3 The Boundary Translation Protocol

The strategy: keep IFC at the boundary, never in the core.

#### 10.3.1 The Internal ECS Remains "Dumb"

Inside the Rust `engine_rs` kernel, the ECS is completely ignorant of what a "Wall" or an `IfcPipeSegment` is. It only knows about `VectorSegment`, `ClearanceCapsule`, and `DomainDiscipline`. This keeps the math pure and $O(1)$ fast.

#### 10.3.2 IFC as a Tag, Not a Structure

Instead of IFC being the core structure, IFC classification is treated as a lightweight optional component in the ECS. An `IfcOntology` component holds literally a string or integer ID:

- **The Math.** `VectorSegment { start: [0,0,0], end: [0,5,0] }`
- **The Physics.** `ClearanceCapsule { radius: 0.15 }`
- **The Metadata.** `IfcOntology { class: "IfcColumn" }`

When Rust runs clash detection, it completely ignores `IfcOntology`. It only looks at the math. But when calculation is done, the metadata is still attached for the export phase.

#### 10.3.3 The I/O Translators (the Air-Lock)

Strict boundaries at the entrance and exit of Vitruvius:

- **Ingestion (Reading BIM).** When an architect uploads an IFC file from Revit, the Python orchestrator strips away bloated 3D meshes and deep inheritance trees. It extracts only centerline coordinates and clearance radii, tags them with their original IFC IDs, and feeds *only the math* into the Rust ECS.
- **Export (Writing BIM).** Once Vitruvius has run A* pathfinding and mathematically proven a clash-free pipe route, the Python orchestrator takes the raw Rust coordinates, wraps them back into the bloated `IfcPipeSegment` schema, and outputs a valid `.ifc` file. The mechanical engineer can then open that file in Revit and see native 3D BIM.

### 10.4 IFC Tooling Landscape

The codebase AI should know what tools exist for IFC I/O:

- **IfcOpenShell** — the canonical open-source IFC library. Python bindings are excellent. Reads, writes, and extracts geometry (via OpenCascade). The pragmatic choice for the Python ingestion side.
- **web-ifc** — TypeScript/WebAssembly IFC parser by ThatOpen Engineering. Fast, browser-friendly. Useful for client-side IFC viewing in the R3F frontend.
- **bonsai-bim** (formerly Blender BIM) — Blender add-on built on IfcOpenShell. Useful for testing the export pipeline by opening Vitruvius-generated `.ifc` files in Blender.
- **xBIM** — .NET-based IFC toolkit. Less relevant for the Rust/Python stack but worth knowing.
- **IFC.js** — older JavaScript IFC tooling, largely succeeded by web-ifc.
- **buildingSMART validation tools** — official conformance checkers. Should be in the test pipeline for any IFC export.

### 10.5 IFC Versions

- **IFC 2x3** — the long-dominant version. Most existing files are 2x3.
- **IFC 4** — adds parametric geometry, better infrastructure support. Increasing adoption.
- **IFC 4.3** — adds civil infrastructure (rail, road, bridges, ports). Recently published.
- **IFC 5** — in development. Will significantly redesign the geometry kernel; potentially less OOP-flavored.

The Vitruvius default should be IFC 4 export with backward compatibility to 2x3 for ingestion. IFC 4.3 is relevant for the urban planning use cases.

### 10.6 The Universal Engine Advantage

By treating IFC as a translation layer rather than a core architecture, Vitruvius becomes the *ultimate universal engine*. The system can:

- Ingest an IFC file from ArchiCAD.
- Strip it down to pure mathematics.
- Run it against the Philippine Building Code in the RocksDB vault.
- Route a clash-free electrical system.
- Export it back as an IFC file for Revit.

Vitruvius remains the **Headless Physics Engine**. Revit, ArchiCAD, and other CAD tools handle the heavy 3D rendering and the strict IFC hierarchies. The division of labor is clean.

### 10.7 Beyond IFC — Other Interchange Formats

- **DWG / DXF** — AutoCAD's formats. Still widely used, especially for 2D drawings and legacy projects. Rust support via `dxf-rs` crate; richer support via Teigha (commercial) or libredwg.
- **glTF** — the de facto web 3D format. Lightweight, designed for streaming. The recommended format for delivering visualization to the R3F frontend.
- **STEP / IGES** — ISO standards for CAD interchange, common in mechanical engineering. Rust support via `truck` and via FFI to OpenCascade.
- **STL / OBJ / PLY** — mesh-only formats. Useful for 3D printing and quick visualization. Rust support is mature.
- **LandXML** — civil engineering interchange (terrain, alignments). Useful for site work.
- **CityGML / 3D Tiles** — for urban planning and city-scale data.
- **PMTiles / MBTiles** — vector tile formats for web maps. Useful for the urban planning frontend.

The codebase AI should treat IFC as the primary interchange and pick others à la carte based on use case.

### 10.8 Open Questions for Interoperability

- **Round-tripping fidelity.** Does an IFC import → Vitruvius processing → IFC export preserve all the metadata an architect cares about? Some loss is acceptable; opacity is not.
- **Performance ceilings.** Large IFC files (a hospital can be 500 MB) take minutes to parse with IfcOpenShell. The ingestion pipeline should be incremental and resumable.
- **Geometry extraction strategy.** IFC stores geometry in many representations (sweeps, B-Reps, meshes). Extracting *centerlines* from arbitrary geometry is a non-trivial geometric problem. The codebase AI should plan for this.
- **Validation of extracted ASTs.** When Vitruvius extracts the centerline of an IFC pipe, did it get it right? A visual diff tool comparing the original IFC against the Vitruvius reconstruction would be valuable for debugging.

---

## 11. International Modular Rule Packages

### 11.1 The Three-Layer International Architecture

The Vitruvius internationalization architecture has three layers:

#### 11.1.1 The Universal Data Plane (Rust)

The Rust ECS remains completely blind to geography. It does not know what "PD 1096" or the "International Building Code (IBC)" is. It only understands abstract AEC physics: `SweepVolume`, `MinimumClearance`, `StructuralDeflection`, `EgressPath`. This keeps the compiled Rust code lean, fast, and globally applicable.

#### 11.1.2 The Jurisdictional Vaults (RocksDB)

Instead of hardcoding Philippine laws in Python or Rust, the RocksDB knowledge graph is structured using **Modular Rule Packages**:

- Philippine Building Code → namespace `jurisdiction:ph:pd1096`.
- Philippine Fire Code → `jurisdiction:ph:ra9514`.
- Philippine Electrical Code → `jurisdiction:ph:pec`.
- Philippine Structural Code → `jurisdiction:ph:nscp`.
- BP 344 (Accessibility) → `jurisdiction:ph:bp344`.
- PD 957 (Subdivisions) → `jurisdiction:ph:pd957`.
- BP 220 (Socialized Housing) → `jurisdiction:ph:bp220`.

When expansion happens to Singapore, the Building and Construction Authority (BCA) guidelines are fed into the LLM pipeline, which generates a parallel namespace `jurisdiction:sg:bca`. These vaults store the specific numerical variables (setback distances, FAR ratios, minimum ceiling heights).

#### 11.1.3 The Context Injection Layer (Python)

When a user starts a project or an educational lab module, they select their location. The Python orchestrator acts as a switchboard:

- Queries the specific Jurisdictional Vault for that project.
- Grabs local numerical variables.
- Injects them into the universal Rust physics engine.

### 11.2 The Global Advantage

This modular approach is what makes the platform dangerous to legacy competitors. To expand educational platforms to prepare students for the ARE (Architect Registration Examination) in the United States, or the equivalent in Hong Kong, the physics engine and core software are not rewritten. The team simply:

1. Acquires the new corpus of text (statutes, IRRs, standards).
2. Runs it through the deterministic LLM ingestion pipeline.
3. Builds a new RocksDB vault.
4. Vitruvius is instantly fluent in a new country's laws.

The engine becomes a **legal cartridge swapper** that can train professionals globally.

### 11.3 Retroactive Compliance Audits (Cross-Reference)

The temporality block on every rule (Section 4.3.2) enables retroactive audits — load a 1995 building, set the orchestrator's clock to 1995, get the rules that were in effect at that time. This is enormously valuable for:

- **Heritage assessment** — verifying that a building was code-compliant when built.
- **Insurance disputes** — establishing the standard of care at the time of construction.
- **Forensic engineering** — reconstructing what reasonable engineers would have known.
- **Legal proceedings** — defending design decisions against later code amendments.

### 11.4 Philippine Codes — Inventory

The codebase AI should know the primary Philippine codes that need ingestion:

- **PD 1096** — National Building Code. Currently operating under the 1977 IRR with significant amendments; a new IRR is in long-running development. Covers occupancy classes, light and ventilation, fire-resistive requirements, structural, sanitary, electrical, mechanical at high level.
- **RA 9514** — Fire Code of the Philippines (2008) and its 2008/2019 IRR. Detailed fire safety requirements, occupant load, egress, sprinklers, alarms.
- **NSCP** — National Structural Code of the Philippines. Currently NSCP 2015 (Volume 1: Buildings) is the operative standard; NSCP 2024 has been published. Covers loads, materials, design methods.
- **PEC** — Philippine Electrical Code. Currently PEC 2017. Closely modeled on the U.S. NEC.
- **PME Code** — Philippine Mechanical Engineering Code.
- **PPC** — Philippine Plumbing Code.
- **BP 344** — Accessibility Law (1983) — and IRR. Mandates accessible design.
- **PD 957** — Subdivision and Condominium Buyer's Protective Decree (1976). Establishes minimum standards for subdivisions.
- **BP 220** — Standards for socialized and economic housing (1982).
- **PD 1067** — Water Code of the Philippines (1976). Governs easements along waterways.

Most of these are publicly available as PDF or as scanned images. PD 1096's IRR is well-publicized; the underlying decree text is short. The NSCP is published by the Association of Structural Engineers of the Philippines and is purchasable. The codebase AI should treat these as ingestion-pipeline inputs rather than as handcoded rules.

### 11.5 International Codes — Inventory for Future Expansion

For future jurisdictions:

- **United States.** ICC suite (IBC, IFC, IECC, IPC, IMC, IRC). NEC. ASCE 7 for loads. State and city amendments are extensive.
- **Singapore.** BCA Approved Documents. SS standards (SS 575 fire, SS 553 air conditioning, etc.).
- **Hong Kong.** Buildings Department's Code of Practice series.
- **Malaysia.** Uniform Building By-Laws 1984 (UBBL) and amendments.
- **Vietnam.** TCVN building code series.
- **Indonesia.** SNI standards.
- **EU.** Eurocodes for structural design (EN 1990–1999).
- **UK.** Approved Documents under the Building Regulations.

Each requires its own ingestion campaign and human review of the LLM-extracted ASTs before promotion to a production vault.

---

## 12. Performance Engineering

### 12.1 Why Rust Compiled to WebAssembly

When Rust compiles to WebAssembly (Wasm) and runs in the browser, it bypasses almost all the performance bottlenecks that plague standard web applications. For simulations like voxel carving and real-time spatial boolean operations, this is the architecture used by Figma, AutoCAD Web, and Photoshop on the Web to achieve desktop-level performance in a browser tab.

#### 12.1.1 Zero Garbage Collection Pauses

JavaScript is garbage-collected. A 3D simulation with 100,000 voxels in pure JavaScript will periodically freeze as the browser pauses to clean up memory. Rust has no garbage collector. When compiled to Wasm, it manages its own linear memory sandbox perfectly. A 3D simulation runs at locked 60 FPS because the browser never pauses to clean up.

#### 12.1.2 Contiguous Memory (the Array Advantage)

In JavaScript, objects scatter across RAM. In a Wasm module, thousands of voxels are stored in a single tightly packed array of raw bytes (Float32Arrays, or `Vec<f32>` in Rust which compiles to the same). When the Wasm kernel runs spatial constraints against the grid, the CPU reads contiguous memory linearly, taking advantage of CPU cache prefetching, making mathematical operations orders of magnitude faster.

#### 12.1.3 SIMD Support

Modern WebAssembly supports SIMD (single instruction, multiple data) — the `wasm32-unknown-unknown` target with the `simd128` feature. With SIMD, computing distances of 4 voxels from a property line happens in a single CPU clock cycle rather than four sequential operations. For 3D spatial algebra, this is a huge multiplier.

#### 12.1.4 The Thin Bridge Architecture (Zero-Copy Memory)

The biggest mistake developers make with Wasm is passing too much data between JavaScript and Wasm. JSON serialization kills performance. The Vitruvius API contract uses **zero-copy memory** — the 3D canvas (Three.js / R3F) and the Wasm kernel share the same physical memory buffer. JavaScript handles rendering (lights, camera, colors). Wasm handles physics (carving, collisions, math). They never translate data between each other.

The pattern is:

1. Wasm allocates a `Float32Array` for vertex data.
2. JavaScript creates a `Float32Array` view over the same Wasm memory range.
3. JavaScript hands the typed array to a Three.js `BufferAttribute`.
4. When Wasm mutates the buffer, Three.js sees the changes on the next frame without a copy.

#### 12.1.5 The Reality Check

Wasm is extremely performant but requires strict discipline. The codebase AI cannot allow lazy patterns like JSON-encoding geometry for transfer between Rust and JavaScript. Internal Rust kernel data must use FlatBuffers or contiguous byte arrays. Discipline is the price of speed.

### 12.2 The Rust → Wasm Toolchain

- **`wasm-bindgen`** — generates JavaScript glue for Rust functions exposed to Wasm. The de facto standard.
- **`wasm-pack`** — wraps `cargo build` + `wasm-bindgen` into a single command, produces NPM-publishable packages.
- **`trunk`** — for full-application Rust+Wasm builds (when Rust drives the entire frontend rather than embedding in a JS app).
- **`wee_alloc`** — small allocator for size-constrained Wasm builds. Less relevant now with `dlmalloc` improvements.
- **`wasm-opt`** — Binaryen's optimizer; significant size and speed wins.

### 12.3 Wasm Threads and Parallelism

WebAssembly threads (via the `wasm32-unknown-unknown` target with the `atomics` and `bulk-memory` features) require:

- A `SharedArrayBuffer` for memory.
- `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp` headers on the host page.
- A worker pool for thread spawning.

For Vitruvius, the parallel scheduler in `bevy_ecs` can take advantage of Wasm threads. The MVP can ship single-threaded; threading is a Phase 2 optimization.

### 12.4 Wasm Memory Limits

Standard Wasm has a 32-bit address space (4 GB max). Wasm `memory64` is in development and will lift this. For Vitruvius, 4 GB is plenty for the in-browser working set, but the codebase AI should be aware of the limit when designing in-browser data structures.

### 12.5 Floating-Point Precision (Cross-Reference)

Section 2.5.1 covers the `f32` / `f64` decision in depth. The performance angle: `f64` operations are roughly the same per-op cost as `f32` on modern hardware but consume 2× the memory bandwidth. For SIMD, `f64` SIMD provides only 2 lanes per 128-bit register vs 4 for `f32`. The hybrid recommendation (f64 for storage, f32 in the inner loop after local-frame transformation) preserves SIMD throughput where it matters.

### 12.6 Octree and BVH Performance Considerations

#### 12.6.1 Loose Octrees

A standard octree partitions space into eight equal octants recursively. Each entity is stored in the smallest node that fully contains its AABB. This is fine for static content but expensive when content moves — small movements can cause an entity to migrate between nodes, requiring tree restructuring.

A loose octree allows nodes to extend slightly beyond their canonical bounds (typically 2× the standard size), so small movements stay within the same node. The lookup cost increases marginally; the update cost drops dramatically. For Vitruvius's dynamic routing, loose octrees are the right default.

#### 12.6.2 Static / Dynamic Layer Separation

Maintain two separate spatial indices:

- **Static index.** Concrete beams, floor slabs, structural walls — built once per session, queried millions of times. Use a tightly-packed standard BVH for fastest queries.
- **Dynamic index.** Pipes and cables currently being routed — rebuilt frequently, contains a small subset of entities. Use a loose octree for cheap updates.

Queries typically check both indices and union the results.

### 12.7 Cache-Friendly Data Layout

The ECS storage layout matters. `bevy_ecs` uses **archetypes** — entities with the same component composition are stored in the same archetype, with each component type stored in a separate contiguous array within that archetype. This is the "Structure of Arrays" (SoA) layout that maximizes cache efficiency for systems that iterate over a single component type.

The codebase AI should resist patterns that defeat archetype-based storage: marker components added to a few entities at a time can cause excessive archetype fragmentation. Use sparse-set components for tags that are added and removed dynamically.

### 12.8 The 48× RAM Reduction

The source files reference an `RUST-PDF-1` audit reporting a 48× reduction in peak RAM usage when migrating a kernel from Python to Rust. This is consistent with broader experience moving numerical code from Python (with NumPy, PyTorch, or pure Python) to Rust:

- Python objects carry significant per-object overhead (PyObject header is 16 bytes minimum, plus reference count and type pointer).
- Python lists of floats are pointer arrays to PyFloat objects; each float costs roughly 24 bytes including overhead, vs 8 bytes for a Rust `f64`.
- Garbage collection metadata adds further overhead.
- NumPy avoids per-element overhead for the data itself but still pays for object headers.

A 48× reduction is plausible for kernels operating on large arrays of small structs. The same migration pattern should apply to other Python kernels in the Vitruvius pipeline as they're identified.

### 12.9 Profiling and Benchmarking

- **`criterion`** — the canonical Rust microbenchmark framework.
- **`pprof`** — sampling profiler with Rust bindings.
- **`tracing`** — structured logging with span timing.
- **Browser DevTools** — for Wasm profiling in the frontend.
- **`stats-gl`** — for in-browser Three.js performance stats.

Performance budgets should be set per kernel. The source files note 30 FPS sustained on mid-range Android over 4G as the bar for the existing SlateCamp 3D Lab; for the Vitruvius computation kernel running headless the bar is different (kernel response time per query), but the discipline of explicit budgets is the same.

</CHUNK_EOF
wc -w /mnt/user-data/outputs/VITRUVIUS_RESEARCH.md
---

## 13. Use Cases — Multi-Disciplinary Generation and Urban Planning

### 13.1 Use Case 1 — Multi-Disciplinary Zero-Clash Generation

**The vision.** Generate Architectural, Structural, and MEP (Mechanical, Electrical, Plumbing) systems mathematically from the start, guaranteeing zero spatial clashes for a five-story building.

**The reality.** This is mathematically achievable using the Z3 Theorem Prover and the spatial kernels described above. If a structural beam is defined as an immutable volume, and an HVAC duct is a volume that must travel from Point A to Point B with a specific turning radius, the solver runs until it finds a path that returns `sat` with zero intersections. The engine generates a *topologically perfect* building.

**The candor — what mathematics does not capture.** Vitruvius will absolutely eliminate the dreaded *clash detection* phase of modern BIM. It will not eliminate construction professionals. Two reasons:

- **Constructability (means and methods).** A pipe might mathematically fit between a steel beam and a concrete slab with 2 mm of clearance. But a human welder cannot fit a hand and a torch in 2 mm. A crane cannot maneuver a beam into that specific slot without hitting temporary scaffolding.
- **Physical entropy.** Math assumes perfect rigidity. Real buildings deflect, settle, and expand with heat.

Vitruvius will not replace engineers. It will elevate them to **Superhuman Editors**. Instead of spending 40 hours figuring out how to route plumbing through a complex floorplate, the engineer reviews five clash-free variations Vitruvius generated in microseconds, and uses human intuition to select the one actually buildable by a crew on a rainy Tuesday in Manila.

#### 13.1.1 Concrete Pipeline for Use Case 1

The pipeline that turns this vision into a working system:

1. **Architecture solves first.** The legal envelope is computed (voxel boolean subtraction against setbacks, FAR, daylight planes, easements). Vertical shafts are placed. Minimum clear ceiling heights are noted as constraints.
2. **Structural solves second.** Column grid is dropped; spans are assigned; beams are sized (Euler-Bernoulli). The structural mesh registers in the Global BVH as `OCCUPIED_RIGID`.
3. **HVAC solves third.** The MEP topology layer (Layer 1, `petgraph`) determines duct connectivity. The analytical arena (Layer 2) routes the duct centerlines as capsules around structural obstacles, using A* in the voxelized plenum with cost penalties for proximity to beams. Duct cross-sections are sized per ASHRAE.
4. **Plumbing solves fourth.** Same pattern, weaving through HVAC volumes, with the additional constraint of gravity slopes.
5. **Electrical solves fifth.** Same pattern, in remaining gaps.
6. **Negotiation runs throughout.** When a kernel fails to find a feasible solution, the Negotiation Protocol triggers and the appropriate higher-precedence discipline yields.
7. **Z3 verifies the final layout.** Every active rule is asserted; the layout is checked for `unsat`.
8. **Rendering happens last** (Layer 3). The 3D model is generated only after verification passes.

### 13.2 Use Case 2 — Business-Driven Urban Planning

**The vision.** Auto-generate a 2-hectare subdivision that perfectly satisfies both local zoning laws (open space, road widths) and strict business goals (ROI timelines, construction costs, yield).

**The reality.** This is a **Pareto Optimization** problem (Section 9.6). The Vitruvius treatment:

1. **Hard constraints (the law).** PD 1096 and subdivision rules — minimum 30% open space, roads minimum 10 m wide. The Z3 solver treats these as unbreakable. Layouts that violate are discarded immediately.
2. **Fitness functions (the business).** Maximize lot yield, minimize linear meters of expensive road paving, target ROI of 24 months.

Because the Rust kernel evaluates geometry in milliseconds, it does not draw one subdivision. It uses a genetic algorithm or simulated annealing to draw *ten thousand* subdivisions, throws away the illegal ones, scores the remaining legal ones against the financial targets, and hands the developer the top three layouts that maximize profit while mathematically guaranteeing legal compliance.

This is **algorithmic real estate**.

#### 13.2.1 The Concrete Workflow

1. The developer uploads the site boundary, the topographical survey, and the project brief (target unit count, target unit mix, target ROI, target completion).
2. Python ingests these into the vault under a project-specific namespace.
3. The site is voxelized; setbacks and easements are subtracted; the buildable envelope is generated.
4. The optimizer (NSGA-II or simulated annealing) generates candidate subdivision layouts: road network, lot subdivision, building placement per lot.
5. Each candidate is verified against the legal AST set (`unsat` triggers discard) and scored against the business fitness functions.
6. The Pareto frontier is extracted. The top three (or top-k) are presented to the developer.
7. The developer picks one. Vitruvius then drills into Resolution 2 and Resolution 3 of the chosen subdivision (per-building, per-floor) for further design.

### 13.3 The Bi-Directional Cascade in Practice

The two use cases are not separate in the Vitruvius philosophy. They are different *resolutions* of the same fractal model. A change at the macro scale (the developer raises the target unit count from 120 to 130) propagates through the resolutions:

- New unit count → new average lot size (smaller) → new building footprint per lot → new structural grid → new MEP shaft sizing → new per-floor routing.
- And in reverse: a constraint failure at the micro scale (MEP cannot fit) triggers a pressure signal back to the macro scale (drop the unit count to 118).

This is the **living, breathing mathematical organism** the source files describe. The codebase AI should design the cross-resolution communication channel as a first-class concern, not an afterthought.

### 13.4 Use Cases Beyond the Two

The two named use cases are starting points. The same engine, with no architectural changes, supports:

- **Renovation and adaptive reuse.** Load an existing IFC, apply current code, identify gaps, propose minimum-intervention compliance solutions.
- **Insurance and underwriting.** Compute risk-adjusted exposure for a portfolio of buildings.
- **Disaster simulation.** Apply seismic or wind loads to existing structures and predict damage.
- **Energy and carbon analysis.** Compute embodied carbon from the BOQ and operational carbon from envelope properties.
- **Regulatory authoring.** Run proposed code amendments retroactively against a portfolio to estimate compliance impact.
- **Education.** Generate exam-relevant scenarios with controllable difficulty (the SlateCamp connection).
- **Research.** Provide a deterministic computational testbed for AEC research projects.

The breadth of downstream use cases is a function of how cleanly the core architecture preserves the separation of physics, law, and orchestration.

---

## 14. Open Research Questions and Risks

### 14.1 Architectural Risks

- **ECS persistence and undo.** `bevy_ecs` is in-memory. Persisting state to RocksDB and supporting undo/redo across sessions requires either event sourcing or full snapshotting. The right choice is unproven.
- **Cross-resolution consistency.** When the bi-directional feedback loop changes a macro decision, micro decisions made on the prior macro state may need to be invalidated. Detecting and gracefully handling this is unsolved.
- **Multi-user collaboration.** AEC projects involve many designers. Optimistic concurrency or operational transformation approaches need to be designed.
- **Wasm parity.** Some Rust crates (those depending on system threads, on file I/O, or on platform-specific features) do not compile to Wasm. The codebase AI should audit dependencies for Wasm compatibility from day one.

### 14.2 Mathematical and Numerical Risks

- **Floating-point precision in compositional ASTs.** Compositions of arithmetic ASTs can accumulate error. Interval arithmetic or symbolic manipulation may be needed for high-stakes computations.
- **Z3 performance on large constraint systems.** Z3 does not scale to billions of constraints. The architecture must keep individual queries small. The decomposition strategy is research-grade.
- **Continuous geometry in Z3.** Z3 has limited support for nonlinear real arithmetic and no native support for trigonometry. Geometric constraints must be discretized or reformulated.
- **Optimizer convergence.** Simulated annealing and NSGA-II are heuristic — they don't guarantee global optima. For high-stakes design decisions, this matters. Hybrid approaches (heuristic to find candidates, MILP to verify optimality on small subproblems) deserve study.

### 14.3 Knowledge Vault Risks

- **LLM extraction reliability.** Even with constrained generation, the LLM can mis-extract a rule. Sample auditing and golden-rule test suites are mandatory but the failure rate at scale is unknown.
- **Rule conflicts.** Two valid rules from different sources may genuinely conflict. The governance layer needs explicit conflict-resolution semantics.
- **Update propagation.** When a code is amended, every Vitruvius deployment globally needs the update. The distribution mechanism is undesigned.
- **Version conflicts in temporality.** A long-lived project may span multiple code amendments. Which version applies — the version at design time, the version at permit submission, the version at construction, or the version at occupancy? Different jurisdictions answer differently. Vitruvius must support all of them.

### 14.4 Performance Risks

- **Wasm threading on Safari and mobile.** Threading support varies. Single-threaded fallback paths are mandatory.
- **Memory limits in the browser.** The 4 GB Wasm32 limit constrains in-browser working set. Streaming and out-of-core approaches may be needed for large projects.
- **GPU acceleration.** Vitruvius is CPU-bound by design (deterministic, no shaders). For some kernels (voxel CSG, ray casting), GPU acceleration could be transformative. The Wasm WebGPU story is maturing; this is a future research direction.
- **Mobile hardware.** The deployment target includes mid-range Android phones. Voxel resolutions and BVH sizes must be tunable downward for these devices.

### 14.5 IFC and Interoperability Risks

- **Round-trip fidelity.** IFC import → Vitruvius → IFC export may lose metadata or introduce geometric drift. Test suites against canonical IFC files are needed.
- **Centerline extraction.** Extracting centerlines from arbitrary IFC geometry is a research problem in its own right. Heuristics will fail on edge cases.
- **IFC versioning.** Supporting IFC 2x3, 4, 4.3, and eventually 5 is a moving target.

### 14.6 Legal and Governance Risks

- **Liability for incorrect compliance.** If Vitruvius certifies a building compliant and the certification is wrong, who is liable? The PE/Architect of record, presumably — but the provenance of the error matters.
- **Regulatory acceptance.** Will Filipino building officials accept Vitruvius-generated permit packages? The DOH-style regulatory acceptance pipeline may be needed.
- **Cross-jurisdictional licensing.** Practicing architecture in jurisdictions without a license is illegal. Vitruvius outputs may need to be tagged with the licensed professional who certified them.

### 14.7 Research Directions Worth Pursuing

- **Differentiable AEC.** Recasting compliance and cost as differentiable losses enables gradient-based optimization. Some AEC academic work explores this; production tools do not.
- **Reinforcement learning for layout.** RL-based level generation in games (e.g. ProcGen) suggests a path for AEC layout that complements WFC.
- **Neural surrogate models for FEA.** Train a neural net on FEA outputs; use it as a fast approximator during optimization, with periodic FEA verification.
- **Probabilistic compliance.** Some rules are inherently probabilistic (seismic risk, fire risk). Treating them as soft constraints with confidence intervals is more honest than treating them as hard.
- **Formal verification of the kernel itself.** Kani, Prusti, and Creusot are bringing formal verification to Rust. The Vitruvius spatial kernels are exactly the kind of code that benefits from formal proof.

### 14.8 Comparable Projects and Competitive Landscape

The codebase AI should know what other tools occupy adjacent territory:

- **Hypar** — computational AEC platform, function-as-a-service model. Closest in philosophy to Vitruvius.
- **Spacemaker (now Autodesk Forma)** — site planning and urban design with multi-objective optimization. Direct competitor to Use Case 2.
- **TestFit** — real-estate yield calculation with rapid feasibility studies. Direct competitor to Use Case 2 at smaller scale.
- **Digital Blue Foam** — generative urban design with sustainability optimization.
- **Speckle** — open-source AEC interoperability layer. Complementary, not competitive.
- **Solibri Model Checker** — IFC-based code checking. Competitor on the compliance angle but rule-author-driven rather than law-driven.
- **Ladybug Tools** — environmental analysis (daylighting, energy, comfort). Complementary; could integrate.
- **Topologic** — non-manifold topology library. Complementary; provides geometric primitives.
- **AECdeltas** — IFC diff and version management. Complementary.
- **Speckle Sharp** — .NET Speckle implementation. Adjacent.
- **ShapeDiver** — parametric Grasshopper definitions in the cloud. Different paradigm but overlapping use cases.

The novelty of Vitruvius relative to all of these is the combination of:

- A game-grade ECS with cache-conscious data layout.
- Z3-based formal verification.
- Versioned, jurisdictional rule packages with temporal queries.
- The Compound AI System pattern with tool-calling LLM.
- Wasm-deployable headless kernel.

No single competitor has all five.

---

## 15. Glossary

**A\* (A-Star) Pathfinding** — Best-first heuristic graph search algorithm; finds optimal paths in the smallest node-expansion count of any guaranteed-optimal algorithm.

**AABB (Axis-Aligned Bounding Box)** — A 3D box aligned to the world axes, used as a coarse spatial extent for broad-phase collision detection.

**AEC** — Architecture, Engineering, and Construction. The industry vertical Vitruvius targets.

**Agentic Bridge** — The pattern by which a natural-language LLM dispatches to deterministic computation via structured tool calls.

**AMBF** — Allowable Maximum Building Footprint. Philippine building code term for the largest footprint a structure may occupy on a lot.

**Append-Only Temporal Graph** — A data store that never deletes; new versions of facts are appended with effective-date metadata, enabling time-travel queries.

**Archetype (in ECS)** — A grouping of entities with identical component composition, stored together in contiguous arrays for cache efficiency.

**AST (Abstract Syntax Tree)** — A tree representation of the syntactic structure of source code or a formula, used in Vitruvius to encode legal rules as machine-executable expressions.

**BHL** — Building Height Limit. Philippine building code term.

**Bilinear Interpolation** — A method for sampling a value at an arbitrary 2D point given values at the four nearest grid corners; used for heightmap lookup.

**BIM (Building Information Modeling)** — A workflow centered on shared 3D models with embedded metadata.

**Boolean Subtraction (CSG)** — One of the constructive solid geometry operations: the set difference of two solids, used in Vitruvius to "carve" the buildable envelope.

**Boundary Translation Protocol** — The Vitruvius pattern of keeping foreign data formats (especially IFC) at the I/O boundary while the internal representation remains pure mathematical primitives.

**B-Rep (Boundary Representation)** — A solid-modeling representation defining a solid by its boundary surfaces; the standard CAD representation, contrasted with mesh and voxel.

**BVH (Bounding Volume Hierarchy)** — A tree of nested bounding volumes used as a spatial index for fast collision and ray queries.

**Capsule (geometric)** — A geometric primitive consisting of a line segment with a uniform radius around it; the swept volume of a sphere along a line. Vitruvius's primary representation for pipes, cables, and other linear elements.

**Catastrophic Cancellation** — Loss of precision in floating-point subtraction of nearly-equal numbers; the AEC consequence is that pipes register at incorrect dimensions.

**ClashEvent** — In the Vitruvius ECS, an event signaling that two entities' clearance capsules overlap.

**Combinatorial Explosion** — The phenomenon where the number of possible configurations grows exponentially with system size; the central computational challenge in multi-disciplinary AEC coordination.

**Compound AI System** — An AI system composed of multiple specialized components (LLM, deterministic kernel, knowledge base, solver) rather than a single model.

**Constraint Satisfaction Problem (CSP)** — A computational problem framed as finding values for variables that satisfy a given set of constraints.

**Cut and Fill** — Earthwork operations: cut is digging soil out, fill is dumping soil in. Vitruvius's optimizer balances them against foundation costs.

**Datalog** — A declarative logic-programming language well-suited to expressing rules over relations and graphs.

**DomainDiscipline** — In the Vitruvius ECS, an enum component identifying which engineering discipline an entity belongs to (Arch, Struct, HVAC, Plumbing, Elec).

**ECS (Entity-Component-System)** — A data-oriented architectural pattern from game development: entities are IDs, components are pure data, systems are functions iterating over component arrays.

**EPA (Expanding Polytope Algorithm)** — Algorithm for computing the exact penetration depth and minimum translation vector between two convex shapes; the natural follow-up to GJK.

**Euler-Bernoulli Beam Theory** — Classical beam-bending theory; the basis of the Vitruvius structural kernel for typical spans.

**FAR (Floor Area Ratio)** — The ratio of total enclosed floor area to lot area; a fundamental zoning constraint.

**FEA (Finite Element Analysis)** — Numerical method for solving engineering problems by discretizing the domain into small elements; used for stress, heat, fluid flow analysis.

**FlatBuffers** — A zero-copy, schema-based binary serialization format from Google. Vitruvius's preferred internal binary format.

**Floating Origin Point** — A coordinate-system technique that dynamically re-centers the world origin near the area of current interest to preserve floating-point precision.

**Fractal ECS** — The Vitruvius design where the same ECS data structures and algorithms operate at every scale (subdivision, building, floor, pipe) without scale-specific code.

**Function Calling (Tool Use)** — The LLM pattern of emitting structured JSON describing a tool to invoke rather than answering directly.

**GJK (Gilbert-Johnson-Keerthi)** — Algorithm for fast convex collision detection; among the fastest known.

**Hazen-Williams Equation** — Empirical formula for water flow head loss in pipes; the basis of the Vitruvius plumbing kernel.

**Heightmap** — A 2.5D representation of terrain as a 2D grid of elevation values; the Vitruvius topography format.

**Hierarchical Lazy Evaluation** — The strategy of solving a project in cascading resolutions (macro envelope → core/shell → micro routing) to manage compute and memory.

**Hierarchy of Precedence** — The ordering of disciplines (Architecture → Structural → HVAC → Plumbing → Electrical) that dictates which yields to which during clash resolution.

**IFC (Industry Foundation Classes)** — The buildingSMART open standard for BIM data interchange; deeply nested, OOP-flavored.

**IfcOntology** — In the Vitruvius ECS, a lightweight component holding the IFC class label for an entity, used only at export.

**Jump Point Search (JPS)** — A pathfinding optimization that skips over symmetric paths on uniform-cost grids, often orders of magnitude faster than vanilla A*.

**Linear Octree** — An octree representation where the tree is stored as a sorted array of Morton-coded centroids rather than as explicit node objects.

**Loose Octree** — An octree variant where nodes may extend beyond their canonical bounds, reducing the cost of updates when entities move.

**MEP (Mechanical, Electrical, Plumbing)** — The collective term for building services systems.

**Monte Carlo Tree Search (MCTS)** — A search algorithm that builds a tree of decisions and balances exploration with exploitation; used for combinatorial optimization.

**Morton Code (Z-Order Curve)** — A space-filling curve mapping multi-dimensional coordinates to a single integer that preserves spatial locality; enables 1D sorting for 2D/3D proximity queries.

**Multi-Objective Constraint Solver** — A solver that handles multiple competing objectives subject to constraints; produces a Pareto frontier rather than a single answer.

**Negotiation Protocol** — The Vitruvius automated clash resolution sequence: when one discipline fails to find a feasible solution, the orchestrator asks adjacent disciplines for incremental concessions until the conflict resolves or escalates.

**NSCP** — National Structural Code of the Philippines.

**NSGA-II** — Non-dominated Sorting Genetic Algorithm II; the dominant Pareto multi-objective optimization algorithm.

**OCL (Object Constraint Language)** — A formal language for expressing constraints in UML/MOF models; used in some IFC validation contexts.

**Octree** — A tree data structure for 3D space, where each internal node has eight children corresponding to the eight octants of its bounding region.

**Pareto Front (Pareto Frontier)** — The set of optimization solutions where no objective can be improved without worsening another.

**PD 1096** — Presidential Decree 1096, the National Building Code of the Philippines (1977) and its IRR.

**PEC** — Philippine Electrical Code.

**Petgraph** — The dominant Rust graph library; used in Vitruvius for MEP topology, egress graphs, and rule dependencies.

**PSO** — Percentage of Site Occupancy. Philippine zoning term.

**RA 9514** — Republic Act 9514, the Fire Code of the Philippines (2008).

**RA 9266** — Republic Act 9266, the Architecture Act of 2004; defines the legal scope of architectural practice in the Philippines.

**Raycasting** — Computing the intersection of a ray with geometry; in Vitruvius, used to project building footprints onto the heightmap to determine ground elevation.

**Retroactive Compliance Audit** — A query against the Vitruvius temporal vault asking whether a building was code-compliant at a historical date.

**RocksDB** — A high-performance embedded key-value store from Facebook (Meta); the Vitruvius knowledge vault.

**SHACL** — Shapes Constraint Language, a W3C standard for expressing constraints over RDF graphs.

**SIMD (Single Instruction, Multiple Data)** — A CPU feature processing multiple data elements per instruction; available in Wasm via the `simd128` feature.

**Simulated Annealing (SA)** — A stochastic optimization algorithm that mimics metallurgical cooling, accepting worse solutions early and converging to refinements over time.

**Sled** — A pure-Rust embedded key-value store; a Wasm-compatible alternative to RocksDB.

**SMT (Satisfiability Modulo Theories)** — A class of constraint satisfaction problem combining Boolean satisfiability with theories like arithmetic, arrays, bit-vectors. Z3 is an SMT solver.

**Steiner Tree** — The minimum-total-length network connecting a set of terminal nodes, allowing intermediate Steiner points; the mathematical structure of optimal MEP routing.

**Structure of Arrays (SoA)** — A data layout where each field of a record is stored in its own contiguous array, contrasted with Array of Structures (AoS); preferred for cache-friendly iteration.

**TGFA** — Total Gross Floor Area. Philippine building code term.

**TIN (Triangulated Irregular Network)** — A mesh-based representation of terrain; contrasted with the heightmap representation Vitruvius uses.

**TOSL** — Total Open Space within a Lot. Philippine zoning term.

**Vector Abstraction** — The Vitruvius representation of spatial elements as 1D line segments with radii (capsules), avoiding the O(N²) cost of mesh-vs-mesh collision detection.

**VectorSegment** — In the Vitruvius ECS, the component carrying a line segment's start and end coordinates.

**Voxel** — A 3D pixel; a discrete cubic cell in a 3D grid. Vitruvius uses 10 cm voxels by default.

**Wasm (WebAssembly)** — A binary instruction format for stack-based virtual machines, designed as a portable compilation target. Vitruvius's deployment format for the browser.

**WFC (Wave Function Collapse)** — A constraint-propagation algorithm originally for procedural texture generation, adapted for AEC layout.

**Z3** — Microsoft Research's SMT solver; the Vitruvius theorem prover.

**Z-Order Curve** — See Morton Code.

---

## 16. References

### 16.1 Source Files Consolidated Here

- `Entity-Component-System__ECS__architecture.md` (uploaded)
- `Hardcoding_the_AEC_Ontology.md` (uploaded)
- `Spatial_Comprehension.md` (uploaded)

### 16.2 Rust Crates (canonical pages on docs.rs and crates.io)

- `bevy_ecs` — https://docs.rs/bevy_ecs
- `hecs` — https://docs.rs/hecs
- `flecs_ecs` — https://docs.rs/flecs_ecs
- `parry3d` — https://docs.rs/parry3d
- `rapier3d` — https://docs.rs/rapier3d
- `truck` — https://docs.rs/truck-modeling
- `nalgebra` — https://docs.rs/nalgebra
- `glam` — https://docs.rs/glam
- `ndarray` — https://docs.rs/ndarray
- `petgraph` — https://docs.rs/petgraph
- `pathfinding` — https://docs.rs/pathfinding
- `wfc` — https://docs.rs/wfc
- `argmin` — https://docs.rs/argmin
- `oxigen` — https://docs.rs/oxigen
- `genevo` — https://docs.rs/genevo
- `good_lp` — https://docs.rs/good_lp
- `highs` — https://docs.rs/highs
- `coin_cbc` — https://docs.rs/coin_cbc
- `z3` — https://docs.rs/z3
- `crepe` — https://docs.rs/crepe
- `ascent` — https://docs.rs/ascent
- `differential-dataflow` — https://docs.rs/differential-dataflow
- `morton-encoding` — https://docs.rs/morton-encoding
- `lindel` — https://docs.rs/lindel
- `building_blocks` — https://github.com/bonsairobo/building-blocks
- `flatbuffers` — https://docs.rs/flatbuffers
- `capnp` — https://docs.rs/capnp
- `prost` (Protocol Buffers) — https://docs.rs/prost
- `arrow` — https://docs.rs/arrow
- `rust-rocksdb` — https://docs.rs/rocksdb
- `sled` — https://docs.rs/sled
- `wasm-bindgen` — https://docs.rs/wasm-bindgen
- `wasm-pack` — https://rustwasm.github.io/wasm-pack/
- `tracing` — https://docs.rs/tracing
- `criterion` — https://docs.rs/criterion
- `ode_solvers` — https://docs.rs/ode_solvers
- `peroxide` — https://docs.rs/peroxide
- `dxf` — https://docs.rs/dxf
- `las` — https://docs.rs/las

### 16.3 IFC and AEC Tooling

- IfcOpenShell — https://ifcopenshell.org/
- web-ifc — https://github.com/ThatOpen/engine_web-ifc
- bonsai-bim (Blender BIM) — https://bonsaibim.org/
- buildingSMART IFC documentation — https://standards.buildingsmart.org/IFC/
- Speckle — https://speckle.systems/
- Hypar — https://hypar.io/
- Topologic — https://topologic.app/
- TestFit — https://testfit.io/
- Ladybug Tools — https://www.ladybug.tools/
- Solibri — https://www.solibri.com/

### 16.4 Algorithms and Theoretical Background

- Christer Ericson, *Real-Time Collision Detection* (Morgan Kaufmann, 2005). Definitive reference for capsule, AABB, BVH, GJK math.
- David Eberly, *Geometric Tools for Computer Graphics*. Companion reference.
- Microsoft Research Z3 documentation — https://microsoft.github.io/z3guide/
- CVC5 — https://cvc5.github.io/
- Maxim Gumin, Wave Function Collapse original repository — https://github.com/mxgmn/WaveFunctionCollapse
- NSGA-II original paper — Deb et al., *A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II*, IEEE Transactions on Evolutionary Computation, 2002.
- ASHRAE Handbook (multi-volume) for HVAC calculations.
- ACI 318 for concrete structural design (used in many Philippine reference contexts).

### 16.5 Philippine Building Codes

- PD 1096 (National Building Code) text and IRR — Department of Public Works and Highways resources.
- RA 9514 (Fire Code of the Philippines) — Bureau of Fire Protection.
- NSCP 2015 / NSCP 2024 — Association of Structural Engineers of the Philippines (purchase required).
- PEC 2017 — Institute of Integrated Electrical Engineers of the Philippines.
- BP 344 (Accessibility Law) — National Council on Disability Affairs.
- PD 957 and BP 220 (Subdivision and socialized housing) — HLURB/DHSUD references.
- PD 1067 (Water Code) — National Water Resources Board.

### 16.6 LLM Tool Calling and Constrained Generation

- Anthropic tool use documentation — https://docs.claude.com/en/docs/build-with-claude/tool-use
- OpenAI structured outputs — https://platform.openai.com/docs/guides/structured-outputs
- Google Gemini function calling — https://ai.google.dev/docs/function_calling
- Outlines — https://github.com/dottxt-ai/outlines
- llama.cpp grammar reference — https://github.com/ggerganov/llama.cpp/blob/master/grammars/README.md

### 16.7 WebAssembly

- WebAssembly specification — https://webassembly.github.io/spec/
- Rust and WebAssembly book — https://rustwasm.github.io/docs/book/
- wasm-bindgen guide — https://rustwasm.github.io/docs/wasm-bindgen/
- WebAssembly SIMD proposal — https://github.com/WebAssembly/simd

### 16.8 Voxel and Spatial Storage

- OpenVDB — https://www.openvdb.org/
- Building Blocks discussion archive — https://github.com/bonsairobo/building-blocks
- Sparse Voxel Octree literature — start with Laine & Karras, *Efficient Sparse Voxel Octrees* (2010).

---

## End of Research Document

This document is intended to be read in full by the codebase AI before any Vitruvius implementation work is undertaken. Subsequent implementation plans should reference specific sections by number and should derive their work from the design space surveyed here. The next logical artifact in the development pipeline is a Phase 00 trigger file under the Standard Execution Loop, scoping the first concrete implementation task — likely the Rust ECS scaffolding with the core component vocabulary (`VectorSegment`, `ClearanceCapsule`, `AABB`, `DomainDiscipline`, `EntityLink`).

