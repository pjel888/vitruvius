---
task: pd1185-concept-fit-admission
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
supersedes: null
---

# 2026-04-17 PD-1185 Concept-Fit Admission Plan

## Objective
Increase tranche graph richness with the next smallest truthful slice by admitting a minimal `PD-1185` concept/relationship set.

## Required deliverables
1. three admitted concept paths for `PD-1185`
2. three dataset-scoped `governs` relationship files for `PD-1185`
3. tranche manifest update
4. fresh tranche source-to-graph execute validation

## Candidate concepts
- `003_Canonical-Knowledge-Layer/shared/concepts/means-of-egress.md`
- `003_Canonical-Knowledge-Layer/shared/concepts/building-permit.md`
- `003_Canonical-Knowledge-Layer/shared/concepts/yards.md`

## Execution order
1. create dataset-scoped promoted relationship files for the three concepts
2. update `config/datasets/laws-tranche-1.yaml` to admit the concepts and relationships for `PD-1185`
3. rerun `run-laws-tranche-source-to-graph`
4. confirm the graph snapshot gains additional `PD-1185` nodes/edges while remaining inside the current tranche

## Acceptance criteria
- `PD-1185` contributes admitted concepts and relationships to the tranche graph
- no new tranche members are introduced
- tranche execute remains bounded to `PD-957`, `PD-1216`, and `PD-1185`
