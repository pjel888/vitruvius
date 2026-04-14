# Vitruvius — Master Roadmap

> **Document type:** Strategic roadmap + phase contract.
> **Audience:** Architects, engineers, auditors, and autonomous agents operating on this repo.
> **Authoritative for:** Phase order, definitions of done, gating metrics, status reconciliation.
> **Supersedes:** Prior phase lists, ad-hoc README roadmaps, and any conflicting status claims.
> **Version:** 2.0.0 · **Last revised:** 2026-04-14 · **Next review due:** 2026-05-01
> **Owner:** Senior Systems Architect

---

## 0. How to Read This Document

- **Sections 1–4** define *what* Vitruvius is, *why* the architecture looks the way it does, and the governance contracts every phase must honor.
- **Section 5** is the honest status matrix — roadmap claims reconciled against the 2026-04-13 audit pack (`.ai/02_audits/`).
- **Sections 6–7** are the phase contracts. Each phase has: objective, prerequisites, deliverables, definition of done, gating metrics, risks, and links to the plans/audits that back it.
- **Section 8** is the sequenced execution plan for the next 90 days.
- **Sections 9–12** cover KPIs, technical debt, cadence, and non-goals.
- If a phase status in this document disagrees with any other document in the repo, **this document wins** until the reconciliation process in §11 is used to update it.

---

## 1. Vision and Strategy

### 1.1 Long-Term Vision
Vitruvius is a **local-first, governance-first knowledge engine** that converts heterogeneous domain sources (laws, regulations, technical standards, reference material) into a **validated, queryable knowledge graph**. It is not a RAG wrapper. It enforces a hard boundary between *raw text*, *candidate signals*, and *canonical truth*, and treats every transformation as auditable.

Initial corpus: **Philippine building laws and regulations** (PD 1096 and its IRR). Long-term: any structured legal or technical domain that can be expressed through the same ingestion → refinement → extraction → review → promotion pipeline.

### 1.2 Multi-Layer Verification Model
No fact enters the Canonical layer without clearing three gates:

1. **Deterministic Gate** — rules-based classification, schema validation, and structural matching.
2. **LLM Review Gate** — semantic validation via a local LLM (currently Ollama / `gemma4:31b`), producing a `keep` / `review_further` / `reject` decision with a bounded confidence score.
3. **Governance Gate (Promotion Layer)** — final schema, registry, and type-safety check before the record is written to `003_Canonical-Knowledge-Layer`. **Currently unimplemented; this is the #1 priority of Section 8.**

High-impact or low-confidence candidates additionally escalate to **Tier 3 (human review)** via the Ranger Dashboard payload defined in Phase 1B.

### 1.3 Strategic Principle: Build Bottom-Up
A clean graph is impossible without clean sources. The phase order is not a preference; it is a prerequisite chain:

```
Ingestion & Structure     →  (ground truth — files + parser telemetry)
Refinement / Normalization →  (identity — stable tokens, shapes, slugs)
Candidate Extraction      →  (signals — relationships, concepts)
Review & Validation       →  (governance gate — LLM + human)
Promotion                 →  (admission — canonical storage)
Graph Contract & Indexing →  (structure — queryable relationships)
Query & AI Augmentation   →  (intelligence — on top of validated graph)
```

AI sits **on top of** a deterministic base; it never replaces it. No phase in the stack may consume outputs from a phase whose gates it does not trust.

### 1.4 Core Operating Principles (Non-Negotiable)
These are enforced in code review, by `run_lint`, and in the audits. They are restated here because they constrain every roadmap decision downstream.

| # | Principle | Enforcement Mechanism |
|---|-----------|----------------------|
| P1 | **Filesystem is the database.** No hidden SQLite, Postgres, or pickle state for core lineage. | `run_lint`, `run_reconcile`, PR review |
| P2 | **Raw layer is immutable.** Nothing in `001_Raw-Source-Layer/` is modified, moved, or deleted by pipeline code. | Code review; no write handles in `001` code paths |
| P3 | **Idempotent stages.** Every `run_*` command is safe to re-run. | Registry signature checks |
| P4 | **Path-based traceability.** `001` → `002` → `003` paths mirror each other structurally. | `reconcile.py` |
| P5 | **Deterministic canonicalization.** IDs come from `canonical_rules.yaml`; no inline string matching. | `canonicalize.py` + linter |
| P6 | **Immutable canonical IDs.** Once written, an ID is permanent and requires a formal migration. | `migrate-ids-plan` workflow |
| P7 | **Explicit concept vocabulary.** Relationship extraction may only use concepts that exist in `003/shared/concepts`. | `relationships.py` + `concepts.py` |
| P8 | **Local-first AI.** Cloud LLMs are opt-in only. Review must run air-gapped. | `ollama_review.py` default |
| P9 | **No soft output.** Any extracted candidate without a `source_section_id` is rejected at the validation boundary. | Schema validation (Phase 7) |
| P10 | **No schema-less growth.** New laws are not ingested until the Promotion Layer is validating existing PD 1096 data. | Project policy, Section 8 gate |

Full text and rationale: `/.ai/00_system/principles.md`.

---

## 2. System Architecture Map

Vitruvius is a layered, filesystem-centric pipeline. The numbered layers below are directories on disk; the arrows are stages in `scripts/pipeline_cli.py`.

```
┌──────────────────────────────────────────────────────────────────────┐
│ 001_Raw-Source-Layer          immutable input: PDFs, DOCX, XLSX      │
│           │                                                          │
│           ▼  scan → status → lint                                    │
│ 006_System-Manifests          registries, run reports, snapshots    │
│           │                                                          │
│           ▼  convert / ocr / office / spreadsheets                   │
│ 002_Raw-Conversion-Layer      raw_markdown + sidecar_json            │
│           │                                                          │
│           ▼  refine (Phase 1C — PLANNED)                             │
│           │   Text Refinement Layer: Tier A/B/C rules                │
│           │   .refined.json manifest per document                    │
│           │                                                          │
│           ▼  canonicalize + concepts                                 │
│ 003_Canonical-Knowledge-Layer canonical sources, concepts,           │
│                               shared/relationships (planned)         │
│           │                                                          │
│           ▼  extract-relationships(-sections) + review (Ollama)      │
│ 006_System-Manifests/runs     latest_relationship_review_ollama.json │
│           │                                                          │
│           ▼  promote (Phase 7 — NOT IMPLEMENTED)                    │
│ 003_Canonical-Knowledge-Layer/shared/relationships/                  │
│           │                                                          │
│           ▼  graph-index (Phase 8 — NOT IMPLEMENTED)                 │
│ 005_Operational-Intelligence  graph artifacts, indices, embeddings   │
│           │                                                          │
│           ▼  derive (Phase 9 — NOT IMPLEMENTED)                      │
│ 004_Derived-Content-Layer     summaries, flashcards, explainers      │
└──────────────────────────────────────────────────────────────────────┘
```

