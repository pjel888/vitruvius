# AEC-MEPFS Neo4j Live-Promotion Readiness Packet

```yaml
status: BOUNDARY_APPROVED_PREP_ONLY
created: 2026-04-27
authority: project-owner-directive-four-gated-lanes
lane: neo4j-isolated-rehearsal-live-promotion-path
classification: GREEN_LIVE_PROMOTION_PREPARATION_ONLY
production_live_promotion_authorized: false
primary_graph_replacement_authorized: false
```

## Purpose

Define the exact live-promotion gates that must be satisfied after isolated
rehearsal validation and before any primary/live Neo4j graph replacement.

## Live-promotion prerequisites

All must be true before live promotion can be considered:

1. Dedicated live-promotion packet names the exact database/namespace, source
   artifact, command transcript, and rollback owner.
2. Fresh live backup/export is executed and its artifact path is recorded.
3. Restore proof is executed against an isolated/stopped target before promotion.
4. Pre-promotion and post-restore graph-count diff commands are recorded.
5. Shadow namespace/database load succeeds without protected content ingest.
6. API/Explorer parity evidence is fresh for the graph surface to be promoted.
7. Protected source admission remains metadata-only or has source-specific legal
   authority for any payloads.
8. Rollback transcript is written before mutation.
9. Production destructive commands are listed and reviewed before execution.
10. Scoped live-promotion authorization is recorded for the named surface only.

## Explicitly blocked

- Broad/global `LIVE_RUNTIME_AUTHORIZED`.
- Destructive production reset without fresh backup/restore proof.
- Primary namespace replacement without a rollback transcript.
- KG rebuild/reload/reset affecting primary graph without a dedicated packet.
- Protected content ingest or payload exposure.

## Current status

The current repo state validates isolated dump/load rehearsal but does not yet
satisfy live-promotion prerequisites. Production live promotion remains blocked.
