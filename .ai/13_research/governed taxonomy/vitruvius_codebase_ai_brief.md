# Vitruvius Codebase AI Brief

## Purpose

You are auditing the **entire Vitruvius codebase** to determine how ready it is to support a governed, global AEC knowledge architecture with a **human-authored canonical taxonomy backbone** and **region-specific / jurisdiction-specific overlays** for laws, codes, standards, and regulatory data.

You must use the attached research files as the **target architectural intent**. Do **not** invent a different ontology. Your job is to:

1. inspect the current repository in full,
2. map the existing architecture and data model,
3. identify conflicts and gaps against the target model,
4. produce an **audit plan**, a **readiness plan**, and an **implementation plan**.

This pass is **analysis-first**. Do **not** start rewriting the system before the audit and plans are complete.

---

## Inputs you must treat as authoritative

Use the attached taxonomy research files as the target direction for the system, including:

- the comprehensive AEC taxonomy research markdown,
- the earlier taxonomy markdown,
- the YAML/JSON sample taxonomy exports,
- any related notes on jurisdiction, standards, and international handling.

If attached files disagree with current code, the **attached files define target intent** and the current code must be audited against them.

---

## Core architectural rules you must not violate

### 1. The main taxonomy backbone is global and human-authored
Vitruvius must have a stable canonical backbone for AEC subject matter. AI may classify into that backbone, but AI must not invent or mutate top-level taxonomy structure without human approval.

### 2. Region-specific and international data must be overlays, not taxonomy forks
Do **not** solve regional variation by duplicating or forking the taxonomy tree per country, state, or city. The canonical backbone stays global. Regional rules, laws, code editions, adoptions, amendments, annexes, and project-specific requirements sit in **separate jurisdictional and regulatory layers**.

### 3. Do not mix different axes in one tree
The following must remain separate, even if the current codebase mixes them:

- primary subject domain,
- lifecycle stage,
- asset/spatial scope,
- system/element class,
- work results / process,
- material class,
- role class,
- knowledge type,
- jurisdiction,
- external standards mappings.

If the current implementation puts these at the same level, flag it as a structural issue.

### 4. Canonical IDs must be independent of external standards
Do not use OmniClass, Uniclass, IFC, MasterFormat, ICC, NFPA, Eurocode, or any other external code as the primary identity of a Vitruvius node. External standards are mappings, not canonical IDs.

### 5. Region handling must support legal and technical precedence
The future system must support ordered precedence such as:

`project-specific requirement > local/city > state/province > national > supranational/regional > international model/consensus standard > internal default guidance`

Audit whether the current codebase can support this. If not, explain exactly why.

---

## Target conceptual model you are auditing against

The codebase must be evaluated against the following target model.

### A. Canonical knowledge backbone
Every knowledge node should ultimately map to one canonical `primary_domain` home in the governed AEC backbone.

### B. Mandatory or controlled facets
The system should support, directly or via adjacent entities, these controlled dimensions:

- `primary_domain` (exactly one)
- `asset_scope` (one or more)
- `lifecycle_stage` (one or more)
- `knowledge_type` (exactly one)
- `jurisdiction` (zero or more)
- `project_type` (zero or more)
- `performance_topic` (zero or more)
- `standard_mapping[]` (zero or more)

### C. Region-specific / international overlay model
The future architecture should separate the following concerns:

1. **Canonical taxonomy node**
2. **Jurisdiction hierarchy**
3. **Authority / publisher / regulator**
4. **Authority document family**
5. **Specific document edition / release**
6. **Document relationships** such as adopts / amends / annexes / supersedes / references
7. **Applicability rules** describing when a regulation or standard applies
8. **Localization / translations / local labels**
9. **Project-specific overlays or owner standards**
10. **Crosswalks to external classification systems**

### D. Target core entities to look for or recommend
Audit whether the codebase has equivalents of these entities, and if not, what would be required to add them:

