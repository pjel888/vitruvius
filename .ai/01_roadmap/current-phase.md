# Current Phase — Sprint Q · Live Wiring & 8GB Hardening (pending dispatch)

> **Authoritative roadmap:** `/.ai/01_roadmap/master-roadmap.md` (v2.0.0)
> **Authoritative execution order:** `/.ai/03_plans/00-governing-implementation-plan.md` (v1.0.0)
> **This document:** snapshot of which sprint is currently active and the next gate.
> **Updated:** 2026-04-15

---

## State

**Active sprint:** **Sprint Q — Live Wiring & 8GB Hardening** (pending user "go" — plan ready).
**Sub-plan:** `.ai/03_plans/live-wiring-and-8gb-hardening-plan.md`
**Streams in order:** W1 (LLM survival mode) → W2 (review pipeline wiring) → W3 (stringency matrix live gate) → W4 (quality harness) → W5 (docs sync).

**Why Sprint Q first:** Streams F (review) and G (promotion) of the statistical upgrade shipped Python modules that are currently imported by nothing — see `pre_review/nb_filter.py`, `review/ontology_prompt.py`, `review/slm_router.py`, `review/conformal.py`, `review/tension_analyzer.py`, `review/reflection_parser.py`, `review/choquet.py`, `promotion/bayesian_fusion.py`, `promotion/stringency_matrix.py`, `promotion/temporal_edges.py`. Every downstream sprint depends on those scaffolds being wired into live paths first.

## Most recently closed sprints

| Sprint | Scope | Notes |
|---|---|---|
| A (Sprint A) | Phase 7 Promotion Governance | Closed 2026-04-14. 6 PD 1096 relationships promoted; 17-rule validator enforced. |
| B (Sprint B) | Phase 1C MVP + Phase 2 + Phase 6A gap closure + Phase 6B | Closed 2026-04-14. Review layer end-to-end. |
| C (Sprint C) | Phase 1B Foundation + polish | Closed 2026-04-14. 9 commits, 80 new tests. Parsers subpackage + `FileEntry.sha256` + rotate-registries CLI. |
| D (Sprint D — Statistical & Architectural Upgrade, Streams A–I) | Stream A bootstrap, B ingestion, C OCR/chunking, D concepts, E extraction, F review scaffolds, G promotion scaffolds, H graph intelligence (Phase 8 base), I query (Phase 9 base) | Closed 2026-04-14. **F and G scaffolds are dead code until Sprint Q wires them.** |

## Snapshot numbers

- **Test suite:** 297/297 passing
- **Canonical relationship files:** 6 PD 1096 promoted + 1 hand-curated (Sprint H entry gate needs ≥25)
- **Enriched concept files:** 16/20 PD 1096 concepts
- **Active branch:** `feat/sprint-d-intelligence-upgrade`
- **Decision log:** AD-001 through AD-023

## Next gates

### Sprint Q entry gate
**None.** Sprint Q can start immediately. The `live-wiring-and-8gb-hardening-plan.md` is already in `implementation_tdd` form.

### Sprint Q exit gate (must all be true to close Q)
- All 8 Stream F review modules imported by `ollama_review.py`.
- All 3 Stream G promotion modules imported by `promotion.py`.
- All 20 canonical concept files have `stringency_vector` frontmatter.
- `pytest tests/test_livewiring_e2e.py -v` green.
- Peak RSS ≤ 5 GB on PD 1096 run under `gemma4:e4b`.
- `features.livewiring_*=false` produces byte-identical output vs pre-Sprint-Q baseline.
- `AD-024` recorded in `.ai/10_state/decisions.md`.

### Immediately after Sprint Q
- **Sprint R** (Per-Layer Embeddings & Agentic) — entry gate is `sprint-q-closed` tag.
- **Sprint H** (3D Spatial Intelligence) — entry gate is `sprint-q-closed` AND ≥25 verified relationships.
- R and H are parallelizable if agent capacity allows.

## Parallel side-track (any time)

**Phase 1B Modernization (§11 Phase 2 + Phase 3)** — parser wrapping + ProcessPoolExecutor + Golden Corpus. Independent of Sprint Q and can run in a side worktree without blocking anything. Plan is `phase-1b-multi-parser-integration-plan.md` but needs a TDD expansion pass before dispatch (see governing plan §5 Task 6).

## Awaiting

User direction on one of:

1. **Dispatch Sprint Q Task 1 (reconcile plans)** followed by Task 2 (Sprint Q dispatch) — the default path per the governing plan.
2. **Expand a later design-spec plan to TDD form** ahead of time (phase-13 / phase-14 / phase-15 / phase-16 / phase-8B / phase-12).
3. **Run Phase 1B Modernization in parallel** while Sprint Q executes.

## Reference

- Governing plan → `/.ai/03_plans/00-governing-implementation-plan.md` — read this first
- Master roadmap → `/.ai/01_roadmap/master-roadmap.md`
- Plan index → `/.ai/03_plans/INDEX.md`
- Milestone tracker → `/.ai/01_roadmap/milestone-tracker.md`
- Active context → `/.ai/10_state/active_context.md`
- Decisions → `/.ai/10_state/decisions.md` (AD-001 through AD-023)
- Known issues → `/.ai/10_state/known_issues.md`
- Archived plans → `/.ai/09_archive/plans/`
