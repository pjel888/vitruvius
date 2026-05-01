# AEC-MEPFS Shadow Completion Context

## Task Statement

Continue the AEC-MEPFS shadow-backbone work autonomously until all safe
shadow-only/read-only slices are complete or a real blocker is documented.

## Desired Outcome

Keep selecting bounded file-backed/read-only AEC-MEPFS Backbone slices,
implementing them, verifying them, committing them, refreshing GitNexus, and
pushing to `main` without promoting any runtime graph behavior.

## Known Facts / Evidence

- Current branch: `main`.
- Current base commit at resume: `e610edb343828a8eac724a55fad5e750297ccdad`.
- Slice 23 added compact read-only `GET /v2/backbone/evidence`.
- Slice 24 is active and hardens the consolidated shadow evidence manifest so
  route inventory, boundary audit, and benchmark reports must record the current
  `api/index.ts` SHA-256 hash.
- Current slice-24 generated report packet:
  - `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260426T093920Z/api-route-inventory-report.json`
  - `006_System-Manifests/aec-mepfs-backbone/parity/20260426T093921Z/api-explorer-parity-report.json`
  - `006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260426T093922Z/shadow-boundary-audit-report.json`
  - `006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T093923Z/benchmark-report.json`
  - `006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T093924Z/shadow-evidence-manifest-report.json`
- The route inventory, boundary audit, benchmark, and manifest reports all
  match the current `api/index.ts` hash:
  `bfb89a2a05d04c05014fda0737e5dcaf3300dafc819f397de25dac3a0a5bc7c3`.

## Constraints

- No live graph promotion.
- No Neo4j writes or queries.
- No KG rebuild.
- No protected content ingest.
- No feature flag cutover.
- No Explorer default graph adoption.
- No `/v2/resolve` runtime route mounting.
- Keep all generated artifacts file-backed and auditable.

## Unknowns / Open Questions

- Gemini CLI is installed but previously failed with HTTP 403 service-disabled
  errors.
- Kimi CLI is installed but previously timed out.
- OMX team runtime cannot launch in this session because `TMUX=unset`.
- `omx_code_intel` MCP transport is closed; GitNexus CLI is the current
  reliable impact/status path.

## Likely Codebase Touchpoints

- `api/index.ts`
- `api/v2Backbone.test.ts`
- `scripts/vitruvius/kg/backbone_shadow_evidence_manifest.py`
- `scripts/vitruvius/kg/backbone_shadow_boundary_audit.py`
- `scripts/vitruvius/kg/backbone_shadow_benchmark.py`
- `scripts/tests/test_kg_backbone_shadow_evidence_manifest.py`
- `.ai/03_plans/AEC-MEPFS-Backbone/`
- `.ai/05_logs/`
- `006_System-Manifests/aec-mepfs-backbone/`
