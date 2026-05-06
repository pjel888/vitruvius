# Phase 7 NodeInspector Learner Resource Visibility Report

**Date:** 2026-05-06
**Unit:** Explorer NodeInspector learner resource visibility defense-in-depth
**Status:** validated, commit pending

## Scope

This unit tightens the learner-facing `NodeInspector` Sources tab so Resource reference cards are rendered only for links whose review status is `accepted` or `human_reviewed`.

Changed files:

- `explorer/src/components/inspector/NodeInspector.tsx`
- `explorer/src/components/componentInteraction.test.tsx`

## Safety Boundary

- No Resource creation.
- No nodeResourceLink creation.
- No candidate promotion.
- No candidate status mutation.
- No source verification.
- No learner exposure of reviewer-only candidates.
- No graph/canonical/P0/high-risk P1 mutation.
- No production Resource Layer registry mutation.

## Implementation Summary

`NodeInspector` now derives `learnerVisibleResources` from `detail.resources` using a conservative allowlist:

- `accepted`
- `human_reviewed`

The learner-visible list is used for:

- Sources tab count.
- Resources / References count.
- resource-card rendering.
- resource empty-state messages.
- combined source-material empty state.

The component still receives the full API payload, but reviewer-only, candidate, unverified, or needs-review records are not passed to `ResourceCard`.

## Test Coverage

`explorer/src/components/componentInteraction.test.tsx` now includes a second resource fixture with:

- `reviewStatus: "candidate"`
- `verificationStatus: "unverified"`
- `resourceType: "standard_candidate"`

The test proves the accepted resource still renders and the candidate resource title/status labels are absent from the learner Sources tab.

## Validation

- `bun test src/components/componentInteraction.test.tsx -t "verified resource"`: PASS, 1 pass.
- `bun run api/validateResourceLayer.ts -- --no-write`: PASS, resources 7, nodeResourceLinks 9, external metadata candidates 2.
- `bun run api/validateGraphRelationships.ts -- --no-write`: PASS, admitted 264, base edges 13,670, effective edges 13,934.
- `bun run api/validateCanonicalGraphStewardship.ts -- --no-write`: PASS, CROSS_DOMAIN_ALIGNMENT 22, blockers [].
- `cd explorer && bun test`: PASS, 120 pass.
- `cd explorer && bun run build`: PASS with existing Vite chunk-size warning.

## Delegated Review

Kimi 1.41.0 reviewed the scoped diff as a project-owner-delegated external AI reviewer and returned `PASS_LEARNER_VISIBILITY_GUARD`.

This is delegated external AI review, not biological human review, not source truth, and not production approval by itself.

## Current State

- Resources remain 7.
- nodeResourceLinks remain 9.
- External metadata candidates remain 2.
- ASCE 7 remains reviewer-only and not learner-visible.
- Earth Retaining Structures remains reviewer-only and not learner-visible.
- No production Resource Layer, graph, canonical, P0, or high-risk P1 mutation occurred.
