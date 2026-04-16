---
title: AEC Engine Traceability Matrix
type: execution-control-artifact
date: 2026-04-16
status: ACTIVE
source_audit: .ai/02_audits/AEC_ENGINE_WHOLE_CODEBASE_READINESS_AUDIT_2026-04-16.md
source_task_list: .ai/04_tasks/aec-engine-master-execution-task-list-2026-04-16.md
supersedes:
  - .ai/04_tasks/aec-engine-traceability-matrix-2026-04-16.md
---

# AEC Engine Traceability Matrix

## Purpose
This matrix is the anti-drift control surface for AEC planning. Every blocker-class audit finding must map to explicit execution tasks, frozen contracts, named tests, concrete file surfaces, and a no-go gate. If a future plan or sprint cannot be traced through this matrix, it is not safe to run.

## Authoritative Inputs
- `.ai/02_audits/AEC_ENGINE_WHOLE_CODEBASE_READINESS_AUDIT_2026-04-16.md`
- `.ai/04_tasks/aec-engine-master-execution-task-list-2026-04-16.md`
- `.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_BOUNDARY_TRANSLATION_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_KNOWLEDGE_VAULT_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_ECS_CORE_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_SPATIAL_KERNEL_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_Z3_VERIFICATION_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_MULTI_DISCIPLINARY_COORDINATION_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_FINANCIAL_PRICING_ORACLE_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_OPTIMIZATION_ENGINE_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_LLM_TOOL_CALLING_IMPLEMENTATION_PLAN.md`

## Status Rules
- `OPEN` = not yet converted into passing evidence.
- `CONTROLLED` = tasks/gates exist but implementation may not start yet.
- `READY` = all named evidence exists and the linked no-go condition is cleared.
- No row may be deleted because it is inconvenient; rows can only move from `OPEN` -> `CONTROLLED` -> `READY`.

## Finding-to-Execution Matrix

