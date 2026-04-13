# Vitruvius — Pipeline Overview

## Purpose
This document provides a code-grounded overview of the Vitruvius execution pipeline. It traces the data lifecycle from raw document ingestion through transformation, canonicalization, and relationship extraction to final review and output.

## Scope
The scope of this document is limited to the executable stages defined in `scripts/pipeline_cli.py` and implemented within the `scripts/vitruvius/` package.

## Pipeline Summary
The Vitruvius pipeline is a **sequential, file-driven workflow** that uses the filesystem as its primary state-tracking mechanism. It progresses through discovery, conversion, normalization into a canonical knowledge layer, and automated extraction of legal relationships.

## Entry Points
- **Main Entry Point:** `scripts/pipeline_cli.py`
  - This script acts as the primary orchestrator, dispatching commands to specific modules.
- **Key Commands:**
  - `run`: Executes the default baseline (Scan → Status → Lint).
  - `convert`: Batch processes new or changed files into Markdown/JSON.
  - `canonicalize-one`: Refines a specific converted file into the Canonical Knowledge Layer.
  - `extract-relationships-one`: Runs pattern-based extraction on a canonical source.
  - `review-relationships-ollama`: Performs LLM-based verification of extracted relationships.

## End-to-End Execution Flow
1.  **Ingestion (`run_scan`)**: Crawls `001_Raw-Source-Layer` to build a file registry.
2.  **State Analysis (`run_status`)**: Compares current scan against previous to find new/changed files.
3.  **Validation (`run_lint`)**: Checks for naming collisions and unsupported formats.
4.  **Transformation (`run_convert`)**:
    - Converts PDFs, Office, and Spreadsheets to Markdown.
    - Routes scanned PDFs to OCR if needed.
5.  **Reconciliation (`run_reconcile`)**: Identifies and flags stale or orphaned artifacts.
6.  **Canonicalization (`run_canonicalize_one`)**: Maps raw markdown to a strict ID and frontmatter schema in `003`.
7.  **Extraction (`run_extract_relationships_one`)**: Identifies legal links using regex patterns.
8.  **Review (`run_review_relationships_ollama`)**: Validates extractions using a local LLM.

## Stage Breakdown

### 1. Ingestion Stage
- **Module:** `scanner.py`
- **Action:** `rglob("*")` on `001_Raw-Source-Layer`.
- **Artifact:** `latest_raw_file_registry.csv` in `006/registries`.

### 2. Status & Lint Stage
- **Modules:** `status.py`, `linting.py`.
- **Action:** Identifies `new`, `changed`, or `missing` files.
- **Artifact:** `latest_status_report.json`, `latest_lint_report.json` in `006/runs`.

### 3. Conversion Stage (Multi-Route)
- **Module:** `conversion.py`.
- **Action:** 
  - **Route A (Text PDF):** `opendataloader_pdf`.
  - **Route B (Office):** `office.py` → PDF → `opendataloader_pdf`.
  - **Route C (Scanned PDF):** `ocr.py` (OCRmyPDF) → PDF → `opendataloader_pdf`.
  - **Route D (Spreadsheet):** `spreadsheets.py` → CSV/JSON.
- **Artifacts:** `.md` and `.json` in `002_Raw-Conversion-Layer`.

### 4. Canonicalization Stage
- **Modules:** `canonicalize.py`, `concepts.py`.
- **Action:** Applies rules from `canonical_rules.yaml`. Assigns IDs like `law-pd-1096`.
- **Artifact:** YAML-frontmatter Markdown files in `003_Canonical-Knowledge-Layer`.

### 5. Extraction Stage
- **Modules:** `relationships.py`, `relationships_sections.py`.
- **Action:** Pattern matching against concepts defined in `003/shared/concepts`.
- **Artifact:** `latest_relationship_extraction.json` in `006/runs`.

### 6. Review Stage
- **Module:** `ollama_review.py`.
- **Action:** Sends relationship candidates to Ollama (`gemma4:31b`) for `keep`/`reject` decision.
- **Artifact:** `latest_relationship_review_ollama.json` in `006/runs`.

## Stage Status (Implemented vs Missing)
| Stage | Status | Notes |
| :--- | :--- | :--- |
| Ingestion | IMPLEMENTED | File-registry based. |
| Status | IMPLEMENTED | Registry comparison logic. |
| Linting | IMPLEMENTED | Filename and extension checks. |
| Conversion | IMPLEMENTED | PDF, Office, Spreadsheet, and OCR routes. |
| Normalization | PARTIAL | Currently handled during Canonicalization. |
| Canonicalization | IMPLEMENTED | Strict ID system with rules engine. |
| Concept Generation | PARTIAL | Single-concept creation implemented. |
| Relationship Extraction | IMPLEMENTED | Regex pattern matching. |
| Review | IMPLEMENTED | Local LLM integration (Ollama). |
| Promotion | NOT IMPLEMENTED | Moving from `draft` to `verified` is manual. |
| Storage (Graph) | NOT IMPLEMENTED | Planned for Layer 005. |

## Data Flow
`Raw Source (.pdf/.docx)` → `Markdown (.md)` → `Canonical Markdown (ID/YAML)` → `Extraction JSON` → `Verified JSON`

## Artifact Generation
- **Operational:** CSV registries and JSON status reports in `006_System-Manifests`.
- **Knowledge:** Markdown files in `002` (raw) and `003` (canonical).
- **Execution:** Timestamped JSON/TXT reports in `006_System-Manifests/runs`.

## Module Mapping
- `pipeline_cli.py` → Orchestrator.
- `paths.py` → Path resolution logic (Contract).
- `constants.py` → System-wide directory and file names.
- `reports.py` → CSV/JSON/Text writing utilities.

## Current Limitations
- **Linearity:** The pipeline is mostly linear; branched processing is handled via manual CLI routing.
- **LLM Dependency:** Review stage requires active Ollama server.
- **State Persistence:** Entirely filesystem-based; no database for querying across files.

## Missing Stages
- **Automated Promotion:** No automated workflow to promote artifacts from conversion to canonical without manual ID verification.
- **Graph Ingestion:** No automatic sync to a graph database (e.g., Neo4j).

## Performance Risks
- **OCR:** Processing large scanned PDFs is slow and CPU-intensive.
- **LLM Review:** Reviewing thousands of relationship candidates via Ollama takes significant time.
- **Registry Size:** As the number of files in `001` grows, CSV-based registry comparisons will slow down.

## Changelog
- **2026-04-13:** Initial Pipeline Overview document created from codebase audit. Traced all `run_` commands and artifact flows.
