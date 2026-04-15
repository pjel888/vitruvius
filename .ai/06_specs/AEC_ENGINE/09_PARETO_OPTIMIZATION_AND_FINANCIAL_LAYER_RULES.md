# Pareto Optimization and Financial Layer Rules

## Purpose
This file defines the mandatory rules for the financial and multi-objective optimization layer in the AEC engine. It exists to keep money, schedule, and Pareto ranking in their proper place: above feasibility, below governance, and outside the Rust physics kernels.

## Scope
This file governs:
- the Python-owned Pricing Oracle
- objective-vector construction for feasible options
- Pareto ranking and tradeoff surfaces
- temporal price binding and jurisdiction-sensitive cost lookup
- replayable optimization artifacts

This file does NOT govern:
- hard-feasibility verification — see `06_FORMAL_VERIFICATION_AND_Z3_PROTOCOL.md`
- vault schema beyond cost-data presence — see `04_KNOWLEDGE_VAULT_AND_RULE_AST_CONTRACT.md`
- repo-wide performance budgets — see `.ai/06_specs/GOVERNANCE/06_PERFORMANCE_BUDGET_AND_BENCHMARK_POLICY.md`
- Rust kernel implementation style — see `.ai/06_specs/RUST/`

## Core Principle
Optimization ranks only what verification has already proved feasible.

## 1. Layer Ownership Rules
- Python MUST own the Pricing Oracle, objective assembly, Pareto frontier construction, and final option ranking.
- Rust MUST NOT read prices, currency labels, ROI targets, or procurement heuristics directly.
- Z3 MUST NOT optimize money, ROI, or schedule directly in place of the optimization layer. It verifies hard constraints only.
- The LLM MUST NOT choose among tradeoffs without a structured ranking result emitted by Python.

## 2. Feasibility Before Ranking
- An option MUST clear the hard-feasibility gate before any financial or Pareto ranking occurs.
- A cheaper option that violates law, clearance, structure, or verified discipline constraints is invalid and MUST be discarded, not ranked.
- Soft objectives MAY break ties among feasible options; they MUST NOT relax the hard-feasibility set silently.
- Optimization retries that try to "buy" a rule violation are forbidden.

## 3. Pricing Oracle Rules
- Pricing data MUST come from the vault or another explicitly governed structured source, never from hard-coded literals in Rust kernels.
- Every price lookup MUST bind:
  - jurisdiction
  - effective date or pricing snapshot date
  - currency
  - unit of measure
- The Pricing Oracle MUST expose a machine-readable explanation of which price records were used for a ranked option.
- A price lookup whose jurisdiction, date, currency, or unit is ambiguous MUST fail closed.

## 4. Objective Vector Rules
- Every optimization task MUST define an explicit objective vector before ranking starts.
- Canonical objectives include:
  - capital cost
  - operating cost
  - embodied carbon
  - maintainability
  - schedule impact
  - usable area / yield
- Objective vectors MUST state direction (`min` or `max`) and units per dimension.
- Hidden weights are forbidden. If weighted aggregation is used after Pareto pruning, the weights MUST be explicit, versioned, and auditable.

## 5. Pareto Frontier Rules
- Pareto ranking MUST preserve the full non-dominated set before any user-facing summary collapses it.
- Any later scalar ranking of Pareto-feasible options MUST be auditable back to the explicit weights or tie-break rules used.
- A frontier artifact MUST identify dominated options and why they were dominated.
- Optimization output MUST distinguish:
  - feasible but dominated
  - feasible and Pareto-optimal
  - infeasible and discarded

## 6. Temporal and Scenario Rules
- Cost ranking MUST bind to the same declared temporal clock used for rule selection unless the task artifact explicitly models a scenario comparison across dates.
- Scenario analysis MAY compare multiple temporal clocks, but each scenario MUST remain internally consistent and separately auditable.
- Forecast or stochastic pricing MAY be modeled only as explicit scenario inputs. It MUST NOT leak into the hard-feasibility layer as if it were fact.

## 7. Performance and Separation Rules
- The financial layer MUST remain orchestration-side. It MUST NOT pollute hot physics kernels with price logic or currency handling.
- Performance work on optimization code MUST follow `.ai/06_specs/GOVERNANCE/06_PERFORMANCE_BUDGET_AND_BENCHMARK_POLICY.md`.
- Compact numeric summaries MAY be passed to Rust only when a compute routine is truly objective-agnostic and the task artifact proves that the kernel remains blind to legal and financial semantics.
- If an optimization workload becomes hot enough to justify Rust, the Rust surface MUST still consume precompiled numeric vectors only. The meaning of "cost", "carbon", or "ROI" remains Python-owned.

## 8. Stop Conditions
The Agent MUST stop and escalate if any of the following occur:
- a proposal ranks infeasible options alongside feasible ones without clear separation
- a proposal lets price or ROI waive a hard rule violation
- a Rust kernel is asked to read prices, currency, jurisdiction, or procurement rules directly
- a proposal uses hidden weights or undocumented tie-break rules
- a proposal cannot trace a ranked option back to the price records and objective vector used
- a performance optimization moves financial semantics into the compute layer
- a scenario mixes temporal clocks without explicit separation

Escalation means stop and re-establish the boundary between feasibility, pricing, and ranking.

## Cross-References
- Companion AEC_ENGINE files:
  - `01_COMPOUND_AI_OPERATING_CONTRACT.md` — Python owns orchestration and pricing; Rust owns no law
  - `04_KNOWLEDGE_VAULT_AND_RULE_AST_CONTRACT.md` — cost data under the `cost:` namespace and temporal metadata
  - `05_MULTI_DISCIPLINARY_COORDINATION_RULES.md` — concession cascades that must replay pricing impacts
  - `06_FORMAL_VERIFICATION_AND_Z3_PROTOCOL.md` — feasibility gate that precedes optimization
  - `08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md` — replayability and temporal-clock requirements
- Related GOVERNANCE / RUST files:
  - `.ai/06_specs/GOVERNANCE/06_PERFORMANCE_BUDGET_AND_BENCHMARK_POLICY.md` — performance evidence required for optimization hot paths
  - `.ai/06_specs/GOVERNANCE/05_TRUTH_GOVERNANCE_AND_PROMOTION_CONTRACT.md` — provenance requirements for truth-bearing optimization outputs
  - `.ai/06_specs/RUST/04_RUST_ARCHITECTURE_AND_BOUNDARY_RULES.md` — Rust compute boundary
  - `.ai/06_specs/RUST/05_RUST_TESTING_BENCHMARKING_AND_VALIDATION.md` — validation if any optimization kernel crosses into Rust

## Final Rule
Money may rank feasible options. It may not purchase a violation.
