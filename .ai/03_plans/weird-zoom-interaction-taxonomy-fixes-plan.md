---
task: weird-zoom-interaction-taxonomy-fixes
phase: 05
author: PLANNER
created: 2026-04-30
supersedes: null
status: VALIDATED
---

# Implementation plan

## Goals
G001 Preserve selection across pan/select mode changes.
G002 Restrict selected-state dragging to the selected visible-edge neighborhood; outside clicks clear selection before new selection.
G003 Add hand/grab cursor behavior in pan mode.
G004 Make Zoom Extent focus the selected node when present, otherwise fit graph.
G005 Expand AEC-MEPFS child taxonomy descendants beyond first layer through bounded subtree expansion.
G006 Add clickable node breadcrumbs in the inspector.
G007 Make spread/child-orbit slider movement reversible.
G008 Add rights-safe metadata organization for architects, standards/laws, and architect-engineer overlaps.

## Plan critique
C001 Global vis-network drag settings do not directly support per-node dragging; use event guards and deselection rather than unsupported internals.
C002 Recursive expansion must be bounded to avoid huge graph additions.
C003 Enrichment code is already modified/untracked; edit minimally and verify no protected payloads or raw-source writes.

## Execution checklist
- [x] Add/adjust tests for G001, G005, G006, G007, G008.
- [x] Patch store and VisNetworkHost for G001-G004 and G007.
- [x] Patch API/client context expansion for G005.
- [x] Patch inspector breadcrumbs for G006.
- [x] Audit and minimally patch enrichment for G008.
- [x] Run targeted explorer/API/Python tests and build where feasible.
- [x] Write validation log.
