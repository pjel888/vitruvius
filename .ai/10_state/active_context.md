# Active Context — Vitruvius

> **Updated:** 2026-04-15 · Sprint Q (Live Wiring & 8GB Hardening) CODE-COMPLETE; Sprint R (Per-Layer Embeddings & Agentic) IN PROGRESS — Streams Y0 + Y2 shipped, Y1 blocked on sentence_transformers, Y3-Y5 pending
> **Branch:** `feat/sprint-r-per-layer-embeddings`
> **Test suite:** 1074 / 1074 passing (excluding the pre-existing untracked `test_ontology_owl_exporter.py` that references an unimplemented Stream M.3 OWL exporter — Sprint H scope)
> **Tag:** `sprint-q-closed` at commit `c3eb939` (code-complete; live RSS/latency bench pending)

## Sprint R Progress (2026-04-15)

| Stream | Scope | Status | Commits |
|---|---|---|---|
| Y0 — Bootstrap & flags | priming/ shell, 5 y_* flags in YAML, backward-compat regression | ✅ 2/3 (Y0.3 golden-fixture regression adapted to module-level asserts because `fixtures/golden_3_files` + `vitruvius.pipeline` don't exist in this codebase) | 9d7fc42, 570f162 |
| Y1 — Contextual priming (PLE) | Source identity vector, prompt prefix injector, drift detector, ontology prompt wiring, extraction wiring | ⚠ **BLOCKED** — requires `sentence_transformers` library which is not installed in this environment. Plan §3.1 assumed Stream A already installed it. Defer until operator runs `pip install sentence-transformers torch`. | — |
| Y2 — Domain-routing MoE | Domain classifier, route_with_moe, policy file + loader, select_review_model hook | ✅ 4/4 closed | ec746c5, d1edcfe, a511de3, bea5a93 |
| Y3 — Thinking mode + CoT audit | parse_cot_strict, cot_audit writer, ollama_review CoT enforcement, ple-cotrace-dump CLI | 📝 Next | — |
| Y4 — Stateful agentic registry | SQLite registry core, wire into ollama_review, vacuum + purge CLI, Phase 6A Resume integration test | 📝 Pending | — |
| Y5 — Vision OCR (gated) | Vision wrapper, table_graph_extractor fallback, ple-vision-probe, operator checklist | 🔒 Gated on `ple-vision-probe` pass (requires live Ollama) | — |

Sprint R is executing on `feat/sprint-r-per-layer-embeddings`. Every Y flag
defaults false, so the pipeline is still byte-identical to the pre-Sprint-R
baseline until an operator flips one on.

## Where We Are

The project has a working end-to-end deterministic-first pipeline:
```
raw → scan/status/lint → convert → refine (Phase 1C)
    → canonicalize (Phase 2) → extract (dedup) → pre-review-filter
    → Tier-1 LLM review (Phase 6A, reduced) → Tier-2 (Phase 6B)
    → promote (Phase 7)
```

AI is now the *exception*, not the rule. Most stages are zero-LLM. The review layer only judges candidates that deterministic rules couldn't auto-accept or auto-reject. Concept enrichment is fully deterministic.

**User priority:** 8 GB M2 MacBook Pro, `gemma4:e4b` only. Minimizing AI reliance is the design goal.

## Phases Shipped

| Phase | Status | AI? | Notes |
|---|---|---|---|
| 0 Foundation | ✅ | No | — |
| 1A Baseline Ingestion | ✅ | No | RI-008 **closed** (rotate-registries CLI); RI-009 **closed** (SHA-256 hash) |
| 1B Multi-Parser Integration | 🔥 Foundation + OpenDataLoader adapter | No | `parsers/` subpackage; OpenDataLoaderParser bridges abstraction → real library; Modernization (Docling/Marker/OCR) + Scaling pending |
| 1C Centralized Normalization | ✅ MVP | No | 8 rules, `.refined.json` manifest |
| 2 Canonicalizer Restoration | ✅ | No | Structured sections + diff-before-write |
| 3C Concept Enrichment | ✅ 16/20 | **No** | Deterministic anchors + section titles + alias miner |
| 4 Identity Cleanup | ✅ | No | — |
| 5 Extraction + dedup | ✅ | No | Registry-aware dedup |
| 6A Review + gap closure | ✅ | Reduced | Retry, resume, parallel, pre-review filter |
| 6B Second-Pass Review | ✅ | Tiny subset | Only uncertain Tier-1 output |
| 7 Promotion Governance | ✅ | No | 17-rule validator, audit log, rollback |

## Pipeline AI Budget on PD 1096

| Stage | Calls | Source |
|---|---|---|
| Pre-review filter (deterministic) | 0 | Auto-accept/reject by 7 rules (A1, A2, A3, A4, R1, R2, R5, R7) |
| Tier-1 review | **2 (was 9)** | Pre-filter now saves 7/9 (78%) via R7 |
| Tier-2 review | 1-2 | Only uncertain Tier-1 output |
| Concept enrichment | 0 | Regex anchors + section titles |
| Promotion | 0 | Schema validation |
| **Total** | **~4** | vs ~25 pre-session |

**R7 (endpoint_not_in_evidence)** is the biggest single LLM-savings lever: it rejects candidates where neither endpoint's phrase appears in the evidence text. 5/9 PD 1096 candidates were regex-extracted via section-window coincidence and discuss unrelated topics (wood construction, glazing, property lines). R7 catches them deterministically.

## Phase 3C Enrichment Results

**16/20 concepts enriched**, all via section-title matching (zero LLM calls):

| Slug | Confidence | Section |
|---|---|---|
| `certificate-of-occupancy` | 0.85 | sec-309 |
| `mixed-occupancy` | 0.85 | sec-703 |
| `building-height` | 0.75 | sec-707 |
| `building-permit` | 0.75 | sec-301 |
| `doors-and-exits` | 0.75 | sec-1007 |
| `fire-resistive-construction` | 0.75 | sec-1215 |
| `floor-area` | 0.75 | sec-705 |
| `light-and-ventilation` | 0.75 | sec-801 |
| `lot-occupancy` | 0.75 | sec-708 |
| `occupancy-classification` | 0.75 | sec-701 |
| `open-courts` | 0.75 | sec-804 |
| `projections-over-public-ways` | 0.75 | sec-1003 |
| `stairs` | 0.75 | sec-1207 |
| `occupancy-load` | 0.75 | sec-1207 (compound title) |
| `means-of-egress` | 0.75 | sec-1207 (compound title) |
| `occupancy-separation` | 0.75 | sec-703 (via mixed-occupancy alias) |

**Still missing (4):** `exit-width`, `parking-and-loading-spaces`, `setbacks`, `yards`. These don't appear as explicit section titles anywhere in PD 1096 or its IRR. They require either an inline-phrase-density fallback or a second source corpus.

## Code Modules (Phase 3C)

- `scripts/vitruvius/concept_definitions.py` — two extractors (anchor-based + section-title-based) with confidence ladder and alias dictionary
- `scripts/vitruvius/concept_aliases.py` — parenthetical abbreviation miner + "also known as" miner
- `scripts/vitruvius/concept_enrichment.py` — orchestrator + batch mode + diff-guard integration
- `scripts/pipeline_cli.py` — new `enrich-concept-one <slug>` and `enrich-concepts` commands

## Code Modules (Phase 1B Foundation — shipped 2026-04-14)

- `scripts/vitruvius/parsers/__init__.py` — public re-exports for the subpackage
- `scripts/vitruvius/parsers/base_parser.py` — `BaseParser` ABC, `ParserTelemetry` (17 fields, kw_only), `ParseResult` (kw_only)
- `scripts/vitruvius/parsers/document_taxonomy.py` — `DocumentClass` enum (9 members), `DocumentFeatures` (frozen, kw_only), `classify_document()` implementing CL-001–CL-008
- `scripts/vitruvius/parsers/quality_gates.py` — `GateStatus`, `GateResult`, `GateReport` (frozen, kw_only), `check_gate_*` functions, `run_quality_gates()` orchestrator (GATE-001–004)
- `scripts/vitruvius/parsers/orchestrator.py` — `TerminalStatus` enum, `AttemptRecord`, `OrchestratorResult` (frozen, kw_only), `ParserOrchestrator` synchronous fallback chain walker
- `scripts/vitruvius/models.py` — `FileEntry.sha256` field (RI-009)
- `scripts/vitruvius/scanner.py` — `_sha256_of_file()` helper + wire-up in `build_file_entries()`
- `scripts/vitruvius/reports.py` — `sha256` added to CSV fieldnames

## Awaiting

User review of the 13 enriched concept files under `003_Canonical-Knowledge-Layer/shared/concepts/`. Branch `feat/phase-7-promotion-governance` is now carrying Sprints A + B + polish + Phase 6B + Phase 3C + Phase 1B Foundation. Nothing has been pushed.

**Phase 1B next steps:** Phase 2 (Modernization — wrap existing parsers, implement Docling/Marker/Surya) and Phase 3 (Scaling & Governance — ProcessPoolExecutor, timeout enforcement, Golden Corpus) are the next natural Sprint C continuations.

## Next Phase Candidates

Ordered by estimated value per hour of work:

1. **Phase 1B Modernization (§11 Phase 2)** — wrap existing parsers behind `BaseParser`, implement `DoclingParser`, `MarkerParser`. Natural Sprint C continuation.
2. **Phase 3C second pass** — fill the 4 missing concepts by extending the alias dictionary and scanning PD 1096 IRR. Pure config, zero code changes.
3. **Extraction on PD 1096 IRR** — the IRR has richer section structure; extraction + review + promote on it would produce more relationship candidates for Phase 7.
4. **Pre-review filter A4/R4 rules** — expand the deterministic filter to push LLM savings further.
5. **Phase 8 Graph Contract & Indexing** — gated on ≥50 verified relationships; currently at 6.

## Reference Map
- Master roadmap → `/.ai/01_roadmap/master-roadmap.md`
- Milestone tracker → `/.ai/01_roadmap/milestone-tracker.md`
- Audits → `/.ai/02_audits/`
- Phase plans (active) → `/.ai/03_plans/` + `INDEX.md`
- Archived plans → `/.ai/09_archive/plans/`
- Known issues → `/.ai/10_state/known_issues.md`
- Decisions → `/.ai/10_state/decisions.md` (AD-009 through AD-022)
- Experiments → `/.ai/07_experiments/`
