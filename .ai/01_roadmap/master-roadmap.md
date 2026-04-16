# Vitruvius — Master Roadmap

> **Document type:** Strategic roadmap + phase contract.
> **Audience:** Architects, engineers, auditors, and autonomous agents operating on this repo.
> **Authoritative for:** Phase order, definitions of done, gating metrics, status reconciliation.
> **Supersedes:** Prior phase lists, ad-hoc README roadmaps, and any conflicting status claims.
> **Version:** 2.3.0 · **Last revised:** 2026-04-15T19:00:00+08:00 · **Next review due:** 2026-05-01
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
Vitruvius is a **local-first, governance-first, domain-agnostic knowledge engine** that converts heterogeneous professional-domain sources (statutes, codes, technical standards, clinical guidelines, engineering specs, reference material) into a **validated, queryable knowledge graph**. It is not a RAG wrapper. It enforces a hard boundary between *raw text*, *candidate signals*, and *canonical truth*, and treats every transformation as auditable.

**Positioning.** Vitruvius is optimized as a **professional-domain specialist** — a tool for fields where precision matters more than coverage. Target domains include architecture & the built environment, engineering (civil / structural / mechanical / electrical), medicine & clinical practice, law & regulatory compliance, and science & academia. The core pipeline is corpus-agnostic: porting to a new domain is a matter of swapping the contents of `001_Raw-Source-Layer/`, the rules under `scripts/vitruvius/rules/`, and the concept vocabulary under `003_Canonical-Knowledge-Layer/shared/concepts/`.

**Active reference corpus.** **Philippine building laws and regulations** (PD 1096 and its IRR). PD 1096 is the benchmark the tests, audits, and per-sprint decision-log numbers are measured against — not the product scope. The README's "Adapting Vitruvius to a new professional domain" section is the operating recipe for a second-domain port.

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
| P10 | **No schema-less growth.** A new corpus (a second jurisdiction's building code, a new medical specialty's guidelines, a new code of practice) is not ingested until the Promotion Layer is validating existing reference-corpus data. | Project policy, Section 8 gate |

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

**Full contract:** `/.ai/09_archive/plans/ingestion-refinement-contract.md` (v2.0.0, archived 2026-04-15 — still frozen and authoritative for the Phase 1B ↔ Phase 1C interface).
Phase 1C MUST reject any document missing these fields. No defaults, no soft validation.

### 3.3 Document Taxonomy (Phase 1B)
Parser selection is driven by a closed taxonomy, priority-ordered `scanned > hybrid > complex > simple`:

`text_pdf_simple`, `text_pdf_complex`, `hybrid_pdf`, `scanned_pdf_clean`, `scanned_pdf_noisy`, `office_doc`, `office_slide`, `spreadsheet_structured`, `spreadsheet_unstructured`.

Classification is deterministic, driven by measurable signals (`text_density`, `image_density`, `vector_density`, `ocr_confidence`, `table_clues`, `garbled_ratio`). See `/.ai/09_archive/plans/phase-1b-multi-parser-integration-plan.md` §4 (archived 2026-04-15 after Phase 1B shipped).

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
| 1C. Centralized Normalization | Planned | **MVP shipped 2026-04-14** — NormalizationEngine with 5 Tier A + 3 Tier B rules + `refine` CLI + `.refined.json` manifest. 6 PD 1096 files refined with real-data idempotency. Tier C, semantic chunking, destructive guard deferred. | ✅ **MVP COMPLETE** | `phase-1c-centralized-normalization-plan.md` (archived) |
| 2. Canonicalization | Complete | **Restored 2026-04-14** — structured section generation (Overview/Coverage/Key Points/Referenced Concepts) + diff-before-write protection with volatile-field stripping + batch CLI. | ✅ **COMPLETE** | `phase-2-canonicalizer-restoration-plan.md` (archived) |
| 3. Concept Layer | Complete (20+ concepts seeded) | **16/20 enriched 2026-04-14** via deterministic extractors (anchor + section-title + 14-entry alias dict + compound-title multi-match), zero LLM calls. 4 concepts still await inline phrase-density extraction. | ✅ **COMPLETE (80% coverage, deterministic)** | `concept_definitions.py`, `concept_enrichment.py`, AD-019, AD-020 |
| 4. Identity Cleanup | Complete | Complete for text replacement; migration map maintained manually | ✅ **COMPLETE** | `codebase-roadmap-audit.md` |
| 5. Relationship Extraction | Complete (Section-Aware) | Regex-based; section-aware variant exists; **82% rejection rate** at review; technically "primitive" | 🟡 **PARTIAL (regex-grade)** | `extraction-audit.md` §10 |
| 6A. Local LLM Review | Complete ✅ | **Gap-closed 2026-04-14** — config-driven URL, high-confidence writer, bounded retries with wall-clock cap, resume-from-in-progress, opt-in parallelization, warmup, `run-with-review` composite command, pre-review filter integration. | ✅ **COMPLETE** | `phase-6a-review-gap-closure-plan.md` (archived) |
| 6B. Second-Pass Review | Planned | **Complete 2026-04-14** — `review_routing.py` (entry criteria + decision table), `ollama_review_second_pass.py` (orchestrator + agreement matrix + human worklist), CLI `review-relationships-ollama-second-pass`. End-to-end smoke-tested on real PD 1096 with `gemma4:e4b` as Tier-2 (qwen3:30b not pulled locally). | ✅ **COMPLETE** | `phase-6b-second-pass-review-plan.md` (archived) |
| **Pre-review filter** *(cross-cutting)* | *(new)* | **Shipped 2026-04-14** — `pre_review_filter.py` with 8 deterministic rules (A1-A4, R1-R2, R5, R7). Auto-accepts / auto-rejects candidates before LLM. Real-data impact: 78% LLM savings on PD 1096. | ✅ **COMPLETE** | AD-018, AD-021 |
| 7. Promotion Governance | Not implemented | Not started; no code in `scripts/vitruvius/` | ✅ **COMPLETE (2026-04-14)** | 6 PD 1096 relationships promoted; 17-rule validator; idempotency + rollback verified |
| 8. Graph Contract & Indexing | Not implemented | Not started | ❌ **NOT STARTED** | — |
| 9. Query & AI Layer | Not implemented | Not started | ❌ **NOT STARTED** | — |
| 10. Canonical Relationship Storage | Not implemented | Folder `003/shared/relationships/` is empty | ❌ **NOT STARTED** | Merged conceptually into Phase 7 |
| 11. Dataset Expansion | Not implemented | Gated on Phase 7 | 🔒 **GATED (do not start)** | Principle P10 |
| 12. AI-Augmented Reasoning | Not implemented | Long-term | 🔒 **GATED (do not start)** | — |

