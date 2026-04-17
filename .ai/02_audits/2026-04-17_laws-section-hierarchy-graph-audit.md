---
task: laws-section-hierarchy-graph
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 Laws Section-Hierarchy Graph Audit

## Audit question
Is the current graph model sufficient for representing legal document structure such as BP220 sections/subsections?

## Verdict
**No.**

The current graph model is sufficient for:
- source nodes
- concept nodes
- relationship evidence tying sources to concepts

It is not sufficient for:
- section tree representation
- subsection hierarchy
- law-outline navigation as graph nodes

## Evidence
- BP220 currently contributes one admitted BP220-native concept file, but the source itself has ~60 extracted headers.
- The graph contract allows only `source`, `concept`, `attribute`, and `spatial_instance` nodes.
- The current snapshot contains only `source` and `concept` nodes.

## Audit recommendation
Add a new planning slice for a **laws section-hierarchy graph**.

## Safe boundary
- keep the current concept graph alive
- add hierarchy modeling additively
- do not collapse section nodes and concept nodes into one overloaded type
