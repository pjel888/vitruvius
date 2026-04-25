---
task: aec-mepfs-backbone
phase: readiness-closure-scorecard
created: 2026-04-25
author: CODEX
status: NOT-READY-FOR-RUNTIME
---

# Readiness Closure Scorecard

## Verdict

The AEC-MEPFS Backbone packet is **more ready than before S1/S2/S3**, but it is
not ready for runtime integration.

It is ready only for the next bounded readiness/control implementation slices.
It is not ready for KG schema wiring, Neo4j mutation, graph rebuild, API/Explorer
runtime adoption, feature flags, canonical backbone admission, or protected
source ingest.

## What Is Closed

- File-backed validator: closed with `backbone_contracts.py` and focused tests.
- Predicate/source-rights fixture validation: closed for readiness with
  `valid_readiness_s2.json` and 35 focused tests.
- Authoring, resolver, API parity, and rollback metadata validation: closed for
  readiness with S2 and S3 fixtures.
- Production registry location plan: closed as a plan with
  `valid_integration_readiness_s3.json`.
- Benchmark plan: closed as a plan with `valid_integration_readiness_s3.json`.
- Current API/Explorer regression smoke: closed for current v1 behavior with
  `api: 18 pass` and `explorer: 35 pass`.
- Neo4j no-shadow mutation evidence: closed for this slice with read-only smoke
  showing `BackboneShadow` count 0.

## What Still Blocks Runtime

- Legal/licensing review: blocked external because no independent
  legal/licensing clearance has been recorded.
- API/Explorer parity runner: planned, not implemented. S3 defines required
  commands/assertions, but no dedicated parity runner/report artifact exists.
- Rollback proof: blocked runtime. `neo4j-admin database dump` cannot dump a
  mounted database, so proof needs a separate safe runtime packet.
- Production registry admission: blocked governance because planned locations
  exist, but no runtime registry file is steward-admitted.
- Canonical source admission: blocked governance because no backbone canonical
  source files have passed source rights and steward review.
- High-impact runtime roots: blocked technical because `CanonicalNode` remains
  CRITICAL and `TaxonomyLoader` / `Neo4jLoader` remain HIGH impact.

## Runtime Boundary

Do not perform any of the following from the current packet:

- edit `CanonicalNode`, `TaxonomyLoader`, `UnifiedSnapshotBuilder`, or
  `Neo4jLoader`
- write to Neo4j
- run backup/restore, cleanup, reset, or graph rebuild commands
- flip `k_taxonomy_v2`, `k_shadow_read`, `k_backbone_validation`, or related
  flags
- create production canonical backbone content
- ingest protected standards or legal source text
- route Explorer/API consumers to a backbone graph

## Next Implementable Slice

The safest next local slice is not runtime integration. It is:

`AEC-BB-S4`: implement a report-producing API/Explorer parity runner against
fixture data and current v1 tests.

S4 must remain file-backed and shadow-only. It may write a report under
`006_System-Manifests/aec-mepfs-backbone/parity/RUN_ID/`, but it must not
change API or Explorer runtime routes unless a separate impact-approved packet
exists.

## Minimum Gates Before Runtime Integration

Runtime integration can be reconsidered only when all of these are true:

- legal/licensing review decisions are recorded
- parity runner exists and produces a passing report
- rollback proof is executed in a safe environment
- production registry files are steward-admitted
- a separate implementation packet names exact runtime roots and d=1 dependents
- fresh GitNexus/code-impact evidence exists after the last commit
- focused backend, API, Explorer, and read-only graph checks pass
