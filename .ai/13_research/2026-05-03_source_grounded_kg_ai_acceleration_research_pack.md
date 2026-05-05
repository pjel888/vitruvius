# Source-Grounded KG AI Acceleration Research Pack

**Date:** 2026-05-03  
**Task:** improve the source-grounded KG AI plans across API, Explorer, database projections, Rust optimization, and cloud AI acceleration.  
**Mode:** planning and analysis only. No graph, canonical, resource, or production database mutation.

## 1. Scope

Vitruvius is moving toward an AI answer system that joins:

```text
question -> resolved graph nodes -> admitted graph paths -> learner-safe resources -> evidence claims -> cited answer
```

This research pack improves the existing north-star and database plans with evidence from:

- API/backend graph and resolver code;
- Explorer selected-node and source/evidence UI;
- current Postgres/Neo4j/KV migration surfaces;
- Rust kernel and spatial-daemon performance candidates;
- local/cloud AI proposal and review paths;
- official external docs for Batch APIs, structured outputs, Memgraph, PostgreSQL, and related projection choices.

## 2. Repository baseline from targeted inspection

### API/backend

Local inspection found the current backend has the pieces for graph exploration but not yet a full cited answer context:

- `api/index.ts` exposes `POST /v2/resolve`, `GET /v2/sources/:source_id`, `GET /node/:id/neighborhood`, `GET /node/:id`, and `GET /edge/:id`.
- `readAecMepfsBackboneGraphArtifacts` loads file-backed graph artifacts and admitted canonical overlays.
- `getAecMepfsExplorerGraphIndex` builds in-memory maps for nodes, edges, incoming/outgoing adjacency, search fields, and cached search.
- `buildAecMepfsNodeDetail` and `buildAecMepfsEdgeDetail` already expose evidence-shaped fields, but current evidence arrays are empty.
- Resource Layer types already include `NodeResourceLink.supportsEdgeIds` and `evidenceClaimIds`, but edge/resource joins are not yet first-class answer-path behavior.

Accepted implication: the next backend packet should be a read-only `SourceGroundedAnswerContext` contract before any AI answer composer.

### Explorer/UI

The Explorer has useful graph and source inspection primitives, but they are not organized around answer claims:

- `explorer/src/App.tsx` auto-hydrates selected node neighborhoods.
- `explorer/src/components/inspector/NodeInspector.tsx` renders resources, source warnings, and evidence/source tabs.
- `explorer/src/components/inspector/EdgeInspector.tsx` renders edge evidence structures.
- `explorer/src/components/BottomDrawer.tsx` can display source excerpts and query result rows.

Accepted implication: do not repurpose selected-node hydration or the Cypher query panel as the AI answer UI. Add a non-mutating answer panel that shows resolved nodes, source-backed claims, admitted graph reasoning, citations, and proposal-only caveats.

### Database/projection/migration

Vitruvius is still file-backed and manifest-governed. Databases are projections unless a future architecture decision changes custody truth.

Current evidence:

- `scripts/vitruvius/graph/snapshot.py` and `scripts/vitruvius/graph/builder.py` produce deterministic file-backed graph snapshots.
- `scripts/vitruvius/kg/postgres_client.py` and `scripts/vitruvius/db/schema.sql` provide Postgres registry/staging primitives, not a canonical custody migration.
- `scripts/vitruvius/kg/neo4j_loader.py` and `scripts/vitruvius/kg/neo4j_client.py` provide optional Neo4j projection/write capability, including reset helpers that remain production-gated.
- `api/index.ts` includes a `/query` Cypher route; this must be treated as local/dev or tightly restricted before production.
- No Memgraph runtime implementation was found; Memgraph is currently a planning candidate.

Accepted implication: API memory first, then import-only Postgres parity, then projection-only Memgraph/Neo4j benchmark. No direct production DB mutation.

### Rust/performance

Existing Rust work is aligned with governance: narrow kernels with fallbacks and benchmark proof.

Current assets:

- `scripts/vitruvius/engine_rs/spatial_kernels/src/adjacency_edges.rs` for spatial adjacency.
- `scripts/vitruvius/engine_rs/spatial_kernels/src/distance_weight.rs` for distance weighting.
- `scripts/vitruvius/engine_rs/stats_kernels/src/mahalanobis.rs` for scoring.
- `scripts/vitruvius/datalog_rs/src/lib.rs` as a narrow proof kernel, not a general rule engine.
- `spatial-daemon/src/cli.ts` still performs pairwise AABB loops and is the best next benchmark candidate if input sizes justify it.

Accepted implication: do not port KG truth, evidence admission, AI orchestration, or source governance to Rust. Benchmark `spatial-daemon` only through a future Rust packet; consider graph traversal Rust only after API-memory and Memgraph/Postgres benchmarks prove a bottleneck.

