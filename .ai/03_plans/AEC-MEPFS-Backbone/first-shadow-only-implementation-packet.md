---
task: aec-mepfs-backbone
phase: first-shadow-only-implementation-packet
created: 2026-04-25
author: CODEX
status: IMPLEMENTED-AND-VALIDATED
---

# First Shadow-Only Implementation Packet

## Decision Basis

The S8 human inbox packet is answered by project-owner directive captured on
2026-04-25T15:39:12Z. Approval is bounded to the declared conservative use:

- no protected content ingest
- no live Neo4j mutation
- no primary graph promotion
- no default-on runtime cutover
- no graph rebuild/reset/cleanup
- first implementation work remains additive and shadow-only

## Authorized First Slice

Implement a file-backed shadow staging surface for AEC-MEPFS Backbone registry
and source metadata.

The first slice may:

- read the S6 predicate and source-rights candidate files
- validate them with the existing backbone contract validators
- materialize a local shadow staging artifact under an operational or manifest
  path
- preserve source IDs, predicate IDs, allowed-use classes, and no-ingest
  boundaries
- expose deterministic report fields for later parity/rollback evidence
- add focused tests for validator and staging behavior

The first slice must not:

- edit `CanonicalNode`
- edit `TaxonomyLoader`
- edit `Neo4jLoader`
- write to Neo4j
- create canonical source content files
- ingest protected source text, clauses, tables, figures, standards content,
  hazard datasets, or source copies
- flip runtime feature flags
- route API or Explorer consumers to backbone data
- change the current MVP graph

## Expected Write Scope

The preferred implementation scope is additive:

- `scripts/vitruvius/kg/` for a small shadow-staging module, if needed
- `scripts/tests/` for focused unit tests
- `006_System-Manifests/aec-mepfs-backbone/` for generated validation reports
- `.ai/03_plans/AEC-MEPFS-Backbone/` and `.ai/05_logs/` for implementation
  evidence updates

Avoid shared KG runtime roots unless a fresh impact map explicitly justifies the
touchpoint.

## Required Impact Checks Before Code

Run GitNexus impact/context before modifying any symbol. Stop and re-plan if
the implementation needs any HIGH or CRITICAL root.

Known roots to avoid in the first slice:

- `CanonicalNode`: CRITICAL
- `TaxonomyLoader`: HIGH
- `Neo4jLoader`: HIGH

## Verification Contract

Minimum focused verification:

- JSON validation for affected registry/source/inbox artifacts
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py`
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_parity_runner.py`
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_rollback_preflight.py`
- read-only Neo4j smoke proving the live graph was not mutated, when Neo4j is
  available
- GitNexus detect/status after commit

Explorer/API verification is required only if the first slice touches Explorer,
API, or parity-route surfaces.

## Implementation Result

Implemented by:

- `scripts/vitruvius/kg/backbone_shadow_staging.py`
- `scripts/tests/test_kg_backbone_shadow_staging.py`

Generated evidence:

- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260425T154000Z/shadow-staging-report.json`
- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260425T154000Z/shadow-backbone-staging.json`

The report stages 12 predicate registry rows and 29 source-rights registry rows
with `shadow_only: true`, `file_backed_only: true`, and all live runtime
mutation/cutover boundaries set to false.

## Runtime Status After This Packet

This packet implements the first shadow-only implementation slice.

It does not authorize live runtime cutover, primary graph replacement, protected
content ingest, canonical content admission, or broad AEC backbone runtime
integration.
