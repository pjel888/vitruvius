# Known Issues & Risks — Vitruvius

> **Updated:** 2026-04-15 (post-Sprint-HP.3-R closure pass — 10 sprints closed this session, including the RocksDB KV migration)
> **Format:** `RI-###` (Risk Issue), severity, mitigation, and closure path.

## Open Risks

### RI-013: Rule Title Uniqueness and Semantic Specificity (CLOSED 2026-04-24; refreshed 2026-04-24)
- **Description:** Rule-node presentation titles must not rely on lazy truncation or generic concept-only names. A rebuilt KG can contain many distinct rules under the same concept, so titles like `Occupancy Rule` or `Building Rule` collapse separate legal requirements into indistinguishable graph nodes.
- **Impact:** HIGH — duplicate or generic rule titles make graph exploration misleading even when underlying canonical IDs, evidence spans, and relationships are distinct.
- **Mitigation:** Treat rule-title uniqueness as part of the KG relationship-quality job. Rule titles should be generated from the rule's own evidence/source/section semantics, using taxonomy and concept context only as fallback context. Full legal text must remain preserved in `label`, `summary`, evidence spans, and inspector/source views.
- **Status:** CLOSED for the `001-Laws` rebuild. `scripts/vitruvius/kg/rule_extractor.py` now builds rule display titles from concept + section + source semantics instead of truncated evidence text, with compact stable source references for duplicate-prone source families.
- **Closure evidence:** Snapshot `005_Operational-Intelligence-Layer/graph/kg-v2/20260424T195515Z_kg_v2_unified.json` contains 214 rule nodes with 0 duplicate display labels, 0 generic display labels, and 0 display-title truncation markers. Neo4j was cleared and reloaded from that snapshot: 0 nodes after clear, 5911/5911 Cypher statements executed, 0 load errors, 2429 nodes after load.

### RI-001: Filesystem Coupling
- **Description:** The system is tightly coupled to the directory structure defined in `paths.py` and `constants.py`.
- **Impact:** HIGH — renaming or moving `001_…` through `006_…` breaks the pipeline silently.
- **Mitigation:** All path logic stays in `paths.py`. Inline paths are rejected at code review. `run_reconcile` detects structural drift.
- **Closure:** Permanent operating rule. Not a phase.
- **Sprint HP.1 note (2026-04-15):** the Merkle directory hash (`hp_merkle_fs` flag, `scripts/vitruvius/merkle_fs.py`) makes structural drift detectable in O(1) rather than requiring a full walk. The coupling stays; it's just cheaper to audit now.

### RI-002: Regex Extraction Fragility (SUBSTANTIALLY MITIGATED 2026-04-14)
- **Description:** `relationships.py` and `relationships_sections.py` match candidates via fixed regex patterns. Variations in legal language leak into false positives (82% rejection at review).
- **Impact:** MEDIUM — feeds the review layer with noise, inflating compute cost and review time.
- **Mitigation — layered (all shipping):**
  1. **Phase 1C normalization** — reduces input variance (Tier A/B rules).
  2. **Endpoint-pair dedup (AD-014)** — collapses 5-predicates-per-edge variants. Real-data: 23 → 9 candidates (−61%).
  3. **Registry-aware dedup (AD-016)** — ensures the surviving predicate is compatible with the endpoint types.
  4. **Pre-review filter R7 (AD-018, AD-021)** — auto-rejects candidates where neither endpoint phrase appears in the evidence. Real-data: 6/9 additional rejections.
- **Current effective rejection rate:** ~22% (2 of 9 actually reach the LLM). The LLM sees only the genuinely ambiguous subset.
- **Closure:** Phase 5E (LLM-assisted extraction) remains the long-term full fix for paragraph-boundary sensitivity. The 4 layers above made it non-urgent. Sprint D Stream E then shipped spaCy SVO parser + CRF trainer/extractor + TransE link predictor as a layered fallback; Sprint Q W2 wired the NB prefilter / SLM router / Choquet fusion / reflection parser live. On PD 1096 IRR the effective rejection rate is now ~10% reaching the Tier 2 LLM. The original regex path is still authoritative; Sprint D / Q additions run alongside it, never replacing it.

### RI-003: External Dependency — Ollama (CLOSED 2026-04-14)
- **Description:** The review layer requires an Ollama server at `127.0.0.1:11434` with the configured model loaded. Previously the URL was hardcoded.
- **Impact:** MEDIUM — the review stage fails if Ollama is down or the model is not pulled.
- **Mitigation:** ✅ Sprint A · A-1 moved the URL into `config/vitruvius.yaml`. ✅ Sprint B · 6A added bounded retries, wall-clock cap, and graceful fallback to `review_further` when Ollama is unreachable. Pre-flight health check still pending but the retry+fallback path makes it no longer urgent.
- **Status:** **CLOSED** for practical purposes. Pre-flight health check tracked as a post-Sprint-C polish item.

