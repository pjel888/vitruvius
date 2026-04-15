# Rust Kernel Development Protocol

## Purpose
This protocol defines the full lifecycle for designing, implementing, testing, benchmarking, reviewing, and validating any Rust kernel in Vitruvius.

## Scope
This protocol applies to:
- geometry kernels
- ECS systems
- collision routines
- voxel or grid kernels
- graph kernels if implemented in Rust
- engineering solvers
- numerical helper modules
- Wasm-exported compute routines
- PyO3-exposed compute routines

## Definition of a Rust Kernel
A Rust kernel is a bounded computation unit with:
- clear inputs
- clear outputs
- deterministic behavior
- performance significance or numerical significance
- explicit architectural purpose

Examples:
- segment-segment distance
- capsule clash check
- broadphase AABB update
- pathfinding inner loop
- beam deflection evaluator
- voxel carve operation
- local-frame transform utility

## Protocol Overview
Every Rust kernel must pass through these stages:

1. Kernel Intent Definition
2. Data Contract Definition
3. Numerical Risk Analysis
4. Architecture Boundary Check
5. Test Design
6. Benchmark Design
7. Controlled Implementation
8. Static Quality Gates
9. Dynamic Validation
10. Documentation and State Update

---

## Stage 1 — Kernel Intent Definition

### Required Questions
Before coding, answer:
- What exact problem does this kernel solve?
- Why must it exist in Rust?
- Why is Python not sufficient here?
- Is this compute-bound, latency-sensitive, memory-sensitive, or all three?
- Is the kernel deterministic?
- Is this part of a hot loop?
- Is this a core engine primitive or a supporting utility?

### Required Output
Document:
- kernel name
- rationale
- owning subsystem
- callers
- frequency of execution
- expected scale
- failure impact

### Example
A capsule clash routine might be justified because it is:
- called millions of times in iterative routing
- numerically sensitive
- performance-critical
- reused by multiple higher-level systems

---

## Stage 2 — Data Contract Definition

### Required Fields
For every kernel define:
- input types
- output types
- units
- coordinate frame
- ownership model
- allowed ranges
- invalid states
- tolerance policy
- determinism expectations

### Mandatory Questions
- Are coordinates absolute or local?
- Are values stored as `f64` or `f32` and why?
- Are zero-length inputs allowed?
- Are NaN and infinity prohibited?
- What tolerance is acceptable near threshold comparisons?
- Are inputs normalized or raw?
- Does output preserve ordering, or is it symmetric?

### Rule
If the data contract is not written, code must not start.

---

## Stage 3 — Numerical Risk Analysis

### Identify Risks
For every kernel, identify possible:
- catastrophic cancellation
- tolerance drift
- threshold instability
- overflow / underflow
- degeneracy
- branching anomalies
- precision loss from coordinate magnitude
- nondeterminism from iteration ordering

### Required for Geometry
Geometry kernels must analyze:
- zero-length segments
- nearly parallel segments
- coincident segments
- overlapping capsules
- very large coordinates
- very small deltas
- boundary values exactly at collision threshold

### Required Decision
Choose and document:
- exact numeric types
- tolerance constants
- comparison strategy
- local-frame transformation needs

---

## Stage 4 — Architecture Boundary Check

### Kernel Must Stay in Rust Only If
At least one is true:
- performance critical
- memory layout critical
- numerical tight loop
- reused by many subsystems
- Wasm compute primitive
- PyO3 compute primitive

### Kernel Must Stay Out of Rust If
Any of the following are the main concern:
- business logic
- policy logic
- legal interpretation
- orchestration logic
- LLM routing
- configuration flow
- UI behavior

### Boundary Questions
- Is Rust doing only computation?
- Is Python retaining orchestration?
- Is the knowledge layer still outside Rust?
- Is the tool-calling layer still outside Rust?

---

## Stage 5 — Test Design

