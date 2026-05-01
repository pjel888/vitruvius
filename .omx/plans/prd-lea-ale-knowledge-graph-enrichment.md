# PRD — LEA/ALE Knowledge Graph Enrichment

- **Created:** 2026-04-29T08:40:24Z
- **Status:** active

## Problem
The AEC-MEPFS backbone contains only shallow Philippine ALE/licensure anchors. It needs subject-domain depth, law/code cross-links, source-aware aliases, and practical semantic relationships for Philippine architecture licensure study and professional reasoning.

## Goals
1. Add substantial LEA/ALE nodes organized by real architectural subjects/domains, not only PRC broad exam-day areas.
2. Add 300+ governed relationships where schema allows, prioritizing law/code/design/utilities/practice/history/theory cross-links.
3. Improve 50+ existing nodes with aliases, descriptions, source references, or relationships where safe.
4. Add 75+ useful aliases/acronyms and 20+ metadata-only source/provenance references where missing.
5. Inventory relevant raw PDFs and classify source rights without ingesting protected payloads.
6. Keep Kimi-only model-assisted enrichment routing and verify no active Codex Spark enrichment provider remains.

## Non-goals
- No live Neo4j promotion or production graph mutation.
- No protected law/code/textbook/reviewer payload ingestion.
- No schedule tracker for PRC exam dates.
- No destructive deletes or raw source writes.

## Acceptance criteria
- File-backed graph content changes are visible in the source-of-truth fixture and generated shadow artifacts.
- Validation passes for contracts, focused enrichment tests, broad affected tests, JSON checks, API backbone test, source-rights safety, and safety grep.
- Final Kimi review confirms taxonomy/source-family reasonableness at a metadata-only level.
