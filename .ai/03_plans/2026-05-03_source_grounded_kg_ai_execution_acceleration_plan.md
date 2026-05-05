# Source-Grounded KG AI Execution Acceleration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans only after a concrete implementation packet from this plan is approved. This is a plan-improvement artifact; it does not authorize graph, Resource Layer, database, or protected-source mutation.

**Goal:** Convert the source-grounded KG AI north star into a concrete, high-throughput execution sequence across API, Explorer, database projections, Rust optimization, and local/cloud AI acceleration.

**Architecture:** Build a read-only, citation-ready answer context before answer generation. Keep canonical custody in file/manifests for now. Use AI to propose and review, not admit. Use API memory for hot graph reads first, Memgraph/Postgres only as governed projections/prototypes, and Rust only for measured deterministic kernels.

**Tech Stack:** Bun API, Explorer React app, Resource Layer, graph-canonical manifests, Python proposal/coverage scripts, local Ollama, optional cloud batch APIs, API in-memory graph index, future PostgreSQL import-only custody prototype, future Memgraph projection, Rust/PyO3/Wasm kernels only after benchmarks.

## Status

- **Status:** active planning improvement.
- **Created:** 2026-05-03.
- **Non-authorization:** This plan does not authorize graph admission, Resource Layer mutation, production database writes, protected payload use, source rewrite, merge/alias/redirect/tombstone, P0/P1 duplicate resolution, or AI-generated truth admission.

## Execution Order

### Phase 0 - No-write coverage inventory

**Purpose:** know what is grounded before building answer AI.

**Deliverables:**

- [ ] No-write report for graph node source/resource coverage.
- [ ] No-write report for admitted relationship evidence/resource support.
- [ ] Classification: `source_backed`, `domain_synthesis`, `proposal_only`, `unsupported`, `blocked_by_rights`.
- [ ] Counts by node type, relation type, source family, and critical answer path.
- [ ] Validation that report generation mutates zero graph/canonical/resource files.

**Likely files:**

- `api/resourceLayer/*`
- `api/validateResourceLayer.ts`
- `006_System-Manifests/graph-canonical/admitted-relationships.json`
- future report under `006_System-Manifests/...` or `.ai/13_research/...` after packet approval.

### Phase 1 - SourceGroundedAnswerContext contract

**Purpose:** define what the AI is allowed to see and cite before generation exists.

**Contract shape:**

```ts
interface SourceGroundedAnswerContext {
  question: string;
  resolvedConcepts: Array<{ nodeId: string; label: string; confidence: number }>;
  graphPaths: Array<{ edgeIds: string[]; relationTypes: string[]; classification: string }>;
  resources: Array<{ resourceId: string; title: string; rightsStatus: string; verificationStatus: string }>;
  evidenceClaims: Array<{ claimId: string; resourceId: string; nodeId?: string; edgeId?: string; selector: { sourceId: string; locator: string; pageOrSection?: string; hash?: string }; displayPolicy: 'payload_free' | 'rights_cleared_snippet' | 'metadata_only' }>; // no raw protected text
  claimClasses: Array<'source_backed_fact' | 'admitted_graph_reasoning' | 'proposal_only' | 'insufficient_evidence'>;
  safetyBoundaries: string[];
}
```

**Deliverables:**

- [ ] Backend type/schema for answer context.
- [ ] Tests proving no mutation and no protected payload exposure.
- [ ] Empty/no-result/conflict behavior.
- [ ] Explicit labeling of graph reasoning vs source-backed facts.

### Phase 2 - Edge/resource/evidence join helpers

**Purpose:** answers usually rely on relationships, not just nodes.

**Deliverables:**

- [ ] Resource lookup by `nodeId` and by `edgeId` using existing `NodeResourceLink.supportsEdgeIds`.
- [ ] Evidence claim lookup by graph path.
- [ ] Unsupported edge classification.
- [ ] Rights-safe evidence selectors instead of protected raw excerpts.
- [ ] Tests for source-backed path, graph-only path, unsupported path, and protected path.

### Phase 3 - Read-only answer-context endpoint

**Candidate route:** `POST /v2/answer/context`.

**Flow:**

1. Resolve question with existing resolver logic.
2. Load graph index from existing API memory path.
3. Build relevant neighborhoods/paths.
4. Attach learner-safe resources and source metadata.
5. Attach evidence claim selectors.
6. Return context only; no LLM call, no mutation, no external service.

**Gates:**

- [ ] No-write validator passes before/after route tests.
- [ ] Protected source data is redacted or omitted.
- [ ] All answer claims are classified before any composer work.

### Phase 4 - Explorer KG Answer Panel

**Purpose:** show answer context without mutating the graph canvas.

**Deliverables:**

- [ ] New non-mutating answer panel separate from selected-node hydration and Cypher query results.
- [ ] Claim-to-citation grouping.
- [ ] Reasoning path list with admitted edge IDs and relation types.
- [ ] Badges for source-backed facts, graph reasoning, proposal-only, and insufficient evidence.
- [ ] Rights-safe citation rendering: show selector/provenance when snippet display is not allowed.
- [ ] Tests that answer panel does not merge nodes/edges into current graph state by default.

### Phase 5 - AI proposal and cloud acceleration packet

**Purpose:** use AI to make work faster while preserving custody.

**Operating model:**

