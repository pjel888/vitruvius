# Milestone Tracker

> **Source of truth:** This tracker is reconciled against `/.ai/01_roadmap/master-roadmap.md` §4 and the 2026-04-13 audit pack.
> **Legend:** `[x]` complete · `[~]` partial / skeleton · `[ ]` not started · `🔒` gated (do not start) · `🔥` highest priority · `🚫` DEFERRED (documented in an AD)
> **Revised:** 2026-04-18 (ready-family aggregate residual-hardening reconciliation)

## Phase 0 — Foundation ✅ COMPLETE
- [x] Layered root structure `001_` through `006_`
- [x] `pipeline_cli.py` CLI orchestrator
- [x] `paths.py` + `constants.py` filesystem contract
- [x] `config/vitruvius.yaml` baseline
- [x] Registry / manifest system under `006_System-Manifests/`

## Phase 1A — Baseline Ingestion ✅ COMPLETE (with known gaps)
- [x] PDF text ingestion (`opendataloader_pdf`)
- [x] PDF detection heuristic (`pypdf`, ≥50 chars × ≥50% pages × ≥300 total)
- [x] Office ingestion (LibreOffice → PDF → OpenDataLoader)
- [x] Spreadsheet ingestion (`openpyxl`)
- [x] OCR integration (`ocrmypdf`)
- [x] File hashing — SHA-256 via `_sha256_of_file()` (RI-009 closed 2026-04-14)
- [ ] OCR parallelization (carried as Phase 1B §11 Phase 2/3)
- [x] Registry rotation — closed 2026-04-14 via Sprint C quality pass (RI-008)

## Phase 1B — Multi-Parser Integration ✅ COMPLETE (2026-04-15 after Tranches 1-3 + Sprint PIPELINE-CLI)

**Foundation (§11 Phase 1) — COMPLETE 2026-04-14** (9 commits, 80 new tests, 177 → 257 passing):
- [x] RI-009: SHA-256 content hash (`FileEntry.sha256`, `_sha256_of_file()`, CSV output)
- [x] `BaseParser` ABC + `ParserTelemetry` (17 fields, kw_only) + `ParseResult` (kw_only)
- [x] Document taxonomy classifier (`DocumentClass` enum 9 members, `classify_document()`, CL-001–CL-008)
- [x] Quality Gates module (`GateStatus`, `GateResult`, `GateReport`, `run_quality_gates()`, GATE-001–004)
- [x] `ParserOrchestrator` skeleton — synchronous fallback chain walker with defensive chain copy
- [x] `scripts/vitruvius/parsers/` subpackage with public re-exports from `__init__.py`

**Modernization (§11 Phase 2) — COMPLETE 2026-04-15** (Tranches 1 + 2 scoped + 3; AD-031, AD-032, AD-033, AD-034):
- [x] Wrap existing parsers (OpenDataLoader, OpenPyxl) behind `BaseParser` — Sprint PIPELINE-CLI AD-040
- [x] Integrate Docling parser (`DoclingParser`) — Sprint 1B-M1 AD-031
- 🚫 Integrate Marker parser (`MarkerParser`) — **DEFERRED per AD-032** (disk at 95.2%, RAM 2.03 GB at feasibility check; ML-dep install too large for 8 GB M2 default profile)
- 🚫 Integrate Surya OCR — **DEFERRED per AD-032** (same feasibility blocker as Marker)
- [x] OCR preprocessor (`OCRPreprocessor` wrapping `ocrmypdf`) — Sprint 1B-M2 AD-032
- [x] LibreOffice preprocessor (`LibreOfficePreprocessor`) — Sprint 1B-M1 AD-031
- [x] Post-LibreOffice quality gates (GATE-005) — Sprint 1B-M1 AD-031
- [x] Migrate `scripts/vitruvius/conversion.py` parser selection to `BaseParser` wrappers — Sprint PIPELINE-CLI AD-040 via `convert-parsers-one` + `build_default_orchestrator()` factory
- [x] Flattened telemetry JSON sidecar per file — delivered with Foundation
- [x] **Bonus**: `RustPdfParser(BaseParser)` — Sprint 1B-M3 AD-034 (audit GO verdict AD-033 = 48× smaller RSS + 625× faster than docling on synthetic PDFs)
- [x] **Bonus**: GATE-006 min-chars-per-page quality gate — Sprint 1B-M3 AD-034

**Scaling & Governance (§11 Phase 3) — PARTIAL 2026-04-15** (batch API shipped; true process-pool fan-out still deferred):
- [~] `ParserOrchestrator.process_batch` batch API shipped with `max_workers` compatibility, but the current implementation remains sequential and reserves real `ProcessPoolExecutor` fan-out for a future upgrade — see `parsers/orchestrator.py`
- [x] Per-parser timeout enforcement — shipped inside orchestrator fallback chain
- [x] `GoldenCorpusBenchmark` harness (30-document fixture) — Sprint 1B-M2 AD-032
- [x] `pipeline_cli.py` flag dispatch — Sprint PIPELINE-CLI AD-040 (`convert-parsers-one` subcommand + byte-identity exit gate + parallel command pattern)
- [x] Expanded registry + per-file sidecar metadata writers — delivered incrementally across Foundation + Tranche 1
- [ ] Page-level isolation for OOM/timeout recovery — **deferred** (no AD; would require per-parser SIGTERM handling; out of current scope)
- [ ] Hallucination Trap quality gate — **adjacent work shipped** (GATE-006 min-chars-per-page is a partial mitigation; full hallucination trap still deferred)
- [ ] Manual Review Lane + Ranger Audit Payload generator — **externally gated** on the Ranger dashboard surface (same gate as Sprint D Stream J)

**Plan:** `/.ai/09_archive/plans/phase-1b-multi-parser-integration-plan.md` (archived 2026-04-15 after Tranches 1-3 + Sprint PIPELINE-CLI closed the Phase 2 + Phase 3 backlog — AD-031/032/033/034/040)

## Phase 1C — Centralized Normalization ✅ MVP COMPLETE (2026-04-14)
- [x] `NormalizationEngine` with phase-locked execution
- [x] `NormalizationRule` protocol
- [x] Tier A rules (Unicode NFC, control chars, whitespace, CRLF, blank-line collapse)
- [x] Tier B rules (Setext→ATX, SEC. → SECTION, heading-whitespace trim)
- [ ] Tier C rules (opt-in semantic corrections) — deferred
- [x] `.refined.json` manifest sidecar
- [ ] Destructive transformation guard (per-class thresholds) — deferred
- [ ] Contract validator (rejects malformed Phase 1B output) — deferred
- [x] `refine` CLI stage integration
- [ ] Slug/ID collision policy + alias registry — deferred
- [ ] Table isolation protocol (whitespace phase) — deferred
- [x] Idempotency test harness (unit + real-data byte-identical check)

**Plan:** `/.ai/09_archive/plans/phase-1c-centralized-normalization-plan.md` (archived)

## Phase 2 — Canonicalization ✅ COMPLETE (2026-04-14)
- [x] Rules engine (`canonical_rules.yaml`)
- [x] Strict ID system (`<prefix>-<slug>`)
- [x] YAML frontmatter + header generation
- [x] Single-file CLI (`canonicalize-one`)
- [x] Structured-section generation (Overview / Coverage / Key Points / Referenced Concepts)
- [x] Batch canonicalization mode (`canonicalize` command)
- [x] `resolve_referenced_concepts()` matches hyphenated + spaced forms
- [x] Diff-before-write protection (`canonical_diff.should_overwrite`) with volatile-field stripping

