---
task: aec-mepfs-backbone
phase: shadow-v2-api-read-route-planning
created: 2026-04-25
author: CODEX
status: READ-PREVIEWS-IMPLEMENTED-RESOLVER-BLOCKED
---

# Shadow V2 API Read Route Planning Packet

## Purpose

Plan the next possible `/v2` read route after the read-only shadow staging
consumer report is validated.

This was planning-only until separate implementation packets were opened.
`third-shadow-v2-backbone-route-implementation-packet.md` authorizes and
implements only `GET /v2/backbone`. The later
`fourteenth-shadow-node-preview-route-implementation-packet.md` authorizes and
implements only `GET /v2/backbone/node/:id`. The later
`fifteenth-shadow-search-preview-route-implementation-packet.md` authorizes and
implements only `GET /v2/search`. The later
`sixteenth-shadow-source-preview-route-implementation-packet.md` authorizes and
implements only `GET /v2/sources/:source_id`. Explorer adoption, feature flags,
Neo4j writes, primary graph promotion, and protected source ingest remain
blocked.

## Proposed Future Slice

The future slice may add a shadow-only `/v2` read route only if the consumer
report remains passing and a fresh impact review confirms the API surface can be
touched without changing v1 semantics.

Candidate routes from the accepted parity contract remain:

- `GET /v2/backbone` - implemented by the third shadow route packet
- `GET /v2/backbone/node/:id` - implemented by the fourteenth shadow route packet
- `GET /v2/search` - implemented by the fifteenth shadow route packet
- `GET /v2/sources/:source_id` - implemented by the sixteenth shadow route packet
- `POST /v2/resolve`
- `GET /v2/resolve/trace/:trace_id`

The first route is the smallest read-only file-backed route:
`GET /v2/backbone`, returning a summary shape derived from
`shadow-staging-consumer-report.json`.

## Required Boundaries

The route must:

- read only file-backed shadow artifacts
- return additive `/v2` responses only
- preserve all v1 route behavior
- expose no protected source text, tables, figures, clauses, or dataset content
- keep source use at reference/metadata level only
- fail closed if the consumer report is missing, failed, or declares runtime
  boundary violations
- remain disabled from default Explorer consumption until parity evidence exists

The route must not:

- write to Neo4j
- read from or mutate primary graph labels
- run graph rebuild/reset/cleanup
- edit `CanonicalNode`, `TaxonomyLoader`, `Neo4jLoader`, or
  `UnifiedSnapshotBuilder`
- flip feature flags or make Explorer use `/v2` by default

## Pre-Implementation Gates

Before route implementation:

1. Consumer report generated for the real `20260425T154000Z` staging run and
   passing.
2. API impact review completed for the exact route files and route helpers.
3. v1 API tests pass before and after the route addition.
4. `/v2` response-shape tests are written before implementation.
5. Explorer tests remain unchanged unless a separate Explorer packet is opened.
6. Read-only graph smoke still reports zero `BackboneShadow` nodes in Neo4j.

## Acceptance Shape

The future first route should return a compact object with:

- schema version
- run ID
- report status
- predicate/source counts
- boundary status
- no-ingest boundary coverage
- report artifact paths

It should not return full protected source payloads or any content copied from
external standards/legal sources.

## Current Decision

`GET /v2/backbone` is implemented by the separate third packet.
`GET /v2/backbone/node/:id` is implemented by the separate fourteenth packet.
`GET /v2/search` is implemented by the separate fifteenth packet.
`GET /v2/sources/:source_id` is implemented by the separate sixteenth packet.
`GET /v2/backbone/placement-qa` is implemented by the separate tenth packet.
`GET /v2/backbone/evidence` is implemented by the separate twenty-third
packet, and the twenty-fifth packet adds explicit-action Explorer consumption
of that evidence summary.

Do not implement the remaining resolver `/v2` routes without a new packet,
route-shape tests, fresh API impact review, and v1 preservation evidence.
