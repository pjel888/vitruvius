---
task: weird-zoom-interaction-taxonomy-fixes
phase: 03
created: 2026-04-30
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Research pack

## Discover
- `omx explore` launched for Explorer graph touchpoints.
- GitNexus query found `VisNetworkHost.tsx`, `GraphScene.tsx`, `ExplorerRail.tsx`, `api/index.ts`, and AEC-MEPFS enrichment scripts as primary touchpoints.
- GitNexus impact for indexed `applyGraphInteractionMode` and `loadGraph`: LOW risk, direct caller is the file, indirect imports from GraphScene and graph components.

## Findings
- Selection clearing is explicit in both store `setGraphInteractionMode('pan')` and `VisNetworkHost.applyGraphInteractionMode('pan')`.
- AEC-MEPFS expansion is one-hop in `buildAecMepfsExpandResult`.
- Fit/Zoom Extent always fits the whole graph, while `focusNode` already supports selected-node camera movement.
- Vis-network drag settings are global; selected-neighborhood-only drag requires a guard around drag start/end behavior.
- Child orbit/spread math supports scaling both ways, but physics restarts and zero-strength no-op behavior can make reversal appear broken.
