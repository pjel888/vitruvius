---
task: app-integrity-reliability
created_at_utc: 20260415T164902Z
workflow: ralph
repo: /Users/philiplewis/vitruvius
branch: main
commit: 027e45711db18990f40d4c9222677711ea058c63
---

# Ralph Context Snapshot — App Integrity Reliability

## Task Statement
Make Vitruvius trustworthy on the current `main` branch by getting the test suite green, verifying core commands work, and reconciling runtime claims with observed behavior.

## Desired Outcome
- `pytest scripts/tests/` passes on the active environment or every remaining failure is explicitly traced to a real blocker with evidence.
- Core CLI commands import and execute at least their help / preflight surfaces without unexpected crashes.
- Repo state and operator-facing claims about app health are reconciled with what the code and commands actually do.

## Known Facts / Evidence
- User explicitly requested an integrity-first pass before new plan implementation.
- Current branch is `main`; current commit is `027e45711db18990f40d4c9222677711ea058c63`.
- `current-phase.md` says the repo is between sprints and active work is governance/planning maintenance.
- `INDEX.md` shows no active plan already covering a runtime integrity sweep.
- `active_context.md` contains historical runtime claims from a different branch and reports older test counts, so it is not a trustworthy live health baseline for `main`.
- User-provided pytest output shows collection currently fails in `scripts/tests/test_livewiring_bench.py` because `scripts/vitruvius/bench/run_livewiring_bench.py` imports `psutil` at module import time.
- GitNexus local CLI is available and reports the index is up to date at commit `027e457`.
- `code-review-graph` MCP tools are not exposed in this session, so graph-first exploration is limited to GitNexus CLI plus direct file inspection.

## Constraints
- Must follow AGENTS.md authority order and the Standard Execution Loop for non-trivial work.
- Must prefer the smallest safe fixes and avoid unrelated refactors.
- Must not hide failing tests or reduce scope to declare success.
- Worktree is already dirty in `.ai/` and other governance files; unrelated user changes must be preserved.

## Unknowns / Open Questions
- Full current `pytest scripts/tests/` baseline on `main`.
- Which CLI commands should count as the integrity-critical surface for this pass.
- Whether failures are limited to optional dependency handling or point to broader regressions.
- Whether state files beyond `active_context.md` need reconciliation after runtime validation.

## Likely Codebase Touchpoints
- `scripts/tests/`
- `scripts/pipeline_cli.py`
- `scripts/vitruvius/`
- `config/vitruvius.yaml`
- `README.md`
- `.ai/04_tasks/`
- `.ai/10_state/baselines/`
- `.ai/13_research/`
- `.ai/02_audits/`
- `.ai/03_plans/`
- `.ai/05_logs/`
