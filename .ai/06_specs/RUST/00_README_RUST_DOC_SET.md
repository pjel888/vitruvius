# Vitruvius Rust Engineering Governance Pack

## Purpose
This document set defines the mandatory rules, safeguards, workflows, and review standards for any Rust work performed on Vitruvius by an AI coding agent or a human engineer.

Rust in Vitruvius is the compute data plane. It is gated by the AD-036 Rust Line (the >=2x wall-time gate) and held to a stricter bar than Python. The actual Rust code lives in two locations:

- `scripts/vitruvius/engine_rs/` — the Cargo workspace with members `core/` (package `vitruvius_engine_rs_core`), `pyo3_shim/` (package `vitruvius_engine_rs`), `spatial_kernels/` (package `vitruvius_spatial_kernels`), `stats_kernels/` (package `vitruvius_stats_kernels`), and `pdf/` (package `vitruvius_rust_pdf`).
- `scripts/vitruvius/datalog_rs/` — the standalone hand-rolled Datalog evaluator crate (package `vitruvius_datalog_rs`) for neuro-symbolic compliance proofs (not a workspace member of `engine_rs`).

This pack exists to make Rust implementation:
- deterministic
- auditable
- testable
- benchmarked
- architecture-safe
- resistant to hidden performance regressions
- resistant to subtle numerical or geometric errors
- resistant to porting numpy/BLAS/C primitives that are already native

## Intended Audience
- any AI coding agent operating on this repo (Claude Code, Codex, etc.)
- human reviewers
- future Rust engineers
- the technical founder supervising AI-assisted implementation

## The Rust Line (AD-036) — Non-Negotiable
> Port a compute kernel to Rust only if the hot path is NOT already a single numpy/BLAS/C-native primitive call. Pure orchestration belongs in Python. Every Rust port MUST include a bench artifact demonstrating a >=2x wall-time improvement on the measured kernel before the flag default is flipped to `true`.

This rule is the single most important policy in this pack. It is encoded as:
- `AD-036` in `.ai/10_state/decisions.md` (defines the crate layout and the Rust Line policy).
- `AD-038` in `.ai/10_state/decisions.md` (closes Sprint RUST-MIG-1 with the four kernel verdicts: S1 200x, S2 12.18x, N4 2.73x, N1 DEFERRED).
- `AD-038a` in `.ai/10_state/decisions.md` (codifies the `DEFER_ALREADY_NATIVE` classification used for N1 `wasserstein_merge_decision` because `ot.emd2` is already a native C++ LP solver).
- Invariant `I6 Rust Line` in `.ai/00_system/EXECUTION_LOOP.md`.

Any Rust task that cannot demonstrate >=2x speedup over the existing Python implementation MUST be closed with an AD that classifies it as `DEFER_ALREADY_NATIVE` or `DEFER_INSUFFICIENT_SPEEDUP`. It MUST NOT be merged with the flag flipped on.

## Feature-Flag Contract
Every Rust port lives behind a feature flag in `config/vitruvius.yaml` under `features:`, loaded by `scripts/vitruvius/features.py` into a frozen `Features` dataclass. The contract is:

1. The Python implementation MUST be preserved as the flag-OFF fallback at the call site.
2. Flag-OFF output MUST be byte-identical to the pre-migration Python baseline. Flag-ON output is allowed to diverge only within the documented differential-test tolerance.
3. The new flag MUST be registered in `scripts/tests/test_features.py::EXPECTED_FLAGS`. Adding a flag without registering it is a BLOCK-level CI failure.
4. A bench artifact MUST be written to `.ai/10_state/audit_<name>_<YYYY-MM-DD>.json` showing the >=2x wall-time improvement.
5. The flag MUST default to `false` until the AD that closes the sprint records the flip.

The two active Rust feature flags as of AD-038 are `rust_mig_spatial_kernels` and `rust_mig_stats_kernels`. Both default `true`.

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
- spatial kernels (S1 `build_spatial_adjacency_edges`, S2 `weight_by_distance`) in `spatial_kernels/` (package `vitruvius_spatial_kernels`)
- stats kernels (N4 `mahalanobis_distance`) in `stats_kernels/` (package `vitruvius_stats_kernels`)
- deterministic numerical and geometry primitives (`SpatialPoint`, `Aabb`, `LinearOctree`) in `core/` (package `vitruvius_engine_rs_core`)
- wasm-compatible compute primitives in `core/` (package `vitruvius_engine_rs_core`; the `aabb_intersects` `#[no_mangle] extern "C"` entry point targets `wasm32-unknown-unknown`)
- pyo3-exposed compute primitives through `pyo3_shim/` (package `vitruvius_engine_rs`), the single CPython link point that re-exports kernel crate entry points as `#[pyfunction]`
- the hand-rolled Datalog evaluator in `datalog_rs/` (package `vitruvius_datalog_rs`) for neuro-symbolic compliance proofs
- PDF ingestion benchmarking in `pdf/` (package `vitruvius_rust_pdf`; audit-only — used to compare against the Python `docling` / `opendataloader_pdf` stack, NOT a production parser)

