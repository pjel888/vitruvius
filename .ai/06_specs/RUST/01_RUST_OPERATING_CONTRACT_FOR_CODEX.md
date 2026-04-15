# Rust Operating Contract for AI Coding Agents

## Purpose
This file defines the non-negotiable behavioral contract any AI coding agent (Claude Code, Codex, etc.) MUST follow whenever working on Rust code in Vitruvius. The historical filename retains the word "Codex" for path stability, but every rule below applies to every agent equally. Where this document says "the Agent", it means whichever AI agent is currently editing Rust.

## Identity of the Rust Layer
The Rust layer is:
- deterministic
- performance-sensitive
- architecture-constrained
- mathematically accountable
- cross-language boundary-sensitive
- gated by the AD-036 Rust Line (the >=2x wall-time gate)
- not a sandbox for improvisation

## The Agent Must Assume
1. Rust changes are high-risk compared to ordinary Python changes.
2. A compiling Rust implementation may still be numerically wrong.
3. A passing Rust test suite may still hide a performance regression.
4. A clean-looking API may still violate cross-language architecture.
5. Any hidden assumption not written down is a bug risk.
6. A passing flag-OFF test run proves nothing about the flag-ON Rust path. Both paths MUST be exercised, and flag-OFF output MUST remain byte-identical to the pre-migration Python baseline.

## The Agent Must Read First
Before touching Rust, the Agent MUST read these files in this order:
1. `.ai/00_system/EXECUTION_LOOP.md` (Vitruvius Standard Execution Loop v3.0)
2. `.ai/00_system/principles.md` (look for `I6 Rust Line` and the full P1-P10 list)
3. `.ai/00_system/architecture.md` (look for the `engine_rs/` and `datalog_rs/` entries)
4. `.ai/01_roadmap/current-phase.md`
5. `.ai/06_specs/RUST/*.md` (this governance pack, in the authority order from `00_README_RUST_DOC_SET.md`)
6. `.ai/10_state/decisions.md` (at minimum AD-036, AD-038, AD-038a, plus any newer AD that touches Rust)
7. The target `Cargo.toml` and `src/lib.rs` for the affected crate
8. Any existing inline `#[cfg(test)] mod tests { ... }` in the affected module
9. The Python caller / fallback path that the Rust port is replacing (so the differential test has a reference)
10. Any existing Python bench harness in `scripts/vitruvius/bench/` that measures the affected kernel

## Mandatory Workflow
The Agent MUST follow this order. Each step has a concrete artifact path.

1. Context read (the 10 files above).
2. Audit the current implementation; write the audit JSON at `.ai/10_state/audit_<name>_<YYYY-MM-DD>.json`.
3. Identify risks and unknowns; capture them in the research pack under `.ai/02_audits/`.
4. Produce the implementation plan under `.ai/03_plans/`.
5. Produce a plan critique (in the same plan file or alongside it).
6. Produce an execution checklist (Section 10 of `08_RUST_TASK_TEMPLATE.md`).
7. Implement the smallest safe slice.
8. Run the validation commands listed under "Completion Standard" below.
9. Summarize results honestly in a short validation block.
10. Append the sprint-close AD to `.ai/10_state/decisions.md` and archive the plan under `.ai/09_archive/plans/`.

## The Agent Must Not
- invent architecture that contradicts the governing docs
- write `unsafe` Rust unless explicitly authorized by an AD
- introduce concurrency or parallelism without a justification AD
- add new dependencies casually
- move logic into Rust just because Rust is faster
- bypass tests because "the code is simple"
- claim performance without bench artifact evidence
- hide uncertainty
- port a numpy hot loop to Rust without first proving the hot path is NOT already a native BLAS / C primitive (AD-036 Rust Line)
- delete or bypass the Python fallback branch at the call site
- add a new feature flag without registering it in `scripts/tests/test_features.py::EXPECTED_FLAGS`
- use `unwrap()`, `expect()`, `panic!()`, `todo!()`, `unimplemented!()`, or `unreachable!()` in non-test code
- compare floats with `==`; always compare against a documented tolerance
- use `HashMap` in any code path whose iteration order escapes the crate boundary; use `BTreeMap` or `IndexMap` instead
- introduce a new Rust dependency without an AD and a `cargo deny check` / `cargo audit` pass
- introduce `rayon`, `tokio`, `async` Rust, `serde`, or hand-rolled SIMD without an AD that justifies it
- use the legacy pyo3 `&PyAny` / `Py<T>` patterns; pyo3 0.22 uses `Bound<'py, PyAny>` and `Bound<'_, PyModule>`

## The Agent Must Always Provide
For every non-trivial Rust change:
- target files
- purpose of change
- data contract (inputs, outputs, units, coordinate frame, numeric types, invalid states, tolerance policy)
- edge cases
- expected complexity
- possible precision risks
- test plan (unit, edge-case, property, differential)
- bench plan for hot paths
- bench artifact path at `.ai/10_state/audit_<name>_<YYYY-MM-DD>.json`
- feature flag name and the commit that registers it in `scripts/tests/test_features.py::EXPECTED_FLAGS`
- rollback strategy (the flag-OFF fallback path and how to flip the default back to `false`)

## Escalation Conditions
The Agent MUST stop and escalate if any of the following occur:
- unclear numerical assumptions
- undefined coordinate system or unit convention
- geometry degeneracy not covered by current contracts
- cross-language boundary mismatch
- need for `unsafe` Rust
- ambiguous memory layout requirements
- bench shows <2x wall-time improvement (the change does not clear the AD-036 Rust Line; close with a `DEFER_INSUFFICIENT_SPEEDUP` AD)
- the existing Python hot path is already a single native BLAS / C primitive call (close with a `DEFER_ALREADY_NATIVE` AD per AD-038a)
- the Python fallback cannot be preserved at the call site
- inconsistent authoritative docs

## Completion Standard
Rust work is not complete until ALL of these commands pass on a clean working tree:

```
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-targets
cargo build --target wasm32-unknown-unknown -p vitruvius_engine_rs_core
maturin develop --manifest-path scripts/vitruvius/engine_rs/pyo3_shim/Cargo.toml
python -m pytest scripts/tests/test_features.py -xvs
python -m pytest scripts/tests/ -x
```

In addition, if the change ports a Python kernel to Rust:
- a bench artifact at `.ai/10_state/audit_<name>_<YYYY-MM-DD>.json` MUST exist and demonstrate >=2x wall-time improvement on the measured kernel
- the new feature flag MUST be registered in `scripts/tests/test_features.py::EXPECTED_FLAGS`
- the flag-OFF path MUST produce byte-identical output against the pre-migration Python baseline
- the flag default MUST stay `false` until the AD that closes the sprint records the flip

## Truthfulness Rule
If the Agent is unsure, it MUST say so explicitly and identify:
- what is uncertain
- why it is uncertain
- what should be tested or measured next

## Principle
In Rust, confidence is not evidence.
Benchmarks and tests are evidence.
The bench artifact at `.ai/10_state/audit_<name>_<YYYY-MM-DD>.json` is the evidence of record.
