---
task: aec-mepfs-shadow-placement-qa-expansion
phase: validation
created: 2026-04-26
author: CODEX
status: PASS
---

# AEC-MEPFS Shadow Placement QA Expansion Validation

## Scope

Thirty-fifth AEC-MEPFS shadow slice: expand the file-backed
placement/authoring QA runner so authoring migration cases must prove case
identity, input context, owner/review status, non-empty source-evidence IDs, and
rationale semantics for LD-8 auto-accept and legacy-label alias handling.

## Files Changed

- `scripts/vitruvius/kg/backbone_placement_qa.py`
- `scripts/tests/test_kg_backbone_placement_qa.py`
- `scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json`
- `006_System-Manifests/aec-mepfs-backbone/placement-qa/20260426T122042Z/placement-qa-report.json`
- `.ai/03_plans/AEC-MEPFS-Backbone/thirty-fifth-shadow-placement-qa-expansion-packet.md`
- `.ai/05_logs/2026-04-26_aec_bb_shadow_placement_qa_expansion_validation.md`

## Implementation Summary

- Added required placement QA coverage for:
  - `case_id_present`
  - `input_context_present`
  - `owner_present`
  - `proposal_level_present`
  - `review_status_candidate`
  - `source_evidence_ids_present`
  - `ld8_auto_accept_rationale`
  - `legacy_label_rationale`
- Added per-case validation for non-empty owner, candidate review status,
  input label or legacy-label context, proposal level, source-evidence IDs, and
  rationale-specific LD-8/alias language.
- Added `case_type_counts`, `proposed_by_counts`, and `workflow_counts` to the
  placement QA summary.
- Added focused negative tests for missing input context, blank source evidence
  IDs, non-candidate review status, auto-accept rationale drift, and legacy
  alias rationale drift.
- Updated the valid fixture legacy rationale so the fixture explicitly says
  document-derived labels must remain aliases and not become canonical labels.

## Generated Evidence Summary

Placement QA report:
`006_System-Manifests/aec-mepfs-backbone/placement-qa/20260426T122042Z/placement-qa-report.json`

- `ok: true`
- 3/3 cases passed.
- Required coverage keys: 11/11 true.
- Case types remain one each for `l3_leaf_auto_accept`, `l1_human_review`, and
  `legacy_label_alias`.
- Safety boundaries remain shadow-only, file-backed, no live Neo4j writes, no
  KG rebuild, no feature-flag cutover, no Explorer default adoption, no
  protected content ingest, and no canonical content admission.

## Verification Commands

- `npx --yes gitnexus@1.6.2-rc.10 status`
  - Result before edits: indexed and current commit matched `c9ace7c`; status
    up-to-date.
- `npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius run_placement_qa_fixture --direction upstream --depth 3 --include-tests`
  - Result: MEDIUM; 8 direct callers/tests, no affected processes.
- `npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius _evaluate_authoring_case --direction upstream --depth 3 --include-tests`
  - Result: LOW; direct impact through `run_placement_qa_fixture` and
    placement QA tests.
- `npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius scripts/vitruvius/kg/backbone_placement_qa.py:_summarize_case_results --direction upstream --depth 3 --include-tests`
  - Result: exact file-qualified private-helper target was not found by
    GitNexus; helper impact is contained by `run_placement_qa_fixture`.
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_placement_qa.py -q`
  - First run: 11 passed, 1 failed because the old legacy-coverage assertion
    expected a single missing key while the expanded coverage gate reports
    multiple missing legacy keys together.
  - Second run after assertion update: 12 passed.
  - Final run after verifier findings were addressed: 13 passed.
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone*.py -q`
  - First result: 177 passed.
  - Final result after verifier findings were addressed: 178 passed.
- `python3 -m py_compile scripts/vitruvius/kg/backbone_placement_qa.py scripts/tests/test_kg_backbone_placement_qa.py`
  - Result: passed.
- `PYTHONPATH=scripts python3 scripts/vitruvius/kg/backbone_placement_qa.py --run-id 20260426T122042Z`
  - Result: passed and wrote the placement QA report.

## Advisory Review

- Gemini CLI was attempted and failed with the existing 403 service-disabled
  response; no findings were produced.
- Codex verifier subagent reported no direct safety regression, but identified
  two quality issues before commit:
  - the confidence-threshold test exercised contract gating rather than the
    runner branch;
  - `source_evidence_traceable` overclaimed resolved provenance because the
    runner only proves non-empty source-evidence IDs.
- Both findings were fixed before final verification: a monkeypatched public
  runner test now covers the independent threshold guard, and the coverage key
  is now `source_evidence_ids_present`.
- Kimi CLI was attempted against the staged diff and produced no output after
  more than two minutes. The process was terminated and the advisory lane is
  recorded as timed out for this slice.

## Safety Invariant Confirmation

- No Neo4j writes or queries.
- No KG rebuild/reset/load.
- No protected content ingest.
- No feature-flag cutover.
- No `/v2/resolve` or `/v2/resolve/trace` route mounting.
- No Explorer default graph adoption.
- No live `PlacementEngine` invocation.
- Generated placement QA artifact is file-backed and auditable.

## Residual Risks

- Downstream boundary audit, benchmark, and evidence manifest still reference
  the earlier placement QA report until the next clean-source evidence refresh.
- The authoring/migration fixture remains a three-case pilot, not the future
  full taxonomy admission dataset.
- Runtime placement and canonical taxonomy admission remain blocked.

## Next Recommended Safe Slice

Commit and push this placement QA expansion. Then regenerate route inventory,
boundary audit, benchmark, and evidence manifest from the clean source tree
using the new placement QA report.
