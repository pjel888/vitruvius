---
task: aec-mepfs-backbone
phase: s6-source-admission-candidates
created: 2026-04-25
author: CODEX
status: CANDIDATE-NOT-STEWARD-ADMITTED
---

# Source Admission Checklist

## Purpose

This checklist converts the accepted source pack into concrete admission rows
that a human steward, legal/licensing reviewer, and later runtime packet can
accept, reject, or defer.

It is not source admission. It authorizes no protected-content ingest, canonical
source materialization, Neo4j write, runtime loader, API route, Explorer route,
or feature flag.

## Candidate Artifacts

| Artifact | Path | Status |
|---|---|---|
| Predicate registry candidate | `.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/predicate-registry.json` | candidate, validator-ready |
| Source-rights registry candidate | `.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json` | candidate, validator-ready |
| S6 validation report | `006_System-Manifests/aec-mepfs-backbone/registry-candidates/20260425T133000Z/registry-candidate-validation-report.json` | generated evidence after validation |

## Required Human Decisions Before Promotion

Every row must have these decisions before it can become a steward-admitted
runtime registry row:

- source steward decision: accept, reject, or defer
- legal/licensing reviewer decision when use exceeds reference or metadata
  crosswalk
- currentness decision from the official source URL
- declared-use boundary accepted exactly as written or revised
- update cadence accepted
- blocking notes resolved or intentionally preserved as blockers

## Promotion Rules

Pass:

- every source row validates against `validate_backbone_contract_file`
- every predicate row validates against `validate_backbone_contract_file`
- runtime consumer remains `none_until_integration_packet`
- no row claims `content_ingest`
- no row claims `cleared_for_declared_use`
- no protected standards text, legal clauses, tables, figures, or dataset caches
  are present

Fail:

- any candidate file is consumed by runtime code
- any source row is promoted without source steward acceptance
- any row escalates beyond reference/crosswalk without legal/licensing reviewer
  evidence
- any government or standards PDF is treated as automatically redistributable
- any hazard dataset is treated as legal obligation by itself

## First-Wave Admission Blocks

| Blocker | Effect |
|---|---|
| Legal/licensing reviewer is unfilled | protected content and local caching remain blocked |
| Independent second reviewer is unfilled | L1/L2 and major architecture admission remain blocked |
| PH legal/code reviewer is unfilled | Philippines legal overlay admission remains blocked |
| Stopped/isolated rollback proof is not executed | graph mutation and cleanup remain blocked |
| Runtime impact packet does not exist | `CanonicalNode`, `TaxonomyLoader`, `Neo4jLoader`, API, and Explorer wiring remain blocked |

## S6 Boundary

S6 closes only the local "candidate rows exist and validate" preparation gate.
It does not close steward admission, legal clearance, canonical source
admission, or runtime integration.
