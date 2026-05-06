# Phase 7 Dynamic Edge Filter Guard Report

**Date:** 2026-05-06
**Unit:** Explorer dynamic relationship filter regression guard
**Status:** validated, commit pending

## Scope

This unit adds regression coverage for Explorer edge-filter visibility so graph-derived relationship types beyond the static edge list remain visible and toggleable in the filter panel.

Changed files:

- `explorer/src/components/ExplorerRail.tsx`
- `explorer/src/components/componentInteraction.test.tsx`

## Implementation Summary

`ExplorerRail` now exposes `buildScopedEdgeTypes(edgeTypeCounts)` as a pure helper. The helper preserves the existing behavior:

- static `EDGE_TYPES` remain the base list.
- edge types present in the loaded graph but absent from `EDGE_TYPES` are appended dynamically.
- dynamic edge types are sorted by key and receive formatted labels.
- each option carries `count` and `available` fields from the current graph edge counts.

The runtime `useMemo` path now delegates to that helper without changing filter behavior.

## Regression Coverage

The new component interaction test proves:

- a graph-derived `HAS_FACET` edge type is included even though it is absent from the static edge list.
- the dynamic option has the expected key, label, count, and availability fields.
- the existing `FiltersPanel` renders the dynamic option.
- toggling the dynamic option emits `HAS_FACET` through `onToggleEdgeType`.

This protects direct relationship visibility cases such as Sendai Mediatheque / Toyo Ito `HAS_FACET` from stale static filter-list regressions.

## Safety Boundary

- No graph/canonical registry mutation.
- No Resource Layer registry mutation.
- No Resource creation.
- No nodeResourceLink creation.
- No candidate promotion or candidate status mutation.
- No learner exposure change.
- No source verification.

## Validation

- `bun test src/components/componentInteraction.test.tsx -t "graph-derived relationship"`: PASS, 1 pass.
- `bun run api/validateResourceLayer.ts -- --no-write`: PASS, resources 7, nodeResourceLinks 9, external metadata candidates 2.
- `bun run api/validateGraphRelationships.ts -- --no-write`: PASS, admitted 264, base edges 13,670, effective edges 13,934.
- `bun run api/validateCanonicalGraphStewardship.ts -- --no-write`: PASS, CROSS_DOMAIN_ALIGNMENT 22, blockers [].
- `cd explorer && bun test`: PASS, 121 pass.
- `cd explorer && bun run build`: PASS with existing Vite chunk-size warning.

## Delegated Review

Kimi 1.41.0 reviewed the scoped diff as a project-owner-delegated external AI reviewer and returned `PASS_DYNAMIC_EDGE_FILTER_GUARD`.

This is delegated external AI review, not biological human review, not source truth, and not production approval by itself.
