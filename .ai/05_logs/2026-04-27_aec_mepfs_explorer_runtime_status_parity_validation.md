---
date: 2026-04-27
task: aec-mepfs-backbone
phase: explorer-runtime-status-parity
status: VERIFIED_SOURCE_AND_EVIDENCE_READY_FOR_COMMIT
classification: GREEN/YELLOW-6
packet: .ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_explorer_runtime_status_parity_packet.md
---

# AEC-MEPFS Explorer Runtime-Status Parity Validation

## Scope

Aligned the file-backed API evidence preview and opt-in Explorer evidence preview with the current guarded-default-off resolver route policy and non-evaluated runtime-threshold disposition. This remains preview-only evidence display; it does not make the resolver live by default and does not make AEC-MEPFS the Explorer default graph.

## Branch / Commits

- Branch: `main`
- Starting commit: `df4b88bf` (`Reconcile AEC benchmark completion state`)
- Source commit 1: `10e63fe4` (`Surface guarded AEC resolver status in previews`)
- Source commit 2: `6665c6a5` (`Remove stale AEC resolver unmounted preview field`)
- Evidence/log commit: pending at log creation
- Working tree before source work: clean and synced except local source slice became ahead of `origin/main`
- Working tree after source commits and evidence generation: source clean; generated evidence/log uncommitted for this validation commit

## Files Inspected

- `.ai/03_plans/AEC-MEPFS-Backbone/api-explorer-parity-contract.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/readiness-closure-scorecard.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/README.md`
- `.ai/05_logs/2026-04-27_aec_mepfs_post_benchmark_state_reconciliation_validation.md`
- `api/index.ts`
- `api/v2Backbone.test.ts`
- `explorer/src/types/index.ts`
- `explorer/src/components/explorer-rail/BackbonePreviewPanel.tsx`
- `explorer/src/components/componentInteraction.test.tsx`
- `explorer/src/app.searchInspector.integration.test.tsx`
- `scripts/tests/fixtures/aec_mepfs_backbone/api-explorer-parity-cases.json`
- `scripts/vitruvius/kg/backbone_shadow_evidence_manifest.py`

## Files Changed

Source/docs/tests:

- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_explorer_runtime_status_parity_packet.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/README.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/api-explorer-parity-contract.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/readiness-closure-scorecard.md`
- `api/index.ts`
- `api/v2Backbone.test.ts`
- `explorer/src/types/index.ts`
- `explorer/src/components/explorer-rail/BackbonePreviewPanel.tsx`
- `explorer/src/components/componentInteraction.test.tsx`
- `explorer/src/app.searchInspector.integration.test.tsx`
- `scripts/tests/fixtures/aec_mepfs_backbone/api-explorer-parity-cases.json`

Evidence generated after source commit `6665c6a5`:

- `006_System-Manifests/aec-mepfs-backbone/parity/20260427T044757Z/api-explorer-parity-report.json`
- `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260427T044757Z/api-route-inventory-report.json`
- `006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260427T044757Z/resolver-qa-report.json`
- `006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260427T044757Z/shadow-boundary-audit-report.json`
- `006_System-Manifests/aec-mepfs-backbone/benchmarks/20260427T044757Z/benchmark-report.json`
- `006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260427T044757Z/shadow-evidence-manifest-report.json`

## Implementation Summary

- Added runtime-status metadata to the evidence preview summary:
  - `resolverRoutePolicy`
  - `benchmarkRuntimeThresholdDisposition`
- API evidence preview now fails closed if either runtime-status field is absent from the evidence manifest.
- Explorer displays the route policy and threshold disposition only inside the existing explicit `Load evidence summary` preview path.
- Removed the stale `resolverRoutesUnmounted` API/type/test-field fallback after Kimi identified that current evidence manifests use `resolver_routes_absent_or_default_off` instead.
- Updated parity fixtures and planning docs so current state is described as `guarded_default_off`, not legacy unmounted-only.

## GitNexus / Blast Radius

- Commit hook for `10e63fe4`: 22 files analyzed, 6 changed functions/classes, 0 affected flows, 0 test gaps, risk score `0.30`.
- Commit hook for `6665c6a5`: 11 files analyzed, 6 changed functions/classes, 0 affected flows, 0 test gaps, risk score `0.30`.
- `npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius buildShadowBackboneEvidencePreview --direction upstream`: `LOW`, 1 impacted node.
- `npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius BackboneEvidencePreview --direction upstream`: `HIGH`, 22 impacted nodes/direct Explorer import surface. This was not ignored; mitigation was full Explorer test, lint, and build plus API tests.
- Attempted unpinned `npx gitnexus impact ...`; it tried `gitnexus@1.6.3` and failed with `Cannot destructure property 'package' of 'node.target' as it is null`. Pinned `1.6.2-rc.10` succeeded.

## Commands Run

```bash
git status --short --branch
git rev-parse --short HEAD
git log --oneline -n 8
rg -n "AEC-MEPFS|Backbone|resolver|resolve|runtime|Neo4j|KG|Explorer|feature flag|threshold|blocked|defer|next safe|TODO|FIXME|remaining|packet|closure|scorecard|readiness|GitNexus|Ralph|UltraQA|Ultrawork|Architect" .ai scripts api explorer 006_System-Manifests
command -v gemini || true
command -v kimi || true
command -v moonshot || true
command -v llm || true
command -v aider || true
command -v opencode || true
gemini --approval-mode plan -p "Review this Vitruvius AEC-MEPFS diff..."
kimi --print -p "Review Vitruvius AEC-MEPFS commit 10e63fe4..."
git diff --check
(cd api && bun test v2Backbone.test.ts)
(cd explorer && bun test src/api/graphApi.test.ts src/components/componentInteraction.test.tsx src/app.searchInspector.integration.test.tsx)
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_parity_runner.py -q
npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius buildShadowBackboneEvidencePreview --direction upstream
npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius BackboneEvidencePreview --direction upstream
RUN_ID=20260427T044757Z
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_parity_runner --run-id "$RUN_ID" --timeout-seconds 300
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_api_route_inventory --run-id "$RUN_ID"
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_resolver_qa --run-id "$RUN_ID"
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_boundary_audit --run-id "$RUN_ID" --resolver-qa-report "006_System-Manifests/aec-mepfs-backbone/resolver-qa/${RUN_ID}/resolver-qa-report.json" --parity-report "006_System-Manifests/aec-mepfs-backbone/parity/${RUN_ID}/api-explorer-parity-report.json"
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_benchmark --run-id "$RUN_ID" --resolver-qa-report "006_System-Manifests/aec-mepfs-backbone/resolver-qa/${RUN_ID}/resolver-qa-report.json" --boundary-audit-report "006_System-Manifests/aec-mepfs-backbone/boundary-audit/${RUN_ID}/shadow-boundary-audit-report.json" --parity-report "006_System-Manifests/aec-mepfs-backbone/parity/${RUN_ID}/api-explorer-parity-report.json"
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_evidence_manifest --run-id "$RUN_ID" --resolver-qa-report "006_System-Manifests/aec-mepfs-backbone/resolver-qa/${RUN_ID}/resolver-qa-report.json" --boundary-audit-report "006_System-Manifests/aec-mepfs-backbone/boundary-audit/${RUN_ID}/shadow-boundary-audit-report.json" --benchmark-report "006_System-Manifests/aec-mepfs-backbone/benchmarks/${RUN_ID}/benchmark-report.json" --route-inventory-report "006_System-Manifests/aec-mepfs-backbone/api-route-inventory/${RUN_ID}/api-route-inventory-report.json" --parity-report "006_System-Manifests/aec-mepfs-backbone/parity/${RUN_ID}/api-explorer-parity-report.json"
(cd api && bun test)
(cd explorer && bun test && bun run lint && bun run build)
rg -n "/v2/resolve|resolve/trace" api explorer scripts --glob '!**/*.md' || true
rg -n "LIVE_RUNTIME_AUTHORIZED|MATCH \\(n\\) DETACH DELETE|DETACH DELETE|Neo4jLoader|TaxonomyLoader|CanonicalNode|run-kg-pipeline|--reset|--reload|protected content|protected ingest|Explorer default|default-on|runtime threshold" api explorer scripts .ai 006_System-Manifests --glob '!**/*.pyc' --glob '!**/__pycache__/**' | head -240 || true
```

## Test / Verification Results

- `git diff --check` — PASS.
- `(cd api && bun test v2Backbone.test.ts)` — PASS, `61 pass`.
- `(cd explorer && bun test src/api/graphApi.test.ts src/components/componentInteraction.test.tsx src/app.searchInspector.integration.test.tsx)` — PASS, `25 pass`.
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_parity_runner.py -q` — PASS, `17 passed`.
- `(cd api && bun test)` — PASS, `93 pass`.
- `(cd explorer && bun test && bun run lint && bun run build)` — PASS, `45 pass`, ESLint PASS, Vite build PASS with existing chunk-size warning.

