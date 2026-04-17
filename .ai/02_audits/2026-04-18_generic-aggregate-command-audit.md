---
task: generic-aggregate-command-path
created: 2026-04-18
status: complete
---

# Audit — Generic aggregate command path

## Reality check
The helper extraction is necessary but not sufficient. Without a generic operator path, the orchestration remains laws-shaped even if some code is shared.

## Safe scope
- add a generic aggregate-manifest command path first
- then keep the laws command as a specialization/wrapper
- avoid changing the current laws MVP behavior while introducing the new generic surface
