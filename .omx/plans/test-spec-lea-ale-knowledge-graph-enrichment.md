# Test Spec — LEA/ALE Knowledge Graph Enrichment

- **Created:** 2026-04-29T08:40:24Z
- **Status:** active

## Required validation
- Python compile check for modified enrichment scripts/tests.
- Focused LEA/ALE enrichment unit test for idempotency, count minimums, alias/source-rights guarantees, no protected payload fields, and category relationship coverage.
- Backbone contract validation and count expectation updates.
- Broad/architecture enrichment compatibility tests.
- Shadow staging generation and shadow consumer report validation.
- API backbone test: `cd api && bun test v2Backbone.test.ts`.
- JSON validation for modified JSON artifacts and registries.
- Duplicate ID/path and orphan checks where supported by contracts.
- Safety grep for exam questions, answer keys, protected clauses/tables/reviewer payloads, live Neo4j promotion, destructive operations, and active Codex Spark routing.
- Kimi final read-only review.
- GitNexus status/update after commits or major index-sensitive changes.
