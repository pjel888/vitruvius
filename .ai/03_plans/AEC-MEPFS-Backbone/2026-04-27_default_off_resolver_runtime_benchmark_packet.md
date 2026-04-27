---
task: aec-mepfs-backbone
phase: default-off-resolver-runtime-benchmark
created: 2026-04-27
author: CODEX
status: PASS
classification: YELLOW-4
---

# Default-Off Resolver Runtime Benchmark Packet

## Purpose

Add an observational benchmark harness for the already-guarded default-off
AEC-MEPFS resolver route surface. The goal is to prove the benchmark harness can
exercise the default-off and explicitly enabled in-process route behavior over
non-protected fixture data, while keeping runtime threshold pass/fail claims
blocked.

## Authority

- Project-owner standing directive for autonomous AEC-MEPFS completion.
- Completed default-off resolver runtime packet: `2026-04-27_default_off_resolver_runtime_packet.md`.
- Completed resolver fixture expansion packet: `2026-04-27_resolver_fixture_expansion_packet.md`.
- Completed parity packet and evidence: `2026-04-27_default_off_resolver_parity_packet.md`, commit `4d0593df`.
- Authority class: `YELLOW-4` benchmark harness preparation. This packet does not authorize runtime threshold pass/fail adoption.

## Allowed Scope

1. Add an API-local benchmark harness that:
   - imports the default API with the resolver flag off and confirms `/v2/resolve` remains absent;
   - imports the API with `VITRUVIUS_AEC_MEPFS_RESOLVER_RUNTIME=true` only inside the harness;
   - exercises deterministic non-protected fixture cases for `single_value`, `composed`, `conflict`, `none`, and trace lookup;
   - writes an auditable JSON report under `006_System-Manifests/aec-mepfs-backbone/runtime-resolver-benchmark/<RUN_ID>/`.
2. Add focused tests for report shape, safety invariants, and output-path fencing.
3. Update the integration benchmark plan so the default-off resolver runtime harness command is concrete instead of a placeholder.
4. Preserve the shadow benchmark runner as file-backed only while recording the dedicated runtime harness command separately.
5. Refresh state docs so the completed parity packet is no longer presented as current work.

## Explicitly Blocked Scope

- Default-on feature flags or hidden cutover behavior.
- Runtime threshold pass/fail claims or `thresholds_green` promotion.
- External API server load testing.
- Neo4j writes, reads for benchmark purposes, reset, reload, backup, restore, or promotion.
- KG rebuild/reload/reset.
- Protected source text, tables, figures, datasets, clauses, or local protected caches.
- Explorer default adoption or automatic preview fetches.
- Edits to `CanonicalNode`, `TaxonomyLoader`, or `Neo4jLoader`.

## Contract Surfaces

- New harness module: `api/aecResolverRuntimeBenchmark.ts`.
- New focused tests: `api/aecResolverRuntimeBenchmark.test.ts`.
- Integration fixture update: `scripts/tests/fixtures/aec_mepfs_backbone/valid_integration_readiness_s3.json`.
- Shadow benchmark/report validation updates:
  - `scripts/vitruvius/kg/backbone_shadow_benchmark.py`
  - `scripts/vitruvius/kg/backbone_shadow_evidence_manifest.py`
  - `scripts/tests/test_kg_backbone_shadow_benchmark.py`
  - `scripts/tests/test_kg_backbone_shadow_evidence_manifest.py`

## Verification Commands

```bash
git diff --check
python3 -m compileall -q scripts/vitruvius/kg/backbone_shadow_benchmark.py scripts/vitruvius/kg/backbone_shadow_evidence_manifest.py
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_shadow_benchmark.py scripts/tests/test_kg_backbone_shadow_evidence_manifest.py scripts/tests/test_kg_backbone_contracts.py -q
(cd api && bun test aecResolverRuntimeBenchmark.test.ts v2Resolver.test.ts)
```

Generated evidence commands after source commit:

