# Source-Grounded KG AI Plan Improvement Audit

**Date:** 2026-05-03  
**Scope:** audit the current plan set and identify the safest next implementation sequence for source-grounded KG AI.  
**Mode:** docs/plans only. No graph, canonical, resource, or database mutation.

## 1. Audit verdict

**Verdict:** plans are directionally correct, but the next work needs tighter sequencing.

The existing north-star and database projection plans correctly identify the product goal and the future serving architecture. The main gap is that they need to turn into concrete, gated implementation packets in the right order:

```text
coverage inventory -> answer context -> evidence joins -> AI proposals -> answer UI/composer -> projections -> Rust kernels only if measured
```

## 2. What is already strong

- The repository now names source-grounded KG AI as the product north star.
- The raw/conversion/canonical layers are correctly framed as custody and evidence-prep infrastructure.
- The graph relationship work is correctly framed as reasoning structure, not final answer truth.
- Resource Layer validation exists and already protects learner exposure.
- API memory graph indexing already exists and should be formalized before adding a graph database.
- Cloud AI is already default-disabled and local-first review exists.
- Existing Rust governance already blocks unbenchmarked or semantics-heavy Rust ports.

## 3. Gaps that need plan-level repair

| Gap | Severity | Evidence | Required plan response |
|---|---:|---|---|
| No answer-context contract yet | High | Resolver returns node/source refs, not citation-ready evidence claims | Define read-only `SourceGroundedAnswerContext` before composer work |
| Node/edge detail evidence arrays are currently empty | High | `buildAecMepfsNodeDetail`, `buildAecMepfsEdgeDetail` expose empty evidence | Add edge/resource/evidence join plan |
| Resource coverage is sparse relative to graph size | High | Tracker baseline: 7 resources / 9 nodeResourceLinks vs 10,018 nodes | Make no-write source coverage inventory the first packet |
| Explorer source UI is fragmented | Medium | NodeInspector/EdgeInspector/BottomDrawer render source pieces separately | Add claim-level answer panel plan |
| Postgres schema could be mistaken as canonical custody | High | Existing schema includes file registry/document version tables | Keep Postgres import-only until explicit AD/parity gate |
| Neo4j query/write surfaces need production hardening | High | Optional loader/reset helpers and `/query` route exist | Require read-only users, parameterization/allowlists, and production query review |
| Memgraph is not implemented | Medium | Planning only | Treat as projection prototype after benchmark, not current dependency |
| Cloud AI could become effective authority | High | Cloud adjudication can affect review recommendation | Require proposal-only status, budgets, allowlists, redaction, and admission separation |
| Rust enthusiasm could cross governance boundary | Medium | User requested Rust optimizations broadly | Limit Rust to measured deterministic kernels with 2x gate |

## 4. Safety invariants preserved by the improved plan

- No fake sources, URLs, editions, standards context, AHJ claims, or numerical criteria.
- No protected payload copying into prompts, graph properties, database rows, or UI snippets without rights clearance.
- No graph admission or Resource Layer mutation from this planning pass.
- No production Neo4j, Memgraph, or Postgres write path authorization.
- No merge, alias, redirect, tombstone, or canonical ID migration.
- AI remains proposal/review acceleration only.
- Databases remain projections or import-only custody prototypes until a future architecture decision.

## 5. Plan critique

The previous plans were correct at the concept level but under-specified these operational gates:

1. Coverage metrics must come before source-link admission.
2. Answer context must come before answer generation.
3. Evidence selectors and rights-safe display policy must come before UI snippets.
4. API in-memory projection should be benchmarked before Memgraph/Neo4j debate.
5. Postgres must start import-only; switching canonical custody is a separate future AD.
6. Cloud batch AI should accelerate candidate generation/review, not write truth.
7. Rust should start with workload census and spatial-daemon benchmark, not KG semantics.

## 6. Recommended immediate sequence

1. Create `source_grounding_coverage_report` no-write script/report.
2. Define `SourceGroundedAnswerContext` TypeScript contract and tests.
3. Add Resource Layer helper plan for resources/evidence by edge ID/path ID.
4. Define append-only AI proposal queue schema and cloud batch operating envelope.
5. Design non-mutating Explorer answer panel UX and tests.
6. Formalize API-memory projection benchmark and versioned projection artifact.
7. Draft Postgres import-only schema parity packet.
8. Draft Memgraph projection benchmark packet.
9. Draft spatial-daemon Rust benchmark packet.

## 7. Stop conditions

Stop automation before implementation if any packet would:

- read protected source payload into cloud AI;
- write graph/resource/canonical registries without explicit admission packet;
- treat Postgres/Memgraph/Neo4j as canonical truth;
- add Rust for policy/source/AI orchestration;
- expose raw local source paths or protected snippets in Explorer;
- claim source-backed answers without resource/evidence IDs.