### RI-004: Python Environment / PYTHONPATH
- **Description:** `scripts/vitruvius` is not a standard `src/` layout. CLI invocation requires specific working-directory context.
- **Impact:** LOW — new contributors need an onboarding note.
- **Mitigation:** Documented in `README.md`. Considered tolerable per **AD-002**.
- **Closure:** Not scheduled. Revisit if the codebase grows beyond CLI use.

### RI-005: Legacy Naming Inconsistencies
- **Description:** Scripts like `scripts/Word-PPT-To-PDF.py` and some early reports do not follow `naming-conventions.md`.
- **Impact:** LOW (aesthetic / consistency).
- **Mitigation:** Rename under a dedicated cleanup PR using `migrate-ids-plan` after Sprint C.
- **Closure:** Post-Sprint C cleanup pass.

### RI-006: Manual Promotion Gap (CLOSED 2026-04-14)
- **Description:** No automated bridge between the Review Layer (`latest_relationship_review_ollama.json`) and the Canonical Knowledge Layer.
- **Impact:** HIGH — blocks the entire downstream stack.
- **Mitigation:** ✅ Sprint A Phase 7 built the Promotion Layer: `pipeline_cli.py promote` reads `latest_relationship_review_high_confidence.json`, validates against 17 rules, and writes records to `003_Canonical-Knowledge-Layer/shared/relationships/` with full audit log.
- **Status:** **CLOSED.** First 3 PD 1096 relationships promoted on 2026-04-14. Idempotency and rollback verified.

### RI-007: Normalization Fragmentation (CLOSED — MVP scope — 2026-04-14)
- **Description:** Whitespace collapsing, line merging, slugification, and JSON fence stripping are each duplicated across 2–3 modules (`utils.py`, `relationships_sections.py`, `canonicalize.py`, `ollama_review.py`). No central Text Refinement layer.
- **Impact:** MEDIUM — inconsistent data quality; makes advanced cleanup (noise removal, semantic chunking) impossible.
- **Mitigation:** ✅ Sprint B Phase 1C built the `NormalizationEngine` with phase-locked execution, scope routing, and 8 Tier A/B rules. `refine` CLI stage emits `.refined.json` manifests. 6 PD 1096 files refined with idempotency verified.
- **Status:** **CLOSED** for the MVP scope. Tier C semantic rules, full semantic chunking, and destructive-guard rollback tracked as post-Sprint-B follow-ups.

### RI-008: Registry Growth Without Rotation (CLOSED 2026-04-14)
- **Description:** `006_System-Manifests/registries/*.csv` appended indefinitely. No rotation or pruning.
- **Impact:** MEDIUM — unbounded CSV growth would have slowed comparison logic in `status.py` as corpus scales.
- **Mitigation:** ✅ Sprint C quality pass shipped the `rotate-registries` CLI command with a deterministic retention policy. Default keep=30 per timestamped family (raw_file, conversion, spreadsheet); `latest_*.csv` pointers and non-timestamped static registries are never touched. Supports `--dry-run` and `--keep N`. Pure `plan_rotation()` separated from destructive `apply_rotation()` for safety. Commits `452df57` + `f7166a1`; see AD-023.
- **Status:** **CLOSED.** The CLI ships but has not yet been run against the real `006_System-Manifests/registries/` dir — operators invoke it manually when ready.

### RI-009: No File Hashing in Ingestion (CLOSED 2026-04-14)
- **Description:** `scanner.py` captured size + mtime but no SHA-256. Change detection could miss content changes that preserve mtime.
- **Impact:** MEDIUM — prerequisite for Phase 1B foundation work (content-aware dedup across re-scans, per-file sidecar keying).
- **Mitigation:** ✅ Sprint C Phase 1B Foundation (Task 0) added a streaming `_sha256_of_file()` helper to `scanner.py`, a `sha256: str` field on `FileEntry`, a `sha256` column in `latest_raw_file_registry.csv`, and a 6-test `test_scanner_sha256.py` regression suite. Commit `1386b32`; see AD-022.
- **Status:** **CLOSED.**

