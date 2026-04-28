# Explorer UI/UX and Performance Audit for Dense AEC-MEPFS Graph

```yaml
status: AUDIT_READY
created: 2026-04-28
branch: main
start_commit: 11f92fa5
latest_aec_graph_run: 20260428T063500Z
latest_aec_graph_nodes: 2424
latest_aec_graph_edges: 2400
```

## 1. Audit scope

This audit reviews Explorer as a dense graph product surface after the AEC-MEPFS
backbone expansion to 2,424 nodes and 2,400 edges. It focuses on UI/UX readiness,
layout controls, graph spacing, zooming, physics behavior, minimap behavior,
large-graph rendering guardrails, and preparation for future document/evidence
relationships.

This audit is planning/readiness only. It does not change API, Explorer runtime,
Neo4j, KG rebuild, protected content, or taxonomy data.

## 2. Current Explorer surfaces inspected

- `explorer/src/components/GraphScene.tsx`
- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/components/graph/largeGraphPerformance.ts`
- `explorer/src/components/graph/layoutSpread.ts`
- `explorer/src/components/graph/Minimap.tsx`
- `explorer/src/components/graph/nodeLabelVisibility.ts`
- `explorer/src/components/componentInteraction.test.tsx`
- `explorer/src/components/graph/VisNetworkHost.test.ts`
- `explorer/src/stores/useSceneStore.ts`
- `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260428T063500Z/explorer-taxonomy-l4-expansion-report.json`

## 3. What is already strong

1. **AEC-MEPFS default graph is real and sizable.** The current evidence run has
   2,424 nodes and 2,400 edges, so the UI is now testing real density rather than
   a toy preview.
2. **Large-graph guardrails exist.** `largeGraphPerformance.ts` centralizes
   thresholds, bounded ForceAtlas2 options, hover-highlight skipping, and physics
   auto-freeze behavior.
3. **Graph remains visible during drag.** The current guardrail preserves edges
   during drag, addressing the earlier disappearing graph symptom.
4. **Manual motion control exists.** `GraphScene` has a pause/resume motion button
   wired to `VisNetworkHost.setMotionPaused`.
5. **Spread control exists.** `GraphScene` exposes a `0.75×` to `2.5×` spread
   slider, backed by `layoutSpread.ts` helpers.
6. **Minimap exists.** The minimap consumes controller overview snapshots and
   supports viewport display plus click/drag centering.
7. **Node label controls exist.** The filter UI can hide node text labels by node
   type without hiding the nodes themselves.
8. **Panel usability has improved.** Left/right panels are resizable, and the
   taxonomy tree supports expand/collapse controls.

## 4. Gaps and risks

### Finding A — Zoom is not yet a first-class continuous control

Explorer has zoom-in, zoom-out, and fit buttons, and `VisNetworkHost` clamps zoom
internally. It does not yet expose a continuous zoom slider or a synchronized zoom
readout. This creates a mismatch between user expectations for a map-like graph
and the current button-only camera controls.

**Risk:** Users cannot easily make fine-grained zoom adjustments or understand the
current zoom level.

**Recommended priority:** P0 quick win.

### Finding B — Current spread bounds are too conservative for 2.4k nodes

`layoutSpread.ts` uses:

- min: `0.75×`
- max: `2.5×`
- default: `1.45×`

Those values were reasonable for smaller graphs, but the current AEC-MEPFS graph
is 2,424 nodes. User feedback confirms the graph still feels cramped.

**Risk:** Users perceive density as chaos even when the taxonomy structure is now
comprehensive.

**Recommended priority:** P0 quick win.

### Finding C — Spread changes do not automatically pause physics

Changing spread calls `setLayoutSpread`, which reapplies layout. Motion pause is a
separate UI control. On dense graphs, live physics plus spread changes can feel
janky because the user changes a deterministic spacing control while the force
simulation continues moving nodes.

**Risk:** The graph appears unstable or sluggish while the user tunes spacing.

**Recommended priority:** P0 quick win.

### Finding D — Store accepts raw spread values

`useSceneStore.setLayoutSpread` currently stores whatever numeric value it
receives. Layout helper functions clamp the value later, but the store and UI can
hold out-of-range values if future callers bypass the input element.

**Risk:** Hidden state inconsistency and harder testability.

**Recommended priority:** P1.

### Finding E — Large-graph thresholds are static

Current thresholds classify graphs above 80 elements as large and 300 elements as
expensive-hover/auto-freeze territory. That is useful, but the app has no adaptive
FPS budget or browser-profile evidence yet.

**Risk:** The app may regress as the graph moves from 2.4k to 5k+ elements and
when document interrelationships are added.

**Recommended priority:** P1/P2.

### Finding F — Minimap correctness needs more interaction coverage

The minimap exists and has snapshot-driven redraw behavior, but future work should
add direct tests for filter updates, viewport update timing, click/drag pan, and
keyboard fit behavior.

**Risk:** Minimap can drift from the visible graph during aggressive filtering,
layout, or zoom changes.

**Recommended priority:** P0/P1 because minimap is the recovery surface for dense graphs.

### Finding G — Future document edges need relationship-density controls

The current graph is mostly taxonomy hierarchy plus L4 concept/rule anchors. Once
actual document relationships, evidence links, legal references, source links, and
formula dependencies are added, edge density will become the dominant visual cost.

**Risk:** Spreading nodes farther apart will not be enough; without edge presets,
semantic zoom, and focus modes, the graph will become unreadable.

**Recommended priority:** P2 before document interrelationship default-on.


### Finding H — Edge strokes and labels need visual hierarchy rules

Current user feedback says edge lines read too thick and labels can compete with
or overpower node bodies. For a 2.4k-node graph, visual hierarchy matters: normal
edges should be thin lines, selected/path edges can be emphasized, and node text
should remain smaller than the node glyph.

**Risk:** Thick edge strokes and oversized labels make the graph feel cramped even
when node spacing improves.

**Recommended priority:** P0 quick win.

### Finding I — Selection should create a one-hop focus lens

Dense graph exploration needs a click interaction where the selected node and its
direct neighbors remain at full opacity with labels, while unrelated graph
context remains visible but de-emphasized. The requested target is approximately
`100%` opacity for selected plus connected nodes and `50%` opacity with no labels
for the rest.

**Risk:** Without a focus lens, users must mentally parse thousands of nodes and
edges even after selecting a point of interest.

**Recommended priority:** P0/P1.

## 5. Readiness verdict

Explorer is **MVP-promising but not yet dense-graph-ready** for the next wave of
document interrelationships. The current graph is usable enough to continue, but
it needs a deliberate optimization slice before the next major content/edge wave.

Recommended next implementation slice:

1. zoom slider + zoom readout;
2. wider spread range and more spacious default;
3. auto-pause physics on spread adjustment;
4. clamp spread in store/controller;
5. tests for zoom, spread pause, minimap filter update, thin edge strokes, label scale, selected-neighborhood emphasis, and layout spread bounds;
6. evidence report for the 2.4k-node baseline.

## 6. Explicit answer to spacing question

Yes: more spacing between nodes is better for this stage. But the product should
not only make everything bigger. The right MVP behavior is:

- default to a more comfortable/spacious layout for AEC-MEPFS;
- give users a Density/Spread control with presets;
- pause physics during manual spacing adjustments;
- use semantic zoom, selected-neighborhood emphasis, and label levels so far-zoom views stay clean;
- keep normal edge lines thin and keep text visually smaller than node bodies;
- add relationship filters before document/evidence edges are default-visible.
