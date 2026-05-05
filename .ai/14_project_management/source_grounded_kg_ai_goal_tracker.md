# Source-Grounded KG AI Goal Tracker

**Status:** active north-star tracker  
**Created:** 2026-05-03  
**Owner:** project_owner_steward  
**Purpose:** track progress toward Vitruvius as a source-grounded KG/GraphRAG-style AI system for AEC-MEPFS knowledge work.

## 1. North Star

Vitruvius should support an AI assistant that can answer domain questions by resolving graph nodes, traversing admitted relationships, retrieving real referenced knowledge resources, and clearly separating:

1. **source-backed facts** — claims grounded in real documents, source records, resource links, and evidence spans;
2. **admitted graph reasoning** — reviewed relationships and graph paths accepted as Vitruvius structure;
3. **AI proposals** — candidate links, summaries, or relationships that are not truth until admitted.

Target answer shape:

```text
question
-> node/concept resolution
-> graph traversal
-> source/resource retrieval
-> evidence-aware answer
-> citations/provenance
-> visible reasoning path
```

## 2. Core Pipeline Purpose

| Layer | Role in the north star | Current expectation |
|---|---|---|
| `001_Raw-Source-Layer/` | Immutable custody for original PDFs, scans, handouts, books, and other source documents | never rewrite raw sources |
| `002_Raw-Conversion-Layer/` | OCR/conversion/extraction staging | not admitted truth by itself |
| `003_Canonical-Knowledge-Layer/` | trusted source artifacts, source records, and evidence-prep outputs | source/evidence attachment layer |
| `004_Derived-Content-Layer/` | generated summaries, study outputs, and downstream content | derived only; cannot redefine truth |
| `005_Operational-Intelligence-Layer/` | chunks, embeddings, graph snapshots, fast indexes, future projections | query/runtime acceleration |
| `006_System-Manifests/` | manifests, registries, admissions, validations, approvals, transaction custody | audit and truth governance |

## 3. Current Baseline

Latest independently audited stable baseline from Phase 5 Final Custody Closure:

- active admitted relationships: 264
- effective graph edges: 13,934
- base graph edges: 13,670
- nodes: 10,018
- active relation families: 15
- P1 packets/reviews: 20/20
- aliases / redirects / tombstones: 0 / 0 / 0
- Resource Layer: 7 resources / 9 nodeResourceLinks
- latest afterHash mismatches: 0
- manifest chain valid: true

Current repository may contain newer uncommitted work. Treat new counts as unverified until validators and audits update this tracker.

## 4. Achieved

| Area | Status | Evidence |
|---|---|---|
| Authored AEC-MEPFS backbone | implemented locally/file-backed | `006_System-Manifests/aec-mepfs-backbone/` |
| Graph relationship enrichment | active and materially improved | `006_System-Manifests/graph-canonical/admitted-relationships.json` |
| Relationship visibility | validated in API/Explorer paths | `api/graphReasoningPaths.test.ts`, graph validators |
| Canonical stewardship | active with transaction manifests and approvals | `006_System-Manifests/graph-canonical/` |
| Resource Layer | file-backed baseline exists | `bun run api/validateResourceLayer.ts -- --no-write` |
| No destructive graph mutation rule | preserved in latest audited baseline | aliases/redirects/tombstones remain zero |
| Database projection direction | planned | `/.ai/03_plans/2026-05-03_vitruvius_database_projection_architecture_plan.md` |

## 5. Main Open Workstreams

### A. Source coverage and resource attachment

**Goal:** important nodes and relationships should point to real source resources or explicitly state that they are admitted domain-synthesis relationships.

Current gaps to track:

- node-to-resource coverage percentage;
- admitted relationship-to-evidence coverage percentage;
- high-value nodes with no resource links;
- source-backed vs domain-synthesis vs proposal-only classification;
- protected-payload/source-rights blockers.

### B. AI-assisted proposal workflow

**Goal:** add Python/AI workflows that propose relationships, source links, and evidence candidates without directly mutating canonical truth.

Required gates:

- proposal-only default;
- no fake source metadata;
- no protected payload copying;
- duplicate/base-edge checks;
- relation vocabulary gate;
- source/context gate;
- steward admission;
- transaction manifest;
- rollback preview;
- validation report.

### C. Graph reasoning quality

**Goal:** graph relationships should improve traversal and reasoning, not only count.

Metrics to track:

- relation-family distribution;
- dominant relation-family audits, especially `COORDINATES_WITH`;
- reasoning-path hard-passing tests;
- source/resource availability on answer-critical paths;
- high-risk duplicate/canonical packets remaining blocked.

### D. Retrieval and answer grounding

**Goal:** future AI answers should retrieve source material and graph paths together.

Needed capabilities:

- node resolver;
- source/resource lookup by node and relationship;
- chunk/evidence retrieval;
- graph path retrieval;
- answer composer that labels source-backed facts vs graph reasoning vs proposal.

