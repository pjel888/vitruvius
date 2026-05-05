# Vitruvius Database Projection Architecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans only after this plan is explicitly promoted from planning reference to active implementation. This file is a planning artifact, not approval to mutate production graph data.

**Goal:** Define a future extremely-fast database architecture for Vitruvius graph/taxonomy/runtime serving without weakening canonical custody, admission, provenance, or rollback governance.

**Architecture:** Keep current canonical truth in deterministic file/manifests custody and admission ledgers; evaluate PostgreSQL only as an import-only/queryable custody prototype until a future AD and parity gates authorize any custody switch; project the admitted property graph into Memgraph for fast graph traversal; and compile the hottest API read paths into an in-memory adjacency projection. Memgraph and API memory are serving projections; they must never become the sole source of truth.

**Tech Stack:** Vitruvius file/manifests custody, optional PostgreSQL import-only prototype, Memgraph, API in-memory adjacency maps, deterministic projection builders, validation/hash manifests, optional Neo4j/TigerGraph comparison benchmarks.

---

## Status

- **Status:** planning reference only.
- **Created:** 2026-05-03.
- **Current-state assumption:** Vitruvius is still primarily file-backed for the AEC-MEPFS graph and canonical stewardship registries.
- **Non-authorization:** This plan does not authorize live Neo4j writes, Memgraph writes, Postgres migration, graph rebuild/reset, Resource Layer mutation, protected payload admission, or destructive graph operations.

## Current Fit

Vitruvius currently has a graph shape that is small enough for extremely fast in-process serving, while the product direction is governance-heavy enough that a graph database should not be treated as canonical truth.

The correct split is:

1. **Canonical custody / admission truth**
   - Existing manifests and registries now.
   - PostgreSQL later as an import-only/queryable custody prototype; canonical custody switch requires a future AD plus parity gates.
2. **Graph traversal projection**
   - Memgraph as the fast property-graph projection for Cypher-style 1-3 hop traversal, path reasoning, and graph analytics.
3. **Hottest runtime projection**
   - API-local compiled adjacency maps for selected-node hydration, dynamic relation filters, node inspector relationship lists, and shallow neighborhoods.

This keeps the core Vitruvius rule intact: **truth is admitted, not generated**.

## Recommended Target Architecture

```text
                       steward / admission workflow
                                  |
                                  v
        +----------------------------------------------------+
        | canonical custody ledger                           |
        | - current: JSON manifests and transaction chain     |
        | - future prototype: PostgreSQL import-only custody tables + hash parity ledger   |
        +----------------------------------------------------+
                                  |
                         deterministic projection
                                  |
                +-----------------+-----------------+
                |                                   |
                v                                   v
   +--------------------------+        +-----------------------------+
   | Memgraph graph projection|        | API in-memory compiled graph|
   | - Cypher traversal       |        | - adjacency maps            |
   | - path reasoning         |        | - relation-family filters   |
   | - graph algorithms       |        | - selected-node hydration   |
   +--------------------------+        +-----------------------------+
                |                                   |
                +-----------------+-----------------+
                                  |
                                  v
                         API / Explorer / GraphRAG
```

## Why This Is the Fast Path

### 1. API in-memory compiled graph is fastest for current hot paths

For current-scale selected-node hydration and shallow neighborhoods, the fastest read path is not a remote database call. It is a precompiled process-local structure:

- `Map<nodeId, NodeRecord>`
- `Map<nodeId, EdgeRecord[]>` for outgoing, incoming, and both-direction adjacency
- `Map<relationType, EdgeRecord[]>`
- optional precomputed 1-hop neighborhood payloads for very hot nodes

This should serve:

- `GET /node/:id/neighborhood?depth=1&direction=both`
- Explorer selected-node hydration
- dynamic edge filters
- Node Inspector relationship lists

### 2. Memgraph is the speed-first graph projection

Memgraph is a good first graph database candidate for Vitruvius because it is designed around in-memory graph operation, supports Cypher-style graph querying, and provides transactional/persistent modes. Its official materials describe low-latency graph workloads, persistence/ACID guarantees, and in-memory transactional storage with snapshots/WAL for recovery.

Use Memgraph for:

- 2-3 hop reasoning paths.
- relation-family traversal.
- path existence checks.
- graph algorithms.
- graph-aware RAG expansion.
- query patterns that are too dynamic to precompute in the API process.

Do **not** let Memgraph become canonical truth. It is a projection rebuilt from admitted canonical state.

### 3. PostgreSQL is the durable custody and audit prototype

PostgreSQL is a better future candidate than a graph database for queryable custody/audit tables, but it remains import-only/prototype until a future AD changes canonical truth. It is attractive because Vitruvius needs:

