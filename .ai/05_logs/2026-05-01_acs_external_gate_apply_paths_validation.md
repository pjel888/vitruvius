# ACS External Gate Apply Paths Validation

Date: 2026-05-01

## Scope

Implemented all remaining repo-actionable external-gate work as file-backed dry-run/preflight tooling. This pass does not admit numerical criteria, ingest protected payloads, mutate canonical labels, apply aliases, write migrations, connect to Neo4j, or promote production graph data.

## Implemented

- Added steward duplicate decision packet validation.
- Added `steward-duplicate-apply-plan-dry-run.json` output for validated or blocked duplicate-apply intent.
- Added protected payload manifest validation for hash-only/source-rights metadata.
- Added live promotion plan validation requiring production target, backup artifact, restore-test artifact, and rollback transcript paths.
- Added CLI flags for steward decision, criteria packet, authority ledger, protected payload manifest, live promotion plan, and rollback proof inputs.
- Added packet path-escape rejection, persisted report schema checks, and packet template documentation.

## Latest report

- `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-gated-review/20260501T090200Z_ACS_EXTERNAL_GATE_APPLY_PATHS_DRY_RUN/architecture-civil-structural-gated-review-report.json`
- `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-gated-review/20260501T090200Z_ACS_EXTERNAL_GATE_APPLY_PATHS_DRY_RUN/steward-duplicate-apply-plan-dry-run.json`

## Validation commands

- `$env:PYTHONPATH='scripts'; python -m pytest -q scripts/tests/test_kg_architecture_civil_structural_gate_review.py` - 20 passed.
- `$env:PYTHONPATH='scripts'; python -m pytest -q scripts/tests/test_kg_architecture_civil_structural_enrichment.py scripts/tests/test_kg_architecture_civil_structural_gate_review.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_resolver_qa.py scripts/tests/test_kg_backbone_graph_quality.py scripts/tests/test_kg_backbone_shadow_staging.py` - 116 passed.
- `$env:PYTHONPATH='scripts'; python -m vitruvius.kg.architecture_civil_structural_gate_review --run-id 20260501T090200Z_ACS_EXTERNAL_GATE_APPLY_PATHS_DRY_RUN` - passed, 0 errors.
- `bun test api` - 118 passed, 0 failed.
- `bun test explorer` - 106 passed, 0 failed.
- `python` JSON syntax check for `docs/knowledge-graph/architecture-civil-structural-prd.json` - passed.
- `git diff --check` - passed with existing line-ending warnings only.
- `bash ./scripts/refresh_code_intelligence.sh` - GitNexus already up to date; ChunkHound processed 16 changed files with 0 file errors; code-review-graph rebuilt the graph but reported the known missing `tree-sitter-yaml` parser warnings and embedding-service `_Task.elapsed` errors.
- `npx.cmd --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius --scope all` - measured HIGH risk across the broader dirty workspace: 16 files, 82 symbols, 8 affected execution flows, including AEC-MEPFS node/detail and shadow-path flows.
- `uvx --with tree-sitter-yaml code-review-graph detect-changes --repo . --brief` - analyzed 24 changed files; 0 changed functions/classes, 0 affected flows, 0 test gaps, overall risk score 0.00.
- `chunkhound search --regex "steward_duplicate_decision_gate|protected_payload_manifest_gate|live_promotion_plan|steward-duplicate-apply-plan-dry-run|ACS_EXTERNAL_GATE_APPLY_PATHS_DRY_RUN"` - indexed the new gate/apply-path terms in state, docs, tests, code, and reports.

## Architect review

- Architect verifier: APPROVED.
- Condition: final reporting must describe this as dry-run/preflight tooling and must not imply duplicate merge, alias application, numeric criteria admission, protected payload ingest, or production promotion is complete.
- Risk note: GitNexus HIGH risk reflects the broader dirty API/shadow workspace and was measured; code-review-graph found 0 affected flows for the current changed-file set.

Post-review spot check:

