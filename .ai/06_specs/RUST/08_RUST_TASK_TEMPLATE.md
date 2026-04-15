# Rust Task Template

## Purpose
Use this template for every non-trivial Rust task. Fill in every section. Do not delete fields you cannot answer — write `unknown` or `n/a` and explain.

---

## 1. Task Identity
- Task name:
- Date:
- Current phase:
- Related roadmap item:
- Related audit:
- Related plan:
- Related AD (e.g. AD-036, AD-038, AD-038a):
- Related feature flag (e.g. `rust_mig_spatial_kernels`, `rust_mig_stats_kernels`):
- Crate (one of: `vitruvius_engine_rs_core` / `vitruvius_engine_rs` (pyo3_shim) / `vitruvius_spatial_kernels` / `vitruvius_stats_kernels` / `vitruvius_rust_pdf` / `vitruvius_datalog_rs`):

## 2. Problem Statement
- What problem is being solved?
- Why does it belong in Rust?
- Why now?
- Is the current Python hot path already a single native BLAS / C primitive call (e.g. `numpy.linalg.*`, `scipy.linalg.*`, `ot.emd2`, anything in `_C` extension modules)? If yes, this task is `DEFER_ALREADY_NATIVE` per AD-038a — close with an AD instead of porting.

## 3. Research Inputs
- `.ai/00_system/EXECUTION_LOOP.md`:
- `.ai/00_system/principles.md` (I6 Rust Line, P1-P10):
- `.ai/00_system/architecture.md` (`engine_rs/` and `datalog_rs/` entries):
- `.ai/01_roadmap/current-phase.md`:
- `.ai/06_specs/RUST/*.md` (this governance pack, in authority order):
- `.ai/10_state/decisions.md` (AD-036, AD-038, AD-038a, plus any newer Rust AD):
- target `Cargo.toml` and `src/lib.rs` for the affected crate:
- existing inline `#[cfg(test)] mod tests { ... }` in the affected module:
- Python caller / fallback path being replaced:
- existing Python bench harness in `scripts/vitruvius/bench/`:
- external references reviewed:

## 4. Audit Summary
- current implementation:
- gaps:
- risks:
- open questions:

## 5. Proposed Kernel / Module
- crate:
- module:
- public API:
- internal helpers:
- FFI / Wasm exposure needed:
- Python fallback call site (file + function that retains the pre-migration Python behavior):

## 6. Data Contract
- inputs:
- outputs:
- units:
- coordinate frame:
- numeric types:
- invalid states:
- tolerance policy:
- wasm32 compatibility (yes/no — if yes, the module MUST live in the `core` crate and any pyo3 imports MUST be gated behind `#[cfg(not(target_arch = "wasm32"))]`):

## 7. Risk Analysis
- correctness risks:
- precision risks:
- performance risks:
- architecture risks:
- maintenance risks:

## 8. Test Plan
- unit tests (inline `#[cfg(test)] mod tests`):
- edge-case tests:
- property tests (where applicable):
- differential tests against the Python baseline:

## 9. Benchmark Plan (AD-036 Rust Line)
- Python baseline harness path (`scripts/vitruvius/bench/...`):
- Python baseline wall-time:
- Python baseline peak RSS:
- Rust port harness path (same file, different branch):
- Rust port wall-time:
- Rust port peak RSS:
- Speedup (MUST be >=2x; else DEFER with an AD):
- Bench artifact path (`.ai/10_state/audit_<name>_<YYYY-MM-DD>.json`):

## 10. Execution Checklist
- [ ] read `.ai/00_system/EXECUTION_LOOP.md` and the Rust governance pack at `.ai/06_specs/RUST/`
- [ ] confirm the hot path is NOT already a native BLAS / C primitive (AD-036 Rust Line)
- [ ] draft the data contract
- [ ] implement the reference version with inline `#[cfg(test)] mod tests`
- [ ] add a differential test against the Python baseline
- [ ] run `cargo fmt --all -- --check`
- [ ] run `cargo clippy --workspace --all-targets --all-features -- -D warnings`
- [ ] run `cargo test --workspace --all-targets`
- [ ] run `cargo build --target wasm32-unknown-unknown -p vitruvius_engine_rs_core` (if the change touches `core`)
- [ ] run `maturin develop --manifest-path scripts/vitruvius/engine_rs/pyo3_shim/Cargo.toml` (if the change touches `pyo3_shim` or any re-exported kernel)
- [ ] run the Python bench harness on both flag-OFF (Python) and flag-ON (Rust) branches
- [ ] write the bench artifact JSON at `.ai/10_state/audit_<name>_<YYYY-MM-DD>.json`
- [ ] confirm speedup >=2x (else DEFER with an AD)
- [ ] register the new feature flag in `scripts/tests/test_features.py::EXPECTED_FLAGS`
- [ ] run `python -m pytest scripts/tests/test_features.py -xvs`
- [ ] run `python -m pytest scripts/tests/ -x` (full suite, confirm test baseline monotonic per I8)
- [ ] confirm flag-OFF output is byte-identical to the pre-migration Python baseline
- [ ] append the sprint-close AD to `.ai/10_state/decisions.md`
- [ ] archive the plan under `.ai/09_archive/plans/`

## 11. Plan Critique
- weak assumptions:
- likely failure points:
- architecture concerns:
- unresolved edge cases:

## 12. Validation Result
- tests:
- benchmarks:
- bench artifact path (`.ai/10_state/audit_<name>_<YYYY-MM-DD>.json`):
- speedup (>=2x or DEFER):
- flag-OFF byte-identity confirmed (yes/no):
- status:
- remaining caveats:

## Final Rule
Do not mark the task done until the validation section is filled honestly.
