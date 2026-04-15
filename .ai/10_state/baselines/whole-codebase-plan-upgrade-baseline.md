---
task: whole-codebase-plan-upgrade
phase: 02
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Baseline — Whole Codebase Plan Upgrade

## Git State
- Commit SHA: `027e45711db18990f40d4c9222677711ea058c63`
- Branch: `main`
- Worktree state at start: dirty due to pre-existing governance and planning edits outside this task, including `AGENTS.md`, `.ai/06_specs/RUST/*`, untracked `.ai/06_specs/AEC_ENGINE/*`, prior AEC audits/plans/logs, and `.omx/` state

## Repo-Intelligence Baseline
- GitNexus CLI: `npx gitnexus status`
  - Repository: `/Users/philiplewis/vitruvius`
  - Indexed commit: `027e457`
  - Current commit: `027e457`
  - Status: `up-to-date`
- code-review-graph MCP tools: not available in this session

## Authority Files Read
- `AGENTS.md`
- `.ai/00_system/EXECUTION_LOOP.md`
- `.ai/00_system/principles.md`
- `.ai/01_roadmap/master-roadmap.md`
- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/10_state/active_context.md`
- `.ai/10_state/known_issues.md`
- relevant GOVERNANCE, RUST, and AEC_ENGINE packs

## Active Plan Layer at Start
- `00-governing-implementation-plan.md`
- `2026-04-15-nested-agents-governance-plan.md`
- `AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`
- 8 AEC subsystem plans
- `INDEX.md`

## Baseline Findings
- The active plan layer is inconsistent with itself.
- `00-governing-implementation-plan.md` still claims a post-cleanup world with only two active plans, which is false.
- `INDEX.md` repeats the same obsolete inventory and contains duplicated changelog text.
- The AEC plan family is structurally sound but under-grounded in the real codebase; it rarely names actual modules, tests, flags, crates, or boundary contracts already present.
- `current-phase.md` still points to old roadmap/plan versions and references a closed historical side-track as if it were the natural next action.
- Root `AGENTS.md` still points to stale state paths under `.ai/10_state/` instead of the live roadmap state files under `.ai/01_roadmap/`.

## Live Codebase Snapshot Relevant to Planning
- Python orchestration spine: `scripts/pipeline_cli.py`
- Python product/runtime roots: `scripts/vitruvius/{parsers,review,graph,query,spatial,compound,geometric,...}`
- Rust compute roots: `scripts/vitruvius/engine_rs/{core,pyo3_shim,pdf,spatial_kernels,stats_kernels}` and `scripts/vitruvius/datalog_rs`
- TypeScript boundary root: `spatial-daemon/`
- Active flags: `p1b_*`, `l_*`, `m_*`, `n_*`, `gt_*`, `geom_*`, `phys_*`, `wiki_*`, `z_*`, `hp_*`, `y_*`
- Test surface: 222 Python `test_*.py` files plus TypeScript tests in `spatial-daemon/tests/`

## Baseline Conclusion
This task begins from a repo whose code reality is richer than its live plan layer. The rewrite must make active plans truthful, code-rooted, and operationally safe without pretending implementation has already begun where it has not.
