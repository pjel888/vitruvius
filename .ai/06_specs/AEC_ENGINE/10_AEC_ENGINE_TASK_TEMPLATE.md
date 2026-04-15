# AEC Engine Task Template

## Purpose
Use this template for every non-trivial AEC-engine task. Fill every section honestly. Do not delete unanswered fields; write `unknown`, `n/a`, or `not yet determined` and explain why.

## Scope
This template is mandatory for work that touches:
- LLM tool routing for the AEC engine
- Python orchestration, rule compilation, or optimization
- Rust spatial / ECS / engineering kernels
- rule-vault schema or ingestion for AEC rules
- Z3 verification flow
- cross-layer DTOs or IFC translation
- determinism, temporal replay, or audit artifacts

## Core Principle
A task is not ready for implementation until its boundaries, contracts, and validation burden are explicit.

## 1. Task Identity
- Task name:
- Date:
- Task class (from `.ai/06_specs/GOVERNANCE/03_TASK_CLASSIFICATION_POLICY.md`):
- Current phase (`.ai/01_roadmap/current-phase.md`):
- Milestone status (`.ai/01_roadmap/milestone-tracker.md`):
- Related roadmap item:
- Related audit:
- Related plan:
- Related AD(s):
- Related feature flag(s):

## 2. Problem Statement
- What problem is being solved?
- Why now?
- What breaks or remains impossible if this task is not done?
- What is explicitly out of scope?

## 3. Governing Inputs Read
- `AGENTS.md`:
- `.ai/00_system/EXECUTION_LOOP.md`:
- `.ai/00_system/principles.md`:
- `.ai/01_roadmap/master-roadmap.md`:
- `.ai/01_roadmap/current-phase.md`:
- `.ai/01_roadmap/milestone-tracker.md`:
- `.ai/10_state/decisions.md`:
- AEC_ENGINE files read (list exact files):
- GOVERNANCE files read (list exact files):
- RUST files read (if touched):
- Research files read:

## 4. Layer-Impact Analysis
- LLM impact:
- Python impact:
- Rust impact:
- RocksDB / rule-vault impact:
- Z3 impact:
- Wasm impact (if any):
- Why each impacted layer is still inside its proper boundary:

## 5. Current-State Audit
- Existing implementation:
- Existing artifacts / files:
- Gaps found:
- Contradictions or stale docs found:
- Known risks:
- Open questions:

## 6. Data and Boundary Contracts
- Input contracts:
- Output contracts:
- Units:
- Coordinate frame:
- Tolerance policy:
- Temporal clock policy:
- Audit artifact expectations:
- Cross-language DTOs touched:
- Validation or schema files to update:

## 7. Verification and Optimization Position
- Hard-feasibility question being verified:
- Decomposition strategy for Z3 (if any):
- Financial / Pareto layer touched?:
- Why optimization remains above verification:
- Why financial semantics stay out of Rust:

## 8. Implementation Plan
1. 
2. 
3. 

## 9. Plan Critique
- Weak assumptions:
- Likely failure points:
- Boundary risks:
- Determinism risks:
- Truth / provenance risks:
- Performance risks:
- What evidence would disprove the current plan:

## 10. Execution Checklist
- [ ] verified alignment with `.ai/01_roadmap/current-phase.md` and `.ai/01_roadmap/milestone-tracker.md`
- [ ] identified every impacted AEC layer
- [ ] checked the relevant AEC_ENGINE, GOVERNANCE, and RUST documents
- [ ] documented every boundary contract touched
- [ ] defined units, coordinate frame, tolerance policy, and temporal clock policy
- [ ] defined validation commands and expected artifacts
- [ ] defined rollback or fallback path
- [ ] defined required state or AD updates

## 11. Validation Plan
- Static validation:
- Contract validation:
- Deterministic functional validation:
- Edge-case validation:
- Differential or oracle validation:
- Integration validation:
- Performance validation:
- Truth / provenance validation:
- Planned validation report path:

## 12. Completion and State Reconciliation
- Files expected to change:
- State docs that must be updated, if reality changes:
- AD required? why or why not:
- Known caveats to record if accepted:
- Final completion criteria for this task:

## Cross-References
- `00_README_AEC_ENGINE_DOC_SET.md` — pack identity and authority order
- `01_COMPOUND_AI_OPERATING_CONTRACT.md` — mandatory layer-impact analysis baseline
- `.ai/06_specs/GOVERNANCE/01_VALIDATION_PROTOCOL.md` — validation layers that the task must satisfy
- `.ai/06_specs/GOVERNANCE/03_TASK_CLASSIFICATION_POLICY.md` — task-class selection and process burden
- `.ai/06_specs/RUST/08_RUST_TASK_TEMPLATE.md` — companion template when the task touches Rust kernels or PyO3/Wasm surfaces
- `.ai/01_roadmap/current-phase.md` and `.ai/01_roadmap/milestone-tracker.md` — live state alignment before implementation

## Final Rule
Do not start implementation until Sections 4, 6, 10, and 11 are concrete enough that another engineer could audit the task without asking what the boundaries are.
