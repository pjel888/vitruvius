# Vitruvius Task Classification Policy

## Purpose
This policy defines how tasks are classified so that agents can determine the required level of planning, validation, documentation, and caution before execution.

Vitruvius must not apply the same process to a one-line typo fix and to a cross-language spatial-kernel refactor. Task classification prevents both under-governance and over-procedure.

## Core Principle
The process burden should scale with risk, not with mood.

## Classification Objectives
Task classification exists to determine:
- whether the full execution loop is required
- what validation is required
- whether state docs must be updated
- whether decisions log updates are required
- whether benchmarks are required
- whether cross-language review is required
- whether truth/provenance safeguards apply

---

## Section 1 — Classification Dimensions

A task may be high-risk for more than one reason. Agents must evaluate across dimensions, not only by file count.

### Risk Dimensions
- architecture impact
- truth impact
- performance impact
- cross-language boundary impact
- state / workflow impact
- data model impact
- blast radius
- reversibility
- ambiguity

---

## Section 2 — Task Classes

### Class T0 — Trivial
#### Definition
A narrowly scoped change with minimal blast radius and no meaningful architecture, performance, truth, or state implications.

#### Examples
- comment fix
- typo correction in non-authoritative text
- dead link fix in a non-governing doc
- isolated display-only copy update
- renaming a clearly local private variable when graph impact confirms isolation

#### Requirements
- no full execution loop required
- quick verification required
- no state update unless reality changed
- no benchmark
- no decision log update

#### Rule
If any ambiguity exists, do not classify as T0.

---

### Class T1 — Moderate
#### Definition
A contained change with limited scope that affects behavior, but not architecture in a major way.

#### Examples
- focused bug fix in one module
- adding a config field with clear local impact
- adding a targeted test suite
- small improvement to pipeline behavior in one stage
- updating a helper function used in a limited context

#### Requirements
- abbreviated execution loop allowed if well understood
- targeted audit or impact check required
- implementation plan preferred if not obvious
- validation required
- state update if status or contract changed

---

### Class T2 — Major
#### Definition
A meaningful implementation task affecting multiple files, modules, or workflows.

#### Examples
- feature addition across several modules
- pipeline-stage refactor
- canonicalization behavior change
- extraction logic expansion
- adding or changing model-routing logic
- meaningful schema or config evolution

#### Requirements
- full execution loop required
- validation report required
- state docs update required
- integration validation required
- audit and plan required
- critique required

---

### Class T3 — Architecture-Affecting
#### Definition
A task that changes system boundaries, core design assumptions, or how major layers interact.

#### Examples
- introducing a new subsystem
- changing execution order of core stages
- moving logic across Python/Rust boundary
- changing contract between RocksDB and compiler
- changing promotion or truth-admission model
- redefining state or roadmap authority flows

#### Requirements
- full execution loop
- architecture review
- decision log update
- integration and regression validation
- likely spec or policy update
- elevated caution

---

### Class T4 — Rust-Critical
#### Definition
Any task where Rust correctness, numerical stability, memory behavior, determinism, or hot-path performance matters.

#### Examples
- geometry kernel implementation
- ECS component or system change
- PyO3 compute interface change
- Wasm compute export change
- numeric type or tolerance change
- spatial index update
- routing inner-loop optimization

#### Requirements
- full execution loop
- Rust governance pack mandatory
- explicit data contract
- edge-case analysis
- benchmark if hot path
- validation report
- stop if tolerance or contract unclear

---

### Class T5 — Truth-Critical
#### Definition
Any task that could change what Vitruvius accepts, promotes, stores, or exposes as trusted knowledge.

#### Examples
- rule extraction logic
- canonical ID mapping logic
- provenance metadata requirements
- confidence thresholds
- promotion rules
- review decisions
- temporal version logic
- evidence-snippet handling
- conflict resolution semantics for rules

#### Requirements
- full execution loop
- provenance and schema validation
- oracle or reviewed-sample validation
- state docs update
- no silent promotion allowed
- extremely high honesty requirements

---

### Class T6 — Performance-Critical
#### Definition
Any task where product viability depends materially on speed, memory, throughput, or latency.

#### Examples
- large pipeline acceleration
- benchmark-driven refactor
- memory footprint reduction
- caching changes
- graph or embedding throughput changes
- feature flags that alter runtime cost
- M2 8GB hardening work

#### Requirements
- full or near-full execution loop
- benchmark plan required
- baseline required
- acceptance threshold required
- rejection if performance regresses beyond threshold without explicit approval

---

### Class T7 — Governance-Critical
#### Definition
A task that changes how the repo governs itself.

#### Examples
- AGENTS changes
- execution loop changes
- validation protocol changes
- document authority changes
- task classification changes
- cross-language contract changes

#### Requirements
- full execution loop
- clear rationale
- decision log or governance update
- careful conflict analysis
- state reconciliation if workflow changes

---

## Section 3 — Classification Procedure

For any non-obvious task, answer:
1. Does it touch architecture boundaries?
2. Does it affect truth-bearing outputs?
3. Does it affect Rust, numerical logic, or performance-critical paths?
4. Does it affect multiple modules or workflows?
5. Does it require state/doc updates?
6. Could it silently break trusted outputs?
7. Would rollback be expensive?

### Rule
If the answer to any of the above is yes, the task is not trivial.

---

## Section 4 — Multi-Class Tasks

Many tasks belong to multiple classes.

### Example
A Rust refactor of relationship extraction scoring could be:
- T2 Major
- T4 Rust-Critical
- T5 Truth-Critical
- T6 Performance-Critical

### Rule
When multiple classes apply, use the strictest process requirements.

---

## Section 5 — Validation Mapping by Task Class

| Class | Execution Loop | Validation Report | State Update | Benchmark | Decision Log |
|------|----------------|------------------|-------------|-----------|--------------|
| T0 | No | No | Rare | No | No |
| T1 | Abbreviated | Sometimes | If needed | Rare | No |
| T2 | Yes | Yes | Yes | If relevant | Maybe |
| T3 | Yes | Yes | Yes | If relevant | Yes |
| T4 | Yes | Yes | Yes | Usually | Maybe |
| T5 | Yes | Yes | Yes | If relevant | Maybe |
| T6 | Yes | Yes | Yes | Yes | Maybe |
| T7 | Yes | Yes | Yes | No | Yes |

---

## Section 6 — Examples

### Example A
“Update a typo in a docstring.”
Likely T0.

### Example B
“Change canonicalization to generate a new metadata field.”
Likely T2, possibly T5 if truth-affecting.

### Example C
“Implement capsule clash detection in Rust.”
T4 and likely T6.

### Example D
“Change promotion rule so low-confidence items are admitted.”
T5 and probably T7.

### Example E
“Refactor PyO3 boundary for Wasm-ready shared compute structs.”
T3 and T4.

---

## Section 7 — Classification Must Be Recorded

For non-trivial tasks, the task class should be written in:
- research pack
- audit
- implementation plan
- validation report

This ensures the required rigor is visible and reviewable.

---

## Final Rule
Do not under-classify a task to save effort.  
That is how silent risk enters the repo.
