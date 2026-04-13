# Vitruvius Master Roadmap (Comprehensive & Upgraded)

## 1. Vision and Strategy

### 1.1 Long-term Vision
Vitruvius is a high-discipline, local-first knowledge engine designed to transform heterogeneous domain sources (legal, technical, regulatory) into a validated, queryable knowledge graph. It moves beyond simple "RAG" by enforcing a strict layer of governance between raw text and canonical truth.

### 1.2 Multi-Layer Verification Model
No knowledge enters the "Canonical" layer without passing through:
1.  **Deterministic Matching:** Rules-based classification.
2.  **LLM Review:** Semantic validation via local LLMs.
3.  **Governance Validation:** Final schema and type-safety checks (Promotion Layer).

### 1.3 Strategic Principle: Building from the Bottom Up
1. Ingestion & Structure (Ground Truth)
2. Normalization & Canonicalization (Identity)
3. Candidate Extraction (Signals)
4. Validation & Promotion (**Governance Gate**)
5. Graph Contract & Indexing (Relationships)
6. Query & AI Augmentation (Intelligence)

---

## 2. Core System Governance (The "Upgraded" Layers)

### 2.1 Relationship Governance
To prevent graph chaos, all relationships must conform to the **Relationship Type Registry**:
*   **Allowed Types:** `governs`, `requires`, `defines`, `depends_on`, `limits`, `affects`, `supersedes`.
*   **Compatibility Rules:**
    *   `governs`: [Source] -> [Concept]
    *   `requires`: [Concept] -> [Concept] | [Concept] -> [Attribute]
    *   `defines`: [Source] -> [Concept]
    *   `limits`: [Source/Section] -> [Concept/Attribute]

### 2.2 Promotion Governance
The Promotion Layer is the terminal gatekeeper. It enforces:
*   **Schema Enforcement:** Every record must contain `source_section_id`, `evidence_snippet`, and `confidence_score`.
*   **Audit Trail:** Every promotion batch generates a `promotion_audit.log`.
*   **Merge Logic:** Duplicate triplets `(subject, type, object)` result in evidence merging rather than record duplication.

### 2.3 Graph Contract
Before any graph database implementation, all components must adhere to the **Filesystem Graph Contract**:
*   **Required Node Fields:** `id`, `type`, `slug`, `trust_level`, `last_updated_utc`.
*   **Required Edge Fields:** `from_id`, `to_id`, `type`, `evidence_id`, `status` (verified/unverified).

---

## 3. Phase Breakdown

### Phase 0. Repository and Pipeline Foundation
*   **Objective:** Establish the core infrastructure and workflow skeleton.
*   **Deliverables:**
    *   Layered Root Structure (001-006).
    *   `pipeline_cli.py` orchestrator.
    *   `paths.py` & `constants.py` filesystem contract.
*   **Status:** **COMPLETE**

### Phase 1. Ingestion and Extraction Foundation
*   **Phase 1A. Baseline Ingestion:**
    *   Support for PDF (OpenDataLoader), Office (LibreOffice), and Spreadsheets.
    *   OCR pathway (OCRmyPDF) for scanned documents.
    *   **Status:** **COMPLETE**
*   **Phase 1B. Multi-parser Integration:**
    *   **Objective:** Reduce upstream noise by selecting the best parser per document type.
    *   **Status:** **PLANNED (High Priority)**
*   **Phase 1C. Centralized Normalization:**
    *   **Objective:** Centralize fragmented cleanup logic into a formal "Text Refinement" layer.
    *   **Status:** **PLANNED (High Priority)**

### Phase 2. Canonicalization Engine
*   **Phase 2A & 2B. Plan & Generation:**
    *   Generate source files with stable IDs and basic frontmatter.
    *   **Status:** **COMPLETE**
*   **Phase 2C. Rules-Driven System:**
    *   Move domain logic to `canonical_rules.yaml`.
    *   **Status:** **COMPLETE**
*   **Phase 2D. ID Standard Enforcement:**
    *   Implementation of the `<prefix>-<slug>` pattern.
    *   **Status:** **COMPLETE**

### Phase 3. Concept Layer
*   **Phase 3A & 3B. Generation & Seeding:**
    *   Creation of `concept-*` files for the PD 1096 domain.
    *   **Status:** **COMPLETE (20+ concepts seeded)**
*   **Phase 3C. Concept Enrichment:**
    *   **Objective:** Transition from skeletons to "Knowledge Nodes" with definitions and regulatory basis.
    *   **Status:** **IN PROGRESS**

### Phase 4. Identity Cleanup and Migration
*   **Objective:** Align legacy IDs with the new strict naming convention.
*   **Status:** **COMPLETE**

### Phase 5. Relationship Extraction
*   **Phase 5D. Section-Aware Extraction:**
    *   Extracting relationships within section boundaries to preserve evidence context.
    *   **Validation:** Every candidate MUST have a `source_section_id`.
    *   **Status:** **COMPLETE**

### Phase 6. Review and Validation Layer
*   **Phase 6A. Local LLM Review:**
    *   Ollama + Gemma 4 31B integration.
    *   CLI: `review-relationships-ollama` command.
    *   Produces `keep`/`reject`/`review_further` decisions with confidence scoring.
    *   **Status:** **COMPLETE** ✅ (Audited 2026-04-13)
