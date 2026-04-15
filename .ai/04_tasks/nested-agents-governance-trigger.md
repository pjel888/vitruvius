---
task: nested-agents-governance
phase: 00
created: 2026-04-15
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Trigger — Nested AGENTS Governance

## Task Statement
Audit the repository and establish a justified hierarchical `AGENTS.md` system that keeps root governance authoritative while adding only directory-local operating rules where they materially improve agent behavior.

## In Scope
- `AGENTS.md`
- existing nested `AGENTS.md` files already present in the repo
- justified new nested `AGENTS.md` files at major directory boundaries
- SEL governance artifacts for this task under `.ai/04_tasks/`, `.ai/10_state/baselines/`, `.ai/13_research/`, `.ai/02_audits/`, `.ai/03_plans/`, and `.ai/05_logs/`

## Out of Scope
- broad rewrites of unrelated governance packs outside AGENTS hierarchy work
- code or runtime behavior changes in Python, Rust, or TypeScript modules
- adding `AGENTS.md` to trivial leaves, generated directories, caches, or vendored dependencies
- changing roadmap phase status unless this task materially alters execution state

## Identity-Locked File Check
- `AGENTS.md`: PASS for scoped governance reconciliation within this task
- `.ai/00_system/EXECUTION_LOOP.md`: not in scope
- `.ai/00_system/principles.md`: not in scope

## Risk Class
- `L` — governance-critical multi-file documentation change spanning root contract, nested operating contracts, and stateful documentation artifacts

## Roles
- PLANNER: Codex
- AUDITOR: Codex self-critique + final external architect review
- IMPLEMENTER: Codex
- REVIEWER: Codex + architect subagent
- STEWARD: Codex

## Linked Prior Artifacts
- none specific to nested AGENTS hierarchy

## MCP / Intelligence Precheck
- GitNexus CLI used: `npx gitnexus status`
- code-review-graph MCP surface unavailable in this session; recorded as tooling-unavailable rather than silently skipped
