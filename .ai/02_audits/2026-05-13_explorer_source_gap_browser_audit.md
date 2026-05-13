# Explorer Source-Gap Browser Audit - 2026-05-13

## Current State

The source-gap workqueue has a safe API preview and a selected-node panel, but Explorer lacks a graph-wide triage surface. Operators can only see source gaps after navigating to a node that happens to have matching workqueue rows.

## Gap

For source-grounding work to be actionable, Explorer needs a global workqueue preview in the left rail:

- total workqueue count;
- returned graph-wide items;
- node-resource gap count;
- relationship-source gap count;
- source-link proposal count;
- top ranked items with proposed resource labels;
- explicit no-write boundaries.

## Safety Assessment

The new browser must remain read-only and must not:

- create Resource Layer links;
- admit source claims;
- admit pending relationship or node-consolidation overlays;
- write active graph files;
- call Neo4j or Postgres;
- include protected source text.

The existing API preview already provides safety boundary booleans and sanitized proposal metadata, so the Explorer work can consume that contract directly.

## Implementation Recommendation

Add a lazy-loaded "Source gaps" section to `BackbonePreviewPanel`, wired through `ExplorerRail` with the same request-id pattern used by the existing preview sections.
