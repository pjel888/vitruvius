# Relationship Schema — Canonical Relationship Files

> **Applies to:** files under `003_Canonical-Knowledge-Layer/shared/relationships/`.
> **Authoritative roadmap reference:** `/.ai/01_roadmap/master-roadmap.md` §3.1, §3.5, Phase 7
> **Schema version:** `1.0.0`
> **Updated:** 2026-04-14

---

## 1. Purpose
A Relationship is a promoted, evidence-bearing edge between two canonical entities (source↔concept or concept↔concept). It is the payload of the Phase 7 Promotion Layer and the unit of truth the Phase 8 graph is built from.

Every field in this schema has the same goal: **make the edge replayable** — any reader or automated checker can trace the edge back to its source section and the review decisions that admitted it.

## 2. File Location & Naming
- **Directory:** `003_Canonical-Knowledge-Layer/shared/relationships/`
- **Filename:** `<slug>.md` — one file per triplet family (multiple evidence snippets for the same `(subject, predicate, object)` merge into one file).
  - Example: `occupancy-governs-fire-requirements.md`
- **ID prefix:** Always `rel-`.
  - Example: `rel-occupancy-governs-fire-requirements`.

## 3. Closed Predicate Vocabulary (Relationship Type Registry)
Only these predicates are allowed. The Promotion Validator rejects any record using an unknown predicate.

| Predicate | Semantics | Allowed Pairs (subject_type → object_type) |
|---|---|---|
| `governs` | Subject legally governs the object. | `source → concept` |
| `defines` | Subject provides the definitional text for the object. | `source → concept` |
| `requires` | Subject requires the object to exist or be satisfied. | `concept → concept`, `concept → attribute` |
| `depends_on` | Subject cannot be determined without the object. | `concept → concept` |
| `limits` | Subject places numeric or scope limits on the object. | `source → concept`, `source → attribute`, `section → concept`, `section → attribute` |
| `affects` | Subject changes the behavior or value of the object without requiring or limiting it. | `concept → concept`, `source → concept` |
| `supersedes` | Subject is a newer version that replaces the object. | `source → source`, `concept → concept` |

Registry location (to be created in Sprint A · A-2): `scripts/vitruvius/rules/relationship_registry.yaml`.

## 4. Frontmatter — Required Fields
Every relationship file MUST include these keys. The Promotion Validator rejects any file missing them.

| Field | Type | Description |
|---|---|---|
| `id` | string | Canonical ID, `rel-<slug>`. Immutable. |
| `title` | string | Human-readable name for the edge family. |
| `page_type` | enum | Literal: `relationship`. |
| `relationship_type` | enum | Predicate from the closed vocabulary in §3. |
| `from_entity` | string | Canonical ID of the subject (source or concept). |
| `to_entity` | string | Canonical ID of the object (source or concept). |
| `trust_level` | enum | Inherited from the lowest-trust source in `evidence`. |
| `canonical_status` | enum | `draft` \| `promoted` \| `verified` \| `superseded`. |
| `confidence_score` | float [0,1] | Minimum confidence across merged evidence entries. |
| `evidence` | object[] | Array of evidence entries — see §5. At least one required. |
| `promotion_batch_id` | string | ID of the Phase 7 batch that created or last updated this record. |
| `promotion_audit_log_ref` | string | Path to the audit log entry for `promotion_batch_id`. |
| `last_promoted_utc` | ISO-8601 UTC | When the last promotion batch wrote this record. |

### 4.1 Canonical Status Lifecycle
```
draft ─► promoted ─► verified ─┐
   ▲                           │
   └───── superseded ◄─────────┘
```
- **`draft`** — Written by a manual curator but not yet processed by the Promotion Layer.
- **`promoted`** — Written or updated by `run_promote` after passing the validator.
- **`verified`** — Reviewed by a human expert or by Tier-3 adjudication (Phase 6B).
- **`superseded`** — Replaced by a newer edge. Retained for history. Not consumed by the graph builder.

## 5. Evidence Entry Shape
Each item in the `evidence` array is a full audit trail for one occurrence of this relationship in a source document.

