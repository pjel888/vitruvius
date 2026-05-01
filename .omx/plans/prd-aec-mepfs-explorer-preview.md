---
task: aec-mepfs-explorer-preview
phase: prd
created: 2026-04-25
author: PLANNER
status: ACCEPTED
---

# PRD: AEC-MEPFS Explorer Preview

## Objective

Add an opt-in Explorer preview for the AEC-MEPFS Backbone shadow summary exposed by `GET /v2/backbone`, without changing the current Explorer graph default.

## User Need

The user needs a visible, inspectable preview of the standards-first AEC-MEPFS readiness artifact from inside Explorer while the existing KG remains the operational MVP graph.

## In Scope

- Add a frontend API client for `/v2/backbone`.
- Add an explicit, non-default UI control or panel in Explorer for the preview.
- Render compact readiness data: status/schema, predicate/source counts, no-ingest posture, and blocked runtime boundaries.
- Add error and loading states.
- Add focused tests covering the API-client or component behavior.

## Out of Scope

- Neo4j writes, graph rebuilds, graph resets, or KG reloads.
- Replacing the current graph with AEC-MEPFS Backbone data.
- Making AEC-MEPFS the Explorer default view.
- Exposing protected source content or raw registry details.
- Adding new dependencies or feature flags.

## Acceptance Criteria

- Explorer still opens into the existing graph experience by default.
- The AEC-MEPFS preview is reachable only through an explicit user action.
- The preview fetches `/v2/backbone` and handles success, loading, and failure states.
- Tests prove the new behavior without weakening existing graph tests.
- Documentation/state reflects that this is a shadow consumer slice, not runtime adoption.