- `TaxonomyNode`
- `Jurisdiction`
- `Authority`
- `AuthorityDocument`
- `DocumentEdition`
- `DocumentRelationship`
- `ApplicabilityRule`
- `Localization`
- `StandardMapping`
- `ProjectOverlay`
- `TaxonomyRelease`

### E. Target region-handling capabilities
The future system should be able to answer questions like:

- What applies globally vs nationally vs locally?
- Which edition of a code is active in a given jurisdiction on a given date?
- What is the relationship between a model code and a local adoption with amendments?
- How do Eurocodes map to National Annexes?
- How do ICC / NFPA / ASCE / ISO / CEN / national codes coexist without corrupting the taxonomy?
- Can a node have one canonical subject meaning but many jurisdiction-specific obligations?
- Can retrieval rank results by project context and jurisdiction precedence?

You must audit whether the current system can support that now, partially support it, or cannot support it.

---

## Required repository audit scope

You must inspect the entire repository. At minimum, audit:

- root structure and project layout,
- data layers and knowledge layers,
- conversion / ingestion pipelines,
- graph schema and node/edge definitions,
- explorer UI taxonomy rendering,
- APIs and payload contracts,
- manifests and config layers,
- search / retrieval / ranking logic,
- AI or local-model classification logic,
- storage schema and migrations,
- testing and validation tooling,
- docs and architecture notes,
- scripts and daemons,
- localization or i18n support,
- any standards / code / regulations handling already present.

### Priority paths to inspect first
You must explicitly inspect and report on paths equivalent to the following if they exist:

- `001-Raw-Source-Layer/`
- `001B_Spatial-Source-Layer/`
- `002-Raw-Conversion-Layer/`
- `003-Canonical-Knowledge-Layer/`
- `004-Derived-Content-Layer/`
- `005-Operational-Intelligence-Layer/`
- `006-System-Manifests/`
- `api/`
- `config/`
- `docs/`
- `explorer/`
- `src/`
- `scripts/`
- `spatial-daemon/`

Also inspect where the current node and edge types are defined, including any equivalents of:

- `Taxonomy`
- `Topic`
- `Subtopic`
- `Concept`
- `Rule`
- `Definition`
- `Procedure`
- `Exception`

and edges such as:

- `HAS_CHILD`
- `BELONGS_TO`
- `RELATED_TO`
- `DEPENDS_ON`
- `DEFINED_BY`
- `REQUIRES`
- `SUPPORTED_BY`

You must determine whether these are sufficient, overloaded, or structurally wrong for the target architecture.

---

## Required questions the audit must answer

Your audit must answer these questions with repo-based evidence.

### Current-state architecture
1. Where is the current taxonomy actually defined?
2. Is taxonomy currently inferred from folders, manifests, code constants, database tables, graph nodes, or generated content?
3. Where are node types and edge types declared?
4. Where are top-level categories hardcoded?
5. Which service or layer currently owns canonical truth?
6. Is there already a distinction between raw, canonical, and derived knowledge?
7. Is there already a graph projection layer, and how is it built?

### Data model and schema
8. What are the current core entities and their fields?
9. Can one node have one canonical parent but many contextual relationships?
10. Can the current model support facets cleanly, or only nested hierarchy?
11. How are IDs generated and persisted?
12. Is versioning already supported?
13. Is there a deprecation / merge / redirect model?
14. Are external standards currently stored as strings, tags, nodes, documents, or not at all?

### Region / jurisdiction / standards
15. Is there any existing model for region, jurisdiction, locale, or country?
16. Is there any existing model for laws, standards, or code editions?
17. Is there any support for effective dates, supersession, annexes, or local amendments?
18. Is there any support for multilingual labels or localization?
19. Can the system represent global guidance separately from enforceable local rules?
20. Can a knowledge node attach to many authorities or standards at once?

