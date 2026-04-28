# AEC-MEPFS Taxonomy Domain Expansion And Explorer Spacing Validation

```yaml
status: VALIDATED
created: 2026-04-28
branch: main
start_commit: df8232d9
end_commit: c2f0a349
run_id: 20260428T053531Z
authority_packet: .ai/03_plans/AEC-MEPFS-Backbone/2026-04-28_aec_mepfs_taxonomy_domain_expansion_and_spacing_packet.md
gemini_used: false
kimi_status: completed_with_actionable_findings_resolved
spark_status: unavailable_rate_limited_during_repo_lookup
```

## Scope

This validation covers a rights-safe, file-backed expansion of the AEC-MEPFS
Backbone taxonomy plus Explorer usability fixes for the larger graph.

Implemented scope:

- Added five new L1 roots: `SAN`, `SEC`, `SMS`, `HRC`, and `LAW`.
- Expanded the admitted backbone fixture to 984 BackboneNode records, 960
  `broader_than` relationships, 24 roots, 240 L2 topics, and 720 L3 subtopics.
- Added `generation_method` to synthesized taxonomy rows so batch-synthesized,
  steward-governed topic families are not confused with protected source payload
  admissions.
- Regenerated shadow staging, consumer, route inventory, and Explorer interaction
  evidence for run `20260428T053531Z`.
- Fixed Explorer minimap snapshots so node-type filters update the minimap by
  excluding filtered or hidden nodes.
- Added an interactive Explorer graph spread slider with clamp helpers and an
  explicit reset-to-default control.

Blocked scope preserved:

- no protected source text, clauses, tables, figures, datasets, or protected local
  caches;
- no Neo4j write/reset/reload/promotion/cleanup;
- no KG rebuild/reload/reset;
- no production graph promotion;
- no broad/global `LIVE_RUNTIME_AUTHORIZED` change;
- no Gemini use;
- no secret, token, credential, database URL, or private connection string output.

## Files inspected

- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/master-roadmap.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-28_aec_mepfs_taxonomy_domain_expansion_and_spacing_packet.md`
- `api/v2Backbone.test.ts`
- `explorer/src/app.searchInspector.integration.test.tsx`
- `explorer/src/components/GraphScene.tsx`
- `explorer/src/components/componentInteraction.test.tsx`
- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/components/graph/VisNetworkHost.test.ts`
- `explorer/src/stores/useSceneStore.ts`
- `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- `scripts/tests/test_kg_backbone_contracts.py`

## Files changed

- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/master-roadmap.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-28_aec_mepfs_taxonomy_domain_expansion_and_spacing_packet.md`
- `.ai/05_logs/2026-04-28_aec_mepfs_taxonomy_domain_expansion_and_spacing_validation.md`
- `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260428T053531Z/api-route-inventory-report.json`
- `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260428T053531Z/explorer-domain-expansion-spacing-report.json`
- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T053531Z/shadow-backbone-graph.json`
- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T053531Z/shadow-backbone-staging.json`
- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T053531Z/shadow-staging-consumer-report.json`
- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T053531Z/shadow-staging-report.json`
- `api/v2Backbone.test.ts`
- `explorer/src/app.searchInspector.integration.test.tsx`
- `explorer/src/components/GraphScene.tsx`
- `explorer/src/components/componentInteraction.test.tsx`
- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/components/graph/VisNetworkHost.test.ts`
- `explorer/src/components/graph/layoutSpread.ts`
- `explorer/src/components/graph/overviewSnapshot.ts`
- `explorer/src/stores/useSceneStore.ts`
- `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- `scripts/tests/test_kg_backbone_contracts.py`

## Generated artifacts

- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T053531Z/shadow-backbone-staging.json`
- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T053531Z/shadow-backbone-graph.json`
- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T053531Z/shadow-staging-report.json`
- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T053531Z/shadow-staging-consumer-report.json`
- `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260428T053531Z/api-route-inventory-report.json`
- `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260428T053531Z/explorer-domain-expansion-spacing-report.json`

## Commands run

