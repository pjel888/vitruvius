# Explorer Scaffold Anchor Visibility Validation — 2026-04-29

## Summary

Implemented a bounded Explorer-only visibility filter for generic AEC-MEPFS
`Concept Anchor` and `Rule Context` scaffold placeholders. The taxonomy fixture,
API, resolver runtime, Neo4j/KG state, and protected-source boundaries were not
changed.

## Repo State

- Branch: `main`
- Starting commit: `dfaa5fbc`
- Ending commit: captured by final Git commit for this validation slice.
- Packet: `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-29_explorer_scaffold_anchor_visibility_packet.md`
- Evidence report: `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260429T010251Z/scaffold-anchor-visibility-report.json`

## Files Inspected

- `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T174344Z/shadow-backbone-graph.json`
- `explorer/src/components/GraphScene.tsx`
- `explorer/src/components/ExplorerRail.tsx`
- `explorer/src/components/explorer-rail/FiltersPanel.tsx`
- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/stores/useSceneStore.ts`

## Files Changed

- `explorer/src/components/graph/scaffoldAnchors.ts`
- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/components/GraphScene.tsx`
- `explorer/src/components/ExplorerRail.tsx`
- `explorer/src/components/explorer-rail/FiltersPanel.tsx`
- `explorer/src/stores/useSceneStore.ts`
- `explorer/src/components/graph/VisNetworkHost.test.ts`
- `explorer/src/components/componentInteraction.test.tsx`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-29_explorer_scaffold_anchor_visibility_packet.md`
- `.ai/05_logs/2026-04-29_explorer_scaffold_anchor_visibility_validation.md`
- `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260429T010251Z/scaffold-anchor-visibility-report.json`

## Baseline Scaffold Counts

From the admitted AEC-MEPFS backbone fixture:

- Total nodes: 4605
- `Concept Anchor` scaffold placeholders: 590
- `Rule Context` scaffold placeholders: 1394
- Total hidden-by-default generic scaffold placeholders: 1984 (43.08%)

## Implementation Notes

- Generic scaffold detection is Explorer-only.
- The detection requires node type `concept` or `rule` plus a label ending in
  `Concept Anchor` or `Rule Context`.
- `.CON` path segments are not used as a blanket scaffold signal because they
  can represent real concepts such as `Concrete`, `Conveyance`, and
  `Connections`.
- The Filters tab now exposes `Show scaffold anchors` as an explicit reveal
  toggle.
- Minimap/overview snapshots honor the same visibility default.

## Verification Commands

- `bun --cwd explorer test src/components/graph/VisNetworkHost.test.ts src/components/componentInteraction.test.tsx`
  - Result: PASS, 55 tests, 236 assertions.
- `(cd explorer && bun test)`
  - Result: PASS, 81 tests, 375 assertions.
- `(cd explorer && bun run lint)`
  - Result: PASS.
- `(cd explorer && bun run build)`
  - Result: PASS; existing Vite chunk-size warning for `vis-network` remained informational.
- `git diff --check`
  - Result: PASS.
- Safety grep for live-runtime/protected/Neo4j/KG/resolver terms across changed Explorer files and this evidence packet
  - Result: PASS for implementation behavior; hits are limited to existing type/test boundary labels and explicit blocked-scope evidence language.

## Safety Invariants

- API changed: no.
- Taxonomy fixture changed: no.
- `/v2/resolve*` changed: no.
- Neo4j mutation: no.
- KG rebuild/reload/reset: no.
- Protected content ingest/exposure: no.
- Explorer layout default changed: no.

## Residual Risks

- Manual browser visual confirmation was not performed in this slice; automated
  Explorer component/unit tests, lint, and build cover the functional wiring.
