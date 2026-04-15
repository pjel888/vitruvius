# Rust Operating Contract for Codex

## Purpose
This file defines the non-negotiable behavioral contract Codex must follow whenever working on Rust code in Vitruvius.

## Identity of the Rust Layer
The Rust layer is:
- deterministic
- performance-sensitive
- architecture-constrained
- mathematically accountable
- cross-language boundary-sensitive
- not a sandbox for improvisation

## Codex Must Assume
1. Rust changes are high-risk compared to ordinary Python changes.
2. A compiling Rust implementation may still be numerically wrong.
3. A passing Rust test suite may still hide performance regression.
4. A clean-looking API may still violate cross-language architecture.
5. Any hidden assumption not written down is a bug risk.

## Codex Must Read First
Before touching Rust, Codex must read:
1. `EXECUTION_LOOP.md`
2. the current roadmap and current phase file
3. the relevant Rust document(s) in this governance pack
4. the target crate manifest and module tree
5. existing tests and benchmarks for the affected module
6. any existing audit or plan for the task

## Mandatory Workflow
Codex must follow this order:
1. Context read
2. Audit current implementation
3. Identify risks and unknowns
4. Produce implementation plan
5. Produce plan critique
6. Produce execution checklist
7. Implement smallest safe slice
8. Run validation commands
9. Summarize results honestly
10. Update state docs

## Codex Must Not
- invent architecture that contradicts the governing docs
- write unsafe Rust unless explicitly authorized
- introduce concurrency or parallelism without a justification section
- add new dependencies casually
- move logic into Rust just because Rust is faster
- bypass tests because “the code is simple”
- claim performance without benchmark evidence
- hide uncertainty

## Codex Must Always Provide
For every non-trivial Rust change:
- target files
- purpose of change
- data contract
- edge cases
- expected complexity
- possible precision risks
- test plan
- benchmark plan for hot paths
- rollback strategy

## Escalation Conditions
Codex must stop and escalate if any of the following occur:
- unclear numerical assumptions
- undefined coordinate system or unit convention
- geometry degeneracy not covered by current contracts
- cross-language boundary mismatch
- need for unsafe Rust
- ambiguous memory layout requirements
- benchmark regressions without clear reason
- inconsistent authoritative docs

## Completion Standard
Rust work is not complete unless:
- `cargo fmt` passes
- `cargo clippy` passes at required strictness
- `cargo test` passes
- property tests pass where applicable
- benchmarks are run for hot paths
- validation report is written
- state docs are updated

## Truthfulness Rule
If Codex is unsure, it must say so explicitly and identify:
- what is uncertain
- why it is uncertain
- what should be tested or measured next

## Principle
In Rust, confidence is not evidence.
Benchmarks and tests are evidence.
