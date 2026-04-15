---
title: AEC Engine Optimization Engine Implementation Plan
type: subsystem-plan
status: proposed
date: 2026-04-16
last_updated: 2026-04-16
planned_code_locations:
  - scripts/vitruvius/aec/optimization/objectives.py
  - scripts/vitruvius/aec/optimization/pareto.py
  - scripts/vitruvius/aec/optimization/search.py
repo_grounding:
  - scripts/vitruvius/geometric/pareto_optimizer.py
  - scripts/vitruvius/graph/physics.py
  - scripts/tests/test_geometric_pareto_optimizer.py
governing_inputs:
  - .ai/06_specs/AEC_ENGINE/09_PARETO_OPTIMIZATION_AND_FINANCIAL_LAYER_RULES.md
  - .ai/06_specs/AEC_ENGINE/08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md
  - .ai/06_specs/GOVERNANCE/06_PERFORMANCE_BUDGET_AND_BENCHMARK_POLICY.md
---

# AEC Engine Optimization Engine Implementation Plan

## 1. Scope
Score verified AEC candidates and rank or filter them using deterministic objective vectors and Pareto logic.

This subsystem begins with deterministic selection.
Any later stochastic search is a gated extension, not baseline behavior.

## 2. Current Repo Anchors
- `scripts/vitruvius/geometric/pareto_optimizer.py` already ships a narrow deterministic optimization site
- `scripts/tests/test_geometric_pareto_optimizer.py` already provides precedent for optimizer-style validation
- `scripts/vitruvius/graph/physics.py` already shows the repo’s pattern for deterministic report-style scoring utilities

## 3. Planned Code Locations
- `scripts/vitruvius/aec/optimization/objectives.py`
- `scripts/vitruvius/aec/optimization/pareto.py`
- `scripts/vitruvius/aec/optimization/search.py`

## 4. V1 Ceiling
- deterministic score vector only
- Pareto frontier construction only
- optional seeded search only after deterministic baseline is stable
- no broad simulated annealing or MCTS by default

## 5. Responsibilities
- objective vector definition
- dominance comparison
- Pareto frontier generation
- reproducibility metadata for every chosen candidate

## 6. Boundaries
- must not bypass Z3 verification
- must not invent law or pricing inputs
- must not let LLMs steer the search policy
- must not hide stochasticity without explicit seeding and replay metadata

## 7. Inputs / Outputs

### Inputs
- verified candidate set
- coordination issue summaries
- quantity and pricing summaries
- explicit optimization objective policy

### Outputs
- ranked or frontier-tagged candidate set
- deterministic score vectors
- reproducibility metadata

## 8. Data Contracts
- `candidate_id`
- `objective_vector`
- `frontier_rank`
- `optimization_run_id`
- `seed` when stochastic search is enabled
- `reproducibility_manifest`

## 9. Dependencies
- AEC master plan
- coordination plan
- pricing plan
- Z3 verification plan

## 10. Ordered Implementation Steps
1. Freeze the v1 objective vector and dominance rules.
2. Implement deterministic scoring over verified candidates.
3. Implement Pareto frontier construction.
4. Reuse the repo’s existing report-oriented result style rather than raw tuples or ad hoc dicts.
5. Add optional seeded search only after deterministic ranking is benchmarked and replayable.

## 11. Edge Cases
- multiple candidates on the same frontier
- candidate sets with missing pricing or quantity inputs
- ties across every objective
- stochastic extension with seed collisions or hidden randomness

## 12. Risks
- optimization silently becomes acceptance authority
- objective vectors drift without versioning
- stochastic search is introduced without replay guarantees
- price and performance signals are mixed without explicit weighting policy

## 13. Validation Plan

### Existing Tests To Reuse As Pattern
- `python -m pytest scripts/tests/test_geometric_pareto_optimizer.py`

### New Tests Required
- `scripts/tests/test_aec_optimization_objectives.py`
- `scripts/tests/test_aec_optimization_frontier.py`
- `scripts/tests/test_aec_optimization_replay.py`
- `scripts/tests/test_aec_optimization_seeded_search.py`

### Acceptance Gates
- deterministic frontier on fixed fixture set
- same fixture inputs produce identical frontier membership
- stochastic extension refuses to run without explicit seed and replay metadata

## 14. Performance Considerations
- stay in Python until objective scoring itself is proven hot
- measure candidate-set growth before introducing heavier search
- keep stochastic search behind a feature or explicit execution gate

## 15. Execution Checklist
- [ ] objective vector frozen
- [ ] dominance rules frozen
- [ ] deterministic frontier implemented
- [ ] replay metadata schema defined
- [ ] stochastic path still deferred or fully seeded
- [ ] new `test_aec_optimization_*` suite added

## 16. Stop Conditions
- optimization is asked to bless unverified candidates
- weighting policy is undefined
- seeded search cannot be replayed
- deterministic baseline is skipped in favor of broad heuristic search
