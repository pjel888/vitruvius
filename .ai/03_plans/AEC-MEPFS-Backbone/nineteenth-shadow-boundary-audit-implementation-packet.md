---
task: aec-mepfs-shadow-boundary-audit
phase: 05
created: 2026-04-26
author: CODEX
status: VALIDATED
supersedes: null
---

# Nineteenth Shadow Slice: Boundary Audit Runner

## Scope

Add a file-backed boundary audit runner that consolidates the latest AEC-MEPFS
shadow evidence into a single machine-readable safety report.

This slice is evidence hardening only. It does not add a route, mount
`/v2/resolve`, query or write Neo4j, rebuild the KG, ingest protected content,
change feature flags, alter Explorer defaults, or promote any shadow artifact
to the live graph.

## Research Baseline

- `.ai/ACTIVE_WORK.md` and `.ai/STRATEGIC_NEXT_MOVE.md` point to another
  bounded shadow slice, with priority on evidence/report hardening before
  runtime cutover.
- `readiness-closure-scorecard.md` keeps runtime integration blocked and
  requires future slices to carry forward the S8 no-ingest, rollback,
  HIGH/CRITICAL root-impact, and v1-preservation boundaries.
- Existing evidence is distributed across the shadow consumer report, sibling
  graph artifact, placement QA report, resolver QA report, parity report,
  config flags, and API route surface.

## Audit Findings

- The latest shadow evidence is green, but the safety invariants were
  documented per slice rather than consolidated into one report.
- GitNexus shows `load_features` is CRITICAL impact, so this slice does not
  modify that shared symbol. The audit reads `config/vitruvius.yaml` directly
  and checks only the AEC-MEPFS-related feature flags.
- The remaining planned `/v2/resolve` routes are still blocked. The audit must
  fail if they appear mounted before a separately accepted runtime packet.

## Implementation Plan

1. Add `scripts/vitruvius/kg/backbone_shadow_boundary_audit.py`.
2. Read only current file-backed evidence:
   - shadow staging consumer report
   - sibling shadow graph artifact
   - placement QA report
   - resolver QA report
   - API/Explorer parity report
   - `config/vitruvius.yaml`
   - `api/index.ts`
3. Validate safety invariants:
   - no Neo4j writes
   - no KG rebuild
   - no protected content ingest
   - no feature flag cutover
   - no Explorer default adoption
   - no resolver route mounting
   - preview/read-only/shadow-only behavior remains opt-in
   - generated artifacts are file-backed and auditable
4. Write
   `006_System-Manifests/aec-mepfs-backbone/boundary-audit/<run-id>/shadow-boundary-audit-report.json`.
5. Add focused tests for drift/fail-closed behavior.
6. Generate fresh boundary evidence and update state docs.

## Plan Critique

- [C001] Do not make the audit a runtime gate that imports or mutates high-risk
  KG roots.
- [C002] Do not use Neo4j, pipeline rebuild commands, API calls, or Explorer
  runtime execution in the audit.
- [C003] Fail closed on feature-flag drift, resolver route mounting, protected
  ingest, or unsafe path/output placement.
- [C004] Keep the generated report append-only under `006_System-Manifests/`.

## Execution Checklist

- [x] Inspect active state, scorecard, and remaining shadow slice docs.
- [x] Run GitNexus query/impact checks before implementation.
- [x] Implement the file-backed boundary audit runner.
- [x] Add focused tests for safety-drift failures and path fences.
- [x] Generate fresh boundary audit evidence.
- [x] Run focused and broader affected Python tests.
- [x] Attempt Gemini/Kimi advisory review and record availability.
- [x] Update evidence/state docs.
- [ ] Commit, refresh GitNexus, push, then inspect the next safe slice.

## Explicit Non-Goals

- No new `/v2` route.
- No `/v2/resolve` mounting.
- No Neo4j writes.
- No KG rebuild.
- No protected content ingest.
- No feature flag cutover.
- No Explorer default graph adoption.
- No canonical source/content admission.
