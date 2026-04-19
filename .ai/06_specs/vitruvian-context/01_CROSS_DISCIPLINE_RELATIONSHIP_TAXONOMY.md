# Cross-Discipline Relationship Taxonomy

> **Extends:** `.ai/06_specs/relationship-schema.md`
> **Authority:** `00_locked_decisions.md` (D1, D2, D7, D10)
> **Schema version:** `2.0.0`
> **Date:** 2026-04-19

---

## 1. Purpose

The existing relationship schema (`.ai/06_specs/relationship-schema.md`) defines 7 predicates for evidence-bearing edges between sources and concepts. This document extends that vocabulary with **cross-discipline connection types** that model how AEC disciplines influence, constrain, and depend on each other.

**Core principle:** Every concept has exactly one `primary_domain` facet value (its home in the backbone), but may connect to many other domains via typed, directional, contextual relationships.

This prevents:
- Duplicate concept nodes for cross-cutting subjects
- Vague `RELATED_TO` edges that lose semantic meaning
- Circular taxonomy dependencies

---

## 2. Relationship Categories

### 2.1 Domain Affiliation (Structural)

| Predicate | Direction | Cardinality | Semantics |
|-----------|-----------|-------------|-----------|
| `BELONGS_TO_DOMAIN` | `concept → backbone_node` | 1:1 | Graph edge connecting concept to its L4 backbone node. Derived from `primary_domain` facet. |

**Rule:** A concept MUST have exactly one `primary_domain` facet value. The `BELONGS_TO_DOMAIN` edge is a graph projection of that facet and must match it.

**Validation:** `validate_backbone.py` checks that every `CanonicalNode` has a non-null `primary_domain` facet. `validate_graph.py` checks that `BELONGS_TO_DOMAIN` edges match the `primary_domain` facet.

---

### 2.2 Cross-Discipline Influence (Semantic)

| Predicate | Direction | Cardinality | Semantics | Example |
|-----------|-----------|-------------|-----------|---------|
| `USED_IN` | `concept → domain` | 1:N | Concept is materially used or applied in another discipline. | Concrete → Architecture (used in envelope) |
| `CONSTRAINS` | `concept → concept` | 1:N | Subject imposes hard limits on object. Must be satisfied. | Reinforced concrete detailing → Architecture (dimensions, clearances) |
| `REQUIRES` | `concept → concept` | 1:N | Subject cannot exist without object. | Fire exit stair → Structural support |
| `AFFECTS` | `concept → concept` | 1:N | Subject changes behavior or value of object without requiring it. | HVAC → Interior design (ceiling heights) |
| `INFLUENCES` | `concept → concept` | 1:N | Subject shapes decisions about object, but no hard constraint. | Sustainability → Material selection |
| `EXECUTED_IN` | `concept → domain` | 1:N | Concept is implemented or constructed in this discipline. | Concrete → Construction |
| `REGULATED_BY` | `concept → domain` | 1:N | Concept is governed by rules from this discipline/domain. | Accessible ramp → Regulatory (BP 344) |
| `SUPPORTED_BY` | `concept → concept` | 1:N | Subject is structurally or logically supported by object. | Slab → Beam |
| `PRODUCES` | `concept → concept` | 1:N | Subject generates or outputs object. | Design → Drawing set |
| `CONSUMES` | `concept → concept` | 1:N | Subject uses or takes in object. | Construction → Concrete |

**Rule:** All cross-discipline edges MUST have a `relationship_type` from this closed vocabulary. No `RELATED_TO` edges are permitted for cross-discipline connections.

---

### 2.3 Standards Mapping

| Predicate | Direction | Cardinality | Semantics |
|-----------|-----------|-------------|-----------|
| `MAPS_TO_STANDARD` | `concept → standard_reference` | 1:N | Concept maps to an external classification system. |
| `EQUIVALENT_TO` | `standard_reference → standard_reference` | 1:1 | Two standard codes are semantically equivalent across systems. |

**Properties:**
- `mapping_type`: `exact` | `narrower` | `broader` | `related`
- `confidence`: float [0, 1]
- `mapped_by`: steward or AI model identifier
- `mapped_at`: ISO-8601 timestamp

---

### 2.4 Jurisdiction + Overlay

| Predicate | Direction | Cardinality | Semantics |
|-----------|-----------|-------------|-----------|
| `APPLIES_IN` | `edition/rule → jurisdiction` | 1:N | Document edition or rule applies in this jurisdiction. |
| `HAS_OVERLAY` | `concept → overlay` | 1:N | Concept has jurisdiction-specific obligation. |
| `BASED_ON` | `overlay → edition` | 1:1 | Overlay is derived from this document edition. |
| `WITHIN_JURISDICTION` | `jurisdiction → jurisdiction` | 1:1 | Child jurisdiction is within parent jurisdiction. |
| `GOVERNS` | `source → concept` | 1:N | Source legally governs the concept. *(Existing — preserved)* |
| `DEFINED_BY` | `source → concept` | 1:N | Source provides definitional text. *(Existing — preserved)* |

