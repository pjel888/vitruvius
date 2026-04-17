---
task: raw-duplicate-sanitization
phase: 01
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 Raw Duplicate & Sanitization Research

## Question
Do we need a dedicated raw-data sanitization / duplicate-handling layer before broader laws expansion?

## Short answer
**Yes.**

## Fresh repo-local evidence

### What already exists
- raw-file SHA-256 hashing is already part of the ingestion foundation
  - reflected in roadmap/milestone history for `FileEntry.sha256`
- the project already recognizes duplicate detection as a real concern:
  - `config/vitruvius.yaml` includes `o_duplicate_detector: false`
- the linter/governance docs already treat duplicate names and structural integrity as important

### What does not yet exist as a complete guardrail
- no active raw-layer duplicate quarantine / aliasing lane is currently wired into the operator surface
- no manifest-visible policy for:
  - exact duplicate PDFs under different filenames
  - same-document alternate copies across folders
  - benign duplicates vs authoritative/reference duplicates
- no explicit operator report that says:
  - these raw files are byte-identical duplicates
  - these should be grouped/aliased/quarantined before tranche admission

## Why this matters now
The broader the corpus gets, the more likely we are to encounter:
- exact duplicate PDFs with different names
- law text + mirrored copy + agency repost + operator download variants
- adjacent reference copies that should not all become parallel truth-bearing inputs

This is especially important before tranche expansion because duplicate raw inputs can distort:
- conversion effort
- source-admission decisions
- perceived coverage
- later graph/source lineage

## Conclusion
We should add a **raw duplicate / sanitization guardrail layer** as another additive readiness lane.

It should sit before broad tranche admission and should not mutate raw files directly.
