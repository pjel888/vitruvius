# 16 — Source-Backed Lower Node Types

## Why these node types should be source-backed

The current graph has many Concept nodes but zero Rule, Definition, Procedure, Exception, Evidence, and Document nodes. These types are powerful, but risky if generated carelessly.

Every node of these types should be backed by at least one accepted resource.

## Definition nodes

A Definition node captures a formal or semi-formal definition.

Requirements:

- must link to at least one source with relationship `defines` or `is_primary_reference_for`,
- avoid overly generic definitions,
- indicate whether definition is domain-specific or jurisdiction/context-specific.

Example:

```text
Definition: Load path definition
Defines: Load Path
Source link: structural textbook/professional guidance
Rationale: Defines load path as the route by which forces are transferred through structural elements to supports/foundations.
```

## Rule nodes

A Rule node captures a constraint, requirement, code-like provision, professional rule-of-thumb, or design criterion.

Requirements:

- must have primary/high-authority source,
- must include jurisdiction/context when code-like,
- must include confidence and review status,
- should be human-reviewed if safety/legal/compliance-critical.

Avoid turning general advice into universal rules, creating rules from blogs, copying code text, or ignoring edition/year.

## Procedure nodes

A Procedure node captures a workflow or method.

Requirements:

- must have source with relationship `provides_procedure`, `provides_analysis_method`, or equivalent,
- should include lifecycle phase,
- should include inputs/outputs if schema supports.

Examples: site survey procedure, geotechnical investigation process, structural analysis workflow, concrete pour and curing procedure, retaining wall inspection procedure, and local corpus source verification process.

## Exception nodes

An Exception node captures a caveat, alternate case, exception, or conditional variation.

Requirements:

- must link to source explaining the exception,
- must identify context/jurisdiction when relevant,
- should connect to the Rule/Concept it qualifies.

## Evidence nodes

An Evidence node captures a source-backed claim or finding.

Requirements:

- must link to academic paper, technical report, professional study, dataset, or verified local evidence source,
- should include claim summary,
- should include strength/limitations if supported,
- should not be used for generic explanatory links.

## Document nodes

A Document node represents an important source as a graph object.

Create when a Resource is reused across many nodes, central to a discipline, is a standard/guideline/manual/book/report, supports multiple definitions/rules/procedures/evidence nodes, and has enough metadata to identify reliably.

Do not create Document nodes for every random webpage, low-quality source, duplicate, unsupported candidate, or resource with missing title/identity.

## Lower node creation workflow

```text
Source discovered
  → resource verified
  → node relationship identified
  → Kimi review if important
  → create lower node only if it adds reasoning value
  → link lower node to parent Concept/Rule/etc.
  → link lower node to Resource
  → validate
```

## Example graph patterns

Definition:

```text
Definition node --defines--> Concept node
Definition node --supported_by--> Resource
```

Rule:

```text
Rule node --constrains--> Concept node
Rule node --governed_by/source_link--> Resource
Rule node --has_exception--> Exception node
```

Procedure:

```text
Procedure node --applies_to--> Concept node
Procedure node --requires_input--> Concept/Document node
Procedure node --produces_output--> Evidence/Document node
Procedure node --provided_by/source_link--> Resource
```

Evidence:

```text
Evidence node --supports--> Concept/Rule/Edge
Evidence node --provided_by--> Resource
Evidence node --has_limitation--> Exception/Caveat node
```

Document:

```text
Document node --represented_by--> Resource
Document node --supports--> Concept/Rule/Procedure/Evidence
Document node --classified_by--> SourceFamily / classification mapping
```

## First recommended lower-node batches

After resource infrastructure works, create:

1. Definitions for 10 high-centrality Architecture/Civil/Structural concepts.
2. Procedures for 5 design/construction processes.
3. Evidence nodes for 5 research/professional claims.
4. Document nodes for 5 repeated high-authority sources.
5. Rule nodes only where primary source and jurisdiction/context are clear.
