---
task: aec-mepfs-backbone
phase: readiness
created: 2026-04-25
author: CODEX
status: iterate-readiness-control
workflow: ralplan-consensus
context:
  - .omx/context/aec-mepfs-backbone-readiness-20260425T010419Z.md
  - .omx/context/aec-mepfs-research-integration-20260425T080306Z.md
research:
  - .ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_knowledge_graph_research.md
  - ".ai/13_research/AECMEPFS++/deep-research-report.md"
  - ".ai/13_research/AECMEPFS++/deep-research-report (1).md"
  - ".ai/13_research/AECMEPFS++/deep-research-report 3.md"
audit:
  - .ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_architecture_audit.md
  - .ai/03_plans/AEC-MEPFS-Backbone/readiness-artifact-history-and-blast-radius-audit.md
related:
  - .ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_architecture_overhaul_plan.md
  - .ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_cleanup_and_blast_radius_plan.md
  - .ai/03_plans/taxonomy-governance/00_locked_decisions.md
  - .ai/03_plans/AEC-MEPFS-Backbone/relationship-predicate-registry-draft.md
  - .ai/03_plans/AEC-MEPFS-Backbone/code-intelligence-impact-map.md
  - .ai/03_plans/AEC-MEPFS-Backbone/sel-mcp-precheck.md
  - .ai/03_plans/AEC-MEPFS-Backbone/shadow-graph-database-safety-protocol.md
  - .ai/03_plans/AEC-MEPFS-Backbone/api-explorer-parity-contract.md
  - .ai/03_plans/AEC-MEPFS-Backbone/verification-and-benchmark-contract.md
  - .ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md
---

# AEC-MEPFS Backbone Readiness Plan

## Purpose

This readiness plan answers one question: what must be true before Vitruvius
opens the first bounded implementation lane for the AEC-MEPFS Backbone?

Readiness here does **not** mean feature-flag cutover, Neo4j cleanup, raw/canonical
rebuild, document-derived enrichment, or replacement of the current Explorer MVP.
It means the project is ready to start a bounded, reversible implementation slice
for the authored backbone.

This plan is a planning/control artifact only. It authorizes documentation,
scorecard, evidence, and decision-record work. It does not authorize source-code
edits, database writes, Neo4j backup test runs, feature-flag changes, pipeline
rebuilds, graph reloads, destructive resets, or derived-artifact cleanup.

## RALPLAN-DR Summary

### Principles

- Author the AEC-MEPFS Backbone first; classify documents and evidence into it
  afterward.
- Treat the tree as a navigation projection and the typed graph as the truth
  model.
- Keep external standards as versioned crosswalks unless licensing explicitly
  permits deeper use.
- Preserve current `001-Laws` Explorer MVP until a shadow graph passes parity.
- No source-code implementation, database write, destructive cleanup, database
  reset, feature-flag cutover, graph rebuild, or backup test run before a later
  execution packet is accepted.

### Decision Drivers

- The current KG runtime is taxonomy-path based, while the intended architecture
  requires a governed backbone.
- Local AI quality improves when it classifies into known concepts instead of
  inventing the ontology during extraction.
- The blast radius spans canonical knowledge, KG schemas/builders, Neo4j, API,
  Explorer, feature flags, and derived artifacts.

### Viable Options

#### Option A - Readiness-Gated Backbone First

Create one readiness gate system before implementation. Start only after
architecture, source rights, seed scope, runtime roots, shadow graph safety,
consumer parity, and verification readiness are all passable.

Pros:

- strongest fit with current AEC blocked state
- minimizes rework and database churn
- keeps old graph available until shadow parity exists
- gives local AI a stable classification target

Cons:

- slower than starting code immediately
- requires more planning discipline and evidence collection

#### Option B - Start Bounded Schema Implementation Now

Begin with `BackboneNode`, validator, and shadow loader while resolving readiness
gaps in parallel.

Pros:

- faster visible progress
- may reveal implementation constraints earlier

Cons:

- risks coding around unsettled source-rights and seed-scope decisions
- can produce another transitional layer if readiness gates change

#### Option C - Enrich Current Graph Further

Continue improving the existing `001-Laws` graph and shared taxonomy before
opening the AEC-MEPFS Backbone.

Pros:

- improves Explorer MVP quickly
- lower immediate architecture disruption

Cons:

- reinforces the old shared-taxonomy runtime path
- delays the authored backbone that should simplify local AI extraction
- increases migration debt

### Preferred Option

Option A. The current packet should become readiness-gated before any runtime
implementation starts.

## Current Readiness Verdict

Status: **not ready for implementation**.

Reason: architecture direction is strong, but readiness gates are not yet closed:

- GitNexus index is stale against current `HEAD`
- code graph / AST MCP was unavailable in the prior planning pass
- source-rights policy is not yet recorded as a scorecard
- seed scope is proposed but not accepted
- shadow graph topology is undecided
- parity and benchmark thresholds need to be made executable
- runtime roots are planned but not yet verified or impact-mapped for this
  backbone slice
- AECMEPFS++ governance, authoring, resolver, source-pack, and QA artifact
  targets are now identified but not yet written or approved

## Evidence Baseline

### Repo State Evidence

- `.ai/01_roadmap/current-phase.md` states Vitruvius is in the AEC-MEPFS
  Backbone readiness-gate phase and must defer runtime implementation until the
  readiness scorecard reaches `ready for bounded implementation`.
- `.ai/01_roadmap/milestone-tracker.md` lists the AEC-MEPFS Backbone readiness
  gate as planned and AEC first bounded slice runtime kickoff as blocked.
