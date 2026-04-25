---
task: aec-mepfs-backbone
phase: readiness-taxonomy-decision
created: 2026-04-25
author: CODEX
status: ACCEPTED-READINESS-CONTROL
---

# Master Taxonomy L1/L2 Decision Record

## Decision

Use a bounded hybrid as the first AEC-MEPFS Backbone planning candidate, with
the 18-domain proposal reduced where locked taxonomy decisions already govern
home-domain assignment.

Accepted-readiness scope: this L1/L2 record is accepted as the first-slice
planning candidate and implementation guardrail. It does not admit canonical
nodes. L1/L2 admission still requires steward approval, independent review, and
the locked-decision reconciliation gates already named in this record.

This record does not override `.ai/03_plans/taxonomy-governance/00_locked_decisions.md`.
In particular, LD-10 controls accessibility, fire/life safety, sustainability,
and security/hardening home-domain assignment until a formal override exists.

`HIS` and `FIG` are auxiliary knowledge-commons domains and do not become
first-slice compliance truth homes.

The larger AECMEPFS++ tree is accepted only as candidate authoring material for
later L2/L3 proposals, not as canonical structure.

## Rationale

The 18-domain proposal is broad enough to cover AEC-MEPFS without copying a
standards vendor taxonomy, but it cannot be imported literally where locked
decisions already assign home domains. The larger AECMEPFS++ tree is useful but
too expansive to import before steward ownership, source rights, review queues,
and resolver golden cases exist.

## Rejected Options

| Option | Decision | Reason |
|---|---|---|
| Import the full AECMEPFS++ tree | rejected | Too broad, source/version claims not verified, risks canonicalizing research output |
| Use one published standard as the backbone | rejected | Creates licensing and jurisdiction bias; external standards should be mapped references |
| Keep document-derived law graph as primary taxonomy | rejected | Repeats current fragmentation and does not create concept-first AEC organization |
| 18-domain envelope with bounded L2 seed | accepted with LD-10 reductions | Gives stable homes while allowing typed graph edges and overlays, but accessibility, sustainability, and security/hardening follow locked home-domain rules |

## Candidate L1 Review Set

| Code | L1 domain | First-slice role |
|---|---|---|
| `ARC` | Architecture | primary operational domain |
| `ACC` | Accessibility And Universal Design | locked subject-specific domain from LD-10 |
| `URB` | Urban Planning And Land Use | primary operational domain |
| `CIV` | Civil Engineering | primary operational domain |
| `STR` | Structural Engineering | primary operational domain |
| `GEO` | Geotechnical And Geospatial | primary operational domain |
| `MEC` | Mechanical Systems | primary MEPFS domain |
| `ELE` | Electrical And Low-Voltage Systems | primary MEPFS domain |
| `PLS` | Plumbing And Sanitary Systems | primary MEPFS domain |
| `FLS` | Fire And Life Safety | primary MEPFS domain |
| `CON` | Construction Methods And Delivery | primary operational domain |
| `MAT` | Materials And Products | primary operational domain |
| `COM` | Codes, Compliance, And Permitting | cross-domain governance domain |
| `PER` | Performance And Resilience | cross-domain performance domain, including security/hardening under LD-10 |
| `SUS` | Sustainability, Energy, And Carbon | locked subject-specific domain from LD-10 |
| `DIG` | Digital Delivery And Information Management | digital/BIM domain |
| `OPS` | Operations, Maintenance, And Facilities | lifecycle domain |
| `HIS` | History, Theory, And Movements | auxiliary knowledge-commons domain |
| `FIG` | People, Firms, And Works | auxiliary knowledge-commons domain |

`HIS` and `FIG` may support discovery, education, precedent, and background
context. They must not own legal, compliance, or resolver truth in the first
slice.

## First L2 Review Set

The first L2 review set is intentionally shallow. It gives every candidate L1 a
reviewable starting shape without pretending to finish the entire discipline
tree.

| L1 | L2 candidates for first-slice review |
|---|---|
| `ARC` | building typologies; spatial planning; envelope; architectural documentation; design coordination |
| `ACC` | accessible routes; barrier-free facilities; universal design; assistive features; accessibility compliance |
| `URB` | zoning; land-use planning; site planning; public realm; subdivision controls |
| `CIV` | roads and circulation; drainage; utilities coordination; earthworks; site development |
| `STR` | structural systems; loads and actions; foundations interface; seismic design; structural materials |
| `GEO` | geohazards; topography; soils; surveying; geospatial reference |
| `MEC` | ventilation; air-conditioning; elevators/escalators; mechanical plant; smoke control interface |
| `ELE` | power distribution; lighting; emergency power; communications; controls |
| `PLS` | water supply; sanitary drainage; storm drainage; fixtures; wastewater |
| `FLS` | fire protection; detection and alarm; egress; compartmentation; fire department access |
| `CON` | procurement; sequencing; temporary works; quality control; construction safety |
| `MAT` | concrete; steel; timber; masonry; finishes and product data |
| `COM` | permits; legal hierarchy; inspections; occupancy; professional responsibility |
| `PER` | acoustics; indoor environmental quality; security and hardening; resilience; maintainability |
| `SUS` | energy; water efficiency; emissions; resource efficiency; sustainability rating context |
| `DIG` | BIM schemas; classification systems; model exchange; information requirements; asset data |
| `OPS` | commissioning; maintenance; asset registers; inspection cycles; facility operations |
| `HIS` | architectural history; movements; precedents; conservation context; theory |
| `FIG` | architects; engineers; builders; firms; works and projects |