Rust in Vitruvius does NOT exist for:
- vague business logic
- loose feature experimentation
- UI logic
- source-of-truth legal interpretation
- LLM routing, orchestration, or any control-plane work
- canonical ID assignment or feature-flag loading
- porting Python code whose hot path is already a single numpy / BLAS / C-native call
- general ECS work (Bevy ECS headless is a forward-looking option per AEC-ECS-SC research; no crate currently depends on `bevy_ecs`)

## Rust Workspace Crate Inventory
The following six Cargo packages are the canonical `[package] name = "..."` identifiers declared in the `Cargo.toml` files under `scripts/vitruvius/engine_rs/` and `scripts/vitruvius/datalog_rs/`. These are package names, NOT directory names — the directory a crate lives in may differ from its package name (for example, the `pyo3_shim/` directory hosts the package `vitruvius_engine_rs`). Any reference elsewhere in this pack to a crate by directory name (`core/`, `pyo3_shim/`, `spatial_kernels/`, `stats_kernels/`, `pdf/`, `datalog_rs/`) resolves to one of the packages below.

- `vitruvius_engine_rs_core` — pure Rust core, `wasm32` + native, zero pyo3 deps. Hosts `SpatialPoint`, `Aabb`, `LinearOctree`, and the `aabb_intersects` `#[no_mangle] extern "C"` entry point. Crate types: `cdylib + rlib`. Directory: `scripts/vitruvius/engine_rs/core/`.
- `vitruvius_engine_rs` — the `pyo3_shim` crate. Single CPython link point for the entire workspace; re-exports kernel crate entry points as `#[pyfunction]`. Python import name: `vitruvius_engine_rs`. Crate type: `cdylib`. Directory: `scripts/vitruvius/engine_rs/pyo3_shim/`.
- `vitruvius_spatial_kernels` — S1 `build_spatial_adjacency_edges` + S2 `weight_by_distance`. Pure Rust, no pyo3. Crate type: `rlib`. Directory: `scripts/vitruvius/engine_rs/spatial_kernels/`.
- `vitruvius_stats_kernels` — N4 `mahalanobis_distance`. Pure Rust, no pyo3. Sole consumer of `nalgebra = "0.33"`. Crate type: `rlib`. Directory: `scripts/vitruvius/engine_rs/stats_kernels/`.
- `vitruvius_rust_pdf` — AUDIT-ONLY benchmark crate used to compare against `docling` / `opendataloader_pdf`. Direct pyo3 link; `lopdf = "0.36"`. NOT wired into the `vitruvius_engine_rs` pyo3_shim re-export. NOT a production parser. Crate types: `cdylib + rlib`. Directory: `scripts/vitruvius/engine_rs/pdf/`.
- `vitruvius_datalog_rs` — standalone crate at `scripts/vitruvius/datalog_rs/`, NOT a workspace member of `engine_rs`. Hand-rolled Datalog evaluator for neuro-symbolic compliance proofs. Direct pyo3 link. Crate type: `cdylib`.

## Required Operating Sequence
For every non-trivial Rust task:
1. Read the governing documents in this pack (in order of authority above).
2. Produce or update the task research pack under `.ai/02_audits/`.
3. Produce or update the audit JSON at `.ai/10_state/audit_<name>_<YYYY-MM-DD>.json`.
4. Produce or update the implementation plan under `.ai/03_plans/`.
5. Produce a plan critique (in the same plan file or alongside it).
6. Produce an execution checklist (Section 10 of `08_RUST_TASK_TEMPLATE.md`).
7. Implement in controlled slices.
8. Run tests and the Python bench harness under `scripts/vitruvius/bench/`.
9. Write a short validation report and append it near the sprint-close AD (not as a separate report file).
10. Append the sprint-close AD to `.ai/10_state/decisions.md` and archive the plan under `.ai/09_archive/plans/`.

