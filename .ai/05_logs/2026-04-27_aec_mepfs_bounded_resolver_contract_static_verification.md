# AEC-MEPFS Bounded Resolver Contract Static Verification

**Date:** 2026-04-27
**Mode:** Ralph / Ultrawork / Team-assisted static implementation
**Scope:** BOUNDARY_APPROVED resolver-runtime contract/static-verification slice only
**Authority:** `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_bounded_resolver_runtime_contract_packet.md`

## Branch and commits

- Branch: `main`
- Starting commit: `690738c5`
- Ending commit: `618a659b`
- Upstream status before implementation: `main...origin/main`, clean and synced

## Working tree state

### Before

- `git status --short --branch`: `## main...origin/main`
- No tracked or untracked task files before implementation.

### After implementation before commit

Changed source/test/fixture files:

- `scripts/vitruvius/kg/backbone_contracts.py`
- `scripts/vitruvius/kg/backbone_resolver_qa.py`
- `scripts/vitruvius/kg/backbone_api_route_inventory.py`
- `scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json`
- `scripts/tests/test_kg_backbone_contracts.py`
- `scripts/tests/test_kg_backbone_resolver_qa.py`
- `scripts/tests/test_kg_backbone_api_route_inventory.py`

Generated evidence artifacts:

- `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260427T020853Z/api-route-inventory-report.json`
- `006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260427T020853Z/resolver-qa-report.json`

Validation log:

- `.ai/05_logs/2026-04-27_aec_mepfs_bounded_resolver_contract_static_verification.md`

## Files inspected

- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_bounded_resolver_runtime_contract_packet.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/runtime-governance-admission-packet.md`
- `scripts/vitruvius/kg/backbone_contracts.py`
- `scripts/vitruvius/kg/backbone_resolver_qa.py`
- `scripts/vitruvius/kg/backbone_api_route_inventory.py`
- `scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json`
- `scripts/tests/test_kg_backbone_contracts.py`
- `scripts/tests/test_kg_backbone_resolver_qa.py`
- `scripts/tests/test_kg_backbone_api_route_inventory.py`
- `api/v2Backbone.test.ts`
- `api/index.ts` route inventory through static scanner

## Implementation scope

Implemented the smallest static/no-op slice authorized by the bounded packet:

1. Extended static resolver contract validation:
   - request shape: `query.text`, context IDs, jurisdiction filters, discipline filters, trace flag
   - result shape: result type, confidence class, canonical node refs, source refs, fallback reason, trace-safe rationale
   - error shape: invalid input, malformed request, missing fixture artifact, blocked runtime route, deterministic no-result
2. Extended safe non-protected fixture coverage in `valid_readiness_s2.json`:
   - golden cases: `single_value`, `composed`, `conflict`, `none`
   - error cases: `invalid_input`, `malformed_request`, `missing_fixture_artifact`, `blocked_runtime_route`, `deterministic_no_result`
3. Hardened static route inventory:
   - `/v2/resolve` and every `/v2/resolve/` child path are forbidden
   - explicit `forbiddenResolveRoutes` list is emitted in route inventory output
4. Extended resolver QA report:
   - `error_summary`
   - `contract_surface`
   - preview route preservation summary
5. Added focused tests for:
   - resolver contract request/result/error coverage
   - malformed static error requests
   - `/v2/resolve/context` child-route detection
   - v2 parity route rejection for `/v2/resolve/context`

## Explicit blocked scope preserved

Confirmed no work performed in these blocked areas:

- no `/v2/resolve`, `/v2/resolve/trace`, or `/v2/resolve*` API route mounting
- no API hot resolver invocation
- no Neo4j write/reset/reload/backup/restore/mutation
- no KG rebuild/reload/reset
- no protected source text, table, figure, dataset, or clause ingest
- no Explorer default graph adoption
- no Explorer default perspective change
- no automatic preview fetch
- no default-on feature flag or hidden cutover behavior
- no runtime latency threshold claim
- no edits to HIGH/CRITICAL runtime roots: `CanonicalNode`, `TaxonomyLoader`, `Neo4jLoader`

## GitNexus / code-impact evidence

- `npx --yes gitnexus@1.6.2-rc.10 status`
  - repository indexed and up to date at `690738c`
- Impact checks run before editing relevant symbols:
  - `run_resolver_qa_fixture`: HIGH risk due to direct resolver QA test/CLI fanout; no runtime processes affected
  - `_evaluate_resolver_case`: LOW risk; direct caller is static QA runner
  - `_summarize_case_results`: LOW risk; direct caller is static QA runner
  - `_validate_resolver_golden_case`: HIGH fanout through contract validator tests and static consumers; no runtime processes affected
  - `_has_forbidden_resolver_route`: LOW risk; direct route inventory/static consumers
  - `_route_boundary_errors`: LOW risk; direct route inventory consumer
  - `_is_forbidden_v2_parity_route`: HIGH fanout through contract validator tests; no runtime processes affected

HIGH risk notices were accepted only because the affected surfaces are static contract/test/report consumers and were fully covered by focused tests.

## Commands run

```bash
git status --short --branch
git rev-parse --short HEAD
git rev-parse --abbrev-ref HEAD
git log -1 --oneline
npx --yes gitnexus@1.6.2-rc.10 status
omx explore --prompt "Map the AEC-MEPFS bounded resolver-runtime contract/static-verification surfaces..."
npx --yes gitnexus@1.6.2-rc.10 impact run_resolver_qa_fixture --repo vitruvius --direction upstream --include-tests --depth 3
npx --yes gitnexus@1.6.2-rc.10 impact _evaluate_resolver_case --repo vitruvius --direction upstream --include-tests --depth 3
npx --yes gitnexus@1.6.2-rc.10 impact _summarize_case_results --repo vitruvius --direction upstream --include-tests --depth 3
npx --yes gitnexus@1.6.2-rc.10 impact _validate_resolver_golden_case --repo vitruvius --direction upstream --include-tests --depth 3
npx --yes gitnexus@1.6.2-rc.10 impact _has_forbidden_resolver_route --repo vitruvius --direction upstream --include-tests --depth 3
npx --yes gitnexus@1.6.2-rc.10 impact _route_boundary_errors --repo vitruvius --direction upstream --include-tests --depth 3
npx --yes gitnexus@1.6.2-rc.10 impact _is_forbidden_v2_parity_route --repo vitruvius --direction upstream --include-tests --depth 3
git diff --check
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_resolver_qa.py -q
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_api_route_inventory.py -q
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py -q
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_resolver_qa.py scripts/tests/test_kg_backbone_api_route_inventory.py -q
(cd api && bun test v2Backbone.test.ts)
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_placement_qa.py scripts/tests/test_kg_backbone_parity_runner.py scripts/tests/test_kg_backbone_shadow_evidence_manifest.py scripts/tests/test_kg_backbone_shadow_boundary_audit.py scripts/tests/test_kg_backbone_shadow_benchmark.py -q
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_api_route_inventory --run-id 20260427T020853Z
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_resolver_qa --run-id 20260427T020853Z
rg -n "app\.(get|post|put|delete|patch|all)\s*\(\s*['\"]\/v2\/resolve" api/index.ts || true
rg -n "/v2/resolve|resolve/trace" api explorer scripts --glob '!**/*.md' || true
rg -n "LIVE_RUNTIME_AUTHORIZED" .ai api explorer scripts || true
git diff --name-only | rg "(CanonicalNode|TaxonomyLoader|Neo4jLoader|neo4j_loader|taxonomy_loader|schemas\.py)" || true
git diff -U0 | rg -n "MATCH \(n\) DETACH DELETE|DETACH DELETE|neo4j.*write|Neo4jLoader|TaxonomyLoader|CanonicalNode|run-kg-pipeline|--reset|protected ingest|protected content|Explorer default|default-on|runtime threshold" || true
```

## Test results

- `git diff --check`: passed
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_resolver_qa.py -q`: 20 passed
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_api_route_inventory.py -q`: 12 passed
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py -q`: 47 passed
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_resolver_qa.py scripts/tests/test_kg_backbone_api_route_inventory.py -q`: 32 passed
- `(cd api && bun test v2Backbone.test.ts)`: 60 passed
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_placement_qa.py scripts/tests/test_kg_backbone_parity_runner.py scripts/tests/test_kg_backbone_shadow_evidence_manifest.py scripts/tests/test_kg_backbone_shadow_boundary_audit.py scripts/tests/test_kg_backbone_shadow_benchmark.py -q`: 69 passed
- Verifier subagent: PASS; no must-fix issues

