# 17 — Implementation Roadmap and Milestones

## Milestone 0 — Repository discovery

Find graph files/data structures, node types, sidebar UI, validation/tests, source/provenance models, local files/books/PDFs, and document the repo map.

## Milestone 1 — Resource data model

Add Resource model, NodeResourceLink model, SourceFamily registry, ResourceCandidate model/queue, ResourceCheck model if feasible, and validation for basic resource/link shape.

Success: accepted resource cannot be missing title/type/status, and node-resource link cannot point to missing node/resource.

## Milestone 2 — Sidebar skeleton

Add sidebar section for eligible nodes, render accepted resources, render empty state, render badges, add filters/sorting if feasible, and test zero/one/many resources.

Success: clicking eligible node shows resource panel without breaking graph UI.

## Milestone 3 — Local corpus indexing

Scan local file folders, extract basic metadata, compute hashes, store local resources, optionally extract text/page chunks, and generate initial local candidates.

Success: local files can appear in sidebar if linked and verified.

## Milestone 4 — Verification/ranking/deduplication

Implement URL checks, DOI/ISBN normalization, canonical URL normalization, duplicate detection, relevance/authority/display scoring, and candidate acceptance workflow.

Success: rejected/duplicate/broken/unverified sources do not show as accepted.

## Milestone 5 — First API adapters

Recommended order:

1. Open Library and/or Google Books for book metadata.
2. Crossref for DOI metadata.
3. OpenAlex/Semantic Scholar for academic discovery.
4. CORE/Unpaywall for OA discovery.
5. Internet Archive for digital library metadata.

Adapters must cache results, produce candidates only, and normalize metadata.

## Milestone 6 — Kimi review loop

Add Kimi review prompt templates, add review log, run review on first candidate batch, and record accepted/rejected suggestions.

Success: Kimi review changes at least one acceptance/ranking/rationale decision or confirms a batch.

## Milestone 7 — Backfill high-priority nodes

Identify high-centrality eligible nodes, process top 25 first, link 3–5 accepted resources each, prefer Architecture/Civil/Structural nodes, validate, and report.

## Milestone 8 — Lower node type creation

Create source-backed Definition, Procedure, Evidence, Document, and carefully selected Rule nodes.

## Milestone 9 — Production-quality metrics and dashboards

Add coverage report, source quality report, broken-link report, duplicate report, Kimi/human review report, and sidebar usage metrics if available.

## Milestone 10 — Continuous loop

Use Ralph-loop and Ultrawork-style workstreams to keep processing batches. Keep updating docs and metrics. Stop only when current quality gates are met.

## Recommended first sprint

1. Add models and source family registry.
2. Add sidebar rendering with seed data.
3. Add validation.
4. Add local corpus scanner.
5. Backfill 10 high-priority nodes manually/semiautomatically.
6. Run Kimi review.
7. Generate quality report.
