---
task: aggregate-hardening-targets
created: 2026-04-18
status: complete
---

# Plan — Aggregate hardening targets

1. add a command that combines build-report and source-to-graph summaries into ranked hardening targets
2. validate it on the combined ready-family aggregate reports
3. use that output as the next remediation selection surface
4. reduce the first hardening cluster conservatively by deriving `covers` edges from existing `Referenced Concepts` sections for currently orphan sources only
