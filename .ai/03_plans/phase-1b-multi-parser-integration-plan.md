# Phase 1B: Multi-parser Integration Implementation Plan (Combined) <!-- updated: 2026-04-13 -->

## 1. Executive Summary
The Vitruvius Knowledge Engine currently relies on siloed scripts with hardcoded selection logic, leading to "upstream noise" and lack of fallback. Phase 1B establishes a high-fidelity, deterministic, and self-correcting ingestion pipeline with explicit governance over failure modes and output quality.

## 2. Definitions
*   **Text Density**: Ratio of alphanumeric characters to estimated visual area (chars / (width * height)).
*   **Image Density**: Ratio of image area to total page area.
*   **Vector Density**: Count of vector path objects per page.
*   **Quality Gate**: Mandatory validation check for "SUCCESS" status.
*   **Fallback Chain**: Ordered list of parsers attempted until a Quality Gate is satisfied.
*   **Document Taxonomy**: Formal classification system based on measurable file features.

## 3. Problem Diagnosis
*   **Parser Selection Gap**: No strategy for Hybrid or Malformed PDFs.
*   **Lack of Governance**: Selection is hardcoded, not configured.
*   **Upstream Noise**: Prioritization of speed over quality for complex docs.
*   **Operational Blindness**: Lack of standardized telemetry.

## 4. Document Taxonomy & Classification Rubric
Classification MUST be determined by measurable signals in this priority order: `scanned > hybrid > complex > simple`.

### 4.1 Feature Extraction Signals
```text
text_density = extracted_text_chars / page_area_estimate
image_density = total_image_area / page_area
vector_density = vector_object_count / page
ocr_confidence = average OCR confidence (if applicable)
table_clues = frequency of grid-like alignment or delimiters
garbled_ratio = non-printable or invalid unicode / total chars
```

### 4.2 Classification Rules
| Rule ID | Condition | Class |
| :--- | :--- | :--- |
| CL-001 | `extension == .docx` | `office_doc` |
| CL-002 | `extension == .pptx` | `office_slide` |
| CL-003 | `extension IN (.xlsx, .csv)` | `spreadsheet_structured` (if first 5 rows have > 80% non-empty columns) ELSE `spreadsheet_unstructured` |
| CL-004 | `ocr_confidence < 0.85` OR `garbled_ratio >= 0.05` | `scanned_pdf_noisy` |
| CL-005 | `ocr_confidence >= 0.85` AND `garbled_ratio < 0.05` | `scanned_pdf_clean` |
| CL-006 | `text_density` [0.3, 0.7] AND `image_density >= 0.2` | `hybrid_pdf` |
| CL-007 | `text_density > 0.6` AND (`table_clues >= 0.2` OR `vector_density >= 0.2`) | `text_pdf_complex` |
| CL-008 | `text_density > 0.85` AND `table_clues < 0.1` AND `image_density < 0.1` | `text_pdf_simple` |

## 5. Parser Chain Strategy
The Orchestrator MUST invoke the chain associated with the detected class. Higher-fidelity parsers (Docling/Marker) MUST precede faster baselines (OpenDataLoader) in complex chains.

| Class | Parser Chain (Priority Order) |
| :--- | :--- |
| `text_pdf_simple` | `[opendataloader]` |
| `text_pdf_complex` | `[docling, marker, opendataloader]` |
| `scanned_pdf_clean` | `[ocr_preprocessor, marker]` |
| `scanned_pdf_noisy` | `[ocr_preprocessor, surya, marker]` |
| `hybrid_pdf` | `[docling, marker]` |
| `office_doc` | `[libreoffice_preprocessor, docling]` |
| `spreadsheet_unstructured` | `[spreadsheet_parser]` |

## 6. Strict Parser Telemetry Contract
Every parser execution MUST emit this exact JSON structure:
```json
{
  "parser_id": "string",
  "attempt_index": "int",
  "attempt_duration_ms": "int",
  "pages_total": "int",
  "pages_processed": "int",
  "page_coverage_ratio": "float",
  "raw_text_length": "int",
  "markdown_length": "int",
  "header_count": "int",
  "table_count": "int",
  "image_count": "int",
  "diagram_captions_extracted": "int",
  "ocr_applied": "bool",
  "confidence_score": "float",
  "validation_passed": "bool",
  "failure_reason": "string|null"
}
```
❗ **Spatial Context**: If an image is detected, the parser MUST attempt to bind the nearest textual bounding box as its caption to preserve context in the resulting Markdown.

