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

## AD-011: First Promoted Relationship Record Shape
- **Date:** 2026-04-14
- **Status:** Implemented
- **Context:** Sprint A · Task 13 produced the first promoted relationships from the existing Gemma review output.
- **Decision:** The record shape matches `/.ai/06_specs/relationship-schema.md` §4 with one minor deviation: `last_promoted_utc` and `extracted_at_utc` use the compact `%Y%m%dT%H%M%SZ` format (e.g. `20260414T035210Z`) rather than RFC-3339 (`2026-04-14T03:52:10Z`). Python 3.11's `datetime.fromisoformat` parses both, so Rule 16 of the validator accepts both forms. A future task may normalize to RFC-3339 for external consumers that don't share this leniency.
- **Observed counts on PD 1096:**
  - Total Gemma review candidates: 23
  - Cleared 0.90 confidence gate: 3
  - Created in Phase 7 batch: 3
  - Merged or skipped on re-run: 3 (idempotent)
- **First batch ID:** `20260414T035210Z_0959acf9`
- **Golden-path records:**
  - `rel-law-national-building-code-of-the-philippines-governs-concept-building-permit` (confidence 1.0)
  - `rel-concept-occupancy-classification-depends-on-concept-mixed-occupancy` (confidence 0.9)
  - `rel-concept-occupancy-classification-affects-concept-mixed-occupancy` (confidence 0.9)
- **Consequence:** Phase 8 (graph contract) is unblocked, gated on the ≥50-record threshold. Future Phase 7 behavior locked: YAML frontmatter via `yaml.safe_dump` (round-trip safe), strict byte-identical idempotency, rollback keyed on batch ID.

## AD-012: Strict Byte-Identical Idempotency
- **Date:** 2026-04-14
- **Status:** Implemented
- **Context:** During Sprint A golden-path verification, the first implementation had weak idempotency: re-running `promote --execute` rewrote files with fresh `promotion_batch_id` and `last_promoted_utc` even when no new evidence was present. This violated the plan's exit criterion "re-run produces no new writes."
- **Decision:** Add a `skipped` action to the orchestrator: when `merge_evidence` returns the same list as the existing evidence (no new fingerprints), classify the candidate as `skipped`, do not rewrite the file, do not update metadata, and do not add an audit log entry. Strict byte-identical determinism is now a test invariant (`test_idempotent_file_bytes_unchanged`).
- **Consequence:** Downstream consumers (Phase 8 graph builder) can rely on deterministic canonical output. Git-diff-based change detection works as expected.

## AD-014: Regex Extractor Dedup by (from, to)
- **Date:** 2026-04-14
- **Status:** Implemented
- **Context:** The 2026-04-14 end-to-end experiment exposed that the regex extractor in `relationships_sections.py` produces up to 5 candidates per endpoint pair (one per predicate pattern match). This inflated the review workload and was the dominant contributor to the 82% rejection rate. Running the deduper against the refined PD 1096 corpus cut the candidate count from 23 to 9 (−61%) without losing any information — dropped predicates are recorded in `alternate_predicates` for Phase 6B to revisit.
- **Decision:** Dedup candidates by `(from, to)` in `relationships_sections.dedupe_by_endpoints` after aggregation. The surviving candidate carries the highest-occurrence predicate (tie-broken by `PREDICATE_PRIORITY` order: `governs > defines > requires > depends_on > limits > affects > supersedes`). Sections and examples from all siblings are merged into the survivor.
- **Consequence:** Directly cuts candidate volume by up to 5×. Review layer no longer wastes cycles on predicate variants. The true Phase 1C rejection-rate impact becomes measurable because the extraction is no longer the dominant noise source.

## AD-016: Registry-Aware Extractor Dedup
- **Date:** 2026-04-14
- **Status:** Implemented
- **Context:** The first post-dedup experiment showed the priority-only picker could select a predicate whose `(subject_type, object_type)` was incompatible with the registry (e.g., `defines` for a concept→concept edge requires a source subject). That single bad pick lost 3 would-be valid concept→concept promotions. The dedup was correct in spirit (collapse 5 variants to 1) but wrong in implementation (priority ignored compatibility).
- **Decision:** Extend `dedupe_by_endpoints` to infer `(from_type, to_type)` from canonical ID prefixes and prefer predicates whose compatibility pair is in the registry. Fall back to priority-only when no predicate in the group is compatible (so Rule 7 can report the real problem downstream instead of silently discarding).
- **Consequence:** The dedup now picks `requires` for concept→concept edges (compatible) instead of `defines` (incompatible). Real-data rerun confirmed zero Rule 7 rejections from the dedup's choices. The helper `_infer_entity_type` is a prefix-based shortcut — a more robust version would load the canonical index, but prefix inference is sufficient for the current ID conventions.

