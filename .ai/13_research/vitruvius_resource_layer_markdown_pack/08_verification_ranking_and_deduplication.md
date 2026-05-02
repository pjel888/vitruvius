# 08 — Verification, Ranking, and Deduplication

## Core rule

Discovery is not verification. A source found by Google Books, Open Library, Crossref, Semantic Scholar, OpenAlex, CORE, Unpaywall, Internet Archive, or web search is only a **candidate** until it passes verification and review.

## Verification layers

1. **Existence:** URL status, DOI resolution, API title metadata, local file exists, local file hash.
2. **Metadata consistency:** title, authors, publisher, year, DOI, ISBN, source domain, and local metadata.
3. **Source authority:** official/professional/government sources rank above general web sources when relevance is similar.
4. **Relevance:** title/heading match, alias match, taxonomy context, semantic similarity, source discipline, extracted passages, page/chapter specificity.
5. **Jurisdiction/context:** identify country/region, standard body, edition/year, binding vs advisory status.
6. **Kimi review:** use for source-node relevance and overclaim detection.
7. **Human review:** use for regulatory, safety, legal, and high-impact claims.

## Authority scoring

```text
1.00 official standard/code/professional body/government source
0.90 recognized textbook/handbook/publisher
0.85 peer-reviewed journal/conference paper
0.75 university/open course material
0.65 manufacturer guide for product-specific topics
0.50 reputable trade article
0.30 general blog/SEO page
0.10 unknown source
```

## Relevance scoring

```text
relevanceScore =
  0.25 * title_or_heading_match
+ 0.20 * node_alias_match
+ 0.20 * semantic_similarity
+ 0.15 * taxonomy_context_match
+ 0.10 * source_discipline_match
+ 0.10 * page_or_section_specificity
```

## Deduplication keys

Deduplicate in this order:

1. DOI.
2. ISBN13 / ISBN10 normalized.
3. Canonical URL.
4. Local file hash.
5. Internet Archive identifier.
6. Normalized title + author + year.
7. Normalized title + organization + edition.

## URL canonicalization

Normalize scheme, host casing, trailing slash, redirects if safe, and remove tracking parameters such as `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`, `fbclid`, and `gclid`.

## Display ranking

```text
displayScore =
  0.35 * relevanceScore
+ 0.25 * authorityScore
+ 0.20 * verificationScore
+ 0.10 * specificityScore
+ 0.05 * localOrStableIdentifierBonus
+ 0.05 * diversityBonus
```

Verification score mapping:

```text
human_reviewed: 1.00
content_verified: 0.90
local_file_verified: 0.85
identifier_verified: 0.80
link_verified: 0.70
metadata_verified: 0.60
unverified: 0.20
rejected: 0.00
```

## Acceptance thresholds

Concept node:

```text
relevanceScore >= 0.60
authorityScore >= 0.50
confidenceScore >= 0.60
reviewStatus = accepted or human_reviewed
```

Rule node:

```text
relevanceScore >= 0.70
authorityScore >= 0.75
confidenceScore >= 0.75
jurisdiction/context present if code-like
relationship = governs or is_primary_reference_for
```

Procedure node:

```text
relevanceScore >= 0.65
source must actually describe workflow/procedure/steps/method
relationship = provides_procedure or provides_analysis_method
```

Evidence node:

```text
relevanceScore >= 0.70
resourceType in academic_paper | technical_report | dataset | professional_guidance | local_document
relationship = provides_evidence
stable identifier preferred
```

Document node:

```text
title present
resource metadata complete enough for identification
one stable identifier or local hash or canonical URL
```

## Rejection reasons

Use structured reasons: `broken_url`, `missing_title`, `duplicate_resource`, `low_relevance`, `too_general`, `low_authority`, `jurisdiction_unclear`, `copyright_risk`, `pirated_copy_risk`, `metadata_mismatch`, `not_accessible`, `not_a_source`, `product_specific_for_generic_node`, `unsupported_claim`, `overclaimed_relationship`, `kimi_rejected`, `human_rejected`.

## Preventing sidebar degradation

Validation should fail if accepted resources lack titles, accepted online resources lack URL/DOI/identifier/local file, accepted local paths do not exist, accepted sources are unverified, Rule links lack jurisdiction/context when code-like, resources duplicate DOI/ISBN/canonical URL/hash, rationales are empty, scores are outside 0..1, or rejected resources appear in the sidebar by default.