## 7. Failure Handling & Fallback Policy
### 7.1 Fallback Triggers
Fallback MUST trigger if any condition occurs:
1.  **Technical Failure**: Process exit code != 0.
2.  **Gate Failure**: `validation_passed == false`.
3.  **Timeout**: `attempt_duration_ms > 120,000ms`.
4.  **Coverage Drop**: `page_coverage_ratio < 0.95`.
5.  **Low Confidence**: `confidence_score < 0.70`.
6.  **Garbled Rate**: `garbled_ratio >= 0.05`.
7.  **Hallucination Trap**: Ratio of dictionary-valid words < 0.40 in extracted text (catch confident gibberish).

### 7.2 Terminal States
If the fallback chain is exhausted without success:
1.  Status MUST be set to `FALLBACK_EXHAUSTED`.
2.  `manual_review_required` MUST be set to `true`.
3.  No downstream processing (Phase 1C) is permitted.

## 8. Validation Requirements (Quality Gates)
*   **Gate-001 (Integrity)**: Markdown is well-formed UTF-8.
*   **Gate-002 (Volume)**: `markdown_length >= 500` chars (or 10% of raw text).
*   **Gate-003 (Structure)**: At least one `#` or `##` header if `pages_total > 5`.
*   **Gate-004 (Office/Sanity)**: Post-conversion page count matches source ±1; non-empty text presence.

## 9. Metrics & Observability
### 9.1 Gating Metrics (Block Pipeline)
*   `validation_failure_rate`: % of files hitting `FALLBACK_EXHAUSTED`.
*   `timeout_rate`: % of processes terminated by orchestrator.
*   `encoding_error_count`: Hard count of non-UTF-8 outputs.

### 9.2 Observability Metrics
*   `parser_preference_distribution`: Success rates per parser in chain.
*   `average_confidence_per_class`: System accuracy trends.
*   `page_coverage_mean`: Reconstruction quality.

## 10. Document Type Specialization
### 10.1 Spreadsheet Handling
*   **Sheet Extraction**: All sheets to separate Refined MD sections.
*   **Header Detection**: Row-density and type-consistency logic.
*   **Merged Cells**: Flattened to preserve relational context.
*   **Formulas**: Preserved in JSON sidecar; evaluated for Markdown.

## 11. Implementation Plan
### Phase 1: Foundation
1. Define `BaseParser` and `ParserOrchestrator` with quality gates.
2. Implement `document_taxonomy` classification logic.
3. Wrap existing `opendataloader` and `spreadsheets.py`.

### Phase 2: Modernization
1. Implement `DoclingParser` and `MarkerParser`.
2. Integrate `OCRPreprocessor` and `Surya`.
3. Implement post-LibreOffice quality gates.

### Phase 3: Scaling & Governance
1. Implement `ProcessPoolExecutor` with **Dynamic Resource Allocation**:
    - `text_pdf_simple`: 4GB RAM per process.
    - `text_pdf_complex`/`hybrid_pdf`: Routed to high-memory queue (8GB+) to prevent OOM kills.
    - `max_runtime_per_parser`: 120s.
2. Create **Golden Corpus Benchmark** (10 simple, 10 complex, 10 scanned, etc.).
3. Build expanded registry and per-file sidecar metadata.

## 12. Manual Review Lane
Final states: `AUTO_ACCEPTED`, `AUTO_REFINED`, `FALLBACK_EXHAUSTED`, `MANUAL_REVIEW_REQUIRED`.

## 13. Non-Negotiable System Principles
*   **No silent failure**: Every fallback logged with `failure_reason`.
*   **No implicit transformation**: Transformations must be declared and traceable.
*   **Strict Contract**: Phase 1C MUST reject any file missing telemetry JSON.
*   **Deterministic Classification**: FIXED thresholds (0.85, 0.6, etc.).
*   **Provenance**: Every file has `sidecar.json` with `parser_provenance`.

## 14. Explicit Non-Goals
*   Semantic summarization or legal interpretation.
*   Graph relationship extraction (Phase 1D).
*   Manual correction of source metadata errors.

## 15. Versioning Strategy
*   **Parser Versioning**: Report library version (e.g. `docling==1.2.0`).
*   **Config Versioning**: `config/vitruvius.yaml` includes `schema_version`.
*   **Pipeline Versioning**: Orchestrator version injected into registry.

---
**Changelog**: Combined v1 and v2 on 2026-04-13 for a unified high-fidelity ingestion plan.