- `$env:PYTHONPATH='scripts'; python -m pytest -q scripts/tests/test_kg_architecture_civil_structural_gate_review.py` - 20 passed after doc/state updates.

## Hard-blocker readiness automation follow-up

Run `20260501T094300Z_ACS_EXTERNAL_GATE_READINESS_BUNDLE` adds always-generated draft skeleton artifacts for the remaining external gates:

- `steward-preserve-packet-skeleton.json`
- `criteria-packet-skeleton.json`
- `authority-ledger-skeleton.json`
- `protected-payload-manifest-skeleton.json`
- `live-promotion-plan-skeleton.json`
- `external-gate-readiness-bundle.json`

The skeletons are generated from repo-known facts and required schemas only. They leave steward, AHJ, legal/source-rights, payload-hash, credential, backup, restore-test, and rollback fields empty rather than fabricating them. The root `.gitignore` now ignores `.env.local` and `.env.*.local`, and `.env.example` lists blank production Neo4j variable names for operators.

Additional validation:

- `$env:PYTHONPATH='scripts'; python -m pytest -q scripts/tests/test_kg_architecture_civil_structural_gate_review.py` - 23 passed.
- `$env:PYTHONPATH='scripts'; python -m vitruvius.kg.architecture_civil_structural_gate_review --run-id 20260501T094300Z_ACS_EXTERNAL_GATE_READINESS_BUNDLE` - passed, 0 errors, wrote readiness skeletons and bundle.
- `$env:PYTHONPATH='scripts'; python -m pytest -q scripts/tests/test_kg_architecture_civil_structural_enrichment.py scripts/tests/test_kg_architecture_civil_structural_gate_review.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_resolver_qa.py scripts/tests/test_kg_backbone_graph_quality.py scripts/tests/test_kg_backbone_shadow_staging.py` - 119 passed.
- `bun test api` - 118 passed, 0 failed.
- `bun test explorer` - 106 passed, 0 failed.
- JSON syntax checks for the PRD, latest gated-review report, and latest readiness bundle - passed.
- `git diff --check` - passed with line-ending warnings only.
- Post-change `bash ./scripts/refresh_code_intelligence.sh` - GitNexus already up to date; ChunkHound processed 21 changed files with 0 file errors; code-review-graph rebuilt with known missing `tree-sitter-yaml` warnings and embedding-service `_Task.elapsed` errors.
- `npx.cmd --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius --scope all` - measured HIGH risk across the broader dirty workspace: 18 files, 82 symbols, 8 affected execution flows.
- `uvx --with tree-sitter-yaml code-review-graph detect-changes --repo . --brief` - analyzed 25 changed files; 0 changed functions/classes, 0 affected flows, 0 test gaps, overall risk score 0.00.
- `chunkhound search --regex "readiness_artifact_paths|external-gate-readiness-bundle|steward-preserve-packet-skeleton|PRODUCTION_NEO4J_CREDENTIAL_NAMES"` - found the new readiness terms in state, manifests, docs, tests, and gate-review code.

Architect follow-up:

- Architect verifier: APPROVED.
- Condition: describe the result as conversion of hard blockers into draft readiness skeletons and a readiness bundle, not as solved external authority or production readiness.
- Scope caveat: GitNexus HIGH risk remains broader dirty-workspace context; code-review-graph reported 0 affected flows/test gaps for the current changed-file set.

## Boundaries maintained

- `canonical_label_mutation`: false.
- `alias_application_performed`: false.
- `migration_write_performed`: false.
- `numeric_criteria_admission`: false.
- `protected_payload_ingest`: false.
- `public_payload_exposure_performed`: false.
- `live_neo4j_writes`: false.
- `production_promotion`: false.
- `kg_rebuild`: false.
- Raw source custody remains unchanged.

## Remaining hard external inputs

User authorization allowed implementing the safe repo-side surfaces, but it does not provide concrete production credentials, rollback transcripts, legal/source-rights records, AHJ/project criteria packets, protected payload clearance, or steward survivor/alias/migration decisions. Those inputs remain necessary before a future dedicated admission or promotion workflow could truthfully apply them.
