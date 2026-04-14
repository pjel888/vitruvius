# Active Context — Vitruvius

> **Updated:** 2026-04-14 (Sprints A + B closed same day)
> **Active sprint:** Awaiting user confirmation to start Sprint C / follow-ons
> **Prior sprint windows:** Sprint A · 2026-04-14 (Phase 7) · Sprint B · 2026-04-14 (Phases 1C MVP, 2, 6A)

## Where We Are
**Sprints A + B closed.** Four phases shipped end-to-end in a single execution pass: Phase 7 Promotion Governance (Sprint A), Phase 1C Centralized Normalization MVP (Sprint B), Phase 2 Canonicalizer Restoration (Sprint B), Phase 6A Review Layer Gap Closure (Sprint B). 81/81 tests passing.

The project now has a working end-to-end pipeline: **`run-with-review`** chains scan → status → lint → convert → refine → (canonicalize/extract — still per-file) → review → promote. Raw source flows to canonical relationship files with full audit trail.

**Honest position:** *late ingestion / early extraction with working promotion*. Ingestion works; canonicalization and concepts are skeletons; extraction is regex-grade (82% rejection); review works and emits high-confidence artifact; **promotion works end-to-end with idempotency and rollback**.

## Sprint A Outcomes (Phase 7)
- ✅ All 14 Phase 7 plan tasks executed.
- ✅ 3 new canonical relationship records promoted with strict idempotency and rollback.
- ✅ RI-003 partially closed (config), RI-006 fully closed.

## Sprint B Outcomes (Phases 1C, 2, 6A)

### Phase 1C — Centralized Normalization MVP
- ✅ `NormalizationEngine` with phase-locked execution and scope routing (`scripts/vitruvius/normalization/engine.py`).
- ✅ 5 Tier A rules: `unicode-nfc`, `strip-control-chars`, `normalize-line-endings`, `collapse-trailing-whitespace`, `collapse-consecutive-blank-lines`.
- ✅ 3 Tier B rules: `normalize-setext-to-atx`, `normalize-section-abbreviation`, `trim-heading-whitespace`.
- ✅ `refine` and `refine-one` CLI commands.
- ✅ `.refined.json` manifest per file with source/output hashes, rule audit, char delta.
- ✅ 6 PD 1096 raw markdown files refined successfully with real-data idempotency (output hash unchanged on re-run).
- ⏸️ Deferred: Tier C semantic rules, full 512-token semantic chunking, destructive-guard rollback, table isolation protocol, alias registry.
- ✅ RI-007 (normalization fragmentation) closed for the MVP scope.

### Phase 2 — Canonicalizer Restoration
- ✅ `build_structured_source_file()` generates Overview, Coverage, Key Points, and Referenced Concepts per `/.ai/06_specs/source-schema.md` §5.
- ✅ `canonical_diff.py` — `should_overwrite()` guards `enriched`/`verified`/`superseded` files from silent overwrites.
- ✅ `canonicalize` batch CLI walking `002_Raw-Conversion-Layer`.
- ✅ `resolve_referenced_concepts()` matches hyphenated and spaced forms against `003/shared/concepts`.
- ✅ RI-011 (canonicalizer regression) closed.

### Phase 6A — Review Layer Full Gap Closure
- ✅ Bounded retries with linear backoff and per-candidate wall-clock cap.
- ✅ Resume from `in_progress` snapshot on relaunch.
- ✅ Opt-in parallelization via `--parallel N` and `ThreadPoolExecutor`.
- ✅ `run-with-review` composite CLI command (scan → status → lint → convert → refine → review).
- ✅ RI-003 fully closed (config + health-related behavior), RI-012 (review not in pipeline) closed.

## Code Delivered (feat/phase-7-promotion-governance branch — now conceptually covers Sprints A + B)

### Phase 7 modules (Sprint A)
- `scripts/vitruvius/config.py` — central config loader
- `scripts/vitruvius/rules/relationship_registry.yaml`
- `scripts/vitruvius/promotion_validator.py` — 17-rule validator + canonical index
- `scripts/vitruvius/promotion.py` — orchestrator, merge, audit, rollback

### Phase 1C modules (Sprint B)
- `scripts/vitruvius/normalization/__init__.py`
- `scripts/vitruvius/normalization/engine.py` — NormalizationEngine, NormalizationRule protocol
- `scripts/vitruvius/normalization/rules_tier_a.py` — 5 Tier A rules
- `scripts/vitruvius/normalization/rules_tier_b.py` — 3 Tier B rules
- `scripts/vitruvius/normalization/refine.py` — `run_refine`, `run_refine_one`, manifest writer

### Phase 2 modules (Sprint B)
- `scripts/vitruvius/canonicalize.py` — restored with `build_structured_source_file`, `run_canonicalize`, extractors
- `scripts/vitruvius/canonical_diff.py` — diff-before-write protection

