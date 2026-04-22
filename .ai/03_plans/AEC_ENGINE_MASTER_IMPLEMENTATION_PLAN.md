---
title: AEC Engine Master Implementation Plan
type: plan
task: aec-engine-master
phase: "05"
status: planned
created: 2026-04-16
last_updated: 2026-04-22
planned_python_namespace: scripts/vitruvius/aec
planned_rust_extension_points:
  - scripts/vitruvius/engine_rs/core
  - scripts/vitruvius/engine_rs/spatial_kernels
  - scripts/vitruvius/engine_rs/pyo3_shim
planned_typescript_boundary: spatial-daemon
derived_from:
  - .ai/13_research/AEC-ECS-SC_RESEARCH.md
related_audit:
  - .ai/02_audits/AEC_ENGINE_RESEARCH_TO_PLAN_AUDIT_2026-04-15.md
  - .ai/02_audits/AEC_ENGINE_PLAN_CRITIQUE_2026-04-15.md
  - .ai/02_audits/WHOLE_CODEBASE_PLAN_LAYER_AUDIT_2026-04-16.md
governing_inputs:
  - AGENTS.md
  - .ai/00_system/EXECUTION_LOOP.md
  - .ai/00_system/principles.md
  - .ai/01_roadmap/master-roadmap.md
  - .ai/01_roadmap/current-phase.md
  - .ai/01_roadmap/milestone-tracker.md
  - .ai/06_specs/GOVERNANCE/01_VALIDATION_PROTOCOL.md
  - .ai/06_specs/GOVERNANCE/04_CROSS_LANGUAGE_BOUNDARY_CONTRACT.md
  - .ai/06_specs/GOVERNANCE/05_TRUTH_GOVERNANCE_AND_PROMOTION_CONTRACT.md
  - .ai/06_specs/GOVERNANCE/06_PERFORMANCE_BUDGET_AND_BENCHMARK_POLICY.md
  - .ai/06_specs/GOVERNANCE/07_RESEARCH_TO_PLAN_CONVERSION_STANDARD.md
  - .ai/06_specs/RUST/01_RUST_OPERATING_CONTRACT_FOR_CODEX.md
  - .ai/06_specs/RUST/04_RUST_ARCHITECTURE_AND_BOUNDARY_RULES.md
  - .ai/06_specs/RUST/05_RUST_TESTING_BENCHMARKING_AND_VALIDATION.md
  - .ai/06_specs/AEC_ENGINE/00_README_AEC_ENGINE_DOC_SET.md
  - .ai/06_specs/AEC_ENGINE/10_AEC_ENGINE_TASK_TEMPLATE.md
repo_grounding:
  - scripts/pipeline_cli.py
  - scripts/vitruvius/spatial/cli.py
  - scripts/vitruvius/spatial/constraint_solver.py
  - scripts/vitruvius/geometric/inequality_compiler.py
  - scripts/vitruvius/geometric/pareto_optimizer.py
  - scripts/vitruvius/graph/event_store.py
  - scripts/vitruvius/review/stateful_registry.py
  - scripts/vitruvius/compound/adversarial.py
  - scripts/vitruvius/query/engine.py
  - spatial-daemon/src/contract_writer.ts
  - scripts/vitruvius/spatial/contract_reader.py
---

# AEC Engine Master Implementation Plan

## 1. Current State and Intent
- Task class: architecture planning and future implementation sequencing
- Repo state: between sprints
- Current truth: the AEC engine is not implemented in runtime code yet
- This plan therefore governs future implementation only
- This master plan remains planned and acts as the sequencing authority if a bounded AEC implementation lane is explicitly reopened later.

## 2. Why This Plan Exists In This Repo
Vitruvius already contains many precursor capabilities the AEC engine must build on rather than duplicate:
- lazy CLI orchestration in `scripts/pipeline_cli.py`
- file-based spatial intake and Z3 evaluation in `scripts/vitruvius/spatial/*`
- graph/event replay patterns in `scripts/vitruvius/graph/*`
- stateful registry and RocksDB factory patterns in `scripts/vitruvius/review/*`
- deterministic compound coordination patterns in `scripts/vitruvius/compound/*`
- narrow optimization precedent in `scripts/vitruvius/geometric/pareto_optimizer.py`
- hardened Rust compute surfaces in `scripts/vitruvius/engine_rs/*`
- a file-contract TypeScript boundary in `spatial-daemon/`

