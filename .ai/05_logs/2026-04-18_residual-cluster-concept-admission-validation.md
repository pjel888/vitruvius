---
task: residual-cluster-concept-admission
created: 2026-04-18
status: complete
---

# Validation — residual cluster concept admission

## Goal
Reduce the remaining residual orphan/partial ready-family laws by admitting a small safe concept bundle into the tranche manifests and rebuilding the aggregates.

## Implementation
- Added reusable CLI/operator surface:
  - `python3 scripts/pipeline_cli.py admit-concepts-to-manifest --manifest <manifest> --folder-name <folder> --concept-path <path> ...`
- Added helper:
  - `vitruvius.aggregate_manifest.admit_concepts_to_manifest()`
- Admitted concepts:
  - RA-9285: `arbitration`, `mediation`, `mediator`
  - RA-6969: `chemical-substance`, `chemical-mixture`, `hazardous-wastes`
  - RA-1378: `master-plumber`
- Re-canonicalized affected source pages so their `Referenced Concepts` sections reflect the admitted concepts.

## Verification
- `python3 -m pytest scripts/tests/test_concept_candidate_suggestions.py scripts/tests/test_concept_matching.py -q`
  - 7 passed
- `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'admit_concepts_to_manifest or concept_candidate or scaffold_completed_aggregate_lane_concepts_reports_summary' -q`
  - 3 passed
- rebuilt:
  - `build-laws-completed-aggregate-manifest`
  - `build-completed-aggregate-from-catalog ... ready-family-aggregate ...`
  - `build-graph --dataset-manifest config/datasets/ready-family-aggregate.yaml`

## Result
### Before concept admission (`20260418T021054Z`)
- `node_count = 136`
- `edge_count = 270`
- `warning_count = 4`
- `covered_folder_count = 42`
- `partial_folder_count = 4`
- orphan nodes:
  - ADR Act
  - Civil Code
  - Plumbing Law
  - Toxic Wastes Act

### After concept admission (`20260418T023807Z`)
- `node_count = 143`
- `edge_count = 266`
- `warning_count = 1`
- `covered_folder_count = 45`
- `partial_folder_count = 1`
- remaining orphan / partial law:
  - `law-civil-code-of-the-philippines`
  - `RA-386`

## Interpretation
The residual cluster is now reduced to essentially one law family (`RA-386`). RA-9285, RA-6969, and RA-1378 were blocked by missing admitted concepts, and the new manifest-admission path successfully moved them into the aggregate graph without fabricating stronger relationships.
