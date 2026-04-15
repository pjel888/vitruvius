> ⚠️ **HISTORICAL SNAPSHOT — SUPERSEDED 2026-04-15**
>
> This audit was written on 2026-04-13 against a pre-Sprint-A baseline. It is retained here as a frozen historical record of what the codebase looked like before Sprints A + B + C + D + Q + R + PHYS + H + GEOM + WIKI + GT + HP + Z + HP.3-R shipped. Almost every "weakness" or "missing feature" flagged below has since been addressed.
>
> **For the current state of the codebase, read these instead:**
> - `/.ai/10_state/active_context.md` — current session state
> - `/.ai/10_state/decisions.md` — architecture decisions AD-001 through AD-029
> - `/.ai/01_roadmap/current-phase.md` — current sprint / phase
> - `/.ai/00_system/architecture.md` — current package layout (including post-Sprint-D additions)
> - `/.ai/00_system/pipeline-overview.md` — current execution flow

---

# Normalization Audit — Vitruvius

## Purpose
This audit provides a code-level forensic analysis of the normalization layer within Vitruvius. It identifies how text is cleaned, structured, and prepared for canonicalization and relationship extraction.

## Scope
The audit covers all Python modules in `scripts/vitruvius/` and the primary CLI entrypoint `scripts/pipeline_cli.py`.

## Repository Map
| Module | Relevance |
| :--- | :--- |
| `utils.py` | Contains basic text and filename normalization utilities. |
| `conversion.py` | Orchestrates the transformation from raw formats to Markdown. |
| `detection.py` | Uses text normalization to verify PDF quality. |
| `canonicalize.py` | Normalizes metadata (titles) for the canonical layer. |
| `relationships_sections.py` | Contains inline text cleaning for section-based extraction. |
| `ocr.py` | Leverages `ocrmypdf` for structural normalization (deskew). |

## Entry Points
- `python scripts/pipeline_cli.py convert`: Entry point for the conversion process where initial text extraction and implicit normalization occur.
- `python scripts/pipeline_cli.py canonicalize-one`: Entry point where metadata normalization happens.

## Import Graph
Normalization logic is **scattered** rather than centralized. 
- `detection.py` imports `normalize_text` from `utils.py`.
- `relationships_sections.py` defines its own internal `normalize_text`.
- `canonicalize.py` defines its own internal `normalize_title`.
- `conversion.py` relies on external library `opendataloader_pdf` for the bulk of content transformation.

## Normalization Pipeline (Actual)
There is **no formal normalization pipeline**. Normalization is currently a series of fragmented, task-specific transformations.

1.  **Ingestion/Detection:** Basic cleanup to count characters.
2.  **Conversion:** Transformation to Markdown (external dependency).
3.  **Extraction Preparation:** Line merging and whitespace collapsing (inline).
4.  **Metadata Mapping:** Title normalization (rules-based).

## Module Breakdown

### `utils.py`
- `normalize_text(text: str)`: 
  - Implementation: `" ".join(text.split())`
  - Effect: Collapses all whitespace (tabs, newlines, multiple spaces) into a single space.
- `normalize_filename(name: str)`: 
  - Implementation: Lowercases stem and removes non-alphanumeric characters.

### `relationships_sections.py`
- `normalize_text(lines: List[str])`:
  - Implementation: Joins lines with a space and then applies `re.sub(r"\s+", " ", text)`.
  - Effect: Nearly identical to `utils.normalize_text` but handles lists of lines.

### `canonicalize.py`
- `normalize_title(path: str, rule: dict | None)`:
  - Implementation: Pulls from YAML rule if present, otherwise uses file stem.

## Transformation Inventory
| Operation | Type | Location | Status |
| :--- | :--- | :--- | :--- |
| Whitespace Collapsing | Cleanup | `utils.py`, `relationships_sections.py` | VERIFIED |
| Line Merging | Structural | `utils.py`, `relationships_sections.py` | VERIFIED |
| Deskewing | Structural | `ocr.py` (via `ocrmypdf`) | VERIFIED |
| Filename Normalization | Metadata | `utils.py` | VERIFIED |
| Title Normalization | Metadata | `canonicalize.py` | VERIFIED |
| Header Normalization | Structural | N/A | **NOT IMPLEMENTED** |
| Noise Removal (Page Nos) | Cleanup | N/A | **NOT IMPLEMENTED** |
| Token Normalization | Semantic | N/A | **NOT IMPLEMENTED** |

## Inline vs Centralized Normalization
- **Finding:** Normalization is **90% inline or duplicated**.
- The same "collapse whitespace" logic exists in multiple places.
- There is no single "Normalize Layer" that takes Raw Markdown and produces Clean Markdown.

## Pipeline Position
Normalization currently occurs **late** in the pipeline, typically immediately before extraction or detection. It does not exist as a standalone stage between `convert` and `canonicalize`.

## Downstream Dependencies
- **Relationship Extraction:** Depends on line merging to prevent regex patterns from failing across line breaks.
- **Detection:** Depends on whitespace collapsing to get an accurate character count for PDF quality assessment.
- **Canonicalization:** Depends on title normalization for stable ID generation.

## Missing Normalization Layer
Vitruvius lacks a **Text Refinement Layer**. 
- Extracted Markdown from `opendataloader_pdf` is taken "as is".
- Common artifacts like "Page 1 of 10", header/footer text, and broken tables are not cleaned before they reach the knowledge layer.

## Inconsistencies
- `utils.normalize_text` vs `relationships_sections.normalize_text`: Two different implementations of the same logic.
- `relationships.py` uses windows of lines directly without calling a shared normalization function, potentially missing relationships that span across its chosen window size (3 lines).

## Dead Code
- No significant dead transformation code found; however, the fragmentation makes it hard to verify coverage.

## Performance Risks
- The use of `re.sub(r"\s+", " ", text)` on very large documents inside extraction loops may introduce minor latency, though unlikely to be a bottleneck compared to OCR or LLM calls.

## Changelog
- **2026-04-13:** Initial Forensic Normalization Audit. Identified fragmentation and lack of a dedicated refinement layer.
