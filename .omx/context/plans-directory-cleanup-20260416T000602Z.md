# Context Snapshot — plans-directory-cleanup

- created_utc: 20260416T000602Z
- task_statement: Clean up `.ai/03_plans` by determining which non-AEC plans are completed versus still active and archiving completed ones into `.ai/09_archive`.
- desired_outcome: `.ai/03_plans` contains only truly active plans plus planning-only AEC plans; completed non-AEC plans are archived and indexes/state reflect reality.

## Known Facts / Evidence
- User says AEC Engine has not been implemented yet, so AEC plans should remain planning-only unless evidence says otherwise.
- Current active index likely still includes completed stabilization plans.
- Recent completed work includes PASS 2 stabilization and duplicate canonical source ID remediation.

## Constraints
- Must follow AGENTS/SEL and keep plan/state/docs truthful.
- Do not archive truly active governance plans by accident.
- Archive only completed non-AEC plans; preserve planning-only AEC family unless evidence says otherwise.
- Update indexes/current-phase as needed after moves.

## Unknowns / Open Questions
- Which non-AEC plans in `.ai/03_plans` are genuinely still active?
- What archive/frontmatter conventions current archived plans use.
- Whether current-phase or other live docs still point at plans that should be archived.

## Likely Touchpoints
- `.ai/03_plans/*`
- `.ai/03_plans/INDEX.md`
- `.ai/01_roadmap/current-phase.md`
- maybe `.ai/10_state/active_context.md` or related live state docs if plan references change
- `.ai/09_archive/plans/`
