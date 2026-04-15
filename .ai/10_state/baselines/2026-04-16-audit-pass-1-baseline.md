---
task: vitruvius-audit-pass-1
phase: 02
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# 02 — Baseline

## Repo State
- Commit SHA: `f0cf21fa7f0205204c098af5a84dc7e40ec0d98c`
- Branch: `main`
- Working tree at audit start included unrelated doc edits in `AGENTS.md` and `CLAUDE.md`.

## Toolchain
- Python: `3.12.5`
- Node: `v25.9.0`
- Cargo: `1.94.1`
- GitNexus status before refresh: stale (`Indexed commit: 027e457`, `Current commit: f0cf21f`)
- GitNexus status after refresh: up to date

## Validation Baseline
- `pytest scripts/tests -q` → `1566 passed, 1 skipped`
- `npm test` in `spatial-daemon/` → `21 passed`
- `npm run typecheck` in `spatial-daemon/` → pass
- `npm run build` in `spatial-daemon/` → pass
- `cargo test --quiet` in `scripts/vitruvius/engine_rs` → pass
- `cargo test --quiet` in `scripts/vitruvius/datalog_rs` → pass

## Strict Static Gate Baseline
- `cargo fmt --all --check` in `engine_rs` → fail
- `cargo clippy --workspace --all-targets -- -D warnings` in `engine_rs` → fail
- `cargo fmt --all --check` in `datalog_rs` → fail
- `cargo clippy --workspace --all-targets -- -D warnings` in `datalog_rs` → fail

## Runtime Command Baseline
- `python3 scripts/pipeline_cli.py --help` → pass
- `python3 scripts/pipeline_cli.py run` → pass, but writes fresh status/lint/tree artifacts
- `python3 scripts/pipeline_cli.py build-graph` → pass
- `python3 scripts/pipeline_cli.py query-structured --function neighbors --subject concept-occupancy-classification` → pass with semantically weak evidence output
- `python3 scripts/pipeline_cli.py query "What governs occupancy classification?"` → returns no supporting evidence
- `python3 scripts/pipeline_cli.py export-graph-owl` → pass

## Baseline Drift Observed
- `pipeline_cli.py run` reported:
  - `82` new files
  - `8` changed files
  - `156` missing files
- `lint` reported:
  - `9` non-PDF files
  - `4` duplicate-like filename groups
- `build-graph` reported:
  - `24` nodes
  - `30` edges
  - `6` orphan-node warnings

## Notes
- Generated artifacts under `005_Operational-Intelligence-Layer/graph/` and `006_System-Manifests/` were modified by audit-time verification commands only.
- No product source files were edited during baseline capture.
