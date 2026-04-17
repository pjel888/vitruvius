---
task: laws-tranche-15-sharding
created: 2026-04-18
status: in_progress
---

# Plan — Tranche-15 LGU sharding

1. inventory LGU materials by city / ordinance family
2. isolate exact duplicate files and raw-alias clusters
3. choose the smallest truthful first shard for tranche-15 execution
4. create a shard-specific tranche manifest only after the grouping is explicit
5. account for duplicate-readiness behavior that still flags unrelated files elsewhere in the LGU folder during shard-only scouting