- `config/vitruvius.yaml` keeps `k_taxonomy_v2`, `k_shadow_read`, and
  `k_backbone_validation` false.
- `config/vitruvius.yaml` has KG transition enabled with Neo4j writes enabled,
  so operational graph changes can affect the live Explorer if not shadowed.
- `scripts/vitruvius/config_flags.py` defaults taxonomy governance flags to
  false and supports environment overrides.
- `scripts/vitruvius/kg/evidence_materializer.py::TaxonomyLoader` loads current
  shared taxonomy/concepts, not a governed backbone.
- `scripts/vitruvius/kg/unified_snapshot_builder.py` builds unified snapshots by
  loading taxonomy/concepts, then evidence, then rules, then placement
  assertions.
- `scripts/vitruvius/kg/schemas.py::CanonicalNode` currently uses a simple
  `taxonomy_path` list.
- `scripts/vitruvius/kg/schemas.py::RelationshipAssertion` already has useful
  assertion/evidence/review separation and should be preserved.
- `scripts/vitruvius/kg/neo4j_loader.py` virtualizes taxonomy/topic/subtopic
  nodes from `taxonomy_path` arrays.
- `api/index.ts` exposes `/search`, `/node/:id`, `/taxonomy`,
  `/perspectives`, and `/perspective/:id/nodes` against the current Neo4j graph
  shape.
- `.gitnexus/meta.json` is stale: its `lastCommit` does not match current
  `HEAD`.
- `omx_state` and `omx_code_intel` MCP transports returned `Transport closed`
  during this readiness pass, so MCP/code-graph evidence remains a blocker for
  implementation approval rather than a satisfied gate.

### External Standards Evidence

- ISO 12006-2 is a classification framework, not a complete operational
  classification table.
- ISO 12006-3 supports dictionary structures that can serve as ontology,
  taxonomy, meronomy, lexicon, and thesaurus.
- bSDD provides versioned dictionary/class/property structure and license fields.
- IFC is appropriate for exchange-object semantics, not for the full editorial
  product taxonomy.
- CSI MasterFormat, UniFormat, and OmniClass are licensed/copyrighted standards
  and should be treated as licensed crosswalks unless allowed use is explicit.
- Uniclass can be referenced/applied under its license, but extensions should
  live in Vitruvius internal backbone nodes rather than modified copied tables.
- CCI is a lower-friction open seed candidate, but still requires attribution,
  version locking, and provenance.
- ISO 19650 is information-management governance, not the AEC subject backbone.

### Local AECMEPFS++ Research Evidence

The AECMEPFS++ research folder adds three planning inputs:

- `deep-research-report.md` argues for taxonomy first, graph second, document
  ingestion third; no external standard as the internal backbone; an 18-domain
  candidate backbone; orthogonal lifecycle/asset/performance/geography/
  knowledge-type/standards facets; deterministic resolver behavior; and a
  Philippines jurisdiction-overlay pilot.
- `deep-research-report (1).md` provides a much larger candidate tree that spans
  foundational sciences, discipline domains, asset/space/system/product domains,
  process/delivery/compliance domains, and information/operations domains.
- `deep-research-report 3.md` expands the readiness artifact set: governance
  pack, taxonomy authoring pack, ingestion/migration/QA pack, resolver/runtime
  pack, standards/legal source pack, and operations/training/risk pack.

Integration rule:

- these reports are strong planning inputs, not admitted source-of-truth
  artifacts
- their standards/version claims must still pass the source registry and
  official-source verification gates before they become canonical
- their proposed trees must be evaluated through the first-slice model spec
  before any L1-L2 or L3-L4 content is admitted

## Hard Readiness Gates

### G-1 - No-Side-Effects Readiness Boundary

Readiness work remains documentation, scorecard, and evidence work until a
separate execution packet is accepted.

Pass criteria:

- no runtime source-code files are modified under this readiness plan
- no Neo4j write, backup test run, reload, cleanup, or reset is performed under
  this readiness plan
- no `k_taxonomy_v2`, `k_shadow_read`, `k_backbone_validation`, or related
  feature flag is flipped under this readiness plan
- no raw/canonical rebuild or derived-artifact reset is performed under this
  readiness plan
- any future implementation handoff names a separate accepted plan and keeps
  this readiness plan as its prerequisite evidence

### G0 - Control-Surface Truth

The active roadmap, milestone tracker, active work docs, and AEC-MEPFS packet all
agree that this is planning/readiness work, not runtime implementation.

Pass criteria:

- `current-phase.md`, `milestone-tracker.md`, `ACTIVE_WORK.md`,
  `STRATEGIC_NEXT_MOVE.md`, and `03_plans/INDEX.md` all reference the
  AEC-MEPFS Backbone readiness packet as the next planning gate.
- No doc implies Neo4j cleanup, feature-flag cutover, or runtime code work is
  already active.
- The broader AEC execution-readiness lane remains blocked until this readiness
  plan reaches `ready for bounded implementation`.

### G1 - Architecture Freeze

The backbone model is specific enough that implementation will not invent the
architecture.

Pass criteria:

- node/entity families are frozen for the first slice
- tree-vs-graph projection rule is written
- facet policy is written
- relationship predicate families are listed and registered for the first slice
- external standards mapping policy is written
- document metadata policy is written as assertion/read-model, not node blob
- canonical source of truth is fixed at `003_Canonical-Knowledge-Layer/backbone/`
- canonical IDs use the locked `VTN-<kind>-<7 digits>` form
- no jurisdiction-specific fork of the canonical backbone is allowed
- jurisdiction-specific meaning is modeled as overlays, edges, and applicability
  rules, not mutated canonical nodes