## Evidence artifact metrics

### Route inventory

Path: `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260427T020853Z/api-route-inventory-report.json`

- `ok`: true
- `route_count`: 22
- `preview_routes_present`: 7
- `preview_routes_required`: 7
- `missing_preview_routes`: []
- `resolve_route_mounted`: false
- `trace_route_mounted`: false
- `forbiddenResolveRoutes`: []

### Resolver QA

Path: `006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260427T020853Z/resolver-qa-report.json`

- `ok`: true
- golden cases: 4 total / 4 passed
- result types: `single_value`, `composed`, `conflict`, `none`
- error cases: 5 total / 5 passed
- error types: `invalid_input`, `malformed_request`, `missing_fixture_artifact`, `blocked_runtime_route`, `deterministic_no_result`
- request contract surface: query text, context IDs, discipline filters, trace flag all covered
- result contract surface: canonical node refs, confidence classes, source refs, fallback reason, trace-safe rationale all covered
- preview route preservation: 7/7 routes present

## Gemini review

Attempted with installed Gemini CLI:

```bash
gemini --approval-mode plan -p "Review this Vitruvius AEC-MEPFS bounded resolver-runtime contract/static-verification diff..."
```

Result: unavailable. Gemini returned HTTP 403 because the account service is disabled. No model review output was available. This is documented as non-blocking under the packet.

## Kimi review

Attempted twice with installed Kimi CLI:

```bash
kimi --work-dir . --quiet --agent default -p "Review this Vitruvius AEC-MEPFS bounded resolver-runtime contract/static-verification diff..."
kimi --work-dir . --quiet --model kimi-code/kimi-for-coding -p "Review this bounded AEC-MEPFS static/no-op resolver contract slice..."
```

Result: unavailable within execution window. Both attempts timed out before returning review findings. This is documented as non-blocking under the packet.

## Native subagent review

A Codex verifier subagent reviewed the diff and returned PASS.

Key findings:

- changed files remain limited to static contract, fixture, QA, and route inventory tests/reports
- no edits to `CanonicalNode`, `TaxonomyLoader`, or `Neo4jLoader`
- static fixture validation and resolver QA pass
- route inventory detects `/v2/resolve`, `/v2/resolve/trace`, `/v2/resolve/context`, and deeper `/v2/resolve/context/detail`
- no requested verification gaps found

## Safety invariant confirmation

- No `/v2/resolve*` route is mounted: confirmed by static grep and route inventory `forbiddenResolveRoutes: []`.
- No hot resolver is called from API: no API files changed; `api/index.ts` route mount grep returned empty.
- No Neo4j mutation introduced: no Neo4j loader/API mutation files changed and dangerous-operation diff grep returned empty.
- No KG rebuild/reload/reset introduced: no pipeline files changed and dangerous-operation diff grep returned empty.
- No protected content ingest introduced: fixture text is synthetic metadata-only; dangerous diff grep returned empty.
- No Explorer default adoption introduced: no Explorer files changed.
- No default-on feature flag introduced: no config or flag files changed.
- No runtime threshold claim made: no benchmark/runtime threshold files changed.
- File-backed preview routes remain present and sanitized: API tests and route inventory pass.
- HIGH/CRITICAL runtime roots untouched: changed-file grep returned empty for `CanonicalNode`, `TaxonomyLoader`, `Neo4jLoader` roots.

## Residual risks

- Route inventory still scans direct Hono `app.<method>(...)` declarations in `api/index.ts`; if future code introduces nested routers or generated route modules, the inventory must be widened before relying on it for runtime admission.
- Existing `scripts/vitruvius/config_flags.py` contains a historical comment mentioning `POST /v2/resolve`, but no code path or API route was changed in this slice.
- Gemini and Kimi advisory reviews did not complete due to external auth/timeout issues; native Codex verifier and local tests covered the same safety questions.

## Exact next safe step

After this commit, the next safe step is **not** live resolver mounting. Prepare the next governance packet for either:

1. a deeper static resolver fixture/trace runner that remains file-backed and unmounted, or
2. a separate runtime packet proposing explicit `/v2/resolve*` mount preconditions, rollback proof, and Neo4j/KG isolation requirements.

Until such a packet is approved, `/v2/resolve*`, Neo4j/KG mutation, protected ingest, Explorer default adoption, and runtime threshold claims remain blocked.
