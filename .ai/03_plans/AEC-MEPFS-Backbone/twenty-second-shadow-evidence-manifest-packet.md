---
task: aec-mepfs-shadow-evidence-manifest
phase: 05
created: 2026-04-26
author: CODEX
status: VALIDATED
supersedes: null
---

# Twenty-Second Shadow Slice: Evidence Manifest Consolidation

## Scope

Add a consolidated file-backed evidence manifest for the current AEC-MEPFS
Backbone shadow packet. The manifest verifies the existing producer, consumer,
graph, parity, placement QA, resolver QA, boundary audit, benchmark, and API
route-inventory reports; records SHA-256 hashes; checks cross-report paths; and
summarizes safety invariants in one auditable JSON report.

This slice is evidence hardening only. It does not add API routes, start the API
server, call Explorer, query or write Neo4j, rebuild the KG, ingest protected
content, change feature flags, or promote any shadow artifact.

## Research Baseline

- The twenty-first route-inventory slice centralized route-boundary evidence but
  left downstream evidence spread across several report directories.
- The benchmark default still needed to point at the newer route-inventory-backed
  boundary audit report instead of the older standalone boundary audit run.
- Runtime integration remains blocked, so the next safe improvement is an
  auditable manifest over already-generated file-backed evidence, not another
  live consumer.

## Audit Findings

- Current evidence is strong but fragmented: a reviewer must manually reconcile
  nine files to confirm that the graph, consumer report, boundary audit,
  benchmark, and route inventory all describe the same shadow packet.
- The manifest should fail closed when benchmark inputs reference stale boundary
  evidence, resolver routes appear mounted, boundary safety invariants drift, or
  required evidence files are missing.
- Artifact paths should remain repo-relative for portability. Absolute paths in
  generated manifest result rows would make the report harder to compare across
  machines.

## Implementation Plan

1. Update `backbone_shadow_benchmark.py` to use the route-inventory-backed
   boundary audit report by default.
2. Add `scripts/vitruvius/kg/backbone_shadow_evidence_manifest.py`.
3. Generate
   `006_System-Manifests/aec-mepfs-backbone/evidence-manifest/<run-id>/shadow-evidence-manifest-report.json`.
4. Validate schema versions, `ok` statuses, route-inventory resolver-route
   absence, benchmark shadow-only scope, and boundary safety invariants.
5. Cross-check producer/consumer/graph/benchmark path relationships.
6. Hash every input evidence file and include graph, benchmark, boundary, and
   route summary counts.
7. Add focused regression tests for happy path, stale benchmark boundary input,
   route resolver mounting, boundary drift, output fencing, run-ID fencing, and
   missing required files.

## Plan Critique

- [C001] Do not treat this as runtime benchmark or promotion evidence.
- [C002] Do not call API/Explorer runtimes; consume only existing files.
- [C003] Do not query Neo4j or import Neo4j clients.
- [C004] Keep output path fenced to the evidence-manifest report directory and
  current run ID.
- [C005] Treat missing evidence and cross-report path drift as failures, not
  warnings.
- [C006] Keep artifact paths repo-relative so generated evidence is portable.

## Execution Checklist

- [x] Inspect current evidence logs, docs, route inventory, benchmark report,
  and generated shadow artifacts.
- [x] Run GitNexus impact check before touching existing benchmark code.
- [x] Implement the evidence manifest runner and focused tests.
- [x] Refresh benchmark evidence against the route-inventory-backed boundary
  audit report.
- [x] Generate the consolidated evidence manifest.
- [x] Attempt Gemini/Kimi advisory review and record availability.
- [x] Run focused and broader affected Python/API verification.
- [x] Commit, refresh GitNexus, push, then inspect the next safe slice.

## Explicit Non-Goals

- No live graph promotion.
- No Neo4j write or query.
- No KG rebuild.
- No protected content ingest.
- No feature flag cutover.
- No Explorer default graph adoption.
- No API route addition or mounting.
- No runtime resolver invocation or runtime latency claim.
