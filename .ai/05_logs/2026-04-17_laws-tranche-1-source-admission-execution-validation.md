# 2026-04-17 Laws Tranche-1 Source Admission Execution Validation

## Scope
Execute tranche-1 source admission conservatively after the tranche source-preparation and source-admission dry-run checkpoints.

## Changes
- `scripts/vitruvius/laws_readiness.py`
  - deduplicated the tranche source-admission helpers
  - added duplicate/raw-alias guardrails for prepared tranche files
  - excluded study-aid variants from authoritative admission
  - added `run_laws_tranche_source_admission(...)`
  - updated tranche manifest writing so admitted, excluded, and blocked state remain explicit
- `scripts/pipeline_cli.py`
  - wired `run-laws-tranche-source-admission`
- `scripts/vitruvius/cli_experience.py`
  - documented the execute step for tranche source admission
- `scripts/vitruvius/rules/canonical_rules.yaml`
  - added canonical rules for `PD-957` IRR and `PD-1185` law admission
- `scripts/tests/test_canonical_rules_additional_laws.py`
  - added rule coverage for `PD-957` and `PD-1185`
- `scripts/tests/test_dataset_pipeline_cli.py`
  - updated tranche source-admission dry-run coverage to use realistic tranche filenames
  - added execute coverage for duplicate-collapse and blocked-state retention
- `config/datasets/laws-tranche-1.yaml`
  - now records explicit source-admission outcomes for `PD-957`, `PD-1185`, and `PD-1216`
- `003_Canonical-Knowledge-Layer/shared/sources/revised-implementing-rules-and-regulations-for-pd-957.md`
  - newly admitted canonical source page
- `003_Canonical-Knowledge-Layer/shared/sources/fire-code-of-the-philippines.md`
  - newly admitted canonical source page

## Verification
- `python3 -m py_compile scripts/vitruvius/laws_readiness.py scripts/pipeline_cli.py scripts/vitruvius/cli_experience.py scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_canonical_rules_additional_laws.py`
- `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py scripts/tests/test_dataset_pipeline_cli.py -k 'source_admission or pd_957 or pd_1185' -q`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-admission-dry-run --tranche-manifest config/datasets/laws-tranche-1.yaml`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-admission --tranche-manifest config/datasets/laws-tranche-1.yaml`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-admission-dry-run --tranche-manifest config/datasets/laws-tranche-1.yaml`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-dry-run --tranche-manifest config/datasets/laws-tranche-1.yaml --review-preset m2-8gb-safe`

## Fresh evidence
- targeted tests:
  - `4 passed, 15 deselected`
- execute summary:
  - `admitted_source_page_count = 2`
  - `canonicalize_failure_count = 0`
  - `blocked_law_folders = [PD-1216]`
- admitted source pages:
  - `003_Canonical-Knowledge-Layer/shared/sources/revised-implementing-rules-and-regulations-for-pd-957.md`
  - `003_Canonical-Knowledge-Layer/shared/sources/fire-code-of-the-philippines.md`
- `PD-957` guardrail evidence:
  - exact duplicate raw variants collapsed to one representative with SHA-256 `1f9ab17a8168...`
  - duplicate law/IRR filename semantics remain explicit in the tranche manifest and execution report
  - excluded variants include:
    - study-aid slide deck
    - two duplicate raw aliases
- post-execute tranche manifest state:
  - `PD-957` → `source_admission_state: admitted`
  - `PD-1185` → `source_admission_state: admitted`
  - `PD-1216` → `source_admission_state: blocked_pending_ocr`
- post-execute dry-run still reports:
  - ready: `PD-957`, `PD-1185`
  - blocked: `PD-1216`
  - `candidate_source_page_count = 2`
  - `excluded_prepared_count = 3`
  - `source_to_graph_execute_ready = false`

## Conclusion
Tranche-1 source admission is now executed truthfully for the ready tranche members.
The repo now admits `PD-957` and `PD-1185` at the canonical source layer while:
- collapsing duplicate raw variants
- preserving excluded study-aid / alias variants explicitly
- keeping `PD-1216` visibly blocked pending OCR
- keeping tranche source→graph execution gated until the next accepted slice.
