# 2026-04-18 Validation — Dataset-wide automation phase 17

## Change
- added starter relationship-input scaffolding command:
  - `scaffold-completed-aggregate-lane-relationships`
- added bootstrap source→concept predicate to the relationship registry:
  - `covers`
- this lets a non-laws starter lane scaffold draft relationship inputs once starter canonical sources and concepts exist

## Fresh verification
- focused relationship-scaffold/regression suite:
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'scaffold_completed_aggregate_lane_canonical_rules_writes_generated_rules or load_rules_merges_generated_overlay or scaffold_completed_aggregate_lane_concepts_writes_concept_files or scaffold_completed_aggregate_lane_relationships_writes_relationship_files or pipeline_cli_scaffold_completed_aggregate_lane_canonical_rules_reports_summary or pipeline_cli_scaffold_completed_aggregate_lane_concepts_reports_summary or pipeline_cli_scaffold_completed_aggregate_lane_relationships_reports_summary or source_admit_completed_aggregate_lane_execute_updates_manifest or pipeline_cli_source_admit_completed_aggregate_lane_execute_reports_summary or source_admit_completed_aggregate_lane_dry_run_reports_candidates_or_blockers or pipeline_cli_source_admit_completed_aggregate_lane_dry_run_reports_status or prepare_completed_aggregate_lane_sources_dry_run_reports_inventory or prepare_completed_aggregate_lane_sources_execute_uses_prepare_helper or pipeline_cli_prepare_completed_aggregate_lane_sources_dry_run_reports_inventory or inspect_completed_aggregate_lane_sources_reports_inventory or pipeline_cli_inspect_completed_aggregate_lane_sources_reports_inventory or scaffold_completed_aggregate_lane_manifest_writes_starter_manifest or pipeline_cli_scaffold_completed_aggregate_lane_manifest_writes_manifest or check_completed_aggregate_family_readiness_reports_blockers or check_completed_aggregate_family_readiness_reports_ready_family or pipeline_cli_check_completed_aggregate_family_reports_blockers or admit_completed_manifest_to_family_updates_ledger_and_index or pipeline_cli_admit_completed_aggregate_manifest_updates_family_ledgers or scaffold_completed_aggregate_family_writes_starter_files or pipeline_cli_scaffold_completed_aggregate_family_writes_starter_files or register_completed_aggregate_family_writes_profile_and_catalog or pipeline_cli_register_completed_aggregate_family_writes_profile_and_catalog or resolve_completed_aggregate_profile_path_returns_registered_profile or pipeline_cli_build_completed_aggregate_manifest_writes_manifest or pipeline_cli_run_completed_aggregate_invokes_dataset_pipeline or pipeline_cli_build_completed_aggregate_from_profile_writes_manifest or pipeline_cli_run_completed_aggregate_from_profile_invokes_dataset_pipeline or pipeline_cli_run_completed_aggregate_family_invokes_dataset_pipeline or generic_completed_manifest_paths_returns_existing_manifests or build_laws_completed_aggregate_manifest or run_laws_completed_aggregate or raw_folder_name_override or manifest_scoped_variants or scoped_variants_for_duplicates' -q`
  - **39 passed**
- temporary non-laws relationship bootstrap demo:
  - scaffolded family: `history-demo`
  - scaffolded starter lane from a copied text-PDF under `002-History`
  - scaffolded canonical rule overlay with `core_concepts = [architectural history]`
  - seeded admitted starter source path
  - scaffolded concepts
  - scaffolded relationships with:
    - `python3 scripts/pipeline_cli.py scaffold-completed-aggregate-lane-relationships --manifest config/datasets/history-demo-lane.yaml --predicate covers`
  - surfaced:
    - `relationship_count = 1`
    - `predicate = covers`
    - `manifest_relationship_count = 1`
    - law-unit admitted relationship path:
      - `003_Canonical-Knowledge-Layer/shared/relationships/rel-handout-chinese-architecture-covers-concept-architectural-history.md`
- temporary demo artifacts and generated overlay entries were removed after validation so repo truth remains focused on committed families only

## Truthful result
- a starter non-laws lane can now bootstrap:
  - canonical sources
  - generated rules
  - draft concepts
  - draft relationship inputs
- this is the first point where a non-laws family has all the structural inputs needed to plausibly reach `ready_to_run = true` once a real family is admitted intentionally
