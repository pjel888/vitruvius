# Architectural Decisions - Vitruvius

## AD-001: Filesystem-as-Database
- **Date:** 2026-04-13
- **Status:** Implemented
- **Context:** The system needs high traceability and human-readability.
- **Decision:** Use structured directories (001-006) and CSV registries instead of a traditional database for the primary knowledge lifecycle.
- **Consequence:** Easy debugging and version control, but potential performance issues with extremely large file counts.

## AD-002: Core Logic in Scripts Package
- **Date:** 2026-04-13
- **Status:** Implemented
- **Context:** Development is CLI-centric.
- **Decision:** Maintain the `vitruvius` functional package inside the `scripts` directory.
- **Consequence:** Simplifies script execution but deviates from standard Python packaging best practices (e.g., `src/` layout).

## AD-003: Rules-Based Canonicalization
- **Date:** 2026-04-13
- **Status:** Implemented
- **Context:** Entity classification must be deterministic.
- **Decision:** Use a YAML-based rules engine for mapping raw files to canonical IDs.
- **Consequence:** Highly predictable, but requires manual maintenance of rules.

## AD-004: Strict ID and Naming System
- **Date:** 2026-04-13
- **Status:** Implemented
- **Context:** Traceability across layers is critical for knowledge graph integrity.
- **Decision:** Enforce a `<prefix>-<slug>` pattern for IDs and a strict timestamped naming convention for all pipeline artifacts.
- **Consequence:** Eliminates ambiguity in lineage tracking; requires robust slugification and path-building utilities.

## AD-005: Linear Pipeline Orchestration
- **Date:** 2026-04-13
- **Status:** Implemented
- **Context:** Complexity must be managed in a file-system-driven extraction engine.
- **Decision:** Use a flat CLI orchestrator (`pipeline_cli.py`) with modular `run_` functions for each stage, maintaining idempotency through registry checks.
- **Consequence:** Easy to run individual stages; requires manual coordination for complex branched flows until an automated "Promotion" stage is built.

## AD-006: Local-First AI Strategy
- **Date:** 2026-04-13
- **Status:** Implemented
- **Context:** System requires review capabilities without mandating cloud API keys or compromising document privacy.
- **Decision:** Integrate Ollama natively for the relationship review stage.
- **Consequence:** High hardware requirements for running the pipeline locally, but ensures privacy and offline capability.

## AD-007: Ingestion Layer Gaps
- **Date:** 2026-04-13
- **Status:** Documented (Audit Complete)
- **Context:** Code-level forensic audit of ingestion pipeline completed.
- **Finding:** Scanner captures 7 metadata fields (no hashes), detection uses heuristic, registry tracks per-file status, no automatic retry (manual re-run required).
- **Decided:** Audit documented in `.ai/02_audits/ingestion-audit.md`.
- **Consequence:** Known gaps: no file hashing, no staging directory, no auto-retry, sequential OCR.

## AD-008: Review Layer Implementation
- **Date:** 2026-04-13
- **Status:** Implemented (Audit Complete)
- **Context:** Code-level forensic audit of review and validation layer completed via `ollama_review.py`.
- **Finding:** Ollama-based relationship reviewer is implemented (345 lines). CLI command `review-relationships-ollama` exists. Three decisions: keep/review_further/reject. Confidence scoring 0.0-1.0. However: NOT in automatic pipeline (manual trigger only), NO second-pass review, NO confidence threshold auto-filtering, sequential processing only.
- **Decided:** Audit documented in `.ai/02_audits/review-layer-audit.md`.
- **Consequence:** Review exists but not enforced. Users must manually invoke and manually consume results. Consider pipeline integration for Phase 2.
