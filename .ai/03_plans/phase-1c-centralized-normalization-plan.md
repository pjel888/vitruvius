# Phase 1C: Centralized Normalization Implementation Plan (Combined) <!-- updated: 2026-04-13 -->

## 1. Executive Summary
The Vitruvius Knowledge Engine currently suffers from fragmentation in text and data normalization across multiple modules. Phase 1C centralizes all text refinement into a formal **Text Refinement Layer** (between Parser Output 1B and Canonicalization 1D) with strict governance over rule safety, execution order, and scope boundaries.

## 2. Definitions
*   **Text Refinement Layer**: Dedicated system sitting between Parser Output (1B) and Canonicalization (1D).
*   **Normalization Rule**: A deterministic function mapping an input string to a "cleaner" output.
*   **Semantic Chunking**: The process of injecting `section_depth` or `semantic_block` markers to ensure structural fidelity for downstream RAG.
*   **Rule Tier**: Classification of risk (A: Lossless, B: Structural, C: Semantic).
*   **Rule Phase**: Specific step in the 5-phase execution sequence.
*   **Rule Scope**: Authorized data field for a rule (e.g., `document_text`, `identifier`).
*   **Idempotency**: Property where `normalize(normalize(x)) == normalize(x)`.

## 3. Current System Audit
| Normalization Logic | File Path | Function Name | Issue |
| :--- | :--- | :--- | :--- |
| Filename | `utils.py` | `normalize_filename` | Brittle alphanumeric only. |
| Basic Whitespace | `utils.py` | `normalize_text` | Inconsistent with extractor. |
| Slugification | `canonicalize.py` | `slugify` | Duplicated in 3 modules. |
| JSON Blocks | `ollama_review.py` | `parse_model_json` | Brittle fence stripping. |

## 4. Rule Classification System (Safety Tiers)
| Tier | Category | Description | Enforcement |
| :--- | :--- | :--- | :--- |
| **Tier A** | Lossless | Unicode NFC, control char removal, basic space collapse. | Always ON. |
| **Tier B** | Structural | Standardizes formatting (e.g., `SEC. 1` -> `SECTION 1`). | Always ON for Markdown. |
| **Tier C** | Semantic | Corrects common OCR typos or legal terminology drift. | OPT-IN ONLY; requires isolation to 'LLM Review Layer' or Human-in-the-loop audit. Log original alongside mutation. |

## 5. Execution Phases (Phase-Locked)
Rules MUST execute in this exact sequence. Phase N+1 rules MUST NOT be applied before Phase N is complete.

1.  **Phase 1 (Encoding)**: UTF-8 enforcement and Unicode NFC normalization.
2.  **Phase 2 (Whitespace)**: Trimming, collapse of multi-spaces, and line-ending normalization.
3.  **Phase 3 (Structural)**: Markdown header standardization, section marker fixing, and **Semantic Chunking** (injection of `section_depth` and `semantic_block` markers).
4.  **Phase 4 (Identifiers)**: Slug generation and filename sanitization.
5.  **Phase 5 (Data Cleanup)**: JSON stripping and Markdown code fence removal.

## 6. Scope Routing & Boundaries
Rules are restricted to specific data scopes. Attempting to apply a rule to an unauthorized scope MUST raise an `AuthorizationError`.
*   `document_text`: Markdown body.
*   `identifier`: Canonical IDs and slugs.
*   `filename`: Filesystem paths.
*   `sheet_name`: Specific to spreadsheet processing.
*   `llm_json_payload`: Raw strings from LLM responses.
*   `metadata_fields`: YAML frontmatter or sidecar keys.

## 7. Normalization Engine Design
```python
class NormalizationRule(Protocol):
    name: str
    tier: Literal["A", "B", "C"]
    phase: int  # 1-5
    scope: List[str]
    is_deterministic: bool
    
    def apply(self, text: str) -> str: ...
```
The engine enforces phase-locked execution and scope-based routing for every input component.

## 8. Canonical ID Stability & Collision Policy
Slug generation MUST be deterministic, order-independent, and collision-resistant.
*   **Collision Handling**: If `slugify(text)` exists, use `base_slug + "--" + short_hash(source_path)`.
*   **Prohibition**: Incremental numbering (`-1`, `-2`) is PROHIBITED.
*   **Alias Registry**: Maintain a mapping (e.g., `pd-1096` -> `national-building-code`) for lookup, not rewriting. Population via manual maintenance AND auto-extraction from common document headers (e.g., "Also known as...", "Abbreviated as...").
*   **Null/Empty Titles**: Fallback to source hash or timestamp.