- all new predicates, ID kinds, flags, and schema families are registered in the
  appropriate architecture decision or registry before implementation starts
- the first-slice model spec explicitly decides whether the 18-domain proposal,
  the larger AECMEPFS++ candidate tree, or a hybrid becomes the governed L1-L2
  seed
- the one-primary-home rule is accepted for canonical concepts, with typed graph
  edges used for all secondary relationships
- lifecycle, asset, performance, geography, knowledge type, and standards
  context are modeled as facets or overlays, not uncontrolled parallel trees

### G2 - Source Rights And Standards Governance

Every standard family used in the seed or crosswalk has an allowed-use decision.

Pass criteria:

- source registry contains publisher, standard family, edition/version, source
  URL, owner, update cadence, license, and allowed-use class
- ISO/CSI are not ingested as full internal tables without explicit allowed terms
- bSDD/IFC/Uniclass/CCI are version-stamped before use
- 100% of selected source families have provenance and license classification
- no source whose license is unknown is used as backbone seed material
- the source pack explicitly covers ISO, buildingSMART, OmniClass/NIBS,
  Uniclass/NBS, CSI, ICC/I-Codes, NFPA, Eurocodes/CEN, ASCE, Philippines
  authorities, and any other selected jurisdiction starter pack
- each AECMEPFS++ report claim about current standard versions or official source
  status is re-verified against primary sources before admission

### G3 - Seed-Corpus Readiness

The first authored corpus is bounded and reviewable.

Pass criteria:

- L1-L2 AEC-MEPFS skeleton is chosen
- L3-L4 pilot slice is chosen
- steward ownership is assigned for human-locked L1-L2 nodes
- history/people/works modeling is decided or explicitly deferred
- sanitary systems placement is decided or explicitly deferred
- standards mappings are sample/pinned, not broad unlicensed imports
- L1-L2 nodes are human-locked, AI may not propose/create/mutate them, and
  changes require PRD, steward approval, and two-human review
- AI additions at L3-L4 follow the LD-8 `PlacementAssertion` thresholds:
  auto-accept only for single-clear leaf at confidence >= 0.92, queue 0.75-0.91,
  and reject below 0.75
- the AECMEPFS++ tree is treated as a candidate authoring corpus, not a
  canonical import

### G4 - Runtime-Root And Blast-Radius Readiness

The first code change is bounded before implementation begins.

Pass criteria:

- GitNexus is refreshed with `scripts/gitnexus_analyze.sh`
- code graph / AST search is available or an equivalent impact map is recorded
- impact analysis exists for `TaxonomyLoader`, `UnifiedSnapshotBuilder`,
  `CanonicalNode`, `Neo4jLoader`, API perspective builders, and Explorer graph
  types
- first implementation roots are named before code starts
- first implementation slice is limited to schema, validator, loader, shadow
  snapshot, and tests
- SEL/MCP precheck evidence is captured as a standalone artifact, including the
  exact graph/code-intel queries attempted, results received, stale-index status,
  and any fallback source-inspection map

### G5 - Shadow Graph And Database Safety

The new backbone can be inspected beside the current graph.

Pass criteria:

- shadow topology is decided: separate database, separate labels, or separate
  local instance
- current Neo4j graph is inventoried
- backup/export command is specified as a later execution prerequisite before
  destructive reset
- rollback target snapshot is selected
- no `MATCH (n) DETACH DELETE n` is allowed before backup and rollback evidence
  exist
- destructive cleanup is sequenced after all of these later execution gates:
  shadow graph build, `/v2` shadow API reads, parity pass, rollback proof, flag
  flip, and a 48-hour monitoring hold
- this readiness plan may write backup/rollback command specifications, but it
  must not run backup/restore commands or modify Neo4j

### G6 - API / Explorer Consumer Parity

The consumer contract is explicit before graph shape changes.

Pass criteria:

- v1 `/search`, `/node/:id`, `/taxonomy`, `/perspectives`, and
  `/perspective/:id/nodes` behavior is preserved until cutover
- `/v2/` Backbone API contract is written before Explorer changes
- v1 routes receive additive fields only; v1 route semantics stay unchanged
- legacy IDs remain resolvable through redirect continuity before any canonical
  ID cutover
- shadow API reads are proven before `k_taxonomy_v2` or shadow-read flags are
  enabled
- Explorer has a Backbone perspective plan
- legacy ID continuity rules are written
- parity query set covers search, node detail, taxonomy navigation, perspective
  loading, evidence display, and path/expand behavior

### G7 - Verification, Performance, And Observability

The proof artifacts are defined before implementation.

Pass criteria:

- validator outputs are defined
- quality report thresholds are defined
- unit/integration/API/Explorer tests are listed
- snapshot determinism check is specified
- Neo4j load smoke check is specified
- API search and perspective latency targets are specified
- Explorer render smoke check is specified
- readiness scorecard can output `not ready`, `conditionally ready`, or `ready
  for bounded implementation`
- Neo4j full-text search target for MVP remains p95 <= 200ms for the agreed
  shadow query set unless a later benchmark plan explicitly revises the budget
- test baselines are monotonic: new implementation work may add stricter checks
  but may not weaken existing v1 contract, KG snapshot, API, or Explorer tests
  without an explicit accepted exception

### G8 - Governance And Editorial Control Readiness

The organizational controls are explicit before taxonomy content expands.

Pass criteria:

- steward roster and RACI exist for L1 domains and source families
- change-control policy exists for add/change/deprecate/merge/split operations
- release and versioning policy separates taxonomy releases, mapping-pack
  releases, and resolver releases
