---
title: AEC Engine Financial / Pricing Oracle Implementation Plan
type: subsystem-plan
status: accepted
date: 2026-04-16
last_updated: 2026-04-16
planned_code_locations:
  - scripts/vitruvius/aec/pricing/schema.py
  - scripts/vitruvius/aec/pricing/quantities.py
  - scripts/vitruvius/aec/pricing/oracle.py
  - scripts/vitruvius/aec/pricing/artifacts.py
repo_grounding:
  - scripts/vitruvius/geometric/pareto_optimizer.py
  - scripts/vitruvius/review/domain_classifier.py
  - scripts/vitruvius/graph/event_store.py
governing_inputs:
  - .ai/06_specs/AEC_ENGINE/09_PARETO_OPTIMIZATION_AND_FINANCIAL_LAYER_RULES.md
  - .ai/06_specs/GOVERNANCE/05_TRUTH_GOVERNANCE_AND_PROMOTION_CONTRACT.md
  - .ai/06_specs/GOVERNANCE/06_PERFORMANCE_BUDGET_AND_BENCHMARK_POLICY.md
---

# AEC Engine Financial / Pricing Oracle Implementation Plan

## 0. Planning Status
- status: accepted
- execution role: downstream / not in first slice
- current use: authoritative subsystem plan paired with the accepted T018 foundation plan

## 1. Scope
Provide deterministic quantity and price scoring for verified AEC candidates using explicit pricebook snapshots.

This subsystem starts as a bounded oracle:
- no market prediction
- no FX conversion
- no business-policy interpretation

## 2. Current Repo Anchors
- `geometric/pareto_optimizer.py` already shows the repo’s style for small deterministic quantitative scoring
- `review/domain_classifier.py` already distinguishes fee/cost language from other review domains, which is useful as a reminder that pricing is domain-specific and should not be inferred generically
- `graph/event_store.py` is the right storage-style precedent for replayable cost artifacts, if event logging is needed

Current truth:
- there is no real pricing engine yet in the repo
- this plan must therefore stay narrow and explicit

## 3. Planned Code Locations
- `scripts/vitruvius/aec/pricing/schema.py`
- `scripts/vitruvius/aec/pricing/quantities.py`
- `scripts/vitruvius/aec/pricing/oracle.py`
- `scripts/vitruvius/aec/pricing/artifacts.py`

## 4. V1 Ceiling
- one currency context per run
- one pricebook snapshot family
- deterministic quantity aggregation from verified model state only
- explicit refusal when price data is missing or stale

## 5. Responsibilities
- pricebook schema and snapshot identity
- quantity takeoff contract from ECS/spatial outputs
- deterministic line-item and total-cost computation
- replayable cost artifacts

## 6. Boundaries
- must not decide compliance
- must not guess prices from natural language
- must not own optimization policy
- must not mix cost truth with discipline precedence

## 7. Inputs / Outputs

### Inputs
- verified candidate outputs
- quantity facts
- pricebook snapshots
- explicit unit system and currency metadata

### Outputs
- line-item pricing payload
- total-cost summary
- missing-price or stale-price refusal artifact

## 8. Data Contracts
- `pricebook_snapshot_id`
- `currency_code`
- `quantity_measure`
- `unit_cost`
- `line_item_total`
- `pricing_run_id`
- `pricing_refusal_reason`

## 9. Dependencies
- AEC master plan
- ECS core plan
- spatial kernel plan
- coordination plan
- optimization plan

## 10. Ordered Implementation Steps
1. Freeze the pricebook schema and snapshot identity model.
2. Define quantity extraction contracts from ECS/spatial outputs.
3. Implement deterministic line-item scoring.
4. Emit replayable artifacts with explicit snapshot IDs and unit/currency metadata.
5. Integrate pricing as read-only input to optimization and coordination.

## 11. Edge Cases
- candidate lacks required quantity facts
- pricebook entry exists but uses mismatched units
- mixed currency or missing currency tags
- snapshot staleness relative to the candidate model revision

## 12. Risks
- pricing becomes an ungoverned spreadsheet dump
- quantities are inferred from non-verified geometry
- optimization weights cost without stable pricing provenance
- users confuse this oracle with live market pricing

## 13. Validation Plan

### Existing Tests To Reuse As Pattern
- `python -m pytest scripts/tests/test_geometric_pareto_optimizer.py`
- `python -m pytest scripts/tests/test_graph_event_store.py`

### New Tests Required
- `scripts/tests/test_aec_pricing_schema.py`
- `scripts/tests/test_aec_pricing_quantities.py`
- `scripts/tests/test_aec_pricing_oracle.py`
- `scripts/tests/test_aec_pricing_refusals.py`

### Acceptance Gates
- same verified candidate plus same pricebook snapshot yields the same totals
- missing or mismatched price inputs refuse explicitly
- pricing artifacts carry snapshot and currency identity

## 14. Performance Considerations
- start in Python with vectorized arithmetic where needed
- avoid Rust until quantity/pricing math itself is proven hot
- keep pricebook loading explicit and cacheable

## 15. Execution Checklist
- [ ] pricebook schema frozen
- [ ] quantity extraction contract frozen
- [ ] refusal behavior frozen
- [ ] replay artifact schema frozen
- [ ] new `test_aec_pricing_*` suite added

## 16. Stop Conditions
- price sources are undefined
- currency or units are ambiguous
- pricing tries to evaluate unverified geometry
- implementation starts mixing pricing authority with optimization or compliance decisions
