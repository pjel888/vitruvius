# Active Context — Vitruvius

> **Updated:** 2026-04-14 · Phase 3C enrichment complete (13/20 concepts)
> **Branch:** `feat/phase-7-promotion-governance` (many commits ahead of `main`)
> **Test suite:** 167/167 passing

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
| 1A Baseline Ingestion | ✅ | No | Known gaps carried as RI-008, RI-009 |
| 1C Centralized Normalization | ✅ MVP | No | 8 rules, `.refined.json` manifest |
| 2 Canonicalizer Restoration | ✅ | No | Structured sections + diff-before-write |
| 3C Concept Enrichment | ✅ 13/20 | **No** | Deterministic anchors + section titles + alias miner |
| 4 Identity Cleanup | ✅ | No | — |
| 5 Extraction + dedup | ✅ | No | Registry-aware dedup |
| 6A Review + gap closure | ✅ | Reduced | Retry, resume, parallel, pre-review filter |
| 6B Second-Pass Review | ✅ | Tiny subset | Only uncertain Tier-1 output |
| 7 Promotion Governance | ✅ | No | 17-rule validator, audit log, rollback |

## Pipeline AI Budget on PD 1096

| Stage | Calls | Source |
|---|---|---|
| Pre-review filter (deterministic) | 0 | Auto-accept/reject by rules |
| Tier-1 review | 7 (was 9) | Pre-filter saved 2 |
| Tier-2 review | 2 | Only `review_further` candidates |
| Concept enrichment | 0 | Regex anchors + section titles |
| Promotion | 0 | Schema validation |
| **Total** | **9** | vs ~25 pre-session |

## Phase 3C Enrichment Results

**13/20 concepts enriched**, all via section-title matching:

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

**Still missing (7):** `exit-width`, `means-of-egress`, `occupancy-load`, `occupancy-separation`, `parking-and-loading-spaces`, `setbacks`, `yards`. These don't appear as explicit section titles in the main PD 1096 file. Likely recoverable via (a) extending the alias dictionary, (b) scanning the PD 1096 IRR which has more granular sections, or (c) adding a co-occurrence fallback.

## Code Modules (Phase 3C)

- `scripts/vitruvius/concept_definitions.py` — two extractors (anchor-based + section-title-based) with confidence ladder and alias dictionary
- `scripts/vitruvius/concept_aliases.py` — parenthetical abbreviation miner + "also known as" miner
- `scripts/vitruvius/concept_enrichment.py` — orchestrator + batch mode + diff-guard integration
- `scripts/pipeline_cli.py` — new `enrich-concept-one <slug>` and `enrich-concepts` commands

## Awaiting

User review of the 13 enriched concept files under `003_Canonical-Knowledge-Layer/shared/concepts/`. Branch `feat/phase-7-promotion-governance` is now carrying Sprints A + B + polish + Phase 6B + Phase 3C. Nothing has been pushed.

## Next Phase Candidates

Ordered by estimated value per hour of work:

1. **Phase 3C second pass** — fill the 7 missing concepts by extending the alias dictionary and scanning PD 1096 IRR. Pure config, zero code changes.
2. **Extraction on PD 1096 IRR** — the IRR has richer section structure; extraction + review + promote on it would produce more relationship candidates for Phase 7.
3. **Pre-review filter A4/R4 rules** — expand the deterministic filter to push LLM savings from 22% → 40%+.
4. **Phase 1B Multi-Parser Integration** — the biggest ingestion upgrade. Multi-session work.
5. **Phase 8 Graph Contract & Indexing** — gated on ≥50 verified relationships; currently at 6.

## Reference Map
- Master roadmap → `/.ai/01_roadmap/master-roadmap.md`
- Milestone tracker → `/.ai/01_roadmap/milestone-tracker.md`
- Audits → `/.ai/02_audits/`
- Phase plans (active) → `/.ai/03_plans/` + `INDEX.md`
- Archived plans → `/.ai/09_archive/plans/`
- Known issues → `/.ai/10_state/known_issues.md`
- Decisions → `/.ai/10_state/decisions.md` (AD-009 through AD-019)
- Experiments → `/.ai/07_experiments/`
