---
task: aec-mepfs-backbone
phase: readiness-api-explorer-parity
created: 2026-04-25
author: CODEX
status: NODE-SHADOW-ROUTE-IMPLEMENTED
---

# API / Explorer Parity Contract

## Purpose

Define what current API and Explorer behavior must preserve while the Backbone is
built in shadow form.

No API or Explorer implementation is authorized by this contract unless a
separate bounded implementation packet is opened.

Accepted-readiness scope: v1 preservation, additive `/v2` shadow routes, parity
query categories, and Explorer label/edge requirements are accepted as consumer
controls. `AEC-BB-S4` adds file-backed parity cases and a runner report for the
accepted categories. Route-backed assertions now exist for `GET /v2/backbone`,
`GET /v2/backbone/taxonomy`, `GET /v2/backbone/node/:id`, and
`GET /v2/backbone/placement-qa`; the remaining `/v2` routes still require
separate implementation packets, route-backed tests, error/status semantics,
ordering rules, and ID resolution cases.

## V1 Preservation Surface

These routes must remain behaviorally compatible until cutover:

- `GET /search`
- `GET /node/:id`
- `GET /taxonomy`
- `GET /perspectives`
- `GET /perspective/:id/nodes`

V1 may receive additive fields only. Existing response semantics, IDs, and
perspective behavior must continue to support the current 001-Laws Explorer MVP.

## Future V2 Surface

Future shadow routes:

- `GET /v2/backbone` — implemented as compact file-backed summary only
- `GET /v2/backbone/taxonomy` — implemented as sanitized file-backed taxonomy and shadow graph preview
- `GET /v2/backbone/node/:id` — implemented as sanitized file-backed node and immediate relationship preview
- `GET /v2/backbone/placement-qa` — implemented as compact file-backed placement QA summary
- `GET /v2/search`
- `POST /v2/resolve`
- `GET /v2/resolve/trace/:trace_id`
- `GET /v2/sources/:source_id`

The `/v2` surface reads shadow backbone data only until parity and rollback
evidence pass.

Current implemented route:

- `GET /v2/backbone`
  - reads
    `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260425T154000Z/shadow-staging-consumer-report.json`
  - returns counts, boundary status, no-ingest coverage, and artifact paths
  - does not return full registry rows, source text, primary graph data, or
    protected source content
- `GET /v2/backbone/node/:id`
  - reads only the shadow consumer report, staging artifact, and sibling shadow
    graph artifact
  - resolves by VTN ID, canonical ID, or path code
  - returns sanitized node fields, immediate relationships, relationship counts,
    boundary status, and artifact paths
  - fails closed when the graph artifact is unavailable and returns 400 for
    malformed escaped IDs
  - does not return source rows, official URLs, blocking notes, source text,
    primary graph data, or protected source content

## Parity Query Set

Minimum parity report categories:

- search by known concept label
- search by alias/deprecated label
- direct node lookup by legacy ID
- direct node lookup by VTN ID
- taxonomy navigation root
- perspective load for default/concepts/taxonomy/evidence/regulatory
- source/evidence display
- edge provenance display
- empty/no-match result
- invalid node ID

The S4 file-backed fixture for these categories is
`scripts/tests/fixtures/aec_mepfs_backbone/api-explorer-parity-cases.json`.
It is readiness evidence, not a substitute for later route-backed `/v2`
runtime parity once those routes exist.

## Explorer Requirements

The future Backbone perspective must:

- display user-facing labels, not document slugs
- keep source labels copyable even when visually truncated
- separate canonical label, display label, source label, and evidence title
- render typed edge families distinctly
- expose conflict/review-state edges as review state, not graph truth
- keep current graph controls and node-inspector workflows working

## Pass / Fail Gate

Pass:

- v1 route contract tests pass unchanged
- `/v2` routes are additive and shadow-only
- Explorer can load current and Backbone perspectives without state collision

Fail:

- v1 semantics change during shadow work
- legacy IDs become unresolved
- Explorer depends on `k_taxonomy_v2` before parity evidence
