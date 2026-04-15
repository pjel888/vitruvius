# Rust Architecture and Boundary Rules

## Purpose
This document defines what belongs in Rust and what does not belong in Rust within Vitruvius.

## Core Principle
Rust holds the physics.
Python holds the logic.
RocksDB holds the rules.
Z3 adjudicates formal constraints.
The LLM only translates.

This boundary is strategic, not stylistic.

---

## What Belongs in Rust

### Category A — Pure Compute
- geometry kernels
- collision checks
- spatial indexing
- ECS system execution
- routing primitives
- local numerical solvers
- deterministic simulation primitives
- high-frequency voxel operations
- performance-critical graph routines

### Category B — Tight Data Representation
- compact computational structs
- local frame transforms
- low-allocation data pipelines
- typed internal math primitives

### Category C — Exportable Compute Interfaces
- PyO3 bindings for compute kernels
- Wasm exports for compute kernels

---

## What Does Not Belong in Rust

### Forbidden or Strongly Discouraged
- legal interpretation
- policy orchestration
- project workflow logic
- audit-generation logic
- roadmap management
- free-form rule processing
- LLM prompt assembly
- user-facing response composition
- canonical truth governance logic unless specifically justified and designed

---

## Boundary Rules

### Rule 1 — Rust Must Be Deterministic by Default
Given the same validated inputs and the same rule compilation context, outputs should be stable and reproducible.

### Rule 2 — Rust Must Not Be the Source of Truth for Law
Rules may be compiled into constraints, but Rust must not own the original legal meaning.

### Rule 3 — Rust Must Not Become a Dumping Ground
Code is not moved to Rust merely because Python feels messy.

### Rule 4 — Rust APIs Must Stay Narrow
Only expose the minimum stable surface required.

### Rule 5 — Internal Representation Is Not Public Contract
Do not expose raw internal ECS or optimization machinery if a narrower DTO-like boundary can be used.

### Rule 6 — Keep Metadata Out of Hot Paths
Semantic labels, provenance, and descriptive metadata should not pollute hot loops unless absolutely required.

---

## Rust Boundary by Layer

### Python → Rust
Allowed to send:
- validated numeric inputs
- compiled constraints
- compact task requests
- local-frame geometry payloads
- route specifications

Not allowed to send:
- loosely structured dictionaries into hot paths
- ambiguous units
- semantically overloaded payloads
- half-validated user input

### Rust → Python
Should return:
- compact deterministic result structures
- explicit error states
- violation details where applicable
- machine-oriented results, not prose

Should not return:
- free-form legal conclusions
- user-facing narrative
- mixed diagnostic and production payloads without structure

---

## Dependency Rules

### Acceptable Dependency Criteria
A new Rust dependency must be:
- clearly justified
- maintained
- compatible with license requirements
- scoped to a real need
- likely to survive long-term

### Dependency Smells
Avoid adding crates because they:
- are fashionable
- slightly shorten code
- hide critical math behind black-box behavior without tests
- complicate Wasm or PyO3 compatibility

---

## Public API Rules

### Public APIs Must
- have doc comments
- define units and coordinate assumptions
- define error behavior
- remain stable unless intentionally versioned
- include example usage if exposed widely

### Public APIs Must Not
- leak experimental abstractions
- expose hidden invariants without documentation
- require callers to guess tolerance policy

---

## Numeric Type Policy

### Default
- `f64` for world coordinates and high-integrity geometry
- use `f32` only with documented local-frame and performance rationale
- integer indexing where grid logic demands it

### Any Numeric-Type Change Requires
- explicit rationale
- benchmark evidence
- precision-risk analysis
- regression testing

---

## Error Handling Policy

### Expected
- explicit result types where errors matter
- clearly classified errors
- no panic in normal operation paths

### Panic Permitted Only For
- impossible invariant violation in clearly internal contexts
- test-only code
- explicit prototype code marked non-production

---

## Concurrency Policy

### Default
Single-threaded correctness first.

### Parallelism Allowed Only After
- deterministic single-thread correctness is proven
- contention model is understood
- benchmark demonstrates real gain
- Wasm implications are considered

### Forbidden
- speculative concurrency without evidence
- clever threading in unstable modules

---

## Optimization Policy

### Sequence
1. correct
2. tested
3. benchmarked
4. optimized
5. benchmarked again

### Forbidden
- premature optimization without baseline
- opaque optimization that cannot be explained
- trading off correctness for speed without documented decision

---

## PyO3 Boundary Rules

### Required
- narrow function signatures
- structured input validation
- deterministic outputs
- minimal Python-visible surface
- explicit ownership expectations

### Avoid
- exposing complex lifetimes over FFI
- unnecessary conversion churn
- giant object graphs crossing the boundary

---

## Wasm Boundary Rules

### Required
- deterministic pure compute
- binary or typed-array interfaces where possible
- limited host assumptions
- explicit memory format

### Avoid
- JSON-heavy hot-loop communication
- mixing render concerns with compute concerns

---

## Final Rule
If a change blurs the Rust/Python/RocksDB/Z3 boundary, treat it as architecture work, not ordinary coding.
