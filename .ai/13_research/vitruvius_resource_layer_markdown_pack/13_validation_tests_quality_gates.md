# 13 — Validation, Tests, and Quality Gates

## Validation principles

The Resource Intelligence Layer needs validation because unverified sources can destroy trust.

Validation should prevent accepted broken links, missing source titles, duplicate resources, accepted local files that do not exist, Rule nodes with no primary source, source links with no rationale, rejected sources appearing in sidebar, unverified resources appearing as trusted, score values outside 0..1, and jurisdictional claims without context.

## Resource checks

Fail if:

- resource ID missing,
- title missing/empty,
- resource type unsupported,
- source authority unsupported,
- access type unsupported,
- verification status unsupported,
- score fields outside 0..1 if present,
- online resource has neither URL nor DOI nor stable identifier,
- local resource has no local path/hash,
- local resource path does not exist when validation runs in full mode,
- accepted resource has `verificationStatus = rejected`,
- accepted resource has `verificationStatus = unverified` unless explicitly allowed in dev mode.

## NodeResourceLink checks

Fail if node ID does not exist, resource ID does not exist, relationship type is unsupported, rationale is empty, relevance/authority/confidence is outside 0..1, an accepted link points to a rejected resource, a rejected link appears in sidebar default output, or a Rule node link lacks a primary/high-authority source.

## Duplicate checks

Detect duplicates by DOI, ISBN13/ISBN10, canonical URL, local file hash, Internet Archive identifier, and normalized title + author + year.

## Jurisdiction checks

Fail or warn when a Rule node has a code/regulatory relationship but no jurisdiction/context, source type is `code` or `standard` but edition/year is missing when available, source claims global scope but the domain is jurisdictional, or relationship type `governs` is used for a general article.

## Copyright/access checks

Warn when a PDF URL appears unofficial for a copyrighted standard/book, source access type is unknown, local file is restricted but UI would expose it publicly, or long excerpts are stored/displayed.

## Sidebar API checks

Test that sidebar renders with zero resources, one accepted resource, and many resources; excludes rejected resources by default; sorts by display score; handles missing optional fields; shows badges; and supports filters.

## Unit tests

Recommended tests:

1. `normalizeDoi()` handles DOI URL and uppercase.
2. `normalizeIsbn()` strips hyphens and validates length.
3. `canonicalizeUrl()` removes tracking parameters.
4. `dedupeResources()` merges DOI duplicates.
5. `scoreResourceCandidate()` returns 0..1.
6. `validateResource()` rejects missing title.
7. `validateNodeResourceLink()` rejects missing rationale.
8. `getNodeResources(nodeId)` excludes rejected resources.
9. `getNodeResources(nodeId)` sorts by display score.
10. `ruleNodeRequiresPrimarySource()` flags missing source.

## Integration tests

Recommended:

1. Create fake Concept node with 3 resources and render sidebar.
2. Create fake Rule node without primary source and verify validation failure.
3. Create local PDF resource with missing file and verify validation failure/full-mode warning.
4. Create duplicate DOI resources and verify dedupe warning/failure.
5. Create resource candidate, reject it, verify it is hidden.
6. Create accepted resource and link, verify resource card fields.

## E2E tests

If Playwright or equivalent exists:

1. Open graph page.
2. Click Concept node.
3. Sidebar opens.
4. Resource cards display.
5. Filters work.
6. Empty state displays for resource-less node.
7. Candidate resources not shown by default.
8. Open URL button exists for online source.
9. Local source badge appears for local source.

## Quality gates

Infrastructure: Resource model, NodeResourceLink model, SourceFamily registry, candidate/accepted/rejected distinction, and validation script exist.

Sidebar: sidebar renders resources for eligible node types, handles zero/one/many resources, hides rejected candidates by default, and shows type/authority/verification/access/rationale.

Verification: accepted resources have metadata, external resources are checked or identifier-verified, local resources are file-verified, duplicate detection works, and Rule node source constraints work.

Coverage: first milestone top 25 high-centrality eligible nodes have at least 3 accepted resources; next milestone top 100 Architecture/Civil/Structural Concept nodes have at least 3 accepted resources.

Kimi review: Kimi reviewed at least one candidate batch, decisions are logged, and Kimi-rejected candidates are not accepted.

## Quality score rubric

| Dimension | Points |
|---|---:|
| Data model completeness | 15 |
| Verification/deduplication | 20 |
| Sidebar UX | 15 |
| Source authority/ranking | 15 |
| Local corpus support | 10 |
| API/source discovery support | 10 |
| Validation/test coverage | 10 |
| Kimi/human review workflow | 5 |

Minimum completion threshold: total >= 85 for the first production-ready milestone, no critical validation failures, no accepted broken links, and no trusted Rule node without source/context.

## Metrics to report

Report total resources, total node-resource links, accepted/candidate/rejected links, resources by type/authority/verification, local resources indexed, high-priority nodes covered, average accepted resources per eligible node, duplicates found/merged, broken links found, Kimi-reviewed candidates, and human-reviewed candidates.
