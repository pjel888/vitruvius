---
task: aec-g2-g8-freeze-pack
phase: 03
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Research Pack — AEC G2-G8 Freeze Pack

## Purpose
Define the minimum planning/spec artifact set required to close global blockers `G2` through `G8` without pretending the AEC family is implementation-ready.

## Inputs reviewed
- `.ai/04_tasks/aec-engine-gates-state-2026-04-16.json`
- `.ai/04_tasks/aec-engine-master-execution-task-list-2026-04-16.md`
- `.ai/04_tasks/aec-engine-traceability-matrix-2026-04-16.md`
- `.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/2026-04-16-aec-first-bounded-slice-pre-implementation-plan.md`
- `.ai/04_tasks/aec-engine-file-touch-matrix-2026-04-16.md`
- `.ai/04_tasks/aec-engine-language-boundary-blacklists-2026-04-16.md`

## Findings
1. `G2`-`G8` are specification/freeze gates, not runtime-code gates.
2. A single accepted freeze pack can close them at the planning layer if it defines auditable decisions for:
   - namespace/ownership
   - replay-safe artifact envelope
   - DTO/ID/version policy
   - frame/unit/tolerance policy
   - candidate/canonical truth split
   - benchmark doctrine
   - parity matrix
3. `AEC-T008` and `AEC-T010A` must be included in the same pack or the freezes remain incomplete.
4. `G1` / `AEC-T006` cannot be closed by documentation alone because the working tree is still dirty.

## Recommendation
Create one accepted freeze pack plus control-surface updates. Close `G2`-`G8`; keep `G1` open and `ready_to_implement=false`.
