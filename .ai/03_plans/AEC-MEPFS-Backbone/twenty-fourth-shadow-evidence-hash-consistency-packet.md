---
task: aec-mepfs-shadow-evidence-hash-consistency
phase: 05
created: 2026-04-26
author: CODEX
status: VALIDATED
supersedes: null
---

# Twenty-Fourth Shadow Slice: Evidence Hash Consistency

## Scope

Harden the consolidated shadow evidence manifest so it verifies that generated
route-inventory, boundary-audit, and benchmark reports were produced from the
current `api/index.ts` file. Then regenerate a coherent file-backed evidence
packet over the current shadow routes.

This slice is manifest/evidence hardening only. It does not add Explorer UI,
promote a graph, mount `/v2/resolve`, query or write Neo4j, rebuild the KG,
ingest protected content, change feature flags, or make Explorer adopt the
shadow graph.

## Research Baseline

- The twenty-third slice added `GET /v2/backbone/evidence` and regenerated
  evidence reports.
- The generated reports intentionally captured `working_tree_dirty: true`
  because they prove the uncommitted slice.
- A stricter manifest should also detect stale report inputs when an upstream
  generated report records an older `api/index.ts` SHA-256 hash.

## Audit Findings

- `backbone_shadow_evidence_manifest.py` currently hashes the report files but
  does not compare report-recorded API hashes against the current API file.
- Route inventory, boundary audit, and benchmark reports all carry
  `input_file_hashes_sha256.api_index`.
- Adding a current-API hash check closes a real evidence gap without touching
  runtime graph code.

## Implementation Plan

1. Add `DEFAULT_API_INDEX_PATH` and an `api_index_path` parameter to the
   evidence manifest runner.
2. Include `api_index` in manifest inputs and input hashes.
3. Cross-check `route_inventory_report`, `boundary_audit_report`, and
   `benchmark_report` recorded API hashes against the current API file hash.
4. Add focused tests for passing API hash consistency and stale API-hash
   failure.
5. Preselect final report run IDs, update the API default evidence manifest
   path first, then regenerate route inventory, parity, boundary audit,
   benchmark, and evidence manifest so the new route inventory hash matches the
   final API code.
6. Update validation evidence and state docs.

## Plan Critique

- [C001] Do not weaken the existing artifact/schema/safety checks.
- [C002] Do not treat `working_tree_dirty: true` as a failure; generated reports
  are expected to be created before commit.
- [C003] Do not add runtime benchmark claims or live API/Explorer calls.
- [C004] Avoid Explorer changes in this slice; keep this as proof hardening.
- [C005] Regenerate dependent artifacts after the final API default-path edit.

## Execution Checklist

- [x] Inspect current evidence manifest implementation and tests.
- [x] Run GitNexus impact for `run_shadow_evidence_manifest`.
- [x] Implement API hash consistency checks and focused tests.
- [x] Regenerate coherent evidence artifacts.
- [x] Attempt Gemini/Kimi advisory review and record availability.
- [x] Run focused and broader affected verification.
- [ ] Commit, refresh GitNexus, push, then inspect the next safe slice.

## Validation Evidence

- Regenerated route inventory:
  `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260426T093920Z/api-route-inventory-report.json`
- Regenerated parity:
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T093921Z/api-explorer-parity-report.json`
- Regenerated boundary audit:
  `006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260426T093922Z/shadow-boundary-audit-report.json`
- Regenerated benchmark:
  `006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T093923Z/benchmark-report.json`
- Regenerated evidence manifest:
  `006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T093924Z/shadow-evidence-manifest-report.json`
- Current `api/index.ts` hash verified in route inventory, boundary audit,
  benchmark, and evidence manifest:
  `bfb89a2a05d04c05014fda0737e5dcaf3300dafc819f397de25dac3a0a5bc7c3`

## Explicit Non-Goals

- No Explorer rendering change.
- No Neo4j write or query.
- No KG rebuild.
- No protected content ingest.
- No feature flag cutover.
- No Explorer default graph adoption.
- No `/v2/resolve` route mounting.
- No runtime latency claim.
