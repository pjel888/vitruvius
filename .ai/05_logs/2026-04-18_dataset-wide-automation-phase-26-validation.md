# 2026-04-18 Validation — Dataset-wide automation phase 26

## Change
- added one-command wrapper for the catalog-driven ready-family aggregate path:
  - `./run-ready-families-mvp-graph`

## Fresh verification
- catalog aggregate dry-run evidence already obtained via:
  - `python3 scripts/pipeline_cli.py run-completed-aggregate-from-catalog --catalog config/datasets/dataset-mvp-profile-catalog.yaml --status ready --dataset-id ready-family-aggregate --dataset-kind dataset-aggregate --out config/datasets/ready-family-aggregate.yaml --graph-output-root 005_Operational-Intelligence-Layer/graph/datasets/ready-family-aggregate --run-output-root 006_System-Manifests/runs/datasets/ready-family-aggregate --query-snapshot-template 005_Operational-Intelligence-Layer/graph/datasets/ready-family-aggregate/{run_id}_graph_snapshot.json --dry-run --review-preset m2-8gb-safe --skip-export-owl`
  - result:
    - `law_unit_count = 53`
    - `source_count = 70`
    - `concept_count = 97`
    - `relationship_count = 132`
    - `raw_slice_anchor_count = 46`
    - `planned_stage_count = 69`
    - `manual_review_required_count = 8`
    - `spot_review_required_count = 27`
    - `summary_auto_withheld_count = 27`
    - `shallow_representation_count = 4`
- one-command wrapper now exposes that same path as the operator surface for the combined ready-family graph

## Truthful result
- there is now a single wrapper command for the combined ready-family aggregate lane
- the remaining work is execute hardening and artifact review, not wrapper availability
