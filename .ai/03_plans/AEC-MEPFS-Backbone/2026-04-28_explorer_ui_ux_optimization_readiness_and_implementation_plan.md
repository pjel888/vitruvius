# Explorer UI/UX Optimization Readiness and Implementation Plan

```yaml
status: PLAN_READY
created: 2026-04-28
branch: main
start_commit: 11f92fa5
owner_intent: make Explorer feel expansive, controllable, and MVP-ready for dense AEC-MEPFS graph exploration
scope: Explorer UI/UX planning for zoom, spread, physics, density, minimap, labels, and future document relationships
implementation_authority: planning_only_in_this_packet
```

## 1. Purpose

The AEC-MEPFS taxonomy is now large enough that Explorer must behave less like a
static graph demo and more like a map-grade knowledge interface. The immediate
user experience issue is density: nodes feel cramped, camera control is limited,
and manual spread adjustments should not fight live physics. The next product
risk is future document/evidence interrelationships, which will add many more
edges and require stronger density controls.

This plan defines the staged implementation path. It does not itself modify code.

## 2. Current baseline

Validated graph evidence:

- latest run: `20260428T063500Z`
- nodes: `2424`
- edges: `2400`
- roots: `24`
- L2 topics: `240`
- L3 subtopics: `720`
- L4 concept/rule anchors: `1440`
- max depth: `4`

Current Explorer capabilities:

- AEC-MEPFS-first Explorer behavior exists.
- Zoom buttons and fit button exist.
- Spread slider exists with `0.75×` to `2.5×`, default `1.45×`.
- Physics pause/resume button exists.
- Large-graph ForceAtlas2 guardrails exist.
- Physics auto-freezes after large-graph stabilization.
- Minimap exists.
- Node text label filters exist.
- Left/right panels are resizable.
- Taxonomy tree expand/collapse exists.

## 3. Design principles

1. **Map-like control.** Explorer should feel like navigating a living map: zoom,
   pan, minimap, fit, density, and focus should be obvious.
2. **Overview first.** Keep the whole graph visible, then let users zoom/filter
   into detail.
3. **Details on demand.** Labels, edge details, document relationships, and
   evidence text should appear progressively, not all at once.
4. **Physics as setup, not constant motion.** Physics should help settle the
   layout and then stop unless the user explicitly resumes it.
5. **User-controlled density.** Dense, Comfortable, and Spacious modes are better
   than a single hard-coded spacing value.
6. **Future edge discipline.** Document/evidence relationships need edge filters
   and focus modes before they become visually dominant.

## 4. Phase 1 — Immediate graph control improvements

### 4.1 Add zoom slider and zoom readout

**Implementation shape**

- Extend `GraphController` with `getZoomScale` or viewport snapshot scale if not
  already available.
- Add a slider to `GraphScene`, likely near zoom buttons or spread controls.
- Synchronize slider with mouse-wheel/gesture zoom by emitting zoom change from
  `VisNetworkHost` into parent state.
- Use a UI-friendly default slider range aligned with controller hard clamps: first
  target `0.1×` to `4.0×`. Keep the internal lower guard at `0.08` only as a
  defensive programmatic clamp, not as a normal user-facing value.
- Include Fit and Reset zoom actions.

**Acceptance criteria**

- Dragging zoom slider changes camera scale.
- Mouse-wheel or button zoom updates the slider/readout.
- Fit view still works.
- Zoom is clamped and does not throw.

**Tests**

- Component test for zoom slider calls controller camera scale update.
- Controller/unit test for scale clamping.
- Interaction test that Fit and zoom buttons remain available.

### 4.2 Expand spread range and default

**Implementation shape**

- Increase `MAX_GRAPH_LAYOUT_SPREAD` from `2.5` to a larger value, recommended
  first target `4.0`.
- Consider increasing default from `1.45` to `1.85` or `2.0` for AEC-MEPFS-first
  Explorer.
- Add Density presets:
  - Dense: `1.0×`
  - Comfortable: `1.85×`
  - Spacious: `2.5×` or `3.0×`
  - Maximum: `4.0×`
- Keep the slider for fine tuning.

**Acceptance criteria**

- The graph can visibly decompress beyond current `2.5×` limit.
- Reset returns to the selected MVP default.
- Existing graph layouts continue to work.

**Tests**

- `layoutSpread.ts` unit assertions updated for new bounds.
- Component test confirms slider exposes new max.
- Store test confirms clamping.

