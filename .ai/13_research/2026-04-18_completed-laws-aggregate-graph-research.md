---
task: completed-laws-aggregate-graph
created: 2026-04-18
status: complete
---

# Research — Aggregate completed-laws graph

## Goal
Produce one curated graph input spanning all completed authoritative laws-wave lanes so the overall interconnectedness can be inspected in one place.

## Truthful boundary
The aggregate graph should include:
- completed executable lanes
- completed remediation lanes
- completed LGU shards
- completed PRC lane

It should exclude:
- residual deferred folders (`BERDE`, bills, draft-only, empty)

## Safest implementation approach
- generate one dataset manifest from the already completed manifest set
- preserve raw storage folder names where required (e.g. `HLURB-DHSUD`)
- deduplicate shared canonical sources, concepts, and relationship inputs across lanes
- keep law units distinct, including multiple `LGU` shard units with unique `law_id`s
