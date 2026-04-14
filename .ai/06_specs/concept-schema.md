# Concept Schema — Canonical Concept Files

> **Applies to:** files under `003_Canonical-Knowledge-Layer/shared/concepts/`.
> **Authoritative roadmap reference:** `/.ai/01_roadmap/master-roadmap.md` §2, §3, Phase 3
> **Schema version:** `1.0.0`
> **Updated:** 2026-04-14

---

## 1. Purpose
A Concept is a named, reusable knowledge node representing a domain idea (e.g., *occupancy classification*, *fire-resistive construction*, *lot occupancy*). Concepts form the **closed vocabulary** that relationship extraction is allowed to use (principle P7).

A concept is a first-class knowledge node: it carries a definition, a regulatory basis, aliases, and cross-references. In the current skeleton phase, most concept files are placeholders — Phase 3C promotes them to fully enriched Knowledge Nodes.

## 2. File Location & Naming
- **Directory:** `003_Canonical-Knowledge-Layer/shared/concepts/`
- **Filename:** `<slug>.md` — lowercase, hyphen-separated, URL-safe.
  - Example: `occupancy-classification.md`
- **ID prefix:** Always `concept-`.
  - Example: `concept-occupancy-classification`.

## 3. Frontmatter — Required Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Canonical ID, `concept-<slug>`. Immutable. |
| `title` | string | Human-readable concept name. |
| `page_type` | enum | Literal: `concept`. |
| `canonical_status` | enum | `placeholder` \| `draft` \| `enriched` \| `verified` \| `superseded`. |
| `concept_status` | enum | *(Phase 3C)* Same lifecycle as `canonical_status`; added to distinguish content-level from file-level readiness. |
| `last_canonicalized_utc` | ISO-8601 UTC | When the file was last regenerated. |

### 3.1 Canonical Status Lifecycle (concept-specific)
```
placeholder ─► draft ─► enriched ─► verified ─┐
    ▲                                         │
    └───────────── superseded ◄───────────────┘
```
- **`placeholder`** — Skeleton produced by the current `concepts.py`. Contains only a one-line stub definition. Consumable as vocabulary but not as knowledge.
- **`draft`** — Has a real definition but regulatory basis and aliases are missing.
- **`enriched`** — Full Knowledge Node: definition + ≥1 source pointer + aliases + cross-references.
- **`verified`** — Enriched and reviewed by a domain expert OR by Tier-3 promotion logic.
- **`superseded`** — Replaced by a newer concept (e.g., merged into a parent). Retained for history; not consumed by extraction.

## 4. Frontmatter — Optional Fields
| Field | Type | Purpose |
|---|---|---|
| `aliases` | string[] | Alternate names and spellings. Populated by Phase 1C alias registry and manual curation. |
| `regulatory_basis` | object[] | Pointers to source sections. Each entry: `{source_id, section_id, evidence_snippet}`. |
| `related_concepts` | string[] | Concept IDs that this concept refers to or depends on. |
| `parent_concept` | string | Concept ID this concept specializes. |
| `child_concepts` | string[] | Concept IDs that specialize this concept. |
| `topic_tags` | string[] | Domain tags for filtering. |
| `jurisdiction` | string | e.g., `philippines`. |
| `language` | string | ISO 639-1 (e.g., `en`). |
| `enriched_at_utc` | ISO-8601 UTC | When the concept transitioned past `draft`. |
| `reviewed_at_utc` | ISO-8601 UTC | When the concept transitioned to `verified`. |
| `reviewer` | string | Reviewer identifier (model or human). |
| `ifc_class` | string | *(Stream M.2)* IFC 4.3 class name that best models this concept (e.g., `IfcDoor`, `IfcWall`, `IfcSpace`). Must start with `Ifc`. Validated by `scripts/vitruvius/ontology/ifc_validator.py` against `scripts/vitruvius/ontology/ifc_mapping.yaml`. |
| `ifc_psets` | string[] | *(Stream M.2)* Optional list of IFC Property Set names paired with `ifc_class` (e.g., `[Pset_DoorCommon]`). Purely descriptive until Stream M.4 lint runs — no behaviour change if omitted. |

## 5. Body Structure — Required Sections

### 5.1 `## Definition` — Always required
A single, precise paragraph. For `placeholder` concepts the canonicalizer emits a stub; for `draft+` the definition is extracted from a source or written by a curator.

### 5.2 `## Regulatory Basis` — Required for `enriched+`
Bulleted list of source pointers. Each bullet:
```
- **[Source Title](source-id)** — Section <section_id>: "<evidence snippet>"
```

### 5.3 `## Related Concepts` — Required for `enriched+`
Bulleted list of concept IDs with one-line relationship descriptions.
```
- `concept-fire-resistive-construction` — determined by this concept's classification.
- `concept-occupancy-load` — calculated per classification class.
```

