---
task: raw-duplicate-sanitization
phase: 01
created: 2026-04-17
author: CODEX
status: DRAFT
supersedes: null
---

# 2026-04-17 Raw Duplicate & Sanitization Plan

## Objective
Add a safe, additive raw duplicate / sanitization layer that helps broader tranche expansion avoid duplicated raw evidence without mutating the raw layer.

## Desired capabilities
1. exact raw duplicate grouping by SHA-256
2. operator-readable report of duplicate clusters
3. tranche/admission-facing duplicate warnings
4. optional future alias/quarantine policy, but not in the first slice

## Scope
In scope:
- duplicate readiness reporting
- exact duplicate grouping
- operator/report surfaces
- tranche/admission guardrail integration later

Out of scope:
- deleting raw files
- auto-merging raw folders
- fuzzy PDF semantic duplicate detection in the first slice

## Recommended order
1. add duplicate-readiness research/audit/log artifacts
2. implement exact duplicate report surface
3. expose duplicate clusters in laws readiness/tranche readiness reports
4. only later consider aliasing/quarantine workflow

## Rust candidacy note
Raw duplicate and sanitization work should stay Python-first for now.

Why:
- current need is operator/reporting/governance clarity
- exact duplicate grouping can reuse existing SHA-256/file-registry data
- this is not yet a demonstrated compute bottleneck

If future corpus-scale profiling shows duplicate clustering becomes a true hot path, a narrow Rust kernel may be justified later. Until then, do not force this lane into Rust.

## Acceptance criteria
- duplicate clusters can be reported before tranche widening
- no raw mutation is required
- broader laws expansion can explicitly account for duplicate raw evidence