**Plan:** `/.ai/09_archive/plans/phase-2-canonicalizer-restoration-plan.md` (archived)

## Phase 3 — Concept Layer ✅ 16/20 ENRICHED (2026-04-14, deterministic)
- [x] Concept file generation with valid YAML frontmatter
- [x] 20+ PD 1096 concepts seeded
- [x] Definition extraction from sources (regex anchors + section-title extractor with alias dict)
- [x] Regulatory basis linkage (each enriched concept → ≥1 source section ID)
- [x] Alias miner (parenthetical abbreviations + "also known as" phrases)
- [x] `concept_status` lifecycle field (placeholder / draft / enriched / verified)
- [x] Zero LLM calls (fully deterministic pipeline)
- [x] 16/20 PD 1096 concepts enriched end-to-end
- [ ] Bidirectional concept-to-concept cross-references — deferred
- [ ] Remaining 4 concepts (`exit-width`, `parking-and-loading-spaces`, `setbacks`, `yards`) — need inline phrase-density extraction or second corpus

**Plan:** `/.ai/09_archive/plans/phase-3-concept-enrichment-plan.md` (archived)

## Phase 4 — Identity Cleanup & Migration ✅ COMPLETE
- [x] `migrate-ids-plan` / `migrate-ids-apply` scripts
- [x] `id_migration_map.yaml`
- [x] Initial legacy ID normalization pass
- *Note: remains an operating rule for any future ID change.*

## Phase 5 — Relationship Extraction 🟡 PARTIAL (REGEX + DEDUP + FILTER)
- [x] Regex pattern extractor (`relationships.py`)
- [x] Section-aware extraction (`relationships_sections.py`) with `source_section_id`
- [x] Aggregate deduplication by `(from, predicate, to)`
- [x] **Endpoint dedup** (`dedupe_by_endpoints`) — registry-aware, collapses 5-predicates-per-edge variants — AD-014, AD-016
- [x] **Pre-review filter** (`pre_review_filter.py`) — 8 deterministic rules (A1-A4, R1-R2, R5, R7) cut LLM calls by 78% on PD 1096 — AD-018, AD-021
- [x] False-positive rate: 82% → effectively ~10% (6/9 auto-rejected deterministically)
- [ ] LLM-assisted candidate generation (Phase 5E — future, gated on 6B)

## Phase 6A — Local LLM Review ✅ COMPLETE (2026-04-14, full gap closure)
- [x] Ollama integration (`ollama_review.py`)
- [x] Default model configurable (`config/vitruvius.yaml` → `review.ollama.default_model`)
- [x] Three decisions: keep / review_further / reject
- [x] Confidence scoring 0.0–1.0 with clamping
- [x] Interruption-safe partial saves
- [x] Progress tracking (in_progress / completed / interrupted)
- [x] Ollama URL in config file (RI-003 closed)
- [x] High-confidence output writer
- [x] Automatic pipeline integration via `run-with-review` composite command
- [x] Per-candidate retry with bounded attempts + wall-clock cap
- [x] Resume-from-progress on relaunch
- [x] Opt-in parallelization (`--parallel N`)
- [x] Model warmup before batch (avoids cold-start retry budget burn)
- [x] Pre-review filter integration (auto-accept/reject before LLM call)

**Plan:** `/.ai/09_archive/plans/phase-6a-review-gap-closure-plan.md` (archived)

## Phase 6B — Second-Pass Review ✅ COMPLETE (2026-04-14)
- [x] `review-relationships-ollama-second-pass` CLI command
- [x] `select_for_second_pass()` — uncertain-candidate filter (all 5 entry criteria)
- [x] `route_adjudication()` — full decision table from `.ai/08_prompts/qwen-second-pass.txt`
- [x] Tier 2 prompt builder (`build_second_pass_prompt`) with `agrees_with_tier_one` field
- [x] Orchestrator with graceful Ollama fallback
- [x] Merged adjudication report (`latest_relationship_review_merged.json`)
- [x] 3x3 agreement matrix
- [x] Human escalation worklist (`latest_human_escalation_worklist.json`)
- [x] Real-data smoke-tested on PD 1096 with `gemma4:e4b` (qwen3:30b awaits hardware)

**Plan:** `/.ai/09_archive/plans/phase-6b-second-pass-review-plan.md` (archived)

## Phase 7 — Promotion Governance ✅ COMPLETE (2026-04-14)
- [x] **A-1** Ollama URL moved to `config/vitruvius.yaml` (RI-003 closed)
- [x] **A-1** `latest_relationship_review_high_confidence.json` writer
- [x] **A-2** `relationship_registry.yaml` (closed vocabulary + compatibility)
- [x] **A-3** `promotion_validator.py` (§3.5 schema enforcement — all 17 rules)
- [x] **A-4** `run_promote` CLI with dry-run default
- [x] **A-4** Evidence-array merge logic with fingerprint deduplication
- [x] **A-4** `promotion_audit.log` writer (append-only)
- [x] **A-4** `--rollback <batch_id>` mode
- [x] **A-5** First 3 PD 1096 relationships promoted end-to-end
- [x] **A-5** Idempotency verified (byte-identical files on re-run, `skipped=3`)
- [x] **A-5** Rollback verified
- [x] **A-6** Decision log `AD-011` written

**Input file:** `latest_relationship_review_high_confidence.json` (A-1, working)
**Output dir:** `003_Canonical-Knowledge-Layer/shared/relationships/` (3 new records)
**Test coverage:** 43/43 passing
**Sprint A closed:** 2026-04-14

## Phase 8 — Graph Contract & Indexing ✅ SUBSUMED (Sprint D Stream H, 2026-04-14)
Base work shipped inside Sprint D Stream H. Sprint GT (tag `sprint-gt-closed`) extended with temporal edges, Parquet archiver, spatial GraphRAG, pyo3 Rust crate + linear octree. Sprint HP.3-R (tag `sprint-hp3r-closed`) replaced the SQLite event store with a RocksDB-backed `RocksDBEventStore` (AD-029: 18.7× faster at n=10000). See `.ai/09_archive/plans/phase-8-graph-contract-indexing-plan.md`.

## Phase 8 — Graph Contract & Indexing (historical checklist — for reference only)
**Gate:** Phase 7 producing ≥50 verified relationships.
- [ ] `graph_contract.py` schema validator
- [ ] Filesystem graph builder (in `005_Operational-Intelligence-Layer/graph/`)
- [ ] `latest_graph_snapshot.json` artifact
- [ ] Graph traversal library (neighbors, typed edges, evidence paths)
- [ ] CLI: `build-graph`, `query-graph`, `export-graph-snapshot`
- [ ] Integrity checks (orphans, dangling edges, type compatibility)
- [ ] Determinism test (same input → byte-identical snapshot)

## Phase 9 — Query & AI Layer ✅ SUBSUMED (Sprint D Stream I, 2026-04-14)
Base work shipped inside Sprint D Stream I. No follow-up sprint has extended this — Query/AI integration for external consumers is gated on Sprint D Stream J (Ranger dashboard surface), externally blocked. See `.ai/09_archive/plans/phase-9-query-ai-layer-plan.md`.