*   **Phase 6B. Second-Pass Review (Two-Stage Adjudication):**
    *   **Objective:** Cross-model validation for low-confidence candidates to minimize false consensus and reduce compute/latency.
    *   **Architecture:**
        *   **Tier 1 (Gemma4:31b):** Primary reviewer for all extracted candidates. High-confidence `keep` (>= 0.90) and `reject` (>= 0.90) are accepted provisionally/suppressed.
        *   **Tier 2 (Qwen3:30b or smaller):** Second-pass reviewer only for `review_further`, low-confidence `keep`/`reject`, and relationship type discrepancies.
        *   **Tier 3 (Human Review):** Escalation for Gemma/Qwen disagreements, high-impact legal relationships, and persistent ambiguity.
    *   **Deliverables:**
        *   CLI: `review-relationships-ollama-second-pass` command.
        *   Filters Gemma review report for low-confidence/`review_further` cases.
        *   Produces a merged adjudication report.
    *   **Status:** **PLANNED (Near-term Priority)**

### Phase 7. Promotion Governance
*   **Objective:** Execute the transfer of reviewed data into the Canonical Layer.
*   **Deliverables:**
    *   `run_promote` module to read `latest_relationship_review_ollama.json`.
    *   Auto-promote `keep` with confidence >= 0.90.
    *   Relationship Registry validator.
    *   Canonical Relationship Files in `003/shared/relationships/`.
*   **Status:** **NOT IMPLEMENTED** (Highest Priority Next)
*   **Prerequisite:** Review Layer (Phase 6A) complete ✅

### Phase 8. Graph Contract & Indexing
*   **Objective:** Build the first queryable index based on the Graph Contract.
*   **Deliverables:**
    *   Filesystem-backed graph indices.
    *   JSON graph artifacts.
    *   Graph traversal support.
*   **Status:** **NOT IMPLEMENTED** (Phase 7 prerequisite)

### Phase 9. Query & AI Layer
*   **Objective:** Enable high-fidelity domain queries ("What governs X?", "Which sections affect building permits?").
*   **Deliverables:**
    *   Structured query interface.
    *   Source traceability.
    *   Confidence-aware answers.
*   **Status:** **NOT IMPLEMENTED**

### Phase 10. Canonical Relationship Storage
*   **Objective:** Store approved relationships as part of the actual knowledge system.
*   **Deliverables:**
    *   Relationship records in `003/shared/relationships/`.
    *   Source-to-concept linkage.
    *   Concept-to-concept linkage.
*   **Status:** **NOT IMPLEMENTED**

### Phase 11. Dataset Expansion
*   **Objective:** Move beyond PD 1096 into broader architectural/legal corpus.
*   **Deliverables:**
    *   PD 1096 IRR support.
    *   Occupancy tables.
    *   Lighting and ventilation sections.
    *   Additional laws and regulations.
*   **Prerequisites:** Multi-parser integration, normalization, promotion layer.
*   **Status:** **NOT IMPLEMENTED**

### Phase 12. AI-Augmented Reasoning (Optional/Long-term)
*   **Objective:** Use AI on top of a structured graph, not on raw text chaos.
*   **Deliverables:**
    *   Concept enrichment via AI.
    *   Semantic linking.
    *   Question generation.
    *   Wiki article assistance.
    *   Learning path generation.
*   **Principle:** AI should sit on top of a structured deterministic base, not replace it.
*   **Status:** **NOT IMPLEMENTED**

---

## 4. Current System Position
*   **Vision Scale:** 50% Complete.
*   **Pipeline Scale:** 60% Complete.
*   **Current State:** Review layer (Phase 6A) audited and verified complete. Next: Promotion Layer (Phase 7) to move approved relationships into canonical storage.
*   **Last Audit Completed:** Review Layer Audit (2026-04-13) - `ollama_review.py` verified working

---

## 5. Immediate Next Actions (STRICT ORDER)
1.  **Implement Promotion Layer (Phase 7):** Build `run_promote` to read `latest_relationship_review_ollama.json` and auto-promote `keep` with confidence >= 0.90.
2.  **Finalize Relationship Schema:** Create the YAML/JSON schema for files in `003/shared/relationships/`.
3.  **Initialize Registry:** Create `scripts/vitruvius/rules/relationship_registry.yaml`.
4.  **Execute Phase 1C:** Centralize normalization to fix the "82% rejection" noise issue.
5.  **Second-Pass Reviewer (Phase 6B):** Add cross-model validation for uncertain candidates (near-term).

---

## 6. Strategic Warnings
*   **No "Soft Output":** Do not accept any extraction that lacks a specific source section pointer.
*   **No "Schema-less Growth":** Do not add new laws until the Promotion Layer is validating existing PD 1096 data.
*   **Local First:** Maintain hardware independence; do not rely on cloud APIs for the core review loop.

---
**Timestamp:** 2026-04-13T14:15:00Z
**Last Audit:** Review Layer Audit completed 2026-04-13 (see `.ai/02_audits/review-layer-audit.md`)
**Owner:** Senior Systems Architect
