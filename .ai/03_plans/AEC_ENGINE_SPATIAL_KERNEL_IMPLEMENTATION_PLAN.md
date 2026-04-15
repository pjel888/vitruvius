---
title: AEC Engine Spatial Kernel Implementation Plan
type: subsystem-plan
status: proposed
date: 2026-04-16
last_updated: 2026-04-16
planned_code_locations:
  - scripts/vitruvius/aec/spatial/contracts.py
  - scripts/vitruvius/aec/spatial/service.py
  - scripts/vitruvius/aec/spatial/parity.py
planned_rust_extension_points:
  - scripts/vitruvius/engine_rs/core
  - scripts/vitruvius/engine_rs/spatial_kernels
  - scripts/vitruvius/engine_rs/pyo3_shim
planned_typescript_touchpoints:
  - spatial-daemon/src/types.ts
  - spatial-daemon/src/contract_writer.ts
repo_grounding:
  - scripts/vitruvius/spatial/cli.py
  - scripts/vitruvius/spatial/schema.py
  - scripts/vitruvius/spatial/contract_reader.py
  - scripts/vitruvius/spatial/spatial_edge_builder.py
  - scripts/vitruvius/spatial/proximity_jump.py
  - scripts/vitruvius/engine_rs/core/src/lib.rs
  - scripts/vitruvius/engine_rs/spatial_kernels
  - spatial-daemon/tests/contract_writer.test.ts
governing_inputs:
  - .ai/06_specs/AEC_ENGINE/03_SPATIAL_COMPREHENSION_PROTOCOL.md
  - .ai/06_specs/GOVERNANCE/04_CROSS_LANGUAGE_BOUNDARY_CONTRACT.md
  - .ai/06_specs/RUST/04_RUST_ARCHITECTURE_AND_BOUNDARY_RULES.md
  - .ai/06_specs/RUST/05_RUST_TESTING_BENCHMARKING_AND_VALIDATION.md
---

# AEC Engine Spatial Kernel Implementation Plan

## 1. Scope
Build the deterministic geometry compute layer for:
- clash and clearance checks
- occupancy and carve-space evaluation
- local/world frame transforms
- bounded routing primitives
- geometry-derived facts handed to verification and coordination

## 2. Current Repo Anchors
- `scripts/vitruvius/spatial/schema.py` already validates spatial payload shape
- `scripts/vitruvius/spatial/contract_reader.py` already enforces the SHA-256 footer contract emitted by TypeScript
- `scripts/vitruvius/spatial/spatial_edge_builder.py` and `proximity_jump.py` already provide adjacency/distance primitives
- `scripts/vitruvius/engine_rs/core` already ships `SpatialPoint`, `Aabb`, and `LinearOctree`
- `scripts/vitruvius/engine_rs/spatial_kernels` already holds pure compute kernels

## 3. Planned Code Locations
- Python orchestration and parity logic: `scripts/vitruvius/aec/spatial/`
- Rust compute extensions: `engine_rs/core`, `engine_rs/spatial_kernels`, and `engine_rs/pyo3_shim`
- TypeScript schema/export updates only when the boundary contract needs them

Rule:
- do not create a second spatial system beside the existing Python/Rust/TypeScript split

## 4. Responsibilities
- compact compute DTOs with explicit units and frame IDs
- deterministic clash and clearance primitives
- occupancy metrics and carve-space facts
- routing primitives bounded to building-scale use cases
- geometry fact export for Z3 and coordination

## 5. Boundaries
- must not interpret law
- must not own orchestration flow
- must not emit user-facing prose
- must not absorb pricing or business semantics
- must not widen into full FEA or CFD without a new approved plan

## 6. Inputs / Outputs

### Inputs
- ECS snapshots
- boundary-admitted geometry DTOs
- explicit frame metadata
- explicit units and tolerance policy

### Outputs
- clash/clearance results
- occupancy summaries
- route candidates
- geometry-derived verification facts
- deterministic audit artifacts for replay

## 7. Data Contracts
- FFI-safe compute DTOs only
- every geometry payload must carry `frame_id` and units
- `f64` at the boundary unless a justified numeric policy says otherwise
- tolerance policy must be declared per operation class
- TypeScript payload schema version and Python reader expectations must remain in parity

## 8. Dependencies
- AEC master plan
- ECS core plan
- boundary translation plan
- cross-language boundary contract
- Rust boundary and benchmarking rules

## 9. Ordered Implementation Steps
1. Freeze spatial compute DTOs and parity fixtures.
2. Reuse the existing spatial contract footer model as the import/export integrity baseline.
3. Build a Python reference path for clash, clearance, and occupancy on bounded fixtures.
4. Extend `engine_rs/core` or `spatial_kernels` only for hot loops justified by measurement.
5. Maintain Python ↔ Rust parity tests for every accelerated operation.
6. Reuse `proximity_jump.py` as the style precedent for routing-like neighborhood queries before adding new algorithms.
7. Add benchmark harnesses before widening the geometry workload.

## 10. Edge Cases
- degenerate geometry
- near-touching objects at tolerance boundaries
- frame mismatch across imported payloads
- large coordinates causing precision loss
- static/dynamic index thrashing under repeated updates

## 11. Risks
- Python dict-shaped payload slop crossing into Rust
- TypeScript schema drift from Python readers
- benchmark-free performance claims
- geometry-heavy solver behavior leaking into Z3

## 12. Validation Plan

### Existing Tests To Reuse
- `python -m pytest scripts/tests/test_spatial_schema.py`
- `python -m pytest scripts/tests/test_spatial_contract_reader.py`
- `python -m pytest scripts/tests/test_spatial_edge_builder.py scripts/tests/test_spatial_edge_builder_parity.py`
- `python -m pytest scripts/tests/test_spatial_cli.py`
- `cargo test --workspace` from `scripts/vitruvius/engine_rs/`
- `npm test && npm run typecheck` from `spatial-daemon/`

### New Tests Required
- `scripts/tests/test_aec_spatial_contracts.py`
- `scripts/tests/test_aec_spatial_parity.py`
- `scripts/tests/test_aec_spatial_routing.py`

### Acceptance Gates
- Python and Rust agree on bounded fixture outputs
- Python reader still verifies every TypeScript-emitted footer
- frame/unit mismatches fail loudly, not silently

## 13. Performance Considerations
- separate static and dynamic spatial indices
- keep semantic metadata out of Rust hot paths
- benchmark before and after each acceleration step
- treat Wasm compatibility as a deployment surface, not as an excuse for premature abstraction

## 14. Execution Checklist
- [ ] compute DTOs frozen
- [ ] units and tolerance policies frozen
- [ ] Python reference path implemented first
- [ ] Rust acceleration sites justified by benchmarks
- [ ] TypeScript parity maintained where boundary schema changes
- [ ] new `test_aec_spatial_*` suite added

## 15. Stop Conditions
- units or tolerance remain ambiguous
- frame handling is undefined
- boundary payloads require semantically overloaded maps
- implementation tries to move policy logic or rich metadata into Rust hot loops