### AI acceleration

Existing AI posture is correct: local-first, proposal-only, cloud optional.

Evidence:

- `config/vitruvius.yaml` defaults local Ollama and keeps `review.cloud.enabled: false`.
- `scripts/vitruvius/ollama_review.py` provides local review behavior.
- `scripts/vitruvius/cloud_review_adjudication.py` provides optional cloud adjudication.
- `scripts/vitruvius/relationships/llm_proposer.py` and `scripts/vitruvius/kg/aec_relationship_improvement.py` already show candidate/proposal patterns.
- `aec_relationship_improvement.py` is the strongest precedent: explicit `--allow-cloud-ai`, allowlisted endpoints, budgets/caps, pending-only outputs, sanitization, ledger reuse, and deterministic final guards.

Accepted implication: cloud AI should be used for speed through batch proposal/review lanes, but all outputs remain candidates until admitted.

## 3. External research basis

Retrieved 2026-05-03. These are evidence inputs, not admitted Vitruvius truth.

- OpenAI Batch API: https://platform.openai.com/docs/guides/batch
- OpenAI Structured Outputs: https://platform.openai.com/docs/guides/structured-outputs
- OpenAI embeddings guide: https://platform.openai.com/docs/guides/embeddings
- OpenAI file search guide: https://platform.openai.com/docs/guides/tools-file-search
- Anthropic Message Batches: https://docs.anthropic.com/en/docs/build-with-claude/batch-processing
- Anthropic tool use / JSON schema: https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview
- Google Gemini Batch API: https://ai.google.dev/gemini-api/docs/batch-mode
- Google Gemini structured output: https://ai.google.dev/gemini-api/docs/structured-output
- Memgraph storage/memory usage docs: https://memgraph.com/docs/fundamentals/storage-memory-usage
- Memgraph storage modes overview: https://memgraph.com/blog/memgraph-storage-modes-explained
- PostgreSQL materialized views: https://www.postgresql.org/docs/current/rules-materializedviews.html
- PostgreSQL logical replication: https://www.postgresql.org/docs/current/logical-replication.html
- Neo4j schema/index docs: https://neo4j.com/docs/getting-started/cypher/schema/
- Supabase Postgres best-practice local skill reference (`C:/Users/phili/.codex/plugins/cache/openai-curated/supabase/3c463363/skills/supabase-postgres-best-practices/SKILL.md`, retrieved 2026-05-03): index WHERE/JOIN columns, foreign keys, composite indexes, batch inserts/COPY, and use connection pooling for application workloads; authoritative SQL behavior should still be checked against official PostgreSQL docs for implementation.

## 4. Subagent findings and disposition

| Agent | Lane | Main suggestion | Disposition |
|---|---|---|---|
| Fermat | API/backend | Build a read-only answer-context builder before any AI composer. Populate source/resource/evidence joins, especially edge support. | Accepted. Added as Phase 1/2 in the execution acceleration plan. |
| Carver | Explorer/UI | Add a non-mutating KG Answer Panel; reuse resource/evidence components but organize around claim-to-citation mapping. | Accepted. Added as Explorer Phase 4 and test gate. |
| Socrates | DB/projection | Keep file manifests canonical; API memory first; Postgres import-only parity; Memgraph/Neo4j projection-only after benchmark. | Accepted. Reinforces the database projection plan. |
| Aristotle | Rust/performance | Do not port KG governance to Rust. Benchmark `spatial-daemon` pairwise geometry first; graph traversal Rust only if measured. | Accepted. Added Rust benchmark gate and explicit non-candidates. |
| Popper | AI integration | Standardize local/cloud AI around proposal-only queues, source-rights preflight, cloud opt-in, budget caps, sanitization, and no admission authority. | Accepted. Added AI acceleration packet. |

Rejected/deferred:

- Direct AI answer generation before answer-context contract: rejected for now.
- Direct Memgraph/Postgres/Neo4j production writes: rejected under current gates.
- Rust for source custody, evidence materialization, graph admission, or AI orchestration: rejected.
- Broad cloud AI use on protected/unknown source text: rejected unless source-rights policy clears it.
- General-purpose Datalog expansion: deferred until fact/rule semantics and deterministic output contracts are defined.

## 5. Planning conclusion

The best next work is not more raw graph-edge admission. It is a sequenced source-grounding and answer-context program:

1. no-write coverage inventory;
2. answer-context contract;
3. edge/resource/evidence joins;
4. proposal-only AI queue and cloud batch acceleration;
5. non-mutating Explorer answer UI;
6. API memory projection benchmark;
7. Postgres/Memgraph projection prototypes after parity and rollback gates;
8. Rust only where benchmarks justify a narrow compute kernel.
