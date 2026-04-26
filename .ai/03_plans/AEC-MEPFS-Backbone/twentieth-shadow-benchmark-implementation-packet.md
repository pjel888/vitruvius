---
task: aec-mepfs-shadow-benchmark
phase: 05
created: 2026-04-26
author: CODEX
status: VALIDATED
supersedes: null
---

# Twentieth Shadow Slice: File-Backed Benchmark Runner

## Scope

Add a file-backed benchmark runner that measures local validation, JSON read,
graph-shape scan, API route static scan, and input-hash scan operations over the
existing AEC-MEPFS shadow evidence.

This slice produces readiness evidence only. It does not run runtime resolver
paths, call API or Explorer servers, query or write Neo4j, rebuild the KG,
ingest protected content, change feature flags, alter Explorer defaults, or
promote any shadow artifact to the live graph.

## Research Baseline

- `verification-and-benchmark-contract.md` and the S3 fixture already define a
  benchmark report path, repetitions, percentiles, and future runtime threshold
  placeholders.
- `readiness-spec-acceptance-record.md` still marks benchmark runner/report
  execution open.
- The nineteenth boundary audit consolidated current safety evidence and is now
  a prerequisite input for this runner.

## Audit Findings

- Runtime benchmark thresholds are intentionally not evaluable while runtime
  integration remains blocked.
- The safe remaining value is to make current file-backed evidence measurable
  and auditable without creating a runtime performance claim.
- The benchmark report must make the runtime-threshold disposition explicit so
  future readers do not mistake file-read timings for resolver/API/Neo4j
  latency proof.

## Implementation Plan

1. Add `scripts/vitruvius/kg/backbone_shadow_benchmark.py`.
2. Read only current file-backed evidence:
   - S3 readiness fixture
   - shadow staging consumer report
   - sibling shadow graph artifact
   - placement QA report
   - resolver QA report
   - API/Explorer parity report
   - boundary audit report
   - `api/index.ts`
3. Measure five file-backed operations for the fixture-declared repetitions:
   - contract validation
   - shadow evidence JSON reads
   - shadow graph shape scan
   - API preview route static scan
   - input hash scan
4. Write
   `006_System-Manifests/aec-mepfs-backbone/benchmarks/<run-id>/benchmark-report.json`
   with p50/p95 timings, input hashes, repo-state metadata, and explicit
   `runtime_thresholds_evaluated: false`.
5. Add focused tests for happy path, resolver route mounting, graph-shape drift,
   invalid benchmark plan, unsafe run IDs, unsafe output paths, and missing
   inputs.
6. Generate fresh benchmark evidence and update state docs.

## Plan Critique

- [C001] Do not present this as runtime resolver/API/Neo4j performance proof.
- [C002] Do not mount `/v2/resolve`, call API servers, call Explorer, or query
  Neo4j from the benchmark runner.
- [C003] Keep output path fenced to the benchmark report directory and current
  run ID.
- [C004] Fail closed if required preview routes disappear or blocked resolver
  routes appear in `api/index.ts`.
- [C005] Preserve the future runtime threshold placeholders as declared
  thresholds only; runtime threshold evaluation remains blocked.

## Execution Checklist

- [x] Inspect active state, scorecard, and remaining shadow benchmark gap.
- [x] Run GitNexus query/impact checks before implementation.
- [x] Implement the file-backed benchmark runner.
- [x] Add focused tests for safety-drift failures and path fences.
- [x] Generate fresh benchmark evidence.
- [x] Attempt Gemini/Kimi advisory review and record availability.
- [x] Run focused and broader affected Python/API verification.
- [ ] Commit, refresh GitNexus, push, then inspect the next safe slice.

## Explicit Non-Goals

- No runtime resolver benchmark.
- No API server benchmark.
- No Explorer runtime benchmark.
- No Neo4j or FTS benchmark.
- No `/v2/resolve` route mounting.
- No Neo4j writes.
- No KG rebuild.
- No protected content ingest.
- No feature flag cutover.
- No Explorer default graph adoption.
- No canonical source/content admission.
