---
task: aec-mepfs-backbone
phase: runtime-root-implementation-packet
created: 2026-04-25
author: CODEX
status: PACKET-PREPARED-NOT-AUTHORIZED
---

# Runtime Root Implementation Packet

## Purpose

Name the HIGH/CRITICAL KG roots and the runtime implementation constraints for a
future AEC-MEPFS Backbone slice.

This packet is separate from the readiness packet because these roots have broad
blast radius.

## Fresh Impact Evidence

Report:
`006_System-Manifests/aec-mepfs-backbone/code-impact/20260425T140845Z/runtime-root-impact-report.json`

GitNexus status:

- indexed commit: `3031a95`
- current commit: `3031a95`
- status: up to date

| Symbol | File | Risk | Direct impacts | Processes affected | Runtime decision |
|---|---|---:|---:|---:|---|
| `CanonicalNode` | `scripts/vitruvius/kg/schemas.py` | CRITICAL | 111 at depth 1 | 6 at depth 1 | avoid in first runtime slice; schema migration packet required before edit |
| `TaxonomyLoader` | `scripts/vitruvius/kg/evidence_materializer.py` | HIGH | 15 | 3 | do not replace in place; add shadow/admission path first |
| `Neo4jLoader` | `scripts/vitruvius/kg/neo4j_loader.py` | HIGH | 23 | 2 | no write-path change until rollback proof and shadow tests exist |
| `UnifiedSnapshotBuilder` | `scripts/vitruvius/kg/unified_snapshot_builder.py` | MEDIUM | 12 | 2 | preserve current MVP snapshot behavior |
| `enrich_snapshot` | `scripts/vitruvius/kg/relationship_enricher.py` | MEDIUM | 4 | 2 | keep inferred/document-derived edges separate from governed backbone edges |

`CanonicalNode` was captured at depth 1 in the generated report because the
depth-3 GitNexus output was too large to parse as valid JSON. Prior depth-3
evidence remains recorded in `code-intelligence-impact-map.md`.

## Required d=1 Runtime Obligations

Any implementation packet that edits the above symbols must explicitly update
or preserve:

- `pipeline_cli.py::main`
- `pipeline_cli.py::run_kg_pipeline`
- `UnifiedSnapshotBuilder.build`
- `canonical_graph_builder.py::add_candidates`
- `backfill_document_versions.py::backfill_canonical_sources`
- `evidence_ingestor.py::ingest`
- `relationship_enricher.py::enrich_snapshot_file`
- `scripts/tests/test_kg_schemas.py`
- `scripts/tests/test_kg_unified_snapshot_builder.py`
- `scripts/tests/test_kg_neo4j_loader.py`
- `scripts/tests/test_kg_relationship_enricher.py`
- API/Explorer parity tests before any read-path change

## First Runtime Slice Shape

The first implementation slice should be additive and shadow-only:

- no edit to `CanonicalNode`
- no `MATCH (n) DETACH DELETE n`
- no graph rebuild
- no `--reset`
- no default-on feature flag
- no source text/table/figure ingestion
- no current v1 Explorer/API behavior change

Preferred first code shape after gates close:

1. Add a new shadow backbone staging/admission module with file-backed tests.
2. Write shadow artifacts under a release/run ID, not into the live primary KG.
3. Add tests proving current MVP snapshots remain unchanged.
4. Add `/v2` or shadow-only API reads after the staging artifact exists.
5. Add Neo4j shadow writer only after rollback proof exists.

## Stop Conditions

Stop before implementation if any of these remain true:

- legal/licensing reviewer is unfilled for the intended use
- source currentness exceptions are unresolved for rows used by the slice
- canonical source admission is unsigned
- stopped/isolated rollback proof is missing
- GitNexus impact evidence is stale after the last commit
- implementation requires editing `CanonicalNode` before a schema migration
  packet exists

## Authorization Status

This packet is prepared for review. It is not accepted for runtime execution.
