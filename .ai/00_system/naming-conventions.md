# Vitruvius — Naming Conventions

## Purpose
This document serves as the single source of truth for all naming conventions within the Vitruvius system. Consistency in naming ensures traceability across the pipeline, prevents collisions in the canonical knowledge layer, and maintains codebase readability.

## Scope
These rules apply to all Python code, CLI interfaces, filesystem structures, and data artifacts (Markdown, JSON, CSV).

## Naming Principles
1.  **Explicitness:** Prefer descriptive names over abbreviations (e.g., `relative_path` instead of `rel_path`).
2.  **Traceability:** Names must reflect the origin or purpose of the entity (e.g., `law-national-building-code`).
3.  **Immutability:** Once a canonical ID is assigned, it should not change, as it acts as a permanent reference.
4.  **Consistency:** Use the same term for the same concept across all layers (e.g., "registry" for state-tracking files).

## Python Code Conventions
Follow [PEP 8](https://peps.python.org/pep-0008/) with the following system-specific refinements:

### Module and Package Naming
- **Packages:** Lowercase, single word if possible, or use underscores (e.g., `vitruvius`).
- **Modules:** Lowercase with underscores (e.g., `canonicalize.py`, `ollama_review.py`).
- **Scripts:** Lowercase with underscores, often suffixed with `_cli` or `_one` (e.g., `pipeline_cli.py`, `Word-PPT-To-PDF.py` - *Note: The latter is a legacy inconsistency to be corrected*).

### Function and Method Naming
- **Entry Points:** Functions invoked by the CLI must start with `run_` (e.g., `run_scan()`, `run_canonicalize_one()`).
- **Internal Actions:** Use `snake_case` verbs (e.g., `build_file_entries()`, `detect_pdf_type()`).
- **Path Builders:** Functions generating filesystem paths must start with `build_` and specify the target type (e.g., `build_conversion_relative_paths()`).
- **Directory Enforcers:** Functions that ensure directory existence must start with `ensure_` (e.g., `ensure_snapshot_dir()`).

### Variable Naming
- **Paths:** Always suffix with `_path` (file) or `_dir` (directory) (e.g., `repo_root`, `registry_dir`).
- **Relative vs Absolute:** Prefix with `rel_` or `abs_` if both are present in the same scope, or use descriptive names like `relative_pdf_path`.
- **Constants:** `UPPER_CASE_WITH_UNDERSCORES` (e.g., `RAW_LAYER_NAME`).

### Class Naming
- **Data Models:** `PascalCase` (e.g., `FileEntry`).
- **Interfaces/Engines:** `PascalCase` (e.g., `PdfReader` - from external lib, follow local patterns for internal classes).

## CLI and Entrypoint Naming
- **Commands:** Lowercase with hyphens (kebab-case) (e.g., `scan`, `status`, `ocr-queue`, `canonicalize-one`).
- **Arguments:** Lowercase with underscores (snake_case) (e.g., `relative_pdf_path`).
- **Flags:** Lowercase with hyphens (kebab-case) (e.g., `--sample-pages`, `--no-deskew`).

## Pipeline Stage Naming
Stages must match the `run_` functions in `pipeline_cli.py`:
1. `scan`
2. `status`
3. `lint`
4. `convert`
5. `canonicalize`
6. `relationships`
7. `review`

## File and Folder Naming

### Root Layers
Folders must be prefixed with a 3-digit index and use Pascal-Kebab-Case:
- `001_Raw-Source-Layer/`
- `002_Raw-Conversion-Layer/`
- `003_Canonical-Knowledge-Layer/`
- `004_Derived-Content-Layer/`
- `005_Operational-Intelligence-Layer/`
- `006_System-Manifests/`

### Sub-Directories
- Use lowercase with underscores or hyphens as established by the specific layer (e.g., `raw_markdown`, `sidecar_json`).

## Artifact Naming (Markdown, JSON, Reports)

### Reports and Logs
- **Latest Version:** `latest_<type>_report.<ext>` (e.g., `latest_status_report.json`).
- **Timestamped Version:** `<ISO8601Z_STAMP>_<safe_stem>_<type>_report.<ext>`.
  - Timestamp Format: `%Y%m%dT%H%M%SZ` (e.g., `20260413T120000Z`).
  - Example: `20260413T043540Z_PD_1096_detect_one_report.json`.

### Registries
- `latest_<type>_registry.csv` (e.g., `latest_conversion_registry.csv`).
- `<ISO8601Z_STAMP>_<type>_registry.csv`.

## Canonical Entity Naming
### ID Naming Standards
Canonical IDs follow the pattern: `<prefix>-<slugified-title>`
- **Valid Prefixes:** `law`, `irr`, `concept`, `glossary`, `relationship`, `handout`, `reviewer`, `law-section`, `source`.
- **Slugification:** Lowercase, alphanumeric, hyphens instead of spaces/special chars.
- **Example:** `law-national-building-code-of-the-philippines`.

### Concept Naming
- **Files:** `<slugified-concept>.md` (e.g., `occupancy-classification.md`).
- **ID:** `concept-<slugified-concept>` (e.g., `concept-occupancy-classification`).

### Source Naming
- **Files:** `<slugified-title>.md` (e.g., `national-building-code.md`).

## Relationship Naming
Relationships extracted between entities must use lowercase verbs:
- `requires`
- `defines`
- `depends_on`
- `limits`
- `affects`
- `governs` (Law → Concept)

## Registry and Manifest Naming
- Headers in CSV registries must use `snake_case` (e.g., `source_relative_path`, `timestamp_utc`).

## Anti-Patterns (Forbidden Naming)
- **Generic Names:** Avoid `data.json`, `process.py`, `tmp/`.
- **Mixed Casing in Files:** Avoid `MyFile.Md` or `data_Report.JSON`.
- **Spaces in Filenames:** Never use spaces; use hyphens for canonical files and underscores for internal reports.
- **Ambiguous Timestamps:** Never use local time; always use UTC with `Z` suffix.

## Migration Rules
When renaming legacy files (e.g., `Word-PPT-To-PDF.py` → `word_ppt_to_pdf_cli.py`), a `migrate-ids-plan` must be generated to ensure no breakage in the registry layer.

## Enforcement Rules
1.  **Linter:** `run_lint` stage in the pipeline checks for basic naming violations.
2.  **Pull Request Review:** All new modules and canonical entities must be verified against this document.
3.  **Automated Checks:** `canonicalize.py` enforces ID prefix validation.

## Changelog
- **2026-04-13:** Initial version established from codebase audit. Standardized timestamp formats, ID prefixes, and report naming patterns.