Every arrow is implemented by one or more `run_` functions in `scripts/vitruvius/` and is traceable back via registries in `006_System-Manifests/`.

**Authoritative references:**
- `/.ai/00_system/architecture.md` — subsystem breakdown and runtime entry points.
- `/.ai/00_system/pipeline-overview.md` — stage-by-stage execution flow.
- `/.ai/00_system/naming-conventions.md` — file, module, ID, and report naming contracts.

---

## 3. Core Governance Contracts

These contracts are the glue between phases. Any phase that breaks one of them is an outage, not a regression.

### 3.1 Relationship Type Registry (Phase 5 ↔ 6 ↔ 7)
- **Allowed predicates** (closed vocabulary): `governs`, `requires`, `defines`, `depends_on`, `limits`, `affects`, `supersedes`.
- **Compatibility rules:**
  - `governs`: `[Source] → [Concept]`
  - `requires`: `[Concept] → [Concept] | [Concept] → [Attribute]`
  - `defines`: `[Source] → [Concept]`
  - `limits`: `[Source | Section] → [Concept | Attribute]`
  - `depends_on`, `affects`, `supersedes`: `[Concept] ↔ [Concept]` with directed semantics.
- **Storage:** `scripts/vitruvius/rules/relationship_registry.yaml` (to be created in Phase 7).
- **Enforcement:** the Promotion Layer rejects any predicate not in the registry or whose subject/object types violate compatibility.

### 3.2 Ingestion → Refinement Contract (Phase 1B ↔ 1C)
Every document that exits Phase 1B (ingestion) and enters Phase 1C (refinement) MUST carry:

| Field | Type | Purpose |
|---|---|---|
| `source_path` | string | Lineage to raw file |
| `file_type` | enum | `pdf` / `docx` / `xlsx` / `pptx` / `csv` |
| `document_class` | enum | One of the 9 taxonomy classes (see §3.3) |
| `parser_id` | string | Winning parser in the fallback chain |
| `confidence_score` | float [0,1] | Parser-reported quality |
| `pages_total` / `pages_processed` | int | Coverage check |
| `markdown_path` | string | Output path |
| `assets_extracted` | string[] | Provenance only; no semantic interpretation |
| `structural_context` | string[] | e.g., `"Section 804"` |
| `versioning` | object | `parser_version`, `pipeline_version`, `config_version` |
| `manual_review` | object | `{required: bool, reason: string\|null}` |

**Full contract:** `/.ai/03_plans/ingestion-refinement-contract.md` (v2.0.0).
Phase 1C MUST reject any document missing these fields. No defaults, no soft validation.

### 3.3 Document Taxonomy (Phase 1B)
Parser selection is driven by a closed taxonomy, priority-ordered `scanned > hybrid > complex > simple`:

`text_pdf_simple`, `text_pdf_complex`, `hybrid_pdf`, `scanned_pdf_clean`, `scanned_pdf_noisy`, `office_doc`, `office_slide`, `spreadsheet_structured`, `spreadsheet_unstructured`.

Classification is deterministic, driven by measurable signals (`text_density`, `image_density`, `vector_density`, `ocr_confidence`, `table_clues`, `garbled_ratio`). See `/.ai/03_plans/phase-1b-multi-parser-integration-plan.md` §4.

### 3.4 Refinement Rule Tiers (Phase 1C)
All normalization rules are classified by risk:

| Tier | Category | Example | Enforcement |
|---|---|---|---|
| **A** | Lossless | Unicode NFC, control-char removal, whitespace collapse | Always on |
| **B** | Structural | `SEC. 1` → `SECTION 1`, header normalization | Always on for Markdown |
| **C** | Semantic | OCR typo correction, terminology drift fixes | **Opt-in only**; requires audit log and Ranger review |

Rules execute in a phase-locked order (encoding → whitespace → structural → identifiers → data cleanup). `normalize(normalize(x)) == normalize(x)` is a hard contract for Tier A/B.

### 3.5 Promotion Governance Contract (Phase 7)
Every record written to `003_Canonical-Knowledge-Layer/shared/relationships/` MUST contain:
- `source_section_id`, `evidence_snippet`, `confidence_score`
- `review_decision`, `reviewer_model`, `reviewed_at_utc`
- `promotion_batch_id`, `promotion_audit_log_ref`

**Merge policy:** Duplicate triplets `(subject, predicate, object)` merge their evidence arrays rather than duplicating rows. **Auto-promotion:** only for `keep` decisions with `confidence >= 0.90` from the LLM review. **Audit trail:** every promotion run emits `promotion_audit.log`.

### 3.6 Filesystem Graph Contract (Phase 8)
Required node fields: `id`, `type`, `slug`, `trust_level`, `last_updated_utc`.
Required edge fields: `from_id`, `to_id`, `type`, `evidence_id`, `status` (`verified` / `unverified`).
No graph database may be introduced until this contract is frozen and its filesystem-backed implementation passes the Phase 8 gate tests.

---

## 4. Status Reconciliation (Roadmap vs. Audit)

The earlier version of this document claimed several phases were "COMPLETE" that the 2026-04-13 audits (`/.ai/02_audits/`) proved to be **skeletons**. This table is the authoritative truth. Revise this table first when a phase advances — never the individual phase blocks alone.

