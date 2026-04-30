---
task: explorer-performance-optimization
phase: 00
created: 2026-04-30
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Explorer Performance Optimization Trigger

Task statement: Optimize the Vitruvius Explorer graph loading, query, indexing, and rendering workload while preserving the current Explorer UX/UI and learner-facing/source-rights boundaries.

## Scope

In scope:
- `api/index.ts` file-backed AEC-MEPFS Explorer graph route/search/detail/expand/path hot paths.
- `explorer/src/api/graphApi.ts` graph payload request profile.
- `explorer/src/components/graph/*` selection/highlight/neighborhood computation and performance tests.
- `explorer/src/graph-engine/*` if needed for frontend graph indexes/worker-safe query contracts.
- `.ai/10_state/baselines/`, `.ai/13_research/`, `.ai/02_audits/`, `.ai/03_plans/`, `.ai/05_logs/` phase evidence.

Out of scope:
- UX redesign, visual refresh, wholesale Explorer rewrite, default renderer migration.
- Neo4j/live graph promotion, KG rebuild/reload/reset, protected source ingestion, destructive graph operations.
- Rust UI implementation or Rust acceleration without post-optimization benchmark evidence.

Identity-locked file check: PASS. No identity-locked file edits are planned.

Risk class: L. Multi-file API/frontend/test optimization with source-rights safety constraints; no production/live graph mutation.

Preservation contracts:
- Existing Explorer layout, toolbar, search workflow, preview/inspector, rail, selection, highlighting, routing, Tailwind styling, Zustand state, React Query posture, and vis-network renderer remain intact.
- Learner-facing default graph remains clean: no raw/source/provenance/internal source rows as ordinary concept nodes.