## Absolute Rule
No Rust code is complete until it has:
- explicit input/output contract
- edge-case analysis
- deterministic tests (inline `#[cfg(test)] mod tests { ... }`)
- differential test against the Python baseline where applicable
- bench artifact at `.ai/10_state/audit_<name>_<YYYY-MM-DD>.json` proving >=2x wall-time improvement before any feature-flag default flip
- review against the architecture boundaries in `04_RUST_ARCHITECTURE_AND_BOUNDARY_RULES.md`
- validation summary appended near the closing AD

## Repo Placement
This governance pack is canonically located at:

`.ai/06_specs/RUST/`

The eight files in this pack are:
- `00_README_RUST_DOC_SET.md` (this file)
- `01_RUST_OPERATING_CONTRACT_FOR_CODEX.md`
- `02_RUST_KERNEL_DEVELOPMENT_PROTOCOL.md`
- `03_RUST_SAFEGUARDS_AND_FAILURE_CONTAINMENT.md`
- `04_RUST_ARCHITECTURE_AND_BOUNDARY_RULES.md`
- `05_RUST_TESTING_BENCHMARKING_AND_VALIDATION.md`
- `06_RUST_CODE_REVIEW_CHECKLIST.md`
- `07_RUST_STYLE_AND_IMPLEMENTATION_RULES.md`
- `08_RUST_TASK_TEMPLATE.md`

Do not move, copy, or fork this pack to any other location.

## Companion Files
These documents must be read alongside this pack:
- `.ai/00_system/EXECUTION_LOOP.md` (Vitruvius Standard Execution Loop v3.0 — authoritative workflow)
- `.ai/00_system/principles.md` (10 enforceable principles P1-P10, including I5 Lazy CLI Imports, I6 Rust Line, I8 Test Baseline Monotonic, I9 Registry Single-Writer)
- `.ai/00_system/architecture.md` (system architecture; contains the `engine_rs/` and `datalog_rs/` subpackage entries)
- `.ai/01_roadmap/master-roadmap.md` (phase-status single source of truth)
- `.ai/01_roadmap/current-phase.md` (snapshot of the active sprint)
- `.ai/01_roadmap/milestone-tracker.md` (sprint-exit ledger)
- `.ai/10_state/decisions.md` (append-only AD ledger; AD-036, AD-038, AD-038a are the three ADs that govern Rust)
- `.ai/10_state/known_issues.md` (risk register)
- `.ai/10_state/active_context.md` (session handoff)
- `.ai/03_plans/00-governing-implementation-plan.md` (execution-order authority)

## Tooling Pins
These are hard requirements. Do not change them without an AD.

- Rust edition: `2021` (workspace-wide).
- `pyo3 = "0.22"` with `features = ["extension-module"]`. The 0.22 API uses `Bound<'py, PyAny>` / `Bound<'_, PyModule>`. The legacy `&PyAny` / `Py<T>` patterns are forbidden.
- `ndarray = "0.15"` pinned at the workspace root in `scripts/vitruvius/engine_rs/Cargo.toml` (cargo requires the pin at workspace level when shared across >=2 members).
- `nalgebra = "0.33"` inline in `stats_kernels/` only (sole consumer).
- `lopdf = "0.36"` in `pdf/` only (audit-only crate; not re-exported through `pyo3_shim`).
- Release profile pinned at workspace root: `opt-level = 3`, `lto = "thin"`, `codegen-units = 1`. Members inherit.
- `.cargo/config.toml` injects `-C link-arg=-undefined -C link-arg=dynamic_lookup` on `aarch64-apple-darwin` and `x86_64-apple-darwin` so `cargo build --release` stays green outside `maturin`. The canonical ship path is still `maturin`.
- Tests live inline as `#[cfg(test)] mod tests { ... }` in the same `.rs` file as the implementation. The project does NOT use a separate `tests/` directory or a separate `benches/` directory inside the Rust workspace. The integration bench harness is Python-side under `scripts/vitruvius/bench/`.

Canonical commands:
- pyo3 extension build: `maturin develop --manifest-path scripts/vitruvius/engine_rs/pyo3_shim/Cargo.toml`
- wasm target build: `cargo build --target wasm32-unknown-unknown -p vitruvius_engine_rs_core`
- workspace tests: `cargo test --workspace --all-targets`
- workspace lint: `cargo clippy --workspace --all-targets --all-features -- -D warnings`
- workspace format check: `cargo fmt --all -- --check`

## Final Rule
No AI-generated Rust is trusted by default.
Only validated Rust survives.
