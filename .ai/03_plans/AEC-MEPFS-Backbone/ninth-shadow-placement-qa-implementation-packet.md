---
task: aec-mepfs-shadow-placement-qa
phase: 05
created: 2026-04-26
author: CODEX
status: VALIDATED
supersedes: null
---

# Ninth Shadow Slice: Placement QA Runner

## Scope

Add a file-backed placement/authoring QA runner over the existing readiness S2
fixture.

This slice validates the authoring/migration QA cases that govern LD-8
`PlacementAssertion` auto-accept, L1/L2 human-review routing, and legacy label
alias handling. It produces an auditable report but does not run the runtime
`PlacementEngine`, write Neo4j, rebuild the KG, ingest protected content, change
feature flags, or alter Explorer defaults.

## Research Baseline

- Current state files identify file-backed classification/placement QA as the
  next bounded shadow slice after parity-runner hardening.
- `taxonomy-authoring-migration-qa-pack.md` requires L3/L4 LD-8 auto-accept
  thresholds, L1/L2 human stewardship, and legacy document-derived labels to be
  aliases/source labels rather than canonical user-facing labels.
- `valid_readiness_s2.json` already contains three candidate QA cases covering:
  - L3 LD-8 auto-accept,
  - L1 human review,
  - legacy label alias migration.
- GitNexus impact for `validate_backbone_contract_file` and
  `validate_backbone_contract` is LOW with zero affected runtime processes.

## Audit Findings

- Contract validation already blocks invalid L1/L2 AI authoring and invalid
  LD-8 auto-accept fields, but there was no separate report-producing QA runner
  that summarizes placement authoring coverage.
- A report-producing runner is safer than wiring runtime placement because it
  stays on fixture rows and does not touch `CanonicalNode`, `PlacementEngine`,
  `Neo4jLoader`, graph rebuilds, or Explorer state.
- The first QA runner should be explicit that it is pilot coverage, not the full
  250-case golden dataset target.

## Implementation Plan

1. Add `scripts/vitruvius/kg/backbone_placement_qa.py`.
2. Read only `valid_readiness_s2.json` by default and validate it with the
   existing contract validator before QA evaluation.
3. Evaluate cases for:
   - LD-8 L3/L4 auto-accept confidence threshold,
   - L1/L2 human-review routing and AI prohibition,
   - legacy label alias/source-label storage.
4. Write `placement-qa-report.json` under
   `006_System-Manifests/aec-mepfs-backbone/placement-qa/RUN_ID/`.
5. Add focused tests for success, contract-gated failure, missing coverage,
   unsafe run IDs, and unsafe report paths.
6. Generate a fresh report and update the readiness docs.

## Plan Critique

- [C001] Do not import or call runtime placement/materialization modules.
- [C002] Do not claim full golden dataset completion from the three-case pilot.
- [C003] Keep protected source content out of the report.
- [C004] Do not expose this through API/Explorer until a separate read-only
  route/consumer packet is created.

## Execution Checklist

- [x] Read state docs and QA pack.
- [x] Run GitNexus impact on reused validator functions.
- [x] Implement file-backed runner.
- [x] Add focused tests.
- [x] Generate fresh placement QA report.
- [x] Run focused and broader backbone tests.
- [x] Attempt Gemini/Kimi advisory review and record availability.
- [x] Update evidence/state docs.
- [ ] Commit, refresh GitNexus, push, then select the next safe slice.

## Explicit Non-Goals

- No runtime `PlacementEngine` execution.
- No Neo4j writes.
- No KG rebuild.
- No protected content ingest.
- No feature flag cutover.
- No Explorer default graph adoption.
- No canonical source/content admission.