---

### 2.5 Lifecycle + Supersession

| Predicate | Direction | Cardinality | Semantics |
|-----------|-----------|-------------|-----------|
| `SUPERSEDES` | `edition → edition` | 1:1 | Newer edition replaces older edition. |
| `SUPERSEDED_BY` | `concept → concept` | 1:1 | Concept/node is replaced by newer version. *(Used for ID migration)* |
| `HAS_EDITION` | `family → edition` | 1:N | Document family contains this edition. |

---

## 3. Domain Pair Constraints

Not all predicates are valid between all domain pairs. The following matrix defines allowed connections.

### 3.1 Cross-Discipline Influence Matrix

Allowed `USED_IN` / `CONSTRAINS` / `REQUIRES` / `AFFECTS` / `INFLUENCES` / `EXECUTED_IN` / `REGULATED_BY` pairs:

| From Domain | To Domain | Allowed Predicates | Rationale |
|-------------|-----------|-------------------|-----------|
| Structural | Architecture | `CONSTRAINS`, `AFFECTS`, `REQUIRES` | Structure drives form |
| Structural | Construction | `EXECUTED_IN`, `REQUIRES` | Structure is built |
| Structural | MEP | `AFFECTS`, `INFLUENCES` | Beam drops affect ducts |
| Architecture | Structural | `REQUIRES`, `INFLUENCES` | Form drives structure |
| Architecture | MEP | `REQUIRES`, `CONSTRAINS` | Ceiling height, shaft locations |
| Architecture | Regulatory | `REGULATED_BY` | Design is code-governed |
| MEP | Architecture | `CONSTRAINS`, `AFFECTS` | Equipment sizes affect spaces |
| MEP | Structural | `REQUIRES`, `AFFECTS` | Equipment loads |
| Construction | Architecture | `CONSTRAINS`, `AFFECTS` | Buildability affects design |
| Construction | Structural | `EXECUTED_IN`, `CONSUMES` | Construction consumes materials |
| Regulatory | Architecture | `CONSTRAINS`, `REQUIRES` | Code constrains design |
| Regulatory | Structural | `CONSTRAINS`, `REQUIRES` | Code constrains structure |
| Regulatory | MEP | `CONSTRAINS`, `REQUIRES` | Code constrains systems |
| Sustainability | Architecture | `INFLUENCES`, `AFFECTS` | Green design influences form |
| Sustainability | MEP | `INFLUENCES`, `REQUIRES` | Energy targets affect systems |
| Fire/Life Safety | Architecture | `CONSTRAINS`, `REQUIRES` | Egress constraints |
| Fire/Life Safety | Structural | `CONSTRAINS`, `REQUIRES` | Fire rating requirements |
| Fire/Life Safety | MEP | `CONSTRAINS`, `REQUIRES` | Smoke control |
| Accessibility | Architecture | `CONSTRAINS`, `REQUIRES` | Clearances, routes |
| Accessibility | Structural | `AFFECTS`, `INFLUENCES` | Slope requirements |

**Rule:** Any edge between domains not in this matrix MUST be reviewed by a steward and documented with rationale.

**AI constraint:** AI tools may only propose edges in this matrix. Out-of-matrix proposals require human steward approval.

---

## 4. Connection Quality Rules

### 4.1 No Vague Edges

**Forbidden:**
- `RELATED_TO` between concepts from different domains
- `SIMILAR_TO` without defined similarity criteria
- `CONNECTED_TO` without predicate type

**Required:** Every cross-discipline edge MUST use a predicate from §2.2 or §2.4.

### 4.2 No Circular Dependencies

**Rule:** The graph of `REQUIRES` + `DEPENDS_ON` + `CONSTRAINS` edges must be acyclic within a single domain.

**Validation:** `scripts/vitruvius/taxonomy/validate_graph.py` runs cycle detection on these edge types per domain.

### 4.3 Primary Domain Immutability

**Rule:** Once a concept's `primary_domain` facet is assigned, it cannot change without:
1. Steward approval
2. Update to all cross-discipline edges
3. Update to `path_code`
4. Entry in backbone change log

### 4.4 Edge Confidence Thresholding

