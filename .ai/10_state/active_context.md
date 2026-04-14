# Active Context — Vitruvius

> **Updated:** 2026-04-14
> **Active sprint:** Sprint A — Unblock Promotion (Phase 7)
> **Sprint window:** 2026-04-14 → 2026-04-28 (2 weeks)

## Where We Are
The 2026-04-13 audit pack is complete. Four forensic audits (ingestion, extraction, normalization, review layer) + one codebase/roadmap audit reconciled the documented roadmap against actual code. The master roadmap has been rewritten as v2.0.0 to reflect ground truth.

**Honest position:** *late ingestion / early extraction*. Ingestion works; canonicalization and concepts are skeletons; extraction is regex-grade; review works but is manual; promotion does not exist.

## Current Goal
Land **Phase 7 — Promotion Governance** on top of the existing Ollama review output. See `/.ai/01_roadmap/current-phase.md` for the task list.

This is the highest-leverage move available: it exercises the governance contract end-to-end and unblocks every downstream phase, without depending on upstream cleanup work.

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
