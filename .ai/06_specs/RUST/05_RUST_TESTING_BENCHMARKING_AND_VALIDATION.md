# Rust Testing, Benchmarking, and Validation

## Purpose
This document defines the mandatory validation regime for Rust work in Vitruvius.

## Principle
Rust code is not trusted because it compiles.
Rust code is trusted only after it survives structured validation.

---

## Validation Pyramid

### Layer 1 — Unit Tests
Prove canonical cases.

### Layer 2 — Edge-Case Tests
Prove difficult or pathological cases.

### Layer 3 — Property-Based Tests
Prove invariants across wide input spaces.

### Layer 4 — Differential Tests
Prove agreement with a slower reference.

### Layer 5 — Benchmarks
Prove acceptable performance.

### Layer 6 — Validation Report
Prove honest interpretation of results.

---

## Unit Test Requirements

Every non-trivial kernel must have:
- canonical happy-path tests
- threshold tests
- deterministic repeatability tests

### Examples
For segment distance:
- intersecting segments
- separated perpendicular segments
- skew segments
- identical segments
- endpoint-touching cases

---

## Edge-Case Test Requirements

### Required Categories
- zero-length inputs
- nearly parallel inputs
- coincident inputs
- extremely large coordinates
- extremely small distances
- near-threshold values
- invalid numeric values where relevant

### Rule
If an edge case is known in design but not tested, the kernel is incomplete.

---

## Property-Based Testing

### Required for
- reusable geometry primitives
- routing-cost utilities
- vector math helpers
- transforms
- collision predicates where invariants are known

### Useful Properties
- symmetry
- idempotence
- non-negativity
- boundedness
- monotonicity
- invariance under translation where appropriate
- determinism under repeated execution

### Recommended Tool
- `proptest`

---

## Differential Testing

### Purpose
Catch optimized-but-wrong implementations.

### Pattern
- reference implementation
- optimized implementation
- random input generator
- compare results within defined tolerance

### Use Cases
- collision routines
- distance functions
- transform helpers
- lightweight solver components

### Rule
Tolerance must be documented, not guessed ad hoc in test code.

---

## Benchmarking

### Benchmark Required For
- any hot-loop primitive
- any ECS system loop
- any routing primitive
- any voxel or spatial index update routine
- any function cited as performance-sensitive

### Recommended Tool
- `criterion`

### Benchmark Categories
- microbenchmark
- subsystem benchmark
- regression benchmark

### Benchmark Inputs
Benchmarks must include:
- representative data
- worst-case data
- edge-density data
- threshold-heavy data when relevant

### Benchmark Report Must State
- throughput or latency
- hardware context
- baseline version
- new version
- regression or improvement percentage
- allocation notes if relevant

---

## Performance Gates

### Example Gate Questions
- Did hot-path latency regress by more than 5%?
- Did allocation count increase?
- Did cache locality likely worsen due to data-shape changes?
- Did benchmark variance increase suspiciously?

### Failure Rule
A performance regression must be explained, accepted explicitly, or fixed.

---

## Static Checks

### Mandatory
- `cargo fmt --all`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `cargo test --all-targets`

### Recommended
- `cargo audit`
- `cargo deny`
- `cargo udeps`

---

## Validation Report Template

### Summary
- task:
- date:
- crate/module:
- reviewer:
- status:

### Test Results
- unit tests:
- edge-case tests:
- property tests:
- differential tests:

### Benchmark Results
- benchmark file:
- baseline:
- current:
- regression threshold:
- outcome:

### Risk Review
- precision risk:
- determinism risk:
- architecture risk:
- known limitations:

### Final Judgment
- accepted / rejected / accepted with caveats

---

## Minimum Acceptance Criteria

A Rust change is acceptable only if:
- all mandatory checks pass
- no unexplained benchmark regression remains
- all known edge cases for the kernel class are tested
- precision policy is explicit
- validation report exists

## Final Rule
A green test suite is necessary but not sufficient.
Performance and correctness must both be proven.
