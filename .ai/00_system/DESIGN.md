---
version: alpha
name: Vitruvius Explorer Design Mandate
description: Grid-first, hierarchy-driven interface rules for Vitruvius UI work.
colors:
  primary: "#071015"
  bg: "#071015"
  panel: "#101922"
  panelHover: "#172331"
  border: "#263646"
  text: "#D9E2EA"
  textDim: "#8FA0AE"
  accent: "#39D5C8"
  accentDim: "#218C91"
typography:
  body:
    fontFamily: Avenir Next
    fontSize: 14px
    lineHeight: 1.45
  title:
    fontFamily: Avenir Next
    fontSize: 14px
    fontWeight: 600
    letterSpacing: "-0.01em"
  labelCaps:
    fontFamily: Avenir Next
    fontSize: 10px
    fontWeight: 500
    letterSpacing: "0.22em"
rounded:
  control: 12px
  card: 16px
  panel: 0px
spacing:
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  region: 32px
layout:
  gridUnit: 4px
  navigatorWidth: 18rem
  inspectorWidth: 24rem
  inspectorCollapsedWidth: 2.5rem
  headerMinHeight: 84px
  canvasInset: 16px
components:
  app-header:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.text}"
    typography: "{typography.body}"
    width: 100%
    height: 84px
    padding: "{spacing.lg}"
  graph-canvas:
    backgroundColor: "{colors.bg}"
    textColor: "{colors.text}"
    typography: "{typography.body}"
    padding: 16px
  dropdown-control:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.text}"
    typography: "{typography.body}"
    rounded: "{rounded.control}"
    height: 40px
    padding: 12px
  card:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.text}"
    rounded: "{rounded.card}"
    padding: "{spacing.lg}"
sourceInfluence:
  googleDesignMd: "https://github.com/google-labs-code/design.md"
---

# Vitruvius Explorer Design Mandate

## Overview

This file is the project-level UX/UI mandate for Vitruvius interfaces. It follows the broad `DESIGN.md` pattern from Google Labs Code: machine-readable tokens first, then human rationale that coding agents can apply consistently. The Google format is intentionally token plus prose; Vitruvius adds stricter product rules for spatial hierarchy, grid alignment, and evidence-first graph work.

The core mandate:

**Every interface must follow a grid, expose hierarchy, and align controls to the content region they affect.**

For Explorer specifically, the layout has three primary horizontal regions:

- `Navigator region`: the left rail, currently `18rem`.
- `Graph canvas region`: the center workspace between Navigator and Inspector.
- `Inspector region`: the right rail, currently `24rem` when open and `2.5rem` when collapsed.

Nothing interactive belongs above the Navigator unless it operates on the Navigator itself. The only header content above the Navigator is the persistent identity block:

```text
Vitruvius
Knowledge Graph
Explorer workspace
```

Graph controls, dropdowns, search, scene controls, and layout controls should align with the graph canvas region. Inspector data and inspector minimize/restore controls should align with the Inspector region.

## Colors

The current Explorer visual language is a dark analytical workspace with a restrained cyan accent. Color is functional, not decorative.

- Use `bg`, `panel`, and `panelHover` to establish depth without changing spatial hierarchy.
- Use `border` to make grid boundaries legible.
- Use `accent` for active controls, focus states, and primary interaction hints.
- Use graph node colors only for semantic graph categories, not generic UI decoration.

Color must not compensate for weak layout. If an interface needs color to explain grouping, the grouping is probably structurally unclear.

## Typography

Typography communicates hierarchy before decoration.

- `labelCaps` is for small section labels above controls, never inside the selected-value text of a dropdown.
- Selected values should be plain, readable text: `All Knowledge`, `Unsaved view`, `Network Layout`.
- Headers should be compact and stable; avoid labels that change width dramatically during normal exploration.
- Long canonical graph labels should be available on inspection, but compact display labels should drive scannability.

## Layout & Spacing

Grid alignment is mandatory.