- deterministic admission tables,
- transaction manifests,
- approvals,
- review records,
- resource links,
- source-rights metadata,
- hash-chain validation,
- repair/audit queries,
- controlled migration and rollback.

PostgreSQL logical replication can support incremental subscribers/projections later, but the first version should stay simpler: deterministic projection jobs from canonical tables/manifests into Memgraph plus an API-local compiled graph snapshot.

## Proposed Data Ownership

### Canonical layer

Canonical state remains the only admitted truth source.

Future import-only PostgreSQL prototype tables should model:

- `canonical_nodes`
- `canonical_edges`
- `admitted_relationships`
- `relation_vocabulary`
- `steward_approvals`
- `stewardship_decisions`
- `transaction_manifests`
- `projection_runs`
- `projection_hashes`
- `resources`
- `node_resource_links`
- `p1_decision_packets`
- `p1_packet_reviews`

### Memgraph projection

Memgraph should contain only projection-safe records:

- admitted nodes,
- base edges,
- admitted overlay edges,
- relation types,
- relation family metadata,
- provenance pointers by ID only,
- projection run ID,
- canonical hash references.

Memgraph should not contain protected source payloads, copied standards text, reviewer text, AHJ assertions, or unadmitted candidate edges.

### API in-memory projection

The API should compile from a validated projection artifact:

- `nodesById`
- `outEdgesByNodeId`
- `inEdgesByNodeId`
- `bothEdgesByNodeId`
- `edgesByRelationType`
- `visibleEdgesByExplorerFilter`
- `nodeInspectorRelationshipRows`

This gives the UI the fastest possible common path and leaves Memgraph for deeper traversal.

## Write Path

- [ ] Validate a proposed steward/admission action against relation vocabulary, source/context gates, duplicate checks, and high-risk gates.
- [ ] Write canonical admission data only through the governed custody workflow.
- [ ] Emit a transaction manifest with before/after hashes.
- [ ] Run canonical validation and graph relationship validation.
- [ ] Build a staging projection from canonical state.
- [ ] Compare staging node/edge/relation-family counts against expected hashes.
- [ ] Load staging projection into Memgraph under a projection run ID.
- [ ] Compile API-local adjacency maps from the same projection artifact.
- [ ] Run graph visibility and reasoning-path tests against both API memory and Memgraph.
- [ ] Atomically promote the projection pointer only after validation passes.

## Read Path

- [ ] Serve depth-1 node neighborhoods from the API in-memory adjacency map.
- [ ] Serve selected-node hydration and Node Inspector relationships from the API in-memory projection.
- [ ] Serve dynamic relation-family filters from precomputed relation maps.
- [ ] Serve 2-3 hop dynamic graph reasoning paths from Memgraph.
- [ ] Serve source/provenance/custody detail from canonical tables/manifests, not from graph projection properties.
- [ ] For GraphRAG, use Memgraph for expansion and canonical custody for evidence/provenance.

## Implementation Phases

### Phase 0 - Planning and benchmark definition

- [ ] Freeze benchmark workloads before picking a database as "fastest."
- [ ] Define datasets: current graph, 10x graph, 100x graph, and synthetic high-degree stress graph.
- [ ] Define read workloads: depth-1 hydration, depth-2 traversal, depth-3 traversal, relation filter, path existence, GraphRAG expansion, provenance lookup.
- [ ] Define write workloads: admitted-edge batch projection, rollback replay, hash-chain validation, Memgraph reload, API snapshot swap.

### Phase 1 - API in-memory compiled projection

- [ ] Add a projection builder that compiles current file-backed canonical graph artifacts into adjacency maps.
- [ ] Add API adapter tests proving selected-node hydration, dynamic filters, and Node Inspector rows can read from compiled memory.
- [ ] Add no-write validation proving projection compilation mutates no canonical files.
- [ ] Add p50/p95/p99 latency reporting without claiming external production thresholds.

### Phase 2 - PostgreSQL import-only custody schema prototype

- [ ] Draft import-only PostgreSQL schema for nodes, edges, admissions, approvals, decisions, resources, P1 reviews, and manifests.
- [ ] Add import-only migration from current JSON manifests into PostgreSQL staging tables.
- [ ] Add hash parity validation between JSON canonical files and PostgreSQL staging tables.
- [ ] Keep JSON manifests authoritative until a later architecture decision explicitly switches custody truth.

### Phase 3 - Memgraph projection prototype

- [ ] Add a local-only Memgraph projection loader from validated canonical artifacts.
- [ ] Add deterministic edge IDs and projection run IDs.
- [ ] Add Cypher queries for depth-2/depth-3 traversal, relation-family distribution, path existence, and graph reasoning tests.
- [ ] Add rollback by projection pointer swap, not ad hoc graph mutation.

