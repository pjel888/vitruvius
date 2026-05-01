# PRD - Weird zoom interaction taxonomy fixes

## Problem
Explorer graph navigation currently loses selection during pan/select transitions, allows dragging irrelevant nodes while a selected-neighborhood focus is active, expands taxonomy nodes only one hop, lacks clickable breadcrumbs, and has spread-slider reversibility problems. The AEC-MEPFS content graph also needs richer metadata organization for architect nationality, standards/laws families, country/local/international law groupings, and architect-engineer overlaps.

## Goals
1. Preserve selection across select to pan to select mode changes.
2. Make pan mode visibly hand-like and non-selecting.
3. When a node is selected, treat selection as a temporary focused neighborhood: dragging outside the selected node/neighborhood clears selection first instead of moving an unrelated node.
4. Add selected-node Zoom Extent behavior using the existing camera control.
5. Expand AEC-MEPFS taxonomy child trees beyond immediate children using a bounded subtree expansion.
6. Add node breadcrumbs for easier navigation.
7. Ensure spread slider changes are reversible in both loose-to-tight and tight-to-loose directions.
8. Add rights-safe graph organization for architects by nationality, laws/standards by authority/country/scope, and stronger architect-engineer relationships.

## Non-goals
- No production Neo4j mutation, KG rebuild/reload/reset, raw-source writes, protected payload ingest, or destructive graph operation.
- No new dependencies.

## Acceptance criteria
- Explorer tests cover interaction-mode selection preservation and spread bounds.
- API tests cover bounded AEC-MEPFS expand subtree behavior.
- Breadcrumb UI test covers clickable taxonomy breadcrumbs.
- Enrichment tests cover nationality, standards/laws classification, and architect-engineer strengthening if data code is changed.
- Build/test/lint or targeted equivalents pass with fresh output.
