---
task: aec-mepfs-backbone
phase: cleanup-plan
created: 2026-04-25
author: CODEX
status: proposed
related:
  - .ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_readiness_plan.md
  - .ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_architecture_overhaul_plan.md
  - .ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_architecture_audit.md
---

# AEC-MEPFS Backbone Cleanup And Blast-Radius Plan

## Purpose

Prepare a cleanup and migration plan for the proposed AEC-MEPFS Backbone
architecture shift without touching runtime code or deleting any database data
yet.

This cleanup plan is subordinate to the readiness plan. It does not authorize
source-code edits, Neo4j backup test runs, graph loads, database writes,
feature-flag flips, rebuilds, resets, or derived-artifact cleanup.

The AECMEPFS++ research reports expand the cleanup blast radius: future cleanup
must account not only for graph/schema migration, but also for governance
artifacts, steward/RACI records, resolver contracts, review queues, golden
datasets, source-rights matrices, and jurisdiction overlay packs. These remain
planning artifacts until a separate execution packet is accepted.

The goal is to make the future implementation clean: authored backbone first,
document classification second, relationship enrichment third, Explorer/API
projection last.

## Technical Opinion

The AEC-MEPFS Backbone approach is the cleaner architecture.

Local AI should not be asked to invent the classification system while also
extracting facts from messy source documents. The stronger design is:

1. author and validate the AEC-MEPFS Backbone first
2. let AI classify documents, rules, chunks, and evidence spans into that known
   graph
3. let AI propose lower-level placements and relationships only as reviewable
   assertions
4. materialize Explorer summaries from the graph instead of embedding large
   document lists into canonical nodes

This lowers prompt ambiguity, reduces vocabulary drift, makes extraction cheaper,
and gives the system a stable target for entity resolution. It does not remove
hard work: document extraction still needs evidence spans, disambiguation,
confidence, versioning, jurisdiction overlays, and relationship review.

## Current Evidence

- `scripts/vitruvius/kg/evidence_materializer.py::TaxonomyLoader` currently
  loads concepts and taxonomy roots from `003_Canonical-Knowledge-Layer/shared/`.
- `TaxonomyLoader` derives `taxonomy_path` from explicit frontmatter or legacy
  `topic_tags` / `category` fields.
- `scripts/vitruvius/kg/unified_snapshot_builder.py::UnifiedSnapshotBuilder`
  starts by loading the current taxonomy/concepts, then evidence, then rules,
  then placement assertions.
- `scripts/vitruvius/kg/schemas.py::CanonicalNode` currently has a simple
  `taxonomy_path: list[str]` field.
- `scripts/vitruvius/kg/schemas.py::RelationshipAssertion` already separates
  relationship claim, reasoning, evidence IDs, document version IDs, validation
  status, and review state.
- `scripts/vitruvius/kg/neo4j_loader.py::Neo4jLoader` virtualizes taxonomy,
  topic, and subtopic nodes from `taxonomy_path` arrays.
- `api/index.ts` currently exposes perspectives and taxonomy/search/node routes
  that assume the existing `Taxonomy`, `Topic`, `Subtopic`, and `CanonicalNode`
  shape.
- `config/vitruvius.yaml` has `k_taxonomy_v2: false` and
  `k_backbone_validation: false`.
- `003_Canonical-Knowledge-Layer/backbone/` is absent.
- The local `.gitnexus/meta.json` exists, but its `lastCommit` does not match the
  current `HEAD`; the GitNexus index must be refreshed before relying on it for
  implementation impact analysis.
- The GitNexus CLI is not directly on `PATH` in this session, but
  `scripts/gitnexus_analyze.sh` exists.
- The `omx_code_intel` AST MCP transport was unavailable in this session, so the
  implementation phase should re-run code-intel/GitNexus in a fresh tool state.

## Blast Radius

### Canonical Knowledge Layer

Impacted:

- `003_Canonical-Knowledge-Layer/backbone/` — new canonical source of truth
- `003_Canonical-Knowledge-Layer/shared/taxonomy/` — migration input
- `003_Canonical-Knowledge-Layer/shared/topics/` — migration input
- `003_Canonical-Knowledge-Layer/shared/subtopics/` — migration input
- `003_Canonical-Knowledge-Layer/shared/concepts/` — migration input and
  classification target
