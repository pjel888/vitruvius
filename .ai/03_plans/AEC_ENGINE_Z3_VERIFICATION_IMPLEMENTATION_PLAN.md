---
title: AEC Engine Z3 Verification Implementation Plan
type: subsystem-plan
status: proposed
date: 2026-04-16
last_updated: 2026-04-16
planned_code_locations:
  - scripts/vitruvius/aec/verification/ast.py
  - scripts/vitruvius/aec/verification/compiler.py
  - scripts/vitruvius/aec/verification/service.py
  - scripts/vitruvius/aec/verification/artifacts.py
repo_grounding:
  - scripts/vitruvius/spatial/constraint_solver.py
  - scripts/vitruvius/geometric/inequality_compiler.py
  - scripts/vitruvius/spatial/cli.py
  - scripts/tests/test_spatial_constraint_solver.py
  - scripts/tests/test_geometric_inequality_compiler.py
governing_inputs:
  - .ai/06_specs/AEC_ENGINE/06_FORMAL_VERIFICATION_AND_Z3_PROTOCOL.md
  - .ai/06_specs/AEC_ENGINE/08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md
  - .ai/06_specs/GOVERNANCE/01_VALIDATION_PROTOCOL.md
---

# AEC Engine Z3 Verification Implementation Plan

## 1. Scope
Compile admitted vault rules plus candidate world facts into bounded Z3 problems that return:
- satisfiable / unsatisfiable verdicts
- witness assignments
- unsat cores or equivalent failure artifacts
- replayable audit envelopes

## 2. Current Repo Anchors
- `scripts/vitruvius/spatial/constraint_solver.py` already proves the repo’s lazy-import and fixture-first Z3 discipline
- `scripts/vitruvius/geometric/inequality_compiler.py` already compiles parametric rules into Z3 expressions
- `scripts/vitruvius/spatial/cli.py` already shows flag-gated evaluation behavior

These are precedents only. The AEC verifier must become a separate subsystem under `scripts/vitruvius/aec/verification/`.

## 3. Initial Supported Rule Families
- scalar min/max constraints
- pairwise clearance or separation constraints using geometry facts precomputed outside Z3
- count, area, and ratio constraints using numeric inputs computed outside the solver
- axis-aligned or precomputed envelope inequalities

## 4. Explicitly Unsupported In V1
- raw legal prose ingestion at runtime
- exception chains expressed only in natural language
- continuous geometry search inside Z3
- non-linear structural, fluid, or thermal solving
- stochastic or probabilistic reasoning

## 5. Responsibilities
- AST-to-solver compilation
- variable binding and namespace discipline
- sat/unsat artifact generation
- replay of a verification run from stored inputs

## 6. Boundaries
- must not replace the spatial kernel
- must not parse raw law on the fly
- must not become the optimizer
- must not emit user-facing explanations directly

## 7. Inputs / Outputs

### Inputs
- admitted rule ASTs from the vault
- candidate state variables from ECS
- geometry-derived facts from the spatial kernel
- explicit query bounds and timeout policy

### Outputs
- sat/unsat verdict
- witness payload
- unsat payload
- replayable audit artifact

## 8. Data Contracts
- `verification_run_id`
- `snapshot_id`
- `rule_family`
- `variable_binding_schema`
- `witness_artifact`
- `unsat_artifact`
- `timeout_reason` or `refusal_reason`

## 9. Dependencies
- AEC master plan
- knowledge vault plan
- ECS core plan
- spatial kernel plan

## 10. Ordered Implementation Steps
1. Freeze the supported-rule whitelist and explicit refusal list.
2. Define the AST compiler boundary under `scripts/vitruvius/aec/verification/`.
3. Define witness and unsat artifact schemas.
4. Build replay fixtures from stored snapshot + rule inputs.
5. Add timeout and oversize-query refusal behavior.
6. Only after the bounded path is stable, consider expanding supported rule families.

## 11. Edge Cases
- under-specified candidate state
- conflicting rule families in one batch
- mixed units entering a supposedly scalar comparison
- solver timeout on combinatorial blow-up
- geometry facts that should have been computed outside Z3

## 12. Risks
- Z3 treated as the source of legal meaning
- unsupported rule classes smuggled into the compiler
- unit or tolerance ambiguity hidden in variable names
- oversize queries accepted without bounded behavior

## 13. Validation Plan

### Existing Tests To Reuse
- `python -m pytest scripts/tests/test_spatial_constraint_solver.py`
- `python -m pytest scripts/tests/test_geometric_inequality_compiler.py`
- `python -m pytest scripts/tests/test_spatial_cli.py`

### New Tests Required
- `scripts/tests/test_aec_z3_compiler.py`
- `scripts/tests/test_aec_z3_replay.py`
- `scripts/tests/test_aec_z3_refusals.py`
- `scripts/tests/test_aec_z3_artifacts.py`

### Acceptance Gates
- at least two sat and two unsat fixtures per supported rule family
- unsupported families are refused explicitly
- replay from stored artifacts is deterministic
- timeout behavior is defined and exercised

## 14. Performance Considerations
- precompute geometry facts outside the solver
- keep variable sets small and named predictably
- benchmark query families before widening the whitelist

## 15. Execution Checklist
- [ ] supported whitelist frozen
- [ ] unsupported list frozen
- [ ] witness/unsat artifact schemas frozen
- [ ] timeout/refusal behavior defined
- [ ] replay harness added
- [ ] new `test_aec_z3_*` suite added

## 16. Stop Conditions
- raw legal prose is entering the solver
- geometry-heavy search is being pushed into Z3
- units or tolerances are implied rather than explicit
- timeout and refusal behavior are undefined