## Phase 9 — Query & AI Layer (historical checklist — for reference only)
**Gate:** Phase 8 stable; ≥200 verified relationships.
- [ ] Structured query interface
- [ ] Source-traceable answers (every response cites section IDs)
- [ ] Confidence-aware output
- [ ] Optional NL front-end (structured translation only, no free generation)
- [ ] CLI: `query "<natural language question>"`
- [ ] Citation accuracy ≥95% on seed-question suite

## Phase 10 — Canonical Relationship Storage
**Merged into Phase 7.** Storage format = Phase 7 deliverable. No separate tracking.

## Phase 11 — Dataset Expansion 🔒 GATED
**Do not start generic expansion.** Gated until Phase 7 validates PD 1096 for ≥1 week with zero audit violations AND 1B/1C are shipping.
- **Bounded pilot note (2026-04-16):** the accepted `/.ai/03_plans/2026-04-16_laws-mini-dataset-graph-pipeline-plan.md` M1 scoped graph proof may proceed as a bounded validation lane only. It does **not** open generic Phase 11 dataset expansion and must remain inside the plan’s additive manifest-scoped guardrails.
- **Resume note (2026-04-18):** the current bounded continuation point is the `ready-family-aggregate` residual-hardening lane, not a new tranche family. The verified baseline is `20260418T023807Z` with `143 nodes / 266 edges / 1 warning / 45 covered folders / 1 partial folder`; the only truthful remaining residual family is `RA-386` / `law-civil-code-of-the-philippines`. See `/.ai/05_logs/2026-04-18_residual-cluster-concept-admission-validation.md`.
- **Parent-lane note (2026-04-18):** `ready-family-aggregate` is the current combined proving surface for the larger laws-wave/operatorization lane. The broader laws-wave state in `/.ai/10_state/laws-wave-status.json` is `saturated_truth_complete` with `41/47` raw folders covered, `25` completed lanes, and a preserved artifact stack (`laws-completed-lanes.yaml`, `laws-remaining-dispositions.yaml`, `laws-source-provenance.yaml`, `laws-manifest-index.yaml`). Resume from that parent context before assuming the next task is only about the aggregate viewer.
- **Execution note (2026-04-16):** the bounded `laws-core-bundle-m1` pilot was implemented and validated as `PARTIAL`; bounded follow-on work then executed inside the accepted pilot lane:
  - M2A source admission is complete for `RA-9514`, `BP-344`, and `BP-220`
  - M2B additive dataset-safe extraction/review/second-pass/promotion path wiring is complete
  - conservative dataset-scoped relationship admission is now complete for `RA-9514` (2 admitted relationship inputs)
  - concept-fit follow-on work admitted minimal law-specific concepts and relationship-backed edges for `BP-344` and `BP-220`
  - M3 orchestration is now complete via the bounded `run-dataset-graph` composite command
  - the four-folder bounded pilot now reaches `SUCCESS`; see `/.ai/05_logs/2026-04-16_laws-core-bundle-bounded-pilot-success-validation.md`
  - M4 expansion-path follow-on is now complete for the accepted minimal slice: model/spec artifacts plus additive `law_units` manifest/runtime/reporting support; see `/.ai/05_logs/2026-04-16_laws-m4-expansion-path-validation.md`
  - the bounded pilot now has a single-command operator lane (`run-laws-pilot` / `./run-laws-pilot`) plus self-contained browser HTML output; see `/.ai/05_logs/2026-04-17_laws-pilot-operator-experience-validation.md`
  - a post-pilot readiness-only expansion lane now exists: `run-laws-all-dry-run` plus `m2-8gb-safe` review preset; see `/.ai/05_logs/2026-04-17_all-laws-readiness-8gb-implementation-validation.md`
  - tranche-expansion implementation now exists as the next safe execution boundary: `laws-tranche-1.yaml`, `run-laws-tranche-dry-run`, and automated structure guardrails; see `/.ai/05_logs/2026-04-17_laws-tranche-expansion-implementation-validation.md`
  - tranche source-preparation dry-run now exists for pre-conversion readiness: `run-laws-tranche-source-prep-dry-run`; see `/.ai/05_logs/2026-04-17_laws-tranche-source-prep-dry-run-validation.md`
  - tranche source-preparation execute step now exists: `run-laws-tranche-source-prep`; see `/.ai/05_logs/2026-04-17_laws-tranche-source-prep-implementation-validation.md`
  - tranche-1 source-admission dry-run now exists: `run-laws-tranche-source-admission-dry-run`; see `/.ai/05_logs/2026-04-17_laws-tranche-1-source-admission-implementation-validation.md`
  - tranche-1 source-admission execute step now exists: `run-laws-tranche-source-admission`; `PD-957` duplicate/raw-alias variants collapse to one admitted IRR source, `PD-1185` is admitted, and `PD-1216` stays blocked pending OCR; see `/.ai/05_logs/2026-04-17_laws-tranche-1-source-admission-execution-validation.md`
  - duplicate-readiness checkpoint now exists: `run-laws-duplicate-dry-run`, and duplicate cluster summaries now appear inside all-laws and tranche readiness reports; see `/.ai/05_logs/2026-04-17_laws-duplicate-readiness-validation.md`
  - tranche-local source-to-graph dry-run now exists: `run-laws-tranche-source-to-graph-dry-run`, which stages only admitted tranche members while keeping `PD-1216` blocked and execute still gated; see `/.ai/05_logs/2026-04-17_laws-tranche-source-to-graph-dry-run-validation.md`
  - PD-957 concept-fit admission slice now exists: three shared concepts plus three dataset-scoped `governs` relationships are admitted, and the tranche source-to-graph dry-run no longer reports shallow representation; see `/.ai/05_logs/2026-04-17_pd957-concept-fit-admission-validation.md`
  - PD-1216 OCR-first preparation slice now exists: OCR outputs plus canonical admission now stage all three tranche laws through source-to-graph dry-run while execute remains gated; see `/.ai/05_logs/2026-04-17_pd1216-ocr-first-preparation-validation.md`
  - tranche-local source-to-graph execute now exists: `run-laws-tranche-source-to-graph` builds the bounded tranche graph lane with all three laws staged and preserves duplicate visibility; see `/.ai/05_logs/2026-04-17_laws-tranche-source-to-graph-execute-validation.md`
  - bounded risk-hardening pass now improves tranche reporting: duplicate/raw-alias visibility is explicit for `PD-957` and OCR-quality spot-review counts are explicit for `PD-1216`; see `/.ai/05_logs/2026-04-17_laws-risk-hardening-execution-validation.md`
  - tranche-2 now exists and executes through the same bounded workflow: `config/datasets/laws-tranche-2.yaml` stages `RA-7279`, `RA-4726`, and `RA-7899`; see `/.ai/05_logs/2026-04-17_laws-tranche-2-execution-validation.md`
  - tranche-2 graph-richness follow-on now exists: a bounded `RA-7899` concept-fit slice raises tranche-2 graph output from `3 nodes / 0 edges` to `4 nodes / 1 edge`; see `/.ai/05_logs/2026-04-17_ra7899-concept-fit-admission-validation.md`
  - tranche-2 condominium-law vocabulary is now expanding: a bounded `RA-4726` common-areas slice raises tranche-2 graph output from `4 nodes / 1 edge` to `5 nodes / 4 edges`; see `/.ai/05_logs/2026-04-17_ra4726-common-areas-concept-fit-validation.md`
  - tranche-2 housing-policy richness is now expanding: a bounded `RA-7279` socialized-housing slice raises tranche-2 graph output from `5 nodes / 4 edges` to `6 nodes / 5 edges`; see `/.ai/05_logs/2026-04-17_ra7279-socialized-housing-concept-fit-validation.md`
  - tranche-3 now exists and executes through the same bounded workflow: `config/datasets/laws-tranche-3.yaml` stages `PD-1067`, `PD-1151`, and `RA-9003`; current execute evidence shows `raw_alias_law_folders = [PD-1067]`, `generated_relationship_count = 1`, `shallow_representation_count = 0`, and graph snapshot `7 nodes / 11 edges`; see `/.ai/05_logs/2026-04-17_laws-tranche-3-execution-validation.md`
  - tranche source admission now respects manifest-level authoritative/excluded variant intent and preserves blocked-law raw-anchor intent on manifest writeback; see `/.ai/05_logs/2026-04-17_tranche-source-admission-variant-selection-validation.md`
  - tranche-3 graph-richness follow-on now exists: a bounded `PD-1067` water-governance slice raises tranche-3 graph output from `4 nodes / 0 edges` to `7 nodes / 11 edges`; see `/.ai/05_logs/2026-04-17_pd1067-water-governance-concept-fit-validation.md`
  - tranche-4 now exists and executes through the same bounded workflow: `config/datasets/laws-tranche-4.yaml` stages `PD-1517`, `RA-6969`, and `RA-10066`; current execute evidence shows `generated_relationship_count = 1`, `spot_review_required_count = 1`, `shallow_representation_count = 0`, and graph snapshot `6 nodes / 7 edges`; see `/.ai/05_logs/2026-04-17_laws-tranche-4-execution-validation.md`
  - tranche-4 graph-richness follow-on now exists: a bounded `RA-10066` cultural-heritage slice raises tranche-4 graph output from `3 nodes / 0 edges` to `6 nodes / 7 edges`; see `/.ai/05_logs/2026-04-17_ra10066-cultural-heritage-concept-fit-validation.md`
  - tranche-5 now exists and executes through the same bounded workflow: `config/datasets/laws-tranche-5.yaml` stages `PD-856`, `RA-7160`, and `RA-9257`; current execute evidence shows `generated_relationship_count = 7`, `shallow_representation_count = 0`, and graph snapshot `13 nodes / 24 edges`; see `/.ai/05_logs/2026-04-17_tranche-5-richness-validation.md`
  - tranche-6 now exists and executes through the same bounded workflow: `config/datasets/laws-tranche-6.yaml` stages `RA-4566`, `RA-386`, and `RA-9184`; current execute evidence shows `generated_relationship_count = 3`, `shallow_representation_count = 0`, and graph snapshot `7 nodes / 9 edges`; see `/.ai/05_logs/2026-04-17_laws-tranche-6-execution-validation.md`
  - tranche-7 now exists and executes through the same bounded workflow: `config/datasets/laws-tranche-7.yaml` stages `RA-1378`, `RA-9285`, and `RA-11201`; current execute evidence shows `generated_relationship_count = 0`, `shallow_representation_count = 0`, and graph snapshot `7 nodes / 6 edges`; excluded plumbing-code / board files remain explicit raw aliases for `RA-1378`; see `/.ai/05_logs/2026-04-17_laws-tranche-7-execution-validation.md`
  - tranche-8 now exists and executes through the same bounded workflow: `config/datasets/laws-tranche-8.yaml` stages `RA-11285`; current execute evidence shows `generated_relationship_count = 0`, `shallow_representation_count = 0`, and graph snapshot `4 nodes / 6 edges`; see `/.ai/05_logs/2026-04-17_laws-tranche-8-execution-validation.md`
  - tranche-9 now exists and executes through the same bounded workflow: `config/datasets/laws-tranche-9.yaml` stages scoped DENR/DOE/DPWH guidance surfaces; current execute evidence shows `generated_relationship_count = 0`, `shallow_representation_count = 0`, and graph snapshot `3 nodes / 0 edges`; see `/.ai/05_logs/2026-04-17_laws-tranche-9-execution-validation.md`
  - remaining uncovered-pool roadmap now exists with concrete future tranche proposals, remediation lanes, and a realistic remaining-lane estimate; see `docs/LAWS_REMAINING_POOL_ROADMAP.md`
  - tranche-10 selection now favors duplicate-remediation-first `RA-9266`, with overlap-closure `PD-9514` deferred to the following lane; see `docs/LAWS_REMAINING_POOL_ROADMAP.md`
  - tranche-10 now exists and executes through the same bounded workflow: `config/datasets/laws-tranche-10.yaml` stages `RA-9266` as a duplicate-remediation-first singleton with explicit raw-alias visibility; current execute evidence shows `generated_relationship_count = 0`, `shallow_representation_count = 0`, and graph snapshot `1 nodes / 0 edges`; see `/.ai/05_logs/2026-04-17_laws-tranche-10-execution-validation.md`
  - tranche-11 now exists and executes through the same bounded workflow: `config/datasets/laws-tranche-11.yaml` stages `PD-9514` as a singleton overlap-closure lane; current execute evidence shows `generated_relationship_count = 7`, `shallow_representation_count = 0`, and graph snapshot `10 nodes / 10 edges`; see `/.ai/05_logs/2026-04-17_laws-tranche-11-execution-validation.md`
  - tranche-12 now exists and executes through the same bounded workflow: `config/datasets/laws-tranche-12.yaml` stages scoped EO and DHSUD guidance surfaces from the legacy combined `HLURB-DHSUD` raw folder; current execute evidence shows `generated_relationship_count = 3`, `shallow_representation_count = 0`, and graph snapshot `7 nodes / 6 edges`; see `/.ai/05_logs/2026-04-17_laws-tranche-12-execution-validation.md`
  - tranche-13 now exists and executes through the same bounded workflow: `config/datasets/laws-tranche-13.yaml` stages scoped CHED/CIAP/UAP professional-standard surfaces; current execute evidence shows `generated_relationship_count = 0`, `spot_review_required_count = 2`, `shallow_representation_count = 0`, and graph snapshot `8 nodes / 6 edges`; CHED OCR-first preparation is complete and the bounded UAP concept-fit slice clears the tranche shallow-representation guardrail; see `/.ai/05_logs/2026-04-17_laws-tranche-13-execution-validation.md`
  - tranche-14 now exists and executes through the same bounded workflow: `config/datasets/laws-tranche-14.yaml` stages scoped DOH/DEPED guidance surfaces; current execute evidence shows `generated_relationship_count = 0`, `manual_review_required_count = 1`, `shallow_representation_count = 0`, and graph snapshot `8 nodes / 12 edges`; the bounded guidance concept-fit slice clears the DEPED shallow-representation finding while DOH table-heavy manual-review risk remains explicit; see `/.ai/05_logs/2026-04-18_laws-tranche-14-execution-validation.md`
  - tranche-15 prep now enters LGU sharding/remediation rather than a normal bundle execute; current scouting shows `56` LGU raw files and `2` exact duplicate clusters before any truthful shard manifest can be opened; see `/.ai/03_plans/2026-04-18_tranche-15-sharding-plan.md`
  - first LGU shard scouting now identifies a San Mateo zoning/CLUP pair as the strongest small candidate, but shard duplicate readiness still reports `duplicate_law_folders = [LGU]` because unrelated duplicates elsewhere in the folder remain visible; see `/.ai/05_logs/2026-04-18_tranche-15-first-shard-scout-validation.md`
  - the first LGU shard now executes cleanly via `config/datasets/laws-tranche-15-san-mateo.yaml`; duplicate readiness now respects selected shard scope, the San Mateo concept slice clears shallow representation, and current execute evidence shows `generated_relationship_count = 2` with graph snapshot `7 nodes / 7 edges`; the wider LGU lane still remains open because only the first shard is complete; see `/.ai/05_logs/2026-04-18_laws-tranche-15-san-mateo-validation.md`
  - the second LGU shard now executes cleanly via `config/datasets/laws-tranche-15-dagupan.yaml`; current execute evidence shows `generated_relationship_count = 3`, `shallow_representation_count = 0`, and graph snapshot `8 nodes / 7 edges`; the wider LGU lane still remains open because only San Mateo and Dagupan are completed shards so far; see `/.ai/05_logs/2026-04-18_laws-tranche-15-dagupan-validation.md`
  - the third LGU shard now executes cleanly via `config/datasets/laws-tranche-15-malolos.yaml`; current execute evidence shows `generated_relationship_count = 2`, `shallow_representation_count = 0`, and graph snapshot `4 nodes / 5 edges`; the wider LGU lane still remains open because only San Mateo, Dagupan, and Malolos are completed shards so far; see `/.ai/05_logs/2026-04-18_laws-tranche-15-malolos-validation.md`
  - the fourth LGU shard now executes cleanly via `config/datasets/laws-tranche-15-meycauayan.yaml`; current execute evidence shows `generated_relationship_count = 2`, `shallow_representation_count = 0`, and graph snapshot `5 nodes / 5 edges`; the wider LGU lane still remains open because only San Mateo, Dagupan, Malolos, and Meycauayan are completed shards so far; see `/.ai/05_logs/2026-04-18_laws-tranche-15-meycauayan-validation.md`
  - the fifth LGU shard now executes cleanly via `config/datasets/laws-tranche-15-davao.yaml`; current execute evidence shows `generated_relationship_count = 0`, `shallow_representation_count = 0`, and graph snapshot `3 nodes / 2 edges`; review signals remain explicit because the Davao source is a slide-deck/graphic-heavy planning surface; see `/.ai/05_logs/2026-04-18_laws-tranche-15-davao-validation.md`
  - the sixth LGU shard now executes cleanly via `config/datasets/laws-tranche-15-tarlac.yaml`; current execute evidence shows `generated_relationship_count = 2`, `shallow_representation_count = 0`, and graph snapshot `5 nodes / 5 edges`; the wider LGU lane still remains open because only San Mateo, Dagupan, Malolos, Meycauayan, Davao, and Tarlac are completed shards so far; see `/.ai/05_logs/2026-04-18_laws-tranche-15-tarlac-validation.md`
  - the seventh LGU shard now executes cleanly via `config/datasets/laws-tranche-15-ordinance-2117.yaml`; current execute evidence shows `generated_relationship_count = 0`, `shallow_representation_count = 0`, and graph snapshot `3 nodes / 3 edges`; review signals remain explicit because the QC-CBD source is layout-heavy and image-backed in places; see `/.ai/05_logs/2026-04-18_laws-tranche-15-ordinance-2117-validation.md`
  - the eighth LGU shard now executes cleanly via `config/datasets/laws-tranche-15-pasay.yaml`; current execute evidence shows `generated_relationship_count = 1`, `shallow_representation_count = 0`, and graph snapshot `6 nodes / 5 edges`; review signals remain explicit because the Pasay source required OCR-first preparation and still carries a spot-review/suppressed-summary path; see `/.ai/05_logs/2026-04-18_laws-tranche-15-pasay-validation.md`
  - the RA-9279 remediation-first lane now executes cleanly via `config/datasets/laws-tranche-ra-9279-remediation.yaml`; current execute evidence shows `generated_relationship_count = 0`, `shallow_representation_count = 0`, and graph snapshot `4 nodes / 4 edges`; the folder/file mismatch is now resolved truthfully by admitting the Section 18 RA 7279 IRR as the actual source identity; see `/.ai/05_logs/2026-04-18_laws-ra-9279-remediation-validation.md`
  - the PRC lane now executes cleanly via `config/datasets/laws-tranche-prc.yaml`; current execute evidence shows `generated_relationship_count = 2`, `shallow_representation_count = 0`, and graph snapshot `12 nodes / 10 edges`; manual-review and summary-withheld signals remain explicit for the weaker PRBoA effectivity-dates source and other guarded resolution surfaces; see `/.ai/05_logs/2026-04-18_laws-tranche-prc-validation.md`
  - the HLURB/DHSUD agency split is now modeled truthfully in tranche metadata: `config/datasets/laws-tranche-12.yaml` stages `DHSUD` guidance surfaces from the legacy combined `HLURB-DHSUD` raw folder, and focused raw-folder-override regression coverage is now in place; see `/.ai/05_logs/2026-04-18_hlurb-dhsud-agency-split-validation.md`
  - final remaining-pool disposition is now explicit: `RA-11361`, `RA-7920`, `HB-3391`, `HB-5207`, `SB-2982`, and `BERDE` are all tracked as defer/final-disposition lanes rather than normal tranche candidates; see `/.ai/05_logs/2026-04-18_remaining-pool-final-disposition-validation.md`
  - machine-readable remaining-pool disposition artifact now exists at `config/datasets/laws-remaining-dispositions.yaml`
  - ready-family aggregate operator alignment is now complete: the one-command operator path no longer reintroduces duplicate-edge regressions; see `/.ai/05_logs/2026-04-18_ready-family-operator-alignment-validation.md`
  - residual-cluster concept admission is now complete: `RA-9285`, `RA-6969`, and `RA-1378` moved into the aggregate through conservative concept admission, leaving only `RA-386` residual; see `/.ai/05_logs/2026-04-18_residual-cluster-concept-admission-validation.md`
  - current checked-in viewer artifact for that baseline: `004_Derived-Content-Layer/graph-visualizations/ready-family-aggregate.html`
  - laws-wave end-state artifacts now make the broader bounded lane resumable without replaying chat history:
    - `config/datasets/laws-completed-lanes.yaml`
    - `config/datasets/laws-remaining-dispositions.yaml`
    - `config/datasets/laws-source-provenance.yaml`
    - `config/datasets/laws-manifest-index.yaml`
    - `docs/LAWS_WAVE_ARTIFACT_INDEX.md`
    - `/.ai/05_logs/2026-04-18_laws-wave-completion-summary.md`
  - generic Phase 11 expansion remains gated