```bash
git status --short --branch
git rev-parse --short HEAD
git log --oneline -n 8
omx explore --prompt "Find the Explorer graph host, minimap, filter, AEC-MEPFS fixture, and current evidence files for taxonomy expansion and graph spacing work."
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_staging --repo-root . --run-id 20260428T053531Z --backbone-nodes scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_report_reader --repo-root . --run-id 20260428T053531Z
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_api_route_inventory --repo-root . --run-id 20260428T053531Z
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_api_route_inventory.py -q
bun --cwd api test v2Backbone.test.ts
bun --cwd explorer test src/components/componentInteraction.test.tsx src/components/graph/VisNetworkHost.test.ts
bun --cwd api test
bun --cwd explorer test
cd explorer && bun run lint && bun run build
git diff --check
git diff --unified=0 -- .ai/01_roadmap .ai/03_plans/AEC-MEPFS-Backbone api/v2Backbone.test.ts explorer/src scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json scripts/tests/test_kg_backbone_contracts.py 006_System-Manifests/aec-mepfs-backbone | rg -n '^\+.*(MATCH \(n\) DETACH DELETE|DETACH DELETE|DROP DATABASE|CREATE OR REPLACE|Neo4jLoader|TaxonomyLoader|CanonicalNode|run-kg-pipeline|--reset|--reload|LIVE_RUNTIME_AUTHORIZED|protected ingest|protected content|KG rebuild|KG reload|KG reset|production graph promotion|secret|credential)' || true
```

## Results

- Focused Python AEC tests: `70 passed`.
- Focused API test: `69 pass, 0 fail`.
- Focused Explorer component/graph tests: `32 pass, 0 fail`.
- Full API tests: `102 pass, 0 fail`.
- Full Explorer tests: `58 pass, 0 fail`.
- Explorer lint: passed.
- Explorer production build: passed. Vite retained the existing `vis-network`
  chunk-size warning.
- `git diff --check`: passed.
- Safety diff grep: no destructive Neo4j/KG/protected-source additions. The only
  added matches were blocked-scope documentation and rights-safe Security topic
  labels containing the word `credential`.

## Kimi advisory review

Kimi/Moonshot was available and completed a read-only advisory review. Findings
and resolution:

1. Stale root counts in two Explorer evidence preview fixtures: fixed from 19 to
   24 and covered by full Explorer tests.
2. Spread control lacked an explicit reset path: fixed with a reset-to-default
   UI control and store-level regression coverage.
3. Synthesized taxonomy rows could be mistaken for individually written source
   payload admissions: fixed by adding `generation_method` to synthesized rows
   and a Python contract regression check.
4. Rights-safe expansion, minimap refresh, protected payload exposure, and
   Neo4j/KG mutation checks were reported clean.

## Safety invariant confirmation

- Protected content ingest: false.
- Neo4j mutation: false.
- KG rebuild/reload/reset: false.
- Production graph promotion: false.
- Generated reports are file-backed and shadow/read-only.
- New taxonomy labels are high-level topic labels only.
- Explorer graph spread reset is a local UI/layout control and does not alter
  backend data or runtime authority.

## Residual risks

- The admitted fixture is intentionally large. Rollback is by git revert; the
  earlier `20260428T033525Z` evidence run remains a historical comparison point.
- Manual browser profiling on a real display was not run in this terminal-only
  pass.
- The production build retains the pre-existing Vite `vis-network` chunk-size
  warning.

## GitNexus/code-impact note

`npx gitnexus --help | head -80` was attempted before commit to discover the
local detect-changes CLI surface. The npm-installed `gitnexus@1.6.3` command
failed during startup with:

```text
Cannot destructure property 'package' of 'node.target' as it is null.
```

The session therefore used focused source inspection, route inventory evidence,
full affected test suites, and post-commit `./scripts/gitnexus_analyze.sh` as the
available repo safety path.

Commit hook evidence for `c2f0a349`: analyzed 24 changed files, found 12 changed functions/classes, 0 affected flows, 8 test gaps, and overall risk score 0.75.
