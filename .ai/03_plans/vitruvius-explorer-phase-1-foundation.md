---
task: vitruvius-explorer-phase-1-foundation
phase: "05"
status: complete
created: 2026-04-19
---

# Phase 1 Foundation: Vitruvius Knowledge Graph Explorer

**Status:** Foundation Document — Phase 1 of 4  
**Date:** 2026-04-19  
**Scope:** Product model, perspective schema, search grammar, visual taxonomy, scene state, wireframes, API contract, component inventory  
**Sources:** Shneiderman's information-seeking mantra, NN/g progressive disclosure, WCAG 2.2 / WAI-ARIA, Baymard autocomplete research, Neo4j Bloom behavioral patterns, live Neo4j schema introspection (`scripts/audit_schema.py`)

---

## 1. Executive Summary

This document locks the product model before any visual design or implementation. It is the single source of truth for the Vitruvius Knowledge Graph Explorer rebuild.

The current `vitruvius-graph.html` is a renderer-first prototype: it loads all nodes and edges, exposes implementation modes (Full Graph / Taxonomy / Concept Web), and asks the user to survive the complexity. The new product is user-first: search-driven, perspective-bound, progressively disclosed, and evidence-centric.

**Four user jobs only:**
1. **Find** a concept, rule, or definition
2. **Browse** a taxonomy branch and its concepts
3. **Validate** a claim with evidence, confidence, and provenance
4. **Trace** how two things are connected

Everything in the UI serves one of these four jobs.

---

## 2. Product Model & User Jobs

### 2.1 Job: Find a Concept

**Trigger:** User knows (roughly) what they are looking for.  
**Goal:** Locate the canonical node, inspect its definition, and see its context.  
**Flow:**
1. User types in the command bar (e.g., "floor area", "BHL", "accessible ramps")
2. Suggestions appear grouped by: Nodes, Taxonomies, Recent, Actions
3. User selects a node → graph centers on it, inspector rail opens
4. Inspector shows: Summary, Taxonomy path, Properties, Evidence, Incoming, Outgoing
5. User can expand neighbors by relationship type, or jump to connected evidence

**Anti-patterns to avoid:**
- Do not dump all nodes and ask the user to pan/zoom to find something
- Do not require exact string matches; support aliases, fuzzy matching, and acronym resolution
- Do not show the full graph on launch

### 2.2 Job: Browse a Taxonomy Branch

**Trigger:** User wants to understand a domain area (e.g., "Fire Life Safety").  
**Goal:** Navigate the taxonomy hierarchy, see concept density per branch, and open concepts of interest.  
**Flow:**
1. User opens the taxonomy rail (or types "browse fire life safety" in the command bar)
2. Taxonomy tree expands to the requested branch; descendant counts are visible
3. User clicks a subtopic → graph shows concepts under that branch (local scene)
4. User clicks a concept → inspector opens with full details
5. User can save this filtered view as a "scene"

**Anti-patterns to avoid:**
- Do not show taxonomy as the default view (it is a browse mode, not a home state)
- Do not require the user to expand every branch manually to find concepts
- Do not lose the user's position when they switch tasks

### 2.3 Job: Validate a Claim with Evidence

**Trigger:** User sees a relationship or definition and asks "why should I believe this?"  
**Goal:** Inspect evidence spans, confidence scores, reasoning summaries, and source documents.  
**Flow:**
1. User inspects a node or edge in the inspector
2. Evidence tab shows supporting spans with document titles, quotes, and deep links
3. Confidence visualization shows the strength of the claim
4. User can open the source document at the exact span (deep_link)
5. Contradictory or competing evidence is shown if it exists

**Anti-patterns to avoid:**
- Do not hide evidence behind multiple clicks
- Do not show evidence without document context (which document? which section?)
- Do not present claims without confidence or reasoning

### 2.4 Job: Trace How Two Things Are Connected

**Trigger:** User wants to understand the relationship between two concepts (e.g., "How does Floor Area affect Building Height?").  
**Goal:** Find the shortest or most relevant path between two nodes, with explanations per hop.  
**Flow:**
1. User selects a start node (click or search)
2. User selects an end node (Shift+click or search)
3. Command bar offers "Trace path" action
4. Graph shows the path; inspector lists each hop with relationship type and reasoning
5. Alternative paths are shown if they exist

**Anti-patterns to avoid:**
- Do not require the user to manually trace edges in a dense graph
- Do not show paths without explaining why each hop exists
- Do not discard the user's current scene when tracing a path

---

## 3. Neo4j Schema Ground Truth

Introspected from the live database on 2026-04-19.

### 3.1 Node Labels (9)

| Label | Count | Role in Explorer |
|-------|-------|-----------------|
| Section | 1,036 | Source document structure — **not shown in graph** |
| Chunk | 827 | Raw text chunks — **not shown in graph** |
| DocumentVersion | 209 | Source documents — **referenced in evidence, not shown in graph** |
| CanonicalNode | 119 | **Primary entity** — concepts, rules, definitions |
| Subtopic | 52 | **Primary entity** — taxonomy leaf nodes |
| EvidenceSpan | 30 | **Primary entity** — evidence quotes and links |
| Topic | 23 | **Primary entity** — taxonomy mid-level nodes |
| Taxonomy | 11 | **Primary entity** — taxonomy root nodes |
| Assertion | (count n/a) | **Primary entity** — relationship assertions |

