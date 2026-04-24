# Explorer Shell Layout Cleanup Validation

**Date:** 2026-04-24
**Plan:** `.ai/03_plans/2026-04-24_explorer_shell_layout_cleanup_plan.md`
**Audit:** `.ai/02_audits/2026-04-24_explorer_shell_layout_ux_audit.md`

## Scope

Validated Explorer shell layout changes only. Knowledge graph rendering internals were not included except for removing duplicated chrome outside the graph canvas.

## Verification

- `npx gitnexus impact --repo vitruvius --direction upstream InspectorRail`
  - Result: `LOW`, `0` impacted upstream symbols.
- `npx gitnexus impact --repo vitruvius --direction upstream CommandBar`
  - Result: `LOW`, `0` impacted upstream symbols.
- `npx gitnexus impact --repo vitruvius --direction upstream GraphScene`
  - Result: `LOW`, `0` impacted upstream symbols.
- `bunx eslint src/components/CommandBar.tsx src/components/InspectorRail.tsx src/components/GraphScene.tsx src/components/command-bar/PerspectiveSwitcher.tsx src/components/command-bar/SceneMenu.tsx src/components/graph/LayoutMenu.tsx src/components/graph/layoutOptions.ts src/app.searchInspector.integration.test.tsx src/components/componentInteraction.test.tsx`
  - Result: pass.
- `bun test src/app.searchInspector.integration.test.tsx src/components/componentInteraction.test.tsx`
  - Result: `14 pass`, `0 fail`, `62 expect()` calls.
- `bun run build`
  - Result: pass with existing `vis-network` chunk-size warning.
- `npx @google/design.md lint .ai/00_system/DESIGN.md`
  - Result: `0` errors, `5` unused-token warnings.
- `git diff --check`
  - Result: pass.

## Known Non-Blocking Issue

- Full `bun run lint` still fails on `explorer/src/components/graph/VisNetworkHost.tsx:152` with `react-refresh/only-export-components`.
- This file is part of a separate dirty worktree lane and was not changed by this cleanup pass.

## Outcome

- Inspector minimize now persists for the active selection.
- Selecting a different node or edge still reopens the inspector.
- Inspector summary/status/toggle now align with the right rail.
- Neo4j/API status pill is horizontally grouped with the sidebar state control and no longer sits underneath the icon.
