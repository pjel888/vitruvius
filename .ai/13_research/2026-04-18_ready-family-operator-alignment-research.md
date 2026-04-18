---
task: ready-family-operator-alignment
created: 2026-04-18
status: complete
---

# Research — ready-family operator alignment

## Goal
Align the full one-command ready-family source-to-graph operator path with the cleaner hardened build path.

## Finding
The one-command source-to-graph path appends generated promoted relationship files into a derived dataset manifest by checking only duplicate **paths**. In aggregate runs, some generated relationship files carry the same frontmatter `id` / evidence identity as relationships already present in the manifest under different paths, which reintroduces duplicate graph edges.

## Chosen remediation
Deduplicate generated relationship admissions by relationship evidence id, not just by file path. Keep the existing manifest relationship when a generated relationship file duplicates the same `rel-*` evidence identity.
