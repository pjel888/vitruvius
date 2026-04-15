---
title: AEC Engine ECS Core Implementation Plan
type: subsystem-plan
status: proposed
date: 2026-04-16
last_updated: 2026-04-16
planned_code_locations:
  - scripts/vitruvius/aec/ecs/models.py
  - scripts/vitruvius/aec/ecs/world.py
  - scripts/vitruvius/aec/ecs/scheduler.py
  - scripts/vitruvius/aec/ecs/snapshot.py
repo_grounding:
  - scripts/vitruvius/graph/contract.py
  - scripts/vitruvius/graph/event_store.py
  - scripts/vitruvius/compound/dependency_tracker.py
  - scripts/vitruvius/compound/differential_propagator.py
  - scripts/vitruvius/engine_rs/core/src/lib.rs
governing_inputs:
  - .ai/06_specs/AEC_ENGINE/02_ECS_AND_COMPONENT_DESIGN_RULES.md
  - .ai/06_specs/AEC_ENGINE/08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md
  - .ai/06_specs/GOVERNANCE/04_CROSS_LANGUAGE_BOUNDARY_CONTRACT.md
  - .ai/06_specs/RUST/04_RUST_ARCHITECTURE_AND_BOUNDARY_RULES.md
---

# AEC Engine ECS Core Implementation Plan

## 1. Scope
Define the canonical in-memory world model for AEC execution:
- entity identity
- component families
- deterministic system order
- snapshot and replay semantics

This subsystem creates the authoritative runtime shape that the spatial, verification, coordination, pricing, and optimization layers consume.

## 2. Current Repo Anchors
- `scripts/vitruvius/graph/contract.py` proves the repo already prefers explicit frozen contracts over ad hoc dicts
- `scripts/vitruvius/graph/event_store.py::Delta` and `compound/differential_propagator.py` show deterministic change propagation patterns
- `scripts/vitruvius/engine_rs/core/src/lib.rs` already exposes pure compute types and is the right style for future acceleration, not the place to begin ECS semantics

## 3. Planned Code Locations
- Python reference implementation must land first under `scripts/vitruvius/aec/ecs/`
- if iteration or indexing later becomes hot, only the frozen compute subset may be mirrored into Rust

Rule:
- do not start by inventing a Rust-first ECS

## 4. Responsibilities
- canonical `entity_id`, `world_revision_id`, and `snapshot_id` policy
- component registry and family boundaries
- deterministic schedule groups and ordering
- static vs dynamic entity classification
- snapshot serialization for replay and downstream auditing

## 5. Boundaries
- must not become the rule vault
- must not absorb IFC or CAD schemas as internal truth
- must not own pricing logic
- must not interpret legal prose
- must not hide collaboration/session state inside entity payloads

## 6. Inputs / Outputs

### Inputs
- canonical DTOs admitted by the boundary layer
- rule bindings admitted by the vault
- explicit frame and units metadata

### Outputs
- deterministic world state
- frozen component snapshots
- system trace envelopes
- compact compute payloads for spatial and verification layers

## 7. Data Contracts

### Required IDs
- `world_revision_id`
- `entity_id`
- `component_family`
- `frame_id`
- `snapshot_id`

### Initial V1 Component Families
- `IdentityComponent`
- `TransformComponent`
- `TopologyRefComponent`
- `DisciplineTagComponent`
- `ConstraintBindingComponent`
- `QuantityStubComponent`
- `AuditRefComponent`

Rule:
- every component family must justify why it is not being smuggled into an existing family

## 8. Dependencies
- AEC master plan
- boundary translation plan
- knowledge vault plan
- determinism/audit rules from the AEC pack

## 9. Ordered Implementation Steps
1. Freeze world-level IDs, revision model, and snapshot envelope.
2. Implement a Python reference `World` object with deterministic insertion and iteration order.
3. Define the initial component family set and ban god-components explicitly.
4. Define schedule groups for:
   - ingest/update
   - spatial prep
   - verification prep
   - coordination prep
   - quantity extraction
5. Serialize one bounded fixture world from existing spatial fixture material such as `scripts/tests/fixtures/spatial/sample_residential_01_spatial.json`.
6. Add replay tests proving stable snapshot -> world -> snapshot round-trip.
7. Only after replay stability, consider Rust acceleration of hot compute subsets.

## 10. Edge Cases
- entities that are static in geometry but dynamic in compliance state
- world revisions that touch only one discipline
- sparse optional discipline metadata
- large coordinate values and frame switching
- partial invalidation after routing or massing changes

## 11. Risks
- god-component drift
- hidden OOP hierarchy disguised as ECS
- schema churn before snapshots stabilize
- premature Rust port before Python contracts are frozen

## 12. Validation Plan

### Existing Tests To Reuse As Style/Contract Precedent
- `python -m pytest scripts/tests/test_graph_contract.py`
- `python -m pytest scripts/tests/test_graph_event_store_delta.py`
- `python -m pytest scripts/tests/test_spatial_bootstrap.py`
- `python -m pytest scripts/tests/test_features.py`

### New Tests Required
- `scripts/tests/test_aec_ecs_contract.py`
- `scripts/tests/test_aec_ecs_replay.py`
- `scripts/tests/test_aec_ecs_schedule.py`

### Acceptance Gates
- same snapshot bytes produce same world graph and same schedule order
- component registration is explicit and lintable
- world revisions can be replayed without hidden mutable state

## 13. Performance Considerations
- keep hot components narrow and contiguous
- keep semantic metadata out of hot loops
- do not push ECS into Rust until a benchmark shows the Python reference path is the bottleneck

## 14. Execution Checklist
- [ ] planned Python ECS namespace accepted
- [ ] world and snapshot envelopes frozen
- [ ] initial component families justified and documented
- [ ] schedule groups defined
- [ ] replay fixture created
- [ ] new `test_aec_ecs_*` suite added

## 15. Stop Conditions
- component families cannot be described without semantic overload
- schedule determinism cannot be demonstrated
- implementation tries to hide rule-vault or pricing semantics inside ECS payloads
- Rust acceleration is proposed before the Python reference path is benchmarked
