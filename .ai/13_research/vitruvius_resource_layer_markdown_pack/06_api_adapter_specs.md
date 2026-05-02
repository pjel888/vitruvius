# 06 — API Adapter Specifications

Accessed/planning date: 2026-05-01

This document summarizes source-discovery adapters. Use official documentation before implementation because APIs and rate limits may change.

## General adapter contract

```ts
type SourceSearchInput = {
  nodeId: string;
  canonicalName: string;
  aliases?: string[];
  taxonomyPath?: string[];
  description?: string;
  disciplineTags?: string[];
  resourceTypes?: string[];
  maxResults?: number;
};

type SourceCandidate = {
  adapter: string;
  title: string;
  authors?: string[];
  organization?: string;
  year?: number;
  url?: string;
  canonicalUrl?: string;
  doi?: string;
  isbn10?: string;
  isbn13?: string;
  sourceAuthority?: string;
  resourceType: string;
  rawMetadata?: unknown;
  preliminaryScore: number;
  rationaleHint?: string;
};
```

Each adapter must rate-limit requests, cache responses, record query used, normalize identifiers, and produce candidates only.

## Google Books adapter

Official docs:

- https://developers.google.com/books/docs/v1/reference/volumes/list
- https://developers.google.com/books/docs/v1/reference/volumes

Planning notes:

- Use `volumes.list` for book discovery.
- Endpoint pattern: `GET https://www.googleapis.com/books/v1/volumes?q={search terms}`.
- Query parameters include filters such as `download`, `filter`, `langRestrict`, and `maxResults`.
- Use for title, authors, publisher, publication date, description, industry identifiers, preview/view links.
- Do not treat a Google Books result as authoritative validation by itself.

## Open Library adapter

Official docs:

- https://openlibrary.org/dev/docs/api/search
- https://openlibrary.org/developers/api

Planning notes:

- Open Library Search API returns Work-level and Edition-level information.
- Useful fields may include title, author information, first publish year, editions, identifiers, and subjects.
- Use for metadata discovery and ISBN cross-checking.

## Crossref adapter

Official docs:

- https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- https://api.crossref.org/swagger-ui/index.html

Planning notes:

- Crossref REST API exposes scholarly metadata deposited by members and trusted sources.
- It supports searching, filtering, faceting, sampling, and JSON responses.
- Use for DOI metadata and bibliographic verification.
- Crossref is mainly metadata, not full-text source discovery.

## Semantic Scholar adapter

Official docs:

- https://api.semanticscholar.org/api-docs/
- https://www.semanticscholar.org/product/api

Planning notes:

- Semantic Scholar Academic Graph API supports paper and author data.
- Useful for citations, related papers, venues, abstracts where available, and paper identifiers.
- Good for Evidence nodes and academic source discovery.
- Respect API key/rate-limit requirements.

## OpenAlex adapter

Official docs:

- https://developers.openalex.org/api-reference/introduction
- https://developers.openalex.org/api-reference/works

Planning notes:

- OpenAlex API provides a catalog of scholarly works, authors, sources, institutions, topics, and more.
- Base URL documented as `https://api.openalex.org`.
- Works are scholarly documents such as journal articles, books, datasets, and theses.
- Use for broad academic discovery and metadata cross-checking.

## CORE adapter

Official docs:

- https://core.ac.uk/documentation/api
- https://api.core.ac.uk/docs/v3

Planning notes:

- CORE indexes metadata and full-text content, typically PDFs, from open-access journals and repositories.
- Use for open-access full text/PDF discovery where licensing permits.
- Store access and license notes.
- Avoid scraping or storing too much copyrighted text.

## DataCite adapter

Official docs:

- https://support.datacite.org/docs/api

Planning notes:

- DataCite REST API supports retrieval, creation, and update of DataCite DOI metadata records and account information.
- It is generally RESTful and returns JSON using JSON:API format.
- Use to verify DOI metadata for datasets, technical reports, and research outputs not covered by Crossref.

## Unpaywall adapter

Official docs:

- https://unpaywall.org/products/api
- https://unpaywall.org/data-format

Planning notes:

- Unpaywall REST API provides programmatic access to open-access availability data.
- Use after DOI discovery to check whether an article has an open-access copy or PDF location.
- Store OA status and license/access notes.
- Do not assume every DOI is covered.

Suggested workflow:

```text
Crossref/SemanticScholar/OpenAlex finds DOI
  → Unpaywall checks OA availability
  → if OA location exists, resource candidate gets pdf/landing URL and accessType = open_access
```

## Internet Archive adapter

Official docs:

- https://archive.org/developers/index-apis.html
- https://archive.org/developers/metadata.html
- https://archive.org/developers/md-read.html
- https://archive.org/help/aboutsearch.htm

Planning notes:

- Item metadata can be fetched with `GET https://archive.org/metadata/{identifier}`.
- Archive search endpoints can search metadata stored for items.
- Use for public-domain/historical books, older manuals, and metadata discovery.
- Be cautious about copyright/access; do not assume legal reusability of every item.

## buildingSMART / IFC / IDS adapter or curated fetcher

Official docs:

- https://technical.buildingsmart.org/standards/ifc/
- https://ifc43-docs.standards.buildingsmart.org/
- https://www.buildingsmart.org/standards/bsi-standards/information-delivery-specification-ids/
- https://technical.buildingsmart.org/projects/information-delivery-specification-ids/

Planning notes:

- IFC documentation is useful for AEC object semantics, relationships, spatial structure, and infrastructure/civil concepts.
- IDS is useful for information requirement and validation concepts.
- Use as a curated source family rather than generic web search.

## Classification adapters / curated fetchers

Uniclass official docs:

- https://www.thenbs.com/our-tools/uniclass
- https://uniclass.thenbs.com/

OmniClass official docs:

- https://www.csiresources.org/standards/omniclass/standards-omniclass-about
- https://www.wbdg.org/resources/omniclass

Use for classification mappings, taxonomy support, and construction information organization.

## Professional AEC sources

Use curated domain/source-family searches for ASCE, ACI, AISC, WBDG/NIBS, RIBA, IStructE, ICE, AIA, FHWA, FEMA, USGS, NIST, EPA, and local authorities where relevant.

## Adapter output discipline

Never let an adapter output go straight to sidebar as accepted. All output must pass normalization, dedupe, scoring, verification, optional Kimi review, and final accept/reject decision.