## Node Classes

First-slice authoring distinguishes these classes:

- `BackboneNode`
- `CanonicalConcept`
- `AuthorityDocumentFamily`
- `AuthorityDocumentEdition`
- `DocumentVersion`
- `EvidenceSpan`
- `Overlay`
- `StandardReference`
- `Jurisdiction`
- `StandardMapping`

Documents, rules, chunks, and evidence attach through assertions/edges. They do
not become large metadata blobs on backbone nodes.

## Canonical Rules

- Every canonical concept has exactly one primary home.
- Secondary placement is represented through typed graph edges, not duplicate
  canonical nodes.
- Jurisdictional meaning is represented through overlays and applicability
  rules, not mutated canonical nodes.
- External standard codes are mappings, not Vitruvius identity.
- L1/L2 nodes are human-locked and require steward approval plus two-human
  review before admission.

## Facets

Facets are orthogonal to the L1/L2 tree:

- lifecycle: planning, design, permitting, procurement, construction,
  commissioning, operations, renovation, demolition
- asset type: building, site, infrastructure, district, component, system,
  product, document
- performance topic: safety, accessibility, energy, water, durability,
  resilience, constructability, maintainability
- geography/jurisdiction: global, country, region, province, city/municipality,
  barangay/site, project
- knowledge type: concept, standard, law, rule, method, person, work, evidence
- standards context: ISO, buildingSMART, Uniclass, CSI, ICC, NFPA, ASCE,
  Eurocode, Philippines authority, local ordinance

Cardinality:

- primary domain: exactly one
- knowledge type: exactly one
- lifecycle, asset, performance, project type, and standards context: zero or
  more
- jurisdiction: overlay/applicability only, never canonical node identity

## Predicate Families For First Slice

- `broader_than` / `narrower_than`
- `part_of`
- `governs`
- `requires`
- `constrains`
- `maps_to_external_standard`
- `applicable_in_jurisdiction`
- `has_facet`
- `conflicts_with`
- `supersedes`
- `evidenced_by`

`related_to` is allowed only as a temporary review-state relationship. It is not
admitted as a governed first-slice predicate because vague predicates would
recreate the current shallow graph problem.

Each predicate must be registered in the later relationship schema before
runtime implementation starts.

See `relationship-predicate-registry-draft.md` for the readiness-stage registry
draft. The draft is not the runtime registry; it is a gate that prevents
implementation from inventing predicates or promoting vague review-state edges.

## ID Policy

Use `VTN-<kind>-<7 digits>`.

First-slice kind codes:

- `DOM` - L1-L4 domain/backbone node
- `CON` - canonical concept
- `RUL` - rule
- `DEF` - definition
- `PRO` - procedure
- `EXC` - exception
- `JUR` - jurisdiction
- `AUT` - authority
- `ADF` - authority document family
- `ADE` - authority document edition
- `APP` - applicability rule
- `OVR` - overlay
- `STD` - standard reference
- `MAP` - standard mapping
- `LOC` - localization
- `REL` - taxonomy release

Example only: `VTN-DOM-0000001` for the first admitted L1 domain. Actual IDs are
assigned by the canonical authoring workflow, not by this decision record.

This record does not introduce new kind values. The list above mirrors the
locked kind set in `.ai/03_plans/taxonomy-governance/00_locked_decisions.md`.

## Historical Failure Constraints

Prior KG audits showed that the 001-Laws Explorer graph was structurally valid
but semantically thin: most assertions were `DEFINED_BY` and `SUPPORTED_BY`, with
very few concept-to-concept semantic relationships. The first-slice taxonomy must
therefore treat source provenance, rule evidence, concept hierarchy, facets, and
cross-domain semantics as separate relationship classes.

Document-derived titles, source slugs, and legacy shared-taxonomy roots are
migration evidence only. They do not become canonical concept names or L1/L2
structure without authoring review.

## Deferred Decisions

- Full L3/L4 expansion is deferred until authoring templates and review queues
  exist.
- History/people/works stay auxiliary in the first slice and must not become
  compliance-rule homes.
- Sanitary systems are included under `PLS` for MVP clarity, with cross-links to
  public health and code compliance.
- A standalone `SEC` L1 is not admitted in this record. Security/hardening is
  assigned under `PER` unless a later ADR formally overrides LD-10.
- Accessibility and sustainability are split out from the original 18-domain
  proposal because LD-10 already assigns them subject-specific homes.
- Jurisdiction-specific code sections are overlays, not L2 taxonomy children.

## Current Shared-Taxonomy Migration Annex

The current 11-root shared taxonomy remains an MVP surface until migrated. A
later migration workbook must map each existing root to:

- exact target L1/L2
- broader target
- narrower target
- split target
- deprecated/no-safe-match

No current shared taxonomy root is automatically canonical in the AEC-MEPFS
Backbone.

## Pass / Fail Gate

Pass:

- the first L1/L2 review set above is treated as the candidate set for the first
  implementation slice
- the AECMEPFS++ tree remains proposal material
- facets and overlays are not encoded as duplicate discipline branches
- LD-10 home-domain rules remain controlling unless a formal override exists

Fail:

- any implementation invents a new L1 without steward review
- any document-derived title becomes a canonical taxonomy node by default
- any external standard code becomes the Vitruvius primary ID
- any implementation admits a standalone `SEC` L1, folds accessibility under
  `ARC`, or folds sustainability into `PER` without a formal LD-10 override
