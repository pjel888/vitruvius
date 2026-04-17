# Active Context — Vitruvius

> **Updated:** 2026-04-17
> **Live branch:** `ralph/laws-dataset-phases`
> **Most recent completed work:** bounded laws pilot operator-experience hardening (`/.ai/05_logs/2026-04-17_laws-pilot-operator-experience-validation.md`)

## Live Repo Truth

- PASS 1 produced the audit pack, master implementation plan, baseline, research, and validation artifacts for the 2026-04-16 stabilization lane.
- PASS 2 is stabilization-only. It is focused on:
  1. truth/state reconciliation
  2. graph identity + query provenance trust
  3. advanced-boundary claim cleanup
  4. Rust/static validation hygiene
- The bounded laws pilot follow-on lane has now been hardened beyond the original scoped-graph proof:
  - `run-dataset-source-to-graph` supports one-command visualization/browser flow
  - `run-laws-pilot` and repo-root `./run-laws-pilot` exist for the 4-law pilot
  - generated graph HTML is self-contained and no longer depends on external/relative browser assets
- a readiness-only next-step lane now exists for broader all-laws planning:
  - `run-laws-all-dry-run`
  - `m2-8gb-safe` review preset
  - `run-laws-tranche-dry-run`
  - automated structure guardrails for BP220-style shallowness
- The 2026-04-15 sprint-wave summary remains historical context in `decisions.md` and `master-roadmap.md`; it is **not** the live dispatcher anymore.

## Current Validation Snapshot

- Python tests: **1572 passed, 1 skipped** (`PYTHONPATH=scripts pytest scripts/tests -q`)
- TypeScript tests: **21 passed** (`spatial-daemon`: `npm test`)
- Rust unit tests: **33 passed** total (`engine_rs` + `datalog_rs`)
- Rust static gates: **green** (`cargo fmt --all --check`, `cargo clippy --workspace --all-targets -- -D warnings`)
- Raw-layer pipeline baseline: `python3 scripts/pipeline_cli.py run` is clean on current corpus state (`350` files, `0` new, `0` changed, `0` missing)
- Graph integrity: `python3 scripts/pipeline_cli.py build-graph` now passes with warnings only; the duplicate canonical IRR source page was remediated in the follow-on fix pass
- Query provenance: `query` / `query-structured` now render real `source_section_id` + `evidence_snippet` when relationship evidence exists
- Bounded laws pilot:
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_graph_visualize_cli.py scripts/tests/test_dataset_source_to_graph_pipeline.py scripts/tests/test_canonicalize_body.py scripts/tests/test_canonicalize_integration.py scripts/tests/test_query_formatter.py -q`
  - **57 passed**
  - `./run-laws-pilot --dry-run` passes
  - `./run-laws-pilot --skip-export-owl --visualize` passes and emits a self-contained HTML artifact
- All-laws readiness slice:
  - `python3 -m pytest scripts/tests/test_config.py scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_dataset_source_to_graph_pipeline.py scripts/tests/test_graph_visualize_cli.py scripts/tests/test_canonicalize_body.py scripts/tests/test_canonicalize_integration.py scripts/tests/test_query_formatter.py -q`
  - **65 passed**
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-all-dry-run --review-preset m2-8gb-safe` passes
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-pilot --dry-run --review-preset m2-8gb-safe` passes
- Tranche-expansion slice:
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -q`
  - **10 passed**
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-dry-run --tranche-manifest config/datasets/laws-tranche-1.yaml --review-preset m2-8gb-safe` passes
  - all-laws readiness now reports `structure_guardrail_law_folders = [BP-220, BP-344, RA-9514]`
- Tranche source-preparation slice:
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -q`
  - **11 passed**
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-prep-dry-run --tranche-manifest config/datasets/laws-tranche-1.yaml` passes
  - current tranche-1 evidence:
    - `raw_file_count = 6`
    - `supported_direct_input_count = 6`
    - `refined_markdown_ready_count = 0`
- Tranche source-preparation execute slice:
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -q`
  - **12 passed**
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-prep --tranche-manifest config/datasets/laws-tranche-1.yaml` passes
  - current tranche-1 execute evidence:
    - `prepared_count = 5`
    - `ocr_required_count = 1`
    - `failed_count = 0`
- Tranche source-admission slice:
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -q`
  - **13 passed**
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-admission-dry-run --tranche-manifest config/datasets/laws-tranche-1.yaml` passes
  - current tranche-1 split:
    - ready: `PD-957`, `PD-1185`
    - blocked: `PD-1216`
- Tranche source-admission execute slice:
  - `python3 -m py_compile scripts/vitruvius/laws_readiness.py scripts/pipeline_cli.py scripts/vitruvius/cli_experience.py scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_canonical_rules_additional_laws.py`
  - **PASS**
  - `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py scripts/tests/test_dataset_pipeline_cli.py -k 'source_admission or pd_957 or pd_1185' -q`
  - **4 passed**
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-admission --tranche-manifest config/datasets/laws-tranche-1.yaml` passes
  - current execute evidence:
    - admitted: `PD-957`, `PD-1185`
    - blocked: `PD-1216`
    - `admitted_source_page_count = 2`
    - `canonicalize_failure_count = 0`
    - `PD-957` same-content raw aliases now collapse to one authoritative IRR source while excluded aliases remain explicit in the tranche manifest/report
