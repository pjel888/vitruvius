# Current Phase — Between Sprints / Governance & Planning Maintenance

> **Authoritative roadmap:** `/.ai/01_roadmap/master-roadmap.md` (v2.3.0)
> **Authoritative execution order:** `/.ai/03_plans/00-governing-implementation-plan.md` (v4.0.0)
> **This document:** live snapshot of active execution state and the next valid gates
> **Updated:** 2026-04-16

---

## State

**Active implementation sprint:** none.

Vitruvius is currently between feature sprints, but it is **not** idle. The live work is governance/planning maintenance, centered on the plan-layer rewrite and pending governance plans rather than runtime feature execution.

**Live branch:** `ralph/laws-dataset-phases`

**Most recent validated implementation burst:** the historical multi-sprint closure recorded on 2026-04-15 remains the latest recorded runtime execution baseline. See `/.ai/10_state/active_context.md` and `/.ai/10_state/decisions.md` for that historical delivery record.

## Active Planning / Governance Tracks

### Recent Completed Governance Work (archived)
- PASS 2 stabilization plan archived to `/.ai/09_archive/plans/2026-04-16_master-audit-implementation-plan.md`
- Duplicate canonical source ID remediation archived to `/.ai/09_archive/plans/2026-04-16_duplicate-canonical-source-id-remediation-plan.md`
- These are complete historical references, not active dispatcher plans.

### 1. Whole-Codebase Plan Layer Rewrite
- Status: active
- Governing artifact: `/.ai/03_plans/2026-04-16-whole-codebase-plans-upgrade-plan.md`
- Goal: make the live plan layer truthful, codebase-aware, and internally consistent

### 2. Nested AGENTS Governance
- Status: accepted / pending execution
- Governing artifact: `/.ai/03_plans/2026-04-15-nested-agents-governance-plan.md`
- Goal: finish the justified hierarchical `AGENTS.md` system at the major repo boundaries

### 3. AEC Engine Planning Family
- Status: baseline-ready / evidence-pending (planning/control layer)
- Governing artifact: `/.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`
- Active sprint artifact: `/.ai/03_plans/2026-04-16-aec-first-bounded-slice-sprint-plan.md`
- Current truth:
  - the bounded-slice candidate has been converted into a true sprint plan
  - a fresh implementation trigger now exists
  - the clean baseline branch/worktree is explicit
  - planning/control blockers for the first bounded slice are cleared
  - the clean baseline exists, but the machine-readable gate artifact still holds `ready_to_implement=false` because execution evidence scaffolds are not yet present
- Blocking gates:
  - execution evidence scaffolds must exist before the first bounded slice can start
  - execution is presently deferred while another Codex task may create conflicts on overlapping repo surfaces
- State-model reference:
  - `/.ai/04_tasks/aec-readiness-vocabulary-and-state-model-2026-04-16.md`
- Conflict protocol:
  - `/.ai/04_tasks/aec-concurrent-execution-deferral-and-write-scope-2026-04-16.md`

### 4. Laws Mini Dataset→Graph Pipeline
- Status: bounded pilot success achieved on 2026-04-16; M3 complete; M4 complete
- Governing artifact: `/.ai/03_plans/2026-04-16_laws-mini-dataset-graph-pipeline-plan.md`
- Goal: prove a truthful, manifest-backed core-laws-bundle scoped graph first, then stage toward broader per-section and interconnected graph workflows
- Phase 11 note: this is a **bounded pilot lane**, not a generic opening of Phase 11 dataset expansion; it may execute only within the accepted M1 scope and guardrails
- Latest validation: `/.ai/05_logs/2026-04-17_laws-pilot-operator-experience-validation.md`
- Follow-on planning artifact: `/.ai/03_plans/2026-04-16_laws-m2-admission-plan.md`
- Follow-on planning state:
  - M2A source admission has now been executed for `RA-9514`, `BP-344`, and `BP-220`; see `/.ai/05_logs/2026-04-16_laws-m2a-source-admission-validation.md`
  - additive M2B dataset-safe stage wiring is now implemented; see `/.ai/05_logs/2026-04-16_laws-m2b-dataset-safe-stage-validation.md`
  - conservative RA-9514 relationship admission is now complete in the official scoped graph; see `/.ai/05_logs/2026-04-16_laws-m2b-relationship-admission-validation.md`
  - concept-fit follow-on slice admitted minimal concepts and relationship-backed edges for `BP-344` and `BP-220`
  - M3 orchestration is now complete via `run-dataset-graph`; see `/.ai/05_logs/2026-04-16_laws-m3-orchestration-validation.md`
  - M4A model/spec artifacts are complete and M4B minimal additive `law_units` manifest/runtime/reporting support is now complete; see `/.ai/05_logs/2026-04-16_laws-m4-expansion-path-validation.md`
  - bounded pilot success validation: `/.ai/05_logs/2026-04-16_laws-core-bundle-bounded-pilot-success-validation.md`
  - bounded pilot operator path is now available via `run-laws-pilot` and `./run-laws-pilot`, with self-contained HTML output and browser-open support; see `/.ai/05_logs/2026-04-17_laws-pilot-operator-experience-validation.md`
  - dataset snapshot provenance now records `contributing_law_ids` from the manifest-backed law-unit contract
  - current truthful bounded state:
    - `PD-1096` = `covered`
    - `RA-9514` = `covered`
    - `BP-344` = `covered`
    - `BP-220` = `covered`

## Historical Runtime Context
The prior sprint chain remains important historical context, but it is not the active dispatcher anymore.

Use it for:
- understanding what already shipped
- checking archived sprint lineage
- locating prior validation evidence

Do not use it for:
- choosing the next live plan by default
- assuming a closed side-track is still the current action

## Next Gates

1. Finish validation of the current plan-layer rewrite.
2. If AGENTS coverage remains incomplete after validation, execute the nested-AGENTS governance plan.
3. If AEC implementation is requested, accept the planned namespace and the relevant subsystem slice, then create fresh trigger/baseline/research/audit artifacts before coding.
4. If follow-on laws dataset work is requested, keep it inside the accepted bounded pilot lane: the bounded four-folder pilot is successful and the accepted M4 slice is complete, but generic Phase 11 expansion remains gated. Any new section-scoped runtime, merged-graph runtime, or broader all-laws expansion work requires a fresh accepted slice rather than continuation by momentum.

## Not Current By Default
- archived sprint plans under `/.ai/09_archive/plans/`
- historical Phase 1B modernization expansion as the “natural next side-track”
- branch-specific cleanup tasks tied to old feature-branch naming

## Reference
- Governing plan → `/.ai/03_plans/00-governing-implementation-plan.md`
- Plan index → `/.ai/03_plans/INDEX.md`
- Milestone tracker → `/.ai/01_roadmap/milestone-tracker.md`
- Active context → `/.ai/10_state/active_context.md`
- Decisions → `/.ai/10_state/decisions.md`
- Known issues → `/.ai/10_state/known_issues.md`
- Archived plans → `/.ai/09_archive/plans/`
