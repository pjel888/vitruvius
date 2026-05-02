# 05 — Source Discovery Research Plan

## Strategy overview

Use a federated source discovery strategy. No single API is enough.

The discovery stack should include:

1. Local corpus.
2. Curated AEC authority registry.
3. Book metadata APIs.
4. Academic metadata APIs.
5. Open-access / PDF discovery APIs.
6. Public digital library APIs.
7. Controlled web search or domain-specific search.
8. Kimi review.
9. Human review for high-risk sources.

## Why local corpus first

If Vitruvius has local books, PDFs, standards, manuals, lecture notes, project docs, or internal references, index them first.

Local sources can offer stable access, file hashes, page references, local search, better citation reliability, less link rot, project-specific knowledge, and sidebar value even without internet.

## Source discovery channels

### Local corpus

Target folders, adapting to repo conventions:

```text
/library
/resources
/resources/local
/docs
/publications
/pdfs
/books
/standards
/manuals
```

Extract title, author/organization, year, file type, path, hash, text chunks, page numbers, table of contents, keywords, and candidate node matches.

### Curated source families

Build a registry of trusted organizations/domains:

- buildingSMART,
- WBDG/NIBS,
- ISO/BSI guidance pages,
- NBS/Uniclass,
- CSI/OmniClass,
- ASCE,
- ACI,
- AISC,
- IStructE,
- ICE,
- RIBA,
- AIA,
- FHWA,
- FEMA,
- USGS,
- NIST,
- EPA,
- local jurisdictional authorities where applicable.

### Book metadata

Use APIs for discovery and metadata, not final truth.

- Google Books: useful for title, author, publisher, publication date, preview links.
- Open Library: useful for Work/Edition metadata, identifiers, subjects, first publication year.

### Academic metadata

Use for evidence and research-backed concepts:

- Crossref,
- Semantic Scholar,
- OpenAlex,
- DataCite,
- CORE,
- Unpaywall.

### Public digital libraries

Use Internet Archive metadata/search carefully. Treat public digital libraries as discovery/access aids; do not assume every available file is legally or professionally appropriate to cite.

## Query patterns by node type

Concept:

```text
{canonical_name} {discipline} design guidance
{canonical_name} {taxonomy_path} definition
{alias} {discipline} handbook
{canonical_name} site:trusted-domain.org
```

Rule:

```text
{rule_subject} standard guidance jurisdiction
{rule_subject} code requirement {jurisdiction}
{rule_subject} professional guidance
```

Procedure:

```text
{procedure_name} procedure guide
{procedure_name} construction process
{procedure_name} inspection testing method
{procedure_name} design workflow
```

Evidence:

```text
{claim_subject} evidence study DOI
{claim_subject} academic paper
{claim_subject} performance study
{claim_subject} technical report
```

Document:

```text
{title} {author} ISBN DOI
{title} official pdf
{title} publisher
{title} archive metadata
```

## Search priority for AEC nodes

For Architecture / Civil / Structural concepts, prefer:

1. local corpus matches,
2. official/professional sources,
3. recognized textbook/handbook metadata,
4. academic or technical reports,
5. classification/ontology docs,
6. lower-tier web sources only if needed.

## Research coverage by discipline

### Architecture

Good source families: WBDG, RIBA, AIA, NIBS, accessibility authorities, building envelope guidance, daylight/acoustic/space planning references, and local architecture books/PDFs.

High-value nodes: space, room, circulation, egress route, accessible route, facade, thermal envelope, fire-rated wall, shaft, stair, door, window, daylighting, acoustic separation.

### Civil Engineering

Good source families: ASCE, FHWA, USGS, FEMA, EPA, local public works agencies, geotechnical textbooks, stormwater manuals, and site design guides.

High-value nodes: site grading, surface runoff, stormwater drainage, catch basin, detention basin, soil bearing capacity, groundwater, retaining wall, pavement, access road, utility corridor.

### Structural Engineering

Good source families: ASCE, ACI, AISC, IStructE, Eurocode bodies where relevant, structural textbooks, steel/concrete/timber handbooks, and local standards manuals.

High-value nodes: load path, dead load, live load, wind load, seismic load, foundation, footing, pile, slab, beam, column, shear wall, diaphragm, braced frame, moment frame, connection, deflection, settlement.

## Candidate ranking before Kimi review

A candidate should enter Kimi review only if it passes minimum thresholds:

```text
relevanceScore >= 0.55
authorityScore >= 0.50
metadata title present
not known duplicate
not obviously broken
```

Higher standards for Rule nodes:

```text
authorityScore >= 0.75
jurisdiction/context present when applicable
primary source preferred
```

## Kimi review payload

Send Kimi node metadata, taxonomy path, candidate resource titles, URLs/identifiers, snippets or short summaries, proposed relationship type, scores, rationale, jurisdiction hints, and local/online status.

Ask Kimi to return accept/reject/needs_review, revised relationship type, revised rationale, missing better sources, jurisdiction concerns, and duplicate concerns.

## Human review queue

Human review should be required or strongly recommended for code/regulatory rules, structural safety claims, fire/life safety claims, accessibility compliance claims, legal/professional advice-like content, high-stakes exceptions, copyright ambiguity, and local standards/manuals with restricted access.
