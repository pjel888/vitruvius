---
task: aec-mepfs-backbone
phase: third-bounded-readiness-implementation-packet
created: 2026-04-25
author: CODEX
status: IMPLEMENTED-VALIDATED
---

# Third Bounded Readiness Implementation Packet

## Slice ID

`AEC-BB-S3`: integration readiness gate fixture and validator extension.

## Goal

Close the next local readiness gap without touching the live KG runtime:
production registry location planning, API/Explorer parity-runner planning,
rollback-proof planning, benchmark planning, and runtime-blocking gate status.

This slice keeps the project moving toward AEC-MEPFS Backbone integration while
still blocking runtime adoption until the missing external and runtime evidence
exists.

## Scope

Allowed write scope:

- `scripts/vitruvius/kg/backbone_contracts.py`
- `scripts/tests/test_kg_backbone_contracts.py`
- `scripts/tests/fixtures/aec_mepfs_backbone/valid_integration_readiness_s3.json`
- AEC-MEPFS readiness docs and validation logs

## Explicit Non-Scope

This slice did not authorize or perform:

- KG schema migration
- `CanonicalNode`, `TaxonomyLoader`, `UnifiedSnapshotBuilder`, or `Neo4jLoader`
  edits
- API or Explorer route changes
- feature-flag changes
- Neo4j writes, backup, restore, cleanup, reset, or graph reload
- raw/canonical source admission
- production registry promotion into `003_Canonical-Knowledge-Layer`
- protected standards, legal clause, table, figure, or source-text ingest

## Contract Added

The validator now checks readiness records for:

- planned registry artifact locations under allowed repo-relative prefixes
- registry location owner, lifecycle state, validator, promotion gate, and
  runtime consumer declarations
- controlled values for lifecycle state, promotion gate, validator, and runtime
  consumer declarations
- API/Explorer parity runner plan coverage for exactly `v1` and `v2`
- parity commands, assertions, fixture path, report path, and runtime report gate
- rollback proof plan, including destructive-operation block, smoke queries,
  backup artifact path, and restore evidence path
- benchmark plan, including commands, hardware baseline, repetitions, p95
  percentile reporting, thresholds, and report path
- integration readiness gates with closed/planned/blocked status counts
- open runtime-blocking gates requiring an explicit blocker reason
- closed gates requiring evidence
- Windows-safe path segments for planned report paths

## Fixture Added

`scripts/tests/fixtures/aec_mepfs_backbone/valid_integration_readiness_s3.json`
is a readiness fixture, not canonical source data and not a production registry.

It records:

- six planned registry/report locations
- a candidate API/Explorer parity runner plan
- a planned, not executed, rollback proof plan
- a benchmark plan with five repetitions and p95 reporting
- six integration readiness gates

## Gate Status After S3

Closed local gates:

- file-backed validator exists
- production registry location plan exists
- benchmark plan exists

Still blocked before runtime integration:

- API/Explorer parity runner must be implemented and produce a report
- backup/export and restore proof must be executed in a safe runtime packet
- legal/licensing reviewer decisions must be recorded
- actual runtime registry files must be steward-admitted
- canonical source files must be admitted under governance

## Validation

Focused validation:

```bash
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py -q
```

Result:

```text
35 passed
```

Consumer parity smoke:

```bash
(cd api && bun test)
(cd explorer && bun test)
```

Results:

```text
api: 18 pass, 0 fail
explorer: 35 pass, 0 fail
```

Static and syntax checks:

```bash
python3 -m json.tool scripts/tests/fixtures/aec_mepfs_backbone/valid_integration_readiness_s3.json
python3 -m compileall -q \
  scripts/vitruvius/kg/backbone_contracts.py \
  scripts/tests/test_kg_backbone_contracts.py
git diff --check
```

All passed.

Read-only Neo4j smoke:

```cypher
MATCH (n) RETURN count(n) AS nodes;
MATCH ()-[r]->() RETURN type(r) AS type, count(*) AS count ORDER BY count DESC LIMIT 10;
MATCH (n:BackboneShadow) RETURN count(n) AS shadow_nodes;
MATCH (n:CanonicalNode) RETURN count(n) AS canonical_nodes;
```

Observed:

- connectivity: true
- nodes: 2429
- top relationship types unchanged for the current MVP snapshot
- `BackboneShadow` nodes: 0
- `CanonicalNode` nodes: 313

This confirms S3 did not create or load a backbone shadow graph.

## Rollback

Rollback is clean:

- remove the S3 fixture
- remove the S3 validator sections and tests
- revert the AEC-MEPFS readiness docs

Because this slice does not touch runtime graph paths, database state, feature
flags, raw sources, canonical sources, or production registries, rollback does
not require Neo4j cleanup or graph rebuild.