- AI-use policy keeps AI in proposal/QA roles and out of editorial authority and
  runtime truth selection
- definitions/naming policy controls labels, aliases, acronyms, definitions,
  synonyms, and deprecated terms
- jurisdiction precedence policy has examples for law, standard, guidance,
  project, local ordinance, and hazard context

### G9 - Vitruvian Context Resolver Readiness

The context resolver is specified before any runtime engine is implemented.

Pass criteria:

- resolver spec defines inputs, outputs, precedence sequence, evidence
  requirements, failure modes, and non-AI hot-path rule
- precedence engine distinguishes validity filtering, operator semantics,
  legal force, specificity, temporal order, and conflict handling
- resolver API contract includes request/response schema, trace/provenance block,
  errors, pagination, caching, and deprecation policy
- resolver test suite includes deterministic golden cases for Philippines and at
  least one non-Philippines starter jurisdiction or explicit deferral rationale
- resolver output can return `single_value`, `composed`, `conflict`, or `none`
  without inventing a winner for equal-force conflicts
- no LLM call is allowed in the hot-path resolver

### G10 - Authoring, Migration QA, And Golden Dataset Readiness

The editorial and migration workflow is ready before any broad classification or
AI proposal run.

Pass criteria:

- node authoring template, definition template, synonym/thesaurus rules, facet
  handbook, relationship vocabulary, and examples corpus exist
- source inventory, legacy-to-canonical mapping workbook, validation ruleset,
  staging layout, and review queue design exist
- confidence policy matrix records auto-accept, human-review, and AI-prohibited
  proposal classes
- golden test dataset target is defined, including size, domain coverage,
  jurisdictions, edge cases, expected outputs, and ownership

### G11 - Philippines Overlay Pilot Readiness

The first country pack is modeled as overlays, not as a second taxonomy.

Pass criteria:

- Philippines jurisdiction tree is specified as `PH` through local/site/project
  scope where available
- first pilot source families are selected or explicitly deferred: BP 344,
  RA 9514, PD 856, DPWH/NBCP, Philippine Green Building Code, BP 220, plumbing,
  electrical, local zoning/ordinance, and hazard context
- overlay kinds are registered at minimum as `legal_normative`,
  `standards_adopted`, `project_contractual`, and `hazard_contextual`
- hazard context from PHIVOLCS, PAGASA, HazardHunterPH/GeoRiskPH is kept
  separate from normative legal obligations
- the first milestone is national baseline plus one or two exemplar city packs,
  not immediate full LGU coverage

## Readiness Scorecard

Score each dimension from 0 to 3.

| Score | Meaning |
|---|---|
| 0 | Absent or contradictory |
| 1 | Drafted but not testable |
| 2 | Testable but missing evidence or owner |
| 3 | Testable, owned, and evidence-backed |

| Dimension | Required Score | Current Score | Notes |
|---|---:|---:|---|
| No-side-effects boundary | 3 | 3 | This readiness packet explicitly blocks code, DB, flags, rebuilds, resets, and backup test runs |
| Architecture model clarity | 3 | 2 | First-slice L1/L2 review set, node classes, facets, predicate families, ID policy, and predicate registry draft exist; score cannot reach `3` until owners, accepted registry, admitted source files, and final locked-decision reconciliation exist |
| Source rights and standards governance | 3 | 2 | Source pack now classifies first-wave families, rights classes, and blocked/unverified claims; Philip Lewis is named source/legal owner for readiness, but legal/licensing reviewer clearance is still needed |
| Seed corpus completeness | 2 | 1 | Bounded hybrid seed is drafted but still in review because LD-10 home-domain reconciliation and owner approval remain open |
| Runtime root and boundary definition | 3 | 2 | Fresh GitNexus CLI evidence was captured for KG/API/Explorer/flag roots; score remains `2` because HIGH/CRITICAL impact roots require a bounded implementation packet and code-review graph MCP was unavailable |
| Blast radius and migration safety | 3 | 2 | Blast radius now includes fresh GitNexus impact evidence; score remains `2` because `CanonicalNode` is CRITICAL and backup/parity/fixture evidence is still missing |
| Shadow graph/database safety | 3 | 2 | Shadow-label topology and destructive-operation block are drafted; backup/restore proof still required |
| API and Explorer parity plan | 3 | 3 | S4 adds a report-producing parity runner, a 14-case parity fixture, and a passing report for current contract/unit surfaces; future `/v2` runtime route parity remains a later shadow-route gate |
| Validation and benchmark readiness | 3 | 2 | Verification commands, thresholds, report classes, and S3 benchmark plan are drafted; benchmark runner/report execution remains open |
| Rollback and observability | 3 | 2 | S5 adds a read-only rollback preflight report and live graph smoke; actual stopped/isolated backup/restore proof remains open |
| Governance and editorial controls | 3 | 2 | Governance pack accepted as readiness control with Philip Lewis as named accountable steward; independent second reviewer, legal/licensing reviewer, and discipline reviewers remain unfilled |
| Resolver and overlay readiness | 3 | 2 | Resolver and PH overlay packs are drafted with contracts, source separation, and golden-case targets; fixtures and non-PH case remain open |
| Authoring, migration QA, and golden dataset | 3 | 2 | Authoring/migration QA pack drafted with templates, queues, confidence policy, review ratios, and 250-case golden dataset target |

Implementation readiness requires:

- no dimension scored 0
- Architecture, Runtime roots, Shadow safety, Consumer parity, Validation, and
  Rollback each score 3
- overall average at least 2.5
- no unresolved destructive branch

Current average: 2.08.