### Application behavior
21. Does the explorer UI assume one flat tree?
22. Does search assume one hierarchy instead of backbone + overlays?
23. Are APIs ready to return context-aware results by jurisdiction and date?
24. Are there hidden coupling points that will break if the taxonomy is normalized?
25. Are there hardcoded assumptions in prompts, scripts, manifests, or UI filters that collapse different axes together?

### Migration feasibility
26. What can be reused as-is?
27. What can be adapted with moderate effort?
28. What is structurally wrong and should not be preserved?
29. What would break if the backbone is frozen and top-level categories are normalized?
30. What is the minimum safe migration path?

---

## Required deliverables

Create the following documents in the repository under a path like:

`docs/plans/taxonomy-governance/`

If a different documentation structure is more appropriate, explain why and keep it organized.

### 1. `01_codebase_audit.md`
This is the evidence-based audit document.

It must include:

- executive summary,
- repository map,
- current architecture narrative,
- current taxonomy implementation map,
- current region / standards / regulatory handling map,
- current node and edge model,
- gap analysis against target architecture,
- risk register,
- unknowns / ambiguities,
- file-path evidence for every major claim.

Every major finding must include:

- what exists now,
- why it is good / insufficient / wrong,
- exactly where it lives,
- what it implies for migration.

### 2. `02_readiness_plan.md`
This is the plan that determines how ready the codebase is for the new architecture.

It must include:

- readiness scorecard by area,
- reuse vs replace analysis,
- blockers,
- prerequisites,
- data migration readiness,
- schema readiness,
- API readiness,
- UI readiness,
- search / retrieval readiness,
- AI pipeline readiness,
- documentation and testing readiness,
- recommended order of enabling work,
- quick wins vs long-lead items.

Score each dimension as one of:

- `ready`
- `partially ready`
- `not ready`

and explain why.

### 3. `03_implementation_plan.md`
This is the phased execution plan.

It must include:

- target architecture summary,
- workstreams,
- phased roadmap,
- repo areas affected per phase,
- schema changes,
- API changes,
- UI changes,
- migration/backfill steps,
- validation and testing strategy,
- release / rollout / rollback strategy,
- dependencies and sequencing,
- unresolved decisions requiring founder review.

### 4. `04_gap_matrix.md`
A structured matrix with columns like:

- target capability,
- current state,
- evidence,
- severity,
- recommended action,
- affected files,
- phase.

### 5. `05_pr_sequence.md`
Break the implementation into practical PR-sized work packages.

For each PR/work package, include:

- purpose,
- files/services likely affected,
- migration risk,
- test requirements,
- dependency on prior PRs.

### 6. `06_risk_register.md`
Track risks such as:

- data loss,
- broken node IDs,
- broken explorer navigation,
- search quality regression,
- standards mapping ambiguity,
- jurisdiction precedence conflicts,
- performance costs,
- operational complexity,
- editorial governance gaps.

---

## Output quality requirements

### Evidence standard
Every substantive claim must be tied to repository evidence:

- file paths,
- module names,
- symbol names,
- schema names,
- config keys,
- API routes,
- UI component names,
- migration files,
- tests.

Do **not** make confident architectural claims from filenames alone. If something is inferred rather than confirmed, label it as inference.

### No generic advice
Do not produce vague architecture writing. Every recommendation must be tied to this codebase.

Bad example:
> The app should use better abstractions.

Good example:
> `explorer/src/...` assumes a single hierarchical `parentId` tree and lacks typed support for jurisdiction overlays, so a secondary applicability index or join layer is required.

### Distinguish three things clearly
You must keep these separate in your writing:

1. **What exists now**
2. **What the target architecture requires**
3. **How to get from now to target**

Do not blur them together.

---

## Required readiness scoring dimensions

Use this scorecard in the readiness plan.

