# Current Phase — Between Sprints (2026-04-15 late pass) — 6 sprints closed this session

> **Authoritative roadmap:** `/.ai/01_roadmap/master-roadmap.md` (v2.0.0)
> **Authoritative execution order:** `/.ai/03_plans/00-governing-implementation-plan.md` (v1.0.0)
> **This document:** snapshot of which sprint is currently active and the next gate.
> **Updated:** 2026-04-15

---

## State

**Active sprint:** **Sprint Q — Live Wiring & 8GB Hardening** — Streams W1–W5 all shipped on 2026-04-15 under TDD. See AD-024 in `/.ai/10_state/decisions.md` for the full stream-by-stream ledger. The sprint is **code-complete**; the only remaining exit gate is a live PD 1096 run to measure peak RSS + end-to-end latency before flipping the tag to `sprint-q-closed`.
**Sub-plan:** `.ai/03_plans/live-wiring-and-8gb-hardening-plan.md`
**Streams in order:** W1 (LLM survival mode) → W2 (review pipeline wiring) → W3 (stringency matrix live gate) → W4 (quality harness) → W5 (docs sync).

**Why Sprint Q first:** Streams F (review) and G (promotion) of the statistical upgrade shipped Python modules that are currently imported by nothing — see `pre_review/nb_filter.py`, `review/ontology_prompt.py`, `review/slm_router.py`, `review/conformal.py`, `review/tension_analyzer.py`, `review/reflection_parser.py`, `review/choquet.py`, `promotion/bayesian_fusion.py`, `promotion/stringency_matrix.py`, `promotion/temporal_edges.py`. Every downstream sprint depends on those scaffolds being wired into live paths first.

## Sprint Q delivery (2026-04-15)

| Stream | Scope | Commits | Tests |
|---|---|---|---|
| W1 — 8GB LLM Survival Mode | model pool + num_ctx cap + budget guard + binary mode | 024edaf, be87273, 23234a2, 47d1b9d | +17 |
| W2 — Review Pipeline Wiring | NB prefilter + ontology prompt + SLM router + conformal + tension/reflection + Choquet | 91178a9, de6ef59, ecc2926, a4bce5a, f37b8a2, a1ee672 | +15 |
| W3 — Stringency Matrix Live Gate | 20-concept migration + lint rule + promotion hook + graph edge governing-standard field | 092f402, 2b5d101, be81e64, 09ee5d3 | +13 |
| W4 — Quality Harness | e2e chain test + flag-OFF backcompat regression + bench harness + decision-log automation | 21a7d7a, 25b59db, 261529c | +7 |
| W5 — Docs Sync | this update + AD-024 + README/AGENTS | (bundled in docs commit) | — |

Total Sprint Q additions: +48 tests, 15 commits (plus 1 reconciliation commit `fd57d25` and 1 docs commit for W5).
Full suite: 297 → **1051 passing** (much of the +754 is the inherited Sprint D Streams A–I expansion already in-branch; Sprint Q's direct delta is +48).

## Most recently closed sprints

| Sprint | Scope | Notes |
|---|---|---|
| A (Sprint A) | Phase 7 Promotion Governance | Closed 2026-04-14. 6 PD 1096 relationships promoted; 17-rule validator enforced. |
| B (Sprint B) | Phase 1C MVP + Phase 2 + Phase 6A gap closure + Phase 6B | Closed 2026-04-14. Review layer end-to-end. |
| C (Sprint C) | Phase 1B Foundation + polish | Closed 2026-04-14. 9 commits, 80 new tests. Parsers subpackage + `FileEntry.sha256` + rotate-registries CLI. |
| D (Sprint D — Statistical & Architectural Upgrade, Streams A–I) | Stream A bootstrap, B ingestion, C OCR/chunking, D concepts, E extraction, F review scaffolds, G promotion scaffolds, H graph intelligence (Phase 8 base), I query (Phase 9 base) | Closed 2026-04-14. F and G scaffolds were dead code until Sprint Q W2 + W3 wired them. |

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

1. **Run the live PD 1096 bench** to measure peak RSS + end-to-end latency with every `w_*` flag turned on in sequence; record the numbers into AD-024; tag `sprint-q-closed`; then enter Sprint R or Sprint H.
2. **Dispatch Sprint R — Per-Layer Embeddings & Agentic Reasoning** in parallel with Sprint H (3D Spatial) once Sprint Q is tagged closed.
3. **Expand a later design-spec plan to TDD form** ahead of time (phase-13 / phase-14 / phase-15 / phase-16 / phase-8B / phase-12).
4. **Run Phase 1B Modernization in a side worktree** while Sprint R/H execute.

## Reference

- Governing plan → `/.ai/03_plans/00-governing-implementation-plan.md` — read this first
- Master roadmap → `/.ai/01_roadmap/master-roadmap.md`
- Plan index → `/.ai/03_plans/INDEX.md`
- Milestone tracker → `/.ai/01_roadmap/milestone-tracker.md`
- Active context → `/.ai/10_state/active_context.md`
- Decisions → `/.ai/10_state/decisions.md` (AD-001 through AD-023)
- Known issues → `/.ai/10_state/known_issues.md`
- Archived plans → `/.ai/09_archive/plans/`