### Phase 6A modules (Sprint B)
- `scripts/vitruvius/ollama_review.py` — retry, resume, parallel, config-driven
- `scripts/pipeline_cli.py` — `promote`, `refine`, `refine-one`, `canonicalize`, `run-with-review`

### Tests (81 total, all passing)
| Module | Test file | Count |
|---|---|---|
| config | `test_config.py` | 4 |
| ollama_review high-conf | `test_high_confidence_writer.py` | 2 |
| ollama_review retry | `test_ollama_retry.py` | 3 |
| ollama_review resume | `test_ollama_resume.py` | 3 |
| ollama_review parallel | `test_ollama_parallel.py` | 2 |
| promotion registry | `test_registry_load.py` | 3 |
| promotion validator | `test_promotion_validator.py` | 17 |
| canonical index | `test_canonical_index.py` | 2 |
| promotion slug | `test_promotion_slug.py` | 4 |
| promotion merge | `test_promotion_merge.py` | 4 |
| promotion audit | `test_promotion_audit.py` | 2 |
| promotion write | `test_promotion_write.py` | 1 |
| run_promote | `test_run_promote.py` | 4 |
| normalization engine | `test_normalization_engine.py` | 4 |
| tier A rules | `test_rules_tier_a.py` | 7 |
| tier B rules | `test_rules_tier_b.py` | 6 |
| refine stage | `test_refine.py` | 4 |
| canonicalize body | `test_canonicalize_body.py` | 4 |
| canonicalize integration | `test_canonicalize_integration.py` | 1 |
| canonical_diff | `test_canonical_diff.py` | 4 |
| **Total** | | **81** |

## Awaiting
User review and confirmation to continue. The branch `feat/phase-7-promotion-governance` now contains Sprints A + B work (Phase 7 + 1C MVP + 2 + 6A). Nothing has been pushed to remote.

## Next Phase Candidates (user's choice)
- **Phase 6B Second-Pass Review** (Sprint C) — Qwen adjudication of low-confidence Gemma decisions; full TDD plan exists.
- **Phase 3C Concept Enrichment** — promote the 20 PD 1096 concept placeholders to enriched Knowledge Nodes; design spec exists.
- **Phase 1B Multi-Parser Integration** — the biggest ingestion upgrade; long design spec exists.
- **Phase 1C follow-ups** — Tier C semantic rules, semantic chunking, destructive guard, alias registry population (the scope deferred from the MVP).
- **Phase 8 Graph Contract & Indexing** — gated on ≥50 verified relationships (we have 3 so far; need 47 more, i.e., more PD 1096 review cycles or corpus expansion).
- **End-to-end rerun** — run `run-with-review` against the current corpus to generate more candidates, then re-promote. This is the highest-signal move if the question is *"does the 82% rejection rate shrink now that 1C is in place?"*.

## Minimizing AI Reliance (Post-Phase-6B, 2026-04-14)

Answer to the user's question "can we design the pipeline such that AI input is minimal?" — **yes**, in two ways now shipping:

### AD-018: Pre-Review Filter
`scripts/vitruvius/pre_review_filter.py` triages candidates before the LLM reviewer. Deterministic rules (registry compatibility, self-reference, evidence length, structural patterns) auto-accept or auto-reject candidates that don't need LLM judgment.

**Real-data impact on refined PD 1096:**
- Before filter: 9 candidates → 9 LLM calls
- After filter: 9 candidates → 7 LLM calls + 1 auto-accept + 1 auto-reject = **22% LLM savings, zero correctness loss**

The auto-accepted candidate (`law-nbc → governs → concept-building-permit` at 0.95 conf via structural pattern) flows straight through to Phase 7 promotion without touching Ollama.

### AD-019: Deterministic Concept Definition Extractor
`scripts/vitruvius/concept_definitions.py` — two extractors:
- **Anchor-based**: "shall mean", "is defined as", "means", etc. with 0.70-0.95 confidence ladder.
- **Section-title-based**: claims section bodies as definitions when the title matches a known concept.

**Real-data impact:** **7/20 PD 1096 concepts got definitions via section-title matching, zero LLM calls.** Gaps (13 concepts) require a section-title alias dictionary — still zero-LLM, just more configuration.

### Current pipeline AI-usage profile
| Stage | AI? | Notes |
|---|---|---|
| Ingestion, conversion, OCR | No | Deterministic parsers |
| Refinement (Phase 1C) | No | Tier A/B regex rules |
| Canonicalization (Phase 2) | No | Section/key-point extractors |
| Relationship extraction | No | Regex + dedup |
| **Pre-review filter** | **No** | **NEW: eliminates 22% of LLM calls** |
| Tier-1 review (Phase 6A) | Yes (reduced) | Only `needs_review` bucket |
| Tier-2 review (Phase 6B) | Yes (tiny subset) | Only uncertain Tier-1 output |
| Promotion (Phase 7) | No | Schema validation + merge |
| **Concept definition** | **No** | **NEW: 35% coverage deterministic** |