| Phase | Earlier Claim | Audit Reality | New Status | Evidence |
|---|---|---|---|---|
| 0. Foundation | Complete | Complete | ✅ **COMPLETE** | CLI, layer scaffolding, paths/constants verified |
| 1A. Baseline Ingestion | Complete | Complete; no file hashes; sequential OCR | ✅ **COMPLETE (with known gaps)** | `ingestion-audit.md` |
| 1B. Multi-Parser Integration | Planned | Not started; plan written | 📝 **PLANNED (detailed plan exists)** | `phase-1b-multi-parser-integration-plan.md` |
| 1C. Centralized Normalization | Planned | Not started; normalization is fragmented across 3 modules | 📝 **PLANNED (detailed plan exists)** | `normalization-audit.md`, `phase-1c-centralized-normalization-plan.md` |
| 2. Canonicalization | Complete | Skeleton — wrapper producing YAML frontmatter only; does not generate "Overview", "Coverage", or "Key Points" | 🟡 **PARTIAL (skeleton)** | `codebase-roadmap-audit.md` §3 |
| 3. Concept Layer | Complete (20+ concepts seeded) | Placeholder generator — only writes "X is a defined concept"; no definitions, no regulatory basis | 🟡 **PARTIAL (placeholders)** | `extraction-audit.md` §9 |
| 4. Identity Cleanup | Complete | Complete for text replacement; migration map maintained manually | ✅ **COMPLETE** | `codebase-roadmap-audit.md` |
| 5. Relationship Extraction | Complete (Section-Aware) | Regex-based; section-aware variant exists; **82% rejection rate** at review; technically "primitive" | 🟡 **PARTIAL (regex-grade)** | `extraction-audit.md` §10 |
| 6A. Local LLM Review | Complete ✅ | Implemented and functional; **manual trigger only**, not in `run`; no second pass; no confidence-threshold auto-filter; hardcoded Ollama URL | ✅ **COMPLETE (with known gaps)** | `review-layer-audit.md` |
| 6B. Second-Pass Review | Planned | Not started | 📝 **PLANNED** | — |
| 7. Promotion Governance | Not implemented | Not started; no code in `scripts/vitruvius/` | ❌ **NOT STARTED (top priority)** | Audit confirms |
| 8. Graph Contract & Indexing | Not implemented | Not started | ❌ **NOT STARTED** | — |
| 9. Query & AI Layer | Not implemented | Not started | ❌ **NOT STARTED** | — |
| 10. Canonical Relationship Storage | Not implemented | Folder `003/shared/relationships/` is empty | ❌ **NOT STARTED** | Merged conceptually into Phase 7 |
| 11. Dataset Expansion | Not implemented | Gated on Phase 7 | 🔒 **GATED (do not start)** | Principle P10 |
| 12. AI-Augmented Reasoning | Not implemented | Long-term | 🔒 **GATED (do not start)** | — |

**Honest overall completion:** *ingestion ≈ 90%, refinement ≈ 0%, canonicalization ≈ 30%, concept layer ≈ 15%, extraction ≈ 40%, review ≈ 70%, promotion onwards ≈ 0%*. The project is best described as *late-ingestion / early-extraction*, not *starting Phase 7*.

---

## 5. Honest Position Statement

- **Where we actually are:** Ingestion is functional but unsophisticated. The review layer works end-to-end for a single source but rejects 82% of candidates — which is *both* a sign that the reviewer is doing its job and a sign that the extractor upstream is too noisy.
- **What's keeping us stuck:** Three interlocking gaps. (1) No Promotion Layer, so nothing graduates from `review_ollama.json` into canonical storage. (2) No normalization layer, so extraction feeds the reviewer garbage. (3) Regex extraction, so good signals drown in false positives.
- **What unblocks the next 90 days:** Build Phase 7 on top of the *existing* Ollama review output (not blocked on upstream fixes), in parallel with Phase 1C (normalization) to reduce the 82% rejection rate. Phase 1B (multi-parser) follows.
- **What must NOT happen next:** expanding the corpus (Phase 11), adding new concepts without enrichment (Phase 3C), or starting graph database work (Phase 8) before the filesystem graph contract is frozen.

---

## 6. Phase Contracts

Every phase below follows the same contract template. A phase is not "done" until every item in its **Definition of Done** is checked, every **Gating Metric** is passing, and its deliverables are linked in `.ai/10_state/decisions.md`.

---

### Phase 0 — Repository and Pipeline Foundation · ✅ COMPLETE

**Objective.** Establish the layered filesystem contract and CLI orchestrator.

**Deliverables.**
- Layered root structure `001_` through `006_`.
- `scripts/pipeline_cli.py` with `scan`, `status`, `lint`, `run` commands.
- `scripts/vitruvius/paths.py` and `constants.py` enforcing the filesystem contract.
- `config/vitruvius.yaml` for system-wide configuration.

**Definition of Done.** All four deliverables present; `run` command executes end-to-end on an empty raw layer without error.

---

### Phase 1A — Baseline Ingestion · ✅ COMPLETE (with known gaps)

**Objective.** Convert PDF, Office, and Spreadsheet inputs into Markdown + JSON sidecars.

**Deliverables (verified).**
- `scanner.py`, `detection.py`, `conversion.py` — PDF pipeline via `opendataloader_pdf`.
- `office.py` — DOCX/PPTX via `soffice` (LibreOffice).
- `spreadsheets.py` — XLSX via `openpyxl`.
- `ocr.py` — OCR pathway via `ocrmypdf`.
- Conversion registry at `006_System-Manifests/registries/latest_conversion_registry.csv`.

**Known gaps (carried as technical debt, not blockers).**
- No file hashing (only size + mtime signatures).
- No staging directory; direct pipeline.
- Sequential OCR — no parallelization.
- Registry grows unbounded; no rotation.
- `Word-PPT-To-PDF.py` legacy naming inconsistency.

**Gating metrics for "done".** `run_scan` + `run_convert` executes over the PD 1096 corpus with zero unhandled exceptions. ✅ Verified 2026-04-13.

**References.** `/.ai/02_audits/ingestion-audit.md`.

---

### Phase 1B — Multi-Parser Integration · 📝 PLANNED

**Objective.** Replace single-path parsing with a classified, fallback-chained parser orchestrator that emits strict telemetry and a provenance sidecar. Reduce upstream noise so that downstream refinement and extraction do not have to compensate.

**Prerequisites.** Phase 1A complete. Plan `/.ai/03_plans/phase-1b-multi-parser-integration-plan.md` accepted.

