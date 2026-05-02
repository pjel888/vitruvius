# 22 — Appendix: Sample Queries and Pseudocode

## Sample resource query SQL

```sql
SELECT
  nrl.id AS link_id,
  r.id AS resource_id,
  r.title,
  r.resource_type,
  r.source_authority,
  r.access_type,
  r.verification_status,
  r.url,
  r.local_path,
  nrl.relationship,
  nrl.relevance_score,
  nrl.authority_score,
  nrl.confidence_score,
  nrl.rationale,
  nrl.page_refs,
  (
    0.35 * nrl.relevance_score +
    0.25 * nrl.authority_score +
    0.20 * CASE r.verification_status
      WHEN 'human_reviewed' THEN 1.0
      WHEN 'content_verified' THEN 0.9
      WHEN 'local_file_verified' THEN 0.85
      WHEN 'identifier_verified' THEN 0.8
      WHEN 'link_verified' THEN 0.7
      WHEN 'metadata_verified' THEN 0.6
      ELSE 0.2
    END +
    0.10 * nrl.confidence_score
  ) AS display_score
FROM node_resource_links nrl
JOIN resources r ON r.id = nrl.resource_id
WHERE nrl.node_id = :node_id
  AND nrl.review_status IN ('accepted', 'human_reviewed')
  AND r.verification_status != 'rejected'
ORDER BY display_score DESC
LIMIT 10;
```

## URL canonicalization pseudocode

```ts
function canonicalizeUrl(input: string): string {
  const url = new URL(input.trim());
  url.protocol = "https:";
  url.hostname = url.hostname.toLowerCase().replace(/^www\./, "");

  const trackingParams = [
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "fbclid", "gclid"
  ];

  for (const p of trackingParams) url.searchParams.delete(p);

  if (url.pathname.endsWith("/") && url.pathname.length > 1) {
    url.pathname = url.pathname.slice(0, -1);
  }

  url.hash = "";
  return url.toString();
}
```

## DOI normalization pseudocode

```ts
function normalizeDoi(input: string): string {
  return input
    .trim()
    .toLowerCase()
    .replace(/^https?:\/\/(dx\.)?doi\.org\//, "")
    .replace(/^doi:/, "")
    .trim();
}
```

## Display score pseudocode

```ts
function verificationScore(status: VerificationStatus): number {
  switch (status) {
    case "human_reviewed": return 1.0;
    case "content_verified": return 0.9;
    case "local_file_verified": return 0.85;
    case "identifier_verified": return 0.8;
    case "link_verified": return 0.7;
    case "metadata_verified": return 0.6;
    case "unverified": return 0.2;
    case "rejected": return 0.0;
  }
}

function displayScore(link: NodeResourceLink, resource: Resource): number {
  const stableIdBonus = resource.doi || resource.isbn13 || resource.localFileHash ? 1 : 0;
  const specificity = link.pageRefs?.length || link.sectionRefs?.length ? 1 : 0.5;

  return (
    0.35 * link.relevanceScore +
    0.25 * link.authorityScore +
    0.20 * verificationScore(resource.verificationStatus) +
    0.10 * specificity +
    0.05 * stableIdBonus +
    0.05 * link.confidenceScore
  );
}
```

## Candidate acceptance pseudocode

```ts
function canAcceptCandidate(candidate, node, resource, link): boolean {
  if (!resource.title?.trim()) return false;
  if (resource.verificationStatus === "rejected") return false;
  if (link.relevanceScore < 0.6) return false;
  if (link.authorityScore < 0.5) return false;
  if (!link.rationale?.trim()) return false;

  if (node.type === "Rule") {
    if (link.authorityScore < 0.75) return false;
    if (isCodeLike(resource) && !resource.jurisdiction) return false;
    if (!["governs", "is_primary_reference_for"].includes(link.relationship)) return false;
  }

  if (resource.localPath && !resource.localFileHash) return false;
  if (!resource.localPath && !resource.url && !resource.doi && !resource.isbn13) return false;

  return true;
}
```

## Backfill batch pseudocode

```ts
async function backfillBatch(nodes: GraphNode[]) {
  for (const node of nodes) {
    const queries = buildQueries(node);

    const candidates = [
      ...await searchLocalCorpus(node),
      ...await searchCuratedSources(node, queries),
      ...await searchBookApis(node, queries),
      ...await searchAcademicApis(node, queries),
      ...await searchDigitalLibraries(node, queries),
    ];

    const normalized = normalizeCandidates(candidates);
    const deduped = dedupeCandidates(normalized);
    const scored = scoreCandidates(node, deduped);
    const verified = await verifyCandidates(scored);
    const reviewSet = selectForKimiReview(verified);
    const kimiDecisions = await reviewWithKimi(node, reviewSet);
    const finalDecisions = applyKimiAndRules(verified, kimiDecisions);

    await persistAcceptedResources(node, finalDecisions.accepted);
    await persistRejectedCandidates(node, finalDecisions.rejected);
    await persistNeedsReview(node, finalDecisions.needsReview);
  }

  await runValidation();
  await updateMetrics();
}
```

## Example search query builder

```ts
function buildQueries(node: GraphNode): string[] {
  const terms = [node.name, ...(node.aliases ?? [])].filter(Boolean);
  const taxonomy = node.taxonomyPath?.join(" ") ?? "";
  const discipline = node.disciplineTags?.join(" ") ?? "";

  return [
    `"${node.name}" ${discipline} definition`,
    `"${node.name}" ${discipline} design guidance`,
    `"${node.name}" ${taxonomy} textbook`,
    ...terms.slice(1).map(alias => `"${alias}" ${discipline} guidance`),
  ];
}
```

## Example source-gap log entry

```md
## Source gap — Node: Temporary Shoring

Attempted:
- local corpus search
- ASCE/FHWA curated search
- Open Library / Google Books
- Crossref / OpenAlex

Result:
Several broad construction references found, but no accepted source with enough direct relevance and authority.

Decision:
Leave node without accepted sidebar source for now. Add to human/local-source review queue.
```
