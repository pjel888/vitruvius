> ⚠️ **HISTORICAL SNAPSHOT — SUPERSEDED 2026-04-15**
>
> This audit was written on 2026-04-13 against a pre-Sprint-A baseline.
> It is retained here as a frozen historical record of what the codebase
> looked like before 21 sprints shipped in a single session. Almost every
> "weakness" or "missing feature" flagged below has since been addressed.
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

# Vitruvius Codebase & Roadmap Audit
**Date:** 2026-04-13
**Auditor:** Senior Architect (Gemini CLI)
**Status:** Brutally Honest / Evidence-Based

## 1. Audit Scope
The audit covered the following areas:
- **CLI Surface:** `scripts/pipeline_cli.py`
- **Core Package:** `scripts/vitruvius/` (All modules)
- **Data Layers:** `001` through `006`
- **Documentation:** `README.md`, `.ai/01_roadmap/`, `docs/`
- **Verification Method:** Direct code inspection and comparison of claims vs. implementation logic.

## 2. Verified Complete Features (High Integrity)
These features are implemented, wired, and reflect high-quality engineering:
- **Multi-Format Ingestion:** PDF (OpenDataLoader), Office (LibreOffice), and Spreadsheet (OpenPyxl/LibreOffice) ingestion paths are fully functional.
- **OCR Pipeline:** OCR queueing and execution (`ocrmypdf`) are properly implemented and integrated with the conversion layer.
- **PDF Detection:** Heuristic-based text vs. scanned detection is solid and used for routing.
- **Registry & Manifest System:** Detailed CSV registries and JSON/TXT run reports are generated for almost every operation.
- **LLM Review Layer:** Ollama integration is functional, including timeout handling, structured JSON parsing, and progress tracking.

## 3. Verified Partial / Weak Features (Low Integrity)
These features are marked "Complete" in roadmaps but are actually minimal placeholders:
- **Canonicalization Layer:** The `canonicalize.py` script is a skeleton. It only generates basic frontmatter and headers. It lacks the ability to generate the "Overview", "Coverage", or "Key Points" seen in some repository examples. The automation is currently just a metadata wrapper.
- **Concept Generation:** `concepts.py` creates placeholder files. It does not extract definitions or enrich content. It simply asserts that "X is a concept".
- **Relationship Extraction:** The logic is purely regex-based matching of concept phrases within a sliding line window. This produces a high volume of false positives (82% rejection rate in latest runs). It is "functional" but technically "primitive".
- **ID Migration:** The scripts work as intended for simple text replacement, but the system relies on manual mapping in `id_migration_map.yaml`.

## 4. Verified Missing / Overstated Features
- **Promotion Layer:** Correctly identified as "Not started" in roadmap. No code exists in `scripts/vitruvius/`.
- **Concept Enrichment:** Marked as `[ ]` in roadmap. Verified as missing.
- **Multi-parser Integration:** No evidence of multi-parser logic beyond the standard PDF extraction.
- **Normalization Pipeline:** No dedicated normalization logic beyond basic text cleaning.
- **Operational Intelligence Layer:** Layers `005` (Chunks, Embeddings, Graphs) are currently empty or only contain placeholder directories.

## 5. Documentation Mismatches
- **Roadmap Inflation:** "Phase 2 — Canonicalization" is marked as `[x] Complete`. In a professional context, this should be `[~] Partial/Placeholder`, as the current script does not produce the quality of content implied by the roadmap's own documentation.
- **State Tracking:** `.ai/10_state` files (e.g., `system_state.json`) are all 0 bytes. The documentation implies active state management that is currently unpopulated.

## 6. Critical Risks
- **Brittle Extraction:** The reliance on basic regex for relationship extraction makes the system heavily dependent on a "ruthless" review layer to filter out noise. Without a better parser, the system will struggle as the concept count grows.
- **Lost Tooling:** There is a mismatch between the current `canonicalize.py` and the existing "high-quality" canonical files in `003_Canonical-Knowledge-Layer`. This suggests the current script is a regression or a simplified replacement for a tool that is no longer in the repo.
- **Hardcoded Endpoints:** Ollama URL is hardcoded to `127.0.0.1:11434`.