Current verdict: **not ready**.

The no-side-effects boundary scores `3` because it is a constraint on this
readiness packet itself. It does not raise implementation readiness while the
architecture, rights, seed, runtime, shadow, parity, validation, and rollback
dimensions remain below threshold. The new governance, resolver, overlay, and
migration-QA dimensions now have accepted readiness-control artifacts, but
remain below full implementation readiness until independent reviewers,
fixtures, official-source legal clearance, backup/restore proof, and executable
acceptance evidence exist.

The score was tightened after second-opinion and architect review because draft
model artifacts without named owners, accepted registries, admitted source files,
and fully accepted locked-decision reconciliation should not score as fully
owned/evidence-backed.

2026-04-25 S3 update: `AEC-BB-S3` validates planned registry locations,
API/Explorer parity-runner plan, rollback-proof plan, benchmark plan, and
runtime-blocking readiness gates. This improves testable readiness evidence but
does not change the verdict to ready because legal/licensing clearance,
report-producing parity execution, backup/restore proof, steward-admitted
registries, canonical source admission, and separate runtime impact packets are
still missing.

2026-04-25 S4 update: `AEC-BB-S4` implements the report-producing parity
runner, adds 14 required API/Explorer parity cases, and writes a passing report
at
`006_System-Manifests/aec-mepfs-backbone/parity/20260425T113719Z/api-explorer-parity-report.json`.
This closes the local parity-runner evidence gap but does not make runtime
implementation ready while rollback proof, legal clearance, steward admission,
canonical source admission, and runtime impact packets remain open.

2026-04-25 S5 update: `AEC-BB-S5` implements the rollback preflight reporter and
writes a read-only report at
`006_System-Manifests/aec-mepfs-backbone/rollback/20260425T130816Z/rollback-preflight-report.json`.
It confirms Neo4j `2026.03.1`, live graph connectivity, 2,429 nodes, 313
`CanonicalNode` nodes, and 0 `BackboneShadow` nodes. It also confirms runtime
remains blocked because the local admin surface has no online backup subcommand
and dump/load require an unmounted database.

## Readiness Work Plan

### R1 - Reconcile Active Plan Surface

Update active state docs so the next AEC action is the AEC-MEPFS Backbone
readiness gate, not runtime kickoff.

Files:

- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/ACTIVE_WORK.md`
- `.ai/STRATEGIC_NEXT_MOVE.md`
- `.ai/03_plans/INDEX.md`

Acceptance:

- all five docs agree on planned/readiness-only status
- no doc claims runtime work is active
- state docs name this readiness plan as the next AEC gate and keep AEC runtime
  kickoff blocked until scorecard approval

Status: current active docs were checked on 2026-04-25 and reference the
AEC-MEPFS Backbone readiness gate. Re-check this gate before any implementation
handoff because these files are live control surfaces.

### R2 - Create Source Rights Registry

Create a standards source registry for the first backbone slice.

Status: accepted as readiness-control in `standards-legal-source-pack.md`;
Philip Lewis is named source/legal owner for readiness, while legal/licensing
reviewer clearance remains required before score `3` or content ingest.

Artifact target:

- `.ai/03_plans/AEC-MEPFS-Backbone/source-rights-registry.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/standards-legal-source-pack.md`

Required columns:

- source family
- publisher
- edition/version
- source URL
- license/rights summary
- allowed-use class
- intended Vitruvius use
- owner
- update cadence
- blocking notes

Acceptance:

- 100% selected source families classified
- ISO/CSI restrictions explicitly represented
- no broad ingestion source lacks allowed-use status
- current-version and official-source claims from the AECMEPFS++ reports are
  either verified against primary sources or marked `unverified`

### R3 - Freeze First-Slice Backbone Model

Write the first-slice model spec.

Status: accepted as readiness-control in
`master-taxonomy-l1-l2-decision-record.md`; first-slice model is now a bounded
hybrid candidate with `HIS` and `FIG` auxiliary and LD-10
accessibility/sustainability/security reductions. Predicate readiness is
accepted as readiness-control in `relationship-predicate-registry-draft.md`.
Independent review, source admission, and locked-decision reconciliation remain
required before score `3`.

Artifact target:

- `.ai/03_plans/AEC-MEPFS-Backbone/first-slice-backbone-model-spec.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/master-taxonomy-l1-l2-decision-record.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/relationship-predicate-registry-draft.md`

Acceptance:

- first-slice node types frozen
- first-slice facet dimensions frozen
- first-slice predicate families frozen
- Layer-3 backbone location and `VTN-<kind>-<7 digits>` ID rule recorded
- history/people/works placement decided or deferred
- sanitary systems placement decided or deferred
- no jurisdiction fork or jurisdiction-mutated canonical node is allowed
- L1-L2 steward and two-human review requirement is recorded
- document metadata policy written
- 18-domain proposal and larger AECMEPFS++ candidate tree are explicitly
  accepted, rejected, or reduced to a bounded hybrid seed

### R4 - Refresh Code Intelligence And Impact Map

Refresh and capture code-intel evidence before implementation.

Artifact targets:

- `.ai/03_plans/AEC-MEPFS-Backbone/code-intelligence-impact-map.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/sel-mcp-precheck.md`

Acceptance:

- `scripts/gitnexus_analyze.sh` run successfully
- `.gitnexus/meta.json lastCommit` equals `HEAD`
- code graph / AST query results captured or fallback impact report written
- impact map includes KG schemas/builders, Neo4j loader, API, Explorer, flags,
  and derived artifact surfaces
- SEL/MCP precheck artifact lists exact tool availability, queries, failures,
  and fallback evidence

Status: fresh GitNexus CLI evidence was captured and recorded in
`code-intelligence-impact-map.md`; `sel-mcp-precheck.md` records MCP transport
closure and CLI parity. R4 is closed for readiness evidence. Runtime score
remains below `3` because `CanonicalNode` is CRITICAL impact, `TaxonomyLoader`
and `Neo4jLoader` are HIGH impact, and every later edited symbol still needs
packet-specific impact evidence.

### R5 - Define Shadow Graph And Database Cleanup Protocol

Choose a shadow topology and write backup/rollback commands without running
database mutation or backup/restore operations in this readiness lane.

Artifact target:

- `.ai/03_plans/AEC-MEPFS-Backbone/shadow-graph-database-safety-protocol.md`

Acceptance:

- shadow topology selected
- Neo4j backup/export command specification written as text only
- restore/reload command specification written as text only
- destructive reset remains blocked until backup evidence exists
- current `001-Laws` MVP snapshot remains baseline
- cleanup sequence explicitly follows shadow graph build, `/v2` shadow reads,
  parity pass, rollback proof, feature-flag enablement, and 48-hour monitoring

Status: accepted as readiness-control in
`shadow-graph-database-safety-protocol.md`; no backup/export, restore, Neo4j
write, graph reload, or cleanup command has been run.

### R6 - Define API / Explorer Parity Contract

Write parity expectations before frontend/backend changes.

Artifact target:

- `.ai/03_plans/AEC-MEPFS-Backbone/api-explorer-parity-contract.md`

Acceptance:

- v1 preservation list written
- v2 Backbone API route sketch written
- Explorer Backbone perspective requirements written
- parity query set written
- legacy ID continuity requirement written
- additive-v1 and `/v2/` route rules recorded
- redirect behavior for old semantic IDs recorded

Status: accepted as readiness-control in `api-explorer-parity-contract.md`;
`AEC-BB-S3` adds a validated parity-runner plan, and `AEC-BB-S4` implements a
report-producing runner with a passing report. Future `/v2` runtime route
parity remains open until shadow routes exist.

### R7 - Define Verification And Benchmark Contract

Write exact verification commands and thresholds.

Artifact target:

- `.ai/03_plans/AEC-MEPFS-Backbone/verification-and-benchmark-contract.md`

Acceptance:

- unit tests named for schema/validator/loader
- integration tests named for snapshot/shadow load
- API contract tests named for v1/v2 parity
- Explorer tests named for Backbone perspective
- latency budgets defined for API search and perspective loading
- snapshot determinism and quality-report outputs defined
- Neo4j FTS p95 <= 200ms target recorded or explicitly superseded by a later
  accepted benchmark plan
- monotonic test-baseline rule recorded
- exact verification commands are listed without being executed by this
  readiness plan
- fixtures, fixture source paths, and baseline snapshots are named
- output artifact paths are specified for every verification class
- pass/fail thresholds are explicit for schema, source rights, predicate
  registry, snapshot determinism, API parity, Explorer smoke, latency, and
  rollback-report validation

Status: accepted as readiness-control in
`verification-and-benchmark-contract.md`; `AEC-BB-S3` adds a validated
benchmark plan, but listed commands are future execution specifications, not
evidence that runtime implementation has passed.

### R8 - Define Governance And Editorial Control Pack

Write the editorial operating controls identified by the AECMEPFS++ artifact
checklist.

Status: accepted as readiness-control in
`governance-editorial-control-pack.md`; Philip Lewis is the named readiness
steward, while independent second reviewer, legal/licensing reviewer, and
discipline reviewer roles remain unfilled before score `3`.

Artifact target:

- `.ai/03_plans/AEC-MEPFS-Backbone/governance-editorial-control-pack.md`

Acceptance:

- steward roster and RACI are specified
- change-control policy is specified
- release/versioning policy is specified
- AI-use policy is specified
- definitions/naming policy is specified
- jurisdiction precedence policy is specified
- each policy has owner, minimum contents, and pass/fail acceptance criteria

### R9 - Define Vitruvian Context Resolver Pack

Write the deterministic resolver contract before any resolver implementation is
opened.

Status: accepted as readiness-control in `vitruvian-context-resolver-pack.md`;
fixture paths, non-Philippines starter case, and implementation-impact map are
still required before score `3`.
The non-Philippines starter jurisdiction is explicitly deferred in the resolver
pack until source-rights and steward evidence exist.

Artifact target:

- `.ai/03_plans/AEC-MEPFS-Backbone/vitruvian-context-resolver-pack.md`

Acceptance:

- resolver inputs and outputs are specified
- precedence engine rules are specified
- resolver API contract is specified
- resolver test suite and golden cases are specified
- no-LLM-hot-path rule is recorded
- trace/provenance and `conflict_set` behavior are specified
- p95 targets for lookup, resolve, search, and overlay fan-out are recorded as
  future verification thresholds

### R10 - Define Taxonomy Authoring And Migration QA Pack

Write the authoring, staging, review, and golden-dataset controls before broad
AI-assisted classification.

Status: remains draft in `taxonomy-authoring-migration-qa-pack.md`; concrete
fixture files, independent/discipline reviewer ownership, and queue storage
locations remain open.
Historical failure regressions for provenance-vs-semantic edges, vague
predicates, long document-derived names, and fragmented source-reference
concepts are now recorded.

Artifact target:

- `.ai/03_plans/AEC-MEPFS-Backbone/taxonomy-authoring-migration-qa-pack.md`

Acceptance:

- node authoring template is specified
- definition template is specified
- synonym/thesaurus rules are specified
- facet handbook is specified
- cross-discipline relationship vocabulary is specified
- examples corpus target is specified
- source inventory and legacy-to-canonical workbook are specified
- validation ruleset and staging/review queue design are specified
- confidence policy matrix and human-review ratios are specified
- golden dataset size, coverage, ownership, and expected outputs are specified

### R11 - Define Philippines Overlay Pilot Pack

Write the first country-pack plan as overlays over the global backbone.

Status: remains draft in `philippines-overlay-pilot-pack.md`; source-rights
review, PSGC version check, and LGU source confirmation remain open.

Artifact target:

- `.ai/03_plans/AEC-MEPFS-Backbone/philippines-overlay-pilot-pack.md`

Acceptance:

- Philippines jurisdiction tree is specified
- selected first-wave authority families are listed with source-rights status
- overlay kinds and precedence behavior are specified
- hazard context is separated from normative legal overlays
- national baseline plus exemplar city-pack scope is specified
- source limitations and fallback citation rules are recorded

## Pre-Mortem

### Failure Scenario 1 - Licensed Standards Leak Into Canonical Backbone

Cause:

- CSI or ISO tables are copied into internal canonical files without allowed-use
  clearance.

Impact:

- legal exposure, inability to redistribute, and polluted source-of-truth layer.

Mitigation:

- source rights registry blocks seed ingestion until allowed-use class is clear.
- licensed standards are metadata/crosswalk only unless explicit terms permit
  deeper use.

### Failure Scenario 2 - Shadow Graph Becomes A Hidden Cutover

Cause:

- new labels/routes are introduced but Explorer starts depending on them before
  parity and rollback evidence exists.

Impact:

- current Explorer MVP breaks and recovery requires manual graph reset.

Mitigation:

- v1 routes stay unchanged.
- shadow-read flag remains false until parity gate passes.
- destructive cleanup blocked until backup/export evidence exists.
- `/v2` shadow reads, rollback proof, feature-flag enablement, and 48-hour
  monitoring must happen before any cleanup resets the current graph baseline.

### Failure Scenario 3 - Readiness Plan Becomes Another Stale Plan

Cause:

- readiness gates are not linked to active roadmap/milestone docs or exact
  evidence files.

Impact:

- future agents bypass the plan and start runtime work from older AEC first-slice
  files.

Mitigation:

- active docs point to this readiness plan.
- readiness scorecard provides current verdict.
- AEC first-slice remains blocked until readiness is `ready for bounded
  implementation`.

### Failure Scenario 4 - Readiness Work Accidentally Performs Implementation

Cause:

- backup tests, graph loads, flag edits, or small schema changes are treated as
  harmless readiness checks.

Impact:

- the project crosses from planning into runtime migration without accepted
  implementation gates or rollback evidence.

Mitigation:

- G-1 blocks all code, DB, flag, rebuild, reset, and backup/restore side effects
  under this plan.
- execution requires a separate accepted packet that references this readiness
  artifact as prerequisite evidence.

### Failure Scenario 5 - Research Tree Becomes Canonical By Copy-Paste

Cause:

- the AECMEPFS++ candidate tree is imported directly because it is detailed and
  useful.

Impact:

- L1-L2 governance is bypassed, source claims remain unverified, and the
  backbone inherits unreviewed scope/placement errors.

Mitigation:

- the reports remain planning inputs only.
- first-slice model and L1-L2 decision artifacts must explicitly accept, reject,
  or reduce candidate tree branches before admission.
- steward and source-rights gates block canonicalization.

### Failure Scenario 6 - Resolver Becomes AI-Driven Runtime Truth

Cause:

- local AI is used to resolve jurisdiction conflicts or compliance answers at
  query time because the graph is incomplete.

Impact:

- outputs become nondeterministic and unauditable.

Mitigation:

- resolver pack requires deterministic precedence, trace output, conflict sets,
  and no LLM in the hot path.
- AI remains limited to proposal, QA, candidate extraction, and review-queue
  preparation.

## Expanded Test Plan

### Unit

- backbone schema validation
- source rights registry validation
- predicate registry validation
- ID/redirect validation
- facet assignment validation
- no-jurisdiction-fork validation
- no-unregistered-predicate validation

### Integration

- backbone seed to shadow snapshot
- shadow snapshot to Neo4j load
- legacy concept mapping to backbone placements
- quality report over shadow graph

### API

- v1 route preservation
- v2 Backbone route contract
- search parity
- node detail parity
- taxonomy/tree projection parity
- evidence display parity
- legacy ID redirect parity
- additive-v1-field compatibility

### Explorer

- Backbone perspective loads
- tree projection renders
- graph projection renders
- node detail/source summary displays
- edge provenance is inspectable
- current concepts/evidence/regulatory perspectives still load

### Observability

- readiness scorecard output
- shadow graph load report
- parity mismatch report
- rollback report
- latency report
- no-side-effects audit for readiness work
- SEL/MCP/code-intel precheck artifact
- governance/editorial-control artifact review
- resolver contract and golden-case review
- source-rights/current-version verification review
- Philippines overlay pilot review

## ADR

### Decision

Adopt an AEC-MEPFS Backbone readiness gate before any runtime implementation.

### Drivers

- current repo state keeps AEC runtime work blocked pending real roots and an
  accepted execution packet
- local AI will perform better against a governed classification graph
- architecture/data migration blast radius is broad enough to require explicit
  safety gates
- AECMEPFS++ reports show that resolver governance, steward/RACI, source packs,
  authoring controls, PH overlays, and golden datasets are readiness
  prerequisites, not later polish

### Alternatives Considered

- start bounded schema implementation now: rejected for now because source rights,
  shadow topology, and parity thresholds are not closed
- continue enriching current graph: rejected as the strategic path because it
  strengthens the temporary shared-taxonomy surface
- flip taxonomy flags: rejected because committed backbone corpus and validation
  evidence do not exist
- import the AECMEPFS++ tree directly: rejected because the reports are planning
  inputs and their source/version claims, L1-L2 placements, and branch
  boundaries need steward and source-rights approval

### Why Chosen

The readiness-gated path gives the strongest chance of a clean architecture
without breaking the current Explorer MVP or polluting the canonical layer with
unlicensed or weakly governed standards content.

### Consequences

- implementation waits until readiness gates close
- the AEC-MEPFS Backbone packet becomes the next AEC planning authority
- AEC first-slice runtime packet remains blocked until readiness is achieved
- database cleanup becomes a late, evidenced migration step
- AECMEPFS++ report claims become source-verification requirements rather than
  accepted canonical truth

### Follow-Ups

- write `source-rights-registry.md`
- write `standards-legal-source-pack.md`
- write `first-slice-backbone-model-spec.md`
- write `master-taxonomy-l1-l2-decision-record.md`
- write `relationship-predicate-registry-draft.md`
- write `readiness-artifact-history-and-blast-radius-audit.md`
- write `code-intelligence-impact-map.md`
- write `sel-mcp-precheck.md`
- write `shadow-graph-database-safety-protocol.md`
- write `api-explorer-parity-contract.md`
- write `verification-and-benchmark-contract.md`
- write `code-intelligence-impact-map.md` and `sel-mcp-precheck.md`
- write `shadow-graph-database-safety-protocol.md`
- write `api-explorer-parity-contract.md`
- write `verification-and-benchmark-contract.md`
- write `governance-editorial-control-pack.md`
- write `vitruvian-context-resolver-pack.md`
- write `taxonomy-authoring-migration-qa-pack.md`
- write `philippines-overlay-pilot-pack.md`
- keep active state docs aligned with the readiness gate

## Available-Agent-Types Roster

Useful follow-up roles:

- `explore`: fast repo lookup and blast-radius mapping
- `researcher`: official standards and licensing research
- `planner`: gate sequencing and scorecard refinement
- `architect`: architecture review, tradeoff tension, subsystem boundaries
- `critic`: plan quality and readiness-gate review
- `test-engineer`: verification matrix and test adequacy
- `security-reviewer`: destructive operation and trust-boundary review
- `executor`: later bounded implementation after readiness approval
- `verifier`: final completion evidence review

## Follow-Up Staffing Guidance

### Ralph Readiness-Documentation Path

Use only if a later user request asks one owner to close the remaining
readiness-documentation artifacts. This is not a runtime implementation path.

Suggested roles:

- leader: `ralph` in documentation/readiness mode only
- support: one `explore` for impact refresh, one `test-engineer` for acceptance
  criteria, one `verifier` for closure evidence

Ralph should prove:

- readiness scorecard is evidence-backed
- no code, DB, flag, rebuild, backup-test, or cleanup side effect occurs
- all active docs point to the correct next gate

### Team Readiness-Documentation Path

Use only if a later user request asks multiple lanes to close the remaining
readiness-documentation artifacts in parallel. This is not a runtime
implementation path.

Suggested lanes:

- standards/rights lane: `researcher`
- code impact lane: `explore`
- data/Neo4j safety lane: `architect`
- API/Explorer parity lane: `test-engineer`
- critique lane: `critic`

Team should prove before shutdown:

- source rights registry exists
- impact map is current
- shadow graph choice is made
- parity contract is testable
- readiness scorecard has an updated verdict

## Readiness Handoff Hints

No execution launch is authorized from this proposed plan. The examples below
are documentation/readiness handoff shapes only and must not be used to start
source-code, database, feature-flag, graph-rebuild, backup-test, or cleanup work.

When readiness-documentation work is explicitly requested later:

```bash
$ralph .ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_readiness_plan.md
```

For coordinated readiness-documentation refinement:

```bash
$team .ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_readiness_plan.md
```

Both paths remain planning/documentation lanes until a separate implementation
packet is accepted.

## Consensus Review Changelog

Planner/explore/research passes established the readiness-gated path, blast
radius, and standards-rights constraints.

Architect review first returned `ITERATE`, then `APPROVE` after the plan added:

- an explicit no-side-effects readiness boundary
- locked taxonomy-governance bindings for Layer 3 source, VTN IDs,
  no-jurisdiction-fork policy, additive `/v2`, redirects, and shadow-first
  rollout
- stricter destructive-cleanup sequencing
- explicit API/Explorer parity and Neo4j FTS latency requirements
- live roadmap/state reconciliation around this readiness gate

Critic review first returned `ITERATE`, then `APPROVE` after the plan added:

- completed/non-blocking status for prior KG maintenance work
- concrete artifact targets for R2-R7
- exactness requirements for future verification commands, fixtures, output
  artifacts, and pass/fail thresholds
- wording that limits `$ralph` and `$team` examples to readiness-documentation
  work only

Current packet status: `ITERATE` as a readiness/control artifact. Current
implementation status remains `not ready`.

Post-consensus locked-decision review returned `ITERATE` on LD-8 and LD-10
alignment. The packet has been revised to follow LD-8 `PlacementAssertion`
thresholds, restore L1/L2 two-human review, and reduce the L1 candidate set so
accessibility, sustainability, and security/hardening follow LD-10. The packet
remains in iteration until that reconciliation receives a later explicit
approval.