```bash
(cd api && bun aecResolverRuntimeBenchmark.ts --run-id <RUN_ID>)
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_benchmark --run-id <RUN_ID> --parity-report 006_System-Manifests/aec-mepfs-backbone/parity/20260427T034739Z/api-explorer-parity-report.json --resolver-qa-report 006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260427T034739Z/resolver-qa-report.json --boundary-audit-report 006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260427T034739Z/shadow-boundary-audit-report.json
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_evidence_manifest --run-id <RUN_ID> --benchmark-report 006_System-Manifests/aec-mepfs-backbone/benchmarks/<RUN_ID>/benchmark-report.json --parity-report 006_System-Manifests/aec-mepfs-backbone/parity/20260427T034739Z/api-explorer-parity-report.json --resolver-qa-report 006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260427T034739Z/resolver-qa-report.json --boundary-audit-report 006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260427T034739Z/shadow-boundary-audit-report.json --route-inventory-report 006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260427T034739Z/api-route-inventory-report.json
```

## Evidence Artifacts

- Runtime resolver benchmark report: `006_System-Manifests/aec-mepfs-backbone/runtime-resolver-benchmark/<RUN_ID>/runtime-resolver-benchmark-report.json`
- Shadow benchmark report: `006_System-Manifests/aec-mepfs-backbone/benchmarks/<RUN_ID>/benchmark-report.json`
- Evidence manifest: `006_System-Manifests/aec-mepfs-backbone/evidence-manifest/<RUN_ID>/shadow-evidence-manifest-report.json`
- Validation log: `.ai/05_logs/2026-04-27_aec_mepfs_default_off_resolver_runtime_benchmark_validation.md`

## Safety Invariants

- The default exported API keeps `/v2/resolve*` absent when `VITRUVIUS_AEC_MEPFS_RESOLVER_RUNTIME` is unset.
- The harness uses in-process Hono `fetch`; it does not start or load-test an external server.
- Fixture data remains non-protected metadata/golden cases only.
- No Neo4j or KG rebuild path is called.
- Runtime durations may be recorded as observations, but `runtimeThresholdEvidence.evaluated` and `passFailClaim` must remain false.
- Explorer defaults and feature-flag defaults remain unchanged.

## Completion Criteria

- Harness and tests pass.
- Shadow benchmark and evidence manifest recognize the concrete runtime harness command without claiming thresholds.
- Generated runtime benchmark evidence exists.
- State docs no longer point to default-off resolver parity as the active next task.
- Evidence log exists and records Gemini/Kimi status.
- Commit is pushed to `origin/main`.

## Next Boundary

After this packet, the next safe work should be derived from repo evidence. Likely candidates are Explorer opt-in documentation/parity alignment or final closure/backlog reconciliation. Neo4j/live graph, protected ingest, Explorer default adoption, default-on flags, and runtime threshold adoption remain separate gated packets.


## Generated Evidence Results

Run id: `20260427T040813Z`

- Runtime resolver benchmark: `006_System-Manifests/aec-mepfs-backbone/runtime-resolver-benchmark/20260427T040813Z/runtime-resolver-benchmark-report.json` — PASS, `6/6` operations, `runtimeThresholdEvidence.evaluated=false`, `passFailClaim=false`.
- Parity report: `006_System-Manifests/aec-mepfs-backbone/parity/20260427T040813Z/api-explorer-parity-report.json` — PASS, `29/29` cases and `7/7` commands.
- Route inventory: `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260427T040813Z/api-route-inventory-report.json` — PASS, `24` routes, resolver policy `guarded_default_off`, `0` unauthorized resolver routes.
- Resolver QA: `006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260427T040813Z/resolver-qa-report.json` — PASS, `7/7` cases.
- Boundary audit: `006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260427T040813Z/shadow-boundary-audit-report.json` — PASS, `10/10` checks.
- Shadow benchmark: `006_System-Manifests/aec-mepfs-backbone/benchmarks/20260427T040813Z/benchmark-report.json` — PASS, `5/5` file-backed operations; `runtime_harness_command_count=1`; runtime thresholds not evaluated.
- Evidence manifest: `006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260427T040813Z/shadow-evidence-manifest-report.json` — PASS, `9` consolidated shadow artifacts indexed; runtime thresholds not evaluated.
