# Milestone Tracker

> **Source of truth:** This tracker is reconciled against `/.ai/01_roadmap/master-roadmap.md` §4 and the 2026-04-13 audit pack.
> **Legend:** `[x]` complete · `[~]` partial / skeleton · `[ ]` not started · `🔒` gated (do not start) · `🔥` highest priority
> **Revised:** 2026-04-14

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
- [ ] Registry rotation (carried as RI-008)

## Phase 1B — Multi-Parser Integration 🔥 IN PROGRESS (Foundation shipped 2026-04-14)

**Foundation (§11 Phase 1) — COMPLETE** (9 commits, 80 new tests, 177 → 257 passing):
- [x] RI-009: SHA-256 content hash (`FileEntry.sha256`, `_sha256_of_file()`, CSV output)
- [x] `BaseParser` ABC + `ParserTelemetry` (17 fields, kw_only) + `ParseResult` (kw_only)
- [x] Document taxonomy classifier (`DocumentClass` enum 9 members, `classify_document()`, CL-001–CL-008)
- [x] Quality Gates module (`GateStatus`, `GateResult`, `GateReport`, `run_quality_gates()`, GATE-001–004)
- [x] `ParserOrchestrator` skeleton — synchronous fallback chain walker with defensive chain copy
- [x] `scripts/vitruvius/parsers/` subpackage with public re-exports from `__init__.py`

**Modernization (§11 Phase 2) — PENDING (Sprint C continuation):**
- [ ] Wrap existing parsers (OpenDataLoader, OpenPyxl) behind `BaseParser`
- [ ] Integrate Docling parser (`DoclingParser`)
- [ ] Integrate Marker parser (`MarkerParser`)
- [ ] Integrate Surya OCR
- [ ] OCR preprocessor + LibreOffice preprocessor
- [ ] Post-LibreOffice quality gates
- [ ] Migrate `scripts/vitruvius/conversion.py` parser selection to `BaseParser` wrappers
- [ ] Flattened telemetry JSON sidecar per file

**Scaling & Governance (§11 Phase 3) — PENDING (Sprint C continuation):**
- [ ] `ProcessPoolExecutor` with dynamic resource allocation (RAM queues)
- [ ] Timeout enforcement (120s per parser)
- [ ] Page-level isolation for OOM/timeout recovery
- [ ] Golden Corpus Benchmark (30 documents)
- [ ] Expanded registry + per-file sidecar metadata writers
- [ ] Hallucination Trap quality gate
- [ ] Manual Review Lane + Ranger Audit Payload generator

**Plan:** `/.ai/03_plans/phase-1b-multi-parser-integration-plan.md`

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

## Phase 8 — Graph Contract & Indexing [ ] NOT STARTED
**Gate:** Phase 7 producing ≥50 verified relationships.
- [ ] `graph_contract.py` schema validator
- [ ] Filesystem graph builder (in `005_Operational-Intelligence-Layer/graph/`)
- [ ] `latest_graph_snapshot.json` artifact
- [ ] Graph traversal library (neighbors, typed edges, evidence paths)
- [ ] CLI: `build-graph`, `query-graph`, `export-graph-snapshot`
- [ ] Integrity checks (orphans, dangling edges, type compatibility)
- [ ] Determinism test (same input → byte-identical snapshot)

## Phase 9 — Query & AI Layer [ ] NOT STARTED
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
**Do not start.** Gated until Phase 7 validates PD 1096 for ≥1 week with zero audit violations AND 1B/1C are shipping.
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
