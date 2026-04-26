---
task: aec-mepfs-shadow-explorer-test-hygiene
phase: 05
created: 2026-04-26
author: CODEX
status: VALIDATED
supersedes: null
---

# Twelfth Shadow Slice: Explorer Test-Hygiene Cleanup

## Scope

Remove the pre-existing React `act(...)` warnings from the Explorer component
test path used by the AEC-MEPFS parity runner.

This is a test-only hygiene slice. It changes no runtime Explorer behavior and
does not alter API, KG, Neo4j, feature flags, or source-ingest behavior.

## Audit Finding

The eleventh shadow slice's generated parity report passed, but the
`componentInteraction.test.tsx` command captured React warnings from
`CopyValueButton` state updates after clipboard clicks. The warnings came from
the `NodeInspector exposes unpin and clear-isolation actions` test and made the
parity report noisier than necessary.

## Implementation Plan

1. Keep the existing `CopyValueButton` behavior unchanged.
2. Wrap the two asynchronous clipboard-click assertions in `act(...)` inside
   the existing component test.
3. Re-run the focused component test and regenerate API/Explorer parity
   evidence.

## Plan Critique

- [C001] Do not modify runtime copy-button behavior for a test-warning fix.
- [C002] Do not suppress warnings globally.
- [C003] Do not change AEC-MEPFS routes, graph state, Neo4j, KG rebuild paths,
  feature flags, or protected-content boundaries.

## Execution Checklist

- [x] Reproduce the warning in the focused component test.
- [x] Capture GitNexus impact for `CopyValueButton`.
- [x] Apply a test-only `act(...)` wrapper around clipboard click assertions.
- [x] Confirm the focused component test output is warning-free.
- [x] Generate a fresh parity report with 22/22 cases passing.
- [ ] Commit, refresh GitNexus, push, then select the next safe slice.

## Explicit Non-Goals

- No Neo4j writes.
- No KG rebuild.
- No protected content ingest.
- No feature flag cutover.
- No Explorer default graph adoption.
- No runtime copy-button behavior change.
