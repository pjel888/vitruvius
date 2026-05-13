# AEC Explorer Overlay UX Context

Created: 2026-05-13T05:11:55Z

## Request

Improve the Explorer experience so the relationship-improvement and node-consolidation campaign results are easier to inspect and use without mutating the active graph.

## Current Observations

- Run `aec_backbone_all_nodes_bounded_004` completed and produced pending-only overlay artifacts.
- Explorer overlay API already exposes approved relationship overlays, needs-evidence relationship overlays, alias-approved node consolidations, and node consolidations needing evidence.
- Existing Explorer preview shows aggregate counts, but the operator cannot quickly filter overlay edge states or inspect provenance/provider details in the edge inspector.
- The active graph admission boundary remains blocked; only pending overlay visualization and review artifacts are in scope.

## Scope

- Add Explorer overlay legend and quick filters.
- Expose richer overlay metadata from the API edge objects.
- Improve edge inspector for pending overlay edges.
- Add concise campaign and use-case documentation, including RA9266/version-control and materials-maintenance examples.
- Preserve pending-only behavior and do not write Neo4j/Postgres or active graph files.

## Verification Targets

- API tests for overlay metadata.
- Explorer tests for preview/filter/inspector behavior where practical.
- Type/build or focused frontend tests.
- No secrets or reasoning content added to committed docs or UI fixtures.
