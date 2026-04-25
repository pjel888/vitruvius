---
task: aec-mepfs-backbone
phase: readiness-shadow-graph-safety
created: 2026-04-25
author: CODEX
status: ACCEPTED-READINESS-CONTROL
---

# Shadow Graph And Database Safety Protocol

## Purpose

Define the safe database path for later AEC-MEPFS Backbone implementation.

This protocol is textual only. No backup, restore, Neo4j write, graph reload, or
cleanup command was run for this artifact.

Accepted-readiness scope: the shadow-label topology, release/run ID separation,
destructive-operation block, and promotion order are accepted as safety
controls. Implementation remains blocked until backup/export, restore, smoke
queries, monitoring, and rollback proof are executed in a later packet.

S5 preflight evidence records that the local Neo4j admin surface exposes
`neo4j-admin database dump` and `neo4j-admin database load`, but both help
surfaces state mounted databases cannot be dumped or replaced. The local
`neo4j-admin backup --help` surface exposes no online backup subcommand.
Therefore rollback proof still requires a stopped or isolated database rehearsal
before any graph mutation.

S7 confirms the local Neo4j server is running and records the safe-rehearsal
disposition in `neo4j-rollback-rehearsal-evidence.md`: no dump/load rehearsal
was executed because a mounted live database cannot be safely dumped/replaced
and stopping the MVP graph is outside the readiness-evidence boundary.

## Recommended Shadow Topology

For the first bounded implementation slice, use shadow labels and release IDs in
the existing local Neo4j environment:

- current graph labels remain readable for v1 Explorer/API routes
- backbone nodes receive shadow-only labels such as `BackboneShadow`,
  `BackboneConceptShadow`, `BackboneOverlayShadow`
- every shadow node and relationship carries `taxonomy_release_id` and
  `shadow_run_id`
- `/v2` shadow reads are the only consumers until parity passes

This topology avoids requiring a second Neo4j database for MVP, but it also means
rollback evidence is mandatory before any cleanup or primary-label promotion.

## Destructive Operation Block

The following remain blocked until a later execution packet proves backup,
restore, shadow parity, flag safety, and monitoring:

```cypher
MATCH (n) DETACH DELETE n
```

```bash
python3 scripts/pipeline_cli.py run-kg-pipeline --reset
```

## Later Backup / Restore Spec

The exact backup/export command must be chosen in the execution packet according
to the running Neo4j edition and deployment mode. S5 indicates the local
rehearsal cannot rely on online backup and must use a stopped or isolated
database flow unless the deployment surface changes. At minimum, capture:

- Neo4j version
- database name
- node/relationship counts
- export path
- restore command
- restore smoke query

## Later Smoke Queries

```cypher
MATCH (n) RETURN count(n) AS nodes;
MATCH ()-[r]->() RETURN type(r) AS type, count(*) AS count ORDER BY count DESC;
MATCH (n:BackboneShadow) RETURN count(n) AS shadow_nodes;
MATCH (n:CanonicalNode) RETURN count(n) AS current_nodes;
```

## Promotion Sequence

1. Build shadow graph.
2. Run `/v2` shadow API reads.
3. Run v1/v2 parity report.
4. Prove rollback from backup/export.
5. Enable shadow-read flag for controlled local validation.
6. Monitor for 48 hours.
7. Only then consider cleanup or primary-label promotion.

## Pass / Fail Gate

Pass:

- shadow labels/release IDs are separated from current graph
- backup/export and restore proof exist before cleanup
- current 001-Laws Explorer graph remains baseline until parity passes

Fail:

- current graph is deleted before backup/restore evidence
- v1 Explorer routes depend on shadow labels before parity
- feature flags are enabled before rollback proof
