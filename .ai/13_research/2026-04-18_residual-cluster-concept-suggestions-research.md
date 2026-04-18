---
task: residual-cluster-concept-suggestions
created: 2026-04-18
status: complete
---

# Research — residual cluster concept suggestions

## Goal
Create a deterministic operator surface that suggests missing concept scaffold candidates from refined source text so the remaining orphan/partial laws can be advanced without inventing stronger relationships.

## Rationale
The residual laws are not blocked by source quality. They are blocked because the current concept inventory does not contain obvious domain terms like ADR / mediation / arbitration / hazardous wastes / master plumber. A suggestion surface is a safe next automation step because it does not directly mutate graph truth.

## Chosen scope
- inspect refined markdown text
- extract explicit definition-style terms (`X means`, quoted terms, definition bullets)
- compare them to the current shared concept inventory
- report matched vs unmatched candidate concepts