## 7. Recommended Roadmap Corrections
- **Demote Phase 2 & 3:** Mark as `[~] Partial` instead of `[x] Complete` until real extraction/enrichment logic is added.
- **Prioritize Promotion:** The project is blocked on moving "Reviewed" knowledge into the "Canonical" layer.
- **Refine Extraction:** High priority to move beyond regex for relationship candidate generation.

---
**Audit result: PROJECT IS IN LATE INGESTION / EARLY EXTRACTION PHASE.**
*Claims of being "Starting Phase 7" are technically correct in terms of sequence, but the foundations (Phase 2, 3, 5) are much thinner than documented.*

---

## 2026-04-15 Post-Sprint Reality Check

This appendix corrects four findings from the body above that are now factually wrong.
The body text is frozen as a historical record; this appendix is the delta.

### Promotion Layer — SHIPPED (Sprint A, 2026-04-14; Sprint Q, 2026-04-15)
Body §4 states "No code exists in `scripts/vitruvius/`." This is no longer true.
- `scripts/vitruvius/promotion/` subpackage ships `bayesian_fusion.py`,
  `stringency_resolver.py`, `temporal_edges.py`, `__init__.py`.
- The `promote` CLI command reads `latest_relationship_review_high_confidence.json`,
  runs a 17-rule validator, and writes records to
  `003_Canonical-Knowledge-Layer/shared/relationships/` with a full audit log.
- Sprint Q (AD-024) wired all 3 Stream G promotion modules into live paths.
  First 3 PD 1096 relationships were promoted on 2026-04-14.
- Risk RI-006 (Manual Promotion Gap) is formally CLOSED.

### Concept Enrichment — SUBSTANTIALLY SHIPPED (Phase 3C, AD-019, AD-020; 2026-04-14)
Body §3 states concepts.py "simply asserts that 'X is a concept'."
- 16/20 PD 1096 concepts now carry real definitions extracted via section-title
  anchors, alias mining, and compound-title matching — zero LLM calls.
- `scripts/vitruvius/concepts/` subpackage: `tfidf_matcher.py`, `pmi_alias_miner.py`,
  `fca_lattice.py`, `contrastive_adapter.py`.
- The 4 remaining concepts (`exit-width`, `parking-and-loading-spaces`, `setbacks`,
  `yards`) need a second corpus or manual curation — not an LLM issue.
- Risk RI-010 is 16/20 closed.

### Normalization Pipeline — SHIPPED (Sprint B, AD-007; 2026-04-14)
Body §4 states "No dedicated normalization logic beyond basic text cleaning."
- `scripts/vitruvius/normalization/` subpackage ships `engine.py` (NormalizationEngine),
  `rules_tier_a.py`, `rules_tier_b.py`, `rules_tier_c.py`, `ast_chunker.py`,
  `embedding_chunker.py`, `refine.py`.
- 8 Tier A/B rules run via the `refine` CLI stage, emitting `.refined.json` manifests.
  6 PD 1096 files refined with idempotency verified.
- Risk RI-007 (Normalization Fragmentation) is CLOSED.

### Hardcoded Ollama URL — FIXED (Sprint A, AD-003 sub-fix; 2026-04-14)
Body §6 states "Ollama URL is hardcoded to `127.0.0.1:11434`."
- The URL is now read from `config/vitruvius.yaml` via
  `scripts/vitruvius/config.py::get_ollama_url()`. The hardcoded value
  (`http://127.0.0.1:11434`) is retained only as a fallback default.
- Sprint B added bounded retries and graceful fallback on connection failure.
- Risk RI-003 (External Dependency — Ollama) is CLOSED.

### Current sprint count and AD ceiling
As of 2026-04-15: **21 sprints closed** in a single session (Q through LSH-1).
Architecture decisions span **AD-001 through AD-042** (plus sub-decision AD-038a).
See `/.ai/03_plans/00-governing-implementation-plan.md` §1.1 for the full ledger.
