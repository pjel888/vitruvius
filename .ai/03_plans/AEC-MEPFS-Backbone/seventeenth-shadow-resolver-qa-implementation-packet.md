---
task: aec-mepfs-shadow-resolver-qa
phase: 05
created: 2026-04-26
author: CODEX
status: VALIDATED
supersedes: null
---

# Seventeenth Shadow Slice: Resolver QA Runner

## Scope

Add a file-backed resolver QA runner over the existing readiness S2 fixture.

This slice validates resolver golden-case metadata for deterministic result
types and review disposition. It writes an auditable report but does not call
the runtime resolver, mount `/v2/resolve`, write Neo4j, rebuild the KG, ingest
protected content, change feature flags, or alter Explorer defaults.

## Research Baseline

- Current state files prioritize file-backed QA/evidence hardening or another
  non-default `/v2` preview before runtime cutover.
- `vitruvian-context-resolver-pack.md` accepts the deterministic, no-LLM hot
  path resolver contract but keeps runtime resolver implementation blocked.
- `valid_readiness_s2.json` already contains four resolver golden cases:
  `single_value`, `composed`, `conflict`, and `none`.
- The correct next step is therefore report-producing QA over the fixture, not
  a live resolver route or API adoption.

## Audit Findings

- The contract validator already requires resolver result-type coverage, but
  there was no report-producing QA artifact that proves the expected confidence
  semantics of each resolver result type.
- A fixture/report runner is safer than touching `scripts/vitruvius/resolver.py`
  or adding `/v2/resolve`, because the current resolver runtime remains a stub
  and future runtime behavior still needs a separate packet.
- The runner should explicitly fail if `/v2/resolve` or
  `/v2/resolve/trace/:trace_id` appears mounted in `api/index.ts`.

## Implementation Plan

1. Add `scripts/vitruvius/kg/backbone_resolver_qa.py`.
2. Read only `valid_readiness_s2.json` by default and validate it with the
   existing contract validator before QA evaluation.
3. Evaluate cases for:
   - `single_value` + `deterministic`,
   - `composed` + `deterministic`,
   - `conflict` + `review_required` and conflict/incompatibility rationale,
   - `none` + `insufficient`.
4. Write `resolver-qa-report.json` under
   `006_System-Manifests/aec-mepfs-backbone/resolver-qa/RUN_ID/`.
5. Add focused tests for success, confidence drift, missing concept IDs,
   missing coverage, unsafe run IDs, unsafe report paths, and accidental
   `/v2/resolve` route mounting.
6. Generate a fresh resolver QA report and update readiness docs.

## Plan Critique

- [C001] Do not import or call the runtime resolver.
- [C002] Do not mount a resolver API route.
- [C003] Do not claim full production resolver readiness from the four-case
  pilot fixture.
- [C004] Keep this artifact as fixture-level QA evidence only.

## Execution Checklist

- [x] Read state docs and resolver planning packet.
- [x] Implement file-backed runner.
- [x] Add focused tests.
- [x] Generate fresh resolver QA report.
- [x] Run focused Python verification.
- [x] Attempt Gemini/Kimi advisory review and record availability.
- [x] Update evidence/state docs.
- [ ] Commit, refresh GitNexus, push, then select the next safe slice.

## Explicit Non-Goals

- No runtime resolver execution.
- No `/v2/resolve` route mounting.
- No Neo4j writes.
- No KG rebuild.
- No protected content ingest.
- No feature flag cutover.
- No Explorer default graph adoption.
- No canonical source/content admission.
