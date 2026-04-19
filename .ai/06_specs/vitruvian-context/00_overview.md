# Vitruvian Context — Overview

> **Type:** Core architectural specification
> **Schema version:** `1.0.0`
> **Date:** 2026-04-19

---

## What is the Vitruvian Context?

> **The Vitruvian Context = the engine that resolves canonical knowledge into context-specific truth.**

It is the runtime layer that sits on top of the taxonomy governance substrate and transforms a query + context into a resolved output that answers:

- **What** applies?
- **Why** it applies?
- **Where** it applies?
- **When** it applies?

The engine never mutates truth. It selects, composes, and ranks.

---

## Documents in this pack

| # | Document | Purpose |
|---|----------|---------|
| 00 | `00_overview.md` | This file — high-level framing and document map |
| 01 | `01_cross_discipline_relationship_taxonomy.md` | Typed predicates for cross-discipline connections, domain pair constraints, validation rules |
| 02 | `02_resolver_engine_spec.md` | `resolve()` contract, precedence rules, algorithm, Cypher, test cases, error codes |
| 03 | `03_integration_plan.md` | How the Vitruvian Context integrates with the taxonomy governance build (Phases 0–11) |

---

## Boundary: Taxonomy Governance vs Vitruvian Context

| Aspect | Taxonomy Governance | Vitruvian Context |
|--------|--------------------:|-------------------|
| **Question** | What exists? How is it classified? | What applies here, now, and why? |
| **Scope** | Data model, migration, governance | Runtime resolution and composition |
| **Layer** | Substrate (backbone, facets, overlays) | Resolver (selection, precedence, reasoning) |
| **Mutates graph?** | Yes (migration, ingestion) | **No** — read-only |
| **Plan home** | `.ai/03_plans/taxonomy-governance/` | `.ai/06_specs/vitruvian-context/` |
| **Code home** | `scripts/vitruvius/taxonomy/`, `scripts/vitruvius/kg/` | `scripts/vitruvius/resolver/` |

---

## Core principle

> The Vitruvian Context never changes truth — it selects and composes it.

- **Backbone** = truth
- **Overlays** = variations
- **Vitruvian Context** = resolver

If the resolver mutates nodes, rewrites definitions, or hallucinates rules, the system breaks.

---

## Quick links

- Locked decisions: `.ai/03_plans/taxonomy-governance/00_locked_decisions.md`
- Implementation plan: `.ai/03_plans/taxonomy-governance/03_implementation_plan.md`
- Resolver stub: `scripts/vitruvius/resolver.py`
- Resolver tests: `scripts/tests/test_vitruvian_context_resolver.py`
- Cross-discipline validator: `scripts/vitruvius/cross_discipline_validator.py`
- Validator tests: `scripts/tests/test_cross_discipline_validator.py`