```yaml
- source_id: law-national-building-code-of-the-philippines
  source_section_id: sec-701
  source_artifact: 002_Raw-Conversion-Layer/001-Laws/raw_markdown/PD-1096/PD 1096.md
  evidence_snippet: "Every building shall be classified in accordance with its use or occupancy…"
  snippet_start_line: 1423
  snippet_end_line: 1428
  review_decision: keep
  reviewer_model: gemma4:31b
  reviewer_confidence: 0.92
  reviewer_reason: "Evidence clearly supports governs relationship between occupancy and fire-resistive requirements."
  second_pass_model: null
  second_pass_decision: null
  second_pass_confidence: null
  extracted_at_utc: 2026-04-13T08:44:19Z
  reviewed_at_utc: 2026-04-13T09:01:02Z
```

### 5.1 Required Evidence Fields
- `source_id` — Must resolve to a file in `003_Canonical-Knowledge-Layer/shared/sources/`.
- `source_section_id` — Non-null. Principle P9 (no soft output).
- `evidence_snippet` — Non-empty string, verbatim from the source.
- `review_decision` — `keep` (only `keep` may be promoted).
- `reviewer_model` — Identifier of the model that produced the decision.
- `reviewer_confidence` — Float [0,1]. Only `>= 0.90` may be auto-promoted.
- `reviewed_at_utc` — ISO-8601 UTC.

### 5.2 Optional Evidence Fields
- `second_pass_*` — Populated if Phase 6B has run.
- `snippet_start_line` / `snippet_end_line` — For precise back-pointing.
- `reviewer_reason` — Human-readable rationale from the reviewer.
- `human_reviewer` — Set if escalated to Tier 3.

## 6. Merge Semantics
When `run_promote` encounters a record with the same `(relationship_type, from_entity, to_entity)` triplet as an existing file:

1. **Append** the new evidence entry to the existing `evidence` array.
2. **Update** `confidence_score` to `min(existing, new)` — the overall edge confidence is only as strong as its weakest piece of supporting evidence.
3. **Update** `trust_level` to the lowest among all evidence sources.
4. **Update** `last_promoted_utc` and `promotion_batch_id`.
5. **Append** an audit log entry referencing both the old and new batch IDs.
6. **Never duplicate a triplet row.** The file is the canonical edge; its evidence array grows over time.

Duplicate *evidence* entries (same source + same section_id + same snippet) are de-duplicated by `(source_id, source_section_id, snippet_hash)`.

## 7. Body Structure — Required Sections

### 7.1 `## Relationship Summary`
One sentence. Plain language. No jargon. Example: *"Occupancy classification determines the level of fire-resistive requirements that must be applied to a building or structure."*

### 7.2 `## Explanation`
1–3 paragraphs of contextual explanation. Written by the canonicalizer or by a human curator. Does not introduce new facts beyond what the evidence supports.

### 7.3 `## Implications`
Bulleted list of the downstream consequences of this relationship.

### 7.4 `## Evidence`
Generated from the frontmatter `evidence` array. One subsection per evidence entry:
```markdown
### Evidence 1 — `law-national-building-code-of-the-philippines` §sec-701

> "Every building shall be classified in accordance with its use or occupancy…"

- Reviewer: `gemma4:31b` · Decision: `keep` · Confidence: `0.92`
- Reviewed: 2026-04-13T09:01:02Z
- Batch: `20260414T030000Z_a1b2c3d4`
```

## 8. Body Structure — Optional Sections
- `## Related Concepts` — Concept IDs logically adjacent to this edge.
- `## Related Relationships` — Other relationship IDs in the same neighborhood.
- `## Notes` — Free-form commentary.

## 9. Worked Example

