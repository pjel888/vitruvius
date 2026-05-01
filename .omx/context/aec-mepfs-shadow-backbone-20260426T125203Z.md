---
task: aec-mepfs-shadow-backbone
created_utc: 20260426T125203Z
mode: ralph-ultrawork-team-fallback
---

# AEC-MEPFS Shadow Backbone Context Snapshot

## Task Statement

Continue the AEC-MEPFS shadow-backbone work autonomously from the current repo
state. Select, implement, verify, commit, push, and continue safe
shadow-only/read-only slices until no repo-evidenced safe work remains.

## Desired Outcome

- Complete safe file-backed/read-only AEC-MEPFS readiness work.
- Keep all runtime integration blocked unless separately authorized by the
  readiness gates.
- Maintain current evidence logs, manifests, state docs, tests, GitNexus index,
  and pushed git history.

## Known Facts / Evidence

- Latest pushed baseline at resume: `5d568c92` on `main`.
- Slice 37 resolver-route parity hygiene is pushed.
- Slice 38 downstream evidence refresh is generated and test-verified but still
  dirty/uncommitted at snapshot time.
- Current Slice 38 artifacts:
  - `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260426T124656Z/api-route-inventory-report.json`
  - `006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260426T124657Z/shadow-boundary-audit-report.json`
  - `006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T124658Z/benchmark-report.json`
  - `006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T124700Z/shadow-evidence-manifest-report.json`
- Focused evidence tests for Slice 38 passed: 98 tests.
- API `v2Backbone.test.ts` passed: 60 tests, 214 assertions.

## Constraints

- Do not write Neo4j.
- Do not rebuild KG.
- Do not ingest protected content.
- Do not cut over feature flags.
- Do not mount `/v2/resolve` or `/v2/resolve/trace`.
- Do not make Explorer adopt the shadow backbone as the default graph.
- Keep generated artifacts file-backed, auditable, and shadow-only.
- Attempt Gemini and Kimi review where locally available; log blocked access.

## Unknowns / Open Questions

- After Slice 38 is committed, the next safe slice must be derived from a fresh
  repo scan rather than assumed.
- Remaining safe candidates likely sit in benchmark/report hardening, manifest
  validation, parity coverage, or opt-in preview evidence.

## Likely Codebase Touchpoints

- `scripts/vitruvius/kg/backbone_*`
- `scripts/tests/test_kg_backbone*.py`
- `api/index.ts`
- `api/v2Backbone.test.ts`
- `explorer/src/components/explorer-rail/BackbonePreviewPanel.tsx`
- `.ai/03_plans/AEC-MEPFS-Backbone/`
- `.ai/05_logs/`
- `006_System-Manifests/aec-mepfs-backbone/`
