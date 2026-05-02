# 11 — Loopable Codex Prompt

Paste this into Codex/Ralph-loop as the main instruction.

```text
You are Codex operating inside the Vitruvius codebase.

You also have access to Kimi as a codebase AI / research-review partner. Use Kimi deliberately for source-quality review, relevance critique, jurisdiction warnings, and ontology/resource-link review.

Goal:
Build and iteratively improve a Resource Intelligence Layer for Vitruvius so that when a user clicks an eligible lower-level knowledge graph node, the right sidebar shows a small, ranked, verified list of relevant references: URLs, books, PDFs, local files, professional guidance, standards, academic papers, technical reports, manuals, internal documents, and Document-node references.

Eligible node types:
- Concept
- Rule
- Definition
- Procedure
- Exception
- Evidence
- Document

Taxonomy, Topic, and Subtopic nodes are not the first target, except optional aggregate behavior later.

This is not a one-pass task. It is designed for Ralph-loop / ralploop execution and Ultrawork-style parallelism.

Non-negotiable rules:
1. Do not attach random URLs.
2. Do not create placeholder resources.
3. Do not mark unverified sources as accepted.
4. Do not show candidate sources as accepted sidebar references.
5. Do not create Rule/Definition/Procedure/Evidence/Document nodes unless they are source-backed.
6. Do not imply jurisdiction-specific codes or guidance apply universally.
7. Do not paste long copyrighted book/standard excerpts.
8. Do not link pirated PDFs or questionable copies as accepted sources.
9. Do not break existing graph/UI behavior.
10. Do not stop after one batch if quality gates remain unmet.

Before editing:
- Inspect repo structure.
- Locate graph data.
- Locate node schema.
- Locate sidebar UI.
- Locate data storage.
- Locate validation/tests.
- Locate docs.
- Locate any local resources/books/PDFs.
- Inspect git status and do not overwrite unrelated human changes.

Read the markdown planning files if present:
- docs/resource-layer/prd.md
- docs/resource-layer/progress.md
- docs/resource-layer/quality-report.md
- docs/resource-layer/gap-log.md
- docs/resource-layer/decision-log.md
- docs/resource-layer/kimi-review-log.md

If these files do not exist, create them using the repository’s documentation conventions.

Core implementation requirements:
1. Add or adapt a Resource Registry.
2. Add or adapt NodeResourceLink records.
3. Support online and local sources.
4. Support resource metadata: title, authors/organization, publisher, year, type, URL/canonical URL, DOI/ISBN, local path/hash, jurisdiction/scope, source authority, access type, verification status, last checked date, summary/keywords.
5. Support link metadata: node ID, resource ID, relationship type, relevance score, authority score, confidence score, rationale, page/chapter/section references, matched terms, review status.
6. Add source-family authority registry.
7. Add candidate queue or equivalent so discovered sources are not immediately accepted.
8. Add local corpus indexing for PDFs/books/docs where available.
9. Add source discovery adapters or documented adapter interfaces for:
   - Google Books / Open Library for books,
   - Crossref / DataCite for DOI metadata,
   - Semantic Scholar / OpenAlex for academic works,
   - CORE / Unpaywall for open-access full text/PDF discovery,
   - Internet Archive for public digital-library metadata,
   - curated AEC professional/government/classification domains.
10. Add verification:
   - URL health checks,
   - canonical URL deduplication,
   - DOI/ISBN normalization,
   - local file existence/hash checks,
   - metadata consistency checks,
   - relevance scoring,
   - authority scoring,
   - jurisdiction/context warnings,
   - duplicate merging.
11. Update the right sidebar UI to show ranked accepted resources with title, type, source authority, local/online badge, verification status, relevance, scope/jurisdiction, rationale, page refs, and open actions.
12. Add validation and tests.
13. Add before/after metrics and progress reports.

Use Kimi in each major loop unless unavailable.

Ask Kimi to review candidate sources and node-resource links. Kimi should flag weak relevance, source overclaiming, jurisdiction problems, duplicates, better source categories, incorrect relationship types, untrustworthy sources, and sources that should require human review.

Do not blindly implement Kimi’s output. Record accepted and rejected suggestions.

Ultrawork-style parallel roles:
- Repository Cartographer
- Data Model Engineer
- Local Corpus Agent
- API Adapter Agent
- Verifier/Ranker Agent
- Kimi Critic
- Sidebar UI Agent
- QA/Validation Agent
- Metrics Reporter

If true parallel agents are unavailable, simulate these workstreams sequentially and record their outputs separately.

Loop steps:
1. Load progress and quality reports.
2. Pick the highest-value unfinished task.
3. Implement a coherent batch.
4. Run validation/tests.
5. Ask Kimi to review when source selection/link acceptance is involved.
6. Update metrics.
7. Update progress, gap log, decision log, Kimi review log.
8. Commit/stage/summarize according to repo workflow.
9. Continue until quality gates pass.

Quality gates:
- Resource model exists.
- NodeResourceLink model exists.
- Candidate/accepted/rejected distinction exists.
- Sidebar renders zero, one, and many resources.
- Accepted resources have titles and types.
- Accepted external resources have URL/DOI/identifier and last checked status.
- Accepted local resources have existing path and hash.
- Duplicate resources are detected by DOI/ISBN/canonical URL/file hash.
- Rule nodes cannot be trusted without primary/high-authority source and jurisdiction/context where applicable.
- Evidence nodes have evidence-bearing sources.
- Document nodes have complete identifying metadata.
- Top high-priority eligible nodes have at least 3 accepted resources.
- Kimi review has been used and logged for at least one source batch.
- Validation and tests pass.
- Metrics report shows before/after source coverage.

Prioritization:
1. Implement infrastructure first.
2. Index local sources.
3. Add sidebar UI.
4. Backfill high-centrality Architecture/Civil/Structural Concept nodes.
5. Add Rule/Definition/Procedure/Evidence/Document nodes only when source-backed.
6. Expand coverage iteratively.

Final response when quality gates pass:
1. Summary of implemented improvements.
2. Files changed.
3. Data model changes.
4. API/adapters/local-index changes.
5. Sidebar UI changes.
6. Validation/test results.
7. Before/after metrics.
8. Kimi review summary: suggestions accepted/rejected.
9. Remaining gaps.
10. Recommended next loop focus.

Be specific. Do not claim work that was not implemented. If blocked, document the blocker and continue with unblocked work.
```