## 6. Body Structure — Optional Sections
- `## Aliases` — Human-readable list when the alias registry has >3 entries.
- `## Examples` — Illustrative examples from sources, each citing a section.
- `## Historical Context` — When the concept was introduced or changed.
- `## Notes` — Free-form. Not consumed by extraction.

## 7. Placeholder Example (current reality)
```markdown
---
id: concept-occupancy-classification
title: Occupancy Classification
page_type: concept
canonical_status: placeholder
concept_status: placeholder
last_canonicalized_utc: 2026-04-13T08:44:19.832285+00:00
---

# Occupancy Classification

## Definition
Occupancy Classification is a defined concept within the Vitruvius system.
```

## 8. Enriched Example (target state — Phase 3C)
```markdown
---
id: concept-occupancy-classification
title: Occupancy Classification
page_type: concept
canonical_status: enriched
concept_status: enriched
last_canonicalized_utc: 2026-05-10T00:00:00Z
enriched_at_utc: 2026-05-10T00:00:00Z
aliases:
  - occupancy type
  - occupancy group
  - use classification
topic_tags:
  - building-code
  - occupancy
  - philippines
jurisdiction: philippines
language: en
regulatory_basis:
  - source_id: law-national-building-code-of-the-philippines
    section_id: sec-701
    evidence_snippet: "Every building shall be classified in accordance with its use or occupancy…"
related_concepts:
  - concept-fire-resistive-construction
  - concept-occupancy-load
  - concept-mixed-occupancy
---

# Occupancy Classification

## Definition
Occupancy Classification is the categorization of a building or structure by
its use, which in turn determines the applicable fire-resistive requirements,
egress requirements, and structural loading rules under the National Building
Code of the Philippines (PD 1096).

## Regulatory Basis
- **[National Building Code of the Philippines](law-national-building-code-of-the-philippines)** — Section 701: "Every building shall be classified in accordance with its use or occupancy…"

## Related Concepts
- `concept-fire-resistive-construction` — fire-resistive requirements are determined by the occupancy classification.
- `concept-occupancy-load` — occupancy load is computed per classification class.
- `concept-mixed-occupancy` — buildings with more than one classification require a mixed-occupancy analysis.
```

## 9. Validation Rules

### 9.1 Structural (enforced by `run_lint` and canonicalizer)
1. Frontmatter present and parseable.
2. `id` matches `^concept-[a-z][a-z0-9-]*$`.
3. `title` non-empty.
4. `page_type == "concept"`.
5. `canonical_status` in allowed enum.
6. `last_canonicalized_utc` parseable.
7. Filename slug matches the ID slug: `concept-<slug>.md` contains `id: concept-<slug>`.
8. **Unique ID** across `003_Canonical-Knowledge-Layer/shared/concepts/`.

### 9.2 Content (enforced at status promotion)
- `canonical_status == "draft"` ⇒ `## Definition` contains more than the placeholder sentence.
- `canonical_status == "enriched"` ⇒ `## Regulatory Basis` has ≥1 source pointer with a non-empty `evidence_snippet`.
- `canonical_status == "enriched"` ⇒ `## Related Concepts` has ≥1 entry, each resolving to an existing concept file.
- `canonical_status == "verified"` ⇒ `reviewer` and `reviewed_at_utc` are set.

### 9.3 Cross-Schema
- Every concept ID referenced in a source's `## Referenced Concepts` MUST exist as a concept file (enforced by source schema §8 rule 10).
- Every concept ID used in a relationship's `from_entity` or `to_entity` MUST exist as a concept file with `canonical_status != "placeholder"` **at promotion time** (enforced by Promotion Validator in Phase 7).

## 10. Relationship to Other Schemas
- **Source schema:** Concepts reference sources through `regulatory_basis`. The Promotion Validator cross-checks that every `source_id` used by a concept resolves to an existing canonical source file.
- **Relationship schema:** Relationship records use concept IDs as their `from_entity` and `to_entity` endpoints. See `/.ai/06_specs/relationship-schema.md` §4.

## 11. Change Policy
- **`id` is immutable.** Use `migrate-ids-plan` to rename.
- **Merging concepts:** produces `superseded` status on the absorbed concept with a `superseded_by` pointer. Extraction ignores superseded concepts.
- **Splitting concepts:** the original concept goes to `superseded`, replaced by two or more new IDs that cross-reference each other. A migration record is required in `/.ai/10_state/decisions.md`.

## 12. Open Questions
- Whether `placeholder` concepts should still be usable by the extractor as vocabulary. Current position: yes — vocabulary presence is the minimum bar for Phase 5 to match. The review layer catches any weak matches downstream.
- Whether `regulatory_basis` should support multi-source concepts with conflict resolution. Deferred until Phase 11 (dataset expansion).

## Changelog
- **2026-04-14** — Initial schema published. Derived from current placeholder generator output + Phase 3C enrichment targets in the master roadmap.
