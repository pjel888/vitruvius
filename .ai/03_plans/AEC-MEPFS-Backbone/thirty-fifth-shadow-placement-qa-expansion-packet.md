---
task: aec-mepfs-shadow-placement-qa-expansion
phase: 03
created: 2026-04-26
author: CODEX
status: PASS
supersedes: null
---

# Thirty-Fifth Shadow Slice: Placement QA Expansion

## Scope

Expand the file-backed AEC-MEPFS placement/authoring QA runner so future
authoring migration cases prove more than the three original coverage buckets.
The runner should also validate case identity, input context, owner/review
status, non-empty source-evidence IDs, and rationale semantics for LD-8
auto-accept and legacy-label alias handling.

This slice stays shadow-only and file-backed. It does not call
`PlacementEngine`, write or query Neo4j, rebuild the KG, ingest protected
content, change feature flags, mount `/v2/resolve`, or make Explorer adopt the
shadow graph.

## Audit Findings

- The current placement QA runner validates three required coverage keys:
  `l3_l4_ld8_auto_accept`, `l1_l2_human_review`, and `legacy_label_alias`.
- Independent remaining-work scan identified taxonomy authoring/migration QA
  fixture checks as a concrete safe shadow-only task after resolver QA
  expansion.
- GitNexus impact before edits:
  - `run_placement_qa_fixture`: MEDIUM, 8 direct callers/tests, no affected
    processes.
  - `_evaluate_authoring_case`: LOW, direct impact through
    `run_placement_qa_fixture`.
  - Private helper impact for `_summarize_case_results` and `_empty_summary`
    could not be resolved by exact file-qualified GitNexus target, but the
    helper call path is contained by `run_placement_qa_fixture`.

## Implementation Plan

1. Add per-case validation for non-empty `case_id`, `owner`, candidate
   `review_status`, input label/legacy-label context, proposal level, and
   non-empty string `source_evidence` entries.
2. Add rationale checks for LD-8 auto-accept and legacy-label alias handling.
3. Expand the report summary with case type, proposed-by, and workflow counts
   plus required coverage keys for the new checks.
4. Add focused tests for new negative cases and update the valid-report
   assertion.
5. Generate a fresh placement QA report.
6. Leave downstream boundary audit, benchmark, and evidence manifest refresh for
   a clean-source follow-up slice after this source change is committed.

## Plan Critique

- [C001] Do not make this a runtime placement-engine implementation.
- [C002] Do not broaden into API route mounting, Explorer adoption, or source
  content admission.
- [C003] Treat generated placement QA evidence as source-slice evidence only;
  refresh downstream evidence separately from a clean source commit.

## Execution Checklist

- [x] Apply placement QA validation expansion.
- [x] Add focused regression tests.
- [x] Run focused Python tests.
- [x] Generate fresh placement QA report.
- [x] Run Gemini/Kimi advisory review where available.
- [ ] Commit and push the source-slice evidence.

## Generated Evidence

Placement QA report:
`006_System-Manifests/aec-mepfs-backbone/placement-qa/20260426T122042Z/placement-qa-report.json`

- `ok: true`
- 3/3 authoring migration cases passed.
- 11/11 required coverage keys are true.
- Case type counts: one `l3_leaf_auto_accept`, one `l1_human_review`, and one
  `legacy_label_alias`.
- Safety boundaries remain shadow-only, file-backed, no Neo4j writes, no KG
  rebuild, no protected ingest, no feature-flag cutover, no Explorer default
  adoption, and no canonical content admission.

## Explicit Non-Goals

- No Neo4j write, query, backup, restore, or cleanup.
- No KG rebuild/reset/load.
- No protected source content ingest.
- No feature flag cutover.
- No `/v2/resolve` or `/v2/resolve/trace` route mounting.
- No Explorer default graph adoption.
- No live runtime performance threshold claim.

## Next Safe Slice

After this source slice is committed and pushed, regenerate route inventory,
boundary audit, benchmark, and evidence manifest from the clean source tree
using the new placement QA report.