The AEC engine must enter the repo as a new bounded subsystem that reuses those patterns.
It must not sprawl across existing packages by convenience.

## 3. Planned Code Locations and Ownership

### 3.1 Planned Python Namespace
Unless a later approved plan explicitly supersedes this, all new AEC orchestration code should live under:
- `scripts/vitruvius/aec/`

Planned Python subpackages:
- `scripts/vitruvius/aec/contracts/`
- `scripts/vitruvius/aec/boundary/`
- `scripts/vitruvius/aec/vault/`
- `scripts/vitruvius/aec/ecs/`
- `scripts/vitruvius/aec/spatial/`
- `scripts/vitruvius/aec/verification/`
- `scripts/vitruvius/aec/coordination/`
- `scripts/vitruvius/aec/optimization/`
- `scripts/vitruvius/aec/pricing/`
- `scripts/vitruvius/aec/tools/`

### 3.2 Planned Rust Extension Points
Rust remains a selective acceleration layer only.

First-choice extension points:
- `scripts/vitruvius/engine_rs/core`
- `scripts/vitruvius/engine_rs/spatial_kernels`
- `scripts/vitruvius/engine_rs/pyo3_shim`

Rule:
- do not create a new Rust crate until a Python reference contract exists and a benchmark justifies the split

### 3.3 Planned TypeScript Boundary
TypeScript remains isolated to `spatial-daemon/`.

Rule:
- AEC work may extend its schema/types only when the change is genuinely boundary-translation work
- TypeScript must not become a second orchestration plane

## 4. First Shippable Slice
The first AEC slice must stay narrow enough to validate deterministically inside the current repo:
- one jurisdiction snapshot at a time
- one building-scale model slice at a time
- one canonical DTO family
- one rule-vault snapshot family
- one verification whitelist
- one pricing snapshot family
- deterministic clash, clearance, envelope, quantity, and verification path only

Explicitly excluded from v1:
- full FEA
- thermal or fluid simulation
- unconstrained multi-user concurrency
- broad IFC round-trip coverage
- open-ended generative layout synthesis
- browser-facing productization

## 5. Architecture

### 5.1 Layer Responsibilities
- `Boundary Translation`
  - imports IFC/CAD/OWL-like payloads into canonical AEC DTOs
  - exports audit-safe boundary payloads
  - owns schema mediation, not truth
- `Knowledge Vault`
  - stores candidate and canonical rule ASTs, provenance, temporal snapshots, and admitted machine-facing rule payloads
- `ECS Core`
  - owns canonical world state, entity/component identity, deterministic snapshots, and schedule order
- `Spatial Kernel`
  - owns geometry-heavy compute, clash/clearance, occupancy, transforms, and routing primitives
- `Z3 Verification`
  - compiles whitelisted AST rules and candidate state into bounded formal queries
- `Coordination`
  - owns cross-discipline issue aggregation, precedence, escalation, and replay logs
- `Pricing`
  - owns pricebook snapshots, quantity scoring, and cost payloads
- `Optimization`
  - owns deterministic score vectors, Pareto selection, and any later bounded search
- `LLM Tools`
  - own intent translation, tool routing, refusal, and explanation

### 5.2 Core Boundaries
- Python owns orchestration and machine-contract assembly.
- Rust owns compute kernels only.
- TypeScript owns file-based spatial export only.
- Z3 adjudicates compiled constraints only.
- The vault stores admitted rule payloads only; it does not execute code.
- Optimization proposes; verification accepts or rejects.
- LLM tools route and explain; they do not decide compliance.

## 6. Current Repo Anchors By Concern

