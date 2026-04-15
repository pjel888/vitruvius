---
task: whole-codebase-plan-upgrade
phase: 05
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Plan — Whole Codebase Plan Upgrade

## Scope Boundary
This task upgrades the live plan layer and only the supporting governance/state files required to keep that layer truthful. It does not implement AEC runtime code or reopen archived sprint execution.

## Files To Update

### Primary Targets
- `.ai/03_plans/00-governing-implementation-plan.md`
- `.ai/03_plans/INDEX.md`
- `.ai/03_plans/2026-04-15-nested-agents-governance-plan.md`
- `.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_ECS_CORE_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_SPATIAL_KERNEL_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_KNOWLEDGE_VAULT_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_Z3_VERIFICATION_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_MULTI_DISCIPLINARY_COORDINATION_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_OPTIMIZATION_ENGINE_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_BOUNDARY_TRANSLATION_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_LLM_TOOL_CALLING_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_FINANCIAL_PRICING_ORACLE_IMPLEMENTATION_PLAN.md`

### Minimal Supporting Reconciliation
- `AGENTS.md`
- `.ai/01_roadmap/current-phase.md`

## Upgrade Intent By File

### Governing Plan
- convert from stale sprint-ledger framing into a live dispatcher for the current plan set
- define active-plan consumption order
- record current repo truth without pretending archived work is live work

### Index
- rebuild the active-plan inventory
- distinguish active, approved-pending-execution, proposed, and archived plans
- remove obsolete dependency/ordering text

### Nested AGENTS Plan
- keep scope bounded to AGENTS hierarchy work
- ground the plan in actual current AGENTS coverage and known gaps
- keep it as a governance plan, not a generic doc pass

### AEC Master Plan
- add actual codebase anchors
- freeze the planned AEC namespace and integration boundaries
- define phase entry/exit gates against real repo surfaces

### AEC Subsystem Plans
- keep existing structure
- add:
  - current repo anchors
  - proposed code locations
  - actual flags
  - actual tests/commands
  - concrete stop conditions
  - existing modules that are precedents, not dumping grounds

## Inheritance / Consistency Model
- root law remains `AGENTS.md` + execution loop + principles + roadmap/state
- `00-governing-implementation-plan.md` becomes the plan-layer dispatcher
- `INDEX.md` becomes the inventory/reference file
- `AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md` governs AEC implementation sequencing
- each AEC subsystem plan inherits the master plan plus the relevant spec packs

## Validation Plan
- scan all active plan files for status/frontmatter/heading integrity
- scan for stale claims such as “only two active plans”
- scan for duplicated placeholder content
- verify that every AEC plan names real code roots, tests, and boundaries
- verify `INDEX.md` inventory matches the actual directory listing
- verify supporting state fixes are narrowly scoped and truthful

## Plan Critique

### Where Am I Over-Documenting?
- The biggest risk is turning the AEC subsystem plans into mini-spec packs. They should stay implementation plans, not restatements of the full AEC governance pack.
- The governing plan should not repeat archived sprint history in detail.

### Where Am I Under-Documenting?
- If the AEC plans still fail to freeze a planned namespace and exact reuse targets, they will remain too abstract.
- If validation sections do not name specific tests and commands, future execution will still drift.

### Where Might Local Files Duplicate Root Law?
- stop conditions, authority order, and execution-loop rules already exist above the plan layer
- the rewrite should reference those rules and only restate plan-local consequences

### Where Might Files Drift Over Time?
- the governing plan and index will drift first because they summarize the plan set
- `current-phase.md` will drift again if future plan rewrites do not reconcile it
- AEC plans will drift if the chosen code namespace changes and the whole set is not updated together

### Where Should I Avoid Writing More?
- do not create more plan files
- do not rewrite archived plans
- do not push detailed task breakdown into code modules that do not yet exist

### Remaining Ambiguities
- the exact future implementation directory for AEC code is still a planning decision, not a codebase fact
- the rewrite must choose a planned location and make that choice explicit as a planning assumption rather than pretend it already exists

## Refined Plan
Use the rewrite to do three things only:
1. make the live plan layer truthful
2. make the AEC plan family repo-grounded
3. fix only the minimal upstream authority/state drift that would otherwise break plan consumption

## Execution Checklist
- [ ] create SEL artifacts for this task
- [ ] rewrite governing plan as a truthful dispatcher for the current plan layer
- [ ] rewrite `INDEX.md` so inventory and statuses match the directory
- [ ] upgrade the nested-AGENTS plan with current coverage and boundaries
- [ ] upgrade all AEC plans with code-root, flag, test, and boundary grounding
- [ ] patch only the minimum supporting authority/state files required for truthful consumption
- [ ] run consistency scans across `.ai/03_plans`
- [ ] perform architect-style review
- [ ] run ai-slop cleanup on changed files only
- [ ] re-verify after cleanup and write the validation report