- [ ] PD 1096 IRR ingestion
- [ ] Occupancy tables (structured spreadsheet pathway)
- [ ] Lighting and ventilation sections
- [ ] Additional Philippine building laws

## Phase 12 — AI-Augmented Reasoning 🔒 GATED
**Do not start.** Gated until Phase 9 is in production with ≥95% citation accuracy and ≥500 verified relationships.
- [ ] Concept enrichment proposals
- [ ] Semantic linking suggestions
- [ ] Question generation
- [ ] Wiki article drafting
- [ ] Learning path generation

---

## Cross-Phase Technical Debt
See `/.ai/10_state/known_issues.md` for the risk register (RI-001…RI-011).

## References
- Master roadmap: `/.ai/01_roadmap/master-roadmap.md`
- Current sprint: `/.ai/01_roadmap/current-phase.md`
- Audit pack: `/.ai/02_audits/*`
- Phase plans: `/.ai/03_plans/*`
- Schemas: `/.ai/06_specs/*`
- State snapshot: `/.ai/10_state/*`

---

# 2026-04-15 Session — 20 Sprints Closed (Governing-Plan + Phase 1B + Post-Z Optimization Queue)

The following **twenty** sprints were delivered under subagent-driven-development across the 2026-04-15 session. All produced `sprint-*-closed` git tags. Full ledgers live in `.ai/10_state/decisions.md` **AD-024 through AD-042** (plus **AD-038a** for the Sprint RUST-MIG-1 N1 DEFER_ALREADY_NATIVE verdict).