| Concern | Existing repo anchors | Planning consequence |
|---|---|---|
| CLI orchestration | `scripts/pipeline_cli.py` | future AEC commands must use lazy imports and should not pollute default `run` |
| Spatial file intake | `scripts/vitruvius/spatial/cli.py`, `walker.py`, `schema.py` | boundary translation must extend existing spatial contract patterns |
| Formal solving precedent | `spatial/constraint_solver.py`, `geometric/inequality_compiler.py` | AEC verification should reuse lazy z3 import and fixture-first validation discipline |
| Deterministic storage/replay | `graph/event_store.py`, `graph/rocksdb_event_store.py`, `review/stateful_registry.py` | vault storage should follow append-only + backend-factory patterns |
| Cross-language integrity | `spatial-daemon/src/contract_writer.ts`, `spatial/contract_reader.py` | boundary translation must preserve footer parity and schema versioning |
| Coordination patterns | `compound/dependency_tracker.py`, `compound/differential_propagator.py`, `query/engine.py` | AEC coordination should reuse deterministic invalidation and evidence-query idioms |
| Optimization precedent | `geometric/pareto_optimizer.py` | AEC optimization should begin deterministic and small before any stochastic search |
| Rust kernels | `engine_rs/core`, `spatial_kernels`, `pyo3_shim` | accelerate only frozen compute DTOs and hot loops |

## 7. Subsystem Matrix

| Subsystem | Owns | Must not own | Main repo anchors |
|---|---|---|---|
| ECS Core | entity/component schema, world revisions, schedule order | legal interpretation, IFC semantics, pricing | `graph/contract.py`, `compound/dependency_tracker.py`, `engine_rs/core` |
| Spatial Kernel | clash, clearance, occupancy, routing, transforms | legal truth, pricing, prose | `spatial/*`, `engine_rs/core`, `spatial_kernels`, `spatial-daemon/` |
| Knowledge Vault | rule ASTs, provenance, temporal snapshots | runtime code execution, geometry solving | `graph/event_store.py`, `review/stateful_registry.py`, `kv_migrate.py` |
| Z3 Verification | AST compiler, sat/unsat, witness artifacts | raw prose parsing, heavy geometry compute | `spatial/constraint_solver.py`, `geometric/inequality_compiler.py` |
| Coordination | conflict registry, precedence, escalation, replay | free-form LLM negotiation, pricing authority | `compound/*`, `query/engine.py`, `graph/physics.py` |
| Optimization | score vectors, Pareto frontier, bounded search | final acceptance authority, raw law | `geometric/pareto_optimizer.py`, `graph/physics.py` |
| Boundary Translation | external schema mediation and audit-safe DTOs | internal truth ownership, rule inference | `spatial/schema.py`, `spatial/concept_mapper.py`, `ontology/ifc_registry.py`, `spatial-daemon/` |
| Pricing | pricebook snapshots, quantity scoring | policy interpretation, optimization policy | `geometric/pareto_optimizer.py` as precedent only |
| LLM Tools | routing, refusal, explanation, audit retrieval | compliance decisions, compute, pricing truth | `query/*`, `compound/adversarial.py`, `compound/dspy_compiler.py` |

## 8. Implementation Phases

### Phase 1 — Contracts and Namespace Freeze
Deliverables:
- planned namespace confirmed as `scripts/vitruvius/aec/`
- shared DTO contracts frozen
- units/frame/tolerance policy frozen
- audit artifact envelope frozen

Entry gate:
- none beyond plan acceptance

Exit gate:
- no subsystem plan still depends on an undefined DTO, frame, or tolerance contract

### Phase 2 — Boundary Translation and Knowledge Vault Foundation
Deliverables:
- boundary import/export DTOs
- rule AST schema
- provenance envelope
- candidate/canonical vault distinction

Repo anchors to reuse:
- `spatial/schema.py`
- `spatial/contract_reader.py`
- `graph/event_store.py`
- `review/stateful_registry.py`

### Phase 3 — ECS Core Baseline
Deliverables:
- Python reference ECS world state
- deterministic snapshot/replay contract
- entity/component registry

Rule:
- no Rust ECS acceleration before the Python reference contract passes replay fixtures

### Phase 4 — Spatial Kernel Baseline
Deliverables:
- compute DTOs
- clash/clearance primitives
- occupancy and routing baseline
- Rust parity harness where justified

