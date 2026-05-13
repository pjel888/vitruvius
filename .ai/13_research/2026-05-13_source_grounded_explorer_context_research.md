# Source-Grounded Explorer Context Research Pack

Date: 2026-05-13

## Question

What is the smallest safe next step that uses the AEC relationship and node-consolidation campaign outputs without admitting them into the active graph, while moving the product closer to source-grounded KG answers in Explorer?

## Local Evidence

- `.ai/ACTIVE_WORK.md` identifies the current path as source-grounded KG AI and lists the first concrete work as a no-write source/resource coverage inventory plus a `SourceGroundedAnswerContext` contract.
- `.ai/STRATEGIC_NEXT_MOVE.md` states the same next move: build a no-write coverage inventory and answer-context contract before answer composition, cloud answering, DB projection, or Rust acceleration.
- `.ai/14_project_management/source_grounded_kg_ai_goal_tracker.md` marks coverage inventory and answer-context contract as not started.
- `.ai/03_plans/2026-05-03_source_grounded_kg_ai_execution_acceleration_plan.md` calls for:
  - Phase 0: source/resource coverage inventory.
  - Phase 1: `SourceGroundedAnswerContext`.
  - Phase 3: read-only `/v2/answer/context` endpoint.
  - Phase 4: Explorer answer panel.
- `api/resourceLayer/registry.ts` already exposes read-only resource-layer data and node-resource rankings.
- `api/index.ts` already exposes AEC-MEPFS backbone graph, improvement overlay, and node detail endpoints.
- `explorer/src/components/inspector/NodeInspector.tsx` already has source/resource and relationship tabs suitable for adding a compact source-grounded context panel.

## Tooling Notes

- `bash ./scripts/refresh_code_intelligence.sh` completed GitNexus and ChunkHound refresh and rebuilt code-review-graph.
- code-review-graph reported missing `tree-sitter-yaml` parser warnings for YAML files.
- code-review-graph embedding refresh reported oversized chunk errors from large campaign logs. The structural graph still rebuilt.
- A prior local semantic search backend returned 429, so implementation uses refreshed local indexes plus targeted file reads.

## Constraints

- Do not mutate active graph files.
- Do not write Neo4j or Postgres.
- Do not auto-admit pending relationship or node-consolidation overlays.
- Do not expose protected source content, API keys, or `reasoning_content`.
- Preserve pending-only relationship-improvement safety behavior.
