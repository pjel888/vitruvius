---
task: explorer-graph-controls-and-rule-labels
phase: 05
created: 2026-04-25
author: PLANNER
status: ACCEPTED
---

# Explorer Graph Controls and Rule Labels Plan

## Decision

Implement a bounded Explorer presentation/control patch. Keep source-faithful KG labels intact, but compact Explorer-facing rule titles and add explicit graph-state escape controls.

Do not add a new node-schema property for this slice. The existing split already models the need:

- `label`: canonical/source-faithful text for audit, evidence, and detail views
- `display_label`: short human title for Explorer graph/search/sidebar presentation

A third field such as `graph_label` should be deferred unless future UX proves that graph labels, search labels, and inspector titles need independently governed text. For now, adding another property would broaden the schema and increase drift while duplicating `display_label`.

## Execution Checklist

- [x] Add deterministic rule display-label compaction in `api/index.ts` and `scripts/vitruvius/kg/rule_extractor.py`, preserving a short section discriminator when available.
- [x] Add a graph motion pause/resume controller path in `VisNetworkHost.tsx` and expose it in `GraphScene.tsx`.
- [x] Make right-sidebar pinning visibly toggle between pin and unpin states.
- [x] Let the right-sidebar isolation button clear isolation when a subgraph is already focused.
- [x] Widen `InspectorRail.tsx` and reduce/no-wrap node inspector tab typography.
- [x] Align `CommandBar.tsx` inspector header width with the right rail and keep the minimize/maximize button anchored while flipping only the icon state.
- [x] Return plain-text node tooltips without HTML break tags.
- [x] Add or update focused API, Explorer component, and graph host tests.
- [x] Run targeted Bun tests and Explorer build.
- [ ] Capture visual QA evidence if a browser run is available.

## Plan Critique

- Do not solve long rule labels by mutating canonical `label`; that would erase source-faithful evidence.
- Do not add a new dependency for title compaction or tooltip rendering.
- Do not hide isolation state only in the graph controller; the sidebar needs visible state through the store.
- Do not rely solely on future KG generation changes, because the current Neo4j graph is already loaded.

## Acceptance Criteria

- Example-style rule labels render as compact but distinguishable titles such as `Socialized Housing Projects Rule · Sec. 50`, not with long article/source suffixes.
- Broad duplicates such as `Zoning Ordinance Rule` should be reduced by short section discriminators when the source graph provides section metadata.
- A user can pause/resume graph motion from the graph controls.
- A pinned node shows an unpin affordance in the inspector.
- A one-hop isolation view can be cleared from the inspector.
- Inspector tabs stay single-line at the right rail width.
- The inspector header boundary aligns with the right rail boundary, and the minimize/maximize button does not shift when toggled.
- Tooltips contain no literal `<br>`/HTML tag fragments.
