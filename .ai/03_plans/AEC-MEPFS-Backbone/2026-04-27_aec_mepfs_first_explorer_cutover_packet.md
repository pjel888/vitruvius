# AEC-MEPFS First Explorer Cutover Packet

```yaml
status: BOUNDARY_APPROVED
created: 2026-04-27
authority: project-owner-directive-prelaunch-aec-mepfs-forward
scope: explorer-and-api-file-backed-aec-mepfs-default-cutover
baseline_commit: 96455a3e
broad_live_runtime_authorized: false
production_neo4j_promotion_authorized: false
protected_content_ingest_authorized: false
kg_rebuild_reload_reset_authorized: false
explorer_default_adoption_authorized: true
legacy_default_preservation_required: false
```

## 1. Project-owner decision

The project owner explicitly reopened the Explorer/default-taxonomy direction after
four-lane closure and stated that Vitruvius is pre-launch, legacy graph behavior is
not a product constraint, and the intended direction is to proceed with the
AEC-MEPFS taxonomy.

This packet therefore supersedes only the previous **Explorer default adoption
blocked** boundary for a bounded, file-backed AEC-MEPFS-first cutover. It does not
turn on broad live runtime authorization and does not authorize protected content
admission, destructive graph mutation, or primary Neo4j promotion.

## 2. Allowed scope

- Make AEC-MEPFS the default Explorer perspective for `/explore` with no query
  parameter.
- Add a file-backed AEC-MEPFS perspective adapter for
  `GET /perspective/aec-mepfs/nodes`.
- Route AEC-MEPFS default search, node detail, edge detail, expansion, path,
  taxonomy-tree, and health/dev-readiness surfaces to sanitized file-backed AEC
  artifacts where practical.
- Keep legacy perspectives accessible as secondary/pre-cutover snapshots.
- Update HomeScreen copy and entry points to communicate AEC-MEPFS-first product
  behavior.
- Update focused API and Explorer tests proving default cutover, preview
  separation, sanitized payloads, and no Neo4j/protected-content mutation.
- Update state docs and evidence logs so the planning surface stops claiming the
  default cutover is still blocked.

## 3. Blocked scope preserved

- No broad/global `LIVE_RUNTIME_AUTHORIZED` status.
- No production Neo4j reset, replacement, promotion, write, or cleanup.
- No KG rebuild/reload/reset affecting the primary graph.
- No protected source text/table/figure/dataset/clause ingest or exposure.
- No default-on hidden resolver runtime expansion beyond existing guarded
  resolver behavior.
- No runtime threshold claims beyond previously scoped resolver benchmark
  evidence.
- No secret/environment printing.

## 4. Implementation plan

1. Add an API-side AEC-MEPFS graph adapter that converts the existing shadow graph
   into Explorer `GraphNode[]` / `GraphEdge[]` shape.
2. Add safe AEC default routes/branches for graph load and related Explorer
   interactions without calling Neo4j for AEC IDs.
3. Change Explorer default constants from `default` to `aec-mepfs`.
4. Update HomeScreen and URL canonicalization so `/explore` means AEC-MEPFS.
5. Keep explicit legacy snapshot access under `default`.
6. Add focused tests and validation evidence.

## 5. Rollback

Rollback is a git revert of the cutover commit. No external data store, primary
Neo4j namespace, protected-content cache, or KG build output is mutated by this
packet.

## 6. Completion criteria

- `/explore` loads `aec-mepfs` by default and keeps the canonical URL clean.
- `GET /perspective/aec-mepfs/nodes` returns sanitized file-backed AEC graph
  nodes and edges.
- AEC search/detail/expand/path/taxonomy/health surfaces use file-backed
  artifacts and do not require Neo4j for AEC IDs or the default dev launcher.
- Existing AEC preview panel remains explicit and does not replace graph state.
- Focused API and Explorer tests pass.
- `git diff --check`, safety greps, Explorer lint/build, and API tests pass.
- Evidence log and adoption report exist.
- Working tree is clean after commit and push.
