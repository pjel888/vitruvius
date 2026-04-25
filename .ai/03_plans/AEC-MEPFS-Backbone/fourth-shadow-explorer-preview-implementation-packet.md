---
task: aec-mepfs-explorer-preview
phase: 05
created: 2026-04-25
author: PLANNER
status: ACCEPTED
supersedes: null
---

# Fourth Shadow Slice: Non-Default Explorer Preview

## Scope

Implement a bounded, opt-in Explorer preview for the existing AEC-MEPFS Backbone shadow summary route, `GET /v2/backbone`.

## Research Baseline

- `.ai/01_roadmap/current-phase.md` states the first additive `/v2` read route is implemented and not authorized for primary graph cutover or Explorer adoption.
- `.ai/STRATEGIC_NEXT_MOVE.md` names the next bounded choice as either another `/v2` route or a non-default Explorer preview.
- The current chosen slice is the non-default Explorer preview.

## Audit Findings

- The current operational Explorer graph must remain the default because AEC-MEPFS is still shadow-only.
- The `/v2/backbone` response is intentionally compact and file-backed, making it suitable for preview consumption without exposing protected corpus content.
- The highest-risk failure mode is accidentally implying runtime cutover or replacing the current graph view.

## Implementation Plan

1. Inspect the existing Explorer layout, API client, and tests.
2. Run impact review on the exact frontend symbols before editing.
3. Add a typed API helper for `/v2/backbone`.
4. Add an explicit UI entry point that renders the shadow preview only after the user opens it.
5. Keep all graph loading and default perspective behavior unchanged.
6. Add focused tests for the client and/or UI behavior.
7. Run Explorer and API verification.
8. Write validation evidence and update state docs if status changes.

## Plan Critique

- [C001] A preview can still look like adoption if the UI labels are too strong. The copy must say shadow/read-only and keep runtime boundaries visible.
- [C002] Adding the preview directly into the graph canvas would risk default-behavior drift. Prefer a contained panel or rail affordance that does not alter the graph model.
- [C003] API response shape must remain governed by the backend contract. The frontend should type the consumed fields but not invent new implied semantics.

## Execution Checklist

- [x] Capture current working tree and GitNexus/code-impact evidence.
- [x] Inspect Explorer UI/API/test structure.
- [x] Implement the opt-in preview.
- [x] Add focused tests.
- [x] Run Explorer verification.
- [x] Run API route verification.
- [x] Write validation log.
- [ ] Commit, refresh GitNexus, and push.

## Explicit Non-Goals

- No Neo4j reset, load, dump, or write.
- No KG rebuild.
- No feature flag default change.
- No Explorer default graph replacement.
- No protected source content exposure.
