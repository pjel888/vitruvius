# P1 Packet Snapshot Rebase Report

Last updated: 2026-05-02T07:20:07Z

## Scope

This run refreshed/rebased the P1 decision-packet custody snapshots after the first steward-approved non-destructive graph admissions:

- Deep Foundations: `VTN-DOM-0000262` <-> `VTN-DOM-0003013` reciprocal `CROSS_DOMAIN_ALIGNMENT`.
- Shallow Foundations: `VTN-DOM-0000261` <-> `VTN-DOM-0003010` reciprocal `CROSS_DOMAIN_ALIGNMENT`.
- Buildings: metadata-only `DISAMBIGUATED_KEEP_SEPARATE`; no visible graph edge.

This rebase did not admit new graph edges, merge nodes, create aliases, create redirects, create tombstones, or mutate Resource Layer data.

## Baseline finding

Canonical validation after the steward-approved admissions reported 20 stale P1 packet source snapshots. The stale state was expected because packet snapshots include graph/canonical custody inputs, including approvals and admitted relationships, and those changed after the original P1 packet generation/review session.

## Implemented rebase semantics

- Packet IDs, group IDs, node IDs, truth caveats, and optional HMAC behavior are preserved.
- Current packet custody fields were refreshed against the current graph/canonical state:
  - `sourceSnapshot`
  - `sourceSnapshot.snapshotHash`
  - `packetContentHash`
  - `groupInputHash`
  - `candidateEdgeNeighborhoodHash`
  - signature metadata where applicable
- Review records remain historical and preserve the originally reviewed hashes.
- Reviews are carried forward only through explicit lineage fields and caveats; no new Kimi or human review was fabricated.
- Consumed/admitted packets now link to the specific approval, decision, and admitted relationship records that consumed them.
- The rebase is transaction-manifested as `canonical-tx-20260502070159-8fa772391342`.

## Rebase metrics

- P1 packets refreshed: 20
- P1 packets changed: 20
- Review records preserved: 8
- Review records carried forward: 8
- Stale review records after rebase: 0
- Invalid review records after rebase: 0
- P1 packets consumed by relationship admission: 2
- P1 packets consumed by metadata-only disambiguation: 1
- P1 packets still unreviewed: 12
- P1 packet signatures: 0 signed / 20 unsigned / 0 invalid
- Latest manifest afterHash mismatches: 0

## Consumed packet status

### Deep Foundations

- Packet: `p1-decision-packet-8a66e785d02a`
- Status: `consumed_by_non_destructive_admission`
- Approval: `canonical-approval-20260502055659-b9a6f6b671e2`
- Admitted relationships:
  - `VTN-DOM-0000262--cross_domain_alignment--VTN-DOM-0003013`
  - `VTN-DOM-0003013--cross_domain_alignment--VTN-DOM-0000262`
- Review: prior Kimi review carried forward with custody-rebase caveat.

### Shallow Foundations

- Packet: `p1-decision-packet-d5a20759fdfd`
- Status: `consumed_by_non_destructive_admission`
- Approval: `canonical-approval-20260502055700-0109b1ea4688`
- Admitted relationships:
  - `VTN-DOM-0000261--cross_domain_alignment--VTN-DOM-0003010`
  - `VTN-DOM-0003010--cross_domain_alignment--VTN-DOM-0000261`
- Review: prior Kimi review carried forward with custody-rebase caveat.

### Buildings

- Packet: `p1-decision-packet-fee6fbd9a0fc`
- Status: `metadata_disambiguation_admitted`
- Approval: `canonical-approval-20260502055700-65171a76c4e6`
- Decision: `canonical-20260502055700-8e92ff2fc366`
- Admitted relationships: none
- Review: prior Kimi review carried forward with custody-rebase caveat.

## HMAC/signature behavior

No `VITRUVIUS_PACKET_HMAC_KEY` was configured. Refreshed packets remain unsigned in non-strict mode. Non-strict validation warns only. Strict packet-signature smoke validation failed as expected with 20 blockers because no key is configured.

## Graph visibility validation

Direct API checks confirmed the admitted alignment edges are visible in selected-node neighborhoods:

- `VTN-DOM-0000262` includes `VTN-DOM-0003013` and `CROSS_DOMAIN_ALIGNMENT`.
- `VTN-DOM-0003013` includes `VTN-DOM-0000262` and `CROSS_DOMAIN_ALIGNMENT`.
- `VTN-DOM-0000261` includes `VTN-DOM-0003010` and `CROSS_DOMAIN_ALIGNMENT`.
- `VTN-DOM-0003010` includes `VTN-DOM-0000261` and `CROSS_DOMAIN_ALIGNMENT`.
- Explorer graph payload includes 4 `CROSS_DOMAIN_ALIGNMENT` edges.

Buildings remains metadata-only; no visible Buildings graph edge was admitted.

## Validation summary

- `bun run api/validateCanonicalGraphStewardship.ts`: passed.
- Strict packet-signature smoke without key: failed as expected with 20 blockers.
- Strict latest-afterHash validation: passed.
- `bun run api/validateGraphRelationships.ts`: passed; 10,018 nodes, 13,674 effective edges, issue count 0.
- `bun run api/validateResourceLayer.ts`: passed with known ASCE 7 / ACI 318 context warnings.
- `cd api && bun test`: passed, 173 tests.
- `cd explorer && bun test`: passed, 112 tests.
- `cd explorer && bun run build`: passed with known Vite chunk-size warning.
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py`: passed, 108 tests.

## Kimi review summary

Accepted Kimi suggestions: keep old review hashes as historical evidence, add explicit carry-forward lineage, link consumed packets to specific approval/admission records, do not carry old HMAC signatures, avoid wording that implies re-review/truth/merge/source authority.

Rejected Kimi risks: fake re-review, broad blanket approval, carrying old signatures forward, implying merge/alias/tombstone/source truth, or reopening consumed packets as active duplicate work.

Deferred Kimi suggestions: fresh Kimi re-review of packets, HMAC-signed regeneration until a real key exists, and broader P1 triage/admission after this custody rebase.

## Confirmation

- No graph mutation occurred in this rebase task.
- No Resource Layer mutation occurred.
- No merge, alias, redirect, or tombstone occurred.
- P0 Concrete/Reinforced Concrete remain high-risk unresolved groups.

## Exact next action

Continue remaining P1 review/admission work: review 3 to 5 additional unreviewed P1 packets with Kimi, then prepare/admit only low/medium-risk non-destructive candidates whose dry-run, validation, rollback, and visibility checks pass.