| Dimension | Score | Reason | Evidence | Action |
|---|---|---|---|---|
| Canonical taxonomy model |  |  |  |  |
| Node/edge graph model |  |  |  |  |
| Schema / storage model |  |  |  |  |
| ID/versioning model |  |  |  |  |
| Standards mapping model |  |  |  |  |
| Jurisdiction / regulatory model |  |  |  |  |
| Localization / i18n model |  |  |  |  |
| Ingestion / conversion pipeline |  |  |  |  |
| API contract readiness |  |  |  |  |
| Explorer UI readiness |  |  |  |  |
| Search / retrieval readiness |  |  |  |  |
| AI classification readiness |  |  |  |  |
| Testing / validation readiness |  |  |  |  |
| Release / migration readiness |  |  |  |  |
| Governance / editorial tooling |  |  |  |  |

---

## Required target architecture sections in the implementation plan

Your implementation plan must include these workstreams.

### Workstream 1. Canonical taxonomy package
Create or identify the source-of-truth package for the human-authored backbone.

Audit whether it should live as YAML/JSON in a versioned package and how the app should ingest it.

### Workstream 2. Controlled facet model
Add or normalize support for:

- `primary_domain`
- `asset_scope`
- `lifecycle_stage`
- `knowledge_type`
- `jurisdiction`
- `project_type`
- `performance_topic`
- `standard_mapping[]`

### Workstream 3. Jurisdiction hierarchy
Implement or recommend a jurisdiction tree that supports at least:

- international,
- supranational/regional,
- national,
- state/province,
- metro/city/local,
- project-specific.

Audit whether this should be adjacency-list, nested-set, materialized path, graph edges, or another model given the current stack.

### Workstream 4. Regulatory document registry
Support storage and retrieval of:

- code families,
- standard families,
- editions,
- effective dates,
- supersession,
- adoption,
- amendment,
- annex relationships,
- references between documents.

### Workstream 5. Applicability engine
Support the ability to attach rules/documents to context. At minimum, the design should consider conditions such as:

- jurisdiction,
- date/effective period,
- asset type,
- project type,
- occupancy/use,
- lifecycle stage,
- climate zone,
- hazard zone,
- owner/project overlay.

If the current codebase cannot support rule evaluation or retrieval ranking by context, say so explicitly.

### Workstream 6. Localization model
Support translations and local labels without mutating canonical IDs.

At minimum, audit support for:

- locale code,
- preferred label,
- alternate label,
- definition,
- synonyms,
- source/authority,
- fallback behavior.

### Workstream 7. Standards crosswalk layer
Support many-to-many mappings from Vitruvius nodes to external schemes and versions.

At minimum, mappings should be able to store:

- scheme,
- table,
- code,
- version,
- title,
- URI,
- mapping status,
- confidence,
- authority.

Mapping status should support values like:

- `exact`
- `broader`
- `narrower`
- `related`
- `candidate`

### Workstream 8. Explorer and API refactor
Audit what needs to change so the UI and APIs can handle:

- canonical subject tree,
- facet filters,
- jurisdiction overlays,
- standards mappings,
- date-aware retrieval,
- context-aware relevance.

### Workstream 9. Search and retrieval
Audit what would be needed so search can rank by:

- canonical relevance,
- jurisdiction precedence,
- effective date,
- project context,
- document authority,
- mapping confidence.

### Workstream 10. Migration and backfill
You must propose how to migrate existing nodes to the new model.

At minimum, define a migration flow for:

1. inventory existing nodes,
2. detect current axis/viewpoint,
3. assign canonical `primary_domain`,
4. assign facets,
5. attach standards mappings,
6. attach jurisdiction where relevant,
7. create redirects from legacy IDs,
8. rebuild projections and indexes,
9. regression test the explorer and search.

### Workstream 11. Governance and release process
The plan must define how Vitruvius will govern changes to:

- canonical taxonomy,
- standards mappings,
- jurisdiction layers,
- code editions,
- translations,
- deprecations,
- migrations.

---

## Required region-specific and international architecture recommendations

When evaluating the codebase, you must explicitly address how the future implementation should handle the following patterns.

### Pattern A. Global concept, local enforcement
Example shape:

- one canonical subject node,
- multiple local obligations or references,
- different editions and jurisdictions,
- same concept, different enforceability.

