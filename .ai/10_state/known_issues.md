# Known Issues & Risks — Vitruvius

> **Updated:** 2026-04-14
> **Format:** `RI-###` (Risk Issue), severity, mitigation, and closure path.

## Open Risks

### RI-001: Filesystem Coupling
- **Description:** The system is tightly coupled to the directory structure defined in `paths.py` and `constants.py`.
- **Impact:** HIGH — renaming or moving `001_…` through `006_…` breaks the pipeline silently.
- **Mitigation:** All path logic stays in `paths.py`. Inline paths are rejected at code review. `run_reconcile` detects structural drift.
- **Closure:** Permanent operating rule. Not a phase.

### RI-002: Regex Extraction Fragility
- **Description:** `relationships.py` and `relationships_sections.py` match candidates via fixed regex patterns. Variations in legal language leak into false positives (82% rejection at review).
- **Impact:** MEDIUM — feeds the review layer with noise, inflating compute cost and review time.
- **Mitigation:** Phase 1C (normalization) reduces input variance. Phase 5E (LLM-assisted extraction) is planned but gated on Phase 6B to avoid multiplying noise.
- **Closure:** Addressed by Phase 1C (partial) and Phase 5E (full, long-term).

### RI-003: External Dependency — Ollama (PARTIALLY CLOSED 2026-04-14)
- **Description:** The review layer requires an Ollama server at `127.0.0.1:11434` with the configured model loaded. Previously the URL was hardcoded.
- **Impact:** MEDIUM — the review stage fails if Ollama is down or the model is not pulled.
- **Mitigation:** ✅ Sprint A · A-1 moved the URL into `config/vitruvius.yaml` (AD-009 implementation). Sprint B will add a pre-flight health check before batch start.
- **Status:** **PARTIALLY CLOSED.** Config migration done; pre-flight health check pending Sprint B.

### RI-004: Python Environment / PYTHONPATH
- **Description:** `scripts/vitruvius` is not a standard `src/` layout. CLI invocation requires specific working-directory context.
- **Impact:** LOW — new contributors need an onboarding note.
- **Mitigation:** Documented in `README.md`. Considered tolerable per **AD-002**.
- **Closure:** Not scheduled. Revisit if the codebase grows beyond CLI use.

### RI-005: Legacy Naming Inconsistencies
- **Description:** Scripts like `scripts/Word-PPT-To-PDF.py` and some early reports do not follow `naming-conventions.md`.
- **Impact:** LOW (aesthetic / consistency).
- **Mitigation:** Rename under a dedicated cleanup PR using `migrate-ids-plan` after Sprint C.
- **Closure:** Post-Sprint C cleanup pass.

### RI-006: Manual Promotion Gap (CLOSED 2026-04-14)
- **Description:** No automated bridge between the Review Layer (`latest_relationship_review_ollama.json`) and the Canonical Knowledge Layer.
- **Impact:** HIGH — blocks the entire downstream stack.
- **Mitigation:** ✅ Sprint A Phase 7 built the Promotion Layer: `pipeline_cli.py promote` reads `latest_relationship_review_high_confidence.json`, validates against 17 rules, and writes records to `003_Canonical-Knowledge-Layer/shared/relationships/` with full audit log.
- **Status:** **CLOSED.** First 3 PD 1096 relationships promoted on 2026-04-14. Idempotency and rollback verified.

### RI-007: Normalization Fragmentation
- **Description:** Whitespace collapsing, line merging, slugification, and JSON fence stripping are each duplicated across 2–3 modules (`utils.py`, `relationships_sections.py`, `canonicalize.py`, `ollama_review.py`). No central Text Refinement layer.
- **Impact:** MEDIUM — inconsistent data quality; makes advanced cleanup (noise removal, semantic chunking) impossible.
- **Mitigation:** Phase 1C builds the central `NormalizationEngine`.
- **Closure:** Sprint B (Phase 1C).

### RI-008: Registry Growth Without Rotation
- **Description:** `006_System-Manifests/registries/*.csv` appends indefinitely. No rotation or pruning.
- **Impact:** MEDIUM — unbounded CSV growth will slow comparison logic in `status.py` as corpus scales.
- **Mitigation:** Add `rotate-registries` CLI with a retention policy (e.g., keep 30 timestamped versions + always the latest).
- **Closure:** Post-Sprint C infrastructure cleanup.

### RI-009: No File Hashing in Ingestion
- **Description:** `scanner.py` captures size + mtime but no SHA-256. Change detection can miss content changes that preserve mtime.
- **Impact:** MEDIUM — Phase 1B telemetry contract expects `source_hash`, so this must close before 1B ships.
- **Mitigation:** Add SHA-256 computation in `scanner.build_file_entries`. Store in `latest_raw_file_registry.csv`.
- **Closure:** Sprint C as a prerequisite for Phase 1B.

### RI-010: Concept Generator Produces Placeholder Content
- **Description:** `concepts.py` writes "X is a defined concept within the Vitruvius system." as the body. No definition extraction, no regulatory linkage.
- **Impact:** MEDIUM — concepts look populated in the filesystem but carry no knowledge. Extraction uses them as vocabulary, so placeholder sprawl is safe structurally but semantically thin.
- **Mitigation:** Phase 3C (concept enrichment) replaces placeholders with extracted definitions.
- **Closure:** Phase 3C — starts after Phase 2 restoration.

### RI-011: Canonicalizer Regression
- **Description:** `canonicalize.py` generates YAML frontmatter + header only. The hand-curated canonical files under `003/shared/sources/` show a richer structure (Overview / Coverage / Key Points / Referenced Concepts) that the current script cannot reproduce.
- **Impact:** MEDIUM — running batch canonicalization against the existing set would flatten the richer hand-curated content. Treated as a **regression** from a tool that no longer exists in the repo.
- **Mitigation:** Add diff-before-write protection based on `canonical_status`. Restore structured-section generation in Phase 2.
- **Closure:** Sprint C — Phase 2 restoration.

### RI-012: Review Layer Not in Default Pipeline
- **Description:** `review-relationships-ollama` is a manual command. It is not part of `run` or any auto-chain after `extract-relationships-one`.
- **Impact:** MEDIUM — each run requires human initiation, breaking the "run then walk away" operator model.
- **Mitigation:** After Sprint A ships Phase 7, add an opt-in `run-with-review` pipeline mode.
- **Closure:** Sprint C.

## Risk Severity Summary (updated 2026-04-14)
| Severity | Count | IDs |
|---|---|---|
| HIGH | 1 (was 2) | RI-001 |
| MEDIUM | 8 (was 9) | RI-002, RI-003 (partial), RI-007, RI-008, RI-009, RI-010, RI-011, RI-012 |
| LOW | 1 | RI-004 |
| CLOSED | 1 | RI-006 ✅ |

*RI-005 is low-impact but MEDIUM-effort to close.*

## Closure Timeline
| Sprint | Risks Closing |
|---|---|
| **Sprint A (closed 2026-04-14)** | ✅ **RI-006** (full), ✅ **RI-003** (partial — config done, health check pending) |
| Sprint B (wk 3–6) | RI-003 (full), RI-007 |
| Sprint C (wk 7–12) | RI-005, RI-009, RI-011, RI-012 |
| Post-Sprint C | RI-008 |
| Phase 3C | RI-010 |
| Phase 5E (long-term) | RI-002 |
| Permanent rule | RI-001, RI-004 |
