# Rust Safeguards and Failure Containment

## Purpose
This document defines the safeguards required to contain mistakes, regressions, incorrect assumptions, and silent failures in Rust work.

## Philosophy
Rust mistakes are not dangerous because they fail loudly.
They are dangerous because they may compile, pass shallow tests, and still be wrong.

Therefore the goal is not only to detect errors.
The goal is to stop wrong Rust from surviving.

## Safeguard Layers
1. Scope restrictions
2. Data-contract enforcement
3. Test fences
4. Differential validation
5. Performance gates
6. Architecture gates
7. Review gates
8. Release gates

---

## Layer 1 — Scope Restrictions

### Allowed Rust Work
- computational kernels
- ECS systems
- geometry utilities
- deterministic numerical routines
- Wasm-exportable compute code
- PyO3-exposed compute primitives
- high-frequency graph or voxel routines when justified

### Restricted Rust Work
- business rules
- legal meaning inference
- roadmap or task orchestration
- open-ended feature logic
- broad application state management

### High-Risk Work Requiring Manual Approval
- `unsafe`
- custom allocators
- manual SIMD intrinsics
- manual threading or lock design
- low-level FFI memory tricks
- cross-crate lifetime-heavy abstractions

---

## Layer 2 — Data-Contract Enforcement

### Mandatory Rules
- no undocumented units
- no undocumented coordinate frame
- no undocumented tolerances
- no NaN acceptance unless explicitly designed
- no unchecked infinity propagation
- no ambiguous threshold comparisons

### Containment Pattern
Every kernel boundary should reject or sanitize invalid data before hot-loop execution.

### Recommended Helpers
Create shared validators for:
- finite floats
- non-negative radii
- valid segment length constraints
- allowed coordinate ranges
- tolerance comparisons

---

## Layer 3 — Test Fences

### Golden Tests
Protect canonical examples with fixed expected outputs.

### Regression Tests
Every bug fix must produce a regression test.

### Property Tests
Use `proptest` or equivalent for invariants.

### Stress Tests
Test dense, repeated, and adversarial geometries.

### Negative Tests
Ensure bad inputs fail clearly or are handled explicitly.

### Containment Rule
If a bug is found, a regression test must be added before the fix is considered complete.

---

## Layer 4 — Differential Validation

### Purpose
Optimized Rust must be checked against a slower, clearer reference implementation.

### Recommended Pattern
- Python reference version for math clarity
- Rust optimized version for production
- randomized differential test harness across large sample counts

### Suitable For
- distance functions
- collision routines
- routing scoring
- beam and fluid helper formulas
- voxel operations

### Rule
If optimized and reference versions disagree, treat optimized output as untrusted until explained.

---

## Layer 5 — Performance Gates

### Rule
Hot-path Rust must have benchmarks.

### Reject Conditions
- slower than baseline beyond threshold
- excess allocation introduced
- memory growth without justification
- unstable performance variance
- optimization justified only by theory, not measurement

### Recommended Tools
- `criterion`
- flamegraph tooling
- allocation counters where appropriate

### Benchmark Governance
Benchmarks should represent:
- realistic data
- worst-case data
- threshold-edge data

---

## Layer 6 — Architecture Gates

### Rust Must Not
- become the policy layer
- become the law layer
- become the source-of-truth state layer
- absorb orchestration from Python
- absorb tool-calling behavior from the LLM interface layer

### Architecture Review Questions
- Is this code pure computation?
- Is orchestration still in Python?
- Is data provenance still outside Rust?
- Is the knowledge vault still authoritative?
- Is Z3 still adjudicating logic outside Rust where intended?

---

## Layer 7 — Review Gates

### Self-Review
Codex must answer:
- what assumptions did I make?
- what can fail silently?
- what tolerance decisions did I make?
- what performance tradeoffs did I accept?
- what edge cases remain weak?

### Second-Pass Review
A second critique must attempt to break:
- geometry assumptions
- threshold logic
- ordering assumptions
- determinism assumptions
- boundary conditions

### Human Review Required For
- unsafe blocks
- public API boundary changes
- FFI or PyO3 changes
- benchmark regressions
- changes in numeric type or tolerance policy

---

## Layer 8 — Release Gates

No Rust change is releasable without:
- passing tests
- passing property tests where applicable
- benchmark evidence for hot paths
- updated docs
- updated validation report
- updated state docs

---

## Precision Safeguards

### Default Position
Use `f64` for world coordinates unless a documented local-frame optimization justifies `f32`.

### Required Checks
- coordinate magnitude analysis
- local-origin policy if needed
- threshold stability near equality
- exact behavior at `distance == radius_sum`

### Geometry-Specific Safeguards
- define EPSILON in one place
- document whether touching counts as clash
- test nearly parallel and coincident segments
- test zero-length segments explicitly

---

## ECS-Specific Safeguards

### Anti-Patterns Forbidden
- god components
- mixing unrelated fields into one hot-path struct
- querying metadata in spatial hot loops
- hidden heap allocations in system loops

### Required Design Questions
- which fields are used together?
- can this component be split?
- is this query loading irrelevant data into cache?
- is archetype layout helping or hurting here?

---

## FFI and Cross-Language Safeguards

### PyO3 Rules
- keep interfaces narrow
- validate inbound data before entering hot kernels
- convert to local Rust-native structures cleanly
- define ownership and lifetime expectations
- avoid exposing fragile internal abstractions directly

### Wasm Rules
- avoid JS serialization in hot paths
- keep binary or typed-array boundaries explicit
- keep deterministic compute separate from rendering concerns

---

## Logging and Diagnostics Safeguards

### Required
For complex kernels, expose debug or diagnostic hooks sufficient to inspect:
- input summary
- output summary
- threshold decisions
- benchmark metadata
- failure-mode classification

### Rule
Diagnostics must not pollute hot loops in release mode.

---

## Red-Line Conditions
Stop work immediately if:
- constraints are contradictory
- test oracle is unclear
- coordinate system is not explicit
- tolerance rules are not settled
- benchmark target is unknown
- architecture boundary is being violated

## Final Principle
Bad Rust should fail fast in validation, not survive into product behavior.
