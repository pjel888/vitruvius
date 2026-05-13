# AEC Explorer Overlay UX Plan

Status: completed
Created: 2026-05-13T05:11:55Z

## Research Pack

- Governing state checked: `current-phase.md`, `milestone-tracker.md`, `master-roadmap.md`, and `EXECUTION_LOOP.md`.
- Code intelligence refreshed with `scripts/refresh_code_intelligence.sh`; GitNexus and code-review-graph completed, ChunkHound reported known generated-artifact embedding warnings but the wrapper succeeded.
- GitNexus query identified the relevant path:
  - `readAecRelationshipImprovementOverlay`
  - `relationshipOverlayEdgeFromRecord`
  - `ExplorerRail`
  - `BackbonePreviewPanel`
  - Explorer graph hydration and preview flows.
- Impact checks returned LOW risk for `BackbonePreviewPanel`, `readAecRelationshipImprovementOverlay`, and `buildAecMepfsExplorerGraph`.

## Audit

- The overlay artifacts are already pending-only and projected into Explorer through API graph overlay edges.
- The active graph is not mutated by the overlay display path.
- Current UX gap: aggregate overlay counts exist, but review states are not explicit enough and there are no quick filters for approved vs needs-evidence vs relationship vs node-consolidation overlays.
- Current inspector gap: overlay edges do not clearly display source run, rationale/evidence, provider/model metadata, or resolution decision metadata.
- Documentation gap: the user-facing use cases for impact visualization, version-control style review, and maintenance/material dependency review are not documented in a concise place.

## Implementation Plan

1. Enrich API overlay edge payloads with safe metadata already present in artifacts:
   - evidence/rationale
   - effective judge/verifier/adjudicator providers and models
   - run ID, resolution decision, admission status, steward action, and review status.
2. Extend Explorer edge types so TypeScript accepts the new safe metadata fields.
3. Add an overlay legend and quick filter controls in the backbone preview rail:
   - Approved overlay edges
   - Needs-evidence overlay edges
   - Relationship overlays
   - Node-consolidation overlays
   - All overlay edges
4. Wire quick filters through `ExplorerRail` to the existing edge-type filter state.
5. Improve `EdgeInspector` so pending overlay edges show:
   - pending-only/run metadata
   - decision state
   - confidence/similarity
   - rationale and evidence
   - provider/model route details
   - canonical survivor / suggested label for node consolidations.
6. Add docs:
   - campaign archive summary for completed runs and future continuation.
   - RA9266/version-control and materials-maintenance Explorer use cases.
7. Run focused tests and compile/type checks where available.
8. Review diff for safety: no active graph mutation, no apply enablement, no secrets/reasoning content.

## Plan Critique

- Risk: broad UI edits could disturb unrelated Explorer filters. Mitigation: reuse existing `visibleEdgeTypes` store and only add quick setters.
- Risk: API may expose too much raw model output. Mitigation: only expose already-summarized fields, not prompts, raw responses, embeddings, API keys, or reasoning content.
- Risk: docs could imply automatic active admission. Mitigation: explicitly state pending overlay visualization and steward-reviewed admission boundary.
- Risk: visual styling could become noisy. Mitigation: keep the rail compact and use familiar filter buttons.

## Execution Checklist

- [x] API overlay metadata enriched.
- [x] Explorer types updated.
- [x] Preview legend and quick filters implemented.
- [x] Edge inspector overlay details implemented.
- [x] Docs/campaign summary added.
- [x] Tests updated.
- [x] Focused tests run.
- [x] Diff reviewed for safety.
- [x] Validation report written.

## Completion Notes

- Explorer now exposes overlay legend counts and one-click edge-type filters for approved, needs-evidence, relationship-only, node-consolidation-only, and all overlay states.
- Overlay edge payloads now include compact rationale/evidence/provider metadata for inspector display.
- The edge inspector now shows pending-only state, run ID, decision/admission status, confidence/similarity, rationale, evidence, provider/model route, and node-consolidation survivor/label metadata when present.
- Campaign and use-case docs were added at `docs/knowledge-graph/aec-explorer-overlay-campaigns.md`.
- No active graph mutation, Neo4j/Postgres write path, or `--apply` path was changed.
