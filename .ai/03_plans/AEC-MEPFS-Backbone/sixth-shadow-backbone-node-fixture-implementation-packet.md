---
task: aec-mepfs-shadow-backbone-node-fixture
phase: 05
created: 2026-04-26
author: CODEX
status: IMPLEMENTED
supersedes: null
---

# Sixth Shadow Slice: Admitted BackboneNode Fixture

## Scope

Implement the first file-backed admitted `BackboneNode` fixture/model slice for
the AEC-MEPFS Backbone, then stage it into a shadow artifact.

This slice admits a small authored L1/L2 fixture **inside shadow staging only**.
It does not admit protected source text, does not write Neo4j, does not rebuild
the KG, and does not make AEC-MEPFS the Explorer default graph.

## Research Baseline

- `master-taxonomy-l1-l2-decision-record.md` accepts the L1/L2 review set as a
  readiness guardrail but not as broad canonical runtime data.
- `taxonomy_v2_schemas.py` already defines `BackboneNode`.
- `backbone_contracts.py` validates generic records but does not yet enforce the
  `BackboneNode` field invariants at admission status.
- `backbone_shadow_staging.py` currently stages predicate and source-rights
  registries, not admitted BackboneNode records.
- GitNexus impact for the exact symbols is LOW:
  `validate_backbone_contract`, `_validate_record`, `stage_shadow_backbone`,
  and `build_shadow_staging_consumer_report`.

## Audit Findings

- Candidate fixtures can remain loose, but any `BackboneNode` marked
  `admitted` or `steward_admitted` must satisfy the v2 model contract.
- Parent/child integrity is not currently enforced for admitted
  `BackboneNode` records.
- The first staged fixture must be tiny and authored from existing planning
  decisions, not generated from document-derived nodes.
- Existing v1 API/Explorer graph behavior must remain untouched.

## Implementation Plan

1. Add a first-slice model spec documenting required admitted BackboneNode
   fields, ID/path rules, parent integrity, and non-goals.
2. Add an admitted L1/L2 fixture under
   `scripts/tests/fixtures/aec_mepfs_backbone/`.
3. Extend `backbone_contracts.py` to enforce v2 `BackboneNode` schema only for
   admitted/steward-admitted BackboneNode records.
4. Add admitted BackboneNode integrity checks:
   ID/canonical ID match, label/preferred label match, owner/steward match,
   path depth/level match, parent path presence, parent existence, and duplicate
   path/code detection.
5. Extend shadow staging so an optional BackboneNode contract file can be
   included in the file-backed artifact and report counts.
6. Extend the consumer report and `/v2/backbone/taxonomy` preview to report
   admitted BackboneNode availability when a shadow artifact contains the
   optional node fixture.
7. Run focused Python/API/Explorer QA and generate a new shadow-staging
   manifest run from commands, not manual output edits.

## Plan Critique

- [C001] Calling the fixture "admitted" can overstate runtime truth. The slice
  must keep the admission scoped to shadow staging and docs must say no runtime
  graph cutover occurred.
- [C002] Enforcing v2 fields on all candidate records would break historical
  readiness fixtures. Only admitted/steward-admitted BackboneNode records get
  strict v2 enforcement.
- [C003] Adding BackboneNode rows to the shadow artifact must not imply source
  content admission. The fixture definitions must be authored summaries with no
  standards text, clauses, tables, figures, or document-derived rule titles.
- [C004] The Explorer route may expose the staged nodes only inside the existing
  opt-in preview. It must not route them into the operational graph store.

## Execution Checklist

- [x] Refresh GitNexus status and exact-symbol impact evidence.
- [x] Inspect existing schema, validator, staging, and tests.
- [x] Add first-slice model spec.
- [x] Add admitted BackboneNode fixture.
- [x] Implement validator and staging support.
- [x] Add focused tests.
- [x] Generate shadow-staging output via command.
- [x] Run UltraQA verification.
- [x] Update validation/state docs.
- [x] Commit, refresh GitNexus, and push.

## Implementation Result

Implemented on 2026-04-26.

- Added the first strict, file-backed admitted L1/L2 `BackboneNode` fixture at
  `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`.
- Extended `backbone_contracts.py` so only `BackboneNode` records with
  `review_status` of `admitted` or `steward_admitted` must satisfy strict v2
  `BackboneNode` schema, identity, ownership, path, level, parent, and duplicate
  checks.
- Extended shadow staging and the consumer report to accept an optional
  BackboneNode contract file and report `backbone_nodes` counts.
- Extended `GET /v2/backbone/taxonomy` and the opt-in Explorer preview to show
  staged admitted BackboneNode metadata when present.
- Generated the new shadow run
  `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T000726Z/`.

The resulting preview remains shadow-only and opt-in. No Neo4j write, KG
rebuild, protected source ingest, feature flag cutover, v1 behavior replacement,
or default Explorer adoption occurred.

## Explicit Non-Goals

- No Neo4j reset, load, dump, or write.
- No KG rebuild.
- No feature flag default change.
- No Explorer default graph replacement.
- No protected source content exposure.
- No broad L3/L4 ontology expansion.