**Key finding:** Only the 11 Taxonomy root nodes carry both `:Taxonomy` and `:CanonicalNode` labels. The 23 Topics and 52 Subtopics carry only `:Topic` / `:Subtopic`. This is why the original `MATCH (c:CanonicalNode {id: $id})` query failed for most taxonomy nodes.

### 3.2 CanonicalNode Type Distribution

| Type | Count | Description |
|------|-------|-------------|
| concept | 88 | Domain concepts (e.g., "Floor Area", "Accessible Ramps") |
| rule | 20 | Regulatory rules and constraints |
| taxonomy | 11 | Root taxonomy categories (only the 11 roots) |

**Note:** `definition` and `procedure` types were expected but are not present in the current dataset. The schema should support them; the data will grow into them.

### 3.3 Relationship Types (10)

| Type | Count | Direction | Description |
|------|-------|-----------|-------------|
| HAS_SECTION | 1,036 | Doc → Section | Document structure — **not shown in graph** |
| HAS_CHUNK | 827 | Doc/Sec → Chunk | Content chunks — **not shown in graph** |
| BELONGS_TO | 108 | Concept → Taxonomy | Concept classification |
| HAS_CHILD | 98 | Taxonomy → Taxonomy | Taxonomy hierarchy |
| SUPPORTED_BY | 45 | Concept → EvidenceSpan | Evidence linkage |
| DEFINED_BY | 40 | Concept → Concept | Definitional relationship |
| HAS_SPAN | 15 | EvidenceSpan → Section | Evidence location — **inspector only** |
| RELATED_TO | 14 | Concept → Concept | General relationship |
| DEPENDS_ON | 12 | Concept → Concept | Dependency relationship |
| REQUIRES | 4 | Concept → Concept | Requirement relationship |

**Graph-relevant relationships:** `HAS_CHILD`, `BELONGS_TO`, `SUPPORTED_BY`, `DEFINED_BY`, `RELATED_TO`, `DEPENDS_ON`, `REQUIRES` (7 types).

### 3.4 Key Node Properties

**CanonicalNode:**
- `id` (string, required) — stable identifier
- `label` (string, required) — human-readable name
- `type` (string, required) — `concept` | `rule` | `definition` | `procedure` | `exception` | `taxonomy`
- `summary` (string) — definition or description
- `slug` (string) — URL-friendly name
- `status` (string) — `candidate` | `reviewed` | `canonical`
- `confidence` (float) — assertion confidence
- `aliases` (string[]) — alternative names
- `taxonomy_path` (string[]) — breadcrumb of taxonomy IDs
- `version` (int) — version number
- `created_at`, `updated_at` (ISO timestamps)

**EvidenceSpan:**
- `id` (string)
- `quote` (string) — raw quote from source
- `normalized_text` (string) — cleaned text
- `deep_link` (string) — URL to source location
- `document_id`, `document_version_id` (string) — provenance
- `selector`, `selector_kind` (string) — location metadata
- `parser`, `parser_version` (string) — extraction metadata

**Taxonomy / Topic / Subtopic:**
- `id` (string)
- `label` (string)
- `kind` (string) — `taxonomy` | `topic` | `subtopic`

### 3.5 Perspective Implications

The graph is currently small (119 canonical nodes, 30 evidence spans, 86 taxonomy nodes). However, the source layer is large (1,036 sections, 827 chunks, 209 document versions). The explorer must:
- **Never** load Section/Chunk/DocumentVersion nodes into the graph scene
- **Lazy-load** EvidenceSpan nodes only when inspecting a concept
- **Pre-compute** taxonomy aggregates (descendant concept counts, branch depth)
- **Budget** for 10× growth: ~1,000 canonical nodes, ~300 evidence spans

---

## 4. Perspective Schema

A **Perspective** is a curated domain view that controls: visible node types, visible relationship types, default layout, styling rules, search scopes, and filter presets. Perspectives are the primary navigation model — not modes.

### 4.1 Default Perspectives

| Perspective ID | Name | Description | Visible Nodes | Visible Edges |
|---------------|------|-------------|---------------|---------------|
| `default` | All Knowledge | Everything, for power users | All canonical + taxonomy | All graph edges |
| `concepts` | Concepts Only | Domain concepts and their relationships | concept, rule, definition, procedure, exception | RELATED_TO, DEPENDS_ON, DEFINED_BY, REQUIRES |
| `taxonomy` | Taxonomy Browser | Hierarchy and classification | taxonomy, topic, subtopic, concept | HAS_CHILD, BELONGS_TO |
| `regulatory` | Regulatory Rules | Rules, requirements, and dependencies | rule, concept | REQUIRES, DEPENDS_ON, DEFINED_BY |
| `evidence` | Evidence Map | Concepts and their supporting evidence | concept, evidence_span | SUPPORTED_BY |

### 4.2 Perspective Schema (JSON)

