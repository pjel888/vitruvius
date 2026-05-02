# 01 — PRD: Vitruvius Resource Intelligence Layer

## Product name

Vitruvius Resource Intelligence Layer

## One-line summary

Add a verified, ranked source/reference layer so eligible knowledge graph nodes can show relevant URLs, books, PDFs, local documents, standards, professional guidance, academic papers, and evidence in the right sidebar.

## Problem

Vitruvius currently has many knowledge graph nodes, but users need a way to understand:

- where a concept comes from,
- what sources explain it,
- whether a rule is authoritative,
- which local PDFs/books are relevant,
- which internet sources are reliable,
- which page or section to consult,
- whether a claim is jurisdiction-sensitive,
- whether the resource has been verified.

A plain list of URLs will not be trustworthy enough. The system needs structured source metadata, verification, ranking, deduplication, and review workflows.

## Goals

1. Add a reusable Resource Registry.
2. Add NodeResourceLink records that connect graph nodes to resources.
3. Support online and local sources.
4. Support books, PDFs, standards, codes, academic papers, webpages, manuals, and internal documents.
5. Add verification and ranking.
6. Add UI sidebar support.
7. Add Codex/Kimi loopable source discovery and review workflows.
8. Add validation to prevent low-quality source links.
9. Create a foundation for source-backed Rule, Definition, Procedure, Exception, Evidence, and Document nodes.

## Non-goals for first release

- Do not backfill every node immediately.
- Do not guarantee every source is legally accessible to every user.
- Do not make legal/code compliance claims.
- Do not redistribute copyrighted book/standard content.
- Do not replace the graph itself with a citation database.
- Do not create hundreds of weak links per node.
- Do not auto-certify safety-critical or jurisdictional rules as final without review.

## Eligible node types

First-class eligible nodes:

- Concept
- Rule
- Definition
- Procedure
- Exception
- Evidence
- Document

Optional future behavior:

- Topic/Subtopic summary sources
- Taxonomy overview sources
- inherited references from child nodes

## User stories

### Story 1 — Concept reference sidebar

As a user, when I click a Concept node, I want to see 3–5 high-quality sources that explain the concept, so I can quickly understand the concept and where it is grounded.

Acceptance:

- Sidebar shows title, type, source authority, relevance, verification status, and rationale.
- Local resources are clearly marked.
- Broken/unverified links are not shown as accepted by default.

### Story 2 — Local PDF/book references

As a user, when a relevant local PDF or book exists, I want the sidebar to show it with page or chapter references where available.

Acceptance:

- Local file exists.
- Local file hash is stored.
- Resource card indicates local-only access.
- Page/chapter reference is shown if extraction succeeded.

### Story 3 — Rule nodes require primary sources

As a user, when I click a Rule node, I need to know the authority/source of that rule and whether it is jurisdiction-specific.

Acceptance:

- Rule nodes have at least one accepted primary or professional source.
- Jurisdiction/context is shown when applicable.
- Unreviewed code-like rules are visibly marked as needs review.

### Story 4 — Evidence nodes cite evidence

As a user, when I click an Evidence node, I want to see the academic, professional, or local source that supports the evidence.

Acceptance:

- Evidence nodes have at least one paper/report/local document source.
- DOI or stable identifier is captured when available.
- Evidence relationship is not confused with general explanation.

### Story 5 — Document nodes have complete metadata

As a user, when I click a Document node, I want to see title, authors/organization, publisher, year, identifiers, online/local access, and linked concepts.

Acceptance:

- Document metadata is complete enough for identification.
- Duplicate documents are merged where possible.
- Linked nodes are visible or queryable.

### Story 6 — Kimi review

As the system owner, I want Kimi to review candidate sources and source-node links so low-quality or overclaimed references are rejected before they pollute the graph.

Acceptance:

- Kimi review batches are recorded.
- Accepted/rejected suggestions are logged.
- Rejected candidates do not appear as accepted sidebar references.

## Functional requirements

### Resource Registry

The system must store structured resources with:

- stable ID,
- title,
- resource type,
- author/organization/publisher where available,
- year where available,
- URL/canonical URL where online,
- DOI/ISBN/identifier where available,
- local path/file hash where local,
- source authority tier,
- discipline/taxonomy tags,
- jurisdiction/scope,
- access type,
- verification status,
- last checked date,
- summary/abstract/keywords where available.

### NodeResourceLink

The system must store links between nodes and resources with:

- node ID,
- resource ID,
- relationship type,
- relevance score,
- authority score,
- confidence score,
- rationale,
- page/chapter/section references if available,
- matched terms/aliases,
- review status,
- reviewer/source of review.

### Source discovery

The system should support adapters or scripts for:

- local corpus indexing,
- Google Books / Open Library book metadata,
- Crossref / DataCite DOI metadata,
- Semantic Scholar / OpenAlex academic discovery,
- CORE / Unpaywall open-access discovery,
- Internet Archive public digital library discovery,
- curated AEC trusted domains.

### Verification

The system must support:

- URL health checks,
- DOI/ISBN normalization,
- local file existence checks,
- file hashing,
- canonical URL deduplication,
- duplicate resource merging,
- authority scoring,
- relevance scoring,
- jurisdiction warnings,
- review status transitions.

### Sidebar

The sidebar must show:

- resource title,
- resource type,
- source authority badge,
- local/online badge,
- verification status,
- relevance score,
- jurisdiction/scope if any,
- short rationale,
- page/chapter/section refs where available,
- open URL or open local file action where supported,
- filters by type/source/status.

## Non-functional requirements

- Must not break existing graph rendering.
- Must tolerate zero resources for a node.
- Must support incremental backfilling.
- Must preserve existing schema conventions where possible.
- Must avoid long blocking web/API calls during normal UI rendering.
- Must cache API results.
- Must rate-limit external API use.
- Must log source-discovery batches.
- Must be loopable by codebase AI.

## Quality gates

Do not declare complete until:

- Resource model exists.
- NodeResourceLink model exists.
- Sidebar can render zero/one/many resources.
- At least one local resource or local-index workflow is supported.
- At least one online discovery adapter or documented interface is implemented.
- Validation catches broken/missing/duplicate resources.
- High-priority nodes have source coverage.
- Kimi review process is documented and used for at least one candidate batch.
- Metrics report before/after coverage.

## Final deliverable report

The codebase AI should produce:

- files changed,
- schema/data-model changes,
- UI changes,
- validation/test changes,
- APIs/adapters added,
- source coverage metrics,
- Kimi review summary,
- remaining gaps,
- recommended next loop.
