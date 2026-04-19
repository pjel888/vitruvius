# UX / UI Audit: `vitruvius-graph.html`

**File:** `004_Derived-Content-Layer/graph-visualizations/vitruvius-graph.html`  
**Date:** 2026-04-19  
**Auditor:** Kimi Code CLI  
**Scope:** Comprehensive user-experience and user-interface audit of the Neo4j-D3 graph explorer  

---

## 1. Executive Summary

`vitruvius-graph.html` is a single-file D3.js + Neo4j-driver graph explorer. It successfully renders a knowledge graph in three views (Full Graph, Taxonomy Tree, Concept Web) and provides a sidebar taxonomy navigator, search, detail panel, and legend. However, several UX friction points persist that degrade the exploration experience:

| Severity | Count | Category |
|----------|-------|----------|
| Critical | 2 | Query correctness, interaction trap |
| High | 5 | State management, visual feedback, navigation |
| Medium | 8 | Layout, labeling, responsiveness, discoverability |
| Low | 6 | Polish, accessibility, edge cases |

**Key Finding:** The tool is functional but not yet *trustworthy* for deep exploration. Users cannot reliably predict what will happen when they click, search, or switch modes.

---

## 2. Critical Issues (Must Fix)

### 2.1 Taxonomy Node Clicks Return No Data — FIXED in `f62a1af`
**Severity: Critical**  
**Location:** `onNodeClick()`, Cypher query  

**Problem:** The detail query used `MATCH (c:CanonicalNode {id: $id})`. Taxonomy nodes (`:Taxonomy`, `:Topic`, `:Subtopic`) do **not** carry the `:CanonicalNode` label. Clicking any taxonomy node in the graph or sidebar produced an empty detail panel. Relationship arms also constrained targets to `:CanonicalNode`, hiding `HAS_CHILD` edges.

**Fix Applied:**
```cypher
-- Before
MATCH (c:CanonicalNode {id: $id})
OPTIONAL MATCH (c)-[r]->(other:CanonicalNode)

-- After
MATCH (c) WHERE c.id = $id
OPTIONAL MATCH (c)-[r]->(other)
```

**Verification Needed:** Confirm taxonomy nodes now show incoming/outgoing `HAS_CHILD` relationships in the detail panel.

---

### 2.2 Force Simulation Auto-Zooms on Every Settle — FIXED in `f62a1af`
**Severity: Critical**  
**Location:** `renderForceLayout()`, `simulation.on('end')` handler  

**Problem:** `renderForceLayout` unconditionally registered:
```javascript
simulation.on('end', () => zoomToFit(svg, g, 600));
```
This meant **every time** the physics simulation cooled down, the camera snapped to fit-all. Consequences:
- User manually zooms in → graph settles → camera yanks back out
- User clicks "Focus 1-hop" → subgraph renders → physics settles → camera zooms back to full graph
- User drags a node to inspect → physics settles → camera resets

**Fix Applied:** Added an `autoFit` option to `renderGraph`. Only initial mode switches pass `autoFit: true`. Subsequent interactions (node click, focus 1-hop) no longer trigger post-simulation zoom.

**Verification Needed:** Click a node, pan/zoom manually, wait 5 seconds — camera should stay put.

---

## 3. High-Severity Issues

### 3.1 Selection State Is Fragile
**Severity: High**  
**Location:** `applyNodeFocus()`, `clearSelection()`, search handler  

**Problem:** The selection system uses three competing CSS classes — `.dimmed`, `.highlight`, `.search-match` — but they are not mutually exclusive. State transitions:
- Click node A → `.highlight` on A, `.dimmed` on everything else
- Search for "foo" → search calls `clearSelection()` then applies `.search-match` / `.dimmed`
- Clear search → all classes removed
- Click node B while search results are shown → `applyNodeFocus` applies `.dimmed` to non-B nodes, but search-match nodes may still retain `.search-match`

**Risk:** Visual state becomes internally inconsistent. A node could theoretically be both `.dimmed` and `.search-match`.

**Recommendation:** Implement a single `updateVisualState()` function that computes the canonical state per node from three inputs (`selectedId`, `searchTerm`, `hoveredId`) and applies the correct class. Do not let multiple functions independently toggle classes.

