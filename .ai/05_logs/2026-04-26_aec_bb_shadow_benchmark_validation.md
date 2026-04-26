# AEC-BB Shadow Benchmark Validation

**Date:** 2026-04-26
**Scope:** twentieth AEC-MEPFS Backbone shadow slice
**Status:** validated

## Implemented Boundary

- Added `scripts/vitruvius/kg/backbone_shadow_benchmark.py`.
- Added focused tests in
  `scripts/tests/test_kg_backbone_shadow_benchmark.py`.
- Generated benchmark evidence at:

`006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T080510Z/benchmark-report.json`

The runner reads only file-backed evidence:

- S3 readiness fixture
- shadow staging consumer report
- sibling shadow graph artifact
- placement QA report
- resolver QA report
- API/Explorer parity report
- boundary audit report
- `api/index.ts`

No runtime resolver calls, API server calls, Explorer calls, Neo4j calls, KG
rebuilds, feature-flag changes, source/content ingest, or graph promotion are
performed.

## GitNexus Impact

- `npx --yes gitnexus@1.6.2-rc.10 status`
  - Result: indexed commit `8ce6f95`, current commit `8ce6f95`, up to date.
- `npx --yes gitnexus@1.6.2-rc.10 impact -r vitruvius --direction upstream validate_backbone_contract_file`
  - Result: MEDIUM risk, 13 impacted symbols, 5 direct callers, 0 affected
    processes.
- This slice imports and calls `validate_backbone_contract_file`; it does not
  edit the validator or any listed direct caller.

## Generated Evidence

Benchmark report:

`006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T080510Z/benchmark-report.json`

Counts and timings:

- Operations passed: 5/5
- Repetitions per operation: 5
- `contract_validation`: p50 0.240041 ms, p95 0.547083 ms
- `shadow_evidence_json_read`: p50 0.311542 ms, p95 2.087125 ms
- `shadow_graph_shape_scan`: p50 0.0295 ms, p95 0.031375 ms
- `api_route_static_scan`: p50 0.391833 ms, p95 0.87625 ms
- `input_hash_scan`: p50 0.207084 ms, p95 0.243458 ms

Auditability fields:

- input file paths for all seven evidence inputs
- SHA-256 hashes for all seven evidence inputs
- git HEAD and working-tree status metadata
- explicit `runtime_thresholds_evaluated: false`
- explicit `runtime_threshold_disposition:
  not_evaluated_shadow_file_backed_only`

## Gemini / Kimi / Verifier Review

- Gemini CLI is present, but the advisory attempt failed with the same Google
  Code Assist HTTP 403 service-disabled response observed in prior slices.
- Kimi CLI is present. One read-only plan-mode review completed and reported no
  safety regressions across Neo4j writes, KG rebuilds, protected content ingest,
  and feature-flag cutover. It also indicated medium-risk hardening
  recommendations around test/evidence/report fragility.
- A second self-contained Kimi print-mode review was attempted for better
  capture, but it did not return before validation continued and was treated as
  unavailable for this slice rather than a blocker.
- Native verifier `Gauss the 2nd` returned PASS with no blocking findings. It
  confirmed the runner is file-backed, the report is `ok: true`, all five
  operations pass, and tests cover route-mount drift, graph-shape drift, invalid
  plans, unsafe run IDs/output paths, and missing inputs.
- After advisory review, the focused suite was expanded to also cover missing
  preview routes, output paths scoped to the wrong run ID, and invalid evidence
  JSON.

Residual review note: both inline review and verifier review point out that API
route safety is currently regex-based over the direct `api/index.ts` Hono route
style. If routes move into nested routers, this benchmark/static audit surface
should be replaced or supplemented by parser-backed route inventory before it is
used as a promotion gate.

## Verification

- `python3 -m py_compile scripts/vitruvius/kg/backbone_shadow_benchmark.py`
  - Result: passed.
- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_shadow_benchmark.py`
  - Result: 10 passed.
- `PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_benchmark --run-id 20260426T080510Z`
  - Result: ok, 5/5 file-backed operations passed.
- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_shadow_benchmark.py scripts/tests/test_kg_backbone_shadow_boundary_audit.py scripts/tests/test_kg_backbone_resolver_qa.py scripts/tests/test_kg_backbone_placement_qa.py scripts/tests/test_kg_backbone_parity_runner.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_shadow_report_reader.py scripts/tests/test_kg_backbone_shadow_staging.py`
  - Result: 127 passed.
- `cd api && bun test v2Backbone.test.ts`
  - Result: 44 passed.
- `python3 -m json.tool 006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T080510Z/benchmark-report.json`
  - Result: passed.

## Safety Invariants

- No Neo4j writes: runner imports no Neo4j client/loader and only reads files.
- No KG rebuild: no pipeline/rebuild/reset command is called or authorized.
- No protected content ingest: runner reads metadata reports and fixture
  records only.
- No feature flag cutover: runner writes no config and changes no feature
  flags.
- No Explorer default graph adoption: no Explorer files are changed.
- No `/v2/resolve` route mounting: the benchmark fails if mounted resolver
  routes appear in `api/index.ts`.
- Preview/read-only/shadow-only behavior remains opt-in: this slice adds no
  route or UI surface.
- Generated artifacts are file-backed and auditable: the report includes input
  paths, SHA-256 hashes, repo state, timings, and runtime-threshold
  non-evaluation.

## Known Residual Risks

- API route detection is regex-based against the current direct Hono route
  style. If routes are later moved into nested routers, the benchmark/static
  route scan should be upgraded before being treated as a runtime promotion
  gate.
- The benchmark intentionally does not prove runtime thresholds for resolver,
  API, Explorer, Neo4j, or FTS paths. It is shadow evidence only.

## Next Recommended Safe Slice

Continue with another file-backed, shadow-only readiness slice after a fresh
repo inspection. Highest-value candidates remain parser-backed/static route
inventory hardening, benchmark/report reader validation, or additional
consumer/API parity checks that do not mount runtime resolver routes or adopt
the Explorer default graph.
