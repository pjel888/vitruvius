---
task: plans-directory-cleanup
phase: 09
created: 2026-04-16
author: REVIEWER
supersedes: null
status: ACCEPTED
---

# 2026-04-16 Plans Directory Cleanup Validation

## Objective
Clean up `/.ai/03_plans/` so completed non-AEC plans are archived to `/.ai/09_archive/plans/`, while live governance/AEC planning files remain in place and the plan index/state docs stay truthful.

## Archived completed non-AEC plans
- `2026-04-16-app-integrity-reliability-plan.md`
- `2026-04-16_cli-human-readable-output-plan.md`
- `2026-04-16_readme-investor-mermaid-diagram-plan.md`
- `2026-04-16_master-audit-implementation-plan.md`
- `2026-04-16_duplicate-canonical-source-id-remediation-plan.md`

## Left live in `.ai/03_plans`
- `00-governing-implementation-plan.md`
- `2026-04-15-nested-agents-governance-plan.md`
- `2026-04-16-whole-codebase-plans-upgrade-plan.md`
- `2026-04-16_graph-warning-and-gitnexus-warning-plan.md` (draft / unexecuted)
- all `AEC_ENGINE_*` plans (planning-only; not implemented)
- `INDEX.md`

## What was verified
- Directory inventory matches `INDEX.md`
- Completed non-AEC plans were moved to archive and marked archived in frontmatter
- Current live state docs no longer point at completed plans as if they were active dispatcher plans
- Existing `decisions.md` AD entries were left untouched because the decision ledger is append-only; the cleanup instead records the archive move in a new AD and updates the current live docs
- AEC planning files remain live because the AEC engine has not been implemented yet
- No formatting issues were introduced in the touched files

## Commands / Checks Run
- inventory + status scan of `.ai/03_plans`
- reference scans for plan filenames across live docs
- exact directory/index reconciliation script (`MATCH=True`)
- `git diff --check` on changed plan/state/archive files
- `python3 scripts/pipeline_cli.py --help` (lightweight runtime sanity)

## Results
- `INDEX.md` now matches the actual live `.ai/03_plans` directory listing exactly
- `current-phase.md` now treats the PASS 2 stabilization plans as archived completed work rather than active plans
- `active_context.md` now points to the archived stabilization/remediation plan paths
- `decisions.md` preserves historical AD-045 as written, and the archive move is instead recorded in new AD-046 per the append-only decision-log rule
- The completed 2026-04-16 non-AEC plans were archived successfully
- The AEC family remains live and planning-only, which matches current repo reality

## Remaining minor note
- `2026-04-16_graph-warning-and-gitnexus-warning-plan.md` remains live as a draft/unexecuted non-AEC plan and is now explicitly listed in `INDEX.md`

## Verdict
**APPROVED** — the plan directory is materially cleaner and more truthful after this pass.
