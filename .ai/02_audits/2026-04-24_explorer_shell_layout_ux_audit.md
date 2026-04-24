# Explorer Shell Layout UX Audit

**Date:** 2026-04-24
**Scope:** Explorer application shell, command surfaces, sidebars, drawers, and layout chrome. Knowledge graph rendering quality is intentionally out of scope.

## Research Inputs

- Carbon spacing guidance: use a tokenized spacing scale for component internals and layout spacing; dense sections are acceptable, but the whole page must still leave visual rest.
- Atlassian spacing guidance: use small spacing values for compact controls, medium values for component groups, and proximity to communicate semantic relationships.
- Fluent layout guidance: spacing creates relationships and hierarchy; a 4px base ramp supports dense product UI while preserving consistency.
- Material layout guidance: structural grids, baseline rhythm, and repeated spacing patterns create scalable hierarchy and focus.

## Audit Findings

1. **Inspector toggle behavior is brittle.**
   - `InspectorRail` auto-opens whenever a selected node or edge exists.
   - This means a user-triggered minimize can be immediately reversed while selection remains active.
   - UX impact: the minimize/maximize control appears broken even when the button fires.

2. **Inspector status cell currently over-stacks related controls.**
   - The API status pill sits below the minimize icon.
   - The pill/icon relationship is too tight vertically and does not read as a single command/status group.
   - UX impact: the user sees an awkward column rather than a stable right-rail control cluster.

3. **Header regions are now conceptually correct but need spacing discipline.**
   - Navigator identity, graph controls, and inspector controls are correctly split.
   - The inspector column still needs a clearer internal grid: summary on the left, status/toggle on the right.
   - UX impact: the right header reads as a loose card instead of a rail-aligned utility area.

4. **Graph-canvas chrome is cleaner after removing the floating scene card.**
   - Scene summary no longer floats over the canvas.
   - Remaining non-graph overlays are layout/query and legend/minimap, which are graph-local and out of this shell audit.

## Design Direction

- Use a 4px/8px spacing rhythm: 4px for micro relationships, 8px for tight compact groups, 12px-16px for control clusters, and 24px+ only for region separation.
- Treat the inspector as a persistent right-side region. Its header cell and body rail must share open and collapsed widths.
- Keep status and control affordances horizontally grouped when they represent one sidebar state area.
- Let user intent override automatic behavior: closing the inspector should remain closed until a new selection is made.

## Acceptance Criteria

- Inspector minimize works even when a node or edge remains selected.
- Selecting a different node or edge still reopens the inspector.
- Neo4j/API status pill is horizontally separated from the minimize icon and no longer sits underneath it.
- Header spacing follows the documented region grid.
- Targeted Explorer interaction tests cover the inspector toggle behavior.
