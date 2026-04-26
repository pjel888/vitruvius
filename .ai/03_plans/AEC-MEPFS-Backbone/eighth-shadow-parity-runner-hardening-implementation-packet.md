---
task: aec-mepfs-shadow-parity-runner-hardening
phase: 05
created: 2026-04-26
author: CODEX
status: VALIDATED
supersedes: null
---

# Eighth Shadow Slice: Parity Runner Hardening

## Scope

Harden the file-backed API/Explorer parity runner so the already implemented
shadow graph and `/v2/backbone/taxonomy` preview are mandatory parity evidence.

This slice does not add runtime behavior. It only expands the existing
readiness fixture, command registry, required parity categories, and generated
parity report coverage.

## Research Baseline

- The seventh shadow slice staged `shadow-backbone-graph.json` with 7 admitted
  nodes, 4 governed hierarchy edges, 3 roots, and max depth 2.
- Current state files identify classification/placement QA or another
  read-only `/v2` surface as the next safe direction.
- The existing S4 parity runner still requires only pre-shadow-graph parity
  categories and does not require the new `/v2/backbone/taxonomy` graph preview
  or Explorer opt-in isolation tests.
- Fresh GitNexus CLI impact in this session reported LOW risk for
  `run_parity_fixture` and `_validate_parity_case_coverage`; the historical S4
  impact map recorded `run_parity_fixture` as MEDIUM at the earlier S4 slice.
  Both runs report zero affected runtime processes.

## Audit Findings

- A generated shadow graph can be present and tested independently while the
  parity runner still reports green using older command coverage.
- The parity runner's allowlisted command registry is the right boundary:
  expanding it preserves shell-free execution and avoids introducing runtime
  graph access.
- The new evidence must remain file-backed and report-producing under
  `006_System-Manifests/aec-mepfs-backbone/parity/`.

## Implementation Plan

1. Add required parity categories for contract validation, shadow summary,
   graph artifact, taxonomy graph preview, fail-closed graph validation, and
   Explorer opt-in preview isolation.
2. Add allowlisted commands for:
   - Python shadow staging/report reader tests,
   - API `v2Backbone.test.ts`,
   - Explorer search/preview integration.
3. Add matching parity cases to
   `scripts/tests/fixtures/aec_mepfs_backbone/api-explorer-parity-cases.json`.
4. Update runner tests for the expanded command set and required categories.
5. Generate a fresh parity report.
6. Run focused and affected verification, including Gemini/Kimi advisory review
   where available.

## Plan Critique

- [C001] Do not treat this as runtime readiness. It only strengthens shadow
  parity evidence.
- [C002] Do not add arbitrary shell execution. Every new command must be
  explicitly allowlisted.
- [C003] Do not add Neo4j, KG rebuild, source ingest, feature flag, or Explorer
  default-adoption paths.
- [C004] Keep parity wording specific: this proves current file-backed
  shadow-route and preview coverage, not future route families.

## Execution Checklist

- [x] Create Ralph context snapshot and PRD/test-spec gate files.
- [x] Run GitNexus impact for edited parity runner symbols.
- [x] Expand parity runner required categories and command registry.
- [x] Expand parity fixtures.
- [x] Update runner tests.
- [x] Generate fresh parity report.
- [x] Run focused and affected verification.
- [x] Run Gemini/Kimi advisory review.
- [x] Update evidence/state docs.
- [ ] Commit, refresh GitNexus, push, then select the next safe slice.

## Explicit Non-Goals

- No Neo4j write or read-load.
- No KG rebuild.
- No protected source content ingest.
- No feature flag cutover.
- No Explorer default graph adoption.
- No runtime graph promotion.
