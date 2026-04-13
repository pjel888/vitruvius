# Vitruvius — Core Principles

## Purpose
This document defines the non-negotiable, enforceable principles that govern how the Vitruvius system is designed, extended, and maintained. These rules dictate architectural choices, code additions, and pipeline behaviors.

## Scope
These principles apply to all developers, all code in `scripts/vitruvius/`, all CLI usage, and all automated agents operating within the repository.

## Core Principles

### 1. The Filesystem is the Database
Vitruvius relies on a strict directory structure (`001` through `006`) rather than a hidden relational database to maintain state, track lineage, and store knowledge.
- **Enforcement:** Code MUST NOT introduce external databases (like SQLite, Postgres) for core document tracking.
- **Consequence:** If the filesystem structure defined in `constants.py` and `paths.py` is bypassed, the system will fail to track state.

### 2. Immutability of Raw Data
The `001_Raw-Source-Layer` represents the ground truth. It is strictly read-only for the pipeline.
- **Enforcement:** Pipeline scripts MUST NOT modify, move, or delete files in `001_Raw-Source-Layer`. All processing must output to downstream layers (e.g., `002_Raw-Conversion-Layer`).
- **Consequence:** Violating this destroys the reproducible nature of the pipeline.

### 3. Idempotent Pipeline Stages
Every stage in the pipeline (Scan, Convert, Canonicalize, Extract) must be capable of being run multiple times without causing duplicate data or corrupted state.
- **Enforcement:** Scripts MUST check registries (e.g., `latest_raw_file_registry.csv`) or filesystem existence before processing to skip already-completed work unless explicitly forced.
- **Consequence:** Non-idempotent scripts will bloat the knowledge graph with duplicate relationships and concepts.

## Data and Pipeline Principles

### 4. Strict Path-Based Traceability
Every artifact produced by the system must be traceable back to its origin.
- **Enforcement:** Output paths in `002_Raw-Conversion-Layer` MUST mirror the internal directory structure of `001_Raw-Source-Layer`.
- **Consequence:** Failure to maintain structural parity breaks `reconcile.py` and breaks lineage tracking.

### 5. Explicit Registry State
The system’s awareness of its own data exists entirely within `006_System-Manifests/registries` (CSV files).
- **Enforcement:** Any script that discovers or processes files MUST update or snapshot the relevant registry using functions in `reports.py`.
- **Consequence:** If a file is on disk but not in the registry, it effectively does not exist to the pipeline orchestrator.

## Canonicalization Principles

### 6. Deterministic Canonical Mapping
Mapping a raw file to a Canonical Knowledge entity must be predictable and rules-driven.
- **Enforcement:** Hardcoding ID mappings in Python is FORBIDDEN. All canonical matching MUST go through `scripts/vitruvius/rules/canonical_rules.yaml`.
- **Consequence:** Arbitrary canonicalization makes the system unmaintainable and breaks graph linking.

### 7. Immutable Canonical IDs
Once an ID (e.g., `law-national-building-code`) is assigned and saved in `003_Canonical-Knowledge-Layer`, it is permanent.
- **Enforcement:** IDs MUST adhere to the strict `<prefix>-<slug>` format defined in `naming-conventions.md`. Changing an ID requires a formal migration script (`migrate-ids-plan` / `migrate-ids-apply`).
- **Consequence:** Silent ID changes break all downstream relationships and graph edges.

## Relationship and Knowledge Principles

### 8. Explicit Concept Vocabulary
Relationship extraction must only use known, predefined concepts.
- **Enforcement:** The extraction subsystem (`relationships.py`) MUST only match concepts that exist as markdown files in `003_Canonical-Knowledge-Layer/shared/concepts/`.
- **Consequence:** Allowing free-text concept extraction leads to uncontrolled vocabulary sprawl.

### 9. Local-First AI Review
Vitruvius prioritizes local, privacy-preserving AI processing.
- **Enforcement:** The review subsystem (`ollama_review.py`) MUST default to a local LLM runner (Ollama). External APIs (like OpenAI or Anthropic) are CONDITIONALLY ALLOWED only if explicitly configured as opt-in alternatives.
- **Consequence:** Forcing cloud dependencies breaks the system's ability to run air-gapped or on sensitive internal documents without review.

## System Integrity Rules

### Allowed Patterns
- **YAML Frontmatter:** Using YAML frontmatter in Markdown files to store structured metadata (IDs, aliases, relationships).
- **Sidecar Files:** Generating `.json` files alongside `.md` files to store complex extraction data that doesn't fit well in Markdown.
- **Timestamped Snapshots:** Creating `YYYYMMDDTHHMMSSZ_...` files for point-in-time auditing.

### Forbidden Patterns
- **In-Place Modification:** Overwriting raw source documents.
- **Hidden State:** Using `.pkl`, `.db`, or hidden configuration files to store pipeline progress outside of `006_System-Manifests`.
- **"Magic" String Matching:** Hardcoding string matches for specific laws inside extraction logic instead of using the rules engine.

### Conditional Patterns
- **Manual Overrides:** Users can manually edit Canonical Markdown files in `003_Canonical-Knowledge-Layer`. However, if they break the YAML frontmatter schema, the `lint` stage must catch and flag it.

## Enforcement Mechanisms
1.  **Linter (`run_lint`):** Checks for missing files, duplicate names, and structural integrity.
2.  **Reconciler (`run_reconcile`):** Detects orphaned artifacts and stale outputs to enforce the path-based traceability principle.
3.  **Code Review:** Any PR modifying the core pipeline must be audited against these principles.

## Violation Consequences
Code or workflows that violate these principles will be rejected during automated linting or PR review. Persistent architectural violations must be documented as "Technical Debt" or "Known Issues" and prioritized for refactoring.

## Changelog
- **2026-04-13:** Initial set of principles derived from codebase audit. Formally documented Filesystem-as-Database, Idempotency, and Traceability rules.