- Align controls to content regions, not to arbitrary neighboring text.
- Header controls that affect the graph must start at the graph canvas column, after `navigatorWidth`.
- Header data that describes or controls the Inspector must sit in the inspector column, above the right rail.
- Menus should open from their trigger and remain in the same region as the trigger.
- Cards in graph corners should align to a shared inset and should not float at unrelated x/y positions.
- Legends, minimaps, overlays, and command panels must share a common edge rhythm.
- A visible boundary, such as the Navigator rail border, creates an alignment contract for every element above and below it.
- Use `xs` and `sm` for micro relationships, `md` and `lg` for control clusters, and `xl` or `region` only for separating major regions.
- Status pills and sidebar buttons are a control cluster: keep them horizontal with at least `md` spacing.

Before changing UI, identify the owning region:

- Navigator control: may align inside the Navigator column.
- Graph control: must align inside the graph canvas column.
- Inspector control: must align inside the inspector column, including minimize and restore buttons.
- Global app identity: may occupy the identity column only.

If a component crosses a region boundary, the design must justify why.

## Elevation & Depth

Depth should clarify interaction state and layering.

- Dropdown menus must render above the graph canvas.
- Menus, popovers, and overlays must never appear underneath canvas or WebGL/vis layers.
- Use shadows and backdrop blur sparingly to separate command surfaces from the graph.
- Stacking order must follow interaction priority: menus above command bar overlays, command surfaces above graph overlays, graph overlays above canvas.

## Shapes

Use consistent rounded corners:

- Controls: `12px`.
- Floating cards and menus: `16px` when space allows.
- Structural panels: square edges unless a panel floats above content.

Rounded corners should indicate an interactive object or floating layer, not every container.

## Components

### Header

The header is a three-region grid, not a bag of controls.

- Left column: identity only, width equals `navigatorWidth`.
- Middle column: graph-affecting controls.
- Right column: inspector-aligned graph summary, API status, and inspector minimize/restore.
- Field labels sit above controls.
- Dropdown buttons show selected values only.
- Search is the dominant control and should receive the most horizontal space.
- Status belongs in the inspector column when it is visually paired with the right rail.
- Status pills must not sit directly above or below sidebar state buttons; the relationship is horizontal, with enough gap to scan both.

### Inspector

The inspector is a first-class layout region, not an overlay.

- The open inspector rail and the header inspector cell must share the same width.
- The collapsed inspector rail and the header restore button must share the same width.
- Minimize and restore controls live above the inspector rail so the user looks in one place for sidebar state.
- Selection details belong inside the inspector body; workspace graph summary belongs above the inspector.
- User minimization takes precedence over auto-open behavior. A new selection can reopen the inspector, but the same existing selection must not immediately reopen after minimize.

### Dropdowns

Dropdowns must separate field label from selected value.

Use:

```text
Perspective
[All Knowledge v]
```

Do not use:

```text
[Perspective
 All Knowledge v]
```

Menu contents should focus on choices and short descriptions. Do not repeat the trigger label unless the menu contains multiple sections and needs internal grouping.

### Graph Controls

Controls that alter graph representation should use user-facing labels:

- Use `Network Layout`, not `Force`.
- Use `Taxonomy Clusters`, not `Clustered`.
- Use `Circle Layout`, not `Circular`.

Technical names can remain in code and state. UI copy should describe user intent.

### Cards

Floating cards must align to the graph canvas grid. If a minimap and legend coexist, they share one alignment system and visual rhythm.

## Do's and Don'ts

Do:

- Establish the grid before placing controls.
- Align controls by region ownership.
- Keep hierarchy visible through position, spacing, and labels.
- Prefer fewer, clearer controls over dense icon-only clusters.
- Use copy that describes user intent rather than implementation mechanics.
- Preserve canonical IDs and source-backed detail in inspectors while using compact labels in navigation surfaces.

Don't:

- Put graph controls above the Navigator rail.
- Let dropdown trigger labels duplicate menu or button contents.
- Rely on icons alone for important graph operations.
- Float cards or overlays at arbitrary offsets.
- Hide layout decisions in ad hoc margins.
- Use color or glow to patch weak hierarchy.

## Agent Checklist

Before finishing UI work, verify:

- The component has an owning region.
- The component aligns to that region's grid.
- Labels are outside controls when the control value is the primary content.
- Menus open above canvas and in front of graph layers.
- Responsive wrapping preserves region ownership.
- UI copy is user-facing and not implementation jargon.
- The result was checked with at least one automated test or browser smoke when interaction/layering changed.