- Duplicate-readiness slice:
  - `python3 -m py_compile scripts/vitruvius/laws_readiness.py scripts/pipeline_cli.py scripts/vitruvius/cli_experience.py scripts/tests/test_dataset_pipeline_cli.py`
  - **PASS**
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'run_laws_all_dry_run or run_laws_tranche_dry_run or run_laws_duplicate_dry_run' -q`
  - **4 passed**
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run --tranche-manifest config/datasets/laws-tranche-1.yaml` passes
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-all-dry-run --review-preset m2-8gb-safe` now surfaces:
    - `duplicate_cluster_count = 9`
    - duplicate-affected folders include `PD-957`, `PD-1096`, `RA-7160`, `RA-9266`
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-dry-run --tranche-manifest config/datasets/laws-tranche-1.yaml --review-preset m2-8gb-safe` now surfaces:
    - `duplicate_cluster_count = 1`
    - `duplicate_law_folders = [PD-957]`
- Tranche source-to-graph dry-run slice:
  - `python3 -m py_compile scripts/vitruvius/laws_readiness.py scripts/pipeline_cli.py scripts/vitruvius/cli_experience.py scripts/tests/test_dataset_pipeline_cli.py`
  - **PASS**
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_canonical_rules_additional_laws.py -k 'source_admission or source_to_graph_dry_run or run_laws_all_dry_run or run_laws_tranche_dry_run or run_laws_duplicate_dry_run or pd_957 or pd_1185' -q`
  - **9 passed**
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph-dry-run --tranche-manifest config/datasets/laws-tranche-1.yaml --review-preset m2-8gb-safe` passes
  - current dry-run evidence:
    - staged: `PD-957`, `PD-1185`
    - blocked: `PD-1216`
    - `planned_stage_count = 2`
    - `duplicate_law_folders = [PD-957]`
    - `shallow_representation_count = 0`
    - `source_to_graph_execute_ready = false`
- PD-957 concept-fit slice:
  - admitted concepts:
    - `floor-area`
    - `setbacks`
    - `yards`
  - admitted dataset-scoped `governs` relationships for the same three concepts
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_canonical_rules_additional_laws.py -k 'tranche_source_to_graph_dry_run or source_admission or pd_957 or pd_1185' -q`
  - **6 passed**
  - live tranche dry-run still keeps:
    - `source_to_graph_execute_ready = false`
- PD-1216 OCR-first preparation slice:
  - `python3 -m py_compile scripts/vitruvius/laws_readiness.py scripts/pipeline_cli.py scripts/vitruvius/cli_experience.py scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_canonical_rules_additional_laws.py`
  - **PASS**
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_canonical_rules_additional_laws.py -k 'prepare_raw_file_allow_ocr or tranche_source_to_graph_dry_run or pd_1216 or pd_957 or pd_1185' -q`
  - **6 passed**
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-prep --tranche-manifest config/datasets/laws-tranche-1.yaml --allow-ocr`
  - current OCR-first prep evidence:
    - `prepared_count = 6`
    - `ocr_required_count = 0`
    - `failed_count = 0`
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-admission --tranche-manifest config/datasets/laws-tranche-1.yaml --source-prep-report 006_System-Manifests/runs/datasets/laws-tranche-1/20260417T065723Z/laws_tranche_source_prep_report.json`
  - tranche source admission now admits:
    - `PD-957`
    - `PD-1216`
    - `PD-1185`
  - latest tranche source-to-graph dry-run:
    - `staged_law_folders = [PD-957, PD-1216, PD-1185]`
    - `blocked_law_folders = []`
    - `planned_stage_count = 3`
    - `shallow_representation_count = 0`
    - `source_to_graph_execute_ready = false`
