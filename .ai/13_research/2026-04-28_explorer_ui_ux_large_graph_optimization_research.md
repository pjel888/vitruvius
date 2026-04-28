# Explorer UI/UX Large-Graph Optimization Research Pack

```yaml
status: RESEARCH_READY
created: 2026-04-28
branch: main
start_commit: 11f92fa5
scope: Explorer dense AEC-MEPFS graph UI/UX and performance planning
```

## 1. Research question

Explorer now renders the AEC-MEPFS backbone as a dense, living graph: latest
validated evidence run `20260428T063500Z` has `2424` nodes, `2400` edges, `24`
roots, `240` L2 topics, `720` L3 subtopics, and `1440` L4 concept/rule anchors.
The product question is how to keep the graph understandable and performant as
it grows into document and evidence interrelationships.

Specific requested directions:

- add a continuous zoom slider, not only zoom buttons;
- make the graph spread more expansive;
- pause physics automatically when the user changes spread;
- give nodes more breathing room so the graph is not cramped;
- plan for a future graph with document/evidence relationships, not just taxonomy
  hierarchy edges.

## 2. External evidence consulted

| Source | Relevant guidance for Vitruvius Explorer |
|---|---|
| Vis Network physics documentation — <https://visjs.github.io/vis/docs/network/physics.html> | Physics can be toggled, stabilized, and tuned through repulsion, spring length, damping, velocity, timestep, and stabilization options. The docs specifically describe stronger repulsion via more negative gravity, larger spring length/node distance, and physics on/off control. |
| Cytoscape.js documentation — <https://js.cytoscape.org/> | Interactive graph libraries are expected to support pan, zoom, selection, and graph event integration; the docs also call out large-graph rendering costs and performance options such as lower pixel ratio, hiding edges during viewport movement, and texture-based viewport interaction. |
| Cytoscape.js 2023 update paper — <https://academic.oup.com/bioinformatics/article/39/1/btad031/6988031> | Modern graph UIs are used for exploratory network visualization, and usability improvements include easier, more precise selection in dense networks plus layout extensibility. This supports investing in dense-network interaction affordances rather than treating the graph as static decoration. |
| Shneiderman information visualization mantra slides — <https://math.nist.gov/mcsd/Seminars/2006/2006-10-03-shneiderman-presentation.pdf> | The classic pattern is overview first, zoom/filter, then details on demand. Explorer already has overview/minimap and filters; the next UI plan should strengthen zoom, semantic label/detail control, and details-on-demand. |
| Semantic zoom / multi-level graph visualization paper — <https://arxiv.org/abs/1906.05996> | Large graph readability benefits from multi-level representations: show appropriate detail at each level, label higher-level nodes without label overlap, and reveal deeper nodes/paths as the user zooms. This maps directly to taxonomy roots/topics/subtopics/concepts/rules and future document relationships. |

## 3. Best-practice synthesis

### 3.1 Overview first, then controlled detail

Explorer should preserve a stable whole-graph overview while making local detail
progressively available. The current minimap and taxonomy tree already point in
that direction. The next step is to make zoom state explicit and user-controllable
through a zoom slider and presets.

### 3.2 Semantic zoom instead of all labels all the time

The graph is already too large for every node label and every future relationship
label to be visible at every zoom level. Node text visibility controls exist, but
semantic zoom should eventually add automatic detail levels:

- far zoom: domains/root nodes and selected highlights;
- mid zoom: topics/subtopics and selected-neighborhood labels;
- near zoom: concept/rule anchors and document/evidence labels;
- focus mode: selected node, ancestors, descendants, and direct evidence links.

### 3.3 Spacing is good, but should be user-controlled

More node spacing is the correct default direction for a 2.4k-node graph. The
current default layout spread (`1.45×`) and max (`2.5×`) were calibrated for a
smaller graph. The larger graph should use a more comfortable default and a wider
upper bound. However, spacing alone will not solve future document-edge density;
spacing must be paired with edge filters, semantic zoom, and neighborhood focus.

### 3.4 Physics should be helpful, then get out of the way

Continuous physics motion is expensive and visually distracting on a dense graph.
The app already pauses/auto-freezes large graph physics after stabilization. User
spread changes should also auto-pause or re-stabilize in a bounded way so the
slider acts like a deterministic layout control rather than a janky live force
simulation.

### 3.5 Future document interrelationships require density management

When actual documents, clauses, evidence, sources, and formulas become graph
neighbors, the taxonomy backbone can no longer rely on a single full-graph view.
Explorer needs at least four density controls before that phase:

1. edge class toggles and relationship presets;
2. neighborhood-depth focus;
3. cluster/expand for taxonomy branches and document groups;
4. performance budgets for 2.5k, 5k, and 10k element scenes.

### 3.6 Selection should create a local focus lens

Dense graph UIs need a fast way to reduce attention load without fully hiding the
network. A one-hop selection lens should keep the selected node and directly
connected nodes at full opacity with labels while unrelated graph context remains
visible at reduced opacity and without labels. This follows the same overview +
details-on-demand principle: context remains, detail moves to the selected local
neighborhood.

### 3.7 Edge and label styling should preserve visual hierarchy

Normal edges should read as thin relationship lines. Thick strokes should be
reserved for selected, hovered, or path-highlighted relationships. Node labels
should be smaller than node bodies so text does not become the dominant visual
shape in the graph.

## 4. Product implications for MVP

Recommended MVP direction:

- Add a zoom slider as a first-class camera control.
- Expand the spread slider range and default to a more spacious layout.
- Auto-pause physics when spread changes; provide an obvious Resume motion action.
- Add graph density presets: Dense, Comfortable, Spacious.
- Add semantic label strategy next, not only manual label checkboxes.
- Make normal edges thin lines and keep text smaller than node bodies.
- Add selected-neighborhood emphasis: selected node plus connected nodes at full
  opacity with labels; unrelated graph at reduced opacity without labels.
- Add performance/readiness gates before document interrelationship edges are
  enabled by default.

## 5. Research limitations

- This pack is a planning artifact; it does not measure browser FPS directly.
- It uses external general graph-visualization guidance and current repo evidence,
  not a fresh user-study of Vitruvius-specific behavior.
- Browser-level profiling should be part of the next implementation slice.
