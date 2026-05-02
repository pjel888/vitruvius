# Continuous Vitruvius Quality Report

Last updated: 2026-05-02T09:31:05+0800

## Quality gate status

| Gate | Status | Notes |
| --- | --- | --- |
| Graph edge integrity | Passed | Graph validation found no broken edge references. |
| Relationship visibility | Passed | Sendai Mediatheque/Toyo Ito regression remains covered by validation/tests. |
| Resource Layer integrity | Passed with warnings | No blockers/errors; known ACI/ASCE context warnings remain honest. |
| Canonical validation | Passed | P1 snapshot counts are clean; no approval/admission was fabricated. |
| P0 Concrete | Blocked/pending | Needs real steward approval before admission. |
| P1 packet readiness | Improved | 20 packets now include source snapshots and content hashes. |
| Production mutation safety | Preserved | No merge, alias, redirect, tombstone, admitted edge, or resource rewrite was applied. |
| Dirty worktree scope | Critical risk remains | GitNexus detect-changes reports critical risk across 34 files, 223 symbols, and 28 affected processes from the broad dirty worktree. |

## New quality checks added

- Missing P1 packet source snapshot is surfaced as validation warning.
- Stale P1 source snapshot or group input hash is surfaced as validation warning.
- Tampered source snapshot self-hash is a blocker.
- Packet content hash mismatch is a blocker.
- Inconsistent source snapshot hashes inside one packet run are a blocker.

## Caveats

- Packet hashes are tamper-evident integrity aids, not proof of ontology truth and not cryptographic authentication without future HMAC/signature support.
- P1 packets remain advisory review artifacts and do not represent steward approval or canonical admission.
