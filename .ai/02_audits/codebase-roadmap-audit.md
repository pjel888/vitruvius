# Vitruvius Codebase & Roadmap Audit
**Date:** 2026-04-13
**Auditor:** Senior Architect (Gemini CLI)
**Status:** Brutally Honest / Evidence-Based

## 1. Audit Scope
The audit covered the following areas:
- **CLI Surface:** `scripts/pipeline_cli.py`
- **Core Package:** `scripts/vitruvius/` (All modules)
- **Data Layers:** `001` through `006`
- **Documentation:** `README.md`, `.ai/01_roadmap/`, `docs/`
- **Verification Method:** Direct code inspection and comparison of claims vs. implementation logic.

## 2. Verified Complete Features (High Integrity)
These features are implemented, wired, and reflect high-quality engineering:
- **Multi-Format Ingestion:** PDF (OpenDataLoader), Office (LibreOffice), and Spreadsheet (OpenPyxl/LibreOffice) ingestion paths are fully functional.
- **OCR Pipeline:** OCR queueing and execution (`ocrmypdf`) are properly implemented and integrated with the conversion layer.
- **PDF Detection:** Heuristic-based text vs. scanned detection is solid and used for routing.
- **Registry & Manifest System:** Detailed CSV registries and JSON/TXT run reports are generated for almost every operation.
- **LLM Review Layer:** Ollama integration is functional, including timeout handling, structured JSON parsing, and progress tracking.

## 3. Verified Partial / Weak Features (Low Integrity)
These features are marked "Complete" in roadmaps but are actually minimal placeholders:
- **Canonicalization Layer:** The `canonicalize.py` script is a skeleton. It only generates basic frontmatter and headers. It lacks the ability to generate the "Overview", "Coverage", or "Key Points" seen in some repository examples. The automation is currently just a metadata wrapper.
- **Concept Generation:** `concepts.py` creates placeholder files. It does not extract definitions or enrich content. It simply asserts that "X is a concept".
- **Relationship Extraction:** The logic is purely regex-based matching of concept phrases within a sliding line window. This produces a high volume of false positives (82% rejection rate in latest runs). It is "functional" but technically "primitive".
- **ID Migration:** The scripts work as intended for simple text replacement, but the system relies on manual mapping in `id_migration_map.yaml`.

## 4. Verified Missing / Overstated Features
- **Promotion Layer:** Correctly identified as "Not started" in roadmap. No code exists in `scripts/vitruvius/`.
- **Concept Enrichment:** Marked as `[ ]` in roadmap. Verified as missing.
- **Multi-parser Integration:** No evidence of multi-parser logic beyond the standard PDF extraction.
- **Normalization Pipeline:** No dedicated normalization logic beyond basic text cleaning.
- **Operational Intelligence Layer:** Layers `005` (Chunks, Embeddings, Graphs) are currently empty or only contain placeholder directories.

## 5. Documentation Mismatches
- **Roadmap Inflation:** "Phase 2 — Canonicalization" is marked as `[x] Complete`. In a professional context, this should be `[~] Partial/Placeholder`, as the current script does not produce the quality of content implied by the roadmap's own documentation.
- **State Tracking:** `.ai/10_state` files (e.g., `system_state.json`) are all 0 bytes. The documentation implies active state management that is currently unpopulated.

## 6. Critical Risks
- **Brittle Extraction:** The reliance on basic regex for relationship extraction makes the system heavily dependent on a "ruthless" review layer to filter out noise. Without a better parser, the system will struggle as the concept count grows.
- **Lost Tooling:** There is a mismatch between the current `canonicalize.py` and the existing "high-quality" canonical files in `003_Canonical-Knowledge-Layer`. This suggests the current script is a regression or a simplified replacement for a tool that is no longer in the repo.
- **Hardcoded Endpoints:** Ollama URL is hardcoded to `127.0.0.1:11434`.

## 7. Recommended Roadmap Corrections
- **Demote Phase 2 & 3:** Mark as `[~] Partial` instead of `[x] Complete` until real extraction/enrichment logic is added.
- **Prioritize Promotion:** The project is blocked on moving "Reviewed" knowledge into the "Canonical" layer.
- **Refine Extraction:** High priority to move beyond regex for relationship candidate generation.

---
**Audit result: PROJECT IS IN LATE INGESTION / EARLY EXTRACTION PHASE.**
*Claims of being "Starting Phase 7" are technically correct in terms of sequence, but the foundations (Phase 2, 3, 5) are much thinner than documented.*
