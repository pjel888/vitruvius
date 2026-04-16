---
task: aec-t013-knowledge-vault-foundation
phase: 05
created: 2026-04-16
author: PLANNER
supersedes: null
status: accepted
implementation_blocked: true
planning_gate_ready: true
subsystem_ready: false
execution_role: downstream-not-selected-for-first-slice
paired_subsystem_plan: AEC_ENGINE_KNOWLEDGE_VAULT_IMPLEMENTATION_PLAN.md
gate_key: knowledge_vault
---

# AEC-T013 Knowledge Vault Foundation Plan

## Planning Status
- planning gate: ready
- execution selection: downstream / not in first bounded slice
- interpretation: planning readiness is satisfied, but execution evidence is still pending and the subsystem is not selected for the current bounded sprint

## Purpose
Resolve `AEC-T013` at the planning layer by defining the accepted vault foundation package while keeping implementation blocked.

## Required outputs
- candidate path defined: `005_Operational-Intelligence-Layer/aec/candidates/`
- canonical path defined: `005_Operational-Intelligence-Layer/aec/admitted/`
- promotion path defined: `006_System-Manifests/aec/promotions/`
- backend rules defined: mutable dual-backend support allowed only for non-canonical stores under `006_System-Manifests/cache/`
- provenance envelope and refusal behavior defined

## Required future tests
- `scripts/tests/test_aec_vault_schema.py`
- `scripts/tests/test_aec_vault_projection.py`
- `scripts/tests/test_aec_vault_provenance.py`
- `scripts/tests/test_aec_vault_backend_parity.py`

## Stop conditions
- canonical storage gets overwrite/purge semantics
- raw prose becomes runtime truth
- backend duality is assumed without explicit law
