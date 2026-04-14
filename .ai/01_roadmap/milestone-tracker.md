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
- [ ] File hashing (size + mtime only — carried as RI-009)
- [ ] OCR parallelization (carried as Phase 1B §11)
- [ ] Registry rotation (carried as RI-008)

## Phase 1B — Multi-Parser Integration 📝 PLANNED
- [ ] `BaseParser` interface + `ParserOrchestrator`
- [ ] Document taxonomy classifier (9 classes)
- [ ] Wrap existing parsers (OpenDataLoader, OpenPyxl)
- [ ] Integrate Docling parser
- [ ] Integrate Marker parser
- [ ] Integrate Surya OCR
- [ ] OCR preprocessor + LibreOffice preprocessor
- [ ] Flattened telemetry JSON sidecar
- [ ] Quality Gates 001–004
- [ ] Fallback chain orchestration
- [ ] Page-level isolation for OOM/timeout
- [ ] Dynamic resource allocation (`ProcessPoolExecutor` + memory buckets)
- [ ] Manual Review Lane + Ranger Audit Payload generator
- [ ] Golden Corpus Benchmark (30 documents)

**Plan:** `/.ai/03_plans/phase-1b-multi-parser-integration-plan.md`

## Phase 1C — Centralized Normalization 📝 PLANNED
- [ ] `NormalizationEngine` with phase-locked execution
- [ ] `NormalizationRule` protocol
- [ ] Tier A rules (Unicode NFC, control chars, whitespace)
- [ ] Tier B rules (structural, header standardization, semantic chunking)
- [ ] Tier C rules (opt-in semantic corrections)
- [ ] Five-phase execution pipeline (encoding → whitespace → structural → identifiers → cleanup)
- [ ] `.refined.json` manifest sidecar
- [ ] Destructive transformation guard (per-class thresholds)
- [ ] Contract validator (rejects malformed Phase 1B output)
- [ ] `refine` CLI stage integration
- [ ] Slug/ID collision policy + alias registry
- [ ] Table isolation protocol (whitespace phase)
- [ ] Idempotency test harness

**Plan:** `/.ai/03_plans/phase-1c-centralized-normalization-plan.md`

## Phase 2 — Canonicalization 🟡 PARTIAL (SKELETON)
- [x] Rules engine (`canonical_rules.yaml`)
- [x] Strict ID system (`<prefix>-<slug>`)
- [x] YAML frontmatter + header generation
- [x] Single-file CLI (`canonicalize-one`)
- [ ] Structured-section generation (Overview / Coverage / Key Points) — **REGRESSION**
- [ ] Batch canonicalization mode
- [ ] Frontmatter schema validation at write time
- [ ] Diff-before-write protection for manually edited files

## Phase 3 — Concept Layer 🟡 PARTIAL (PLACEHOLDERS)
- [x] Concept file generation with valid YAML frontmatter
- [x] 20+ PD 1096 concepts seeded
- [ ] Definition extraction from sources
- [ ] Regulatory basis linkage (each concept → ≥1 source section ID)
- [ ] Alias registry population
- [ ] Bidirectional concept-to-concept cross-references
- [ ] `concept_status` lifecycle field (placeholder / draft / enriched / verified)

## Phase 4 — Identity Cleanup & Migration ✅ COMPLETE
- [x] `migrate-ids-plan` / `migrate-ids-apply` scripts
- [x] `id_migration_map.yaml`
- [x] Initial legacy ID normalization pass
- *Note: remains an operating rule for any future ID change.*

## Phase 5 — Relationship Extraction 🟡 PARTIAL (REGEX-GRADE)
- [x] Regex pattern extractor (`relationships.py`)
- [x] Section-aware extraction (`relationships_sections.py`) with `source_section_id`
- [x] Deduplication
- [ ] False-positive rate < 50% (currently 82% rejection)
- [ ] LLM-assisted candidate generation (Phase 5E — future, gated on 6B)

## Phase 6A — Local LLM Review ✅ COMPLETE (with partial gap closure)
- [x] Ollama integration (`ollama_review.py`)
- [x] Default model `gemma4:31b`
- [x] Three decisions: keep / review_further / reject
- [x] Confidence scoring 0.0–1.0 with clamping
- [x] Interruption-safe partial saves
- [x] Progress tracking (in_progress / completed / interrupted)
- [x] **Move Ollama URL to config file** (closed 2026-04-14, Sprint A · A-1)
- [x] **High-confidence output writer** (closed 2026-04-14, Sprint A · A-1)
- [ ] Automatic pipeline integration (non-manual trigger) — Sprint C
- [ ] Per-candidate retry with bounded attempts — Sprint B
- [ ] Resume-from-progress on relaunch — Sprint B
- [ ] Sequential → parallelized processing — Sprint B

## Phase 6B — Second-Pass Review 📝 PLANNED (Sprint C)
- [ ] `review-relationships-ollama-second-pass` CLI command
- [ ] Uncertain-candidate filter (low-confidence `keep`/`reject`, all `review_further`)
- [ ] Tier 2 reviewer integration (`qwen3:30b` or smaller)
- [ ] Merged adjudication report with agreement matrix
- [ ] Human escalation worklist (Tier 3)
- [ ] Disagreement rate logging

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
