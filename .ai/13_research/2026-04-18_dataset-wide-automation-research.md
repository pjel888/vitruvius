---
task: dataset-wide-automation-mvp
created: 2026-04-18
status: complete
---

# Research — Dataset-wide automation MVP

## Position of this note

This is a **narrow next-step strategy note**.

It should be read together with:

- `/.ai/13_research/2026-04-18_dataset-family-workflow-and-graph-stack-analysis.md`

Use that companion note for:

- the larger parent goal
- the repeatable bounded-lane workflow
- the technical stack
- the laws-wave as the strongest current reference implementation
- the role of `ready-family-aggregate`
- the current artifact-stack pattern

Use **this** note for the narrower question:

- how to lift the already-proven family/laws pattern into a more generic
  dataset-wide automation MVP

## Goal
Generalize the laws-wave automation pattern so dataset-to-knowledge-graph execution is not special-cased to laws only.

## Current reusable pieces
Already reusable:
- `run-dataset-source-to-graph`
- manifest-driven graph execution
- machine-readable completed/disposition/provenance ledgers
- artifact indices and reload protocol pattern

Currently laws-specific:
- completed-lanes ledger schema and aggregate-manifest synthesis logic
- residual defer/disposition policy rules
- law-centric source-quality expectations and benchmark hints

## MVP direction
Build a generic automation layer that can:
1. define a dataset scope via machine-readable ledgers
2. synthesize an aggregate manifest from completed lane manifests
3. exclude deferred/non-authoritative items automatically
4. run one command to produce a graph for the trusted subset

## Why this is the right next step
The laws wave proved the pattern. The next leverage point is not more manual curation, but lifting the pattern into a generic dataset automation framework.

## In one sentence

If `dataset-family-workflow-and-graph-stack-analysis.md` explains **what we are
doing and how the current system works**, this note explains **what we should
generalize next**.
