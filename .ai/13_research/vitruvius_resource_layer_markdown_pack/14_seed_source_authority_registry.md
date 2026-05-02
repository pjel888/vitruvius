# 14 — Seed Source Authority Registry

## Purpose

A source authority registry helps the system rank and review resources. It prevents low-quality web sources from outranking official/professional references when relevance is similar.

This file is a planning seed. Codex should adapt it to the actual codebase format.

## Authority tiers

### Tier 1 — Official / professional / government / standards-oriented

```yaml
- id: buildingsmart
  label: buildingSMART International
  domains: [buildingsmart.org, technical.buildingsmart.org, standards.buildingsmart.org, ifc43-docs.standards.buildingsmart.org]
  authority: official
  authorityTier: 1
  disciplines: [AEC, BIM, information_management, interoperability]
  typicalResourceTypes: [ontology_documentation, standard, professional_guidance]
  allowedForPrimaryRuleSource: true
  notes: IFC/IDS/bSDD documentation; use for information/model semantics, not as universal construction truth.

- id: wbdg_nibs
  label: Whole Building Design Guide / NIBS
  domains: [wbdg.org, nibs.org]
  authority: government
  authorityTier: 1
  disciplines: [architecture, engineering, construction, operations, performance]
  typicalResourceTypes: [professional_guidance, government_guidance, webpage]
  allowedForPrimaryRuleSource: true

- id: asce
  label: American Society of Civil Engineers
  domains: [asce.org, ascelibrary.org]
  authority: professional_body
  authorityTier: 1
  disciplines: [civil_engineering, structural_engineering]
  typicalResourceTypes: [standard, professional_guidance, academic_paper]
  allowedForPrimaryRuleSource: true
  notes: US/professional context; code adoption depends on jurisdiction.

- id: aci
  label: American Concrete Institute
  domains: [concrete.org]
  authority: professional_body
  authorityTier: 1
  disciplines: [structural_engineering, concrete]
  typicalResourceTypes: [standard, code, professional_guidance]
  allowedForPrimaryRuleSource: true
  notes: Strong for concrete; identify edition/year and adoption context.

- id: aisc
  label: American Institute of Steel Construction
  domains: [aisc.org]
  authority: professional_body
  authorityTier: 1
  disciplines: [structural_engineering, steel]
  typicalResourceTypes: [standard, manual, professional_guidance]
  allowedForPrimaryRuleSource: true
  notes: Strong for structural steel; US-oriented.

- id: riba
  label: Royal Institute of British Architects
  domains: [riba.org]
  authority: professional_body
  authorityTier: 1
  disciplines: [architecture, project_process]
  typicalResourceTypes: [professional_guidance]
  allowedForPrimaryRuleSource: false

- id: istructe
  label: Institution of Structural Engineers
  domains: [istructe.org]
  authority: professional_body
  authorityTier: 1
  disciplines: [structural_engineering]
  typicalResourceTypes: [professional_guidance, technical_report]
  allowedForPrimaryRuleSource: true

- id: fhwa
  label: Federal Highway Administration
  domains: [fhwa.dot.gov]
  authority: government
  authorityTier: 1
  disciplines: [civil_engineering, transportation, geotechnical, infrastructure]
  typicalResourceTypes: [government_guidance, technical_report, manual]
  allowedForPrimaryRuleSource: true

- id: fema
  label: Federal Emergency Management Agency
  domains: [fema.gov]
  authority: government
  authorityTier: 1
  disciplines: [resilience, flood_risk, hazards, civil_engineering, architecture]
  typicalResourceTypes: [government_guidance, technical_report]
  allowedForPrimaryRuleSource: true

- id: usgs
  label: United States Geological Survey
  domains: [usgs.gov]
  authority: government
  authorityTier: 1
  disciplines: [geology, hazards, geotechnical_context, water]
  typicalResourceTypes: [dataset, technical_report, government_guidance]
  allowedForPrimaryRuleSource: false

- id: nist
  label: National Institute of Standards and Technology
  domains: [nist.gov]
  authority: government
  authorityTier: 1
  disciplines: [engineering, resilience, performance, measurement]
  typicalResourceTypes: [technical_report, government_guidance]
  allowedForPrimaryRuleSource: true

- id: uniclass_nbs
  label: NBS Uniclass
  domains: [thenbs.com, uniclass.thenbs.com]
  authority: professional_body
  authorityTier: 1
  disciplines: [classification, built_environment, information_management]
  typicalResourceTypes: [classification_system]
  allowedForPrimaryRuleSource: false
  notes: Use for classification/mapping, not design compliance.

- id: omniclass_csi
  label: OmniClass / CSI
  domains: [csiresources.org, wbdg.org]
  authority: professional_body
  authorityTier: 1
  disciplines: [classification, construction_information]
  typicalResourceTypes: [classification_system]
  allowedForPrimaryRuleSource: false
```