### 4.3 Auto-pause physics on spread changes

**Implementation shape**

- When a user changes spread in `GraphScene`, set `motionPaused` to `true` before
  or alongside `setLayoutSpread`.
- Add a small UI cue: `Physics paused after spread change` or keep the motion
  button visibly paused.
- Preserve explicit Resume behavior.
- Avoid auto-pausing when layout spread is restored during initialization unless
  it came from direct user input.

**Acceptance criteria**

- User-driven spread changes pause physics.
- Resume motion still works.
- Programmatic initialization does not create confusing toasts/cues.
- ForceAtlas2 and non-physics layouts remain stable.

**Tests**

- Component test: firing spread slider change causes Pause state to become Resume.
- Controller test: `setMotionPaused(true)` gets reflected in physics options.

### 4.4 Clamp spread in store and controller

**Implementation shape**

- Treat clamping as internal normalization, not a public store contract break.
- Import `clampGraphLayoutSpread` into `useSceneStore` or normalize at action
  boundaries so `layoutSpread` state remains valid for all callers.
- Clamp `VisNetworkHost.setLayoutSpread` too, so future controller callers cannot
  bypass store guards.
- Preserve the existing `setLayoutSpread(number)` API shape; only its persisted
  value becomes normalized.

**Acceptance criteria**

- Store never persists invalid spread.
- Controller never applies invalid spread.

**Tests**

- Store low/high clamp assertions.
- Controller spread application test with out-of-range input.


### 4.5 Harden minimap synchronization

**Implementation shape**

- Ensure `getOverviewSnapshot` version increments after filter, label/detail,
  layout, spread, zoom, and fit updates that can alter visible nodes or viewport.
- Add a visible-node-count/readiness field to the snapshot if needed so the
  minimap can distinguish unchanged positions from changed filter state.
- Keep minimap redraw throttled, but make filter/layout/zoom changes observable
  without waiting for unrelated graph movement.

**Acceptance criteria**

- Minimap updates after node-type filters change.
- Minimap updates after spread/layout changes.
- Minimap viewport updates after zoom slider, zoom buttons, mouse-wheel zoom, fit,
  and click/drag centering.

**Tests**

- Unit/component test for snapshot version changes on filter/layout/zoom events.
- Minimap interaction test for click/drag pan and keyboard fit where practical.

### 4.6 Thin edge strokes and label-to-node scale rules

**Implementation shape**

- Make default graph edge strokes visually thin: target `1px` equivalent for
  normal edges, with only selected/hover/path-highlight edges allowed to become
  slightly stronger.
- Keep edge lines as lines, not thick bands, so the taxonomy and future document
  relationships do not visually overpower nodes.
- Define node label font sizing so node text is smaller than the node glyph/body.
  Labels should read as annotations, not as larger visual objects than the nodes
  they describe.
- Preserve accessibility by relying on hover/selection/detail panels for full text
  rather than oversized always-visible labels.

**Acceptance criteria**

- Normal edge stroke width is thin and deterministic.
- Selected/path-highlight edge stroke remains visually distinguishable without
  making all edges thick.
- Node label text is smaller than the node visual body across node types.
- Tests or snapshot-style assertions pin normal/selected edge widths and label
  font sizing constants.

### 4.7 Selected-neighborhood emphasis mode

**Implementation shape**

- On node click/select, render the selected node and directly connected nodes at
  full opacity (`100%`).
- Show labels/text for the selected node and its directly connected neighbors.
- Render all unrelated nodes/edges at reduced opacity, target `50%`, with labels
  suppressed.
- Preserve selected-neighborhood ancestors/descendants as a future configurable
  depth option, but the MVP interaction should start with direct neighbors.
- Clearing selection restores the global label/filter state.

**Acceptance criteria**

- Selecting a node highlights that node and one-hop neighbors at full opacity.
- Non-neighbor nodes/edges remain visible but de-emphasized at roughly `50%`.
- Non-neighbor labels are hidden while selected-neighborhood labels remain visible.
- Clearing selection restores normal opacity and label behavior.
- Behavior composes with existing node-type filters and label visibility toggles.

**Tests**

- Unit/helper test for selected-neighborhood membership.
- Graph display test for selected vs non-selected opacity classes/options.
- Component test that node selection toggles label visibility and de-emphasis.

## 5. Phase 2 — Density and readability controls

### 5.1 Semantic label levels

