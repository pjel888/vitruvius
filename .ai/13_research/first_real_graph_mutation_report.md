# First Real Graph Mutation Report

Date: 2026-05-02T06:03:16Z

This is the first run that created active production/file-backed graph relationship overlay records under canonical stewardship.

## Mutation type

- Non-destructive admitted relationship overlay: yes, 4 active edges.
- Metadata-only governed disambiguation: yes, Buildings.
- Base shadow graph row rewrite: no.
- Node mutation: no.
- Resource Layer mutation: no.
- Merge/alias/redirect/tombstone: no.

## Effective graph counts

- Nodes: 10018
- Base graph edges: 13670
- Active admitted stewardship overlay edges: 4
- Effective graph edges served by API/validation overlay: 13674

## Rollback

Each decision exposes rollback preview through `GET /graph/canonical/decisions/:decisionId/rollback-preview`; rollback marks scoped approvals/admitted relationships rolled back through the existing canonical rollback transaction flow.

## Post-Kimi implementation-safety repair (2026-05-02T06:20:00Z)

Kimi's final implementation-safety review was accepted. Before commit, the run repaired two custody issues:

- Approval records for Deep Foundations, Shallow Foundations, and Buildings now contain revalidated embedded snapshots with `ok: true` and no embedded false blocker snapshots.
- Buildings remains a metadata-only `DISAMBIGUATED_KEEP_SEPARATE` / governed-disambiguation decision; latent `CROSS_DOMAIN_ALIGNMENT` relationship proposals were cleared and no Buildings graph edge was admitted.
- A new `canonical_approval_metadata_revalidation` transaction manifest (`canonical-tx-20260502061917-f0d21c4f7013`) records the approval/decision metadata repair.
- Current canonical validation: blockers 0; approvals 3; admitted relationships 4; transaction manifests 30; latest afterHash mismatches 0.

Accepted Kimi suggestions: repair failed embedded validation snapshots; remove latent Buildings edge proposals; isolate commit scope. Rejected: none. Deferred: P1 packet custody snapshot refresh after admitted canonical state.