**Deliverables.**
1. **`BaseParser` interface** + `ParserOrchestrator` honoring the taxonomy in §3.3 and the fallback chains in `phase-1b-multi-parser-integration-plan.md` §5.
2. **Document taxonomy classifier** (deterministic, threshold-driven — no ML).
3. **Parser implementations**: wrap existing `opendataloader`; add `Docling`, `Marker`, `Surya`; integrate `OCR preprocessor` and `LibreOffice preprocessor`.
4. **Strict telemetry JSON** (flattened schema in plan §6) per parser attempt.
5. **Quality gates**: Gate-001 (UTF-8), Gate-002 (volume ≥500 chars), Gate-003 (≥1 header if pages>5), Gate-004 (Office sanity).
6. **Fallback orchestration** with page-level isolation for OOM/timeout cases.
7. **Dynamic resource allocation** via `ProcessPoolExecutor` with per-class memory buckets.
8. **Manual Review Lane** + Ranger Audit Payload generator.
9. **Golden Corpus Benchmark** (30 documents: 10 simple / 10 complex / 10 scanned).

**Definition of Done.**
- [ ] Every Phase 1A parser call routes through the orchestrator.
- [ ] 100% of documents processed on the golden corpus emit a schema-valid telemetry sidecar.
- [ ] Fallback chain correctness verified on injected failures.
- [ ] `FALLBACK_EXHAUSTED` and `MANUAL_REVIEW_REQUIRED` states produce a Ranger Audit Payload with all six required sections.
- [ ] Versioning (`parser_version`, `pipeline_version`, `config_version`) present in every sidecar.

**Gating metrics.**
- `validation_failure_rate` < 5% on the golden corpus.
- `timeout_rate` < 2%.
- `encoding_error_count` == 0.
- `page_coverage_mean` ≥ 0.97 on text-class documents.

**Key risks.** Parser licensing friction (Docling/Marker); OOM on hybrid PDFs; hallucinated content from over-eager OCR engines (mitigated by the "hallucination trap" heuristic in §7.1 of the plan).

**Non-goals.** Semantic interpretation of extracted images; relationship extraction; visual diagram understanding.

**References.** `/.ai/03_plans/phase-1b-multi-parser-integration-plan.md`.

---

### Phase 1C — Centralized Normalization (Text Refinement Layer) · 📝 PLANNED

**Objective.** Eliminate fragmented normalization (currently duplicated across `utils.py`, `relationships_sections.py`, `canonicalize.py`) by building a formal Text Refinement Layer between Phase 1B (ingestion) and Phase 2 (canonicalization), with tier-based safety classification and phase-locked execution order.

**Prerequisites.** Phase 1B telemetry contract frozen (even if implementation is in flight) — 1C validates 1B output on entry.

**Deliverables.**
1. **`NormalizationEngine`** enforcing phase-locked execution and scope routing.
2. **`NormalizationRule` protocol** with fields `name`, `tier` (A/B/C), `phase` (1–5), `scope[]`, `gated_by[]`, `is_deterministic`.
3. **Tier A/B/C rule set** per `phase-1c-centralized-normalization-plan.md` §5.
4. **Five-phase execution pipeline**: encoding → whitespace → structural (+ semantic chunking) → identifiers → data cleanup.
5. **Semantic chunking** producing `section_depth` + `semantic_block` markers, token-aware (≤512 tokens/block), table-isolated during whitespace phase.
6. **`.refined.json` manifest sidecar** per document (flattened schema in plan §7).
7. **Destructive transformation guard** with per-class thresholds (10% / 15% / 30%).
8. **Contract validator** rejecting any Phase 1B output missing required metadata fields.
9. **CLI**: `python scripts/pipeline_cli.py refine` as a first-class stage between `convert` and `canonicalize`.
10. **Slug/ID collision policy** with hash-based disambiguation; alias registry; incremental numbering prohibited.

**Definition of Done.**
- [ ] All existing normalization call sites removed from `utils.py`, `relationships_sections.py`, `canonicalize.py`.
- [ ] `normalize(normalize(x)) == normalize(x)` verified by automated tests for every Tier A and Tier B rule.
- [ ] Refinement manifest schema validates against the golden corpus.
- [ ] `refine` stage integrated into `pipeline_cli.py` dispatch.
- [ ] Destructive-guard rollback triggers on synthetic inputs and flags `MANUAL_REVIEW_REQUIRED`.
- [ ] Tier C rules require explicit opt-in and emit audit events.

**Gating metrics.**
- `idempotency_failure_rate` == 0 for Tier A/B rules.
- `contract_violation_rate` < 1% (Phase 1B handoff).
- `structural_corruption_count` == 0 (no broken tables/lists).
- `encoding_failure_rate` == 0.

**Key risks.** Normalization too aggressive → semantic loss; too conservative → 82% rejection persists; table handling regressions during whitespace phase (mitigated by table isolation protocol).

**Non-goals.** Entity/relationship extraction; visual interpretation; semantic rewrite; database persistence.

**References.** `/.ai/03_plans/phase-1c-centralized-normalization-plan.md`, `/.ai/02_audits/normalization-audit.md`.

---

### Phase 2 — Canonicalization Engine · 🟡 PARTIAL (SKELETON)

**Objective.** Transform refined Markdown into canonical source files with strict IDs, frontmatter, and structured sections.

**Current state (audit-verified).**
- ✅ Rules engine (`canonical_rules.yaml`) exists and is used.
- ✅ ID standard (`<prefix>-<slug>`) enforced.
- 🟡 `canonicalize.py` only generates frontmatter + header; it does not produce the "Overview", "Coverage", or "Key Points" sections shown in the existing hand-curated canonical files. The current script is a regression from an earlier tool.

**Remaining work.**
1. Restore or rebuild structured-section generation (Overview / Coverage / Key Points / Referenced Concepts).
2. Wire canonicalization to the new Phase 1C refined Markdown + semantic blocks.
3. Add a `canonicalize` batch mode (currently `-one` only).
4. Frontmatter schema validation at write time.