## Sprint Q — Live Wiring & 8GB Hardening ✅ CLOSED (tag `sprint-q-closed`)
- [x] W1 — 8GB LLM Survival Mode (model pool + num_ctx cap + budget guard + binary mode, +17 tests)
- [x] W2 — Review Pipeline Wiring (NB prefilter + ontology prompt + SLM router + conformal + tension/reflection + Choquet, +15 tests)
- [x] W3 — Stringency Matrix Live Gate (20-concept migration + lint rule + promotion hook + governing-standard field, +13 tests)
- [x] W4 — Quality Harness (e2e chain test + flag-OFF regression + bench harness + decision-log automation, +7 tests)
- [x] W5 — Docs Sync (bundled in docs commit)
- **Total:** +48 tests, 15 functional commits, archived at `.ai/09_archive/plans/live-wiring-and-8gb-hardening-plan.md`

## Sprint R — Per-Layer Embeddings & Agentic ✅ CLOSED (tag `sprint-r-closed`)
- [x] Y0 — Bootstrap & flags (priming/ shell, 5 y_* flags, backward-compat regression)
- [x] Y1 — Contextual priming (source identity vector, prompt prefix injector, drift detector, ontology wiring, extraction wiring)
- [x] Y2 — Domain-routing MoE (classifier, route_with_moe, policy file + loader, reviewer model hook)
- [x] Y3 — Thinking mode + CoT audit (parse_cot_strict, audit writer, enforcement, ple-cotrace-dump CLI)
- [x] Y4 — Stateful agentic registry (SQLite core, ollama_review wiring, vacuum/purge CLI, Phase 6A Resume integration)
- [x] Y5 — Vision OCR (wrapper with mocked tests, table_graph_extractor fallback, ple-vision-probe CLI, operator checklist)
- **Total:** 20/20 tasks, archived at `.ai/09_archive/plans/per-layer-embeddings-agentic-upgrade-plan.md`
- Note: Y5 requires operator activation (install psutil + Pillow + pull moondream + run probe + flip flag). Non-Y5 flags fully code-complete.

