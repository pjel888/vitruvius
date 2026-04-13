# Known Issues & Risks - Vitruvius

## RI-001: Filesystem Coupling
- **Description:** The system is tightly coupled to the directory structure defined in `paths.py`.
- **Impact:** High. Moving or renaming directories without updating code will break the pipeline.

## RI-002: Regex Extraction Fragility
- **Description:** Relationship extraction relies on fixed regex patterns.
- **Impact:** Medium. Variations in legal language or formatting may lead to missed extractions.

## RI-003: External Dependency (Ollama)
- **Description:** The review layer requires an external Ollama service.
- **Impact:** Medium. The pipeline fails if the service is unavailable or the model is not loaded.

## RI-004: Python Environment
- **Description:** `scripts/vitruvius` location requires specific `PYTHONPATH` or working directory context.
- **Impact:** Low.

## RI-005: Legacy Naming Inconsistencies
- **Description:** Some scripts (`Word-PPT-To-PDF.py`) and early reports do not follow the new `naming-conventions.md` standard.
- **Impact:** Low (aesthetic/consistency), but may cause confusion for new developers.

## RI-006: Manual Promotion Gap
- **Description:** There is no automated bridge between the Conversion Layer (002) and the Canonical Knowledge Layer (003); ID verification and frontmatter generation require manual oversight.
- **Impact:** Medium. Slows down high-volume ingestion and increases risk of ID collisions if not monitored.

## RI-007: Normalization Fragmentation
- **Description:** Text normalization (whitespace collapsing, line merging) is duplicated across `utils.py` and `relationships_sections.py`, and lacks a centralized "Text Refinement" layer.
- **Impact:** Medium. Leads to inconsistent data quality and makes it harder to implement advanced cleanup (e.g., noise removal).