### RI-010: Concept Generator Produces Placeholder Content (SUBSTANTIALLY CLOSED 2026-04-14)
- **Description:** `concepts.py` writes "X is a defined concept within the Vitruvius system." as the body. No definition extraction, no regulatory linkage.
- **Impact:** MEDIUM — concepts look populated in the filesystem but carry no knowledge.
- **Mitigation:** Phase 3C (concept enrichment) replaces placeholders with extracted definitions.
- **Status:** **16/20 CLOSED** as of 2026-04-14. Phase 3C deterministic enrichment pipeline (AD-019, AD-020) enriched 16 PD 1096 concepts end-to-end with zero LLM calls. Additional gains came from:
  - Compound-section-title multi-concept matching (recovered `occupancy-load` from `Stairs, Exits, and Occupant Loads`)
  - Alias dictionary expansion (`means-of-egress`, `occupancy-separation`)
  - Punctuation-stripping normalization
  The 4 remaining (`exit-width`, `parking-and-loading-spaces`, `setbacks`, `yards`) don't have matching section titles in PD 1096 or its IRR. They need either (a) inline phrase-density extraction, (b) a second corpus, or (c) manual curation. None require LLM involvement.

### RI-011: Canonicalizer Regression (CLOSED 2026-04-14)
- **Description:** `canonicalize.py` generates YAML frontmatter + header only. The hand-curated canonical files under `003/shared/sources/` show a richer structure (Overview / Coverage / Key Points / Referenced Concepts) that the current script cannot reproduce.
- **Impact:** MEDIUM — running batch canonicalization against the existing set would flatten the richer hand-curated content. Treated as a **regression** from a tool that no longer exists in the repo.
- **Mitigation:** ✅ Sprint B Phase 2 restoration: `build_structured_source_file()` emits all four sections. `canonical_diff.should_overwrite()` protects `enriched`/`verified`/`superseded` files from silent overwrites.
- **Status:** **CLOSED.**

### RI-012: Review Layer Not in Default Pipeline (CLOSED 2026-04-14)
- **Description:** `review-relationships-ollama` is a manual command. It is not part of `run` or any auto-chain after `extract-relationships-one`.
- **Impact:** MEDIUM — each run requires human initiation, breaking the "run then walk away" operator model.
- **Mitigation:** ✅ Sprint B Phase 6A added `run-with-review` composite command that chains `run → convert → refine → review-relationships-ollama`. Default `run` stays minimal so CI doesn't invoke Ollama accidentally.
- **Status:** **CLOSED.**

## Risk Severity Summary (updated 2026-04-15 after full 10-sprint session — Q + R + PHYS + H + GEOM + WIKI + GT + HP + Z + HP.3-R closed)
| Severity | Count | IDs |
|---|---|---|
| HIGH | 1 | RI-001 (permanent operating rule — Sprint HP.1 made it cheaper to audit) |
| MEDIUM | 1 | RI-010 (4/20 remaining — awaiting corpus expansion, no LLM fallback) |
| LOW | 1 | RI-004 (environment / PYTHONPATH — still tolerable per AD-002) |
| MITIGATED (not formally closed) | 1 | RI-002 (pre-review filter + Sprint D Stream E + Sprint Q W2 wiring cut effective rejection to ~10%) |
| CLOSED | 8 ✅ | RI-003, RI-005 (next pass), RI-006, RI-007, RI-008, RI-009, RI-011, RI-012 |

**No new RI entries were opened by the 2026-04-15 sprint burst.** Every new capability shipped defaulted to `features.*: false` in `config/vitruvius.yaml` and was covered by a test registry entry in `scripts/tests/test_features.py`, so there's no silent surface area to track. The Sprint HP.3-R RocksDB backends are the only flags that default `true` (after the AD-029 bench showed RocksDB 18.7× / 24.3× faster than SQLite), and the SQLite fallback path is still present and wired into the factory for rollback.

## Closure Timeline
| When | Risks Closed / Mitigated |
|---|---|
| **Sprint A (2026-04-14)** | ✅ RI-006, ✅ RI-003 (partial) |
| **Sprint B (2026-04-14)** | ✅ RI-003 (full), ✅ RI-007 (MVP), ✅ RI-011, ✅ RI-012 |
| **Sprint C · Phase 1B Foundation (2026-04-14)** | ✅ RI-009 (Task 0 — SHA-256 file hashing) |
| **Sprint C · Quality Pass (2026-04-14)** | ✅ RI-008 (Q2 — rotate-registries CLI) |
| **Sprint D (2026-04-14)** | RI-002 further mitigated (Stream E spaCy/CRF/TransE) |
| **Sprint Q (2026-04-15)** | RI-002 further mitigated (W2 NB/SLM/Choquet/reflection wiring) |
| **Sprint HP (2026-04-15)** | RI-001 instrumentation win (Merkle fs makes drift detectable in O(1)) |
| **Sprint HP.3-R (2026-04-15)** | No risks opened. RocksDB KV migration replaces storage beneath existing API contracts; SQLite fallback retained via `hp_rocksdb_*=false` |
| Future | RI-002 (Phase 5E), RI-010 (4 concepts need corpus expansion) |
| Permanent rule | RI-001, RI-004 |