```json
{
  "id": "concepts",
  "name": "Concepts Only",
  "description": "Domain concepts and their relationships",
  "version": 1,
  "node_rules": [
    { "label": "CanonicalNode", "where": "type IN ['concept', 'rule', 'definition', 'procedure', 'exception']", "visible": true },
    { "label": "Taxonomy", "visible": false },
    { "label": "Topic", "visible": false },
    { "label": "Subtopic", "visible": false }
  ],
  "edge_rules": [
    { "type": "RELATED_TO", "visible": true },
    { "type": "DEPENDS_ON", "visible": true },
    { "type": "DEFINED_BY", "visible": true },
    { "type": "REQUIRES", "visible": true },
    { "type": "HAS_CHILD", "visible": false },
    { "type": "BELONGS_TO", "visible": false },
    { "type": "SUPPORTED_BY", "visible": false }
  ],
  "layout": {
    "engine": "force",
    "settings": { "charge": -600, "linkDistance": 150 }
  },
  "styling": {
    "node_defaults": { "label_visibility_threshold": 0.6 },
    "edge_defaults": { "arrowheads": true }
  },
  "search_scopes": ["CanonicalNode"],
  "filter_presets": [
    { "id": "high_confidence", "label": "High Confidence", "where": "confidence >= 0.8" }
  ],
  "scene_budget": {
    "group_parallel_edges": true,
    "label_visibility_threshold": 0.6
  }
}
```

### 4.3 Perspective Switcher

The perspective switcher lives in the command bar. It is a dropdown (combobox) with:
- Perspective name + icon
- Node count estimate
- "Create custom perspective" action (future)
- "Save current as perspective" action (future)

Switching perspectives:
1. Updates visible nodes/edges
2. Preserves camera position if possible
3. Resets selection if the selected node is hidden
4. Updates the URL (`?perspective=concepts`)

---

## 5. Search Grammar

The command bar is a combobox, not a plain input. It supports five suggestion categories: **Nodes**, **Taxonomies**, **Paths**, **Queries**, and **Actions**.

### 5.1 Suggestion Categories

| Category | Prefix | Examples | Behavior |
|----------|--------|----------|----------|
| Nodes | (none) | "floor area", "BHL", "accessible ramps" | Match `label`, `aliases`, `slug`, `id` fuzzy |
| Taxonomies | `in:` or `browse ` | `in:fire-life-safety`, `browse accessibility` | Open taxonomy branch in graph |
| Paths | `from:` | `from:floor-area to:building-height` | Trace shortest path |
| Queries | `query:` | `query:rules with confidence < 0.5` | Structured filter (future) |
| Actions | `/` | `/save`, `/reset`, `/share`, `/focus` | Execute action |

### 5.2 Search Behavior

**Input handling:**
- Typing starts immediately (no debounce for the first 2 characters; 150ms debounce after)
- Minimum 2 characters to trigger search
- Maximum 20 suggestions visible at once (no scrollbar)
- Group headers separate categories visually
- Arrow keys navigate; Enter selects; Escape closes; Tab accepts first match

**Result ranking:**
1. Exact label match
2. Prefix match on label
3. Word-boundary match on label
4. Match on aliases
5. Match on slug
6. Substring match on label
7. Fuzzy match (Levenshtein distance ≤ 3)

**No auto-pan:** Selecting a suggestion highlights the node and opens the inspector. The camera does not move unless the user explicitly clicks "Center on selection" or presses `Ctrl+Enter`.

### 5.3 Empty-State Suggestions

When the command bar is focused but empty, show:
- Recent searches (last 5)
- Recent nodes (last 5 inspected)
- Saved scenes (last 3)
- Example queries:
  - "Find rules about floor area"
  - "Browse Fire Life Safety"
  - "Trace path from BHL to AMVB"

---

## 6. Node/Edge Taxonomy & Visual Encoding

### 6.1 Node Types

| Type | Shape | Color | Icon | Size | Label Priority |
|------|-------|-------|------|------|---------------|
| taxonomy | Square | #60a5fa | 🏛️ | 12px | High |
| topic | Rounded square | #818cf8 | 📂 | 10px | High |
| subtopic | Rounded square | #c084fc | 📁 | 9px | High |
| concept | Circle | #a78bfa | 💡 | 8px | Medium |
| rule | Diamond | #f87171 | ⚖️ | 9px | High |
| definition | Hexagon | #34d399 | 📖 | 8px | Medium |
| procedure | Rounded rect | #fbbf24 | 🔧 | 8px | Medium |
| exception | Cut-corner | #f472b6 | ⚠️ | 8px | Medium |
| evidence_span | Document | #94a3b8 | 📄 | 6px | Low |

