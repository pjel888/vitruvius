---
task: kg-first-cleanup
phase: blast-radius-audit
created: 2026-04-29
author: CODEX
status: COMPLETE
---

# KG-First Cleanup Blast-Radius Audit

## Boundary Statement

This audit plans cleanup only. It does not authorize source-code deletion,
filesystem layer renames, KG rebuild/reload/reset, Neo4j mutation, protected
source ingest, API behavior changes, or Explorer behavior changes.

## Blast-Radius Summary

| Surface | Evidence | Risk | Cleanup disposition |
|---|---|---:|---|
| `.ai/00_system/EXECUTION_LOOP.md` | ChunkHound shows it defines the old six-layer model and identity locks. | XL | Do not rewrite casually. Create a new decision/update first, or add a KG-first overlay while preserving raw immutability. |
| `AGENTS.md` / nested AGENTS | Root still documents six layers and pipeline commands. | High | Reconcile wording after plan approval; do not remove safety rules. |
| `scripts/pipeline_cli.py` | GitNexus/OMX Explore identifies it as the legacy and dataset/KG entrypoint. | High | No deletion. First slice may update help text only with tests. Function edits require exact GitNexus impact. |
| `scripts/vitruvius/conversion.py` | Reads raw source and writes conversion artifacts. | High | Keep as source-ingestion/evidence-prep adapter. |
| `scripts/vitruvius/normalization/refine.py` | Refined markdown preparation. | Medium | Keep until source-to-node evidence pipeline supersedes it with tests. |
| `scripts/vitruvius/canonicalize.py` | Canonical source writing and old source identity flow. | High | Do not delete; reframe as optional canonical-source artifact generation. |
| `scripts/vitruvius/source_identity.py` | Maps conversion/refined paths to canonical source IDs. | High | Preserve until source attachment IDs are migrated and parity-tested. |
| `scripts/vitruvius/dataset_pipeline.py` | KG-first bridge path; contains source-to-graph orchestration. | High | Preserve and likely promote in docs as the bridge. |
| `scripts/vitruvius/kg/evidence_ingestor.py` | GitNexus impact: MEDIUM, 37 impacted symbols. | Medium | Preserve; any edit requires `test_evidence_ingestor.py` and CLI checks. |
| `scripts/vitruvius/kg/backbone_*` | Current AEC-MEPFS contracts, staging, QA, reports. | High | Preserve. This is core KG-first infrastructure. |
| `scripts/vitruvius/kg/*taxonomy*` | Current taxonomy generation/enrichment. | High | Preserve. Cleanup must not remove current taxonomy artifacts. |
| `api/index.ts` | Hosts `/v2/backbone*`, `/v2/resolve*`, Explorer graph adapters. | High | Out of scope for cleanup planning. Any later edit needs API tests. |
| `explorer/src/**` | Current AEC-MEPFS-first UI behavior and performance work. | High | Out of scope for first cleanup. Any later edit needs Explorer tests/build. |
| `001_Raw-Source-Layer/**` | Identity-locked immutable input. | XL | Never rewrite/delete in cleanup. Curators may add sources only under governed ingest. |
| `002_Raw-Conversion-Layer/**` | Derived conversion outputs. | High | Do not bulk-delete without reset protocol and tests. |
| `003_Canonical-Knowledge-Layer/**` | Legacy trusted layer plus shared source/relationship contracts. | XL | Do not rename/delete. Future role may become compatibility/evidence artifact layer. |
| `006_System-Manifests/**` | Evidence, reports, route inventories, benchmarks. | High | Do not delete logs/reports; archive/index only if necessary. |

## Keep / Reframe / Deprecate / Delete-Later

### Keep

- Current AEC-MEPFS KG/backbone modules under `scripts/vitruvius/kg/`.
- AEC-MEPFS API routes and Explorer graph behavior.
- Source-rights/currentness/admission reports.
- Evidence manifests and validation logs.
- Raw-source immutability and provenance rules.
- Tests that pin legacy conversion/canonical behavior.

### Reframe

- `001_Raw-Source-Layer` becomes source custody/input evidence, not the product
  starting point.
- `002_Raw-Conversion-Layer` becomes source extraction/staging artifacts.
- `003_Canonical-Knowledge-Layer` becomes compatibility/trusted-source artifacts
  and historical canonical source IDs, not the sole canonical truth of the KG.
- `scripts/pipeline_cli.py` remains the operator CLI but should lead with
  KG-first/source-admission language.

### Deprecate

- Docs that present raw -> conversion -> canonical as the primary future product
  strategy.
- CLI/help text that implies the old full document pipeline is the main route for
  AEC-MEPFS graph growth.
- Completed plan families listed as live work.

### Delete Later Only After Proof

- One-off smoke scripts if replaced by maintained tests.
- Superseded planning docs after archive index references exist.
- Generated derived artifacts only through explicit reset/cleanup commands.
- Dead compatibility adapters only after GitNexus reports no callers and tests
  are updated.

## Tripwires

Stop before implementation if a proposed cleanup slice:

- writes to `001_Raw-Source-Layer/**`,
- renames any numbered layer directory,
- edits `.ai/00_system/EXECUTION_LOOP.md` without a decision record/overlay plan,
- deletes validation logs or system manifests,
- changes `/v2/*` route behavior,
- changes Explorer defaults or graph rendering,
- runs KG rebuild/reload/reset,
- touches Neo4j,
- ingests or exposes protected source payloads,
- removes tests to make cleanup easier.