### E. Fast serving projections

**Goal:** make the system fast without making projection stores canonical truth.

Preferred architecture:

```text
current canonical file/manifests custody
-> optional Postgres import-only/queryable custody prototype after future AD
-> deterministic projection manifests
-> Memgraph for dynamic graph traversal
-> API in-memory compiled adjacency for hottest UI/runtime paths
```

## 6. Milestone Roadmap

| Milestone | Status | Definition of done |
|---|---|---|
| M0 Purpose reconciliation | in progress | README and `.ai` docs name source-grounded KG AI as the north star |
| M1 Coverage inventory | not started | no-write report lists node/resource and relationship/evidence coverage |
| M2 Proposal-only AI script contract | not started | script produces candidate queues, not canonical mutations |
| M3 Source-link admission workflow | gated | source/resource links admitted with validation and rollback |
| M4 Reasoning plus evidence tests | not started | priority answer paths require graph path plus source/resource support |
| M5 Retrieval prototype | not started | AI answer prototype retrieves sources and graph paths with provenance labels |
| M6 Database projection benchmark | planned | API memory vs Memgraph vs Neo4j/Postgres projection benchmark on Vitruvius workloads |
| M7 Production projection readiness | blocked | credentials, backup/restore/rollback proof, no-write validators, and security review complete |

## 7. Current Risks

| Risk | Severity | Mitigation |
|---|---:|---|
| Graph edge count becomes mistaken for product maturity | High | track source coverage and reasoning quality, not only edge totals |
| AI proposals become admitted truth without gates | High | proposal-only script contract and admission manifests |
| Sources are referenced vaguely rather than through real resource/evidence links | High | Resource Layer coverage report and evidence-link validation |
| Protected payload leaks into graph or projections | High | store source IDs/selectors/provenance, not protected text |
| Database projections bypass custody | High | current canonical file/manifests remain truth; Postgres is import-only/prototype until future AD; Memgraph/API memory are rebuildable projections |
| High-risk duplicate packets get accidentally resolved | High | keep merge/alias/redirect/tombstone gates blocked without explicit steward authority |

## 8. Tracker Update Rules

Update this file when any of these change:

- admitted relationship count or relation-family distribution;
- Resource Layer resource/link count;
- source-to-node or source-to-relationship coverage;
- AI proposal/admission workflow behavior;
- graph reasoning test coverage;
- database projection architecture;
- high-risk packet status;
- production/protected-payload gate status.

Do not update this tracker with unverified success claims. If a metric is not freshly validated, label it as reported or unverified.

## 9. Immediate Next Actions

1. Build a no-write source/resource coverage inventory for graph nodes, admitted relationships, and answer-critical paths.
2. Define `SourceGroundedAnswerContext` before any AI answer composer: resolved nodes, graph paths, learner-safe resources, evidence claim selectors, claim classes, and safety boundaries.
3. Add edge/resource/evidence join planning around `NodeResourceLink.supportsEdgeIds` and `evidenceClaimIds`.
4. Define the append-only AI proposal queue contract with local Ollama baseline, optional cloud batch acceleration, source-rights preflight, budget caps, redaction, and no direct admission.
5. Design a non-mutating Explorer answer panel with claim-to-citation grouping and rights-safe citation display.
6. Benchmark API in-memory projection before Memgraph/Neo4j projection work or any Postgres import-only custody prototype.
7. Benchmark `spatial-daemon` before any new Rust port; keep Rust out of source custody, admission, and AI orchestration.

## 10. 2026-05-03 Plan Improvement Checkpoint

**Status:** plan improved, implementation still gated.

New governing support artifacts:

- `.ai/13_research/2026-05-03_source_grounded_kg_ai_acceleration_research_pack.md`
- `.ai/02_audits/2026-05-03_source_grounded_kg_ai_plan_improvement_audit.md`
- `.ai/03_plans/2026-05-03_source_grounded_kg_ai_execution_acceleration_plan.md`
- `.ai/05_logs/2026-05-03_source_grounded_kg_ai_plan_improvement_validation.md`

Accepted direction:

- API: build answer context before answer generation.
- Explorer: add a non-mutating answer panel rather than reusing selected-node hydration or query-result merge behavior.
- Database: API memory first, Postgres import-only parity prototype later, Memgraph/Neo4j projection-only after benchmark.
- Rust: benchmark narrow compute kernels only; `spatial-daemon` is a candidate for a future Rust packet, not an authorized port.
- AI: local-first proposal/review baseline, cloud batch acceleration only with explicit opt-in, budgets, source-rights preflight, and no admission authority.

Current state remains unchanged for graph/source truth:

- No graph admission.
- No Resource Layer mutation.
- No canonical or raw source mutation intended by this checkpoint.
- No production database write.
- No protected payload copying.