**Definition of Done.**
- [ ] `run_canonicalize` produces canonical files indistinguishable in structure from the existing hand-curated set.
- [ ] Batch canonicalization runs over the PD 1096 refined outputs without frontmatter schema violations.
- [ ] Any regression against the golden canonical corpus is caught by automated diff testing.

**Gating metrics.**
- Frontmatter schema validation pass rate == 100%.
- Structural-section presence rate ≥ 95% of canonicalized documents.

**Key risks.** Drift from previously hand-curated canonical files; silent overwrites of manual edits (mitigated by `canonical_status` frontmatter + diff-before-write).

**References.** `/.ai/02_audits/codebase-roadmap-audit.md` §3.

---

### Phase 3 — Concept Layer · 🟡 PARTIAL (PLACEHOLDERS)

**Objective.** Promote concept files from placeholders to "Knowledge Nodes" carrying definition, regulatory basis, aliases, and cross-references.

**Current state.**
- ✅ `concepts.py` generates properly formatted YAML frontmatter files.
- 🟡 Content is a placeholder sentence: *"X is a defined concept within the Vitruvius system."*

**Remaining work (3C Concept Enrichment).**
1. **Definition extraction.** Pull definitions from PD 1096 §3 and IRR glossaries where a matching concept exists.
2. **Regulatory basis linkage.** Every concept links back to at least one source section ID.
3. **Alias registry.** Auto-populate aliases from document headers ("Also known as…"), and allow manual curation.
4. **Cross-references.** Bidirectional concept-to-concept links where justified by the document.
5. **`concept_status` frontmatter field** with values `placeholder` / `draft` / `enriched` / `verified`.

**Definition of Done.**
- [ ] No concept with `concept_status: placeholder` remains in `003/shared/concepts/` for the PD 1096 core vocabulary.
- [ ] Every `enriched` concept has ≥1 `source_section_id` pointer and ≥1 evidence snippet.
- [ ] Alias registry populated for at least the 20 seeded PD 1096 concepts.

**Gating metrics.**
- Placeholder-to-enriched conversion rate per week.
- Evidence coverage (% concepts with ≥1 source pointer).

**Key risks.** Free-text concept drift (mitigated by principle P7); alias collisions (mitigated by Phase 1C collision policy).

---

### Phase 4 — Identity Cleanup & Migration · ✅ COMPLETE

**Objective.** Align legacy IDs with the `<prefix>-<slug>` standard.

**Status.** Complete for text-replacement semantics; migration map maintained in `scripts/vitruvius/rules/id_migration_map.yaml`.

**Open item.** Future ID changes must go through `migrate-ids-plan` → `migrate-ids-apply` (never find-and-replace). This is a permanent operating rule, not a phase to repeat.

---

### Phase 5 — Relationship Extraction · 🟡 PARTIAL (REGEX-GRADE)

**Objective.** Identify candidate relationships between sources, sections, and concepts, with strict section-anchored evidence.

**Current state.**
- ✅ `relationships.py` regex extractor (patterns for `is_of`, `relates_to`, `depends_on`).
- ✅ `relationships_sections.py` section-aware variant — every candidate carries `source_section_id`.
- ✅ Deduplication implemented.
- 🟡 Regex-only; 82% of candidates are rejected by the LLM review layer.

**Remaining work.**
1. **Section-anchored extractor (Phase 5D)** — already exists; verify evidence-context preservation across all candidates.
2. **LLM-assisted candidate generation (Phase 5E — new)** — use the local LLM to propose candidates in addition to regex, with schema-enforced output. **Gated on Phase 6B being in place** to avoid multiplying noise.
3. **Pattern expansion for IRR-specific phrasings** when IRR support begins (Phase 11, gated).

**Definition of Done (Phase 5 as a whole).**
- [ ] 100% of candidates carry `source_section_id` and `evidence_snippet`.
- [ ] False-positive rate (Gemma review `reject` with confidence ≥0.85) drops below 50% after Phase 1C lands.
- [ ] Candidate schema matches what Phase 6 reviewers expect, byte-for-byte.

**Gating metrics.**
- Extraction rejection rate (target: <50% after 1C, <30% after 5E).
- Null `source_section_id` rate == 0.

**References.** `/.ai/02_audits/extraction-audit.md`.

---

### Phase 6 — Review & Validation Layer

#### Phase 6A — Local LLM Review · ✅ COMPLETE (with gaps)

**Objective.** Validate regex-extracted candidates using a local LLM, producing `keep` / `review_further` / `reject` decisions with confidence scoring.

**Current state (audit-verified 2026-04-13).**
- ✅ `ollama_review.py` (345 lines) — HTTP calls to Ollama `/api/generate`.
- ✅ `gemma4:31b` default model; configurable via `--model`.
- ✅ Three-decision output with clamped confidence [0,1].
- ✅ Interruption-safe with partial saves.
- 🟡 **Not in the default pipeline** — manual trigger only.
- 🟡 **No automatic confidence-threshold filtering** (counts high-confidence bins but does not act on them).
- 🟡 **Ollama URL hardcoded** — no config file support.
- 🟡 **Sequential only**; no parallelization.
- 🟡 **No per-candidate retry**; no model fallback.
- 🟡 **No resume** (saves progress but does not resume from it on relaunch).

**Gap closure (required before Phase 7 can auto-consume):**
1. Move the Ollama URL to `config/vitruvius.yaml`.
2. Add resume-from-progress on relaunch.
3. Add per-candidate retry with bounded attempts (3).
4. Emit a separate `latest_relationship_review_high_confidence.json` that Phase 7 consumes directly.

**Definition of Done for 6A.**
- [x] Review works end-to-end on PD 1096 corpus.
- [ ] Four gap-closure items above completed.

**References.** `/.ai/02_audits/review-layer-audit.md`.

#### Phase 6B — Second-Pass Review (Two-Stage Adjudication) · 📝 PLANNED

**Objective.** Minimize false consensus and reduce compute by routing only uncertain cases through a second model.

**Tiered architecture.**
- **Tier 1 (`gemma4:31b`):** Primary reviewer. `keep` with confidence ≥0.90 and `reject` with confidence ≥0.90 are accepted/suppressed provisionally.
- **Tier 2 (`qwen3:30b` or smaller):** Second pass — runs only for `review_further`, low-confidence `keep`/`reject`, and predicate-type disagreements.
- **Tier 3 (Human):** Escalation for Gemma/Qwen disagreements, high-impact legal edges, and persistent ambiguity. Reuses the Ranger Audit Payload format.

