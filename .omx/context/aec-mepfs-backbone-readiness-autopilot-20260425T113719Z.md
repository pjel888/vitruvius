# Autopilot Context Snapshot

Task statement:

- Continue autonomously until the AEC-MEPFS Backbone is ready to be implemented.

Desired outcome:

- Close every local, non-destructive readiness gate that can be closed before
  runtime implementation.
- Produce executable evidence for the next missing gate without wiring runtime
  KG, Neo4j, API, Explorer, feature flags, or canonical source admission.

Known facts/evidence:

- Latest pushed commit is `aa34e80d`.
- S1/S2/S3 readiness validator slices are implemented and validated.
- The current scorecard says the full runtime Backbone is not ready.
- The next local implementable slice is `AEC-BB-S4`: a report-producing
  API/Explorer parity runner.
- Existing `explorer/package.json` is dirty and unrelated; do not stage it.

Constraints:

- No Neo4j writes, graph rebuild, backup/restore, cleanup/reset, or flag flips.
- No edits to `CanonicalNode`, `TaxonomyLoader`, `UnifiedSnapshotBuilder`, or
  `Neo4jLoader`.
- No protected source-text ingest and no production canonical backbone admission.
- Use standard-library Python where possible; no new dependency without need.
- Commit and push completed readiness slices with Lore commit trailers.

Unknowns/open questions:

- Legal/licensing clearance cannot be completed by code.
- Executed rollback proof likely requires a separate safe Neo4j environment
  because `neo4j-admin database dump` cannot dump a mounted database.
- Production registry admission requires steward/legal decisions, not only code.

Likely codebase touchpoints:

- `scripts/vitruvius/kg/backbone_contracts.py`
- new file-backed parity runner under `scripts/vitruvius/kg/`
- focused tests under `scripts/tests/`
- fixtures under `scripts/tests/fixtures/aec_mepfs_backbone/`
- AEC-MEPFS readiness docs under `.ai/03_plans/AEC-MEPFS-Backbone/`
- validation logs under `.ai/05_logs/`
