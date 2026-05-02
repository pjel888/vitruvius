# Canonical Operations Loop Progress

Date: 2026-05-01 23:08:42 +08:00

## Intent

Operationalize canonical graph stewardship without broad automatic duplicate cleanup. This loop focuses on scalable review, priority ordering, batch triage, rollback preview/apply, hash-chained manifests, stronger mutation gates, and concrete decision packets.

## Acceptance criteria in progress

- Dirty worktree/change-scope report: complete.
- Duplicate priorities: implemented in pi/graph/canonicalStewardship.ts and exposed by /graph/canonical/priorities.
- Batch review: implemented with file-backed batch records and non-destructive API routes.
- Concrete/Reinforced Concrete decision packet: drafted in this loop; no production merge applied.
- Rollback/unmerge: implemented for metadata decisions; destructive merge rollback remains partial/blocked by policy.
- Manifest integrity: canonical and Resource Layer manifests now include hash-chain metadata and optional HMAC signatures.
- Admin/mutation gate: production mutation requires token or local/dev gate.
- Search ambiguity: canonical search reports unresolved duplicate group ambiguity for matching nodes.
- Tests/validation: targeted tests pass; full suite pending at time of this progress update.

## Current baseline from validation

- Duplicate groups: 544
- Unresolved duplicate groups: 544
- Groups by risk: high=69, medium=475
- Groups by priority: P0=2, P1=66, P2=223, P3=253
- Concrete duplicate groups: 2
- Applied decisions: 0
- Aliases: 0
- Redirects: 0
- Batches: 0 production records
- Transaction manifests: 0 production canonical manifests

## Safety notes

- No production duplicate merge was applied.
- No production alias/redirect was applied.
- No Resource Layer records were auto-promoted.
- No local files were auto-linked.
- Batch merge is blocked server-side.
