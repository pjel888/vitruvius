# Vitruvius — Core Principles

## Purpose
This document defines the non-negotiable, enforceable principles that govern how the Vitruvius system is designed, extended, and maintained. These rules dictate architectural choices, code additions, and pipeline behaviors.

## Scope
These principles apply to all developers, all code in `scripts/vitruvius/`, all CLI usage, and all automated agents operating within the repository.

## Core Principles

### 1. The Filesystem is the Database (for Document Lifecycle)
Vitruvius relies on a strict directory structure (`001` through `006`) and `006_System-Manifests` CSV registries to track document lineage, canonical state, and pipeline progress. These registries are the single source of truth for document lifecycle.
- **Enforcement:** Code MUST NOT introduce external databases (SQLite, Postgres, etc.) to replace or shadow the `006_System-Manifests` registries for document tracking. The canonical knowledge layer (`003`) and raw layer (`001`) MUST remain filesystem-only.
- **Storage-layer exception (AD-029):** The append-only event log (`graph/event_store.py`) and stateful review registry (`review/stateful_registry.py`) are performance-layer KV stores for graph events and LLM reviewer verdicts. These do NOT track document identity or pipeline state — they track graph mutation events and cached LLM decisions. They are accessed exclusively through factory functions (`make_event_store()` / `make_stateful_registry()`) that dispatch on feature flags, and both carry a filesystem fallback path.
- **Consequence:** If the filesystem structure defined in `constants.py` and `paths.py` is bypassed for document lifecycle tracking, the system will fail to track state. Storage-layer KV backends are additive performance wins, not replacements for the registry contract.

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

## Canonicalization Principles

### 5. Deterministic Canonical Mapping
Mapping a raw file to a Canonical Knowledge entity must be predictable and rules-driven.
- **Enforcement:** Hardcoding ID mappings in Python is FORBIDDEN. All canonical matching MUST go through `scripts/vitruvius/rules/canonical_rules.yaml`.
- **Consequence:** Arbitrary canonicalization makes the system unmaintainable and breaks graph linking.

### 6. Immutable Canonical IDs
Once an ID (e.g., `law-national-building-code`) is assigned and saved in `003_Canonical-Knowledge-Layer`, it is permanent.
- **Enforcement:** IDs MUST adhere to the strict `<prefix>-<slug>` format defined in `naming-conventions.md`. Changing an ID requires a formal migration script (`migrate-ids-plan` / `migrate-ids-apply`).
- **Consequence:** Silent ID changes break all downstream relationships and graph edges.

## Relationship and Knowledge Principles

### 7. Explicit Concept Vocabulary
Relationship extraction must only use known, predefined concepts.
- **Enforcement:** The extraction subsystem (`relationships.py`) MUST only match concepts that exist as markdown files in `003_Canonical-Knowledge-Layer/shared/concepts/`.
- **Consequence:** Allowing free-text concept extraction leads to uncontrolled vocabulary sprawl.

### 8. Local-First AI Review
Vitruvius prioritizes local, privacy-preserving AI processing.
- **Enforcement:** The review subsystem (`ollama_review.py`) MUST default to a local LLM runner (Ollama) at `http://127.0.0.1:11434` (reads from `config/vitruvius.yaml` via `get_ollama_url()`, not hardcoded). External APIs (like OpenAI or Anthropic) are CONDITIONALLY ALLOWED only if explicitly configured as opt-in alternatives in `config/vitruvius.yaml`. Any new LLM integration that would break air-gap operation is XL-risk and requires explicit Philip consent (I7 in EXECUTION_LOOP.md).
- **Consequence:** Forcing cloud dependencies breaks the system's ability to run air-gapped or on sensitive internal documents without external review.

### 9. No Soft Output
Every pipeline stage must produce deterministic, verifiable artifacts. Probabilistic or "best-effort" output MUST carry an explicit confidence signal or be gated behind a review stage before promotion.
- **Enforcement:** Relationship candidates MUST NOT be promoted to the canonical layer (`003`) without passing through the review subsystem or a deterministic pre-review filter. Soft signals (scores, probabilities) that influence promotion MUST be written to `006_System-Manifests` as auditable artifacts.
- **Consequence:** Allowing unreviewed soft output to reach `003` produces an unauditable knowledge graph.

### 10. No Schema-less Growth
Every new structured artifact type (relationship predicates, canonical ID prefixes, flag names, report shapes) MUST be registered before deployment.
- **Enforcement:** New relationship predicates require a schema bump in `.ai/06_specs/relationship-schema.md` AND an AD. New canonical ID prefixes require an update to `naming-conventions.md` AND an AD. New feature flags require a `EXPECTED_FLAGS` entry in `scripts/tests/test_features.py` before merging (CI-enforced). See I3 and I4 in EXECUTION_LOOP.md.
- **Consequence:** Unregistered schema additions break graph lineage, cause test failures in `test_features.py`, and defeat the audit trail maintained by the AD ledger.

## System Integrity Rules

