# 2026-04-18 Validation — Dataset-wide automation phase 15

## Change
- added starter canonical-rule scaffolding command:
  - `scaffold-completed-aggregate-lane-canonical-rules`
- added canonical rule overlay loading so generated starter rules can participate in canonical planning/admission without editing the base rules file:
  - `config/datasets/canonical_rules.generated.yaml`

## Fresh verification
- focused canonical-rule-scaffold/regression suite:
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'scaffold_completed_aggregate_lane_canonical_rules_writes_generated_rules or load_rules_merges_generated_overlay or pipeline_cli_scaffold_completed_aggregate_lane_canonical_rules_reports_summary or source_admit_completed_aggregate_lane_execute_updates_manifest or pipeline_cli_source_admit_completed_aggregate_lane_execute_reports_summary or source_admit_completed_aggregate_lane_dry_run_reports_candidates_or_blockers or pipeline_cli_source_admit_completed_aggregate_lane_dry_run_reports_status or prepare_completed_aggregate_lane_sources_dry_run_reports_inventory or prepare_completed_aggregate_lane_sources_execute_uses_prepare_helper or pipeline_cli_prepare_completed_aggregate_lane_sources_dry_run_reports_inventory or inspect_completed_aggregate_lane_sources_reports_inventory or pipeline_cli_inspect_completed_aggregate_lane_sources_reports_inventory or scaffold_completed_aggregate_lane_manifest_writes_starter_manifest or pipeline_cli_scaffold_completed_aggregate_lane_manifest_writes_manifest or check_completed_aggregate_family_readiness_reports_blockers or check_completed_aggregate_family_readiness_reports_ready_family or pipeline_cli_check_completed_aggregate_family_reports_blockers or admit_completed_manifest_to_family_updates_ledger_and_index or pipeline_cli_admit_completed_aggregate_manifest_updates_family_ledgers or scaffold_completed_aggregate_family_writes_starter_files or pipeline_cli_scaffold_completed_aggregate_family_writes_starter_files or register_completed_aggregate_family_writes_profile_and_catalog or pipeline_cli_register_completed_aggregate_family_writes_profile_and_catalog or resolve_completed_aggregate_profile_path_returns_registered_profile or pipeline_cli_build_completed_aggregate_manifest_writes_manifest or pipeline_cli_run_completed_aggregate_invokes_dataset_pipeline or pipeline_cli_build_completed_aggregate_from_profile_writes_manifest or pipeline_cli_run_completed_aggregate_from_profile_invokes_dataset_pipeline or pipeline_cli_run_completed_aggregate_family_invokes_dataset_pipeline or generic_completed_manifest_paths_returns_existing_manifests or build_laws_completed_aggregate_manifest or run_laws_completed_aggregate or raw_folder_name_override or manifest_scoped_variants or scoped_variants_for_duplicates' -q`
  - **35 passed**
- temporary non-laws end-to-end demo:
  - scaffolded family: `history-demo`
  - scaffolded starter lane from a copied text-PDF under `002-History`
  - prepared source outputs
  - scaffolded starter canonical rule overlay with:
    - `source_type = handout`
    - `trust_level = secondary`
  - executed starter source admission
  - surfaced:
    - `scaffolded_rule_count = 1`
    - `admission_status = admitted`
    - `admitted_source_page_count = 1`
    - `canonical_source_count = 1`
    - admitted source path on the law unit:
      - `003_Canonical-Knowledge-Layer/shared/sources/chinese-architecture.md`
- temporary `history-demo` artifacts, copied raw file, conversion outputs, generated overlay entries, and canonical outputs were removed after validation so repo truth remains focused on committed families only

## Truthful result
- a starter non-laws lane can now move from:
  - raw inventory
  - to prepared output
  - to generated canonical rule overlay
  - to admitted canonical source page
- the remaining missing step is now even narrower and genuinely domain-truth-bound:
  - admitted concepts and relationship inputs for a first true non-laws family
