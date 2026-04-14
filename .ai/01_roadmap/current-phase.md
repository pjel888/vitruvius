# Current Phase — (between sprints)

> **Authoritative roadmap:** `/.ai/01_roadmap/master-roadmap.md` (v2.0.0)
> **This document:** snapshot of where work is currently paused.
> **Updated:** 2026-04-14 — all active implementation sprints closed.

---

## State

**No active sprint.** The project is currently between user-driven execution
passes. Sprints A and B are both closed, plus a post-Sprint-B quality pass
that delivered the pre-review filter, concept enrichment, integration tests,
and README refresh.

## Phases completed in the most recent work window (2026-04-14)

| Phase | Outcome |
|---|---|
| **Phase 7 — Promotion Governance** | ✅ Complete — 6 PD 1096 relationships promoted, idempotency + rollback verified, 17-rule validator enforced |
| **Phase 1C — Centralized Normalization (MVP)** | ✅ MVP — `NormalizationEngine` + 5 Tier A + 3 Tier B rules + `refine` CLI + `.refined.json` manifests. Tier C deferred. |
| **Phase 2 — Canonicalizer Restoration** | ✅ Complete — structured section generator restored, diff-before-write protection |
| **Phase 6A — Review Gap Closure** | ✅ Complete — retry, resume, parallel, warmup, config-driven URL, `run-with-review` composite |
| **Phase 6B — Second-Pass Review** | ✅ Complete — routing + Tier-2 orchestrator + agreement matrix + human escalation worklist |
| **Phase 3C — Concept Enrichment** | ✅ 16/20 (80%) — deterministic regex anchor + section-title + alias miner, **zero LLM calls** |
| **Pre-review filter** | ✅ Shipped — 22% → 78% LLM savings on PD 1096 (AD-018, AD-021) |
| **Integration tests** | ✅ 4 tests covering full pipeline wire-to-wire (AD-021) |

## Snapshot numbers

- **Test suite:** 177 passing (under strict `-W error::DeprecationWarning`)
- **Canonical relationship files:** 7 (6 promoted + 1 hand-curated)
- **Enriched concept files:** 16 out of 20 PD 1096 concepts
- **AI budget on PD 1096 full pipeline run:** ~4 Ollama calls (was ~25)
- **Commits on `feat/phase-7-promotion-governance`:** ~65+ ahead of main
- **Decision log:** AD-001 through AD-021 (chronological)

## Still unfinished in the active roadmap (`.ai/03_plans/`)

- **Phase 1B — Multi-Parser Integration** — design spec, ready to expand into TDD
- **Phase 8 — Graph Contract & Indexing** — gated on ≥50 verified relationships (currently 7)
- **Phase 9 — Query & AI Layer** — gated on Phase 8
- **ingestion-refinement-contract** — frozen contract, no action needed

## Open backlog (not blocking)

- **4 concepts remain as placeholders:** `exit-width`, `parking-and-loading-spaces`, `setbacks`, `yards`. They don't match any PD 1096 section title. Recoverable via inline phrase-density extraction or a second source corpus — no LLM required.
- **Phase 3C follow-ups:** alias miner for concept files, related-concepts detection, full schema compliance including typed `regulatory_basis`. All optional.
- **`ollama_review.py` splitting** — the module has grown to ~500 lines. Could be split into `ollama_client.py` (HTTP), `ollama_review.py` (orchestrator), `review_artifacts.py` (writers). Not urgent — integration tests would protect the refactor.
- **Branch rename** — `feat/phase-7-promotion-governance` now contains ~65 commits spanning 6+ phases. A conceptual rename (e.g., `feat/sprint-a-b-bundle`) would improve merge-commit messaging.

## Awaiting

User direction on which phase to tackle next. Recommendations, ranked:

1. **Phase 1B Multi-Parser Integration** — biggest ingestion quality lever, but multi-session work.
2. **Run the full pipeline on PD 1096 IRR** — second corpus, should yield more relationships and fill some of the 4 missing concepts.
3. **Split `ollama_review.py`** — quality refactor with forcing function from the integration tests.
4. **Pull `qwen3:30b`** to run a true architectural-diversity Tier-2 pass (deferred because of 8 GB hardware constraint).

## Reference

- `/.ai/01_roadmap/master-roadmap.md` — authoritative roadmap, §4 status matrix
- `/.ai/01_roadmap/milestone-tracker.md` — per-phase checkbox tracker
- `/.ai/10_state/active_context.md` — pipeline architecture + AI budget
- `/.ai/10_state/decisions.md` — AD-001 through AD-021
- `/.ai/09_archive/plans/` — 6 archived plans (phase 7, 1C, 2, 6A, 6B, 3C, polish)
