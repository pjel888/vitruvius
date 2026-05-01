# PRD — AEC-MEPFS Backbone Readiness Closure

## Goal
Close every locally executable, non-destructive readiness gate required before
the AEC-MEPFS Backbone can enter a bounded integration lane.

## Scope
- Production registry location plan and release boundary.
- Exact fixture contracts for API/Explorer parity and resolver cases.
- Rollback-proof evidence plan and required commands/artifacts.
- Benchmark/report artifact plan.
- Validator/test coverage for the readiness gates above.
- Readiness scorecard that separates closed gates from external blockers.

## Out Of Scope
- Neo4j writes, graph rebuilds, destructive resets, or cleanup.
- KG schema, loader, API, Explorer, or feature-flag runtime wiring.
- Canonical taxonomy/source admission.
- Protected standards/legal text ingestion.
- Legal/licensing decisions that require a human reviewer.

## User Stories
### US-001 Registry Location Readiness
As a future integration implementer, I need exact registry file locations and
promotion boundaries so runtime code does not invent registry paths.

### US-002 Parity Runner Readiness
As an Explorer/API maintainer, I need exact fixture assertions before any v2
shadow route can be wired.

### US-003 Rollback Proof Readiness
As a database operator, I need required backup/export, restore, and smoke-query
evidence before any graph mutation or shadow promotion.

### US-004 Benchmark Readiness
As a verifier, I need exact benchmark commands, reports, thresholds, and
percentile requirements before integration claims are made.

### US-005 Scorecard Closure
As the project steward, I need a truthful scorecard distinguishing closed local
gates from externally blocked gates.
