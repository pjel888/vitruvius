# AEC-MEPFS Neo4j Isolated Rehearsal Packet

```yaml
status: BOUNDARY_APPROVED_REHEARSAL_VALIDATION_ONLY
created: 2026-04-27
authority: project-owner-directive-four-gated-lanes
lane: neo4j-isolated-rehearsal-live-promotion-path
classification: GREEN_REHEARSAL_VALIDATION_AND_PROMOTION_PREP_ONLY
baseline_commit: 1296626e
production_live_promotion_authorized: false
primary_graph_mutation_authorized: false
```

## 1. Purpose

Complete repo-actionable Neo4j rehearsal and live-promotion preparation without
mutating the primary/live graph. This packet validates the existing isolated
dump/load proof and produces a live-promotion readiness checklist; it does not
promote, replace, reset, reload, or mutate Neo4j.

## 2. Authority and baseline

- Umbrella packet: `2026-04-27_four_gated_lanes_reopen_packet.md`.
- Prior isolated rehearsal evidence:
  `006_System-Manifests/aec-mepfs-backbone/rollback/20260425T144332Z/isolated-dump-load-rehearsal-report.json`.
- Prior rollback preflight evidence:
  `006_System-Manifests/aec-mepfs-backbone/rollback/20260425T130816Z/rollback-preflight-report.json`.
- Protected-source admission evidence:
  `006_System-Manifests/aec-mepfs-backbone/source-admission/20260427T121648Z/source-admission-report.json`.
- Runtime-root packet: `runtime-root-implementation-packet.md`.
- Verification contract: `verification-and-benchmark-contract.md`.

## 3. Allowed scope

- Validate prior isolated/stopped dump-load proof.
- Run read-only rollback preflight checks.
- Require rollback preflight `proof_status` to remain blocked/read-only.
- Bind the source-admission promotion gate to metadata-only/no-protected-ingest
  evidence instead of assuming clearance.
- Generate a Neo4j rehearsal readiness report under
  `006_System-Manifests/aec-mepfs-backbone/neo4j-rehearsal/<RUN_ID>/`.
- Create a live-promotion readiness packet with exact prerequisites and rollback
  transcript requirements.
- Add tests proving unsafe live-promotion states fail closed.

## 4. Explicitly blocked scope

- Destructive production Neo4j reset.
- Production primary graph replacement.
- KG rebuild/reload/reset that affects primary graph.
- Shadow-to-primary graph promotion.
- `MATCH (n) DETACH DELETE n`, `DROP DATABASE`, `CREATE OR REPLACE`, or similar
  destructive commands.
- Protected source ingest.
- Broad/global `LIVE_RUNTIME_AUTHORIZED`.

## 5. Verification plan

```bash
python3 -m compileall -q scripts/vitruvius/kg/backbone_neo4j_rehearsal.py
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_neo4j_rehearsal.py scripts/tests/test_kg_backbone_rollback_preflight.py -q
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_rollback_preflight --run-id <RUN_ID> --timeout-seconds 20
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_neo4j_rehearsal --run-id <RUN_ID> --rollback-preflight-report <generated rollback preflight>
git diff --check
```

## 6. Evidence artifacts

- Neo4j rehearsal readiness report:
  `006_System-Manifests/aec-mepfs-backbone/neo4j-rehearsal/<RUN_ID>/neo4j-rehearsal-readiness-report.json`
- Optional read-only rollback preflight report:
  `006_System-Manifests/aec-mepfs-backbone/rollback/<RUN_ID>/rollback-preflight-report.json`
- Validation log:
  `.ai/05_logs/2026-04-27_aec_mepfs_neo4j_rehearsal_validation.md`

## 7. Completion criteria

- Existing isolated rehearsal is validated as offline/throwaway with all steps
  successful and live Neo4j untouched.
- Rollback preflight remains explicitly blocked/read-only and does not execute
  backup/dump/load proof.
- Source-admission prerequisite is evidence-backed by a metadata-only/no
  protected-ingest report, or remains unsatisfied if that evidence is absent.
- Live-promotion readiness remains false until a future live-promotion packet
  records a fresh live backup/export, restore proof, graph-count diff, rollback
  transcript, shadow namespace load, and explicit promotion decision.
- No Neo4j mutation or KG rebuild occurs in this packet.
- No protected source content is ingested.

## 8. Next boundary

Production live graph promotion remains `UNSATISFIED_YELLOW`. The next packet may
prepare live-promotion decision criteria, but actual production replacement is
blocked until fresh backup/restore proof, graph diff, rollback transcript,
source-admission safety, and explicit scoped live-promotion authorization exist.
