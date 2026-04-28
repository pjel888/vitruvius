# AEC-MEPFS Actual Implementation / Cutover Packet

```yaml
status: BOUNDARY_APPROVED_ACTUAL_IMPLEMENTATION
created: 2026-04-27
executed: 2026-04-28
authority: project-owner-directive-actual-aec-mepfs-implementation-cutover
previous_closure_was_prep_only: true
prep_only_closure_sufficient: false
broad_global_live_runtime_authorized: false
gemini_used: false
```

## Purpose

Move AEC-MEPFS from prep-only/rehearsal-only/readiness-only closure into actual
implementation where local repo gates allow it. The prior four-lane closure
remains useful evidence, but it is not the final implementation state.

This packet authorizes actual local implementation/cutover for:

1. Runtime resolver implementation and mounting.
2. Explorer AEC-MEPFS default behavior.
3. Runtime threshold adoption for implemented runtime surfaces.
4. Neo4j live graph promotion only if live credentials, target identity,
   backup/restore proof, graph diff, and rollback transcript exist.
5. Protected source content admission only if valid legal/steward/source-rights
   authority exists.

## Non-Negotiable Boundaries

- Do not grant broad/global `LIVE_RUNTIME_AUTHORIZED`.
- Do not print secrets, tokens, database URLs, API keys, or environment values.
- Do not mutate production Neo4j without production target identity, fresh
  backup/export, isolated restore proof, graph-count diff, rollback transcript,
  and named-surface promotion authorization.
- Do not rebuild/reload/reset a primary KG graph without the same rollback proof.
- Do not ingest or expose protected text, tables, figures, datasets, clauses, or
  local protected caches without source-specific legal/steward/source-rights
  authority.
- Do not use Gemini.
- Treat Kimi/Moonshot and Spark as advisory only; verify accepted findings with
  repo tests.

## Lane Classifications

| Lane | Final status | Reason |
| --- | --- | --- |
| Runtime resolver implementation | `IMPLEMENTED_AND_VERIFIED` | `/v2/resolve` and `/v2/resolve/trace/:trace_id` are mounted by default over deterministic file-backed, non-protected artifacts with explicit rollback disable values for `VITRUVIUS_AEC_MEPFS_RESOLVER_RUNTIME`. |
| Explorer default adoption | `IMPLEMENTED_AND_VERIFIED` | `/explore` is AEC-MEPFS-first from the prelaunch file-backed cutover, while legacy graph behavior remains available through the documented selector/escape path and tests. |
| Runtime threshold adoption | `IMPLEMENTED_AND_VERIFIED` for implemented API-local resolver runtime; broader external/browser/Neo4j thresholds hard-blocked | Run `20260428T004350Z` benchmarks actual default-on `/v2/resolve*` Hono handlers in process and emits pass/fail threshold evidence. External server, Explorer browser, and Neo4j-backed thresholds require runtime surfaces that are not locally credentialed/promoted. |
| Neo4j live graph promotion | `BLOCKED_BY_MISSING_PRODUCTION_CREDENTIALS` | Existing rehearsal/readiness evidence does not identify a production target, credentials, fresh live backup/export, isolated restore against the target, graph-count diff, or prewritten rollback transcript. No live mutation was performed. |
| Protected source content admission | `BLOCKED_BY_MISSING_EXTERNAL_AUTHORITY` | Existing legal/steward admission records authorize metadata/reference/no-ingest use only. No source-specific authority clears protected payload ingestion or exposure. |

## Implementation Scope

### Runtime Resolver

- Make `VITRUVIUS_AEC_MEPFS_RESOLVER_RUNTIME` default-on for prelaunch.
- Preserve rollback with explicit disabled values: `0`, `false`, `no`, `off`,
  and `disabled`.
- Keep the resolver deterministic, file-backed, non-LLM, non-Neo4j-mutating, and
  fail-closed.
- Preserve single-value, composed, conflict, none, invalid-input, missing
  artifact, and trace cases through actual API handlers.

### Explorer Default

- Preserve the AEC-MEPFS-first file-backed Explorer default already implemented
  by the prelaunch cutover.
- Keep legacy graph behavior accessible.
- Keep preview labels truthful: preview surfaces do not mutate Neo4j or force
  live graph adoption.

### Runtime Thresholds

- Adopt pass/fail threshold evidence only for the implemented API-local
  default-on resolver route harness.
- Keep global AEC runtime thresholds false until external server, Explorer
  browser, Neo4j-backed, and production live graph paths exist and are measured.
- Reject shadow-only benchmark evidence as runtime threshold proof.

### Neo4j Live Promotion

- Do not run production destructive commands.
- Do not promote to a primary/live namespace.
- Preserve existing readiness proof as blocker evidence only.

### Protected Sources

- Do not ingest protected payloads.
- Preserve metadata-only/no-ingest proof as blocker evidence only.

## Verification Matrix

Required checks:

- `git diff --check`
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_api_route_inventory.py scripts/tests/test_kg_backbone_runtime_thresholds.py -q`
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_api_route_inventory.py scripts/tests/test_kg_backbone_runtime_thresholds.py scripts/tests/test_kg_backbone_source_admission.py scripts/tests/test_kg_backbone_neo4j_rehearsal.py scripts/tests/test_kg_backbone_shadow_evidence_manifest.py scripts/tests/test_kg_backbone_shadow_benchmark.py -q`
- `(cd api && bun test)`
- `(cd explorer && bun test src/app.searchInspector.integration.test.tsx src/components/componentInteraction.test.tsx src/api/graphApi.test.ts src/utils/explorerRuntime.test.ts)`
- `(cd explorer && bun run lint)`
- `(cd explorer && bun run build)`

## Evidence Artifacts

- Route inventory:
  `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260428T004350Z/api-route-inventory-report.json`
- Runtime benchmark:
  `006_System-Manifests/aec-mepfs-backbone/runtime-resolver-benchmark/20260428T004350Z/runtime-resolver-benchmark-report.json`
- Runtime threshold adoption:
  `006_System-Manifests/aec-mepfs-backbone/runtime-thresholds/20260428T004350Z/runtime-threshold-adoption-report.json`
- Actual implementation status:
  `006_System-Manifests/aec-mepfs-backbone/runtime-implementation/20260428T004350Z/actual-implementation-status-report.json`
- Final closure:
  `006_System-Manifests/aec-mepfs-backbone/final-implementation-closure/20260428T004350Z/final-actual-implementation-closure-report.json`

## Completion Criteria

This packet is complete only when:

1. Runtime resolver implementation is `IMPLEMENTED_AND_VERIFIED`.
2. Explorer default adoption is `IMPLEMENTED_AND_VERIFIED`.
3. Runtime thresholds are `IMPLEMENTED_AND_VERIFIED` for implemented runtime
   surfaces and hard-blocked for unavailable surfaces.
4. Neo4j live graph promotion is either `IMPLEMENTED_WITH_ROLLBACK_READY` or
   hard-blocked with an exact credential/safety reason.
5. Protected content admission is either `IMPLEMENTED_AND_VERIFIED` for
   authorized sources or `BLOCKED_BY_MISSING_EXTERNAL_AUTHORITY`.
6. No lane is closed as prep-only, metadata-only, rehearsal-only, readiness-only,
   or complete-to-repo-actionable-scope without a hard blocker.
7. Verification evidence and closure docs are committed and pushed.