**Encoding rules:**
- Color + shape + icon + label must all convey type; never color alone
- Selected node: accent stroke (#4fc1e9), 3px width, slight scale-up (1.15×)
- Hover: accent stroke, tooltip with full label and type
- Dimmed (non-selected): opacity 0.35, desaturated
- Hidden: not rendered (not just opacity 0)

### 6.2 Edge Types

| Type | Color | Style | Arrowhead | Badge |
|------|-------|-------|-----------|-------|
| HAS_CHILD | #6b7280 | Solid | None | — |
| BELONGS_TO | #6b7280 | Dashed | None | — |
| RELATED_TO | #6b7280 | Solid | Yes | — |
| DEPENDS_ON | #f59e0b | Solid | Yes | ⚠️ if confidence < 0.5 |
| DEFINED_BY | #10b981 | Solid | Yes | ✓ |
| REQUIRES | #8b5cf6 | Solid | Yes | ! if blocking |
| SUPPORTED_BY | #94a3b8 | Dotted | None | 📄 evidence count |

**Encoding rules:**
- Arrowheads only when direction matters (relationships, not hierarchies)
- Parallel edges between the same pair are grouped into a single line with a count badge
- Hover on edge: tooltip shows relationship type, confidence, reasoning summary
- Selected edge: full inspector panel with evidence, assertion ID, confidence

### 6.3 Confidence Visualization

Confidence is a first-class visual property:
- **Node confidence:** Stroke opacity or inner halo intensity
- **Edge confidence:** Line opacity + optional warning badge if < 0.5
- **Inspector:** Explicit percentage + qualitative label ("High", "Medium", "Low", "Unverified")

---

## 7. Scene State Model

The scene is the user's current view into the graph. It must be serializable, restorable, and shareable.

### 7.1 Scene State Object

```typescript
interface SceneState {
  // Identity
  id: string;           // UUID
  name: string;         // User-given name
  perspectiveId: string;
  createdAt: string;    // ISO timestamp
  updatedAt: string;

  // Camera
  camera: {
    x: number;
    y: number;
    ratio: number;      // zoom level
  };

  // Selection
  selectedNodeIds: string[];
  selectedEdgeIds: string[];
  pinnedNodeIds: string[];  // Nodes that stay visible regardless of filters

  // Filters
  filters: {
    nodeTypes: string[];      // Included types (empty = all)
    edgeTypes: string[];      // Included types (empty = all)
    minConfidence: number;    // 0.0 to 1.0
    maxConfidence: number;
    searchQuery: string;
  };

  // Local expansion
  expandedNodeIds: string[];  // Nodes whose neighbors were manually expanded
  hiddenNodeIds: string[];    // Nodes explicitly hidden by user

  // Layout
  layoutEngine: 'force' | 'tree' | 'hierarchical' | 'radial';
  layoutSettings: Record<string, unknown>;
}
```

### 7.2 URL Sync

Scene state is persisted in the URL via query parameters:

```
/explore?perspective=concepts&selected=concept-floor-area&camera=120.5,-80.2,1.3
```

**Rules:**
- Camera updates are throttled (500ms) to avoid URL thrashing
- Selection changes are immediate
- Filter changes are immediate
- Scene name is not in URL (it requires save action)

### 7.3 Saved Scenes

Users can save scenes with a name and optional description. Saved scenes are stored in localStorage (MVP) and later synced to a backend.

```typescript
interface SavedScene {
  id: string;
  name: string;
  description?: string;
  state: SceneState;
  thumbnail?: string;  // Base64 PNG of the scene at save time
}
```

---

## 8. App Shell & Zone Architecture

### 8.1 Four-Zone Desktop Shell

```
+-------------------------------------------------------------+
| [Logo] [Perspective ▼] [Command Bar___________] [Status]   |  56px
+----------+----------------------------------+---------------+
|          |                                  |               |
| Explorer |        GRAPH SCENE               |  Inspector    |
|  Rail    |        (fluid canvas)            |  Rail         |
|  320px   |                                  |  400px        |
|          |                                  |               |
|          |                                  |               |
|          |                                  |               |
|          |                                  |               |
+----------+----------------------------------+---------------+
| [Bottom drawer — closed by default]                         |
+-------------------------------------------------------------+
```

**Zone details:**

| Zone | Width | Purpose | Default State |
|------|-------|---------|---------------|
| Command Bar | Full width | Search, perspective switch, actions, status | Always visible |
| Explorer Rail | 320px | Taxonomy tree, saved scenes, filter panel, recent | Open on browse tasks |
| Graph Scene | Fluid | WebGL graph canvas, minimap, floating actions | Always visible |
| Inspector Rail | 400px | Node/edge details, evidence, properties, history | Open when something is selected |
| Bottom Drawer | Full width | Source preview, table view, query details, console | Closed; opens on evidence click |

### 8.2 Responsive Breakpoints

| Breakpoint | Explorer | Inspector | Bottom Drawer |
|-----------|----------|-----------|---------------|
| ≥1440px | 320px rail | 400px rail | Full width |
| ≥1024px | 280px rail | 360px rail | Full width |
| <1024px | Collapsed to icon button | Collapsed to icon button | Sheet (modal) |
| <768px | Bottom sheet | Bottom sheet | Bottom sheet |

On tablet/mobile, prioritize: search → inspect → saved scenes. Freeform graph authoring is secondary.

---

## 9. Wireframes

### 9.1 Home / Empty State

```
+-------------------------------------------------------------+
| Vitruvius Graph   [Perspective: All Knowledge ▼]   Conn ✓  |
+-------------------------------------------------------------+
|                                                             |
|                    Vitruvius Knowledge Graph                |
|                                                             |
|     [🔍 Search the graph]        [📊 Show sample graph]     |
|                                                             |
|  ─────────────────── Recent ────────────────────           |
|  [📁 Fire Life Safety]  [📁 Accessible Ramps]  [📁 BHL]    |
|                                                             |
|  ───────────────── Saved Scenes ────────────────           |
|  [🎬 Regulatory Rules]  [🎬 Evidence Map]                  |
|                                                             |
|  ─────────────── Example Queries ───────────────           |
|  "Find rules about floor area"                              |
|  "Browse Fire Life Safety taxonomy"                        |
|  "Trace path from BHL to AMVB"                             |
|  "Show high-confidence definitions"                        |
|                                                             |
+-------------------------------------------------------------+
```

**Rules:**
- Do not auto-load the full graph
- Primary actions: Search, Sample Graph
- Secondary: Recent perspectives, saved scenes, example queries
- Keyboard: Tab cycles through primary actions; Enter activates

### 9.2 Explore (Active Scene)

```
+-------------------------------------------------------------+
| Vitruvius Graph  [All Knowledge ▼] [Search____________] [⚙️] |
+----------+----------------------------------+---------------+
| Taxonomy |                                  | Inspector     |
| ▼ Fire   |      [Graph Scene]               | ┌───────────┐ |
|   ▼ Life |                                  │ │ Floor Area│ |
|     ▼ Saf|      ●─────→●                    │ │ (concept) │ |
|       [🔥│      │      ↑                     │ ├───────────┤ |
|       [🏗│      ↓      │                     │ │ Summary   │ |
|       [🏠│      ●←─────●                    │ │ ...       │ |
|          |                                  │ ├───────────┤ |
| [Filters]|                                  │ │ Evidence  │ |
| ☑ concept|      [Minimap]                   │ │ 📄 3 spans│ |
| ☑ rule   |      [Fit] [Zoom+] [Zoom-]       │ ├───────────┤ |
|          |                                  │ │ Incoming  │ |
|          |                                  │ │ ← DEFINED_BY│ |
|          |                                  │ ├───────────┤ |
|          |                                  │ │ Outgoing  │ |
|          |                                  │ │ → DEPENDS_ON│ |
|          |                                  │ └───────────┘ |
+----------+----------------------------------+---------------+
```

**Rules:**
- Explorer rail shows taxonomy tree + filter toggles
- Graph scene is the dominant surface
- Inspector rail opens on selection; empty state when nothing selected
- Minimap is bottom-right overlay
- Zoom controls are bottom-left overlay
- Selection persists when panning/zooming

### 9.3 Taxonomy Browse

```
+-------------------------------------------------------------+
| ...                                                         |
+----------+----------------------------------+---------------+
| Taxonomy |                                  | Inspector     |
| ▼ Fire   |      [Filtered Graph]            │               |
|   ▼ Life |                                  │  Select a     |
|     ▼ Saf|      ●──●──●                     │  concept to   |
|       [🔥│      │  │  │                     │  see details  |
|       [🏗│      ●  ●  ●                     │               |
|       [🏠│                                  │               |
|          |      12 concepts in this branch  │               |
| [Filters]|                                  │               |
|          |                                  │               |
+----------+----------------------------------+---------------+
```

**Rules:**
- Clicking a taxonomy branch filters the graph to concepts under that branch
- Branch concept count is shown in the tree (descendant count, not just direct)
- Graph title or breadcrumb shows the active branch
- "Clear filter" action returns to unfiltered perspective

### 9.4 Inspector — Node Detail

```
┌─────────────────────────────────────┐
│ Floor Area                    [×]   │
│ (concept)  [⭐ Pin] [🎯 Focus]      │
├─────────────────────────────────────┤
│ 📋 Summary                          │
│ The overall size of a proposed      │
│ building/structure characterized    │
│ by gross floor area...              │
├─────────────────────────────────────┤
│ 🗂️ Taxonomy Path                    │
│ Building Code > Floor Area > ...    │
├─────────────────────────────────────┤
│ 📄 Evidence (3)                     │
│ ├─ 📄 PD957 §4.2 — "The overall..." │
│ ├─ 📄 IRR §3.1 — "Gross floor..."   │
│ └─ 📄 CLUP §2.5 — "Building bulk..."│
├─────────────────────────────────────┤
│ ← Incoming (2)                      │
│ DEFINED_BY ← Building Bulk          │
│ RELATED_TO ← AMVB                   │
├─────────────────────────────────────┤
│ → Outgoing (4)                      │
│ DEPENDS_ON → Building Height        │
│ REQUIRES → Setback                  │
│ DEFINED_BY → GFA                    │
│ RELATED_TO → AMBF                   │
├─────────────────────────────────────┤
│ ⚡ Actions                           │
│ [Expand neighbors] [Trace path]     │
│ [Hide node] [Copy ID]               │
└─────────────────────────────────────┘
```

**Rules:**
- Tabs or collapsible sections: Summary, Evidence, Incoming, Outgoing, Actions, History
- Evidence spans are clickable → open source preview in bottom drawer
- Relationship rows are clickable → select the edge in the graph
- Pin action keeps the node visible across filter changes
- Focus action isolates the 1-hop neighborhood

### 9.5 Inspector — Edge Detail

```
┌─────────────────────────────────────┐
│ DEPENDS_ON                    [×]   │
│ Floor Area → Building Height        │
├─────────────────────────────────────┤
│ Confidence: 0.82 (High)             │
│ Assertion ID: asst-001-...          │
├─────────────────────────────────────┤
│ 🧠 Reasoning                        │
│ Floor area directly constrains the  │
│ maximum building height through the │
│ AMVB calculation...                 │
├─────────────────────────────────────┤
│ 📄 Supporting Evidence              │
│ ├─ PD957 §4.2 (confidence: 0.9)     │
│ └─ IRR §3.1 (confidence: 0.75)      │
├─────────────────────────────────────┤
│ ⚡ Actions                           │
│ [Select source] [Select target]     │
│ [Hide edge] [Copy assertion ID]     │
└─────────────────────────────────────┘
```

### 9.6 Path Trace View

```
+-------------------------------------------------------------+
| ...                                                         |
+----------+----------------------------------+---------------+
|          |      [Path Highlighted]          | Path Inspector│
|          |                                  │               │
|          │      ●──→●──→●──→●              │ From: Floor   │
|          │      A    B    C    D           │ Area          │
|          |                                  │ To: Building  │
|          |                                  │ Height        │
|          |                                  │               │
|          |                                  │ Hop 1:        │
|          |                                  │ DEPENDS_ON    │
|          |                                  │ Floor Area →  │
|          |                                  │ AMVB          │
|          |                                  │               │
|          |                                  │ Hop 2:        │
|          |                                  │ REQUIRES      │
|          |                                  │ AMVB → BHL    │
|          |                                  │               │
|          |                                  │ [Show alt     │
|          |                                  │  paths]       │
+----------+----------------------------------+---------------+
```

---

## 10. Graph API Contract

The browser never connects directly to Neo4j. All data access goes through a Graph API BFF.

### 10.1 Base URL

```
https://api.vitruvius.local/v1/graph
```

### 10.2 Endpoints

#### `GET /search`

Full-text and structured search across the graph.

**Query parameters:**
```
q          string  required  Search query
perspective string  optional  Filter by perspective ID
limit      integer optional  Max results (default: 20)
offset     integer optional  Pagination offset
```

**Response:**
```json
{
  "results": [
    {
      "kind": "node",
      "id": "concept-floor-area",
      "label": "Floor Area",
      "type": "concept",
      "matchType": "exact",
      "matchedField": "label",
      "highlight": "<mark>Floor</mark> <mark>Area</mark>"
    }
  ],
  "suggestions": {
    "nodes": [...],
    "taxonomies": [...],
    "actions": [...]
  }
}
```

#### `GET /node/:id`

Fetch a single node with its relationships and evidence.

**Response:**
```json
{
  "node": {
    "id": "concept-floor-area",
    "label": "Floor Area",
    "type": "concept",
    "summary": "...",
    "properties": { ... }
  },
  "taxonomyPath": [
    { "id": "taxonomy-building-code", "label": "Building Code", "kind": "taxonomy" },
    { "id": "topic-floor-area", "label": "Floor Area", "kind": "topic" }
  ],
  "incoming": [
    {
      "relType": "DEFINED_BY",
      "from": { "id": "concept-building-bulk", "label": "Building Bulk", "type": "concept" },
      "reasoning": "...",
      "confidence": 0.85,
      "assertionId": "asst-001"
    }
  ],
  "outgoing": [...],
  "evidence": [
    {
      "id": "span-001",
      "quote": "The overall size...",
      "documentId": "doc-pd957",
      "documentTitle": "PD 957",
      "deepLink": "/viewer/pd957?section=...",
      "confidence": 0.92
    }
  ]
}
```

#### `GET /expand`

Fetch neighbors of a node, optionally filtered by relationship type.

**Query parameters:**
```
nodeId     string  required
relTypes   string  optional  Comma-separated (e.g., "DEPENDS_ON,REQUIRES")
direction  string  optional  "out", "in", "both" (default: "both")
limit      integer optional  Max neighbors (default: 50)
```

**Response:**
```json
{
  "nodeId": "concept-floor-area",
  "neighbors": [
    { "node": { ... }, "relType": "DEPENDS_ON", "direction": "out", "edge": { ... } }
  ],
  "hasMore": false
}
```

#### `GET /path`

Find paths between two nodes.

**Query parameters:**
```
from       string  required  Start node ID
to         string  required  End node ID
maxHops    integer optional  Max path length (default: 6)
limit      integer optional  Max paths (default: 5)
```

**Response:**
```json
{
  "paths": [
    {
      "length": 3,
      "nodes": [{ ... }, { ... }, { ... }],
      "edges": [{ ... }, { ... }]
    }
  ]
}
```

#### `GET /taxonomy`

Fetch the taxonomy tree structure.

**Query parameters:**
```
rootId     string  optional  Filter to a specific root
includeCounts boolean optional  Include descendant concept counts (default: true)
```

**Response:**
```json
{
  "roots": [
    {
      "id": "taxonomy-fire-life-safety",
      "label": "Fire Life Safety",
      "kind": "taxonomy",
      "conceptCount": 14,
      "children": [
        {
          "id": "topic-fire-suppression",
          "label": "Fire Suppression",
          "kind": "topic",
          "conceptCount": 8,
          "children": [...]
        }
      ]
    }
  ]
}
```

#### `GET /perspectives`

List available perspectives.

**Response:**
```json
{
  "perspectives": [
    { "id": "default", "name": "All Knowledge", "nodeCount": 205, "isDefault": true },
    { "id": "concepts", "name": "Concepts Only", "nodeCount": 108 }
  ]
}
```

#### `POST /scene/save`

Save a scene state.

**Request body:** `SceneState` object (see §7.1)

**Response:** `{ "sceneId": "uuid", "url": "/explore?scene=uuid" }`

#### `GET /scene/:id`

Retrieve a saved scene.

**Response:** `SceneState` object

### 10.3 Error Schema

```json
{
  "error": {
    "code": "NODE_NOT_FOUND",
    "message": "Node 'concept-unknown' not found",
    "status": 404
  }
}
```

| Code | Status | Meaning |
|------|--------|---------|
| `NODE_NOT_FOUND` | 404 | Requested node does not exist |
| `INVALID_PERSPECTIVE` | 400 | Perspective ID is not recognized |
| `PATH_NOT_FOUND` | 404 | No path exists between the given nodes |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

---

## 11. Component Inventory

### 11.1 Shell Components

| Component | Source | Notes |
|-----------|--------|-------|
| CommandBar | Custom | Combobox with grouped suggestions; follows WAI-ARIA combobox pattern |
| Toolbar | Custom | Follows WAI-ARIA toolbar pattern; arrow-key navigation |
| PerspectiveSwitcher | Custom | Dropdown within command bar |
| StatusIndicator | Custom | Connection status, node count, last updated |

### 11.2 Explorer Rail Components

| Component | Source | Notes |
|-----------|--------|-------|
| TaxonomyTree | Custom | WAI-ARIA treeview pattern; keyboard: arrows, Home/End, typeahead |
| FilterPanel | Custom | Checkbox groups for node types, edge types, confidence range |
| SavedSceneList | Custom | List of saved scenes with thumbnails |
| RecentList | Custom | Recent nodes, searches, scenes |

### 11.3 Graph Scene Components

| Component | Source | Notes |
|-----------|--------|-------|
| GraphRenderer | **Sigma.js** | WebGL graph engine; primary renderer |
| Minimap | Sigma.js plugin or custom | Overview window, click to pan |
| ZoomControls | Custom | + / - / fit buttons |
| SelectionLasso | Sigma.js or custom | Marquee/multi-select |
| ContextMenu | Custom | Right-click menu on nodes/edges/canvas |

### 11.4 Inspector Rail Components

| Component | Source | Notes |
|-----------|--------|-------|
| NodeInspector | Custom | Tabs: Summary, Evidence, Incoming, Outgoing, Actions |
| EdgeInspector | Custom | Relationship details, evidence, confidence |
| EvidenceList | Custom | Collapsible evidence spans with document links |
| PropertyTable | Custom | Key-value table for node properties |

### 11.5 Bottom Drawer Components

| Component | Source | Notes |
|-----------|--------|-------|
| SourcePreview | Custom | Render source document at evidence span location |
| TableView | Custom | Tabular view of nodes/edges for the current scene |
| QueryDetails | Custom | Show the Cypher/API query that produced the current view |

### 11.6 Third-Party Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| React | 18.x | UI framework |
| TypeScript | 5.x | Type safety |
| Sigma.js | 3.x | WebGL graph renderer |
| graphology | 0.25 | Graph data structure and algorithms |
| Tailwind CSS | 3.x | Utility-first styling |
| Radix UI | 1.x | Primitives: combobox, tooltip, dialog, tabs |
| React Query | 5.x | Server state management |
| Zustand | 4.x | Client state management |
| React Router | 6.x | URL routing and state sync |

---

## 12. Accessibility Requirements (WCAG 2.2)

### 12.1 Keyboard Completeness

| Feature | Key | Behavior |
|---------|-----|----------|
| Focus command bar | `/` or `Ctrl+K` | Focus search input |
| Navigate suggestions | ↑ / ↓ | Move through suggestion list |
| Accept suggestion | Enter | Select highlighted suggestion |
| Accept first | Tab | Accept first suggestion |
| Close suggestions | Escape | Close list, keep input focused |
| Clear selection | Escape | Clear graph selection |
| Zoom in | `+` | Increase zoom |
| Zoom out | `-` | Decrease zoom |
| Fit to view | `0` | Fit all visible nodes |
| Switch perspective | `1`–`5` | Jump to perspective N |
| Pan canvas | Arrow keys | Move camera |
| Select next node | Tab | Cycle through visible nodes |
| Expand neighbors | `E` | Expand selected node |
| Trace path | `P` | Open path trace dialog |
| Save scene | `Ctrl+S` | Save current scene |

### 12.2 Focus Management

- All interactive elements have visible focus indicators (minimum 2px outline, accent color)
- Focus trap inside modals and drawers
- `aria-live="polite"` region for search results and status updates
- `aria-label` on all icon-only buttons

### 12.3 Target Sizes

- Minimum: 24×24px (WCAG 2.5.8 Level AA)
- Preferred desktop: 32×32px
- Touch targets: 44×44px

### 12.4 Color & Contrast

- Never convey information by color alone; always pair with shape, icon, or text
- Minimum contrast ratio: 4.5:1 for normal text, 3:1 for large text/UI components
- Dimmed nodes at 0.35 opacity must still be perceivable (test with grayscale)

### 12.5 Dragging Alternatives

- Pan: drag OR arrow keys
- Zoom: scroll OR +/- keys OR buttons
- Node drag: drag OR select + arrow keys to nudge
- Multi-select: Shift+click OR checkbox list in inspector

---

## 13. Analytics & Events

Track these events to measure product health:

| Event | Trigger | Purpose |
|-------|---------|---------|
| `search.executed` | User submits search | Measure search adoption |
| `search.result_clicked` | User clicks a suggestion | Measure search success |
| `node.selected` | User clicks a node | Measure exploration depth |
| `edge.selected` | User clicks an edge | Measure relationship inspection |
| `evidence.opened` | User clicks evidence span | Measure trust verification |
| `source.opened` | User opens source document | Measure provenance follow-through |
| `perspective.changed` | User switches perspective | Measure perspective utility |
| `scene.saved` | User saves a scene | Measure engagement |
| `scene.shared` | User copies scene URL | Measure shareability |
| `path.traced` | User traces a path | Measure trace utility |
| `error.api` | API returns error | Measure reliability |

---

## 14. Level-of-Detail Budgets

### 14.1 Rendering Performance Model

The system does not impose arbitrary visibility caps. Instead, it adapts to the data and offers user control over the trade-off between completeness and performance.

**Adaptive rendering (automatic):**

| Resource | Adaptive Behavior | User Override |
|----------|------------------|---------------|
| Node visibility | All nodes rendered by default; clustering offered when FPS drops below 30 for 2s | User can toggle clustering on/off |
| Labels | Hidden when zoom < 0.4; shown when zoom ≥ 0.4; always shown on hover/selection | User can force "show all labels" |
| Edges | All edges rendered; parallel edges grouped automatically | Grouping toggle |
| Evidence spans | All spans listed in inspector; collapsed by default after 5 | "Expand all" button per section |
| Search results | All matches returned; top 10 shown, scroll for more | Limit dropdown (10 / 25 / 50 / All) |

**Performance safeguards (not hard limits):**

| Trigger | System Response |
|---------|-----------------|
| Scene exceeds 2,000 nodes on load | Show notice: "2,847 nodes found. Rendering all. Disable 'Show all labels' if performance degrades." |
| FPS drops below 20 for 3s | Show toast: "Performance notice: consider enabling clustering or hiding labels." |
| Expansion would add >500 nodes | Show confirmation: "This will add 612 nodes to the scene. Continue?" |
| Path search exceeds 8 hops | Show: "No path found within 8 hops. Increase hop limit?" |

**User-controlled visibility panel (in Explorer Rail):**

```
[✓] Show all nodes
[✓] Show all edges
[✓] Show all labels  [⚠️ may affect performance]
[✓] Group parallel edges
[✓] Cluster dense regions  [?]

Node type visibility:
[✓] Taxonomy    [✓] Topic    [✓] Subtopic
[✓] Concept     [✓] Rule     [✓] Definition
[✓] Procedure   [✓] Exception

Edge type visibility:
[✓] HAS_CHILD   [✓] BELONGS_TO   [✓] RELATED_TO
[✓] DEPENDS_ON  [✓] DEFINED_BY   [✓] REQUIRES
[✓] SUPPORTED_BY

Performance:
Current: 312 nodes, 248 edges  |  60 FPS
```

### 14.2 Hard Limits (System Guardrails Only)

| Resource | Hard Limit | Behavior |
|----------|-----------|----------|
| Path length search | 12 hops | Configurable up to 12; beyond that, return "path too long" |
| Saved scenes | 100 per user | Warn at 90; offer export/delete |
| Search result payload | 1,000 items | Paginate beyond 1,000 |
| API timeout | 30s | Return partial results with continuation token |

---

## 15. Success Criteria (Phase 1 Gates)

Phase 1 is complete when:

- [ ] All documents in this foundation are reviewed and approved
- [ ] Wireframes are validated with 2+ user walkthroughs (even if informal)
- [ ] Graph API contract is reviewed by backend owner
- [ ] Neo4j schema is confirmed to support all API endpoints (or migration plan exists)
- [ ] Component inventory is approved by frontend owner
- [ ] Accessibility checklist is reviewed
- [ ] Analytics event schema is instrumented in the design

Phase 2 may not begin until all gates are true.

---

## 16. Appendix: Current vs. Target Comparison

| Aspect | Current (vitruvius-graph.html) | Target (Explorer) |
|--------|-------------------------------|-------------------|
| **Entry point** | Full graph auto-loads | Home screen with search + samples |
| **Primary nav** | Mode buttons (Full/Taxonomy/Concept) | Perspective switcher + command bar |
| **Search** | Substring input, auto-pans to first match | Combobox with ranked, grouped suggestions |
| **Taxonomy** | Flat div tree, 16px toggles | ARIA treeview with keyboard nav, counts |
| **Graph renderer** | D3 SVG force layout | Sigma.js WebGL |
| **Inspector** | 220px bottom drawer | 400px right rail with tabs |
| **Evidence** | Inline in detail panel | Dedicated Evidence tab with source links |
| **Path tracing** | Not supported | First-class feature with inspector |
| **State** | Global mutable vars | Normalized store + URL sync |
| **Backend** | Browser → Neo4j direct | Graph API BFF |
| **Accessibility** | Hover-only tooltips | Keyboard-complete, focus-aware, WCAG 2.2 |
| **Mobile** | Not supported | Responsive sheets + prioritized actions |

---

*End of Phase 1 Foundation Document.*
