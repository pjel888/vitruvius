---
task: laws-m4-expansion-path
phase: 05
created: 2026-04-16
author: PLANNER
status: COMPLETE
---

# 2026-04-16 Laws M4 Expansion Path Plan

## Goal
Make post-pilot scaling safe, repeatable, and provenance-correct.

## M4 deliverables
1. per-law repetition model
2. per-section graph model
3. merged-graph collision/provenance rules

## Decision
Implement M4 in two layers:
- **M4A** — formalize the model/spec layer
- **M4B** — add only the smallest additive runtime/schema support justified by M4A

## Scope of this first M4 step
### In scope
- explicit M4 research/audit/spec/plan artifacts
- any minimal manifest/schema/runtime support that is directly required by those artifacts

### Out of scope for now
- broad all-laws batch expansion
- canonical section-node ontology
- full merged-graph orchestration command family

## Recommended first runtime support
If code support is added in the first M4 step, keep it minimal:
- optional manifest `law_units` support for repeatable law entries
- optional reporting surfaces that summarize those law units
- nothing that changes current bounded-pilot behavior when unused

## Validation rule
Do not call M4 complete until:
- the model/spec artifacts exist
- any added runtime support is additive and tested
- current bounded pilot success remains intact

## Completion note
Completed on 2026-04-16 with:
- M4A research/audit/spec/plan artifacts in place
- M4B additive manifest `law_units` support and reporting surfaces implemented
- no new section-scoped or merged-graph runtime introduced
- bounded pilot success preserved
