---
task: raw-duplicate-sanitization
phase: 01
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 Raw Duplicate & Sanitization Audit

## Audit question
Is the current system sufficiently protected against raw-PDF duplication and sanitization issues for broader laws expansion?

## Verdict
**Partially, but not enough.**

## Existing protections
- SHA-256 hashing exists
- duplicate detection is recognized in config/feature flags
- linter/governance care about duplicate structural states

## Missing protections
- no explicit raw duplicate readiness report for operators
- no tranche/admission gate that blocks or flags duplicate raw evidence clusters
- no clear policy surface for exact duplicates under different filenames

## Audit recommendation
Introduce a dedicated raw duplicate / sanitization readiness slice with:
1. exact duplicate grouping by hash
2. operator-readable report
3. tranche/admission guardrails
4. no raw-file mutation by default
