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

Fresh GitNexus CLI evidence was captured on 2026-04-25. The latest S5 refresh
was captured against current `HEAD` `4afd707` before the S5 commit.

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

- R4 baseline: GitNexus wrapper completed successfully in 70.3s.
- R4 baseline indexed commit and current commit both resolved to `da3569d`.
- S4 refresh: `npx --yes gitnexus@1.6.2-rc.10 analyze --force
  --skip-agents-md` completed successfully in 12.5s.
- S4 refresh indexed commit and current commit both resolved to `aa34e80`.
- S4 refresh `.gitnexus/meta.json` records `indexedAt:
  2026-04-25T12:19:44.576Z`.
- S4 refresh stats: 1,353 files, 11,913 nodes, 28,982 edges, 580
  communities, 300 processes, 0 embeddings.
- S5 refresh: `npx --yes gitnexus@1.6.2-rc.10 analyze --force
  --skip-agents-md` completed successfully in 12.9s.
- S5 refresh indexed commit and current commit both resolved to `4afd707`.
- S5 refresh status: up to date.
- S5 refresh stats: 1,356 files, 11,964 nodes, 29,123 edges, 579
  clusters, 300 flows, 0 embeddings.
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

## S4 Parity Runner Impact Evidence

The S4 readiness-control slice adds a runtime-disconnected parity runner and
focused tests. Fresh pre-commit CLI evidence for the public runner symbol:

```bash
npx --yes gitnexus@1.6.2-rc.10 status
npx --yes gitnexus@1.6.2-rc.10 impact run_parity_fixture \
  -r vitruvius \
  --direction upstream \
  --depth 3 \
  --include-tests
```

Observed on 2026-04-25 before commit:

- indexed commit: `aa34e80`
- current commit: `aa34e80`
- status: up to date
- symbol: `scripts/vitruvius/kg/backbone_parity_runner.py::run_parity_fixture`
- risk: MEDIUM
- impacted count: 15
- direct impacts: 13
- affected processes: 0
- affected modules: `Kg`

Additional helper impact evidence after the case-fixture and timeout fixes:

- `_load_parity_cases`: LOW risk, impacted count 15, direct impacts 1,
  affected processes 0.
- `_validate_parity_case_coverage`: LOW risk, impacted count 15, direct
  impacts 1, affected processes 0.

Disposition: accepted for S4 because the symbol is new, runtime-disconnected,
shell-free for default command execution, validates declared parity cases before
command execution, preserves a report on timeout/unknown-command failures, and
has zero affected runtime processes.

### S8 Shadow Parity Runner Hardening Refresh

Fresh CLI evidence for the eighth shadow parity-runner hardening slice:

```bash
npx --yes gitnexus@1.6.2-rc.10 status
npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius run_parity_fixture --direction upstream
npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius _validate_parity_case_coverage --direction upstream
```

Observed on 2026-04-26 before commit:

- indexed commit: `8a68b14`
- current commit: `8a68b14`
- status: up to date
- `run_parity_fixture`: LOW risk, impacted count 2, direct impacts 1,
  affected processes 0, affected module `Kg`
- `_validate_parity_case_coverage`: LOW risk, impacted count 3, direct
  impacts 1, affected processes 0, affected module `Kg`

CLI note: `npx --yes gitnexus@1.6.2-rc.10 detect-changes --repo vitruvius`
is not available in this GitNexus release (`unknown command 'detect-changes'`),
so this slice uses impact/status plus explicit git diff scope for the
pre-commit scope check.

## S9 Placement QA Runner Impact Evidence

The S9 shadow placement QA slice adds a new runtime-disconnected report runner
and tests. Fresh CLI evidence for reused validator symbols:

```bash
npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius validate_backbone_contract_file --direction upstream
npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius validate_backbone_contract --direction upstream
```

Observed on 2026-04-26 before commit:

- `validate_backbone_contract_file`: LOW risk, impacted count 7, direct impacts
  3, affected processes 0, affected module `Kg`
- `validate_backbone_contract`: LOW risk, impacted count 6, direct impacts 1,
  affected processes 0, affected module `Kg`

Disposition: accepted because S9 adds a new file-backed runner and does not
modify the reused validator symbols, runtime placement engine, Neo4j loader,
feature flags, API runtime, or Explorer default graph paths.

## S10 Placement QA `/v2` Route Impact Evidence

The S10 shadow placement QA route slice adds an additive read-only API route and
extends the parity fixture/category list. Fresh CLI evidence for the existing
API/parity symbols touched by the slice:

```bash
npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius buildShadowBackboneSummary --direction upstream
npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius buildShadowBackboneTaxonomyPreview --direction upstream
npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius readShadowBackboneConsumerReport --direction upstream
npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius run_parity_fixture --direction upstream
npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius _validate_parity_case_coverage --direction upstream
```

Observed on 2026-04-26 before commit:

- `buildShadowBackboneSummary`: LOW risk, impacted count 1, direct impacts 1,
  affected processes 0
- `buildShadowBackboneTaxonomyPreview`: LOW risk, impacted count 1, direct
  impacts 1, affected processes 0
- `readShadowBackboneConsumerReport`: LOW risk, impacted count 1, direct
  impacts 1, affected processes 0
- `run_parity_fixture`: LOW risk, impacted count 2, direct impacts 1, affected
  processes 0
