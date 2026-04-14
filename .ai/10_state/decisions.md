# Architectural Decisions — Vitruvius

> **Updated:** 2026-04-14
> **Format:** ADR-lite. Each entry: date, status, context, decision, consequence.

## AD-001: Filesystem-as-Database
- **Date:** 2026-04-13
- **Status:** Implemented
- **Context:** The system needs high traceability, human-readability, and reproducibility.
- **Decision:** Use structured directories (`001_…` through `006_…`) and CSV/JSON registries instead of a relational database for the primary knowledge lifecycle.
- **Consequence:** Easy debugging, version control, and offline inspection. Tradeoff: performance risk for extremely large file counts (carried as RI-008).

## AD-002: Core Logic in `scripts/vitruvius` Package
- **Date:** 2026-04-13
- **Status:** Implemented
- **Context:** Development is CLI-centric; full `src/` packaging would add friction.
- **Decision:** Maintain the `vitruvius` functional package inside `scripts/`.
- **Consequence:** Simplifies CLI execution; deviates from standard Python packaging (`src/` layout). Contributors must run from repo root (carried as RI-004).

## AD-003: Rules-Based Canonicalization
- **Date:** 2026-04-13
- **Status:** Implemented
- **Context:** Entity classification must be deterministic.
- **Decision:** Use a YAML rules engine (`scripts/vitruvius/rules/canonical_rules.yaml`) for mapping raw files to canonical IDs.
- **Consequence:** Predictable and auditable. Rules must be maintained by hand.

## AD-004: Strict ID and Naming System
- **Date:** 2026-04-13
- **Status:** Implemented
- **Context:** Traceability across layers is critical for graph integrity.
- **Decision:** Enforce the `<prefix>-<slug>` pattern for all canonical IDs, and strict timestamped naming for all pipeline artifacts. See `/.ai/00_system/naming-conventions.md`.
- **Consequence:** Eliminates ambiguity in lineage. Requires robust slugification utilities. ID changes require migration (AD-004 + Phase 4 tooling).

## AD-005: Linear Pipeline Orchestration
- **Date:** 2026-04-13
- **Status:** Implemented
- **Context:** Complexity must be managed in a filesystem-driven extraction engine.
- **Decision:** Use a flat CLI orchestrator (`pipeline_cli.py`) with modular `run_` functions per stage. Idempotency is enforced through registry checks.
- **Consequence:** Easy to run individual stages. Branched flows require manual coordination until Phase 7 automates Review→Promote.

## AD-006: Local-First AI Strategy
- **Date:** 2026-04-13
- **Status:** Implemented
- **Context:** Review capability must not depend on cloud API keys or compromise document privacy.
- **Decision:** Integrate Ollama natively for the relationship review stage. Cloud providers are opt-in only.
- **Consequence:** Higher hardware requirements; guaranteed offline capability; compatible with air-gapped operation.

## AD-007: Ingestion Layer — Documented Gaps
- **Date:** 2026-04-13
- **Status:** Documented
- **Context:** Code-level forensic audit of the ingestion pipeline completed (`/.ai/02_audits/ingestion-audit.md`).
- **Finding:** Scanner captures 7 metadata fields, no hashes. Detection uses heuristic thresholds. Registry tracks per-file status. No automatic retry (manual re-run required). Sequential OCR.
- **Decision:** Accept current gaps as technical debt rather than blocking Phase 1A completion.
- **Consequence:** Gaps tracked as RI-008 (registry rotation), RI-009 (hashing), and Phase 1B (parallelization, multi-parser).

## AD-008: Review Layer Implementation — Documented Gaps
- **Date:** 2026-04-13
- **Status:** Documented
- **Context:** Code-level forensic audit of the review and validation layer completed (`/.ai/02_audits/review-layer-audit.md`).
- **Finding:** `ollama_review.py` (345 lines) implements Gemma4:31b-based review. Three decisions, confidence scoring, interruption-safe. **Not in the default pipeline** (manual trigger only). No second-pass, no confidence-threshold auto-filter, hardcoded Ollama URL, sequential processing only.
- **Decision:** Accept manual-trigger review as sufficient for Sprint A (which only consumes existing review output). Gap closure queued for Sprints A, B, and C.
- **Consequence:** Phase 7 can proceed without further review-layer blockers. Full closure tracked in the milestone tracker.

## AD-009: Master Roadmap v2.0.0 Published
- **Date:** 2026-04-14
- **Status:** Implemented
- **Context:** The previous roadmap (v1.x) claimed Phases 2, 3, and 5 were "complete" in ways that the 2026-04-13 audit pack disproved. Phases are too thin for Phase 7 to consume cleanly without also driving Phase 1C in parallel.
- **Decision:** Rewrite `/.ai/01_roadmap/master-roadmap.md` as v2.0.0. Reconcile status against the audits (§4), formalize the governance contracts (§3 — Relationship Registry, Ingestion-Refinement Contract, Document Taxonomy, Rule Tiers, Promotion Contract, Graph Contract), add per-phase contracts with Definition of Done and gating metrics (§6), a dependency graph (§7), a 90-day sprint sequence (§8), a KPI table (§9), a technical debt register (§10), and cadence protocol (§11).
- **Consequence:** Single source of truth for phase status and sequencing. Any conflict between v2.0.0 and other repo documents is resolved in favor of v2.0.0. `milestone-tracker.md`, `current-phase.md`, and `active_context.md` revised to match on 2026-04-14.

## AD-010: Three-Sprint Execution Sequence
- **Date:** 2026-04-14
- **Status:** Implemented
- **Context:** Several high-value phases (Promotion, Normalization, Multi-Parser, Second-Pass Review, Canonicalizer Restoration) have overlapping dependencies. Sequencing them naively would either block Promotion on upstream cleanup (slow) or build Promotion on garbage inputs (fragile).
- **Decision:** Adopt a three-sprint sequence:
  1. **Sprint A (weeks 1–2) — Unblock Promotion.** Land Phase 7 on top of the existing Ollama review output. Independent of upstream cleanup. Uses the 0.90 confidence gate to avoid promoting noise.
  2. **Sprint B (weeks 3–6) — Shrink the 82% Rejection Rate.** Build Phase 1C (normalization) + full Phase 6A gap closure. Re-run PD 1096 to measure.
  3. **Sprint C (weeks 7–12) — Harden the Front End.** Phase 1B (multi-parser) + Phase 6B (second-pass) + Phase 2 (canonicalizer restoration) in parallel.
- **Consequence:** Phase 7 exists and exercises the governance contract before upstream is perfect. The 0.90 gate ensures only high-signal edges enter canonical storage regardless of input noise. Downstream phases (8, 9, 11, 12) remain gated until after Sprint C.

## AD-011: First Promoted Relationship Record Shape *(pending)*
- **Date:** TBD (Sprint A exit)
- **Status:** Planned
- **Context:** Sprint A writes the first canonical relationship files. Their final shape must be recorded here before Sprint B begins, so downstream phases have a stable contract.
- **Decision:** *(To be filled in after A-5 runs.)*
- **Consequence:** Any deviation from master-roadmap §3.5 is documented here and back-propagated into the roadmap.

---

## Decision Process
- New decisions land here as `AD-NNN` in numerical order.
- Each decision references the context (audit, plan, sprint) that prompted it.
- Superseded decisions are marked `Superseded by AD-NNN` rather than deleted.
- This file is authoritative for *why* the system is the way it is. Code shows *what*; this file shows *why*.