### Tier 2 — Academic and metadata infrastructures

```yaml
- id: crossref
  label: Crossref
  domains: [crossref.org, api.crossref.org]
  authority: academic
  authorityTier: 2
  disciplines: [research_metadata]
  typicalResourceTypes: [academic_paper, technical_report]
  allowedForPrimaryRuleSource: false
  notes: Metadata registry, not a source authority for the content itself.

- id: semantic_scholar
  label: Semantic Scholar
  domains: [semanticscholar.org, api.semanticscholar.org]
  authority: academic
  authorityTier: 2
  disciplines: [research_metadata]
  typicalResourceTypes: [academic_paper]
  allowedForPrimaryRuleSource: false

- id: openalex
  label: OpenAlex
  domains: [openalex.org, developers.openalex.org]
  authority: academic
  authorityTier: 2
  disciplines: [research_metadata]
  typicalResourceTypes: [academic_paper, book, dataset]
  allowedForPrimaryRuleSource: false

- id: datacite
  label: DataCite
  domains: [datacite.org, support.datacite.org]
  authority: academic
  authorityTier: 2
  disciplines: [research_metadata, datasets]
  typicalResourceTypes: [dataset, technical_report, academic_paper]
  allowedForPrimaryRuleSource: false

- id: core
  label: CORE
  domains: [core.ac.uk]
  authority: academic
  authorityTier: 2
  disciplines: [open_access_research]
  typicalResourceTypes: [academic_paper]
  allowedForPrimaryRuleSource: false

- id: unpaywall
  label: Unpaywall
  domains: [unpaywall.org]
  authority: academic
  authorityTier: 2
  disciplines: [open_access_discovery]
  typicalResourceTypes: [academic_paper]
  allowedForPrimaryRuleSource: false
```

### Tier 3 — Books and public libraries

```yaml
- id: google_books
  label: Google Books
  domains: [books.google.com, developers.google.com]
  authority: recognized_publisher
  authorityTier: 3
  disciplines: [book_metadata]
  typicalResourceTypes: [book, textbook]
  allowedForPrimaryRuleSource: false
  notes: Metadata/preview discovery; not authority by itself.

- id: open_library
  label: Open Library
  domains: [openlibrary.org]
  authority: recognized_publisher
  authorityTier: 3
  disciplines: [book_metadata]
  typicalResourceTypes: [book, textbook]
  allowedForPrimaryRuleSource: false

- id: internet_archive
  label: Internet Archive
  domains: [archive.org]
  authority: recognized_publisher
  authorityTier: 3
  disciplines: [digital_library]
  typicalResourceTypes: [book, local_book, pdf, webpage]
  allowedForPrimaryRuleSource: false
  notes: Useful for public/historical works; check copyright/access.
```

### Tier 4 — Manufacturer / product-specific

```yaml
- id: manufacturer_generic
  label: Manufacturer technical documentation
  authority: manufacturer
  authorityTier: 4
  disciplines: [product_specific, installation, maintenance]
  typicalResourceTypes: [manufacturer_manual, manual, webpage]
  allowedForPrimaryRuleSource: false
  notes: Do not use as generic design authority unless product-specific.
```

### Tier 5 — General web

```yaml
- id: general_web
  label: General web
  authority: general_web
  authorityTier: 5
  disciplines: [general]
  typicalResourceTypes: [webpage]
  allowedForPrimaryRuleSource: false
  notes: Candidate only; requires stronger review and should rarely be top-ranked.
```

## Authority score mapping

```text
Tier 1: 0.90–1.00
Tier 2: 0.75–0.90 depending on item quality
Tier 3: 0.60–0.85 depending on book/source quality
Tier 4: 0.50–0.75 if product-specific; lower if generic node
Tier 5: 0.10–0.50
```

Authority tier does not equal relevance. A Tier 1 source can still be a bad match if it only mentions the term in passing.
