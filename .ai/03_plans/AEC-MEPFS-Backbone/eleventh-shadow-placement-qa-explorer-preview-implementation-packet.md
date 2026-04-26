---
task: aec-mepfs-shadow-placement-qa-explorer-preview
phase: 05
created: 2026-04-26
author: CODEX
status: VALIDATED
supersedes: null
---

# Eleventh Shadow Slice: Explorer Placement QA Preview

## Scope

Add an opt-in Explorer rail section for the existing read-only placement QA
summary route:

`GET /v2/backbone/placement-qa`

The UI shows compact placement readiness counts, required coverage, review
queues, warnings, and safety boundaries only after the user explicitly loads
the placement QA summary from the existing AEC-MEPFS preview panel.

## Research Baseline

- The tenth shadow slice exposed the file-backed placement QA report as a
  compact `/v2/backbone/placement-qa` route.
- `ACTIVE_WORK.md` and `STRATEGIC_NEXT_MOVE.md` identified an opt-in Explorer
  placement QA preview section as the next safe shadow slice.
- The existing Explorer pattern already separates summary loading from deeper
  taxonomy readiness loading, so placement QA can use the same explicit-action
  preview model.

## Audit Findings

- Placement QA evidence was available through API and parity artifacts, but not
  inspectable in the Explorer preview.
- The Explorer integration had to remain explicit-action only. It must not
  fetch placement QA on page load, on preview-open summary load, or through
  default graph adoption.
- Refreshing the AEC-MEPFS summary must reset deeper taxonomy and placement QA
  preview details so stale shadow evidence cannot persist after a new summary
  load.

## Implementation Plan

1. Add an additive `BackbonePlacementQaPreview` type and
   `getBackbonePlacementQaPreview()` API client helper.
2. Add placement QA state, request-id guarding, reset-on-summary-refresh, and an
   explicit loader in `ExplorerRail.tsx`.
3. Add a compact placement QA subsection and icon control in
   `BackbonePreviewPanel.tsx`.
4. Extend component and ExploreView integration tests to prove opt-in loading,
   preview rendering, reset behavior, and unchanged graph state.
5. Add a parity case/category for Explorer placement QA opt-in isolation and
   regenerate the parity report.

## Plan Critique

- [C001] Do not fetch placement QA as part of the default graph or the initial
  preview summary load.
- [C002] Do not render `case_results`, expected outputs, protected content, or
  source payloads.
- [C003] Do not change v1 API behavior, graph store semantics, perspectives, or
  Explorer default adoption.
- [C004] Keep this as a UI preview over an already file-backed API route, not a
  placement engine or KG runtime invocation.

## Execution Checklist

- [x] Inspect current Explorer preview patterns and parity conventions.
- [x] Capture GitNexus impact for touched Explorer/parity surfaces.
- [x] Implement the API client, preview state, panel rendering, and tests.
- [x] Add `shadow_placement_qa_preview_opt_in_isolation` to parity coverage.
- [x] Generate fresh parity report with 22/22 cases passing.
- [x] Attempt Gemini/Kimi advisory review and record availability.
- [x] Run focused and broad Explorer/API/Python verification.
- [ ] Commit, refresh GitNexus, push, then select the next safe slice.

## Explicit Non-Goals

- No Neo4j writes.
- No KG rebuild.
- No protected content ingest.
- No feature flag cutover.
- No Explorer default graph adoption.
- No runtime `PlacementEngine` execution.
- No canonical source/content admission.
