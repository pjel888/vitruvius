---
task: laws-tranche-expansion
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 Laws Tranche Expansion Audit

## Audit question
What is the safest truthful execution boundary after the 4-law pilot?

## Verdict
**Tranche expansion is the only safe next execution boundary.**

## Why
- all-laws execute remains gated
- current corpus size is much larger than the admitted pilot
- current broad coverage is highly uneven
- 8GB machine safety still matters even with a smaller model preset

## Evidence
- latest readiness run shows:
  - 47 law folders
  - 183 PDFs
  - only 4 covered by the current bounded pilot
  - 43 still inventory-only
- the new `m2-8gb-safe` preset makes broad readiness planning safer
- it does not make broad execution automatically safe

## Safe now
- all-laws readiness dry-run
- tranche planning
- tranche manifests
- tranche-specific dry-runs
- tranche-specific source admission work

## Unsafe now
- one-shot all-laws execute
- one-shot all-resources execute
- claiming that dry-run readiness equals execute readiness

## Audit recommendation
The next accepted slice should be:
1. tranche manifest support / naming convention
2. tranche-1 source admission plan
3. tranche-1 dry-run and only then tranche-1 execution