- Tranche source-to-graph execute slice:
  - `python3 -m py_compile scripts/vitruvius/laws_readiness.py scripts/pipeline_cli.py scripts/vitruvius/cli_experience.py scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_canonical_rules_additional_laws.py`
  - **PASS**
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_canonical_rules_additional_laws.py -k 'tranche_source_to_graph_dry_run or tranche_source_to_graph_execute or prepare_raw_file_allow_ocr or pd_1216 or pd_957 or pd_1185' -q`
  - **7 passed**
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-1.yaml --review-preset m2-8gb-safe`
  - current execute evidence:
    - `staged_law_folders = [PD-957, PD-1216, PD-1185]`
    - `duplicate_law_folders = [PD-957]`
    - `generated_relationship_count = 2`
    - `filtered_relationship_count = 0`
    - `shallow_representation_count = 0`
    - `source_to_graph_execute_completed = true`
- Risk-hardening follow-on:
  - `python3 -m py_compile scripts/vitruvius/dataset_pipeline.py scripts/vitruvius/laws_readiness.py scripts/tests/test_dataset_source_to_graph_pipeline.py`
  - **PASS**
  - `python3 -m pytest scripts/tests/test_dataset_source_to_graph_pipeline.py scripts/tests/test_dataset_pipeline_cli.py -k 'source_to_graph or duplicate' -q`
  - **16 passed**
  - fresh tranche dry-run and execute now explicitly show:
    - `duplicate_law_folders = [PD-957]`
    - `raw_alias_law_folders = [PD-957]`
    - `guardrail_law_folders = [PD-957]`
    - `spot_review_required_count = 1`
    - `summary_auto_withheld_count = 1`
  - OCR-quality acceptance for `PD-1216` is now a spot-review path rather than a blind accept path

## Residual Graph Caveat

- `build-graph` is now green on errors, but still reports six orphan-node warnings that remain informational rather than blocking.

## Reference Map

- Governing plan: `/.ai/03_plans/00-governing-implementation-plan.md`
- PASS 2 master plan (archived): `/.ai/09_archive/plans/2026-04-16_master-audit-implementation-plan.md`
- PASS 1 validation: `/.ai/05_logs/2026-04-16_audit-pass-1-validation.md`
- PASS 2 validation: `/.ai/05_logs/2026-04-16_audit-pass-2-fix-validation.md`
- Duplicate-ID remediation plan (archived): `/.ai/09_archive/plans/2026-04-16_duplicate-canonical-source-id-remediation-plan.md`
- Active roadmap snapshot: `/.ai/01_roadmap/current-phase.md`
- Milestones: `/.ai/01_roadmap/milestone-tracker.md`
- Decisions: `/.ai/10_state/decisions.md`
- Latest bounded-laws operator validation: `/.ai/05_logs/2026-04-17_laws-pilot-operator-experience-validation.md`
- Latest all-laws readiness validation: `/.ai/05_logs/2026-04-17_all-laws-readiness-8gb-implementation-validation.md`
- Latest tranche-expansion validation: `/.ai/05_logs/2026-04-17_laws-tranche-expansion-implementation-validation.md`
- Latest tranche source-preparation validation: `/.ai/05_logs/2026-04-17_laws-tranche-source-prep-dry-run-validation.md`
- Latest tranche source-preparation execute validation: `/.ai/05_logs/2026-04-17_laws-tranche-source-prep-implementation-validation.md`
- Latest tranche source-admission validation: `/.ai/05_logs/2026-04-17_laws-tranche-1-source-admission-implementation-validation.md`
- Latest tranche source-admission execute validation: `/.ai/05_logs/2026-04-17_laws-tranche-1-source-admission-execution-validation.md`
- Latest duplicate-readiness validation: `/.ai/05_logs/2026-04-17_laws-duplicate-readiness-validation.md`
- Latest tranche source-to-graph dry-run validation: `/.ai/05_logs/2026-04-17_laws-tranche-source-to-graph-dry-run-validation.md`
- Latest PD-957 concept-fit validation: `/.ai/05_logs/2026-04-17_pd957-concept-fit-admission-validation.md`
- Latest PD-1216 OCR-first validation: `/.ai/05_logs/2026-04-17_pd1216-ocr-first-preparation-validation.md`
- Latest tranche source-to-graph execute validation: `/.ai/05_logs/2026-04-17_laws-tranche-source-to-graph-execute-validation.md`
- Latest risk-hardening validation: `/.ai/05_logs/2026-04-17_laws-risk-hardening-execution-validation.md`

## Handoff Note

If you continue from here, do **not** restart with a new repo-wide audit. Consult the **archived** 2026-04-16 stabilization/remediation plans together with the PASS 2 validation log and the duplicate-ID remediation validation log.
