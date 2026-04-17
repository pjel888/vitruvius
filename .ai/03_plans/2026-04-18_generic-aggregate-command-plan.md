---
task: generic-aggregate-command-path
created: 2026-04-18
status: in_progress
---

# Plan — Generic aggregate command path

1. add a generic aggregate-manifest build function and CLI command
2. add a generic aggregate graph run command that delegates to `run-dataset-source-to-graph`
3. keep the laws command as a thin wrapper over the generic surface
4. add focused tests proving the generic path works and does not regress the laws MVP
