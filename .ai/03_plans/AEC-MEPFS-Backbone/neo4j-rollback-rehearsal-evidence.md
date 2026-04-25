---
task: aec-mepfs-backbone
phase: neo4j-rollback-rehearsal
created: 2026-04-25
author: CODEX
status: SAFE-REHEARSAL-BLOCKED-BY-LIVE-DATABASE
---

# Neo4j Rollback Rehearsal Evidence

## Purpose

Record what was safely verified for rollback readiness and why a live dump/load
rehearsal was not executed.

## Local Evidence

Commands inspected:

```bash
neo4j-admin database dump --help
neo4j-admin database load --help
neo4j-admin --version
neo4j-admin database backup --help
neo4j-admin database restore --help
ps aux | rg -i '[n]eo4j|[j]ava.*neo4j'
```

Observed:

- local Neo4j version: `2026.03.1`
- local Neo4j Community server is running
- `neo4j-admin database dump` is available
- `neo4j-admin database load` is available
- `neo4j-admin database backup` is not exposed in the local Community command
  surface
- `neo4j-admin database restore` is not exposed in the local Community command
  surface
- local help states a mounted database cannot be dumped or replaced

## Official Documentation Evidence

Neo4j Operations Manual evidence checked on 2026-04-25:

- Docker/offline dump/load documentation says `neo4j-admin database dump` and
  `database load` are for dumping/loading an offline database.
- Restore documentation says Community edition load runs only on an offline
  DBMS and that a mounted running database cannot be replaced.
- Neo4j Admin/CLI documentation identifies online backup/restore as Enterprise
  commands, while local Community help exposes only dump/load/import/check/info.

## Rehearsal Disposition

Stopped/isolated dump/load proof status:
`not_executed_safe_environment_required`

Reason:

- The local MVP graph is live and serving the Explorer/API stack.
- Stopping it would be user-visible and outside the safe readiness-evidence
  boundary.
- Running dump/load against the live mounted database is explicitly unsupported.
- No separate isolated Neo4j DBMS home/data directory was available for a
  meaningful dump/load rehearsal.

## Required Rehearsal Before Runtime Mutation

Before any Neo4j mutation, cleanup, or primary-label promotion, run a separate
operator-approved rehearsal in one of these environments:

1. Stopped local Neo4j with a confirmed maintenance window.
2. Isolated throwaway Neo4j home/data directory loaded with a representative
   graph.
3. Enterprise online-backup-capable Neo4j environment, if the deployment changes.

Minimum proof fields:

- database name
- Neo4j version and edition
- pre-dump node/relationship counts
- dump command and output path
- load command and target directory/database
- post-load node/relationship counts
- smoke query results
- rollback time and failure mode

## Runtime Rule

Until this proof exists, do not:

- clear Neo4j
- run graph rebuilds that mutate Neo4j
- promote shadow labels into primary labels
- flip API/Explorer reads to a new graph
- treat S5/S7 preflight evidence as rollback proof