- `003_Canonical-Knowledge-Layer/shared/sources/` — document provenance input
- `003_Canonical-Knowledge-Layer/shared/relationships/` — relationship migration
  and review input

Cleanup direction:

- do not delete shared taxonomy during planning
- create backbone as new canonical corpus
- demote shared taxonomy to migration/source material after parity passes
- preserve old IDs through redirects/mappings

### KG Schema And Builders

Impacted:

- `scripts/vitruvius/kg/schemas.py`
- `scripts/vitruvius/kg/evidence_materializer.py`
- `scripts/vitruvius/kg/unified_snapshot_builder.py`
- `scripts/vitruvius/kg/edge_materializer.py`
- `scripts/vitruvius/kg/neo4j_loader.py`
- `scripts/vitruvius/kg/quality_report.py`
- `scripts/vitruvius/kg/relationship_enricher.py`

Cleanup direction:

- add explicit `BackboneNode`, `FacetAssignment`, `StandardMapping`, and
  `DocumentClassification` models before replacing loaders
- split "load authored backbone" from "classify document evidence"
- keep `RelationshipAssertion`; extend it rather than replacing it
- isolate the old `taxonomy_path` path as a legacy adapter until migration is
  complete

### CLI And Feature Flags

Impacted:

- `scripts/pipeline_cli.py`
- `scripts/vitruvius/config_flags.py`
- `config/vitruvius.yaml`

Cleanup direction:

- keep `k_taxonomy_v2` and `k_backbone_validation` false until shadow validation
  passes
- add dry-run planning/reporting commands before destructive reset commands
- keep destructive reset behind explicit confirmation
- do not make AEC-MEPFS Backbone the default graph until parity succeeds

### Neo4j / Operational Graph Database

Impacted:

- current local Neo4j graph
- `005_Operational-Intelligence-Layer/graph/kg-v2/`
- current Explorer/API read assumptions

Cleanup direction:

- do not clear Neo4j until a backup/export and rollback path exist
- prefer shadow graph labels or a separate local Neo4j database during migration
- after cutover, clear/reload only from the validated backbone snapshot
- keep current `001-Laws` MVP graph as a baseline snapshot until the new graph is
  verified

### API And Explorer

Impacted:

- `api/index.ts`
- `api/perspectiveContracts.test.ts`
- `explorer/src/types/index.ts`
- `explorer/src/api/graphApi.ts`
- `explorer/src/App.tsx`
- `explorer/src/components/*`
- `explorer/src/components/graph/VisNetworkHost.tsx`

Cleanup direction:

- add v2/backbone routes rather than mutating v1 routes first
- add an explicit Backbone perspective
- use materialized counts and source summaries for node sidebars
- do not rely on raw `taxonomy_path` arrays for user-facing hierarchy once the
  backbone is admitted

### Tests And Validation

Impacted:

- `scripts/tests/test_kg*.py`
- `api/*.test.ts`
- `explorer/src/**/*.test.tsx`
- future GitNexus/code-graph validation evidence

Cleanup direction:

- add tests before cleanup edits
- preserve current API/Explorer contract tests while adding v2 tests
- run GitNexus/code graph impact analysis before source-code implementation
- treat resolver, governance, review-queue, and golden-dataset artifacts as
  prerequisites before broad cleanup or classification automation

## Cleanup Sequence

### Phase C0 - Planning Freeze

Deliverables:

- accepted AEC-MEPFS Backbone architecture plan
- accepted cleanup/blast-radius plan
- decision on seed strategy

Do not:

- delete data
- rebuild Neo4j
- flip feature flags
- change runtime code

### Phase C1 - Fresh Code Intelligence Baseline

Deliverables:

- refreshed GitNexus index with `scripts/gitnexus_analyze.sh`
- code graph / GitNexus impact report for:
  - `TaxonomyLoader`
  - `UnifiedSnapshotBuilder`
  - `CanonicalNode`
  - `Neo4jLoader`
  - API perspective builders
  - Explorer graph node/edge types
- stale-index note cleared

Gate:

- do not begin implementation if code-intel tools remain unavailable and impact
  cannot be independently mapped.
- capture a standalone SEL/MCP precheck artifact that records tool availability,
  exact queries, stale-index status, and fallback evidence.

### Phase C2 - Data Inventory And Backup Plan

