# 04 — Node Resource Linking Strategy

## Core idea

A source link is not merely “related to” a node. It should have a clear function.

For each node-resource pair, record:

- what the resource does for the node,
- why it is relevant,
- how authoritative it is,
- whether it is local or online,
- whether the relationship is verified,
- where in the resource the relevant material appears.

## Relationship types

| Relationship | Use when |
|---|---|
| `defines` | The source gives a formal/semi-formal definition. |
| `explains` | The source explains the concept generally. |
| `governs` | The source is a standard/code/rule authority. |
| `supports` | The source supports a claim but is not necessarily primary. |
| `provides_procedure` | The source describes a process/workflow/procedure. |
| `provides_evidence` | The source provides empirical/research/professional evidence. |
| `provides_example` | The source gives examples/case studies. |
| `provides_classification` | The source classifies or maps the concept. |
| `provides_design_guidance` | The source guides design decisions. |
| `provides_construction_guidance` | The source guides construction/installation. |
| `provides_analysis_method` | The source describes calculation/analysis methods. |
| `provides_maintenance_guidance` | The source covers O&M/inspection/maintenance. |
| `is_primary_reference_for` | The strongest source for the node. |
| `is_supplementary_reference_for` | Helpful but not primary. |
| `is_local_reference_for` | Local file is relevant to the node. |

## Node-type-specific linking

### Concept node

Recommended source mix:

- one definition or classification source,
- one professional/textbook/source-family reference,
- one practical design/construction source,
- optional academic/evidence source,
- optional local source.

Example:

```text
Node: Retaining Wall
Resources:
- geotechnical/structural textbook: explains
- professional design guide: provides_design_guidance
- local retaining wall PDF: is_local_reference_for
- academic paper on wall drainage/failure: provides_evidence
```

### Definition node

Must link to sources that justify the definition. Avoid vague web definitions when a professional or official source is available.

### Rule node

Requires primary or high-authority source. Include jurisdiction/context, source type, caveat if project-dependent, and avoid universal wording unless truly general.

### Procedure node

Should link to sources that describe steps or workflows, such as structural analysis procedures, site surveys, concrete curing, inspections, and source verification processes.

### Exception node

Should link to a source explaining the caveat/exception/conditional case.

### Evidence node

Should link to evidence-bearing resources: DOI paper, technical report, field study, professional research report, or verified local evidence source.

### Document node

Should link to Resource metadata and to concepts the document supports. A Document node is a graph entity; a Resource is the file/metadata record.

## Link creation workflow

1. Select node.
2. Gather canonical name, aliases, taxonomy, parent topic/subtopic, description, related nodes, and edge context.
3. Generate search queries.
4. Search local corpus first.
5. Search curated source families.
6. Search APIs.
7. Normalize and dedupe candidates.
8. Score preliminary relevance.
9. Run verification checks.
10. Ask Kimi to review high-scoring candidates.
11. Accept only strong candidates.
12. Store `NodeResourceLink` with rationale.
13. Update metrics.

## Query generation examples

For `Accessible Route`:

```text
"accessible route" architecture design guidance
"accessible route" building design standard
"accessible route" slope clearance threshold
"accessible route" site grading building entrance
"barrier free route" architecture accessibility guidance
```

For `Retaining Wall`:

```text
"retaining wall" lateral earth pressure drainage design guide
"retaining wall" geotechnical engineering textbook
"retaining wall" backfill drainage failure evidence
"retaining structure" civil engineering guidance
```

For `Load Path`:

```text
"load path" structural engineering building design
"load transfer path" structural frame foundation
"load path" diaphragm shear wall foundation
"structural load path" design guidance
```

## Rationale writing

Good rationale:

```text
Explains how retaining walls resist lateral earth pressure and why drainage/backfill conditions are important to wall stability.
```

Bad rationale:

```text
Mentions retaining walls.
```

## Diversity rule

A good sidebar should not show five near-identical sources from the same domain.

For high-priority nodes, prefer a spread:

- official/professional guidance,
- textbook/handbook,
- local document,
- academic/evidence source,
- classification/ontology mapping where useful.

## Avoid source pollution

Reject candidates when:

- title/metadata does not match,
- source is too general,
- source is an SEO/blog page with no professional value,
- link is broken,
- source is a duplicate,
- source is likely pirated,
- source lacks context for a code/regulatory claim,
- source is product-specific but node is generic,
- source overclaims or contradicts known domain context.
