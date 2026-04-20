<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-20 -->

# datalog_rs

## Purpose
Hardened Rust crate for datalog engine integration and rule compilation. Bridges declarative rule logic with the Python pipeline.

## Key Files
| File | Description |
|------|-------------|
| `Cargo.toml` | Crate manifest |
| `src/lib.rs` | Library root and PyO3 exports |

## For AI Agents

### Working In This Directory
- **Rust is a hardened compute zone.** This crate exists for deterministic rule evaluation and datalog engine integration.
- **It does NOT exist for:** orchestration, legal/policy interpretation, AI prompt logic, knowledge-truth governance, or casual feature experimentation.
- **Read the Rust governance pack before writing Rust code.** Minimum required: Rust Operating Contract, Rust Kernel Development Protocol, Rust Safeguards and Failure Containment, Rust Architecture and Boundary Rules, Rust Testing/Benchmarking/Validation, Rust Code Review Checklist, Rust Style and Implementation Rules.
- **Avoid `unsafe` unless explicitly justified and reviewed.**
- **Define data contract and edge cases before code.**

### Testing Requirements
- Rust tests run via `cargo test`.
- Benchmark before claiming performance: `cargo bench`.
- Test before optimization.

### Common Patterns
- PyO3-exposed primitives only where justified.
- Rule schemas must be versioned.
- Datalog facts must be traceable to canonical sources.