---

### 3.2 Detail Panel Rebuilds from Scratch on Every Node Click
**Severity: High**  
**Location:** `onNodeClick()`  

**Problem:** `detail.innerHTML = '...'` destroys and recreates the entire panel DOM on every click, including the close button. This:
- Loses scroll position if the user was reading evidence spans
- Causes visual flash/FOUC
- Makes it impossible to animate transitions
- Prevents the browser from optimizing DOM diffing

**Recommendation:** Use stable DOM structure with `display: none/block` or opacity transitions. Only update text content and visibility. Keep the close button as a persistent element.

---

### 3.3 No "Back" or Breadcrumb Navigation
**Severity: High**  
**Location:** Global  

**Problem:** The user can navigate:
1. Full Graph → click taxonomy sidebar item → filtered concept subgraph
2. Full Graph → click "Focus 1-hop" → 1-hop neighborhood
3. Full Graph → search → click a match

But there is **no way to return to the previous view state** except "Reset" which jumps all the way back to Full Graph. The user loses context.

**Recommendation:** Maintain a lightweight navigation stack (`viewHistory = []`). Add a back button (←) in the header. Pushing a new view appends to the stack; Reset clears it.

---

### 3.4 Search Auto-Pans to First Match Without User Consent
**Severity: High**  
**Location:** Search input handler  

**Problem:** Typing in the search box immediately pans and zooms to the first match at 1.5× scale. If the user was carefully inspecting a region, the camera jerks away. There is no way to see all matches without losing their spatial context.

**Recommendation:**
- Remove auto-pan on input
- Add a "Jump to first match" button next to the search box
- Show match count (e.g., "3 of 12") and next/previous buttons
- Highlight matches with a persistent glow ring but do not move the camera

---

### 3.5 Mode Buttons Lie About Active State
**Severity: High**  
**Location:** `setMode()`, `onTaxonomyClick()`  

**Problem:** Clicking a sidebar taxonomy item calls `showConceptsUnderTaxonomy()`, which renders a filtered force layout. However, the mode buttons still show "Full Graph" as active. The user is not in Full Graph mode; they are in a filtered subgraph. The UI state does not reflect the actual graph state.

**Recommendation:** Either:
- (A) Add a fourth mode button "Filtered" that becomes active when a sidebar filter is applied, or
- (B) Add a breadcrumb/bar showing the active filter (e.g., "Filtered: Construction > Safety") with an X to clear it

---

## 4. Medium-Severity Issues

### 4.1 Tree Layout Is Horizontal and Cramped
**Severity: Medium**  
**Location:** `renderTreeLayout()`  

**Problem:** The taxonomy tree uses `d3.tree().nodeSize([28, 160])` with `d3.linkHorizontal()`. This produces a left-to-right tree. With 200+ nodes, labels overlap vertically (only 28px per node). Deep hierarchies extend far to the right, requiring heavy horizontal scrolling even after zoom.

**Recommendation:** Switch to a **vertical top-down tree** (`linkVertical`, `nodeSize([160, 60])`) or a **radial layout** for taxonomy. Vertical trees map better to screen aspect ratios (wider than tall).

---

### 4.2 Node Labels Do Not Scale with Zoom
**Severity: Medium**  
**Location:** `renderForceLayout()`  

**Problem:** Text labels are always rendered at 11px regardless of zoom level. At 0.2× zoom, labels become a solid gray smear. At 3× zoom, labels are readable but enormous relative to the node.

**Recommendation:** Attach a zoom listener that shows/hides labels based on transform scale:
```javascript
svg.on('zoom', (e) => {
  g.selectAll('.node text').style('display', e.transform.k < 0.4 ? 'none' : 'block');
});
```

---

### 4.3 Arrow Markers Clip Into Large Nodes
**Severity: Medium**  
**Location:** `renderForceLayout()`, arrow markers  

**Problem:** `refX: 22` is hardcoded for all arrow markers. Taxonomy nodes have radius 10, concept nodes radius 8. The arrow sits 22px from the link endpoint, which is inside the target node circle for many cases. The arrow head is invisible or clipped.

