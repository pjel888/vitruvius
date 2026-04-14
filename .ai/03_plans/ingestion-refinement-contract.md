---
plan_id: contract-ingestion-refinement
phase: "1B↔1C"
title: Ingestion → Refinement Handoff Contract
status: frozen
priority: high
sprint: "N/A — contract frozen for both sides"
version: 2.0.0
plan_type: contract
created: 2026-04-13
last_updated: 2026-04-14
owner: Senior Systems Architect
prerequisites: []
dependencies:
  - .ai/01_roadmap/master-roadmap.md §3.2
related_plans:
  - phase-1b-multi-parser-integration-plan.md (producer side)
  - phase-1c-centralized-normalization-plan.md (consumer side)
contract_version: 2.0.0
---

# Ingestion-Refinement Contract (Combined) <!-- updated: 2026-04-14 -->

## 1. Purpose
This contract defines the strict, non-negotiable interface between Phase 1B (Ingestion/Parsing) and Phase 1C (Normalization/Refinement). It ensures structural fidelity and metadata consistency as documents move through the Vitruvius Knowledge Engine.

## 2. Definitions
*   **Artifact**: A physical file produced by the Ingestion Layer (1B) for consumption by the Refinement Layer (1C).
*   **Contract Violation**: Any deviation from the required schema, encoding, or file structure.
*   **Upstream Failure**: A state where Phase 1B provides invalid or incomplete inputs, triggering an immediate abort in Phase 1C.

## 3. Required Artifacts
For every source document processed, Phase 1B MUST produce the following artifacts in the `002_Raw-Conversion-Layer/converted/` directory:
1.  **Markdown**: `{top_category}/raw_markdown/{stem}.md`
2.  **Sidecar Metadata**: `{top_category}/sidecar_json/{stem}.json`

## 4. Mandatory Metadata Schema (sidecar_json)
The sidecar JSON MUST contain the following fields. Phase 1C MUST reject any document missing these keys.

| Field | Type | Description |
| :--- | :--- | :--- |
| `source_path` | `string` | Relative path to the raw source file. |
| `file_type` | `string` | `pdf`, `docx`, `xlsx`, `pptx`, or `csv`. |
| `document_class` | `string` | Must match one of the 9 formal taxonomy classes (e.g., `hybrid_pdf`). |
| `parser_id` | `string` | Unique identifier of the successful parser. |
| `confidence_score` | `float` | Parser-reported confidence [0.0 - 1.0]. |
| `pages_total` | `int` | Total pages in the source document. |
| `pages_processed` | `int` | Number of pages successfully processed by the parser. |
| `markdown_path` | `string` | Relative path to the generated MD file. |
| `assets_extracted` | `string[]` | Array of extracted source-asset URIs preserved strictly for provenance and downstream reference. No semantic interpretation is implied at handoff. |
| `structural_context` | `string[]` | Detected structural identifiers (e.g., "Section 804") for context preservation. |
| `versioning` | `object` | MUST include `parser_version`, `pipeline_version`, and `config_version`. |
| `manual_review` | `object` | MUST include `required` (bool) and `reason` (string|null). |

## 5. Encoding & Formatting Guarantees
*   **Encoding**: All artifacts MUST be encoded in `UTF-8` WITHOUT Byte Order Mark (BOM).
*   **Null Bytes**: Artifacts MUST NOT contain null bytes (`\x00`).
*   **Markdown Structure**: 
    - Headings MUST use ATX style (`#`, `##`). Setext style is PROHIBITED.
    - MUST preserve headings where detected.
    - MUST NOT contain binary artifacts or "mixed" encodings.
*   **JSON Structure**: 
    - MUST be valid, parseable JSON. 
    - Markdown code fences inside JSON values MUST be escaped.
    - MUST NOT contain raw markdown fences surrounding the JSON object.

## 6. Failure Handling & Abort Logic

### 6.1 Failure Codes
Phase 1B MUST report one of these codes if Success is not achieved:
*   `PARSER_FAILURE`: Process crashed or exited non-zero.
*   `VALIDATION_FAILURE`: Failed a Quality Gate (e.g., page coverage < 95%).
*   `TIMEOUT`: Process exceeded maximum allowed runtime.
*   `ENCODING_ERROR`: Parser produced non-UTF-8 content.
*   `STRUCTURE_LOSS`: Parser failed to detect any headings or structural markers.
*   `UPSTREAM_INVALID`: Catch-all for malformed source files that block parsing.

### 6.2 Handoff Abort Logic
Phase 1C MUST validate this contract before initialization. If any field is missing or any file path is invalid:
1.  **Stop**: Phase 1C MUST NOT attempt to read or refine the Markdown.
2.  **Report**: Log `CONTRACT_VIOLATION` to the system manifest.
3.  **Payload Enrichment**: If a failure occurs, the terminal state record MUST include `document_class` and `structural_context` to aid Ranger review.
4.  **Status**: Mark the document as `UPSTREAM_INVALID`.

## 7. Validation Requirements
*   **Handoff Check**: A schema validator (e.g., Pydantic or JSON Schema) MUST be used by Phase 1C to verify the sidecar JSON.
*   **Completeness Check**: Phase 1C MUST verify that the character count of the `.md` file matches the `markdown_length` reported in the sidecar metadata ±5% (if reported) or verify file existence and non-zero size.

## 8. Metrics Classification

### 8.1 Gating Metrics
*   `contract_compliance_rate`: % of handoffs that pass Phase 1C schema validation.
*   `artifact_integrity_failure_count`: Hard count of missing or corrupted artifacts.

### 8.2 Observability Metrics
*   `mean_confidence_score_handoff`: Average confidence of documents entering refinement.
*   `taxonomy_distribution_handoff`: Count of documents per class entering Phase 1C.

## 9. Versioning Strategy
*   This contract is versioned independently. The current version is `v2.0.0`.
*   Both Phase 1B and 1C MUST report compliance with `contract_version: 2.0.0`.

## 10. Enforcement Rules
1.  **Zero Guessing**: If a required metadata field is missing, the document is INVALID. No default values are permitted.
2.  **No Partial Handoff**: Both the `.md` and `.json` must exist and be valid.
3.  **Strict UTF-8**: Any non-UTF-8 character in the Markdown body triggers an immediate `ENCODING_ERROR` and aborts the handoff.
4.  **No Fallback**: Phase 1C MUST reject any input that does not meet this contract. No fallback or "soft" validation is allowed at this stage.

## 11. Explicit Non-Goals
*   Accuracy of extracted text (governed by Phase 1B Quality Gates).
*   Cleanliness of normalized text (governed by Phase 1C Normalization Rules).

---
**Changelog**: Combined original contract and v2 on 2026-04-13 for a unified high-fidelity interface specification.
