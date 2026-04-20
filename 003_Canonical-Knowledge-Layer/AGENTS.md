<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-20 -->

# 003_Canonical-Knowledge-Layer

## Purpose
Trusted, curated knowledge pages. This is the canonical working layer for source documents, concepts, and relationships. Raw materials are evidence; canonical materials are the trusted working layer.

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| `001-Laws/` through `009-Practice/` | Domain-specific canonical knowledge |
| `shared/concepts/` | Cross-domain shared concept pages |
| `shared/relationships/` | Cross-domain relationship records |
| `shared/sources/` | Cross-domain canonical source pages |

## For AI Agents

### Working In This Directory
- **Canonical materials are the trusted working layer.** Do not silently redefine truth in derived artifacts.
- **Content trust order:** Canonical > Raw Conversion > Raw Source.
- **Frontmatter is required** on all canonical pages (`id`, `title`, `canonical_status`).
- **Relationship records** must use `rel-` prefixed IDs and `canonical_status` of `promoted` or `verified` to appear in graphs.
- **Do not mutate raw source files.** Raw sources live in `001_Raw-Source-Layer/`; canonical sources live here.

### Testing Requirements
- Run canonical rule tests after adding or modifying canonicalization rules.
- Verify graph build passes with zero warnings after admitting new sources or relationships.

### Common Patterns
- One concept per file in `shared/concepts/`.
- One relationship per file in `shared/relationships/`.
- Sources are organized by domain folder (`001-Laws/`, etc.) or `shared/sources/`.
- Use `scripts/pipeline_cli.py build-graph --dataset-manifest ...` to verify graph health after changes.
