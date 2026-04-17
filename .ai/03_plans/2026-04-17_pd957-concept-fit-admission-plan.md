---
task: pd957-concept-fit-admission
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
supersedes: null
---

# 2026-04-17 PD-957 Concept-Fit Admission Plan

## Objective
Reduce the tranche shallow-representation risk by admitting a minimal, truthful PD-957 concept/relationship slice.

## Required deliverables
1. three admitted concept paths for `PD-957`
2. three dataset-scoped `governs` relationship files for `PD-957`
3. tranche manifest update
4. fresh tranche source-to-graph dry-run validation

## Candidate concepts
- `003_Canonical-Knowledge-Layer/shared/concepts/floor-area.md`
- `003_Canonical-Knowledge-Layer/shared/concepts/setbacks.md`
- `003_Canonical-Knowledge-Layer/shared/concepts/yards.md`

## Execution order
1. create dataset-scoped promoted relationship files for the three concepts
2. update `config/datasets/laws-tranche-1.yaml` to admit the concepts and relationships for `PD-957`
3. rerun tranche source-to-graph dry-run
4. confirm shallow-representation count falls

## Acceptance criteria
- `PD-957` no longer drives `shallow_representation_count`
- `PD-1216` remains blocked
- tranche execute still remains gated