| Predicate | Minimum Confidence | Review Required |
|-----------|-------------------|-----------------|
| `primary_domain` (facet) | 1.0 (human-assigned) | Always |
| `CONSTRAINS` | 0.90 | Steward |
| `REQUIRES` | 0.90 | Steward |
| `AFFECTS` | 0.75 | AI-review queue |
| `INFLUENCES` | 0.70 | AI-review queue |
| `USED_IN` | 0.75 | AI-review queue |
| `EXECUTED_IN` | 0.80 | AI-review queue |
| `REGULATED_BY` | 0.95 | Steward |
| `MAPS_TO_STANDARD` | 0.70 | Domain expert |

---

## 5. Example: Reinforced Concrete Detailing

```cypher
// Backbone placement
CREATE (c:CanonicalNode {
  canonical_id: "VTN-CON-0000100",
  path_code: "STR.RCD.001",
  label: "Reinforced Concrete Detailing",
  primary_domain: "taxonomy-structural"
})

// Primary domain
CREATE (str:BackboneNode {path_code: "STR", pref_label: "Structural Engineering"})
CREATE (c)-[:BELONGS_TO_DOMAIN]->(str)

// Cross-discipline connections
CREATE (arch:BackboneNode {path_code: "ARC", pref_label: "Architecture"})
CREATE (con:BackboneNode {path_code: "CON", pref_label: "Construction"})
CREATE (reg:BackboneNode {path_code: "REG", pref_label: "Regulatory"})

CREATE (c)-[:CONSTRAINS {confidence: 0.95, rationale: "rebar cover determines finish clearance"}]->(arch)
CREATE (c)-[:EXECUTED_IN {confidence: 0.98, rationale: "concrete placement is construction activity"}]->(con)
CREATE (c)-[:REGULATED_BY {confidence: 0.96, rationale: "NSCP Chapter 4 governs detailing"}]->(reg)
```

**Explorer UI rendering:**
```
Reinforced Concrete Detailing
VTN-CON-0000100
🔵 Canonical | Structural Engineering

Primary Domain:
→ Structural Engineering

Also affects:
→ Architecture (constrains: rebar cover)
→ Construction (executed in: concrete placement)
→ Regulatory (regulated by: NSCP Chapter 4)
```

---

## 6. Migration from Existing Graph

### 6.1 Current State

Existing edges are typed as:
- `HAS_CHILD` / `BELONGS_TO` — taxonomy hierarchy
- `RELATED_TO` — vague cross-concept links
- `DEFINED_BY` / `DEPENDS_ON` / `REQUIRES` — existing semantic edges

### 6.2 Migration Rules

1. `HAS_CHILD` / `BELONGS_TO` → Replace with `BELONGS_TO_DOMAIN` + backbone edges
2. `RELATED_TO` → Review and retype:
   - If same domain → keep as `RELATED_TO` (intra-domain)
   - If different domain → retype to `USED_IN`, `CONSTRAINS`, `AFFECTS`, `INFLUENCES`, or `REQUIRES`
   - If cannot determine type → flag for steward review
3. `DEFINED_BY` / `DEPENDS_ON` / `REQUIRES` → Preserve if intra-domain; review if cross-domain

### 6.3 Validation

Post-migration:
- Zero `RELATED_TO` edges between different domains
- Every concept has exactly one `primary_domain` facet value
- No cycles in `REQUIRES` + `DEPENDS_ON` + `CONSTRAINS` per domain
- All cross-discipline edges have `confidence >=` threshold

---

## 7. Registry Update

**File:** `scripts/vitruvius/rules/relationship_registry.yaml`

The registry MUST be updated to include all predicates from §2.2, §2.3, §2.4, §2.5.

**Validation:** `scripts/vitruvius/promotion/promotion_validator.py::load_registry()` rejects any edge with an unregistered predicate.

---

## 8. Integration with Vitruvian Context

The Vitruvian Context resolver (see `02_RESOLVER_ENGINE_SPEC.md`) uses cross-discipline edges to:

1. **Filter by domain:** `primary_domain` facet restricts the search space
2. **Expand by influence:** `CONSTRAINS`, `AFFECTS`, `REQUIRES` identify downstream impacts
3. **Resolve precedence:** `REGULATED_BY` edges contribute to jurisdiction overlay resolution
4. **Trace evidence:** `SUPPORTED_BY` edges provide the reasoning chain

**Example query:**
```text
"What architectural elements are constrained by structural requirements?"
```

**Cypher:**
```cypher
MATCH (a:CanonicalNode {primary_domain: "taxonomy-architecture"})
MATCH (a)<-[:CONSTRAINS]-(s:CanonicalNode {primary_domain: "taxonomy-structural"})
RETURN a.canonical_id, a.label, s.canonical_id, s.label
```

This query uses the cross-discipline taxonomy to answer multi-disciplinary reasoning questions.
