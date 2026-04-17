# 2026-04-18 Validation — Dataset-wide automation phase 22

## Change
- fixed starter-lane scaffolding and one-command bootstrap to honor explicit raw-file selection:
  - `--raw-path <repo-relative-raw-file>`
- this removes a practical failure mode where a mixed-quality raw root could pick the wrong first file and produce a misleading family-level blocker

## Fresh verification
- focused selector/regression suite:
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'scaffold_completed_aggregate_lane_manifest_honors_explicit_raw_paths or pipeline_cli_scaffold_completed_aggregate_lane_manifest_honors_raw_path or bootstrap_completed_aggregate_family_lane_orchestrates_steps or pipeline_cli_bootstrap_completed_aggregate_family_lane_reports_summary or promote_completed_aggregate_lane_relationships_updates_status or pipeline_cli_promote_completed_aggregate_lane_relationships_reports_summary or scaffold_completed_aggregate_lane_canonical_rules_writes_generated_rules or load_rules_merges_generated_overlay or scaffold_completed_aggregate_lane_concepts_writes_concept_files or scaffold_completed_aggregate_lane_relationships_writes_relationship_files or pipeline_cli_scaffold_completed_aggregate_lane_canonical_rules_reports_summary or pipeline_cli_scaffold_completed_aggregate_lane_concepts_reports_summary or pipeline_cli_scaffold_completed_aggregate_lane_relationships_reports_summary or source_admit_completed_aggregate_lane_execute_updates_manifest or pipeline_cli_source_admit_completed_aggregate_lane_execute_reports_summary or source_admit_completed_aggregate_lane_dry_run_reports_candidates_or_blockers or pipeline_cli_source_admit_completed_aggregate_lane_dry_run_reports_status or prepare_completed_aggregate_lane_sources_dry_run_reports_inventory or prepare_completed_aggregate_lane_sources_execute_uses_prepare_helper or pipeline_cli_prepare_completed_aggregate_lane_sources_dry_run_reports_inventory or inspect_completed_aggregate_lane_sources_reports_inventory or pipeline_cli_inspect_completed_aggregate_lane_sources_reports_inventory or scaffold_completed_aggregate_lane_manifest_writes_starter_manifest or pipeline_cli_scaffold_completed_aggregate_lane_manifest_writes_manifest or check_completed_aggregate_family_readiness_reports_blockers or check_completed_aggregate_family_readiness_reports_ready_family or pipeline_cli_check_completed_aggregate_family_reports_blockers or admit_completed_manifest_to_family_updates_ledger_and_index or pipeline_cli_admit_completed_aggregate_manifest_updates_family_ledgers or scaffold_completed_aggregate_family_writes_starter_files or pipeline_cli_scaffold_completed_aggregate_family_writes_starter_files or register_completed_aggregate_family_writes_profile_and_catalog or pipeline_cli_register_completed_aggregate_family_writes_profile_and_catalog or resolve_completed_aggregate_profile_path_returns_registered_profile or pipeline_cli_build_completed_aggregate_manifest_writes_manifest or pipeline_cli_run_completed_aggregate_invokes_dataset_pipeline or pipeline_cli_build_completed_aggregate_from_profile_writes_manifest or pipeline_cli_run_completed_aggregate_from_profile_invokes_dataset_pipeline or pipeline_cli_run_completed_aggregate_family_invokes_dataset_pipeline or generic_completed_manifest_paths_returns_existing_manifests or build_laws_completed_aggregate_manifest or run_laws_completed_aggregate or raw_folder_name_override or manifest_scoped_variants or scoped_variants_for_duplicates' -q`
  - **45 passed**
- raw-path steering evidence on a mixed technology root:
  - default first-file bootstrap selected a poor candidate and stayed blocked / not ready
  - explicit-file bootstrap using:
    - `001_Raw-Source-Layer/004-Technology/Architectural Cost Estimates By Max Fajardo.pdf`
    reached:
    - `completed_lane_count = 1`
    - `resolved_manifest_count = 1`
    - `source_count = 1`
    - `concept_count = 1`
    - `relationship_count = 1`
    - `ready_to_run = true`
  - execute then showed a still-truthful caveat:
    - source quality remained review-heavy / shallow for that selected lane

## Truthful result
- the automation path now supports explicit operator steering when a family root mixes strong and weak candidates
- this is not a shortcut around truth; it is a way to choose the best authoritative candidate without reshaping the filesystem first
- the remaining work for a future technology-family proof is content quality / review hardening, not raw-path selection plumbing
