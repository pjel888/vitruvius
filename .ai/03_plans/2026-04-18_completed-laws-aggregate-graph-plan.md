---
task: completed-laws-aggregate-graph
created: 2026-04-18
status: in_progress
---

# Plan — Aggregate completed-laws graph

1. generate one dataset manifest from the completed manifest index and completed-lanes ledger
2. validate that the aggregate manifest parses and keeps unique law-unit IDs
3. run aggregate `run-dataset-source-to-graph` dry-run and execute
4. record validation and add the aggregate manifest to the laws-wave artifact stack
