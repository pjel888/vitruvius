# Vitruvius Performance Budget and Benchmark Policy

## Purpose
This document defines how Vitruvius treats performance requirements, benchmark evidence, and regression thresholds.

Performance in Vitruvius is not merely an implementation detail. It is part of the product promise. Therefore performance-sensitive work must be governed, measured, and defended explicitly.

## Core Principle
Do not claim speed.  
Measure it.

## Scope
This policy applies to:
- Rust kernels
- ECS systems
- geometry and routing routines
- large pipeline stages
- graph and embedding workloads
- OCR and parsing orchestration where latency or throughput matters
- caching layers
- memory-sensitive workflows
- Wasm compute modules
- M2 8GB hardening work

---

## Section 1 — Performance Budgets

A performance budget is an explicit limit or target for a task, module, or workflow.

### Budget Categories
- latency budget
- throughput budget
- memory budget
- allocation budget
- startup or warmup budget
- index or build-time budget

### Rule
No performance-sensitive task should proceed without knowing which budget matters.

---

## Section 2 — Budget Definition Requirements

For any performance-critical task, define:
- what metric matters
- why it matters
- baseline
- target or threshold
- hardware context
- representative workload
- worst-case workload
- acceptable regression threshold

### Example
A geometry kernel may define:
- metric: nanoseconds per call and memory allocations
- baseline: current main branch
- threshold: no regression > 5%
- target hardware: Apple M2 8GB
- workloads: sparse scene, dense scene, threshold-heavy scene

---

## Section 3 — Mandatory Benchmark Triggers

Benchmarks are mandatory when:
- a hot path changes
- a Rust kernel changes
- a data shape or component layout changes
- a memory-heavy workflow changes
- a caching strategy changes
- a pipeline acceleration claim is made
- a graph or retrieval path changes cost profile
- a feature flag alters runtime overhead
- a Wasm compute boundary changes

### Rule
If performance matters and code changed, benchmark.

---

## Section 4 — Benchmark Types

### Microbenchmark
Measures a tight primitive.
Examples:
- segment distance
- capsule clash check
- AABB update
- scoring function

### Mesobenchmark
Measures a subsystem loop.
Examples:
- route one floor’s MEP paths
- compile one rule batch
- process one canonicalization batch

### Workflow Benchmark
Measures a realistic pipeline or feature path.
Examples:
- run a conversion stage on a representative corpus
- perform one end-to-end review pass
- load and query a graph snapshot

### Rule
Use the smallest benchmark that can still answer the question honestly. Use larger workflow benchmarks when subsystem interaction is the risk.

---

## Section 5 — Hardware Policy

### Baseline Hardware
Vitruvius should maintain awareness of its constrained reference environment:
- Apple M2
- 8 GB unified memory

### Rule
Benchmarks should specify hardware context. If benchmark hardware differs materially from reference hardware, say so explicitly.

### Recommended Practice
When possible, track both:
- dev-machine measurements
- normalized or relative comparison against baseline branch

---

## Section 6 — Benchmark Inputs

Benchmarks must include representative data.

### Required Input Categories
- normal-case
- edge-density
- worst-case or adversarial
- threshold-heavy
- scale-appropriate realistic corpus when relevant

### Rule
Synthetic benchmarks that flatter the code but do not resemble real usage are weak evidence.

---

## Section 7 — Regression Policy

A regression is any material worsening in a tracked metric relative to baseline.

### Response Options
- fix it
- justify it explicitly
- defer it with recorded caveat
- reject the change

### Rule
No unexplained regression should be silently accepted.

### Example Thresholds
Thresholds must be task-specific, but common examples may include:
- no latency regression over 5% in hot kernels
- no memory regression over 10% without justification
- no new heap allocation in critical hot loops unless justified
- no meaningful warmup regression in frequently invoked tooling without justification

---

## Section 8 — Benchmark Evidence Requirements

Every benchmark-backed claim should state:
- benchmark file or method
- baseline branch or commit
- current branch or commit
- hardware
- workload description
- result summary
- interpretation

### Poor Evidence Example
“It felt faster.”

### Acceptable Evidence Example
“Criterion benchmark on M2 8GB shows 12.4% improvement in median runtime for dense 10,000-segment collision checks versus baseline commit X.”

---

## Section 9 — Performance and Architecture

Performance optimizations must still respect:
- architecture boundaries
- truth governance
- determinism requirements
- maintainability thresholds

### Rule
A faster implementation that weakens truth, determinism, or architecture integrity is not automatically acceptable.

---

## Section 10 — Performance Debt

Sometimes a task intentionally ships with known performance debt.

### Allowed Only If
- debt is explicitly recorded
- impact is understood
- budget overrun is acknowledged
- follow-up work is planned

### Not Allowed
- pretending unmeasured code is fine
- hiding slow paths under optimistic language

---

## Section 11 — Required Benchmark Artifact Structure

Suggested benchmark note structure:
- task
- benchmark target
- hardware
- baseline
- current result
- threshold
- result interpretation
- regressions
- caveats

This may live in:
- validation report
- benchmark markdown
- benchmark output logs
- dedicated performance notes

---

## Section 12 — Performance by Task Class

### Rust-Critical
Benchmark almost always required if computation path changed.

### Performance-Critical
Benchmark always required.

### Major
Benchmark when runtime or memory profile plausibly changed.

### Moderate
Benchmark only if performance-sensitive area touched.

### Trivial
Usually no benchmark required.

---

## Section 13 — Review Questions

Before accepting a performance-sensitive change, ask:
- Was the right metric measured?
- Was the workload realistic?
- Was the baseline valid?
- Is the improvement or regression statistically believable?
- Did the change add hidden cost elsewhere?
- Does the benchmark ignore integration cost?
- Was readability or maintainability damaged beyond reason?

---

## Final Principle
Performance is part of trust.  
Unmeasured performance is guesswork.  
Guesswork does not belong in a performance product.
