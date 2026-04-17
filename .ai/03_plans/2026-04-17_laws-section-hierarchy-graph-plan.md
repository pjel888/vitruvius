---
task: laws-section-hierarchy-graph
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
supersedes: null
---

# 2026-04-17 Laws Section-Hierarchy Graph Plan

## Objective
Plan an additive graph-model extension so laws can contribute document outline structure (rules, sections, subsections, clauses) instead of only source/concept nodes.

## Why this exists
The current graph makes laws look shallower than they really are. BP220 is the clearest example:
- one admitted BP220-native concept
- many source-backed relationships to shared concepts
- ~60 detected structural headings in the refined source
- no way to materialize those headings as graph nodes

## Design intent
Add a **document-structure graph layer** that can coexist with the current concept graph.

## Proposed node classes
Candidates:
- `source_section`
- `source_subsection`
- `source_clause`

Alternative:
- one generic `source_outline_node` with level metadata

## Proposed edge classes
- `contains`
- `next_sibling`
- `governs`
- `defines`
- `references`
- `supports`

## Recommended implementation order
1. contract/model planning
2. hierarchy-node identity strategy
3. source→hierarchy extraction rules
4. bounded pilot proof for one law (likely BP220 or PD1096 IRR)
5. only then wider tranche adoption

## Acceptance criteria
- graph contract extension is explicit
- section-node identity rules are explicit
- additive compatibility with the current concept graph is preserved
- a bounded proof target is chosen before broad rollout

## Non-goals
- full implementation in this planning slice
- replacing the current source/concept graph
- generic all-laws rollout in the same change