**Honest overall completion (updated 2026-04-14 after Sprints A + B):** *ingestion ≈ 90%, refinement ≈ 60% (Tier A/B rules shipping; Tier C + semantic chunking deferred), canonicalization ≈ 75% (restored with structured sections), concept layer ≈ 15%, extraction ≈ 40%, review ≈ 95% (retry, resume, parallelism, composite command; 6B separate), promotion ≈ 100%, downstream (8, 9, 11, 12) ≈ 0%*. The project now has a working end-to-end path: `run-with-review` → scan → status → lint → convert → refine → canonicalize → extract → review → promote. **Next candidates:** Phase 6B second-pass adjudication, Phase 3C concept enrichment, Phase 8 graph contract.

---

## 5. Honest Position Statement (updated 2026-04-15 19:00)

**What works end-to-end today:**
- Ingestion → conversion → refinement (Phase 1C MVP) → canonicalization → extraction → pre-review filter → Tier 1 LLM review → Tier 2 adjudication → promotion → canonical graph write.
- Sprint D Streams A–I shipped on 2026-04-14: dependency bootstrap, Shannon classifier, table-to-graph, parametric NER, Tier C OCR, AST chunker, TF-IDF/PMI/FCA, spaCy/CRF/TransE extraction, Bayesian fusion + stringency matrix + temporal edges (as scaffolds), Phase 8 base, Phase 9 base.
- Sprint Q (Live Wiring & 8GB Hardening) shipped on 2026-04-15: wired every Stream F + G scaffold into the live pipeline, rolled out the 20-concept stringency matrix gate, added the 8GB LLM survival mode, shipped the quality harness.
- Sprint R (Per-Layer Embeddings & Agentic) shipped on 2026-04-15: contextual priming, MoE domain routing, thinking-mode CoT audit, stateful agentic registry, vision OCR (operator-gated).
- Sprint PHYS (Statistical Mechanics & Graph Physics) shipped on 2026-04-15.
- Sprint H (3D Spatial Intelligence) shipped on 2026-04-15: all 20 tasks across Streams L/M/N/O; TypeScript sibling subproject at `spatial-daemon/`.
- Sprint GEOM (Geometric Constraint Engine) shipped on 2026-04-15: Z3 CSP, shapely/trimesh/cvxpy pipeline.
- Sprint WIKI (Autonomous Knowledge Synthesis) shipped on 2026-04-15: Docling + Kuzu + Ollama + ego linter.
- Sprint GT (Geo-Topological Knowledge Graph) shipped on 2026-04-15: pyo3 Rust crate + linear octree + temporal graph + spatial GraphRAG + hardware hardening.
- Sprint HP (High-Performance Optimizations) shipped on 2026-04-15: Merkle fs, SQLite event store (pivoted from RocksDB at the time), Wasm spatial kernels, GraphSAGE loopholes.
- Sprint Z (Compound AI Evolution) shipped on 2026-04-15: neuro-symbolic Datalog bridge (Rust `datalog_rs` crate), adversarial swarm, differential dataflow, Wasm kernel, DSPy prompt compiler.
- **Sprint HP.3-R (RocksDB KV Migration) shipped on 2026-04-15**: completed the original HP.3 spec. `RocksDBEventStore` + `RocksDBStatefulReviewRegistry` + factory dispatch + `ple-kv-migrate` CLI + O(1) count optimization. Bench at n=10000 measured RocksDB **18.7× faster** (event store) and **24.3× faster** (verdict cache) than SQLite; flag defaults flipped to `true` per AD-029.
- **Sprint 1B-M1 (Phase 1B Modernization Tranche 1) shipped on 2026-04-15**: `DoclingParser(BaseParser)` + `LibreOfficePreprocessor` + `GATE-005` quality gate + orchestrator `preprocessors` kwarg wiring. Two `p1b_*` feature flags default false until pipeline_cli.py integration lands. AD-031.
- **Sprint 1B-M2 (Phase 1B Modernization Tranche 2, scoped) shipped on 2026-04-15**: `OCRPreprocessor` (wraps `ocrmypdf`) + `ParserOrchestrator.process_batch` + `GoldenCorpusBenchmark` harness + 2 `p1b_*` flags. Marker/Surya **DEFERRED** per AD-032 feasibility finding (disk at 95.2% during tranche execution, RAM headroom 2.03 GB — insufficient for safe ML-dep install on 8 GB M2). AD-032.
- **Sprint RUST-PDF-1 (Rust PDF Ingestion Audit) shipped on 2026-04-15**: **GO verdict.** lopdf-based `vitruvius_rust_pdf` crate measured at **13.7 MB peak RSS (48× smaller than docling) and 0.05 s wall-clock (625× faster)** on synthetic PDFs. This audit unblocks the "low-spec M2 target" and is the single largest ingestion RAM win in the tree. AD-033.
- **Sprint 1B-M3 (Phase 1B Modernization Tranche 3) shipped on 2026-04-15**: `RustPdfParser(BaseParser)` wraps `vitruvius_rust_pdf`; `GATE-006` min-chars-per-page quality gate added; `p1b_rust_pdf_parser` flag (default false); real-PDF LCS quality rollback gate at **0.9925** on `History of Architecture Sample Exam.pdf` (pypdf baseline comparison). AD-034.
- **Sprint DISTILL-1 (LLM Reviewer Distillation Audit) shipped on 2026-04-15**: **DEFER_NO_DATA verdict.** Audit harness walks the Sprint R Y4 `StatefulReviewRegistry` + RocksDB verdict cache at 5 known locations and found 0 verdicts. Pre-committed threshold was ≥50 verdicts. Harness committed for re-run after the live review pipeline has been run with `y_stateful_registry=true` + `w_review_nb_prefilter=true` + `w_review_choquet_aggregator=true` on ≥20 PD 1096 sections. AD-035.
- **Meta Docs Cleanup Sprint shipped on 2026-04-15**: `.ai/00_system/architecture.md` + `.ai/00_system/pipeline-overview.md` refreshed; `.ai/01_roadmap/master-roadmap.md` bumped to v2.1.0 (this file, now v2.3.0); `.ai/02_audits/` banners marked historical; `.ai/10_state/known_issues.md` reconciled; 3 superseded plans archived (phase-8, phase-9, ultimate-architecture). Plan written + executed in-session via subagent dispatch.
- **Sprint RUST-MIG-1 (Python → Rust polyglot split) shipped on 2026-04-15**: 3 Rust kernels ported + N1 DEFERred. S1 `build_spatial_adjacency_edges` reduced O(n²) → O(n log n) via existing `LinearOctree::query_aabb` — **200× raw kernel speedup** (n=2000, 57% end-to-end wall improvement through the subprocess path); S2 `weight_by_distance` **12.18× raw / 2.84× end-to-end** (n=10000) via nalgebra vectorized `exp(-λ·d)`; N4 Mahalanobis core **2.73× end-to-end** (n=1000, 64-dim) via nalgebra covariance invert. N1 sliced Wasserstein DEFER_ALREADY_NATIVE per **AD-038a** — POT backend is already a thin wrapper over a native C++ LP solver; a Rust port would add marshalling overhead without speed. Both `rust_mig_spatial_kernels` + `rust_mig_stats_kernels` flags flipped to `true`. AD-036 + AD-037 + AD-038 + AD-038a.
- **Sprint AUDIT-1 (Advanced Tech Audit) shipped on 2026-04-15**: three pre-committed numeric gates, three different verdicts. FlatBuffers **NO_GO** — measured 5-10× SLOWER than CPython `_json` at the ~150B record sizes Vitruvius produces (runtime gate not met). Monte Carlo Dropout **PARK** — GraphSAGE runs under `torch.no_grad()` by design and there are no viable injection sites in the current review pipeline. Numerical Integrity **GO_GAP** — BLAKE3 measured 0.7× CPython SHA-256 on Apple Silicon (ARMv8 SHA hardware extension trumps BLAKE3's SIMD), BUT the audit identified a MEDIUM gap in spatial-daemon contract files and shipped a SHA-256 integrity footer via `spatial/contract_reader.py` + `spatial-daemon/src/contract_writer.ts`. Zero new Rust candidates surfaced. AD-039.
- **Sprint PIPELINE-CLI (Phase 1B Flag Integration) shipped on 2026-04-15**: new `convert-parsers-one` subcommand wires all 5 `p1b_*` deployment-readiness flags (`p1b_docling_parser`, `p1b_libreoffice_preprocessor`, `p1b_ocr_preprocessor`, `p1b_process_pool_orchestration`, `p1b_rust_pdf_parser`) end-to-end via `parsers/factory.py::build_default_orchestrator()` + `parsers/cli_handler.py::run_convert_parsers_one()`. Parallel command pattern (not a replacement of the existing `convert-one` dispatch) guarantees byte-identity with all flags OFF. Side-fix: `RustPdfParser` was in `parsers.__all__` but never imported (broken since AD-034). Unblocks user-facing use of every Phase 1B Tranche 1/2/3 deliverable. AD-040.
- **Sprint PQ-1 (GraphSAGE Product Quantization) shipped on 2026-04-15**: **32× exact compression** on GraphSAGE structural embeddings (256 B/node → 8 B/node; M=8 sub-spaces, k=256 centroids, sub_dim=8 over 64-d float32). **0.00017 cosine similarity delta** on held-out set — **117× under the pre-committed 0.02 gate**. Pure numpy implementation with k-means in M sub-spaces, `encode_to_pq` / `decode_from_pq` / `adc_distance` helpers, npz persistence, and `compress_graphsage_report` integration helper. Zero new pip dependencies, zero Rust escalation. `hp_graphsage_pq` feature flag stays false pending an embedding persistence layer that actually consumes the PQ codes. AD-041.
- **Sprint LSH-1 (MinHash Fuzzy Near-Duplicate Dedup) shipped on 2026-04-15**: vectorized Carter-Wegman MinHash (pure numpy, no `datasketch` dependency) + band-based LSH index + union-find component walk + representative pick. Initial nested-loop implementation was 8s at n=1000; vectorization dropped it to 108ms — **70× faster**. Fuzzy hit rate **14.17% at 20% injection** (clears the ≥10% AD-037 gate); **0 false positives** on 200-candidate disjoint audit. Plan's proposed `num_bands=4` was underpowered — tuned to `num_perm=256, num_bands=32, r=8` for 99% recall at Jaccard ≥ 0.78. Reframed by AD-037 from "O(n²) scaling fix" to "fuzzy near-duplicate detection for predicate variants" — current `dedupe_by_endpoints` is already O(n log n) dict-grouped. `w_lsh_dedup` feature flag stays false pending full-PD-1096 operator run. AD-042.

**Historical hard numbers from the 2026-04-15 sprint-closure snapshot (not the live 2026-04-16 stabilization baseline):**
- Python test suite: **1528 passed, 1 skipped** (grew from pre-session 297 — +1231 delta; +91 delta for the 5-sprint closing block alone from the prior 1437 mark at 14:45)
- TypeScript test suite: **21 / 21 passing** (`spatial-daemon/` — +1 integrity footer test from Sprint AUDIT-1)
- Rust unit tests: **33 passing** (`engine_rs` core + `datalog_rs` + new `spatial_kernels` + `stats_kernels` workspace members from Sprint RUST-MIG-1; +23 from the RUST-MIG-1 port parity suite) + wasm api tests + adjacent lopdf smoke tests
- Canonical relationships: **31 verified** (unchanged — 2026-04-14 baseline)
- Enriched concept files: **20 / 20** PD 1096 concepts (all carry `stringency_vector` frontmatter)
- Sprint tags: **20** — `sprint-q-closed`, `sprint-r-closed`, `sprint-phys-closed`, `sprint-h-closed`, `sprint-geom-closed`, `sprint-wiki-closed`, `sprint-gt-closed`, `sprint-hp-closed`, `sprint-z-closed`, `sprint-hp3r-closed`, `sprint-1b-m1-closed`, `sprint-1b-m2-closed`, `sprint-rust-pdf-1-closed`, `sprint-1b-m3-closed`, `sprint-distill-1-closed`, `sprint-rust-mig-1-closed`, `sprint-audit-1-closed`, `sprint-pipeline-cli-closed`, `sprint-pq-1-closed`, `sprint-lsh-1-closed`
- Decision log: **AD-001 through AD-042 + AD-038a** in `.ai/10_state/decisions.md` (AD-024–AD-042 + AD-038a are the 2026-04-15 session ledgers)
- Active branch at that historical snapshot: **`main`** — fully pushed to `origin/main` (HEAD `58161bd`); all 20 sprint tags published
- Git remote: **FIXED** — `gh auth setup-git` ran; `origin` (`github.com/pjel888/vitruvius.git`) authenticates and accepts pushes

**Historical work queue snapshot:** empty at 2026-04-15 close. Live stabilization truth for 2026-04-16 now lives in `current-phase.md`, `active_context.md`, and the dated PASS 2 validation log.

**What still needs doing (open options, not yet plans):**
- **Sprint D Streams J (active learning) + K (CLUP scaling)** — externally gated on the Ranger dashboard surface (J) and a 2nd jurisdiction corpus (K). Will light up when their external unblockers land. The `statistical-architectural-upgrade-plan.md` has been archived as of 2026-04-15 19:00 with an `archived_with_open_streams: "J,K"` frontmatter note preserving the defer status.
- **Phase 1B Modernization §11 Phase 3 (Scaling & Governance)** — **✅ CLOSED.** Tranches 1/2/3 all shipped (M1, M2-scoped, M3) plus the pipeline_cli integration was shipped in Sprint PIPELINE-CLI (AD-040). `phase-1b-multi-parser-integration-plan.md` has been archived as of 2026-04-15 19:00.
- **Fresh roadmap brainstorm** — the project is materially ahead of the v2.0.0 roadmap envelope and is producing 5–6 sprints per session (ceiling observed this session: **21 sprints**). Next horizon (Phase 12+ / corpus expansion / real-world evaluation against board-exam prep use case) is undefined. Worth a fresh strategy pass before committing to a new sprint chain.

**Where to read the per-sprint ledger:** `.ai/10_state/decisions.md` AD-024 through AD-042 (plus AD-038a) have the full commit SHAs, test counts, and exit gates for every sprint closed this session.

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

**Prerequisites.** Phase 1A complete. Plan `/.ai/09_archive/plans/phase-1b-multi-parser-integration-plan.md` accepted (archived 2026-04-15).

**Deliverables.**
1. **`BaseParser` interface** + `ParserOrchestrator` honoring the taxonomy in §3.3 and the fallback chains in `.ai/09_archive/plans/phase-1b-multi-parser-integration-plan.md` §5.
2. **Document taxonomy classifier** (deterministic, threshold-driven — no ML).
3. **Parser implementations**: wrap existing `opendataloader`; add `Docling`, `Marker`, `Surya`; integrate `OCR preprocessor` and `LibreOffice preprocessor`.
4. **Strict telemetry JSON** (flattened schema in plan §6) per parser attempt.
5. **Quality gates**: Gate-001 (UTF-8), Gate-002 (volume ≥500 chars), Gate-003 (≥1 header if pages>5), Gate-004 (Office sanity).
6. **Fallback orchestration** with page-level isolation for OOM/timeout cases.
7. **Batch-processing/resource-allocation API** with `process_batch(..., max_workers=...)` and a documented upgrade path to future `ProcessPoolExecutor` fan-out.
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

**References.** `/.ai/09_archive/plans/phase-1b-multi-parser-integration-plan.md` (archived 2026-04-15).

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

### Phase 2 — Canonicalization Engine · ✅ COMPLETE (2026-04-14)

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

### Phase 3 — Concept Layer · ✅ 16/20 ENRICHED (2026-04-14, deterministic)

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

#### Phase 6A — Local LLM Review · ✅ COMPLETE (full gap closure 2026-04-14)

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

#### Phase 6B — Second-Pass Review (Two-Stage Adjudication) · ✅ COMPLETE (2026-04-14)

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

### Phase 7 — Promotion Governance · ✅ COMPLETE (2026-04-14)

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

### Phase 8 — Graph Contract & Indexing · ✅ **SUBSUMED** (Sprint D Stream H, 2026-04-14)

**Status:** ✅ **SUBSUMED** — base work shipped inside Sprint D Stream H on 2026-04-14. Original design spec archived 2026-04-15 at `.ai/09_archive/plans/phase-8-graph-contract-indexing-plan.md`. Sprint GT (`sprint-gt-closed`) subsequently extended this with temporal edges (GT.3.1), Parquet archiver (GT.3.3), spatial GraphRAG bridge (GT.4), and the `engine_rs` Rust data plane (GT.1/GT.2) — see `.ai/09_archive/plans/phase-8b-geo-topological-graph-plan.md` (also archived). Sprint HP.3-R (`sprint-hp3r-closed`) further replaced the SQLite event store with a RocksDB-backed `RocksDBEventStore` measured 18.7× faster at n=10000 — see AD-029.

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

### Phase 9 — Query & AI Augmentation · ✅ **SUBSUMED** (Sprint D Stream I, 2026-04-14)

**Status:** ✅ **SUBSUMED** — base work shipped inside Sprint D Stream I on 2026-04-14. Original design spec archived 2026-04-15 at `.ai/09_archive/plans/phase-9-query-ai-layer-plan.md`. No follow-up sprint has extended it — Query/AI integration for external consumers is gated on Sprint D Stream J (Ranger dashboard surface), which is externally blocked.

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

**Bounded pilot note (2026-04-16).**
The accepted `/.ai/03_plans/2026-04-16_laws-mini-dataset-graph-pipeline-plan.md` M1 slice is allowed as a **bounded validation pilot**, not as the opening of generic Phase 11 corpus expansion.

That exception is valid only because the M1 slice is explicitly constrained to:
- manifest-selected canonical/promoted inputs
- dataset-scoped artifacts and freshness metadata
- preservation of the default/global path when dataset mode is unused
- no claim of generic all-laws expansion beyond the accepted pilot bundle

If implementation widens beyond that bounded pilot contract, it becomes normal Phase 11 dataset-expansion work again and remains gated by the conditions above.

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

## 8. 90-Day Execution Sequence — 21 SPRINTS CLOSED, QUEUE EMPTY (2026-04-15 19:00 local)

> **Status:** **All** governing-plan sprints + a Phase 1B Modernization three-tranche push + a Rust PDF audit + an LLM reviewer distillation audit + a meta docs cleanup sprint + **five optimization sprints** (RUST-MIG-1, AUDIT-1, PIPELINE-CLI, PQ-1, LSH-1) all shipped in the 2026-04-15 session via subagent-driven-development. **21 sprints closed, queue empty.** Sprints A–C from the pre-session pass are retained below for historical context; the authoritative "what's next" is a **fresh roadmap brainstorm** — no plans are queued.

### Sprint chain (all closed)

| # | Sprint | Scope | Tag | AD ref |
|---|---|---|---|---|
| 1 | A — Phase 7 Promotion Governance | 17-rule validator, audit log, rollback | (pre-session) | AD-015 |
| 2 | B — Phase 1C + Phase 2 + Phase 6A/B | Normalization, canonicalizer, review gap closure | (pre-session) | AD-016/017 |
| 3 | C — Phase 1B Foundation + polish | Parsers subpackage, FileEntry.sha256, rotate-registries | (pre-session) | AD-022/023 |
| 4 | D — Statistical & Architectural Upgrade | Streams A-I (J/K deferred) | (pre-session) | AD-024 |
| 5 | Q — Live Wiring & 8GB Hardening | Wire F/G scaffolds live, 8GB LLM mode | `sprint-q-closed` | AD-024 |
| 6 | R — Per-Layer Embeddings & Agentic | Priming, MoE router, CoT audit, registry, vision OCR | `sprint-r-closed` | AD-025 |
| 7 | PHYS — Graph Physics | PageRank, Boltzmann gate, Shannon, eigenvector cascade | `sprint-phys-closed` | AD-026 |
| 8 | H — 3D Spatial Intelligence | Spatial ingest, Z3 solver, IFC/OWL, TS daemon | `sprint-h-closed` | AD-026 |
| 9 | GEOM — Geometric Constraint Engine | Z3 CSP, 2D/3D envelope, Pareto optimizer | `sprint-geom-closed` | AD-027 |
| 10 | WIKI — Autonomous Knowledge Synthesis | Docling, Kuzu, Ollama, ego linter | `sprint-wiki-closed` | AD-027 |
| 11 | GT — Geo-Topological Knowledge Graph | Rust crate, linear octree, temporal graph, spatial GraphRAG | `sprint-gt-closed` | AD-028 |
| 12 | HP — High-Performance Optimizations | Merkle fs, SQLite events, Wasm kernels, GraphSAGE | `sprint-hp-closed` | AD-028 |
| 13 | Z — Compound AI Evolution | Datalog bridge, adversarial swarm, differential dataflow, DSPy | `sprint-z-closed` | AD-028 |
| 14 | HP.3-R — RocksDB KV Migration | RocksDBEventStore + RocksDBStatefulReviewRegistry + factory + CLI + O(1) count; bench 18.7×/24.3× faster than SQLite | `sprint-hp3r-closed` | AD-029 |
| 15 | Meta — Docs Cleanup Sprint | `.ai/00_system/` + `.ai/01_roadmap/` + `.ai/02_audits/` + `.ai/10_state/known_issues.md` refreshed; 3 superseded plans archived; INDEX reconciled | (no tag; meta) | AD-030 |
| 16 | 1B-M1 — Phase 1B Modernization Tranche 1 | DoclingParser + LibreOfficePreprocessor + GATE-005 + orchestrator preprocessor wiring | `sprint-1b-m1-closed` | AD-031 |
| 17 | 1B-M2 — Phase 1B Modernization Tranche 2 (scoped) | OCRPreprocessor + process_batch + GoldenCorpusBenchmark; marker/surya DEFERRED on feasibility evidence | `sprint-1b-m2-closed` | AD-032 |
| 18 | **RUST-PDF-1 — Rust PDF Ingestion Audit** | lopdf `vitruvius_rust_pdf` crate + pyo3 bindings + subprocess-isolated bench vs docling/opendataloader_pdf. **GO verdict.** 13.7 MB RSS (48× smaller) + 0.05 s wall (625× faster) — **single largest ingestion RAM win** | `sprint-rust-pdf-1-closed` | **AD-033** |
| 19 | 1B-M3 — Phase 1B Modernization Tranche 3 | RustPdfParser(BaseParser) + GATE-006 min-chars-per-page + real-PDF LCS quality gate (0.9925) + `p1b_rust_pdf_parser` flag | `sprint-1b-m3-closed` | AD-034 |
| 20 | DISTILL-1 — LLM Reviewer Distillation Audit | Audit harness walks 5 known cache locations. **DEFER_NO_DATA verdict** — Sprint R Y4 verdict cache empty; needs ≥50 live verdicts before training a student model is meaningful. Harness committed for re-run. | `sprint-distill-1-closed` | AD-035 |
| 21 | **RUST-MIG-1 — Python → Rust Polyglot Split** | 3 Rust kernels shipped + N1 DEFER_ALREADY_NATIVE. S1 `build_spatial_adjacency_edges` **200× raw kernel speedup** (O(n²) → O(n log n) via existing `LinearOctree::query_aabb`), S2 `weight_by_distance` **12.18× raw / 2.84× end-to-end** via nalgebra vectorized `exp(-λ·d)`, N4 Mahalanobis core **2.73× end-to-end** via nalgebra covariance invert. N1 sliced Wasserstein DEFERred per AD-038a — POT backend is already native C++ LP. Both `rust_mig_*` flags flipped to `true`. | `sprint-rust-mig-1-closed` | **AD-036 + AD-037 + AD-038 + AD-038a** |
| 22 | **AUDIT-1 — Advanced Tech Audit** | FlatBuffers **NO_GO** (5-10× SLOWER than CPython `_json` at ~150B records) + Monte Carlo Dropout **PARK** (GraphSAGE is `torch.no_grad()` by design — no viable injection sites) + Numerical Integrity **GO_GAP** (SHA-256 integrity footer shipped for spatial contracts via `spatial/contract_reader.py` + `spatial-daemon/src/contract_writer.ts`). Zero new Rust candidates surfaced. | `sprint-audit-1-closed` | AD-039 |
| 23 | **PIPELINE-CLI — Phase 1B Flag Integration** | New `convert-parsers-one` subcommand + `parsers/factory.py::build_default_orchestrator()` + `parsers/cli_handler.py::run_convert_parsers_one()`. Wires all 5 `p1b_*` deployment-readiness flags end-to-end. Parallel command pattern guarantees byte-identity with flags OFF. Side-fix: `RustPdfParser` was in `__all__` but never imported (broken since AD-034). | `sprint-pipeline-cli-closed` | AD-040 |
| 24 | **PQ-1 — GraphSAGE Product Quantization** | 32× exact compression (256 B → 8 B per node; M=8, k=256, sub_dim=8 over 64-d float32). **0.00017 cosine similarity delta** on held-out set — **117× under the 0.02 gate**. Pure numpy, zero new deps, zero Rust escalation. `hp_graphsage_pq` stays false pending an embedding persistence layer. | `sprint-pq-1-closed` | AD-041 |
| 25 | **LSH-1 — MinHash Fuzzy Near-Duplicate Dedup** | Vectorized Carter-Wegman MinHash (pure numpy, no `datasketch` dep) — **70× faster** than initial nested-loop (8s → 108ms at n=1000). **14.17% fuzzy hit rate** at 20% injection (>10% gate); **0 false positives** on 200-candidate disjoint audit. Tuned to `num_perm=256, num_bands=32, r=8` for 99% recall at J≥0.78 (plan's `num_bands=4` was underpowered). `w_lsh_dedup` stays false pending PD 1096 operator validation. | `sprint-lsh-1-closed` | AD-042 (premise: AD-037) |

### Queued work

Queue fully closed on 2026-04-15; no plans queued. Governing plan §10 recommends a fresh roadmap brainstorm as the next action.

### What's NOT in the queue (still open options)

- **Sprint D Streams J + K** — externally gated:
  - Stream J (active learning) needs the Ranger dashboard surface
  - Stream K (CLUP scaling) needs a 2nd jurisdiction corpus to benchmark against
- **Phase 1B Modernization §11 Phase 3 (Scaling & Governance)** beyond what Tranches 1/2/3 already delivered — the remaining work is rolled into the pipeline_cli integration plan and AD-032's marker/surya deferral
- **Fresh roadmap brainstorm** — the project is materially ahead of the v2.0.0 envelope and producing 5–6 sprints per session. Next horizon is undefined (Phase 12+ / corpus expansion / real-world evaluation against board-exam prep). Worth a fresh strategy pass before committing to a new sprint chain

### Delivery pattern validation

The 2026-04-15 session validated **subagent-driven-development** as the working delivery pattern. Key parameters:
- Wave-parallel dispatch (up to 6 parallel implementers per wave with file-disjoint work)
- Two-stage review per task (spec compliance → code quality)
- Fresh subagent per task to avoid context pollution
- Single orchestrator-held commit at end of each wave to avoid `git add` races

**Ceiling observed so far: 21 sprints closed in one session** (test suite 297 → 1528 passing, +1231 delta; 18+ plans archived; 20 sprint tags published; main fully pushed to origin). Five of those 21 sprints were the back-to-back closure of the Task 8 optimization queue (RUST-MIG-1 → AUDIT-1 → PIPELINE-CLI → PQ-1 → LSH-1, +91 test delta across the five alone), which validates that subagent-driven-development can sustain the cadence across optimization work just as well as feature work. Future planning can reasonably assume this cadence is repeatable when the plan specs are solid and the flag defaults are disciplined. **Two of the 21 sprints were audits** (DISTILL-1 and AUDIT-1) — reinforcing that audits count as delivery work and should be ranked alongside implementation sprints rather than discounted as "just research".

---

### §8.HISTORICAL — Original Sprint A-C plan (retained for history)

The original pre-Sprint-D execution plan is retained below as historical context. All three sprints shipped and are superseded by the Sprint chain table above.

> **Status (historical):** Sprint A (Phase 7) shipped. Sprint B (1C + 2 + 6A) shipped. Sprint C (1B + 6B) partially shipped — 6B delivered, 1B still planned. Pre-review filter (cross-cutting) added as a quality-pass.

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

### §8.4 Sprint Order (post-2026-04-15)

> **Status:** Sprints A, B, C **CLOSED 2026-04-14**. Sprint D (Statistical & Architectural Upgrade) Streams A–I **CLOSED 2026-04-14**, which also shipped Phase 8 base (Stream H) and Phase 9 base (Stream I). Those two formerly-separate plans (`phase-8-graph-contract-indexing-plan.md` and `phase-9-query-ai-layer-plan.md`) are therefore **subsumed**, not separately dispatchable.
>
> **Authoritative execution order:** `/.ai/03_plans/00-governing-implementation-plan.md` §3. This subsection is a short forward reference; if it disagrees with the governing plan, the governing plan wins.

The post-2026-04-15 sprint sequence is:

| Order | Sprint | Sub-plan | Purpose |
|---|---|---|---|
| 1 | **Q — Live Wiring & 8GB Hardening** 🔥 | `live-wiring-and-8gb-hardening-plan.md` | Wire the Stream F review + Stream G promotion scaffolds into `ollama_review.py` / `promotion.py`; migrate 20 concepts to have `stringency_vector`; install quality harness. HIGHEST PRIORITY — all downstream sprints are value-gated by this. |
| 2a | **R — Per-Layer Embeddings & Agentic** (parallel with 2b) | `per-layer-embeddings-agentic-upgrade-plan.md` | Port Gemma 4 PLE/MoE/CoT/stateful/vision innovations; absorbs Stream U psutil hardware router from superseded ultimate plan. |
| 2b | **H — 3D Spatial Intelligence** (parallel with 2a) | `3d-spatial-intelligence-upgrade-plan.md` | Add Z3 spatial ingestion + IFC/OWL ontology + TS daemon + foraging scaffold. Gated on ≥25 verified relationships. |
| 3 | **D-residual J / K** (conditional, skip if gates unmet) | `statistical-architectural-upgrade-plan.md` §Streams J, K | Active learning (gated on Ranger dashboard); CLUP scaling (gated on 2nd jurisdiction corpus). |
| 4 | **GT — Geo-Topological Rust Vault** | `phase-8b-geo-topological-graph-plan.md` | Replace TS spatial daemon with Rust `engine_rs` crate via `pyo3`, FlatBuffers, RocksDB, linear octree. |
| 5 | **HP — High-Performance Optimizations** | `phase-13-high-performance-optimizations-plan.md` | Merkle fs status, AST chunking, event-sourced graph, Wasm spatial kernels, GraphSAGE PQ. |
| 6 | **WIKI — Autonomous Knowledge Synthesis** | `phase-14-autonomous-knowledge-synthesis-plan.md` | Docling+Heron ingestion, synthesis loop, Kuzu hybrid store, SHA-256 delta linting. |
| 7 | **GEOM — Geometric Constraint Engine** | `phase-15-geometric-constraint-engine-plan.md` | Inequality extraction, Z3 CSP solver, 3D buildable envelope, multimodal IoU audit. |
| 8 | **PHYS — Graph Physics** | `phase-16-statistical-mechanics-graph-physics-plan.md` | PageRank authority, Boltzmann stability, Shannon sampling, eigenvector cascade. Absorbs orphan Stream O VF2 + Boltzmann gate from the statistical plan. |
| 9 (stretch) | **Z — Compound AI Evolution** | `phase-12-compound-ai-evolution-plan.md` | Neuro-symbolic Datalog bridge, adversarial swarm, differential dataflow, Wasm kernel, DSPy prompt compilation. Gated on GEOM + PHYS closure. |

All sprints from GT onwards require a **TDD-expansion pass** (governing plan Task 6) on the owning plan before dispatch, because those plans currently ship as `plan_type: design_spec`.

A non-blocking parallel side-track is **Phase 1B Modernization** (`phase-1b-multi-parser-integration-plan.md` §11 Phase 2–3), which can run in a side worktree at any time without gating any sprint.

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

### 11.X — Subagent-Driven Wave Delivery (2026-04-15 addition)

Validated in the 2026-04-15 session that closed ten sprints in a single working block. The pattern:

1. **Orchestrator extracts all tasks upfront** from the plan and creates a TodoWrite / TaskCreate checklist (so parallel dispatches can be tracked).
2. **Wave-parallel dispatch** — up to ~6 parallel `Agent` calls per wave, each with file-disjoint work. More than 6 risks `git add` races and human-scale coordination errors.
3. **Per-task two-stage review** — spec compliance review first, then code quality review. Both are cheap model dispatches; both must pass before the task is marked complete.
4. **Orchestrator-held commits** — subagents write files but never run `git add` or `git commit`. The orchestrator stages and commits once per wave.
5. **Per-sprint AD ledger entry** — every sprint closure must produce an `AD-###` entry in `.ai/10_state/decisions.md` with commit SHAs, test deltas, sprint tag, and archival status.

Ceiling observed so far: **21 sprints per session** (ten governing-plan sprints + HP.3-R bench-driven migration + docs cleanup meta sprint + Phase 1B three-tranche push + Rust PDF audit + LLM distillation audit + RUST-MIG-1 polyglot split + AUDIT-1 tech audit + PIPELINE-CLI flag integration + PQ-1 GraphSAGE compression + LSH-1 fuzzy dedup), **+1231 test delta** (297 → 1528), **~35+ subagent dispatches** across 7+ waves. Future sessions can use this as a planning baseline; the 21-sprint bound came from time-boxing, not agent capacity. The last 5 sprints (the Task 8 optimization queue) shipped back-to-back at roughly ~30-45 min each, validating that subagent-driven-development holds up for optimization work just as well as feature work.

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

**Audits (2026-04-13, historical).** `codebase-roadmap-audit.md`, `ingestion-audit.md`, `extraction-audit.md`, `normalization-audit.md`, `review-layer-audit.md` — all marked ⚠️ `HISTORICAL SNAPSHOT — SUPERSEDED 2026-04-15` in their own header banners and pointed at current state docs.

**Active plans.**
- `/.ai/03_plans/00-governing-implementation-plan.md` — governing orchestration plan (**v3.0.0**, 2026-04-15 19:00 post-queue-closure) — read this first before picking a plan to execute
- `/.ai/03_plans/INDEX.md` — plan index

As of the 2026-04-15 19:00 cleanup pass, only the governing plan + INDEX remain in `.ai/03_plans/`. All other plans either shipped and were archived, or were archived with defer notes for externally-gated work.

**Archived plans (successor sprint plans).**
- `/.ai/09_archive/plans/phase-8-graph-contract-indexing-plan.md` — ✅ subsumed by Sprint D Stream H, archived 2026-04-15
- `/.ai/09_archive/plans/phase-9-query-ai-layer-plan.md` — ✅ subsumed by Sprint D Stream I, archived 2026-04-15
- `/.ai/09_archive/plans/ultimate-architecture-upgrade-plan.md` — ❌ superseded, archived 2026-04-15
- `/.ai/09_archive/plans/phase-8b-geo-topological-graph-plan.md` — ✅ Sprint GT, archived 2026-04-15
- `/.ai/09_archive/plans/phase-12-compound-ai-evolution-plan.md` — ✅ Sprint Z, archived 2026-04-15
- `/.ai/09_archive/plans/phase-13-high-performance-optimizations-plan.md` — ✅ Sprint HP, archived 2026-04-15
- `/.ai/09_archive/plans/phase-14-autonomous-knowledge-synthesis-plan.md` — ✅ Sprint WIKI, archived 2026-04-15
- `/.ai/09_archive/plans/phase-15-geometric-constraint-engine-plan.md` — ✅ Sprint GEOM, archived 2026-04-15
- `/.ai/09_archive/plans/phase-16-statistical-mechanics-graph-physics-plan.md` — ✅ Sprint PHYS, archived 2026-04-15
- `/.ai/09_archive/plans/3d-spatial-intelligence-upgrade-plan.md` — ✅ Sprint H, archived 2026-04-15
- `/.ai/09_archive/plans/live-wiring-and-8gb-hardening-plan.md` — ✅ Sprint Q, archived 2026-04-15
- `/.ai/09_archive/plans/per-layer-embeddings-agentic-upgrade-plan.md` — ✅ Sprint R, archived 2026-04-15
- `/.ai/09_archive/plans/2026-04-15-rocksdb-kv-migration-plan.md` — ✅ Sprint HP.3-R, archived 2026-04-15
- `/.ai/09_archive/plans/2026-04-15-phase-1b-modernization-tdd-plan.md` — ✅ Sprint 1B-M1, archived 2026-04-15
- `/.ai/09_archive/plans/2026-04-15-phase-1b-modernization-tranche-2-plan.md` — ✅ Sprint 1B-M2, archived 2026-04-15
- `/.ai/09_archive/plans/2026-04-15-rust-pdf-audit-plan.md` — ✅ Sprint RUST-PDF-1, archived 2026-04-15
- `/.ai/09_archive/plans/2026-04-15-phase-1b-modernization-tranche-3-plan.md` — ✅ Sprint 1B-M3, archived 2026-04-15
- `/.ai/09_archive/plans/2026-04-15-llm-distillation-audit-plan.md` — ✅ Sprint DISTILL-1, archived 2026-04-15
- `/.ai/09_archive/plans/2026-04-15-docs-cleanup-plan.md` — ✅ Meta Docs Cleanup Sprint, archived 2026-04-15
- `/.ai/09_archive/plans/2026-04-15-rust-migration-audit-plan.md` — ✅ Sprint RUST-MIG-1 (3 Rust kernels + N1 DEFER_ALREADY_NATIVE; AD-036/037/038/038a), archived 2026-04-15
- `/.ai/09_archive/plans/2026-04-15-advanced-tech-audit-plan.md` — ✅ Sprint AUDIT-1 (FlatBuffers NO_GO + MC Dropout PARK + SHA-256 integrity footer GO; AD-039), archived 2026-04-15
- `/.ai/09_archive/plans/2026-04-15-pipeline-cli-integration-plan.md` — ✅ Sprint PIPELINE-CLI (`convert-parsers-one` subcommand + 5 `p1b_*` flag integration; AD-040), archived 2026-04-15
- `/.ai/09_archive/plans/2026-04-15-graphsage-pq-embeddings-plan.md` — ✅ Sprint PQ-1 (32× GraphSAGE compression, 0.00017 cosine delta — 117× under gate; AD-041), archived 2026-04-15
- `/.ai/09_archive/plans/2026-04-15-lsh-dedup-plan.md` — ✅ Sprint LSH-1 (MinHash fuzzy dedup, 14.17% hit rate, 0 FP, Carter-Wegman 70× speedup; AD-042), archived 2026-04-15
- `/.ai/09_archive/plans/phase-1b-multi-parser-integration-plan.md` — ✅ Phase 1B Foundation (Sprint C) + Tranches 1/2/3 (1B-M1/M2/M3, AD-031/032/034) + §11 Phase 3 Scaling (Sprint PIPELINE-CLI, AD-040) all shipped, archived 2026-04-15 19:00
- `/.ai/09_archive/plans/statistical-architectural-upgrade-plan.md` — 🟡 Partial archive: Streams A–I all closed 2026-04-14; Streams J (active learning) + K (CLUP scaling) remain externally gated (Ranger dashboard + second-jurisdiction corpus). Archived 2026-04-15 19:00 with `archived_with_open_streams: "J,K"` frontmatter preserving the defer status.
- `/.ai/09_archive/plans/ingestion-refinement-contract.md` — ❄️ Frozen contract between Phase 1B ↔ Phase 1C; both sides shipped. Archived 2026-04-15 19:00 per user instruction to leave only governing plan + INDEX in the active plans folder.

**Plans & contracts (historical references — all now archived).** `phase-1b-multi-parser-integration-plan.md`, `phase-1c-centralized-normalization-plan.md`, `ingestion-refinement-contract.md`.

**State.** `/.ai/10_state/active_context.md`, `/.ai/10_state/decisions.md`, `/.ai/10_state/known_issues.md`.

**Schemas (stubs — to be populated).** `/.ai/06_specs/source-schema.md`, `/.ai/06_specs/concept-schema.md`, `/.ai/06_specs/relationship-schema.md`.

---

## Changelog

- **2026-04-15 · v2.3.0** — Third-wave reconciliation after §8's queued work grew by **5 more sprints closed back-to-back** (RUST-MIG-1, AUDIT-1, PIPELINE-CLI, PQ-1, LSH-1) — the entire Task 8 optimization queue shipped during the same session it was written in. §5 rewritten with 1528/1 Python test count (grew from 1437; +91 for the 5-sprint closing block alone), 20 sprint tags (grew from 15), AD-001–AD-042 + AD-038a (grew from AD-001–AD-035), HEAD bumped from `c2c154a` to `58161bd`, 33 Rust unit tests (grew from 10 via RUST-MIG-1's `spatial_kernels` + `stats_kernels` parity suite), 21 TypeScript tests (grew from 20 via the AUDIT-1 integrity-footer test). Five new bullets added to "What works end-to-end today" covering each sprint closure with AD references + headline numbers. "Active work queue" block replaced with a one-liner noting the queue is empty. §8 Sprint chain table grew from 20 to 25 rows. "Queued work" block replaced with a one-line closure note pointing at the governing plan §10 fresh-brainstorm recommendation. §8 delivery-pattern ceiling updated to **21 sprints per session** (from 16). §11.X ceiling also updated to 21. §13 Reference Index: "Active plans" list shrunk to just governing + INDEX after the 2026-04-15 19:00 archival pass moved `statistical-architectural-upgrade-plan.md` (with `archived_with_open_streams: "J,K"` frontmatter), `phase-1b-multi-parser-integration-plan.md` (fully shipped via 1B-M1/M2/M3 + PIPELINE-CLI), and `ingestion-refinement-contract.md` (per user instruction) into `.ai/09_archive/plans/`. "Queued implementation plans" subsection deleted entirely. "Archived plans" list grew to cover the 5 Task 8 sprint plans + the 3 former-active plan archivals. No breaking changes to §1 Vision, §2 Architecture Map, §3 Governance Contracts, §4 Status Reconciliation, §6 Phase Contracts, §7 Dependency Graph, §9 KPIs, §10 Tech Debt, or §12 Non-Goals — those remain authoritative as written in v2.2.0 / v2.1.0 / v2.0.0. — *Senior Systems Architect*
- **2026-04-15 · v2.2.0** — Second-wave reconciliation after §8's queued work grew by **6 more sprints** (1B-M1, 1B-M2, RUST-PDF-1, 1B-M3, DISTILL-1, meta Docs Cleanup) and **5 new queued plans** landed (Advanced Tech Audit, RUST-MIG-1, pipeline_cli integration, PQ-1, LSH-1). §1.1 Long-Term Vision rewritten to reflect the repositioned "domain-agnostic professional-domain specialist" framing from the README update (PD 1096 is now named the "reference corpus", not the "initial corpus"). §1.4 Principle P10 generalized to "new corpus" from "new laws". §5 rewritten with 1437/1 Python test count (grew from 1396), 15 sprint tags (grew from 10), AD-001–AD-035 (grew from AD-029), git remote marked FIXED, and a new "active work queue" block listing the 5 queued optimization plans. §8 Sprint chain table grew to 20 rows, with a new "Queued work" block ranking the 5 plans and a "Dispatch order rationale" paragraph explaining why Sprint RUST-MIG-1 dispatches before pipeline_cli and Sprint LSH-1. §8 delivery-pattern ceiling updated to **16 sprints per session** (from 10). §11.X ceiling also updated. §13 Reference Index grew to list the 5 queued plans + 6 new archived plans. No breaking changes to §2 Architecture Map, §3 Governance Contracts, §6 Phase Contracts, §7 Dependency Graph, §9 KPIs, §10 Tech Debt, or §12 Non-Goals — those remain authoritative as written in v2.1.0 / v2.0.0. — *Senior Systems Architect*
- **2026-04-15 · v2.1.0** — Reconciled §5 Honest Position, §6 Phase 8 + Phase 9 contracts, §8 90-Day Execution Sequence, §11 Cadence, and §13 Reference Index against the 2026-04-15 session (**10 sprints closed**: Q, R, PHYS, H, GEOM, WIKI, GT, HP, Z, HP.3-R). §5 rewritten with 1396/1 Python test count, 20/20 TypeScript, 10 Rust unit tests, 31 verified relationships, and all 10 sprint tags. §6 Phase 8 marked ✅ SUBSUMED by Sprint D Stream H + extended by Sprint GT + RocksDB-backed by Sprint HP.3-R (AD-029). §6 Phase 9 marked ✅ SUBSUMED by Sprint D Stream I. §8 rewritten with the Sprint chain table (14 rows through HP.3-R) and a "what's next" block pointing at Phase 1B Modernization, Streams J/K externally gated, git remote fix, fresh roadmap brainstorm. §11 adds the Subagent-Driven Wave Delivery addendum. §13 refreshes the Reference Index with active plans, archived plans (13 archival entries), and audit pack marked as historical. No breaking changes to §1–§4 (vision, architecture map, governance contracts) or §9–§10 (KPIs, tech debt) — those remain authoritative as written in 2.0.0. — *Senior Systems Architect*
- **2026-04-14 · v2.0.0** — Full rewrite. Reconciled status against the 2026-04-13 audit pack (ingestion, extraction, normalization, review-layer, codebase-roadmap). Integrated Phase 1B Multi-Parser plan, Phase 1C Refinement plan, and the Ingestion-Refinement Contract. Added governance contract section (§3), dependency graph (§7), 90-day sprint sequence (§8), KPI table (§9), and cadence protocol (§11). Corrected inflated "complete" claims in Phases 2, 3, and 5 to match audit reality. Added non-goals and strategic warnings explicitly. — *Senior Systems Architect*
- **2026-04-13 · v1.x** — Prior version with inflated Phase 2/3/5 claims. Retained in git history.

**Timestamp:** 2026-04-15T19:00:00+08:00
