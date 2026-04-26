---
task: aec-mepfs-backbone
phase: readiness-api-explorer-parity
created: 2026-04-25
author: CODEX
status: EVIDENCE-EXPLORER-PREVIEWED
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
`GET /v2/backbone/taxonomy`, `GET /v2/backbone/node/:id`,
`GET /v2/backbone/placement-qa`, `GET /v2/backbone/evidence`,
`GET /v2/search`, and `GET /v2/sources/:source_id`. The remaining resolver
routes still require separate implementation packets, route-backed tests,
error/status semantics, ordering rules, trace semantics, and ID resolution
cases.

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
- `GET /v2/backbone/evidence` — implemented as compact file-backed evidence manifest summary
- `GET /v2/search` — implemented as sanitized file-backed BackboneNode metadata search
- `GET /v2/sources/:source_id` — implemented as sanitized file-backed source metadata preview
- `POST /v2/resolve`
- `GET /v2/resolve/trace/:trace_id`

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
- `GET /v2/backbone/placement-qa`
  - reads only the file-backed placement QA report
  - returns compact pass/fail counts, required coverage booleans, safety
    boundaries, and warnings
  - fails closed when the report is unavailable, not passing, or loses required
    coverage
  - does not return per-case source payloads, source text, primary graph data,
    or protected source content
- `GET /v2/backbone/evidence`
  - reads only the file-backed consolidated evidence manifest
  - returns compact manifest counts, safety invariants, evidence file labels,
    report paths, and repo-state metadata
  - fails closed when manifest safety invariants drift, artifact counts drift,
    preview route coverage drifts, reports are stale against the current API
    hash, or the newest manifest run is incomplete
  - validates raw input hashes but returns only an input-hash count; it does not
    expose raw input hashes, full report payloads, source rows, official URLs,
    blocking notes, source text, primary graph data, or protected source content
- `GET /v2/search`
  - reads only the shadow consumer report, staging artifact, and sibling shadow
    graph artifact
  - searches staged BackboneNode labels, preferred labels, path codes, and
    authored aliases
  - returns sanitized node result fields, match metadata, detail routes,
    boundary status, and artifact paths
  - fails closed when the graph artifact is unavailable and returns 400 for
    empty queries
  - does not return source rows, official URLs, blocking notes, source text,
    primary graph data, or protected source content
- `GET /v2/sources/:source_id`
  - reads only the shadow consumer report and staging artifact
  - resolves by source ID or source-family label
  - returns sanitized copyable source labels, evidence title, source-rights
    class, clearance state, currentness date, steward, update cadence, boundary
    status, and artifact paths
  - returns 404 for unknown source IDs and 400 for malformed escaped or blank
    decoded source IDs
  - does not return official URLs, blocking notes, intended-use prose, source
    text, primary graph data, or protected source content

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
- invalid source ID

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
- keep shadow Backbone previews behind explicit user action inside the
  non-default AEC-MEPFS preview until runtime cutover is separately authorized

## Pass / Fail Gate

Pass:

- v1 route contract tests pass unchanged
- `/v2` routes are additive and shadow-only
- Explorer can load current and Backbone perspectives without state collision
- Explorer shadow detail consumers remain explicit-action and do not replace
  the current graph state

Fail:

- v1 semantics change during shadow work
- legacy IDs become unresolved
- Explorer depends on `k_taxonomy_v2` before parity evidence
- `/v2/resolve` or `/v2/resolve/trace` is mounted before a separate accepted
  runtime packet