**Recommendation:** Compute `refX` dynamically per node type: `refX = targetRadius + 10`. Or switch to path-based arrows drawn on the link line itself.

---

### 4.4 Resize Handler Destroys and Rebuilds Everything
**Severity: Medium**  
**Location:** Window resize event  

**Problem:** Resize calls `showFullGraphView()` / `showTaxonomyView()` / `showConceptView()`, which call `renderGraph()`, which destroys the entire SVG and restarts the force simulation from scratch. On window resize (e.g., snapping side-by-side), the user loses:
- Current zoom/pan position
- Selected node state
- Simulation warmth (nodes fly around again)

**Recommendation:** Debounce is already implemented (300ms), but the approach is wrong. Instead, update the SVG `viewBox` or D3 center force. Do not re-render the graph.

---

### 4.5 Loading State Is Binary (On/Off)
**Severity: Medium**  
**Location:** `loadData()`  

**Problem:** The loading spinner shows while Neo4j queries run, but there is no progress indication for the 5 sequential queries. On a slow Neo4j instance, the screen is blank for 10+ seconds with no feedback about which stage is running.

**Recommendation:** Show query progress:
```
Loading taxonomy nodes... ✓
Loading concepts... ✓
Loading hierarchy edges... (spinner)
```

---

### 4.6 Legend Is Overwhelming in Full Graph Mode
**Severity: Medium**  
**Location:** `updateLegend()`  

**Problem:** Full Graph legend shows 13 items (8 node types + 5 edge types). On smaller screens, the legend covers the graph. The edge-type colors are too similar (`var(--edge-related)` is reused for 4 edge types).

**Recommendation:**
- Collapse legend by default; click to expand
- Group edge types by semantic category (hierarchy, dependency, equivalence, contradiction)
- Use distinct colors or dash patterns for edge types that currently share gray

---

### 4.7 No Node Type Filters
**Severity: Medium**  
**Location:** Global  

**Problem:** The user cannot hide/show specific node types (e.g., hide all `:procedure` nodes to reduce clutter). This is a basic feature in Neo4j Browser and most graph explorers.

**Recommendation:** Add a filter panel in the sidebar or header with checkboxes per node type. Filters should apply without destroying the simulation — just toggle `display: none` on matching nodes and their incident edges.

---

### 4.8 Tooltip Follows Mouse but Has No Delay
**Severity: Medium**  
**Location:** `showTooltip()`  

**Problem:** Tooltip appears instantly on mouseover. When moving the cursor across a dense cluster, the tooltip flickers rapidly and is distracting.

**Recommendation:** Add a 150ms delay before showing, and a 50ms delay before hiding. Use a single timeout variable.

---

## 5. Low-Severity Issues (Polish)

### 5.1 Missing Keyboard Shortcuts
**Severity: Low**  

- `Escape` clears selection ✓ (implemented)
- `Ctrl+F` should focus search box
- `+`/`-` should zoom in/out
- Arrow keys should pan
- `1`, `2`, `3` should switch modes

### 5.2 No Right-Click Context Menu
**Severity: Low**  

Right-clicking a node does nothing. Users expect:
- "Focus this node"
- "Hide this node"
- "Show neighbors"
- "Copy node ID"

### 5.3 Detail Panel Height Is Fixed
**Severity: Low**  

`height: 220px` cannot be resized. On large monitors, this wastes space. On small laptops, it's too tall. Add a drag handle to resize.

### 5.4 Node Click Does Not Expand Sidebar Tree
**Severity: Low**  

Clicking a taxonomy node in the graph does not expand or highlight the corresponding branch in the sidebar. The two views are disconnected.

### 5.5 No Visual Feedback on Long Queries
**Severity: Low**  

When clicking a node, the detail panel shows "Loading..." but the node itself does not show a spinner or pulse. The user may wonder if the click registered.

### 5.6 Color Contrast on Dimmed Nodes
**Severity: Low**  

