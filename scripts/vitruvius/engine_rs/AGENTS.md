<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-20 -->

# engine_rs

## Purpose
Hardened Rust compute crate for deterministic geometry kernels, ECS systems, spatial indexing, numerical routines, and Wasm-compatible compute modules.

## Key Files
| File | Description |
|------|-------------|
| `Cargo.toml` | Crate manifest |
| `src/lib.rs` | Library root and PyO3 shim exports |
| `core/` | Core ECS and world-state modules |
| `spatial_kernels/` | Deterministic spatial compute kernels |

## For AI Agents

### Working In This Directory
- **Rust is a hardened compute zone.** It exists for deterministic computation, geometry kernels, ECS, spatial indexing, and numerical routines.
- **It does NOT exist for:** orchestration, legal/policy interpretation, AI prompt logic, knowledge-truth governance, or casual feature experimentation.
- **Read the Rust governance pack before writing Rust code.** Minimum required: Rust Operating Contract, Rust Kernel Development Protocol, Rust Safeguards and Failure Containment, Rust Architecture and Boundary Rules, Rust Testing/Benchmarking/Validation, Rust Code Review Checklist, Rust Style and Implementation Rules.
- **Avoid `unsafe` unless explicitly justified and reviewed.**
- **Define data contract, numeric type policy, edge cases, and tolerance policy before code.**

### Testing Requirements
- Rust tests run via `cargo test`.
- Benchmark before claiming performance: `cargo bench`.
- Test before optimization.

### Common Patterns
- PyO3-exposed compute primitives only where justified.
- Coordinate frames and units must be explicit.
- Tolerance policies must be defined for all geometric operations.