### Allowed Patterns
- **YAML Frontmatter:** Using YAML frontmatter in Markdown files to store structured metadata (IDs, aliases, relationships).
- **Sidecar Files:** Generating `.json` files alongside `.md` files to store complex extraction data that doesn't fit well in Markdown.
- **Timestamped Snapshots:** Creating `YYYYMMDDTHHMMSSZ_...` files for point-in-time auditing.

### Forbidden Patterns
- **In-Place Modification:** Overwriting raw source documents.
- **Hidden State:** Using `.pkl` or hidden configuration files to store pipeline progress outside of `006_System-Manifests`. **Exception:** KV performance stores (SQLite `.db` event log and RocksDB directory in `005_Operational-Intelligence-Layer/`) are explicitly permitted per AD-029 when accessed through factory functions (`make_event_store()` / `make_stateful_registry()`). These stores do not track document identity or canonical state.
- **"Magic" String Matching:** Hardcoding string matches for specific laws inside extraction logic instead of using the rules engine.

### Conditional Patterns
- **Manual Overrides:** Users can manually edit Canonical Markdown files in `003_Canonical-Knowledge-Layer`. However, if they break the YAML frontmatter schema, the `lint` stage must catch and flag it.

## Operational Invariants (from EXECUTION_LOOP.md v3.0)

These are BLOCK-level rules enforced by the daily execution loop. A plan that violates any of them is rejected before dispatch.

#### Lazy CLI Imports (AD-015, I5)
- **Rule:** Every `subparsers.add_parser(...)` dispatch branch in `scripts/pipeline_cli.py` MUST import its heavy dependencies INSIDE the `if args.command == "..."` branch, not at module top-level.
- **Enforcement:** `scripts/tests/test_cli_lazy_imports.py` asserts this automatically. Violation = BLOCK.
- **Consequence:** A top-level import of a heavy package (e.g., `docling`, `torch`, `rocksdict`) in `pipeline_cli.py` would add that package's load time to every CLI invocation, regardless of which command is run.

#### The Rust Line (AD-036, I6)
- **Rule:** Port a compute kernel to Rust only if the hot path is NOT already a single numpy/BLAS/C-native primitive call. Pure orchestration belongs in Python. Every Rust port MUST include a bench artifact demonstrating a ≥2× wall-time improvement on the measured kernel before the flag default is flipped to `true`.
- **Enforcement:** Any PR that ports a numpy hot loop to Rust without a bench artifact is BLOCK. Sprint PQ-1 and LSH-1 correctly recorded DEFER_ALREADY_NATIVE for numpy BLAS paths. Sprint RUST-MIG-1 (S1: 200×, S2: 12.18×, N4: 2.73×) cleared the gate.
- **Consequence:** Unnecessary Rust porting adds FFI overhead (pyo3 boundary cost) that can easily negate the kernel speedup. The ≥2× gate filters out false positives.

#### Test Baseline Monotonic (I8)
- **Rule:** The `pytest scripts/tests/` passing test count is monotonically non-decreasing across commits. The current baseline is **1528 passed / 1 skipped** (as of Sprint LSH-1 closure, AD-042).
- **Enforcement:** Any plan that reduces the passing-test count without replacing the deleted coverage with equivalent tests is BLOCK. A sprint that adds new behavior MUST add tests for that behavior; the net test delta must be ≥0.
- **Consequence:** Shrinking the test suite destroys the regression safety net that makes feature-flag defaults safe to flip.

#### Registry Single-Writer (I9)
- **Rule:** CSV registries under `006_System-Manifests/registries/` are single-writer per pipeline stage. Concurrent writes to the same registry from multiple processes or threads are FORBIDDEN without a lock design and an AD.
- **Enforcement:** Code review. Any plan that introduces parallel pipeline execution across stages (e.g., `ProcessPoolExecutor` at the stage level) must explicitly design a registry lock before dispatch.
- **Consequence:** Concurrent registry mutation produces corrupted CSV state that breaks `status.py` and `reconcile.py`.

## Enforcement Mechanisms
1.  **Linter (`run_lint`):** Checks for missing files, duplicate names, and structural integrity.
2.  **Reconciler (`run_reconcile`):** Detects orphaned artifacts and stale outputs to enforce the path-based traceability principle.
3.  **Code Review:** Any PR modifying the core pipeline must be audited against these principles.

## Violation Consequences
Code or workflows that violate these principles will be rejected during automated linting or PR review. Persistent architectural violations must be documented as "Technical Debt" or "Known Issues" and prioritized for refactoring.

## Changelog
- **2026-04-13:** Initial set of principles derived from codebase audit. Formally documented Filesystem-as-Database, Idempotency, and Traceability rules.
- **2026-04-15:** Updated to reflect 21 sprint closures. P1 enforcement clause amended to allow storage-layer KV backends per AD-029. Renumbered Local-First AI from P9 to P8. Added P9 (No Soft Output) and P10 (No Schema-less Growth) from EXECUTION_LOOP.md v3.0 canonical P-list. Added Operational Invariants section with I5 (Lazy CLI Imports / AD-015), I6 (Rust Line / AD-036), I8 (Test Baseline Monotonic), I9 (Registry Single-Writer). Updated Forbidden Patterns to permit `.db` KV stores per the AD-029 storage exception.
