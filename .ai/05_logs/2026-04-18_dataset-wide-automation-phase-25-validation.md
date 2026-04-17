# 2026-04-18 Validation — Dataset-wide automation phase 25

## Change
- added catalog-driven aggregate build/run surfaces:
  - `build-completed-aggregate-from-catalog`
  - `run-completed-aggregate-from-catalog`
- these allow all ready dataset families to be aggregated through one reusable command path
- also hardened the helper layer so catalog manifest discovery only requires each family profile's ledger/index fields instead of the full runtime profile contract

## Fresh verification
- focused catalog-aggregate/regression suite:
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'completed_manifest_paths_from_catalog_filters_ready_profiles or pipeline_cli_build_completed_aggregate_from_catalog_writes_manifest or pipeline_cli_run_completed_aggregate_from_catalog_invokes_dataset_pipeline or update_completed_aggregate_family_catalog_entry_updates_status or suggest_completed_aggregate_family_candidates_ranks_text_pdfs_first or pipeline_cli_suggest_completed_aggregate_family_candidates_reports_summary or scaffold_completed_aggregate_lane_manifest_honors_explicit_raw_paths or pipeline_cli_scaffold_completed_aggregate_lane_manifest_honors_raw_path or scaffold_completed_aggregate_lane_manifest_uses_ranked_default_candidates or pipeline_cli_scaffold_completed_aggregate_lane_manifest_uses_ranked_default_candidates or bootstrap_completed_aggregate_family_lane_orchestrates_steps or pipeline_cli_bootstrap_completed_aggregate_family_lane_reports_summary or promote_completed_aggregate_lane_relationships_updates_status or pipeline_cli_promote_completed_aggregate_lane_relationships_reports_summary or scaffold_completed_aggregate_lane_canonical_rules_writes_generated_rules or load_rules_merges_generated_overlay or scaffold_completed_aggregate_lane_concepts_writes_concept_files or scaffold_completed_aggregate_lane_relationships_writes_relationship_files or pipeline_cli_scaffold_completed_aggregate_lane_canonical_rules_reports_summary or pipeline_cli_scaffold_completed_aggregate_lane_concepts_reports_summary or pipeline_cli_scaffold_completed_aggregate_lane_relationships_reports_summary or source_admit_completed_aggregate_lane_execute_updates_manifest or pipeline_cli_source_admit_completed_aggregate_lane_execute_reports_summary or source_admit_completed_aggregate_lane_dry_run_reports_candidates_or_blockers or pipeline_cli_source_admit_completed_aggregate_lane_dry_run_reports_status or prepare_completed_aggregate_lane_sources_dry_run_reports_inventory or prepare_completed_aggregate_lane_sources_execute_uses_prepare_helper or pipeline_cli_prepare_completed_aggregate_lane_sources_dry_run_reports_inventory or inspect_completed_aggregate_lane_sources_reports_inventory or pipeline_cli_inspect_completed_aggregate_lane_sources_reports_inventory or scaffold_completed_aggregate_lane_manifest_writes_starter_manifest or pipeline_cli_scaffold_completed_aggregate_lane_manifest_writes_manifest or check_completed_aggregate_family_readiness_reports_blockers or check_completed_aggregate_family_readiness_reports_ready_family or pipeline_cli_check_completed_aggregate_family_reports_blockers or admit_completed_manifest_to_family_updates_ledger_and_index or pipeline_cli_admit_completed_aggregate_manifest_updates_family_ledgers or scaffold_completed_aggregate_family_writes_starter_files or pipeline_cli_scaffold_completed_aggregate_family_writes_starter_files or register_completed_aggregate_family_writes_profile_and_catalog or pipeline_cli_register_completed_aggregate_family_writes_profile_and_catalog or resolve_completed_aggregate_profile_path_returns_registered_profile or pipeline_cli_build_completed_aggregate_manifest_writes_manifest or pipeline_cli_run_completed_aggregate_invokes_dataset_pipeline or pipeline_cli_build_completed_aggregate_from_profile_writes_manifest or pipeline_cli_run_completed_aggregate_from_profile_invokes_dataset_pipeline or pipeline_cli_run_completed_aggregate_family_invokes_dataset_pipeline or generic_completed_manifest_paths_returns_existing_manifests or build_laws_completed_aggregate_manifest or run_laws_completed_aggregate or raw_folder_name_override or manifest_scoped_variants or scoped_variants_for_duplicates' -q`
  - **53 passed**
- registry suite:
  - `python3 -m pytest scripts/tests/test_registry_load.py -q`
  - **3 passed**
- catalog aggregate dry-run across ready families:
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
    - `benchmark_hint_count = 5`

## Truthful result
- we now have a reusable way to aggregate every family currently marked `ready` into one combined manifest/run path
- this is a major step toward the user's all-dataset interconnectedness goal, even though the combined graph still carries the accumulated quality caveats of the included families