## Sprint PHYS — Graph Physics ✅ CLOSED (tag `sprint-phys-closed`)
- [x] PHYS.1 — PageRank over canonical relationship graph
- [x] PHYS.2 — Boltzmann stability gate (absorbs orphan Stream O VF2 motif matcher)
- [x] PHYS.3 — Shannon entropy sampler
- [x] PHYS.4 — Eigenvector centrality cascade sim
- **Total:** 4 streams + orphan absorption shipped atomically, archived at `.ai/09_archive/plans/phase-16-statistical-mechanics-graph-physics-plan.md`

## Sprint H — 3D Spatial Intelligence ✅ CLOSED (tag `sprint-h-closed`)
- [x] Streams L/M/N/O — 20/20 tasks shipped
- [x] TypeScript sibling subproject at `spatial-daemon/` (GJK + AABB + contract writer + CLI; 20/20 vitest tests)
- [x] Z3 solver integration for spatial constraints (Stream L.5)
- [x] IFC registry loader + OWL exporter (M.1/M.2)
- **Total:** 20/20 tasks, archived at `.ai/09_archive/plans/3d-spatial-intelligence-upgrade-plan.md`

## Sprint GEOM — Geometric Constraint Engine ✅ CLOSED (tag `sprint-geom-closed`)
- [x] GEOM.1 — Inequality compiler (Z3 CSP from canonical rules)
- [x] GEOM.2 — Envelope 2D (shapely)
- [x] GEOM.3 — Envelope 3D (trimesh + mapbox-earcut + manifold3d)
- [x] GEOM.4 — Multimodal IoU audit (cvxpy Pareto optimizer)
- **Total:** 4 streams shipped, archived at `.ai/09_archive/plans/phase-15-geometric-constraint-engine-plan.md`

## Sprint WIKI — Autonomous Knowledge Synthesis ✅ CLOSED (tag `sprint-wiki-closed`)
- [x] WIKI.1 — Docling parser + Kuzu hybrid store
- [x] WIKI.2 — Delta tracker + synthesis loop
- [x] WIKI.3 — SHA-256 delta linting + LLM ego-graph linter
- [x] WIKI.4 — Ollama client adapter for synthesis loop + ego linter
- **Total:** 4 streams shipped, archived at `.ai/09_archive/plans/phase-14-autonomous-knowledge-synthesis-plan.md`

## Sprint GT — Geo-Topological Knowledge Graph ✅ CLOSED (tag `sprint-gt-closed`)
- [x] GT.1 — pyo3 Rust crate scaffold (Cargo workspace, core + pyo3_shim)
- [x] GT.2 — Linear octree (SpatialPoint + LinearOctree exposed to Python)
- [x] GT.3 — Temporal knowledge graph (TemporalEdge + versioned query + Parquet archiver)
- [x] GT.4 — Spatial GraphRAG bridge (proximity jump + decay-weighted edges)
- [x] GT.5 — Hardware hardening (mmap + Bloom filter + MC dropout)
- **Total:** 5 streams shipped, archived at `.ai/09_archive/plans/phase-8b-geo-topological-graph-plan.md`

## Sprint HP — High-Performance Optimizations ✅ CLOSED (tag `sprint-hp-closed`)
- [x] HP.1 — Merkle directory hash
- [x] HP.2 — AST chunking (retroactively covered by Sprint D Stream C.2)
- [x] HP.3 — SQLite append-only event store (pivoted from RocksDB — no wheel at time of HP closure)
- [x] HP.4 — Wasm spatial kernels (engine_rs workspace split)
- [x] HP.5 — GraphSAGE loopholes detector
- **Total:** 5 streams shipped, archived at `.ai/09_archive/plans/phase-13-high-performance-optimizations-plan.md`

## Sprint Z — Compound AI Evolution ✅ CLOSED (tag `sprint-z-closed`)
- [x] S1 — Neuro-symbolic Datalog bridge (Rust `datalog_rs` crate + pyo3 + prompt directive)
- [x] S2 — Proposer/Inspector/Adjudicator adversarial swarm
- [x] S3 — Differential dataflow (Delta + DependencyTracker + DifferentialPropagator)
- [x] S4 — Wasm kernel (workspace split + wasmtime loader)
- [x] S5 — DSPy prompt compiler
- **Total:** 5 streams shipped, archived at `.ai/09_archive/plans/phase-12-compound-ai-evolution-plan.md`

