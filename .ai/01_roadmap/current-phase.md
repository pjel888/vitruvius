# Current Phase — Sprint A: Unblock Promotion (Phase 7)

> **Authoritative roadmap:** `/.ai/01_roadmap/master-roadmap.md` (v2.0.0)
> **This document is the execution snapshot for the active sprint only.**
> **Revised:** 2026-04-14 · **Sprint ends:** 2026-04-28 (2 weeks)

---

## North-Star Objective
Land **Phase 7 — Promotion Governance** on top of the existing Ollama review output so approved candidates graduate from `latest_relationship_review_ollama.json` into the Canonical Knowledge Layer under a strict schema and audit log.

This unblocks the entire downstream stack (Phase 8 graph, Phase 9 query, Phase 11 expansion) and exercises the governance contract end-to-end for the first time.

## Why Now
- **Phase 6A (LLM Review) is functional** — verified by the 2026-04-13 audit. It produces structured `keep` / `review_further` / `reject` decisions with bounded confidence. We already have output to promote.
- **Phase 7 is independent of upstream noise.** Even with the current 82% rejection rate, high-confidence `keep` decisions exist and are safe to promote behind the 0.90 confidence threshold.
- **Every downstream phase is blocked on Phase 7.** No graph, no query, no corpus expansion until promotion works.
- **Normalization (Phase 1C) is happening in parallel** in Sprint B — it shrinks the noise but is not on Sprint A's critical path.

## Sprint A Task List (strict order)

### A-1. Phase 6A Minimal Gap Closure (1–2 days)
- [ ] Move hardcoded Ollama URL from `ollama_review.py` into `config/vitruvius.yaml` under `review.ollama.url`.
- [ ] Add a `latest_relationship_review_high_confidence.json` writer that filters Gemma output to `keep` decisions with `confidence >= 0.90`. This is the Phase 7 input file.
- [ ] Verify the writer emits an empty-but-valid file when no candidates clear the threshold.

**Exit criteria:** Phase 7 has a clean, schema-stable input file to consume.

### A-2. Relationship Type Registry (0.5 day)
- [ ] Create `scripts/vitruvius/rules/relationship_registry.yaml`.
- [ ] Populate with the closed vocabulary from master-roadmap §3.1: `governs`, `requires`, `defines`, `depends_on`, `limits`, `affects`, `supersedes`.
- [ ] Encode compatibility rules as `allowed_pairs: [{subject_type, object_type}]` per predicate.
- [ ] Add version: `schema_version: 1.0.0`.

**Exit criteria:** Registry loads, validates YAML, and is importable by `promotion_validator.py`.

### A-3. Promotion Validator (1–2 days)
- [ ] Create `scripts/vitruvius/promotion_validator.py`.
- [ ] Enforce the schema in master-roadmap §3.5: required fields `source_section_id`, `evidence_snippet`, `confidence_score`, `review_decision`, `reviewer_model`, `reviewed_at_utc`, `promotion_batch_id`, `promotion_audit_log_ref`.
- [ ] Predicate-in-registry check.
- [ ] Subject/object type compatibility check against the registry.
- [ ] Produce a `ValidationResult` with pass/fail + reasons (no exceptions for validation failures — treat them as data).

**Exit criteria:** Validator is unit-tested against one valid record and three invalid records (unknown predicate, missing section_id, incompatible types).

### A-4. Promotion Writer `run_promote` (3–4 days)
- [ ] Create `scripts/vitruvius/promotion.py` with `run_promote`.
- [ ] Register CLI command: `python scripts/pipeline_cli.py promote`.
- [ ] **Dry-run by default** (`--execute` to actually write).
- [ ] Read `latest_relationship_review_high_confidence.json`.
- [ ] For each record: validate → locate or create the target relationship file under `003_Canonical-Knowledge-Layer/shared/relationships/` → merge evidence if the triplet already exists, else create.
- [ ] Generate `promotion_batch_id` as `YYYYMMDDTHHMMSSZ_<short_hash>`.
- [ ] Write `006_System-Manifests/runs/latest_promotion_audit.log` and a timestamped copy.
- [ ] Idempotency: re-running with no new high-confidence candidates writes an empty batch, not a duplicate.
- [ ] Add `--rollback <batch_id>` that reverses edits listed in a batch's audit entries.

**Exit criteria:** `pipeline_cli.py promote --dry-run` on the PD 1096 review output lists the candidates that would be promoted. `pipeline_cli.py promote --execute` writes them.

### A-5. Golden Path (0.5 day)
- [ ] Run the full pipeline on PD 1096 up to review.
- [ ] Execute `promote --execute`.
- [ ] Verify at least 3 relationships land in `003/shared/relationships/` with all required fields.
- [ ] Verify `promotion_audit.log` records the batch.
- [ ] Re-run `promote` to confirm idempotency (no duplicate writes, no audit noise).

**Exit criteria:** Three relationship files exist in canonical storage with passing schema validation.

### A-6. Decision Log (0.25 day)
- [ ] Add `AD-011: Promotion Layer First Promotion` to `/.ai/10_state/decisions.md` recording:
  - Final shape of the first promoted record.
  - Any schema deviations from master-roadmap §3.5 and why.
  - Observed high-confidence volume vs. total candidates.
- [ ] Update `/.ai/10_state/active_context.md` to reflect Sprint A completion and Sprint B kickoff.
- [ ] Update the §4 status table in `master-roadmap.md` — Phase 7 from ❌ to 🟡 PARTIAL, then ✅ COMPLETE once all exit criteria hold.

## Blockers / Dependencies
- **None internal.** Sprint A is deliberately independent of Sprint B (normalization) and Sprint C (multi-parser).
- **External:** Ollama must be running on the developer machine for A-5. No cloud dependencies.

## Out of Scope for Sprint A
- Second-pass review (Phase 6B) — Sprint C.
- Normalization layer (Phase 1C) — Sprint B.
- Multi-parser orchestrator (Phase 1B) — Sprint C.
- Graph indexing (Phase 8) — blocked on Phase 7 producing ≥50 records.
- Adding new laws or documents — blocked by principle P10.

## Sprint A Exit Criteria (Definition of Done)
- [x] Master roadmap v2.0.0 published (this action, already done).
- [ ] Ollama URL configurable via `config/vitruvius.yaml`.
- [ ] High-confidence review artifact writer shipping.
- [ ] Relationship registry YAML present and validated.
- [ ] Promotion validator unit-tested.
- [ ] `run_promote` CLI command registered, dry-run and execute modes working.
- [ ] First 3 PD 1096 relationships live in `003/shared/relationships/` with passing validation.
- [ ] `promotion_audit.log` records the batch.
- [ ] Idempotency verified (re-run produces no new writes).
- [ ] Rollback tested on a throwaway batch.
- [ ] Decision log entry written.
- [ ] Roadmap §4 status updated.

## Sprint A Gating Metrics
- Promotion schema validation pass rate == 100% on valid inputs.
- Registry rejection rate == 0% on verified `keep` inputs.
- Audit log completeness == 100%.
- Dry-run / execute parity: bytes written in execute mode == bytes previewed in dry-run.

## Next Sprint Preview (Sprint B — weeks 3–6)
- **Phase 1C Text Refinement Layer** to shrink the 82% rejection rate.
- **Phase 6A full gap closure** (retry, resume, per-candidate timeout).
- Re-run PD 1096 end-to-end and measure the new rejection rate.