```markdown
---
id: rel-occupancy-governs-fire-requirements
title: Occupancy Classification Governs Fire-Resistive Requirements
page_type: relationship
relationship_type: governs
from_entity: concept-occupancy-classification
to_entity: concept-fire-resistive-construction
trust_level: primary
canonical_status: promoted
confidence_score: 0.92
promotion_batch_id: 20260414T030000Z_a1b2c3d4
promotion_audit_log_ref: 006_System-Manifests/runs/20260414T030000Z_a1b2c3d4_promotion_audit.log
last_promoted_utc: 2026-04-14T03:00:00Z
evidence:
  - source_id: law-national-building-code-of-the-philippines
    source_section_id: sec-701
    source_artifact: 002_Raw-Conversion-Layer/001-Laws/raw_markdown/PD-1096/PD 1096 IRR.md
    evidence_snippet: "Every building shall be classified in accordance with its use or occupancy…"
    snippet_start_line: 1423
    snippet_end_line: 1428
    review_decision: keep
    reviewer_model: gemma4:31b
    reviewer_confidence: 0.92
    reviewer_reason: "Evidence clearly supports a governs relationship."
    second_pass_model: null
    second_pass_decision: null
    second_pass_confidence: null
    extracted_at_utc: 2026-04-13T08:44:19Z
    reviewed_at_utc: 2026-04-13T09:01:02Z
---

# Occupancy Classification Governs Fire-Resistive Requirements

## Relationship Summary
Occupancy classification determines the level of fire-resistive requirements that must be applied to a building or structure.

## Explanation
Under the Implementing Rules and Regulations (IRR) of the National Building Code of the Philippines,
different occupancy groups present different levels of risk to life and property. As a result, each
occupancy classification is assigned corresponding fire-resistive requirements…

## Implications
- Incorrect occupancy classification leads to incorrect fire safety design.
- Fire-resistive construction cannot be determined independently of occupancy.
- Compliance review must evaluate both occupancy and fire provisions together.

## Evidence

### Evidence 1 — `law-national-building-code-of-the-philippines` §sec-701

> "Every building shall be classified in accordance with its use or occupancy…"

- Reviewer: `gemma4:31b` · Decision: `keep` · Confidence: `0.92`
- Reviewed: 2026-04-13T09:01:02Z
- Batch: `20260414T030000Z_a1b2c3d4`
```

## 10. Validation Rules (Promotion Validator)
The Promotion Validator MUST enforce the following. Failure on any rule aborts promotion for that record and logs the reason to the audit log.

### 10.1 Structural
1. Frontmatter present and parseable.
2. `id` matches `^rel-[a-z][a-z0-9-]*$`.
3. `page_type == "relationship"`.
4. `relationship_type` in the closed vocabulary (§3).
5. `from_entity` / `to_entity` are existing canonical IDs.
6. `evidence` array non-empty.

### 10.2 Registry Compatibility
7. `(from_entity.type, to_entity.type)` is an allowed pair for `relationship_type` per the registry.

### 10.3 Evidence Integrity
8. Every evidence entry has a non-null `source_section_id`.
9. Every evidence entry has a non-empty `evidence_snippet`.
10. Every evidence `source_id` resolves to an existing canonical source.
11. `reviewer_confidence` is a float in `[0, 1]`.
12. `review_decision == "keep"` on every evidence entry (only `keep` can be promoted).

### 10.4 Promotion Threshold
13. `confidence_score >= 0.90` unless the record is being updated (merge mode) and an existing evidence entry already met the threshold.

### 10.5 Trust Propagation
14. `trust_level == min(evidence[].source.trust_level)`.

### 10.6 Audit Integrity
15. `promotion_batch_id` is set and appears in the audit log.
16. `last_promoted_utc` is set.

### 10.7 Referential Integrity
17. `canonical_status == "promoted"` implies `from_entity` and `to_entity` are each in `canonical_status != "placeholder"` and `!= "superseded"`.

## 11. Relationship to Other Schemas
- **Source schema:** every `evidence[].source_id` resolves to a source file. `trust_level` is inherited.
- **Concept schema:** `from_entity` and `to_entity` resolve to concept or source files. Concepts referenced must not be in `placeholder` status at promotion time.

## 12. Change Policy
- **`id` is immutable.** Use `migrate-ids-plan` to rename.
- **Adding evidence** is a merge operation via `run_promote`. Never edit `evidence` arrays by hand if the file has `canonical_status == "promoted"`.
- **Removing evidence** requires a rollback batch referencing the original `promotion_batch_id`.
- **Predicate changes** (e.g., `affects` → `governs`) are not edits — they produce a new `rel-*` record; the old one transitions to `superseded` with `superseded_by` set.

## 13. Open Questions
- Whether negative evidence (`review_decision == "reject"` with high confidence) should produce a complementary "anti-edge" record. Deferred until Phase 8 graph operations need it.
- Whether `affects` should be further specialized into `strengthens` / `weakens`. Deferred — would fragment the closed vocabulary.

## Changelog
- **2026-04-14** — Initial schema published. Aligned with master-roadmap §3.1 and §3.5. Derived from the existing draft relationship file plus Phase 7 Promotion Contract requirements.
