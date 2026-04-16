---
task: aec-handoff-crosswalk-matrix
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC Handoff Crosswalk Matrix

## Purpose
This matrix maps the main AEC handoff artifacts to their future execution use.

| Artifact | Role | Open when | Prevents |
|---|---|---|---|
| `.ai/10_state/baselines/aec-clean-implementation-baseline-2026-04-16.md` | baseline truth | before any execution starts | dirty-worktree ambiguity |
| `.ai/04_tasks/aec-engine-gates-state-2026-04-16.json` | live gate truth | before any readiness claim | stale readiness language |
| `.ai/03_plans/2026-04-16-aec-first-bounded-slice-sprint-plan.md` | bounded execution plan | when implementation starts | scope creep and unordered execution |
| `.ai/04_tasks/2026-04-16-aec-first-bounded-slice-implementation-trigger.md` | execution authorization surface | when confirming slice kickoff | implicit execution start |
| `.omx/plans/prd-aec-first-bounded-slice.md` | product scope | before coding | fuzzy feature intent |
| `.omx/plans/test-spec-aec-first-bounded-slice.md` | test obligations | before coding and before review | incomplete test expectations |
| `.ai/04_tasks/aec-t011-fixture-corpus-spec-2026-04-16.md` | fixture families | before fixture creation | ad hoc fixture drift |
| `.ai/04_tasks/aec-first-slice-test-and-fixture-scaffold-map-2026-04-16.md` | test/fixture ownership | before creating tests | missing or duplicated test intent |
| `.ai/04_tasks/aec-first-slice-module-order-and-fixture-shapes-2026-04-16.md` | module/fixture order | before runtime file creation | churn from wrong build order |
| `.ai/04_tasks/aec-first-slice-artifact-shapes-2026-04-16.md` | runtime output shapes | before writing artifacts | ad hoc output formats |
| `.ai/04_tasks/aec-first-slice-ownership-and-review-checklist-2026-04-16.md` | lane ownership + review | during implementation and final review | scope drift |
| `.ai/04_tasks/aec-first-slice-verification-runbook-2026-04-16.md` | command sequence | before running proof commands | ad hoc verification |
| `.ai/04_tasks/aec-g10-closure-criteria-2026-04-16.md` | last-blocker contract | before any closure claim | partial-proof closure |
| `.ai/04_tasks/aec-g10-evidence-packet-template-2026-04-16.md` | closure evidence packet | during closure attempt | missing closure evidence |
| `.ai/05_logs/aec-first-slice-validation-template-2026-04-16.md` | final validation report shape | at end of proof sequence | proof drift |
| `.ai/04_tasks/aec-g10-work-order-2026-04-16.md` | exact final blocker work order | when implementing evidence | unordered blocker resolution |
| `.ai/04_tasks/aec-first-slice-session-packet-2026-04-16.md` | compact operator checklist | at start of execution session | forgotten setup steps |
| `.ai/04_tasks/aec-readiness-vocabulary-and-state-model-2026-04-16.md` | state-language law | whenever state wording is updated | readiness vocabulary drift |
| `.ai/04_tasks/aec-first-slice-failure-triage-matrix-2026-04-16.md` | bounded failure handling | when any lane fails | improvised recovery |
| `.ai/04_tasks/aec-first-slice-execution-handoff-dossier-2026-04-16.md` | single-entry navigation surface | first file to open during future execution | operator fragmentation |

## Historical checkpoint artifacts
Use for lineage, not live execution truth:
- `.ai/03_plans/2026-04-16-aec-first-bounded-slice-pre-implementation-plan.md`
- `.ai/03_plans/2026-04-16-aec-g2-g8-freeze-pack-plan.md`

## Final rule
If an operator cannot say why a file is being opened using this matrix, they should return to the execution handoff dossier first.
