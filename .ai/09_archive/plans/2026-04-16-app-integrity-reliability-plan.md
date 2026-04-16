---
plan_id: app-integrity-reliability
phase: 05
title: "App Integrity Reliability Plan"
status: archived
priority: high
sprint: "Integrity Maintenance"
version: 1.0.0
plan_type: maintenance
created: 2026-04-16
last_updated: 2026-04-16
owner: Codex
depends_on:
  - .ai/04_tasks/app-integrity-reliability-trigger.md
  - .ai/10_state/baselines/app-integrity-reliability-baseline.md
  - .ai/13_research/app-integrity-reliability-research.md
  - .ai/02_audits/APP_INTEGRITY_RELIABILITY_AUDIT_2026-04-16.md
archive_status: complete
archived_at: 2026-04-16T00:11:22Z
archived_at: 2026-04-16T00:11:22Z
---

# App Integrity Reliability Plan

## 1. Purpose
Restore confidence in the current `main` branch by fixing the first reproducible test blocker, validating the highest-value command surfaces, and reconciling runtime-health claims with fresh evidence.

## 2. Scope

### In Scope
- `scripts/vitruvius/bench/run_livewiring_bench.py`
- `scripts/tests/test_livewiring_bench.py`
- `scripts/pipeline_cli.py` command validation
- state/doc truthfulness updates only where fresh evidence proves a claim is stale
- validation artifacts for this integrity pass

### Out of Scope
- new feature delivery
- AEC implementation work
- broad refactors unrelated to test and command integrity
- reverting unrelated dirty worktree changes

## 3. Execution Sequence

### Step 1 — Remove the import-time blocker
- modify the livewiring bench harness so it does not require `psutil` merely to import
- preserve the existing test contract:
  - summary still includes `peak_rss_mb`
  - `flag_on_config()` remains non-mutating
  - optional dependency handling is explicit and truthful

### Step 2 — Revalidate the local fix
- run the targeted bench test module first
- run file-level diagnostics on the changed Python file

### Step 3 — Re-run the broader Python baseline
- rerun `PYTHONPATH=scripts python3 -m pytest scripts/tests/ -q`
- if new failures appear, triage them into:
  - same-cluster fallout
  - separate integrity defects
  - environment/service blockers

### Step 4 — Expand command validation
- validate the operator-critical command ladder:
  - `pipeline_cli.py --help`
  - `pipeline_cli.py run --help`
  - `pipeline_cli.py status`
  - additional help/preflight commands only as needed based on failures or stale claims

### Step 5 — Reconcile truthfulness
- if fresh evidence diverges from `.ai/10_state/active_context.md` or similar health claims, update them narrowly to reflect observed reality

### Step 6 — Close with fresh evidence
- write a validation report with actual command/test outputs
- obtain final verification before declaring the branch healthy

## 4. Stop Conditions
- full pytest reveals a wider failure cluster that changes the task from maintenance to broader stabilization
- command validation exposes missing external prerequisites that require user/environment decisions
- a truthfulness fix would require rewriting historical state rather than updating the live baseline

## 5. Success Criteria
- the livewiring bench module imports without `psutil` installed
- `scripts/tests/test_livewiring_bench.py` passes
- the broader pytest baseline is rerun and its result is recorded honestly
- the key CLI command surfaces are revalidated
- stale branch-health claims are either updated or explicitly called out in the validation report
