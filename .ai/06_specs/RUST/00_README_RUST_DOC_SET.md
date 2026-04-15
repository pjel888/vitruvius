# Vitruvius Rust Engineering Governance Pack

## Purpose
This document set defines the mandatory rules, safeguards, workflows, and review standards for any Rust work performed on Vitruvius by Codex or any other AI coding agent.

This pack exists to make Rust implementation:
- deterministic
- auditable
- testable
- benchmarked
- architecture-safe
- resistant to hidden performance regressions
- resistant to subtle numerical or geometric errors

## Intended Audience
- Codex
- human reviewers
- future Rust engineers
- technical founders supervising AI-assisted implementation

## Document Order of Authority
1. `01_RUST_OPERATING_CONTRACT_FOR_CODEX.md`
2. `02_RUST_KERNEL_DEVELOPMENT_PROTOCOL.md`
3. `03_RUST_SAFEGUARDS_AND_FAILURE_CONTAINMENT.md`
4. `04_RUST_ARCHITECTURE_AND_BOUNDARY_RULES.md`
5. `05_RUST_TESTING_BENCHMARKING_AND_VALIDATION.md`
6. `06_RUST_CODE_REVIEW_CHECKLIST.md`
7. `07_RUST_STYLE_AND_IMPLEMENTATION_RULES.md`
8. `08_RUST_TASK_TEMPLATE.md`

If any lower document conflicts with a higher document, the higher document wins.

## Core Principle
Rust is not a general coding zone. Rust is a hardened compute zone.

Rust in Vitruvius exists for:
- deterministic computation
- spatial kernels
- geometry math
- ECS systems
- constrained high-performance routines
- numerical verification support
- Wasm-compatible compute modules
- PyO3-exposed kernels where justified

Rust does **not** exist for:
- vague business logic
- loose feature experimentation
- UI logic
- source-of-truth legal interpretation
- uncontrolled architecture invention

## Required Operating Sequence
For every non-trivial Rust task:
1. Read the governing documents in this pack.
2. Produce or update the task research pack.
3. Produce or update the audit document.
4. Produce or update the implementation plan.
5. Produce a plan critique.
6. Produce an execution checklist.
7. Implement in controlled slices.
8. Run tests, property tests, and benchmarks.
9. Write a validation report.
10. Update state and decisions documentation.

## Absolute Rule
No Rust code is complete until it has:
- explicit input/output contract
- edge-case analysis
- deterministic tests
- property-based tests where applicable
- benchmark evidence for hot paths
- review against architecture boundaries
- validation report

## Recommended Repo Placement
Place these documents under a path such as:
- `.ai/00_system/rust/`
- `.ai/11_skills/rust/`
- `.ai/12_agents/codex/rust/`

## Suggested Companion Files
These documents should be used alongside:
- `EXECUTION_LOOP.md`
- `principles.md`
- `architecture.md`
- `current-phase.md`
- `master-roadmap.md`
- `milestone-tracker.md`
- `decisions.md`

## Final Rule
No AI-generated Rust is trusted by default.
Only validated Rust survives.
