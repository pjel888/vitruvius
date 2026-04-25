---
task: explorer-graph-controls-and-rule-labels
phase: 04
created: 2026-04-25
author: PLANNER
status: ACCEPTED
---

# Explorer Graph Controls and Rule Labels Audit

## Request

Improve the Explorer graph UX after the laws-only KG rebuild:

- add a graph motion stop/resume option
- make Explorer-facing rule names shorter
- allow unpinning from the right sidebar
- allow clearing a one-hop isolation view
- widen the right sidebar and keep tab buttons on one line
- remove visible HTML fragments such as `<br>` from node tooltips

## Current Evidence

- The active milestone is KG relationship quality and graph UX maintenance, with the `001-Laws` Explorer graph refresh already completed.
- `explorer/src/components/graph/VisNetworkHost.tsx` owns vis-network physics, graph isolation, tooltip text, and rule-label derivation.
- `explorer/src/components/GraphScene.tsx` owns the graph control cluster and controller wiring.
- `explorer/src/components/inspector/NodeInspector.tsx` owns the right-sidebar pin button, isolation button, and tab labels.
- `explorer/src/components/InspectorRail.tsx` fixes the right rail width at `w-96`.
- `explorer/src/components/CommandBar.tsx` owns the top-right inspector summary and minimize/maximize toggle; it used a different open width from the rail after the rail width change.
- `api/index.ts` normalizes Neo4j nodes and currently trusts stored rule `display_label` values without compacting them.
- `scripts/vitruvius/kg/rule_extractor.py` generates future rule `display_label` values and can compose long labels with section/source suffixes.

## Findings

- Rule canonical `label` and Explorer-facing `display_label` are already separated. The fix should preserve source-faithful labels and compact only `display_label` or UI presentation.
- Current graph physics can be disabled by non-force layouts, but there is no user-visible freeze/resume control for the force-directed layout.
- The pin button already toggles pinned state, but the tooltip and aria label always say "Pin", making the unpin behavior invisible.
- `focusSubgraph` hides unrelated nodes, and `showAll` exists in the graph controller, but the right sidebar does not expose a clear-isolation action.
- Sidebar tabs include labels plus counts in four equal columns. At the current rail width and font size, "Relationships (N)" can wrap.
- The header inspector toggle changes between different button layouts in open vs closed states, which can make the control appear to shift instead of staying anchored at the right edge.
- `buildNodeTooltip` currently joins HTML fragments with `<br/>`, which can surface as visible literal text in native/tool-specific tooltip rendering.

## Blast Radius

- Frontend behavior: graph controls, inspector rail, graph tooltip text, and node display labels.
- API behavior: rule display-label normalization for current Neo4j data.
- KG generation behavior: future rule `display_label` compactness only; canonical source labels and summaries are out of scope.

## Out Of Scope

- Rebuilding or reloading the KG.
- Changing canonical `label`, source evidence text, or relationship assertions.
- Cross-subject enrichment.
