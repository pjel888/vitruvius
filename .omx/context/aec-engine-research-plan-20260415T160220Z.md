## Task Statement
Convert `.ai/13_research/AEC-ECS-SC_RESEARCH.md` into one master governing implementation plan plus multiple subsystem implementation plans under `.ai/03_plans`, following the Vitruvius execution loop.

## Desired Outcome
- Research-derived audit grounded in repo reality
- One master AEC engine implementation plan
- Multiple subsystem implementation plans with strict boundaries
- Plan critique covering overreach, hidden dependencies, and drift risks
- Validation report confirming completeness and consistency

## Known Facts / Evidence
- Research document is explicitly marked exploratory, not executable.
- Root authority stack is `AGENTS.md` -> `EXECUTION_LOOP.md` -> `principles.md` -> roadmap/state -> specs.
- Relevant law packs are present under `.ai/06_specs/GOVERNANCE/`, `.ai/06_specs/RUST/`, and `.ai/06_specs/AEC_ENGINE/`.
- Repo roadmap/state indicate Vitruvius already has substantial pipeline, graph, Rust, and query infrastructure, but not a fully integrated AEC engine implementation plan set.
- Current live planning directory contains only `00-governing-implementation-plan.md`, an index, and a nested-AGENTS plan from separate work.

## Constraints
- Do not write code.
- Do not treat research as direct instructions.
- Plans must align with GOVERNANCE, RUST, and AEC_ENGINE packs.
- Plans must remain grounded in current repo state and roadmap.
- Subsystems must stay boundary-clean: LLM speaks, Python orchestrates, Rust computes, RocksDB stores rules, Z3 adjudicates.

## Unknowns / Open Questions
- Exact persistence mechanism for future ECS state remains unsettled.
- Extent of early FEA support is unresolved.
- WFC and stochastic search maturity is unresolved.
- Final concurrency model is unresolved.
- Precise repo placement for future AEC runtime code is not yet decided by existing state docs.

## Likely Touchpoints
- `.ai/13_research/AEC-ECS-SC_RESEARCH.md`
- `.ai/06_specs/AEC_ENGINE/*`
- `.ai/06_specs/GOVERNANCE/*`
- `.ai/06_specs/RUST/*`
- `.ai/01_roadmap/master-roadmap.md`
- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/03_plans/`
- `.ai/02_audits/`
- `.ai/05_logs/`
