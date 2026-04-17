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

## Handoff Note

If you continue from here, do **not** restart with a new repo-wide audit. Consult the **archived** 2026-04-16 stabilization/remediation plans together with the PASS 2 validation log and the duplicate-ID remediation validation log.