### Phase 4 - Hybrid API routing

- [ ] Route depth-1 Explorer paths to API memory.
- [ ] Route deeper reasoning and dynamic path queries to Memgraph.
- [ ] Route provenance/custody detail to canonical manifests first, or to PostgreSQL only after import-only parity is proven.
- [ ] Add fallback behavior when Memgraph is unavailable.

### Phase 5 - Production-readiness gates

- [ ] Require backup/restore/rollback proof before any production graph database promotion.
- [ ] Require no-write validators for projection checks.
- [ ] Require manifest-chain closure for every projection artifact.
- [ ] Require validation that no Resource Layer mutation occurred during projection.
- [ ] Require security review for query parameterization and Cypher injection prevention.

## Benchmark Workloads

The database choice should be decided by Vitruvius workloads, not vendor claims.

Minimum benchmark cases:

- selected-node depth-1 neighborhood by node ID,
- selected-node depth-1 both-direction neighborhood with relation filter,
- depth-2 and depth-3 path expansion with relation whitelist,
- path existence from discipline to related concept,
- relation-family distribution query,
- high-degree node hydration,
- graph reasoning path regression suite,
- batch projection load,
- rollback pointer swap,
- cold start projection compile,
- warm API cache query.

## Safety Invariants

- [ ] Canonical custody remains source of truth.
- [ ] Memgraph is projection-only.
- [ ] API memory is projection-only.
- [ ] No direct production graph mutation.
- [ ] No graph rebuild/reset without a governed projection run.
- [ ] No fake sources, standards editions, AHJ claims, or numerical criteria.
- [ ] No protected payload copying into database properties.
- [ ] No Resource Layer mutation from projection jobs.
- [ ] No alias, redirect, tombstone, merge, or equivalence action unless separately authorized.
- [ ] Every projection has a manifest, afterHash, rollback pointer, and validation report.

## Recommended Default Decision

Use this default unless benchmark evidence disproves it:

1. **Canonical custody:** current JSON/file manifests remain truth; PostgreSQL is import-only/queryable custody prototype until a future AD and parity gates explicitly authorize a custody switch.
2. **Graph traversal projection:** Memgraph.
3. **Hottest API read path:** in-memory compiled adjacency projection.
4. **Maturity fallback:** Neo4j if operational maturity/ecosystem matters more than raw speed.
5. **Large distributed analytics fallback:** TigerGraph only if Vitruvius reaches genuinely massive graph scale where distributed graph analytics is required.

## Risks

| Risk | Severity | Mitigation |
|---|---:|---|
| Projection database becomes treated as truth | High | Make all writes flow through canonical custody and rebuild projections deterministically |
| Dual-write drift between Postgres, Memgraph, and API memory | High | Use one canonical write path plus projection manifests and hash checks |
| Direct Cypher/SQL mutation bypasses stewardship | High | Use read-only app users for projections where possible; lock mutation to projection loader |
| Cache/projection stale reads | Medium | Projection run IDs, atomic pointer swaps, and visible version metadata in API responses |
| Overengineering before scale requires it | Medium | Build API in-memory projection first; only add Memgraph/Postgres after benchmarks justify it |
| Query injection in dynamic traversal | Medium | Parameterized queries and relation/type allowlists |
| Protected payload leakage into projection properties | High | Store IDs and provenance pointers only, not protected text |

## Validation Commands for a Future Implementation

These are future commands, not commands run by this planning note.

```powershell
bun run api/validateGraphRelationships.ts -- --no-write
bun run api/validateCanonicalGraphStewardship.ts -- --no-write
bun run api/validateResourceLayer.ts -- --no-write
bun test api/graphReasoningPaths.test.ts
cd api; bun test
cd explorer; bun test
.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py
```

## External Research Basis

Retrieved on 2026-05-03:

- Memgraph database overview: https://memgraph.com/memgraphdb
- Memgraph storage modes overview: https://memgraph.com/blog/memgraph-storage-modes-explained
- PostgreSQL logical replication documentation: https://www.postgresql.org/docs/current/logical-replication.html
- Neo4j search-performance indexes documentation: https://neo4j.com/docs/cypher-manual/current/indexes/search-performance-indexes/
- TigerGraph DB overview: https://www.tigergraph.com/tigergraph-db/

## Final Position

The fastest defensible future architecture for Vitruvius is not one database doing everything. It is:

```text
JSON/file manifests as truth; PostgreSQL only as import-only/queryable custody prototype until future AD
-> deterministic projection manifests
-> Memgraph for dynamic graph traversal
-> API in-memory compiled adjacency for hottest UI/runtime paths
```

This gives Vitruvius speed without sacrificing custody, admission, rollback, source-rights, or graph-stewardship guarantees.