```text
local source/graph context -> proposal queue -> local Ollama review -> optional cloud batch/adjudication -> deterministic gates -> steward admission packet
```

**Deliverables:**

- [ ] Append-only proposal queue schema for relationship, source-link, evidence-claim, summary, and Resource Layer candidates.
- [ ] Local-first result envelope shared by proposal scripts.
- [ ] Optional cloud mode with explicit opt-in, provider allowlist, budget/call caps, retry/resume, and redaction.
- [ ] Structured-output schema for candidate results.
- [ ] Batch mode support for non-interactive candidate review where source-rights allow it.
- [ ] Tests blocking protected/unknown source payloads from cloud prompts.

**Cloud policy:**

- Cloud AI may accelerate extraction, classification, review, and critique.
- Cloud AI must not write canonical truth.
- Cloud outputs remain candidates until admitted by deterministic gates and steward approval.
- Secrets must stay in environment variables and never be persisted.

### Phase 6 - API in-memory projection formalization

**Purpose:** make the current fastest hot path explicit and benchmarked.

**Deliverables:**

- [ ] Versioned projection artifact/hash for API memory graph index.
- [ ] p50/p95/p99 benchmark for node lookup, search, depth-1 neighborhood, relation filters, and answer-context assembly.
- [ ] Atomic pointer/cache-version strategy.
- [ ] No-write projection validation.
- [ ] Degraded-mode behavior if graph DB is unavailable later.

### Phase 7 - Postgres import-only custody prototype

**Purpose:** prepare durable queryable custody without switching truth.

**Deliverables:**

- [ ] Import-only tables for nodes, edges, admitted relationships, approvals, manifests, resources, reviews, and evidence selectors.
- [ ] Hash parity from JSON/manifests to Postgres staging.
- [ ] Foreign-key indexes, composite indexes for common filters, COPY/batch import path, and connection pooling plan.
- [ ] Explicit no-dual-write rule.
- [ ] Future AD plus parity gates required before Postgres can become canonical custody; until then it is import-only/queryable prototype.

### Phase 8 - Memgraph projection benchmark

**Purpose:** evaluate fast dynamic graph traversal as projection-only runtime.

**Deliverables:**

- [ ] Deterministic projection package from canonical custody.
- [ ] Memgraph load script under projection run ID.
- [ ] Cypher queries for depth-2/depth-3 traversal, path existence, relation-family distribution, and GraphRAG expansion.
- [ ] Projection hash and rollback pointer.
- [ ] Benchmark against API memory and optional Neo4j local projection.
- [ ] Read-only app role and mutation-only projection loader.

### Phase 9 - Rust performance benchmark packet

**Purpose:** identify real compute bottlenecks before writing Rust.

**Deliverables:**

- [ ] Workload census for graph reads, answer-context assembly, spatial-daemon contexts, and source/evidence processing.
- [ ] `spatial-daemon/src/cli.ts` pairwise AABB benchmark may be proposed in a future Rust packet for 100, 1k, 5k, 10k entities.
- [ ] Include output serialization and deterministic ordering checks.
- [ ] Consider Rust/Wasm/PyO3 only if the applicable Rust governance benchmark gate is met and contract parity is proven.
- [ ] Do not port source custody, evidence admission, graph truth, AI orchestration, or policy interpretation.

## Acceptance Criteria

- [ ] Plans clearly prioritize source grounding and answer context over raw edge count.
- [ ] No implementation packet admits graph/resource/canonical truth without gates.
- [ ] AI proposal workflows are proposal-only by default.
- [ ] Database projections are rebuildable and non-canonical until future AD.
- [ ] Rust candidates have benchmark gates and governance boundaries.
- [ ] Explorer answer UI is non-mutating and rights-safe.
- [ ] Every future packet has no-write validation and rollback/manifest strategy where applicable.

## Validation Commands for Future Packets

```powershell
bun run api/validateGraphRelationships.ts -- --no-write
bun run api/validateCanonicalGraphStewardship.ts -- --no-write
bun run api/validateResourceLayer.ts -- --no-write
bun test api/graphReasoningPaths.test.ts
cd api; bun test
cd explorer; bun test
cd explorer; bun run build
.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py
```

## External Research Basis

Retrieved 2026-05-03:

- OpenAI Batch API: https://platform.openai.com/docs/guides/batch
- OpenAI Structured Outputs: https://platform.openai.com/docs/guides/structured-outputs
- Anthropic Message Batches: https://docs.anthropic.com/en/docs/build-with-claude/batch-processing
- Google Gemini Batch API: https://ai.google.dev/gemini-api/docs/batch-mode
- Memgraph storage/memory docs: https://memgraph.com/docs/fundamentals/storage-memory-usage
- PostgreSQL materialized views: https://www.postgresql.org/docs/current/rules-materializedviews.html
- PostgreSQL logical replication: https://www.postgresql.org/docs/current/logical-replication.html

## Final Position

The fastest safe plan is:

```text
source/resource/evidence coverage inventory
-> answer-context contract
-> proposal-only AI acceleration
-> non-mutating answer UI
-> API-memory benchmark
-> Postgres import-only parity
-> Memgraph projection benchmark
-> Rust only for measured kernels
```

This keeps Vitruvius fast without letting AI, graph databases, or Rust bypass custody and admission truth.
