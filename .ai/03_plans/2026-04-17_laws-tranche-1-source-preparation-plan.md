---
task: laws-tranche-1-source-preparation
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
supersedes: null
---

# 2026-04-17 Laws Tranche-1 Source Preparation Plan

## Objective
Prepare tranche-1 candidate laws for later source→graph dry-run and execution by establishing produced-data readiness first.

## Candidate tranche
- `PD-957`
- `PD-1216`
- `PD-1185`

## Current blocker
No produced-data inventory yet for these candidate laws.

## Required deliverables
1. produced-data readiness inventory for tranche-1 candidates
2. conversion/refinement execution plan for tranche-1 candidates
3. source admission criteria for tranche-1 candidates
4. explicit tranche-1 dry-run go/no-go gate

## Execution order
1. inspect raw source file counts and formats
2. run conversion/refinement for tranche-1 candidates only
3. inspect source-quality output
4. create tranche-1 source admission plan
5. then rerun `run-laws-tranche-dry-run`

## Acceptance criteria
- each tranche-1 candidate has produced-data inventory
- tranche-1 can be re-evaluated with real refined inputs
- no generic all-laws widening is implied