## Sprint HP.3-R — RocksDB KV Migration ✅ CLOSED (tag `sprint-hp3r-closed`)
- [x] Task 1 — SQLite baseline bench harness (`scripts/vitruvius/bench/bench_kv_backends.py`)
- [x] Task 2 — Install rocksdict 0.3.29 binding + smoke test
- [x] Task 3 — Feature flags `hp_rocksdb_event_store` + `hp_rocksdb_verdict_cache`
- [x] Task 4 — `RocksDBEventStore` class (+ concurrent-read lock fix via `AccessType.read_only()`)
- [x] Task 5 — `RocksDBStatefulReviewRegistry` class
- [x] Task 6 — Factory dispatch (`make_event_store`, `make_stateful_registry`; purge CLI routed through factory)
- [x] Task 7 — `ple-kv-migrate` CLI (idempotent, dry-run capable, both event + registry paths)
- [x] Task 8 — RocksDB bench + decision gate + O(1) count() optimization via `meta:*_count` keys
- [x] Task 9 — Flag flip + AD-029 + docs + archival + closing fixes (`flush()` API parity on SQLite class)
- **Total:** 14 commits shipped, archived at `.ai/09_archive/plans/2026-04-15-rocksdb-kv-migration-plan.md`
- **Bench at n=10000:** RocksDB **18.7× faster** on event store (0.1888s vs 3.5313s), **24.3× faster** on verdict cache (0.1480s vs 3.6004s). Flag defaults flipped to `true` per AD-029.

## Sprint 1B-M1 — Phase 1B Modernization Tranche 1 ✅ CLOSED (tag `sprint-1b-m1-closed`)
- [x] `DoclingParser(BaseParser)` — wraps `docling 2.88` parser chain
- [x] `LibreOfficePreprocessor` — Office→PDF via subprocess dispatch
- [x] `GATE-005` post-LibreOffice quality gate
- [x] `ParserOrchestrator.preprocessors` kwarg wiring
- [x] 2 new `p1b_*` feature flags (`p1b_docling_parser`, `p1b_libreoffice_preprocessor`, both default `false`)
- **AD:** AD-031. **Plan:** `.ai/09_archive/plans/2026-04-15-phase-1b-modernization-tdd-plan.md`

## Sprint 1B-M2 — Phase 1B Modernization Tranche 2 (scoped) ✅ CLOSED (tag `sprint-1b-m2-closed`)
- [x] `OCRPreprocessor` wrapping `ocrmypdf`
- [x] `ParserOrchestrator.process_batch` with `ProcessPoolExecutor` parallelism
- [x] `GoldenCorpusBenchmark` 30-document fixture harness
- [x] 2 new `p1b_*` feature flags (`p1b_ocr_preprocessor`, `p1b_process_pool_orchestration`)
- 🚫 Marker-pdf 1.10.2 + Surya-ocr 0.17.1 **DEFERRED** per AD-032 feasibility finding (disk at 95.2%, RAM headroom 2.03 GB)
- **AD:** AD-032. **Plan:** `.ai/09_archive/plans/2026-04-15-phase-1b-modernization-tranche-2-plan.md`

## Sprint RUST-PDF-1 — Rust PDF Ingestion Audit ✅ CLOSED (tag `sprint-rust-pdf-1-closed`)
- [x] `vitruvius_rust_pdf` lopdf-backed Cargo crate + pyo3 bindings
- [x] Subprocess-isolated bench vs docling + opendataloader_pdf
- [x] **GO verdict:** 13.7 MB peak RSS (**48× smaller** than docling) + 0.05 s wall (**625× faster**) on synthetic PDFs
- [x] Unlocks the low-spec M2 target
- **AD:** AD-033. **Plan:** `.ai/09_archive/plans/2026-04-15-rust-pdf-audit-plan.md`

## Sprint 1B-M3 — Phase 1B Modernization Tranche 3 ✅ CLOSED (tag `sprint-1b-m3-closed`)
- [x] `RustPdfParser(BaseParser)` wraps the `vitruvius_rust_pdf` Rust crate from Sprint RUST-PDF-1
- [x] `GATE-006` min-chars-per-page quality gate
- [x] `p1b_rust_pdf_parser` feature flag (default `false`)
- [x] Real-PDF quality rollback gate: **LCS similarity 0.9925** on `History of Architecture Sample Exam.pdf` vs pypdf baseline
- **AD:** AD-034. **Plan:** `.ai/09_archive/plans/2026-04-15-phase-1b-modernization-tranche-3-plan.md`

## Sprint DISTILL-1 — LLM Reviewer Distillation Audit ✅ CLOSED with DEFER_NO_DATA (tag `sprint-distill-1-closed`)
- [x] `distillation_audit.py` corpus inspector walks 5 known cache locations
- 🚫 **DEFER_NO_DATA verdict**: Sprint R Y4 verdict cache is empty (0 verdicts < 50 threshold). Audit harness committed for re-run after live LLM review populates the cache.
- **Unblocker**: run `run-with-review` with `y_stateful_registry=true` + `w_review_nb_prefilter=true` + `w_review_choquet_aggregator=true` on ≥20 PD 1096 sections
- **AD:** AD-035. **Plan:** `.ai/09_archive/plans/2026-04-15-llm-distillation-audit-plan.md`

## Meta — Docs Cleanup Sprint ✅ CLOSED (no git tag — meta sprint)
- [x] `.ai/00_system/architecture.md` + `pipeline-overview.md` refreshed post-Sprint-Z
- [x] `.ai/01_roadmap/master-roadmap.md` bumped to v2.1.0 (then v2.2.0 → v2.3.0 in later passes)
- [x] `.ai/02_audits/` banners marked historical snapshots
- [x] `.ai/10_state/known_issues.md` reconciled
- [x] 3 superseded plans archived (phase-8, phase-9, ultimate-architecture)
- [x] `INDEX.md` reconciled
- **Plan:** `.ai/09_archive/plans/2026-04-15-docs-cleanup-plan.md`