`.node.dimmed { opacity: 0.12 }` makes nodes nearly invisible. At 0.12 opacity on a dark background (#0f1115), the contrast ratio is well below WCAG. Users with low vision may not perceive that dimmed nodes exist at all.

**Recommendation:** Use `opacity: 0.35` for dimmed nodes, or desaturate instead of fading.

---

## 6. Accessibility (a11y)

| Issue | WCAG Level | Notes |
|-------|-----------|-------|
| No `aria-label` on SVG elements | A | Screen readers cannot describe the graph |
| No keyboard navigation for nodes | A | Tab key does not reach nodes |
| No focus indicators | A | `outline: none` is applied globally via `*` selector without replacement |
| Color alone conveys edge type | A | Edge types are distinguished only by color |
| Tooltip is not announced | A | `pointer-events: none` prevents screen reader access |
| Search has no `aria-live` region | A | Match count changes are not announced |

**Recommendation:** At minimum, add an `aria-live="polite"` region for search results and ensure the search input has a proper `<label>`.

---

## 7. Performance Observations

### 7.1 Force Simulation Re-Initialization
Every mode switch or filter change destroys the SVG, recreates all D3 selections, and restarts the force simulation. For ~500 nodes this is acceptable, but for >2000 nodes it will stutter.

### 7.2 No Data Throttling
`loadData()` fetches all nodes and edges unconditionally. There is no pagination, lazy loading, or culling. The Neo4j queries are:
```cypher
MATCH (c:CanonicalNode) WHERE c.type <> 'taxonomy'
MATCH (a:CanonicalNode)-[r]->(b:CanonicalNode)
```
These are full-table scans. With a large graph, initial load will become the bottleneck before rendering does.

### 7.3 Shallow Copies Everywhere
`allNodes.map(n => ({ ...n }))` and `allLinks.map(l => ({ ...l }))` create new objects on every view switch. For large datasets, this allocates significant temporary memory.

---

## 8. Recommendations (Prioritized)

### Phase 1 — Trust & Correctness (Do First)
1. ✅ ~~Fix taxonomy node detail query~~ (`f62a1af`)
2. ✅ ~~Fix auto-zoom on simulation settle~~ (`f62a1af`)
3. Implement a single `updateVisualState()` function to eliminate class-toggle conflicts
4. Add view history stack with back button
5. Show active filter state in the UI (mode buttons or breadcrumb)

### Phase 2 — Exploration Flow
6. Replace search auto-pan with match counter + manual jump buttons
7. Make detail panel DOM stable (no full innerHTML rebuild)
8. Add node type filter toggles in sidebar
9. Add scale-dependent label visibility
10. Fix arrow marker `refX` to respect node radius

### Phase 3 — Layout & Visual Quality
11. Switch taxonomy tree to vertical layout or radial layout
12. Make legend collapsible and group edge types semantically
13. Resize graph without full re-render (update center force + viewBox)
14. Add loading progress text ("Loaded 3 of 5 queries...")

### Phase 4 — Polish & Accessibility
15. Add keyboard shortcuts (zoom, pan, mode switch)
16. Add right-click context menu on nodes
17. Make detail panel resizable with drag handle
18. Sync sidebar tree expansion with graph node selection
19. Improve dimmed node opacity for visibility
20. Add `aria-live` region and focus management

---

## 9. Positive Findings

| Feature | Assessment |
|---------|-----------|
| Dark theme | Consistent, low eye strain, professional |
| Color palette | Semantically meaningful (blue=taxonomy, red=rule, green=definition) |
| Self-contained file | No build step required; works in any browser |
| Sidebar taxonomy tree | Useful structural overview with expand/collapse |
| Detail panel | Well-organized with incoming/outgoing sections |
| Loading spinner | Clear feedback during initial connection |
| Close button on detail panel | Obvious exit path |
| Escape key support | Standard interaction pattern |
| Zoom-to-fit | Correctly frames the graph on initial load |
| Debounced resize | Prevents excessive re-renders |

---

## 10. Conclusion

`vitruvius-graph.html` is a competent single-file graph explorer with a solid visual foundation. The two critical bugs (taxonomy query and auto-zoom) have been fixed. Remaining work centers on **state predictability** — ensuring the user always knows where they are, how they got there, and how to get back. The highest-impact next steps are the unified visual state manager, view history, and removing the search auto-pan behavior.

---

*End of audit.*
