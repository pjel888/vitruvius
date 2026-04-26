---
task: aec-mepfs-shadow-benchmark-evidence-hardening
phase: 05
created: 2026-04-26
author: CODEX
status: PASS
supersedes: null
---

# Thirty-Ninth Shadow Slice: Benchmark Evidence Hardening

## Scope

Harden the file-backed shadow benchmark report so it records explicit operation
coverage and runtime-threshold non-evaluation evidence, then harden the
consolidated evidence manifest so it fails closed if that benchmark evidence
drifts.

This slice changes report schemas and tests only. It does not run runtime
resolver paths, call API or Explorer servers, query or write Neo4j, rebuild the
KG, ingest protected content, change feature flags, mount `/v2/resolve`, or
make Explorer adopt the shadow graph by default.

## Audit Findings

- Fresh post-`e6333a17` scans found no safe unresolved `/v2` preview parity
  implementation slice.
- The latest benchmark report already records file-backed operations and keeps
  runtime thresholds unevaluated, but the manifest only counted operations; it
  did not validate expected operation coverage or explicit runtime-threshold
  evidence fields.
- GitNexus impact for `run_shadow_benchmark`: MEDIUM, 14 upstream impacts, no
  affected process flows, direct callers are tests and CLI `main`.
- GitNexus impact for `run_shadow_evidence_manifest`: MEDIUM, 13 upstream
  impacts, no affected process flows, direct callers are tests and CLI `main`.

## Implementation

- `backbone_shadow_benchmark.py` now emits:
  - `operation_coverage.required_operations`
  - operation pass/total counts
  - missing/unexpected operation lists
  - `runtime_threshold_evidence` with declared threshold count, blocked runtime
    scope, exact future runtime commands from the declared plan, and explicit
    non-evaluation disposition
- `backbone_shadow_evidence_manifest.py` now validates:
  - benchmark required operation set, missing/unexpected operations, pass counts,
    and duplicate required operation names
  - runtime-threshold evidence disposition, non-evaluation booleans, blocked
    runtime scope, declared command/threshold counts, and exact future runtime
    command alignment with `plan.declared_commands`
  - summary fields for required-operation presence, threshold disposition, and
    declared threshold count
- Focused tests now assert the benchmark report shape and reject manifest drift
  when operation coverage or runtime-threshold evidence changes unsafely.

## Plan Critique

- [C001] Do not evaluate runtime thresholds in this slice; runtime benchmarking
  remains blocked until runtime resolver/API/Explorer/Neo4j paths are accepted.
- [C002] Keep validation report-only and fixture-backed; do not add API or
  Explorer adoption requirements until the generated manifest has been refreshed.
- [C003] Required operation coverage should be order-insensitive in the manifest
  to avoid false failure on harmless ordering changes.

## Execution Checklist

- [x] Run fresh remaining-work scan after Slice 38.
- [x] Run GitNexus impact for benchmark and evidence manifest runner roots.
- [x] Implement benchmark operation coverage and threshold evidence fields.
- [x] Implement evidence manifest validation for those fields.
- [x] Add focused positive and drift tests.
- [x] Add regression coverage for required-operation mismatch, duplicate
  required operations, unexpected operations, future-command drift, and missing
  blocked runtime scope.
- [x] Run focused benchmark/manifest tests.
- [x] Run full `test_kg_backbone*.py` suite.
- [x] Run API `/v2` tests for compatibility.
- [x] Attempt Gemini/Kimi advisory review and apply accepted findings.
- [ ] Commit this code/doc slice.
- [ ] Generate source-clean benchmark and manifest evidence in the next slice.

## Explicit Non-Goals

- No Neo4j write, query, backup, restore, or cleanup.
- No KG rebuild/reset/load.
- No protected source content ingest.
- No feature flag cutover.
- No `/v2/resolve` or `/v2/resolve/trace` route mounting.
- No Explorer default graph adoption.
- No live runtime performance threshold claim.

## Next Safe Slice

After this code/doc slice is committed and pushed, regenerate the file-backed
benchmark and consolidated evidence manifest from a clean source tree so the new
benchmark evidence fields are present in generated evidence.