**Deliverables.**
1. `review-relationships-ollama-second-pass` CLI command.
2. Filter step that selects uncertain candidates from Gemma output.
3. Merged adjudication report with both reviewers' decisions and an agreement matrix.
4. Human-escalation worklist writer.

**Definition of Done.**
- [ ] Second-pass reduces `review_further` volume by ≥70%.
- [ ] Agreement matrix computed and logged per run.
- [ ] Human worklist file materially reviewable by a domain expert.

**Gating metrics.**
- Model disagreement rate (expected 10–20% on the uncertain subset).
- Human-escalation rate <5% of all candidates.

---

### Phase 7 — Promotion Governance · ❌ NOT STARTED · 🔥 HIGHEST PRIORITY

**Objective.** Transfer LLM-approved relationship records into canonical storage under the governance contract in §3.5.

**Prerequisites.** Phase 6A gap-closure items 1 & 4 (Ollama config + high-confidence output file). Nothing else; this is deliberately unblocked.

**Deliverables.**
1. **`scripts/vitruvius/promotion.py`** module with `run_promote` CLI command.
2. **`promotion_validator.py`** enforcing the §3.5 schema.
3. **`scripts/vitruvius/rules/relationship_registry.yaml`** — the closed vocabulary + compatibility rules from §3.1.
4. **Canonical relationship file format** under `003_Canonical-Knowledge-Layer/shared/relationships/` (one file per source document, YAML frontmatter + Markdown body).
5. **Merge logic** for duplicate triplets `(subject, predicate, object)` — evidence arrays merge, not rows.
6. **Audit log writer** producing `promotion_audit.log` per batch.
7. **Dry-run mode** (`--dry-run`) that reports what would change without writing.
8. **Rollback mode** (`--rollback <batch_id>`) keyed on audit log batch IDs.

**Definition of Done.**
- [ ] First three PD 1096 relationships land in `003/shared/relationships/` with passing schema validation.
- [ ] Registry rejects any predicate not in the allowed set.
- [ ] Merge logic verified on synthetic duplicate candidates.
- [ ] Promotion batch appears in `promotion_audit.log` with idempotent re-run behavior.
- [ ] Dry-run and rollback both functional.

**Gating metrics.**
- Schema validation pass rate == 100%.
- Registry rejection rate == 0 on verified `keep` inputs.
- Audit log completeness == 100% (every write has an audit entry).

**Key risks.** Silent overwrite of manually curated relationship files (mitigated by `canonical_status` check + dry-run default); audit log corruption (mitigated by append-only writes + periodic snapshots).

**Non-goals.** Graph indexing (Phase 8); query interface (Phase 9); cross-document reconciliation.

---

### Phase 8 — Graph Contract & Indexing · ❌ NOT STARTED

**Objective.** Build the first queryable index over promoted relationships, backed by the Filesystem Graph Contract (§3.6).

**Prerequisites.** Phase 7 producing at least 50 verified relationships with the promotion audit log in place.

**Deliverables.**
1. **`graph_contract.py`** — schema validator for nodes and edges.
2. **Filesystem graph builder** — indices in `005_Operational-Intelligence-Layer/graph/`.
3. **JSON graph artifact**: `latest_graph_snapshot.json` with node and edge arrays.
4. **Graph traversal library** — typed, evidence-aware traversal helpers.
5. **CLI**: `build-graph`, `query-graph`, `export-graph-snapshot`.
6. **Integrity checks**: orphan detection, dangling edge detection, type compatibility.

**Definition of Done.**
- [ ] PD 1096 verified relationships render as a connected graph with zero orphans and zero contract violations.
- [ ] Traversal library supports: neighbors, typed edges, evidence-joined paths.
- [ ] Graph snapshot is deterministic (same inputs → same output, byte-for-byte).

**Gating metrics.**
- Orphan rate == 0.
- Contract violation count == 0.
- Snapshot determinism test passes.

**Explicit non-goal.** No Neo4j, Dgraph, or other external graph DB yet. The filesystem implementation must freeze the contract first.

---

### Phase 9 — Query & AI Augmentation · ❌ NOT STARTED

**Objective.** Enable high-fidelity, evidence-linked domain queries: *"What governs X?"*, *"Which sections affect building permits?"*.

**Prerequisites.** Phase 8 graph stable; ≥200 verified relationships.

**Deliverables.**
1. **Structured query interface** — typed query functions over the filesystem graph.
2. **Natural-language front-end** (optional) — converts NL queries to structured queries via the local LLM, NEVER free-generating answers.
3. **Source-traceable answers** — every response links back to a canonical source file with a section ID.
4. **Confidence-aware output** — queries surface the confidence of each supporting edge.
5. **CLI**: `query "what governs building permits?"`.

**Definition of Done.**
- [ ] Ten seed questions answered with ≥95% source-citation accuracy.
- [ ] Every answer contains at least one `source_section_id` link.
- [ ] Answer latency < 2s for local graph traversal queries.

**Non-goal.** Hallucination-capable free-text answers.

---

### Phase 10 — Canonical Relationship Storage
**Status.** Merged conceptually into Phase 7. The storage format *is* the Phase 7 deliverable. Retained in the tracker as a pointer; no separate phase work.

---

### Phase 11 — Dataset Expansion · 🔒 GATED

**Objective.** Expand beyond PD 1096 into the IRR, occupancy tables, lighting/ventilation sections, and additional Philippine building laws.

**Gate condition.** **Do not start** until:
- Phase 7 is stably validating existing PD 1096 data (at least 100 promoted relationships, zero audit violations for a full week).
- Phase 1B and 1C are shipping — new documents must enter through the hardened pipeline.

**Priority order once gated.**
1. PD 1096 IRR.
2. Occupancy tables (structured spreadsheet pathway).
3. Lighting & ventilation sections.
4. Additional laws and regulations.

---

### Phase 12 — AI-Augmented Reasoning · 🔒 GATED

**Objective.** Layer AI on top of a clean graph: concept enrichment suggestions, semantic linking proposals, question generation, wiki drafting, learning-path generation.

