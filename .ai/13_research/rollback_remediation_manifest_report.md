# Rollback Remediation Manifest Report

Date: 2026-05-01

## Outcome

Partial rollback remediation manifest support was added, but no production remediation manifest was created because this loop performed no destructive or partial rollback operation.

## Model

A remediation manifest records:

- remediationManifestId,
- decisionId,
- rollbackId,
- rollbackCapability (`full`, `partial`, `blocked`, `unsupported`),
- affected nodes, edges, Resource Layer links, aliases, redirects, and tombstones,
- unresolved restoration tasks,
- recommended manual steps,
- validation warnings,
- reviewer,
- status (`open`, `in_progress`, `resolved`, `waived`),
- resolution notes.

## API/UI

Added read/update support:

- `GET /graph/canonical/remediation`
- `GET /graph/canonical/remediation/:id`
- `POST /graph/canonical/remediation/:id/status`

`/dev/canonical-review` now displays remediation manifests and allows status updates through the same mutation gate.

## Validation

Canonical validation now reports open remediation manifests and partial rollback decisions lacking remediation. Current state: `openRemediationManifests: 0`, `remediationManifestCount: 0`, `partialRollbackDecisionsWithoutRemediation: 0`.

## Deferred

Run a future rollback/replay drill with a controlled fixture before permitting high-risk production merge rollback workflows.
