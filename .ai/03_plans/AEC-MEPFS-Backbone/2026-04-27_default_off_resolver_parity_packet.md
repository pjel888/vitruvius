---
task: aec-mepfs-backbone
phase: default-off-resolver-parity
created: 2026-04-27
author: CODEX
status: PASS
classification: GREEN,YELLOW-1,YELLOW-2
---

# Default-Off Resolver Parity Packet

## Purpose

Bring API/Explorer parity governance up to the current default-off resolver
runtime boundary. The default-off `/v2/resolve*` route slice is already complete
through `6e91b96a`, and non-protected resolver fixture coverage is complete
through `e90710ac`. Parity fixtures still treat every `/v2/resolve*` path as
forbidden. This packet updates parity validation so only exact default-off,
file-backed resolver routes can be represented in parity evidence.

## Authority

- Project-owner standing directive for autonomous AEC-MEPFS completion.
- Completed default-off resolver runtime commits: `fa93008b`, `6e91b96a`.
- Completed non-protected fixture expansion commits: `8afe54d1`, `e90710ac`.
- This packet does not authorize new route mounting; it only documents and tests
  the already guarded default-off routes.

## Allowed Scope

1. Add parity cases for exact default-off resolver paths:
   - `POST /v2/resolve`
   - `GET /v2/resolve/trace/:trace_id`
2. Require resolver parity cases to declare:
   - `default_off_only: true`
   - `execution_mode: api_default_off_resolver_unit`
   - `covered_by_command: (cd api && bun test v2Resolver.test.ts)`
3. Add the resolver test command to the parity runner allowlist and readiness
   runner plan.
4. Update contract/parity tests and regenerate parity/downstream evidence.
5. Update state docs and logs so the next active packet is explicit.

## Explicitly Blocked Scope

- New `/v2/resolve*` route mounting or default-on runtime behavior.
- Hot resolver changes beyond the existing file-backed builder tests.
- Neo4j writes/reloads/resets/backups/restores/promotions.
- KG rebuild/reload/reset.
- Protected source payload ingest or exposure.
- Explorer default adoption or automatic preview fetches.
- Runtime threshold pass/fail claims.
- Edits to `CanonicalNode`, `TaxonomyLoader`, or `Neo4jLoader`.

## Tests

Focused checks:

```bash
git diff --check
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_parity_runner.py -q
(cd api && bun test v2Resolver.test.ts v2Backbone.test.ts)
```

Downstream checks:

```bash
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_api_route_inventory.py scripts/tests/test_kg_backbone_shadow_boundary_audit.py scripts/tests/test_kg_backbone_shadow_benchmark.py scripts/tests/test_kg_backbone_shadow_evidence_manifest.py -q
```

## Evidence Artifacts

Regenerate after source commit:

- parity report under `006_System-Manifests/aec-mepfs-backbone/parity/<RUN_ID>/`
- route inventory, resolver QA, boundary audit, benchmark, and evidence manifest
  under the same run id where practical.

## Safety Invariants

- Default exported API still returns no `/v2/resolve*` route unless the explicit
  default-off flag is enabled.
- Parity cases are metadata/test declarations only; they do not expose protected
  source text or change API runtime behavior.
- Non-exact resolver subroutes such as `/v2/resolve/context` remain rejected.
- Runtime thresholds remain unevaluated unless a later benchmark packet provides
  an actual runtime path and threshold protocol.

## Completion Criteria

- Parity fixture has exact default-off resolver cases for resolve and trace.
- Contract validation rejects unguarded or non-exact resolver parity routes.
- Parity runner executes the `v2Resolver.test.ts` command and reports green.
- Generated parity/evidence artifacts are current.
- Evidence log exists under `.ai/05_logs/`.
- Commits are pushed to `origin/main`.

## Next Boundary

After this packet, the next safe packet may prepare a runtime benchmark harness
for the default-off resolver route without evaluating thresholds, or may align
Explorer opt-in preview documentation. Neo4j/live graph, protected source ingest,
Explorer default adoption, default-on flags, and runtime threshold claims remain
separate gated work.


## Generated Evidence Results

Run id: `20260427T034739Z`

- Parity report: `006_System-Manifests/aec-mepfs-backbone/parity/20260427T034739Z/api-explorer-parity-report.json` — PASS, `29/29` cases, `7/7` commands.
- Route inventory: `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260427T034739Z/api-route-inventory-report.json` — PASS, `24` routes, resolver policy `guarded_default_off`, `0` unauthorized resolver routes, `7/7` preview routes present.
- Resolver QA: `006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260427T034739Z/resolver-qa-report.json` — PASS, `7/7` resolver cases, `5/5` static error cases.
- Boundary audit: `006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260427T034739Z/shadow-boundary-audit-report.json` — PASS, `10/10` checks.
- Benchmark manifest: `006_System-Manifests/aec-mepfs-backbone/benchmarks/20260427T034739Z/benchmark-report.json` — PASS for shadow file-backed operations only; runtime thresholds remain unevaluated.
- Evidence manifest: `006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260427T034739Z/shadow-evidence-manifest-report.json` — PASS, `9` artifacts indexed.