## Generated Evidence Results

Run id: `20260427T044757Z` against source commit `6665c6a5`.

- Parity: PASS, `29/29` cases and `7/7` commands.
- Route inventory: PASS, `24` routes, `7/7` preview routes present, resolver route policy `guarded_default_off`, guarded resolver declarations `2`, unauthorized resolver routes `0`, mounted default resolver routes `false`.
- Resolver QA: PASS, `7/7` cases; result types `single_value=4`, `composed=1`, `conflict=1`, `none=1`.
- Boundary audit: PASS, `10/10` checks; no Neo4j writes, no KG rebuild, no protected ingest, no feature-flag cutover, no Explorer default adoption.
- Benchmark: PASS, `5/5` file-backed operations; runtime threshold disposition `not_evaluated_shadow_file_backed_only`; runtime thresholds not evaluated.
- Evidence manifest: PASS, `9` artifacts, `route_count=24`, `resolver_route_policy=guarded_default_off`, `benchmark_runtime_threshold_disposition=not_evaluated_shadow_file_backed_only`, `source_working_tree_dirty=false`, `source_dirty_path_count=0`.

## Advisory Review

- Gemini: command available at `/opt/homebrew/bin/gemini`, but review attempt failed with account/service 403 (`SERVICE_DISABLED`). No secrets were printed. Unavailable; not a blocker.
- Kimi: command available at `/Users/philiplewis/.local/bin/kimi`. Kimi reviewed commit `10e63fe4` and evidence run `20260427T043732Z`; finding: no safety violations, but stale `resolverRoutesUnmounted` references should be removed. That finding was accepted and fixed in commit `6665c6a5`, then fresh evidence was regenerated under run `20260427T044757Z`.

## Safety Invariant Confirmation

Confirmed after source and evidence generation:

- No unguarded or default-on `/v2/resolve*` behavior introduced.
- No Explorer browser-side `/v2/resolve*` calls introduced.
- No Neo4j writes, resets, reloads, backups, restores, or mutation introduced.
- No KG rebuild/reload/reset introduced.
- No protected source text, table, figure, dataset, clause, or local protected cache ingest introduced.
- No Explorer default graph adoption introduced.
- No default-on feature flag introduced.
- No runtime threshold pass/fail claim made; thresholds remain requirements only.
- Preview behavior remains opt-in and evidence-only.
- Generated artifacts remain file-backed and auditable.

## Residual Risks / Known Gaps

- Runtime threshold pass/fail claims remain blocked; benchmark evidence here is shadow/file-backed and observational only.
- Integration rollback proof remains planned, not executed; this is explicitly reported by benchmark/parity warnings and is not hidden.
- The Vite build still reports the pre-existing large chunk-size warning for `vis-network`.
- Broader Neo4j/live graph, protected-source admission, Explorer default adoption, and default-on feature flags remain gated by separate packets.

## Next Action

Commit this validation log and the `20260427T044757Z` generated evidence, refresh GitNexus, push to `origin/main`, then rebuild the AEC-MEPFS backlog from repo evidence for the next authorized slice.
