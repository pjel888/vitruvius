---
task: aec-mepfs-backbone
phase: first-bounded-implementation-packet
created: 2026-04-25
author: CODEX
status: IMPLEMENTED-VALIDATED
---

# First Bounded Implementation Packet

## Purpose

Define the first actual code slice for the AEC-MEPFS Backbone after readiness
closure. This packet is deliberately narrow because fresh GitNexus evidence
shows HIGH and CRITICAL impact roots in the current KG core.

This packet authorized only the bounded validator slice below. It did not
authorize runtime KG schema migration, Neo4j work, API/Explorer work, feature
flags, graph rebuilds, canonical content admission, or protected source ingest.

## Slice ID

`AEC-BB-S1`: static backbone contract validator.

## Goal

Add a file-backed validator for future AEC-MEPFS Backbone registry artifacts
without loading them into the current KG, Neo4j, API, Explorer, or pipeline.

The first slice should prove that candidate backbone records can be checked for
shape, IDs, predicate names, source-rights fields, owner fields, and no-vague
predicate constraints before any runtime path consumes them.

## Why This Slice Comes First

Fresh impact evidence shows:

- `CanonicalNode` is CRITICAL impact, with 315 upstream impacts and 111 direct
  dependents.
- `TaxonomyLoader` and `Neo4jLoader` are HIGH impact.
- API/Explorer graph-client surfaces are lower impact, but depend on stable v1
  behavior and parity fixtures that are not executable yet.

Therefore the first code slice must avoid schema migration, loader integration,
Neo4j mutation, API route changes, Explorer changes, and feature flags.

## Proposed Write Scope

Allowed files for the first implementation slice:

- `scripts/vitruvius/kg/backbone_contracts.py`
- `scripts/tests/test_kg_backbone_contracts.py`
- `scripts/tests/fixtures/aec_mepfs_backbone/*.json`
- optional README or fixture note under `scripts/tests/fixtures/aec_mepfs_backbone/`

The implementation should use standard-library parsing and existing project
patterns. No new dependency is allowed.

## Explicit Non-Scope

The first slice must not edit:

- `scripts/vitruvius/kg/schemas.py`
- `scripts/vitruvius/kg/evidence_materializer.py`
- `scripts/vitruvius/kg/unified_snapshot_builder.py`
- `scripts/vitruvius/kg/neo4j_loader.py`
- `scripts/vitruvius/kg/relationship_enricher.py`
- `scripts/pipeline_cli.py`
- `api/index.ts`
- `explorer/src/api/graphApi.ts`
- `config/vitruvius.yaml`
- `scripts/vitruvius/config_flags.py`
- any raw/canonical/operational data-layer artifact outside test fixtures

The first slice must not:

- rebuild the KG
- load Neo4j
- reset derived artifacts
- enable a feature flag
- admit canonical backbone content
- ingest protected standards or legal text
- create production source-rights registry rows

## Validator Contract

The validator should accept a candidate JSON object or fixture file and return a
structured report with:

- `ok`
- `errors`
- `warnings`
- `record_counts`
- `predicate_counts`
- `owner_coverage`
- `source_rights_coverage`

Minimum checks:

- every ID matches the accepted `VTN-<kind>-<7 digits>` pattern
- every governed predicate appears in the readiness predicate registry list
- `RELATED_TO`, `CONNECTED_TO`, `SIMILAR_TO`, and unqualified `affects` fail for
  governed edges
- every record has `label`, `record_type`, `owner`, and `review_status`
- every source mapping has `source_rights_class`, `clearance_state`,
  `official_url`, and `currentness_check_date`
- no record claims `content_ingest` unless `clearance_state` is
  `cleared_for_declared_use`
- jurisdiction fields are overlays/applicability, not canonical ID components

## Test Requirements

Focused tests must cover:

- valid minimal candidate fixture passes
- invalid ID fails
- vague governed predicate fails
- unknown predicate fails
- content-ingest source without clearance fails
- missing owner fails
- jurisdiction-mutated canonical ID fails
- deterministic report ordering

Suggested command:

```bash
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py
```

## Impact And Verification Commands

Before editing:

```bash
git status --short
./scripts/gitnexus_analyze.sh
npx --yes gitnexus@1.6.2-rc.10 status
```

After editing:

```bash
git diff --check
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py
npx --yes gitnexus@1.6.2-rc.10 impact backbone_contracts --repo vitruvius --direction upstream --depth 3 --include-tests || true
git status --short
git diff --name-status
```

The installed `gitnexus@1.6.2-rc.10` CLI does not expose a `detect_changes`
command. If a GitNexus MCP `detect_changes` surface is available in the later
implementation session, use it. Otherwise record the CLI limitation and use
`git status --short`, `git diff --name-status`, focused tests, and fresh
GitNexus `status`/`impact` output as the scope report.

## Acceptance Criteria

Pass:

- only the allowed files are changed
- no existing runtime import path references the new validator
- focused validator tests pass
- `git diff --check` passes
- GitNexus status/impact evidence is recorded
- no current 001-Laws Explorer/API behavior is changed

Fail:

- any KG schema, loader, pipeline, Neo4j, API, Explorer, or flag file changes
- validator imports or mutates live KG runtime types
- protected source content enters fixtures
- tests weaken or remove current behavior

## Rollback

Rollback is clean: remove the new validator module and tests. Because the slice
does not touch runtime paths, database state, feature flags, or data-layer
artifacts, rollback should not require Neo4j cleanup or graph rebuild.

## Implementation Result

Implemented on 2026-04-25:

- `scripts/vitruvius/kg/backbone_contracts.py`
- `scripts/tests/test_kg_backbone_contracts.py`
- `scripts/tests/fixtures/aec_mepfs_backbone/valid_minimal.json`

The implementation is file-backed and runtime-disconnected. It imports no KG
schemas, loaders, Neo4j clients, API modules, Explorer modules, or feature-flag
configuration.

Verification:

```bash
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py -q
python3 -m py_compile scripts/vitruvius/kg/backbone_contracts.py
git diff --check -- scripts/vitruvius/kg/backbone_contracts.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/fixtures/aec_mepfs_backbone/valid_minimal.json
```

Result: 8 focused tests passed.
