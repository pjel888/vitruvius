# P1 Decision Packet Generation Report

Date: 2026-05-02

## Summary

Generated 20 non-destructive P1 decision packets in `006_System-Manifests/graph-canonical/p1-decision-packets.json`. These packets are review-readiness artifacts only; they are not steward approvals, canonical admissions, aliases, redirects, tombstones, graph edge writes, or merge decisions.

## Counts

- P1 packets generated: 20
- Destructive P1 actions applied: 0
- Alias/redirect/tombstone writes: 0
- Production graph edge writes: 0
- Resource link rewrites: 0
- P1 packets missing source snapshot: 0
- P1 packets stale source snapshot: 0
- P1 packets tampered source snapshot: 0

## Evidence-locking added in the continuous loop

Each generated packet now includes:

- `truthCaveat`: `advisory_packet_only_not_steward_approval_not_canonical_admission`
- `sourceSnapshot.snapshotHash`
- `packetContentHash`
- `groupInputHash`
- `candidateEdgeNeighborhoodHash`
- Graph counts and hashes for nodes, edges, duplicate groups, resources, stewardship decisions, approvals, admitted relationships, aliases, redirects, tombstones, and priority overrides.

Validation now blocks packet content hash mismatches and source snapshot self-hash tampering. Stale source/group hashes are warnings for historical packets and should be treated as blockers before future admission decisions.

## Top packets

1. `dup-ca1078594013` ? building ? nodes `VTN-DOM-0000716`, `VTN-DOM-0000757` ? medium risk ? recommended `NEEDS_HUMAN_REVIEW`.
2. `dup-621135f7b4b9` ? load path ? nodes `VTN-DOM-0002932`, `VTN-DOM-0012160` ? high risk ? recommended `NEEDS_HUMAN_REVIEW`.
3. `dup-6400e3e0c204` ? shallow foundation ? nodes `VTN-DOM-0000261`, `VTN-DOM-0003010` ? medium risk ? recommended `DISAMBIGUATED_KEEP_SEPARATE`.
4. `dup-79f6cd2af6bf` ? wall finishe ? nodes `VTN-DOM-0000513`, `VTN-DOM-0003441`, `VTN-DOM-0012156` ? high risk ? recommended `NEEDS_HUMAN_REVIEW`.
5. `dup-a403cae6e1ea` ? mat foundation ? nodes `VTN-DOM-0000263`, `VTN-DOM-0003016`, `VTN-DOM-0012278` ? high risk ? recommended `NEEDS_HUMAN_REVIEW`.
6. `dup-5c6457d515c1` ? deep foundation ? recommended `DISAMBIGUATED_KEEP_SEPARATE`.
7. `dup-db832ee203d2` ? shear wall ? high risk ? recommended `NEEDS_HUMAN_REVIEW`.
8. `dup-b2f8807aa183` ? retaining wall ? high risk ? recommended `NEEDS_HUMAN_REVIEW`.
9. `dup-7a43f7bf68ed` ? door hardware usability ? recommended `DISAMBIGUATED_KEEP_SEPARATE`.
10. `dup-ffcce92d5e84` ? humidity resistant material ? recommended `DISAMBIGUATED_KEEP_SEPARATE`.

## Deferred

- Optional HMAC/signature for packet snapshots.
- Kimi review for each individual P1 packet.
- Human steward decisions for P1 groups.
- Source/resource custody snapshots beyond hashes of current local registries.
