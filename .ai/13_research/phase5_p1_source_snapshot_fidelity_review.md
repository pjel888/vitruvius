# Phase 5 P1 Source Snapshot Fidelity Review

Date: 2026-05-03T02:15:00+08:00

## Problem Statement

All 20 P1 decision packets report:
- `groupInputHash is stale relative to current duplicate group state`
- `sourceSnapshot is stale relative to current graph/resource/canonical state`

These are **warnings**, not blockers. The validator reports `p1PacketsStaleSourceSnapshot: 20`.

## What Exactly Is Stale?

### `groupInputHash`

Computed as: `hash(stableStringify(compactGroupForSnapshot(group)))`

Where `compactGroupForSnapshot` includes:
- `groupId`
- `label` (loose normalized label)
- `nodeIds` (sorted)
- `priorityBand`

The hash changes whenever the group's label, node IDs, or priority band change. After the skeleton-shadow graph rebase, duplicate groups were rebuilt from the shadow graph, which may have slightly different node metadata than the original groups.

### `sourceSnapshot`

Computed as: `p1SourceSnapshotHash(buildP1SourceSnapshot(...))`

Where the snapshot includes aggregate hashes of:
- `nodesHash` — hash of `compactNodeForSnapshot` for all nodes
- `edgesHash` — hash of `compactEdgeForSnapshot` for all edges
- `groupsHash` — hash of `compactGroupForSnapshot` for all groups
- `resourcesHash`, `decisionsHash`, `approvalsHash`, etc.

The `compactNodeForSnapshot` function captures only:
```ts
{ id, label, type }
```

The `compactEdgeForSnapshot` function captures only:
```ts
{ id, source, target, type }
```

## Root Cause Analysis

### Is it stale relative to current graph state?

**Technically yes**: The validator rebuilds the snapshot from the current graph and compares the hash. If any node's label, any edge's endpoint, or any group's composition changed, the hash differs.

**Semantically no**: The packets were rebased against a skeleton shadow graph with minimal node metadata. The "staleness" is because:
1. The original packets were generated from a richer in-memory graph context
2. The rebase rebuilt them from the shadow staging artifact, which has fewer fields
3. The validator then compares against the shadow artifact, creating a circular mismatch

### Does it affect merge/admission safety?

**No.** The source snapshot is an "evidence lock" — it records the state of the graph at the time the packet was generated. The snapshot's purpose is:
1. Detect tampering (hash mismatch within the packet itself)
2. Allow auditors to reconstruct the context

The snapshot does **not** need to match the current graph state. A stale snapshot is expected after any graph mutation. The validator's warning is informational.

## Should Validator Wording Change?

**Recommendation: Yes, minor wording improvement.**

Current:
> "P1 decision packet {id} sourceSnapshot is stale relative to current graph/resource/canonical state"

Proposed:
> "P1 decision packet {id} sourceSnapshot was generated from a different graph context (expected after rebase or admission); snapshot integrity within packet is valid"

Similarly for `groupInputHash`:
> "P1 decision packet {id} groupInputHash reflects the duplicate group state at packet generation time; group may have changed since"

## Can the Snapshot Builder Include Richer Metadata?

**Yes, but not recommended in this loop.**

`compactNodeForSnapshot` could include:
- `path_code`
- `taxonomyPath`
- `level`
- `aliases`

`compactEdgeForSnapshot` could include:
- `semanticOverlayCategory`
- `rationale`

However, richer snapshots would:
1. Change the hash computation
2. Require all 20 packets to be regenerated
3. Trigger another rebase cycle
4. Potentially invalidate carried-forward reviews

## Would Richer Snapshots Require a New Rebase?

**Yes.** Changing `compactNodeForSnapshot` or `compactEdgeForSnapshot` changes the hash algorithm effectively. All packets would need new `sourceSnapshot` blocks, new `packetContentHash` values, and new review carry-forwards.

## Is This Worth Doing Now?

**No.** The current behavior is safe:
- Packet integrity is verified (`selfHash === packet.sourceSnapshot.snapshotHash`)
- No tampering is detected (`p1PacketsTamperedSourceSnapshot: 0`)
- Reviews are current (`p1PacketReviewStale: 0`)
- Content hashes match (`p1PacketsContentHashMismatch: 0`)

The "staleness" warnings are expected and non-blocking. Improving validator wording is a nice-to-have. Regenerating snapshots is unnecessary work with risk of review invalidation.

## Classification

| Question | Answer |
|----------|--------|
| Is this an acceptable warning? | **Yes** — expected after rebase/admission |
| Is it a validator wording issue? | **Partially** — wording could be clearer |
| Is it a real data-quality improvement opportunity? | **No** — snapshot fidelity is adequate for safety |
| Should we act now? | **No** — defer to future maintenance window |

## Recommended Action

1. **Do not mutate packet schemas in this loop.**
2. **Document the expected staleness** in this report (done).
3. **Optionally improve validator wording** in a future small PR.
4. **Queue for future maintenance**: If a P1 packet regeneration is ever needed for other reasons, upgrade `compactNodeForSnapshot` at that time.
