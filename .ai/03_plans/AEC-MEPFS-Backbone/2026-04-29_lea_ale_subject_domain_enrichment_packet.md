---
task: lea-ale-knowledge-graph-enrichment
phase: 05
created: 2026-04-29
author: PLANNER
supersedes: null
status: DRAFT
---

# Plan — LEA/ALE Subject-Domain Knowledge Graph Enrichment

## Objective
Improve the AEC-MEPFS file-backed backbone so it can answer practical Philippine architecture licensure questions across real subjects/domains, legal/code domains, practice domains, and architectural knowledge topics.

## Strategy
1. Inspect current graph, source-rights registry, predicate registry, enrichment scripts, tests, generated reports, opencode Kimi routing, and raw-source filename inventory.
2. Use official/public metadata and Kimi advisory synthesis to build a source-safe LEA/ALE subject-domain map.
3. Add a deterministic enrichment script that adds missing real nodes, improves weak existing nodes, appends metadata-only source refs, and adds governed relationships without new predicates.
4. Regenerate the file-backed fixture and shadow artifacts.
5. Add focused tests and update affected contract/API expectations.
6. Run validation, safety greps, Kimi final review, and state/doc reconciliation.

## Relationship predicate mapping
- `governed_by`, `regulates`, `applies_to` → source node uses `governs` or `constrains` toward topic.
- `exemplifies`, `influences`, `used_in` → use `has_facet`, `part_of`, `requires`, or `constrains` depending on direction and semantic fit.
- Avoid `related_to` and other vague predicates unless already governed; current plan uses stricter governed predicates.

## Plan Critique
[C001] Count targets must not override semantic quality. Relationships must be category-reported and spot-checkable.
[C002] Raw-source inspection can become unsafe if body text is extracted from protected reviewers or standards. Limit to filenames/metadata unless official public law text is clearly safe and still summarize originally.
[C003] Broad taxonomy and existing architecture enrichment may reprocess new level-3 semantic nodes. Exclude new semantic node kinds from broad auto-enrichment if needed.
[C004] Generated report and API count expectations must be updated only after actual fixture generation.

## Execution Checklist
- [ ] [G001] Verify Kimi routing and no active Codex Spark enrichment routing.
- [ ] [G002] Inventory raw PDFs/XLSX and classify source rights.
- [ ] [G003] Run Kimi advisory taxonomy/source-family review.
- [ ] [G004] Run GitNexus impact for modified enrichment symbols.
- [ ] [G005] Implement source-safe LEA/ALE enrichment script and update source-rights rows.
- [ ] [G006] Generate fixture/report artifacts and tests.
- [ ] [G007] Run validations and safety greps; fix failures.
- [ ] [G008] Run Kimi final review and write validation log/state updates.