- `_validate_parity_case_coverage`: LOW risk, impacted count 3, direct impacts
  1, affected processes 0

Disposition: accepted because S10 is additive under `/v2/backbone/placement-qa`,
reads only the placement QA JSON report, adds fail-closed route tests, and
keeps Explorer, Neo4j, KG rebuild, protected ingest, and feature flags
unchanged.

## S11 Placement QA Explorer Preview Impact Evidence

The S11 shadow placement QA Explorer preview slice adds an explicit-action
Explorer consumer for the existing read-only placement QA route and extends
parity evidence. Fresh CLI evidence for the exact Explorer/parity symbols:

```bash
npx --yes gitnexus@1.6.2-rc.10 status
npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius BackbonePreviewPanel --direction upstream
npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius ExplorerRail --direction upstream
npx --yes gitnexus@1.6.2-rc.10 analyze --force --skip-agents-md
npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius getBackbonePlacementQaPreview --direction upstream
npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius run_parity_fixture --direction upstream
```

Observed on 2026-04-26 before commit:

- indexed commit: `d6a8fbe`
- current commit: `d6a8fbe`
- status: up to date
- `BackbonePreviewPanel`: LOW risk, impacted count 0, direct impacts 0,
  affected processes 0
- `ExplorerRail`: LOW risk, impacted count 0, direct impacts 0, affected
  processes 0
- `getBackbonePlacementQaPreview`: LOW risk, impacted count 2, direct impacts
  1, affected process `ExplorerRail`
- `run_parity_fixture`: LOW risk, impacted count 2, direct impacts 1, affected
  processes 0

Disposition: accepted because S11 is Explorer preview-only, fetches placement QA
only after explicit user action, resets the detail on summary refresh, and
does not change Neo4j, KG rebuild paths, protected ingest, feature flags, v1
routes, or Explorer default graph adoption. The central type barrel change is
additive only.

## S5 Rollback Preflight Impact Evidence

The S5 readiness-control slice adds a runtime-disconnected rollback preflight
runner, focused tests, and a generated read-only report. Fresh pre-commit CLI
evidence for the public runner symbol:

```bash
npx --yes gitnexus@1.6.2-rc.10 status
npx --yes gitnexus@1.6.2-rc.10 impact run_rollback_preflight \
  --repo vitruvius \
  --direction upstream \
  --depth 3 \
  --include-tests
```

Observed on 2026-04-25 before commit:

- indexed commit: `4afd707`
- current commit: `4afd707`
- status: up to date
- symbol:
  `scripts/vitruvius/kg/backbone_rollback_preflight.py::run_rollback_preflight`
- risk: MEDIUM
- impacted count: 10
- direct impacts: 8
- affected processes: 0
- affected modules: `Kg`

Additional helper impact evidence:

- `_read_live_graph_counts`: LOW risk, impacted count 0, direct impacts 0,
  affected processes 0.
- `_admin_capabilities`: LOW risk, impacted count 10, direct impacts 1,
  affected processes 0.
- `_resolve_report_path`: LOW risk, impacted count 10, direct impacts 1,
  affected processes 0.

Disposition: accepted for S5 because the runner is new, shell-free, fixed-argv
only, runtime-disconnected from pipeline writes, constrains output under the
rollback report root, runs only help/version commands plus read-only Cypher
counts, and has zero affected runtime processes.

## S6 Registry Candidate Impact Evidence

The S6 readiness-control slice adds data and documentation only:

- `.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/predicate-registry.json`
- `.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json`
- `.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-admission-checklist.md`
- `006_System-Manifests/aec-mepfs-backbone/registry-candidates/20260425T133000Z/registry-candidate-validation-report.json`

No Python, TypeScript, API, Explorer, Neo4j loader, schema, snapshot, pipeline,
or feature-flag symbol is edited. The applicable impact response is contract
validation plus `git diff --check`, not symbol-specific impact analysis.

## S7 Runtime-Root Impact Evidence

The S7 readiness-control slice adds documentation and generated evidence only.
Fresh GitNexus evidence was captured at current `HEAD` `3031a95` and stored in:

```text
006_System-Manifests/aec-mepfs-backbone/code-impact/20260425T140845Z/runtime-root-impact-report.json
```

Observed summary:

| Symbol | Risk | Direct | Processes affected | Disposition |
|---|---:|---:|---:|---|
| `CanonicalNode` | CRITICAL | 111 at depth 1 | 6 at depth 1 | avoid in first runtime slice; schema migration packet required before edit |
| `TaxonomyLoader` | HIGH | 15 | 3 | do not replace in place; add shadow/admission path first |
| `Neo4jLoader` | HIGH | 23 | 2 | no write-path change until rollback proof and shadow tests exist |
| `UnifiedSnapshotBuilder` | MEDIUM | 12 | 2 | preserve current MVP snapshot behavior |
| `enrich_snapshot` | MEDIUM | 4 | 2 | keep governed backbone edges distinct from inferred/document edges |

The generated report records `CanonicalNode` at depth 1 because depth 3 output
from GitNexus 1.6.2-rc.10 was too large to parse as valid JSON. Existing depth 3
evidence in this map remains the broader CRITICAL-risk reference.

No runtime code was edited for S7, so symbol-specific impact evidence is
readiness evidence for the later runtime packet, not approval to implement.

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
