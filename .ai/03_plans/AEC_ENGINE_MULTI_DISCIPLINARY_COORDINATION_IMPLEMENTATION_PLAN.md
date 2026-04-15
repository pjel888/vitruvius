---
title: AEC Engine Multi-Disciplinary Coordination Implementation Plan
type: subsystem-plan
status: proposed
date: 2026-04-16
last_updated: 2026-04-16
planned_code_locations:
  - scripts/vitruvius/aec/coordination/models.py
  - scripts/vitruvius/aec/coordination/precedence.py
  - scripts/vitruvius/aec/coordination/service.py
  - scripts/vitruvius/aec/coordination/replay.py
repo_grounding:
  - scripts/vitruvius/compound/dependency_tracker.py
  - scripts/vitruvius/compound/differential_propagator.py
  - scripts/vitruvius/query/engine.py
  - scripts/vitruvius/graph/physics.py
  - scripts/vitruvius/graph/event_store.py
governing_inputs:
  - .ai/06_specs/AEC_ENGINE/05_MULTI_DISCIPLINARY_COORDINATION_RULES.md
  - .ai/06_specs/AEC_ENGINE/08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md
  - .ai/06_specs/GOVERNANCE/01_VALIDATION_PROTOCOL.md
---

# AEC Engine Multi-Disciplinary Coordination Implementation Plan

## 1. Scope
Coordinate architecture, structure, MEP, fire/egress, and related discipline constraints on a single bounded AEC candidate model.

This subsystem owns:
- issue aggregation
- precedence
- escalation
- replayable coordination logs

It does not own legal interpretation, geometry-heavy compute, or pricing authority.

## 2. Current Repo Anchors
- `compound/dependency_tracker.py` already models deterministic dependency registration
- `compound/differential_propagator.py` already models bounded invalidation walks
- `query/engine.py` already models evidence-citing deterministic query outputs
- `graph/physics.py` already shows how the repo packages ranking/priority computations as deterministic reports

These are implementation idioms, not a license to dump AEC coordination into unrelated existing modules.

## 3. Planned Code Locations
- `scripts/vitruvius/aec/coordination/models.py`
- `scripts/vitruvius/aec/coordination/precedence.py`
- `scripts/vitruvius/aec/coordination/service.py`
- `scripts/vitruvius/aec/coordination/replay.py`

## 4. Responsibilities
- discipline request schema
- conflict/issue registry
- precedence manifest
- escalation classes
- deterministic replay of coordination decisions
- change-cascade invalidation after accepted modifications

## 5. Boundaries
- must not call LLM roles to negotiate discipline truth
- must not own geometry compute
- must not bypass Z3 verification
- must not collapse pricing into discipline precedence

## 6. Inputs / Outputs

### Inputs
- ECS snapshots
- spatial clash and route results
- verification violations and witnesses
- price/quantity summaries as read-only context

### Outputs
- coordination issue set
- precedence/routing decisions
- escalation worklists
- replay log

## 7. Data Contracts
- `coordination_run_id`
- `discipline_request_id`
- `coordination_issue_id`
- `precedence_rule_id`
- `escalation_state`
- `affected_entity_ids`
- `replay_event`

## 8. Dependencies
- AEC master plan
- ECS core plan
- spatial kernel plan
- Z3 verification plan
- pricing plan

## 9. Ordered Implementation Steps
1. Freeze the discipline enum and precedence manifest.
2. Define the coordination issue model that can carry:
   - spatial conflict
   - rule conflict
   - quantity/pricing impact summary
3. Reuse dependency-tracker style invalidation for downstream issue recalculation.
4. Implement a deterministic resolver with explicit escalation outcomes:
   - auto-resolved
   - blocked pending upstream fix
   - human review required
5. Add replay logging so the same inputs yield the same issue ordering and escalation set.
6. Only after the deterministic path is stable, consider more advanced coordination heuristics.

## 10. Edge Cases
- one change fixes one discipline while breaking another
- issue oscillation between two local optima
- coordination cascades that touch many downstream entities
- precedence ambiguity between discipline rules
- stale pricing context attached to a changed model

## 11. Risks
- coordination degenerates into implicit optimization
- precedence is undocumented and becomes guesswork
- replay logs do not capture enough context to reproduce the decision
- pricing starts steering coordination instead of informing it

## 12. Validation Plan

### Existing Tests To Reuse As Pattern
- `python -m pytest scripts/tests/test_query_engine.py`
- `python -m pytest scripts/tests/test_graph_event_store_delta.py`
- `python -m pytest scripts/tests/test_graphrag_router.py`

### New Tests Required
- `scripts/tests/test_aec_coordination_precedence.py`
- `scripts/tests/test_aec_coordination_replay.py`
- `scripts/tests/test_aec_coordination_escalation.py`
- `scripts/tests/test_aec_coordination_oscillation.py`

### Acceptance Gates
- the same inputs yield the same issue order and escalation outcomes
- precedence is explicit, not inferred from dictionary order
- cascade bounds are tested on multi-issue fixtures

## 13. Performance Considerations
- avoid rebuilding the full issue graph on every tiny delta if dependency-local invalidation is enough
- keep coordination logs structured and compact
- defer any global search behavior to the optimization subsystem

## 14. Execution Checklist
- [ ] discipline enum frozen
- [ ] precedence manifest frozen
- [ ] escalation states defined
- [ ] replay log schema defined
- [ ] invalidation path bounded
- [ ] new `test_aec_coordination_*` suite added

## 15. Stop Conditions
- precedence rules are undefined
- oscillation cannot be detected or bounded
- coordination attempts to replace verification or optimization
- replay logs cannot reproduce the same issue ordering