Repo anchors to reuse:
- `spatial_edge_builder.py`
- `proximity_jump.py`
- `engine_rs/core`
- `engine_rs/spatial_kernels`

### Phase 5 — Z3 Verification Baseline
Deliverables:
- whitelisted AST-to-Z3 compiler
- witness/unsat artifact schema
- replay harness

Repo anchors to reuse:
- `spatial/constraint_solver.py`
- `geometric/inequality_compiler.py`

### Phase 6 — Coordination Baseline
Deliverables:
- discipline request schema
- conflict registry
- deterministic precedence and escalation logic
- replayable coordination log

### Phase 7 — Pricing Baseline
Deliverables:
- pricebook snapshot schema
- quantity-to-price scoring contract
- verified-candidate cost payload

### Phase 8 — Optimization Baseline
Deliverables:
- deterministic objective vector
- Pareto frontier builder
- optional later seeded search behind explicit gate

### Phase 9 — Tool Layer and Integration
Deliverables:
- bounded tool schemas
- refusal taxonomy
- explanation payloads
- integration path from translation through optimization without authority leakage

## 9. Dependency Graph
- Boundary Translation depends on frozen DTOs and schema policy.
- Knowledge Vault depends on DTOs, provenance policy, and truth-governance rules.
- ECS Core depends on DTOs and vault-admitted inputs.
- Spatial Kernel depends on ECS snapshots, frame/tolerance policy, and cross-language contracts.
- Z3 Verification depends on vault ASTs, ECS state, and spatial precomputed facts.
- Coordination depends on ECS, Spatial, Z3, and vault snapshots.
- Pricing depends on verified candidate outputs and quantity facts from ECS/spatial.
- Optimization depends on Coordination and Pricing, and every candidate must round-trip through Verification.
- LLM Tools depend on all lower layers but own none of their authority.

## 10. Validation Strategy

### 10.1 Python Validation
Use existing surfaces as precedent and extend them:
- `python -m pytest scripts/tests/test_features.py`
- `python -m pytest scripts/tests/test_spatial_constraint_solver.py scripts/tests/test_geometric_inequality_compiler.py`
- `python -m pytest scripts/tests/test_spatial_contract_reader.py scripts/tests/test_spatial_cli.py`
- `python -m pytest scripts/tests/test_graph_event_store.py scripts/tests/test_graph_event_store_delta.py scripts/tests/test_temporal_query.py`
- `python -m pytest scripts/tests/test_query_engine.py scripts/tests/test_graphrag_router.py`

### 10.2 Rust Validation
From `scripts/vitruvius/engine_rs/`:
- `cargo test --workspace`

Rule:
- any new AEC Rust kernel must add parity tests against the Python reference path before benchmark claims count

### 10.3 TypeScript Validation
From `spatial-daemon/`:
- `npm test`
- `npm run typecheck`

### 10.4 New AEC Test Families To Add
- `scripts/tests/test_aec_*`
- keep them split by subsystem, not one monolithic integration blob
- add cross-language parity tests only at the actual boundary seams

## 11. Performance Strategy
- stay Python-first until contracts are frozen and hot paths are measured
- use Rust only for compute kernels with benchmark evidence
- treat RocksDB as a storage implementation detail behind a stable factory
- do not claim performance wins without a reproducible harness and artifact
- do not widen `pipeline_cli.py` imports or default paths with heavyweight AEC dependencies

## 12. Stop Conditions
- the planned `scripts/vitruvius/aec/` namespace is not accepted but implementation starts anyway
- any subsystem tries to own law, pricing, or orchestration inside Rust
- TypeScript is asked to become a live authority rather than a boundary emitter
- raw legal prose is fed directly into Z3 at runtime
- optimization is started before verification artifacts and replay are stable
- any new AEC command is wired into default `run` before the subsystem is stable and lazy-loaded

## 13. Completion Criteria
The AEC plan family is implementation-ready only when:
- namespace and boundary ownership are frozen
- every subsystem plan names real repo anchors and validation surfaces
- every subsystem has explicit stop conditions
- the integration path is deterministic and auditable on one bounded slice
- pricing and optimization remain downstream of verification