## Sprint RUST-MIG-1 — Python→Rust Polyglot Split ✅ CLOSED (tag `sprint-rust-mig-1-closed`)
- [x] S1 `build_spatial_adjacency_edges` Rust port — **200× raw kernel speedup** (0.836 ms vs ~170 ms at n=2000); O(n²) → O(n log n) via existing `LinearOctree::query_aabb`
- [x] S2 `weight_by_distance` Rust port — **12.18× raw kernel / 2.84× end-to-end** (0.183 ms vs 2.234 ms at n=10000); pure `exp(-λd)` loop
- [x] N4 Mahalanobis core Rust port — **2.73× end-to-end** via nalgebra (34.16 ms vs 93.28 ms at n=1000 queries, 64-dim); WeakKeyDictionary cache keyed on `OutlierModel` instances
- 🚫 N1 sliced Wasserstein — **DEFER_ALREADY_NATIVE** per AD-038a (thin `ot.emd2` wrapper over POT's native C++ network simplex LP)
- [x] Two new member crates in `engine_rs/` workspace: `spatial_kernels` + `stats_kernels`
- [x] `rust_mig_spatial_kernels` + `rust_mig_stats_kernels` feature flags **flipped to `true`** per AD-038 (both kernels cleared the ≥2× bench threshold)
- **AD:** AD-036 (crate layout), AD-037 (Sprint LSH-1 premise correction), AD-038 (sprint closure), AD-038a (N1 DEFER). **Plan:** `.ai/09_archive/plans/2026-04-15-rust-migration-audit-plan.md`

## Sprint AUDIT-1 — Advanced Tech Audit ✅ CLOSED (tag `sprint-audit-1-closed`)
- [x] Task 1: FlatBuffers audit harness — **NO_GO verdict** (pure-Python flatbuffers 5-10× SLOWER than CPython `_json` at ~150 B records)
- [x] Task 2: Numerical Integrity audit — **GO_GAP verdict** → shipped SHA-256 integrity footer for spatial contracts (`spatial/contract_reader.py` + `spatial-daemon/src/contract_writer.ts` `writeContract()` appends `# sha256:` footer)
- [x] Task 3: Monte Carlo Dropout site survey — **PARK verdict** (0 of 5 neural-inference modules viable; GraphSAGE explicitly disables dropout via `torch.no_grad()`)
- **AD:** AD-039. **Plan:** `.ai/09_archive/plans/2026-04-15-advanced-tech-audit-plan.md`

## Sprint PIPELINE-CLI — `p1b_*` Flag Integration ✅ CLOSED (tag `sprint-pipeline-cli-closed`)
- [x] `parsers/factory.py::build_default_orchestrator()` — lru_cached factory that reads all 5 `p1b_*` flags and wires the right parser chain + preprocessors
- [x] `parsers/cli_handler.py::run_convert_parsers_one()` — path-resolve + classify + factory-dispatch + file-write + exit-code orchestration
- [x] New `convert-parsers-one` CLI subcommand registered in `pipeline_cli.py` (parallel command pattern — does NOT modify `convert-one` so byte-identity with flags OFF is structurally guaranteed)
- [x] Byte-identity exit gate: parametrized `--help` check across 8 pre-plan commands + lazy-import contract extension of AD-015 + empty-stderr check
- [x] **Side-fix:** `RustPdfParser` was in `parsers/__init__.py::__all__` but never imported (broken since AD-034) — fixed as part of the Task 1 commit
- **AD:** AD-040. **Plan:** `.ai/09_archive/plans/2026-04-15-pipeline-cli-integration-plan.md`

## Sprint PQ-1 — GraphSAGE Product Quantization ✅ CLOSED (tag `sprint-pq-1-closed`)
- [x] `PQCodebook` + `train_pq_codebook()` — pure numpy k-means with BLAS GEMM + `np.argmin` + `np.add.at`
- [x] `encode_to_pq()` + `decode_from_pq()` — vectorized L2 via GEMM + integer-index gather
- [x] `adc_distance()` — asymmetric distance computation for fast approximate queries
- [x] `save_codebook()` / `load_codebook()` — npz roundtrip
- [x] `compress_graphsage_report()` integration helper
- [x] `hp_graphsage_pq` feature flag (default `false` — stays false pending embedding persistence layer)
- **Measured:** 32× exact compression (256 B/node → 8 B/node), **0.00017 cosine similarity delta** (117× under the 0.02 gate)
- **AD:** AD-041. **Plan:** `.ai/09_archive/plans/2026-04-15-graphsage-pq-embeddings-plan.md`

## Sprint LSH-1 — MinHash Fuzzy Near-Duplicate Dedup ✅ CLOSED (tag `sprint-lsh-1-closed`)
- [x] `minhash.py::compute_minhash_signature()` — Carter-Wegman MinHash (SHA-256 base hash + numpy broadcast grid + 31-bit Mersenne modulus) — **70× faster** than initial nested-loop (8 s → 108 ms at n=1000)
- [x] `lsh_index.py::LSHIndex` — band-based bucketing with `num_perm=256, num_bands=32, r=8` (99% recall at J≥0.78)
- [x] `lsh_dedup.py::dedupe_by_endpoints_lsh()` — fuzzy layer on top of exact `dedupe_by_endpoints`
- [x] `w_lsh_dedup` feature flag (default `false` pending PD 1096 operator validation)
- [x] Reframed per AD-037 — this sprint ships fuzzy near-duplicate detection (semantic variants like "lot area ≥ 100 sqm" vs "minimum lot area of 100 square meters"), NOT an O(n²) scaling fix (which was the original-audit's misclaim)
- **Measured:** 14.17% fuzzy hit rate at 20% injection (> 10% AD-037 gate), **0 false positives** on 200-candidate disjoint audit
- **AD:** AD-042. **Plan:** `.ai/09_archive/plans/2026-04-15-lsh-dedup-plan.md`

## Session-level totals (2026-04-15 19:50, post-LSH-1 + path-rewrite sweep)
- **Python test suite:** 297 → **1528 passing**, 1 skipped (+1231 delta across the session)
- **TypeScript test suite:** 20 → **21 / 21 passing** (`spatial-daemon/` — +1 integrity footer assertion from Sprint AUDIT-1)
- **Rust unit tests:** 10 → **33 passing** (23 new from Sprint RUST-MIG-1: 7 adjacency_edges + 6 distance_weight + 10 mahalanobis; plus wasm api tests + datalog_rs)
- **New Rust crates / workspace members:** `engine_rs` workspace (existing) extended with `spatial_kernels` + `stats_kernels` + `pdf` crates (2 new, 1 from Sprint RUST-PDF-1); `datalog_rs` (existing)
- **New TypeScript sibling:** 1 (`spatial-daemon/`, extended in Sprint AUDIT-1 with integrity footer writer)
- **New Python subpackages:** 10 (`compound/`, `wiki/`, `geometric/`, `foraging/`, `priming/`, `bench/`, `relationships/minhash.py`, `relationships/lsh_index.py`, `relationships/lsh_dedup.py`, `spatial/_feature_gate.py`)
- **Plans archived:** 22 (12 from the Sprint-Q→HP.3-R burst + 3 from the 2026-04-15 cleanup pass + 5 from the Phase 1B tranches + 2 from the post-Z optimization queue that landed in-sprint + 3 from the final 2026-04-15 cleanup pass archiving `phase-1b`, `statistical-architectural-upgrade`, `ingestion-refinement-contract`)
- **ADs added:** AD-024 through **AD-042** plus **AD-038a** (20 entries)
- **Git tags:** **20** total sprint tags (10 original governing-plan sprints: `sprint-q/r/phys/h/geom/wiki/gt/hp/z/hp3r-closed`; 5 Phase 1B tranche tags: `sprint-1b-m1/1b-m2/rust-pdf-1/1b-m3/distill-1-closed`; 5 post-Z optimization queue tags: `sprint-rust-mig-1/audit-1/pipeline-cli/pq-1/lsh-1-closed`)
- **Branch:** `main` fully pushed to `origin/main` at commit `119cba3` (post-Sprint-LSH-1 + path-rewrite sweep); Git remote auth fixed via `gh auth setup-git`

## Active plans folder state
As of 2026-04-16, `.ai/03_plans/` again contains **multiple live-reference plans**. The authoritative live inventory is `/.ai/03_plans/INDEX.md`; any older claim that the directory contains exactly 2 files is stale.

Current live plan families include:
- governing dispatcher + active plan-layer rewrite
- nested AGENTS governance
- accepted laws mini dataset→graph plan + accepted bounded M2 follow-on
- draft graph-warning / GitNexus warning investigation
- planning-only AEC family