## 9. Near-Duplicate Policy
Normalization MUST NOT merge or rewrite near-duplicates.
*   Detect similarity (Levenshtein or cosine).
*   Flag as `possible_duplicate` in the manifest.
*   Defer resolution to Phase 1D.

## 10. Failure Handling & Contract Enforcement
### 10.1 Cross-Phase Contract Enforcement
Validate Phase 1B outputs before processing:
1.  **Input Check**: Verify presence of `.md` and `.json` sidecar.
2.  **Schema Check**: Verify JSON contains `parser_id`, `pages`, and `confidence_score`.
3.  **Action**: If check fails, set status to `UPSTREAM_INVALID` and ABORT.

### 10.2 Destructive Transformation Guard
If a rule reduces character count by > **Dynamic Threshold**:
1.  **Thresholds**: `text_pdf_simple` (10%), `text_pdf_complex` (15%), `scanned_pdf_noisy` (30%).
2.  Roll back the transformation if threshold exceeded.
3.  Flag the file as `MANUAL_REVIEW_REQUIRED`.
4.  Log a `severity: high` audit event.

## 11. Validation Requirements
*   **Idempotency**: `normalize(normalize(x)) == normalize(x)`. All Tier A/B rules MUST pass this.
*   **Stability**: Slug generation MUST be deterministic across runs.
*   **Markdown Integrity**: Rules MUST NOT break table syntax (`|`) or list markers.
*   **Table Isolation Protocol**: Temporarily tokenize Markdown tables during Phase 2 (Whitespace) to prevent structural collapse from aggressive trailing space removal. Re-inject tables post-whitespace cleanup.

## 12. Metrics & Observability
### 12.1 Gating Metrics (Block Pipeline)
*   `idempotency_failure_rate`: Count of rules failing the double-run test.
*   `contract_violation_rate`: Count of Phase 1B handoff failures.
*   `structural_corruption_count`: Detected breaks in Markdown tables/lists.
*   `encoding_failure_rate`: Hard count of non-UTF-8 outputs.

### 12.2 Observability Metrics
*   `normalization_rate_per_rule`: Frequency of application.
*   `text_diff_percentage_mean`: Magnitude of cleanup per document class.
*   `collision_resolution_count`: Frequency of hash-based slug deduplication.

## 13. Implementation Plan
### Phase 1: Core Engine & Safety Tiers
1. Implement `NormalizationEngine` with tier-based rule management.
2. Build initial Tier A rules (Unicode, control chars).
3. Implement Transformation Traceability (audit logs).

### Phase 2: Refactoring & Unification
1. Replace scattered slugification logic with the new engine.
2. Implement ID Collision Policy and Alias Registry.
3. Update `pipeline_cli.py` to support the `refine` stage.

### Phase 3: Manifests & Validation
1. Build per-file Refinement Manifest sidecar system.
2. Create **Golden Set Validation** (using Phase 1B corpus).

## 14. Manual Review Lane
Final states: `AUTO_ACCEPTED`, `AUTO_REFINED`, `UPSTREAM_INVALID`, `MANUAL_REVIEW_REQUIRED`.

## 15. Non-Negotiable System Principles
*   **No silent transformation**: Every mutation MUST emit a `TransformationEvent` with snapshots.
*   **No implicit transformation**: Transformations must be declared and traceable.
*   **Strict Contract**: Phase 1C MUST reject any file missing telemetry JSON from 1B.
*   **Deterministic Outputs**: Identical files must produce identical IDs and structures.
*   **Provenance**: Every file has a `.refined.json` manifest detailing rules applied.

## 16. Explicit Non-Goals
*   Semantic rewrite or summarization.
*   Entity extraction (Phase 1D).
*   Correction of factual errors in source laws.

## 17. Versioning Strategy
*   **Rule Engine Version**: SemVer for the `NormalizationEngine` core.
*   **Rule Versioning**: Individual rules MUST be versioned (e.g., `CollapseWhitespace v1.2`).
*   **Config Versioning**: `config/vitruvius.yaml` includes `schema_version`.

---
**Changelog**: Combined v1 and v2 on 2026-04-13 for a centralized high-fidelity normalization plan.
