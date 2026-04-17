---
task: laws-tranche-1-source-preparation
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 Laws Tranche-1 Source Preparation Research

## Question
What must happen before tranche-1 can move from readiness dry-run into source-to-graph dry-run and later execution?

## Fresh evidence
From the latest tranche dry-run report:
- `run-laws-tranche-dry-run --tranche-manifest config/datasets/laws-tranche-1.yaml --review-preset m2-8gb-safe`
- tranche candidates:
  - `PD-957`
  - `PD-1216`
  - `PD-1185`
- current inventory for all three:
  - refined markdown count = **0**
  - raw markdown count = **0**
  - sidecar JSON count = **0**

## Meaning
Tranche-1 is not blocked by graph logic first.
It is blocked by **upstream produced-data readiness**.

That means the next truthful move is:
1. source inventory confirmation
2. conversion/refinement planning
3. source admission planning
4. only then tranche source→graph dry-run

## Required stages before tranche execute
1. raw source confirmation per candidate law
2. conversion output generation
3. refinement output generation
4. canonical source planning/admission
5. concept-fit / relationship-fit review
6. tranche source→graph dry-run
7. tranche execute only after dry-run evidence is acceptable

## Non-goal
- do not pretend tranche-1 is ready for source→graph just because the tranche dry-run command exists
