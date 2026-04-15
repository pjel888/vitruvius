# Active Context — Vitruvius

> **Updated:** 2026-04-15 (very late pass) · **ALL 9 governing-plan sprints closed this session.** Sprint Q ✅ + Sprint R ✅ + Sprint PHYS ✅ + Sprint H ✅ + Sprint GEOM ✅ + Sprint WIKI ✅ + Sprint GT ✅ + Sprint HP ✅ + Sprint Z ✅. See AD-024 through AD-028 for per-sprint ledgers.
> **Branch:** `feat/sprint-r-per-layer-embeddings` (misnomer at this point — branch carries 9 sprints, not just Sprint R; will be renamed when merged to main)
> **Python test suite:** **1364 / 1364 passing**, 1 skipped
> **TypeScript test suite:** 20 / 20 passing (spatial-daemon/)
> **Rust unit tests:** 10 passing (engine_rs core + datalog_rs)
> **Sprint tags (9):** `sprint-q-closed`, `sprint-r-closed`, `sprint-phys-closed`, `sprint-h-closed`, `sprint-geom-closed`, `sprint-wiki-closed`, `sprint-gt-closed`, `sprint-hp-closed`, `sprint-z-closed`
> **Canonical relationships:** **31 verified** (Sprint H entry gate cleared — grew from 7 via PD 1096 IRR ingest)
> **Governing plan status:** Task 7 sprint chain **fully executed**. Remaining work is optional polish (Sprint D residuals J/K, gated externally) or side-tracks (Phase 1B Modernization §11 Phase 2/3).

## Sprint R Progress (2026-04-15)

| Stream | Scope | Status | Commits |
|---|---|---|---|
| Y0 — Bootstrap & flags | priming/ shell, 5 y_* flags in YAML, backward-compat regression | ✅ 3/3 closed | 9d7fc42, 570f162, 1de5ad2 (static source check) |
| Y1 — Contextual priming (PLE) | Source identity vector, prompt prefix injector, drift detector, ontology prompt wiring, extraction wiring | ✅ 5/5 closed (sentence_transformers WAS available on the Homebrew Python 3.11 that pytest uses — initial blocker was a wrong-interpreter false alarm) | a8fa345, 6cbed34, 1de5ad2 |
| Y2 — Domain-routing MoE | Domain classifier, route_with_moe, policy file + loader, select_review_model hook | ✅ 4/4 closed | ec746c5, d1edcfe, a511de3, bea5a93 |
| Y3 — Thinking mode + CoT audit | parse_cot_strict, cot_audit writer, ollama_review CoT enforcement, ple-cotrace-dump CLI | ✅ 4/4 closed | ffe5e83, 4e5d3ae, 1e0b987, 02b068d |
| Y4 — Stateful agentic registry | SQLite registry core, wire into ollama_review, vacuum + purge CLI, Phase 6A Resume integration test | ✅ 4/4 closed (Phase 6A Resume gap closed at root) | 169145e, 8c38bbf |
| Y5 — Vision OCR | Vision wrapper (mocked tests), table_graph_extractor fallback, ple-vision-probe CLI, operator checklist in AGENTS.md | ✅ 4/4 closed. Live activation still requires operator work: install psutil + Pillow, `ollama pull moondream`, run `ple-vision-probe`, then flip `features.y_vision_ocr: true`. | 3a8d150 |

Sprint R is **CODE-COMPLETE** on `feat/sprint-r-per-layer-embeddings`:
**20 of 20 Sprint R tasks shipped; test suite at 1123 passing**.
Every Y flag defaults false, so the pipeline is still byte-identical
to the pre-Sprint-R baseline until an operator flips one on.

`per-layer-embeddings-agentic-upgrade-plan.md` is archived at
`.ai/09_archive/plans/`.

Stream Y5 still requires **operator** activation work (documented in
AGENTS.md): install psutil + Pillow, pull a ≤2B-param vision model
via Ollama, run `ple-vision-probe`, and only then flip
`features.y_vision_ocr: true`. No code work remains.

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

The governing-plan Task 7 sprint chain is **fully executed**. The branch `feat/sprint-r-per-layer-embeddings` (misnomer — carries 9 sprints) is ready for merge review. User direction is open.

## Next Phase Candidates

1. **Merge + rename branch** — `feat/sprint-r-per-layer-embeddings` → main. Rename on merge since it now carries Sprints Q, R, PHYS, H, GEOM, WIKI, GT, HP, Z.
2. **Phase 1B Modernization (§11 Phase 2 + Phase 3)** — parser wrapping, Docling/Marker, ProcessPoolExecutor, Golden Corpus. Plan needs a TDD expansion pass first (see governing plan §5 Task 6).
3. **Sprint D residuals J / K** — Stream J (query integration) and Stream K (docs+CI) are externally gated on Ranger dashboard + 2nd jurisdiction corpus.
4. **Retroactive ledger cleanup** — split commit `61be8a2` into Sprint Z S1 + HP.4 via `git rebase -i` for cleaner history (optional).
5. **Fresh roadmap brainstorm** — the project is materially ahead of the v2.0.0 roadmap envelope; next horizon is undefined.

## Reference Map
- Governing plan → `/.ai/03_plans/00-governing-implementation-plan.md`
- Master roadmap → `/.ai/01_roadmap/master-roadmap.md`
- Milestone tracker → `/.ai/01_roadmap/milestone-tracker.md`
- Audits → `/.ai/02_audits/`
- Phase plans (active) → `/.ai/03_plans/` + `INDEX.md`
- Archived plans → `/.ai/09_archive/plans/` (9 plans archived this session)
- Known issues → `/.ai/10_state/known_issues.md`
- Decisions → `/.ai/10_state/decisions.md` (AD-001 through AD-028)
- Experiments → `/.ai/07_experiments/`
