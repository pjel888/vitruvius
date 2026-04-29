# Cross-Domain Overlay Enrichment Audit

Date: 2026-04-29  
Run id: 20260429T075023Z  
Status: completed after validation

## Audit purpose

Determine whether the post-targeted AEC-MEPFS backbone could be materially improved by adding practical typed relationships and applicability overlays without crossing protected-content, live graph, or production runtime boundaries.

## Baseline before this slice

- Latest validated graph before this work: `20260429T065436Z`
- Baseline counts: 9076 BackboneNode records, 9326 relationships, 41 source-rights registry rows
- Strength: broad taxonomy and standards-family anchors were already present.
- Weakness: cross-domain coordination, commissioning workflow, operational resilience, and applicability overlay semantics were still sparse compared with practical AEC-MEPFS questions.

## Findings

1. **Relationship depth was the highest-value gap.** Existing breadth needed typed semantic edges for real questions such as what constrains generator placement, what integrated systems testing depends on, and which applicability overlays trigger discipline constraints.
2. **Overlay nodes were justified but should stay bounded.** Missing intermediate nodes were needed for AHJ/local adoption, nonstructural support coordination, commissioning workflow semantics, and operational continuity concepts.
3. **Existing predicates were sufficient.** The valid governed vocabulary supports `broader_than`, `part_of`, `requires`, `constrains`, `maps_to_external_standard`, `governs`, and `applicable_in_jurisdiction`; no new predicate was needed.
4. **Rights risk remains manageable only with metadata-only source usage.** Standards-family titles and public URLs are appropriate; protected clauses/tables/figures are not.
5. **Kimi-only enrichment routing remains required.** Existing Kimi routes in `opencode.json` remain the appropriate model-assisted route; Codex Spark must not be used as enrichment provider.

## Risk assessment

| Risk | Assessment | Mitigation |
|---|---|---|
| Protected source ingestion | High if standards text is copied | Store source-family metadata and steward-written descriptions only |
| Decorative/count-chasing edges | Medium | Require meaningful governed predicates and endpoint-specific semantic value |
| Invalid path codes | Medium | Three-uppercase-character path segment checks and contract validation |
| Duplicate nodes | Medium | Idempotent path-code merge behavior and fixture reruns |
| Runtime drift | Medium | Regenerate shadow staging only; API tests update counts but no route logic |
| Live graph mutation | High | File-backed fixture, registry, reports, and shadow artifacts only |
| Codex Spark routing | Medium | Verify active enrichment routes point to Kimi; safety grep active routing |

## Approved implementation scope

- Add real overlay/source/reference BackboneNode rows where missing.
- Improve existing endpoint nodes with aliases/source-family metadata.
- Add substantial governed relationships across the four requested focus areas.
- Add metadata-only source-rights rows for missing public source families.
- Add deterministic script and regression tests.
- Regenerate shadow staging and update API count expectations.

## Blocked scope

- No live Neo4j mutation or promotion.
- No KG rebuild/reload/reset/destructive operation.
- No protected standard source text, clauses, tables, figures, diagrams, or payloads.
- No fake Kimi integration or placeholder enrichment content.
- No new unsupported predicates.

## Audit conclusion

The slice is justified because the graph becomes materially better at answering cross-discipline coordination, commissioning, continuity, and applicability questions. The scope remains file-backed, metadata-only, and schema-governed.
