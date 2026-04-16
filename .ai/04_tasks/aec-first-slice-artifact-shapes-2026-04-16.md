---
task: aec-first-slice-artifact-shapes
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC First-Slice Artifact Shapes

## Purpose
This is the exact no-code handoff for the minimum runtime output file shapes expected from the bounded first slice.

## 1. Boundary DTO artifact
Root:
- `005_Operational-Intelligence-Layer/aec/candidates/first-slice/boundary/`

Minimum shape:
```json
{
  "artifact_type": "aec-boundary-payload",
  "schema_version": "v1",
  "snapshot_id": "...",
  "run_id": "...",
  "frame_id": "building-local-mm",
  "unit_system": "mm",
  "input_artifact_refs": [],
  "output_artifact_refs": [],
  "payload": {}
}
```

## 2. ECS snapshot artifact
Root:
- `005_Operational-Intelligence-Layer/aec/candidates/first-slice/ecs/`

Minimum shape:
```json
{
  "artifact_type": "aec-world-snapshot",
  "schema_version": "v1",
  "snapshot_id": "...",
  "world_revision_id": "...",
  "entity_count": 0,
  "component_families": [],
  "input_artifact_refs": [],
  "output_artifact_refs": []
}
```

## 3. Spatial fact bundle artifact
Root:
- `005_Operational-Intelligence-Layer/aec/candidates/first-slice/spatial/`

Minimum shape:
```json
{
  "artifact_type": "aec-spatial-fact-bundle",
  "schema_version": "v1",
  "snapshot_id": "...",
  "frame_id": "building-local-mm",
  "unit_system": "mm",
  "facts": [],
  "tolerance_class": "clearance-1mm"
}
```

## 4. Verification verdict artifact
Root:
- `005_Operational-Intelligence-Layer/aec/candidates/first-slice/verification/`

Minimum shape:
```json
{
  "artifact_type": "aec-verification-run",
  "schema_version": "v1",
  "verification_run_id": "...",
  "snapshot_id": "...",
  "rule_family": "scalar-min-max",
  "verdict": "sat",
  "refusal_reason": null,
  "witness_artifact": null,
  "unsat_artifact": null
}
```

## 5. Admitted artifact manifest
Root:
- `005_Operational-Intelligence-Layer/aec/admitted/first-slice/`

Minimum shape:
```json
{
  "artifact_type": "aec-admitted-manifest",
  "schema_version": "v1",
  "snapshot_id": "...",
  "admitted_artifact_refs": [],
  "source_candidate_refs": []
}
```

## 6. Promotion / audit manifest
Root:
- `006_System-Manifests/aec/promotions/first-slice/`

Minimum shape:
```json
{
  "artifact_type": "aec-promotion-audit",
  "schema_version": "v1",
  "promotion_run_id": "...",
  "input_artifact_refs": [],
  "output_artifact_refs": [],
  "status": "accepted"
}
```

## 7. Validation log minimum sections
Any future bounded-slice validation log must include:
- baseline used
- command matrix run
- artifact roots inspected
- out-of-scope file drift check
- final verdict

## Final rule
The implementation phase should not invent new output shapes for the bounded first slice without first updating this artifact contract. G10 still remains open until real files and tests exist.
