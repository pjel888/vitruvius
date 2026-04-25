---
task: aec-mepfs-backbone
phase: readiness-code-intelligence
created: 2026-04-25
author: CODEX
status: REVIEWED-FRESH-GITNEXUS-HIGH-RISK
---

# Code-Intelligence Impact Map

## Purpose

This map names the code surfaces that a later AEC-MEPFS Backbone implementation
must impact-analyze before editing.

No code edits, graph rebuilds, feature-flag changes, or Neo4j writes are
authorized by this artifact.

## Current Evidence Status

Fresh GitNexus CLI evidence was captured on 2026-04-25 against `HEAD`
`da3569d81b14430f035c0150faf34130144b3fff`.

Code-review-graph and GitNexus MCP tools were not exposed through the available
MCP surface. The available `omx_code_intel` AST surface later returned a
transport-closed error, so symbol discovery fell back to `rg`. Impact evidence
therefore uses the project-pinned GitNexus CLI, not MCP.

R4 is closed for readiness evidence, but not for implementation approval:
`CanonicalNode` is a CRITICAL impact root and several KG runtime surfaces are
HIGH risk. Any implementation packet that edits those symbols must run
symbol-specific impact evidence again and define the d=1 update obligations.

## Fresh Index Evidence

Commands run:

```bash
./scripts/gitnexus_analyze.sh
git rev-parse HEAD
npx --yes gitnexus@1.6.2-rc.10 status
python3 -m json.tool .gitnexus/meta.json
```

Observed evidence:

- GitNexus wrapper completed successfully in 70.3s.
- Indexed commit and current commit both resolved to `da3569d`.
- `.gitnexus/meta.json` records `indexedAt:
  2026-04-25T09:29:05.106Z`.
- Index stats: 1,348 files, 11,744 nodes, 28,383 edges, 569 communities, 300
  processes, 0 embeddings.
- The unpinned `npx gitnexus --help` path failed with a package destructuring
  error. Use the pinned `gitnexus@1.6.2-rc.10` command or
  `./scripts/gitnexus_analyze.sh`.
- Because multiple repositories are indexed (`vitruvius`, `slatecamp`), impact
  commands must include `--repo vitruvius`.

## Impact Evidence Ledger

All rows used:

```bash
npx --yes gitnexus@1.6.2-rc.10 impact <symbol> --repo vitruvius --direction upstream --depth 3 --include-tests
```

| Symbol | File | Risk | Count | Direct | Process impact | Required implementation response |
|---|---|---:|---:|---:|---|---|
| `TaxonomyLoader` | `scripts/vitruvius/kg/evidence_materializer.py` | HIGH | 54 | 15 | `pipeline_cli.py::main`, `UnifiedSnapshotBuilder.build`, `run_kg_pipeline` | Do not replace in-place; first slice must add shadow/admission path or prove all direct tests and pipeline callers are updated |
| `UnifiedSnapshotBuilder` | `scripts/vitruvius/kg/unified_snapshot_builder.py` | MEDIUM | 45 | 12 | `pipeline_cli.py::main`, `run_kg_pipeline` | Preserve current MVP snapshot behavior; add shadow output only behind explicit release/run IDs |
| `CanonicalNode` | `scripts/vitruvius/kg/schemas.py` | CRITICAL | 315 | 111 | 7 processes including canonical builder, enricher, snapshot builder, ingestor, backfill, aggregate admission, CLI | Treat as implementation stop condition; first code slice should avoid changing this class unless a separate schema migration packet exists |
| `Neo4jLoader` | `scripts/vitruvius/kg/neo4j_loader.py` | HIGH | 57 | 23 | `pipeline_cli.py::main`, `run_kg_pipeline` | No Neo4j write-path changes until shadow-label, backup/restore, and loader tests are executable |
| `enrich_snapshot` | `scripts/vitruvius/kg/relationship_enricher.py` | MEDIUM | 37 | 4 | `enrich_snapshot_file`, `pipeline_cli.py::main` | Predicate/quality work must keep provenance, inferred, explicit, and steward-curated edges distinguishable |
| `enrich_snapshot_file` | `scripts/vitruvius/kg/relationship_enricher.py` | LOW | 0 | 0 | none reported | Low upstream count does not remove the `enrich_snapshot` process obligation above |
| `buildSearchTypeFilter` | `api/index.ts` | LOW | 2 | 2 | none reported | Preserve `api/perspectiveContracts.test.ts` and current v1 search semantics |
| `buildPerspectiveQueries` | `api/index.ts` | LOW | 3 | 3 | none reported | Keep perspective contracts additive until `/v2` fixtures exist |
| `getNodesForPerspective` | `explorer/src/api/graphApi.ts` | LOW | 5 | 3 | `HomeScreen`, `ExploreView` | Explorer first slice must preserve current perspective loading and graph state behavior |
| `searchNodes` | `explorer/src/api/graphApi.ts` | LOW | 1 | 1 | `CommandBar` | Preserve command/search UX and response shape |
| `FeatureFlags` | `scripts/vitruvius/config_flags.py` | LOW | 2 | 1 | none reported | Flags remain default-off; any new flag must include load/default tests |

## S3 Validator Impact Evidence

The S3 readiness-control slice edited only the file-backed validator and its
focused tests/fixtures. Fresh pre-commit CLI evidence for the edited public
validator symbol:

```bash
npx --yes gitnexus@1.6.2-rc.10 status
npx --yes gitnexus@1.6.2-rc.10 impact validate_backbone_contract \
  -r vitruvius \
  --direction upstream \
  --depth 3 \
  --include-tests
```

Observed on 2026-04-25 before commit:

- indexed commit: `2e59867`
- current commit: `2e59867`
- status: up to date
- symbol: `scripts/vitruvius/kg/backbone_contracts.py::validate_backbone_contract`
- risk: CRITICAL
- impacted count: 34
- direct impacts: 31
- affected processes: 0
- affected modules: `Tests`, `Kg`

Disposition: accepted for S3 because the symbol is runtime-disconnected,
affected processes are zero, and direct impacts are validator tests plus
`validate_backbone_contract_file`. This does not relax the HIGH/CRITICAL gate
for KG runtime roots.

## Direct d=1 Obligations

The following d=1 obligations must be carried into any implementation packet:

- `TaxonomyLoader`: `pipeline_cli.py::main`, `UnifiedSnapshotBuilder.build`,
  `run_kg_pipeline`, and focused tests in
  `scripts/tests/test_evidence_materializer.py`,
  `scripts/tests/test_pdf_evidence_integration.py`,
  `scripts/tests/test_edge_materializer.py`, and related imports.
- `UnifiedSnapshotBuilder`: `run_kg_pipeline`, `pipeline_cli.py::main`,
  `scripts/tests/test_kg_unified_snapshot_builder.py`,
  `scripts/tests/test_kg_pipeline_force_path.py`, and
  `scripts/tests/test_dataset_pipeline_cli.py`.
- `CanonicalNode`: all schema, canonicalizer, query, loader, relationship,
  evidence, parity, quality, and graph-visualization tests importing or
  constructing canonical nodes. This is too broad for a first slice.
- `Neo4jLoader`: `run_kg_pipeline`, `pipeline_cli.py::main`, and
  `scripts/tests/test_kg_neo4j_loader.py`.
- `enrich_snapshot`: `pipeline_cli.py::main`,
  `scripts/tests/test_kg_relationship_enricher.py`, and dataset pipeline CLI
  relationship promotion tests.
- API/Explorer: `api/perspectiveContracts.test.ts`,
  `explorer/src/components/HomeScreen.tsx`, `explorer/src/App.tsx`, and
  `explorer/src/components/CommandBar.tsx`.

## Primary Impact Roots

| Surface | Current files | Risk |
|---|---|---|
| Taxonomy materialization | `scripts/vitruvius/kg/evidence_materializer.py::TaxonomyLoader` | current shared taxonomy loader may conflict with authored backbone source |
| Unified graph snapshot | `scripts/vitruvius/kg/unified_snapshot_builder.py::UnifiedSnapshotBuilder` | snapshot schema must distinguish current MVP nodes from shadow backbone nodes |
| Canonical schemas | `scripts/vitruvius/kg/schemas.py::CanonicalNode`, `taxonomy_v2_schemas.py` | ID, label, facet, overlay, and predicate model changes can break serialization |
| Neo4j loader | `scripts/vitruvius/kg/neo4j_loader.py::Neo4jLoader` | shadow labels and relationship registry must not contaminate current graph |
| Relationship enrichment | `scripts/vitruvius/kg/relationship_enricher.py` | must not promote vague or inferred edges as governed backbone truth |
| API graph views | `api/index.ts`, `api/perspectiveContracts.test.ts` | v1 routes must remain additive and `/v2` must be shadow-only until parity |
| Explorer graph client | `explorer/src/api/graphApi.ts`, `ExplorerRail.tsx`, `GraphScene.tsx`, `InspectorRail.tsx` | new backbone perspective must not regress current 001-Laws Explorer MVP |
| Feature flags | `config/vitruvius.yaml`, `scripts/vitruvius/config_flags.py` | `k_taxonomy_v2`, `k_shadow_read`, and `k_backbone_validation` remain false until gates pass |

## Existing Focused Tests To Preserve

- `scripts/tests/test_evidence_materializer.py`
- `scripts/tests/test_kg_unified_snapshot_builder.py`
- `scripts/tests/test_kg_schemas.py`
- `scripts/tests/test_kg_serialization_contract.py`
- `scripts/tests/test_kg_assertion_validator.py`
- `scripts/tests/test_kg_quality_report.py`
- `scripts/tests/test_kg_neo4j_loader.py`
- `scripts/tests/test_vitruvian_context_resolver.py`
- `api/perspectiveContracts.test.ts`
- `explorer/src/app.searchInspector.integration.test.tsx`
- `explorer/src/components/componentInteraction.test.tsx`
- `explorer/src/components/graph/VisNetworkHost.test.ts`

## Required Later Evidence

- Fresh GitNexus or equivalent impact output for every primary impact root
  edited by the bounded implementation packet.
- Direct callers and d=1 dependents listed for every modified symbol.
- HIGH or CRITICAL impact warnings resolved before edits.
- `gitnexus_detect_changes()` or equivalent scope report before commit.
- A written exception if MCP graph tooling remains unavailable and the CLI is
  the accepted parity path.

## Pass / Fail Gate

Pass:

- impact graph is fresh for `HEAD`
- every edited symbol has impact evidence
- tests map to each primary impact root

Fail:

- implementation edits any primary root without fresh impact evidence
- feature flags are changed before shadow/parity gates
- current Explorer/API behavior is treated as disposable
- first implementation slice edits `CanonicalNode` without a separate schema
  migration packet and full test plan
