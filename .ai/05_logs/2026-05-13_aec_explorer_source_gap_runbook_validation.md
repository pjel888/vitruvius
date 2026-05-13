# AEC Explorer Source-Gap Runbook Validation â€” 2026-05-13

## Scope

Updated `docs/knowledge-graph/aec-explorer-overlay-campaigns.md` to document Explorer review steps for pending overlays and source-gap proposals.

## Validation

Command:

```bash
git diff --check -- docs/knowledge-graph/aec-explorer-overlay-campaigns.md
```

Result: passed.

## Safety

The documentation explicitly states that Explorer does not approve relationships, merge nodes, create Resource Layer links, admit source claims, mutate active graph files, or write to Neo4j/Postgres.
