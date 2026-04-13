# ingestion-refinement-contract-v2.md

## 1. Definitions Section
*   **Artifact**: A physical file produced by the Ingestion Layer (1B) for consumption by the Refinement Layer (1C).
*   **Contract Violation**: Any deviation from the required schema, encoding, or file structure.
*   **Upstream Failure**: A state where Phase 1B provides invalid or incomplete inputs, triggering an immediate abort in Phase 1C.

## 2. Deterministic Rules Section

### 2.1 Required Artifacts
For every source document processed, Phase 1B MUST produce:
1.  `002_Raw-Conversion-Layer/converted/{top_category}/raw_markdown/{stem}.md`
2.  `002_Raw-Conversion-Layer/converted/{top_category}/sidecar_json/{stem}.json`

### 2.2 Mandatory Metadata Schema (sidecar_json)
The sidecar JSON MUST contain the following fields with their specified types:

| Field | Type | Description |
| :--- | :--- | :--- |
| `source_path` | `string` | Relative path to the raw source file. |
| `file_type` | `string` | `pdf`, `docx`, `xlsx`, `pptx`, or `csv`. |
| `document_class` | `string` | Must match one of the 9 formal taxonomy classes (e.g., `hybrid_pdf`). |
| `parser_id` | `string` | Unique identifier of the successful parser. |
| `confidence_score` | `float` | Parser-reported confidence [0.0 - 1.0]. |
| `pages_total` | `int` | Total pages in the source document. |
| `markdown_path` | `string` | Relative path to the generated MD file. |
| `versioning` | `object` | MUST include `parser_version`, `pipeline_version`, and `config_version`. |

### 2.3 Encoding & Formatting Guarantees
*   **Encoding**: All artifacts MUST be encoded in `UTF-8` WITHOUT Byte Order Mark (BOM).
*   **Null Bytes**: Artifacts MUST NOT contain null bytes (`\x00`).
*   **Markdown Structure**: Headings MUST use ATX style (`#`, `##`). Setext style is PROHIBITED.
*   **JSON Structure**: MUST be valid, parseable JSON. Markdown code fences inside the JSON values MUST be escaped.

## 3. Failure Handling Section

### 3.1 Failure Codes
Phase 1B MUST report one of these codes in the registry if Success is not achieved:
*   `PARSER_FAILURE`: Process crashed or exited non-zero.
*   `VALIDATION_FAILURE`: Failed a Quality Gate (e.g., page coverage < 95%).
*   `TIMEOUT`: Process exceeded maximum allowed runtime.
*   `ENCODING_ERROR`: Parser produced non-UTF-8 content.
*   `STRUCTURE_LOSS`: Parser failed to detect any headings or structural markers.

### 3.2 Handoff Abort Logic
Phase 1C MUST validate this contract before initialization. If any field is missing or any file path is invalid:
1.  **Stop**: Phase 1C MUST NOT attempt to read or refine the Markdown.
2.  **Report**: Log `CONTRACT_VIOLATION` to the system manifest.
3.  **Status**: Mark the document as `UPSTREAM_INVALID`.

## 4. Validation Requirements
*   **Handoff Check**: A schema validator (e.g., Pydantic or JSON Schema) MUST be used by Phase 1C to verify the sidecar JSON.
*   **Completeness Check**: Phase 1C MUST verify that the character count of the `.md` file matches the `markdown_length` reported in the sidecar metadata ±5%.

## 5. Metrics Classification

### 5.1 Gating Metrics
*   `contract_compliance_rate`: % of handoffs that pass Phase 1C schema validation.
*   `artifact_integrity_failure_count`: Hard count of missing or corrupted `.md` files.

### 5.2 Observability Metrics
*   `mean_confidence_score_handoff`: Average confidence of documents entering refinement.
*   `taxonomy_distribution_handoff`: Count of documents per class entering Phase 1C.

## 6. Explicit Non-Goals
*   This contract does NOT govern the accuracy of the extracted text (handled by Phase 1B Quality Gates).
*   This contract does NOT govern the "cleanliness" of the text (handled by Phase 1C Normalization Rules).

## 7. Versioning Strategy
*   This contract is versioned independently. The current version is `v2.0.0`.
*   Both Phase 1B and 1C MUST report compliance with `contract_version: 2.0.0`.

## 8. Enforcement Rules
1.  **Zero Guessing**: If a required metadata field is missing, the document is INVALID. No default values are permitted.
2.  **No Partial Handoff**: Both the `.md` and `.json` must exist and be valid.
3.  **Strict UTF-8**: Any non-UTF-8 character in the Markdown body triggers an immediate `ENCODING_ERROR` and aborts the handoff.