Deliverables:

- inventory of current Neo4j node/relationship counts
- inventory of current `kg-v2` snapshots
- inventory of current shared taxonomy/topic/subtopic/concept counts
- backup/export command plan for Neo4j
- rollback target snapshot selected

Do not:

- run `MATCH (n) DETACH DELETE n` yet
- delete `005` graph snapshots yet
- run backup/restore tests yet under the readiness lane

### Phase C3 - Legacy Taxonomy Quarantine Plan

Deliverables:

- identify which current shared taxonomy files become backbone seeds
- identify which files become legacy migration inputs
- map existing concept IDs to proposed backbone placements
- define redirect policy for any future opaque IDs

Gate:

- no old concept ID disappears from API/search before redirect support exists.
- canonical IDs follow `VTN-<kind>-<7 digits>` and old semantic IDs remain
  resolvable through redirects.

### Phase C4 - Backbone Shadow Build Plan

Deliverables:

- shadow snapshot output path
- shadow Neo4j label/database strategy
- shadow API route names
- parity report format
- quality report thresholds

Gate:

- v1 Explorer remains usable during shadow work.

### Phase C4A - Governance, Resolver, And QA Control Plan

Deliverables:

- governance/editorial-control pack
- deterministic resolver pack
- taxonomy authoring/migration QA pack
- Philippines overlay pilot pack
- standards/legal source pack

Gate:

- no broad classification automation, graph cutover, or cleanup proceeds until
  these artifacts exist and the readiness scorecard is updated.

### Phase C5 - Database Cleanup Execution Plan

Deliverables:

- final approved cleanup checklist
- backup/export evidence
- rollback command
- graph reload command
- smoke-test checklist

Destructive actions allowed only after approval:

- clear current Neo4j graph
- remove obsolete derived snapshots
- demote legacy taxonomy runtime path

Approval means all earlier gates have passed, including shadow graph build,
`/v2` shadow API reads, parity pass, rollback proof, feature-flag enablement, and
the locked 48-hour monitoring hold.

### Phase C6 - Post-Cutover Cleanup

Deliverables:

- delete or archive dead adapters
- remove duplicated taxonomy code paths
- update docs/state/decision logs
- update known issues
- run final GitNexus/code graph detect-changes pass

## Database Cleanup Policy

Use three tiers:

1. **Preserve**: raw sources, canonical source docs, historical validation logs,
   and current accepted snapshots.
2. **Shadow**: new backbone graph, v2 API routes, materialized read models.
3. **Retire**: legacy derived artifacts and old Neo4j graph only after backup,
   parity, and rollback are proven.

Neo4j cleanup should be a controlled migration step, not an early reset. The
first implementation phase should create a shadow graph so we can inspect the new
backbone beside the current Explorer graph.

## Optimization Opportunities

- Precompute ancestor/descendant closure for tree navigation.
- Precompute document/rule/source counts per backbone node.
- Store large document lists as edges/assertions and materialized summaries, not
  canonical node properties.
- Use full-text indexes for labels, aliases, external codes, and source titles.
- Keep source evidence in separate labels/nodes so concept graph views stay
  light.
- Let local AI classify against a closed candidate set instead of open-ended
  generating labels.
- Use confidence thresholds and review queues for lower-level additions and
  relationship proposals.

## Acceptance Criteria

- Cleanup plan exists before any cleanup edit.
- GitNexus/code graph impact is refreshed before implementation.
- Current database state is inventoried before cleanup.
- Neo4j has a backup/export before destructive reset.
- New backbone graph is loaded in shadow mode before cutover.
- Current Explorer MVP remains available until parity passes.
- No old canonical ID is deleted without redirect/migration support.
- Feature flags remain false until validators and parity checks pass.
- No cleanup/reset/rebuild/backup test run is performed by the readiness lane.

## Open Questions

- Should the shadow graph use a separate Neo4j database, separate labels, or a
  separate local Neo4j instance?
- Should `AEC-MEPFS` include sanitary systems explicitly as a top-level domain or
  as part of Plumbing/Public Health/Fire Protection?
- Should history/people/works be a top-level domain or a facet/entity layer that
  cuts across Architecture and Engineering?
- Which external standards are allowed for broad seed ingestion versus reference
  mapping only, based on licensing?