**Gate condition.** Phase 9 (query layer) in production with ≥95% citation accuracy, and a stable set of ≥500 verified relationships.

**Non-negotiable constraint.** AI sits on top of the graph; it never replaces it. Every AI-generated artifact must be reviewable against canonical sources, and nothing AI-generated may write to `003_Canonical-Knowledge-Layer/` without passing the Promotion Gate.

---

## 7. Dependency Graph

```
              ┌───────────────┐
              │ Phase 0       │
              │ Foundation    │
              └──────┬────────┘
                     ▼
              ┌───────────────┐
              │ Phase 1A      │
              │ Baseline      │
              │ Ingestion     │
              └──────┬────────┘
                     │
           ┌─────────┴─────────┐
           ▼                   ▼
    ┌──────────┐        ┌────────────┐
    │ Phase 1B │ ◀────▶ │ Phase 1C   │  (1B and 1C cross-validate via
    │ Multi-   │        │ Refinement │   the §3.2 contract; each must
    │ Parser   │        │ Layer      │   freeze that contract to ship.)
    └────┬─────┘        └─────┬──────┘
         │                    │
         └──────────┬─────────┘
                    ▼
            ┌───────────────┐
            │ Phase 2       │
            │ Canonicaliza- │
            │ tion (rebuild)│
            └──────┬────────┘
                   ▼
         ┌──────────────────┐
         │ Phase 3 Concepts │
         │ (enrichment)     │
         └──────┬───────────┘
                ▼
         ┌──────────────────┐
         │ Phase 5          │
         │ Relationship     │
         │ Extraction       │
         └──────┬───────────┘
                ▼
         ┌──────────────────┐            ┌─────────────────┐
         │ Phase 6A         │──────────▶ │ Phase 6B        │
         │ LLM Review       │            │ Second-Pass     │
         │ (gap closure)    │            │ Review          │
         └──────┬───────────┘            └────────┬────────┘
                │                                 │
                └────────────────┬────────────────┘
                                 ▼
                        ┌────────────────┐
                        │ Phase 7        │  ◀── CRITICAL GATE
                        │ Promotion      │
                        │ Governance     │
                        └──────┬─────────┘
                               ▼
                        ┌────────────────┐
                        │ Phase 8        │
                        │ Graph Contract │
                        │ & Indexing     │
                        └──────┬─────────┘
                               ▼
                        ┌────────────────┐
                        │ Phase 9        │
                        │ Query & AI     │
                        └──────┬─────────┘
                               ▼
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
         ┌──────────────┐           ┌────────────────┐
         │ Phase 11     │           │ Phase 12       │
         │ Dataset      │           │ AI Reasoning   │
         │ Expansion    │           │ (long-term)    │
         └──────────────┘           └────────────────┘
```

**Phase-4 identity cleanup** is an operating rule, not a node — it applies whenever an ID needs migration.

---

## 8. 90-Day Execution Sequence (Strict Order)

This section supersedes any prior "Next Actions" list. Items are ordered by dependency, not preference. **Do not reorder without updating §7 and §4.**

### Sprint A — Unblock Promotion (weeks 1–2) 🔥
**Goal:** Land Phase 7 on top of the *existing* Ollama review output. This is the highest-leverage move: it starts exercising the Promotion contract immediately and does not require any upstream fix.

1. **Phase 6A gap closure (minimal):** move Ollama URL to `config/vitruvius.yaml`; add `latest_relationship_review_high_confidence.json` writer. (1–2 days)
2. **Phase 7 spec:** create `relationship_registry.yaml` with the §3.1 registry. (0.5 day)
3. **Phase 7 validator:** build `promotion_validator.py` enforcing §3.5. (1–2 days)
4. **Phase 7 writer:** build `run_promote` — dry-run default, audit log, merge logic. (3–4 days)
5. **Golden path:** promote the first 3 PD 1096 relationships end-to-end. (0.5 day)
6. **Decision log entry** in `/.ai/10_state/decisions.md` recording the shape of the first promoted records.

**Exit criteria:** Sprint A is done when three canonical relationship files exist in `003/shared/relationships/` and `promotion_audit.log` records the batch.

### Sprint B — Shrink the 82% Rejection Rate (weeks 3–6)
**Goal:** Reduce upstream noise so Phase 7's auto-promotion threshold is meaningful.

1. **Phase 1C Core Engine** — `NormalizationEngine` + Tier A rules + idempotency tests. (week 3)
2. **Phase 1C Refactoring** — unify slugification + whitespace handling across existing modules. (week 3–4)
3. **Phase 1C Manifests + `refine` CLI stage.** (week 4)
4. **Phase 1C Destructive guard + golden-set validation.** (week 5)
5. **Phase 6A full gap closure** — resume support, retry, per-candidate timeout. (week 5)
6. **Re-run PD 1096 through refine → extract → review** and measure the new rejection rate. (week 6)

**Exit criteria:** Rejection rate <50%, idempotency_failure_rate == 0, contract_violation_rate <1%.

### Sprint C — Harden the Front End (weeks 7–12)
**Goal:** Make ingestion worthy of the corpus expansion in Phase 11.

1. **Phase 1B Foundation** — `BaseParser`, `ParserOrchestrator`, taxonomy classifier, wrap existing parsers. (weeks 7–8)
2. **Phase 1B Modernization** — integrate Docling / Marker / Surya / OCR preprocessor / LibreOffice preprocessor. (weeks 8–10)
3. **Phase 1B Governance** — `ProcessPoolExecutor`, golden corpus benchmark, registry sidecars. (week 11)
4. **Phase 6B Second-Pass Review** — Qwen adjudication, agreement matrix, human escalation worklist. (week 11–12)
5. **Phase 2 restoration** — rebuild structured-section generation in `canonicalize.py`. (week 12, in parallel)

**Exit criteria:** 1B and 1C both shipping; 6B producing agreement matrices; Phase 7 consuming the full pipeline end-to-end without manual intervention.

### After Sprint C
- **Phase 3 enrichment** can start once Phase 2 can generate the supporting structural sections.
- **Phase 8 graph indexing** starts once Phase 7 has ≥50 verified relationships.
- **Phase 11 corpus expansion** remains gated until all Sprint B and C exit criteria hold.

---

