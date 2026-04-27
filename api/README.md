# api

To install dependencies:

```bash
bun install
```

To run:

```bash
bun run index.ts
```

To test:

```bash
bun test
```

The API fronts Neo4j for explorer workflows and now persists saved scenes in `api/.data/scenes.json`.

## Shadow Backbone Route

`GET /v2/backbone` is an additive, read-only shadow route. It reads the
file-backed AEC-MEPFS Backbone consumer report and returns a compact summary
only.

`GET /v2/backbone/taxonomy` is the next bounded shadow route. It validates the
same consumer report, resolves the referenced staging artifact inside the
shadow-staging directory, and returns sanitized predicate/source-rights registry
metadata plus staged admitted `BackboneNode` metadata when present. When the
consumer report references `shadow-backbone-graph.json`, the route also returns
sanitized shadow graph counts and hierarchy edge previews after validating the
graph schema, run id, source artifact, count parity, and edge endpoints. This
is for readiness preview only. It does not expose standards text, raw examples,
official URLs, blocking notes, or protected source content.

`GET /v2/backbone/placement-qa` is an additive shadow route over the
file-backed placement QA report. `GET /v2/backbone/evidence` is an additive
shadow route over the consolidated file-backed evidence manifest. Both routes
return compact, sanitized summaries and fail closed on unsafe or stale evidence.
The evidence preview distinguishes source-tree dirtiness from generated
evidence dirtiness, reports legacy freshness fields as unknown, and fails closed
when refreshed evidence explicitly reports source-tree dirtiness.

`GET /v2/search` is an additive shadow route over staged BackboneNode labels,
path codes, and authored aliases. `GET /v2/sources/:source_id` is an additive
shadow route over staged source-rights metadata. Both routes read only
file-backed shadow artifacts and return sanitized preview payloads.

`POST /v2/resolve` and `GET /v2/resolve/trace/:trace_id` are a separate
default-off AEC-MEPFS resolver surface. They are mounted only when
`VITRUVIUS_AEC_MEPFS_RESOLVER_RUNTIME` is explicitly enabled. The current
implementation is file-backed over non-protected resolver fixtures, exposes
only canonical IDs/source IDs/safe rationale, and does not read or write Neo4j,
rebuild the graph, ingest protected content, claim runtime thresholds, or make
AEC-MEPFS the Explorer default.

None of the shadow preview routes read or write Neo4j, change default-on feature
flags, rebuild the graph, ingest protected content, or make AEC-MEPFS the
Explorer default.

This project was created using `bun init` in bun v1.3.12. [Bun](https://bun.com) is a fast all-in-one JavaScript runtime.
