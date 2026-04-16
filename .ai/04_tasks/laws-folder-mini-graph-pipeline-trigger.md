---
task: laws-folder-mini-graph-pipeline
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Trigger — Laws-Folder Mini Graph Pipeline Plan

## Task Statement
Create a repo-grounded implementation plan for a mini dataset→graph pipeline that can produce a knowledge graph for a single laws-folder scope first, then scale to per-section graphs and eventually an interconnected graph.

## In Scope
- research current code paths from raw source intake through graph output
- map the full source→graph path and likely blast radius before execution
- assess optimization opportunities and future Rust candidacy at the audit/planning level only
- assess whether a one-folder or one-law pilot is already possible
- define the smallest safe scoped pipeline plan
- write SEL planning artifacts and a new live plan in `/.ai/03_plans/`

## Out of Scope
- implementing the mini dataset pipeline
- changing graph/query/promotion code in this task
- archiving AEC plans
- broad repo audit unrelated to the mini graph pipeline question

## Risk Class
- **L** — new live plan plus cross-layer pipeline/design grounding; no runtime code changes in this task

## Role Assignments
- PLANNER: Codex
- AUDITOR: Codex + consensus architect/critic pass
- IMPLEMENTER: future task
- REVIEWER: future task
- STEWARD: Codex

## Linked Prior Artifacts
- `.ai/02_audits/2026-04-16_backend-and-api-audit.md`
- `.ai/02_audits/2026-04-16_targeted-stabilization-reaudit.md`
- `.ai/09_archive/plans/phase-8-graph-contract-indexing-plan.md`
- `.ai/09_archive/plans/phase-9-query-ai-layer-plan.md`

## MCP / Exploration Precheck
- `omx explore` repository sweep for source→graph command paths
- targeted file inspection of `pipeline_cli.py`, graph/query modules, canonicalization, relationships, review, and promotion paths
