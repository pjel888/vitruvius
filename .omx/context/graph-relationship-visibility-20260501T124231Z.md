# Graph Relationship Visibility Context Snapshot

Date: 2026-05-01 20:42:31 +08:00

## Task statement
Implement the next Vitruvius loop: fix graph relationship visibility, hydration, traversal, and canonical node identity so selected KG nodes show actual direct interrelationships in the graph UI, while preserving Resource Layer loop 1/2 behavior.

## Desired outcome
- Selected node direct neighborhood can show all direct incoming/outgoing ontology relationships or clearly report hidden/filter reasons.
- Relationship list and canvas agree from a shared normalized source.
- Semantic/cross-links are not silently omitted.
- Missing edge endpoint nodes hydrate into the visible graph.
- Duplicate/canonical label issues are detected and reported, with safe merge avoided unless proven.
- Resource Layer routes/UI/tests remain green.

## Known facts/evidence
- Team mode requested but tmux is unavailable on this Windows shell; use native subagents and record blocker.
- docs/shared/agent-tiers.md is missing.
- Code intelligence refresh ran before editing; GitNexus/ChunkHound/code-review-graph wrapper completed with YAML parser warnings.
- Resource Layer loop 2 has file-backed review workflow, /dev/resource-review, validation/tests passing per previous report.
- Current git tree is dirty with many pre-existing modified/untracked files.

## Constraints
- No fake nodes/edges/resources.
- No broad backfill.
- No reckless duplicate merges.
- Preserve Resource Layer routes and review UI.
- Use Kimi for diagnosis, implementation, and final review.
- Add tests and validation.

## Unknowns/open questions
- Actual edge storage and API/frontend divergence root cause.
- Whether Sendai Mediatheque/Toyo Ito exists in the active shadow-staging graph.
- Whether graph canvas currently has expansion/hydration controls.
- Exact duplicate/canonical fragmentation patterns.

## Likely codebase touchpoints
- api/index.ts
- api graph data builders around AEC-MEPFS shadow-staging
- explorer/src/api/graphApi.ts
- explorer/src/App.tsx
- explorer graph components/search/inspector/sidebar
- scripts/vitruvius/kg graph quality/backbone files
- 006_System-Manifests/aec-mepfs-backbone/shadow-staging
- .ai reports/logs/decisions
