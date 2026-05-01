# KG-First Cleanup Implementation Context

## Task statement
Implement the Vitruvius KG-first cleanup plan safely, starting with Phase 1 live documentation reconciliation.

## Desired outcome
Live docs describe AEC-MEPFS/KG-first as current product direction while preserving old numbered layer paths as source custody, extraction staging, evidence preparation, compatibility, and provenance infrastructure.

## Constraints
- No Codex Spark / gpt-5.3-codex-spark / Spark-backed workers.
- Use Kimi CLI advisory passes only.
- Do not use OMX team if it cannot be forced to Kimi.
- No product behavior changes, API/Explorer changes, Neo4j/KG mutation, protected ingest, raw-source writes, numbered layer renames, or evidence deletion.
- Prefer docs-only before code-facing cleanup.

## Likely touchpoints
README.md, AGENTS.md, scripts/AGENTS.md, .ai live docs, roadmap docs, cleanup validation log.