Add a label strategy that responds to zoom and selection:

- far: root/domain labels only;
- mid: root + L2/L3 labels;
- near: concept/rule labels;
- focus: selected neighborhood labels regardless of global zoom.

This should complement, not replace, the existing manual label-type toggles.

### 5.2 Relationship and edge controls

Before document interrelationships become default-visible, add edge presets:

- Taxonomy only;
- Taxonomy + concept/rule anchors;
- Evidence links;
- Document references;
- Formula/code/constraint links;
- Selected neighborhood only.

### 5.3 Neighborhood focus mode

Add a focus mode for selected nodes:

- selected node;
- ancestors;
- descendants;
- direct evidence/source/document relationships;
- configurable depth (`1`, `2`, `3`, all visible branch).

### 5.4 Cluster and expand behavior

For future 5k+ scenes, use clusters or branch collapse:

- collapse by root domain;
- collapse by L2 topic;
- expand branch on click/search;
- keep minimap aligned with expanded/collapsed state.

## 6. Phase 3 — Performance readiness gates

### 6.1 Browser performance baseline

Create an Explorer performance harness with at least:

- load-to-first-render time;
- interaction pan/zoom smoke;
- node count and edge count captured;
- minimap update health;
- console error count;
- mandatory FPS or frame-budget sample for the implementation slice. If a true
  browser FPS counter is not available, the slice must explicitly build the
  missing Playwright/browser harness or document the hard blocker and use an
  interim interaction-timing proxy.

### 6.2 Test graph sizes

Maintain fixtures/evidence for:

- current 2.4k-node AEC graph;
- synthetic 5k graph;
- synthetic 10k graph or projected document-edge graph;
- selected-neighborhood reduced view.

### 6.3 Readiness thresholds

Suggested initial readiness targets:

- no console errors during load/pan/filter smoke;
- controls remain interactive under 2.4k-node baseline;
- no graph disappears during pan/drag;
- minimap updates after filters/layout changes;
- full Explorer test/lint/build stays green.

## 7. Phase 4 — MVP polish

- Add keyboard shortcuts for zoom, fit, pause/resume, search focus, and density
  presets.
- Add a short help/onboarding overlay for graph navigation.
- Persist user density/zoom/label preferences.
- Add saved views for Architecture, Structural, Electrical, Laws, Heritage, and
  Smart Systems branches.
- Add accessible labels and visible state text for graph controls.

## 8. Proposed implementation order

1. Phase 1 implementation packet: zoom slider, spread expansion, auto-pause,
   store/controller clamping, minimap sync hardening, thin edge strokes,
   label-to-node scale rules, selected-neighborhood emphasis, focused tests.
2. Browser smoke and performance evidence for the 2.4k graph, including a
   mandatory FPS/frame-budget sample or an explicit harness blocker.
3. Semantic label levels and edge presets.
4. Neighborhood focus mode.
5. Cluster/collapse branch behavior for future document relationships.
6. MVP polish and saved view presets.

## 8.1 Document interrelationship default-on gate

Document/evidence/source interrelationship edges must not become default-visible
only because taxonomy spacing improves. Before default-on document relationships,
all of the following must be true:

- semantic label levels are implemented and tested;
- selected-neighborhood emphasis is implemented and tested;
- edge presets are implemented and tested;
- normal edge stroke width and label-to-node scale rules are pinned;
- neighborhood focus mode is implemented and tested;
- minimap sync remains correct under filters/layout/zoom;
- 5k-element smoke/performance evidence passes the declared frame/interaction
  budget;
- no protected payloads are exposed in graph nodes, edges, labels, minimap,
  copied text, or reports.

## 9. Rollback strategy

Every Phase 1 change should be revertible by one commit. It should not change API
contracts, graph data, taxonomy fixtures, resolver behavior, Neo4j, KG rebuilds,
or protected content handling.

If the zoom/spread behavior feels worse, revert the Explorer UI commit and retain
this planning packet as the decision record.

## 10. Next implementation packet stub

Recommended next file:

`.ai/03_plans/AEC-MEPFS-Backbone/2026-04-28_explorer_zoom_spread_physics_implementation_packet.md`

Recommended scope:

- code changes only in Explorer UI/controller/store/minimap/graph display/tests;
- no API changes;
- no taxonomy changes;
- no Neo4j/KG/protected content changes;
- verification with focused Explorer tests, full Explorer tests, lint, build,
  and browser smoke if available.