## 9. KPIs and Health Indicators

Track weekly in `/.ai/05_logs/` (format TBD). Any red indicator escalates to a §11 review.

| KPI | Target | Red Line | Source |
|---|---|---|---|
| Ingestion coverage (pages successfully converted / total pages) | ≥97% | <90% | `latest_conversion_registry.csv` |
| Parser fallback exhaustion rate | <5% | >10% | Phase 1B telemetry |
| Refinement idempotency failures | 0 | >0 | Phase 1C manifest |
| Refinement destructive rollbacks | <2% | >5% | `.refined.json` manifests |
| Extraction rejection rate (Gemma) | <50% post-1C | >70% | `latest_relationship_review_ollama.json` |
| Auto-promote rate (keep, conf≥0.90) | >30% | <10% | Phase 7 audit log |
| Promotion schema violations | 0 | >0 | Phase 7 audit log |
| Orphan nodes in graph | 0 | >0 | Phase 8 integrity check |
| Query citation accuracy | ≥95% | <90% | Phase 9 query tests |
| Pipeline idempotency (double-run diff) | 0-byte | any diff | `run_reconcile` |

---

## 10. Known Technical Debt & Risks

Carried forward from `/.ai/10_state/known_issues.md` and the 2026-04-13 audits. These are *acknowledged*, not *ignored*.

| ID | Risk | Owner | Mitigation |
|---|---|---|---|
| RI-001 | Filesystem coupling | Architecture | Keep all path logic in `paths.py`; prohibit inline paths in code review |
| RI-002 | Regex extraction fragility | Extraction | Phase 1C reduces input noise; Phase 5E optional LLM-assisted extraction |
| RI-003 | Ollama dependency | Review | Config-driven URL (Sprint A); add health check before batch start |
| RI-005 | Legacy naming inconsistencies (`Word-PPT-To-PDF.py`) | Cleanup | Rename under `migrate-ids-plan` in a dedicated cleanup PR |
| RI-006 | Manual promotion gap | Promotion | **Closed by Phase 7** |
| RI-007 | Normalization fragmentation | Refinement | **Closed by Phase 1C** |
| RI-008 *(new)* | Registry growth (no rotation) | Infra | Add `rotate-registries` CLI (post-Sprint C) |
| RI-009 *(new)* | No file hashing in ingestion | Infra | Add SHA-256 to `scanner.py` in Sprint C |
| RI-010 *(new)* | `concepts.py` produces placeholder content | Concept layer | Addressed in Phase 3 enrichment |
| RI-011 *(new)* | Canonicalizer is a regression from earlier tooling | Canonical | Addressed in Phase 2 restoration |

---

## 11. Cadence, Ownership, Review Process

- **Owner.** Senior Systems Architect (see changelog).
- **Review cadence.** Every 2 weeks. Update §4 status table and §8 sprint exit criteria; re-check KPIs in §9.
- **When to revise this document.**
  1. Any phase changes status.
  2. A new audit supersedes a prior audit.
  3. A contract (§3) changes.
  4. A sprint exit criterion is hit.
- **How to revise.** Bump the version in the header, update the relevant section, and record the change in `/.ai/10_state/decisions.md` with an `AD-XXX` entry. Do not rewrite silently — this document has archaeological value.
- **Conflict resolution.** If this document disagrees with any README, wiki page, or `current-phase.md`, **this document wins** until a reconciliation PR updates both.

---

## 12. Strategic Warnings & Non-Goals

### Strategic Warnings (load-bearing)
- **No "soft output."** Any extraction lacking `source_section_id` is rejected at the validation boundary. (Principle P9)
- **No "schema-less growth."** New laws wait until Phase 7 is validating existing PD 1096 data. (Principle P10)
- **Local-first, always.** The core review loop must run air-gapped. Cloud LLMs are opt-in alternatives only. (Principle P8)
- **Immutable canonical IDs.** Any ID change goes through `migrate-ids-plan`, never find-and-replace.
- **No silent transformation.** Every Tier C rule emits an audit event with the original/mutated pair.

### Explicit Non-Goals (system-wide)
- Free-form text generation that is not source-cited.
- Replacing the deterministic core with a neural model.
- 3D scene generation, visual interpretation, image caption generation, or diagram understanding. (Refinement plan v2 §18 — *"purged 3D/GLB contamination on 2026-04-14"*.)
- Cloud-only operation modes.
- Database-backed persistence for the core lineage (the filesystem is the database).
- Cross-domain universal knowledge extraction — Vitruvius is domain-disciplined.

---

## 13. Reference Index

**System docs.** `/.ai/00_system/architecture.md`, `/.ai/00_system/principles.md`, `/.ai/00_system/pipeline-overview.md`, `/.ai/00_system/naming-conventions.md`.

**Audits (2026-04-13).** `codebase-roadmap-audit.md`, `ingestion-audit.md`, `extraction-audit.md`, `normalization-audit.md`, `review-layer-audit.md`.

**Plans & contracts.** `phase-1b-multi-parser-integration-plan.md`, `phase-1c-centralized-normalization-plan.md`, `ingestion-refinement-contract.md`.

**State.** `/.ai/10_state/active_context.md`, `/.ai/10_state/decisions.md`, `/.ai/10_state/known_issues.md`.

**Schemas (stubs — to be populated).** `/.ai/06_specs/source-schema.md`, `/.ai/06_specs/concept-schema.md`, `/.ai/06_specs/relationship-schema.md`.

---

## Changelog

- **2026-04-14 · v2.0.0** — Full rewrite. Reconciled status against the 2026-04-13 audit pack (ingestion, extraction, normalization, review-layer, codebase-roadmap). Integrated Phase 1B Multi-Parser plan, Phase 1C Refinement plan, and the Ingestion-Refinement Contract. Added governance contract section (§3), dependency graph (§7), 90-day sprint sequence (§8), KPI table (§9), and cadence protocol (§11). Corrected inflated "complete" claims in Phases 2, 3, and 5 to match audit reality. Added non-goals and strategic warnings explicitly. — *Senior Systems Architect*
- **2026-04-13 · v1.x** — Prior version with inflated Phase 2/3/5 claims. Retained in git history.

**Timestamp:** 2026-04-14T02:49:00Z
