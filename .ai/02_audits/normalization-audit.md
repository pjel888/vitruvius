> ⚠️ **HISTORICAL SNAPSHOT — SUPERSEDED 2026-04-15**
>
> This audit was written on 2026-04-13 against a pre-Sprint-A baseline.
> It is retained here as a frozen historical record of what the normalization
> layer looked like before 21 sprints shipped in a single session.
>
> The 21 closed sprints (in execution order) are: Q · R · H · GT · HP ·
> HP.3-R · WIKI · GEOM · PHYS · Z · Meta-Docs · 1B-M1 · 1B-M2 ·
> RUST-PDF-1 · 1B-M3 · DISTILL-1 · RUST-MIG-1 · AUDIT-1 · PIPELINE-CLI ·
> PQ-1 · LSH-1. See the governing plan §1.1 for the full per-sprint ledger.
>
> Architecture decisions now span AD-001 through AD-042 (plus sub-decision
> AD-038a). The pointer "AD-001 through AD-029" in this file is outdated.
>
> **For the current state of the codebase, read these instead:**
> - `/.ai/03_plans/00-governing-implementation-plan.md` — authoritative sprint ledger (v3.0.0)
> - `/.ai/00_system/EXECUTION_LOOP.md` — v3.0 canonical operating contract
> - `/.ai/01_roadmap/master-roadmap.md` — roadmap v2.2.0
> - `/.ai/10_state/active_context.md` — current session state
> - `/.ai/10_state/decisions.md` — architecture decisions AD-001 through AD-042
> - `/.ai/10_state/known_issues.md` — open risks + closure timeline
> - `/.ai/01_roadmap/current-phase.md` — current sprint / phase
> - `/.ai/00_system/architecture.md` — current package layout
> - `/.ai/00_system/pipeline-overview.md` — current execution flow
> - `/.ai/00_system/naming-conventions.md` — naming rules
> - `/.ai/00_system/principles.md` — architectural principles

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

---

## 2026-04-15 Post-Sprint Reality Check

### The normalization layer now exists — SHIPPED (Sprint B, AD-007; 2026-04-14)
The central finding of this audit — "There is no formal normalization pipeline" — was the
precise motivation for Sprint B. Sprint B built exactly what was described as missing.

**`scripts/vitruvius/normalization/` subpackage** (6 files):
- `engine.py` — `NormalizationEngine` with phase-locked execution and scope routing.
  Accepts a `RefinementContext` (scope: `document`, `section`, or `token`), runs the
  applicable tier stack in order, and returns a `RefinedDocument`.
- `rules_tier_a.py` — Tier A structural rules: whitespace collapsing, line merging,
  JSON-fence stripping, page-number artifact removal, header/footer noise suppression.
- `rules_tier_b.py` — Tier B content rules: section-header normalization, bullet
  normalisation, trailing-punctuation cleanup.
- `rules_tier_c.py` — Tier C semantic rules: token normalization, abbreviation expansion
  (Philippine legal register).
- `ast_chunker.py` — AST-based semantic chunking for Layer 4/5 retrieval.
- `embedding_chunker.py` — Embedding-aware chunking for retrieval infrastructure.
- `refine.py` — CLI stage handler; emits `.refined.json` manifests per processed file.

**Transformation inventory corrections** (the "NOT IMPLEMENTED" rows in §Transformation
Inventory are now wrong):
- Header Normalization: **SHIPPED** — Tier B header-normalization rule.
- Noise Removal (Page Numbers, Headers/Footers): **SHIPPED** — Tier A artifact-removal rules.
- Token Normalization: **SHIPPED** — Tier C semantic rules.

**Import fragmentation corrected:**
Risk RI-007 flagged the 3-way duplication of `normalize_text` across `utils.py`,
`relationships_sections.py`, and `canonicalize.py`. Sprint B made the `NormalizationEngine`
the canonical authority. The inline duplicates are retained for backward compatibility but
new code routes through the engine.

**Pipeline position corrected:**
The audit noted normalization was "90% inline" with no standalone stage. The `refine` CLI
command now runs as an explicit pipeline step (`run-with-review` composite chains it after
`convert` and before `review`).

6 PD 1096 files were refined in the first Sprint B pass with idempotency verified.
Risk RI-007 (Normalization Fragmentation) is **CLOSED** for MVP scope. Tier C semantic
rules, full semantic chunking, and destructive-guard rollback are tracked as post-Sprint-B
follow-ups and are substantially shipped via the subpackage files above.

### Current sprint count and AD ceiling
As of 2026-04-15: **21 sprints closed**. Architecture decisions span **AD-001 through
AD-042** (plus sub-decision AD-038a).
