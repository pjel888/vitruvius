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

`GET /v2/search` is an additive shadow route over staged BackboneNode labels,
path codes, and authored aliases. `GET /v2/sources/:source_id` is an additive
shadow route over staged source-rights metadata. Both routes read only
file-backed shadow artifacts and return sanitized preview payloads.

None of these routes read or write Neo4j, mount `/v2/resolve`, change feature
flags, rebuild the graph, ingest protected content, or make AEC-MEPFS the
Explorer default.

This project was created using `bun init` in bun v1.3.12. [Bun](https://bun.com) is a fast all-in-one JavaScript runtime.