| Finding ID | Audit section(s) | Finding summary | Evidence-bearing repo surfaces | Required task IDs | Contract / freeze dependency | Required tests / validation evidence | Gate / stop linkage | Status |
|---|---|---|---|---|---|---|---|---|
| F-001 | §§2, 4, 17 | No dedicated AEC namespace exists | `scripts/vitruvius/aec/` (absent), `.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md` | AEC-T001 | namespace freeze | namespace ownership review; file-touch matrix update | stop if AEC work lands in unrelated packages before namespace freeze | READY |
| F-002 | §§2, 4, 12, 17 | No replay-safe audit/snapshot envelope exists | `scripts/vitruvius/graph/cli.py`, `scripts/vitruvius/graph/builder.py`, `scripts/vitruvius/graph/event_store.py`, `scripts/vitruvius/graph/rocksdb_event_store.py` | AEC-T002 | envelope freeze | envelope checklist; artifact identity review | stop if `latest_*`, wall-clock, or mtime identity leaks into AEC artifacts | READY |
| F-003 | §§2, 4, 10, 17 | No AEC DTO / ID / version family exists | future `scripts/vitruvius/aec/contracts/*`; `scripts/vitruvius/graph/contract.py` as precedent only | AEC-T003 | DTO / ID / version freeze | contract review; schema diff review | stop if more than one subsystem starts on soft DTOs | READY |
| F-004 | §§2, 4, 8, 10, 17 | `frame_id`, payload-level units, and tolerance policy are undefined | `scripts/vitruvius/spatial/schema.py`, `spatial-daemon/src/types.ts`, `spatial-daemon/src/contract_writer.ts`, `scripts/tests/test_spatial_contract_reader.py` | AEC-T004, AEC-T012 | boundary-v2 freeze | `test_aec_boundary_contract_parity.py`; invalid fixture set; explicit tolerance manifest review | stop if units/tolerances remain implicit or TS-owned | READY |
| F-005 | §§2, 4, 10, 12, 17 | Candidate/canonical separation is not yet enforceable for AEC truth | `scripts/vitruvius/review/stateful_registry.py`, `scripts/vitruvius/review/rocksdb_stateful_registry.py`, `003_Canonical-Knowledge-Layer/shared/relationships/*`, `006_System-Manifests/runs/latest_*` | AEC-T005, AEC-T013 | candidate/canonical freeze | vault backend parity plan; promotion-path review | stop if canonical truth inherits overwrite/purge semantics | READY |
| F-006 | §§2, 8, 17 | Dirty working tree and baseline ambiguity can corrupt planning truth | repo working tree; `.ai/01_roadmap/current-phase.md`; `.ai/01_roadmap/milestone-tracker.md` | AEC-T006 | clean baseline gate | clean `git status --short`; state reconciliation review | stop if AEC branch begins from a dirty baseline | READY |
| F-007 | §§8, 10, 12 | Live boundary ingest is legacy-tolerant and provenance-dropping | `scripts/vitruvius/spatial/contract_reader.py`, `scripts/vitruvius/spatial/walker.py`, `scripts/vitruvius/spatial/cli.py`, `scripts/tests/test_spatial_cli.py` | AEC-T007, AEC-T012 | strict-vs-legacy boundary split | TS→Python end-to-end import lane; provenance retention review | stop if AEC import silently accepts weak inputs or drops footer/provenance metadata | READY |
| F-008 | §§6, 7, 8, 12 | Current graph contract/status vocabulary is insufficient for AEC artifact law | `scripts/vitruvius/graph/contract.py`, `scripts/vitruvius/graph/physics.py`, `scripts/vitruvius/graph/snapshot.py` | AEC-T008 | contract-family decision | graph contract decision review | stop if graph node/status/evidence vocab is silently reused for AEC | READY |
| F-009 | §§9, 10, 15 | No AEC-specific benchmark doctrine exists | `scripts/vitruvius/bench/bench_rust_mig_baseline.py`, `.ai/06_specs/GOVERNANCE/06_PERFORMANCE_BUDGET_AND_BENCHMARK_POLICY.md`, `.ai/06_specs/RUST/05_RUST_TESTING_BENCHMARKING_AND_VALIDATION.md` | AEC-T009 | benchmark-policy freeze | benchmark spec with workload, wall-time, peak RSS, hardware, thresholds | stop if any Rust port is proposed without AEC-specific benchmark evidence | READY |
| F-010 | §§9, 10, 15 | Cross-language parity matrix is incomplete | `spatial-daemon/tests/contract_writer.test.ts`, `scripts/tests/test_spatial_contract_reader.py`, `scripts/tests/test_spatial_edge_builder_parity.py`, `scripts/tests/test_mahalanobis_parity.py` | AEC-T010, AEC-T021 | parity doctrine | named parity matrix covering TS↔Python and Python↔Rust seams | stop if any seam remains informal | CONTROLLED |
| F-011 | §§9, 11, 15 | Replay / fixture corpus for AEC does not exist | future `scripts/tests/fixtures/aec/**`; current fixtures as precedent only | AEC-T011 | replay-fixture freeze | fixture catalog with sat/unsat/refusal/timeout/legacy/strict cases | stop if replay tests are planned without frozen fixtures | CONTROLLED |
| F-012 | §§6, 8, 9 | TypeScript boundary is real but too narrow for AEC v2 and already drifts on metadata | `spatial-daemon/src/cli.ts`, `spatial-daemon/src/types.ts`, `spatial-daemon/src/contract_writer.ts`, `scripts/tests/fixtures/spatial/sample_residential_01_spatial.json` | AEC-T012, AEC-T021 | boundary-v2 freeze | TS→Python parity suite; metadata vocabulary review | stop if TS gains policy/orchestration authority | CONTROLLED |
| F-013 | §§4, 7, 10, 12 | No AEC vault/admission surface exists | future `scripts/vitruvius/aec/vault/*`; `scripts/vitruvius/promotion_validator.py` as precedent only | AEC-T013 | truth-governance freeze | `test_aec_vault_backend_parity.py`; promotion/refusal design review | stop if mutable caches are treated as vault law | CONTROLLED |
| F-014 | §§4, 6, 10, 12 | ECS is only a precedent set, not a runtime AEC substrate | future `scripts/vitruvius/aec/ecs/*` | AEC-T014 | namespace + envelope + DTO freezes | `test_aec_ecs_contract.py`; `test_aec_ecs_replay.py`; `test_aec_ecs_schedule.py` | stop if ECS is proposed Rust-first or without replay evidence | CONTROLLED |
| F-015 | §§4, 8, 10, 12 | Spatial foundation must begin as Python reference, not Rust-first | future `scripts/vitruvius/aec/spatial/*`; `scripts/vitruvius/spatial/spatial_edge_builder.py`; `scripts/vitruvius/spatial/proximity_jump.py`; `scripts/vitruvius/engine_rs/spatial_kernels/*` | AEC-T015 | Python-reference-first freeze | `test_aec_spatial_contracts.py`; `test_aec_spatial_parity.py`; benchmark harness | stop if kernel migration happens before Python reference behavior and thresholds | CONTROLLED |
| F-016 | §§4, 10, 12 | Z3 precedent is narrow; raw prose or geometry-heavy search would be misuse | future `scripts/vitruvius/aec/verification/*`; `scripts/vitruvius/spatial/constraint_solver.py` as precedent only | AEC-T016 | AST whitelist + refusal freeze | `test_aec_z3_replay.py`; `test_aec_z3_refusals.py`; artifact-schema review | stop if raw prose or unbounded geometry enters solver | CONTROLLED |
| F-017 | §§4, 10, 12 | Coordination precedent is invalidation-only and not replay-grade | future `scripts/vitruvius/aec/coordination/*`; `scripts/vitruvius/compound/dependency_tracker.py`; `scripts/vitruvius/compound/differential_propagator.py` as precedent only | AEC-T017 | coordination replay freeze | `test_aec_coordination_replay.py`; escalation/oscillation fixtures | stop if coordination lacks persisted replay/audit log | CONTROLLED |
| F-018 | §§4, 10, 12 | Pricing and optimization are downstream-only and semantics-heavy | future `scripts/vitruvius/aec/pricing/*`; future `scripts/vitruvius/aec/optimization/*` | AEC-T018 | Python-reference-first freeze | `test_aec_pricing_refusals.py`; `test_aec_optimization_replay.py` | stop if pricing/optimization bless unverified or non-canonical inputs | CONTROLLED |
| F-019 | §§4, 10, 12 | LLM/tooling must remain downstream of deterministic artifacts | future `scripts/vitruvius/aec/tools/*`; `scripts/vitruvius/query/nl_translator.py`; `scripts/vitruvius/review/ontology_prompt_builder.py` as negative precedents | AEC-T019 | refusal/audit freeze | `test_aec_tools_refusals.py`; tool-catalog review | stop if raw vault/rule/candidate payloads are sent directly to LLMs | CONTROLLED |
| F-020 | §§15, 18 | First implementation slice must remain narrow and non-heroic | future slice plan + checklist | AEC-T020 | all upstream freezes | first-sprint template completion; slice-specific fixture set | stop if first slice spans multiple downstream subsystems | CONTROLLED |
| F-021 | §§9, 15, 18 | Backend duality is allowed only where explicit law exists | future AEC cache/vault backends; current SQLite/RocksDB review stores as precedent only | AEC-T010A, AEC-T013 | backend law freeze | backend parity suite; migration/idempotency proof | stop if backend duality is assumed for canonical truth without law | CONTROLLED |
| F-022 | §§17, 18 | Stop conditions must be executable controls, not soft prose | all future AEC planning and validation logs | AEC-T020A, AEC-T022 | stop-condition freeze | gate-check package; stop-condition checklist | stop if blocker-class conditions are downgraded to warnings | CONTROLLED |

## Minimum Named Test Families
- `scripts/tests/test_aec_boundary_contract_parity.py`
- `scripts/tests/test_aec_ecs_replay.py`
- `scripts/tests/test_aec_spatial_parity.py`
- `scripts/tests/test_aec_vault_backend_parity.py`
- `scripts/tests/test_aec_z3_replay.py`
- `scripts/tests/test_aec_coordination_replay.py`
- `scripts/tests/test_aec_pricing_refusals.py`
- `scripts/tests/test_aec_optimization_replay.py`
- `scripts/tests/test_aec_tools_refusals.py`

## Control Checks
- Every new AEC task must cite at least one `Finding ID` from this matrix.
- Every contract freeze must point to a row in this matrix and to a task in the master execution list.
- No implementation-ready claim is valid unless the relevant row status is `READY` and the linked gate says `passed`.

## Failure Modes If Ignored
- architecture drift: subsystems start from different assumptions
- truth-governance leak: mutable caches become de facto canonical truth
- replay/determinism leak: artifacts depend on wall clock, mtime, or `latest_*` aliases
- premature Rust migration: benchmark doctrine is bypassed by enthusiasm
- TypeScript orchestration creep: emitter becomes a second authority plane
