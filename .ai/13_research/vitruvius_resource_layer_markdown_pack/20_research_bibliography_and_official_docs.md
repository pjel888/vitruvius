# 20 — Research Bibliography and Official Docs

Accessed/planning date: 2026-05-01

This file lists official documentation and source families useful for building the Vitruvius Resource Intelligence Layer.

## API / metadata discovery documentation

### Google Books API

- Volumes list documentation: https://developers.google.com/books/docs/v1/reference/volumes/list
- Volumes resource documentation: https://developers.google.com/books/docs/v1/reference/volumes

Use for book metadata, title/author/publisher/year, ISBN identifiers, and preview/view links. Treat as metadata discovery, not final authority.

### Open Library API

- Search API: https://openlibrary.org/dev/docs/api/search
- API overview: https://openlibrary.org/developers/api

Use for Work-level and Edition-level book metadata, author information, first publish year, identifiers, and subjects.

### Crossref REST API

- Metadata retrieval REST API: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- Swagger UI: https://api.crossref.org/swagger-ui/index.html

Use for DOI metadata, scholarly bibliographic metadata, and JSON search/filter/facet results.

### Semantic Scholar API

- API docs: https://api.semanticscholar.org/api-docs/
- Product/API overview: https://www.semanticscholar.org/product/api

Use for paper discovery, author/paper/citation metadata, Evidence nodes, and academic candidate discovery.

### OpenAlex API

- API overview: https://developers.openalex.org/api-reference/introduction
- Works overview: https://developers.openalex.org/api-reference/works

Use for scholarly works, authors, sources, institutions, topics, and academic metadata cross-checking.

### CORE API

- API documentation: https://core.ac.uk/documentation/api
- API v3 docs: https://api.core.ac.uk/docs/v3

Use for open-access research metadata and full-text/PDF discovery where available.

### DataCite REST API

- API introduction: https://support.datacite.org/docs/api

Use for DataCite DOI metadata, datasets, technical reports, and non-Crossref research outputs.

### Unpaywall API

- REST API: https://unpaywall.org/products/api
- Data format: https://unpaywall.org/data-format

Use for open-access availability by DOI and OA location/PDF discovery.

### Internet Archive APIs

- Tools and APIs: https://archive.org/developers/index-apis.html
- Item Metadata API: https://archive.org/developers/metadata.html
- Item metadata read endpoint: https://archive.org/developers/md-read.html
- Search information: https://archive.org/help/aboutsearch.htm

Use for public digital library metadata, item metadata by identifier, and historical/public-domain technical works where appropriate.

## AEC / BIM / classification documentation

### buildingSMART IFC

- IFC standards page: https://technical.buildingsmart.org/standards/ifc/
- IFC 4.3.2 docs: https://ifc43-docs.standards.buildingsmart.org/

Use for AEC spatial/object semantics, infrastructure/civil concepts, model relationships, and classification/mapping support.

### buildingSMART IDS

- IDS page: https://www.buildingsmart.org/standards/bsi-standards/information-delivery-specification-ids/
- Technical IDS project: https://technical.buildingsmart.org/projects/information-delivery-specification-ids/

Use for information requirement concepts, model data validation concepts, and source-backed information management nodes.

### ISO 19650

- ISO 19650-1 overview: https://www.iso.org/standard/68078.html
- BSI ISO 19650 overview: https://www.bsigroup.com/en-SG/products-and-services/standards/iso-19650-building-information-modelling-bim/

Use for information management concepts and project/asset information organization. Do not copy paywalled standard text.

### Uniclass

- NBS Uniclass overview: https://www.thenbs.com/our-tools/uniclass
- Uniclass browser: https://uniclass.thenbs.com/
- What is Uniclass: https://www.thenbs.com/knowledge/what-is-uniclass

Use for classification mappings, built-environment information organization, and source registry/document nodes.

### OmniClass

- CSI OmniClass overview: https://www.csiresources.org/standards/omniclass/standards-omniclass-about
- WBDG OmniClass resource: https://www.wbdg.org/resources/omniclass

Use for classification mappings and construction information organization.

## AEC professional / government source families

### WBDG / NIBS

- Whole Building Design: https://www.wbdg.org/whole-building-design
- WBDG home: https://www.wbdg.org/home
- NIBS WBDG page: https://nibs.org/wbdg/

Use for integrated whole-building design, building systems/interdisciplinary relationships, and lifecycle/performance concepts.

### ASCE / ASCE 7

- ASCE 7 page: https://www.asce.org/publications-and-news/asce-7
- ASCE/SEI 7-22 page: https://www.asce.org/publications-and-news/codes-and-standards/asce-sei-7-22

Use for structural/civil loads, hazards, and design-load source family. Jurisdiction/adoption matters.

### ACI / ACI 318

- ACI 318 Building Code Portal: https://www.concrete.org/topicsinconcrete/318buildingcodeportal.aspx
- ACI product page example: https://www.concrete.org/store/productdetail.aspx?ItemID=318U19

Use for structural concrete references and concrete design/detailing source family. Editions/adoption matter; do not copy standard text.

### AISC

- AISC home: https://www.aisc.org/

Use for structural steel references, steel manuals/specifications/source family.

### RIBA Plan of Work

- RIBA Plan of Work: https://www.riba.org/work/insights-and-resources/riba-plan-of-work/

Use for architectural/project lifecycle process concepts.

### IStructE Structural Plan of Work

- Structural Plan of Work: https://www.istructe.org/resources/guidance/the-structural-plan-of-work/

Use for structural engineering process/lifecycle concepts and interdisciplinary deliverables/roles.

## Research expansion areas

For future loops, research AEC knowledge graphs, semantic web for buildings, civil infrastructure ontologies, structural engineering ontologies, BIM-to-knowledge-graph mapping, digital twins for built assets, source-backed rules/evidence in engineering knowledge systems, local code/standard source management, and document-grounded retrieval/verification.