**Rough AI budget** on PD 1096 today: 7 Tier-1 calls + 2 Tier-2 calls = **9 Ollama calls for the full pipeline** (vs. 25+ in the pre-dedup, pre-filter era).

## Sprint B Polish (Post-Experiment, 2026-04-14)

Six tactical improvements landed after the end-to-end experiment, all committed to `feat/phase-7-promotion-governance`:

- ✅ **Task 1** — Regex extractor dedup by `(from, to)` → AD-014 · Real-data impact: 23 → 9 candidates on refined PD 1096.
- ✅ **Task 2** — Ollama model warmup before batch.
- ✅ **Task 3** — Lazy CLI imports → AD-015. `pipeline_cli.py promote --help` works without PDF deps installed.
- ✅ **Task 4** — Timestamp-aware diff in `canonical_diff.py`. Six volatile fields stripped before byte compare.
- ✅ **Task 5** — Legacy `utils.normalize_text` / `normalize_filename` deprecated.
- ✅ **Task 6** — `concepts.py` emits `canonical_status: placeholder` + `concept_status: placeholder` honestly.

Test coverage: **100/100 passing** (81 baseline + 19 polish).

## Reference Map
- Sprint plan (now historic) → `/.ai/01_roadmap/current-phase.md`
- Master roadmap → `/.ai/01_roadmap/master-roadmap.md` (Phase 7 status: ✅)
- Milestone tracker → `/.ai/01_roadmap/milestone-tracker.md` (Phase 7 all ticked)
- Audits → `/.ai/02_audits/`
- Phase plans → `/.ai/03_plans/` + `INDEX.md`
- Known issues → `/.ai/10_state/known_issues.md`
- Decisions → `/.ai/10_state/decisions.md` (AD-011 filled)

## Why This Order
1. **Phase 7 is unblocked.** Phase 6A already produces reviewed candidates. High-confidence `keep` decisions exist today.
2. **Normalization (1C) runs in parallel** in Sprint B — it shrinks noise but is not on Sprint A's critical path.
3. **Multi-parser (1B) is Sprint C** — it hardens the front end for corpus expansion.
4. **Nothing downstream of Phase 7 can start** until Phase 7 ships: graph (8), query (9), expansion (11), AI reasoning (12) are all gated.

## Active Deliverables (Sprint A)
- `config/vitruvius.yaml` — Ollama URL configurable
- `scripts/vitruvius/rules/relationship_registry.yaml`
- `scripts/vitruvius/promotion_validator.py`
- `scripts/vitruvius/promotion.py` + `pipeline_cli.py promote` command
- First 3 canonical relationship files under `003/shared/relationships/`
- `006_System-Manifests/runs/latest_promotion_audit.log`

## Status of Supporting Work
| Area | Status | Owner | Next step |
|---|---|---|---|
| Master roadmap v2.0.0 | ✅ Published | Architect | Revisit at sprint exit |
| Phase 6A gap closure (minimal) | 🟡 In progress (A-1) | Sprint A | Config move + high-confidence writer |
| Phase 7 implementation | 🟡 In progress (A-2…A-5) | Sprint A | Registry + validator + writer |
| Phase 1C normalization | 📝 Planned (Sprint B) | Sprint B | `NormalizationEngine` skeleton |
| Phase 1B multi-parser | 📝 Planned (Sprint C) | Sprint C | Orchestrator + taxonomy |
| Phase 6B second-pass | 📝 Planned (Sprint C) | Sprint C | Qwen integration |
| Phase 2 canonicalizer restoration | 📝 Planned (Sprint C) | Sprint C | Structured-section generator |

## Blockers
None internal to Sprint A. External: Ollama must be running for the end-to-end verification in A-5.

## Recent Decisions (see `decisions.md` for full entries)
- **AD-009 (2026-04-14):** Adopted master roadmap v2.0.0 with honest status reconciliation.
- **AD-010 (2026-04-14):** Adopted the three-sprint sequence (A: Promotion, B: Normalization, C: Multi-parser/Second-pass/Canonicalizer).

## Upcoming Decisions
- **AD-011:** Shape of the first promoted relationship record (written after A-5 runs).
- **AD-012:** Whether to promote before or after Phase 1C lands (default: yes, behind 0.90 confidence gate).

## Reference Map
- Sprint plan → `/.ai/01_roadmap/current-phase.md`
- Master roadmap → `/.ai/01_roadmap/master-roadmap.md`
- Milestone tracker → `/.ai/01_roadmap/milestone-tracker.md`
- Audits → `/.ai/02_audits/`
- Phase plans → `/.ai/03_plans/`
- Known issues → `/.ai/10_state/known_issues.md`
- Decisions → `/.ai/10_state/decisions.md`
