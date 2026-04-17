# Current Phase — Between Sprints / Governance & Planning Maintenance

> **Authoritative roadmap:** `/.ai/01_roadmap/master-roadmap.md` (v2.3.0)
> **Authoritative execution order:** `/.ai/03_plans/00-governing-implementation-plan.md` (v4.0.0)
> **This document:** live snapshot of active execution state and the next valid gates
> **Updated:** 2026-04-17

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
  - post-pilot whole-dataset readiness follow-on is now in place as a readiness-only lane:
    - planning artifacts created for all-laws / 8GB rollout
    - `run-laws-all-dry-run` added as the next safe step
    - `m2-8gb-safe` review preset added for bounded planning / dry-run work
    - see `/.ai/05_logs/2026-04-17_all-laws-readiness-8gb-implementation-validation.md`
  - next truthful execution boundary is now documented as **tranche expansion**, not generic all-laws execution:
    - research / audit / rollout-plan artifacts created for tranche-based widening
    - see `/.ai/05_logs/2026-04-17_laws-tranche-expansion-planning-validation.md`
  - tranche implementation follow-on is now in place:
    - `config/datasets/laws-tranche-1.yaml`
    - `run-laws-tranche-dry-run`
    - structure-vs-concept guardrails now surface BP220-style shallowness automatically in readiness reporting
    - see `/.ai/05_logs/2026-04-17_laws-tranche-expansion-implementation-validation.md`
  - tranche source-preparation follow-on is now in place:
    - `run-laws-tranche-source-prep-dry-run`
    - tranche raw-file inventory and expected convert/refine output reporting
    - see `/.ai/05_logs/2026-04-17_laws-tranche-source-prep-dry-run-validation.md`
  - tranche source-preparation execute step is now in place:
    - `run-laws-tranche-source-prep`
    - current tranche-1 result: `prepared_count = 5`, `ocr_required_count = 1`
    - see `/.ai/05_logs/2026-04-17_laws-tranche-source-prep-implementation-validation.md`
  - tranche-1 source-admission checkpoint is now implemented:
    - `run-laws-tranche-source-admission-dry-run`
    - current tranche split: ready = `PD-957`, `PD-1185`; blocked = `PD-1216`
    - see `/.ai/05_logs/2026-04-17_laws-tranche-1-source-admission-implementation-validation.md`
  - tranche-1 source-admission execute step is now complete:
    - `run-laws-tranche-source-admission`
    - admitted canonical source pages:
      - `revised-implementing-rules-and-regulations-for-pd-957.md`
      - `fire-code-of-the-philippines.md`
    - `PD-957` duplicate/raw-alias guardrails now collapse the same-content raw cluster to one authoritative representative while keeping excluded aliases explicit
    - `PD-1216` remains explicitly blocked pending OCR
    - see `/.ai/05_logs/2026-04-17_laws-tranche-1-source-admission-execution-validation.md`
  - duplicate-readiness guardrails now exist before broader widening:
    - `run-laws-duplicate-dry-run`
    - exact duplicate raw-PDF clusters now surface in both:
      - `run-laws-all-dry-run`
      - `run-laws-tranche-dry-run`
    - current whole-laws evidence reports 9 duplicate clusters; tranche-1 reports 1 duplicate cluster affecting `PD-957`
    - see `/.ai/05_logs/2026-04-17_laws-duplicate-readiness-validation.md`
  - tranche-local source-to-graph dry-run now exists:
    - `run-laws-tranche-source-to-graph-dry-run`
    - stages only admitted tranche members:
      - `PD-957`
      - `PD-1185`
    - keeps blocked member explicit:
      - `PD-1216`
    - current live dry-run now shows `planned_stage_count = 2`, `shallow_representation_count = 0`, and `source_to_graph_execute_ready = false`
    - see `/.ai/05_logs/2026-04-17_laws-tranche-source-to-graph-dry-run-validation.md`
  - PD-957 concept-fit follow-on slice is now admitted:
    - shared concepts admitted:
      - `floor-area`
      - `setbacks`
      - `yards`
    - dataset-scoped `governs` relationships admitted for the same three concepts
    - this removes the tranche shallow-representation finding without widening execute
    - see `/.ai/05_logs/2026-04-17_pd957-concept-fit-admission-validation.md`
  - PD-1216 OCR-first preparation is now complete:
    - OCR PDF + raw markdown + refined markdown + sidecar JSON now exist
    - PD-1216 source admission is now executed
    - tranche source-to-graph dry-run now stages:
      - `PD-957`
      - `PD-1216`
      - `PD-1185`
    - current live dry-run shows `planned_stage_count = 3`, `blocked_law_folders = []`, `shallow_representation_count = 0`, and `source_to_graph_execute_ready = false`
    - see `/.ai/05_logs/2026-04-17_pd1216-ocr-first-preparation-validation.md`
  - tranche-local source-to-graph execute wrapper is now complete:
    - `run-laws-tranche-source-to-graph`
    - current live execute stages:
      - `PD-957`
      - `PD-1216`
      - `PD-1185`
    - current live execute shows:
      - `generated_relationship_count = 2`
      - `filtered_relationship_count = 0`
      - `shallow_representation_count = 0`
      - `source_to_graph_execute_completed = true`
    - see `/.ai/05_logs/2026-04-17_laws-tranche-source-to-graph-execute-validation.md`
  - bounded risk-hardening pass is now in progress/completed for the current tranche:
    - duplicate/raw-alias visibility for `PD-957` is now surfaced more explicitly in tranche dry-run/execute reports
    - OCR-quality acceptance for `PD-1216` now rolls up as spot-review-required rather than a silent accept path
    - fresh tranche dry-run/execute now show:
      - `duplicate_law_folders = [PD-957]`
      - `spot_review_required_count = 1`
      - `summary_auto_withheld_count = 1`
    - see `/.ai/05_logs/2026-04-17_laws-risk-hardening-execution-validation.md`
  - tranche-2 is now defined and executed through the same bounded workflow:
    - manifest: `config/datasets/laws-tranche-2.yaml`
    - tranche-2 laws:
      - `RA-7279`
      - `RA-4726`
      - `RA-7899`
    - current execute evidence:
      - `staged_law_folders = [RA-7279, RA-4726, RA-7899]`
      - `duplicate_law_folders = []`
      - `generated_relationship_count = 0`
      - `source_to_graph_execute_completed = true`
    - see `/.ai/05_logs/2026-04-17_laws-tranche-2-execution-validation.md`
  - tranche-2 graph-richness follow-on is now started with a bounded `RA-7899` concept-fit slice:
    - admitted concept:
      - `floor-area`
    - admitted dataset-scoped relationship:
      - `law-amendments-to-the-condominium-act governs concept-floor-area`
    - fresh tranche-2 execute graph moves from:
      - `3 nodes / 0 edges`
      - to `4 nodes / 1 edge`
    - see `/.ai/05_logs/2026-04-17_ra7899-concept-fit-admission-validation.md`
  - tranche-2 common-areas follow-on is now started with a bounded `RA-4726` concept-fit slice:
    - new shared concept:
      - `common-areas`
    - admitted dataset-scoped relationship:
      - `law-condominium-act governs concept-common-areas`
    - fresh tranche-2 execute graph moves from:
      - `4 nodes / 1 edge`
      - to `5 nodes / 4 edges`
    - see `/.ai/05_logs/2026-04-17_ra4726-common-areas-concept-fit-validation.md`
  - tranche-2 socialized-housing follow-on is now started with a bounded `RA-7279` concept-fit slice:
    - admitted concept:
      - `socialized-housing-projects`
    - admitted dataset-scoped relationship:
      - `law-urban-development-and-housing-act governs concept-socialized-housing-projects`
    - fresh tranche-2 execute graph moves from:
      - `5 nodes / 4 edges`
      - to `6 nodes / 5 edges`
    - see `/.ai/05_logs/2026-04-17_ra7279-socialized-housing-concept-fit-validation.md`
  - tranche-3 is now defined and executed through the same bounded workflow:
    - manifest: `config/datasets/laws-tranche-3.yaml`
    - tranche-3 laws:
      - `PD-1067`
      - `PD-1151`
      - `RA-9003`
    - current execute evidence:
      - `staged_law_folders = [PD-1067, PD-1151, RA-9003]`
      - `duplicate_law_folders = []`
      - `raw_alias_law_folders = [PD-1067]`
      - `generated_relationship_count = 0`
      - `shallow_representation_count = 0`
      - `source_to_graph_execute_completed = true`
    - tranche source admission now respects manifest-level authoritative/excluded variant intent, preserving explicit raw-alias visibility for `PD-1067`
    - bounded `PD-1067` water-governance concept-fit follow-on is now admitted:
      - concepts:
        - `water-permit`
        - `water-right`
        - `groundwater-drilling`
      - fresh tranche-3 execute graph moves from:
        - `4 nodes / 0 edges`
        - to `7 nodes / 11 edges`
    - see `/.ai/05_logs/2026-04-17_laws-tranche-3-execution-validation.md`
    - see `/.ai/05_logs/2026-04-17_tranche-source-admission-variant-selection-validation.md`
    - see `/.ai/05_logs/2026-04-17_pd1067-water-governance-concept-fit-validation.md`
  - tranche-4 is now defined and executed through the same bounded workflow:
    - manifest: `config/datasets/laws-tranche-4.yaml`
    - tranche-4 laws:
      - `PD-1517`
      - `RA-6969`
      - `RA-10066`
    - current execute evidence:
      - `staged_law_folders = [PD-1517, RA-6969, RA-10066]`
      - `duplicate_law_folders = []`
      - `generated_relationship_count = 1`
      - `spot_review_required_count = 1`
      - `shallow_representation_count = 0`
      - `source_to_graph_execute_completed = true`
    - bounded `RA-10066` cultural-heritage concept-fit follow-on is now admitted:
      - concepts:
        - `adaptive-reuse`
        - `built-heritage`
        - `heritage-zone`
      - fresh tranche-4 execute graph moves from:
        - `3 nodes / 0 edges`
        - to `6 nodes / 7 edges`
    - see `/.ai/05_logs/2026-04-17_laws-tranche-4-execution-validation.md`
    - see `/.ai/05_logs/2026-04-17_tranche-4-scouting-validation.md`
    - see `/.ai/05_logs/2026-04-17_ra10066-cultural-heritage-concept-fit-validation.md`
  - tranche-5 is now defined and executed through the same bounded workflow:
    - manifest: `config/datasets/laws-tranche-5.yaml`
    - tranche-5 laws:
      - `PD-856`
      - `RA-7160`
      - `RA-9257`
    - current execute evidence:
      - `staged_law_folders = [PD-856, RA-7160, RA-9257]`
      - `duplicate_law_folders = []`
      - `generated_relationship_count = 7`
      - `shallow_representation_count = 0`
      - `source_to_graph_execute_completed = true`
      - graph snapshot: `13 nodes / 24 edges`
    - `RA-9257` folder naming remains explicit while canonical source truth resolves to `RA 9275 / Philippine Clean Water Act of 2004`
    - see `/.ai/05_logs/2026-04-17_tranche-5-richness-validation.md`
  - tranche-6 scouting now favors a compact construction / civil / procurement governance cohort:
    - rejected scout set:
      - `RA-4566`
      - `RA-9184`
      - `RA-9266`
      - because `RA-9266` currently carries duplicate risk
    - preferred scout set:
      - `RA-4566`
      - `RA-386`
      - `RA-9184`
    - see `/.ai/13_research/2026-04-17_tranche-6-expansion-research.md`
  - tranche-6 is now defined and executed through the same bounded workflow:
    - manifest: `config/datasets/laws-tranche-6.yaml`
    - tranche-6 laws:
      - `RA-4566`
      - `RA-386`
      - `RA-9184`
    - current execute evidence:
      - `staged_law_folders = [RA-4566, RA-386, RA-9184]`
      - `duplicate_law_folders = []`
      - `generated_relationship_count = 3`
      - `shallow_representation_count = 0`
      - `source_to_graph_execute_completed = true`
      - graph snapshot: `7 nodes / 9 edges`
    - bounded `RA-9184` procurement concept-fit follow-on is now admitted
    - see `/.ai/05_logs/2026-04-17_laws-tranche-6-execution-validation.md`
    - see `/.ai/05_logs/2026-04-17_ra9184-procurement-concept-fit-validation.md`
  - tranche-7 is now defined and executed through the same bounded workflow:
    - manifest: `config/datasets/laws-tranche-7.yaml`
    - tranche-7 laws:
      - `RA-1378`
      - `RA-9285`
      - `RA-11201`
    - current execute evidence:
      - `staged_law_folders = [RA-1378, RA-9285, RA-11201]`
      - `blocked_law_folders = []`
      - `generated_relationship_count = 0`
      - `shallow_representation_count = 0`
      - `source_to_graph_execute_completed = true`
      - graph snapshot: `7 nodes / 6 edges`
    - bounded `RA-11201` housing-governance concept-fit follow-on is now admitted
    - `RA-1378` now stages cleanly on the authoritative `MASTER PLUMBING LAW.pdf` path while excluded auxiliary plumbing-code / board files remain explicit raw aliases
    - see `/.ai/05_logs/2026-04-17_laws-tranche-7-execution-validation.md`
    - see `/.ai/05_logs/2026-04-17_ra11201-housing-governance-concept-fit-validation.md`
    - see `/.ai/05_logs/2026-04-17_laws-tranche-7-clean-rerun-validation.md`
  - tranche-8 is now defined and executed through the same bounded workflow:
    - manifest: `config/datasets/laws-tranche-8.yaml`
    - tranche-8 law:
      - `RA-11285`
    - current execute evidence:
      - `staged_law_folders = [RA-11285]`
      - `duplicate_law_folders = []`
      - `generated_relationship_count = 0`
      - `shallow_representation_count = 0`
      - `source_to_graph_execute_completed = true`
      - graph snapshot: `4 nodes / 6 edges`
    - bounded `RA-11285` energy-governance concept-fit follow-on is now admitted
    - see `/.ai/05_logs/2026-04-17_laws-tranche-8-execution-validation.md`
    - see `/.ai/05_logs/2026-04-17_ra11285-energy-governance-concept-fit-validation.md`
  - remaining uncovered-pool roadmap is now explicit for planning/tracking:
    - see `docs/LAWS_REMAINING_POOL_ROADMAP.md`
    - see `/.ai/13_research/2026-04-17_remaining-pool-tranche-roadmap-research.md`
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
