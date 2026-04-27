# AEC-MEPFS Runtime Threshold Adoption Packet

```yaml
status: BOUNDARY_APPROVED
authority: project-owner-directive-four-gated-lanes
lane: runtime-threshold-adoption
classification: SATISFIED_YELLOW_FOR_FILE_BACKED_RUNTIME_BENCHMARK_EVALUATION
created: 2026-04-27
baseline_commit: 64d341cf
live_runtime_authorization: scoped_runtime_threshold_report_only
global_live_authorization: false
```

## 1. Purpose

Convert the existing guarded, default-off AEC-MEPFS resolver runtime benchmark
from observational evidence into a reproducible threshold-adoption report for
that exact runtime path.

This packet authorizes only a threshold evaluator that consumes a freshly
produced runtime resolver benchmark report and emits a separate auditable
threshold adoption report. It does not authorize default-on resolver behavior,
Explorer default adoption, Neo4j/KG mutation, protected ingest, or broad/global
live runtime status.

## 2. Authority and baseline

- Reopen umbrella packet: `2026-04-27_four_gated_lanes_reopen_packet.md`.
- Existing benchmark packet: `2026-04-27_default_off_resolver_runtime_benchmark_packet.md`.
- Existing guarded runtime harness: `api/aecResolverRuntimeBenchmark.ts`.
- Existing benchmark tests: `api/aecResolverRuntimeBenchmark.test.ts`.
- Previous evidence run: `20260427T044757Z`.

The runtime path is reproducible because the API-local harness imports the Hono
application in-process, verifies `/v2/resolve` is absent by default, enables the
resolver only inside the harness, exercises non-protected golden fixture cases,
and records per-operation p50/p95 measurements without external server calls.

## 3. Allowed scope

- Add a file-backed runtime threshold evaluator.
- Add focused tests for evaluator criteria and fail-closed behavior.
- Generate a fresh runtime resolver benchmark report after thresholds are
  declared in this packet and evaluator source.
- Generate `runtime-thresholds/<run-id>/runtime-threshold-adoption-report.json`.
- Set `passFailClaim=true` only in the threshold adoption report when the
  evaluator confirms the source report is an actual runtime benchmark report,
  the fixed corpus/plan/environment is present, and every operation threshold is
  evaluated.

## 4. Explicitly blocked scope

- Broad/global `LIVE_RUNTIME_AUTHORIZED` status.
- Default-on resolver feature flag or hidden cutover.
- External API server load testing.
- Neo4j reads/writes/reset/reload/backup/restore/promotion.
- KG rebuild/reload/reset.
- Protected source payload ingestion or exposure.
- Explorer default adoption or automatic preview fetch.
- Threshold adoption from shadow-only benchmark evidence.

## 5. Predeclared thresholds

The evaluator must declare these thresholds before the fresh benchmark run used
for final evidence:

| Operation | Threshold |
|---|---:|
| `default_off_resolve_absent` | p95 <= 100 ms |
| `enabled_single_value_resolve` | p95 <= 100 ms |
| `enabled_composed_resolve` | p95 <= 250 ms |
| `enabled_conflict_resolve` | p95 <= 250 ms |
| `enabled_none_resolve` | p95 <= 250 ms |
| `enabled_trace_lookup` | p95 <= 250 ms |

These apply only to the guarded default-off in-process resolver benchmark over
non-protected fixture cases. They do not apply to Neo4j-backed, production,
Explorer, or protected-source runtime paths.

## 6. Implementation plan

1. Add `scripts/vitruvius/kg/backbone_runtime_thresholds.py`.
2. Add `scripts/tests/test_kg_backbone_runtime_thresholds.py`.
3. Generate a fresh benchmark run after the evaluator exists.
4. Evaluate that fresh report into `006_System-Manifests/aec-mepfs-backbone/runtime-thresholds/<run-id>/`.
5. Update validation log with commands, report paths, Kimi status, and safety
   invariants.

## 7. Verification plan

```bash
git diff --check
python3 -m compileall -q scripts/vitruvius/kg/backbone_runtime_thresholds.py
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_runtime_thresholds.py scripts/tests/test_kg_backbone_shadow_benchmark.py -q
(cd api && bun test aecResolverRuntimeBenchmark.test.ts)
(cd api && bun aecResolverRuntimeBenchmark.ts --run-id <RUN_ID>)
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_runtime_thresholds --run-id <RUN_ID> --runtime-benchmark-report 006_System-Manifests/aec-mepfs-backbone/runtime-resolver-benchmark/<RUN_ID>/runtime-resolver-benchmark-report.json
```

## 8. Evidence artifacts

- Runtime benchmark input:
  `006_System-Manifests/aec-mepfs-backbone/runtime-resolver-benchmark/<RUN_ID>/runtime-resolver-benchmark-report.json`
- Threshold adoption output:
  `006_System-Manifests/aec-mepfs-backbone/runtime-thresholds/<RUN_ID>/runtime-threshold-adoption-report.json`
- Validation log:
  `.ai/05_logs/2026-04-27_aec_mepfs_runtime_threshold_adoption_validation.md`

## 9. Safety invariants

- Threshold adoption is limited to the guarded default-off, in-process Hono
  runtime harness.
- Source report must prove no external API server calls, Neo4j queries, KG
  rebuild, protected ingest, Explorer runtime calls, or feature-flag cutover.
- Evaluator rejects shadow-only benchmark reports and malformed/missing runtime
  reports.
- Output path is fenced to the runtime-threshold evidence directory.
- No production graph, source, Explorer default, or default-on flag is changed.

## 10. Completion criteria

- Packet exists and is internally consistent.
- Evaluator and tests pass.
- Fresh runtime benchmark evidence exists after threshold declaration.
- Threshold adoption report exists and truthfully states pass/fail for the
  guarded in-process runtime path only.
- Validation log records Kimi/Spark status, commands, artifacts, and safety
  invariants.
- Working tree is committed and pushed before proceeding to the next lane.

## 11. Next boundary

Explorer default adoption remains separate. Protected source admission remains
metadata-only unless valid rights/steward/legal authority exists. Neo4j rehearsal
remains isolated/sandbox-only unless its dedicated packet satisfies rollback and
namespace safety gates.

## Generated Evidence Results

Run id: `20260427T114711Z`

- Runtime resolver benchmark input:
  `006_System-Manifests/aec-mepfs-backbone/runtime-resolver-benchmark/20260427T114711Z/runtime-resolver-benchmark-report.json`
  - PASS, `6/6` operations; runtime source report remains observational with
    `runtimeThresholdEvidence.passFailClaim=false`.
- Runtime threshold adoption report:
  `006_System-Manifests/aec-mepfs-backbone/runtime-thresholds/20260427T114711Z/runtime-threshold-adoption-report.json`
  - PASS for the scoped guarded default-off in-process resolver runtime path.
  - `passFailClaim=true` only in this threshold-adoption report after evaluator
    criteria passed.
  - `overall_aec_runtime_thresholds_adopted=false`; API-server search, Neo4j
    FTS, Explorer runtime, and production live graph thresholds remain outside
    this scoped report.