### Test Classes
Each kernel must define:

#### A. Contract Tests
- type and shape correctness
- legal input acceptance
- illegal input rejection

#### B. Deterministic Unit Tests
- canonical examples
- known expected outputs
- threshold cases

#### C. Edge-Case Tests
- degenerate input
- parallel or identical geometry
- zero-length or near-zero length values
- extremely large and extremely small values

#### D. Regression Tests
- protect previously fixed bugs
- preserve decisions around tolerances

#### E. Property-Based Tests
- symmetry
- invariants
- monotonicity where applicable
- boundedness
- idempotence where applicable

#### F. Differential Tests
- compare Rust implementation against slow reference implementation in Python or a mathematically straightforward Rust reference

### Rule
No kernel is approved without a test map.

---

## Stage 6 — Benchmark Design

### Required for Hot Paths
For any performance-sensitive kernel:
- define benchmark target
- define representative workloads
- define data sizes
- define baseline
- define regression threshold

### Benchmark Questions
- what is the expected throughput?
- what is the maximum acceptable slowdown?
- what is the memory target?
- what data distribution is realistic?
- what worst-case pattern should be included?

### Benchmark Types
- microbenchmarks for primitives
- mesobenchmarks for subsystem loops
- regression benchmarks against previous versions

### Rule
Performance claims without a benchmark are invalid.

---

## Stage 7 — Controlled Implementation

### Mandatory Implementation Sequence
1. write the simplest correct reference version
2. prove behavior with tests
3. optimize incrementally
4. rerun tests after each optimization
5. benchmark each meaningful optimization
6. document what changed and why

### Coding Rules
- keep functions small
- keep hot-path data minimal
- avoid unnecessary allocation
- avoid cloning large values
- separate atomic components instead of creating god structs
- avoid hidden globals
- avoid cleverness without measurable gain

### Unsafe Rule
Unsafe Rust is forbidden unless:
- explicitly justified
- isolated
- heavily documented
- surrounded by tests
- reviewed manually

---

## Stage 8 — Static Quality Gates

### Mandatory Commands
At minimum:
- `cargo fmt --all`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `cargo test --all-targets`
- `cargo doc` if public APIs changed

### Optional But Recommended
- `cargo audit`
- `cargo udeps`
- `cargo machete`
- `cargo deny`

### Failure Rule
Any warning treated as a risk signal, not cosmetic noise.

---

## Stage 9 — Dynamic Validation

### Validation Must Include
- test result summary
- property-test summary
- benchmark summary
- edge-case summary
- architecture compliance summary
- precision risk summary
- known limitations

### Required Question
Can this kernel fail silently in a way that matters to compliance, routing, or geometry?

If yes:
- contain it
- expose it
- or reject it

---

## Stage 10 — Documentation and State Update

### Update Required
- implementation plan status
- validation report
- state / milestone tracker
- decision log if architecture changed
- docstrings or module docs if API changed

### Validation Report Must State
- what was implemented
- what was proven
- what was not proven
- what remains risky
- what benchmark says
- what future work is deferred

---

## Mandatory Kernel Record Template

### Kernel
- Name:
- Subsystem:
- Owner:
- Status:

### Intent
- Problem solved:
- Why Rust:
- Why now:
- Call frequency:

### Data Contract
- Inputs:
- Outputs:
- Units:
- Coordinate frame:
- Numeric type:
- Invalid states:
- Tolerances:

### Risks
- Precision risks:
- Degeneracy risks:
- Performance risks:
- Architecture risks:

### Test Plan
- Contract tests:
- Unit tests:
- Edge cases:
- Property tests:
- Differential tests:

### Benchmark Plan
- Metric:
- Baseline:
- Threshold:
- Datasets:

### Completion
- Static checks:
- Dynamic checks:
- Validation report path:

## Final Rule
Do not optimize what is not yet proven correct.
Do not ship what is not yet proven stable.