## AD-017: Phase 6B Second-Pass Review
- **Date:** 2026-04-14
- **Status:** Implemented
- **Context:** The dedup exposed that Tier-1 review still leaves `review_further` candidates with insufficient signal. Phase 6B adds a Tier-2 adjudicator that runs only on the uncertain subset.
- **Decision:** Implement `select_for_second_pass` (entry-criteria filter) + `route_adjudication` (decision table) + `ollama_review_second_pass.run_second_pass_inner` (orchestrator with graceful Ollama fallback). The Tier-2 prompt matches `.ai/08_prompts/qwen-second-pass.txt` byte-for-byte. Outputs: `latest_relationship_review_merged.json` (with agreement matrix) and `latest_human_escalation_worklist.json`.
- **Consequence:** The full two-stage adjudication pipeline is shipping. Only uncertain Tier-1 decisions go to Tier-2, bounding compute cost. A small real-data smoke test on PD 1096 (9 Tier-1 candidates → 2 routed → 1 suppress, 1 human_review) validated the end-to-end flow. Full calibration awaits pulling `qwen3:30b` for architectural-diversity adjudication.

## AD-015: Lazy CLI Imports
- **Date:** 2026-04-14
- **Status:** Implemented
- **Context:** `scripts/pipeline_cli.py` eagerly imported every handler at module load, pulling in heavy PDF/OCR dependencies (`opendataloader_pdf`, `pypdf`, `ocrmypdf`) even for commands like `promote`, `refine`, and `canonicalize` that never touch conversion. This blocked the CLI from running in minimal environments and was hit firsthand during Phase 7 execution when `pip3 install -r requirements.txt` was required before `promote --help` would work.
- **Decision:** Move every handler import inside its `if args.command == "..."` branch. Top-level imports reduced to `argparse` only. Each command handler is imported lazily the first time it is dispatched.
- **Consequence:** `pipeline_cli.py promote --help` now works without any PDF libraries installed. Minimal-deployment environments (audit/CI containers, minimal operator workstations) can use promote/refine/canonicalize without the full conversion stack. Test `test_cli_lazy_imports.test_promote_help_does_not_import_conversion` asserts that `vitruvius.conversion`, `opendataloader_pdf`, `pypdf`, and `ocrmypdf` are NOT in `sys.modules` after importing `pipeline_cli`. The test runs in a subprocess so it cannot pollute the parent pytest process — an initial in-process approach broke `test_ollama_warmup` by leaving stale module references.

## AD-013: yaml.safe_dump for Frontmatter Emission
- **Date:** 2026-04-14
- **Status:** Implemented
- **Context:** The initial `_render_frontmatter` used a hand-rolled `_yaml_scalar` emitter to control key ordering. It was not perfectly round-trip-safe: loading the written file via `yaml.safe_load` returned slightly different strings, which caused `evidence_fingerprint` to produce a different hash and `merge_evidence` to treat identical evidence as new.
- **Decision:** Replace the custom emitter with `yaml.safe_dump(ordered_dict, sort_keys=False, default_flow_style=False, allow_unicode=True, width=1000000)`. Key ordering is preserved by inserting keys into a Python dict in the desired order (dict preserves insertion order since Python 3.7).
- **Consequence:** Round-trip loads are byte-stable. Any future field additions must be added to the `ordered_keys` list in `_render_frontmatter`; PyYAML handles all escaping automatically.

---

## Decision Process
- New decisions land here as `AD-NNN` in numerical order.
- Each decision references the context (audit, plan, sprint) that prompted it.
- Superseded decisions are marked `Superseded by AD-NNN` rather than deleted.
- This file is authoritative for *why* the system is the way it is. Code shows *what*; this file shows *why*.
