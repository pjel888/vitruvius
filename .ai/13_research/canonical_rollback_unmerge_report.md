# Canonical Rollback and Unmerge Report

Date: 2026-05-01 23:08:42 +08:00

## Implemented rollback support

- GET /graph/canonical/decisions/:decisionId/rollback-preview
- POST /graph/canonical/decisions/:decisionId/rollback
- previewCanonicalRollback(...)
- ollbackCanonicalDecision(...)

## Full rollback support

Full rollback is supported for metadata-only decisions where the service created aliases, redirects, or decision status records and did not rewrite production graph nodes/edges.

Examples:
- alias decision rollback removes decision-linked alias records and marks the decision olled_back.
- keep-separate/reject/needs-review rollback marks decision state accordingly without graph mutation.

## Partial or blocked rollback

Destructive merge rollback is partial when affected edges or Resource Layer links exist. Current production merge application remains blocked for non-low-risk groups, and this loop did not perform production merges.

## Kimi review accepted

- Store rollback capability on decision records.
- Add schema version to before snapshots.
- Preserve duplicate alias records per decision to avoid later-decision alias loss.

## Kimi review deferred

- Alias/redirect tombstones instead of hard deletion.
- Full unmerge restoration for destructive graph edge rewrites.
- Concurrent rollback simulation.
- Dedicated partial-rollback remediation manifest file.

## Tests

Targeted API tests cover alias rollback, hash-chain validation after rollback, tampered manifest detection, and unsafe merge blocking.
