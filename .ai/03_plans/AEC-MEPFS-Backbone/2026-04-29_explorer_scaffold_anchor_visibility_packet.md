---
task: aec-mepfs-explorer-scaffold-anchor-visibility
phase: aec-mepfs-file-backed-explorer-ux
status: BOUNDARY_APPROVED
authority: project-owner-directed-explorer-ux-noise-reduction
created: 2026-04-29
---

# Explorer Scaffold Anchor Visibility Packet

## Purpose

The project owner reported duplicate-looking AEC-MEPFS Explorer nodes such as
`Signing And Sealing Concept Anchor` and `Signing And Sealing Rule Context`.
This packet authorizes a bounded Explorer-only visibility improvement that hides
these generic scaffold placeholders by default while preserving a visible filter
escape hatch.

## Baseline Evidence

- Starting commit: `dfaa5fbc`.
- Source fixture: `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`.
- Source graph: `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T174344Z/shadow-backbone-graph.json`.
- Baseline graph size: 4605 nodes.
- Generic scaffold labels found:
  - `Concept Anchor`: 590 nodes.
  - `Rule Context`: 1394 nodes.
  - Total hidden-by-default scaffold placeholders: 1984 nodes (43.08%).

## Allowed Scope

- Add Explorer-only classification for generic scaffold placeholders.
- Hide `concept` or `rule` nodes whose displayed label ends with
  `Concept Anchor` or `Rule Context` by default.
- Add a Filters-tab toggle named `Show scaffold anchors` to reveal them.
- Apply the same default filtering to the minimap/overview snapshot.
- Add focused tests proving real concept nodes such as `Concrete` are not hidden
  merely because a path segment ends in `.CON`.
- Produce validation and evidence artifacts.

## Blocked Scope

- No taxonomy fixture mutation.
- No API behavior change.
- No `/v2/resolve*` behavior change.
- No Neo4j writes, KG rebuild/reload/reset, or graph promotion.
- No protected source ingest or protected payload exposure.
- No Explorer default-layout change.
- No production/runtime threshold claim.

## Implementation Plan

1. Add a small Explorer helper that detects generic scaffold anchors by node type
   plus label suffix, not by `.CON` path code alone.
2. Thread a `showScaffoldAnchors` UI/store flag through Explorer filters.
3. Default the flag to `false` and reset loaded scenes to the default.
4. Filter generic scaffold anchors from graph rendering and overview snapshots
   unless the flag is enabled.
5. Add component/store/helper tests.
6. Run focused Explorer tests, full Explorer tests, lint, build, and diff checks.

## Completion Criteria

- Duplicate-looking generic scaffold nodes are hidden by default.
- A user can restore them from the Filters tab.
- Real concepts/rules remain governed by the existing node-type filters.
- Explorer tests/lint/build pass.
- Evidence report and validation log are written.
