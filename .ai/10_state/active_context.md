# Active Context — Vitruvius

> **Updated:** 2026-04-14 (Sprint A closed)
> **Active sprint:** Awaiting user confirmation to start Sprint B
> **Prior sprint window:** Sprint A · 2026-04-14 → 2026-04-14 (completed same-day)

## Where We Are
Sprint A — Phase 7 Promotion Governance — is **COMPLETE**. The full TDD plan at `/.ai/03_plans/phase-7-promotion-governance-plan.md` was executed end-to-end with 43/43 tests passing and three real PD 1096 relationships promoted from the existing Gemma review output into `003_Canonical-Knowledge-Layer/shared/relationships/`.

The project now has a working end-to-end pipeline: raw source → canonical source → regex extraction → Ollama review → promotion → canonical relationship file with full audit trail.

**Honest position:** *late ingestion / early extraction with working promotion*. Ingestion works; canonicalization and concepts are skeletons; extraction is regex-grade (82% rejection); review works and emits high-confidence artifact; **promotion works end-to-end with idempotency and rollback**.

## Sprint A Outcomes
- ✅ All 14 Phase 7 plan tasks executed.
- ✅ 43/43 tests passing (`scripts/tests/`).
- ✅ 3 new canonical relationship records:
  - `rel-law-national-building-code-of-the-philippines-governs-concept-building-permit` (conf 1.0)
  - `rel-concept-occupancy-classification-depends-on-concept-mixed-occupancy` (conf 0.9)
  - `rel-concept-occupancy-classification-affects-concept-mixed-occupancy` (conf 0.9)
- ✅ Promotion audit log at `006_System-Manifests/runs/latest_promotion_audit.log`.
- ✅ Idempotency: re-run produces `skipped=3`, byte-identical files.
- ✅ Rollback tested successfully (then re-promoted for the final state).
- ✅ Phase 6A partial gap closure: Ollama URL moved to config, high-confidence writer shipping.
- ✅ RI-003 (hardcoded Ollama URL) closed.
- ✅ RI-006 (manual promotion gap) closed.

## Code Delivered (feat/phase-7-promotion-governance branch)
| File | Purpose | Lines |
|---|---|---|
| `scripts/vitruvius/config.py` | Central config loader | ~40 |
| `scripts/vitruvius/rules/relationship_registry.yaml` | Closed predicate vocabulary | ~45 |
| `scripts/vitruvius/promotion_validator.py` | 17-rule validator + canonical index | ~200 |
| `scripts/vitruvius/promotion.py` | `run_promote` orchestrator, merge, audit, rollback | ~320 |
| `scripts/pipeline_cli.py` | New `promote` subcommand (+`--execute`, `--rollback`) | +14 |
| `scripts/vitruvius/ollama_review.py` | Config-driven URL, `write_high_confidence_review` | +50 |
| `config/vitruvius.yaml` | `review.ollama.*`, `promotion.*` keys | +10 |
| `scripts/tests/test_*.py` (9 files) | 43 unit tests including the 17 validator rules | ~700 |

## Awaiting
User review and confirmation to proceed to Sprint B. Per the user's instruction, execution pauses at the end of each phase for code review before the next phase begins.

## Next Sprint Candidates
- **Sprint B — Shrink the 82% rejection rate.** Phase 1C Centralized Normalization + full Phase 6A gap closure (retry, resume, wall-clock cap, parallelization).
- Alternative: Phase 2 Canonicalizer Restoration (smaller, Sprint C task pulled forward).

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
