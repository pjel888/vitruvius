---
task: aec-mepfs-backbone
phase: readiness-api-explorer-parity
created: 2026-04-25
author: CODEX
status: ACCEPTED-READINESS-CONTROL
---

# API / Explorer Parity Contract

## Purpose

Define what current API and Explorer behavior must preserve while the Backbone is
built in shadow form.

No API or Explorer implementation is authorized by this contract.

Accepted-readiness scope: v1 preservation, additive `/v2` shadow routes, parity
query categories, and Explorer label/edge requirements are accepted as consumer
controls. Runtime implementation remains blocked until exact fixtures,
response-shape assertions, error/status semantics, ordering rules, and ID
resolution cases are executable.

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

- `GET /v2/backbone`
- `GET /v2/backbone/node/:id`
- `GET /v2/search`
- `POST /v2/resolve`
- `GET /v2/resolve/trace/:trace_id`
- `GET /v2/sources/:source_id`

The `/v2` surface reads shadow backbone data only until parity and rollback
evidence pass.

## Parity Query Set

Minimum later parity report must cover:

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
