# AEC-MEPFS Neo4j Rehearsal Validation

```yaml
created: 2026-04-27
lane: neo4j-isolated-rehearsal-live-promotion-path
packet: .ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_neo4j_isolated_rehearsal_packet.md
classification: GREEN_REHEARSAL_VALIDATION_AND_PROMOTION_PREP_ONLY
starting_branch: main
starting_commit: 1296626e
ending_commit: pending_commit_that_includes_this_log
run_id: 20260427T122953Z
```

## Scope

Validate existing offline/throwaway Neo4j dump-load rehearsal evidence and fresh
read-only rollback preflight evidence without mutating the primary/live graph.
Prepare live-promotion prerequisites, but keep production live graph promotion
blocked.

## Files inspected

- `.ai/03_plans/AEC-MEPFS-Backbone/final-aec-mepfs-closure-packet.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_final_closure_and_state_reconciliation_packet.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_four_gated_lanes_reopen_packet.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_protected_source_admission_packet.md`
- `006_System-Manifests/aec-mepfs-backbone/rollback/20260425T144332Z/isolated-dump-load-rehearsal-report.json`
- `006_System-Manifests/aec-mepfs-backbone/source-admission/20260427T121648Z/source-admission-report.json`
- `scripts/vitruvius/kg/backbone_rollback_preflight.py`
- `scripts/tests/test_kg_backbone_rollback_preflight.py`

## Files changed

- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_neo4j_isolated_rehearsal_packet.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_neo4j_live_promotion_readiness_packet.md`
- `.ai/05_logs/2026-04-27_aec_mepfs_neo4j_rehearsal_validation.md`
- `scripts/vitruvius/kg/backbone_neo4j_rehearsal.py`
- `scripts/tests/test_kg_backbone_neo4j_rehearsal.py`
- `006_System-Manifests/aec-mepfs-backbone/rollback/20260427T122953Z/rollback-preflight-report.json`
- `006_System-Manifests/aec-mepfs-backbone/neo4j-rehearsal/20260427T122953Z/neo4j-rehearsal-readiness-report.json`

## Generated evidence

- Read-only rollback preflight:
  `006_System-Manifests/aec-mepfs-backbone/rollback/20260427T122953Z/rollback-preflight-report.json`
- Neo4j rehearsal readiness:
  `006_System-Manifests/aec-mepfs-backbone/neo4j-rehearsal/20260427T122953Z/neo4j-rehearsal-readiness-report.json`

Key report facts:

- `ok: true`
- `status.isolatedRehearsalVerified: true`
- `status.readOnlyPreflightAvailable: true`
- `status.livePromotionReady: false`
- `status.productionLivePromotionAuthorized: false`
- `status.primaryGraphMutationAuthorized: false`
- `destructive_command_matches: []`
- rollback preflight `proof_status: blocked_runtime_stopped_or_isolated_database_required`
- rollback preflight `destructive_operations_executed: false`
- rollback preflight `backup_dump_load_executed: false`
- source-admission input is evidence-backed by
  `006_System-Manifests/aec-mepfs-backbone/source-admission/20260427T121648Z/source-admission-report.json`
- source-admission gate confirms metadata-only/no-protected-ingest evidence:
  `content_ingest_rows: 0`, `protected_payload_key_hits: 0`,
  `protectedContentIngestAuthorized: false`

## Commands run

```bash
git status --short --branch
git rev-parse --short HEAD
git log --oneline -n 12
command -v codex || true
codex --help 2>/dev/null | head -80 || true
command -v kimi || true
command -v moonshot || true
command -v llm || true
command -v aider || true
command -v opencode || true
python3 -m compileall -q scripts/vitruvius/kg/backbone_neo4j_rehearsal.py
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_neo4j_rehearsal.py -q
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_neo4j_rehearsal.py scripts/tests/test_kg_backbone_rollback_preflight.py -q
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_rollback_preflight --run-id 20260427T122953Z --timeout-seconds 20
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_neo4j_rehearsal --run-id 20260427T122953Z --rollback-preflight-report 006_System-Manifests/aec-mepfs-backbone/rollback/20260427T122953Z/rollback-preflight-report.json
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_runtime_thresholds.py scripts/tests/test_kg_backbone_explorer_default_adoption.py scripts/tests/test_kg_backbone_source_admission.py scripts/tests/test_kg_backbone_neo4j_rehearsal.py -q
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_neo4j_rehearsal.py scripts/tests/test_kg_backbone_rollback_preflight.py scripts/tests/test_kg_backbone_source_admission.py -q
git diff --check
rg -n "MATCH \(n\) DETACH DELETE|DETACH DELETE|DROP DATABASE|CREATE OR REPLACE|run-kg-pipeline|--reset|--reload|Neo4jLoader|TaxonomyLoader|CanonicalNode" scripts/vitruvius/kg/backbone_neo4j_rehearsal.py scripts/tests/test_kg_backbone_neo4j_rehearsal.py .ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_neo4j_isolated_rehearsal_packet.md .ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_neo4j_live_promotion_readiness_packet.md || true
```

## Test results

- `scripts/tests/test_kg_backbone_neo4j_rehearsal.py`: `10 passed`
- Neo4j rehearsal + rollback preflight: `17 passed`
- Focused four-lane Python tests: `60 passed`
- Neo4j rehearsal + rollback preflight + source admission: `26 passed`
- `git diff --check`: passed

## Review results

### Spark / GPT-5.3-Codex-Spark

Initial Spark review found two valid issues:

1. Rollback preflight gate did not require blocked `proof_status`.
2. Source-admission live-promotion gate was hardcoded true instead of
   evidence-backed.

Both findings were fixed:

- `preflight_proof_status_blocks_runtime` check added and covered by regression.
- source-admission evidence is now optional/evidence-backed; missing evidence
  leaves the gate unsatisfied, unsafe evidence fails the report, and the real
  run binds to the metadata-only source-admission report.

Final Spark review after fixes: no findings. It verified that rollback
preflight `proof_status` is checked, source-admission gating is evidence-backed,
no Neo4j mutation or KG rebuild/reset path was introduced, live-promotion flags
remain false, and direct regression tests pass (`10 passed`).

### Kimi / Moonshot

Kimi was attempted twice without Gemini:

- Full diff review: timed out after 90 seconds with no usable output.
- Short conceptual review: timed out after 45 seconds with no usable output.

Kimi unavailability is non-blocking per the project-owner directive.

## Safety invariants

Confirmed for this lane:

- no broad/global `LIVE_RUNTIME_AUTHORIZED`
- no production live promotion
- no primary graph mutation authorization
- no destructive production Neo4j reset
- no `MATCH (n) DETACH DELETE n`, `DROP DATABASE`, or `CREATE OR REPLACE`
  executed
- no KG rebuild/reload/reset
- no protected source ingest
- no protected payload exposure
- source-admission promotion gate is evidence-backed, not assumed
- live promotion remains `UNSATISFIED_YELLOW`

## Residual risks / blocked work

Production live graph promotion remains blocked until a future dedicated packet
records, before mutation:

- fresh live backup/export,
- isolated restore proof,
- pre/post graph-count diff,
- shadow namespace/database load,
- current API/Explorer parity for the promoted surface,
- rollback transcript,
- scoped live-promotion authorization.

## Next action

Commit this Neo4j rehearsal validation slice, push it, then reconcile all four
lanes in the final four-lane closure packet.
