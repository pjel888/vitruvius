---
task: whole-codebase-plan-upgrade
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Trigger — Whole Codebase Plan Upgrade

## Task Statement
Audit the whole Vitruvius codebase, then upgrade every planning document in `.ai/03_plans/` so the active plan layer is detailed, comprehensive, codebase-aware, and aligned with current repo reality.

## In Scope
- full-plan-layer audit grounded in the live Python, Rust, TypeScript, config, test, and governance surfaces
- all active plan documents in `.ai/03_plans/`
- SEL artifacts for this task under `.ai/04_tasks/`, `.ai/10_state/baselines/`, `.ai/13_research/`, `.ai/02_audits/`, `.ai/03_plans/`, and `.ai/05_logs/`
- minimal state or authority-file reconciliation only where stale references would misroute future execution

## Out of Scope
- implementation of AEC runtime code
- broad runtime refactors outside the planning/governance layer
- archival sweeps of historical plans outside `.ai/03_plans/` unless a live plan rewrite requires cross-reference correction
- speculative roadmap changes unsupported by current repo evidence

## Identity-Locked File Check
- `AGENTS.md`: in scope only for minimal truthfulness fixes if required by the plan rewrite
- `.ai/00_system/EXECUTION_LOOP.md`: read-only authority
- `.ai/00_system/principles.md`: read-only authority
- `.ai/01_roadmap/master-roadmap.md`: read-only authority unless a direct contradiction blocks truthful plan updates
- `.ai/01_roadmap/current-phase.md`: may be updated only if live plan references are stale enough to misroute execution

## Risk Class
- `L` — governance-critical multi-file rewrite across the active planning layer, with direct effect on future agent behavior

## Roles
- PLANNER: Codex
- AUDITOR: Codex + delegated reviewers
- IMPLEMENTER: Codex
- REVIEWER: architect-style subagent review before completion
- STEWARD: Codex

## Linked Prior Artifacts
- `.omx/context/whole-codebase-plans-audit-20260415T161709Z.md`
- `.ai/02_audits/AEC_ENGINE_RESEARCH_TO_PLAN_AUDIT_2026-04-15.md`
- `.ai/02_audits/AEC_ENGINE_PLAN_CRITIQUE_2026-04-15.md`

## MCP / Intelligence Precheck
- GitNexus CLI used: `npx gitnexus status`
- Result: indexed commit and current commit both `027e457`; status `up-to-date`
- code-review-graph MCP surface was not exposed in this session; recorded as unavailable rather than silently skipped
