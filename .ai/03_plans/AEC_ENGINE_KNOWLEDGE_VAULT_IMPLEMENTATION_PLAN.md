---
title: AEC Engine Knowledge Vault Implementation Plan
type: subsystem-plan
task: aec-engine-knowledge-vault
phase: "05"
status: accepted
created: 2026-04-16
last_updated: 2026-04-16
planned_code_locations:
  - scripts/vitruvius/aec/vault/schema.py
  - scripts/vitruvius/aec/vault/store.py
  - scripts/vitruvius/aec/vault/projection.py
  - scripts/vitruvius/aec/vault/provenance.py
planned_artifact_locations:
  - 005_Operational-Intelligence-Layer/aec/
  - 006_System-Manifests/cache/aec_rule_vault.sqlite
  - 006_System-Manifests/cache/aec_rule_vault.rocksdb
repo_grounding:
  - scripts/vitruvius/graph/event_store.py
  - scripts/vitruvius/graph/rocksdb_event_store.py
  - scripts/vitruvius/review/stateful_registry.py
  - scripts/vitruvius/review/rocksdb_stateful_registry.py
  - scripts/vitruvius/kv_migrate.py
  - scripts/vitruvius/promotion_validator.py
  - scripts/vitruvius/graph/contract.py
governing_inputs:
  - .ai/06_specs/AEC_ENGINE/04_KNOWLEDGE_VAULT_AND_RULE_AST_CONTRACT.md
  - .ai/06_specs/AEC_ENGINE/08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md
  - .ai/06_specs/GOVERNANCE/05_TRUTH_GOVERNANCE_AND_PROMOTION_CONTRACT.md
  - .ai/06_specs/GOVERNANCE/01_VALIDATION_PROTOCOL.md
---

# AEC Engine Knowledge Vault Implementation Plan

## 0. Planning Status
- status: accepted
- execution role: downstream / not in first slice
- current use: authoritative subsystem plan paired with the accepted T013 foundation plan

## 1. Scope
Create the machine-admitted rule vault for AEC execution:
- candidate and canonical rule AST storage
- provenance bundles
- temporal snapshots
- read/query surfaces for downstream ECS and verification work

This is not a replacement for the canonical human knowledge layer.

## 2. Current Repo Anchors
- `graph/event_store.py` and `graph/rocksdb_event_store.py` already show append-only replayable storage patterns
- `review/stateful_registry.py` and its RocksDB variant already show feature-gated backend factories
- `kv_migrate.py` already shows migration discipline between SQLite and RocksDB stores
- `promotion_validator.py` already shows how the repo enforces admission gates instead of trusting raw candidates

## 3. Planned Code and Artifact Locations

### Code
- `scripts/vitruvius/aec/vault/schema.py`
- `scripts/vitruvius/aec/vault/store.py`
- `scripts/vitruvius/aec/vault/projection.py`
- `scripts/vitruvius/aec/vault/provenance.py`

### Artifacts
- machine-facing exported snapshots: `005_Operational-Intelligence-Layer/aec/`
- mutable store backends and caches: `006_System-Manifests/cache/`

Rule:
- human-authored canonical law stays in layer 3
- machine-admitted ASTs and snapshot projections live in layers 5/6

## 4. Responsibilities
- AST schema and versioning
- candidate vs canonical separation
- provenance and source linkage
- temporal validity (`effective_from`, `effective_to`)
- read-only snapshot projection for downstream consumers

## 5. Boundaries
- must not execute code from stored payloads
- must not store opaque free-form LLM text as canonical rule truth
- must not own geometry solving
- must not bypass promotion/admission governance

## 6. Inputs / Outputs

### Inputs
- source-derived rule fragments
- provenance records
- jurisdiction and version metadata
- promotion/admission decisions

### Outputs
- candidate AST records
- canonical snapshot projections
- provenance manifests
- replayable vault query results

## 7. Data Contracts
- `rule_source_id`
- `rule_ast_id`
- `jurisdiction_id`
- `effective_from`
- `effective_to`
- `provenance_bundle`
- `admission_status`
- `snapshot_id`

Rule:
- AST payloads must be structured and schema-validated before storage

## 8. Dependencies
- AEC master plan
- boundary translation plan
- GOVERNANCE truth contract
- validation protocol

## 9. Ordered Implementation Steps
1. Freeze the rule AST schema and provenance envelope.
2. Implement a reference store patterned after `graph/event_store.py` and `stateful_registry.py`.
3. Separate candidate records from canonical/admitted projections.
4. Add snapshot projection logic and time-travel query surface.
5. Keep backend choice behind a factory so SQLite parity remains available even if RocksDB becomes the default.
6. Add migration support only after schema and projection are stable.

## 10. Edge Cases
- overlapping effective-date windows
- supersession without deletion
- conflicting candidate records for the same rule source
- provenance bundles missing section-level evidence
- backend mismatch between local environments

## 11. Risks
- vault becomes a dumping ground for unadmitted rule text
- backend details leak into downstream consumers
- rule identity and snapshot identity diverge
- silent truth elevation from candidate to canonical

## 12. Validation Plan

### Existing Tests To Reuse As Storage/Replay Precedent
- `python -m pytest scripts/tests/test_graph_event_store.py`
- `python -m pytest scripts/tests/test_graph_event_store_delta.py`
- `python -m pytest scripts/tests/test_temporal_query.py`
- `python -m pytest scripts/tests/test_review_stateful_registry.py scripts/tests/test_review_stateful_registry_integration.py`
- `python -m pytest scripts/tests/test_integrity_audit.py`

### New Tests Required
- `scripts/tests/test_aec_vault_schema.py`
- `scripts/tests/test_aec_vault_projection.py`
- `scripts/tests/test_aec_vault_provenance.py`
- `scripts/tests/test_aec_vault_backend_parity.py`

### Acceptance Gates
- candidate and canonical records are physically and logically separated
- the same snapshot query returns the same result on repeated runs
- backend factories preserve public behavior across SQLite and RocksDB

## 13. Performance Considerations
- keep backend selection behind a stable interface
- optimize read/query paths only after snapshot correctness is proven
- store structured payloads, not heavyweight duplicated renderings

## 14. Execution Checklist
- [ ] AST schema frozen
- [ ] provenance bundle schema frozen
- [ ] candidate/canonical separation enforced
- [ ] snapshot projection defined
- [ ] backend factory defined
- [ ] new `test_aec_vault_*` suite added

## 15. Stop Conditions
- candidate and canonical payloads are being co-mingled
- provenance requirements are undefined
- backend-specific details leak into downstream contracts
- implementation tries to store executable logic inside the vault