### Pattern B. Model code adopted with amendments
The data model must distinguish:

- original source document,
- adoption jurisdiction,
- effective edition,
- amendment package,
- superseding edition,
- project-specific overrides.

### Pattern C. International standard with national annex
The model must be able to represent:

- base international or regional standard,
- national annex,
- local adaptation,
- applicability in a specific jurisdiction.

### Pattern D. Voluntary guidance vs mandatory requirement
The system must distinguish:

- mandatory law/code,
- referenced standard,
- consensus standard,
- guidance,
- internal best practice,
- project requirement.

### Pattern E. Multilingual and localized terminology
The system must support local labels and translations while preserving one canonical meaning.

### Pattern F. Time-sensitive applicability
The system must support effective periods. A rule that applied in 2020 may be superseded in 2026.

You must audit whether the current codebase can support each of these patterns.

---

## Required implementation sequencing

Your implementation plan must sequence work in phases and explain why that sequence is safest.

Use a structure similar to this, but adapt it to what the repo actually needs:

### Phase 0. Freeze and inventory
- freeze top-level taxonomy edits,
- inventory current nodes/types/edges,
- locate hardcoded assumptions,
- document unknowns.

### Phase 1. Canonical taxonomy source of truth
- create or normalize the governed backbone package,
- define schema validation,
- define canonical IDs,
- define release/versioning.

### Phase 2. Core schema and graph changes
- add normalized entities/fields for facets, mappings, jurisdictions, editions,
- add required edge types,
- preserve backward compatibility where possible.

### Phase 3. Region and regulatory layer
- add jurisdiction tree,
- add authority documents and editions,
- add adoption / annex / amendment / supersession modeling,
- add applicability rules.

### Phase 4. Ingestion and mapping
- update conversion and canonicalization pipelines,
- map existing content into new schema,
- attach crosswalks,
- create migration scripts.

### Phase 5. Explorer and API
- update API contracts,
- update explorer UI to render backbone + filters + overlays,
- preserve or redirect legacy navigation.

### Phase 6. Search and ranking
- update indexes,
- add context-aware ranking,
- support jurisdiction/date-aware retrieval.

### Phase 7. Backfill, QA, and release
- backfill legacy content,
- validate mappings,
- regression test,
- staged rollout,
- rollback plan.

### Phase 8. Governance tooling
- editorial workflows,
- change approval,
- version releases,
- deprecation and redirect handling,
- review queues for AI-proposed mappings.

---

## Required PR/work-package format

In `05_pr_sequence.md`, use a format like this for each work package:

### PR-01: Canonical taxonomy schema foundation
- Objective:
- Why this comes first:
- Repo areas affected:
- Schema changes:
- API changes:
- UI impact:
- Migration impact:
- Test requirements:
- Risks:
- Depends on:

Every work package must be small enough to implement and review.

---

## Required migration safety rules

When proposing implementation, follow these rules:

1. Prefer additive migrations before destructive cleanup.
2. Preserve legacy IDs through redirects or mapping tables where possible.
3. Do not break the explorer without an explicit compatibility plan.
4. Do not convert standards codes into canonical IDs.
5. Do not bury jurisdiction inside free text.
6. Do not solve localization by duplicating nodes.
7. Do not treat folders as ontology unless the repo explicitly proves that they are the canonical source.

---

## Required final summary section

At the end of the work, produce a final summary that answers these five questions directly:

1. What is structurally sound in the current codebase?
2. What is fundamentally wrong and should be changed?
3. What is the minimum viable path to readiness?
4. What is the safest phased implementation order?
5. What founder decisions are still required before coding begins?

---

## Short instruction for execution

Perform the work in this order:

1. inspect the full repository,
2. produce the audit,
3. produce the readiness plan,
4. produce the implementation plan,
5. produce the supporting matrices and PR sequence,
6. stop and wait for approval before major code changes.

Do not skip the audit. Do not jump straight to refactoring.

