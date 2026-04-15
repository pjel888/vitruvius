---
task: app-integrity-reliability
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Trigger — App Integrity Reliability

## Task Statement
Audit and repair the current `main` branch so the Vitruvius app health claims are grounded in fresh evidence: tests pass, core commands work, and integrity regressions are surfaced or fixed.

## In Scope
- `scripts/tests/` baseline and failing-test triage
- import-time and runtime failures in `scripts/vitruvius/` and `scripts/pipeline_cli.py`
- validation of core pipeline command surfaces and their help / preflight behavior
- creation of SEL artifacts for this integrity initiative under `.omx/context/`, `.ai/10_state/baselines/`, `.ai/13_research/`, `.ai/02_audits/`, `.ai/03_plans/`, and `.ai/05_logs/`
- minimal truthfulness updates to operator-facing state/docs if validation evidence proves a claim is stale

## Out of Scope
- new AEC implementation work
- speculative roadmap rewrites unrelated to runtime integrity
- broad feature work beyond what is required to restore tests/commands/integrity
- destructive cleanup of unrelated dirty worktree changes

## Identity-Locked File Check
- `AGENTS.md`: read-only unless a truthfulness contradiction directly blocks integrity validation
- `.ai/00_system/EXECUTION_LOOP.md`: read-only authority
- `.ai/00_system/principles.md`: read-only authority
- `.ai/01_roadmap/master-roadmap.md`: read-only authority
- `.ai/10_state/decisions.md`: append-only if a new architectural decision is actually required

## Risk Class
- `L` — broad runtime integrity sweep across tests, CLI surfaces, and state truthfulness

## Roles
- PLANNER: Codex
- AUDITOR: Codex plus delegated verification lanes if needed
- IMPLEMENTER: Codex
- REVIEWER: architect/verifier lane before completion
- STEWARD: Codex

## Linked Prior Artifacts
- `.omx/context/app-integrity-reliability-20260415T164902Z.md`
- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/03_plans/00-governing-implementation-plan.md`
- `.ai/10_state/known_issues.md`

## MCP / Intelligence Precheck
- GitNexus CLI available and up to date on commit `027e457`
- `code-review-graph` MCP surface unavailable in this session; recorded explicitly rather than assumed
- `docs/shared/agent-tiers.md` was not present under `/Users/philiplewis/.codex` or the repo, so Ralph delegation will use explicit role selection without a local tiers file
